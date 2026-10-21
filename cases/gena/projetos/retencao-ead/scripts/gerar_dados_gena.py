#!/usr/bin/env python3
"""Gera a primeira melhoria de dados fictícios do GENA.

O módulo não executa geração ao ser importado. Use ``generate`` para gerar os
CSV e o manifesto ou execute este arquivo pela linha de comando.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Any, Iterable, Mapping


ALLOWED_VERSIONS = {"1.0.0"}
SNAPSHOT = date(2025, 12, 31)
SIGNAL_CUTOFF = date(2025, 2, 28)
OPENING_START = date(2025, 1, 1)

ALUNOS_FIELDS = [
    "student_id",
    "curso",
    "polo",
    "data_admissao",
    "tipo_coorte",
    "simulado",
]

MATRICULAS_FIELDS = [
    "matricula_id",
    "student_id",
    "curso",
    "polo",
    "data_inicio",
    "status_final",
    "data_saida",
    "tipo_coorte",
    "pertencente_abertura",
    "elegivel_churn",
    "motivo_saida",
    "simulado",
]

FINANCEIRO_FIELDS = [
    "titulo_id",
    "matricula_id",
    "competencia",
    "vencimento",
    "valor_devido_centavos",
    "valor_pago_centavos",
    "data_pagamento",
    "saldo_aberto_centavos",
    "posicao_financeira2025-12-31",
    "simulado",
]

ENGAJAMENTO_FIELDS = [
    "matricula_id",
    "semana_inicio",
    "semana_fim",
    "dias_com_acesso",
    "atividades_previstas",
    "atividades_entregues",
    "origem_simulada",
    "simulado",
]

NPS_FIELDS = [
    "resposta_id",
    "matricula_id",
    "data_pesquisa",
    "nota",
    "classificacao_nps",
    "simulado",
]

REFERENCIAS_FIELDS = [
    "segmento",
    "ativos_2024",
    "ativos_2025",
    "ticket_centavos",
    "churn_percentual_referencia",
    "inadimplencia_percentual_referencia",
    "nps_referencia",
    "simulado",
]

CSV_NAMES = [
    "alunos_ead.csv",
    "matriculas_ead.csv",
    "financeiro_ead.csv",
    "engajamento_semanal_ead.csv",
    "pesquisa_nps_ead.csv",
    "referencias_segmentos.csv",
]

GRANULARIDADES = {
    "alunos_ead.csv": "uma linha por aluno sintético EAD (3970 linhas)",
    "matriculas_ead.csv": "uma linha por matrícula sintética, uma por aluno (3970 linhas)",
    "financeiro_ead.csv": "uma linha por título mensal de 2025, no máximo 12 por matrícula",
    "engajamento_semanal_ead.csv": "uma linha por matrícula da abertura de 2025 e semana de sinal; 8 semanas",
    "pesquisa_nps_ead.csv": "uma linha por resposta NPS sintética; amostra distinta de alunos ativos no fechamento",
    "referencias_segmentos.csv": "uma linha agregada por segmento de referência, sem entidades individuais",
}


class ConfigError(ValueError):
    """Indica uma configuração incompatível com as equações da base."""


def _bool(value: bool) -> str:
    return "true" if value else "false"


def _sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _namespace_rng(seed: int, namespace: str) -> random.Random:
    """Cria um RNG estável e independente para um namespace da semente."""
    material = f"{seed}:{namespace}".encode("utf-8")
    digest = hashlib.sha256(material).digest()
    return random.Random(int.from_bytes(digest[:16], "big"))


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ConfigError(message)


def _int_value(mapping: Mapping[str, Any], key: str) -> int:
    value = mapping.get(key)
    _require(isinstance(value, int) and not isinstance(value, bool), f"configuração inválida: {key} deve ser inteiro")
    return value


def _validate_config(config: Mapping[str, Any]) -> None:
    version = config.get("versao")
    _require(version in ALLOWED_VERSIONS, f"versao não suportada: {version!r}")
    _require(config.get("ano_referencia") == 2025, "ano_referencia deve ser 2025")
    _require(config.get("snapshot") == "2025-12-31", "snapshot deve ser 2025-12-31")
    _require(config.get("data_corte_sinais") == "2025-02-28", "data_corte_sinais deve ser 2025-02-28")
    seed = config.get("semente")
    _require(isinstance(seed, int) and not isinstance(seed, bool), "semente deve ser inteiro")

    ead = config.get("ead")
    _require(isinstance(ead, dict), "configuração ead ausente ou inválida")
    opening = _int_value(ead, "populacao_abertura")
    conclusions = _int_value(ead, "conclusoes_coorte_abertura")
    transfers = _int_value(ead, "transferencias_coorte_abertura")
    eligible = _int_value(ead, "populacao_elegivel_churn")
    churn = _int_value(ead, "saidas_churn")
    retained = _int_value(ead, "retidos_coorte_abertura")
    new = _int_value(ead, "novas_matriculas")
    closing = _int_value(ead, "ativos_fechamento")
    nps_responses = _int_value(ead, "nps_respostas")
    promoters = _int_value(ead, "nps_promotores")
    passives = _int_value(ead, "nps_passivos")
    detractors = _int_value(ead, "nps_detratores")

    _require(opening > 0 and new >= 0, "populações devem ser não negativas e a abertura positiva")
    _require(eligible > 0 and min(conclusions, transfers, churn, retained, closing) >= 0, "populações inválidas ou denominador acadêmico nulo")
    _require(eligible == opening - conclusions - transfers, "elegibilidade deve excluir conclusões e transferências")
    _require(churn + retained == eligible, "churn mais retidos deve igualar a população elegível")
    _require(closing == retained + new, "ativos no fechamento deve igualar retidos mais ingressantes")
    _require(opening + new == closing + conclusions + transfers + churn, "equação da população total incompatível")
    _require(nps_responses == promoters + passives + detractors, "categorias NPS não somam as respostas")
    _require(nps_responses > 0 and promoters >= 0 and passives >= 0 and detractors >= 0, "contagens NPS inválidas")

    _require(isinstance(ead.get("polos"), list) and ead["polos"], "polos devem ser uma lista não vazia")
    _require(isinstance(ead.get("cursos"), list) and ead["cursos"], "cursos devem ser uma lista não vazia")
    _require(_int_value(ead, "semanas_sinais_abertura") == 8, "semanas_sinais_abertura deve ser 8")
    ticket = _int_value(ead, "ticket_mensal_centavos")
    _require(ticket > 0, "ticket_mensal_centavos deve ser positivo")
    target = Decimal(str(ead.get("inadimplencia_monetaria_alvo")))
    _require(Decimal("0") <= target <= Decimal("1"), "inadimplencia_monetaria_alvo deve ser uma fração entre 0 e 1")

    references = config.get("segmentos_referencia")
    _require(isinstance(references, list), "segmentos_referencia deve ser uma lista")
    _require(len(references) == 4 and len({row.get("segmento") for row in references}) == 4, "são necessárias quatro referências de segmentos distintas")
    ead_reference = next((row for row in references if row.get("segmento") == "Graduacao EAD"), None)
    _require(ead_reference is not None, "segmento Graduacao EAD ausente nas referências")
    _require(int(ead_reference["ativos_2024"]) == opening and int(ead_reference["ativos_2025"]) == closing, "fotografias EAD não fecham com abertura e fechamento")
    _require(Decimal(str(ead_reference["inadimplencia_percentual_referencia"])) == target * 100, "posição financeira EAD não fecha com a referência")
    reference_churn = Decimal(str(ead_reference["churn_percentual_referencia"]))
    calculated_churn = (Decimal(churn) * Decimal("100")) / Decimal(eligible)
    _require(calculated_churn == reference_churn, "percentual de churn não fecha com a população elegível")
    reference_nps = int(ead_reference["nps_referencia"])
    calculated_nps = (Decimal(promoters - detractors) * Decimal("100")) / Decimal(nps_responses)
    _require(calculated_nps == Decimal(reference_nps), "NPS de referência não fecha com as categorias")
    _require(int(ead_reference["ticket_centavos"]) == ticket, "ticket EAD não fecha com a referência")


def _read_config(config_path: Path) -> tuple[dict[str, Any], bytes]:
    config_bytes = config_path.read_bytes()
    config = json.loads(config_bytes.decode("utf-8"))
    _require(isinstance(config, dict), "configuração deve ser um objeto JSON")
    _validate_config(config)
    return config, config_bytes


def _write_csv(path: Path, fields: list[str], rows: Iterable[Mapping[str, Any]]) -> int:
    """Escreve CSV UTF-8, separado por vírgula e com LF, sem valores implícitos."""
    count = 0
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
            delimiter=",",
            lineterminator="\n",
            extrasaction="raise",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})
            count += 1
    return count


def _round_half_up_fraction(value: Decimal) -> int:
    return int(value.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def _build_students(config: Mapping[str, Any]) -> tuple[list[dict[str, str]], dict[str, dict[str, str]]]:
    ead = config["ead"]
    opening = int(ead["populacao_abertura"])
    new_count = int(ead["novas_matriculas"])
    courses = [str(item) for item in ead["cursos"]]
    polos = [str(item) for item in ead["polos"]]
    seed = int(config["semente"])
    structural_rng = _namespace_rng(seed, "estrutura_alunos")

    admission_years = [2022] * (opening // 3) + [2023] * (opening // 3) + [2024] * (opening - 2 * (opening // 3))
    structural_rng.shuffle(admission_years)
    people: dict[str, dict[str, str]] = {}

    for ordinal in range(1, opening + new_count + 1):
        student_id = f"ALU{ordinal:06d}"
        curso = structural_rng.choice(courses)
        polo = structural_rng.choice(polos)
        if ordinal <= opening:
            admission_year = admission_years[ordinal - 1]
            admission_date = date(admission_year, 1, 1)
            tipo_coorte = "abertura_2025"
        else:
            entry_month = structural_rng.randint(3, 11)
            admission_date = date(2025, entry_month, 1)
            tipo_coorte = "ingressante_2025"
        people[student_id] = {
            "student_id": student_id,
            "curso": curso,
            "polo": polo,
            "data_admissao": admission_date.isoformat(),
            "tipo_coorte": tipo_coorte,
            "simulado": "true",
        }

    rows = [people[key] for key in sorted(people)]
    return rows, people


def _build_matriculas(
    config: Mapping[str, Any], people: Mapping[str, Mapping[str, str]]
) -> tuple[list[dict[str, str]], dict[str, str]]:
    ead = config["ead"]
    opening = int(ead["populacao_abertura"])
    conclusions = int(ead["conclusoes_coorte_abertura"])
    transfers = int(ead["transferencias_coorte_abertura"])
    churn_count = int(ead["saidas_churn"])
    student_ids = sorted(people)
    opening_ids = student_ids[:opening]
    opening_2022 = [sid for sid in opening_ids if people[sid]["data_admissao"].startswith("2022-")]
    _require(len(opening_2022) >= conclusions, "não há alunos de 2022 suficientes para as conclusões")

    seed = int(config["semente"])
    outcome_rng = _namespace_rng(seed, "desfechos")
    outcome_rng.shuffle(opening_2022)
    concluded = set(opening_2022[:conclusions])

    remaining_after_conclusion = [sid for sid in opening_ids if sid not in concluded]
    outcome_rng.shuffle(remaining_after_conclusion)
    transferred = set(remaining_after_conclusion[:transfers])
    eligible = [sid for sid in remaining_after_conclusion if sid not in transferred]
    _require(len(eligible) == int(ead["populacao_elegivel_churn"]), "elegibilidade calculada diverge da configuração")
    outcome_rng.shuffle(eligible)
    canceled = set(eligible[:churn_count])
    retained = set(eligible[churn_count:])
    _require(len(retained) == int(ead["retidos_coorte_abertura"]), "retenção calculada diverge da configuração")

    exiting = concluded | transferred | canceled
    exit_rng = _namespace_rng(seed, "datas_saida")
    exit_dates: dict[str, str] = {}
    for student_id in sorted(exiting):
        month = exit_rng.randint(4, 12)
        day = exit_rng.randint(15, 28)
        exit_dates[student_id] = date(2025, month, day).isoformat()

    reason_pool = ["financeiro", "academico", "pessoal", "nao_informado"]
    repeated_reasons = (reason_pool * ((len(canceled) + len(reason_pool) - 1) // len(reason_pool)))[: len(canceled)]
    reason_rng = _namespace_rng(seed, "motivos_cancelamento")
    reason_rng.shuffle(repeated_reasons)
    cancel_reasons = dict(zip(sorted(canceled), repeated_reasons))

    status: dict[str, str] = {}
    for sid in concluded:
        status[sid] = "concluido"
    for sid in transferred:
        status[sid] = "transferido"
    for sid in canceled:
        status[sid] = "cancelado"
    for sid in retained:
        status[sid] = "ativo"
    new_ids = student_ids[opening:]
    for sid in new_ids:
        status[sid] = "ativo"

    matricula_by_student: dict[str, str] = {}
    rows: list[dict[str, str]] = []
    for ordinal, student_id in enumerate(student_ids, start=1):
        person = people[student_id]
        matricula_id = f"MAT{ordinal:06d}"
        matricula_by_student[student_id] = matricula_id
        is_opening = student_id in opening_ids
        data_inicio = OPENING_START if is_opening else date.fromisoformat(person["data_admissao"])
        final_status = status[student_id]
        rows.append(
            {
                "matricula_id": matricula_id,
                "student_id": student_id,
                "curso": person["curso"],
                "polo": person["polo"],
                "data_inicio": data_inicio.isoformat(),
                "status_final": final_status,
                "data_saida": exit_dates.get(student_id, ""),
                "tipo_coorte": person["tipo_coorte"],
                "pertencente_abertura": _bool(is_opening),
                "elegivel_churn": _bool(student_id in eligible),
                "motivo_saida": cancel_reasons.get(student_id, ""),
                "simulado": "true",
            }
        )

    _require(len(concluded) == conclusions, "quantidade de conclusões inválida")
    _require(len(transferred) == transfers, "quantidade de transferências inválida")
    _require(len(canceled) == churn_count, "quantidade de cancelamentos inválida")
    _require(sum(row["status_final"] == "ativo" for row in rows) == int(ead["ativos_fechamento"]), "ativos finais inválidos")
    _require(sum(row["elegivel_churn"] == "true" for row in rows) == int(ead["populacao_elegivel_churn"]), "elegibilidade final inválida")
    return rows, matricula_by_student


def _build_engajamento(config: Mapping[str, Any], matriculas: Iterable[Mapping[str, str]]) -> list[dict[str, str]]:
    opening_matriculas = [row for row in matriculas if row["pertencente_abertura"] == "true"]
    opening_matriculas.sort(key=lambda row: row["matricula_id"])
    seed = int(config["semente"])
    engagement_rng = _namespace_rng(seed, "engajamento_semanal")
    rows: list[dict[str, str]] = []
    starts = [date(2025, 1, 6) + timedelta(days=7 * index) for index in range(8)]
    for matricula in opening_matriculas:
        for start in starts:
            end = min(start + timedelta(days=6), SIGNAL_CUTOFF)
            actual_days = (end - start).days + 1
            dias = engagement_rng.randint(0, min(7, actual_days))
            previstas = engagement_rng.randint(1, 12)
            entregues = engagement_rng.randint(0, previstas)
            rows.append(
                {
                    "matricula_id": matricula["matricula_id"],
                    "semana_inicio": start.isoformat(),
                    "semana_fim": end.isoformat(),
                    "dias_com_acesso": str(dias),
                    "atividades_previstas": str(previstas),
                    "atividades_entregues": str(entregues),
                    "origem_simulada": "true",
                    "simulado": "true",
                }
            )
    rows.sort(key=lambda row: (row["matricula_id"], row["semana_inicio"]))
    expected = int(config["ead"]["populacao_abertura"]) * 8
    _require(len(rows) == expected, "quantidade de sinais semanais inválida")
    return rows


def _build_financeiro(config: Mapping[str, Any], matriculas: Iterable[Mapping[str, str]]) -> list[dict[str, str]]:
    ead = config["ead"]
    ticket = int(ead["ticket_mensal_centavos"])
    snapshot = date.fromisoformat(str(config["snapshot"]))
    rows: list[dict[str, str]] = []
    for matricula in sorted(matriculas, key=lambda row: row["matricula_id"]):
        start_month = date.fromisoformat(matricula["data_inicio"]).month
        if matricula["data_saida"]:
            end_month = date.fromisoformat(matricula["data_saida"]).month
        else:
            end_month = snapshot.month
        _require(1 <= start_month <= end_month <= 12, "janela financeira mensal inválida")
        for month in range(start_month, end_month + 1):
            rows.append(
                {
                    "titulo_id": "",
                    "matricula_id": matricula["matricula_id"],
                    "competencia": f"2025-{month:02d}",
                    "vencimento": date(2025, month, 10).isoformat(),
                    "valor_devido_centavos": str(ticket),
                    "valor_pago_centavos": "",
                    "data_pagamento": "",
                    "saldo_aberto_centavos": "",
                    "posicao_financeira2025-12-31": "",
                    "simulado": "true",
                }
            )

    rows.sort(key=lambda row: (row["matricula_id"], row["competencia"]))
    for ordinal, row in enumerate(rows, start=1):
        row["titulo_id"] = f"TIT{ordinal:07d}"

    total_due = sum(int(row["valor_devido_centavos"]) for row in rows)
    target_rate = Decimal(str(ead["inadimplencia_monetaria_alvo"]))
    target_open = _round_half_up_fraction(Decimal(total_due) * target_rate)
    allocation_rng = _namespace_rng(int(config["semente"]), "financeiro_alocacao_inadimplencia")
    allocation_order = list(range(len(rows)))
    allocation_rng.shuffle(allocation_order)
    remaining = target_open
    unpaid_by_index: dict[int, int] = {}
    for index in allocation_order:
        due = int(rows[index]["valor_devido_centavos"])
        unpaid = min(due, remaining)
        unpaid_by_index[index] = unpaid
        remaining -= unpaid
    _require(remaining == 0, "não foi possível calibrar o saldo aberto")

    payment_rng = _namespace_rng(int(config["semente"]), "financeiro_datas_pagamento")
    for index, row in enumerate(rows):
        due = int(row["valor_devido_centavos"])
        unpaid = unpaid_by_index[index]
        paid = due - unpaid
        row["valor_pago_centavos"] = str(paid)
        row["saldo_aberto_centavos"] = str(unpaid)
        row["posicao_financeira2025-12-31"] = "aberto" if unpaid else "liquidado"
        if paid == 0:
            row["data_pagamento"] = ""
        else:
            first_of_month = date(2025, int(row["competencia"][5:7]), 1)
            offset = payment_rng.randint(0, (snapshot - first_of_month).days)
            row["data_pagamento"] = (first_of_month + timedelta(days=offset)).isoformat()

    calculated_open = sum(int(row["saldo_aberto_centavos"]) for row in rows)
    _require(calculated_open == target_open, "saldo aberto não fecha com a calibração monetária")
    titles_by_matricula: dict[str, int] = {}
    for row in rows:
        matricula_id = row["matricula_id"]
        titles_by_matricula[matricula_id] = titles_by_matricula.get(matricula_id, 0) + 1
    _require(max(titles_by_matricula.values(), default=0) <= 12, "há mais de 12 títulos por matrícula")
    return rows


def _build_nps(config: Mapping[str, Any], matriculas: Iterable[Mapping[str, str]]) -> list[dict[str, str]]:
    ead = config["ead"]
    active_ids = sorted(row["matricula_id"] for row in matriculas if row["status_final"] == "ativo")
    sample_count = int(ead["nps_respostas"])
    _require(len(active_ids) >= sample_count, "amostra NPS maior que os ativos finais")
    sample_rng = _namespace_rng(int(config["semente"]), "nps_amostra")
    selected = sample_rng.sample(active_ids, sample_count)

    scores = [9, 10] * ((int(ead["nps_promotores"]) + 1) // 2)
    scores = scores[: int(ead["nps_promotores"])]
    scores += [7, 8] * ((int(ead["nps_passivos"]) + 1) // 2)
    scores = scores[: int(ead["nps_promotores"]) + int(ead["nps_passivos"])] + [0, 1, 2, 3, 4, 5, 6] * ((int(ead["nps_detratores"]) + 6) // 7)
    scores = scores[:sample_count]
    score_rng = _namespace_rng(int(config["semente"]), "nps_notas")
    score_rng.shuffle(scores)

    rows: list[dict[str, str]] = []
    for matricula_id, score in zip(selected, scores):
        if score >= 9:
            classification = "promotor"
        elif score >= 7:
            classification = "passivo"
        else:
            classification = "detrator"
        rows.append(
            {
                "resposta_id": "",
                "matricula_id": matricula_id,
                "data_pesquisa": "2025-12-15",
                "nota": str(score),
                "classificacao_nps": classification,
                "simulado": "true",
            }
        )
    rows.sort(key=lambda row: row["matricula_id"])
    for ordinal, row in enumerate(rows, start=1):
        row["resposta_id"] = f"NPS{ordinal:04d}"
    _require(len({row["matricula_id"] for row in rows}) == sample_count, "IDs NPS não são distintos")
    _require(sum(row["classificacao_nps"] == "promotor" for row in rows) == int(ead["nps_promotores"]), "promotores NPS inválidos")
    _require(sum(row["classificacao_nps"] == "passivo" for row in rows) == int(ead["nps_passivos"]), "passivos NPS inválidos")
    _require(sum(row["classificacao_nps"] == "detrator" for row in rows) == int(ead["nps_detratores"]), "detratores NPS inválidos")
    return rows


def _build_references(config: Mapping[str, Any]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for reference in config["segmentos_referencia"]:
        rows.append(
            {
                "segmento": str(reference["segmento"]),
                "ativos_2024": str(reference["ativos_2024"]),
                "ativos_2025": str(reference["ativos_2025"]),
                "ticket_centavos": str(reference["ticket_centavos"]),
                "churn_percentual_referencia": str(reference["churn_percentual_referencia"]),
                "inadimplencia_percentual_referencia": str(reference["inadimplencia_percentual_referencia"]),
                "nps_referencia": str(reference["nps_referencia"]),
                "simulado": "true",
            }
        )
    rows.sort(key=lambda row: row["segmento"])
    _require(len(rows) == 4, "referencias_segmentos deve conter quatro linhas agregadas")
    return rows


def _manifest(
    output_dir: Path,
    config: Mapping[str, Any],
    config_bytes: bytes,
    row_counts: Mapping[str, int],
) -> dict[str, Any]:
    counts = {name: int(row_counts[name]) for name in CSV_NAMES}
    sizes: dict[str, int] = {}
    hashes: dict[str, str] = {}
    files: dict[str, dict[str, Any]] = {}
    for name in CSV_NAMES:
        content = (output_dir / name).read_bytes()
        size = len(content)
        digest = _sha256_bytes(content)
        sizes[name] = size
        hashes[name] = digest
        files[name] = {
            "contagem": counts[name],
            "tamanho_bytes": size,
            "sha256": digest,
            "granularidade": GRANULARIDADES[name],
        }

    aviso = (
        "Dados inteiramente fictícios e calibrados para a primeira melhoria; não são evidência de efeito, "
        "não incluem modelo, dashboard, custos, ROI, desempenho causal ou atendimentos. "
        "A inadimplência é uma posição monetária em 2025-12-31, não uma média mensal anual, e o NPS é uma "
        "amostra sintética de 200 ativos, não uma estimativa da população."
    )
    manifest: dict[str, Any] = {
        "versao": str(config["versao"]),
        "semente": int(config["semente"]),
        "seed": int(config["semente"]),
        "config_sha256": _sha256_bytes(config_bytes),
        "config": {"arquivo": "dados/config.json", "sha256": _sha256_bytes(config_bytes)},
        "snapshot": str(config["snapshot"]),
        "data_corte_sinais": str(config["data_corte_sinais"]),
        "contagens": counts,
        "sizes": sizes,
        "sha256": hashes,
        "granularidade": dict(GRANULARIDADES),
        "arquivos": files,
        "calibracoes": {
            "churn": f"{config['ead']['saidas_churn']} cancelamentos entre {config['ead']['populacao_elegivel_churn']} elegíveis; conclusões e transferências são excluídas da elegibilidade",
            "nps": f"{config['ead']['nps_promotores']} promotores, {config['ead']['nps_passivos']} passivos e {config['ead']['nps_detratores']} detratores entre {config['ead']['nps_respostas']} respostas",
            "financeiro": f"saldo aberto total = ROUND_HALF_UP(total devido * {config['ead']['inadimplencia_monetaria_alvo']}) em centavos",
        },
        "aviso": aviso,
        "aviso_calibrado": aviso,
    }
    manifest_path = output_dir / "manifesto.json"
    manifest_bytes = (json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    manifest_path.write_bytes(manifest_bytes)
    return manifest


def generate(config_path: str | Path, output_dir: str | Path) -> dict[str, Any]:
    """Gera os seis CSV e ``manifesto.json`` e retorna o manifesto.

    A função aceita caminhos relativos ou absolutos, não exclui arquivos que não
    sejam os seus nomes gerados e não possui efeitos colaterais no import.
    """
    config_path = Path(config_path)
    output_dir = Path(output_dir)
    config, config_bytes = _read_config(config_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    alunos, people = _build_students(config)
    matriculas, matricula_by_student = _build_matriculas(config, people)
    _require(len(matricula_by_student) == len(alunos), "cada aluno deve possuir exatamente uma matrícula")
    engajamento = _build_engajamento(config, matriculas)
    financeiro = _build_financeiro(config, matriculas)
    nps = _build_nps(config, matriculas)
    referencias = _build_references(config)

    datasets: list[tuple[str, list[str], list[dict[str, str]]]] = [
        ("alunos_ead.csv", ALUNOS_FIELDS, alunos),
        ("matriculas_ead.csv", MATRICULAS_FIELDS, matriculas),
        ("financeiro_ead.csv", FINANCEIRO_FIELDS, financeiro),
        ("engajamento_semanal_ead.csv", ENGAJAMENTO_FIELDS, engajamento),
        ("pesquisa_nps_ead.csv", NPS_FIELDS, nps),
        ("referencias_segmentos.csv", REFERENCIAS_FIELDS, referencias),
    ]
    row_counts: dict[str, int] = {}
    for filename, fields, rows in datasets:
        row_counts[filename] = _write_csv(output_dir / filename, fields, rows)

    manifest = _manifest(output_dir, config, config_bytes, row_counts)
    return manifest


def _default_root() -> Path:
    return Path(__file__).resolve().parents[1]


def main(argv: list[str] | None = None) -> int:
    root = _default_root()
    parser = argparse.ArgumentParser(description="Gera dados fictícios determinísticos do GENA EAD")
    parser.add_argument("--config", default=str(root / "dados" / "config.json"))
    parser.add_argument("--output", default=str(root / "dados" / "csv"))
    args = parser.parse_args(argv)
    manifest = generate(args.config, args.output)
    total_rows = sum(manifest["contagens"].values())
    print(
        "Dados fictícios GENA gerados: "
        f"{len(manifest['contagens'])} CSV, {total_rows} linhas de dados; "
        f"manifesto em {Path(args.output) / 'manifesto.json'}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
