import json
import tempfile
import unittest
from pathlib import Path

from scripts.run_qi_process_tensor_bounded_tick_from_daemon_v0_1 import main


def write_json(path: Path, payload):
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


def write_granted_receipts(daemon_dir: Path):
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


class QiProcessTensorBoundedTickManualRunnerTests(unittest.TestCase):
    def test_manual_runner_without_token_writes_denial_receipt(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            daemon_dir = root / "daemon"
            output_dir = root / "out"
            raw_state = root / "raw_state.json"
            evidence = root / "evidence.json"
            daemon_dir.mkdir()
            raw_state.write_text(json.dumps({"qi_state": {}, "process_history": []}), encoding="utf-8")
            evidence.write_text(json.dumps({"evidence": []}), encoding="utf-8")
            write_json(
                daemon_dir / "daemon_qi_process_tensor_reentry_license_gate_v0_1.json",
                {
                    "gate_status": "QI_PROCESS_TENSOR_REENTRY_LICENSE_DENIED_HOLD",
                    "license_decision": "NO_BOUNDED_TICK_LICENSE",
                    "bounded_tick_license": False,
                    "may_invoke_next_tick": False,
                    "denied_reason": "reentry_plan_is_held",
                    "required_preconditions": ["observation_or_quarantine_exit_required"],
                },
            )
            rc = main([
                "--daemon-dir", str(daemon_dir),
                "--raw-state", str(raw_state),
                "--evidence", str(evidence),
                "--output-dir", str(output_dir),
                "--write",
            ])
            self.assertEqual(rc, 0)
            receipt_path = daemon_dir / "daemon_qi_process_tensor_bounded_tick_executor_receipt_v0_1.json"
            self.assertTrue(receipt_path.exists())
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            self.assertEqual(receipt["executor_status"], "QI_PROCESS_TENSOR_BOUNDED_TICK_NOT_INVOKED")
            self.assertFalse(receipt["tick_invoked"])
            self.assertFalse(receipt["grants_execution_authority"])
            self.assertFalse((output_dir / "run_manifest_v0_1.json").exists())

    def test_manual_runner_with_token_invokes_one_tick_without_health_projection(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            daemon_dir = root / "daemon"
            output_dir = root / "out"
            raw_state = root / "raw_state.json"
            evidence = root / "evidence.json"
            daemon_dir.mkdir()
            raw_state.write_text(json.dumps({"qi_state": {}, "process_history": []}), encoding="utf-8")
            evidence.write_text(json.dumps({"evidence": []}), encoding="utf-8")
            write_granted_receipts(daemon_dir)
            rc = main([
                "--daemon-dir", str(daemon_dir),
                "--raw-state", str(raw_state),
                "--evidence", str(evidence),
                "--output-dir", str(output_dir),
                "--write",
            ])
            self.assertEqual(rc, 0)
            receipt_path = daemon_dir / "daemon_qi_process_tensor_bounded_tick_executor_receipt_v0_1.json"
            self.assertTrue(receipt_path.exists())
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            self.assertEqual(receipt["executor_status"], "QI_PROCESS_TENSOR_BOUNDED_TICK_INVOKED")
            self.assertTrue(receipt["tick_invoked"])
            self.assertTrue(receipt["single_tick_invocation_token"])
            self.assertTrue(receipt["grants_execution_authority"])
            self.assertTrue((output_dir / "run_manifest_v0_1.json").exists())

    def test_manual_runner_with_health_projection_invokes_only_when_health_allows(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            daemon_dir = root / "daemon"
            output_dir = root / "out"
            raw_state = root / "raw_state.json"
            evidence = root / "evidence.json"
            daemon_dir.mkdir()
            raw_state.write_text(json.dumps({"qi_state": {}, "process_history": []}), encoding="utf-8")
            evidence.write_text(json.dumps({"evidence": []}), encoding="utf-8")
            write_granted_receipts(daemon_dir)
            write_json(
                daemon_dir / "daemon_qi_process_tensor_health_projection_v0_1.json",
                {
                    "projection_status": "QI_PROCESS_TENSOR_HEALTH_PROJECTED_WITH_RECOVERABILITY",
                    "recovery_unsafe": False,
                    "next_operator_action": "invoke_manual_runner",
                    "recoverability_status": "RECOVERABLE_BY_MANUAL_RUNNER",
                    "local_recovery_allowed": True,
                },
            )
            rc = main([
                "--daemon-dir", str(daemon_dir),
                "--raw-state", str(raw_state),
                "--evidence", str(evidence),
                "--output-dir", str(output_dir),
                "--write",
            ])
            self.assertEqual(rc, 0)
            receipt = json.loads((daemon_dir / "daemon_qi_process_tensor_bounded_tick_executor_receipt_v0_1.json").read_text(encoding="utf-8"))
            self.assertEqual(receipt["executor_status"], "QI_PROCESS_TENSOR_BOUNDED_TICK_INVOKED")
            self.assertTrue(receipt["tick_invoked"])
            self.assertTrue((output_dir / "run_manifest_v0_1.json").exists())

    def test_manual_runner_health_projection_blocks_unsafe_recovery_even_with_token(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            daemon_dir = root / "daemon"
            output_dir = root / "out"
            raw_state = root / "raw_state.json"
            evidence = root / "evidence.json"
            daemon_dir.mkdir()
            raw_state.write_text(json.dumps({"qi_state": {}, "process_history": []}), encoding="utf-8")
            evidence.write_text(json.dumps({"evidence": []}), encoding="utf-8")
            write_granted_receipts(daemon_dir)
            write_json(
                daemon_dir / "daemon_qi_process_tensor_health_projection_v0_1.json",
                {
                    "projection_status": "QI_PROCESS_TENSOR_HEALTH_PROJECTED_WITH_RECOVERABILITY",
                    "recovery_unsafe": True,
                    "next_operator_action": "hold",
                    "recoverability_status": "UNSAFE_RECOVERY",
                    "local_recovery_allowed": False,
                },
            )
            rc = main([
                "--daemon-dir", str(daemon_dir),
                "--raw-state", str(raw_state),
                "--evidence", str(evidence),
                "--output-dir", str(output_dir),
                "--write",
            ])
            self.assertEqual(rc, 0)
            receipt = json.loads((daemon_dir / "daemon_qi_process_tensor_bounded_tick_executor_receipt_v0_1.json").read_text(encoding="utf-8"))
            self.assertEqual(receipt["executor_status"], "QI_PROCESS_TENSOR_BOUNDED_TICK_NOT_INVOKED")
            self.assertEqual(receipt["denied_reason"], "health_projection_recovery_unsafe")
            self.assertFalse(receipt["tick_invoked"])
            self.assertFalse(receipt["grants_execution_authority"])
            self.assertFalse((output_dir / "run_manifest_v0_1.json").exists())

    def test_manual_runner_health_projection_blocks_non_manual_action(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            daemon_dir = root / "daemon"
            output_dir = root / "out"
            raw_state = root / "raw_state.json"
            evidence = root / "evidence.json"
            daemon_dir.mkdir()
            raw_state.write_text(json.dumps({"qi_state": {}, "process_history": []}), encoding="utf-8")
            evidence.write_text(json.dumps({"evidence": []}), encoding="utf-8")
            write_granted_receipts(daemon_dir)
            write_json(
                daemon_dir / "daemon_qi_process_tensor_health_projection_v0_1.json",
                {
                    "projection_status": "QI_PROCESS_TENSOR_HEALTH_PROJECTED_WITH_RECOVERABILITY",
                    "recovery_unsafe": False,
                    "next_operator_action": "reobserve",
                    "recoverability_status": "RECOVERABLE_BY_REOBSERVATION",
                    "local_recovery_allowed": True,
                },
            )
            rc = main([
                "--daemon-dir", str(daemon_dir),
                "--raw-state", str(raw_state),
                "--evidence", str(evidence),
                "--output-dir", str(output_dir),
                "--write",
            ])
            self.assertEqual(rc, 0)
            receipt = json.loads((daemon_dir / "daemon_qi_process_tensor_bounded_tick_executor_receipt_v0_1.json").read_text(encoding="utf-8"))
            self.assertEqual(receipt["executor_status"], "QI_PROCESS_TENSOR_BOUNDED_TICK_NOT_INVOKED")
            self.assertEqual(receipt["denied_reason"], "health_projection_next_operator_action_not_invoke_manual_runner")
            self.assertFalse(receipt["tick_invoked"])
            self.assertFalse((output_dir / "run_manifest_v0_1.json").exists())


if __name__ == "__main__":
    unittest.main()
