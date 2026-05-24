import json
import tempfile
import unittest
from pathlib import Path

from runtime.kuuos_runtime_daemon_qi_routed_cycle_projection_plan_runner_v0_1 import run_qi_routed_cycle_projection_plan

PROCESS_HISTORY = [
    {"step_id": "p0", "transition_visible": True, "memory_link_visible": True, "nonmarkov_link_visible": False},
    {"step_id": "p1", "transition_visible": True, "memory_link_visible": True, "nonmarkov_link_visible": True},
    {"step_id": "p2", "transition_visible": True, "memory_link_visible": True, "nonmarkov_link_visible": True},
]

RAW = {
    "cycle_id": "projection-plan-runner-001",
    "next_cycle_id": "projection-plan-runner-002",
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
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


class QiRoutedCycleProjectionPlanRunnerTests(unittest.TestCase):
    def test_runner_writes_routed_cycle_bridge_summary_and_plan(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_path = root / "raw.json"
            evidence_path = root / "evidence.json"
            daemon_dir = root / "daemon"
            dispatch_dir = root / "dispatch"
            dump(raw_path, RAW)
            dump(evidence_path, EVIDENCE)
            result = run_qi_routed_cycle_projection_plan(
                raw_state_path=raw_path,
                evidence_path=evidence_path,
                daemon_dir=daemon_dir,
                dispatch_dir=dispatch_dir,
                max_daemon_ticks=1,
                max_steps_per_tick=1,
                requested_max_reentry_cycles=1,
            )
            self.assertEqual(result.runner_status, "QI_ROUTED_CYCLE_PROJECTION_PLAN_COMPILED")
            self.assertTrue(Path(result.routed_cycle_result_path).is_file())
            self.assertTrue(Path(result.projection_plan_bridge_result_path).is_file())
            self.assertTrue(Path(result.qi_routed_cycle_operational_summary_path).is_file())
            self.assertTrue(Path(result.qi_next_runtime_mode_plan_path).is_file())
            self.assertIn("recoverability", result.projection_statuses)
            self.assertIn("health", result.projection_statuses)
            self.assertIn("observation_debt", result.projection_statuses)
            self.assertIn("trace_compaction", result.projection_statuses)
            self.assertIsInstance(result.required_pre_tick_actions, list)
            self.assertTrue(result.bridge_only)
            self.assertTrue(result.read_only)
            self.assertTrue(result.plan_only)
            self.assertFalse(result.grants_execution_authority)
            self.assertFalse(result.grants_next_tick_execution_authority)


if __name__ == "__main__":
    unittest.main()
