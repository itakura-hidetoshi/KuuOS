import json
import tempfile
import unittest
from pathlib import Path

from runtime.kuuos_runtime_daemon_qi_reentry_handoff_chain_runner_v0_1 import run_qi_reentry_handoff_chain


def write_json(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


def base_files(root: Path):
    daemon_dir = root / "daemon"
    chain_dir = root / "chain"
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
    return daemon_dir, chain_dir, raw_state, evidence


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


class QiReentryHandoffChainRunnerTests(unittest.TestCase):
    def test_chain_runs_two_cycles_using_handoff(self):
        with tempfile.TemporaryDirectory() as tmp:
            daemon_dir, chain_dir, raw_state, evidence = base_files(Path(tmp))
            write_health(daemon_dir)
            result = run_qi_reentry_handoff_chain(
                daemon_dir=daemon_dir,
                raw_state_path=raw_state,
                evidence_path=evidence,
                chain_dir=chain_dir,
                max_cycles=2,
                refresh_before_first=False,
                refresh_after_each=False,
            )
            self.assertEqual(result.chain_status, "QI_REENTRY_HANDOFF_CHAIN_COMPLETED")
            self.assertEqual(result.cycles_requested, 2)
            self.assertEqual(result.cycles_run, 2)
            self.assertEqual(result.ticks_invoked, 2)
            self.assertEqual(result.stop_reason, "MAX_CYCLES_REACHED")
            self.assertTrue(Path(result.final_raw_state_path).is_file())
            self.assertTrue(Path(result.final_state_bundle_path).is_file())
            self.assertTrue(Path(result.final_executor_receipt_path).is_file())
            self.assertEqual(len(result.cycle_result_paths), 2)
            for rel in result.cycle_result_paths:
                self.assertTrue(Path(rel).is_file())
                cycle = json.loads(Path(rel).read_text(encoding="utf-8"))
                self.assertTrue(cycle["handoff_available"])
                self.assertTrue(Path(cycle["handoff_raw_state_path"]).is_file())
                self.assertTrue(Path(cycle["handoff_state_bundle_path"]).is_file())

    def test_chain_stops_without_handoff_when_health_blocks(self):
        with tempfile.TemporaryDirectory() as tmp:
            daemon_dir, chain_dir, raw_state, evidence = base_files(Path(tmp))
            write_health(daemon_dir, action="hold", status="UNSAFE_RECOVERY", unsafe=True, allowed=False)
            result = run_qi_reentry_handoff_chain(
                daemon_dir=daemon_dir,
                raw_state_path=raw_state,
                evidence_path=evidence,
                chain_dir=chain_dir,
                max_cycles=3,
                refresh_before_first=False,
                refresh_after_each=False,
            )
            self.assertEqual(result.chain_status, "QI_REENTRY_HANDOFF_CHAIN_NOT_INVOKED")
            self.assertEqual(result.cycles_requested, 3)
            self.assertEqual(result.cycles_run, 1)
            self.assertEqual(result.ticks_invoked, 0)
            self.assertEqual(result.stop_reason, "health_projection_recovery_unsafe")
            self.assertIsNone(result.final_raw_state_path)
            self.assertIsNone(result.final_state_bundle_path)
            self.assertTrue(Path(result.final_executor_receipt_path).is_file())
            self.assertEqual(len(result.cycle_result_paths), 1)
            cycle = json.loads(Path(result.cycle_result_paths[0]).read_text(encoding="utf-8"))
            self.assertFalse(cycle["handoff_available"])
            self.assertIsNone(cycle["handoff_raw_state_path"])
            self.assertFalse(cycle["grants_execution_authority"])

    def test_chain_caps_max_cycles_to_five(self):
        with tempfile.TemporaryDirectory() as tmp:
            daemon_dir, chain_dir, raw_state, evidence = base_files(Path(tmp))
            write_health(daemon_dir)
            result = run_qi_reentry_handoff_chain(
                daemon_dir=daemon_dir,
                raw_state_path=raw_state,
                evidence_path=evidence,
                chain_dir=chain_dir,
                max_cycles=100,
                refresh_before_first=False,
                refresh_after_each=False,
            )
            self.assertEqual(result.cycles_requested, 5)
            self.assertEqual(result.cycles_run, 5)
            self.assertEqual(result.ticks_invoked, 5)
            self.assertEqual(result.stop_reason, "MAX_CYCLES_REACHED")


if __name__ == "__main__":
    unittest.main()
