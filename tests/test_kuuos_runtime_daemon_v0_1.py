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
    "cycle_id": "daemon-001",
    "next_cycle_id": "daemon-002",
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


class KuuOSRuntimeDaemonTests(unittest.TestCase):
    def test_daemon_runs_until_max_ticks(self):
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
            self.assertEqual(result.daemon_status, "DAEMON_MAX_TICKS_REACHED_APPEND_ONLY")
            self.assertEqual(result.stop_reason, "MAX_TICKS_REACHED")
            self.assertEqual(result.ticks_run, 2)
            self.assertTrue(Path(result.tick_log_path).is_file())
            self.assertTrue(Path(result.final_raw_state_path).is_file())
            self.assertTrue(Path(result.final_state_bundle_path).is_file())
            self.assertTrue(Path(result.qi_policy_result_path).is_file())
            self.assertTrue(Path(result.emptiness_gate_result_path).is_file())
            self.assertEqual(result.qi_policy_recommended_tick_mode, "CONTINUE_WITH_QI_MEMORY_MONITOR")
            self.assertEqual(result.emptiness_recommended_action, "CONTINUE_ADVISORY_ONLY")
            tick_log = load(Path(result.tick_log_path))
            self.assertEqual(len(tick_log), 2)
            self.assertFalse(tick_log[0]["grants_execution_authority"])
            daemon_result = load(daemon_dir / "daemon_result_v0_1.json")
            policy_result = load(Path(result.qi_policy_result_path))
            emptiness_result = load(Path(result.emptiness_gate_result_path))
            self.assertEqual(daemon_result["qi_policy_recommended_tick_mode"], "CONTINUE_WITH_QI_MEMORY_MONITOR")
            self.assertEqual(daemon_result["emptiness_recommended_action"], "CONTINUE_ADVISORY_ONLY")
            self.assertEqual(policy_result["recommended_tick_mode"], "CONTINUE_WITH_QI_MEMORY_MONITOR")
            self.assertEqual(emptiness_result["recommended_emptiness_action"], "CONTINUE_ADVISORY_ONLY")
            self.assertTrue(emptiness_result["non_reification_assertions"]["policy_hint_is_not_command"])
            self.assertFalse(policy_result["grants_execution_authority"])
            self.assertFalse(emptiness_result["grants_execution_authority"])
            self.assertFalse(daemon_result["grants_truth_authority"])

    def test_daemon_stops_on_waiting(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw = dict(RAW)
            raw["physical_process_visible"] = False
            raw["thermodynamic_activity_visible"] = False
            raw["process_history"] = []
            evidence = dict(EVIDENCE)
            evidence["value_witness_receipt"] = False
            raw_path = root / "raw.json"
            evidence_path = root / "evidence.json"
            dump(raw_path, raw)
            dump(evidence_path, evidence)
            result = run_runtime_daemon(
                raw_state_path=raw_path,
                evidence_path=evidence_path,
                daemon_dir=root / "daemon",
                max_ticks=5,
                max_steps_per_tick=1,
            )
            self.assertEqual(result.daemon_status, "DAEMON_WAITING_APPEND_ONLY")
            self.assertEqual(result.stop_reason, "WAITING_FOR_MORE_EVIDENCE")
            self.assertEqual(result.ticks_run, 1)
            self.assertEqual(result.qi_policy_recommended_tick_mode, "REQUEST_MORE_EVIDENCE")
            self.assertEqual(result.emptiness_recommended_action, "REOBSERVE_WITH_NON_REIFICATION")

    def test_daemon_stops_on_quarantine(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw = dict(RAW)
            raw["world_identity_blocker"] = False
            raw_path = root / "raw.json"
            evidence_path = root / "evidence.json"
            dump(raw_path, raw)
            dump(evidence_path, EVIDENCE)
            result = run_runtime_daemon(
                raw_state_path=raw_path,
                evidence_path=evidence_path,
                daemon_dir=root / "daemon",
                max_ticks=5,
                max_steps_per_tick=1,
            )
            self.assertEqual(result.daemon_status, "DAEMON_QUARANTINE_RETAINED_APPEND_ONLY")
            self.assertEqual(result.stop_reason, "QUARANTINE_RETAINED")
            self.assertEqual(result.ticks_run, 1)
            self.assertEqual(result.qi_policy_recommended_tick_mode, "QUARANTINE_REVIEW")
            self.assertEqual(result.emptiness_recommended_action, "HOLD_OR_QUARANTINE_NONFINAL")

    def test_daemon_caps_tick_and_step_bounds(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_path = root / "raw.json"
            evidence_path = root / "evidence.json"
            dump(raw_path, RAW)
            dump(evidence_path, EVIDENCE)
            result = run_runtime_daemon(
                raw_state_path=raw_path,
                evidence_path=evidence_path,
                daemon_dir=root / "daemon",
                max_ticks=0,
                max_steps_per_tick=0,
            )
            self.assertEqual(result.ticks_run, 1)
            self.assertTrue(Path(result.qi_policy_result_path).is_file())
            self.assertTrue(Path(result.emptiness_gate_result_path).is_file())


if __name__ == "__main__":
    unittest.main()
