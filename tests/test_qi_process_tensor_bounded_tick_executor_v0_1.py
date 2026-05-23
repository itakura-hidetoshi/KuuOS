import json
import tempfile
import unittest
from pathlib import Path

from runtime.kuuos_runtime_daemon_qi_process_tensor_bounded_tick_executor_v0_1 import (
    compile_denied_bounded_tick_executor_receipt,
    run_qi_process_tensor_bounded_tick_executor,
)


class QiProcessTensorBoundedTickExecutorTests(unittest.TestCase):
    def test_denied_license_does_not_invoke_tick(self):
        receipt = compile_denied_bounded_tick_executor_receipt(
            {
                "gate_status": "QI_PROCESS_TENSOR_REENTRY_LICENSE_DENIED_REOBSERVE",
                "license_decision": "NO_BOUNDED_TICK_LICENSE",
                "bounded_tick_license": False,
                "denied_reason": "reobserve_required_before_reentry",
                "required_preconditions": ["fresh_observation_required_before_reentry"],
            }
        )
        self.assertEqual(receipt.executor_status, "QI_PROCESS_TENSOR_BOUNDED_TICK_NOT_INVOKED")
        self.assertFalse(receipt.tick_invoked)
        self.assertFalse(receipt.grants_execution_authority)
        self.assertEqual(receipt.steps_run, 0)
        self.assertEqual(receipt.denied_reason, "reobserve_required_before_reentry")

    def test_missing_license_does_not_invoke_tick_even_with_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_state = root / "raw_state.json"
            evidence = root / "evidence.json"
            output_dir = root / "out"
            raw_state.write_text(json.dumps({"qi_state": {}}), encoding="utf-8")
            evidence.write_text(json.dumps({"evidence": []}), encoding="utf-8")
            receipt = run_qi_process_tensor_bounded_tick_executor(
                license_gate={"license_decision": "NO_BOUNDED_TICK_LICENSE"},
                raw_state_path=raw_state,
                evidence_path=evidence,
                output_dir=output_dir,
            )
            self.assertFalse(receipt.tick_invoked)
            self.assertFalse(receipt.grants_execution_authority)
            self.assertFalse((output_dir / "run_manifest_v0_1.json").exists())

    def test_granted_license_invokes_one_bounded_state_io_tick(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_state = root / "raw_state.json"
            evidence = root / "evidence.json"
            output_dir = root / "out"
            raw_state.write_text(json.dumps({"qi_state": {}, "process_history": []}), encoding="utf-8")
            evidence.write_text(json.dumps({"evidence": []}), encoding="utf-8")
            receipt = run_qi_process_tensor_bounded_tick_executor(
                license_gate={
                    "gate_status": "QI_PROCESS_TENSOR_REENTRY_LICENSE_GRANTED",
                    "license_decision": "BOUNDED_TICK_LICENSE_GRANTED",
                    "bounded_tick_license": True,
                    "may_invoke_next_tick": True,
                    "licensed_max_steps_per_tick": 1,
                },
                raw_state_path=raw_state,
                evidence_path=evidence,
                output_dir=output_dir,
            )
            self.assertEqual(receipt.executor_status, "QI_PROCESS_TENSOR_BOUNDED_TICK_INVOKED")
            self.assertTrue(receipt.tick_invoked)
            self.assertTrue(receipt.grants_execution_authority)
            self.assertEqual(receipt.licensed_max_steps_per_tick, 1)
            self.assertTrue((output_dir / "run_manifest_v0_1.json").exists())
            self.assertTrue((output_dir / "next_raw_state_v0_1.json").exists())
            self.assertTrue((output_dir / "state_bundle_v0_1.json").exists())
            self.assertTrue((output_dir / "step_trace_v0_1.json").exists())
            self.assertIsNone(receipt.denied_reason)

    def test_granted_license_clamps_max_steps(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_state = root / "raw_state.json"
            evidence = root / "evidence.json"
            output_dir = root / "out"
            raw_state.write_text(json.dumps({"qi_state": {}, "process_history": []}), encoding="utf-8")
            evidence.write_text(json.dumps({"evidence": []}), encoding="utf-8")
            receipt = run_qi_process_tensor_bounded_tick_executor(
                license_gate={
                    "gate_status": "QI_PROCESS_TENSOR_REENTRY_LICENSE_GRANTED",
                    "license_decision": "BOUNDED_TICK_LICENSE_GRANTED",
                    "bounded_tick_license": True,
                    "may_invoke_next_tick": True,
                    "licensed_max_steps_per_tick": 1000,
                },
                raw_state_path=raw_state,
                evidence_path=evidence,
                output_dir=output_dir,
            )
            self.assertEqual(receipt.licensed_max_steps_per_tick, 25)


if __name__ == "__main__":
    unittest.main()
