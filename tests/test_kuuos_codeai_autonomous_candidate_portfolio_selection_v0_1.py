from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path
import unittest

from runtime.kuuos_codeai_candidate_patch_envelope_v0_1 import seal
from runtime.kuuos_codeai_autonomous_unified_diff_candidates_v0_1 import (
    RECEIPT_DIGEST_FIELD as UNIFIED_DIFF_RECEIPT_DIGEST_FIELD,
    GeneratedUnifiedDiffCandidate,
    build_codeai_autonomous_unified_diff_candidates,
)
from runtime.kuuos_codeai_autonomous_structured_edit_types_v0_1 import (
    DISPOSITION_SYNTHESIZED as STRUCTURED_EDIT_DISPOSITION_SYNTHESIZED,
    RECEIPT_DIGEST_FIELD as STRUCTURED_EDIT_RECEIPT_DIGEST_FIELD,
)
from runtime.kuuos_codeai_autonomous_candidate_portfolio_selection_v0_1 import (
    POLICY_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    STATUS_BLOCKED,
    STATUS_READY,
    build_codeai_autonomous_candidate_portfolio_selection,
)

ROOT = Path(__file__).resolve().parents[1]
EPOCH = 1784319000


def upstream_portfolio():
    proposals = json.loads(
        (ROOT / "examples" / "codeai_autonomous_unified_diff_candidates_v0_1.json").read_text(
            encoding="utf-8"
        )
    )
    candidate_data = json.loads(
        (ROOT / "examples" / "codeai_candidate_patch_envelope_v0_1.json").read_text(
            encoding="utf-8"
        )
    )
    result = build_codeai_autonomous_unified_diff_candidates(
        source_observation_receipt=candidate_data["source_observation_receipt"],
        repository_files=proposals["repository_files"],
        proposals=proposals["proposals"],
        candidate_policy=candidate_data["candidate_policy"],
    )
    assert result.receipt is not None
    return result


def source_digest(receipt: dict) -> str:
    if UNIFIED_DIFF_RECEIPT_DIGEST_FIELD in receipt:
        return receipt[UNIFIED_DIFF_RECEIPT_DIGEST_FIELD]
    return receipt[STRUCTURED_EDIT_RECEIPT_DIGEST_FIELD]


def selection_request(receipt: dict, **changes: object) -> dict:
    value = {
        "selection_request_id": "selection-test-001",
        "selection_request_revision": "r1",
        "source_portfolio_receipt_digest": source_digest(receipt),
        "selection_purpose": "independent_verification",
        "requested_by_actor_id": "repository-owner",
        "request_created_epoch": EPOCH - 10,
    }
    value.update(changes)
    return seal(value, REQUEST_DIGEST_FIELD)


def selection_policy(receipt: dict, **changes: object) -> dict:
    value = {
        "expected_source_portfolio_receipt_digest": source_digest(receipt),
        "maximum_candidate_count": 16,
        "maximum_patch_bytes": 1000000,
        "maximum_changed_paths": 64,
        "allowed_risk_labels": ["documentation", "release", "security"],
        "forbidden_risk_labels": ["release", "security"],
        "require_no_unresolved_questions": True,
        "allowed_path_prefixes": ["docs/CodeAI"],
        "forbidden_path_prefixes": ["docs/CodeAI/private"],
        "selection_strategy": "least_change_admissible",
        "evaluation_epoch": EPOCH,
        "maximum_request_age": 3600,
    }
    value.update(changes)
    return seal(value, POLICY_DIGEST_FIELD)


class AutonomousCandidatePortfolioSelectionTests(unittest.TestCase):
    def build(
        self,
        upstream=None,
        candidates=None,
        request=None,
        policy=None,
    ):
        upstream = upstream or upstream_portfolio()
        assert upstream.receipt is not None
        return build_codeai_autonomous_candidate_portfolio_selection(
            source_portfolio_receipt=upstream.receipt,
            candidates=candidates if candidates is not None else upstream.candidates,
            selection_request=request or selection_request(upstream.receipt),
            selection_policy=policy or selection_policy(upstream.receipt),
        )

    def test_selects_rank_one_least_change_candidate(self) -> None:
        result = self.build()
        self.assertEqual(result.status, STATUS_READY)
        self.assertIsNotNone(result.selected_candidate)
        self.assertEqual(result.selected_candidate.upstream_rank, 1)
        self.assertTrue(result.receipt["candidate_selected"])

    def test_path_policy_can_skip_rank_one_and_select_next(self) -> None:
        upstream = upstream_portfolio()
        first_path = upstream.candidates[0].patch_candidate["changed_paths"][0]
        result = self.build(
            upstream,
            policy=selection_policy(
                upstream.receipt,
                forbidden_path_prefixes=[first_path],
            ),
        )
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.selected_candidate.upstream_rank, 2)
        self.assertEqual(result.receipt["rejected_candidate_count"], 1)

    def test_no_admissible_candidate_records_blocked_receipt(self) -> None:
        upstream = upstream_portfolio()
        result = self.build(
            upstream,
            policy=selection_policy(upstream.receipt, maximum_patch_bytes=1),
        )
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIsNone(result.selected_candidate)
        self.assertIsNotNone(result.receipt)
        self.assertFalse(result.receipt["candidate_selected"])
        self.assertEqual(result.receipt["admissible_candidate_count"], 0)

    def test_request_digest_mismatch_blocks_before_selection(self) -> None:
        upstream = upstream_portfolio()
        malformed = selection_request(upstream.receipt)
        malformed[REQUEST_DIGEST_FIELD] = "0" * 64
        result = self.build(upstream, request=malformed)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIsNone(result.receipt)
        self.assertIn("selection_request_digest_mismatch", result.issues)

    def test_stale_request_blocks_before_selection(self) -> None:
        upstream = upstream_portfolio()
        stale = selection_request(upstream.receipt, request_created_epoch=EPOCH - 10000)
        result = self.build(upstream, request=stale)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertEqual(result.issues, ("selection_request_window_invalid",))

    def test_tampered_patch_artifact_is_rejected(self) -> None:
        upstream = upstream_portfolio()
        first = upstream.candidates[0]
        tampered = GeneratedUnifiedDiffCandidate(
            first.rank,
            first.proposal_id,
            first.patch_candidate,
            first.patch_artifact + "tampered\n",
            first.candidate_receipt,
        )
        result = self.build(upstream, candidates=(tampered,) + upstream.candidates[1:])
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIsNone(result.receipt)
        self.assertTrue(any("patch_artifact_digest_mismatch" in issue for issue in result.issues))

    def test_duplicate_rank_is_rejected(self) -> None:
        upstream = upstream_portfolio()
        second = replace(upstream.candidates[1], rank=1)
        result = self.build(upstream, candidates=(upstream.candidates[0], second))
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertTrue(any("rank_duplicate" in issue for issue in result.issues))

    def test_source_candidate_correspondence_is_exact(self) -> None:
        upstream = upstream_portfolio()
        reversed_candidates = tuple(reversed(upstream.candidates))
        result = self.build(upstream, candidates=reversed_candidates)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("source_portfolio_candidate_ids_mismatch", result.issues)

    def test_structured_edit_synthesis_receipt_is_supported(self) -> None:
        upstream = upstream_portfolio()
        source = dict(upstream.receipt)
        source.pop(UNIFIED_DIFF_RECEIPT_DIGEST_FIELD)
        source["codeai_disposition"] = STRUCTURED_EDIT_DISPOSITION_SYNTHESIZED
        source = seal(source, STRUCTURED_EDIT_RECEIPT_DIGEST_FIELD)
        result = build_codeai_autonomous_candidate_portfolio_selection(
            source_portfolio_receipt=source,
            candidates=upstream.candidates,
            selection_request=selection_request(source),
            selection_policy=selection_policy(source),
        )
        self.assertEqual(result.status, STATUS_READY)
        self.assertIsNotNone(result.selected_candidate)

    def test_selection_grants_no_verification_or_execution_effect(self) -> None:
        result = self.build()
        receipt = result.receipt
        self.assertTrue(receipt["selection_authority_consumed_by_kernel"])
        self.assertFalse(receipt["successor_selection_authority_granted"])
        self.assertFalse(receipt["verification_lease_issued"])
        self.assertFalse(receipt["execution_lease_issued"])
        self.assertFalse(receipt["repository_mutation_performed"])
        self.assertFalse(receipt["git_ref_changed"])
        self.assertFalse(receipt["selected_candidate_treated_as_correct"])
        self.assertFalse(receipt["selection_treated_as_verification"])


if __name__ == "__main__":
    unittest.main()
