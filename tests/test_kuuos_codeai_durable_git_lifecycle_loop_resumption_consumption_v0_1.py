#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
import unittest

from runtime.kuuos_codeai_durable_git_lifecycle_loop_resumption_admission_types_v0_1 import (
    DISPOSITION_ADMITTED as SOURCE_DISPOSITION_ADMITTED,
    EVIDENCE_DIGEST_FIELD as SOURCE_EVIDENCE_DIGEST_FIELD,
    PROFILE_VERSION as SOURCE_PROFILE_VERSION,
    RECEIPT_DIGEST_FIELD as SOURCE_RECEIPT_DIGEST_FIELD,
    REGISTRY_DIGEST_FIELD as SOURCE_REGISTRY_DIGEST_FIELD,
    RESUME_INPUT_DIGEST_FIELD as SOURCE_RESUME_INPUT_DIGEST_FIELD,
    canonical_digest,
)
from runtime.kuuos_codeai_durable_git_lifecycle_loop_resumption_consumption_v0_1 import (
    DISPOSITION_CONSUMED,
    EVIDENCE_DIGEST_FIELD,
    EXECUTION_INPUT_DIGEST_FIELD,
    EXECUTION_INPUT_PROFILE_VERSION,
    POLICY_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD,
    REGISTRY_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    STATUS_BLOCKED,
    STATUS_READY,
    build_codeai_durable_git_lifecycle_loop_resumption_consumption,
)


def seal(value: dict, field: str) -> dict:
    value.pop(field, None)
    value[field] = canonical_digest(value)
    return value


def source_bundle() -> tuple[dict, dict, dict, dict]:
    resume_input = seal(
        {
            "schema_version": "v0.1",
            "profile_version": SOURCE_PROFILE_VERSION,
            "resume_input_id": "git-loop-resumption-session-001:resume-input",
            "checkpoint_id": "git-loop-checkpoint-001",
            "checkpoint_envelope_digest": "a" * 64,
            "source_persistence_receipt_digest": "b" * 64,
            "source_persistence_registry_digest": "c" * 64,
            "source_store_state_digest": "d" * 64,
            "loop_id": "git-loop-001",
            "lifecycle_id": "codeai-autonomous-git-lifecycle-v0-1-001",
            "repository_full_name": "itakura-hidetoshi/KuuOS",
            "loop_disposition": "bounded_git_lifecycle_loop_completed",
            "prior_effect_count": 4,
            "prior_maximum_effect_count": 8,
            "final_lifecycle_receipt_digest": "e" * 64,
            "final_lifecycle_state_digest": "f" * 64,
            "final_lifecycle_completed": True,
            "final_execution_lease_issued": False,
            "resume_effect_budget": 3,
            "resume_execution_command_budget": 6,
            "resume_execution_output_bytes": 6000,
            "issued_epoch": 500,
            "future_only": True,
            "active_now": False,
            "loop_execution_authorized": False,
            "git_effect_authorized": False,
            "automatic_resumption_authorized": False,
            "general_successor_stage_authority_granted": False,
        },
        SOURCE_RESUME_INPUT_DIGEST_FIELD,
    )
    source_registry = seal(
        {
            "registry_id": "git-loop-resumption-registry-001",
            "registry_revision": 1,
            "consumed_resumption_nonce_digests": ["1" * 64],
            "admitted_checkpoint_ids": ["git-loop-checkpoint-001"],
            "admitted_checkpoint_envelope_digests": ["a" * 64],
            "admitted_persistence_receipt_digests": ["b" * 64],
            "resumption_attempt_count": 1,
            "successful_resumption_admission_count": 1,
            "last_resumption_epoch": 500,
        },
        SOURCE_REGISTRY_DIGEST_FIELD,
    )
    source_evidence = seal(
        {
            "schema_version": "v0.1",
            "profile_version": SOURCE_PROFILE_VERSION,
            "resume_input_digest": resume_input[SOURCE_RESUME_INPUT_DIGEST_FIELD],
            "checkpoint_read_verified": True,
            "resume_input_issued": True,
            "loop_executed": False,
            "git_effect_performed": False,
            "automatic_resumption_performed": False,
        },
        SOURCE_EVIDENCE_DIGEST_FIELD,
    )
    source_receipt = seal(
        {
            "schema_version": "v0.1",
            "profile_version": SOURCE_PROFILE_VERSION,
            "resumption_evidence_digest": source_evidence[SOURCE_EVIDENCE_DIGEST_FIELD],
            "next_resumption_registry_digest": source_registry[SOURCE_REGISTRY_DIGEST_FIELD],
            "resume_input_digest": resume_input[SOURCE_RESUME_INPUT_DIGEST_FIELD],
            "checkpoint_id": "git-loop-checkpoint-001",
            "checkpoint_envelope_digest": "a" * 64,
            "loop_id": "git-loop-001",
            "lifecycle_id": "codeai-autonomous-git-lifecycle-v0-1-001",
            "repository_full_name": "itakura-hidetoshi/KuuOS",
            "codeai_disposition": SOURCE_DISPOSITION_ADMITTED,
            "route_receipt_recorded": True,
            "source_persistence_bundle_verified": True,
            "resumption_nonce_consumed": True,
            "resumption_registry_advanced_once": True,
            "read_adapter_invoked_once": True,
            "checkpoint_read_verified": True,
            "checkpoint_unavailable": False,
            "checkpoint_read_failed": False,
            "checkpoint_read_evidence_quarantined": False,
            "resume_input_issued": True,
            "loop_execution_performed": False,
            "git_effect_performed": False,
            "automatic_resumption_performed": False,
            "network_accessed": False,
            "secret_material_read": False,
            "general_git_authority_granted": False,
            "general_successor_stage_authority_granted": False,
            "future_only": True,
            "active_now": False,
        },
        SOURCE_RECEIPT_DIGEST_FIELD,
    )
    return source_receipt, source_evidence, source_registry, resume_input


def request_for(source_receipt: dict, source_evidence: dict, source_registry: dict, resume_input: dict) -> dict:
    return seal(
        {
            "consumption_session_id": "git-loop-resumption-consumption-001",
            "consumption_nonce_digest": "2" * 64,
            "source_resumption_receipt_digest": source_receipt[SOURCE_RECEIPT_DIGEST_FIELD],
            "source_resumption_evidence_digest": source_evidence[SOURCE_EVIDENCE_DIGEST_FIELD],
            "source_resumption_registry_digest": source_registry[SOURCE_REGISTRY_DIGEST_FIELD],
            "source_resume_input_digest": resume_input[SOURCE_RESUME_INPUT_DIGEST_FIELD],
            "checkpoint_id": resume_input["checkpoint_id"],
            "checkpoint_envelope_digest": resume_input["checkpoint_envelope_digest"],
            "loop_id": resume_input["loop_id"],
            "lifecycle_id": resume_input["lifecycle_id"],
            "repository_full_name": resume_input["repository_full_name"],
            "consumer_id": "codeai-loop-resumption-consumer",
            "execution_session_id": "git-loop-resume-execution-001",
            "request_created_epoch": 510,
            "consume_resume_input": True,
            "issue_execution_input": True,
            "source_correspondence_confirmed": True,
        },
        REQUEST_DIGEST_FIELD,
    )


def policy_for(source_receipt: dict, source_evidence: dict, source_registry: dict, resume_input: dict) -> dict:
    return seal(
        {
            "expected_source_resumption_receipt_digest": source_receipt[SOURCE_RECEIPT_DIGEST_FIELD],
            "expected_source_resumption_evidence_digest": source_evidence[SOURCE_EVIDENCE_DIGEST_FIELD],
            "expected_source_resumption_registry_digest": source_registry[SOURCE_REGISTRY_DIGEST_FIELD],
            "expected_source_resume_input_digest": resume_input[SOURCE_RESUME_INPUT_DIGEST_FIELD],
            "expected_repository_full_name": resume_input["repository_full_name"],
            "authorized_consumer_ids": ["codeai-loop-resumption-consumer"],
            "maximum_request_age": 100,
            "maximum_registry_entries": 16,
            "maximum_resume_effect_budget": 5,
            "maximum_resume_execution_command_budget": 10,
            "maximum_resume_execution_output_bytes": 10000,
            "evaluation_epoch": 510,
            "allow_resume_input_consumption": True,
            "require_future_only_input": True,
            "require_inactive_input": True,
            "require_nonce_consumption": True,
            "allow_execution_input_issuance": True,
            "allow_loop_execution_during_consumption": False,
            "allow_git_effect_during_consumption": False,
            "allow_automatic_resumption": False,
            "allow_network_access": False,
            "allow_secret_material_read": False,
            "allow_general_successor_authority": False,
        },
        POLICY_DIGEST_FIELD,
    )


def empty_registry() -> dict:
    return seal(
        {
            "registry_id": "git-loop-resumption-consumption-registry-001",
            "registry_revision": 0,
            "consumed_consumption_nonce_digests": [],
            "consumed_resumption_receipt_digests": [],
            "consumed_resume_input_digests": [],
            "issued_execution_input_digests": [],
            "successful_consumption_count": 0,
            "last_consumption_epoch": 0,
        },
        REGISTRY_DIGEST_FIELD,
    )


def valid_inputs() -> dict:
    source_receipt, source_evidence, source_registry, resume_input = source_bundle()
    return {
        "resumption_receipt": source_receipt,
        "resumption_evidence": source_evidence,
        "resumption_registry": source_registry,
        "resume_input": resume_input,
        "consumption_request": request_for(
            source_receipt, source_evidence, source_registry, resume_input
        ),
        "consumption_policy": policy_for(
            source_receipt, source_evidence, source_registry, resume_input
        ),
        "consumption_registry": empty_registry(),
    }


class DurableGitLifecycleLoopResumptionConsumptionTests(unittest.TestCase):
    def build(self, values: dict):
        return build_codeai_durable_git_lifecycle_loop_resumption_consumption(**values)

    def mutate_and_reseal(self, values: dict, key: str, field: str, value, digest_field: str):
        values[key][field] = value
        seal(values[key], digest_field)

    def test_success_issues_one_active_execution_input(self):
        result = self.build(valid_inputs())
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.issues, ())
        self.assertIsNotNone(result.execution_input)
        self.assertTrue(result.execution_input["active_now"])
        self.assertTrue(result.execution_input["one_shot"])
        self.assertFalse(result.execution_input["reusable"])
        self.assertTrue(result.execution_input["loop_execution_authorized"])
        self.assertFalse(result.execution_input["direct_git_effect_authorized"])
        self.assertEqual(result.execution_input["profile_version"], EXECUTION_INPUT_PROFILE_VERSION)
        self.assertEqual(
            result.execution_input[EXECUTION_INPUT_DIGEST_FIELD],
            canonical_digest({
                key: value
                for key, value in result.execution_input.items()
                if key != EXECUTION_INPUT_DIGEST_FIELD
            }),
        )

    def test_success_advances_parallel_registry_histories_once(self):
        result = self.build(valid_inputs())
        self.assertEqual(result.next_registry["registry_revision"], 1)
        self.assertEqual(result.next_registry["successful_consumption_count"], 1)
        self.assertEqual(len(result.next_registry["consumed_consumption_nonce_digests"]), 1)
        self.assertEqual(len(result.next_registry["consumed_resumption_receipt_digests"]), 1)
        self.assertEqual(len(result.next_registry["consumed_resume_input_digests"]), 1)
        self.assertEqual(len(result.next_registry["issued_execution_input_digests"]), 1)

    def test_success_receipt_records_no_effect_during_consumption(self):
        result = self.build(valid_inputs())
        receipt = result.receipt
        self.assertEqual(receipt["codeai_disposition"], DISPOSITION_CONSUMED)
        self.assertFalse(receipt["loop_execution_performed"])
        self.assertFalse(receipt["git_effect_performed"])
        self.assertFalse(receipt["automatic_resumption_performed"])
        self.assertFalse(receipt["network_accessed"])
        self.assertFalse(receipt["secret_material_read"])
        self.assertFalse(receipt["general_git_authority_granted"])
        self.assertFalse(receipt["general_successor_stage_authority_granted"])
        self.assertTrue(receipt["execution_input_active"])
        self.assertEqual(
            receipt[RECEIPT_DIGEST_FIELD],
            canonical_digest({
                key: value for key, value in receipt.items() if key != RECEIPT_DIGEST_FIELD
            }),
        )

    def test_non_mapping_input_blocks(self):
        values = valid_inputs()
        values["resume_input"] = None
        result = self.build(values)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("resume_input_not_mapping", result.issues)

    def test_source_receipt_tamper_blocks(self):
        values = valid_inputs()
        values["resumption_receipt"]["checkpoint_id"] = "other"
        result = self.build(values)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("source_resumption_receipt_digest_mismatch", result.issues)

    def test_source_receipt_non_admitted_blocks(self):
        values = valid_inputs()
        self.mutate_and_reseal(
            values,
            "resumption_receipt",
            "codeai_disposition",
            "checkpoint_read_failed",
            SOURCE_RECEIPT_DIGEST_FIELD,
        )
        result = self.build(values)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("source_resumption_receipt_disposition_invalid", result.issues)

    def test_source_evidence_not_verified_blocks(self):
        values = valid_inputs()
        self.mutate_and_reseal(
            values,
            "resumption_evidence",
            "checkpoint_read_verified",
            False,
            SOURCE_EVIDENCE_DIGEST_FIELD,
        )
        result = self.build(values)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("source_resumption_evidence_checkpoint_not_verified", result.issues)

    def test_source_registry_checkpoint_absence_blocks(self):
        values = valid_inputs()
        self.mutate_and_reseal(
            values,
            "resumption_registry",
            "admitted_checkpoint_ids",
            ["other-checkpoint"],
            SOURCE_REGISTRY_DIGEST_FIELD,
        )
        result = self.build(values)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("resumption_consumption_source_correspondence_mismatch", result.issues)

    def test_resume_input_digest_tamper_blocks(self):
        values = valid_inputs()
        values["resume_input"]["loop_id"] = "other-loop"
        result = self.build(values)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("source_resume_input_digest_mismatch", result.issues)

    def test_resume_input_extra_field_blocks(self):
        values = valid_inputs()
        values["resume_input"]["unexpected"] = True
        seal(values["resume_input"], SOURCE_RESUME_INPUT_DIGEST_FIELD)
        result = self.build(values)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertTrue(any(issue.startswith("source_resume_input_extra_fields:") for issue in result.issues))

    def test_resume_input_not_future_only_blocks(self):
        values = valid_inputs()
        self.mutate_and_reseal(
            values, "resume_input", "future_only", False, SOURCE_RESUME_INPUT_DIGEST_FIELD
        )
        result = self.build(values)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("source_resume_input_not_future_only", result.issues)

    def test_resume_input_already_active_blocks(self):
        values = valid_inputs()
        self.mutate_and_reseal(
            values, "resume_input", "active_now", True, SOURCE_RESUME_INPUT_DIGEST_FIELD
        )
        result = self.build(values)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("source_resume_input_required_false:active_now", result.issues)

    def test_resume_input_prior_loop_authority_blocks(self):
        values = valid_inputs()
        self.mutate_and_reseal(
            values,
            "resume_input",
            "loop_execution_authorized",
            True,
            SOURCE_RESUME_INPUT_DIGEST_FIELD,
        )
        result = self.build(values)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn(
            "source_resume_input_required_false:loop_execution_authorized", result.issues
        )

    def test_request_correspondence_mismatch_blocks(self):
        values = valid_inputs()
        self.mutate_and_reseal(
            values,
            "consumption_request",
            "checkpoint_id",
            "other-checkpoint",
            REQUEST_DIGEST_FIELD,
        )
        result = self.build(values)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("resumption_consumption_source_correspondence_mismatch", result.issues)

    def test_stale_request_blocks(self):
        values = valid_inputs()
        self.mutate_and_reseal(
            values,
            "consumption_request",
            "request_created_epoch",
            1,
            REQUEST_DIGEST_FIELD,
        )
        result = self.build(values)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn(
            "resumption_consumption_freshness_capacity_or_replay_violation", result.issues
        )

    def test_unauthorized_consumer_blocks(self):
        values = valid_inputs()
        self.mutate_and_reseal(
            values,
            "consumption_request",
            "consumer_id",
            "other-consumer",
            REQUEST_DIGEST_FIELD,
        )
        result = self.build(values)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("resumption_consumption_source_correspondence_mismatch", result.issues)

    def test_nonce_replay_blocks(self):
        values = valid_inputs()
        registry = values["consumption_registry"]
        registry["registry_revision"] = 1
        registry["successful_consumption_count"] = 1
        registry["consumed_consumption_nonce_digests"] = [
            values["consumption_request"]["consumption_nonce_digest"]
        ]
        registry["consumed_resumption_receipt_digests"] = ["3" * 64]
        registry["consumed_resume_input_digests"] = ["4" * 64]
        registry["issued_execution_input_digests"] = ["5" * 64]
        seal(registry, REGISTRY_DIGEST_FIELD)
        result = self.build(values)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn(
            "resumption_consumption_freshness_capacity_or_replay_violation", result.issues
        )

    def test_receipt_replay_blocks(self):
        values = valid_inputs()
        registry = values["consumption_registry"]
        registry["registry_revision"] = 1
        registry["successful_consumption_count"] = 1
        registry["consumed_consumption_nonce_digests"] = ["3" * 64]
        registry["consumed_resumption_receipt_digests"] = [
            values["consumption_request"]["source_resumption_receipt_digest"]
        ]
        registry["consumed_resume_input_digests"] = ["4" * 64]
        registry["issued_execution_input_digests"] = ["5" * 64]
        seal(registry, REGISTRY_DIGEST_FIELD)
        result = self.build(values)
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_resume_input_replay_blocks(self):
        values = valid_inputs()
        registry = values["consumption_registry"]
        registry["registry_revision"] = 1
        registry["successful_consumption_count"] = 1
        registry["consumed_consumption_nonce_digests"] = ["3" * 64]
        registry["consumed_resumption_receipt_digests"] = ["4" * 64]
        registry["consumed_resume_input_digests"] = [
            values["consumption_request"]["source_resume_input_digest"]
        ]
        registry["issued_execution_input_digests"] = ["5" * 64]
        seal(registry, REGISTRY_DIGEST_FIELD)
        result = self.build(values)
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_registry_capacity_blocks(self):
        values = valid_inputs()
        values["consumption_policy"]["maximum_registry_entries"] = 1
        seal(values["consumption_policy"], POLICY_DIGEST_FIELD)
        registry = values["consumption_registry"]
        registry["registry_revision"] = 1
        registry["successful_consumption_count"] = 1
        registry["consumed_consumption_nonce_digests"] = ["3" * 64]
        registry["consumed_resumption_receipt_digests"] = ["4" * 64]
        registry["consumed_resume_input_digests"] = ["5" * 64]
        registry["issued_execution_input_digests"] = ["6" * 64]
        seal(registry, REGISTRY_DIGEST_FIELD)
        result = self.build(values)
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_policy_forbidden_loop_execution_blocks(self):
        values = valid_inputs()
        self.mutate_and_reseal(
            values,
            "consumption_policy",
            "allow_loop_execution_during_consumption",
            True,
            POLICY_DIGEST_FIELD,
        )
        result = self.build(values)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("resumption_consumption_policy_not_safe", result.issues)

    def test_policy_forbidden_git_effect_blocks(self):
        values = valid_inputs()
        self.mutate_and_reseal(
            values,
            "consumption_policy",
            "allow_git_effect_during_consumption",
            True,
            POLICY_DIGEST_FIELD,
        )
        result = self.build(values)
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_policy_forbidden_automatic_resumption_blocks(self):
        values = valid_inputs()
        self.mutate_and_reseal(
            values,
            "consumption_policy",
            "allow_automatic_resumption",
            True,
            POLICY_DIGEST_FIELD,
        )
        result = self.build(values)
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_policy_forbidden_network_blocks(self):
        values = valid_inputs()
        self.mutate_and_reseal(
            values,
            "consumption_policy",
            "allow_network_access",
            True,
            POLICY_DIGEST_FIELD,
        )
        result = self.build(values)
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_policy_forbidden_secret_read_blocks(self):
        values = valid_inputs()
        self.mutate_and_reseal(
            values,
            "consumption_policy",
            "allow_secret_material_read",
            True,
            POLICY_DIGEST_FIELD,
        )
        result = self.build(values)
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_policy_forbidden_general_successor_blocks(self):
        values = valid_inputs()
        self.mutate_and_reseal(
            values,
            "consumption_policy",
            "allow_general_successor_authority",
            True,
            POLICY_DIGEST_FIELD,
        )
        result = self.build(values)
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_effect_budget_excess_blocks(self):
        values = valid_inputs()
        values["consumption_policy"]["maximum_resume_effect_budget"] = 2
        seal(values["consumption_policy"], POLICY_DIGEST_FIELD)
        result = self.build(values)
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_command_budget_excess_blocks(self):
        values = valid_inputs()
        values["consumption_policy"]["maximum_resume_execution_command_budget"] = 5
        seal(values["consumption_policy"], POLICY_DIGEST_FIELD)
        result = self.build(values)
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_output_budget_excess_blocks(self):
        values = valid_inputs()
        values["consumption_policy"]["maximum_resume_execution_output_bytes"] = 5999
        seal(values["consumption_policy"], POLICY_DIGEST_FIELD)
        result = self.build(values)
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_request_must_explicitly_consume(self):
        values = valid_inputs()
        self.mutate_and_reseal(
            values,
            "consumption_request",
            "consume_resume_input",
            False,
            REQUEST_DIGEST_FIELD,
        )
        result = self.build(values)
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_request_must_explicitly_request_execution_input(self):
        values = valid_inputs()
        self.mutate_and_reseal(
            values,
            "consumption_request",
            "issue_execution_input",
            False,
            REQUEST_DIGEST_FIELD,
        )
        result = self.build(values)
        self.assertEqual(result.status, STATUS_BLOCKED)


if __name__ == "__main__":
    unittest.main()
