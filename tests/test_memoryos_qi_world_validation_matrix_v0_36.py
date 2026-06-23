from __future__ import annotations

from copy import deepcopy
import unittest

from scripts import check_memoryos_qi_world_validation_matrix_v0_36 as checker


class MemoryOSQiWorldValidationMatrixV036Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.matrix = checker.load_json(checker.MATRIX_PATH)
        self.cases = checker.load_json(checker.CASES_PATH)

    def test_matrix_is_valid(self) -> None:
        self.assertEqual(checker.validate_matrix(deepcopy(self.matrix)), [])

    def test_cases_are_valid(self) -> None:
        self.assertEqual(checker.validate_cases(deepcopy(self.cases)), [])

    def test_required_failure_classes_are_visible(self) -> None:
        self.assertTrue(
            checker.REQUIRED_FAILURES.issubset(
                set(self.matrix["required_failure_classes"])
            )
        )

    def test_ci_truth_promotion_is_rejected(self) -> None:
        matrix = deepcopy(self.matrix)
        matrix["non_authority"]["ci_pass_promotes_truth"] = True
        self.assertIn(
            "non_authority_ci_pass_promotes_truth_invalid",
            checker.validate_matrix(matrix),
        )

    def test_missing_referenced_file_is_rejected(self) -> None:
        matrix = deepcopy(self.matrix)
        matrix["component"]["runtime"] = "runtime/not-present-v0_36.py"
        self.assertIn(
            "component_runtime_missing_file",
            checker.validate_matrix(matrix),
        )

    def test_validation_layer_requires_explicit_nonclaims(self) -> None:
        matrix = deepcopy(self.matrix)
        matrix["validation_layers"][0]["pass_does_not_mean"] = []
        self.assertIn(
            "validation_layer_static_registration_pass_does_not_mean_invalid",
            checker.validate_matrix(matrix),
        )

    def test_legacy_failure_is_fixture_inconsistency_not_current_regression(self) -> None:
        legacy = next(
            item
            for item in self.cases["cases"]
            if item["case_id"] == "legacy_incomplete_fixture_inventory_mismatch"
        )
        self.assertEqual(
            legacy["failure_class"],
            "test_fixture_inventory_inconsistency",
        )
        self.assertFalse(legacy["current_runtime_regression"])
        self.assertFalse(legacy["authority_granted"])

    def test_duplicate_case_id_is_rejected(self) -> None:
        cases = deepcopy(self.cases)
        cases["cases"].append(deepcopy(cases["cases"][0]))
        self.assertIn("case_ids_not_unique", checker.validate_cases(cases))


if __name__ == "__main__":
    unittest.main()
