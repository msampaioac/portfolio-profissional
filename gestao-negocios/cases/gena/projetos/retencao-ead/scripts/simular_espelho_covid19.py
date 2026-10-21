#!/usr/bin/env python3
"""Gera taxas descritivas a partir de premissas explícitas de um cenário fictício."""

from __future__ import annotations

import argparse
import csv
import json
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Any

PROJECT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = PROJECT_DIR / "dados" / "covid19_config.json"
DEFAULT_OUTPUT = PROJECT_DIR / "dados" / "covid19_espelho_resultados.csv"
BRANCHES = ("without_coordinated_package", "with_hypothetical_package")


def _percent(numerator: int, denominator: int) -> Decimal:
    if denominator <= 0:
        raise ValueError("O denominador precisa ser positivo.")
    return (Decimal(numerator) * Decimal("100") / Decimal(denominator)).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )


def load_config(path: Path = DEFAULT_CONFIG) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        config = json.load(handle)
    if config.get("status") != "simulacao_ficticia":
        raise ValueError("O cenário precisa estar explicitamente marcado como simulação fictícia.")
    scenario_id = str(config.get("scenario_id", ""))
    if "covid19" not in scenario_id.lower() or "2020" not in scenario_id:
        raise ValueError("O identificador precisa indicar a simulação COVID-19 de 2020.")
    weeks = int(config.get("horizon_weeks", 0))
    days = int(config.get("horizon_days", 0))
    if weeks <= 0 or int(config.get("cohort_size", 0)) <= 0 or days != weeks * 7:
        raise ValueError("Coorte e horizonte precisam ser positivos e consistentes em semanas/dias.")
    if set(config.get("branches", {})) != set(BRANCHES):
        raise ValueError("A configuração deve conter os dois ramos hipotéticos definidos.")
    return config


def build_rows(config: dict[str, Any]) -> list[dict[str, str]]:
    denominators = {**config.get("denominators", {}), "cohort_size": config["cohort_size"]}
    rows: list[dict[str, str]] = []
    for metric in config["metrics"]:
        denominator_key = metric["denominator"]
        if denominator_key not in denominators:
            raise ValueError(f"Denominador ausente: {denominator_key}")
        denominator = int(denominators[denominator_key])
        if denominator <= 0:
            raise ValueError(f"Denominador não positivo para {metric['key']}.")
        numerators: dict[str, int] = {}
        rates: dict[str, Decimal] = {}
        for branch in BRANCHES:
            numerator = int(config["branches"][branch][metric["numerator"]])
            if numerator < 0 or numerator > denominator:
                raise ValueError(f"Numerador inválido para {metric['key']} em {branch}.")
            numerators[branch] = numerator
            rates[branch] = _percent(numerator, denominator)

        numerator_delta = numerators[BRANCHES[1]] - numerators[BRANCHES[0]]
        delta_pp = (Decimal(numerator_delta) * Decimal("100") / Decimal(denominator)).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        relative_change = (
            Decimal(numerator_delta) * Decimal("100") / Decimal(numerators[BRANCHES[0]])
            if numerators[BRANCHES[0]] != 0
            else None
        )
        rows.append(
            {
                "scenario_id": str(config["scenario_id"]),
                "status": str(config["status"]),
                "metric_key": str(metric["key"]),
                "metric_label": str(metric["label"]),
                "direction": str(metric["direction"]),
                "numerator_without_package": str(numerators[BRANCHES[0]]),
                "denominator": str(denominator),
                "rate_without_package_pct": f"{rates[BRANCHES[0]]:.2f}",
                "numerator_with_hypothetical_package": str(numerators[BRANCHES[1]]),
                "rate_with_hypothetical_package_pct": f"{rates[BRANCHES[1]]:.2f}",
                "difference_percentage_points": f"{delta_pp:.2f}",
                "relative_change_pct": f"{relative_change.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP):.2f}" if relative_change is not None else "",
            }
        )
    return rows


def generate(config_path: Path = DEFAULT_CONFIG, output_path: Path = DEFAULT_OUTPUT) -> list[dict[str, str]]:
    config = load_config(config_path)
    rows = build_rows(config)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    rows = generate(args.config, args.output)
    print(f"Geradas {len(rows)} métricas de ramos hipotéticos em {args.output}")
    print("Isto reproduz premissas declaradas; não mede resultados nem efeito causal.")


if __name__ == "__main__":
    main()
