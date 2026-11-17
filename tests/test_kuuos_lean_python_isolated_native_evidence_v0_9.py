"""v0.9 tests: a real native fixture built in a separate Python process.

No externally authenticated signature, host authority, formal Lean refinement,
or proof of the historical origin of locally forgeable JSON is inferred.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from contextlib import contextmanager
from copy import deepcopy
import json
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from runtime import kuuos_qi_world_native_full_cycle_v1_3 as native
from runtime.kuuos_lean_python_isolated_native_receipt_evidence_v0_9 import (
    BLOCKED, EVIDENCE_FILE, GOOD, MAX_EVIDENCE_BYTES, MODE, NO_DATA,
    ROOT, SOURCE_MAIN, VERSION,
    audit_isolated_evidence, build_isolated_fixture_evidence,
    evidence_digest, root_binding, _write_once,
)
from runtime.kuuos_lean_python_native_cycle_receipt_capture_v0_8 import (
    capture_digest,
)
from runtime.kuuos_decision_os_wa_types_v0_3 import wa_activation_receipt_digest


class IsolatedNativeEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = TemporaryDirectory(prefix="kuuos-lean-python-v09-isolated-")
        cls.addClassCleanup(cls.temp.cleanup)
        cls.root = Path(cls.temp.name)
        cls.wa_original = staticmethod(native.build_replan_wa_activation_receipt)
        cls.plan_original = staticmethod(native.build_plan_phase_activation_receipt)
        cls.created = build_isolated_fixture_evidence(cls.root)
        cls.record_path = cls.root / EVIDENCE_FILE
        cls.record = json.loads(cls.record_path.read_text(encoding="utf-8"))

    @contextmanager
    def clone(self):
        with TemporaryDirectory(prefix="kuuos-v09-copy-") as folder:
            root = Path(folder) / "copied-fixture"
            shutil.copytree(self.root, root)
            path = root / EVIDENCE_FILE
            record = json.loads(path.read_text(encoding="utf-8"))
            # Explicitly rebind a copied local fixture. A self-consistent
            # local checksum is not an external signature or origin proof.
            record["root_binding_sha256"] = root_binding(root)
            record["record_sha256"] = evidence_digest(record)
            path.write_text(json.dumps(record, ensure_ascii=False, sort_keys=True)
                            + "\n", encoding="utf-8")
            yield root, path, record

    @staticmethod
    def reseal(path, packet):
        packet["record_sha256"] = evidence_digest(packet)
        path.write_text(json.dumps(packet, ensure_ascii=False, sort_keys=True)
                        + "\n", encoding="utf-8")

    def test_real_process_isolated_original_capture_and_ledger_replays(self):
        actual = audit_isolated_evidence(self.root)
        self.assertEqual(actual.status, GOOD, (actual.violations, actual.missing))
        self.assertTrue(actual.local_record_checked)
        self.assertEqual(actual.record_sha256, self.record["record_sha256"])
        self.assertEqual(actual.native_cycle_digest,
                         self.record["native_cycle_digest"])
        self.assertEqual(actual.local_audit.status,
                         "LOCAL_NATIVE_RECEIPT_RETURNS_MATCHED")
        self.assertEqual(actual.local_audit.native_replay.status,
                         "NATIVE_FIXTURE_LINKS_REPLAYED")
        self.assertEqual(len(actual.local_audit.native_replay.segments), 3)
        self.assertGreater(actual.local_audit.native_replay.ledger_commit_count, 0)

    def test_file_is_original_capture_plus_complete_native_snapshot(self):
        packet = self.record
        self.assertEqual(packet["version"], VERSION)
        self.assertEqual(packet["source_main"], SOURCE_MAIN)
        self.assertEqual(packet["mode"], MODE)
        self.assertEqual(packet["root_binding_sha256"], root_binding(self.root))
        self.assertEqual(packet["record_sha256"], evidence_digest(packet))
        self.assertEqual(
            packet["return_capture"]["native_cycle_digest"],
            packet["native_cycle_digest"],
        )
        self.assertEqual(
            packet["return_capture_sha256"],
            packet["return_capture"]["capture_sha256"],
        )
        self.assertEqual(len(packet["native_cycle_receipt"]["native_artifacts"]), 10)
        self.assertEqual(
            packet["return_capture"]["return_sequence"],
            ["DecisionOSWa->PlanOS", "PlanOS->ActOS"],
        )

    def test_real_original_constructor_bindings_not_patched_in_parent(self):
        self.assertIs(native.build_replan_wa_activation_receipt,
                      self.wa_original)
        self.assertIs(native.build_plan_phase_activation_receipt,
                      self.plan_original)

    def test_audit_never_spawns_process_or_changes_evidence_and_store(self):
        paths = (
            self.record_path,
            self.root / "act" / "act-genesis.json",
            self.root / "act" / "act-ledger.jsonl",
            self.root / "act" / "act-snapshot.json",
        )
        previous = {str(path): path.read_bytes() for path in paths}
        with patch(
            "runtime.kuuos_lean_python_isolated_native_receipt_evidence_v0_9.subprocess.run",
            side_effect=AssertionError("audit must not launch a process"),
        ):
            result = audit_isolated_evidence(self.root)
        self.assertEqual(result.status, GOOD, result)
        self.assertEqual(previous, {str(path): path.read_bytes() for path in paths})

    def test_repeated_audit_produces_stable_scoped_results(self):
        self.assertEqual(audit_isolated_evidence(self.root), self.created)
        self.assertEqual(audit_isolated_evidence(self.root),
                         audit_isolated_evidence(self.root))

    def test_none_of_these_local_checks_grant_authenticity_or_authority(self):
        result = audit_isolated_evidence(self.root)
        self.assertEqual(result.status, GOOD, result)
        for field in (
            "external_issuer_authenticated", "historical_issuance_proved",
            "lean_python_refinement_proved", "formal_descent_certified",
            "execution_authority_granted", "truth_authority_granted",
            "git_merge_authority_granted",
        ):
            with self.subTest(field=field):
                self.assertIs(getattr(result, field), False)
        self.assertFalse(result.local_audit.original_constructor_returns_observed)

    def test_repeated_build_refuses_preexisting_fixture_without_overwrite(self):
        before = self.record_path.read_bytes()
        with self.assertRaises(ValueError):
            build_isolated_fixture_evidence(self.root)
        self.assertEqual(before, self.record_path.read_bytes())

    def test_explicit_atomic_write_once_does_not_replace_old_file(self):
        with self.clone() as (root, path, record):
            previous = path.read_bytes()
            with self.assertRaises(FileExistsError):
                _write_once(root, record)
            self.assertEqual(path.read_bytes(), previous)

    def test_missing_evidence_file_remains_no_data(self):
        with self.clone() as (root, path, record):
            path.unlink()
            result = audit_isolated_evidence(root)
        self.assertEqual(result.status, NO_DATA)
        self.assertIn("record:missing", result.missing)
        self.assertFalse(result.local_record_checked)

    def test_symlinked_evidence_is_blocked(self):
        with self.clone() as (root, path, record):
            path.unlink()
            path.symlink_to(self.record_path)
            result = audit_isolated_evidence(root)
        self.assertEqual(result.status, BLOCKED)
        self.assertIn("record:symlink_not_allowed", result.violations)

    def test_copied_directory_without_binding_update_is_blocked(self):
        with TemporaryDirectory(prefix="kuuos-v09-copy-unrebound-") as folder:
            root = Path(folder) / "copy"
            shutil.copytree(self.root, root)
            result = audit_isolated_evidence(root)
        self.assertEqual(result.status, BLOCKED)
        self.assertIn("record:root_binding_mismatch", result.violations)

    def test_explicitly_rebound_copy_demonstrates_no_external_signature(self):
        with self.clone() as (root, path, record):
            result = audit_isolated_evidence(root)
        self.assertEqual(result.status, GOOD, (result.violations, result.missing))
        self.assertFalse(result.external_issuer_authenticated)
        self.assertFalse(result.historical_issuance_proved)

    def test_wrong_record_checksum_is_not_ignored(self):
        with self.clone() as (root, path, packet):
            packet["record_sha256"] = "a" * 64
            path.write_text(json.dumps(packet) + "\n", encoding="utf-8")
            result = audit_isolated_evidence(root)
        self.assertEqual(result.status, BLOCKED)
        self.assertIn("record:checksum_mismatch", result.violations)

    def test_unknown_field_after_checksum_reseal_is_blocked(self):
        with self.clone() as (root, path, packet):
            packet["external_issuer_signature_verified"] = True
            self.reseal(path, packet)
            result = audit_isolated_evidence(root)
        self.assertEqual(result.status, BLOCKED)
        self.assertIn("record:field_inventory_mismatch", result.violations)

    def test_mode_and_source_commit_cannot_be_rewritten_to_pass(self):
        for name, value in (
            ("source_main", "invented-source-main"),
            ("mode", "externally-authenticated"),
            ("version", "v0.0"),
        ):
            with self.subTest(name=name), self.clone() as (root, path, packet):
                packet[name] = value
                self.reseal(path, packet)
                result = audit_isolated_evidence(root)
                self.assertEqual(result.status, BLOCKED)
                self.assertIn("record:source_version_mismatch"
                              if name != "mode" else
                              "record:observation_mode_mismatch", result.violations)

    def test_return_capture_reference_mismatch_survives_reseal(self):
        with self.clone() as (root, path, packet):
            packet["return_capture_sha256"] = "f" * 64
            self.reseal(path, packet)
            result = audit_isolated_evidence(root)
        self.assertEqual(result.status, BLOCKED)
        self.assertIn("record:return_capture_reference_mismatch",
                      result.violations)

    def test_original_wa_receipt_substitution_rejected_even_if_resealed(self):
        with self.clone() as (root, path, packet):
            capture = packet["return_capture"]
            wa = capture["wa_activation_receipt"]
            wa["next_plan_basis_digest"] = "tampered-next-plan"
            wa["wa_activation_receipt_digest"] = wa_activation_receipt_digest(wa)
            capture["capture_sha256"] = capture_digest(capture)
            packet["return_capture_sha256"] = capture["capture_sha256"]
            self.reseal(path, packet)
            result = audit_isolated_evidence(root)
        self.assertEqual(result.status, BLOCKED)
        self.assertTrue(any("original_native:captured_wa_receipt:" in s
                            for s in result.violations))

    def test_native_cycle_reference_substitution_rejected_even_if_resealed(self):
        with self.clone() as (root, path, packet):
            packet["native_cycle_digest"] = "different-digest"
            self.reseal(path, packet)
            result = audit_isolated_evidence(root)
        self.assertEqual(result.status, BLOCKED)
        self.assertIn("record:native_cycle_reference_mismatch",
                      result.violations)

    def test_original_ledger_tamper_blocks_local_record(self):
        with self.clone() as (root, path, packet):
            journal = root / "act" / "act-ledger.jsonl"
            lines = journal.read_text(encoding="utf-8").splitlines()
            entry = json.loads(lines[0])
            entry["result_act_state_digest"] = "0" * 64
            lines[0] = json.dumps(entry)
            journal.write_text("\n".join(lines) + "\n", encoding="utf-8")
            result = audit_isolated_evidence(root)
        self.assertEqual(result.status, BLOCKED)
        self.assertTrue(any(s.startswith("original_native:native_replay:act_store")
                            for s in result.violations))

    def test_record_invalid_json_is_blocked(self):
        with self.clone() as (root, path, packet):
            path.write_text("{ malformed json", encoding="utf-8")
            result = audit_isolated_evidence(root)
        self.assertEqual(result.status, BLOCKED)
        self.assertIn("record:invalid_json_or_read_failed", result.violations)

    def test_nonfinite_json_does_not_cross_runtime_boundary(self):
        with self.clone() as (root, path, packet):
            packet["return_capture"]["bad"] = float("nan")
            path.write_text(json.dumps(packet) + "\n", encoding="utf-8")
            result = audit_isolated_evidence(root)
        self.assertEqual(result.status, BLOCKED)

    def test_oversized_record_blocks_before_loading(self):
        with self.clone() as (root, path, packet):
            with path.open("wb") as handle:
                handle.write(b" " * (MAX_EVIDENCE_BYTES + 1))
            result = audit_isolated_evidence(root)
        self.assertEqual(result.status, BLOCKED)
        self.assertIn("record:oversize", result.violations)

    def test_refuse_untrusted_nonpath_and_symlink_root(self):
        result = audit_isolated_evidence(str(self.root))
        self.assertEqual(result.status, BLOCKED)
        with TemporaryDirectory(prefix="kuuos-v09-symlink-") as folder:
            linked = Path(folder) / "sym"
            linked.symlink_to(self.root, target_is_directory=True)
            self.assertEqual(audit_isolated_evidence(linked).status, BLOCKED)
            with self.assertRaises(ValueError):
                build_isolated_fixture_evidence(linked)

    def test_record_data_is_stored_under_only_one_fixed_filename(self):
        files = [p.name for p in self.root.iterdir() if p.is_file()]
        self.assertEqual(files, [EVIDENCE_FILE])
        self.assertNotIn("external_signature", self.record)

    def test_child_command_requires_explicit_flag(self):
        from runtime import kuuos_lean_python_isolated_native_receipt_evidence_v0_9 as mod
        self.assertEqual(mod.main([]), 2)
        self.assertEqual(mod.main(["--unknown", str(self.root)]), 2)

    def test_build_in_nonempty_root_is_refused_pre_effect(self):
        with TemporaryDirectory(prefix="kuuos-v09-no-overwrite-") as folder:
            root = Path(folder)
            marker = root / "keep.txt"
            marker.write_text("keep", encoding="utf-8")
            with self.assertRaises(ValueError):
                build_isolated_fixture_evidence(root)
            self.assertEqual(marker.read_text(encoding="utf-8"), "keep")
            self.assertFalse((root / "act").exists())


class EvidenceSourcePinTests(unittest.TestCase):
    def test_original_source_pins_and_native_test_registration(self):
        from scripts.check_kuuos_lean_python_isolated_evidence_sources_v0_9 import (
            SOURCE_BLOBS, check_sources,
        )
        self.assertGreaterEqual(len(SOURCE_BLOBS), 6)
        self.assertEqual(check_sources(ROOT), ())

    def test_source_byte_drift_is_detected_without_running_host(self):
        from scripts import check_kuuos_lean_python_isolated_evidence_sources_v0_9 as checker
        with TemporaryDirectory(prefix="kuuos-v09-pin-") as folder:
            root = Path(folder)
            candidate = "runtime/original.py"
            item = root / candidate
            item.parent.mkdir(parents=True)
            item.write_bytes(b"modified\n")
            with patch.object(checker, "SOURCE_BLOBS", {candidate: "0" * 40}), \
                 patch.object(checker, "REQUIRED_PATHS", ()):
                errors = checker.check_sources(root, check_registration=False)
        self.assertIn("source_byte_drift:" + candidate, errors)

    def test_comments_are_not_executable_cumulative_registration(self):
        from scripts import check_kuuos_lean_python_isolated_evidence_sources_v0_9 as checker
        with TemporaryDirectory(prefix="kuuos-v09-registration-") as folder:
            root = Path(folder)
            path = root / checker.REGISTERED_TEST_PATH
            path.parent.mkdir(parents=True)
            path.write_text(
                "# from tests.test_kuuos_lean_python_isolated_native_evidence_v0_9 "
                "import IsolatedNativeEvidenceTests\n",
                encoding="utf-8",
            )
            with patch.object(checker, "SOURCE_BLOBS", {}), \
                 patch.object(checker, "REQUIRED_PATHS", ()):
                errors = checker.check_sources(root)
        self.assertIn("native_tests_not_registered", errors)


if __name__ == "__main__":
    unittest.main()
