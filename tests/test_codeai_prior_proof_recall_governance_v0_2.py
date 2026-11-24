"""Exact research-recall registration; no exception to audit-control or Lean checks."""
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import patch

from scripts.select_impacted_checks import load_registry, select

ROOT = Path(__file__).resolve().parents[1]
FRAGMENT = "ci/check_registry.d/codeai_prior_proof_recall_v0_2.json"
CHECK = "codeai-prior-proof-recall-v02"
SCOPE = [
    ".github/workflows/codeai-prior-proof-recall-gate-v0-1.yml",
    ".github/workflows/codeai-prior-proof-subject-recall-v0-2.yml",
    "AGENTS.md",
    "ci/check_registry.d/codeai_prior_proof_recall_v0_2.json",
    "docs/CodeAI/PRIOR_PROOF_RECALL_GOVERNANCE_ROUTING_20261124.md",
    "docs/KUUOS_CODEAI_PRIOR_PROOF_RECALL_GATE_v0_1.md",
    "docs/KUUOS_CODEAI_PRIOR_PROOF_SUBJECT_RECALL_v0_2.md",
    "memoryos/research_prior_proof_subject_index_v0_2.json",
    "runtime/kuuos_codeai_prior_proof_recall_gate_v0_1.py",
    "runtime/kuuos_codeai_prior_proof_subject_gate_v0_2.py",
    "runtime/kuuos_codeai_research_structured_edit_synthesis_v0_1.py",
    "scripts/check_codeai_prior_proof_recall_gate_v0_1.py",
    "scripts/check_codeai_prior_proof_subject_gate_v0_2.py",
    "scripts/check_codeai_research_structured_edit_synthesis_v0_1.py",
    "scripts/codeai_prior_proof_recall_gate_v0_1.py",
    "tests/test_codeai_prior_proof_recall_governance_v0_2.py"
]
def selected_ids(result):
    return {item["id"] for item in result["selected_checks"]}

class PriorProofRecallGovernanceTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = load_registry(ROOT / "ci/check_registry.yaml")

    def test_exact_scope_after_registration(self):
        result = select(self.registry, [p for p in SCOPE if p != FRAGMENT], None)
        self.assertEqual(result["unknown_paths"], [])
        self.assertEqual(result["unmapped_paths"], [])
        self.assertEqual(result["full_audit_trigger_paths"], [])
        self.assertFalse(result["full_audit_required"])
        self.assertFalse(result["lean_required"])
        self.assertIn(CHECK, selected_ids(result))

    def test_first_registration_retains_full_audit(self):
        result = select(self.registry, SCOPE, None)
        self.assertEqual(result["unknown_paths"], [])
        self.assertEqual(result["unmapped_paths"], [])
        self.assertIn(FRAGMENT, result["full_audit_trigger_paths"])
        self.assertTrue(result["full_audit_required"])
        self.assertTrue(result["lean_required"])
        self.assertIn("lean-formal", selected_ids(result))
        self.assertIn(CHECK, selected_ids(result))

    def test_every_recall_path_is_exactly_registered(self):
        check = self.registry["checks"][CHECK]
        self.assertTrue(check["pr_required"])
        self.assertTrue(check["full_audit_member"])
        self.assertEqual(sorted(check["paths"]), sorted(SCOPE))
        for path in SCOPE:
            with self.subTest(path=path):
                self.assertIn(CHECK, selected_ids(select(self.registry, [path], None)))

    def test_unmapped_future_script_and_control_remain_fail_closed(self):
        for path in ("scripts/unclassified_prior_proof_future_research.py",
                     "ci/check_registry.yaml", ".github/workflows/pr-governance-gate.yml"):
            with self.subTest(path=path):
                result = select(self.registry, [p for p in SCOPE if p != FRAGMENT] + [path], None)
                self.assertTrue(result["full_audit_required"])
                self.assertTrue(result["lean_required"])

    def test_real_lean_and_pin_changes_remain_strict(self):
        with patch("scripts.select_impacted_checks.select_lean_targets",
                   return_value=(["KuuOSFormal"], "synthetic scope test")):
            for path in ("formal/Kuu/F112/ActualResearch.lean",
                         "lean-toolchain", "lake-manifest.json", "lakefile.toml"):
                with self.subTest(path=path):
                    result = select(self.registry, [p for p in SCOPE if p != FRAGMENT] + [path], None)
                    self.assertTrue(result["lean_required"])
                    self.assertIn("lean-formal", selected_ids(result))

if __name__ == "__main__":
    main(verbosity=2)
