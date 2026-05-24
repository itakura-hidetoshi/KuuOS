import json
import tempfile
import unittest
from pathlib import Path

from runtime.kuuos_runtime_daemon_qi_managed_daemon_cycle_runner_v0_1 import run_qi_managed_daemon_cycle

PROCESS_HISTORY = [
    {"step_id": "p0", "transition_visible": True, "memory_link_visible": True, "nonmarkov_link_visible": False},
    {"step_id": "p1", "transition_visible": True, "memory_link_visible": True, "nonmarkov_link_visible": True},
    {"step_id": "p2", "transition_visible": True, "memory_link_visible": True, "nonmarkov_link_visible": True},
]

RAW = {
    "cycle_id": "managed-daemon-001",
    "next_cycle_id": "managed-daemon-002",
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
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class QiManagedDaemonCycleRunnerTests(unittest.TestCase):
    def test_managed_daemon_cycle_returns_daemon_and_chain_summary(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_path = root / "raw.json"
            evidence_path = root / "evidence.json"
            daemon_dir = root / "daemon"
            chain_dir = root / "managed_chain"
            dump(raw_path, RAW)
            dump(evidence_path, EVIDENCE)
            result = run_qi_managed_daemon_cycle(
                raw_state_path=raw_path,
                evidence_path=evidence_path,
                daemon_dir=daemon_dir,
                chain_dir=chain_dir,
                max_daemon_ticks=1,
                max_steps_per_tick=1,
                requested_max_reentry_cycles=2,
                refresh_before_first_reentry=True,
                refresh_after_each_reentry=True,
            )
            self.assertIn(result.cycle_status, {
                "QI_MANAGED_DAEMON_CYCLE_REENTRY_INVOKED",
                "QI_MANAGED_DAEMON_CYCLE_REENTRY_STOPPED",
                "QI_MANAGED_DAEMON_CYCLE_DAEMON_ONLY",
            })
            self.assertTrue(Path(result.daemon_result_path).is_file())
            self.assertTrue(Path(result.daemon_health_projection_path).is_file())
            self.assertTrue(Path(result.managed_chain_result_path).is_file())
            self.assertTrue(Path(result.final_raw_state_path).is_file())
            self.assertTrue(Path(result.final_state_bundle_path).is_file())
            self.assertEqual(result.daemon_ticks_run, 1)
            self.assertIsNotNone(result.daemon_health_status)
            self.assertIsNotNone(result.daemon_recoverability_status)
            self.assertIsNotNone(result.controller_decision)
            managed_chain = load(Path(result.managed_chain_result_path))
            daemon_result = load(Path(result.daemon_result_path))
            self.assertEqual(managed_chain["controller_decision"], result.controller_decision)
            self.assertEqual(daemon_result["daemon_health_status"], result.daemon_health_status)
            self.assertFalse(daemon_result["grants_truth_authority"])
            self.assertFalse(result.grants_truth_authority)

    def test_managed_daemon_cycle_respects_requested_reentry_cap(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_path = root / "raw.json"
            evidence_path = root / "evidence.json"
            daemon_dir = root / "daemon"
            chain_dir = root / "managed_chain"
            dump(raw_path, RAW)
            dump(evidence_path, EVIDENCE)
            result = run_qi_managed_daemon_cycle(
                raw_state_path=raw_path,
                evidence_path=evidence_path,
                daemon_dir=daemon_dir,
                chain_dir=chain_dir,
                max_daemon_ticks=1,
                max_steps_per_tick=1,
                requested_max_reentry_cycles=1,
                refresh_before_first_reentry=True,
                refresh_after_each_reentry=True,
            )
            self.assertLessEqual(result.allowed_max_cycles, 1)
            self.assertLessEqual(result.reentry_cycles_run, 1)
            self.assertLessEqual(result.reentry_ticks_invoked, 1)


if __name__ == "__main__":
    unittest.main()
