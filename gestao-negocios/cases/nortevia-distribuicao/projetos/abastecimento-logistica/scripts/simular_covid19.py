#!/usr/bin/env python3
"""Gera resultados aritméticos de uma simulação didática, sem inferência causal."""
from __future__ import annotations

import csv
import json
import sys
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path
from typing import Any

PROJECT_DIR = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_DIR / "dados" / "covid19_config.json"
OUTPUT_PATH = PROJECT_DIR / "dados" / "covid19_resultados.csv"
EXPECTED_BRANCHES = ("sem pacote coordenado", "com pacote hipotético")
CSV_FIELDS = (
    "schema_version",
    "metric_id",
    "metric_name",
    "branch",
    "numerator",
    "denominator",
    "unit",
    "value",
    "comparison_delta",
    "comparison_delta_unit",
    "comparison_relative_pct",
)


def as_decimal(value: Any, label: str) -> Decimal:
    """Converte número textual em Decimal finito e não negativo."""
    try:
        number = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError) as exc:
        raise ValueError(f"{label}: valor numérico inválido: {value!r}") from exc
    if not number.is_finite():
        raise ValueError(f"{label}: valor precisa ser finito")
    if number < 0:
        raise ValueError(f"{label}: valor não pode ser negativo")
    return number


def quantize(value: Decimal, precision: int) -> Decimal:
    quantum = Decimal(1).scaleb(-precision)
    return value.quantize(quantum, rounding=ROUND_HALF_UP)


def format_decimal(value: Decimal, precision: int) -> str:
    return f"{quantize(value, precision):.{precision}f}"


def validate_config(config: dict[str, Any]) -> None:
    case = config.get("case", {})
    branches = case.get("branches")
    if not isinstance(branches, list) or tuple(branches) != EXPECTED_BRANCHES:
        raise ValueError("Os dois ramos devem ser, nesta ordem: " + " e ".join(EXPECTED_BRANCHES))
    cohort = case.get("cohort", {})
    if cohort.get("planned_orders") != 100 or cohort.get("denominator_fixed") is not True:
        raise ValueError("A coorte deve manter denominador fixo de 100 pedidos planejados")
    metrics = config.get("metrics")
    if not isinstance(metrics, list) or not metrics:
        raise ValueError("A configuração precisa conter métricas")
    ids: set[str] = set()
    for metric in metrics:
        metric_id = metric.get("id")
        if not metric_id or metric_id in ids:
            raise ValueError(f"ID de métrica ausente ou duplicado: {metric_id!r}")
        ids.add(metric_id)
        precision = metric.get("precision")
        if not isinstance(precision, int) or not 0 <= precision <= 6:
            raise ValueError(f"{metric_id}: precisão inválida")
        if metric.get("kind") not in {"proportion", "ratio"}:
            raise ValueError(f"{metric_id}: tipo de métrica inválido")
        metric_branches = metric.get("branches", {})
        if set(metric_branches) != set(EXPECTED_BRANCHES):
            raise ValueError(f"{metric_id}: cada ramo esperado precisa estar presente")
        expected_denominator = as_decimal(metric["denominator"]["value"], f"{metric_id}.denominator")
        if expected_denominator <= 0:
            raise ValueError(f"{metric_id}: denominador precisa ser positivo")
        for branch in EXPECTED_BRANCHES:
            item = metric_branches[branch]
            numerator = as_decimal(item.get("numerator"), f"{metric_id}.{branch}.numerator")
            denominator = as_decimal(item.get("denominator"), f"{metric_id}.{branch}.denominator")
            if denominator <= 0:
                raise ValueError(f"{metric_id}.{branch}: denominador precisa ser positivo")
            if denominator != expected_denominator:
                raise ValueError(f"{metric_id}.{branch}: denominador diverge da definição fixa")
            if metric["kind"] == "proportion" and numerator > denominator:
                raise ValueError(f"{metric_id}.{branch}: numerador da proporção excede o denominador")


def build_rows(config: dict[str, Any]) -> list[dict[str, str]]:
    validate_config(config)
    rows: list[dict[str, str]] = []
    for metric in config["metrics"]:
        precision = metric["precision"]
        computed: dict[str, tuple[Decimal, Decimal, Decimal, Decimal]] = {}
        for branch in EXPECTED_BRANCHES:
            item = metric["branches"][branch]
            numerator = Decimal(str(item["numerator"]))
            denominator = Decimal(str(item["denominator"]))
            value = numerator / denominator
            if metric["kind"] == "proportion":
                value *= Decimal(100)
            computed[branch] = (numerator, denominator, value, value)
        base_value = computed[EXPECTED_BRANCHES[0]][2]
        package_value = computed[EXPECTED_BRANCHES[1]][2]
        delta = package_value - base_value
        if metric["kind"] == "proportion":
            delta_unit = "p.p."
            relative_pct = ""
        else:
            delta_unit = metric["unit"]
            relative_pct = format_decimal(delta / base_value * Decimal(100), 2) if base_value else ""

        for branch in EXPECTED_BRANCHES:
            numerator, denominator, value, _ = computed[branch]
            rows.append(
                {
                    "schema_version": str(config["schema_version"]),
                    "metric_id": metric["id"],
                    "metric_name": metric["name"],
                    "branch": branch,
                    "numerator": format_decimal(numerator, 2) if metric["kind"] == "ratio" else format_decimal(numerator, 0),
                    "denominator": format_decimal(denominator, 2) if metric["kind"] == "ratio" else format_decimal(denominator, 0),
                    "unit": metric["unit"],
                    "value": format_decimal(value, precision),
                    "comparison_delta": format_decimal(delta, precision),
                    "comparison_delta_unit": delta_unit,
                    "comparison_relative_pct": relative_pct,
                }
            )
    return rows


def render_csv(rows: list[dict[str, str]]) -> str:
    from io import StringIO

    output = StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=CSV_FIELDS, lineterminator="\n", extrasaction="raise")
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


def generate(config_path: Path = CONFIG_PATH, output_path: Path = OUTPUT_PATH) -> str:
    with config_path.open(encoding="utf-8") as source:
        config = json.load(source, parse_float=Decimal)
    csv_text = render_csv(build_rows(config))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(csv_text, encoding="utf-8", newline="")
    return csv_text


def main() -> int:
    try:
        generate()
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"Erro ao gerar simulação: {exc}", file=sys.stderr)
        return 1
    print(f"CSV gerado: {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
