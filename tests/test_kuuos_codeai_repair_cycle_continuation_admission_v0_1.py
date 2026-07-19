#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
import unittest

from runtime.kuuos_codeai_candidate_patch_envelope_v0_1 import seal
from runtime.kuuos_codeai_bounded_repair_cycle_orchestration_v0_1 import (
    DISPOSITION_ABORTED as SOURCE_DISPOSITION_ABORTED,
    DISPOSITION_FAILED as SOURCE_DISPOSITION_FAILED,
    MODE_BOUNDED_REPAIR_CYCLE as SOURCE_MODE,
    PROFILE_VERSION as SOURCE_PROFILE_VERSION,
    RECEIPT_DIGEST_FIELD as SOURCE_RECEIPT_DIGEST_FIELD,
)
from runtime.kuuos_codeai_repair_cycle_continuation_admission_v0_1 import (
    BUDGET_LEDGER_DIGEST_FIELD,
    DISPOSITION_ADMITTED,
    MODE_CONTINUATION_ADMISSION,
    POLICY_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    STATUS_BLOCKED,
    STATUS_READY,
    build_codeai_repair_cycle_continuation_admission,
)


def _source_receipt(
    *,
    cycle_index: int = 1,
    maximum_cycle_count: int = 3,
    disposition: str = SOURCE_DISPOSITION_FAILED,
    next_cycle_eligible: bool = True,
    cycle_verification_passed: bool = False,
    cycle_limit_reached: bool = False,
) -> dict:
    return seal(
        {
            "schema_version": "v0.1",
            "profile_version": SOURCE_PROFILE_VERSION,
            "selected_candidate_digest": "a" * 64,
            "cycle_index": cycle_index,
            "maximum_cycle_count": maximum_cycle_count,
            "codeai_disposition": disposition,
            "operating_mode": SOURCE_MODE,
            "route_receipt_recorded": True,
            "cycle_completed": True,
            "cycle_verification_passed": cycle_verification_passed,
            "cycle_limit_reached": cycle_limit_reached,
            "next_cycle_eligible": next_cycle_eligible,
            "next_cycle_authority_granted": False,
            "repository_mutation_performed": False,
            "git_ref_changed": False,
            "network_access_performed": False,
            "secret_access_performed": False,
            "merge_performed": False,
            "deployment_performed": False,
            "execution_authority_granted": False,
            "successor_stage_authority_granted": False,
            "history_read_only": True,
            "future_only": True,
            "active_now": False,
        },
        SOURCE_RECEIPT_DIGEST_FIELD,
    )


def _request(source: dict, *, epoch: int = 1000, next_index: int = 2) -> dict:
    return seal(
        {
            "continuation_request_id": "continuation-test-001",
            "continuation_request_revision": "r1",
            "source_cycle_receipt_digest": source[SOURCE_RECEIPT_DIGEST_FIELD],
            "source_selected_candidate_digest": source["selected_candidate_digest"],
            "requested_next_cycle_index": next_index,
            "requested_candidate_reservation": 3,
            "requested_provider_call_reservation": 1,
            "requested_command_reservation": 4,
            "requested_timeout_seconds_reservation": 120,
            "requested_output_bytes_reservation": 16384,
            "continuation_nonce_digest": "b" * 64,
            "requested_by_actor_id": "codeai-test",
            "request_created_epoch": epoch,
        },
        REQUEST_DIGEST_FIELD,
    )


def _policy(source: dict, *, epoch: int = 1000) -> dict:
    return seal(
        {
            "expected_source_cycle_receipt_digest": source[SOURCE_RECEIPT_DIGEST_FIELD],
            "expected_source_selected_candidate_digest": source["selected_candidate_digest"],
            "expected_current_cycle_index": source["cycle_index"],
            "maximum_cycle_count": source["maximum_cycle_count"],
            "maximum_total_candidate_count": 12,
            "maximum_total_provider_calls": 6,
            "maximum_total_commands": 24,
            "maximum_total_timeout_seconds": 900,
            "maximum_total_output_bytes": 131072,
            "maximum_candidate_reservation_per_cycle": 4,
            "maximum_provider_call_reservation_per_cycle": 2,
            "maximum_command_reservation_per_cycle": 6,
            "maximum_timeout_seconds_reservation_per_cycle": 180,
            "maximum_output_bytes_reservation_per_cycle": 32768,
            "minimum_candidate_reservation": 1,
            "minimum_provider_call_reservation": 1,
            "minimum_command_reservation": 1,
            "minimum_timeout_seconds_reservation": 30,
            "minimum_output_bytes_reservation": 1024,
            "network_access_allowed": False,
            "secrets_allowed": False,
            "live_repository_access_allowed": False,
            "git_operations_allowed": False,
            "automatic_execution_allowed": False,
            "evaluation_epoch": epoch,
            "maximum_request_age": 20,
        },
        POLICY_DIGEST_FIELD,
    )


def _ledger(source: dict, *, epoch: int = 1000) -> dict:
    return seal(
        {
            "source_cycle_receipt_digest": source[SOURCE_RECEIPT_DIGEST_FIELD],
            "completed_cycle_count": source["cycle_index"],
            "candidate_count_consumed": 3,
            "provider_call_count_consumed": 1,
            "command_count_consumed": 4,
            "timeout_seconds_consumed": 120,
            "output_bytes_consumed": 16384,
            "ledger_created_epoch": epoch,
        },
        BUDGET_LEDGER_DIGEST_FIELD,
    )


def _build(source=None, request=None, policy=None, ledger=None):
    source = source or _source_receipt()
    return build_codeai_repair_cycle_continuation_admission(
        source_cycle_receipt=source,
        continuation_request=request or _request(source),
        continuation_policy=policy or _policy(source),
        budget_ledger=ledger or _ledger(source),
    )


class RepairCycleContinuationAdmissionTests(unittest.TestCase):
    def test_admits_exactly_one_next_cycle(self):
        result = _build()
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.issues, ())
        assert result.receipt is not None
        receipt = result.receipt
        self.assertEqual(receipt["codeai_disposition"], DISPOSITION_ADMITTED)
        self.assertEqual(receipt["operating_mode"], MODE_CONTINUATION_ADMISSION)
        self.assertEqual(receipt["current_cycle_index"], 1)
        self.assertEqual(receipt["admitted_cycle_index"], 2)
        self.assertTrue(receipt["exactly_one_next_cycle_admitted"])
        self.assertTrue(receipt["continuation_admission_authority_granted"])
        self.assertFalse(receipt["admission_reusable"])
        self.assertFalse(receipt["automatic_next_cycle_started"])

    def test_budget_arithmetic_is_sealed(self):
        result = _build()
        assert result.receipt is not None
        self.assertEqual(result.receipt["remaining_candidate_before_reservation"], 9)
        self.assertEqual(result.receipt["remaining_candidate_after_reservation"], 6)
        self.assertEqual(result.receipt["remaining_provider_call_after_reservation"], 4)
        self.assertEqual(result.receipt["remaining_command_after_reservation"], 16)
        self.assertEqual(result.receipt["remaining_timeout_seconds_after_reservation"], 660)
        self.assertEqual(result.receipt["remaining_output_bytes_after_reservation"], 98304)
        self.assertIn(RECEIPT_DIGEST_FIELD, result.receipt)

    def test_budget_abort_is_continuable(self):
        source = _source_receipt(disposition=SOURCE_DISPOSITION_ABORTED)
        self.assertEqual(_build(source=source).status, STATUS_READY)

    def test_passed_cycle_is_not_continuable(self):
        source = _source_receipt(
            disposition="repair_cycle_verification_passed",
            next_cycle_eligible=False,
            cycle_verification_passed=True,
        )
        result = _build(source=source)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertTrue(any("not_continuable" in issue for issue in result.issues))

    def test_source_eligibility_is_required(self):
        source = _source_receipt(next_cycle_eligible=False)
        self.assertEqual(_build(source=source).status, STATUS_BLOCKED)

    def test_cycle_limit_is_fail_closed(self):
        source = _source_receipt(
            cycle_index=3,
            maximum_cycle_count=3,
            next_cycle_eligible=False,
            cycle_limit_reached=True,
        )
        self.assertEqual(_build(source=source).status, STATUS_BLOCKED)

    def test_next_cycle_must_be_exact_successor(self):
        source = _source_receipt()
        request = _request(source, next_index=3)
        result = _build(source=source, request=request)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("continuation_next_cycle_not_exact_successor", result.issues)

    def test_source_digest_tamper_is_rejected(self):
        source = _source_receipt()
        source["cycle_index"] = 2
        self.assertEqual(_build(source=source).status, STATUS_BLOCKED)

    def test_request_digest_tamper_is_rejected(self):
        source = _source_receipt()
        request = _request(source)
        request["requested_candidate_reservation"] = 2
        self.assertEqual(_build(source=source, request=request).status, STATUS_BLOCKED)

    def test_policy_digest_tamper_is_rejected(self):
        source = _source_receipt()
        policy = _policy(source)
        policy["maximum_cycle_count"] = 4
        self.assertEqual(_build(source=source, policy=policy).status, STATUS_BLOCKED)

    def test_ledger_digest_tamper_is_rejected(self):
        source = _source_receipt()
        ledger = _ledger(source)
        ledger["candidate_count_consumed"] = 4
        self.assertEqual(_build(source=source, ledger=ledger).status, STATUS_BLOCKED)

    def test_ledger_lineage_must_match_source(self):
        source = _source_receipt()
        ledger = _ledger(source)
        ledger["source_cycle_receipt_digest"] = "c" * 64
        ledger = seal(ledger, BUDGET_LEDGER_DIGEST_FIELD)
        result = _build(source=source, ledger=ledger)
        self.assertIn(
            "continuation_correspondence_mismatch:ledger_source_cycle",
            result.issues,
        )

    def test_completed_cycle_count_must_match(self):
        source = _source_receipt()
        ledger = _ledger(source)
        ledger["completed_cycle_count"] = 0
        ledger = seal(ledger, BUDGET_LEDGER_DIGEST_FIELD)
        result = _build(source=source, ledger=ledger)
        self.assertIn("continuation_ledger_completed_cycle_count_mismatch", result.issues)

    def test_reservation_cannot_exceed_remaining_total(self):
        source = _source_receipt()
        policy = _policy(source)
        policy["maximum_total_candidate_count"] = 5
        policy = seal(policy, POLICY_DIGEST_FIELD)
        result = _build(source=source, policy=policy)
        self.assertIn(
            "continuation_budget_reservation_exceeds_remaining:candidate",
            result.issues,
        )

    def test_reservation_cannot_exceed_per_cycle_maximum(self):
        source = _source_receipt()
        request = _request(source)
        request["requested_command_reservation"] = 7
        request = seal(request, REQUEST_DIGEST_FIELD)
        result = _build(source=source, request=request)
        self.assertIn(
            "continuation_budget_reservation_exceeds_cycle_maximum:command",
            result.issues,
        )

    def test_reservation_must_meet_minimum(self):
        source = _source_receipt()
        request = _request(source)
        request["requested_timeout_seconds_reservation"] = 20
        request = seal(request, REQUEST_DIGEST_FIELD)
        result = _build(source=source, request=request)
        self.assertIn(
            "continuation_budget_reservation_below_minimum:timeout_seconds",
            result.issues,
        )

    def test_stale_request_is_rejected(self):
        source = _source_receipt()
        request = _request(source, epoch=970)
        result = _build(source=source, request=request)
        self.assertIn("continuation_request_window_invalid", result.issues)

    def test_forbidden_capability_is_rejected(self):
        source = _source_receipt()
        for field in (
            "network_access_allowed",
            "secrets_allowed",
            "live_repository_access_allowed",
            "git_operations_allowed",
            "automatic_execution_allowed",
        ):
            policy = _policy(source)
            policy[field] = True
            policy = seal(policy, POLICY_DIGEST_FIELD)
            with self.subTest(field=field):
                self.assertEqual(_build(source=source, policy=policy).status, STATUS_BLOCKED)

    def test_admission_grants_no_execution_or_live_authority(self):
        result = _build()
        assert result.receipt is not None
        for field in (
            "automatic_next_cycle_started",
            "cycle_execution_performed",
            "runner_invoked",
            "candidate_generated",
            "candidate_selected",
            "patch_applied",
            "repository_mutation_performed",
            "git_ref_changed",
            "branch_created",
            "commit_created",
            "push_performed",
            "pull_request_created",
            "merge_performed",
            "deployment_performed",
            "secret_access_performed",
            "network_access_performed",
            "selection_authority_granted",
            "verification_authority_granted",
            "execution_authority_granted",
            "automatic_execution_authority_granted",
            "merge_authority_granted",
            "deployment_authority_granted",
            "secret_access_authority_granted",
            "general_successor_stage_authority_granted",
        ):
            self.assertFalse(result.receipt[field], field)

    def test_extra_fields_fail_closed(self):
        source = _source_receipt()
        request = _request(source)
        request["unexpected"] = True
        request = seal(request, REQUEST_DIGEST_FIELD)
        self.assertEqual(_build(source=source, request=request).status, STATUS_BLOCKED)

    def test_deterministic_receipt(self):
        first = _build()
        second = _build()
        self.assertEqual(first.receipt, second.receipt)


if __name__ == "__main__":
    unittest.main()
