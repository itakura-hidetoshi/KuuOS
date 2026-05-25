import json
import tempfile
import unittest
from pathlib import Path

from runtime.kuuos_runtime_daemon_qi_supervised_loop_runner_v0_1 import run_qi_supervised_loop

PROCESS_HISTORY = [
    {"step_id": "p0", "transition_visible": True, "memory_link_visible": True, "nonmarkov_link_visible": False},
    {"step_id": "p1", "transition_visible": True, "memory_link_visible": True, "nonmarkov_link_visible": True},
    {"step_id": "p2", "transition_visible": True, "memory_link_visible": True, "nonmarkov_link_visible": True},
]

RAW = {
    "cycle_id": "supervised-loop-001",
    "next_cycle_id": "supervised-loop-002",
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


class QiSupervisedLoopRunnerTests(unittest.TestCase):
    def test_supervised_loop_is_bounded_and_writes_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_path = root / "raw.json"
            evidence_path = root / "evidence.json"
            out_dir = root / "loop"
            dump(raw_path, RAW)
            dump(evidence_path, EVIDENCE)
            result = run_qi_supervised_loop(
                raw_state_path=raw_path,
                evidence_path=evidence_path,
                out_dir=out_dir,
                max_cycles=2,
                max_daemon_ticks=1,
                max_steps_per_tick=1,
                requested_max_reentry_cycles=1,
            )
            self.assertEqual(result.loop_status, "QI_SUPERVISED_LOOP_COMPLETED")
            self.assertGreaterEqual(result.cycles_run, 1)
            self.assertLessEqual(result.cycles_run, 2)
            self.assertEqual(result.max_cycles, 2)
            self.assertTrue(Path(result.loop_manifest_path).is_file())
            self.assertTrue(result.supervised_loop_only)
            self.assertTrue(result.bounded)
            self.assertTrue(result.read_only)
            self.assertFalse(result.grants_execution_authority)
            self.assertFalse(result.grants_next_tick_execution_authority)
            self.assertIn(result.final_stop_reason, {
                "max_cycles_reached",
                "hold_reobserve_requested",
                "successor_raw_state_missing",
                "successor_raw_state_not_found",
                "successor_raw_state_unchanged",
            })
            for record in result.cycle_records:
                self.assertTrue(Path(record["routed_projection_plan_result_path"]).is_file())
                self.assertTrue(Path(record["readable_summary_path"]).is_file())
                self.assertIn("recoverability", record["projection_statuses"])
                self.assertIn("health", record["projection_statuses"])
                self.assertIn("observation_debt", record["projection_statuses"])
                self.assertIn("trace_compaction", record["projection_statuses"])

    def test_supervised_loop_rejects_zero_max_cycles(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_path = root / "raw.json"
            evidence_path = root / "evidence.json"
            dump(raw_path, RAW)
            dump(evidence_path, EVIDENCE)
            with self.assertRaises(ValueError):
                run_qi_supervised_loop(
                    raw_state_path=raw_path,
                    evidence_path=evidence_path,
                    out_dir=root / "loop",
                    max_cycles=0,
                )


if __name__ == "__main__":
    unittest.main()
