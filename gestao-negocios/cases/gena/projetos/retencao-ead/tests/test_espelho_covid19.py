import json
import tempfile
import unittest
from pathlib import Path

from scripts.simular_espelho_covid19 import (
    DEFAULT_CONFIG,
    DEFAULT_OUTPUT,
    build_rows,
    generate,
    load_config,
)


class EspelhoCovid19Tests(unittest.TestCase):
    def setUp(self):
        self.config = load_config(DEFAULT_CONFIG)
        self.rows = {row["metric_key"]: row for row in build_rows(self.config)}

    def test_config_explicitly_marks_2020_scenario_as_fictional(self):
        self.assertEqual(self.config["status"], "simulacao_ficticia")
        self.assertEqual(self.config["scenario_id"], "gena-covid19-2020")
        self.assertEqual(self.config["cohort_size"], 1000)
        self.assertEqual(self.config["horizon_weeks"], 8)
        self.assertEqual(self.config["horizon_days"], 56)
        self.assertEqual(
            set(self.config["branches"]),
            {"without_coordinated_package", "with_hypothetical_package"},
        )

    def test_each_metric_declares_definition_maturity_and_limits(self):
        self.assertEqual(len(self.config["metrics"]), 6)
        for metric in self.config["metrics"]:
            with self.subTest(metric=metric["key"]):
                self.assertTrue(metric.get("definition"))
                self.assertTrue(metric.get("maturity_rule"))
                self.assertTrue(metric.get("interpretation_limit"))

    def test_expected_rates_and_percentage_point_changes(self):
        expected = {
            "lesson_continuity": ("58.00", "90.00", "32.00"),
            "recurring_engagement": ("62.00", "76.00", "14.00"),
            "access_support": ("20.00", "75.00", "55.00"),
            "support_sla": ("30.00", "80.00", "50.00"),
            "financial_response_sla": ("30.00", "80.00", "50.00"),
            "cancellations_8_weeks": ("12.00", "9.00", "-3.00"),
        }
        for key, values in expected.items():
            with self.subTest(metric=key):
                row = self.rows[key]
                self.assertEqual(
                    (
                        row["rate_without_package_pct"],
                        row["rate_with_hypothetical_package_pct"],
                        row["difference_percentage_points"],
                    ),
                    values,
                )

    def test_cancellation_relative_change_is_not_percentage_points(self):
        row = self.rows["cancellations_8_weeks"]
        self.assertEqual(row["relative_change_pct"], "-25.00")
        self.assertEqual(row["difference_percentage_points"], "-3.00")

    def test_invalid_numerator_is_rejected(self):
        broken = json.loads(json.dumps(self.config))
        broken["branches"]["with_hypothetical_package"]["lessons_delivered"] = 301
        with self.assertRaises(ValueError):
            build_rows(broken)

    def test_output_is_byte_reproducible(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            first = Path(temp_dir) / "first.csv"
            second = Path(temp_dir) / "second.csv"
            generate(DEFAULT_CONFIG, first)
            generate(DEFAULT_CONFIG, second)
            self.assertEqual(first.read_bytes(), second.read_bytes())

    def test_versioned_csv_matches_generator(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            generated = Path(temp_dir) / "generated.csv"
            generate(DEFAULT_CONFIG, generated)
            self.assertEqual(generated.read_bytes(), DEFAULT_OUTPUT.read_bytes())


if __name__ == "__main__":
    unittest.main()
