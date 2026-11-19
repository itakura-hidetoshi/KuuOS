"""v0.37 original native VerifyOS→LearnOS persisted history tests.

The native v1.3 cycle and original v0.1 verification/learning fixtures
are used, never fake a proof witness, an issuer signature or host effect.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
import unittest

from runtime.kuuos_verify_os_store_v0_1 import VerifyStore
from runtime.kuuos_learn_os_store_v0_1 import LearnStore
from runtime.kuuos_learn_os_fixture_v0_1 import (
    prepared_gated_state, source_verify_state,
)
from runtime.v01_learn_os_future_only_evidence_learning import _finish as finish_learn
from runtime.kuuos_qi_world_native_full_cycle_v1_3 import (
    build_native_full_cycle_receipt, validate_native_full_cycle_receipt,
)
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _fingerprint
from runtime.kuuos_lean_python_verify_learn_store_compat_v0_37 import (
    SCOPED_COMPATIBLE, NO_DATA, BLOCKED,
    audit_native_verify_learn_store_compatibility,
)


class NativeVerifyLearnStoreCompatTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = TemporaryDirectory(prefix="kuuos-v037-verify-learn-")
        cls.addClassCleanup(cls.tmp.cleanup)
        cls.root = Path(cls.tmp.name)
        cls.native = build_native_full_cycle_receipt(cls.root)
        assert validate_native_full_cycle_receipt(cls.native) == []
        cls.verify = cls.native["native_artifacts"]["VerifyOS"]
        cls.learn = cls.native["native_artifacts"]["LearnOS"]
        cls.verify_root = cls.root / "downstream" / "verify"
        cls.learn_root = cls.root / "downstream" / "learn"

    def audit(self, verify=None, learn=None, verify_root=None, learn_root=None):
        return audit_native_verify_learn_store_compatibility(
            self.verify if verify is None else verify,
            self.learn if learn is None else learn,
            self.verify_root if verify_root is None else verify_root,
            self.learn_root if learn_root is None else learn_root,
        )

    def test_real_saved_original_verify_learn_replay(self):
        self.assertEqual(VerifyStore(self.verify_root).recover(), self.verify)
        self.assertEqual(LearnStore(self.learn_root).recover(), self.learn)
        self.assertEqual(validate_native_full_cycle_receipt(self.native), [])

    def test_true_native_verify_to_learn_genesis_and_final(self):
        result = self.audit()
        self.assertEqual(result.status, SCOPED_COMPATIBLE, result.issues)
        self.assertTrue(result.verify_original_store_replayed)
        self.assertTrue(result.learn_original_store_replayed)
        self.assertTrue(result.original_verify_to_learn_genesis_edge_checked)
        self.assertTrue(result.original_final_learn_lean_data_checked)
        self.assertEqual(result.verification_verdict, "PASSED")
        self.assertEqual(result.learning_kind, "reinforcement")
        self.assertEqual(result.learning_route, "LEARNING_REINFORCEMENT_CANDIDATE")
        self.assertEqual(result.original_verify_digest, _fingerprint(self.verify))
        self.assertEqual(result.original_learn_final_digest, _fingerprint(self.learn))
        self.assertGreater(result.verify_commit_count, 0)
        self.assertGreater(result.learn_commit_count, 0)

    def test_original_counters_and_unresolved_source_are_preserved(self):
        result = self.audit()
        self.assertEqual(result.status, SCOPED_COMPATIBLE, result.issues)
        self.assertIn("LearnOS.source_counterevidence_digests",
                      result.checked_source_paths)
        self.assertIn("LearnOS.source_unresolved_conflict",
                      result.checked_source_paths)
        self.assertEqual(
            self.learn["source_counterevidence_digests"],
            self.verify["challenge_packet"]["counterevidence_digests"],
        )
        self.assertEqual(
            self.learn["source_unresolved_conflict"],
            self.verify["corroboration_report"]["unresolved_conflict"],
        )

    def test_real_pathlib_concrete_roots(self):
        self.assertIsInstance(self.verify_root, Path)
        self.assertIsInstance(self.learn_root, Path)
        self.assertEqual(self.audit().status, SCOPED_COMPATIBLE)

    def test_string_roots(self):
        self.assertEqual(
            self.audit(
                verify_root=str(self.verify_root),
                learn_root=str(self.learn_root),
            ).status,
            SCOPED_COMPATIBLE,
        )

    def test_untrusted_custom_path_never_converted(self):
        class HostilePath:
            def __fspath__(self):
                raise AssertionError("untrusted path conversion")
        self.assertEqual(self.audit(learn_root=HostilePath()).status, BLOCKED)

    def test_store_roots_must_be_distinct(self):
        self.assertEqual(self.audit(learn_root=self.verify_root).status, BLOCKED)

    def test_missing_verify_state_is_no_data(self):
        self.assertEqual(
            audit_native_verify_learn_store_compatibility(
                None, self.learn, self.verify_root, self.learn_root,
            ).status, NO_DATA,
        )

    def test_missing_learn_state_is_no_data(self):
        self.assertEqual(
            audit_native_verify_learn_store_compatibility(
                self.verify, None, self.verify_root, self.learn_root,
            ).status, NO_DATA,
        )

    def test_missing_real_learn_ledger_is_no_data(self):
        with TemporaryDirectory(prefix="kuuos-v037-missing-") as temp:
            root = Path(temp) / "learn"
            shutil.copytree(self.learn_root, root)
            (root / "learn-ledger.jsonl").unlink()
            self.assertEqual(self.audit(learn_root=root).status, NO_DATA)

    def test_untrusted_json_type_is_blocked(self):
        self.assertEqual(
            audit_native_verify_learn_store_compatibility(
                self.verify, [], self.verify_root, self.learn_root,
            ).status, BLOCKED,
        )

    def test_tampered_verify_source_is_blocked(self):
        altered = deepcopy(self.verify)
        altered["verification_evidence_digest"] = "forged"
        self.assertEqual(self.audit(verify=altered).status, BLOCKED)

    def test_tampered_learn_source_is_blocked(self):
        altered = deepcopy(self.learn)
        altered["source_verify_state_digest"] = "forged"
        self.assertEqual(self.audit(learn=altered).status, BLOCKED)

    def test_tampered_learning_delta_is_blocked(self):
        altered = deepcopy(self.learn)
        altered["learning_delta"]["active_now"] = True
        self.assertEqual(self.audit(learn=altered).status, BLOCKED)

    def test_tampered_counterevidence_history_is_blocked(self):
        altered = deepcopy(self.learn)
        altered["source_counterevidence_digests"] = ["forged"]
        self.assertEqual(self.audit(learn=altered).status, BLOCKED)

    def test_corrupt_learn_snapshot_is_blocked(self):
        with TemporaryDirectory(prefix="kuuos-v037-corrupt-") as temp:
            root = Path(temp) / "learn"
            shutil.copytree(self.learn_root, root)
            target = root / "learn-snapshot.json"
            bad = json.loads(target.read_text(encoding="utf-8"))
            bad["learn_state_digest"] = "forged"
            target.write_text(json.dumps(bad), encoding="utf-8")
            self.assertEqual(self.audit(learn_root=root).status, BLOCKED)

    def test_corrupt_learn_ledger_is_blocked(self):
        with TemporaryDirectory(prefix="kuuos-v037-corrupt-") as temp:
            root = Path(temp) / "learn"
            shutil.copytree(self.learn_root, root)
            with (root / "learn-ledger.jsonl").open("a", encoding="utf-8") as handle:
                handle.write("{}\n")
            self.assertEqual(self.audit(learn_root=root).status, BLOCKED)

    def test_corrupt_verify_snapshot_is_blocked(self):
        with TemporaryDirectory(prefix="kuuos-v037-corrupt-") as temp:
            root = Path(temp) / "verify"
            shutil.copytree(self.verify_root, root)
            target = root / "verify-snapshot.json"
            bad = json.loads(target.read_text(encoding="utf-8"))
            bad["verify_state_digest"] = "forged"
            target.write_text(json.dumps(bad), encoding="utf-8")
            self.assertEqual(self.audit(verify_root=root).status, BLOCKED)

    def test_symlink_original_learn_root_is_blocked(self):
        with TemporaryDirectory(prefix="kuuos-v037-link-") as temp:
            link = Path(temp) / "learn"
            link.symlink_to(self.learn_root, target_is_directory=True)
            self.assertEqual(self.audit(learn_root=link).status, BLOCKED)

    def test_symlink_original_learn_ledger_is_blocked(self):
        with TemporaryDirectory(prefix="kuuos-v037-link-") as temp:
            root = Path(temp) / "learn"
            shutil.copytree(self.learn_root, root)
            ledger = root / "learn-ledger.jsonl"
            ledger.unlink()
            ledger.symlink_to(self.learn_root / "learn-ledger.jsonl")
            self.assertEqual(self.audit(learn_root=root).status, BLOCKED)

    def test_repair_reobservation_and_hold_remain_inactive_candidates(self):
        cases = (
            ("FAILED", "repair", "plan_assumption", True,
             "LEARNING_REPAIR_CANDIDATE"),
            ("INDETERMINATE", "reobservation", "observation_policy", True,
             "LEARNING_REOBSERVATION_CANDIDATE"),
            ("PASSED", "reinforcement", "belief_candidate", False, "LEARNING_HOLD"),
        )
        with TemporaryDirectory(prefix="kuuos-v037-routes-") as temp:
            for verdict, kind, scope, admissible, route in cases:
                with self.subTest(verdict=verdict, route=route):
                    root = Path(temp) / (verdict + "-" + route)
                    verify = source_verify_state(root / "source", verdict=verdict)
                    store, prepared = prepared_gated_state(
                        root=root / "learn",
                        learn_id="v037-" + kind + "-" + verdict.lower(),
                        verify_state=verify,
                        learning_kind=kind,
                        target_scope=scope,
                        admissible=admissible,
                    )
                    learn, _ = finish_learn(store=store, state=prepared, tick=78)
                    audit = audit_native_verify_learn_store_compatibility(
                        verify, learn, root / "source" / "verify", root / "learn",
                    )
                    self.assertEqual(audit.status, SCOPED_COMPATIBLE, audit.issues)
                    self.assertEqual(audit.verification_verdict, verdict)
                    self.assertEqual(audit.learning_route, route)
                    self.assertTrue(learn["learning_recorded"])
                    self.assertTrue(learn["learning_debt_discharged"])
                    self.assertTrue(learn["replan_required"])
                    self.assertFalse(learn["active_now"])
                    if verdict == "FAILED":
                        self.assertTrue(learn["corrective_action_required"])
                    if verdict == "INDETERMINATE":
                        self.assertTrue(learn["reobservation_required"])

    def test_no_original_store_writes_or_host_calls(self):
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

    def test_never_promotes_verification_or_learning_to_authority(self):
        result = self.audit()
        self.assertEqual(result.status, SCOPED_COMPATIBLE)
        for name in (
            "external_receipt_authenticated", "learning_is_truth",
            "learning_grants_causality", "memory_overwrite_authority_granted",
            "learning_activated_now", "whole_program_lean_python_refinement_proved",
            "global_descent_proved", "clinical_authority_granted",
            "execution_authority_granted", "host_license_granted",
            "git_authority_granted", "original_store_mutated",
        ):
            self.assertIs(getattr(result, name), False, name)


if __name__ == "__main__":
    unittest.main()
