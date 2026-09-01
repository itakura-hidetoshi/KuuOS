#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "runtime" / "kuuos_openclaw_audit_observation_ingest_v0_3.py"
SPEC = importlib.util.spec_from_file_location("kuuos_openclaw_audit_observation_ingest_v0_3", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


def sample_event(sequence: int = 7, event_id: str = "evt-7") -> dict:
    return {
        "eventType": "tool_action",
        "schemaVersion": 1,
        "eventId": event_id,
        "sequence": sequence,
        "sourceSequence": sequence,
        "occurredAt": 1_800_000_000_000,
        "kind": "tool_action",
        "action": "tool.action.finished",
        "status": "succeeded",
        "actor": {"kind": "agent", "id": "agent-main"},
        "redaction": "metadata_only",
        "agentId": "main",
        "runId": "run-1",
        "sessionKey": "telegram:private-peer-id",
        "sessionId": "session-private-id",
        "toolCallId": "tool-fingerprint",
        "toolName": "read",
        "prompt": "must never persist",
        "toolArgs": {"path": "/secret"},
        "result": "must never persist",
    }


class OpenClawAuditObservationIngestTests(unittest.TestCase):
    def test_projection_is_allowlisted_and_identity_context_is_hashed(self) -> None:
        event = sample_event()
        projected = mod.project_event(event)
        self.assertEqual(projected["eventId"], "evt-7")
        self.assertEqual(projected["toolName"], "read")
        self.assertNotIn("actor", projected)
        self.assertNotIn("sessionKey", projected)
        self.assertNotIn("sessionId", projected)
        self.assertNotIn("prompt", projected)
        self.assertNotIn("toolArgs", projected)
        self.assertNotIn("result", projected)
        self.assertIn("actorDigest", projected)
        self.assertIn("sessionKeyDigest", projected)
        self.assertIn("sessionIdDigest", projected)
        self.assertEqual(projected["sourceEventDigest"], mod.digest(event))

    def test_non_metadata_only_event_is_rejected(self) -> None:
        event = sample_event()
        event["redaction"] = "full"
        with self.assertRaises(RuntimeError):
            mod.project_event(event)

    def test_append_only_candidate_dedup_source_can_be_recovered(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            ledger = mod.ObservationLedger(Path(directory))
            first = ledger.append_candidate(sample_event(), "query-digest")
            self.assertFalse(first["semantics"]["observeCommitPerformed"])
            self.assertFalse(first["semantics"]["truthPromotionAuthority"])
            self.assertFalse(first["semantics"]["automaticPlanCompletion"])
            self.assertFalse(first["semantics"]["automaticRollback"])
            self.assertEqual(ledger.seen_event_ids(), {"evt-7"})

            raw = json.loads(ledger.path.read_text(encoding="utf-8").strip())
            self.assertEqual(raw["event"]["eventId"], "evt-7")
            self.assertNotIn("prompt", raw["event"])

    def test_checkpoint_round_trip_preserves_non_authoritative_pagination_state(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = mod.CheckpointStore(Path(directory))
            state = store.load()
            qdigest = mod.query_digest({"kind": "tool_action"})
            entry = mod._entry_for(state, qdigest)
            entry["maxSequence"] = 10
            entry["resumeCursor"] = "cursor-1"
            entry["catchupHighWaterSequence"] = 25
            store.save(state)

            recovered = store.load()
            recovered_entry = mod._entry_for(recovered, qdigest)
            self.assertEqual(recovered_entry["maxSequence"], 10)
            self.assertEqual(recovered_entry["resumeCursor"], "cursor-1")
            self.assertEqual(recovered_entry["catchupHighWaterSequence"], 25)


if __name__ == "__main__":
    unittest.main()
