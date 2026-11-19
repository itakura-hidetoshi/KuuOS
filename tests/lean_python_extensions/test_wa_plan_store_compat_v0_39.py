"""v0.39 original Wa/Plan full origins and genuine suffix-history regressions.

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
from runtime.kuuos_decision_os_wa_kernel_v0_3 import (
    apply_wa_event, build_replan_wa_activation_receipt,
)
from runtime.kuuos_decision_os_wa_store_v0_3 import WaDecisionStore
from runtime.kuuos_decision_os_wa_types_v0_3 import wa_store_commit_digest
from runtime.kuuos_plan_os_kernel_v0_1 import apply_plan_event
from runtime.kuuos_plan_os_store_v0_1 import PlanStore
from runtime.kuuos_plan_os_types_v0_1 import plan_store_commit_digest
from runtime.kuuos_qi_world_native_full_cycle_v1_3 import (
    build_native_full_cycle_receipt, validate_native_full_cycle_receipt,
)
from runtime.kuuos_lean_python_act_observe_store_compat_v0_35 import _native_store
from runtime.kuuos_lean_python_decision_plan_handoff_v0_3 import _same
from runtime.kuuos_lean_python_os_path_composition_v0_6 import audit_typed_path
from runtime.kuuos_lean_python_wa_plan_local_compat_v0_33 import (
    audit_native_wa_plan_local_compatibility,
)
from runtime import kuuos_lean_python_wa_plan_store_compat_v0_39 as subject


class NativeWaPlanStoreCompatibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = TemporaryDirectory(prefix="kuuos-v039-native-")
        cls.addClassCleanup(cls.tmp.cleanup)
        cls.root = Path(cls.tmp.name)
        cls.native = build_native_full_cycle_receipt(cls.root)
        assert validate_native_full_cycle_receipt(cls.native) == []
        cls.states = cls.native["native_artifacts"]
        # The fixture does not retain this packet. This is fixture-only
        # generation with its original constructor/parameters, not attestation.
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
            plural_state=self.states["DecisionOSPlural"],
            wa_state=self.states["DecisionOSWa"],
            plan_state=self.states["PlanOS"],
            replan_activation_receipt=self.receipt,
            original_wa_store_root=self.root / "wa",
            original_plan_store_root=self.root / "plan",
        )
        values.update(overrides)
        return subject.audit_native_wa_plan_store_compatibility(**values)

    def copy_store(self, name):
        tmp = TemporaryDirectory(prefix="kuuos-v039-copy-")
        self.addCleanup(tmp.cleanup)
        target = Path(tmp.name) / name
        shutil.copytree(self.root / name, target)
        return target

    def test_original_full_origins_are_locally_compatible(self):
        result = self.audit()
        self.assertEqual(result.status, subject.SCOPED_COMPATIBLE, result.issues)
        self.assertEqual((result.wa_commit_count, result.plan_commit_count), (6, 7))
        self.assertTrue(result.wa_original_store_replayed)
        self.assertTrue(result.plan_original_store_replayed)
        self.assertTrue(result.wa_genesis_matches_original_constructor)
        self.assertTrue(result.plan_genesis_matches_original_constructor)
        self.assertTrue(result.original_final_wa_plan_conditions_checked)
        self.assertTrue(result.store_bytes_stable_during_audit)
        self.assertEqual(result.staged_typed_edge_statuses, (
            ("DecisionOSPlural->DecisionOSWa", "SCOPED_PATH_CHECKED"),
            ("DecisionOSWa->PlanOS", "SCOPED_PATH_CHECKED"),
        ))
        self.assertEqual(len(result.checked_source_paths), 6)

    def check_suffix_is_blocked(self, name):
        is_wa = name == "wa"
        cls = WaDecisionStore if is_wa else PlanStore
        advance = apply_wa_event if is_wa else apply_plan_event
        stem = "wa-v03" if is_wa else "plan"
        names = (stem + "-genesis.json", stem + "-ledger.jsonl",
                 stem + "-snapshot.json")
        origin, final, commits = _native_store(self.root / name, cls, names)
        intermediate = advance(origin, commits[0]["event"])
        self.assertEqual(intermediate["status"], "APPLIED")
        with TemporaryDirectory(prefix="kuuos-v039-suffix-") as d:
            alternate = cls(Path(d) / name)
            alternate.initialize(intermediate["state"])
            for row in commits[1:]:
                self.assertEqual(alternate.apply(row["event"])["status"], "APPLIED")
            genesis, recovered, suffix = _native_store(alternate.root, cls, names)
            self.assertTrue(_same(recovered, final))
            self.assertEqual(len(suffix), len(commits) - 1)
            earlier = audit_native_wa_plan_local_compatibility(
                self.states["DecisionOSPlural"], self.states["DecisionOSWa"],
                self.states["PlanOS"], self.receipt,
            )
            self.assertEqual(earlier.status, "SCOPED_WA_PLAN_SOURCE_COMPATIBLE")
            if is_wa:
                staged = audit_typed_path(
                    {"DecisionOSPlural": self.states["DecisionOSPlural"],
                     "DecisionOSWa": genesis},
                    start="DecisionOSPlural", end="DecisionOSWa",
                )
                result = self.audit(original_wa_store_root=alternate.root)
            else:
                staged = audit_typed_path(
                    {"DecisionOSWa": self.states["DecisionOSWa"], "PlanOS": genesis},
                    receipts={"DecisionOSWa->PlanOS": self.receipt},
                    start="DecisionOSWa", end="PlanOS",
                )
                result = self.audit(original_plan_store_root=alternate.root)
            self.assertEqual(staged.status, "SCOPED_PATH_CHECKED")
            self.assertEqual(result.status, subject.BLOCKED, result.issues)
            expected = ("DecisionOSWa" if is_wa else "PlanOS")
            self.assertIn(expected + ":genesis_not_original_constructor", result.issues)

    def test_wa_suffix_history_cannot_replace_original_genesis(self):
        self.check_suffix_is_blocked("wa")

    def test_plan_suffix_history_cannot_replace_original_genesis(self):
        self.check_suffix_is_blocked("plan")

    def test_missing_required_input_stays_no_data(self):
        for key in (
            "plural_state", "wa_state", "plan_state", "replan_activation_receipt",
            "original_wa_store_root", "original_plan_store_root",
        ):
            with self.subTest(key=key):
                self.assertEqual(self.audit(**{key: None}).status, subject.NO_DATA)

    def test_missing_each_original_file_stays_no_data(self):
        for name, stem in (("wa", "wa-v03"), ("plan", "plan")):
            for suffix in ("-genesis.json", "-ledger.jsonl", "-snapshot.json"):
                with self.subTest(name=name, suffix=suffix):
                    root = self.copy_store(name)
                    (root / (stem + suffix)).unlink()
                    self.assertEqual(self.audit(**{
                        "original_" + name + "_store_root": root,
                    }).status, subject.NO_DATA)

    def test_empty_original_history_stays_no_data(self):
        for name, cls in (("wa", WaDecisionStore), ("plan", PlanStore)):
            with self.subTest(name=name), TemporaryDirectory() as d:
                original = cls(self.root / name)
                empty = cls(Path(d) / name)
                empty.initialize(original._read_json(original.genesis_path))
                self.assertEqual(self.audit(**{
                    "original_" + name + "_store_root": empty.root,
                }).status, subject.NO_DATA)

    def test_uncommitted_original_history_stays_no_data(self):
        for name, cls in (("wa", WaDecisionStore), ("plan", PlanStore)):
            with self.subTest(name=name), TemporaryDirectory() as d:
                original = cls(self.root / name)
                partial = cls(Path(d) / name)
                partial.initialize(original._read_json(original.genesis_path))
                state = partial.apply(original._read_ledger()[0]["event"])["state"]
                self.assertEqual(self.audit(**{
                    "original_" + name + "_store_root": partial.root,
                    ("wa_state" if name == "wa" else "plan_state"): state,
                }).status, subject.NO_DATA)

    def test_plain_json_inputs_required(self):
        for key in ("plural_state", "wa_state", "plan_state",
                    "replan_activation_receipt"):
            with self.subTest(key=key):
                self.assertEqual(self.audit(**{key: []}).status, subject.BLOCKED)

    def test_nonfinite_or_custom_json_input_is_blocked(self):
        for value in (float("nan"), float("inf"), object()):
            bad = deepcopy(self.states["DecisionOSWa"])
            bad["extra"] = value
            self.assertEqual(self.audit(wa_state=bad).status, subject.BLOCKED)

    def test_custom_path_hook_is_never_executed(self):
        class HostilePath:
            def __fspath__(self):
                raise AssertionError("custom path conversion executed")
        self.assertEqual(self.audit(
            original_wa_store_root=HostilePath()).status, subject.BLOCKED)

    def test_duplicate_roots_are_blocked(self):
        self.assertEqual(self.audit(
            original_plan_store_root=self.root / "wa").status, subject.BLOCKED)

    def test_string_paths_are_accepted(self):
        result = self.audit(original_wa_store_root=str(self.root / "wa"),
                            original_plan_store_root=str(self.root / "plan"))
        self.assertEqual(result.status, subject.SCOPED_COMPATIBLE, result.issues)

    def test_store_root_symlink_is_blocked(self):
        with TemporaryDirectory() as d:
            alias = Path(d) / "wa-link"
            alias.symlink_to(self.root / "wa", target_is_directory=True)
            self.assertEqual(self.audit(
                original_wa_store_root=alias).status, subject.BLOCKED)

    def test_parent_directory_symlink_is_blocked(self):
        with TemporaryDirectory() as d:
            alias = Path(d) / "alias"
            alias.symlink_to(self.root, target_is_directory=True)
            self.assertEqual(self.audit(
                original_wa_store_root=alias / "wa").status, subject.BLOCKED)

    def test_cyclic_root_is_blocked_without_raising(self):
        with TemporaryDirectory() as d:
            cyclic = Path(d) / "cycle"
            cyclic.symlink_to(cyclic, target_is_directory=True)
            self.assertEqual(self.audit(
                original_wa_store_root=cyclic).status, subject.BLOCKED)

    def test_parent_traversal_root_requires_explicit_canonical_path(self):
        self.assertEqual(self.audit(
            original_wa_store_root=self.root / "plan" / ".." / "wa",
        ).status, subject.BLOCKED)

    def test_store_file_symlink_is_blocked(self):
        root = self.copy_store("plan")
        target = root / "plan-genesis.json"
        target.unlink()
        target.symlink_to(self.root / "plan" / target.name)
        self.assertEqual(self.audit(
            original_plan_store_root=root).status, subject.BLOCKED)

    def test_corrupt_ledger_is_blocked(self):
        for name, stem in (("wa", "wa-v03"), ("plan", "plan")):
            with self.subTest(name=name):
                root = self.copy_store(name)
                (root / (stem + "-ledger.jsonl")).write_text("{broken\n")
                self.assertEqual(self.audit(**{
                    "original_" + name + "_store_root": root,
                }).status, subject.BLOCKED)

    def test_snapshot_metadata_must_match_replayed_state(self):
        root = self.copy_store("wa")
        path = root / "wa-v03-snapshot.json"
        state = json.loads(path.read_text())
        state["event_index"] = float(state["event_index"])
        path.write_text(json.dumps(state))
        self.assertEqual(self.audit(
            original_wa_store_root=root).status, subject.BLOCKED)

    def test_dense_commit_indices_require_exact_integers(self):
        for name, stem, digest in (
            ("wa", "wa-v03", wa_store_commit_digest),
            ("plan", "plan", plan_store_commit_digest),
        ):
            for bad_index in (True, 1.0, 9):
                with self.subTest(name=name, bad_index=bad_index):
                    root = self.copy_store(name)
                    path = root / (stem + "-ledger.jsonl")
                    rows = [json.loads(line) for line in path.read_text().splitlines()]
                    rows[0]["commit_index"] = bad_index
                    previous = ""
                    key = "wa_store_commit_digest" if name == "wa" else "plan_store_commit_digest"
                    for row in rows:
                        row["predecessor_commit_digest"] = previous
                        row[key] = digest(row)
                        previous = row[key]
                    path.write_text("".join(json.dumps(r) + "\n" for r in rows))
                    self.assertEqual(self.audit(**{
                        "original_" + name + "_store_root": root,
                    }).status, subject.BLOCKED)

    def test_supplied_final_must_match_exact_original_replay(self):
        for arg, state_name, key in (
            ("wa_state", "DecisionOSWa", "wa_state_digest"),
            ("plan_state", "PlanOS", "plan_state_digest"),
        ):
            bad = deepcopy(self.states[state_name])
            bad[key] = "forged"
            self.assertEqual(self.audit(**{arg: bad}).status, subject.BLOCKED)

    def test_nonfinite_ledger_metadata_cannot_hide_outside_final_state(self):
        for name, stem, cls, digest in (
            ("wa", "wa-v03", WaDecisionStore, wa_store_commit_digest),
            ("plan", "plan", PlanStore, plan_store_commit_digest),
        ):
            for number in (float("nan"), float("inf")):
                with self.subTest(name=name, number=number):
                    root = self.copy_store(name)
                    path = root / (stem + "-ledger.jsonl")
                    rows = [json.loads(line) for line in path.read_text().splitlines()]
                    rows[0]["uninterpreted_metadata"] = {"nested": [number]}
                    key = "wa_store_commit_digest" if name == "wa" else "plan_store_commit_digest"
                    previous = ""
                    for row in rows:
                        row["predecessor_commit_digest"] = previous
                        row[key] = digest(row)
                        previous = row[key]
                    path.write_text("".join(json.dumps(r) + "\n" for r in rows))
                    final, _ = cls(root)._recover_unlocked()
                    expected = self.states["DecisionOSWa" if name == "wa" else "PlanOS"]
                    self.assertTrue(_same(final, expected))
                    self.assertEqual(self.audit(**{
                        "original_" + name + "_store_root": root,
                    }).status, subject.BLOCKED)

    def test_native_ledger_boundary_whitespace_is_preserved(self):
        for name, stem, cls in (("wa", "wa-v03", WaDecisionStore),
                                ("plan", "plan", PlanStore)):
            for boundary, newline in ((b"\x0c", b"\n"), (b"\x0b", b"\r\n"),
                                      ("\u00a0".encode("utf-8"), b"\r")):
                with self.subTest(name=name, boundary=boundary, newline=newline):
                    root = self.copy_store(name)
                    path = root / (stem + "-ledger.jsonl")
                    lines = path.read_bytes().splitlines()
                    path.write_bytes(newline.join(boundary + line + boundary
                                                   for line in lines) + newline)
                    final, commits = cls(root)._recover_unlocked()
                    expected = self.states["DecisionOSWa" if name == "wa" else "PlanOS"]
                    self.assertTrue(_same(final, expected))
                    self.assertEqual(len(commits), 6 if name == "wa" else 7)
                    result = self.audit(**{"original_" + name + "_store_root": root})
                    self.assertEqual(result.status, subject.SCOPED_COMPATIBLE, result.issues)

    def test_shadowed_nonfinite_values_in_captured_files_are_blocked(self):
        for name, stem, cls in (("wa", "wa-v03", WaDecisionStore),
                                ("plan", "plan", PlanStore)):
            for suffix in ("-genesis.json", "-ledger.jsonl", "-snapshot.json"):
                for number in ("NaN", "Infinity", "1e999"):
                    with self.subTest(name=name, suffix=suffix, number=number):
                        root = self.copy_store(name)
                        path = root / (stem + suffix)
                        text = path.read_text()
                        first = text.splitlines()[0] if suffix == "-ledger.jsonl" else text
                        key = next(iter(json.loads(first)))
                        # Native decoding retains the later original value.
                        start = text.index("{") + 1
                        path.write_text(text[:start] + json.dumps(key) + ":" + number
                                        + "," + text[start:])
                        final, _ = cls(root)._recover_unlocked()
                        expected = self.states["DecisionOSWa" if name == "wa" else "PlanOS"]
                        self.assertTrue(_same(final, expected))
                        self.assertEqual(self.audit(**{
                            "original_" + name + "_store_root": root,
                        }).status, subject.BLOCKED)

    def test_original_replay_consumes_captured_bytes_without_reopening_input(self):
        root = self.copy_store("plan")
        native_recover = PlanStore._recover_unlocked
        def change_only_while_replaying(store):
            path = store.genesis_path
            original = path.read_bytes()
            try:
                path.write_bytes(b"{not-json}\n")
                return native_recover(store)
            finally:
                path.write_bytes(original)
        with patch.object(PlanStore, "_recover_unlocked", change_only_while_replaying):
            result = self.audit(original_plan_store_root=root)
        self.assertEqual(result.status, subject.SCOPED_COMPATIBLE, result.issues)
        self.assertEqual(result.plan_commit_count, 7)
        self.assertTrue(result.store_bytes_stable_during_audit)

    def test_receipt_binding_and_authority_cannot_be_forged(self):
        for key, value in (("wa_activation_receipt_digest", "forged"),
                           ("future_only", False),
                           ("host_license_granted", True)):
            with self.subTest(key=key):
                bad = deepcopy(self.receipt)
                bad[key] = value
                self.assertEqual(self.audit(
                    replan_activation_receipt=bad).status, subject.BLOCKED)

    def test_incompatible_plural_source_is_blocked(self):
        bad = deepcopy(self.states["DecisionOSPlural"])
        bad["plural_state_digest"] = "forged"
        self.assertEqual(self.audit(plural_state=bad).status, subject.BLOCKED)

    def test_audit_rechecks_bytes_after_original_local_validation(self):
        root = self.copy_store("plan")
        original = subject.audit_native_wa_plan_local_compatibility
        def concurrent_change(*args):
            result = original(*args)
            path = root / "plan-snapshot.json"
            path.write_bytes(path.read_bytes() + b"\n")
            return result
        with patch.object(subject, "audit_native_wa_plan_local_compatibility",
                          side_effect=concurrent_change):
            result = self.audit(original_plan_store_root=root)
        self.assertEqual(result.status, subject.BLOCKED, result.issues)
        self.assertIn("wa_plan_store:original_bytes_changed", result.issues)
        self.assertFalse(result.store_bytes_stable_during_audit)

    def test_audit_preserves_all_original_files_and_input_objects(self):
        before = {str(p.relative_to(self.root)): p.read_bytes()
                  for p in self.root.rglob("*") if p.is_file()}
        inputs = deepcopy((self.native, self.receipt))
        self.assertEqual(self.audit().status, subject.SCOPED_COMPATIBLE)
        after = {str(p.relative_to(self.root)): p.read_bytes()
                 for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)
        self.assertTrue(_same(inputs, (self.native, self.receipt)))

    def test_local_success_grants_no_formal_or_external_authority(self):
        result = self.audit()
        self.assertEqual(result.status, subject.SCOPED_COMPATIBLE, result.issues)
        for field in (
            "formal_global_descent_proved", "lean_python_semantic_refinement_proved",
            "global_atomic_snapshot_proved", "external_replan_issuer_authenticated",
            "plural_original_store_replayed", "actual_act_numeric_witnesses_proved",
            "execution_authority_granted", "host_license_granted",
            "truth_authority_granted", "clinical_authority_granted",
            "legal_authority_granted", "git_authority_granted",
            "memory_overwrite_authority_granted", "original_store_mutated",
        ):
            self.assertIs(getattr(result, field), False, field)


if __name__ == "__main__":
    unittest.main()
