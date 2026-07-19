#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from runtime.kuuos_codeai_candidate_patch_envelope_v0_1 import seal
from runtime.kuuos_codeai_repair_cycle_continuation_admission_v0_1 import (
    RECEIPT_DIGEST_FIELD as ADMISSION_RECEIPT_DIGEST_FIELD,
)
from runtime.kuuos_codeai_repair_cycle_admission_consumption_v0_1 import (
    EXECUTION_INPUT_DIGEST_FIELD,
    POLICY_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD,
    REGISTRY_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    STATUS_BLOCKED,
    STATUS_READY,
    build_codeai_repair_cycle_admission_consumption,
)


EXAMPLE = Path("examples/codeai_repair_cycle_admission_consumption_v0_1.json")


class CodeAIRepairCycleAdmissionConsumptionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.payload = json.loads(EXAMPLE.read_text(encoding="utf-8"))

    @staticmethod
    def _reseal(value: dict, field: str) -> dict:
        copy_value = {key: item for key, item in value.items() if key != field}
        return seal(copy_value, field)

    def _run(self, payload: dict | None = None):
        value = self.payload if payload is None else payload
        return build_codeai_repair_cycle_admission_consumption(
            admission_receipt=value["admission_receipt"],
            consumption_request=value["consumption_request"],
            consumption_policy=value["consumption_policy"],
            consumption_registry=value["consumption_registry"],
        )

    def test_successful_consumption_issues_one_execution_input(self) -> None:
        result = self._run()
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.issues, ())
        self.assertIsNotNone(result.execution_input)
        self.assertIsNotNone(result.next_registry)
        self.assertIsNotNone(result.receipt)
        assert result.execution_input is not None
        assert result.next_registry is not None
        assert result.receipt is not None
        self.assertTrue(result.execution_input["execution_input_active"])
        self.assertFalse(result.execution_input["execution_input_reusable"])
        self.assertFalse(result.execution_input["execution_input_consumed"])
        self.assertTrue(result.receipt["source_admission_consumed"])
        self.assertTrue(result.receipt["exactly_one_execution_input_issued"])
        self.assertEqual(result.next_registry["registry_revision"], 2)
        self.assertEqual(result.receipt["next_consumed_admission_count"], 1)

    def test_reserved_budgets_map_exactly_to_execution_input(self) -> None:
        result = self._run()
        assert result.execution_input is not None
        assert result.receipt is not None
        pairs = (
            ("reserved_candidate", "maximum_candidate_count", "execution_candidate_budget"),
            ("reserved_provider_call", "maximum_provider_call_count", "execution_provider_call_budget"),
            ("reserved_command", "maximum_command_count", "execution_command_budget"),
            ("reserved_timeout_seconds", "maximum_total_timeout_seconds", "execution_timeout_seconds_budget"),
            ("reserved_output_bytes", "maximum_total_output_bytes", "execution_output_bytes_budget"),
        )
        admission = self.payload["admission_receipt"]
        for source_field, input_field, receipt_field in pairs:
            self.assertEqual(result.execution_input[input_field], admission[source_field])
            self.assertEqual(result.receipt[receipt_field], admission[source_field])

    def test_output_digests_are_sealed(self) -> None:
        result = self._run()
        assert result.execution_input is not None
        assert result.next_registry is not None
        assert result.receipt is not None
        self.assertEqual(
            self._reseal(result.execution_input, EXECUTION_INPUT_DIGEST_FIELD),
            result.execution_input,
        )
        self.assertEqual(
            self._reseal(result.next_registry, REGISTRY_DIGEST_FIELD),
            result.next_registry,
        )
        self.assertEqual(
            self._reseal(result.receipt, RECEIPT_DIGEST_FIELD),
            result.receipt,
        )

    def test_non_mapping_admission_blocks(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["admission_receipt"] = []
        result = self._run(payload)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("admission_receipt_not_mapping", result.issues)

    def test_admission_digest_mismatch_blocks(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["admission_receipt"]["admitted_cycle_index"] = 3
        result = self._run(payload)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("admission_receipt_digest_mismatch", result.issues)

    def test_unsupported_admission_profile_blocks(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["admission_receipt"]["profile_version"] = "unsupported"
        payload["admission_receipt"] = self._reseal(
            payload["admission_receipt"], ADMISSION_RECEIPT_DIGEST_FIELD
        )
        result = self._run(payload)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("admission_profile_unsupported", result.issues)

    def test_already_consumed_admission_blocks(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["admission_receipt"]["admission_consumed"] = True
        payload["admission_receipt"] = self._reseal(
            payload["admission_receipt"], ADMISSION_RECEIPT_DIGEST_FIELD
        )
        result = self._run(payload)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("admission_required_false:admission_consumed", result.issues)

    def test_reusable_admission_blocks(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["admission_receipt"]["admission_reusable"] = True
        payload["admission_receipt"] = self._reseal(
            payload["admission_receipt"], ADMISSION_RECEIPT_DIGEST_FIELD
        )
        result = self._run(payload)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("admission_required_false:admission_reusable", result.issues)

    def test_active_admission_blocks(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["admission_receipt"]["active_now"] = True
        payload["admission_receipt"] = self._reseal(
            payload["admission_receipt"], ADMISSION_RECEIPT_DIGEST_FIELD
        )
        result = self._run(payload)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("admission_required_false:active_now", result.issues)

    def test_admission_budget_conservation_mismatch_blocks(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["admission_receipt"]["remaining_command_after_reservation"] += 1
        payload["admission_receipt"] = self._reseal(
            payload["admission_receipt"], ADMISSION_RECEIPT_DIGEST_FIELD
        )
        admission_digest = payload["admission_receipt"][ADMISSION_RECEIPT_DIGEST_FIELD]
        payload["consumption_request"]["admission_receipt_digest"] = admission_digest
        payload["consumption_request"] = self._reseal(
            payload["consumption_request"], REQUEST_DIGEST_FIELD
        )
        payload["consumption_policy"]["expected_admission_receipt_digest"] = admission_digest
        payload["consumption_policy"] = self._reseal(
            payload["consumption_policy"], POLICY_DIGEST_FIELD
        )
        result = self._run(payload)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("admission_budget_conservation_mismatch:command", result.issues)

    def test_request_extra_field_blocks(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["consumption_request"]["unexpected"] = "value"
        result = self._run(payload)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("consumption_request_extra_fields:unexpected", result.issues)

    def test_request_digest_mismatch_blocks(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["consumption_request"]["execution_session_id"] = "changed"
        result = self._run(payload)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("consumption_request_digest_mismatch", result.issues)

    def test_policy_authority_escalation_blocks(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["consumption_policy"]["network_access_allowed"] = True
        payload["consumption_policy"] = self._reseal(
            payload["consumption_policy"], POLICY_DIGEST_FIELD
        )
        result = self._run(payload)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn(
            "consumption_policy_required_false:network_access_allowed", result.issues
        )

    def test_registry_digest_mismatch_blocks(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["consumption_registry"]["registry_revision"] = 2
        result = self._run(payload)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("consumption_registry_digest_mismatch", result.issues)

    def test_parallel_registry_history_mismatch_blocks(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["consumption_registry"]["consumed_execution_nonce_digests"] = ["2" * 64]
        payload["consumption_registry"] = self._reseal(
            payload["consumption_registry"], REGISTRY_DIGEST_FIELD
        )
        result = self._run(payload)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn(
            "consumption_registry_parallel_history_length_mismatch", result.issues
        )

    def test_admission_correspondence_mismatch_blocks(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["consumption_request"]["admission_receipt_digest"] = "9" * 64
        payload["consumption_request"] = self._reseal(
            payload["consumption_request"], REQUEST_DIGEST_FIELD
        )
        result = self._run(payload)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn(
            "consumption_correspondence_mismatch:request_admission", result.issues
        )

    def test_cycle_index_mismatch_blocks(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["consumption_request"]["admitted_cycle_index"] = 3
        payload["consumption_request"] = self._reseal(
            payload["consumption_request"], REQUEST_DIGEST_FIELD
        )
        result = self._run(payload)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn(
            "consumption_correspondence_mismatch:request_cycle_index", result.issues
        )

    def test_downstream_lineage_mismatch_blocks(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["consumption_request"]["repair_candidate_set_digest"] = "8" * 64
        payload["consumption_request"] = self._reseal(
            payload["consumption_request"], REQUEST_DIGEST_FIELD
        )
        result = self._run(payload)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn(
            "consumption_correspondence_mismatch:repair_candidate_set", result.issues
        )

    def test_actor_mismatch_blocks(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["consumption_request"]["requested_by_actor_id"] = "other"
        payload["consumption_request"] = self._reseal(
            payload["consumption_request"], REQUEST_DIGEST_FIELD
        )
        result = self._run(payload)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn(
            "consumption_correspondence_mismatch:consumer_actor", result.issues
        )

    def test_stale_request_blocks(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["consumption_request"]["request_created_epoch"] = 1000
        payload["consumption_request"] = self._reseal(
            payload["consumption_request"], REQUEST_DIGEST_FIELD
        )
        result = self._run(payload)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("consumption_request_window_invalid", result.issues)

    def test_admission_replay_blocks(self) -> None:
        payload = copy.deepcopy(self.payload)
        admission_digest = payload["admission_receipt"][ADMISSION_RECEIPT_DIGEST_FIELD]
        payload["consumption_registry"]["consumed_admission_receipt_digests"] = [
            admission_digest
        ]
        payload["consumption_registry"]["consumed_execution_nonce_digests"] = [
            "2" * 64
        ]
        payload["consumption_registry"] = self._reseal(
            payload["consumption_registry"], REGISTRY_DIGEST_FIELD
        )
        result = self._run(payload)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("consumption_admission_replay_detected", result.issues)

    def test_nonce_replay_blocks(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["consumption_registry"]["consumed_admission_receipt_digests"] = [
            "7" * 64
        ]
        payload["consumption_registry"]["consumed_execution_nonce_digests"] = [
            payload["consumption_request"]["execution_nonce_digest"]
        ]
        payload["consumption_registry"] = self._reseal(
            payload["consumption_registry"], REGISTRY_DIGEST_FIELD
        )
        result = self._run(payload)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("consumption_execution_nonce_replay_detected", result.issues)

    def test_registry_capacity_exhaustion_blocks(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["consumption_policy"]["maximum_consumed_admission_count"] = 1
        payload["consumption_policy"] = self._reseal(
            payload["consumption_policy"], POLICY_DIGEST_FIELD
        )
        payload["consumption_registry"]["consumed_admission_receipt_digests"] = [
            "7" * 64
        ]
        payload["consumption_registry"]["consumed_execution_nonce_digests"] = [
            "6" * 64
        ]
        payload["consumption_registry"] = self._reseal(
            payload["consumption_registry"], REGISTRY_DIGEST_FIELD
        )
        result = self._run(payload)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("consumption_registry_capacity_exhausted", result.issues)

    def test_non_monotone_registry_frontier_blocks(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["consumption_registry"]["last_consumed_cycle_index"] = 2
        payload["consumption_registry"] = self._reseal(
            payload["consumption_registry"], REGISTRY_DIGEST_FIELD
        )
        result = self._run(payload)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn(
            "consumption_cycle_not_strictly_after_registry_frontier", result.issues
        )

    def test_consumption_performs_no_side_effect(self) -> None:
        result = self._run()
        assert result.execution_input is not None
        assert result.receipt is not None
        for field in (
            "cycle_execution_performed",
            "provider_invoked",
            "runner_invoked",
            "candidate_generated",
            "candidate_selected",
            "patch_applied",
            "verification_executed",
            "repository_mutation_performed",
            "git_ref_changed",
            "network_access_performed",
            "secret_access_performed",
            "merge_performed",
            "deployment_performed",
        ):
            self.assertFalse(result.execution_input[field])
            self.assertFalse(result.receipt[field])


if __name__ == "__main__":
    unittest.main()
