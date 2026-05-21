import json
import tempfile
import unittest
from pathlib import Path

from runtime.kuuos_runtime_daemon_v0_1 import run_runtime_daemon
from runtime.kuuos_runtime_daemon_status_v0_1 import read_runtime_daemon_status

RAW = {
    "cycle_id": "status-001",
    "next_cycle_id": "status-002",
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
    "process_history": [
        {"transition_visible": True, "memory_link_visible": True, "nonmarkov_link_visible": False},
        {"transition_visible": True, "memory_link_visible": False, "nonmarkov_link_visible": False},
        {"transition_visible": True, "memory_link_visible": False, "nonmarkov_link_visible": True}
    ],
    "barrier_witness_visible": True,
    "receipt_hash": True,
    "support_refs": True,
    "registry_key": True,
    "view_delivery_receipt": True,
    "channel_scope": True,
    "acknowledgment_marker": True
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
    "hold_review_evidence": True
}


def dump(path, payload):
    path.write_text(json.dumps(payload), encoding="utf-8")


class RuntimeDaemonStatusTests(unittest.TestCase):
    def test_reads_latest_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw = root / "raw.json"
            ev = root / "ev.json"
            out = root / "out"
            dump(raw, RAW)
            dump(ev, EVIDENCE)
            run_runtime_daemon(raw_state_path=raw, evidence_path=ev, daemon_dir=out, max_ticks=2, max_steps_per_tick=1)
            status = read_runtime_daemon_status(out)
            self.assertEqual(status.status, "DAEMON_STATUS_READY")
            self.assertEqual(status.stop_reason, "MAX_TICKS_REACHED")
            self.assertEqual(status.ticks_run, 2)
            self.assertEqual(status.latest_tick_index, 1)
            self.assertEqual(status.missing_files, [])
            self.assertTrue(Path(status.latest_step_trace_path).is_file())
            summary = status.latest_qi_process_tensor_summary
            self.assertTrue(summary["process_tensor_visible"])
            self.assertEqual(summary["process_history_length"], 3)
            self.assertFalse(status.grants_execution_authority)

    def test_missing_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "missing"
            status = read_runtime_daemon_status(missing)
            self.assertEqual(status.status, "DAEMON_DIR_MISSING")
            self.assertIn(str(missing), status.missing_files)


if __name__ == "__main__":
    unittest.main()
