#!/usr/bin/env python3
"""Testes isolados dos contratos e da reconciliação didática GENA EAD."""

from __future__ import annotations

import csv
import json
import shutil
import sys
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
SOURCE = ROOT.parent / "retencao-ead" / "dados"
sys.path.insert(0, str(SCRIPTS))

from reconciliar_indicadores import (  # noqa: E402
    ReconciliacaoError,
    _read_csv,
    analisar,
    gerar_comparacao_csv,
    gerar_relatorio,
    validar_elegibilidade,
    _json_bytes,
    _percentual,
    _validate_financeiro,
)


class TestReconciliacao(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = analisar(SOURCE)

    def test_populacao_fk_equacoes_e_unicos(self) -> None:
        population = self.result["populacao"]
        self.assertEqual(population["abertura"], 2880)
        self.assertEqual(population["conclusoes"], 40)
        self.assertEqual(population["transferencias"], 40)
        self.assertEqual(population["elegiveis"], 2800)
        self.assertEqual(population["saidas_cancelamento"], 770)
        self.assertEqual(population["retidos"], 2030)
        self.assertEqual(population["ingressantes"], 1090)
        self.assertEqual(population["ativos_fechamento"], 3120)
        self.assertEqual(population["unicos"], 3970)
        self.assertTrue(population["fk_alunos_matriculas_valida"])
        self.assertTrue(population["ids_unicos"])

    def test_manifesto_config_hash_e_seis_csv(self) -> None:
        integrity = self.result["integridade"]
        self.assertTrue(integrity["config_hash_verificado"])
        self.assertTrue(integrity["manifesto_csv_sha256_verificado"])
        self.assertEqual(integrity["csv_verificados"], 6)
        self.assertEqual(len(integrity["arquivos"]), 6)
        for item in integrity["arquivos"].values():
            self.assertEqual(len(item["sha256"]), 64)
            self.assertGreater(item["contagem"], 0)

    def test_denominador_errado_e_coorte_correta(self) -> None:
        comparison = self.result["comparacao_churn"]
        self.assertEqual(comparison["saidas"], 770)
        self.assertEqual(comparison["denominador_fotografia_ativos_fechamento"], 3120)
        self.assertEqual(comparison["denominador_coorte_elegivel"], 2800)
        self.assertEqual(comparison["percentual_coorte"], Decimal("27.5"))
        self.assertEqual(comparison["percentual_fotografia"], Decimal("24.679487179487179487179487179487179487179487179487"))
        self.assertEqual(comparison["diferenca_pontos_percentuais"], Decimal("2.820512820512820512820512820512820512820512820513"))

    def test_engajamento_metadata_nao_calcula_indicador(self) -> None:
        engagement = self.result["complementares"]["engajamento"]
        self.assertEqual(engagement["linhas"], 23040)
        self.assertEqual(engagement["matriculas"], 2880)
        self.assertEqual(engagement["semanas_por_matricula"], 8)
        self.assertEqual(engagement["janela_inicio"], "2025-01-06")
        self.assertEqual(engagement["janela_fim"], "2025-02-28")
        self.assertTrue(engagement["dominios_validados"])
        self.assertFalse(any(key.startswith("media_") for key in engagement))
        self.assertNotIn("engajamento", self.result["indicadores"])
        self.assertTrue(self.result["complementares"]["engajamento_nao_entra_nos_cinco_indicadores"])

    def test_nps_sem_conversao(self) -> None:
        nps = self.result["indicadores"]["nps"]
        self.assertEqual((nps["respostas"], nps["promotores"], nps["passivos"], nps["detratores"], nps["valor"]), (200, 118, 42, 40, 39))
        conversion = self.result["conversao"]
        self.assertEqual(conversion["status"], "nao_calculada")
        self.assertFalse(conversion["testada"])
        self.assertIn("CRM", conversion["motivo"])

    def test_objeto_positivo_tem_exatamente_cinco_defs_e_faixas(self) -> None:
        indicators = self.result["indicadores"]
        self.assertEqual(
            set(indicators),
            {"churn", "retencao", "inadimplencia_monetaria", "adimplencia_monetaria", "nps"},
        )
        for name in ("churn", "retencao", "inadimplencia_monetaria", "adimplencia_monetaria"):
            self.assertGreaterEqual(indicators[name]["percentual"], Decimal("0"))
            self.assertLessEqual(indicators[name]["percentual"], Decimal("100"))
        self.assertEqual(indicators["churn"]["percentual"] + indicators["retencao"]["percentual"], Decimal("100"))
        self.assertEqual(indicators["inadimplencia_monetaria"]["percentual"] + indicators["adimplencia_monetaria"]["percentual"], Decimal("100"))
        self.assertGreaterEqual(indicators["nps"]["valor"], -100)
        self.assertLessEqual(indicators["nps"]["valor"], 100)
        self.assertTrue(self.result["ficcionalidade"]["dados_inteiramente_ficticios"])

    def test_bytes_de_dois_outputs_sao_reprodutiveis(self) -> None:
        first = dict(self.result)
        second = dict(self.result)
        first["execucao"] = {"testes_executados": 12, "resultado_testes": "OK", "referencia_dados": "2025-12-31"}
        second["execucao"] = {"testes_executados": 12, "resultado_testes": "OK", "referencia_dados": "2025-12-31"}
        with tempfile.TemporaryDirectory() as temp:
            left = Path(temp) / "left"
            right = Path(temp) / "right"
            left.mkdir()
            right.mkdir()
            for directory, value in ((left, first), (right, second)):
                (directory / "comparacao-churn.csv").write_bytes(gerar_comparacao_csv(value))
                (directory / "resultado-reconciliacao.json").write_bytes(_json_bytes(value))
                (directory / "reconciliacao.md").write_bytes(gerar_relatorio(value, 10))
            for name in ("comparacao-churn.csv", "resultado-reconciliacao.json", "reconciliacao.md"):
                self.assertEqual((left / name).read_bytes(), (right / name).read_bytes(), name)

    def test_hash_corrompido_e_rejeitado(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            copy = Path(temp) / "dados"
            shutil.copytree(SOURCE, copy)
            path = copy / "csv" / "matriculas_ead.csv"
            path.write_bytes(path.read_bytes() + b"\n")
            with self.assertRaises(ReconciliacaoError):
                analisar(copy)

    def test_flag_elegibilidade_divergente_e_rejeitada(self) -> None:
        rows = _read_csv(SOURCE / "csv" / "matriculas_ead.csv")
        rows[0] = dict(rows[0])
        rows[0]["elegivel_churn"] = "false"
        with self.assertRaises(ReconciliacaoError):
            validar_elegibilidade(rows)

    def test_financeiro_round_half_up_e_defs_calculadas_da_base(self) -> None:
        financial = self.result["indicadores"]["inadimplencia_monetaria"]
        paid = self.result["indicadores"]["adimplencia_monetaria"]
        self.assertEqual(financial["saldo_aberto_centavos"], 157950270)
        self.assertEqual(financial["total_devido_centavos"], 1170002000)
        self.assertEqual(financial["percentual"], Decimal("13.5"))
        self.assertEqual(paid["percentual"], Decimal("86.5"))
        self.assertEqual(financial["arredondamento"], "ROUND_HALF_UP")

    def test_denominador_zero_e_rejeitado(self) -> None:
        with self.assertRaises(ReconciliacaoError):
            _percentual(1, 0)

    def test_titulo_com_vencimento_futuro_e_rejeitado_antes_dos_valores(self) -> None:
        rows = _read_csv(SOURCE / "csv" / "financeiro_ead.csv")
        rows[0] = dict(rows[0])
        rows[0]["vencimento"] = "2026-01-10"
        config = json.loads((SOURCE / "config.json").read_text(encoding="utf-8"))
        matricula_ids = {row["matricula_id"] for row in _read_csv(SOURCE / "csv" / "matriculas_ead.csv")}
        with self.assertRaises(ReconciliacaoError):
            _validate_financeiro(config, rows, matricula_ids)


if __name__ == "__main__":
    unittest.main()
