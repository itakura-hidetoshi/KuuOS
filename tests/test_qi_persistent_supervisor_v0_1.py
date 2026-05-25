import json
import tempfile
import unittest
from pathlib import Path

from runtime.kuuos_runtime_daemon_qi_persistent_supervisor_v0_1 import run_qi_persistent_supervisor

PROCESS_HISTORY = [
    {"step_id": "p0", "transition_visible": True, "memory_link_visible": True, "nonmarkov_link_visible": False},
    {"step_id": "p1", "transition_visible": True, "memory_link_visible": True, "nonmarkov_link_visible": True},
    {"step_id": "p2", "transition_visible": True, "memory_link_visible": True, "nonmarkov_link_visible": True},
]

RAW = {
    "cycle_id": "persistent-supervisor-001",
    "next_cycle_id": "persistent-supervisor-002",
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


class QiPersistentSupervisorTests(unittest.TestCase):
    def test_persistent_supervisor_runs_bounded_iteration_and_writes_heartbeat_status_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_path = root / "raw.json"
            evidence_path = root / "evidence.json"
            control_path = root / "control.json"
            out_dir = root / "supervisor"
            dump(raw_path, RAW)
            dump(evidence_path, EVIDENCE)
            dump(control_path, {"enabled": True, "stop_requested": False, "max_cycles": 1, "sleep_seconds_between_cycles": 0})
            result = run_qi_persistent_supervisor(
                raw_state_path=raw_path,
                evidence_path=evidence_path,
                out_dir=out_dir,
                control_path=control_path,
                max_outer_iterations=2,
                max_daemon_ticks=1,
                max_steps_per_tick=1,
                requested_max_reentry_cycles=1,
                sleep_seconds_between_iterations=0,
            )
            self.assertEqual(result.supervisor_status, "QI_PERSISTENT_SUPERVISOR_COMPLETED")
            self.assertGreaterEqual(result.iterations_run, 1)
            self.assertLessEqual(result.iterations_run, 2)
            self.assertTrue(Path(result.supervisor_manifest_path).is_file())
            self.assertTrue(result.persistent_supervisor_only)
            self.assertTrue(result.bounded)
            self.assertTrue(result.read_only)
            self.assertFalse(result.grants_execution_authority)
            self.assertFalse(result.grants_next_tick_execution_authority)
            for record in result.iteration_records:
                self.assertTrue(Path(record["heartbeat_path"]).is_file())
                self.assertTrue(Path(record["status_path"]).is_file())
                if record["loop_allowed"]:
                    self.assertTrue(Path(record["controlled_loop_result_path"]).is_file())
                    self.assertGreaterEqual(record["control_checks"], 1)
            self.assertIn(result.final_stop_reason, {
                "max_outer_iterations_reached",
                "max_cycles_reached",
                "hold_reobserve_requested",
                "successor_raw_state_missing",
                "successor_raw_state_not_found",
                "successor_raw_state_unchanged",
                "loop_disabled",
                "stop_requested",
            })

    def test_persistent_supervisor_stops_before_controlled_loop_when_stop_requested(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_path = root / "raw.json"
            evidence_path = root / "evidence.json"
            control_path = root / "control.json"
            out_dir = root / "supervisor"
            dump(raw_path, RAW)
            dump(evidence_path, EVIDENCE)
            dump(control_path, {"enabled": True, "stop_requested": True, "max_cycles": 1})
            result = run_qi_persistent_supervisor(
                raw_state_path=raw_path,
                evidence_path=evidence_path,
                out_dir=out_dir,
                control_path=control_path,
                max_outer_iterations=2,
            )
            self.assertEqual(result.iterations_run, 1)
            self.assertEqual(result.total_cycles_run, 0)
            self.assertEqual(result.final_stop_reason, "stop_requested")
            self.assertEqual(result.iteration_records[0]["loop_allowed"], False)
            self.assertIsNone(result.iteration_records[0]["controlled_loop_result_path"])
            self.assertTrue(Path(result.iteration_records[0]["heartbeat_path"]).is_file())
            self.assertTrue(Path(result.iteration_records[0]["status_path"]).is_file())

    def test_persistent_supervisor_rejects_invalid_outer_limits(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_path = root / "raw.json"
            evidence_path = root / "evidence.json"
            control_path = root / "control.json"
            dump(raw_path, RAW)
            dump(evidence_path, EVIDENCE)
            dump(control_path, {"enabled": True, "stop_requested": False, "max_cycles": 1})
            with self.assertRaises(ValueError):
                run_qi_persistent_supervisor(
                    raw_state_path=raw_path,
                    evidence_path=evidence_path,
                    out_dir=root / "supervisor",
                    control_path=control_path,
                    max_outer_iterations=0,
                )
            with self.assertRaises(ValueError):
                run_qi_persistent_supervisor(
                    raw_state_path=raw_path,
                    evidence_path=evidence_path,
                    out_dir=root / "supervisor",
                    control_path=control_path,
                    sleep_seconds_between_iterations=-1,
                )


if __name__ == "__main__":
    unittest.main()
