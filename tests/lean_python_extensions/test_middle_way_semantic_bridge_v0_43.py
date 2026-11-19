"""Real nine-store middle-way operational bridge and negative controls.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import shutil
import unittest

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_decision_os_wa_kernel_v0_3 import (
    build_replan_wa_activation_receipt,
)
from runtime.kuuos_plan_os_kernel_v0_1 import (
    build_plan_phase_activation_receipt,
)
from runtime.kuuos_qi_world_native_full_cycle_v1_3 import (
    build_native_full_cycle_receipt, validate_native_full_cycle_receipt,
)
from runtime.kuuos_lean_python_decision_plan_handoff_v0_3 import _same
from runtime import kuuos_lean_python_middle_way_semantic_bridge_v0_43 as subject


class MiddleWaySemanticBridgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = TemporaryDirectory(prefix="kuuos-v043-native-middle-")
        cls.addClassCleanup(cls.tmp.cleanup)
        cls.root = Path(cls.tmp.name)
        cls.native = build_native_full_cycle_receipt(cls.root)
        assert validate_native_full_cycle_receipt(cls.native) == []
        cls.states = cls.native["native_artifacts"]
        cls.wa_receipt = build_replan_wa_activation_receipt(
            state=cls.states["DecisionOSWa"],
            mission_cycle_phase="replan",
            mission_cycle_state_digest=sha("native-full-cycle-replan-state"),
            replan_receipt_digest=sha("native-full-cycle-replan-receipt"),
            next_plan_basis_digest=sha("native-full-cycle-next-plan-basis"),
            now_ms=50_000,
        )
        cls.plan_receipt = build_plan_phase_activation_receipt(
            state=cls.states["PlanOS"],
            mission_cycle_phase="plan",
            mission_cycle_state_digest=sha("native-full-cycle-plan-phase-state"),
            plan_phase_receipt_digest=sha("native-full-cycle-plan-phase-receipt"),
            now_ms=80_000,
        )

    def audit(self, **overrides):
        args = dict(
            native_states=self.states,
            wa_replan_activation_receipt=self.wa_receipt,
            plan_phase_activation_receipt=self.plan_receipt,
            original_cycle_root=self.root,
        )
        args.update(overrides)
        return subject.audit_native_middle_way_semantics(**args)

    def test_original_nine_stores_are_locally_checked_under_one_plan_seam(self):
        result = self.audit()
        self.assertEqual(result.status, subject.SCOPED_COMPATIBLE, result.issues)
        self.assertEqual(result.checked_local_history_count, 9)
        self.assertEqual(result.local_evidence_statuses, (
            ("BeliefOS->PlanOS", subject.LOCALLY_CHECKED),
            ("PlanOS->LearnOS", subject.LOCALLY_CHECKED),
            ("PlanOS:typed-contextual-seam", subject.LOCALLY_CHECKED),
        ))
        self.assertEqual(len(result.original_source_file_paths), 27)
        self.assertEqual(len(result.historical_edges), 8)
        self.assertEqual(result.original_store_root, str(self.root.resolve()))
        self.assertEqual(result.context_lineage,
                         self.states["PlanOS"]["lineage_id"])
        self.assertEqual(result.context_mission_digest,
                         self.states["PlanOS"]["mission_contract_digest"])
        self.assertEqual(
            result.plan_seam_final_sha256,
            subject._fingerprint(self.states["PlanOS"]),
        )

    def test_lean_source_names_are_interpretive_not_refinement_proofs(self):
        result = self.audit()
        self.assertEqual(result.status, subject.SCOPED_COMPATIBLE, result.issues)
        self.assertEqual(len(result.interpreted_lean_sources), 6)
        self.assertIn("UNPROVED_UNIVERSAL_LEAN_PYTHON_REFINEMENT",
                      result.unresolved_obstructions)
        self.assertFalse(result.local_formal_simulation_witness_constructed)
        self.assertFalse(result.universal_lean_python_semantic_refinement_proved)
        self.assertFalse(result.source_blobs_pinned_by_static_checker)

    def test_plurality_and_obstruction_are_not_erased_on_positive_result(self):
        result = self.audit()
        self.assertEqual(result.status, subject.SCOPED_COMPATIBLE)
        self.assertIn("ACTOS_ACTUAL_NUMERIC_WITNESSES_UNPROVED",
                      result.unresolved_obstructions)
        self.assertIn("WORLD_IDENTITY_NOT_EXTERNALLY_CERTIFIED",
                      result.unresolved_obstructions)
        self.assertIn("UNPROVED_GLOBAL_DESCENT_AND_ATOMIC_SNAPSHOT",
                      result.unresolved_obstructions)

    def test_mixed_numeric_time_does_not_block_local_source_equivalence(self):
        result = self.audit()
        self.assertEqual(result.status, subject.SCOPED_COMPATIBLE)
        self.assertEqual(
            result.source_time_relation,
            "SOURCE_RECEIPT_NUMERICALLY_AFTER_DECISION_GENESIS",
        )
        self.assertIn("UNPROVED_COMMON_CAUSAL_CLOCK",
                      result.unresolved_obstructions)
        self.assertFalse(result.common_causal_clock_proved)

    def test_codeai_memory_decision_plan_consume_advice_not_authority(self):
        result = self.audit()
        self.assertEqual(result.status, subject.SCOPED_COMPATIBLE)
        self.assertEqual(
            dict(result.read_only_consumer_advice),
            dict(subject.ADVICE_ON_SCOPED_CHECK),
        )
        for os in ("CodeAI", "MemoryOS", "DecisionOS", "PlanOS"):
            self.assertIn(os, dict(result.read_only_consumer_advice))
        for prop in (
            "codeai_repair_executed", "memoryos_write_performed",
            "decisionos_selection_performed", "planos_synthesis_performed",
            "host_action_performed", "execution_authority_granted",
            "truth_authority_granted", "git_authority_granted",
        ):
            self.assertFalse(getattr(result, prop), prop)

    def test_missing_any_original_receipt_is_no_data(self):
        for key in (
            "wa_replan_activation_receipt", "plan_phase_activation_receipt",
            "native_states", "original_cycle_root",
        ):
            with self.subTest(key=key):
                self.assertEqual(self.audit(**{key: None}).status,
                                 subject.NO_DATA)

    def test_missing_native_node_is_no_data(self):
        for key in subject.REQUIRED_STATES:
            with self.subTest(key=key):
                bad = dict(self.states)
                bad.pop(key)
                self.assertEqual(self.audit(native_states=bad).status,
                                 subject.NO_DATA)

    def test_wrong_or_unknown_named_state_is_blocked(self):
        bad = dict(self.states, FakeOS={})
        self.assertEqual(self.audit(native_states=bad).status,
                         subject.BLOCKED)
        self.assertEqual(self.audit(native_states=[]).status,
                         subject.BLOCKED)

    def test_forged_original_belief_receipt_blocks_even_if_plan_to_learn_passes(self):
        states = deepcopy(self.states)
        states["BeliefOSReceipt"]["belief_gerbe_receipt_digest"] = "forged"
        r = self.audit(native_states=states)
        self.assertEqual(r.status, subject.BLOCKED, r.issues)
        self.assertEqual(
            dict(r.local_evidence_statuses)["PlanOS->LearnOS"],
            subject.LOCALLY_CHECKED,
        )
        self.assertEqual(
            dict(r.local_evidence_statuses)["BeliefOS->PlanOS"],
            subject.BLOCKED,
        )

    def test_forged_plan_phase_receipt_blocks_even_if_belief_chain_passes(self):
        receipt = deepcopy(self.plan_receipt)
        receipt["plan_activation_receipt_digest"] = "forged"
        r = self.audit(plan_phase_activation_receipt=receipt)
        self.assertEqual(r.status, subject.BLOCKED, r.issues)
        self.assertEqual(
            dict(r.local_evidence_statuses)["BeliefOS->PlanOS"],
            subject.LOCALLY_CHECKED,
        )
        self.assertEqual(
            dict(r.local_evidence_statuses)["PlanOS->LearnOS"],
            subject.BLOCKED,
        )

    def test_wa_replan_receipt_must_be_original_source(self):
        receipt = deepcopy(self.wa_receipt)
        receipt["host_license_granted"] = True
        r = self.audit(wa_replan_activation_receipt=receipt)
        self.assertEqual(r.status, subject.BLOCKED, r.issues)

    def test_seam_fingerprint_mismatch_blocks_despite_both_subaudits_success(self):
        prior = subject.audit_native_five_store_chain_compatibility

        def swap_plan_digest(*args, **kwargs):
            observed = prior(*args, **kwargs)
            self.assertEqual(observed.status, subject.PLAN_LEARN_PASS)
            return replace(
                observed,
                final_native_state_digests=tuple(
                    (name, "different-final" if name == "PlanOS" else digest)
                    for name, digest in observed.final_native_state_digests
                ),
            )
        with patch.object(subject, "audit_native_five_store_chain_compatibility",
                          side_effect=swap_plan_digest):
            r = self.audit()
        self.assertEqual(r.status, subject.BLOCKED, r.issues)
        self.assertIn("middle_way:PlanOS_semantic_seam_incompatible", r.issues)

    def test_consumer_advice_on_missing_sources_is_hold_only(self):
        with TemporaryDirectory() as d:
            root = Path(d)
            r = self.audit(original_cycle_root=root)
            self.assertEqual(r.status, subject.NO_DATA)
            self.assertEqual(
                dict(r.read_only_consumer_advice),
                dict(subject.ADVICE_ON_HOLD),
            )

    def test_missing_real_original_ledger_retains_no_data(self):
        with TemporaryDirectory(prefix="kuuos-v043-missing-") as d:
            copied = Path(d) / "cycle"
            shutil.copytree(self.root, copied)
            (copied / "decision" / "decision-ledger.jsonl").unlink()
            self.assertEqual(self.audit(original_cycle_root=copied).status,
                             subject.NO_DATA)

    def test_untrusted_custom_path_is_not_executed(self):
        class HostilePath:
            def __fspath__(self):
                raise AssertionError("untrusted path coercion")
        self.assertEqual(self.audit(original_cycle_root=HostilePath()).status,
                         subject.BLOCKED)

    def test_root_alias_symlink_is_blocked(self):
        with TemporaryDirectory() as d:
            alias = Path(d) / "alias"
            alias.symlink_to(self.root, target_is_directory=True)
            self.assertEqual(self.audit(original_cycle_root=alias).status,
                             subject.BLOCKED)

    def test_child_root_symlink_is_blocked(self):
        with TemporaryDirectory(prefix="kuuos-v043-child-link-") as d:
            copied = Path(d) / "cycle"
            shutil.copytree(self.root, copied)
            (copied / "plan").rename(copied / "renamed-plan")
            (copied / "plan").symlink_to(copied / "renamed-plan",
                                         target_is_directory=True)
            self.assertEqual(self.audit(original_cycle_root=copied).status,
                             subject.BLOCKED)

    def test_wrong_plan_final_cannot_be_reconciled_by_local_preference(self):
        states = deepcopy(self.states)
        states["PlanOS"]["plan_state_digest"] = "misleading-preferred-output"
        self.assertEqual(self.audit(native_states=states).status,
                         subject.BLOCKED)

    def test_compatible_plan_root_is_not_a_global_atomic_snapshot(self):
        r = self.audit()
        self.assertEqual(r.status, subject.SCOPED_COMPATIBLE)
        self.assertFalse(r.globally_atomic_snapshot_proved)
        self.assertFalse(r.global_descent_proved)
        self.assertFalse(r.provenance_is_externally_authenticated)

    def test_input_and_original_store_files_are_unchanged(self):
        before = {str(p.relative_to(self.root)): p.read_bytes()
                  for p in self.root.rglob("*") if p.is_file()}
        originals = deepcopy((self.states, self.wa_receipt,
                              self.plan_receipt))
        self.assertEqual(self.audit().status, subject.SCOPED_COMPATIBLE)
        after = {str(p.relative_to(self.root)): p.read_bytes()
                 for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)
        self.assertTrue(_same(originals, (self.states, self.wa_receipt,
                                          self.plan_receipt)))

    def test_join_exactly_matches_three_way_policy_exhaustive(self):
        vals = (subject.LOCALLY_CHECKED, subject.NO_DATA, subject.BLOCKED)
        for a in vals:
            for b in vals:
                with self.subTest(a=a, b=b):
                    out = subject.combine_evidence(a, b)
                    expected = (subject.BLOCKED if subject.BLOCKED in (a, b)
                                else subject.NO_DATA if subject.NO_DATA in (a, b)
                                else subject.LOCALLY_CHECKED)
                    self.assertEqual(out, expected)
        self.assertEqual(subject.combine_evidence("PASS", subject.LOCALLY_CHECKED),
                         subject.BLOCKED)

    def test_exact_history_provenance_not_proof_of_causal_or_semantic_truth(self):
        r = self.audit()
        self.assertEqual(r.status, subject.SCOPED_COMPATIBLE)
        for name in (
            "local_formal_simulation_witness_constructed",
            "universal_lean_python_semantic_refinement_proved",
            "global_descent_proved", "globally_atomic_snapshot_proved",
            "common_causal_clock_proved", "clinical_authority_granted",
            "institutional_authority_granted", "memory_overwrite_authority_granted",
            "original_store_mutated",
        ):
            self.assertIs(getattr(r, name), False, name)


if __name__ == "__main__":
    unittest.main()
