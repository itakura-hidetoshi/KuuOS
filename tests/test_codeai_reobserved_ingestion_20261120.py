"""2026-11-20 renewed CodeAI official-evidence lineage; historic receipt preserved."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.check_codeai_external_result_process_evidence_ingestion_v0_1 import (
    build_reobserved_fixture,
    validate_live_binding,
)

ROOT = Path(__file__).resolve().parents[1]
CURRENT = ROOT / "ci/codeai_external_evidence_reobserved_20261120.json"
HISTORICAL = ROOT / "ci/codeai_external_evidence_reobserved_20261016.json"
WORKFLOW = ROOT / ".github/workflows/codeai-external-result-process-evidence-ingestion-v0-1.yml"


class ReobservedCodeAIEvidence20261120Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.current = json.loads(CURRENT.read_text(encoding="utf-8"))
        self.historical = json.loads(HISTORICAL.read_text(encoding="utf-8"))

    def test_exact_completed_run_and_artifact_binding(self) -> None:
        validate_live_binding(self.current)
        self.assertEqual(self.current["predecessor_workflow_run_id"], 44739105282)
        self.assertEqual(self.current["predecessor_workflow_run_attempt"], 1)
        self.assertEqual(self.current["predecessor_artifact_id"], 14629743535)
        self.assertEqual(self.current["predecessor_workflow_head_sha"],
                         "9cc37f52d04d2137225a2a51cff781099cee249d")
        self.assertEqual(self.current["predecessor_artifact_digest"],
                         "cd1bf0907d7510f954622a1a553e294613300005e605013efd501809002398b1")
        self.assertEqual(self.current["external_observation_digest"],
                         "22268a13a116013cf36c6f9cfde52166bd1d99a4f7f415a8653a505d13874a74")

    def test_new_receipt_is_distinct_and_non_authorizing(self) -> None:
        current = build_reobserved_fixture(self.current, receipt_edition="20261120")
        historical = build_reobserved_fixture(self.historical)
        self.assertEqual(current["request"]["request_id"],
                         "external-result-ingestion-request-reobserved-20261120")
        self.assertEqual(current["request"]["request_revision"],
                         "external-result-ingestion-rev-003")
        self.assertEqual(historical["request"]["request_revision"],
                         "external-result-ingestion-rev-002")
        self.assertNotEqual(current["request"]["request_id"],
                            historical["request"]["request_id"])
        self.assertNotEqual(current["receipt"], historical["receipt"])
        self.assertFalse(current["receipt"]["correctness_claimed"])
        self.assertFalse(current["receipt"]["git_authority_granted"])

    def test_preserved_historical_evidence_identity(self) -> None:
        validate_live_binding(self.historical)
        self.assertEqual(self.historical["predecessor_workflow_run_id"], 38878097337)
        self.assertEqual(self.historical["predecessor_artifact_id"], 12039184115)
        self.assertNotEqual(self.current["predecessor_artifact_id"],
                            self.historical["predecessor_artifact_id"])

    def test_workflow_uses_only_new_exact_live_binding(self) -> None:
        source = WORKFLOW.read_text(encoding="utf-8")
        for text in (
            "PREDECESSOR_RUN_ID: '44739105282'",
            "PREDECESSOR_ARTIFACT_ID: '14629743535'",
            "REOBSERVED_BINDING_FILE: ci/codeai_external_evidence_reobserved_20261120.json",
            "--receipt-edition 20261120",
            "tests.test_codeai_reobserved_ingestion_20261120",
        ):
            self.assertIn(text, source)

    def test_unregistered_receipt_edition_rejected(self) -> None:
        with self.assertRaises(SystemExit):
            build_reobserved_fixture(self.current, receipt_edition="unverified")

    def test_missing_or_mismatched_binding_rejected(self) -> None:
        for key, replacement in (
            ("predecessor_artifact_id", 0),
            ("predecessor_workflow_head_sha", "invalid"),
            ("prediction_digest", "0" * 64),
            ("predecessor_artifact_name", "wrong"),
        ):
            candidate = dict(self.current, **{key: replacement})
            with self.subTest(key=key), self.assertRaises(SystemExit):
                validate_live_binding(candidate)


if __name__ == "__main__":
    unittest.main()
