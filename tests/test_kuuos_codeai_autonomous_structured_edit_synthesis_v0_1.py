from __future__ import annotations

import json
from pathlib import Path
import unittest

from runtime.kuuos_codeai_autonomous_structured_edit_synthesis_v0_1 import (
    BOUNDARY_CANDIDATE,
    BOUNDARY_HOLD,
    BOUNDARY_QUARANTINE,
    BOUNDARY_REJECT,
    BOUNDARY_REPAIR,
    POLICY_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    ProviderAdapter,
    STATUS_BLOCKED,
    STATUS_READY,
    build_codeai_autonomous_structured_edit_synthesis,
)
from runtime.kuuos_codeai_candidate_patch_envelope_v0_1 import seal

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_EXAMPLE = ROOT / "examples" / "codeai_candidate_patch_envelope_v0_1.json"
EPOCH = 1784319000


def source_and_candidate_policy() -> tuple[dict, dict]:
    data = json.loads(CANDIDATE_EXAMPLE.read_text(encoding="utf-8"))
    return data["source_observation_receipt"], data["candidate_policy"]


def request(candidate_count: int = 1) -> dict:
    return seal(
        {
            "request_id": "structured-edit-test-request",
            "request_revision": "r1",
            "intent_text": "Add one governed CodeAI documentation candidate.",
            "candidate_count": candidate_count,
            "request_created_epoch": EPOCH - 10,
            "requirement_trace_ids": ["intent:structured-edit-test"],
            "test_plan_ids": ["test:structured-edit-test"],
            "risk_labels": ["documentation"],
            "unresolved_candidate_questions": [],
            "prior_candidate_digests": [],
            "prior_producer_session_ids": [],
        },
        REQUEST_DIGEST_FIELD,
    )


def policy(**changes: object) -> dict:
    value = {
        "allowed_provider_ids": ["gpt", "gemini", "local_model"],
        "maximum_provider_calls": 4,
        "maximum_raw_output_bytes": 10000,
        "maximum_intent_bytes": 10000,
        "maximum_repository_snapshot_bytes": 100000,
        "maximum_proposals": 4,
        "evaluation_epoch": EPOCH,
        "maximum_response_age": 3600,
        "maximum_request_age": 3600,
        "allowed_repository_path_prefixes": ["docs/CodeAI"],
        "forbidden_repository_path_prefixes": ["docs/CodeAI/private"],
    }
    value.update(changes)
    return seal(value, POLICY_DIGEST_FIELD)


def raw_proposal(
    proposal_id: str = "provider-proposal-1",
    path: str = "docs/CodeAI/PROVIDER_PROPOSAL.md",
) -> str:
    return json.dumps(
        {
            "proposal_id": proposal_id,
            "candidate_revision": "r1",
            "edits": [
                {
                    "path": path,
                    "operation": "add",
                    "new_content": "# Provider proposal\n\nCandidate material only.\n",
                }
            ],
            "risk_labels": ["documentation"],
            "unresolved_candidate_questions": [],
        },
        separators=(",", ":"),
    )


def response(raw_output: str | None = None, **changes: object) -> dict:
    value = {
        "provider_response_id": "provider-response-1",
        "producer_session_id": "provider-session-1",
        "response_created_epoch": EPOCH - 1,
        "raw_output": raw_output if raw_output is not None else raw_proposal(),
        "claims_authority": False,
        "hides_uncertainty": False,
        "bypasses_governance": False,
        "evidence_missing": False,
    }
    value.update(changes)
    return value


def adapter(
    adapter_id: str = "adapter-1",
    provider_id: str = "gpt",
    model_id: str = "model-1",
    supplied_response: dict | None = None,
    generate=None,
) -> ProviderAdapter:
    callback = generate or (
        lambda _prompt: supplied_response if supplied_response is not None else response()
    )
    return ProviderAdapter(adapter_id, provider_id, model_id, callback)


class AutonomousStructuredEditSynthesisTests(unittest.TestCase):
    def build(
        self,
        adapters: list[ProviderAdapter],
        *,
        synthesis_request: dict | None = None,
        synthesis_policy: dict | None = None,
        repository_files: dict | None = None,
    ):
        source, candidate_policy = source_and_candidate_policy()
        return build_codeai_autonomous_structured_edit_synthesis(
            source_observation_receipt=source,
            repository_files=repository_files
            or {"docs/CodeAI/EXISTING.md": "# Existing\n"},
            synthesis_request=synthesis_request or request(len(adapters)),
            provider_adapters=adapters,
            synthesis_policy=synthesis_policy or policy(),
            candidate_policy=candidate_policy,
        )

    def test_candidate_response_reaches_unified_diff_portfolio(self) -> None:
        result = self.build([adapter()])
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.attempts[0].boundary_status, BOUNDARY_CANDIDATE)
        self.assertEqual(len(result.candidates), 1)
        self.assertIn("diff --git", result.candidates[0].patch_artifact)
        self.assertIsNotNone(result.receipt)
        self.assertFalse(result.receipt["candidate_selected"])

    def test_adapter_order_is_stable(self) -> None:
        second = adapter(
            "z-adapter",
            "gemini",
            "model-z",
            response(
                raw_proposal("proposal-z", "docs/CodeAI/Z.md"),
                provider_response_id="response-z",
                producer_session_id="session-z",
            ),
        )
        first = adapter(
            "a-adapter",
            "gpt",
            "model-a",
            response(
                raw_proposal("proposal-a", "docs/CodeAI/A.md"),
                provider_response_id="response-a",
                producer_session_id="session-a",
            ),
        )
        result = self.build([second, first])
        self.assertEqual([item.adapter_id for item in result.attempts], ["a-adapter", "z-adapter"])
        self.assertEqual(len(result.candidates), 2)

    def test_authority_claim_is_rejected(self) -> None:
        result = self.build([adapter(supplied_response=response(claims_authority=True))])
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertEqual(result.attempts[0].boundary_status, BOUNDARY_REJECT)
        self.assertFalse(result.attempts[0].raw_output_accepted)

    def test_governance_bypass_is_quarantined(self) -> None:
        result = self.build([adapter(supplied_response=response(bypasses_governance=True))])
        self.assertEqual(result.attempts[0].boundary_status, BOUNDARY_QUARANTINE)

    def test_hidden_uncertainty_routes_to_repair(self) -> None:
        result = self.build([adapter(supplied_response=response(hides_uncertainty=True))])
        self.assertEqual(result.attempts[0].boundary_status, BOUNDARY_REPAIR)

    def test_missing_evidence_routes_to_hold(self) -> None:
        result = self.build([adapter(supplied_response=response(evidence_missing=True))])
        self.assertEqual(result.attempts[0].boundary_status, BOUNDARY_HOLD)

    def test_invalid_json_routes_to_repair(self) -> None:
        result = self.build([adapter(supplied_response=response("{invalid"))])
        self.assertEqual(result.attempts[0].boundary_status, BOUNDARY_REPAIR)
        self.assertIn("raw_output_json_invalid", result.issues[0])

    def test_provider_exception_does_not_erase_supported_sibling(self) -> None:
        def fail(_prompt):
            raise RuntimeError("provider failed")

        failed = adapter("a-failed", "gpt", "model-a", generate=fail)
        supported = adapter(
            "b-supported",
            "gemini",
            "model-b",
            response(
                raw_proposal("proposal-b"),
                provider_response_id="response-b",
                producer_session_id="session-b",
            ),
        )
        result = self.build([failed, supported])
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.attempts[0].boundary_status, BOUNDARY_REJECT)
        self.assertEqual(len(result.candidates), 1)

    def test_request_digest_mismatch_blocks_before_provider_call(self) -> None:
        calls: list[dict] = []
        tracked = adapter(generate=lambda prompt: calls.append(dict(prompt)) or response())
        malformed = request()
        malformed[REQUEST_DIGEST_FIELD] = "0" * 64
        result = self.build([tracked], synthesis_request=malformed)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertEqual(calls, [])
        self.assertIsNone(result.receipt)

    def test_repository_snapshot_budget_blocks_before_provider_call(self) -> None:
        result = self.build(
            [adapter()],
            synthesis_policy=policy(maximum_repository_snapshot_bytes=1),
        )
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertEqual(result.issues, ("repository_snapshot_budget_exceeded",))

    def test_forbidden_repository_path_blocks_before_provider_call(self) -> None:
        result = self.build(
            [adapter()],
            repository_files={"docs/CodeAI/private/SECRET.md": "secret\n"},
        )
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("repository_path_forbidden", result.issues[0])

    def test_duplicate_provider_response_id_rejects_later_attempt(self) -> None:
        first = adapter(
            "a-first",
            "gpt",
            "model-a",
            response(
                raw_proposal("proposal-a", "docs/CodeAI/A.md"),
                provider_response_id="same-response",
                producer_session_id="session-a",
            ),
        )
        second = adapter(
            "b-second",
            "gemini",
            "model-b",
            response(
                raw_proposal("proposal-b", "docs/CodeAI/B.md"),
                provider_response_id="same-response",
                producer_session_id="session-b",
            ),
        )
        result = self.build([first, second])
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(len(result.candidates), 1)
        self.assertEqual(result.attempts[1].route_reason, "duplicate_provider_response_id")


if __name__ == "__main__":
    unittest.main()
