"""v0.41 actual Decision store full-origin, Belief receipt, and time obstruction.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
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
from runtime.kuuos_belief_os_gerbe_types_v0_3 import receipt_digest
from runtime.kuuos_decision_os_kernel_v0_1 import apply_decision_event
from runtime.kuuos_decision_os_store_v0_1 import DecisionStore
from runtime.kuuos_decision_os_types_v0_1 import store_commit_digest
from runtime.kuuos_decision_os_wa_kernel_v0_3 import (
    build_replan_wa_activation_receipt,
)
from runtime.kuuos_qi_world_native_full_cycle_v1_3 import (
    build_native_full_cycle_receipt, validate_native_full_cycle_receipt,
)
from runtime.kuuos_lean_python_act_observe_store_compat_v0_35 import _native_store
from runtime.kuuos_lean_python_decision_plan_handoff_v0_3 import _same
from runtime.kuuos_lean_python_plural_store_origin_v0_40 import (
    SCOPED_COMPATIBLE as PRIOR_PASS, audit_native_plural_store_origin,
)
from runtime import kuuos_lean_python_decision_store_origin_v0_41 as subject

_DECISION_FILES = (
    "decision-genesis.json", "decision-ledger.jsonl", "decision-snapshot.json",
)


class NativeDecisionStoreOriginTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = TemporaryDirectory(prefix="kuuos-v041-native-")
        cls.addClassCleanup(cls.tmp.cleanup)
        cls.root = Path(cls.tmp.name)
        cls.native = build_native_full_cycle_receipt(cls.root)
        assert validate_native_full_cycle_receipt(cls.native) == []
        cls.states = cls.native["native_artifacts"]
        # Fixture-only native constructor. No such receipt is fabricated
        # inside the production auditor.
        cls.receipt = build_replan_wa_activation_receipt(
            state=cls.states["DecisionOSWa"],
            mission_cycle_phase="replan",
            mission_cycle_state_digest=sha("native-full-cycle-replan-state"),
            replan_receipt_digest=sha("native-full-cycle-replan-receipt"),
            next_plan_basis_digest=sha("native-full-cycle-next-plan-basis"),
            now_ms=50_000,
        )

    def audit(self, **overrides):
        args = dict(
            belief_receipt=self.states["BeliefOSReceipt"],
            decision_state=self.states["DecisionOS"],
            plural_state=self.states["DecisionOSPlural"],
            wa_state=self.states["DecisionOSWa"],
            plan_state=self.states["PlanOS"],
            replan_activation_receipt=self.receipt,
            original_decision_store_root=self.root / "decision",
            original_plural_store_root=self.root / "plural",
            original_wa_store_root=self.root / "wa",
            original_plan_store_root=self.root / "plan",
        )
        args.update(overrides)
        return subject.audit_native_decision_store_origin(**args)

    def copy_decision(self):
        tmp = TemporaryDirectory(prefix="kuuos-v041-decision-copy-")
        self.addCleanup(tmp.cleanup)
        path = Path(tmp.name) / "decision"
        shutil.copytree(self.root / "decision", path)
        return path

    def test_original_decision_plural_wa_plan_chain_passes_scoped_audit(self):
        result = self.audit()
        self.assertEqual(result.status, subject.SCOPED_COMPATIBLE, result.issues)
        self.assertTrue(result.decision_original_store_replayed)
        self.assertTrue(result.decision_genesis_matches_original_constructor)
        self.assertTrue(result.decision_history_data_conditions_checked)
        self.assertTrue(result.supplied_belief_receipt_locally_valid)
        self.assertTrue(result.belief_decision_source_identity_checked)
        self.assertTrue(result.prior_plural_wa_plan_origins_checked)
        self.assertTrue(result.decision_store_bytes_stable_during_audit)
        self.assertTrue(result.prior_store_bytes_stable_during_audit)
        self.assertEqual(result.decision_committed_deliberation_count, 1)
        self.assertEqual(result.decision_summary_count, 1)
        self.assertEqual(result.decision_ledger_commit_count,
                         len(DecisionStore(self.root / "decision")._read_ledger()))
        self.assertEqual(len(result.checked_source_paths), 13)
        self.assertEqual(result.staged_typed_edge_statuses, (
            ("DecisionOS->DecisionOSPlural", "SCOPED_PATH_CHECKED"),
            ("DecisionOSPlural->DecisionOSWa", "SCOPED_PATH_CHECKED"),
            ("DecisionOSWa->PlanOS", "SCOPED_PATH_CHECKED"),
        ))

    def test_real_suffix_history_is_native_valid_but_not_original_genesis(self):
        origin, final, commits = _native_store(
            self.root / "decision", DecisionStore, _DECISION_FILES,
        )
        intermediate = apply_decision_event(origin, commits[0]["event"])
        self.assertEqual(intermediate["status"], "APPLIED")
        with TemporaryDirectory(prefix="kuuos-v041-suffix-") as d:
            suffix_store = DecisionStore(Path(d) / "decision")
            suffix_store.initialize(intermediate["state"])
            for commit in commits[1:]:
                self.assertEqual(
                    suffix_store.apply(commit["event"])["status"], "APPLIED",
                )
            substituted, recovered, subset = _native_store(
                suffix_store.root, DecisionStore, _DECISION_FILES,
            )
            self.assertTrue(_same(recovered, final))
            self.assertEqual(len(subset), len(commits) - 1)
            self.assertNotEqual(substituted["current_phase"], "frame")
            prior = audit_native_plural_store_origin(
                self.states["DecisionOS"], self.states["DecisionOSPlural"],
                self.states["DecisionOSWa"], self.states["PlanOS"],
                self.receipt, self.root / "plural", self.root / "wa",
                self.root / "plan",
            )
            self.assertEqual(prior.status, PRIOR_PASS)
            result = self.audit(original_decision_store_root=suffix_store.root)
            self.assertEqual(result.status, subject.BLOCKED, result.issues)
            self.assertIn("DecisionOS:genesis_not_original_constructor",
                          result.issues)

    def test_fixture_numeric_times_are_inverted_without_clock_proof(self):
        result = self.audit()
        self.assertEqual(result.status, subject.SCOPED_COMPATIBLE, result.issues)
        self.assertEqual(result.source_receipt_created_at_ms, 5_000)
        self.assertEqual(result.decision_genesis_updated_at_ms, 1_000)
        self.assertEqual(
            result.cross_source_time_relation,
            "SOURCE_RECEIPT_NUMERICALLY_AFTER_DECISION_GENESIS",
        )
        self.assertFalse(result.common_source_decision_clock_proved)
        self.assertFalse(result.global_temporal_descent_proved)

    def test_missing_all_required_sources_remains_no_data(self):
        keys = (
            "belief_receipt", "decision_state", "plural_state", "wa_state",
            "plan_state", "replan_activation_receipt",
            "original_decision_store_root", "original_plural_store_root",
            "original_wa_store_root", "original_plan_store_root",
        )
        for key in keys:
            with self.subTest(key=key):
                self.assertEqual(self.audit(**{key: None}).status, subject.NO_DATA)

    def test_missing_each_original_decision_file_is_no_data(self):
        for name in _DECISION_FILES:
            with self.subTest(name=name):
                root = self.copy_decision()
                (root / name).unlink()
                self.assertEqual(
                    self.audit(original_decision_store_root=root).status,
                    subject.NO_DATA,
                )

    def test_empty_or_uncommitted_original_decision_is_no_data(self):
        original = DecisionStore(self.root / "decision")
        genesis = original._read_json(original.genesis_path)
        for count in (0, 1):
            with self.subTest(count=count), TemporaryDirectory() as d:
                partial = DecisionStore(Path(d) / "decision")
                partial.initialize(genesis)
                state = genesis
                for row in original._read_ledger()[:count]:
                    state = partial.apply(row["event"])["state"]
                self.assertEqual(
                    self.audit(original_decision_store_root=partial.root,
                               decision_state=state).status,
                    subject.NO_DATA,
                )

    def test_missing_belief_receipt_is_not_synthesized(self):
        self.assertEqual(self.audit(belief_receipt=None).status, subject.NO_DATA)

    def test_invalid_belief_receipt_digest_is_blocked(self):
        bad = deepcopy(self.states["BeliefOSReceipt"])
        bad["belief_gerbe_receipt_digest"] = "forged"
        self.assertEqual(self.audit(belief_receipt=bad).status, subject.BLOCKED)

    def test_belief_reseal_cannot_substitute_for_original_source(self):
        bad = deepcopy(self.states["BeliefOSReceipt"])
        bad["lineage_id"] = "coherent-but-different-lineage"
        bad["belief_gerbe_receipt_digest"] = receipt_digest(bad)
        self.assertEqual(self.audit(belief_receipt=bad).status, subject.BLOCKED)

    def test_belief_local_license_and_authority_boundaries_hold(self):
        for field, value in (
            ("route", "OBSERVE"),
            ("planning_support_license", False),
            ("future_only", False),
            ("memory_overwrite", True),
        ):
            with self.subTest(field=field):
                bad = deepcopy(self.states["BeliefOSReceipt"])
                bad[field] = value
                bad["belief_gerbe_receipt_digest"] = receipt_digest(bad)
                self.assertEqual(self.audit(belief_receipt=bad).status,
                                 subject.BLOCKED)

    def test_belief_non_authority_cannot_be_forged(self):
        bad = deepcopy(self.states["BeliefOSReceipt"])
        bad["non_authority"]["execution_authority_granted"] = True
        bad["belief_gerbe_receipt_digest"] = receipt_digest(bad)
        self.assertEqual(self.audit(belief_receipt=bad).status, subject.BLOCKED)

    def test_belief_time_is_observed_not_fabricated(self):
        bad = deepcopy(self.states["BeliefOSReceipt"])
        bad.pop("created_at_ms")
        bad["belief_gerbe_receipt_digest"] = receipt_digest(bad)
        self.assertEqual(self.audit(belief_receipt=bad).status, subject.NO_DATA)

    def test_plain_json_and_root_types_are_required(self):
        class HostilePath:
            def __fspath__(self):
                raise AssertionError("untrusted __fspath__ invoked")
        for value in (HostilePath(), 123, [], object()):
            self.assertEqual(
                self.audit(original_decision_store_root=value).status,
                subject.BLOCKED,
            )
        self.assertEqual(self.audit(decision_state=[]).status, subject.BLOCKED)
        self.assertEqual(self.audit(belief_receipt=[]).status, subject.BLOCKED)

    def test_nonfinite_and_custom_json_sources_block(self):
        for value in (float("nan"), float("inf"), object()):
            with self.subTest(value=type(value).__name__):
                bad = deepcopy(self.states["BeliefOSReceipt"])
                bad["new_field"] = value
                self.assertEqual(self.audit(belief_receipt=bad).status,
                                 subject.BLOCKED)

    def test_roots_aliased_nested_or_traversed_are_blocked(self):
        for value in (
            self.root / "plural",
            self.root,
            self.root / "decision" / ".." / "decision",
        ):
            with self.subTest(root=str(value)):
                self.assertEqual(
                    self.audit(original_decision_store_root=value).status,
                    subject.BLOCKED,
                )

    def test_strings_supported_for_each_original_root(self):
        result = self.audit(
            original_decision_store_root=str(self.root / "decision"),
            original_plural_store_root=str(self.root / "plural"),
            original_wa_store_root=str(self.root / "wa"),
            original_plan_store_root=str(self.root / "plan"),
        )
        self.assertEqual(result.status, subject.SCOPED_COMPATIBLE, result.issues)

    def test_root_and_ancestor_symlinks_are_blocked(self):
        with TemporaryDirectory() as d:
            alias = Path(d) / "alias"
            alias.symlink_to(self.root / "decision", target_is_directory=True)
            self.assertEqual(self.audit(
                original_decision_store_root=alias).status, subject.BLOCKED)
            alias.unlink()
            alias.symlink_to(self.root, target_is_directory=True)
            self.assertEqual(self.audit(
                original_decision_store_root=alias / "decision").status,
                subject.BLOCKED)

    def test_cyclic_root_and_file_symlinks_are_blocked(self):
        with TemporaryDirectory() as d:
            loop = Path(d) / "loop"
            loop.symlink_to(loop, target_is_directory=True)
            self.assertEqual(self.audit(
                original_decision_store_root=loop).status, subject.BLOCKED)
        root = self.copy_decision()
        file = root / _DECISION_FILES[0]
        file.unlink()
        file.symlink_to(self.root / "decision" / file.name)
        self.assertEqual(self.audit(
            original_decision_store_root=root).status, subject.BLOCKED)

    def test_malformed_decision_ledger_is_blocked(self):
        root = self.copy_decision()
        (root / _DECISION_FILES[1]).write_text("{wrong-json\n")
        self.assertEqual(self.audit(
            original_decision_store_root=root).status, subject.BLOCKED)

    def test_snapshot_must_match_full_original_replayed_json(self):
        root = self.copy_decision()
        file = root / _DECISION_FILES[2]
        snapshot = json.loads(file.read_text())
        snapshot["event_index"] = float(snapshot["event_index"])
        file.write_text(json.dumps(snapshot))
        self.assertEqual(self.audit(
            original_decision_store_root=root).status, subject.BLOCKED)

    def test_dense_commit_indices_are_strict_integers(self):
        for value in (True, 1.0, 9):
            with self.subTest(value=value):
                root = self.copy_decision()
                file = root / _DECISION_FILES[1]
                records = [json.loads(line) for line in file.read_text().splitlines()]
                records[0]["commit_index"] = value
                previous = ""
                for record in records:
                    record["predecessor_commit_digest"] = previous
                    record["decision_store_commit_digest"] = store_commit_digest(record)
                    previous = record["decision_store_commit_digest"]
                file.write_text("".join(json.dumps(r) + "\n" for r in records))
                original_recovered, _ = DecisionStore(root)._recover_unlocked()
                self.assertTrue(_same(
                    original_recovered, self.states["DecisionOS"],
                ))
                self.assertEqual(self.audit(
                    original_decision_store_root=root).status, subject.BLOCKED)

    def test_supplied_final_must_match_original_store(self):
        bad = deepcopy(self.states["DecisionOS"])
        bad["decision_state_digest"] = "not-original"
        self.assertEqual(self.audit(decision_state=bad).status, subject.BLOCKED)

    def test_history_alignment_has_independent_gate(self):
        with patch.object(subject, "_decision_history_alignment",
                          return_value=(False, 1, 0)):
            result = self.audit()
        self.assertEqual(result.status, subject.BLOCKED)
        self.assertIn("DecisionOS:commit_summary_history_not_aligned",
                      result.issues)

    def test_original_native_ledger_whitespace_and_line_endings_retained(self):
        for boundary, newline in ((b"\x0c", b"\n"), (b"\x0b", b"\r\n"),
                                  ("\u00a0".encode("utf-8"), b"\r")):
            with self.subTest(boundary=boundary):
                root = self.copy_decision()
                file = root / _DECISION_FILES[1]
                rows = file.read_bytes().splitlines()
                file.write_bytes(
                    newline.join(boundary + row + boundary for row in rows)
                    + newline
                )
                recovered, commits = DecisionStore(root)._recover_unlocked()
                self.assertTrue(_same(recovered, self.states["DecisionOS"]))
                self.assertGreater(len(commits), 0)
                result = self.audit(original_decision_store_root=root)
                self.assertEqual(result.status, subject.SCOPED_COMPATIBLE,
                                 result.issues)

    def test_duplicate_shadowed_nonfinite_literals_are_rejected(self):
        for filename in _DECISION_FILES:
            for value in ("NaN", "Infinity", "1e999"):
                with self.subTest(filename=filename, value=value):
                    root = self.copy_decision()
                    path = root / filename
                    text = path.read_text()
                    first = (text.splitlines()[0] if filename.endswith(".jsonl")
                             else text)
                    key = next(iter(json.loads(first)))
                    opening = text.index("{") + 1
                    path.write_text(
                        text[:opening] + json.dumps(key) + ":" + value
                        + "," + text[opening:]
                    )
                    recovered, _ = DecisionStore(root)._recover_unlocked()
                    self.assertTrue(_same(recovered, self.states["DecisionOS"]))
                    self.assertEqual(self.audit(
                        original_decision_store_root=root).status, subject.BLOCKED)

    def test_original_replay_uses_first_capture_not_later_file_reads(self):
        root = self.copy_decision()
        recover = DecisionStore._recover_unlocked

        def alter_while_replaying(store):
            file = store.genesis_path
            original = file.read_bytes()
            try:
                file.write_bytes(b"{invalid-json}\n")
                return recover(store)
            finally:
                file.write_bytes(original)

        with patch.object(DecisionStore, "_recover_unlocked",
                          alter_while_replaying):
            result = self.audit(original_decision_store_root=root)
        self.assertEqual(result.status, subject.SCOPED_COMPATIBLE, result.issues)
        self.assertTrue(result.decision_store_bytes_stable_during_audit)

    def test_changes_after_prior_audit_are_detected(self):
        root = self.copy_decision()
        previous = subject.audit_native_plural_store_origin

        def mutate_after_prior(*args, **kwargs):
            result = previous(*args, **kwargs)
            file = root / _DECISION_FILES[2]
            file.write_bytes(file.read_bytes() + b"\n")
            return result

        with patch.object(subject, "audit_native_plural_store_origin",
                          side_effect=mutate_after_prior):
            result = self.audit(original_decision_store_root=root)
        self.assertEqual(result.status, subject.BLOCKED, result.issues)
        self.assertIn("decision_store:original_bytes_changed", result.issues)

    def test_previous_plural_wa_plan_failure_is_not_promoted(self):
        bad = deepcopy(self.receipt)
        bad["host_license_granted"] = True
        self.assertEqual(self.audit(
            replan_activation_receipt=bad).status, subject.BLOCKED)

    def test_source_objects_and_every_original_file_unchanged(self):
        before = {
            str(p.relative_to(self.root)): p.read_bytes()
            for p in self.root.rglob("*") if p.is_file()
        }
        originals = deepcopy((self.native, self.receipt))
        self.assertEqual(self.audit().status, subject.SCOPED_COMPATIBLE)
        after = {
            str(p.relative_to(self.root)): p.read_bytes()
            for p in self.root.rglob("*") if p.is_file()
        }
        self.assertEqual(before, after)
        self.assertTrue(_same(originals, (self.native, self.receipt)))

    def test_no_issuer_temporal_or_external_authority_promoted(self):
        result = self.audit()
        self.assertEqual(result.status, subject.SCOPED_COMPATIBLE, result.issues)
        for key in (
            "common_source_decision_clock_proved",
            "global_temporal_descent_proved", "original_belief_store_replayed",
            "globally_atomic_four_store_snapshot_proved",
            "global_descent_proved", "lean_python_semantic_refinement_proved",
            "external_issuer_authenticated", "actual_act_numeric_witnesses_proved",
            "host_license_granted", "execution_authority_granted",
            "truth_authority_granted", "clinical_authority_granted",
            "legal_authority_granted", "git_authority_granted",
            "memory_overwrite_authority_granted", "original_store_mutated",
        ):
            self.assertIs(getattr(result, key), False, key)


if __name__ == "__main__":
    unittest.main()
