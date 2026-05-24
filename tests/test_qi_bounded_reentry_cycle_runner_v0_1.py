import json
import tempfile
import unittest
from pathlib import Path

from runtime.kuuos_runtime_daemon_qi_bounded_reentry_cycle_runner_v0_1 import run_qi_bounded_reentry_cycle


def write_json(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


def base_files(root: Path):
    daemon_dir = root / "daemon"
    output_dir = root / "out"
    raw_state = root / "raw_state.json"
    evidence = root / "evidence.json"
    daemon_dir.mkdir()
    write_json(raw_state, {"qi_state": {}, "process_history": []})
    write_json(evidence, {"evidence": []})
    write_json(
        daemon_dir / "daemon_qi_process_tensor_reentry_license_gate_v0_1.json",
        {
            "gate_status": "QI_PROCESS_TENSOR_REENTRY_LICENSE_GRANTED",
            "license_decision": "BOUNDED_TICK_LICENSE_GRANTED",
            "bounded_tick_license": True,
            "may_invoke_next_tick": True,
            "licensed_max_steps_per_tick": 1,
        },
    )
    write_json(
        daemon_dir / "daemon_qi_process_tensor_bounded_tick_invocation_boundary_v0_1.json",
        {
            "boundary_status": "QI_PROCESS_TENSOR_INVOCATION_BOUNDARY_GRANTED_SINGLE_TICK",
            "invocation_decision": "SINGLE_TICK_INVOCATION_TOKEN_GRANTED",
            "single_tick_invocation_token": True,
            "licensed_max_steps_per_tick": 1,
        },
    )
    return daemon_dir, output_dir, raw_state, evidence


def write_health(daemon_dir: Path, *, action="invoke_manual_runner", status="RECOVERABLE_BY_MANUAL_RUNNER", unsafe=False, allowed=True):
    write_json(
        daemon_dir / "daemon_qi_process_tensor_health_projection_v0_1.json",
        {
            "projection_status": "QI_PROCESS_TENSOR_HEALTH_PROJECTED_WITH_RECOVERABILITY",
            "daemon_health_status": "HEALTHY_REENTRY_READY" if action == "invoke_manual_runner" else "REOBSERVE_REQUIRED",
            "next_operator_action": action,
            "recoverability_status": status,
            "recovery_unsafe": unsafe,
            "local_recovery_allowed": allowed,
        },
    )


class QiBoundedReentryCycleRunnerTests(unittest.TestCase):
    def test_cycle_invokes_when_health_allows_without_refresh_before(self):
        with tempfile.TemporaryDirectory() as tmp:
            daemon_dir, output_dir, raw_state, evidence = base_files(Path(tmp))
            write_health(daemon_dir)
            result = run_qi_bounded_reentry_cycle(
                daemon_dir=daemon_dir,
                raw_state_path=raw_state,
                evidence_path=evidence,
                output_dir=output_dir,
                refresh_before=False,
                refresh_after=False,
            )
            self.assertEqual(result.cycle_status, "QI_BOUNDED_REENTRY_CYCLE_INVOKED")
            self.assertTrue(result.tick_invoked)
            self.assertTrue(result.grants_execution_authority)
            self.assertTrue(result.handoff_available)
            self.assertEqual(result.handoff_steps_run, 1)
            self.assertTrue(Path(result.handoff_raw_state_path).is_file())
            self.assertTrue(Path(result.handoff_state_bundle_path).is_file())
            self.assertTrue(Path(result.handoff_run_manifest_path).is_file())
            self.assertTrue(Path(result.handoff_step_trace_path).is_file())
            self.assertEqual(result.pre_next_operator_action, "invoke_manual_runner")
            self.assertTrue((output_dir / "run_manifest_v0_1.json").exists())
            receipt = json.loads(Path(result.executor_receipt_path).read_text(encoding="utf-8"))
            self.assertEqual(receipt["executor_status"], "QI_PROCESS_TENSOR_BOUNDED_TICK_INVOKED")
            self.assertEqual(receipt["next_raw_state_path"], result.handoff_raw_state_path)
            self.assertEqual(receipt["state_bundle_path"], result.handoff_state_bundle_path)
            self.assertEqual(receipt["step_trace_path"], result.handoff_step_trace_path)

    def test_cycle_blocks_unsafe_health_even_with_token(self):
        with tempfile.TemporaryDirectory() as tmp:
            daemon_dir, output_dir, raw_state, evidence = base_files(Path(tmp))
            write_health(daemon_dir, action="hold", status="UNSAFE_RECOVERY", unsafe=True, allowed=False)
            result = run_qi_bounded_reentry_cycle(
                daemon_dir=daemon_dir,
                raw_state_path=raw_state,
                evidence_path=evidence,
                output_dir=output_dir,
                refresh_before=False,
                refresh_after=False,
            )
            self.assertEqual(result.cycle_status, "QI_BOUNDED_REENTRY_CYCLE_NOT_INVOKED")
            self.assertFalse(result.tick_invoked)
            self.assertFalse(result.grants_execution_authority)
            self.assertFalse(result.handoff_available)
            self.assertIsNone(result.handoff_raw_state_path)
            self.assertIsNone(result.handoff_state_bundle_path)
            self.assertIsNone(result.handoff_step_trace_path)
            self.assertEqual(result.handoff_steps_run, 0)
            self.assertEqual(result.denied_reason, "health_projection_recovery_unsafe")
            self.assertFalse((output_dir / "run_manifest_v0_1.json").exists())

    def test_cycle_blocks_non_manual_health_action(self):
        with tempfile.TemporaryDirectory() as tmp:
            daemon_dir, output_dir, raw_state, evidence = base_files(Path(tmp))
            write_health(daemon_dir, action="reobserve", status="RECOVERABLE_BY_REOBSERVATION", unsafe=False, allowed=True)
            result = run_qi_bounded_reentry_cycle(
                daemon_dir=daemon_dir,
                raw_state_path=raw_state,
                evidence_path=evidence,
                output_dir=output_dir,
                refresh_before=False,
                refresh_after=False,
            )
            self.assertEqual(result.cycle_status, "QI_BOUNDED_REENTRY_CYCLE_NOT_INVOKED")
            self.assertFalse(result.tick_invoked)
            self.assertFalse(result.handoff_available)
            self.assertEqual(result.denied_reason, "health_projection_next_operator_action_not_invoke_manual_runner")

    def test_cycle_refresh_after_updates_post_health(self):
        with tempfile.TemporaryDirectory() as tmp:
            daemon_dir, output_dir, raw_state, evidence = base_files(Path(tmp))
            write_health(daemon_dir)
            result = run_qi_bounded_reentry_cycle(
                daemon_dir=daemon_dir,
                raw_state_path=raw_state,
                evidence_path=evidence,
                output_dir=output_dir,
                refresh_before=False,
                refresh_after=True,
            )
            self.assertEqual(result.cycle_status, "QI_BOUNDED_REENTRY_CYCLE_INVOKED")
            self.assertTrue(result.handoff_available)
            self.assertTrue(Path(result.post_health_projection_path).is_file())
            self.assertIsNotNone(result.post_daemon_health_status)
            self.assertIsNotNone(result.post_recoverability_status)


if __name__ == "__main__":
    unittest.main()
