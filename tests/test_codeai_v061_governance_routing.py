"""Fail-closed PR governance routing for KuuOS native CodeAI v0.61.

The dedicated GitHub CI must still run both independent pinned Lean verifiers;
this selector regression does not claim that Python checks prove Lean code.
"""
from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main
from unittest.mock import patch

from scripts.select_impacted_checks import load_registry, select

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ".github/workflows/kuuos-codeai-v061-exact-learning-feedback.yml"
FRAGMENT = "ci/check_registry.d/codeai_v061_exact_learning.json"
TEST = "tests/test_codeai_v061_governance_routing.py"
SCRIPTS = (
    "scripts/codeai_v061_exact_real_lean_mcp.py",
    "scripts/codeai_v061_independent_candidate_verification.py",
    "scripts/codeai_v061_multi_candidate_portfolio.py",
    "scripts/codeai_v061_two_stage_proof_proposal.py",
    "scripts/codeai_v061_version_bound_learning_replay.py",
)
EXAMPLES = (
    "examples/codeai_v061_two_stage_private_append.lean.txt",
    "examples/codeai_v061_two_stage_private_append_variant_b.lean.txt",
    "examples/codeai_v061_two_stage_private_append_variant_c.lean.txt",
)
SCOPE = sorted((
    WORKFLOW, FRAGMENT, TEST,
    "docs/CodeAI/V061_EXACT_LEARNING_ROUTE_EVIDENCE_20261121.md",
    *SCRIPTS, *EXAMPLES,
))


def ids(result: dict) -> set[str]:
    return {row["id"] for row in result["selected_checks"]}


class CodeAIV061GovernanceRoutingTests(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = load_registry(ROOT / "ci/check_registry.yaml")

    def test_exact_scoped_proposal_stays_focused_without_skipping_runtime(self) -> None:
        result = select(self.registry, SCOPE, None)
        self.assertEqual(result["unknown_paths"], [])
        self.assertEqual(result["unmapped_paths"], [])
        self.assertEqual(result["full_audit_trigger_paths"], [])
        self.assertFalse(result["full_audit_required"])
        self.assertFalse(result["lean_required"])  # No real formal/**/*.lean changed.
        self.assertEqual(ids(result), {
            "codeai-v061-exact-learning-contract",
            "ci-audit-tests", "runtime-full", "workflow-integrity",
        })

    def test_each_new_codeai_script_is_registered_individually(self) -> None:
        check = self.registry["checks"]["codeai-v061-exact-learning-contract"]
        self.assertTrue(check["pr_required"])
        self.assertTrue(check["full_audit_member"])
        self.assertEqual(set(check["depends_on"]), {
            "ci-audit-tests", "runtime-full", "workflow-integrity",
        })
        for path in (*SCRIPTS, *EXAMPLES, WORKFLOW, FRAGMENT, TEST):
            with self.subTest(path=path):
                self.assertIn(path, check["paths"])
                self.assertIn("codeai-v061-exact-learning-contract",
                              ids(select(self.registry, [path], None)))

    def test_new_unregistered_script_remains_full_audit(self) -> None:
        path = "scripts/codeai_v061_unregistered_future_repair.py"
        result = select(self.registry, SCOPE + [path], None)
        self.assertTrue(result["full_audit_required"])
        self.assertIn(path, result["unmapped_paths"])
        self.assertTrue(result["lean_required"])
        self.assertIn("lean-formal", ids(result))

    def test_actual_formal_lean_change_still_requires_strict_lean(self) -> None:
        proof = "formal/KUOS/Architecture/LeanPythonTwoStagePrivateAppendV0_61.lean"
        with patch("scripts.select_impacted_checks.select_lean_targets",
                   return_value=(["KuuOSFormal"], "synthetic-proof-file")):
            result = select(self.registry, SCOPE + [proof], None)
        self.assertTrue(result["lean_required"])
        self.assertIn("lean-formal", ids(result))

    def test_toolchain_and_governance_controls_fail_closed(self) -> None:
        for path in ("lean-toolchain", "lake-manifest.json",
                     "ci/check_registry.yaml",
                     ".github/workflows/pr-governance-gate.yml"):
            with self.subTest(path=path):
                result = select(self.registry, SCOPE + [path], None)
                self.assertTrue(result["lean_required"])
                self.assertIn("lean-formal", ids(result))
                if path in ("ci/check_registry.yaml",
                            ".github/workflows/pr-governance-gate.yml"):
                    self.assertTrue(result["full_audit_required"])

    def test_actual_independent_lean_and_memory_workflow_is_retained(self) -> None:
        content = (ROOT / WORKFLOW).read_text(encoding="utf-8")
        for item in (
            "native-codeai-direct-then-real-lean-mcp:",
            "independent-fixed-kernel-and-eight-axioms:",
            "read-only-exact-subtask-memory-replay:",
            "needs: native-codeai-direct-then-real-lean-mcp",
            "needs: independent-fixed-kernel-and-eight-axioms",
            "-DwarningAsError=true", "-DsorryAsError=true",
            "codeai_v061_independent_candidate_verification.py",
            "codeai_v061_exact_real_lean_mcp.py",
            "codeai_v061_version_bound_learning_replay.py",
        ):
            with self.subTest(item=item):
                self.assertIn(item, content)

    def test_actual_memory_source_keeps_inconclusive_until_ensemble(self) -> None:
        content = (ROOT / "scripts/codeai_v061_version_bound_learning_replay.py").read_text(
            encoding="utf-8")
        self.assertIn('"outcome":memory.OUTCOME_INCONCLUSIVE', content)
        self.assertIn('"independent_verifier_ensemble_v0_2": "NO_DATA"', content)
        self.assertIn('"allow_git_authority":False', content)


if __name__ == "__main__":
    main()
