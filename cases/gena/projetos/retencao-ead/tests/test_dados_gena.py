"""Testes de contrato dos dados fictícios, sem bibliotecas externas.

Rodar na pasta do projeto de Retenção EAD: python3 -m unittest discover -s tests -v
Testar dados calibrados demonstra consistência, não validação empírica.
"""
from __future__ import annotations

import copy
import csv
import hashlib
import json
import sys
import tempfile
import unittest
from collections import Counter, defaultdict
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import gerar_dados_gena as gerador


def ler_csv(pasta: Path, nome: str) -> list[dict[str, str]]:
    with (pasta / nome).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


class ContratoGENA(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.pasta = Path(cls.tmp.name) / "base"
        cls.config_path = ROOT / "dados/config.json"
        cls.config = json.loads(cls.config_path.read_text())
        cls.manifesto = gerador.generate(cls.config_path, cls.pasta)
        cls.tabelas = {nome: ler_csv(cls.pasta, nome) for nome in gerador.CSV_NAMES}
        cls.matriculas = {r["matricula_id"]: r for r in cls.tabelas["matriculas_ead.csv"]}

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_01_chaves_unicas_e_integridade_referencial(self):
        pks = {"alunos_ead.csv": "student_id", "matriculas_ead.csv": "matricula_id",
               "financeiro_ead.csv": "titulo_id", "pesquisa_nps_ead.csv": "resposta_id",
               "referencias_segmentos.csv": "segmento"}
        for nome, pk in pks.items():
            linhas = self.tabelas[nome]
            self.assertTrue(all(r[pk] for r in linhas))
            self.assertEqual(len(linhas), len({r[pk] for r in linhas}), nome)
        alunos = {r["student_id"]: r for r in self.tabelas["alunos_ead.csv"]}
        self.assertEqual(len(alunos), len(self.matriculas))
        self.assertEqual(set(alunos), {r["student_id"] for r in self.matriculas.values()})
        for r in self.matriculas.values():
            a = alunos[r["student_id"]]
            self.assertEqual(r["curso"], a["curso"])
            self.assertEqual(r["polo"], a["polo"])
            self.assertEqual(r["tipo_coorte"], a["tipo_coorte"])
            self.assertLessEqual(date.fromisoformat(a["data_admissao"]), date.fromisoformat(r["data_inicio"]))
        for nome in ["financeiro_ead.csv", "engajamento_semanal_ead.csv", "pesquisa_nps_ead.csv"]:
            self.assertTrue(all(r["matricula_id"] in self.matriculas for r in self.tabelas[nome]), nome)

    def test_02_status_e_equacao_da_populacao(self):
        e = self.config["ead"]
        rows = list(self.matriculas.values())
        abertura = [r for r in rows if r["pertencente_abertura"] == "true"]
        novas = [r for r in rows if r["tipo_coorte"] == "ingressante_2025"]
        elegiveis = [r for r in rows if r["elegivel_churn"] == "true"]
        status = Counter(r["status_final"] for r in rows)
        self.assertEqual(status, {"ativo": e["ativos_fechamento"], "cancelado": e["saidas_churn"],
                                 "concluido": e["conclusoes_coorte_abertura"], "transferido": e["transferencias_coorte_abertura"]})
        self.assertEqual(len(abertura), e["populacao_abertura"])
        self.assertEqual(len(novas), e["novas_matriculas"])
        self.assertEqual(len(elegiveis), e["populacao_elegivel_churn"])
        self.assertEqual(len(rows), len(abertura) + len(novas))
        self.assertEqual(len(abertura) - status["concluido"] - status["transferido"] - status["cancelado"] + len(novas), status["ativo"])
        for r in rows:
            esperado = r["pertencente_abertura"] == "true" and r["status_final"] in {"ativo", "cancelado"}
            self.assertEqual(r["elegivel_churn"] == "true", esperado)
        self.assertTrue(all(r["status_final"] == "ativo" and r["pertencente_abertura"] == "false" for r in novas))
        churn = Decimal(sum(r["status_final"] == "cancelado" for r in elegiveis)) / len(elegiveis)
        retencao = Decimal(sum(r["status_final"] == "ativo" for r in elegiveis)) / len(elegiveis)
        referencia = next(r for r in self.config["segmentos_referencia"] if r["segmento"] == "Graduacao EAD")
        self.assertEqual(churn * 100, Decimal(referencia["churn_percentual_referencia"]))
        self.assertEqual(churn + retencao, 1)

    def test_03_datas_de_entrada_saida_e_conclusao(self):
        alunos = {r["student_id"]: r for r in self.tabelas["alunos_ead.csv"]}
        for r in self.matriculas.values():
            inicio = date.fromisoformat(r["data_inicio"])
            if r["pertencente_abertura"] == "true":
                self.assertEqual(inicio, date(2025, 1, 1))
            else:
                self.assertEqual(inicio.year, 2025)
                self.assertIn(inicio.month, range(3, 12))
            if r["status_final"] == "ativo":
                self.assertEqual(r["data_saida"], "")
                self.assertEqual(r["motivo_saida"], "")
            else:
                saida = date.fromisoformat(r["data_saida"])
                self.assertLessEqual(inicio, saida)
                self.assertGreater(saida, date(2025, 2, 28))
                self.assertLessEqual(saida, date(2025, 12, 31))
                self.assertIn(saida.month, range(4, 13))
                self.assertGreaterEqual(saida.day, 15)
            if r["status_final"] == "concluido":
                self.assertTrue(alunos[r["student_id"]]["data_admissao"].startswith("2022-"))
            if r["status_final"] == "cancelado":
                self.assertIn(r["motivo_saida"], {"financeiro", "academico", "pessoal", "nao_informado"})

    def test_04_competencias_e_emissao_financeira(self):
        por_matricula = defaultdict(list)
        for r in self.tabelas["financeiro_ead.csv"]:
            por_matricula[r["matricula_id"]].append(r)
            ano, mes = map(int, r["competencia"].split("-"))
            self.assertEqual(ano, 2025)
            self.assertEqual(r["vencimento"], date(ano, mes, 10).isoformat())
            self.assertLessEqual(date.fromisoformat(r["vencimento"]), date(2025, 12, 31))
        self.assertEqual(set(por_matricula), set(self.matriculas))
        for mid, rows in por_matricula.items():
            m = self.matriculas[mid]
            inicio = date.fromisoformat(m["data_inicio"]).month
            fim = date.fromisoformat(m["data_saida"]).month if m["data_saida"] else 12
            esperado = {f"2025-{mes:02d}" for mes in range(inicio, fim + 1)}
            self.assertEqual({r["competencia"] for r in rows}, esperado)
            self.assertEqual(len(rows), len(esperado))
            self.assertLessEqual(len(rows), 12)

    def test_05_valores_monetarios_e_posicao(self):
        rows = self.tabelas["financeiro_ead.csv"]
        devido = pago = saldo = 0
        for r in rows:
            d, p, s = (int(r[k]) for k in ["valor_devido_centavos", "valor_pago_centavos", "saldo_aberto_centavos"])
            self.assertEqual(d, self.config["ead"]["ticket_mensal_centavos"])
            self.assertGreaterEqual(p, 0)
            self.assertGreaterEqual(s, 0)
            self.assertEqual(d, p + s)
            self.assertEqual(r["posicao_financeira2025-12-31"], "aberto" if s else "liquidado")
            if p == 0:
                self.assertEqual(r["data_pagamento"], "")
            else:
                dp = date.fromisoformat(r["data_pagamento"])
                self.assertLessEqual(dp, date(2025, 12, 31))
                self.assertGreaterEqual(dp, date.fromisoformat(r["competencia"] + "-01"))
            devido += d
            pago += p
            saldo += s
        alvo = int((Decimal(devido) * Decimal(self.config["ead"]["inadimplencia_monetaria_alvo"])).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
        self.assertEqual(saldo, alvo)
        self.assertEqual(devido, pago + saldo)

    def test_06_janelas_de_engajamento_sem_vazamento(self):
        rows = self.tabelas["engajamento_semanal_ead.csv"]
        esperado = {mid for mid, m in self.matriculas.items() if m["pertencente_abertura"] == "true"}
        contagens = Counter(r["matricula_id"] for r in rows)
        self.assertEqual(set(contagens), esperado)
        self.assertTrue(all(n == 8 for n in contagens.values()))
        self.assertEqual(len({(r["matricula_id"], r["semana_inicio"]) for r in rows}), len(rows))
        for r in rows:
            inicio, fim = date.fromisoformat(r["semana_inicio"]), date.fromisoformat(r["semana_fim"])
            self.assertGreaterEqual(inicio, date(2025, 1, 6))
            self.assertLessEqual(fim, date(2025, 2, 28))
            self.assertLessEqual(inicio, fim)
            self.assertTrue(0 <= int(r["dias_com_acesso"]) <= (fim - inicio).days + 1)
            self.assertTrue(0 <= int(r["atividades_entregues"]) <= int(r["atividades_previstas"]))
            self.assertGreater(int(r["atividades_previstas"]), 0)
        proibidas = {"status_final", "data_saida", "motivo_saida", "elegivel_churn", "nota", "saldo_aberto_centavos"}
        self.assertFalse(proibidas & set(rows[0]))

    def test_07_engajamento_nao_usa_desfecho(self):
        alteradas = copy.deepcopy(list(self.matriculas.values()))
        for r in alteradas:
            r["status_final"] = "cancelado"
            r["data_saida"] = "2025-04-20"
            r["motivo_saida"] = "financeiro"
        sinais = gerador._build_engajamento(self.config, alteradas)
        self.assertEqual(sinais, self.tabelas["engajamento_semanal_ead.csv"])

    def test_08_nps_amostra_e_classificacao(self):
        rows = self.tabelas["pesquisa_nps_ead.csv"]
        e = self.config["ead"]
        self.assertEqual(len(rows), e["nps_respostas"])
        self.assertEqual(len({r["matricula_id"] for r in rows}), len(rows))
        counts = Counter(r["classificacao_nps"] for r in rows)
        self.assertEqual(counts, {"promotor": e["nps_promotores"], "passivo": e["nps_passivos"], "detrator": e["nps_detratores"]})
        for r in rows:
            nota = int(r["nota"])
            self.assertTrue(0 <= nota <= 10)
            self.assertEqual(r["classificacao_nps"], "promotor" if nota >= 9 else "passivo" if nota >= 7 else "detrator")
            m = self.matriculas[r["matricula_id"]]
            self.assertEqual(m["status_final"], "ativo")
            self.assertGreaterEqual(date.fromisoformat(r["data_pesquisa"]), date.fromisoformat(m["data_inicio"]))
        referencia = next(r for r in self.config["segmentos_referencia"] if r["segmento"] == "Graduacao EAD")
        self.assertEqual(Decimal(counts["promotor"] - counts["detrator"]) * 100 / len(rows), referencia["nps_referencia"])

    def test_09_referencias_macro_e_total(self):
        rows = self.tabelas["referencias_segmentos.csv"]
        self.assertEqual(len(rows), 4)
        self.assertEqual(sum(int(r["ativos_2025"]) for r in rows), 10040)
        self.assertEqual(sum(int(r["ativos_2024"]) for r in rows), 9580)
        ead = next(r for r in rows if r["segmento"] == "Graduacao EAD")
        self.assertEqual(int(ead["ativos_2024"]), self.config["ead"]["populacao_abertura"])
        self.assertEqual(int(ead["ativos_2025"]), sum(r["status_final"] == "ativo" for r in self.matriculas.values()))
        self.assertEqual(Decimal(ead["inadimplencia_percentual_referencia"]), Decimal(self.config["ead"]["inadimplencia_monetaria_alvo"]) * 100)
        self.assertEqual({r["curso"] for r in self.matriculas.values()}, set(self.config["ead"]["cursos"]))
        self.assertEqual({r["polo"] for r in self.matriculas.values()}, set(self.config["ead"]["polos"]))

    def test_10_sem_dados_pessoais_e_simulacao_explicita(self):
        proibidos = {"nome", "cpf", "rg", "email", "telefone", "endereco", "data_nascimento"}
        for nome, rows in self.tabelas.items():
            self.assertFalse(proibidos & set(rows[0]), nome)
            self.assertTrue(all(r["simulado"] == "true" for r in rows), nome)
        for p in self.pasta.glob("*"):
            self.assertTrue(p.read_bytes().endswith(b"\n"))

    def test_11_manifesto_e_hashes(self):
        m = self.manifesto
        self.assertEqual(m["config_sha256"], hashlib.sha256(self.config_path.read_bytes()).hexdigest())
        for nome in gerador.CSV_NAMES:
            b = (self.pasta / nome).read_bytes()
            self.assertEqual(m["sha256"][nome], hashlib.sha256(b).hexdigest())
            self.assertEqual(m["contagens"][nome], len(self.tabelas[nome]))
            self.assertEqual(m["sizes"][nome], len(b))

    def test_12_reproducibilidade_byte_a_byte(self):
        outra = Path(self.tmp.name) / "reproducao"
        gerador.generate(self.config_path, outra)
        for nome in gerador.CSV_NAMES + ["manifesto.json"]:
            self.assertEqual((self.pasta / nome).read_bytes(), (outra / nome).read_bytes(), nome)

    def test_13_configuracao_inconsistente_e_rejeitada(self):
        ruim = copy.deepcopy(self.config)
        ruim["ead"]["populacao_elegivel_churn"] += 1
        cfg = Path(self.tmp.name) / "config-invalida.json"
        cfg.write_text(json.dumps(ruim))
        with self.assertRaises(gerador.ConfigError):
            gerador.generate(cfg, Path(self.tmp.name) / "nao-deve-gerar")
        self.assertFalse((Path(self.tmp.name) / "nao-deve-gerar").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
