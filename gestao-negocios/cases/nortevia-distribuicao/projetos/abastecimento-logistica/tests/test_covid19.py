from __future__ import annotations

import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR / "scripts"))

import simular_covid19 as sim  # noqa: E402


class SimulacaoCovid19Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        with (PROJECT_DIR / "dados" / "covid19_config.json").open(encoding="utf-8") as source:
            cls.config = json.load(source)
        cls.rows = sim.build_rows(cls.config)
        cls.by_key = {(row["metric_id"], row["branch"]): row for row in cls.rows}

    def test_valores_exatos_e_denominadores(self) -> None:
        expected = {
            "otif": (("62", "100", "62.0"), ("82", "100", "82.0")),
            "fill_rate": (("8000", "10000", "80.0"), ("9100", "10000", "91.0")),
            "disponibilidade_skus": (("250", "400", "62.5"), ("340", "400", "85.0")),
            "perda_avaria_validade": (("35", "1000", "3.5"), ("20", "1000", "2.0")),
            "custo_transporte_por_pedido": (("9200.00", "100.00", "92.00"), ("8400.00", "100.00", "84.00")),
            "contas_vencidas_30d": (("220000", "1000000", "22.0"), ("150000", "1000000", "15.0")),
        }
        branches = sim.EXPECTED_BRANCHES
        for metric_id, branch_values in expected.items():
            for branch, (numerator, denominator, value) in zip(branches, branch_values):
                row = self.by_key[(metric_id, branch)]
                self.assertEqual((row["numerator"], row["denominator"], row["value"]), (numerator, denominator, value))

    def test_proporcoes_comparam_em_pontos_percentuais_nao_percentual_relativo(self) -> None:
        expected = {
            "otif": "20.0",
            "fill_rate": "11.0",
            "disponibilidade_skus": "22.5",
            "perda_avaria_validade": "-1.5",
            "contas_vencidas_30d": "-7.0",
        }
        for metric_id, delta in expected.items():
            row = self.by_key[(metric_id, sim.EXPECTED_BRANCHES[0])]
            self.assertEqual(row["comparison_delta"], delta)
            self.assertEqual(row["comparison_delta_unit"], "p.p.")
            self.assertEqual(row["comparison_relative_pct"], "")

    def test_custo_tem_delta_absoluto_e_relativo_separados(self) -> None:
        row = self.by_key[("custo_transporte_por_pedido", sim.EXPECTED_BRANCHES[0])]
        self.assertEqual(row["comparison_delta"], "-8.00")
        self.assertEqual(row["comparison_delta_unit"], "BRL/pedido planejado")
        self.assertEqual(row["comparison_relative_pct"], "-8.70")

    def test_rejeita_numerador_de_proporcao_acima_do_denominador(self) -> None:
        config = json.loads(json.dumps(self.config))
        config["metrics"][0]["branches"][sim.EXPECTED_BRANCHES[0]]["numerator"] = "101"
        with self.assertRaisesRegex(ValueError, "excede o denominador"):
            sim.build_rows(config)

    def test_rejeita_denominador_zero_e_valores_invalidos(self) -> None:
        config = json.loads(json.dumps(self.config))
        config["metrics"][0]["branches"][sim.EXPECTED_BRANCHES[0]]["denominator"] = "0"
        with self.assertRaisesRegex(ValueError, "positivo"):
            sim.build_rows(config)
        with self.assertRaisesRegex(ValueError, "inválido"):
            sim.as_decimal("não-numérico", "teste")
        with self.assertRaisesRegex(ValueError, "negativo"):
            sim.as_decimal("-1", "teste")

    def test_rejeita_nomes_de_ramos_diferentes_dos_do_contrato(self) -> None:
        config = json.loads(json.dumps(self.config))
        config["case"]["branches"] = ["antes", "depois"]
        with self.assertRaisesRegex(ValueError, "dois ramos"):
            sim.build_rows(config)

    def test_csv_versionado_estavel_e_identico_ao_artefato(self) -> None:
        first = sim.render_csv(sim.build_rows(self.config))
        second = sim.render_csv(sim.build_rows(self.config))
        self.assertEqual(first, second)
        self.assertTrue(first.endswith("\n"))
        self.assertNotIn("\r\n", first)
        versioned = list(csv.DictReader(first.splitlines()))
        self.assertEqual(len(versioned), 12)
        self.assertTrue(all(row["schema_version"] == "1.0" for row in versioned))
        artifact = (PROJECT_DIR / "dados" / "covid19_resultados.csv").read_text(encoding="utf-8")
        self.assertEqual(artifact, first)
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "resultados.csv"
            generated = sim.generate(PROJECT_DIR / "dados" / "covid19_config.json", output)
            self.assertEqual(generated, first)
            self.assertEqual(output.read_bytes(), (PROJECT_DIR / "dados" / "covid19_resultados.csv").read_bytes())


if __name__ == "__main__":
    unittest.main()
