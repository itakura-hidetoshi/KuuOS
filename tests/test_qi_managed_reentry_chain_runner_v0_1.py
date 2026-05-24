import json
import tempfile
import unittest
from pathlib import Path

from runtime.kuuos_runtime_daemon_qi_managed_reentry_chain_runner_v0_1 import run_qi_managed_reentry_chain


def write_json(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


def base_files(root: Path):
    daemon_dir = root / "daemon"
    chain_dir = root / "managed_chain"
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


def write_health(daemon_dir: Path, *, score=0.95, action="invoke_manual_runner", status="RECOVERABLE_BY_MANUAL_RUNNER", unsafe=False, allowed=True):
    write_json(
        daemon_dir / "daemon_qi_process_tensor_health_projection_v0_1.json",
        {
            "projection_status": "QI_PROCESS_TENSOR_HEALTH_PROJECTED_WITH_RECOVERABILITY",
            "daemon_health_status": "HEALTHY_REENTRY_READY" if action == "invoke_manual_runner" else "REOBSERVE_REQUIRED",
            "next_operator_action": action,
            "recoverability_status": status,
            "recoverability_score": score,
            "recovery_unsafe": unsafe,
            "local_recovery_allowed": allowed,
        },
    )


class QiManagedReentryChainRunnerTests(unittest.TestCase):
    def test_managed_runner_invokes_allowed_chain_with_controller_limit(self):
        with tempfile.TemporaryDirectory() as tmp:
            daemon_dir, chain_dir, raw_state, evidence = base_files(Path(tmp))
            write_health(daemon_dir, score=0.95)
            result = run_qi_managed_reentry_chain(
                daemon_dir=daemon_dir,
                raw_state_path=raw_state,
                evidence_path=evidence,
                chain_dir=chain_dir,
                requested_max_cycles=5,
                refresh_before_first=False,
                refresh_after_each=False,
            )
            self.assertEqual(result.managed_runner_status, "QI_MANAGED_REENTRY_CHAIN_INVOKED")
            self.assertEqual(result.requested_max_cycles, 5)
            self.assertEqual(result.allowed_max_cycles, 3)
            self.assertEqual(result.controller_decision, "CHAIN_ALLOWED_STABLE")
            self.assertTrue(result.chain_invoked)
            self.assertEqual(result.cycles_run, 3)
            self.assertEqual(result.ticks_invoked, 3)
            self.assertTrue(Path(result.controller_decision_path).is_file())
            self.assertTrue(Path(result.chain_result_path).is_file())
            self.assertTrue(Path(result.final_raw_state_path).is_file())
            self.assertTrue(Path(result.final_state_bundle_path).is_file())
            controller = json.loads(Path(result.controller_decision_path).read_text(encoding="utf-8"))
            chain = json.loads(Path(result.chain_result_path).read_text(encoding="utf-8"))
            self.assertEqual(controller["allowed_max_cycles"], 3)
            self.assertEqual(chain["ticks_invoked"], 3)

    def test_managed_runner_uses_bounded_controller_limit(self):
        with tempfile.TemporaryDirectory() as tmp:
            daemon_dir, chain_dir, raw_state, evidence = base_files(Path(tmp))
            write_health(daemon_dir, score=0.75)
            result = run_qi_managed_reentry_chain(
                daemon_dir=daemon_dir,
                raw_state_path=raw_state,
                evidence_path=evidence,
                chain_dir=chain_dir,
                requested_max_cycles=5,
                refresh_before_first=False,
                refresh_after_each=False,
            )
            self.assertEqual(result.allowed_max_cycles, 2)
            self.assertEqual(result.cycles_run, 2)
            self.assertEqual(result.ticks_invoked, 2)
            self.assertEqual(result.controller_decision, "CHAIN_ALLOWED_BOUNDED")

    def test_managed_runner_does_not_invoke_when_controller_blocks(self):
        with tempfile.TemporaryDirectory() as tmp:
            daemon_dir, chain_dir, raw_state, evidence = base_files(Path(tmp))
            write_health(daemon_dir, action="hold", status="UNSAFE_RECOVERY", unsafe=True, allowed=False)
            result = run_qi_managed_reentry_chain(
                daemon_dir=daemon_dir,
                raw_state_path=raw_state,
                evidence_path=evidence,
                chain_dir=chain_dir,
                requested_max_cycles=5,
                refresh_before_first=False,
                refresh_after_each=False,
            )
            self.assertEqual(result.managed_runner_status, "QI_MANAGED_REENTRY_CHAIN_NOT_INVOKED")
            self.assertEqual(result.allowed_max_cycles, 0)
            self.assertEqual(result.controller_decision, "CHAIN_NOT_ALLOWED")
            self.assertEqual(result.controller_reason, "recovery_unsafe")
            self.assertFalse(result.chain_invoked)
            self.assertEqual(result.cycles_run, 0)
            self.assertEqual(result.ticks_invoked, 0)
            self.assertIsNone(result.chain_result_path)
            self.assertIsNone(result.final_raw_state_path)
            self.assertFalse(result.grants_execution_authority)
            self.assertTrue(Path(result.controller_decision_path).is_file())

    def test_managed_runner_single_step_for_fragile_recovery(self):
        with tempfile.TemporaryDirectory() as tmp:
            daemon_dir, chain_dir, raw_state, evidence = base_files(Path(tmp))
            write_health(daemon_dir, score=0.4)
            result = run_qi_managed_reentry_chain(
                daemon_dir=daemon_dir,
                raw_state_path=raw_state,
                evidence_path=evidence,
                chain_dir=chain_dir,
                requested_max_cycles=5,
                refresh_before_first=False,
                refresh_after_each=False,
            )
            self.assertEqual(result.controller_decision, "CHAIN_ALLOWED_SINGLE_STEP")
            self.assertEqual(result.allowed_max_cycles, 1)
            self.assertEqual(result.cycles_run, 1)
            self.assertEqual(result.ticks_invoked, 1)


if __name__ == "__main__":
    unittest.main()
