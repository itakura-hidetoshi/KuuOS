from __future__ import annotations

import unittest
from copy import deepcopy

from runtime.kuuos_adaptive_retrieval_policy_v0_1 import (
    MODE_NAMES,
    RetrievalMode,
    example_context,
    select_least_sufficient,
    validate_receipt,
)


def complete(**values: bool) -> dict[str, bool]:
    result = {name: False for name in MODE_NAMES}
    result.update(values)
    return result


class AdaptiveRetrievalPolicyV01Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.context = example_context("unit-test-query")

    def test_selects_lexical_over_more_complex_adequate_modes(self) -> None:
        receipt = select_least_sufficient(
            self.context,
            complete(LEXICAL=True, PREEMBEDDED=True, GRAPH_RELATIONAL=True),
        )
        self.assertEqual(receipt["selected_mode"], RetrievalMode.LEXICAL.name)

    def test_selects_first_adequate_mode(self) -> None:
        receipt = select_least_sufficient(
            self.context,
            complete(SEMANTIC_ON_DEMAND=True, HYBRID=True),
        )
        self.assertEqual(
            receipt["selected_mode"], RetrievalMode.SEMANTIC_ON_DEMAND.name
        )

    def test_graph_requires_all_simpler_modes_inadequate(self) -> None:
        receipt = select_least_sufficient(
            self.context,
            complete(GRAPH_RELATIONAL=True),
        )
        self.assertEqual(
            receipt["selected_mode"], RetrievalMode.GRAPH_RELATIONAL.name
        )
        self.assertFalse(
            any(
                row["adequate"]
                for row in receipt["assessments"]
                if row["rank"] < int(RetrievalMode.GRAPH_RELATIONAL)
            )
        )

    def test_no_data_when_all_modes_inadequate(self) -> None:
        receipt = select_least_sufficient(self.context, complete())
        self.assertEqual(receipt["route"], "NO_DATA")
        self.assertIsNone(receipt["selected_mode"])
        self.assertFalse(receipt["least_sufficient"])

    def test_partial_assessment_fails_closed(self) -> None:
        with self.assertRaises(ValueError):
            select_least_sufficient(self.context, {"LEXICAL": True})

    def test_no_authority_is_granted(self) -> None:
        receipt = select_least_sufficient(self.context, complete(LEXICAL=True))
        for key, value in receipt.items():
            if key.endswith("_authority_granted"):
                self.assertFalse(value)

    def test_tampering_breaks_validation(self) -> None:
        receipt = select_least_sufficient(self.context, complete(HYBRID=True))
        tampered = deepcopy(receipt)
        tampered["selected_mode"] = RetrievalMode.PREEMBEDDED.name
        with self.assertRaises(ValueError):
            validate_receipt(tampered)


if __name__ == "__main__":
    unittest.main()
