"""v0.42 original Belief gerbe store origin and last native receipt tests.

Real KuuOS v1.3 native OS cycle; no mock acceptance or synthetic runtime
source history in a positive test. Copyright Hidetoshi Itakura / 板倉英俊.
Apache-2.0.
"""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_belief_os_gerbe_store_v0_3 import (
    BeliefGerbeStore, build_initial_gerbe_state,
)
from runtime.kuuos_belief_os_gerbe_types_v0_3 import (
    receipt_digest, store_commit_digest,
)
from runtime.kuuos_decision_os_wa_kernel_v0_3 import (
    build_replan_wa_activation_receipt,
)
from runtime.kuuos_qi_world_native_full_cycle_v1_3 import (
    build_native_full_cycle_receipt, validate_native_full_cycle_receipt,
)
from runtime.kuuos_lean_python_belief_receipt_guard_v0_18 import (
    _replay_belief_ledger,
)
from runtime.kuuos_lean_python_act_observe_store_compat_v0_35 import _native_store
from runtime.kuuos_lean_python_decision_plan_handoff_v0_3 import _same
from runtime.kuuos_lean_python_decision_store_origin_v0_41 import (
    SCOPED_COMPATIBLE as PRIOR_PASS,
    audit_native_decision_store_origin,
)
from runtime import kuuos_lean_python_belief_gerbe_store_origin_v0_42 as subject


class NativeBeliefGerbeStoreOriginTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = TemporaryDirectory(prefix="kuuos-v042-native-")
        cls.addClassCleanup(cls.tmp.cleanup)
        cls.root = Path(cls.tmp.name)
        cls.native = build_native_full_cycle_receipt(cls.root)
        assert validate_native_full_cycle_receipt(cls.native) == []
        cls.states = cls.native["native_artifacts"]
        # Only a TEST constructs the native v1.3 fixture's original receipt.
        # A production audit MUST require an actually supplied packet.
        cls.wa_receipt = build_replan_wa_activation_receipt(
            state=cls.states["DecisionOSWa"],
            mission_cycle_phase="replan",
            mission_cycle_state_digest=sha("native-full-cycle-replan-state"),
            replan_receipt_digest=sha("native-full-cycle-replan-receipt"),
            next_plan_basis_digest=sha("native-full-cycle-next-plan-basis"),
            now_ms=50_000,
        )

    def audit(self, **overrides):
        args = dict(
            belief_state=self.states["BeliefOSState"],
            belief_receipt=self.states["BeliefOSReceipt"],
            decision_state=self.states["DecisionOS"],
            plural_state=self.states["DecisionOSPlural"],
            wa_state=self.states["DecisionOSWa"],
            plan_state=self.states["PlanOS"],
            replan_activation_receipt=self.wa_receipt,
            original_belief_store_root=self.root / "belief",
            original_decision_store_root=self.root / "decision",
            original_plural_store_root=self.root / "plural",
            original_wa_store_root=self.root / "wa",
            original_plan_store_root=self.root / "plan",
        )
        args.update(overrides)
        return subject.audit_native_belief_gerbe_store_origin(**args)

    def copy_belief(self):
        temp = TemporaryDirectory(prefix="kuuos-v042-belief-copy-")
        self.addCleanup(temp.cleanup)
        dst = Path(temp.name) / "belief"
        shutil.copytree(self.root / "belief", dst)
        return dst

    def test_original_belief_to_plan_has_five_replayed_origins(self):
        result = self.audit()
        self.assertEqual(result.status, subject.SCOPED_COMPATIBLE, result.issues)
        self.assertEqual(result.belief_commit_count, 1)
        self.assertEqual(result.belief_history_receipt_count, 1)
        self.assertTrue(result.belief_original_store_replayed)
        self.assertTrue(result.belief_genesis_matches_original_constructor)
        self.assertTrue(result.belief_history_data_conditions_checked)
        self.assertTrue(result.replayed_native_receipt_equals_supplied)
        self.assertTrue(result.prior_decision_plural_wa_plan_origins_checked)
        self.assertTrue(result.belief_store_bytes_stable_during_audit)
        self.assertTrue(result.prior_store_bytes_stable_during_audit)
        self.assertEqual(result.replayed_last_receipt_sha256,
                         result.supplied_last_receipt_sha256)
        self.assertEqual(len(result.checked_source_paths), 17)
        self.assertEqual(
            tuple(n for n, _ in result.staged_typed_edge_statuses),
            ("DecisionOS->DecisionOSPlural",
             "DecisionOSPlural->DecisionOSWa",
             "DecisionOSWa->PlanOS"),
        )

    def test_original_genesis_is_pure_constructor_output(self):
        store = BeliefGerbeStore(self.root / "belief")
        genesis = store._read_json(store.genesis_path)
        expected = build_initial_gerbe_state(
            lineage_id=genesis["lineage_id"],
            now_ms=genesis["updated_at_ms"],
        )
        self.assertTrue(_same(expected, genesis))
        self.assertEqual(genesis["event_count"], 0)
        self.assertEqual(genesis["run_count"], 0)

    def test_v018_reconstructs_exact_last_original_receipt(self):
        genesis, final, commits = _native_store(
            self.root / "belief", BeliefGerbeStore, subject._BELIEF_FILES,
        )
        reconstructed, commit_digest = _replay_belief_ledger(
            genesis, commits, final,
        )
        self.assertTrue(_same(reconstructed, self.states["BeliefOSReceipt"]))
        self.assertEqual(
            commit_digest, commits[-1]["belief_gerbe_store_commit_digest"],
        )

    def test_alternative_origin_from_valid_final_has_empty_history_obstruction(self):
        # The original store accepts any valid state for initialize.
        # A newly initialized store at the final state has the same
        # recover() result, but never contains the historical packet.
        with TemporaryDirectory(prefix="kuuos-v042-truncated-") as d:
            truncated = BeliefGerbeStore(Path(d) / "belief")
            truncated.initialize(self.states["BeliefOSState"])
            self.assertTrue(_same(
                truncated.recover(), self.states["BeliefOSState"],
            ))
            prior = audit_native_decision_store_origin(
                self.states["BeliefOSReceipt"],
                self.states["DecisionOS"], self.states["DecisionOSPlural"],
                self.states["DecisionOSWa"], self.states["PlanOS"],
                self.wa_receipt,
                self.root / "decision", self.root / "plural",
                self.root / "wa", self.root / "plan",
            )
            self.assertEqual(prior.status, PRIOR_PASS)
            result = self.audit(original_belief_store_root=truncated.root)
            self.assertEqual(result.status, subject.NO_DATA, result.issues)
            self.assertFalse(result.replayed_native_receipt_equals_supplied)

    def test_missing_each_required_argument_remains_no_data(self):
        for key in (
            "belief_state", "belief_receipt", "decision_state",
            "plural_state", "wa_state", "plan_state",
            "replan_activation_receipt", "original_belief_store_root",
            "original_decision_store_root", "original_plural_store_root",
            "original_wa_store_root", "original_plan_store_root",
        ):
            with self.subTest(key=key):
                self.assertEqual(self.audit(**{key: None}).status, subject.NO_DATA)

    def test_each_original_belief_file_missing_remains_no_data(self):
        for name in subject._BELIEF_FILES:
            with self.subTest(name=name):
                root = self.copy_belief()
                (root / name).unlink()
                self.assertEqual(self.audit(
                    original_belief_store_root=root,
                ).status, subject.NO_DATA)

    def test_empty_original_history_is_not_promoted(self):
        store = BeliefGerbeStore(self.root / "belief")
        origin = store._read_json(store.genesis_path)
        with TemporaryDirectory() as d:
            empty = BeliefGerbeStore(Path(d) / "belief")
            empty.initialize(origin)
            self.assertEqual(self.audit(
                original_belief_store_root=empty.root,
                belief_state=origin,
            ).status, subject.NO_DATA)

    def test_forged_belief_final_state_is_blocked(self):
        bad = deepcopy(self.states["BeliefOSState"])
        bad["belief_gerbe_state_digest"] = "forged"
        self.assertEqual(self.audit(belief_state=bad).status, subject.BLOCKED)

    def test_forged_belief_receipt_is_not_a_native_source(self):
        bad = deepcopy(self.states["BeliefOSReceipt"])
        bad["belief_gerbe_receipt_digest"] = "forged"
        self.assertEqual(self.audit(belief_receipt=bad).status, subject.BLOCKED)

    def test_resealed_gerbe_receipt_cannot_replace_original_last_receipt(self):
        bad = deepcopy(self.states["BeliefOSReceipt"])
        bad["reasoning_license"] = False
        bad["belief_gerbe_receipt_digest"] = receipt_digest(bad)
        # Direct last-receipt equality rejects even when an independently
        # recomputed hash has been provided.
        result = self.audit(belief_receipt=bad)
        self.assertEqual(result.status, subject.BLOCKED, result.issues)
        self.assertIn("BeliefOSReceipt:not_original_last_replayed_receipt",
                      result.issues)

    def test_missing_genuine_prior_receipt_is_no_data(self):
        self.assertEqual(self.audit(
            replan_activation_receipt=None,
        ).status, subject.NO_DATA)

    def test_previous_decision_origin_cannot_be_bypassed(self):
        bad = deepcopy(self.states["DecisionOS"])
        bad["decision_state_digest"] = "forged"
        self.assertEqual(self.audit(decision_state=bad).status, subject.BLOCKED)

    def test_plain_json_sources_and_concrete_path_roots_required(self):
        class HostileRoot:
            def __fspath__(self):
                raise AssertionError("untrusted conversion called")
        for val in (HostileRoot(), 123, [], object()):
            with self.subTest(value=type(val).__name__):
                self.assertEqual(self.audit(
                    original_belief_store_root=val,
                ).status, subject.BLOCKED)
        self.assertEqual(self.audit(belief_state=[]).status, subject.BLOCKED)
        self.assertEqual(self.audit(belief_receipt=[]).status, subject.BLOCKED)

    def test_string_roots_are_allowed(self):
        kwargs = {
            "original_" + name + "_store_root": str(self.root / name)
            for name in ("belief", "decision", "plural", "wa", "plan")
        }
        self.assertEqual(self.audit(**kwargs).status, subject.SCOPED_COMPATIBLE)

    def test_overlapping_aliased_or_nested_roots_block(self):
        for root in (
            self.root / "decision", self.root,
            self.root / "belief" / ".." / "belief",
        ):
            with self.subTest(root=str(root)):
                self.assertEqual(self.audit(
                    original_belief_store_root=root,
                ).status, subject.BLOCKED)

    def test_symlink_to_root_and_parent_are_blocked(self):
        with TemporaryDirectory() as d:
            link = Path(d) / "belief-link"
            link.symlink_to(self.root / "belief", target_is_directory=True)
            self.assertEqual(self.audit(
                original_belief_store_root=link,
            ).status, subject.BLOCKED)
            link.unlink()
            link.symlink_to(self.root, target_is_directory=True)
            self.assertEqual(self.audit(
                original_belief_store_root=link / "belief",
            ).status, subject.BLOCKED)

    def test_cyclic_root_and_belief_file_symlink_block(self):
        with TemporaryDirectory() as d:
            loop = Path(d) / "cycle"
            loop.symlink_to(loop, target_is_directory=True)
            self.assertEqual(self.audit(
                original_belief_store_root=loop,
            ).status, subject.BLOCKED)
        root = self.copy_belief()
        file = root / subject._BELIEF_FILES[0]
        file.unlink()
        file.symlink_to(self.root / "belief" / file.name)
        self.assertEqual(self.audit(
            original_belief_store_root=root,
        ).status, subject.BLOCKED)

    def test_bad_original_gerbe_ledger_blocks(self):
        root = self.copy_belief()
        (root / subject._BELIEF_FILES[1]).write_text("{broken\n")
        self.assertEqual(self.audit(
            original_belief_store_root=root,
        ).status, subject.BLOCKED)

    def test_snapshot_metadata_requires_exact_replay(self):
        root = self.copy_belief()
        file = root / subject._BELIEF_FILES[2]
        state = json.loads(file.read_text())
        state["event_count"] = float(state["event_count"])
        file.write_text(json.dumps(state))
        self.assertEqual(self.audit(
            original_belief_store_root=root,
        ).status, subject.BLOCKED)

    def test_exact_integer_commit_indexes_required(self):
        for value in (True, 1.0, 9):
            with self.subTest(value=value):
                root = self.copy_belief()
                file = root / subject._BELIEF_FILES[1]
                rows = [json.loads(line) for line in file.read_text().splitlines()]
                rows[0]["commit_index"] = value
                previous = ""
                for row in rows:
                    row["predecessor_commit_digest"] = previous
                    row["belief_gerbe_store_commit_digest"] = store_commit_digest(row)
                    previous = row["belief_gerbe_store_commit_digest"]
                file.write_text("".join(json.dumps(x) + "\n" for x in rows))
                recovered, _ = BeliefGerbeStore(root)._recover_unlocked()
                self.assertTrue(_same(recovered, self.states["BeliefOSState"]))
                self.assertEqual(self.audit(
                    original_belief_store_root=root,
                ).status, subject.BLOCKED)

    def test_belief_ledger_native_whitespace_is_preserved(self):
        for boundary, newline in ((b"\x0c", b"\n"), (b"\x0b", b"\r\n"),
                                  ("\u00a0".encode("utf-8"), b"\r")):
            with self.subTest(boundary=boundary):
                root = self.copy_belief()
                file = root / subject._BELIEF_FILES[1]
                rows = file.read_bytes().splitlines()
                file.write_bytes(
                    newline.join(boundary + row + boundary for row in rows)
                    + newline
                )
                recovered, commits = BeliefGerbeStore(root)._recover_unlocked()
                self.assertTrue(_same(recovered, self.states["BeliefOSState"]))
                self.assertEqual(len(commits), 1)
                result = self.audit(original_belief_store_root=root)
                self.assertEqual(result.status, subject.SCOPED_COMPATIBLE,
                                 result.issues)

    def test_shadowed_nan_infinity_and_overflow_are_rejected(self):
        for name in subject._BELIEF_FILES:
            for number in ("NaN", "Infinity", "1e999"):
                with self.subTest(name=name, number=number):
                    root = self.copy_belief()
                    file = root / name
                    text = file.read_text()
                    first = text.splitlines()[0] if name.endswith(".jsonl") else text
                    key = next(iter(json.loads(first)))
                    opening = text.index("{") + 1
                    file.write_text(
                        text[:opening] + json.dumps(key) + ":" + number
                        + "," + text[opening:]
                    )
                    recovered, _ = BeliefGerbeStore(root)._recover_unlocked()
                    self.assertTrue(_same(recovered, self.states["BeliefOSState"]))
                    self.assertEqual(self.audit(
                        original_belief_store_root=root,
                    ).status, subject.BLOCKED)

    def test_history_alignment_is_a_separate_local_gate(self):
        with patch.object(subject, "_history_data_conditions",
                          return_value=False):
            result = self.audit()
        self.assertEqual(result.status, subject.BLOCKED)
        self.assertIn("BeliefOSState:surface_holonomy_history_not_aligned",
                      result.issues)

    def test_native_replay_consumes_first_observed_bytes(self):
        root = self.copy_belief()
        native = BeliefGerbeStore._recover_unlocked

        def rewrite_during_replay(store):
            path = store.genesis_path
            original = path.read_bytes()
            try:
                path.write_bytes(b"{broken-json}\n")
                return native(store)
            finally:
                path.write_bytes(original)

        with patch.object(BeliefGerbeStore, "_recover_unlocked",
                          rewrite_during_replay):
            result = self.audit(original_belief_store_root=root)
        self.assertEqual(result.status, subject.SCOPED_COMPATIBLE, result.issues)
        self.assertTrue(result.belief_store_bytes_stable_during_audit)

    def test_second_observation_detects_changed_original_bytes(self):
        root = self.copy_belief()
        prior = subject.audit_native_decision_store_origin

        def alter_after_prior(*args, **kwargs):
            value = prior(*args, **kwargs)
            file = root / subject._BELIEF_FILES[2]
            file.write_bytes(file.read_bytes() + b"\n")
            return value

        with patch.object(subject, "audit_native_decision_store_origin",
                          side_effect=alter_after_prior):
            result = self.audit(original_belief_store_root=root)
        self.assertEqual(result.status, subject.BLOCKED, result.issues)
        self.assertIn("belief_store:original_bytes_changed", result.issues)

    def test_original_source_files_and_inputs_are_not_mutated(self):
        before = {
            str(p.relative_to(self.root)): p.read_bytes()
            for p in self.root.rglob("*") if p.is_file()
        }
        original = deepcopy((self.native, self.wa_receipt))
        self.assertEqual(self.audit().status, subject.SCOPED_COMPATIBLE)
        after = {
            str(p.relative_to(self.root)): p.read_bytes()
            for p in self.root.rglob("*") if p.is_file()
        }
        self.assertEqual(before, after)
        self.assertTrue(_same(original, (self.native, self.wa_receipt)))

    def test_original_cross_source_time_inversion_retained(self):
        result = self.audit()
        self.assertEqual(result.status, subject.SCOPED_COMPATIBLE, result.issues)
        self.assertEqual(result.belief_receipt_time_ms, 5000)
        self.assertEqual(result.decision_genesis_time_ms, 1000)
        self.assertEqual(
            result.cross_source_time_relation,
            "SOURCE_RECEIPT_NUMERICALLY_AFTER_DECISION_GENESIS",
        )
        self.assertFalse(result.common_belief_decision_clock_proved)
        self.assertFalse(result.global_temporal_descent_proved)

    def test_no_learn_proof_authenticity_or_execution_authority_promoted(self):
        result = self.audit()
        self.assertEqual(result.status, subject.SCOPED_COMPATIBLE, result.issues)
        for name in (
            "common_belief_decision_clock_proved",
            "global_temporal_descent_proved",
            "global_atomic_five_store_snapshot_proved",
            "original_transport_issuer_authenticated",
            "belief_receipt_external_issuer_authenticated",
            "global_descent_proved", "lean_python_semantic_refinement_proved",
            "actual_act_numeric_witnesses_proved",
            "host_license_granted", "execution_authority_granted",
            "truth_authority_granted", "clinical_authority_granted",
            "legal_authority_granted", "git_authority_granted",
            "memory_overwrite_authority_granted", "original_store_mutated",
        ):
            self.assertIs(getattr(result, name), False, name)


if __name__ == "__main__":
    unittest.main()
