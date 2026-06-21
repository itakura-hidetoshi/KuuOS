from __future__ import annotations

from pathlib import Path
import json
import tempfile
import unittest

from runtime.kuuos_open_ended_background_agency_v0_30 import (
    CORE_HORIZONS,
    apply_request,
    commit_request,
    make_initial_state,
    make_request,
    validate_state,
)


ROOT = "a" * 64


class OpenEndedBackgroundAgencyV030Test(unittest.TestCase):
    def initial(self):
        return make_initial_state(agency_id="agency-1", root_lineage_digest=ROOT, created_at_ms=100)

    def request(self, state, action, payload, request_id="r1", at=110):
        return make_request(
            request_id=request_id,
            source_state_digest=state["body_digest"],
            action=action,
            payload=payload,
            requested_at_ms=at,
        )

    def result_state(self, transition):
        return transition["body"]["result_state"]

    def test_initial_state_keeps_all_core_horizons_open_without_global_ceiling(self):
        state = self.initial()
        body = validate_state(state)
        self.assertEqual(set(CORE_HORIZONS), set(body["constitutional_horizons"]))
        self.assertTrue(all(value == "OPEN" for value in body["constitutional_horizons"].values()))
        self.assertNotIn("max_total_cycles", body)
        self.assertNotIn("max_goal_depth", body)
        self.assertTrue(body["successor_possibility_open"])

    def test_expansion_candidate_is_not_authority(self):
        state = self.initial()
        request = self.request(state, "PROPOSE_EXPANSION", {
            "candidate_id": "goal-1",
            "dimension": "goal_formation",
            "description": "Form a new mission candidate from unresolved world evidence",
            "evidence_refs": ["obs:1"],
            "requested_capabilities": ["observe"],
        })
        result = self.result_state(apply_request(state, request, applied_at_ms=120))
        candidate = result["body"]["candidate_expansions"][0]
        self.assertEqual("CANDIDATE", candidate["status"])
        self.assertFalse(candidate["grants_execution_authority"])
        self.assertFalse(result["body"]["grants_execution_authority"])
        self.assertEqual("OPEN", result["body"]["constitutional_horizons"]["goal_formation"])

    def test_local_hold_cannot_close_constitutional_horizon(self):
        state = self.initial()
        request = self.request(state, "LOCAL_HOLD", {
            "control_id": "hold-1",
            "scope_kind": "connector",
            "scope_id": "github",
            "reason": "credential rotation",
            "expires_at_ms": 500,
        })
        result = self.result_state(apply_request(state, request, applied_at_ms=120))
        body = result["body"]
        self.assertEqual("PAUSED", body["background_posture"])
        self.assertTrue(all(value == "OPEN" for value in body["constitutional_horizons"].values()))
        self.assertEqual("NONE", body["local_controls"][0]["constitutional_effect"])
        self.assertFalse(body["local_controls"][0]["closes_horizon"])

    def test_defer_and_admit_preserve_possibility_and_add_no_authority(self):
        state = self.initial()
        proposal = self.request(state, "PROPOSE_EXPANSION", {
            "candidate_id": "tool-1",
            "dimension": "tool_creation",
            "description": "Create a new validated observation tool",
        })
        state = self.result_state(apply_request(state, proposal, applied_at_ms=120))
        defer = self.request(state, "DEFER_CANDIDATE", {"candidate_id": "tool-1"}, "r2", 130)
        state = self.result_state(apply_request(state, defer, applied_at_ms=140))
        self.assertEqual("DEFERRED", state["body"]["candidate_expansions"][0]["status"])
        admit = self.request(state, "ADMIT_CANDIDATE", {"candidate_id": "tool-1"}, "r3", 150)
        state = self.result_state(apply_request(state, admit, applied_at_ms=160))
        self.assertEqual("ADMITTED", state["body"]["candidate_expansions"][0]["status"])
        self.assertFalse(state["body"]["candidate_expansions"][0]["grants_execution_authority"])
        self.assertEqual("OPEN", state["body"]["constitutional_horizons"]["tool_creation"])

    def test_contraction_and_global_ceiling_actions_are_rejected(self):
        for index, action in enumerate(("CLOSE_HORIZON", "SET_GLOBAL_LIMIT", "SELF_AUTHORIZE_EXECUTION")):
            state = self.initial()
            request = self.request(state, action, {}, request_id=f"r{index}")
            with self.assertRaisesRegex(ValueError, "constitutional_contraction_rejected"):
                apply_request(state, request, applied_at_ms=120)

    def test_termination_of_instance_does_not_close_successor_possibility(self):
        state = self.initial()
        request = self.request(state, "TERMINATE_INSTANCE", {})
        result = self.result_state(apply_request(state, request, applied_at_ms=120))
        body = result["body"]
        self.assertEqual("TERMINATED", body["background_posture"])
        self.assertTrue(body["instance_terminated"])
        self.assertTrue(body["successor_possibility_open"])
        self.assertTrue(all(value == "OPEN" for value in body["constitutional_horizons"].values()))

    def test_additive_new_horizon_is_allowed(self):
        state = self.initial()
        request = self.request(state, "ADD_OPEN_HORIZON", {"name": "new_scientific_language_creation"})
        result = self.result_state(apply_request(state, request, applied_at_ms=120))
        self.assertEqual("OPEN", result["body"]["constitutional_horizons"]["new_scientific_language_creation"])

    def test_stale_state_and_tampering_are_rejected(self):
        state = self.initial()
        request = self.request(state, "SET_POSTURE", {"posture": "WAITING"})
        next_state = self.result_state(apply_request(state, request, applied_at_ms=120))
        with self.assertRaisesRegex(ValueError, "stale_source_state"):
            apply_request(next_state, request, applied_at_ms=130)
        tampered = json.loads(json.dumps(state))
        tampered["body"]["constitutional_horizons"]["goal_formation"] = "CLOSED"
        with self.assertRaisesRegex(ValueError, "digest_mismatch"):
            validate_state(tampered)

    def test_commit_is_append_only_and_exact_replay_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_path = Path(tmp) / "state.json"
            ledger_path = Path(tmp) / "ledger.jsonl"
            state = self.initial()
            state_path.write_text(json.dumps(state), encoding="utf-8")
            request = self.request(state, "SET_POSTURE", {"posture": "WAITING"})
            first = commit_request(
                state_path=state_path,
                ledger_path=ledger_path,
                request_envelope=request,
                applied_at_ms=120,
            )
            second = commit_request(
                state_path=state_path,
                ledger_path=ledger_path,
                request_envelope=request,
                applied_at_ms=130,
            )
            self.assertEqual("COMMITTED", first.status)
            self.assertEqual("REPLAYED", second.status)
            self.assertEqual(1, first.ledger_entries)
            self.assertEqual(1, second.ledger_entries)
            self.assertEqual(1, len(ledger_path.read_text(encoding="utf-8").splitlines()))
            self.assertEqual(first.transition, second.transition)


if __name__ == "__main__":
    unittest.main()
