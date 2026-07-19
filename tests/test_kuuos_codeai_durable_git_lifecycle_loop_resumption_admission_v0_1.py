#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
import unittest

from runtime.kuuos_codeai_durable_git_lifecycle_loop_checkpoint_persistence_v0_1 import (
    ADAPTER_RESULT_DIGEST_FIELD as PERSISTENCE_ADAPTER_RESULT_DIGEST_FIELD,
    POLICY_DIGEST_FIELD as PERSISTENCE_POLICY_DIGEST_FIELD,
    REGISTRY_DIGEST_FIELD as PERSISTENCE_REGISTRY_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD as PERSISTENCE_REQUEST_DIGEST_FIELD,
    STORE_STATE_DIGEST_FIELD,
    STATUS_READY as PERSISTENCE_READY,
    build_codeai_durable_git_lifecycle_loop_checkpoint_persistence,
    canonical_digest,
)
from runtime.kuuos_codeai_durable_git_lifecycle_loop_resumption_admission_v0_1 import (
    ADAPTER_STATUS_FAILED,
    ADAPTER_STATUS_UNAVAILABLE,
    ADAPTER_STATUS_VERIFIED,
    DISPOSITION_ADMITTED,
    DISPOSITION_EVIDENCE_QUARANTINED,
    DISPOSITION_FAILED,
    DISPOSITION_UNAVAILABLE,
    POLICY_DIGEST_FIELD,
    READ_RESULT_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD,
    REGISTRY_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    RESUME_INPUT_DIGEST_FIELD,
    STATUS_BLOCKED,
    STATUS_READY,
    build_codeai_durable_git_lifecycle_loop_resumption_admission,
)
from tests.test_kuuos_codeai_bounded_autonomous_git_lifecycle_loop_orchestration_v0_1 import (
    run_loop,
)


def seal(value: dict, field: str) -> dict:
    out = deepcopy(value)
    out.pop(field, None)
    out[field] = canonical_digest(out)
    return out


def committed_persistence_bundle():
    loop = run_loop()
    assert loop.status == STATUS_READY and loop.receipt is not None
    request = {
        "checkpoint_id": "git-loop-checkpoint-001",
        "checkpoint_revision": 1,
        "persistence_session_id": "git-loop-checkpoint-session-001",
        "persistence_nonce_digest": "d" * 64,
        "source_loop_receipt_digest": loop.receipt["codeai_bounded_autonomous_git_lifecycle_loop_receipt_digest"],
        "source_loop_evidence_digest": loop.evidence["codeai_bounded_autonomous_git_lifecycle_loop_evidence_digest"],
        "source_loop_registry_digest": loop.next_loop_registry["codeai_bounded_autonomous_git_lifecycle_loop_registry_digest"],
        "source_execution_registry_digest": loop.next_execution_registry["codeai_autonomous_git_effect_execution_registry_digest"],
        "source_reobservation_registry_digest": loop.next_reobservation_registry["codeai_autonomous_git_effect_reobservation_registry_digest"],
        "source_continuation_registry_digest": loop.next_continuation_registry["codeai_reobservation_gated_git_lifecycle_continuation_registry_digest"],
        "final_lifecycle_receipt_digest": loop.final_lifecycle_receipt["codeai_autonomous_git_lifecycle_receipt_digest"],
        "final_lifecycle_state_digest": loop.final_lifecycle_state["codeai_autonomous_git_lifecycle_state_digest"],
        "loop_id": loop.receipt["loop_id"],
        "lifecycle_id": loop.receipt["lifecycle_id"],
        "repository_full_name": loop.receipt["repository_full_name"],
        "persister_id": "codeai-checkpoint-persister",
        "adapter_id": "durable-checkpoint-store-adapter",
        "store_id": "codeai-git-loop-checkpoint-store",
        "expected_store_revision": 0,
        "request_created_epoch": 400,
        "provenance_integrity_confirmed": True,
        "source_correspondence_confirmed": True,
        "persistence_requested": True,
    }
    request = seal(request, PERSISTENCE_REQUEST_DIGEST_FIELD)
    policy = {
        "expected_source_loop_receipt_digest": request["source_loop_receipt_digest"],
        "expected_source_loop_evidence_digest": request["source_loop_evidence_digest"],
        "expected_repository_full_name": request["repository_full_name"],
        "authorized_persister_ids": ["codeai-checkpoint-persister"],
        "allowed_adapter_ids": ["durable-checkpoint-store-adapter"],
        "allowed_store_ids": ["codeai-git-loop-checkpoint-store"],
        "maximum_request_age": 100,
        "maximum_registry_entries": 16,
        "maximum_store_entries": 16,
        "maximum_adapter_command_count": 1,
        "maximum_adapter_output_bytes": 4096,
        "evaluation_epoch": 400,
        "allow_checkpoint_persistence": True,
        "require_atomic_compare_and_swap": True,
        "require_checkpoint_absence": True,
        "require_nonce_consumption": True,
        "allow_checkpoint_overwrite": False,
        "allow_checkpoint_delete": False,
        "allow_network_access": False,
        "allow_secret_material_read": False,
        "allow_git_effect": False,
        "allow_loop_execution": False,
        "allow_resume_input_issuance": False,
        "allow_automatic_resumption": False,
        "allow_general_successor_authority": False,
    }
    policy = seal(policy, PERSISTENCE_POLICY_DIGEST_FIELD)
    registry = seal({
        "registry_id": "checkpoint-persistence-registry-001",
        "registry_revision": 0,
        "consumed_persistence_nonce_digests": [],
        "persisted_loop_receipt_digests": [],
        "persisted_checkpoint_ids": [],
        "persistence_attempt_count": 0,
        "successful_persistence_count": 0,
        "last_persistence_epoch": 0,
    }, PERSISTENCE_REGISTRY_DIGEST_FIELD)
    store = seal({
        "schema_version": "v0.1",
        "profile_version": "CodeAI Durable Git Lifecycle Loop Checkpoint Persistence v0.1",
        "store_id": "codeai-git-loop-checkpoint-store",
        "store_revision": 0,
        "checkpoint_ids": [],
        "checkpoint_envelope_digests": [],
        "last_committed_epoch": 0,
    }, STORE_STATE_DIGEST_FIELD)

    captured = {}
    def adapter(invocation):
        captured["envelope"] = dict(invocation.checkpoint_envelope)
        value = {
            "adapter_id": invocation.adapter_id,
            "adapter_session_id": invocation.persistence_session_id,
            "store_id": invocation.store_id,
            "checkpoint_id": invocation.checkpoint_id,
            "expected_store_revision": invocation.expected_store_revision,
            "observed_store_revision": invocation.expected_store_revision,
            "committed_store_revision": invocation.expected_store_revision + 1,
            "checkpoint_envelope_digest": invocation.checkpoint_envelope_digest,
            "status": "committed",
            "command_count": 1,
            "output_bytes": 256,
            "completed_epoch": 400,
            "atomic_compare_and_swap_attempted": True,
            "atomic_compare_and_swap_succeeded": True,
            "checkpoint_absent_before_write": True,
            "write_committed": True,
            "checkpoint_overwritten": False,
            "checkpoint_deleted": False,
            "network_accessed": False,
            "secret_material_read": False,
            "git_effect_performed": False,
            "loop_executed": False,
            "resume_input_issued": False,
            "arbitrary_command_executed": False,
            "exception_type": "",
        }
        return seal(value, PERSISTENCE_ADAPTER_RESULT_DIGEST_FIELD)

    result = build_codeai_durable_git_lifecycle_loop_checkpoint_persistence(
        source_loop_receipt=loop.receipt,
        source_loop_evidence=loop.evidence,
        source_loop_registry=loop.next_loop_registry,
        source_execution_registry=loop.next_execution_registry,
        source_reobservation_registry=loop.next_reobservation_registry,
        source_continuation_registry=loop.next_continuation_registry,
        final_lifecycle_receipt=loop.final_lifecycle_receipt,
        final_lifecycle_state=loop.final_lifecycle_state,
        persistence_request=request,
        persistence_policy=policy,
        persistence_registry=registry,
        checkpoint_store_state=store,
        adapter=adapter,
    )
    assert result.status == PERSISTENCE_READY and result.receipt is not None
    return result, captured["envelope"]


def admission_fixture():
    persistence, envelope = committed_persistence_bundle()
    request = {
        "resumption_session_id": "git-loop-resumption-session-001",
        "resumption_nonce_digest": "e" * 64,
        "checkpoint_id": persistence.receipt["checkpoint_id"],
        "checkpoint_envelope_digest": persistence.receipt["checkpoint_envelope_digest"],
        "source_persistence_receipt_digest": persistence.receipt["codeai_durable_git_lifecycle_loop_checkpoint_persistence_receipt_digest"],
        "source_persistence_evidence_digest": persistence.evidence["codeai_durable_git_lifecycle_loop_checkpoint_persistence_evidence_digest"],
        "source_persistence_registry_digest": persistence.next_registry[PERSISTENCE_REGISTRY_DIGEST_FIELD],
        "source_store_state_digest": persistence.next_store_state[STORE_STATE_DIGEST_FIELD],
        "loop_id": persistence.receipt["loop_id"],
        "lifecycle_id": persistence.receipt["lifecycle_id"],
        "repository_full_name": persistence.receipt["repository_full_name"],
        "store_id": persistence.receipt["store_id"],
        "reader_id": "codeai-checkpoint-reader",
        "adapter_id": "durable-checkpoint-read-adapter",
        "requested_resume_effect_budget": 3,
        "requested_resume_execution_command_budget": 6,
        "requested_resume_execution_output_bytes": 6000,
        "request_created_epoch": 500,
        "provenance_integrity_confirmed": True,
        "source_correspondence_confirmed": True,
        "checkpoint_read_requested": True,
        "resumption_input_requested": True,
    }
    request = seal(request, REQUEST_DIGEST_FIELD)
    policy = {
        "expected_source_persistence_receipt_digest": request["source_persistence_receipt_digest"],
        "expected_source_persistence_evidence_digest": request["source_persistence_evidence_digest"],
        "expected_checkpoint_envelope_digest": request["checkpoint_envelope_digest"],
        "expected_repository_full_name": request["repository_full_name"],
        "authorized_reader_ids": ["codeai-checkpoint-reader"],
        "allowed_adapter_ids": ["durable-checkpoint-read-adapter"],
        "allowed_store_ids": [request["store_id"]],
        "maximum_request_age": 100,
        "maximum_registry_entries": 16,
        "maximum_adapter_command_count": 1,
        "maximum_adapter_output_bytes": 8192,
        "maximum_resume_effect_budget": 5,
        "maximum_resume_execution_command_budget": 10,
        "maximum_resume_execution_output_bytes": 10000,
        "evaluation_epoch": 500,
        "allow_checkpoint_read": True,
        "require_committed_checkpoint": True,
        "require_exact_checkpoint_envelope_digest": True,
        "require_nonce_consumption": True,
        "allow_resumption_input_issuance": True,
        "allow_loop_execution": False,
        "allow_git_effect": False,
        "allow_automatic_resumption": False,
        "allow_network_access": False,
        "allow_secret_material_read": False,
        "allow_general_successor_authority": False,
    }
    policy = seal(policy, POLICY_DIGEST_FIELD)
    registry = seal({
        "registry_id": "git-loop-resumption-registry-001",
        "registry_revision": 0,
        "consumed_resumption_nonce_digests": [],
        "admitted_checkpoint_ids": [],
        "admitted_checkpoint_envelope_digests": [],
        "admitted_persistence_receipt_digests": [],
        "resumption_attempt_count": 0,
        "successful_resumption_admission_count": 0,
        "last_resumption_epoch": 0,
    }, REGISTRY_DIGEST_FIELD)
    return persistence, envelope, request, policy, registry


def read_result(invocation, envelope, *, status=ADAPTER_STATUS_VERIFIED, **overrides):
    value = {
        "adapter_id": invocation.adapter_id,
        "adapter_session_id": invocation.resumption_session_id,
        "store_id": invocation.store_id,
        "checkpoint_id": invocation.checkpoint_id,
        "checkpoint_envelope_digest": invocation.checkpoint_envelope_digest,
        "checkpoint_envelope": deepcopy(envelope) if status == ADAPTER_STATUS_VERIFIED else None,
        "status": status,
        "command_count": 1,
        "output_bytes": 1024,
        "completed_epoch": 500,
        "checkpoint_found": status == ADAPTER_STATUS_VERIFIED,
        "checkpoint_read_performed": status != ADAPTER_STATUS_FAILED,
        "network_accessed": False,
        "secret_material_read": False,
        "git_effect_performed": False,
        "loop_executed": False,
        "resume_input_issued": False,
        "arbitrary_command_executed": False,
        "exception_type": "",
    }
    value.update(overrides)
    return seal(value, READ_RESULT_DIGEST_FIELD)


def run_admission(*, mutate=None, adapter_mode="verified"):
    persistence, envelope, request, policy, registry = admission_fixture()
    values = [persistence, envelope, request, policy, registry]
    if mutate:
        mutate(values)
    def adapter(invocation):
        if adapter_mode == "exception":
            raise RuntimeError("read failed")
        if adapter_mode == "unavailable":
            return read_result(invocation, values[1], status=ADAPTER_STATUS_UNAVAILABLE,
                               checkpoint_found=False, checkpoint_read_performed=True)
        if adapter_mode == "failed":
            return read_result(invocation, values[1], status=ADAPTER_STATUS_FAILED,
                               checkpoint_found=False, checkpoint_read_performed=False,
                               exception_type="StoreFailure")
        if adapter_mode == "bad_digest":
            result = read_result(invocation, values[1])
            result["checkpoint_envelope_digest"] = "f" * 64
            return seal(result, READ_RESULT_DIGEST_FIELD)
        if adapter_mode == "effect":
            return read_result(invocation, values[1], network_accessed=True)
        return read_result(invocation, values[1])
    return build_codeai_durable_git_lifecycle_loop_resumption_admission(
        persistence_receipt=values[0].receipt,
        persistence_evidence=values[0].evidence,
        persistence_registry=values[0].next_registry,
        checkpoint_store_state=values[0].next_store_state,
        resumption_request=values[2],
        resumption_policy=values[3],
        resumption_registry=values[4],
        read_adapter=adapter,
    )


class DurableGitLifecycleLoopResumptionAdmissionTests(unittest.TestCase):
    def test_verified_read_issues_one_future_only_resume_input(self):
        result = run_admission()
        self.assertEqual(result.status, STATUS_READY, result.issues)
        self.assertEqual(result.receipt["codeai_disposition"], DISPOSITION_ADMITTED)
        self.assertTrue(result.receipt["resume_input_issued"])
        self.assertIsNotNone(result.resume_input)
        self.assertFalse(result.resume_input["active_now"])
        self.assertFalse(result.resume_input["loop_execution_authorized"])
        self.assertFalse(result.resume_input["git_effect_authorized"])
        self.assertEqual(result.next_registry["successful_resumption_admission_count"], 1)

    def test_resume_input_digest_is_canonical(self):
        result = run_admission()
        self.assertEqual(result.resume_input[RESUME_INPUT_DIGEST_FIELD], canonical_digest({
            k: v for k, v in result.resume_input.items() if k != RESUME_INPUT_DIGEST_FIELD
        }))

    def test_receipt_digest_is_canonical(self):
        result = run_admission()
        self.assertEqual(result.receipt[RECEIPT_DIGEST_FIELD], canonical_digest({
            k: v for k, v in result.receipt.items() if k != RECEIPT_DIGEST_FIELD
        }))

    def test_unavailable_consumes_nonce_but_not_checkpoint(self):
        result = run_admission(adapter_mode="unavailable")
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.receipt["codeai_disposition"], DISPOSITION_UNAVAILABLE)
        self.assertFalse(result.receipt["resume_input_issued"])
        self.assertIsNone(result.resume_input)
        self.assertEqual(result.next_registry["resumption_attempt_count"], 1)
        self.assertEqual(result.next_registry["successful_resumption_admission_count"], 0)
        self.assertEqual(result.next_registry["admitted_checkpoint_ids"], [])

    def test_failed_read_preserves_success_history(self):
        result = run_admission(adapter_mode="failed")
        self.assertEqual(result.receipt["codeai_disposition"], DISPOSITION_FAILED)
        self.assertEqual(result.next_registry["successful_resumption_admission_count"], 0)

    def test_adapter_exception_is_sealed_failed(self):
        result = run_admission(adapter_mode="exception")
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.receipt["codeai_disposition"], DISPOSITION_FAILED)
        self.assertFalse(result.receipt["resume_input_issued"])

    def test_bad_adapter_digest_is_quarantined(self):
        result = run_admission(adapter_mode="bad_digest")
        self.assertEqual(result.receipt["codeai_disposition"], DISPOSITION_EVIDENCE_QUARANTINED)
        self.assertFalse(result.receipt["resume_input_issued"])

    def test_effect_bearing_read_is_quarantined(self):
        result = run_admission(adapter_mode="effect")
        self.assertEqual(result.receipt["codeai_disposition"], DISPOSITION_EVIDENCE_QUARANTINED)

    def test_request_tamper_blocks_before_read(self):
        def mutate(values):
            values[2]["repository_full_name"] = "other/repo"
        result = run_admission(mutate=mutate)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIsNone(result.receipt)

    def test_resealed_request_correspondence_tamper_blocks(self):
        def mutate(values):
            values[2]["checkpoint_id"] = "other-checkpoint"
            values[2] = seal(values[2], REQUEST_DIGEST_FIELD)
        result = run_admission(mutate=mutate)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("resumption_admission_correspondence_mismatch", result.issues)

    def test_uncommitted_persistence_receipt_blocks(self):
        def mutate(values):
            receipt = values[0].receipt
            receipt["checkpoint_persisted"] = False
            resealed = seal(receipt, "codeai_durable_git_lifecycle_loop_checkpoint_persistence_receipt_digest")
            receipt.clear()
            receipt.update(resealed)
        result = run_admission(mutate=mutate)
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_stale_request_blocks(self):
        def mutate(values):
            values[2]["request_created_epoch"] = 300
            values[2] = seal(values[2], REQUEST_DIGEST_FIELD)
        result = run_admission(mutate=mutate)
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_nonce_replay_blocks(self):
        def mutate(values):
            values[4]["consumed_resumption_nonce_digests"] = [values[2]["resumption_nonce_digest"]]
            values[4]["registry_revision"] = 1
            values[4]["resumption_attempt_count"] = 1
            values[4] = seal(values[4], REGISTRY_DIGEST_FIELD)
        result = run_admission(mutate=mutate)
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_checkpoint_replay_blocks(self):
        def mutate(values):
            values[4]["consumed_resumption_nonce_digests"] = ["1" * 64]
            values[4]["admitted_checkpoint_ids"] = [values[2]["checkpoint_id"]]
            values[4]["admitted_checkpoint_envelope_digests"] = [values[2]["checkpoint_envelope_digest"]]
            values[4]["admitted_persistence_receipt_digests"] = [values[2]["source_persistence_receipt_digest"]]
            values[4]["registry_revision"] = 1
            values[4]["resumption_attempt_count"] = 1
            values[4]["successful_resumption_admission_count"] = 1
            values[4] = seal(values[4], REGISTRY_DIGEST_FIELD)
        result = run_admission(mutate=mutate)
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_automatic_resumption_policy_is_rejected(self):
        def mutate(values):
            values[3]["allow_automatic_resumption"] = True
            values[3] = seal(values[3], POLICY_DIGEST_FIELD)
        result = run_admission(mutate=mutate)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("resumption_admission_policy_not_safe", result.issues)

    def test_git_effect_policy_is_rejected(self):
        def mutate(values):
            values[3]["allow_git_effect"] = True
            values[3] = seal(values[3], POLICY_DIGEST_FIELD)
        result = run_admission(mutate=mutate)
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_resume_budget_exceeding_policy_blocks(self):
        def mutate(values):
            values[2]["requested_resume_effect_budget"] = 6
            values[2] = seal(values[2], REQUEST_DIGEST_FIELD)
        result = run_admission(mutate=mutate)
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_missing_request_field_blocks(self):
        def mutate(values):
            del values[2]["reader_id"]
        result = run_admission(mutate=mutate)
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_extra_policy_field_blocks(self):
        def mutate(values):
            values[3]["extra"] = True
        result = run_admission(mutate=mutate)
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_parallel_registry_history_mismatch_blocks(self):
        def mutate(values):
            values[4]["admitted_checkpoint_ids"] = [values[2]["checkpoint_id"]]
            values[4] = seal(values[4], REGISTRY_DIGEST_FIELD)
        result = run_admission(mutate=mutate)
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_source_store_tamper_blocks(self):
        def mutate(values):
            values[0].next_store_state["store_revision"] = 2
        result = run_admission(mutate=mutate)
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_source_evidence_tamper_blocks(self):
        def mutate(values):
            values[0].evidence["loop_reexecuted"] = True
        result = run_admission(mutate=mutate)
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_success_grants_no_general_authority(self):
        result = run_admission()
        self.assertFalse(result.receipt["general_git_authority_granted"])
        self.assertFalse(result.receipt["general_successor_stage_authority_granted"])
        self.assertFalse(result.receipt["active_now"])
        self.assertFalse(result.receipt["automatic_resumption_performed"])


if __name__ == "__main__":
    unittest.main()
