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

    def test_existing_registered_sources_use_focused_governance(self) -> None:
        # The fragment is already installed and NOT changed in this scenario.
        paths = [path for path in SCOPE if path != FRAGMENT]
        result = select(self.registry, paths, None)
        self.assertEqual(result["unknown_paths"], [])
        self.assertEqual(result["unmapped_paths"], [])
        self.assertEqual(result["full_audit_trigger_paths"], [])
        self.assertFalse(result["full_audit_required"])
        self.assertFalse(result["lean_required"])  # No real formal/**/*.lean changed.
        self.assertEqual(ids(result), {
            "codeai-v061-exact-learning-contract",
            "ci-audit-tests", "runtime-full", "workflow-integrity",
        })

    def test_first_registration_of_audit_fragment_is_full_governance(self) -> None:
        # This v0.61 PR ADDS the fragment. The central selector correctly
        # treats it as an audit-control change, so this PR stays full/strict.
        result = select(self.registry, SCOPE, None)
        self.assertEqual(result["unknown_paths"], [])
        self.assertEqual(result["unmapped_paths"], [])
        self.assertTrue(result["full_audit_required"])
        self.assertIn(FRAGMENT, result["full_audit_trigger_paths"])
        self.assertTrue(result["lean_required"])
        self.assertIn("lean-formal", ids(result))
        self.assertIn("codeai-v061-exact-learning-contract", ids(result))

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

    def test_actual_four_family_ensemble_kernel_blocks_unattested_single_family(self) -> None:
        from scripts import codeai_v061_version_bound_learning_replay as replay
        now = 500
        evidence = {
            "evidence_digest": "d" * 64,
            "results": [{
                "status": "INDEPENDENT_FIXED_LEAN_AND_AXIOM_PASSED",
                "axiom_declarations_checked": 8,
                "strict_lean_exit_code": 0,
                "sorryAx": False,
                "source_sha256": "a" * 64,
            }],
        }
        hold = replay.check_actual_v02_ensemble_hold(evidence, now)
        self.assertTrue(hold["actual_original_ensemble_v02_invoked"])
        self.assertEqual(hold["actual_original_ensemble_v02_status"], "blocked")
        self.assertEqual(hold["independent_organizations_attested"], 0)
        self.assertEqual(hold["external_verifier_issuer_authentication"], "NO_DATA")
        self.assertFalse(hold["verified_useful"])
        self.assertFalse(hold["reusable_memory_hint"])
        reasons = set(hold["ensemble_v02_issues"])
        self.assertIn("ensemble_required_family_missing", reasons)
        self.assertIn("ensemble_insufficient_organization_count", reasons)
        self.assertIn("ensemble_insufficient_verifier_count", reasons)

    def test_actual_memory_source_keeps_inconclusive_until_ensemble(self) -> None:
        content = (ROOT / "scripts/codeai_v061_version_bound_learning_replay.py").read_text(
            encoding="utf-8")
        self.assertIn('"outcome":memory.OUTCOME_INCONCLUSIVE', content)
        self.assertIn('"independent_verifier_ensemble_v0_2": "NO_DATA"', content)
        self.assertIn('"allow_git_authority":False', content)


    def _actual_c_negative_fixture(self):
        import hashlib

        from scripts import codeai_v061_version_bound_learning_replay as replay

        text = (ROOT / "examples/codeai_v061_two_stage_private_append_variant_c.lean.txt").read_text(
            encoding="utf-8")
        msg = "try 'simp' instead of 'simpa'"
        log = (
            f"/tmp/ProposedV061.lean:140:7: error: {msg}\n"
            f"/tmp/ProposedV061.lean:159:7: error: {msg}\n"
        )
        c = {
            "label": "model-c",
            "status": "DIRECT_LEAN_REJECTED_TYPED_LINT_PENDING",
            "source_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "diagnostic_digest": hashlib.sha256(log.encode("utf-8")).hexdigest(),
            "diagnostics": [msg, msg],
            "error_count": 2,
            "strict_lean_exit_code": 1,
            "proven_lean_declarations": 0,
            "original_source_unchanged": True,
            "independent_repair_evidence_admitted": False,
            "reusable_repair_memory_admitted": False,
        }
        evidence = {
            "source_candidate_portfolio": "model_supplied_proposals_governed_by_actual_codeai",
            "typed_error_classification_c_admitted": False,
            "results": [{}, {}, c],
        }
        evidence["evidence_digest"] = replay.stable(evidence)
        return replay, evidence, log, text

    def test_c_compiler_lint_is_bound_but_not_native_typed_classification(self) -> None:
        replay, evidence, log, text = self._actual_c_negative_fixture()
        receipt = replay.check_candidate_c_compiler_lint_boundary(evidence, log, text)
        self.assertEqual([row["line"] for row in receipt["observed_diagnostics"]], [140, 159])
        self.assertFalse(receipt["native_typed_error_classification_certified"])
        self.assertFalse(receipt["verified_useful_memory_admitted"])
        self.assertFalse(receipt["reusable_memory_hint"])
        self.assertEqual(receipt["verification_guided_regeneration_receipt"], "NO_DATA")

    def test_c_compiler_log_digest_tampering_is_rejected(self) -> None:
        replay, evidence, log, text = self._actual_c_negative_fixture()
        with self.assertRaises(AssertionError):
            replay.check_candidate_c_compiler_lint_boundary(
                evidence, log.replace(":159:7:", ":158:7:"), text)

    def test_c_source_and_classifier_promotion_are_rejected(self) -> None:
        from copy import deepcopy
        replay, evidence, log, text = self._actual_c_negative_fixture()
        with self.assertRaises(AssertionError):
            replay.check_candidate_c_compiler_lint_boundary(evidence, log, text + "\n")
        promoted = deepcopy(evidence)
        promoted["typed_error_classification_c_admitted"] = True
        with self.assertRaises(AssertionError):
            replay.check_candidate_c_compiler_lint_boundary(promoted, log, text)
        forged = deepcopy(evidence)
        forged["results"][2]["reusable_repair_memory_admitted"] = True
        with self.assertRaises(AssertionError):
            replay.check_candidate_c_compiler_lint_boundary(forged, log, text)

    def test_c_compiler_messages_cannot_become_static_preflight_findings(self) -> None:
        from copy import deepcopy
        import hashlib
        replay, evidence, log, text = self._actual_c_negative_fixture()
        forged = deepcopy(evidence)
        altered = log.replace("try 'simp' instead of 'simpa'", "unrelated failure")
        forged["results"][2]["diagnostic_digest"] = hashlib.sha256(
            altered.encode("utf-8")).hexdigest()
        forged["results"][2]["diagnostics"] = ["unrelated failure", "unrelated failure"]
        with self.assertRaises(AssertionError):
            replay.check_candidate_c_compiler_lint_boundary(forged, altered, text)



    @staticmethod
    def _actual_native_two_stage_snapshots(route):
        """Build THREE genuine v0.53 SQLite observations, not mock certificates.

        The original v0.56 / v0.58 archive and v0.60 audit implementations
        are reused unchanged. All branch-private rows are appended, never
        rewritten or collapsed into a single chronological branch.
        """
        import shutil
        from pathlib import Path
        from tempfile import TemporaryDirectory

        from runtime import kuuos_lean_python_tagged_fork_archive_v0_58 as tagged
        from tests.lean_python_extensions import (
            test_common_ancestor_fork_v0_56 as origin,
        )

        origin.CommonAncestorForkV056Tests.setUpClass()
        helper = origin.CommonAncestorForkV056Tests(
            "test_six_native_routes_yield_local_fork_only"
        )

        def append_pair(db, n):
            return helper._commit(
                db, route,
                seq={"first": n, "second": n + 1},
                nonce={
                    "first": f"{1000 + n:032x}",
                    "second": f"{2000 + n:032x}",
                },
            )

        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            original = root / "ancestor.sqlite"
            left = root / "left.sqlite"
            right = root / "right.sqlite"
            helper._commit(original, route)
            ancestor = helper._manifest(original)
            shutil.copyfile(original, left)
            shutil.copyfile(original, right)

            archives = []
            for left_sequence, right_sequence in ((9, 11), (13, 15), (17, 19)):
                append_pair(left, left_sequence)
                append_pair(right, right_sequence)
                actual = tagged.build_local_tagged_fork_archive(
                    ancestor, helper._manifest(left), helper._manifest(right)
                )
                assert actual.archive is not None, actual
                archives.append(actual.archive)

        shared = len(ancestor["entries"])
        def annotations(archive):
            left_rows = len(archive["branches"][0]["snapshot"]["entries"])
            right_rows = len(archive["branches"][1]["snapshot"]["entries"])
            common = [f"same-ancestor-{i}" for i in range(shared)]
            lv = common + [f"left-private-{i}" for i in range(left_rows - shared)]
            rv = common + [f"right-private-{i}" for i in range(right_rows - shared)]
            return lv, rv

        return tuple(archives), tuple(annotations(a) for a in archives)

    def test_v061_two_stage_behavioral_regression_all_native_six_routes(self) -> None:
        """Behavioral evidence, not a Lean/Python refinement certificate."""
        from runtime import kuuos_lean_python_tagged_private_append_v0_60 as native
        from runtime.kuuos_lean_python_middle_way_verify_plan_six_routes_v0_45 import ROUTES

        for route, _, _, _ in ROUTES:
            with self.subTest(native_route=route):
                (old, mid, final), (a, b, c) = self._actual_native_two_stage_snapshots(route)
                first = native.audit_tagged_private_append(old, mid, *a, *b)
                second = native.audit_tagged_private_append(mid, final, *b, *c)
                self.assertEqual(first.status, native.PRESERVED_COMPATIBILITY)
                self.assertEqual(second.status, native.PRESERVED_COMPATIBILITY)
                self.assertEqual(first.mismatch_indices, ())
                self.assertEqual(second.mismatch_indices, ())
                self.assertTrue(first.overlap_status_invariant_verified)
                self.assertTrue(second.overlap_status_invariant_verified)
                self.assertTrue(first.all_old_rows_and_annotations_preserved)
                self.assertTrue(second.all_old_rows_and_annotations_preserved)
                self.assertTrue(first.old_fork_obstruction_preserved)
                self.assertTrue(second.old_fork_obstruction_preserved)
                self.assertTrue(second.new_overlap_compatible)
                self.assertEqual(
                    (first.appended_left_rows, first.appended_right_rows), (2, 2))
                self.assertEqual(
                    (second.appended_left_rows, second.appended_right_rows), (2, 2))
                self.assertFalse(first.linear_history_descended)
                self.assertFalse(second.global_descent_certified)
                self.assertFalse(second.original_lean_python_refinement_proved)
                self.assertFalse(second.host_execution_authorized)
                self.assertIsNone(second.selected_successor)

    def test_v061_two_stage_adversarial_shared_mismatch_remains_obstruction(self) -> None:
        from runtime import kuuos_lean_python_tagged_private_append_v0_60 as native

        (old, mid, final), (a, b, c) = self._actual_native_two_stage_snapshots("retain")
        a[1][0] = "shared-conflict"
        b[1][0] = "shared-conflict"
        c[1][0] = "shared-conflict"
        first = native.audit_tagged_private_append(old, mid, *a, *b)
        second = native.audit_tagged_private_append(mid, final, *b, *c)
        self.assertEqual(first.status, native.PRESERVED_MISMATCH)
        self.assertEqual(second.status, native.PRESERVED_MISMATCH)
        self.assertEqual(first.mismatch_indices, (0,))
        self.assertEqual(second.mismatch_indices, (0,))
        self.assertFalse(second.new_overlap_compatible)
        self.assertIsNone(second.newly_glued)
        self.assertFalse(second.host_execution_authorized)

        # One changed old observation in stage 2 must NOT erase that mismatch.
        corrupt = [list(c[0]), list(c[1])]
        corrupt[1][0] = c[0][0]
        reject = native.audit_tagged_private_append(mid, final, *b, *corrupt)
        self.assertEqual(reject.status, native.OBSERVATION_REWRITE)
        self.assertFalse(reject.overlap_status_invariant_verified)

    def test_v061_behavioral_source_provenance_is_exact_but_not_refinement(self) -> None:
        """Binding actual model-provided Lean A/B does not prove Python semantics."""
        import hashlib
        from scripts.codeai_v061_independent_candidate_verification import EXPECTED_SHA256
        from scripts.codeai_v061_multi_candidate_portfolio import INPUTS
        from scripts import codeai_v061_two_stage_proof_proposal as source

        self.assertEqual(source.TOOLCHAIN, "leanprover/lean4:v4.30.0-rc2")
        self.assertEqual(
            source.MATHLIB,
            "5450b53e5ddc75d46418fabb605edbf36bd0beb6")
        self.assertEqual(set(EXPECTED_SHA256), {k for k, _ in INPUTS})
        for label, path in INPUTS:
            content = (ROOT / path).read_bytes()
            self.assertEqual(hashlib.sha256(content).hexdigest(), EXPECTED_SHA256[label])
        # Both models give the same eight types; syntactic/behavioral inspection
        # makes NO claim of independently generated proof strategies.
        self.assertIn("two_stage_tagged_gluing_iff", (ROOT / INPUTS[0][1]).read_text())
        self.assertIn("two_stage_obstruction_persists", (ROOT / INPUTS[0][1]).read_text())



if __name__ == "__main__":
    main()
