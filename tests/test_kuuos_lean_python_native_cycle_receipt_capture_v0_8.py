"""Genuine native v1.3 in-process original-return capture tests (v0.8).

This is an isolated bounded LOCAL fixture. The two original receipt builders
are not replaced by mocks: the capture shims call the genuine functions and
return their unchanged result. The audit is read-only. Neither authenticates
an external issuer nor certifies Lean/Python refinement.
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

from runtime import kuuos_qi_world_native_full_cycle_v1_3 as native
from runtime.kuuos_plan_os_kernel_v0_1 import build_plan_phase_activation_receipt
from runtime.kuuos_decision_os_wa_kernel_v0_3 import build_replan_wa_activation_receipt
from runtime.kuuos_plan_os_types_v0_1 import plan_activation_receipt_digest
from runtime.kuuos_decision_os_wa_types_v0_3 import wa_activation_receipt_digest
from runtime.kuuos_lean_python_native_cycle_receipt_capture_v0_8 import (
    BLOCKED, NO_DATA, SUCCESS, EDGES, WA_EDGE, PLAN_EDGE,
    CAPTURE_MODE, VERSION, audit_captured_native_receipts,
    build_captured_native_test_fixture, capture_digest,
)
from runtime.kuuos_qi_world_native_full_cycle_v1_3 import (
    validate_native_full_cycle_receipt,
)


class CaptureSourceV08Tests(unittest.TestCase):
    """Static guard is independently exercised by the cumulative Python suite."""

    def test_eight_original_source_blobs_match(self):
        from scripts import check_kuuos_lean_python_native_capture_sources_v0_8 as checker
        self.assertEqual(len(checker.SOURCE_BLOBS), 8)
        self.assertEqual(checker.check_sources(checker.ROOT), ())

    def test_source_byte_drift_is_preserved_as_blocker(self):
        from scripts import check_kuuos_lean_python_native_capture_sources_v0_8 as checker
        with TemporaryDirectory(prefix="kuuos-v08-static-") as folder:
            root = Path(folder)
            original = "runtime/source.py"
            file = root / original
            file.parent.mkdir(parents=True)
            file.write_bytes(b"changed\n")
            with patch.object(checker, "SOURCE_BLOBS", {original: "0" * 40}), \
                 patch.object(checker, "NEW_PATHS", ()):
                issues = checker.check_sources(root)
        self.assertIn("source_drift:" + original, issues)

    def test_comment_is_not_actual_native_test_registration(self):
        from scripts import check_kuuos_lean_python_native_capture_sources_v0_8 as checker
        with TemporaryDirectory(prefix="kuuos-v08-registration-") as folder:
            root = Path(folder)
            original = root / checker.RUNNER_TEST
            original.parent.mkdir(parents=True)
            original.write_text(
                "# import from tests.test_kuuos_lean_python_native_cycle_receipt_capture_v0_8\n"
                "import unittest\n",
                encoding="utf-8",
            )
            with patch.object(checker, "SOURCE_BLOBS", {}), \
                 patch.object(checker, "NEW_PATHS", ()):
                issues = checker.check_sources(root)
        self.assertIn("cumulative_v08_native_tests_not_registered_exactly_once", issues)


class NativeCaptureV08Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = TemporaryDirectory(prefix="kuuos-lean-python-captured-v08-")
        cls.addClassCleanup(cls.temp.cleanup)
        cls.root = Path(cls.temp.name)
        cls.orig_wa = native.build_replan_wa_activation_receipt
        cls.orig_plan = native.build_plan_phase_activation_receipt
        cls.native_receipt, cls.capture = build_captured_native_test_fixture(cls.root)
        if validate_native_full_cycle_receipt(cls.native_receipt):
            raise AssertionError("original_native_source_validator_failed")

    def audit(self, capture=None, receipt=None, *, root=None):
        return audit_captured_native_receipts(
            self.root if root is None else root,
            self.native_receipt if receipt is None else receipt,
            self.capture if capture is None else capture,
        )

    @staticmethod
    def reseal(capture):
        capture["capture_sha256"] = capture_digest(capture)

    def test_same_origin_local_original_returns_pass_full_packet_comparison(self):
        result = self.audit()
        self.assertEqual(result.status, SUCCESS, (result.violations, result.missing))
        self.assertTrue(result.local_fixture_integrity_checked)
        self.assertIsNotNone(result.native_replay)
        self.assertEqual(result.native_replay.status, "NATIVE_FIXTURE_LINKS_REPLAYED")
        self.assertGreater(result.native_replay.ledger_commit_count, 0)
        self.assertEqual(
            result.wa_receipt_digest,
            self.native_receipt["native_artifacts"]["PlanOS"]["replan_activation_receipt_digest"],
        )
        self.assertEqual(
            result.plan_receipt_digest,
            self.native_receipt["native_artifacts"]["ActOS"]["plan_activation_receipt_digest"],
        )
        self.assertEqual(len(result.native_replay.segments), 3)

    def test_exact_raw_native_original_return_properties(self):
        self.assertEqual(self.capture["return_sequence"], list(EDGES))
        self.assertEqual(self.capture["version"], VERSION)
        self.assertEqual(self.capture["capture_mode"], CAPTURE_MODE)
        self.assertEqual(self.capture["native_cycle_digest"],
                         self.native_receipt["native_full_cycle_receipt_digest"])
        self.assertEqual(self.capture["capture_sha256"], capture_digest(self.capture))
        self.assertEqual(self.capture["wa_activation_receipt"]["wa_activation_receipt_digest"],
                         wa_activation_receipt_digest(self.capture["wa_activation_receipt"]))
        self.assertEqual(self.capture["plan_activation_receipt"]["plan_activation_receipt_digest"],
                         plan_activation_receipt_digest(self.capture["plan_activation_receipt"]))
        self.assertEqual(self.capture["wa_activation_receipt"]["mission_cycle_phase"], "replan")
        self.assertEqual(self.capture["plan_activation_receipt"]["mission_cycle_phase"], "plan")

    def test_observation_shims_are_removed_after_fixture_build(self):
        self.assertIs(native.build_replan_wa_activation_receipt, self.orig_wa)
        self.assertIs(native.build_plan_phase_activation_receipt, self.orig_plan)
        self.assertIs(native.build_replan_wa_activation_receipt,
                      build_replan_wa_activation_receipt)
        self.assertIs(native.build_plan_phase_activation_receipt,
                      build_plan_phase_activation_receipt)

    def test_read_only_auditor_preserves_arguments_and_persisted_act_ledger(self):
        original_receipt, original_capture = deepcopy((self.native_receipt, self.capture))
        root = self.root / "act"
        filenames = ("act-genesis.json", "act-ledger.jsonl", "act-snapshot.json")
        snapshot = {filename: (root / filename).read_bytes() for filename in filenames}
        result = self.audit()
        self.assertEqual(result.status, SUCCESS, result)
        self.assertEqual(self.native_receipt, original_receipt)
        self.assertEqual(self.capture, original_capture)
        self.assertEqual(snapshot, {filename: (root / filename).read_bytes()
                                    for filename in filenames})

    def test_authentication_and_formal_authorities_are_not_inferred(self):
        result = self.audit()
        self.assertEqual(result.status, SUCCESS, result)
        self.assertFalse(result.original_constructor_returns_observed)
        self.assertFalse(result.external_issuer_authenticated)
        self.assertFalse(result.historical_receipt_issuance_proved)
        self.assertFalse(result.formal_descent_certified)
        self.assertFalse(result.lean_python_refinement_proved)
        self.assertFalse(result.execution_authority_granted)
        self.assertFalse(result.truth_authority_granted)
        self.assertFalse(result.git_merge_authority_granted)

    def test_missing_capture_packet_is_no_data(self):
        result = audit_captured_native_receipts(self.root, self.native_receipt, None)
        self.assertEqual(result.status, NO_DATA)
        self.assertIn("capture_packet:missing", result.missing)

    def test_untrusted_capture_object_is_blocked(self):
        for bad in ([], object(), "capture", True, 3):
            with self.subTest(kind=type(bad).__name__):
                result = audit_captured_native_receipts(self.root, self.native_receipt, bad)
                self.assertEqual(result.status, BLOCKED)

    def test_wrong_capture_checksum_fails_even_if_raw_receipts_match(self):
        capture = deepcopy(self.capture)
        capture["capture_sha256"] = "f" * 64
        result = self.audit(capture=capture)
        self.assertEqual(result.status, BLOCKED)
        self.assertIn("capture_packet:checksum_mismatch", result.violations)

    def test_inverted_return_order_cannot_be_promoted_after_reseal(self):
        capture = deepcopy(self.capture)
        capture["return_sequence"].reverse()
        self.reseal(capture)
        result = self.audit(capture=capture)
        self.assertEqual(result.status, BLOCKED)
        self.assertIn("capture_packet:return_order_or_count_mismatch", result.violations)

    def test_duplicate_or_missing_return_cannot_be_promoted(self):
        for sequence in ([WA_EDGE, WA_EDGE], [WA_EDGE], [], [PLAN_EDGE]):
            with self.subTest(sequence=sequence):
                capture = deepcopy(self.capture)
                capture["return_sequence"] = sequence
                self.reseal(capture)
                result = self.audit(capture=capture)
                self.assertEqual(result.status, BLOCKED)

    def test_wrong_source_native_cycle_digest_cannot_be_resealed_away(self):
        capture = deepcopy(self.capture)
        capture["native_cycle_digest"] = "other-original-cycle"
        self.reseal(capture)
        result = self.audit(capture=capture)
        self.assertEqual(result.status, BLOCKED)
        self.assertIn("capture_packet:native_cycle_binding_mismatch", result.violations)

    def test_forged_full_wa_receipt_even_with_original_wa_hash_blocks(self):
        capture = deepcopy(self.capture)
        capture["wa_activation_receipt"]["next_plan_basis_digest"] = "wrong-next-plan"
        capture["wa_activation_receipt"]["wa_activation_receipt_digest"] = (
            wa_activation_receipt_digest(capture["wa_activation_receipt"])
        )
        self.reseal(capture)
        result = self.audit(capture=capture)
        self.assertEqual(result.status, BLOCKED)
        self.assertIn("captured_wa_receipt:whole_packet_mismatch", result.violations)

    def test_forged_full_plan_receipt_even_with_original_plan_hash_blocks(self):
        capture = deepcopy(self.capture)
        capture["plan_activation_receipt"]["plan_phase_receipt_digest"] = "wrong-source"
        capture["plan_activation_receipt"]["plan_activation_receipt_digest"] = (
            plan_activation_receipt_digest(capture["plan_activation_receipt"])
        )
        self.reseal(capture)
        result = self.audit(capture=capture)
        self.assertEqual(result.status, BLOCKED)
        self.assertIn("captured_plan_receipt:whole_packet_mismatch", result.violations)

    def test_source_and_synthetic_receipts_remain_distinct(self):
        capture = deepcopy(self.capture)
        capture["wa_activation_receipt"] = deepcopy(capture["plan_activation_receipt"])
        self.reseal(capture)
        result = self.audit(capture=capture)
        self.assertEqual(result.status, BLOCKED)

    def test_missing_full_receipt_field_is_fail_closed(self):
        capture = deepcopy(self.capture)
        capture["wa_activation_receipt"] = None
        self.reseal(capture)
        result = self.audit(capture=capture)
        self.assertEqual(result.status, BLOCKED)
        self.assertIn("capture_packet:receipt_objects_required", result.violations)

    def test_capture_unknown_or_missing_fields_are_rejected(self):
        for mode in ("unknown", "missing"):
            with self.subTest(mode=mode):
                capture = deepcopy(self.capture)
                if mode == "unknown":
                    capture["authority_override"] = True
                else:
                    del capture["return_sequence"]
                self.reseal(capture)
                result = self.audit(capture=capture)
                self.assertEqual(result.status, BLOCKED)
                self.assertIn("capture_packet:field_inventory_mismatch", result.violations)

    def test_bad_native_packet_prevents_local_capture_promotion(self):
        native_receipt = deepcopy(self.native_receipt)
        native_receipt["native_full_cycle_receipt_digest"] = "0" * 64
        result = self.audit(receipt=native_receipt)
        self.assertEqual(result.status, BLOCKED)
        self.assertIn("native_replay:native_receipt:native_full_cycle_digest_invalid",
                      result.violations)

    def test_missing_native_store_is_no_data_and_no_capture_claim(self):
        with TemporaryDirectory(prefix="kuuos-v08-store-missing-") as folder:
            result = self.audit(root=Path(folder))
        self.assertEqual(result.status, NO_DATA)
        self.assertFalse(result.local_fixture_integrity_checked)
        self.assertTrue(any("native_replay:" in entry for entry in result.missing))

    def test_malformed_capture_json_fails_without_custom_hook(self):
        class EvilDict(dict):
            def items(self):
                raise AssertionError("custom JSON hook executed")
        for bad in (float("nan"), object(), EvilDict()):
            capture = deepcopy(self.capture)
            capture["extra"] = bad
            result = self.audit(capture=capture)
            self.assertEqual(result.status, BLOCKED)

    def test_issued_packet_cannot_appear_with_changed_version_or_mode(self):
        for name, bad in (("version", "unknown"), ("capture_mode", "external-certified")):
            capture = deepcopy(self.capture)
            capture[name] = bad
            self.reseal(capture)
            result = self.audit(capture=capture)
            self.assertEqual(result.status, BLOCKED)
            self.assertIn("capture_packet:version_or_mode_mismatch", result.violations)

    def test_builder_refuses_existing_fixture_dir_instead_of_overwriting(self):
        with self.assertRaises(ValueError):
            build_captured_native_test_fixture(self.root)

    def test_builder_restores_shims_when_native_generator_raises(self):
        with TemporaryDirectory(prefix="kuuos-v08-fail-") as folder:
            with patch.object(native, "build_native_full_cycle_receipt",
                              side_effect=RuntimeError("simulated build failure")):
                with self.assertRaises(RuntimeError):
                    build_captured_native_test_fixture(Path(folder))
            self.assertIs(native.build_replan_wa_activation_receipt, self.orig_wa)
            self.assertIs(native.build_plan_phase_activation_receipt, self.orig_plan)

    def test_missing_second_return_is_rejected_as_incomplete(self):
        with TemporaryDirectory(prefix="kuuos-v08-missing-return-") as folder:
            with patch.object(native, "build_plan_phase_activation_receipt",
                              side_effect=RuntimeError("no plan issuance")):
                with self.assertRaises((RuntimeError, ValueError)):
                    build_captured_native_test_fixture(Path(folder))
            self.assertIs(native.build_replan_wa_activation_receipt, self.orig_wa)
            self.assertIs(native.build_plan_phase_activation_receipt, self.orig_plan)

    def test_bad_ledger_is_still_blocked_by_original_replay(self):
        with TemporaryDirectory(prefix="kuuos-v08-altered-ledger-") as folder:
            root = Path(folder)
            shutil.copytree(self.root / "act", root / "act")
            journal = root / "act" / "act-ledger.jsonl"
            lines = journal.read_text(encoding="utf-8").splitlines()
            item = json.loads(lines[0])
            item["result_act_state_digest"] = "f" * 64
            lines[0] = json.dumps(item, sort_keys=True)
            journal.write_text("\n".join(lines) + "\n", encoding="utf-8")
            result = self.audit(root=root)
        self.assertEqual(result.status, BLOCKED)
        self.assertTrue(any(x.startswith("native_replay:act_store:")
                            for x in result.violations))

    def test_capture_result_determinism(self):
        first = self.audit()
        second = self.audit()
        self.assertEqual(first, second)
        self.assertEqual(first.status, SUCCESS)
        self.assertEqual(first.capture_sha256, self.capture["capture_sha256"])
        self.assertEqual(len(first.capture_sha256), 64)


if __name__ == "__main__":
    unittest.main()
