"""v0.36 regression: original Observe/Verify stored typed handoff.

Exercises the real v1.3 native full cycle and original VerifyOS
adjudication fixtures. No mocked OS kernel, direct host invocation,
or assertion of global Lean/Python refinement.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
import unittest

from runtime.kuuos_observe_os_store_v0_1 import ObserveStore
from runtime.kuuos_verify_os_store_v0_1 import VerifyStore
from runtime.kuuos_qi_world_native_full_cycle_v1_3 import (
    build_native_full_cycle_receipt, validate_native_full_cycle_receipt,
)
from runtime.kuuos_verify_os_fixture_v0_1 import (
    prepared_corroborated_state, source_observe_state,
)
from runtime.v01_verify_os_evidence_bound_verification import _finish
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _fingerprint
from runtime.kuuos_lean_python_observe_verify_store_compat_v0_36 import (
    SCOPED_COMPATIBLE, NO_DATA, BLOCKED,
    audit_native_observe_verify_store_compatibility,
)


class NativeObserveVerifyStoreCompatTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = TemporaryDirectory(prefix="kuuos-v036-observe-verify-")
        cls.addClassCleanup(cls.tmp.cleanup)
        cls.root = Path(cls.tmp.name)
        cls.native = build_native_full_cycle_receipt(cls.root)
        assert validate_native_full_cycle_receipt(cls.native) == []
        cls.observe = cls.native["native_artifacts"]["ObserveOS"]
        cls.verify = cls.native["native_artifacts"]["VerifyOS"]
        cls.obs_root = cls.root / "downstream" / "observe"
        cls.verify_root = cls.root / "downstream" / "verify"

    def audit(self, observe=None, verify=None, obs_root=None, verify_root=None):
        return audit_native_observe_verify_store_compatibility(
            self.observe if observe is None else observe,
            self.verify if verify is None else verify,
            self.obs_root if obs_root is None else obs_root,
            self.verify_root if verify_root is None else verify_root,
        )

    def test_real_saved_observe_verify_replay(self):
        self.assertEqual(ObserveStore(self.obs_root).recover(), self.observe)
        self.assertEqual(VerifyStore(self.verify_root).recover(), self.verify)
        self.assertEqual(validate_native_full_cycle_receipt(self.native), [])

    def test_original_observe_verify_genesis_and_final_compatibility(self):
        audit = self.audit()
        self.assertEqual(audit.status, SCOPED_COMPATIBLE, audit.issues)
        self.assertTrue(audit.observe_original_store_replayed)
        self.assertTrue(audit.verify_original_store_replayed)
        self.assertTrue(audit.original_observe_to_verify_genesis_edge_checked)
        self.assertTrue(audit.original_final_verify_lean_data_checked)
        self.assertEqual(audit.adjudication_verdict, "PASSED")
        self.assertEqual(audit.original_observe_digest, _fingerprint(self.observe))
        self.assertEqual(audit.original_verify_final_digest, _fingerprint(self.verify))
        self.assertGreater(audit.observe_commit_count, 0)
        self.assertGreater(audit.verify_commit_count, 0)
        self.assertTrue(any("comparison_receipt" in x
                            for x in audit.checked_source_paths))
        self.assertTrue(any("adjudication_receipt" in x
                            for x in audit.checked_source_paths))

    def test_original_string_path_roots_accepted(self):
        self.assertEqual(
            self.audit(obs_root=str(self.obs_root),
                       verify_root=str(self.verify_root)).status,
            SCOPED_COMPATIBLE,
        )

    def test_real_concrete_pathlib_roots_accepted(self):
        self.assertIsInstance(self.obs_root, Path)
        self.assertIsInstance(self.verify_root, Path)
        self.assertEqual(self.audit().status, SCOPED_COMPATIBLE)

    def test_custom_path_like_root_blocked_before_conversion(self):
        class HostileRoot:
            def __fspath__(self):
                raise AssertionError("custom path must not be converted")
        self.assertEqual(self.audit(verify_root=HostileRoot()).status, BLOCKED)

    def test_observe_verify_store_roots_must_be_distinct(self):
        self.assertEqual(self.audit(verify_root=self.obs_root).status, BLOCKED)

    def test_missing_observe_source_is_no_data(self):
        self.assertEqual(audit_native_observe_verify_store_compatibility(
            None, self.verify, self.obs_root, self.verify_root).status, NO_DATA)

    def test_missing_verify_source_is_no_data(self):
        self.assertEqual(audit_native_observe_verify_store_compatibility(
            self.observe, None, self.obs_root, self.verify_root).status, NO_DATA)

    def test_missing_original_store_is_no_data(self):
        with TemporaryDirectory(prefix="kuuos-v036-missing-") as temp:
            dst = Path(temp) / "verify"
            shutil.copytree(self.verify_root, dst)
            (dst / "verify-ledger.jsonl").unlink()
            self.assertEqual(self.audit(verify_root=dst).status, NO_DATA)

    def test_invalid_supplied_json_type_is_blocked(self):
        self.assertEqual(audit_native_observe_verify_store_compatibility(
            self.observe, [], self.obs_root, self.verify_root).status, BLOCKED)

    def test_modified_observe_source_is_blocked(self):
        bad = deepcopy(self.observe)
        bad["comparison_receipt_digest"] = "forged"
        self.assertEqual(self.audit(observe=bad).status, BLOCKED)

    def test_modified_verify_source_is_blocked(self):
        bad = deepcopy(self.verify)
        bad["source_observe_state_digest"] = "forged"
        self.assertEqual(self.audit(verify=bad).status, BLOCKED)

    def test_modified_final_adjudication_receipt_blocks(self):
        bad = deepcopy(self.verify)
        bad["adjudication_receipt"]["verdict"] = "FAILED"
        self.assertEqual(self.audit(verify=bad).status, BLOCKED)

    def test_corrupt_verify_snapshot_blocks(self):
        with TemporaryDirectory(prefix="kuuos-v036-corrupt-") as temp:
            dst = Path(temp) / "verify"
            shutil.copytree(self.verify_root, dst)
            path = dst / "verify-snapshot.json"
            bad = json.loads(path.read_text(encoding="utf-8"))
            bad["verify_state_digest"] = "forged"
            path.write_text(json.dumps(bad), encoding="utf-8")
            self.assertEqual(self.audit(verify_root=dst).status, BLOCKED)

    def test_corrupt_verify_ledger_blocks(self):
        with TemporaryDirectory(prefix="kuuos-v036-corrupt-") as temp:
            dst = Path(temp) / "verify"
            shutil.copytree(self.verify_root, dst)
            with (dst / "verify-ledger.jsonl").open("a", encoding="utf-8") as f:
                f.write("{}\n")
            self.assertEqual(self.audit(verify_root=dst).status, BLOCKED)

    def test_corrupt_original_observe_snapshot_blocks(self):
        with TemporaryDirectory(prefix="kuuos-v036-corrupt-") as temp:
            dst = Path(temp) / "observe"
            shutil.copytree(self.obs_root, dst)
            path = dst / "observe-snapshot.json"
            bad = json.loads(path.read_text(encoding="utf-8"))
            bad["observe_state_digest"] = "forged"
            path.write_text(json.dumps(bad), encoding="utf-8")
            self.assertEqual(self.audit(obs_root=dst).status, BLOCKED)

    def test_verify_root_symlink_blocks(self):
        with TemporaryDirectory(prefix="kuuos-v036-link-") as temp:
            link = Path(temp) / "verify-link"
            link.symlink_to(self.verify_root, target_is_directory=True)
            self.assertEqual(self.audit(verify_root=link).status, BLOCKED)

    def test_verify_ledger_symlink_blocks(self):
        with TemporaryDirectory(prefix="kuuos-v036-link-") as temp:
            dst = Path(temp) / "verify"
            shutil.copytree(self.verify_root, dst)
            ledger = dst / "verify-ledger.jsonl"
            ledger.unlink()
            ledger.symlink_to(self.verify_root / "verify-ledger.jsonl")
            self.assertEqual(self.audit(verify_root=dst).status, BLOCKED)

    def test_real_failed_and_indeterminate_verdict_debt_is_preserved(self):
        cases = (
            ("DIVERGENT", "FAILED", False, True, "VERIFICATION_FAILED"),
            ("CONFLICTED", "INDETERMINATE", False, False,
             "VERIFICATION_INDETERMINATE"),
        )
        with TemporaryDirectory(prefix="kuuos-v036-verdicts-") as temp:
            for observation_verdict, verification_verdict, satisfied, admissible, route in cases:
                with self.subTest(verdict=verification_verdict):
                    root = Path(temp) / observation_verdict.lower()
                    observe = source_observe_state(root / "source", verdict=observation_verdict)
                    obs_root = root / "source" / ("observe-" + observation_verdict.lower())
                    store, prepared = prepared_corroborated_state(
                        root=root / "verify",
                        verify_id="v036-" + verification_verdict.lower(),
                        observe_state=observe,
                        admissible=admissible,
                    )
                    final, _ = _finish(
                        store=store, state=prepared,
                        verdict=verification_verdict,
                        criterion_satisfied=satisfied, tick=42,
                    )
                    audit = audit_native_observe_verify_store_compatibility(
                        observe, final, obs_root, root / "verify",
                    )
                    self.assertEqual(audit.status, SCOPED_COMPATIBLE, audit.issues)
                    self.assertEqual(audit.adjudication_verdict, verification_verdict)
                    self.assertEqual(final["route"], route)
                    self.assertTrue(final["learning_required"])
                    if verification_verdict == "FAILED":
                        self.assertTrue(final["verification_debt_discharged"])
                        self.assertTrue(final["corrective_action_required"])
                    else:
                        self.assertFalse(final["verification_debt_discharged"])
                        self.assertTrue(final["verification_required"])
                        self.assertTrue(final["reobservation_required"])

    def test_no_host_calls_or_original_store_writes(self):
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

    def test_scoped_success_never_grants_truth_or_any_authority(self):
        result = self.audit()
        self.assertEqual(result.status, SCOPED_COMPATIBLE)
        for name in (
            "external_receipt_authenticated",
            "verification_is_truth",
            "causal_attribution_authority_granted",
            "whole_program_lean_python_refinement_proved",
            "global_descent_proved",
            "clinical_authority_granted",
            "execution_authority_granted",
            "host_license_granted",
            "git_authority_granted",
            "original_store_mutated",
        ):
            self.assertIs(getattr(result, name), False, name)


if __name__ == "__main__":
    unittest.main()
