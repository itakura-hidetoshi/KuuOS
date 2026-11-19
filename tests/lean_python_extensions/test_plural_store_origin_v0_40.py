"""Original v1.3 Plural store replay, origin and provenance regressions.

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
from runtime.kuuos_decision_os_plural_kernel_v0_2 import apply_plural_event
from runtime.kuuos_decision_os_plural_store_v0_2 import PluralDecisionStore
from runtime.kuuos_decision_os_plural_types_v0_2 import store_commit_digest
from runtime.kuuos_decision_os_wa_kernel_v0_3 import (
    build_replan_wa_activation_receipt,
)
from runtime.kuuos_qi_world_native_full_cycle_v1_3 import (
    build_native_full_cycle_receipt, validate_native_full_cycle_receipt,
)
from runtime.kuuos_lean_python_act_observe_store_compat_v0_35 import _native_store
from runtime.kuuos_lean_python_decision_plan_handoff_v0_3 import _same
from runtime.kuuos_lean_python_os_path_composition_v0_6 import audit_typed_path
from runtime.kuuos_lean_python_wa_plan_store_compat_v0_39 import (
    SCOPED_COMPATIBLE as PREVIOUS_PASS,
    audit_native_wa_plan_store_compatibility,
)
from runtime import kuuos_lean_python_plural_store_origin_v0_40 as subject


PLURAL_FILES = (
    "plural-genesis.json", "plural-ledger.jsonl", "plural-snapshot.json",
)


class NativePluralStoreOriginTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = TemporaryDirectory(prefix="kuuos-v040-native-")
        cls.addClassCleanup(cls.tmp.cleanup)
        cls.root = Path(cls.tmp.name)
        cls.native = build_native_full_cycle_receipt(cls.root)
        assert validate_native_full_cycle_receipt(cls.native) == []
        cls.states = cls.native["native_artifacts"]
        # This original constructor is called only inside the TEST fixture.
        # The production auditor requires an externally supplied receipt.
        cls.receipt = build_replan_wa_activation_receipt(
            state=cls.states["DecisionOSWa"],
            mission_cycle_phase="replan",
            mission_cycle_state_digest=sha("native-full-cycle-replan-state"),
            replan_receipt_digest=sha("native-full-cycle-replan-receipt"),
            next_plan_basis_digest=sha("native-full-cycle-next-plan-basis"),
            now_ms=50_000,
        )

    def audit(self, **overrides):
        values = dict(
            decision_state=self.states["DecisionOS"],
            plural_state=self.states["DecisionOSPlural"],
            wa_state=self.states["DecisionOSWa"],
            plan_state=self.states["PlanOS"],
            replan_activation_receipt=self.receipt,
            original_plural_store_root=self.root / "plural",
            original_wa_store_root=self.root / "wa",
            original_plan_store_root=self.root / "plan",
        )
        values.update(overrides)
        return subject.audit_native_plural_store_origin(**values)

    def copy_plural(self):
        tmp = TemporaryDirectory(prefix="kuuos-v040-plural-copy-")
        self.addCleanup(tmp.cleanup)
        dst = Path(tmp.name) / "plural"
        shutil.copytree(self.root / "plural", dst)
        return dst

    def test_original_plural_wa_plan_chain_is_scoped_compatible(self):
        result = self.audit()
        self.assertEqual(result.status, subject.SCOPED_COMPATIBLE, result.issues)
        self.assertEqual(result.plural_commit_count, 8)
        self.assertEqual(result.plural_committed_decision_count, 1)
        self.assertEqual(result.plural_summary_count, 1)
        self.assertTrue(result.plural_original_store_replayed)
        self.assertTrue(result.plural_genesis_matches_original_constructor)
        self.assertTrue(result.plural_lean_history_data_conditions_checked)
        self.assertTrue(result.decision_to_plural_original_edge_checked)
        self.assertTrue(result.prior_wa_plan_original_stores_checked)
        self.assertTrue(result.plural_store_bytes_stable_during_audit)
        self.assertTrue(result.wa_plan_store_bytes_stable_during_audit)
        self.assertEqual(result.staged_typed_edge_statuses, (
            ("DecisionOS->DecisionOSPlural", "SCOPED_PATH_CHECKED"),
            ("DecisionOSPlural->DecisionOSWa", "SCOPED_PATH_CHECKED"),
            ("DecisionOSWa->PlanOS", "SCOPED_PATH_CHECKED"),
        ))
        self.assertEqual(len(result.checked_source_paths), 9)

    def test_native_suffix_can_replay_but_is_not_original_plural_genesis(self):
        origin, final, rows = _native_store(
            self.root / "plural", PluralDecisionStore, PLURAL_FILES,
        )
        first = apply_plural_event(origin, rows[0]["event"])
        self.assertEqual(first["status"], "APPLIED")
        with TemporaryDirectory(prefix="kuuos-v040-suffix-") as d:
            substitute = PluralDecisionStore(Path(d) / "plural")
            substitute.initialize(first["state"])
            for row in rows[1:]:
                self.assertEqual(substitute.apply(row["event"])["status"], "APPLIED")
            false_genesis, reconstructed, short_rows = _native_store(
                substitute.root, PluralDecisionStore, PLURAL_FILES,
            )
            self.assertTrue(_same(final, reconstructed))
            self.assertEqual(len(short_rows), len(rows) - 1)
            old = audit_native_wa_plan_store_compatibility(
                self.states["DecisionOSPlural"], self.states["DecisionOSWa"],
                self.states["PlanOS"], self.receipt,
                self.root / "wa", self.root / "plan",
            )
            self.assertEqual(old.status, PREVIOUS_PASS)
            # The original typed edge only reads source bindings, not origin.
            typed = audit_typed_path(
                {"DecisionOS": self.states["DecisionOS"],
                 "DecisionOSPlural": false_genesis},
                start="DecisionOS", end="DecisionOSPlural",
            )
            self.assertEqual(typed.status, "SCOPED_PATH_CHECKED")
            new = self.audit(original_plural_store_root=substitute.root)
            self.assertEqual(new.status, subject.BLOCKED, new.issues)
            self.assertIn(
                "DecisionOSPlural:genesis_not_original_constructor", new.issues,
            )

    def test_each_missing_argument_is_no_data(self):
        keys = (
            "decision_state", "plural_state", "wa_state", "plan_state",
            "replan_activation_receipt", "original_plural_store_root",
            "original_wa_store_root", "original_plan_store_root",
        )
        for key in keys:
            with self.subTest(key=key):
                result = self.audit(**{key: None})
                self.assertEqual(result.status, subject.NO_DATA)

    def test_each_missing_plural_file_is_no_data(self):
        for name in PLURAL_FILES:
            with self.subTest(name=name):
                root = self.copy_plural()
                (root / name).unlink()
                self.assertEqual(self.audit(
                    original_plural_store_root=root,
                ).status, subject.NO_DATA)

    def test_empty_and_uncommitted_plural_histories_remain_no_data(self):
        original = PluralDecisionStore(self.root / "plural")
        genesis = original._read_json(original.genesis_path)
        for prefix in (0, 1):
            with self.subTest(prefix=prefix), TemporaryDirectory() as d:
                partial = PluralDecisionStore(Path(d) / "plural")
                partial.initialize(genesis)
                state = genesis
                for row in original._read_ledger()[:prefix]:
                    state = partial.apply(row["event"])["state"]
                self.assertEqual(self.audit(
                    original_plural_store_root=partial.root,
                    plural_state=state,
                ).status, subject.NO_DATA)

    def test_inputs_and_custom_path_hooks_are_rejected(self):
        class HostilePath:
            def __fspath__(self):
                raise AssertionError("hostile path executed")
        self.assertEqual(self.audit(
            original_plural_store_root=HostilePath(),
        ).status, subject.BLOCKED)
        self.assertEqual(self.audit(decision_state=[]).status, subject.BLOCKED)
        self.assertEqual(self.audit(plural_state=[]).status, subject.BLOCKED)
        self.assertEqual(self.audit(
            original_plural_store_root=123,
        ).status, subject.BLOCKED)

    def test_nonfinite_and_custom_source_json_is_blocked(self):
        for payload in (float("nan"), float("inf"), object()):
            with self.subTest(payload=type(payload).__name__):
                bad = deepcopy(self.states["DecisionOS"])
                bad["malformed_metadata"] = payload
                self.assertEqual(self.audit(decision_state=bad).status,
                                 subject.BLOCKED)

    def test_three_original_roots_must_be_distinct(self):
        for root in (self.root / "wa", self.root / "plan"):
            with self.subTest(root=str(root)):
                self.assertEqual(self.audit(
                    original_plural_store_root=root,
                ).status, subject.BLOCKED)

    def test_nested_store_roots_are_blocked(self):
        self.assertEqual(self.audit(
            original_plural_store_root=self.root,
        ).status, subject.BLOCKED)

    def test_plain_string_roots_are_supported(self):
        self.assertEqual(self.audit(
            original_plural_store_root=str(self.root / "plural"),
            original_wa_store_root=str(self.root / "wa"),
            original_plan_store_root=str(self.root / "plan"),
        ).status, subject.SCOPED_COMPATIBLE)

    def test_plural_root_symlink_is_blocked(self):
        with TemporaryDirectory() as d:
            alias = Path(d) / "plural"
            alias.symlink_to(self.root / "plural", target_is_directory=True)
            self.assertEqual(self.audit(
                original_plural_store_root=alias,
            ).status, subject.BLOCKED)

    def test_parent_symlink_is_blocked(self):
        with TemporaryDirectory() as d:
            alias = Path(d) / "link"
            alias.symlink_to(self.root, target_is_directory=True)
            self.assertEqual(self.audit(
                original_plural_store_root=alias / "plural",
            ).status, subject.BLOCKED)

    def test_cyclic_symlink_and_parent_traversal_are_blocked(self):
        with TemporaryDirectory() as d:
            loop = Path(d) / "loop"
            loop.symlink_to(loop, target_is_directory=True)
            self.assertEqual(self.audit(original_plural_store_root=loop).status,
                             subject.BLOCKED)
        self.assertEqual(self.audit(
            original_plural_store_root=self.root / "plural" / ".." / "plural",
        ).status, subject.BLOCKED)

    def test_original_file_symlink_is_blocked(self):
        root = self.copy_plural()
        target = root / PLURAL_FILES[0]
        target.unlink()
        target.symlink_to(self.root / "plural" / target.name)
        self.assertEqual(self.audit(
            original_plural_store_root=root,
        ).status, subject.BLOCKED)

    def test_corrupt_ledger_is_blocked(self):
        root = self.copy_plural()
        (root / PLURAL_FILES[1]).write_text("{broken\n")
        self.assertEqual(self.audit(
            original_plural_store_root=root,
        ).status, subject.BLOCKED)

    def test_snapshot_requires_exact_original_replayed_fields(self):
        root = self.copy_plural()
        snapshot = root / PLURAL_FILES[2]
        value = json.loads(snapshot.read_text())
        value["event_index"] = float(value["event_index"])
        snapshot.write_text(json.dumps(value) + "\n")
        self.assertEqual(self.audit(
            original_plural_store_root=root,
        ).status, subject.BLOCKED)

    def test_plurals_commit_indices_are_exact_dense_ints(self):
        for value in (True, 1.0, 9):
            with self.subTest(value=value):
                root = self.copy_plural()
                path = root / PLURAL_FILES[1]
                rows = [json.loads(line) for line in path.read_text().splitlines()]
                rows[0]["commit_index"] = value
                predecessor = ""
                for row in rows:
                    row["predecessor_commit_digest"] = predecessor
                    row["plural_store_commit_digest"] = store_commit_digest(row)
                    predecessor = row["plural_store_commit_digest"]
                path.write_text("".join(json.dumps(r) + "\n" for r in rows))
                native = PluralDecisionStore(root)
                recovered, _ = native._recover_unlocked()
                self.assertTrue(_same(recovered, self.states["DecisionOSPlural"]))
                self.assertEqual(self.audit(
                    original_plural_store_root=root,
                ).status, subject.BLOCKED)

    def test_forged_decision_final_is_blocked(self):
        bad = deepcopy(self.states["DecisionOS"])
        bad["decision_state_digest"] = "forged"
        self.assertEqual(self.audit(decision_state=bad).status, subject.BLOCKED)

    def test_forged_plural_final_is_blocked(self):
        bad = deepcopy(self.states["DecisionOSPlural"])
        bad["plural_state_digest"] = "forged"
        self.assertEqual(self.audit(plural_state=bad).status, subject.BLOCKED)

    def test_invalid_wa_plan_source_is_not_promoted(self):
        bad = deepcopy(self.receipt)
        bad["host_license_granted"] = True
        self.assertEqual(self.audit(
            replan_activation_receipt=bad,
        ).status, subject.BLOCKED)

    def test_lean_plural_history_data_condition_is_a_separate_gate(self):
        with patch.object(subject, "_plural_history_alignment",
                          return_value=(False, 1, 0)):
            result = self.audit()
        self.assertEqual(result.status, subject.BLOCKED)
        self.assertIn("DecisionOSPlural:commit_summary_history_not_aligned",
                      result.issues)

    def test_plural_ledger_boundary_whitespace_matches_native(self):
        for boundary, newline in ((b"\x0c", b"\n"), (b"\x0b", b"\r\n"),
                                  ("\u00a0".encode("utf-8"), b"\r")):
            with self.subTest(boundary=boundary):
                root = self.copy_plural()
                path = root / PLURAL_FILES[1]
                lines = path.read_bytes().splitlines()
                path.write_bytes(
                    newline.join(boundary + line + boundary for line in lines)
                    + newline
                )
                state, commits = PluralDecisionStore(root)._recover_unlocked()
                self.assertTrue(_same(state, self.states["DecisionOSPlural"]))
                self.assertEqual(len(commits), 8)
                result = self.audit(original_plural_store_root=root)
                self.assertEqual(result.status, subject.SCOPED_COMPATIBLE,
                                 result.issues)

    def test_shadowed_nonfinite_json_is_rejected_before_native_use(self):
        for name in PLURAL_FILES:
            for number in ("NaN", "Infinity", "1e999"):
                with self.subTest(name=name, number=number):
                    root = self.copy_plural()
                    path = root / name
                    text = path.read_text()
                    line = (text.splitlines()[0] if name.endswith(".jsonl")
                            else text)
                    key = next(iter(json.loads(line)))
                    brace = text.index("{") + 1
                    path.write_text(text[:brace] + json.dumps(key) + ":"
                                    + number + "," + text[brace:])
                    recovered, _ = PluralDecisionStore(root)._recover_unlocked()
                    self.assertTrue(_same(recovered, self.states["DecisionOSPlural"]))
                    self.assertEqual(self.audit(
                        original_plural_store_root=root,
                    ).status, subject.BLOCKED)

    def test_original_replay_consumes_the_first_captured_bytes(self):
        root = self.copy_plural()
        native_recover = PluralDecisionStore._recover_unlocked

        def alter_only_during_replay(store):
            path = store.genesis_path
            original = path.read_bytes()
            try:
                path.write_bytes(b"{invalid-json}\n")
                return native_recover(store)
            finally:
                path.write_bytes(original)

        with patch.object(PluralDecisionStore, "_recover_unlocked",
                          alter_only_during_replay):
            result = self.audit(original_plural_store_root=root)
        self.assertEqual(result.status, subject.SCOPED_COMPATIBLE, result.issues)
        self.assertTrue(result.plural_store_bytes_stable_during_audit)

    def test_change_after_native_checks_is_detected(self):
        root = self.copy_plural()
        prior = subject.audit_native_wa_plan_store_compatibility

        def mutate_after_prior(*args, **kwargs):
            result = prior(*args, **kwargs)
            path = root / PLURAL_FILES[2]
            path.write_bytes(path.read_bytes() + b"\n")
            return result

        with patch.object(subject, "audit_native_wa_plan_store_compatibility",
                          side_effect=mutate_after_prior):
            result = self.audit(original_plural_store_root=root)
        self.assertEqual(result.status, subject.BLOCKED, result.issues)
        self.assertIn("plural_store:original_bytes_changed", result.issues)
        self.assertFalse(result.plural_store_bytes_stable_during_audit)

    def test_source_objects_and_original_files_are_not_mutated(self):
        before = {
            str(path.relative_to(self.root)): path.read_bytes()
            for path in self.root.rglob("*") if path.is_file()
        }
        original = deepcopy((self.native, self.receipt))
        self.assertEqual(self.audit().status, subject.SCOPED_COMPATIBLE)
        after = {
            str(path.relative_to(self.root)): path.read_bytes()
            for path in self.root.rglob("*") if path.is_file()
        }
        self.assertEqual(before, after)
        self.assertTrue(_same(original, (self.native, self.receipt)))

    def test_no_global_proof_authenticity_or_write_authority_is_inferred(self):
        result = self.audit()
        self.assertEqual(result.status, subject.SCOPED_COMPATIBLE, result.issues)
        for key in (
            "original_decision_store_replayed",
            "globally_atomic_three_store_snapshot_proved",
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
