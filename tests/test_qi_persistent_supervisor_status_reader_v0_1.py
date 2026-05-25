import json
import tempfile
import unittest
from pathlib import Path

from runtime.kuuos_runtime_daemon_qi_persistent_supervisor_v0_1 import run_qi_persistent_supervisor
from runtime.kuuos_runtime_daemon_qi_persistent_supervisor_status_reader_v0_1 import read_qi_persistent_supervisor_status

PROCESS_HISTORY = [
    {"step_id": "p0", "transition_visible": True, "memory_link_visible": True, "nonmarkov_link_visible": False},
    {"step_id": "p1", "transition_visible": True, "memory_link_visible": True, "nonmarkov_link_visible": True},
    {"step_id": "p2", "transition_visible": True, "memory_link_visible": True, "nonmarkov_link_visible": True},
]

RAW = {
    "cycle_id": "persistent-status-001",
    "next_cycle_id": "persistent-status-002",
    "generated_at_utc": "2026-05-21T00:00:00+00:00",
    "dispatched_at_utc": "2026-05-21T00:00:01+00:00",
    "candidate_only": True,
    "nonfinal_marker": True,
    "two_truths_gap": True,
    "noncollapse_guard": True,
    "memory_overwrite_blocker": True,
    "world_identity_blocker": True,
    "physical_process_visible": True,
    "thermodynamic_activity_visible": True,
    "process_history": PROCESS_HISTORY,
    "barrier_witness_visible": True,
    "receipt_hash": True,
    "support_refs": True,
    "registry_key": True,
    "view_delivery_receipt": True,
    "channel_scope": True,
    "acknowledgment_marker": True,
}

EVIDENCE = {
    "boundary_review_evidence": True,
    "two_truths_gap": True,
    "noncollapse_guard": True,
    "identity_blocker": True,
    "receipt_hash": True,
    "support_refs": True,
    "registry_key": True,
    "view_delivery_receipt": True,
    "channel_scope": True,
    "acknowledgment_marker": True,
    "runtime_variation_visible": True,
    "policy_candidate_receipt": True,
    "value_witness_receipt": True,
    "barrier_witness_receipt": True,
    "candidate_only": True,
    "nonfinal_marker": True,
    "hold_review_evidence": True,
}


def dump(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


class QiPersistentSupervisorStatusReaderTests(unittest.TestCase):
    def test_reads_latest_heartbeat_and_status_from_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_path = root / "raw.json"
            evidence_path = root / "evidence.json"
            control_path = root / "control.json"
            out_dir = root / "supervisor"
            dump(raw_path, RAW)
            dump(evidence_path, EVIDENCE)
            dump(control_path, {"enabled": True, "stop_requested": False, "max_cycles": 1, "sleep_seconds_between_cycles": 0})
            loop_result = run_qi_persistent_supervisor(
                raw_state_path=raw_path,
                evidence_path=evidence_path,
                out_dir=out_dir,
                control_path=control_path,
                max_outer_iterations=1,
                max_daemon_ticks=1,
                max_steps_per_tick=1,
                requested_max_reentry_cycles=1,
                sleep_seconds_between_iterations=0,
            )
            readout = read_qi_persistent_supervisor_status(
                supervisor_manifest_path=Path(loop_result.supervisor_manifest_path)
            )
            self.assertEqual(readout.readout_status, "QI_PERSISTENT_SUPERVISOR_STATUS_READ")
            self.assertEqual(readout.supervisor_status, "QI_PERSISTENT_SUPERVISOR_COMPLETED")
            self.assertEqual(readout.iterations_run, loop_result.iterations_run)
            self.assertEqual(readout.total_cycles_run, loop_result.total_cycles_run)
            self.assertEqual(readout.total_control_checks, loop_result.total_control_checks)
            self.assertEqual(readout.final_stop_reason, loop_result.final_stop_reason)
            self.assertIsNotNone(readout.latest_iteration_index)
            self.assertTrue(Path(readout.latest_heartbeat_path).is_file())
            self.assertTrue(Path(readout.latest_status_path).is_file())
            self.assertIn("heartbeat_version", readout.latest_heartbeat)
            self.assertIn("status_version", readout.latest_status)
            self.assertTrue(readout.readout_only)
            self.assertTrue(readout.read_only)
            self.assertFalse(readout.grants_execution_authority)
            self.assertFalse(readout.grants_next_tick_execution_authority)

    def test_missing_manifest_returns_missing_readout_without_authority(self):
        with tempfile.TemporaryDirectory() as tmp:
            readout = read_qi_persistent_supervisor_status(
                supervisor_manifest_path=Path(tmp) / "missing.json"
            )
            self.assertEqual(readout.readout_status, "QI_PERSISTENT_SUPERVISOR_STATUS_MISSING")
            self.assertEqual(readout.iterations_run, 0)
            self.assertEqual(readout.total_cycles_run, 0)
            self.assertEqual(readout.total_control_checks, 0)
            self.assertIsNone(readout.latest_iteration_index)
            self.assertEqual(readout.latest_heartbeat, {})
            self.assertEqual(readout.latest_status, {})
            self.assertFalse(readout.grants_truth_authority)
            self.assertFalse(readout.grants_memory_overwrite_authority)


if __name__ == "__main__":
    unittest.main()
