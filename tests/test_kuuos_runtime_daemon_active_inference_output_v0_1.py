import json
import tempfile
import unittest
from pathlib import Path

from runtime.kuuos_runtime_daemon_v0_1 import run_runtime_daemon

PROCESS_HISTORY = [
    {"step_id": "p0", "transition_visible": True, "memory_link_visible": True, "nonmarkov_link_visible": False},
    {"step_id": "p1", "transition_visible": True, "memory_link_visible": False, "nonmarkov_link_visible": False},
    {"step_id": "p2", "transition_visible": True, "memory_link_visible": False, "nonmarkov_link_visible": True},
]

RAW = {
    "cycle_id": "active-output-001",
    "next_cycle_id": "active-output-002",
    "generated_at_utc": "2026-05-23T00:00:00+00:00",
    "dispatched_at_utc": "2026-05-23T00:00:01+00:00",
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
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class DaemonActiveInferenceOutputTests(unittest.TestCase):
    def test_daemon_writes_active_inference_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_path = root / "raw.json"
            evidence_path = root / "evidence.json"
            daemon_dir = root / "daemon"
            dump(raw_path, RAW)
            dump(evidence_path, EVIDENCE)

            result = run_runtime_daemon(
                raw_state_path=raw_path,
                evidence_path=evidence_path,
                daemon_dir=daemon_dir,
                max_ticks=2,
                max_steps_per_tick=1,
                sleep_seconds=0,
            )

            self.assertTrue(Path(result.active_inference_kernel_result_path).is_file())
            self.assertEqual(result.active_inference_selected_policy, "CONTINUE_HARMONIZED")
            self.assertIsInstance(result.active_inference_expected_free_energy, float)
            self.assertIsInstance(result.active_inference_posterior_precision, float)

            daemon_result = load(daemon_dir / "daemon_result_v0_1.json")
            active_result = load(Path(result.active_inference_kernel_result_path))
            self.assertEqual(daemon_result["active_inference_kernel_result_path"], result.active_inference_kernel_result_path)
            self.assertEqual(daemon_result["active_inference_selected_policy"], "CONTINUE_HARMONIZED")
            self.assertEqual(active_result["selected_policy"], "CONTINUE_HARMONIZED")
            self.assertIn("policy_free_energy_table", active_result)
            self.assertIn("posterior_belief_state", active_result)
            self.assertFalse(active_result["grants_execution_authority"])
            self.assertFalse(daemon_result["grants_execution_authority"])


if __name__ == "__main__":
    unittest.main()
