import json
import tempfile
import unittest
from pathlib import Path

from runtime.kuuos_state_io_runner_v0_1 import run_state_io

RAW = {
    "cycle_id": "io-001",
    "next_cycle_id": "io-002",
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
    "process_tensor_visible": True,
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


def dump(path, payload):
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


class StateIORunnerTests(unittest.TestCase):
    def test_writes_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_path = root / "raw.json"
            ev_path = root / "evidence.json"
            out = root / "out"
            dump(raw_path, RAW)
            dump(ev_path, EVIDENCE)
            manifest = run_state_io(raw_state_path=raw_path, evidence_path=ev_path, output_dir=out, max_steps=2)
            self.assertEqual(manifest.stop_reason, "MAX_STEPS_REACHED")
            self.assertTrue((out / "kuuos_driver_result_v0_1.json").is_file())
            self.assertTrue((out / "next_raw_state_v0_1.json").is_file())
            self.assertTrue((out / "state_bundle_v0_1.json").is_file())
            self.assertTrue((out / "step_trace_v0_1.json").is_file())
            self.assertTrue((out / "run_manifest_v0_1.json").is_file())
            self.assertEqual(len(load(out / "step_trace_v0_1.json")), 2)
            self.assertFalse(load(out / "state_bundle_v0_1.json")["grants_execution_authority"])

    def test_accepts_existing_bundle(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_path = root / "raw.json"
            ev_path = root / "evidence.json"
            dump(raw_path, RAW)
            dump(ev_path, EVIDENCE)
            first = run_state_io(raw_state_path=raw_path, evidence_path=ev_path, output_dir=root / "out1", max_steps=1)
            next_raw = load(Path(first.next_raw_state_path))
            next_raw["next_cycle_id"] = "io-003"
            raw2 = root / "raw2.json"
            dump(raw2, next_raw)
            second = run_state_io(raw_state_path=raw2, evidence_path=ev_path, output_dir=root / "out2", max_steps=1, state_bundle_path=Path(first.state_bundle_path))
            self.assertEqual(len(load(Path(second.state_bundle_path))["loop_log"]), 2)


if __name__ == "__main__":
    unittest.main()
