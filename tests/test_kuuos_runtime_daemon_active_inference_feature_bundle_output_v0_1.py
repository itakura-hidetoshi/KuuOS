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
    "cycle_id": "feature-bundle-001",
    "next_cycle_id": "feature-bundle-002",
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


class DaemonFeatureBundleOutputTests(unittest.TestCase):
    def test_daemon_writes_feature_bundle_and_kernel_reads_it(self):
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

            bundle_path = daemon_dir / "daemon_active_inference_feature_bundle_v0_1.json"
            kernel_path = daemon_dir / "daemon_active_inference_kernel_result_v0_1.json"
            self.assertTrue(bundle_path.is_file())
            self.assertTrue(kernel_path.is_file())

            bundle = load(bundle_path)
            kernel = load(kernel_path)
            daemon_result = load(daemon_dir / "daemon_result_v0_1.json")

            self.assertEqual(bundle["compiler_status"], "FEATURES_COMPILED_WITH_PRIMARY_QI")
            self.assertIn("active_inference_inputs", bundle)
            self.assertIn("optional_lenses", bundle)
            self.assertIn("hard_constraints", bundle)
            self.assertIn("preference_priors", bundle)
            self.assertEqual(kernel["source_summary"]["qi_policy_mode"], bundle["active_inference_inputs"]["qi_policy_mode"])
            self.assertEqual(daemon_result["active_inference_feature_bundle_path"], str(bundle_path))
            self.assertEqual(daemon_result["active_inference_selected_policy"], kernel["selected_policy"])
            self.assertFalse(bundle["grants_execution_authority"])
            self.assertFalse(kernel["grants_execution_authority"])


if __name__ == "__main__":
    unittest.main()
