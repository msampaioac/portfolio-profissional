#!/usr/bin/env python3
"""Reconciliação didática dos indicadores sintéticos GENA EAD.

O módulo somente lê a pasta de dados recebida. A função ``analisar`` é
importável e sem efeitos colaterais; a CLI valida os testes do projeto antes
de materializar qualquer evidência.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import sys
import unittest
from collections import Counter
from datetime import date
from decimal import Decimal, ROUND_HALF_UP, localcontext
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE_DIR = ROOT.parent / "retencao-ead" / "dados"
DEFAULT_OUTPUT_DIR = ROOT / "evidencias"
ARTIFACT_VERSION = "1.0"
SNAPSHOT = "2025-12-31"
SIGNAL_CUTOFF = "2025-02-28"
CSV_NAMES = (
    "alunos_ead.csv",
    "engajamento_semanal_ead.csv",
    "financeiro_ead.csv",
    "matriculas_ead.csv",
    "pesquisa_nps_ead.csv",
    "referencias_segmentos.csv",
)
CALCULATION_CSVS = ("matriculas_ead.csv", "financeiro_ead.csv", "pesquisa_nps_ead.csv")
AUXILIARY_CSVS = {
    "alunos_ead.csv": "identificacao/FK",
    "engajamento_semanal_ead.csv": "contagem/qualidade complementar (nao entra nos cinco indicadores)",
    "referencias_segmentos.csv": "referencias agregadas/configuracao",
}
EXCLUDED_STATUSES = frozenset({"concluido", "transferido"})


class ReconciliacaoError(ValueError):
    """Erro de contrato, integridade ou semântica encontrado na base."""


def _fail(message: str) -> None:
    raise ReconciliacaoError(message)


def _assert(condition: bool, message: str) -> None:
    if not condition:
        _fail(message)


def _bool(value: str, field: str, row_number: int | None = None) -> bool:
    if value not in {"true", "false"}:
        suffix = f" na linha {row_number}" if row_number is not None else ""
        _fail(f"{field} precisa ser true/false{suffix}; recebido {value!r}")
    return value == "true"


def _integer(value: str, field: str, row_number: int | None = None) -> int:
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        suffix = f" na linha {row_number}" if row_number is not None else ""
        raise ReconciliacaoError(f"{field} precisa ser inteiro{suffix}; recebido {value!r}") from exc


def _iso_date(value: str | None, field: str, row_number: int | None = None) -> date:
    """Converte uma data ISO e expõe toda falha como erro de contrato."""
    suffix = f" na linha {row_number}" if row_number is not None else ""
    _assert(value not in (None, ""), f"{field} precisa ser data ISO{suffix}")
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError) as exc:
        raise ReconciliacaoError(f"{field} precisa ser data ISO{suffix}; recebido {value!r}") from exc


def _read_json(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            value = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise ReconciliacaoError(f"nao foi possivel ler JSON {path}: {exc}") from exc
    _assert(isinstance(value, dict), f"JSON {path} precisa ser objeto")
    return value


def _read_csv(path: Path) -> list[dict[str, str]]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            _assert(reader.fieldnames is not None, f"CSV sem cabecalho: {path}")
            rows = list(reader)
    except OSError as exc:
        raise ReconciliacaoError(f"nao foi possivel ler CSV {path}: {exc}") from exc
    _assert(all(row.get(None) is None for row in rows), f"CSV com colunas extras: {path}")
    return rows


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as exc:
        raise ReconciliacaoError(f"nao foi possivel ler bytes de {path}: {exc}") from exc
    return digest.hexdigest()


def _config_and_manifest(source_dir: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    config_path = source_dir / "config.json"
    manifest_path = source_dir / "csv" / "manifesto.json"
    config = _read_json(config_path)
    manifest = _read_json(manifest_path)
    actual_config_hash = _sha256(config_path)
    expected_config_hashes = {
        manifest.get("config_sha256"),
        (manifest.get("config") or {}).get("sha256"),
    }
    expected_config_hashes.discard(None)
    _assert(expected_config_hashes, "manifesto nao informa hash de config")
    _assert(len(expected_config_hashes) == 1, "manifesto tem hashes de config divergentes")
    _assert(actual_config_hash in expected_config_hashes, "hash de config divergente do manifesto")
    _assert(manifest.get("versao") == config.get("versao"), "versao config/manifesto divergente")
    _assert(manifest.get("snapshot") == config.get("snapshot") == SNAPSHOT, "snapshot divergente")
    _assert(manifest.get("data_corte_sinais") == config.get("data_corte_sinais") == SIGNAL_CUTOFF, "corte de sinais divergente")

    hashes: dict[str, Any] = {
        "config_sha256": actual_config_hash,
        "csv": {},
        "csv_count": 0,
    }
    manifest_files = manifest.get("arquivos")
    manifest_sha = manifest.get("sha256")
    manifest_counts = manifest.get("contagens")
    manifest_sizes = manifest.get("sizes")
    _assert(isinstance(manifest_files, dict), "manifesto sem arquivos")
    _assert(isinstance(manifest_sha, dict), "manifesto sem sha256 de CSV")
    _assert(isinstance(manifest_counts, dict), "manifesto sem contagens")
    _assert(isinstance(manifest_sizes, dict), "manifesto sem sizes")

    for name in CSV_NAMES:
        path = source_dir / "csv" / name
        actual_hash = _sha256(path)
        actual_size = path.stat().st_size
        rows = _read_csv(path)
        actual_count = len(rows)
        entry = manifest_files.get(name) or {}
        expected_hashes = {entry.get("sha256"), manifest_sha.get(name)}
        expected_hashes.discard(None)
        _assert(len(expected_hashes) == 1, f"hashes divergentes ou ausentes para {name}")
        _assert(actual_hash in expected_hashes, f"hash divergente para {name}")
        _assert(actual_count == entry.get("contagem") == manifest_counts.get(name), f"contagem divergente para {name}")
        _assert(actual_size == entry.get("tamanho_bytes") == manifest_sizes.get(name), f"tamanho divergente para {name}")
        hashes["csv"][name] = {
            "sha256": actual_hash,
            "contagem": actual_count,
            "tamanho_bytes": actual_size,
            "uso": "calculo" if name in CALCULATION_CSVS else AUXILIARY_CSVS[name],
        }
        hashes["csv_count"] += 1
    return config, manifest, hashes


def _is_opening(row: Mapping[str, str]) -> bool:
    """Deriva abertura a partir da coorte/flag de abertura e data de início."""
    return (
        row.get("tipo_coorte") == "abertura_2025"
        and row.get("data_inicio") == "2025-01-01"
        and row.get("pertencente_abertura") == "true"
    )


def _derived_eligible(row: Mapping[str, str]) -> bool:
    """Deriva elegibilidade sem consultar a coluna de flag persistida."""
    return _is_opening(row) and row.get("status_final") not in EXCLUDED_STATUSES


def validar_elegibilidade(rows: Sequence[Mapping[str, str]]) -> dict[str, int]:
    """Valida a flag persistida contra abertura/status e retorna contagens.

    Esta função é pública para que o teste de corrupção da flag não precise
    alterar bytes nem o manifesto antes de testar a regra semântica.
    """
    derived = [_derived_eligible(row) for row in rows]
    for index, (row, expected) in enumerate(zip(rows, derived), start=2):
        persisted = row.get("elegivel_churn")
        _assert(persisted in {"true", "false"}, f"flag elegivel_churn invalida na linha {index}")
        if (persisted == "true") != expected:
            _fail(
                f"elegibilidade divergente para {row.get('matricula_id', '<sem id>')}: "
                f"persistida={persisted}, derivada={'true' if expected else 'false'}"
            )
    opening = sum(_is_opening(row) for row in rows)
    eligible = sum(derived)
    exits = sum(expected and row.get("status_final") == "cancelado" for row, expected in zip(rows, derived))
    retained = sum(expected and row.get("status_final") == "ativo" for row, expected in zip(rows, derived))
    concluded = sum(_is_opening(row) and row.get("status_final") == "concluido" for row in rows)
    transferred = sum(_is_opening(row) and row.get("status_final") == "transferido" for row in rows)
    return {
        "abertura": int(opening),
        "elegiveis": int(eligible),
        "saidas_cancelamento": int(exits),
        "retidos": int(retained),
        "conclusoes": int(concluded),
        "transferencias": int(transferred),
    }


def _percentual(numerator: int, denominator: int) -> Decimal:
    _assert(denominator > 0, "denominador precisa ser positivo")
    with localcontext() as context:
        context.prec = 50
        return (Decimal(numerator) / Decimal(denominator) * Decimal(100)).normalize()


def _money_rate(open_cents: int, due_cents: int) -> Decimal:
    with localcontext() as context:
        context.prec = 50
        return (Decimal(open_cents) / Decimal(due_cents) * Decimal(100)).normalize()


def _validate_population(
    config: Mapping[str, Any],
    alunos: Sequence[Mapping[str, str]],
    matriculas: Sequence[Mapping[str, str]],
) -> tuple[dict[str, int], set[str], set[str]]:
    ead = config["ead"]
    _assert(len(alunos) == 3970, "populacao de alunos diferente de 3970")
    _assert(len(matriculas) == 3970, "populacao de matriculas diferente de 3970")
    student_ids = [row.get("student_id", "") for row in alunos]
    matricula_ids = [row.get("matricula_id", "") for row in matriculas]
    _assert(len(set(student_ids)) == 3970, "student_id nao e unico")
    _assert(len(set(matricula_ids)) == 3970, "matricula_id nao e unico")
    aluno_set = set(student_ids)
    matricula_student_ids = [row.get("student_id", "") for row in matriculas]
    _assert(set(matricula_student_ids) == aluno_set, "FK student_id de matriculas divergente de alunos")
    _assert(len(matricula_student_ids) == len(set(matricula_student_ids)), "student_id nao e 1:1 em matriculas")
    for index, row in enumerate(alunos, start=2):
        _bool(row.get("simulado", ""), "alunos.simulado", index)
    for index, row in enumerate(matriculas, start=2):
        _bool(row.get("pertencente_abertura", ""), "matriculas.pertencente_abertura", index)
        _bool(row.get("elegivel_churn", ""), "matriculas.elegivel_churn", index)
        _bool(row.get("simulado", ""), "matriculas.simulado", index)
    counts = validar_elegibilidade(matriculas)
    _assert(counts["abertura"] == ead["populacao_abertura"] == 2880, "abertura nao confere")
    _assert(counts["conclusoes"] == ead["conclusoes_coorte_abertura"] == 40, "conclusoes nao conferem")
    _assert(counts["transferencias"] == ead["transferencias_coorte_abertura"] == 40, "transferencias nao conferem")
    _assert(counts["elegiveis"] == ead["populacao_elegivel_churn"] == 2800, "elegiveis nao conferem")
    _assert(counts["saidas_cancelamento"] == ead["saidas_churn"] == 770, "saidas nao conferem")
    _assert(counts["retidos"] == ead["retidos_coorte_abertura"] == 2030, "retidos nao conferem")
    ingressantes = sum(row.get("tipo_coorte") == "ingressante_2025" for row in matriculas)
    _assert(ingressantes == ead["novas_matriculas"] == 1090, "ingressantes nao conferem")
    ativos_fechamento = sum(row.get("status_final") == "ativo" for row in matriculas)
    _assert(ativos_fechamento == ead["ativos_fechamento"] == 3120, "ativos de fechamento nao conferem")
    _assert(counts["abertura"] - counts["conclusoes"] - counts["transferencias"] == counts["elegiveis"], "equacao de elegibilidade falhou")
    _assert(counts["elegiveis"] == counts["saidas_cancelamento"] + counts["retidos"], "equacao de churn falhou")
    _assert(counts["retidos"] + ingressantes == ativos_fechamento, "equacao de fechamento falhou")
    _assert(counts["abertura"] + ingressantes == len(matriculas), "equacao de unicos falhou")
    return {**counts, "ingressantes": ingressantes, "ativos_fechamento": ativos_fechamento, "unicos": len(matriculas)}, aluno_set, set(matricula_ids)


def _validate_financeiro(config: Mapping[str, Any], rows: Sequence[Mapping[str, str]], matricula_ids: set[str]) -> dict[str, int | Decimal]:
    ead = config["ead"]
    _assert(rows, "financeiro vazio")
    snapshot_date = _iso_date(SNAPSHOT, "SNAPSHOT")
    titulo_ids: set[str] = set()
    due = 0
    paid = 0
    open_cents = 0
    for index, row in enumerate(rows, start=2):
        titulo_id = row.get("titulo_id", "")
        _assert(titulo_id and titulo_id not in titulo_ids, f"titulo_id duplicado/vazio na linha {index}")
        titulo_ids.add(titulo_id)
        _assert(row.get("matricula_id") in matricula_ids, f"FK financeiro.matricula_id invalida na linha {index}")
        _bool(row.get("simulado", ""), "financeiro.simulado", index)
        _assert(row.get("simulado") == "true", f"financeiro.simulado precisa ser true na linha {index}")
        competencia_raw = row.get("competencia", "")
        competencia_value = _iso_date(f"{competencia_raw}-01", "financeiro.competencia", index)
        vencimento_value = _iso_date(row.get("vencimento"), "financeiro.vencimento", index)
        _assert(competencia_value.year == snapshot_date.year, f"competencia financeira fora de 2025 na linha {index}")
        _assert(vencimento_value.year == snapshot_date.year, f"vencimento financeiro fora de 2025 na linha {index}")
        _assert(competencia_value <= snapshot_date, f"competencia financeira posterior ao snapshot na linha {index}")
        _assert(vencimento_value <= snapshot_date, f"vencimento financeiro posterior ao snapshot na linha {index}")
        _assert(
            (vencimento_value.year, vencimento_value.month) == (competencia_value.year, competencia_value.month),
            f"vencimento nao corresponde a competencia na linha {index}",
        )
        row_due = _integer(row.get("valor_devido_centavos", ""), "valor_devido_centavos", index)
        row_paid = _integer(row.get("valor_pago_centavos", ""), "valor_pago_centavos", index)
        row_open = _integer(row.get("saldo_aberto_centavos", ""), "saldo_aberto_centavos", index)
        _assert(row_due == ead["ticket_mensal_centavos"] == 31000, f"ticket divergente na linha {index}")
        _assert(0 <= row_paid <= row_due, f"pagamento invalido na linha {index}")
        _assert(row_open == row_due - row_paid, f"saldo divergente na linha {index}")
        payment_raw = row.get("data_pagamento")
        if row_paid > 0:
            _assert(payment_raw not in (None, ""), f"pagamento positivo sem data na linha {index}")
            payment_date = _iso_date(payment_raw, "financeiro.data_pagamento", index)
            _assert(payment_date <= snapshot_date, f"data de pagamento posterior ao snapshot na linha {index}")
        else:
            _assert(payment_raw in (None, ""), f"pagamento sem valor nao pode ter data na linha {index}")
        _assert(row.get("posicao_financeira2025-12-31") == ("aberto" if row_open else "liquidado"), f"posicao divergente na linha {index}")
        due += row_due
        paid += row_paid
        open_cents += row_open
    target = (Decimal(due) * Decimal(ead["inadimplencia_monetaria_alvo"])).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    _assert(open_cents == int(target), "saldo aberto nao confere com ROUND_HALF_UP do alvo")
    _assert(paid + open_cents == due, "soma financeiro nao fecha")
    return {
        "titulos": len(rows),
        "total_devido_centavos": due,
        "total_pago_centavos": paid,
        "saldo_aberto_centavos": open_cents,
        "saldo_liquidado_centavos": paid,
        "inadimplencia_percentual": _money_rate(open_cents, due),
        "adimplencia_percentual": _money_rate(paid, due),
        "alvo_arredondado_centavos": int(target),
    }


def _validate_nps(config: Mapping[str, Any], rows: Sequence[Mapping[str, str]], matricula_rows: Sequence[Mapping[str, str]]) -> dict[str, int | Decimal]:
    ead = config["ead"]
    active_ids = {row["matricula_id"] for row in matricula_rows if row.get("status_final") == "ativo"}
    response_ids: set[str] = set()
    respondent_ids: set[str] = set()
    counts: Counter[str] = Counter()
    for index, row in enumerate(rows, start=2):
        response_id = row.get("resposta_id", "")
        respondent_id = row.get("matricula_id", "")
        _assert(response_id and response_id not in response_ids, f"resposta_id duplicado/vazio na linha {index}")
        _assert(respondent_id in active_ids, f"NPS referencia matricula nao ativa na linha {index}")
        _assert(respondent_id not in respondent_ids, f"matricula NPS repetida na linha {index}")
        response_ids.add(response_id)
        respondent_ids.add(respondent_id)
        nota = _integer(row.get("nota", ""), "nota NPS", index)
        _assert(0 <= nota <= 10, f"nota NPS fora do intervalo na linha {index}")
        if nota >= 9:
            expected_class = "promotor"
        elif nota >= 7:
            expected_class = "passivo"
        else:
            expected_class = "detrator"
        _assert(row.get("classificacao_nps") == expected_class, f"classificacao NPS divergente na linha {index}")
        _bool(row.get("simulado", ""), "NPS.simulado", index)
        counts[expected_class] += 1
    _assert(len(rows) == ead["nps_respostas"] == 200, "quantidade NPS divergente")
    _assert(counts["promotor"] == ead["nps_promotores"] == 118, "promotores divergentes")
    _assert(counts["passivo"] == ead["nps_passivos"] == 42, "passivos divergentes")
    _assert(counts["detrator"] == ead["nps_detratores"] == 40, "detratores divergentes")
    nps = _percentual(counts["promotor"] - counts["detrator"], len(rows))
    _assert(nps == Decimal("39"), "NPS nao fecha em 39")
    return {
        "respostas": len(rows),
        "promotores": counts["promotor"],
        "passivos": counts["passivo"],
        "detratores": counts["detrator"],
        "valor": int(nps),
    }


def _validate_engajamento(rows: Sequence[Mapping[str, str]], opening_ids: set[str]) -> dict[str, int | str | bool]:
    _assert(len(rows) == 23040, "quantidade de linhas de engajamento divergente")
    pairs: set[tuple[str, str]] = set()
    per_matricula: Counter[str] = Counter()
    week_starts: set[date] = set()
    week_ends: set[date] = set()
    cutoff = _iso_date(SIGNAL_CUTOFF, "data_corte_sinais")
    for index, row in enumerate(rows, start=2):
        mid = row.get("matricula_id", "")
        pair = (mid, row.get("semana_inicio", ""))
        _assert(mid in opening_ids, f"engajamento referencia matricula fora da abertura na linha {index}")
        _assert(pair not in pairs, f"chave composta de engajamento duplicada na linha {index}")
        pairs.add(pair)
        per_matricula[mid] += 1
        week_start = _iso_date(row.get("semana_inicio"), "engajamento.semana_inicio", index)
        week_end = _iso_date(row.get("semana_fim"), "engajamento.semana_fim", index)
        _assert(week_start <= week_end, f"janela de engajamento invertida na linha {index}")
        _assert(week_end <= cutoff, f"janela de engajamento posterior a 28/02/2025 na linha {index}")
        week_starts.add(week_start)
        week_ends.add(week_end)
        _bool(row.get("origem_simulada", ""), "engajamento.origem_simulada", index)
        _bool(row.get("simulado", ""), "engajamento.simulado", index)
        dias = _integer(row.get("dias_com_acesso", ""), "dias_com_acesso", index)
        previstas = _integer(row.get("atividades_previstas", ""), "atividades_previstas", index)
        entregues = _integer(row.get("atividades_entregues", ""), "atividades_entregues", index)
        _assert(0 <= dias <= 7 and previstas >= 1 and 0 <= entregues <= previstas, f"valores de engajamento invalidos na linha {index}")
    _assert(len(per_matricula) == len(opening_ids) and all(value == 8 for value in per_matricula.values()), "engajamento nao tem 8 semanas por abertura")
    _assert(len(week_starts) == 8 and len(week_ends) == 8, "engajamento nao tem 8 janelas distintas")
    return {
        "linhas": len(rows),
        "matriculas": len(per_matricula),
        "semanas_por_matricula": 8,
        "janela_inicio": min(week_starts).isoformat(),
        "janela_fim": max(week_ends).isoformat(),
        "dominios_validados": True,
    }


def _validate_references(config: Mapping[str, Any], rows: Sequence[Mapping[str, str]]) -> dict[str, Any]:
    configured = {item["segmento"]: item for item in config["segmentos_referencia"]}
    _assert(set(configured) == {row.get("segmento") for row in rows}, "segmentos de referencia divergentes")
    for row in rows:
        _bool(row.get("simulado", ""), "referencias.simulado")
        reference = configured[row["segmento"]]
        for key in ("ativos_2024", "ativos_2025", "ticket_centavos", "nps_referencia"):
            _assert(_integer(row[key], f"referencia.{key}") == reference[key], f"referencia {row['segmento']} divergente em {key}")
    ead_reference = next(row for row in rows if row["segmento"] == "Graduacao EAD")
    _assert(Decimal(ead_reference["churn_percentual_referencia"]) == Decimal("27.5"), "referencia de churn EAD divergente")
    _assert(Decimal(ead_reference["inadimplencia_percentual_referencia"]) == Decimal("13.5"), "referencia de inadimplencia EAD divergente")
    _assert(_integer(ead_reference["nps_referencia"], "referencia.nps") == 39, "referencia NPS EAD divergente")
    return {"linhas": len(rows), "segmentos": sorted(configured), "graduacao_ead_confere": True}


def analisar(source_dir: str | Path = DEFAULT_SOURCE_DIR) -> dict[str, Any]:
    """Lê, valida e reconcilia a fonte; não cria arquivos nem altera a fonte."""
    source = Path(source_dir).expanduser().resolve()
    _assert(source.is_dir(), f"source_dir inexistente: {source}")
    config, manifest, hashes = _config_and_manifest(source)
    csv_dir = source / "csv"
    alunos = _read_csv(csv_dir / "alunos_ead.csv")
    engagement = _read_csv(csv_dir / "engajamento_semanal_ead.csv")
    financeiro = _read_csv(csv_dir / "financeiro_ead.csv")
    matriculas = _read_csv(csv_dir / "matriculas_ead.csv")
    nps_rows = _read_csv(csv_dir / "pesquisa_nps_ead.csv")
    referencias = _read_csv(csv_dir / "referencias_segmentos.csv")
    population, aluno_ids, matricula_ids = _validate_population(config, alunos, matriculas)
    financial = _validate_financeiro(config, financeiro, matricula_ids)
    nps = _validate_nps(config, nps_rows, matriculas)
    opening_ids = {row["matricula_id"] for row in matriculas if _is_opening(row)}
    engagement_summary = _validate_engajamento(engagement, opening_ids)
    references = _validate_references(config, referencias)

    exits = population["saidas_cancelamento"]
    eligible = population["elegiveis"]
    retained = population["retidos"]
    wrong_denominator = population["ativos_fechamento"]
    wrong_rate = _percentual(exits, wrong_denominator)
    churn_rate = _percentual(exits, eligible)
    retention_rate = _percentual(retained, eligible)
    with localcontext() as context:
        context.prec = 50
        difference_pp = churn_rate - wrong_rate
    config_ead = config["ead"]
    _assert(churn_rate == Decimal("27.5"), "churn calculado nao e 27.5%")
    _assert(retention_rate == Decimal("72.5"), "retencao calculada nao e 72.5%")
    _assert(financial["inadimplencia_percentual"] == Decimal("13.5"), "inadimplencia calculada nao e 13.5%")
    _assert(financial["adimplencia_percentual"] == Decimal("86.5"), "adimplencia calculada nao e 86.5%")
    _assert(nps["valor"] == 39, "NPS calculado nao e 39")
    _assert(Decimal(config_ead["inadimplencia_monetaria_alvo"]) == Decimal("0.135"), "alvo monetario divergente")
    _assert(Decimal(str(config["segmentos_referencia"][2]["churn_percentual_referencia"])) == Decimal("27.5"), "config referencia churn divergente")

    return {
        "artefato": {
            "nome": "reconciliacao_indicadores",
            "versao": ARTIFACT_VERSION,
            "versao_config": str(config["versao"]),
            "snapshot": SNAPSHOT,
            "referencia_dados": SNAPSHOT,
            "sem_timestamp_execucao": True,
        },
        "ficcionalidade": {
            "dados_inteiramente_ficticios": True,
            "controle_tecnico_nao_valida_mercado": True,
            "aviso": "Base inteiramente fictícia; reconciliação técnica de contrato, bytes e definições, sem validação de mercado ou efeito de negócio.",
        },
        "integridade": {
            "config_hash_verificado": True,
            "manifesto_csv_sha256_verificado": True,
            "csv_verificados": hashes["csv_count"],
            "config_sha256": hashes["config_sha256"],
            "arquivos": hashes["csv"],
        },
        "populacao": {
            **population,
            "equacoes": [
                "2880 - 40 - 40 = 2800",
                "2800 = 770 + 2030",
                "2030 + 1090 = 3120",
                "2880 + 1090 = 3970",
            ],
            "fk_alunos_matriculas_valida": True,
            "ids_unicos": aluno_ids == {row["student_id"] for row in alunos} and len(matricula_ids) == 3970,
        },
        "comparacao_churn": {
            "saidas": exits,
            "denominador_fotografia_ativos_fechamento": wrong_denominator,
            "percentual_fotografia": wrong_rate,
            "denominador_coorte_elegivel": eligible,
            "percentual_coorte": churn_rate,
            "diferenca_pontos_percentuais": difference_pp,
            "interpretacao": "A diferenca e correcao de definicao do denominador; nao e aumento de churn nem efeito de negocio.",
        },
        "indicadores": {
            "churn": {"numerador": exits, "denominador": eligible, "percentual": churn_rate},
            "retencao": {"numerador": retained, "denominador": eligible, "percentual": retention_rate},
            "inadimplencia_monetaria": {
                "saldo_aberto_centavos": financial["saldo_aberto_centavos"],
                "total_devido_centavos": financial["total_devido_centavos"],
                "percentual": financial["inadimplencia_percentual"],
                "arredondamento": "ROUND_HALF_UP",
            },
            "adimplencia_monetaria": {
                "saldo_liquidado_centavos": financial["saldo_liquidado_centavos"],
                "total_devido_centavos": financial["total_devido_centavos"],
                "percentual": financial["adimplencia_percentual"],
            },
            "nps": {
                "respostas": nps["respostas"],
                "promotores": nps["promotores"],
                "passivos": nps["passivos"],
                "detratores": nps["detratores"],
                "valor": nps["valor"],
            },
        },
        "complementares": {
            "engajamento": engagement_summary,
            "referencias": references,
            "engajamento_nao_entra_nos_cinco_indicadores": True,
        },
        "conversao": {
            "status": "nao_calculada",
            "testada": False,
            "motivo": "Nao ha CRM, funil ou dados de conversao nesta fonte.",
        },
        "controles": {
            "elegibilidade_derivada_de_abertura_status": True,
            "flag_elegivel_churn_validada": True,
            "manifesto_inclui_seis_csv": True,
            "fontes_de_calculo": list(CALCULATION_CSVS),
            "fontes_auxiliares": dict(AUXILIARY_CSVS),
        },
    }


class DecimalJSONEncoder(json.JSONEncoder):
    """Handler determinístico: Decimals são serializados como texto decimal."""

    def default(self, value: Any) -> Any:
        if isinstance(value, Decimal):
            return format(value, "f")
        return super().default(value)


def _decimal_text(value: Decimal | int) -> str:
    return format(value, "f") if isinstance(value, Decimal) else str(value)


def _format_pt_int(value: int) -> str:
    return f"{int(value):,}".replace(",", ".")


def _format_pt_percent(value: Decimal | int) -> str:
    rounded = Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return f"{rounded:.2f}".replace(".", ",")


def _format_brl_centavos(value: int) -> str:
    reais, centavos = divmod(int(value), 100)
    return f"R$ {_format_pt_int(reais)},{centavos:02d}"


def _json_bytes(result: Mapping[str, Any]) -> bytes:
    return (json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True, cls=DecimalJSONEncoder) + "\n").encode("utf-8")


def gerar_comparacao_csv(result: Mapping[str, Any]) -> bytes:
    comparison = result["comparacao_churn"]
    output = io.StringIO(newline="")
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(("cenario", "saidas_churn", "denominador", "percentual_churn", "diferenca_p.p.", "leitura"))
    writer.writerow((
        "foto_ativos_fechamento",
        comparison["saidas"],
        comparison["denominador_fotografia_ativos_fechamento"],
        _decimal_text(comparison["percentual_fotografia"]),
        _decimal_text(comparison["diferenca_pontos_percentuais"]),
        "denominador didatico incorreto; nao representa churn da coorte",
    ))
    writer.writerow((
        "coorte_abertura_elegivel",
        comparison["saidas"],
        comparison["denominador_coorte_elegivel"],
        _decimal_text(comparison["percentual_coorte"]),
        "0",
        "definicao corrigida: abertura menos concluido e transferido",
    ))
    return output.getvalue().encode("utf-8")


def gerar_relatorio(result: Mapping[str, Any], testes_executados: int) -> bytes:
    integrity = result["integridade"]
    population = result["populacao"]
    comparison = result["comparacao_churn"]
    indicators = result["indicadores"]
    financial = indicators["inadimplencia_monetaria"]
    nps = indicators["nps"]
    comp = result["complementares"]
    lines = [
        "# Reconciliação didática de indicadores — GENA EAD",
        "",
        "> **Escopo e aviso:** base inteiramente fictícia; reconciliação técnica de contrato, bytes e definições, sem validação de mercado ou efeito de negócio.",
        "",
        "## Rastreabilidade, fontes e integridade",
        "",
        f"- Referência dos dados: snapshot `{SNAPSHOT}`; versão do artefato: `{ARTIFACT_VERSION}`; versão da configuração: `{result['artefato']['versao_config']}`.",
        f"- Configuração: [`config.json`](../../retencao-ead/dados/config.json), SHA-256 verificado `{integrity['config_sha256'][:16]}…` (completo no [`resultado-reconciliacao.json`](./resultado-reconciliacao.json)).",
        "- Dicionário da fonte: [`dicionario.md`](../../retencao-ead/dados/dicionario.md).",
        "- Manifesto e hashes: [`manifesto.json`](../../retencao-ead/dados/csv/manifesto.json); 6/6 CSVs tiveram SHA-256, tamanho e contagem conferidos.",
        "",
        "| CSV | Uso | SHA-256 verificado | Linhas |\n|:---|:---|:---|---:|",
    ]
    for name in CSV_NAMES:
        item = integrity["arquivos"][name]
        lines.append(f"| [`{name}`](../../retencao-ead/dados/csv/{name}) | {item['uso']} | `{item['sha256'][:16]}…` | {_format_pt_int(item['contagem'])} |")
    lines.extend([
        "",
        "- Fontes usadas no cálculo dos cinco indicadores: `matriculas_ead.csv`, `financeiro_ead.csv`, `pesquisa_nps_ead.csv`.",
        "- `alunos_ead.csv` apoia identificação/FK; `referencias_segmentos.csv` confere referências; `engajamento_semanal_ead.csv` fornece apenas contagem/qualidade complementar, não entra nos cinco indicadores.",
        "- Implementação: [`scripts/reconciliar_indicadores.py`](../scripts/reconciliar_indicadores.py). Testes isolados: [`tests/test_reconciliacao.py`](../tests/test_reconciliacao.py). Contexto do caso: [`README.md`](../README.md), [`registro-decisoes.md`](../docs/registro-decisoes.md), [`dicionario-indicadores.md`](../docs/dicionario-indicadores.md).",
        "",
        "## Erro semântico deliberado e correção",
        "",
        "A mesma quantidade de 770 cancelamentos foi dividida primeiro pela fotografia de fechamento de 3.120 (denominador didático deliberadamente errado) e depois pela coorte de abertura elegível de 2.800. O segundo denominador é derivado de abertura/status e exclui retrospectivamente 40 concluídos e 40 transferidos. A anomalia foi criada intencionalmente para o exercício; não é descoberta operacional.",
        "",
        "| Definição | Saídas | Denominador | Churn |\n|:---|---:|---:|---:|",
        f"| Foto de ativos no fechamento (errado) | {_format_pt_int(comparison['saidas'])} | {_format_pt_int(comparison['denominador_fotografia_ativos_fechamento'])} | {_format_pt_percent(comparison['percentual_fotografia'])}% |",
        f"| Coorte de abertura elegível (correto) | {_format_pt_int(comparison['saidas'])} | {_format_pt_int(comparison['denominador_coorte_elegivel'])} | {_format_pt_percent(comparison['percentual_coorte'])}% |",
        "",
        f"Diferença: **{_format_pt_percent(comparison['diferenca_pontos_percentuais'])} p.p.** (a precisão integral permanece no JSON e no CSV). Isso é correção de definição, **não aumento de churn nem efeito de negócio**.",
        "",
        "## Reconciliação populacional",
        "",
        f"- Abertura: `{_format_pt_int(population['abertura'])}`; conclusões: `{_format_pt_int(population['conclusoes'])}`; transferências: `{_format_pt_int(population['transferencias'])}`; elegíveis: `{_format_pt_int(population['elegiveis'])}`; cancelamentos: `{_format_pt_int(population['saidas_cancelamento'])}`; retidos: `{_format_pt_int(population['retidos'])}`; ingressantes: `{_format_pt_int(population['ingressantes'])}`; ativos no fechamento: `{_format_pt_int(population['ativos_fechamento'])}`.",
        "- Equações conferidas: `2880 − 40 − 40 = 2800`; `2800 = 770 + 2030`; `2030 + 1090 = 3120`; `2880 + 1090 = 3970`.",
        f"- IDs únicos: `{_format_pt_int(population['unicos'])}`; FK aluno–matrícula e flag `elegivel_churn` conferidas contra abertura/status.",
        "",
        "## Cinco indicadores recalculados independentemente",
        "",
        "| Indicador | Numerador/contagem | Denominador/base | Resultado |\n|:---|---:|---:|---:|",
        f"| Churn | {_format_pt_int(indicators['churn']['numerador'])} saídas | {_format_pt_int(indicators['churn']['denominador'])} elegíveis | **{_format_pt_percent(indicators['churn']['percentual'])}%** |",
        f"| Retenção | {_format_pt_int(indicators['retencao']['numerador'])} retidos | {_format_pt_int(indicators['retencao']['denominador'])} elegíveis | **{_format_pt_percent(indicators['retencao']['percentual'])}%** |",
        f"| Inadimplência monetária | {_format_brl_centavos(financial['saldo_aberto_centavos'])} em aberto | {_format_brl_centavos(financial['total_devido_centavos'])} devidos | **{_format_pt_percent(financial['percentual'])}%** |",
        f"| Adimplência monetária | {_format_brl_centavos(indicators['adimplencia_monetaria']['saldo_liquidado_centavos'])} liquidados | {_format_brl_centavos(indicators['adimplencia_monetaria']['total_devido_centavos'])} devidos | **{_format_pt_percent(indicators['adimplencia_monetaria']['percentual'])}%** |",
        f"| NPS amostral | {_format_pt_int(nps['promotores'])} promotores − {_format_pt_int(nps['detratores'])} detratores | {_format_pt_int(nps['respostas'])} respostas | **{nps['valor']}** |",
        "",
        "A posição monetária foi conferida em centavos com `ROUND_HALF_UP` sobre o total devido e alvo `0.135`. O NPS conferiu `200 = 118 + 42 + 40` e `(118 − 40) / 200 × 100 = 39`; ele não é estimativa populacional.",
        "",
        "## Complementares e limites",
        "",
        f"- Engajamento: {_format_pt_int(comp['engajamento']['linhas'])} linhas, {_format_pt_int(comp['engajamento']['matriculas'])} matrículas, {_format_pt_int(comp['engajamento']['semanas_por_matricula'])} janelas por matrícula, de `{comp['engajamento']['janela_inicio']}` a `{comp['engajamento']['janela_fim']}`. É apenas controle de contagem/qualidade; não há indicador agregado nem inferência de causalidade.",
        "- Referência `Graduacao EAD` em configuração/CSV confere churn 27,50%, inadimplência 13,50%, NPS 39, ativos 2025 3.120 e ticket de R$ 310,00.",
        "- Conversão: **não calculada, não testada, preliminarmente sem CRM/funil**; não há dado de conversão nesta fonte.",
        "- Não há SQL, dashboard, modelo, piloto, ROI, custo, causalidade ou afirmação de impacto nesta entrega.",
        "",
        "## Execução reprodutível",
        "",
        f"- O CLI executou **{testes_executados} testes deste projeto** no momento da geração, antes de escrever as evidências, e só prosseguiu com resultado OK; não é gravado timestamp variável e esse número é independente de outros testes `test_dados_gena`.",
        "- Comando principal (a partir de `governanca-indicadores`): `python3 scripts/reconciliar_indicadores.py`.",
        "- Opções: `--source-dir CAMINHO_DADOS` troca a pasta `dados` (espera `config.json` e `csv/manifesto.json`); `--output-dir DIRETORIO` troca a pasta dos três artefatos; `--output CAMINHO_JSON` troca apenas o caminho do JSON (sem `--output-dir`, CSV/Markdown usam o diretório pai do JSON).",
        "- Para apenas validar/inspecionar sem escrever, importe `analisar(source_dir)`; ela é side-effect-free. A referência de dados é o snapshot; a execução é real, mas os artefatos não registram o relógio.",
    ])
    return ("\n".join(lines) + "\n").encode("utf-8")


def _run_project_tests() -> int:
    """Executa unittest discover em tests/ e retorna a contagem real."""
    loader = unittest.defaultTestLoader
    suite = loader.discover(start_dir=str(ROOT / "tests"), pattern="test_*.py")
    stream = io.StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=1)
    result = runner.run(suite)
    if not result.wasSuccessful():
        print(stream.getvalue(), file=sys.stderr)
        raise ReconciliacaoError("testes do projeto falharam; nenhuma evidencia foi escrita")
    return result.testsRun


def _write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, default=DEFAULT_SOURCE_DIR, help="pasta dados contendo config.json e csv/ (padrao: ../retencao-ead/dados)")
    parser.add_argument("--output-dir", type=Path, default=None, help="diretorio para CSV, JSON e Markdown")
    parser.add_argument("--output", type=Path, default=None, help="caminho alternativo apenas para resultado-reconciliacao.json")
    args = parser.parse_args(argv)

    try:
        test_count = _run_project_tests()
        result = analisar(args.source_dir)
        result["execucao"] = {
            "testes_executados": test_count,
            "resultado_testes": "OK",
            "referencia_dados": SNAPSHOT,
        }
        if args.output is not None:
            json_path = args.output
            output_dir = args.output_dir if args.output_dir is not None else json_path.parent
        else:
            output_dir = args.output_dir or DEFAULT_OUTPUT_DIR
            json_path = output_dir / "resultado-reconciliacao.json"
        csv_path = output_dir / "comparacao-churn.csv"
        markdown_path = output_dir / "reconciliacao.md"
        # All validation and test gates occur before the first mkdir/write.
        _write(csv_path, gerar_comparacao_csv(result))
        _write(json_path, _json_bytes(result))
        _write(markdown_path, gerar_relatorio(result, test_count))
    except (ReconciliacaoError, OSError) as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1
    print(f"OK: {test_count} testes; 3 evidencias escritas em {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
