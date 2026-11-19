"""v0.35 read-only original ActOS→ObserveOS persisted source tests.

No mocked OS validators, no synthetic source success, and no other OS
kernel changes. The original native v1.3 fixture creates both real
file-backed stores and full append-only event history.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
import unittest

from runtime.kuuos_act_os_store_v0_1 import ActStore
from runtime.kuuos_observe_os_store_v0_1 import ObserveStore
from runtime.kuuos_qi_world_native_full_cycle_v1_3 import (
    build_native_full_cycle_receipt, validate_native_full_cycle_receipt,
)
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _fingerprint
from runtime.kuuos_lean_python_act_observe_store_compat_v0_35 import (
    audit_native_act_observe_store_compatibility,
    SCOPED_COMPATIBLE, NO_DATA, BLOCKED,
)


class NativeActObserveStoreCompatTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = TemporaryDirectory(prefix="kuuos-v035-act-observe-")
        cls.addClassCleanup(cls.tmp.cleanup)
        cls.root = Path(cls.tmp.name)
        cls.native = build_native_full_cycle_receipt(cls.root)
        assert validate_native_full_cycle_receipt(cls.native) == []
        cls.act = cls.native["native_artifacts"]["ActOS"]
        cls.observe = cls.native["native_artifacts"]["ObserveOS"]
        cls.act_root = cls.root / "act"
        cls.obs_root = cls.root / "downstream" / "observe"

    def audit(self, act=None, observe=None, act_root=None, obs_root=None):
        return audit_native_act_observe_store_compatibility(
            self.act if act is None else act,
            self.observe if observe is None else observe,
            self.act_root if act_root is None else act_root,
            self.obs_root if obs_root is None else obs_root,
        )

    def test_original_stores_replay_without_source_changes(self):
        self.assertEqual(ActStore(self.act_root).recover(), self.act)
        self.assertEqual(ObserveStore(self.obs_root).recover(), self.observe)
        self.assertEqual(validate_native_full_cycle_receipt(self.native), [])

    def test_true_native_act_to_observe_store_compatibility(self):
        report = self.audit()
        self.assertEqual(report.status, SCOPED_COMPATIBLE, report.issues)
        self.assertTrue(report.act_original_store_replayed)
        self.assertTrue(report.observe_original_store_replayed)
        self.assertTrue(report.original_act_to_observe_genesis_edge_checked)
        self.assertTrue(report.original_final_observe_lean_data_checked)
        self.assertGreater(report.act_commit_count, 0)
        self.assertGreater(report.observe_commit_count, 0)
        self.assertEqual(report.original_act_digest, _fingerprint(self.act))
        self.assertEqual(report.original_observe_final_digest, _fingerprint(self.observe))

    def test_missing_act_is_no_data(self):
        self.assertEqual(audit_native_act_observe_store_compatibility(
            None, self.observe, self.act_root, self.obs_root).status, NO_DATA)

    def test_missing_observation_is_no_data(self):
        self.assertEqual(audit_native_act_observe_store_compatibility(
            self.act, None, self.act_root, self.obs_root).status, NO_DATA)

    def test_missing_store_file_is_no_data(self):
        with TemporaryDirectory(prefix="kuuos-v035-missing-") as tmp:
            dst = Path(tmp) / "observe"
            shutil.copytree(self.obs_root, dst)
            (dst / "observe-ledger.jsonl").unlink()
            self.assertEqual(self.audit(obs_root=dst).status, NO_DATA)

    def test_invalid_source_type_is_blocked(self):
        self.assertEqual(audit_native_act_observe_store_compatibility(
            [], self.observe, self.act_root, self.obs_root).status, BLOCKED)

    def test_original_native_concrete_pathlib_roots_are_supported(self):
        # pathlib.Path() on POSIX creates PosixPath, not type(Path).
        self.assertIsInstance(self.act_root, Path)
        self.assertIsInstance(self.obs_root, Path)
        self.assertEqual(self.audit().status, SCOPED_COMPATIBLE)

    def test_original_native_builtin_string_roots_are_supported(self):
        self.assertEqual(
            self.audit(act_root=str(self.act_root),
                       obs_root=str(self.obs_root)).status,
            SCOPED_COMPATIBLE,
        )

    def test_untrusted_custom_store_root_is_blocked(self):
        class CustomPath:
            def __fspath__(self):
                raise AssertionError("no untrusted path conversion allowed")
        self.assertEqual(self.audit(obs_root=CustomPath()).status, BLOCKED)

    def test_act_store_root_and_observe_store_root_must_differ(self):
        self.assertEqual(self.audit(obs_root=self.act_root).status, BLOCKED)

    def test_tampered_act_state_cannot_bind_observation(self):
        bad = deepcopy(self.act)
        bad["act_state_digest"] = "forged"
        self.assertEqual(self.audit(act=bad).status, BLOCKED)

    def test_tampered_observe_state_cannot_bind_effect(self):
        bad = deepcopy(self.observe)
        bad["source_act_state_digest"] = "forged"
        self.assertEqual(self.audit(observe=bad).status, BLOCKED)

    def test_tampered_observation_comparison_is_blocked(self):
        bad = deepcopy(self.observe)
        bad["comparison_receipt"]["verdict"] = "DIVERGENT"
        self.assertEqual(self.audit(observe=bad).status, BLOCKED)

    def test_observe_persisted_snapshot_corruption_blocks(self):
        with TemporaryDirectory(prefix="kuuos-v035-corrupt-") as tmp:
            dst = Path(tmp) / "observe"
            shutil.copytree(self.obs_root, dst)
            p = dst / "observe-snapshot.json"
            obj = json.loads(p.read_text(encoding="utf-8"))
            obj["observe_state_digest"] = "forged"
            p.write_text(json.dumps(obj), encoding="utf-8")
            self.assertEqual(self.audit(obs_root=dst).status, BLOCKED)

    def test_observe_persisted_ledger_corruption_blocks(self):
        with TemporaryDirectory(prefix="kuuos-v035-corrupt-") as tmp:
            dst = Path(tmp) / "observe"
            shutil.copytree(self.obs_root, dst)
            with (dst / "observe-ledger.jsonl").open("a", encoding="utf-8") as f:
                f.write("{}\n")
            self.assertEqual(self.audit(obs_root=dst).status, BLOCKED)

    def test_symlink_original_observe_root_blocks(self):
        with TemporaryDirectory(prefix="kuuos-v035-symlink-") as tmp:
            link = Path(tmp) / "observe-link"
            link.symlink_to(self.obs_root, target_is_directory=True)
            self.assertEqual(self.audit(obs_root=link).status, BLOCKED)

    def test_no_new_host_calls_or_store_writes(self):
        before = {
            str(path.relative_to(self.root)): path.read_bytes()
            for path in self.root.rglob("*") if path.is_file()
        }
        self.assertEqual(self.audit().status, SCOPED_COMPATIBLE)
        after = {
            str(path.relative_to(self.root)): path.read_bytes()
            for path in self.root.rglob("*") if path.is_file()
        }
        self.assertEqual(before, after)

    def test_observation_never_proves_host_counts_truth_or_descent(self):
        result = self.audit()
        self.assertEqual(result.status, SCOPED_COMPATIBLE)
        for field in (
            "act_jobs_claimed_numeric_witness_proved",
            "act_slices_run_numeric_witness_proved",
            "external_receipt_authenticated",
            "observation_is_verification", "observation_grants_truth",
            "whole_program_lean_python_refinement_proved",
            "global_descent_proved", "execution_authority_granted",
            "host_license_granted", "git_authority_granted",
            "original_store_mutated",
        ):
            self.assertIs(getattr(result, field), False, field)


if __name__ == "__main__":
    unittest.main()
