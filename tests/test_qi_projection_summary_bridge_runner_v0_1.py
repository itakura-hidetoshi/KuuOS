import json
import tempfile
import unittest
from pathlib import Path

from runtime.kuuos_runtime_daemon_v0_1 import run_runtime_daemon
from runtime.kuuos_runtime_daemon_qi_projection_summary_bridge_runner_v0_1 import run_qi_projection_summary_bridge

PROCESS_HISTORY = [
    {"step_id": "p0", "transition_visible": True, "memory_link_visible": True, "nonmarkov_link_visible": False},
    {"step_id": "p1", "transition_visible": True, "memory_link_visible": True, "nonmarkov_link_visible": True},
    {"step_id": "p2", "transition_visible": True, "memory_link_visible": True, "nonmarkov_link_visible": True},
]

RAW = {
    "cycle_id": "projection-bridge-001",
    "next_cycle_id": "projection-bridge-002",
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


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class QiProjectionSummaryBridgeRunnerTests(unittest.TestCase):
    def test_bridge_writes_projection_outputs_and_refreshes_operational_summary(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_path = root / "raw.json"
            evidence_path = root / "evidence.json"
            daemon_dir = root / "daemon"
            dispatch_dir = root / "dispatch"
            dump(raw_path, RAW)
            dump(evidence_path, EVIDENCE)
            run_runtime_daemon(
                raw_state_path=raw_path,
                evidence_path=evidence_path,
                daemon_dir=daemon_dir,
                max_ticks=1,
                max_steps_per_tick=1,
                sleep_seconds=0,
            )
            result = run_qi_projection_summary_bridge(daemon_dir=daemon_dir, dispatch_dir=dispatch_dir)
            self.assertEqual(result.bridge_status, "QI_PROJECTION_SUMMARY_BRIDGE_COMPILED")
            self.assertTrue(Path(result.projection_writer_result_path).is_file())
            self.assertTrue(Path(result.refreshed_operational_summary_path).is_file())
            self.assertTrue(Path(result.recoverability_projection_path).is_file())
            self.assertTrue(Path(result.health_projection_path).is_file())
            self.assertTrue(Path(result.observation_debt_schedule_path).is_file())
            self.assertTrue(Path(result.trace_compaction_plan_path).is_file())
            projection = load(Path(result.projection_writer_result_path))
            summary = load(Path(result.refreshed_operational_summary_path))
            self.assertEqual(result.recoverability_status, projection["recoverability_status"])
            self.assertEqual(result.daemon_health_status, projection["daemon_health_status"])
            self.assertEqual(result.observation_debt_status, projection["observation_debt_status"])
            self.assertEqual(result.compaction_plan_status, projection["compaction_plan_status"])
            self.assertEqual(summary["health_projection_status"], "QI_PROCESS_TENSOR_HEALTH_PROJECTED_WITH_RECOVERABILITY")
            self.assertEqual(summary["recoverability_projection_status"], "QI_PROCESS_TENSOR_RECOVERABILITY_PROJECTED")
            self.assertEqual(summary["observation_debt_status"], "QI_PROCESS_TENSOR_OBSERVATION_DEBT_SCHEDULED")
            self.assertEqual(summary["trace_compaction_status"], "QI_PROCESS_TENSOR_TRACE_COMPACTION_PLANNED")
            self.assertEqual(summary["recommended_next_runtime_mode"], result.recommended_next_runtime_mode)
            self.assertTrue(result.bridge_only)
            self.assertTrue(result.read_only)
            self.assertFalse(result.grants_execution_authority)
            self.assertFalse(result.grants_next_tick_execution_authority)


if __name__ == "__main__":
    unittest.main()
