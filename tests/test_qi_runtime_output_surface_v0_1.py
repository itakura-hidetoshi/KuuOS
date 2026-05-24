import json
import tempfile
import unittest
from pathlib import Path

from runtime.kuuos_runtime_daemon_qi_runtime_output_surface_v0_1 import compile_qi_runtime_output_surface


def write_json(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


class QiRuntimeOutputSurfaceTests(unittest.TestCase):
    def test_surface_reads_daemon_qi_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            daemon_dir = Path(tmp) / "daemon"
            write_json(daemon_dir / "daemon_result_v0_1.json", {
                "daemon_status": "DAEMON_MAX_TICKS_REACHED_APPEND_ONLY",
                "stop_reason": "MAX_TICKS_REACHED",
                "ticks_run": 1,
                "final_raw_state_path": str(daemon_dir / "raw.json"),
                "final_state_bundle_path": str(daemon_dir / "bundle.json"),
            })
            write_json(daemon_dir / "daemon_qi_process_tensor_recoverability_projection_v0_1.json", {
                "recoverability_status": "RECOVERABLE_BY_MANUAL_RUNNER",
                "dominant_recovery_path": "manual_runner",
                "recommended_recovery_action": "invoke_manual_runner",
                "recoverability_score": 0.9,
                "recovery_unsafe": False,
                "local_recovery_allowed": True,
            })
            write_json(daemon_dir / "daemon_qi_process_tensor_health_projection_v0_1.json", {
                "qi_process_tensor_phase": "QI_SINGLE_TICK_TOKEN_READY",
                "daemon_health_status": "HEALTHY_REENTRY_READY",
                "next_operator_action": "invoke_manual_runner",
                "health_reason": "manual_runner_available",
            })
            write_json(daemon_dir / "daemon_qi_process_tensor_observation_debt_schedule_v0_1.json", {
                "observation_debt_status": "NO_OBSERVATION_DEBT",
                "recommended_observation_action": "no_action",
                "observation_priority": "low",
                "observation_urgency_score": 0.0,
            })
            write_json(daemon_dir / "daemon_qi_process_tensor_trace_compaction_plan_v0_1.json", {
                "compaction_plan_status": "NO_COMPACTION_DEBT",
                "recommended_compaction_action": "no_action",
                "compaction_priority": "low",
                "compaction_urgency_score": 0.0,
            })
            surface = compile_qi_runtime_output_surface(daemon_dir)
            self.assertEqual(surface.surface_status, "QI_RUNTIME_OUTPUT_SURFACE_COMPILED")
            self.assertEqual(surface.daemon_status, "DAEMON_MAX_TICKS_REACHED_APPEND_ONLY")
            self.assertEqual(surface.daemon_ticks_run, 1)
            self.assertEqual(surface.recoverability_status, "RECOVERABLE_BY_MANUAL_RUNNER")
            self.assertEqual(surface.daemon_health_status, "HEALTHY_REENTRY_READY")
            self.assertEqual(surface.observation_debt_status, "NO_OBSERVATION_DEBT")
            self.assertEqual(surface.compaction_plan_status, "NO_COMPACTION_DEBT")
            self.assertFalse(surface.grants_execution_authority)
            self.assertFalse(surface.grants_truth_authority)


if __name__ == "__main__":
    unittest.main()
