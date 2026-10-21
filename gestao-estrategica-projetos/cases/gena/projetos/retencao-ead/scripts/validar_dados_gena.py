#!/usr/bin/env python3
"""Valida os CSV publicados e gera reconciliação; não mede impacto de negócio."""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import sys
import unittest
from collections import Counter, defaultdict
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

PROJETO = Path(__file__).resolve().parents[1]


def _encontrar_raiz_unificada(projeto: Path) -> Path:
    """Encontra a raiz Git mais próxima ou reconhece a subpasta de Gestão."""
    for candidato in (projeto, *projeto.parents):
        marcador = candidato / ".git"
        if marcador.is_dir() or marcador.is_file():
            return candidato
    for candidato in (projeto, *projeto.parents):
        if candidato.name == "gestao-estrategica-projetos":
            return candidato.parent
    return projeto.parents[3] if len(projeto.parents) > 3 else projeto.parent


ROOT = PROJETO
REPO_ROOT = _encontrar_raiz_unificada(PROJETO)
try:
    PROJECT_DOC_PATH = PROJETO.relative_to(REPO_ROOT).as_posix()
except ValueError:
    PROJECT_DOC_PATH = PROJETO.name


def exigir(condicao: bool, mensagem: str) -> None:
    if not condicao:
        raise ValueError(mensagem)


def br(numero: Decimal | int, casas: int = 2) -> str:
    return f"{numero:,.{casas}f}".replace(",", "@REPLACE@").replace(".", ",").replace("@REPLACE@", ".")


def verificar_csv(pasta: Path, config_path: Path) -> dict:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    manifesto = json.loads((pasta / "manifesto.json").read_text(encoding="utf-8"))
    exigir(manifesto["config_sha256"] == hashlib.sha256(config_path.read_bytes()).hexdigest(), "Configuração diverge do manifesto")
    tabelas = {}
    for nome, contrato in manifesto["arquivos"].items():
        p = pasta / nome
        conteudo = p.read_bytes()
        exigir(hashlib.sha256(conteudo).hexdigest() == contrato["sha256"], f"Hash inválido: {nome}")
        exigir(len(conteudo) == contrato["tamanho_bytes"], f"Tamanho inválido: {nome}")
        with p.open(encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        exigir(len(rows) == contrato["contagem"], f"Contagem inválida: {nome}")
        exigir(rows and all(r["simulado"] == "true" for r in rows), f"Simulação sem identificação: {nome}")
        tabelas[nome] = rows
    matriculas = tabelas["matriculas_ead.csv"]
    ids = {r["matricula_id"] for r in matriculas}
    exigir(len(ids) == len(matriculas), "Matrícula duplicada")
    alunos = tabelas["alunos_ead.csv"]
    exigir(len(alunos) == len({r["student_id"] for r in alunos}), "Aluno duplicado")
    exigir({r["student_id"] for r in alunos} == {r["student_id"] for r in matriculas}, "FK aluno inválida")
    for nome in ["financeiro_ead.csv", "engajamento_semanal_ead.csv", "pesquisa_nps_ead.csv"]:
        exigir(all(r["matricula_id"] in ids for r in tabelas[nome]), f"FK matrícula inválida: {nome}")
    e = config["ead"]
    abertura = [r for r in matriculas if r["pertencente_abertura"] == "true"]
    elegiveis = [r for r in matriculas if r["elegivel_churn"] == "true"]
    novas = [r for r in matriculas if r["tipo_coorte"] == "ingressante_2025"]
    counts = Counter(r["status_final"] for r in matriculas)
    exigir(len(abertura) == e["populacao_abertura"], "Abertura divergente")
    exigir(len(elegiveis) == e["populacao_elegivel_churn"], "Elegibilidade divergente")
    exigir(len(novas) == e["novas_matriculas"], "Entradas divergentes")
    exigir(counts == {"ativo": e["ativos_fechamento"], "cancelado": e["saidas_churn"], "concluido": e["conclusoes_coorte_abertura"], "transferido": e["transferencias_coorte_abertura"]}, "Status divergente")
    exigir(len(elegiveis) > 0, "Denominador acadêmico nulo")
    exigir(all((r["elegivel_churn"] == "true") == (r["pertencente_abertura"] == "true" and r["status_final"] in {"ativo", "cancelado"}) for r in matriculas), "Elegibilidade incorreta")
    cancelados = sum(r["status_final"] == "cancelado" for r in elegiveis)
    retidos = sum(r["status_final"] == "ativo" for r in elegiveis)
    churn = Decimal(cancelados) * 100 / len(elegiveis)
    retencao = Decimal(retidos) * 100 / len(elegiveis)
    exigir(churn + retencao == 100, "Churn/retencao não conciliam")
    exigir(len(abertura) - counts["concluido"] - counts["transferido"] - cancelados + len(novas) == counts["ativo"], "Fluxo não concilia")
    financeiro = tabelas["financeiro_ead.csv"]
    exigir(len({r["titulo_id"] for r in financeiro}) == len(financeiro), "Título duplicado")
    exigir(all(int(r["valor_devido_centavos"]) == int(r["valor_pago_centavos"]) + int(r["saldo_aberto_centavos"]) for r in financeiro), "Título não concilia")
    devido = sum(int(r["valor_devido_centavos"]) for r in financeiro)
    pago = sum(int(r["valor_pago_centavos"]) for r in financeiro)
    saldo = sum(int(r["saldo_aberto_centavos"]) for r in financeiro)
    exigir(devido > 0, "Denominador financeiro nulo")
    exigir(saldo == int((Decimal(devido) * Decimal(e["inadimplencia_monetaria_alvo"])).quantize(Decimal("1"), rounding=ROUND_HALF_UP)), "Calibração financeira divergente")
    inadimplencia = Decimal(saldo) * 100 / devido
    sinais = tabelas["engajamento_semanal_ead.csv"]
    por_id = Counter(r["matricula_id"] for r in sinais)
    exigir(set(por_id) == {r["matricula_id"] for r in abertura}, "Cobertura de sinais divergente")
    exigir(all(n == 8 for n in por_id.values()), "Oito janelas obrigatórias")
    exigir(all(r["semana_fim"] <= config["data_corte_sinais"] for r in sinais), "Vazamento temporal nos sinais")
    nps_rows = tabelas["pesquisa_nps_ead.csv"]
    nps_counts = Counter(r["classificacao_nps"] for r in nps_rows)
    exigir(len({r["matricula_id"] for r in nps_rows}) == len(nps_rows), "Resposta NPS duplicada")
    exigir(len(nps_rows) == e["nps_respostas"], "Amostra NPS divergente")
    exigir(nps_counts == {"promotor": e["nps_promotores"], "passivo": e["nps_passivos"], "detrator": e["nps_detratores"]}, "Categorias NPS divergentes")
    nps = Decimal(nps_counts["promotor"] - nps_counts["detrator"]) * 100 / len(nps_rows)
    referencias = tabelas["referencias_segmentos.csv"]
    ref_ead = next(r for r in referencias if r["segmento"] == "Graduacao EAD")
    exigir(churn == Decimal(ref_ead["churn_percentual_referencia"]), "Referência churn não concilia")
    exigir(nps == Decimal(ref_ead["nps_referencia"]), "Referência NPS não concilia")
    exigir(int(ref_ead["ativos_2024"]) == len(abertura) and int(ref_ead["ativos_2025"]) == counts["ativo"], "Referência população não concilia")
    exigir(Decimal(ref_ead["inadimplencia_percentual_referencia"]) == Decimal(e["inadimplencia_monetaria_alvo"]) * 100, "Referência financeira não concilia")
    return locals()


def main(argv=None):
    parser = argparse.ArgumentParser(description="Confere dados fictícios e atualiza relatório de reconciliação")
    parser.add_argument("--data-dir", type=Path, default=ROOT / "dados/csv")
    parser.add_argument("--config", type=Path, default=ROOT / "dados/config.json")
    parser.add_argument("--report", type=Path, default=ROOT / "dados/validacao.md")
    args = parser.parse_args(argv)
    v = verificar_csv(args.data_dir, args.config)
    stream = io.StringIO()
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), pattern="test_dados_gena.py")
    resultado = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    print(stream.getvalue(), end="")
    if not resultado.wasSuccessful():
        raise SystemExit("Falha nos testes: o relatório não foi atualizado como aprovado.")
    counts, e = v["counts"], v["e"]
    linhas = [
        "# Reconciliação e testes — GENA fictícia",
        "",
        f"**Versão {v['config']['versao']} · Cenário de 2025 · Conferência de dados sintéticos**",
        "",
        "[Base e reprodução](README.md) · [Contrato](../docs/contrato-dados.md) · [Dicionário](dicionario.md)",
        "",
        "Esta reconciliação foi recalculada a partir dos CSV. A base é calibrada: o resultado demonstra consistência técnica, não descoberta, execução operacional, validade empírica ou efeito de retenção.",
        "",
        "## População e indicadores acadêmicos",
        "",
        "| Item | Valor calculado |",
        "|:---|---:|",
        f"| Abertura em 01/01/2025 | {br(len(v['abertura']), 0)} |",
        f"| Conclusões separadas | {br(counts['concluido'], 0)} |",
        f"| Transferências externas separadas | {br(counts['transferido'], 0)} |",
        f"| Elegíveis ao churn | {br(len(v['elegiveis']), 0)} |",
        f"| Cancelados elegíveis | {br(v['cancelados'], 0)} |",
        f"| Retidos elegíveis | {br(v['retidos'], 0)} |",
        f"| Novas matrículas | {br(len(v['novas']), 0)} |",
        f"| Ativos no fechamento | {br(counts['ativo'], 0)} |",
        f"| Matrículas distintas no ano | {br(len(v['matriculas']), 0)} |",
        f"| Churn anual da abertura | {br(v['churn'], 1)}% |",
        f"| Retenção anual da abertura | {br(v['retencao'], 1)}% |",
        "",
        "Conclusões/transferências são excluídas retrospectivamente de ambos os denominadores. Os ingressantes estão todos ativos por simplificação; não se estima churn desse grupo.",
        "",
        "## Financeiro na posição de 31/12/2025",
        "",
        "| Item | Valor calculado |",
        "|:---|---:|",
        f"| Títulos vencidos de 2025 | {br(len(v['financeiro']), 0)} |",
        f"| Valor devido | R$ {br(Decimal(v['devido']) / 100)} |",
        f"| Valor pago até o snapshot | R$ {br(Decimal(v['pago']) / 100)} |",
        f"| Saldo aberto | R$ {br(Decimal(v['saldo']) / 100)} |",
        f"| Inadimplência monetária | {br(v['inadimplencia'], 1)}% |",
        f"| Adimplência monetária | {br(100 - v['inadimplencia'], 1)}% |",
        "",
        "Não são média de taxas mensais, receita contábil ou benefício de intervenção. O saldo-alvo é arredondado ao centavo; os títulos incluem o mês da saída, nunca meses posteriores.",
        "",
        "## NPS e cobertura",
        "",
        f"O NPS calculado é **{br(v['nps'], 0)}**, com {len(v['nps_rows'])} respostas únicas: {v['nps_counts']['promotor']} promotores, {v['nps_counts']['passivo']} passivos e {v['nps_counts']['detrator']} detratores. A composição foi calibrada; não é pesquisa real ou estimativa representativa.",
        "",
        f"Há {br(len(v['sinais']), 0)} registros de engajamento nas oito janelas iniciais de 2.880 matrículas. O total institucional de referência é {br(sum(int(r['ativos_2025']) for r in v['referencias']), 0)} ativos; somente EAD possui microdados.",
        "",
        "## Arquivos conferidos",
        "",
        "| Arquivo | Linhas de dados | SHA-256 abreviado |",
        "|:---|---:|:---|",
    ]
    for nome, r in v["manifesto"]["arquivos"].items():
        linhas.append(f"| [{nome}](csv/{nome}) | {br(r['contagem'], 0)} | `{r['sha256'][:16]}…` |")
    linhas += [
        "",
        "Hashes completos e tamanhos estão em [manifesto.json](csv/manifesto.json). A configuração utilizada foi conferida pelo seu hash.",
        "",
        "## Controles executados",
        "",
        f"**{resultado.testsRun} testes automatizados aprovados**, além da conferência dos CSV publicados e do manifesto. Os testes regeneram o cenário em pasta temporária e verificam:",
        "",
        "- Chaves, vínculos, status, populações, fórmulas e emissão de títulos.",
        "- Centavos inteiros, reconciliação de pagamentos e ausência de datas falsas para não pagos.",
        "- Janelas iniciais sem campos de desfecho e invariância dos sinais quando os desfechos são alterados.",
        "- Composição do NPS, referência institucional e identificação de simulação.",
        "- Reprodução byte a byte e rejeição de configuração incoerente.",
        "",
        "Os testes de contrato validam as regras sintéticas, não predizem evasão nem homologam a operação de uma instituição real. Reexecute após qualquer alteração.",
        "",
        "A partir da raiz do repositório, entre na pasta do projeto:",
        "",
        "```bash",
        f"cd {PROJECT_DOC_PATH}",
        "python3 scripts/gerar_dados_gena.py",
        "python3 -m unittest discover -s tests -v",
        "python3 scripts/validar_dados_gena.py",
        "```",
        "",
        "[Testes](../tests/test_dados_gena.py) · [Validador](../scripts/validar_dados_gena.py) · [Registro de mudanças](../docs/registro-mudancas.md)",
        "",
        "**Próxima etapa, ainda não realizada:** análise diagnóstica, consultas SQL, painel e desenho detalhado de avaliação do piloto. Não há resultado de intervenção, ROI ou modelo treinado.",
    ]
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print(f"CSV conferidos e {resultado.testsRun} testes aprovados. Relatório: {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
