import json
import tempfile
import unittest
from pathlib import Path

from runtime.kuuos_runtime_daemon_qi_persistent_supervisor_v0_1 import run_qi_persistent_supervisor
from runtime.kuuos_runtime_daemon_qi_persistent_supervisor_status_view_v0_1 import (
    compile_qi_persistent_supervisor_status_view,
)

PROCESS_HISTORY = [
    {"step_id": "p0", "transition_visible": True, "memory_link_visible": True, "nonmarkov_link_visible": False},
    {"step_id": "p1", "transition_visible": True, "memory_link_visible": True, "nonmarkov_link_visible": True},
    {"step_id": "p2", "transition_visible": True, "memory_link_visible": True, "nonmarkov_link_visible": True},
]

RAW = {
    "cycle_id": "persistent-status-view-001",
    "next_cycle_id": "persistent-status-view-002",
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


class QiPersistentSupervisorStatusViewTests(unittest.TestCase):
    def test_status_view_reads_manifest_latest_heartbeat_status_advantage_and_probe_plan(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_path = root / "raw.json"
            evidence_path = root / "evidence.json"
            control_path = root / "control.json"
            out_dir = root / "supervisor"
            dump(raw_path, RAW)
            dump(evidence_path, EVIDENCE)
            dump(control_path, {"enabled": True, "stop_requested": False, "max_cycles": 1, "sleep_seconds_between_cycles": 0})
            supervisor = run_qi_persistent_supervisor(
                raw_state_path=raw_path,
                evidence_path=evidence_path,
                out_dir=out_dir,
                control_path=control_path,
                max_outer_iterations=1,
                max_daemon_ticks=1,
                max_steps_per_tick=1,
                requested_max_reentry_cycles=1,
            )
            view = compile_qi_persistent_supervisor_status_view(out_dir=out_dir)
            self.assertEqual(view.status_view_status, "QI_PERSISTENT_SUPERVISOR_STATUS_VIEW_READY")
            self.assertEqual(view.supervisor_status, supervisor.supervisor_status)
            self.assertEqual(view.iterations_run, supervisor.iterations_run)
            self.assertEqual(view.total_cycles_run, supervisor.total_cycles_run)
            self.assertEqual(view.total_control_checks, supervisor.total_control_checks)
            self.assertEqual(view.final_stop_reason, supervisor.final_stop_reason)
            self.assertEqual(view.latest_iteration_index, supervisor.iteration_records[-1]["iteration_index"])
            self.assertTrue(Path(view.latest_heartbeat_path).is_file())
            self.assertTrue(Path(view.latest_status_path).is_file())
            self.assertTrue(Path(view.latest_controlled_loop_result_path).is_file())
            self.assertIn("heartbeat_utc", view.latest_heartbeat)
            self.assertIn("status", view.latest_status)
            self.assertEqual(
                view.latest_process_tensor_advantage_metrics["metrics_status"],
                "QI_PROCESS_TENSOR_ADVANTAGE_READY",
            )
            self.assertGreater(view.process_tensor_advantage_score, 0)
            self.assertIn(view.process_tensor_advantage_level, {"high", "medium", "low", "minimal"})
            self.assertIn(view.recommended_next_process_focus, {
                "continue_process_tensor_supervision",
                "resolve_observation_debt",
                "open_recoverability_branch",
                "preserve_memory_kernel",
                "widen_safe_reentry_window",
            })
            self.assertIn(
                view.latest_process_tensor_probe_plan["probe_plan_status"],
                {"QI_PROCESS_TENSOR_PROBE_PLAN_READY", "QI_PROCESS_TENSOR_PROBE_PLAN_READY_WITH_WARNINGS"},
            )
            self.assertIn(view.recommended_probe_type, {
                "continue_process_tensor_supervision_probe",
                "observation_debt_probe",
                "recoverability_branch_probe",
                "memory_kernel_probe",
                "safe_reentry_window_probe",
                "nonmarkov_memory_link_probe",
                "multi_time_correlation_probe",
            })
            self.assertIsNotNone(view.probe_target_time_slice)
            self.assertIn(view.probe_risk_level, {"low", "medium", "high"})
            self.assertTrue(view.latest_process_tensor_probe_plan["probe_plan_only"])
            self.assertTrue(view.latest_process_tensor_probe_plan["read_only"])
            self.assertEqual(view.latest_process_tensor_probe_plan["authority"], "none")
            self.assertFalse(view.latest_process_tensor_probe_plan["grants_probe_execution_authority"])
            self.assertTrue(view.status_view_only)
            self.assertTrue(view.read_only)
            self.assertFalse(view.grants_execution_authority)
            self.assertFalse(view.grants_probe_execution_authority)
            self.assertFalse(view.grants_next_tick_execution_authority)

    def test_status_view_blocks_when_manifest_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            view = compile_qi_persistent_supervisor_status_view(out_dir=Path(tmp) / "missing")
            self.assertEqual(view.status_view_status, "QI_PERSISTENT_SUPERVISOR_STATUS_VIEW_BLOCKED")
            self.assertIn("supervisor_manifest_missing", view.view_blockers)
            self.assertEqual(view.iterations_run, 0)
            self.assertEqual(view.latest_process_tensor_advantage_metrics, {})
            self.assertEqual(view.latest_process_tensor_probe_plan, {})
            self.assertIsNone(view.process_tensor_advantage_score)
            self.assertIsNone(view.process_tensor_advantage_level)
            self.assertIsNone(view.recommended_probe_type)
            self.assertIsNone(view.probe_target_time_slice)
            self.assertIsNone(view.probe_risk_level)
            self.assertTrue(view.read_only)


if __name__ == "__main__":
    unittest.main()
