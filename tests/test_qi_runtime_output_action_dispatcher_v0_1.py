import json
import tempfile
import unittest
from pathlib import Path

from runtime.kuuos_runtime_daemon_qi_runtime_output_action_dispatcher_v0_1 import dispatch_qi_runtime_output_action


def write_json(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


def write_surface(daemon_dir: Path, **updates):
    surface = {
        "daemon_status": "DAEMON_MAX_TICKS_REACHED_APPEND_ONLY",
        "daemon_stop_reason": "MAX_TICKS_REACHED",
        "recoverability_status": "RECOVERY_UNRESOLVED",
        "recommended_recovery_action": "no_action",
        "recovery_unsafe": False,
        "daemon_health_status": "HEALTHY",
        "next_operator_action": "no_action",
        "observation_debt_status": "NO_OBSERVATION_DEBT",
        "recommended_observation_action": "no_action",
        "compaction_plan_status": "NO_COMPACTION_DEBT",
        "recommended_compaction_action": "no_action",
    }
    surface.update(updates)
    write_json(daemon_dir / "daemon_qi_runtime_output_surface_v0_1.json", surface)


def write_reentry_receipts(daemon_dir: Path):
    write_json(daemon_dir / "daemon_qi_process_tensor_reentry_license_gate_v0_1.json", {
        "gate_status": "QI_PROCESS_TENSOR_REENTRY_LICENSE_GRANTED",
        "license_decision": "BOUNDED_TICK_LICENSE_GRANTED",
        "bounded_tick_license": True,
        "may_invoke_next_tick": True,
        "licensed_max_steps_per_tick": 1,
    })
    write_json(daemon_dir / "daemon_qi_process_tensor_bounded_tick_invocation_boundary_v0_1.json", {
        "boundary_status": "QI_PROCESS_TENSOR_INVOCATION_BOUNDARY_GRANTED_SINGLE_TICK",
        "invocation_decision": "SINGLE_TICK_INVOCATION_TOKEN_GRANTED",
        "single_tick_invocation_token": True,
        "licensed_max_steps_per_tick": 1,
    })
    write_json(daemon_dir / "daemon_qi_process_tensor_health_projection_v0_1.json", {
        "recoverability_status": "RECOVERABLE_BY_MANUAL_RUNNER",
        "recoverability_score": 0.95,
        "recovery_unsafe": False,
        "local_recovery_allowed": True,
        "next_operator_action": "invoke_manual_runner",
        "daemon_health_status": "HEALTHY_REENTRY_READY",
    })


class QiRuntimeOutputActionDispatcherTests(unittest.TestCase):
    def test_dispatcher_does_not_execute_hold_route(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            daemon_dir = root / "daemon"
            dispatch_dir = root / "dispatch"
            write_surface(daemon_dir, recovery_unsafe=True, next_operator_action="hold")
            result = dispatch_qi_runtime_output_action(daemon_dir=daemon_dir, dispatch_dir=dispatch_dir)
            self.assertEqual(result.dispatcher_status, "QI_RUNTIME_OUTPUT_ACTION_NOT_DISPATCHED")
            self.assertEqual(result.next_outer_action, "hold")
            self.assertFalse(result.action_invoked)
            self.assertFalse(result.grants_execution_authority)
            self.assertTrue(Path(result.route_path).is_file())

    def test_dispatcher_does_not_execute_observation_or_compaction_routes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            daemon_dir = root / "daemon"
            dispatch_dir = root / "dispatch"
            write_surface(daemon_dir, observation_debt_status="OBSERVATION_DEBT_OPEN", recommended_observation_action="observe")
            result = dispatch_qi_runtime_output_action(daemon_dir=daemon_dir, dispatch_dir=dispatch_dir)
            self.assertEqual(result.next_outer_action, "observe")
            self.assertFalse(result.action_invoked)
            write_surface(daemon_dir, observation_debt_status="NO_OBSERVATION_DEBT", recommended_observation_action="no_action", compaction_plan_status="COMPACTION_READY", recommended_compaction_action="compact_trace")
            result = dispatch_qi_runtime_output_action(daemon_dir=daemon_dir, dispatch_dir=dispatch_dir)
            self.assertEqual(result.next_outer_action, "compact_trace")
            self.assertFalse(result.action_invoked)

    def test_dispatcher_requires_raw_state_and_evidence_for_reentry(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            daemon_dir = root / "daemon"
            dispatch_dir = root / "dispatch"
            write_surface(daemon_dir, recoverability_status="RECOVERABLE_BY_MANUAL_RUNNER", recommended_recovery_action="invoke_manual_runner", next_operator_action="invoke_manual_runner")
            result = dispatch_qi_runtime_output_action(daemon_dir=daemon_dir, dispatch_dir=dispatch_dir)
            self.assertEqual(result.next_outer_action, "managed_reentry_chain")
            self.assertFalse(result.action_invoked)
            self.assertEqual(result.dispatch_reason, "managed_reentry_requires_raw_state_and_evidence")

    def test_dispatcher_invokes_managed_reentry_chain_when_inputs_present(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            daemon_dir = root / "daemon"
            dispatch_dir = root / "dispatch"
            raw_state = root / "raw.json"
            evidence = root / "evidence.json"
            write_json(raw_state, {"qi_state": {}, "process_history": []})
            write_json(evidence, {"evidence": []})
            write_surface(daemon_dir, recoverability_status="RECOVERABLE_BY_MANUAL_RUNNER", recommended_recovery_action="invoke_manual_runner", next_operator_action="invoke_manual_runner")
            write_reentry_receipts(daemon_dir)
            result = dispatch_qi_runtime_output_action(
                daemon_dir=daemon_dir,
                dispatch_dir=dispatch_dir,
                raw_state_path=raw_state,
                evidence_path=evidence,
                requested_max_reentry_cycles=1,
                refresh_before_first=False,
                refresh_after_each=False,
            )
            self.assertEqual(result.dispatcher_status, "QI_RUNTIME_OUTPUT_ACTION_DISPATCHED")
            self.assertTrue(result.action_invoked)
            self.assertEqual(result.invoked_action, "managed_reentry_chain")
            self.assertEqual(result.reentry_ticks_invoked, 1)
            self.assertTrue(Path(result.managed_chain_result_path).is_file())
            self.assertTrue(Path(result.final_raw_state_path).is_file())


if __name__ == "__main__":
    unittest.main()
