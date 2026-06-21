from __future__ import annotations

from pathlib import Path
import json
import tempfile
import unittest

from runtime.kuuos_open_ended_background_agency_entry_v0_30 import (
    commit_request,
    make_initial_state,
    make_request,
)
from runtime.kuuos_open_ended_background_agency_v0_30 import commit_request as core_commit_request


class OpenEndedBackgroundAgencyEntryV030Test(unittest.TestCase):
    def initial(self):
        return make_initial_state(
            agency_id="agency-entry-1",
            root_lineage_digest="c" * 64,
            created_at_ms=100,
        )

    def request(self, state, request_id, posture, at):
        return make_request(
            request_id=request_id,
            source_state_digest=state["body_digest"],
            action="SET_POSTURE",
            payload={"posture": posture},
            requested_at_ms=at,
        )

    def test_replay_repairs_source_snapshot_from_authoritative_ledger(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_path = Path(tmp) / "state.json"
            ledger_path = Path(tmp) / "ledger.jsonl"
            initial = self.initial()
            state_path.write_text(json.dumps(initial), encoding="utf-8")
            request = self.request(initial, "repair-1", "WAITING", 110)
            committed = core_commit_request(
                state_path=state_path,
                ledger_path=ledger_path,
                request_envelope=request,
                applied_at_ms=120,
            )
            state_path.write_text(json.dumps(initial), encoding="utf-8")
            replay = commit_request(
                state_path=state_path,
                ledger_path=ledger_path,
                request_envelope=request,
                applied_at_ms=130,
            )
            repaired = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual("REPLAYED_REPAIRED", replay.status)
            self.assertEqual(committed.state, repaired)
            self.assertEqual(1, len(ledger_path.read_text(encoding="utf-8").splitlines()))

    def test_request_id_cannot_be_reused_for_different_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_path = Path(tmp) / "state.json"
            ledger_path = Path(tmp) / "ledger.jsonl"
            initial = self.initial()
            state_path.write_text(json.dumps(initial), encoding="utf-8")
            first_request = self.request(initial, "stable-id", "WAITING", 110)
            first = commit_request(
                state_path=state_path,
                ledger_path=ledger_path,
                request_envelope=first_request,
                applied_at_ms=120,
            )
            different_request = self.request(first.state, "stable-id", "ACTIVE", 130)
            with self.assertRaisesRegex(ValueError, "request_id_reuse_with_different_content"):
                commit_request(
                    state_path=state_path,
                    ledger_path=ledger_path,
                    request_envelope=different_request,
                    applied_at_ms=140,
                )

    def test_old_replay_does_not_replace_a_later_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_path = Path(tmp) / "state.json"
            ledger_path = Path(tmp) / "ledger.jsonl"
            initial = self.initial()
            state_path.write_text(json.dumps(initial), encoding="utf-8")
            first_request = self.request(initial, "r1", "WAITING", 110)
            first = commit_request(
                state_path=state_path,
                ledger_path=ledger_path,
                request_envelope=first_request,
                applied_at_ms=120,
            )
            second_request = self.request(first.state, "r2", "ACTIVE", 130)
            second = commit_request(
                state_path=state_path,
                ledger_path=ledger_path,
                request_envelope=second_request,
                applied_at_ms=140,
            )
            replay = commit_request(
                state_path=state_path,
                ledger_path=ledger_path,
                request_envelope=first_request,
                applied_at_ms=150,
            )
            current = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual("REPLAYED_WITH_LATER_STATE", replay.status)
            self.assertEqual(second.state, replay.state)
            self.assertEqual(second.state, current)
            self.assertEqual(2, len(ledger_path.read_text(encoding="utf-8").splitlines()))


if __name__ == "__main__":
    unittest.main()
