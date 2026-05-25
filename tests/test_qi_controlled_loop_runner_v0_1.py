import json
import tempfile
import unittest
from pathlib import Path

from runtime.kuuos_runtime_daemon_qi_controlled_loop_runner_v0_1 import run_qi_controlled_loop

PROCESS_HISTORY = [
    {"step_id": "p0", "transition_visible": True, "memory_link_visible": True, "nonmarkov_link_visible": False},
    {"step_id": "p1", "transition_visible": True, "memory_link_visible": True, "nonmarkov_link_visible": True},
    {"step_id": "p2", "transition_visible": True, "memory_link_visible": True, "nonmarkov_link_visible": True},
]

RAW = {
    "cycle_id": "controlled-loop-001",
    "next_cycle_id": "controlled-loop-002",
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


class QiControlledLoopRunnerTests(unittest.TestCase):
    def test_controlled_loop_runs_with_allow_control_and_writes_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_path = root / "raw.json"
            evidence_path = root / "evidence.json"
            control_path = root / "control.json"
            out_dir = root / "controlled"
            dump(raw_path, RAW)
            dump(evidence_path, EVIDENCE)
            dump(control_path, {"enabled": True, "stop_requested": False, "max_cycles": 2, "sleep_seconds_between_cycles": 0})
            result = run_qi_controlled_loop(
                raw_state_path=raw_path,
                evidence_path=evidence_path,
                out_dir=out_dir,
                control_path=control_path,
                max_daemon_ticks=1,
                max_steps_per_tick=1,
                requested_max_reentry_cycles=1,
            )
            self.assertEqual(result.loop_status, "QI_CONTROLLED_LOOP_COMPLETED")
            self.assertGreaterEqual(result.control_checks, 1)
            self.assertGreaterEqual(result.cycles_run, 1)
            self.assertLessEqual(result.cycles_run, 2)
            self.assertTrue(Path(result.loop_manifest_path).is_file())
            self.assertTrue(result.controlled_loop_only)
            self.assertTrue(result.bounded)
            self.assertTrue(result.read_only)
            self.assertFalse(result.grants_execution_authority)
            self.assertFalse(result.grants_next_tick_execution_authority)
            for record in result.cycle_records:
                if record["loop_allowed"]:
                    self.assertTrue(Path(record["routed_projection_plan_result_path"]).is_file())
                    self.assertTrue(Path(record["readable_summary_path"]).is_file())
                    self.assertIn("recoverability", record["projection_statuses"])

    def test_controlled_loop_stops_before_cycle_when_stop_requested(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_path = root / "raw.json"
            evidence_path = root / "evidence.json"
            control_path = root / "control.json"
            out_dir = root / "controlled"
            dump(raw_path, RAW)
            dump(evidence_path, EVIDENCE)
            dump(control_path, {"enabled": True, "stop_requested": True, "max_cycles": 2, "sleep_seconds_between_cycles": 0})
            result = run_qi_controlled_loop(
                raw_state_path=raw_path,
                evidence_path=evidence_path,
                out_dir=out_dir,
                control_path=control_path,
            )
            self.assertEqual(result.cycles_run, 0)
            self.assertEqual(result.final_stop_reason, "stop_requested")
            self.assertEqual(result.control_checks, 1)
            self.assertEqual(len(result.cycle_records), 1)
            self.assertFalse(result.cycle_records[0]["loop_allowed"])
            self.assertTrue(Path(result.loop_manifest_path).is_file())

    def test_controlled_loop_stops_before_cycle_when_disabled(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_path = root / "raw.json"
            evidence_path = root / "evidence.json"
            control_path = root / "control.json"
            out_dir = root / "controlled"
            dump(raw_path, RAW)
            dump(evidence_path, EVIDENCE)
            dump(control_path, {"enabled": False, "stop_requested": False, "max_cycles": 2})
            result = run_qi_controlled_loop(
                raw_state_path=raw_path,
                evidence_path=evidence_path,
                out_dir=out_dir,
                control_path=control_path,
            )
            self.assertEqual(result.cycles_run, 0)
            self.assertEqual(result.final_stop_reason, "loop_disabled")
            self.assertFalse(result.cycle_records[0]["loop_allowed"])


if __name__ == "__main__":
    unittest.main()
