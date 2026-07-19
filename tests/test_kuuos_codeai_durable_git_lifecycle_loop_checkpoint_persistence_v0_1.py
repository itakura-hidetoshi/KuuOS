#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
import unittest

from runtime.kuuos_codeai_durable_git_lifecycle_loop_checkpoint_persistence_v0_1 import (
    ADAPTER_RESULT_DIGEST_FIELD,
    ADAPTER_STATUS_COMMITTED,
    ADAPTER_STATUS_CONFLICT,
    ADAPTER_STATUS_FAILED,
    CHECKPOINT_ENVELOPE_DIGEST_FIELD,
    DISPOSITION_CONFLICT,
    DISPOSITION_EVIDENCE_QUARANTINED,
    DISPOSITION_FAILED,
    DISPOSITION_PERSISTED,
    POLICY_DIGEST_FIELD,
    PROFILE_VERSION,
    RECEIPT_DIGEST_FIELD,
    REGISTRY_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    SCHEMA_VERSION,
    STATUS_BLOCKED,
    STATUS_READY,
    STORE_STATE_DIGEST_FIELD,
    build_codeai_durable_git_lifecycle_loop_checkpoint_persistence,
    canonical_digest,
)
from runtime.kuuos_codeai_bounded_autonomous_git_lifecycle_loop_orchestration_v0_1 import (
    EVIDENCE_DIGEST_FIELD as LOOP_EVIDENCE_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as LOOP_RECEIPT_DIGEST_FIELD,
    REGISTRY_DIGEST_FIELD as LOOP_REGISTRY_DIGEST_FIELD,
)
from runtime.kuuos_codeai_autonomous_git_effect_execution_types_v0_1 import (
    REGISTRY_DIGEST_FIELD as EXECUTION_REGISTRY_DIGEST_FIELD,
)
from runtime.kuuos_codeai_autonomous_git_effect_reobservation_v0_1 import (
    REGISTRY_DIGEST_FIELD as REOBSERVATION_REGISTRY_DIGEST_FIELD,
)
from runtime.kuuos_codeai_reobservation_gated_git_lifecycle_continuation_v0_1 import (
    REGISTRY_DIGEST_FIELD as CONTINUATION_REGISTRY_DIGEST_FIELD,
)
from runtime.kuuos_codeai_autonomous_git_lifecycle_envelope_v0_1 import (
    RECEIPT_DIGEST_FIELD as LIFECYCLE_RECEIPT_DIGEST_FIELD,
    STATE_DIGEST_FIELD as LIFECYCLE_STATE_DIGEST_FIELD,
)
from tests.test_kuuos_codeai_bounded_autonomous_git_lifecycle_loop_orchestration_v0_1 import (
    run_loop,
)


def seal(value: dict, field: str) -> dict:
    out = deepcopy(value)
    out.pop(field, None)
    out[field] = canonical_digest(out)
    return out


def fixture():
    loop = run_loop()
    assert loop.status == STATUS_READY
    assert loop.receipt is not None
    assert loop.evidence is not None
    assert loop.next_loop_registry is not None
    assert loop.next_execution_registry is not None
    assert loop.next_reobservation_registry is not None
    assert loop.next_continuation_registry is not None
    assert loop.final_lifecycle_receipt is not None
    assert loop.final_lifecycle_state is not None

    request = {
        "checkpoint_id": "git-loop-checkpoint-001",
        "checkpoint_revision": 1,
        "persistence_session_id": "git-loop-checkpoint-session-001",
        "persistence_nonce_digest": "d" * 64,
        "source_loop_receipt_digest": loop.receipt[LOOP_RECEIPT_DIGEST_FIELD],
        "source_loop_evidence_digest": loop.evidence[LOOP_EVIDENCE_DIGEST_FIELD],
        "source_loop_registry_digest": loop.next_loop_registry[LOOP_REGISTRY_DIGEST_FIELD],
        "source_execution_registry_digest": loop.next_execution_registry[EXECUTION_REGISTRY_DIGEST_FIELD],
        "source_reobservation_registry_digest": loop.next_reobservation_registry[REOBSERVATION_REGISTRY_DIGEST_FIELD],
        "source_continuation_registry_digest": loop.next_continuation_registry[CONTINUATION_REGISTRY_DIGEST_FIELD],
        "final_lifecycle_receipt_digest": loop.final_lifecycle_receipt[LIFECYCLE_RECEIPT_DIGEST_FIELD],
        "final_lifecycle_state_digest": loop.final_lifecycle_state[LIFECYCLE_STATE_DIGEST_FIELD],
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
    request = seal(request, REQUEST_DIGEST_FIELD)

    policy = {
        "expected_source_loop_receipt_digest": loop.receipt[LOOP_RECEIPT_DIGEST_FIELD],
        "expected_source_loop_evidence_digest": loop.evidence[LOOP_EVIDENCE_DIGEST_FIELD],
        "expected_repository_full_name": loop.receipt["repository_full_name"],
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
    policy = seal(policy, POLICY_DIGEST_FIELD)

    registry = seal({
        "registry_id": "checkpoint-persistence-registry-001",
        "registry_revision": 0,
        "consumed_persistence_nonce_digests": [],
        "persisted_loop_receipt_digests": [],
        "persisted_checkpoint_ids": [],
        "persistence_attempt_count": 0,
        "successful_persistence_count": 0,
        "last_persistence_epoch": 0,
    }, REGISTRY_DIGEST_FIELD)

    store_state = seal({
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "store_id": "codeai-git-loop-checkpoint-store",
        "store_revision": 0,
        "checkpoint_ids": [],
        "checkpoint_envelope_digests": [],
        "last_committed_epoch": 0,
    }, STORE_STATE_DIGEST_FIELD)

    return [
        loop.receipt,
        loop.evidence,
        loop.next_loop_registry,
        loop.next_execution_registry,
        loop.next_reobservation_registry,
        loop.next_continuation_registry,
        loop.final_lifecycle_receipt,
        loop.final_lifecycle_state,
        request,
        policy,
        registry,
        store_state,
    ]


def adapter_result(invocation, *, status=ADAPTER_STATUS_COMMITTED, mutate=None):
    if status == ADAPTER_STATUS_COMMITTED:
        observed = invocation.expected_store_revision
        committed = observed + 1
        cas_succeeded = True
        absent = True
        write_committed = True
        exception_type = ""
    elif status == ADAPTER_STATUS_CONFLICT:
        observed = invocation.expected_store_revision + 1
        committed = observed
        cas_succeeded = False
        absent = False
        write_committed = False
        exception_type = ""
    else:
        observed = invocation.expected_store_revision
        committed = observed
        cas_succeeded = False
        absent = True
        write_committed = False
        exception_type = "StoreError"
    value = {
        "adapter_id": invocation.adapter_id,
        "adapter_session_id": invocation.persistence_session_id,
        "store_id": invocation.store_id,
        "checkpoint_id": invocation.checkpoint_id,
        "expected_store_revision": invocation.expected_store_revision,
        "observed_store_revision": observed,
        "committed_store_revision": committed,
        "checkpoint_envelope_digest": invocation.checkpoint_envelope_digest,
        "status": status,
        "command_count": 1,
        "output_bytes": 512,
        "completed_epoch": 400,
        "atomic_compare_and_swap_attempted": True,
        "atomic_compare_and_swap_succeeded": cas_succeeded,
        "checkpoint_absent_before_write": absent,
        "write_committed": write_committed,
        "checkpoint_overwritten": False,
        "checkpoint_deleted": False,
        "network_accessed": False,
        "secret_material_read": False,
        "git_effect_performed": False,
        "loop_executed": False,
        "resume_input_issued": False,
        "arbitrary_command_executed": False,
        "exception_type": exception_type,
    }
    if mutate is not None:
        mutate(value)
    return seal(value, ADAPTER_RESULT_DIGEST_FIELD)


def run_persistence(*, mutate=None, adapter=None):
    values = fixture()
    if mutate is not None:
        mutate(values)
    selected_adapter = adapter or (lambda invocation: adapter_result(invocation))
    return build_codeai_durable_git_lifecycle_loop_checkpoint_persistence(
        source_loop_receipt=values[0],
        source_loop_evidence=values[1],
        source_loop_registry=values[2],
        source_execution_registry=values[3],
        source_reobservation_registry=values[4],
        source_continuation_registry=values[5],
        final_lifecycle_receipt=values[6],
        final_lifecycle_state=values[7],
        persistence_request=values[8],
        persistence_policy=values[9],
        persistence_registry=values[10],
        checkpoint_store_state=values[11],
        adapter=selected_adapter,
    )


class DurableCheckpointPersistenceTests(unittest.TestCase):
    def test_successful_compare_and_swap_persists_checkpoint(self):
        result = run_persistence()
        self.assertEqual(result.status, STATUS_READY, result.issues)
        self.assertEqual(result.receipt["codeai_disposition"], DISPOSITION_PERSISTED)
        self.assertTrue(result.receipt["checkpoint_persisted"])
        self.assertEqual(result.next_store_state["store_revision"], 1)

    def test_receipt_digest_is_canonical(self):
        result = run_persistence()
        self.assertEqual(
            result.receipt[RECEIPT_DIGEST_FIELD],
            canonical_digest({k: v for k, v in result.receipt.items() if k != RECEIPT_DIGEST_FIELD}),
        )

    def test_checkpoint_envelope_digest_is_canonical(self):
        result = run_persistence()
        self.assertEqual(
            result.checkpoint_envelope[CHECKPOINT_ENVELOPE_DIGEST_FIELD],
            canonical_digest({k: v for k, v in result.checkpoint_envelope.items() if k != CHECKPOINT_ENVELOPE_DIGEST_FIELD}),
        )

    def test_registry_advances_once_and_consumes_nonce(self):
        result = run_persistence()
        self.assertEqual(result.next_registry["registry_revision"], 1)
        self.assertEqual(result.next_registry["persistence_attempt_count"], 1)
        self.assertEqual(result.next_registry["successful_persistence_count"], 1)
        self.assertEqual(len(result.next_registry["consumed_persistence_nonce_digests"]), 1)

    def test_store_state_appends_exact_checkpoint(self):
        result = run_persistence()
        self.assertEqual(result.next_store_state["checkpoint_ids"], ["git-loop-checkpoint-001"])
        self.assertEqual(
            result.next_store_state["checkpoint_envelope_digests"],
            [result.checkpoint_envelope[CHECKPOINT_ENVELOPE_DIGEST_FIELD]],
        )

    def test_persistence_grants_no_resumption_or_general_authority(self):
        result = run_persistence()
        self.assertFalse(result.receipt["resume_input_issued"])
        self.assertFalse(result.receipt["automatic_resumption_performed"])
        self.assertFalse(result.receipt["general_git_authority_granted"])
        self.assertFalse(result.receipt["general_successor_stage_authority_granted"])

    def test_compare_and_swap_conflict_is_recorded_without_store_advance(self):
        result = run_persistence(adapter=lambda invocation: adapter_result(invocation, status=ADAPTER_STATUS_CONFLICT))
        self.assertEqual(result.status, STATUS_READY, result.issues)
        self.assertEqual(result.receipt["codeai_disposition"], DISPOSITION_CONFLICT)
        self.assertEqual(result.next_store_state["store_revision"], 0)
        self.assertEqual(result.next_registry["successful_persistence_count"], 0)

    def test_adapter_failure_is_recorded_without_store_advance(self):
        result = run_persistence(adapter=lambda invocation: adapter_result(invocation, status=ADAPTER_STATUS_FAILED))
        self.assertEqual(result.receipt["codeai_disposition"], DISPOSITION_FAILED)
        self.assertEqual(result.next_store_state["store_revision"], 0)

    def test_adapter_exception_is_converted_to_failed_receipt(self):
        def boom(_):
            raise RuntimeError("boom")
        result = run_persistence(adapter=boom)
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.receipt["codeai_disposition"], DISPOSITION_FAILED)
        self.assertEqual(result.evidence["adapter_result"]["exception_type"], "RuntimeError")

    def test_non_mapping_adapter_result_is_quarantined(self):
        result = run_persistence(adapter=lambda _: "not-a-mapping")
        self.assertEqual(result.receipt["codeai_disposition"], DISPOSITION_EVIDENCE_QUARANTINED)
        self.assertTrue(result.receipt["checkpoint_evidence_quarantined"])

    def test_malformed_adapter_digest_is_quarantined(self):
        def bad(invocation):
            value = adapter_result(invocation)
            value[ADAPTER_RESULT_DIGEST_FIELD] = "0" * 64
            return value
        result = run_persistence(adapter=bad)
        self.assertEqual(result.receipt["codeai_disposition"], DISPOSITION_EVIDENCE_QUARANTINED)

    def test_forbidden_adapter_effect_is_quarantined(self):
        result = run_persistence(
            adapter=lambda invocation: adapter_result(
                invocation, mutate=lambda value: value.__setitem__("git_effect_performed", True)
            )
        )
        self.assertEqual(result.receipt["codeai_disposition"], DISPOSITION_EVIDENCE_QUARANTINED)

    def test_request_digest_tamper_blocks(self):
        result = run_persistence(mutate=lambda values: values[8].__setitem__("repository_full_name", "other/repo"))
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIsNone(result.receipt)

    def test_resealed_request_correspondence_mismatch_blocks(self):
        def mutate(values):
            values[8]["repository_full_name"] = "other/repo"
            values[8] = seal(values[8], REQUEST_DIGEST_FIELD)
        result = run_persistence(mutate=mutate)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("checkpoint_persistence_correspondence_mismatch", result.issues)

    def test_stale_request_blocks(self):
        def mutate(values):
            values[8]["request_created_epoch"] = 1
            values[8] = seal(values[8], REQUEST_DIGEST_FIELD)
        result = run_persistence(mutate=mutate)
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_nonce_replay_blocks(self):
        def mutate(values):
            values[10]["consumed_persistence_nonce_digests"] = [values[8]["persistence_nonce_digest"]]
            values[10]["persistence_attempt_count"] = 1
            values[10] = seal(values[10], REGISTRY_DIGEST_FIELD)
        result = run_persistence(mutate=mutate)
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_loop_receipt_replay_blocks(self):
        def mutate(values):
            values[10]["consumed_persistence_nonce_digests"] = ["e" * 64]
            values[10]["persisted_loop_receipt_digests"] = [values[0][LOOP_RECEIPT_DIGEST_FIELD]]
            values[10]["persisted_checkpoint_ids"] = ["old-checkpoint"]
            values[10]["persistence_attempt_count"] = 1
            values[10]["successful_persistence_count"] = 1
            values[11]["store_revision"] = 1
            values[11]["checkpoint_ids"] = ["old-checkpoint"]
            values[11]["checkpoint_envelope_digests"] = ["f" * 64]
            values[8]["expected_store_revision"] = 1
            values[8] = seal(values[8], REQUEST_DIGEST_FIELD)
            values[10] = seal(values[10], REGISTRY_DIGEST_FIELD)
            values[11] = seal(values[11], STORE_STATE_DIGEST_FIELD)
        result = run_persistence(mutate=mutate)
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_checkpoint_id_replay_blocks(self):
        def mutate(values):
            values[10]["consumed_persistence_nonce_digests"] = ["e" * 64]
            values[10]["persisted_loop_receipt_digests"] = ["f" * 64]
            values[10]["persisted_checkpoint_ids"] = [values[8]["checkpoint_id"]]
            values[10]["persistence_attempt_count"] = 1
            values[10]["successful_persistence_count"] = 1
            values[11]["store_revision"] = 1
            values[11]["checkpoint_ids"] = [values[8]["checkpoint_id"]]
            values[11]["checkpoint_envelope_digests"] = ["a" * 64]
            values[8]["expected_store_revision"] = 1
            values[8] = seal(values[8], REQUEST_DIGEST_FIELD)
            values[10] = seal(values[10], REGISTRY_DIGEST_FIELD)
            values[11] = seal(values[11], STORE_STATE_DIGEST_FIELD)
        result = run_persistence(mutate=mutate)
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_store_id_mismatch_blocks(self):
        def mutate(values):
            values[8]["store_id"] = "other-store"
            values[8] = seal(values[8], REQUEST_DIGEST_FIELD)
        result = run_persistence(mutate=mutate)
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_expected_revision_mismatch_blocks(self):
        def mutate(values):
            values[8]["expected_store_revision"] = 2
            values[8] = seal(values[8], REQUEST_DIGEST_FIELD)
        result = run_persistence(mutate=mutate)
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_network_permission_blocks(self):
        def mutate(values):
            values[9]["allow_network_access"] = True
            values[9] = seal(values[9], POLICY_DIGEST_FIELD)
        result = run_persistence(mutate=mutate)
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_loop_execution_permission_blocks(self):
        def mutate(values):
            values[9]["allow_loop_execution"] = True
            values[9] = seal(values[9], POLICY_DIGEST_FIELD)
        result = run_persistence(mutate=mutate)
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_resume_input_permission_blocks(self):
        def mutate(values):
            values[9]["allow_resume_input_issuance"] = True
            values[9] = seal(values[9], POLICY_DIGEST_FIELD)
        result = run_persistence(mutate=mutate)
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_overwrite_permission_blocks(self):
        def mutate(values):
            values[9]["allow_checkpoint_overwrite"] = True
            values[9] = seal(values[9], POLICY_DIGEST_FIELD)
        result = run_persistence(mutate=mutate)
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_source_loop_receipt_tamper_blocks(self):
        result = run_persistence(mutate=lambda values: values[0].__setitem__("effect_count", 99))
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_final_lifecycle_state_tamper_blocks(self):
        result = run_persistence(mutate=lambda values: values[7].__setitem__("mergeable", False))
        self.assertEqual(result.status, STATUS_BLOCKED)


if __name__ == "__main__":
    unittest.main()
