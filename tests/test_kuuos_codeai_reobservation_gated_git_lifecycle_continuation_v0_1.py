from __future__ import annotations

from copy import deepcopy
import unittest

from scripts.check_codeai_autonomous_git_lifecycle_envelope_v0_1 import (
    load_example,
    reseal_policy as reseal_lifecycle_policy,
    reseal_request as reseal_lifecycle_request,
    reseal_state as reseal_lifecycle_state,
)
from runtime.kuuos_codeai_autonomous_git_lifecycle_envelope_v0_1 import (
    PHASE_LOCAL_COMMIT,
    PHASE_PUSH,
    RECEIPT_DIGEST_FIELD as LIFECYCLE_RECEIPT_DIGEST_FIELD,
    build_codeai_autonomous_git_lifecycle_envelope,
)
from runtime.kuuos_codeai_autonomous_git_effect_execution_v0_1 import (
    POLICY_DIGEST_FIELD as EXECUTION_POLICY_DIGEST_FIELD,
    REGISTRY_DIGEST_FIELD as EXECUTION_REGISTRY_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD as EXECUTION_REQUEST_DIGEST_FIELD,
    build_codeai_autonomous_git_effect_execution,
)
from runtime.kuuos_codeai_autonomous_git_effect_reobservation_v0_1 import (
    POLICY_DIGEST_FIELD as REOBSERVATION_POLICY_DIGEST_FIELD,
    REGISTRY_DIGEST_FIELD as REOBSERVATION_REGISTRY_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD as REOBSERVATION_REQUEST_DIGEST_FIELD,
    build_codeai_autonomous_git_effect_reobservation,
)
from runtime.kuuos_codeai_reobservation_gated_git_lifecycle_continuation_v0_1 import (
    POLICY_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD,
    REGISTRY_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    STATUS_BLOCKED,
    STATUS_READY,
    build_codeai_reobservation_gated_git_lifecycle_continuation,
    canonical_digest,
)

COMMIT_SHA = "b" * 40
CONTINUATION_NONCE = "e" * 64


def seal(value: dict, field: str) -> dict:
    result = deepcopy(value)
    result.pop(field, None)
    result[field] = canonical_digest(result)
    return result


def execution_adapter(invocation):
    return {
        "adapter_id": "continuation-fixture-git-adapter",
        "adapter_session_id": "continuation-fixture-git-adapter-session",
        "effect_phase": invocation.effect_phase,
        "status": "completed",
        "exit_code": 0,
        "command_count": 1,
        "stdout": "committed",
        "stderr": "",
        "completed_epoch": 109,
        "local_commit_created": True,
        "local_commit_sha": COMMIT_SHA,
        "local_commit_parent_sha": invocation.source_commit_sha,
        "branch_pushed": False,
        "pushed_head_sha": "",
        "pull_request_created": False,
        "pull_request_number": 0,
        "pull_request_url_digest": "",
        "pull_request_draft": False,
        "pr_head_sha": "",
        "pr_base_branch": "",
        "pull_request_marked_ready": False,
        "merge_performed": False,
        "merged_head_sha": "",
        "merge_commit_sha": "",
        "force_push_performed": False,
        "remote_branch_deleted": False,
        "admin_merge_bypass_used": False,
        "deployment_performed": False,
        "secret_material_read": False,
        "token_material_emitted": False,
        "opaque_token_used": False,
        "exception_type": "",
    }


def observation_adapter(invocation, source_lifecycle_receipt):
    return {
        "adapter_id": "continuation-fixture-read-only-observer",
        "adapter_session_id": "continuation-fixture-observer-session",
        "status": "observed",
        "command_count": 4,
        "output_bytes": 4096,
        "completed_epoch": 209,
        "network_accessed": False,
        "secret_material_read": False,
        "git_write_performed": False,
        "deployment_performed": False,
        "exception_type": "",
        "lifecycle_id": invocation.lifecycle_id,
        "source_trajectory_receipt_digest": source_lifecycle_receipt["source_trajectory_receipt_digest"],
        "repository_full_name": invocation.repository_full_name,
        "source_commit_sha": invocation.source_commit_sha,
        "executor_id": source_lifecycle_receipt["executor_id"],
        "base_branch": invocation.base_branch,
        "head_branch": invocation.head_branch,
        "remote_name": invocation.remote_name,
        "change_set_digest": invocation.change_set_digest,
        "commit_message_digest": invocation.commit_message_digest,
        "merge_method": invocation.merge_method,
        "local_commit_created": True,
        "local_commit_sha": COMMIT_SHA,
        "local_commit_parent_sha": invocation.source_commit_sha,
        "branch_pushed": False,
        "pushed_head_sha": "",
        "pull_request_created": False,
        "pull_request_number": 0,
        "pull_request_url_digest": "",
        "pull_request_draft": False,
        "pr_head_sha": "",
        "pr_base_branch": "",
        "checks_observed": False,
        "required_check_names": list(invocation.required_check_names),
        "successful_check_names": [],
        "pending_check_names": [],
        "failed_check_names": [],
        "mergeable": False,
        "unresolved_blocker_count": 0,
        "merge_performed": False,
        "merged_head_sha": "",
        "merge_commit_sha": "",
        "force_push_performed": False,
        "remote_branch_deleted": False,
        "admin_merge_bypass_used": False,
        "human_handover_performed": False,
        "external_authority_handover_performed": False,
        "observed_at_epoch": 209,
        "provenance_integrity_confirmed": True,
        "source_correspondence_confirmed": True,
    }


def fixture() -> dict:
    example = load_example()
    trajectory = deepcopy(example["source_trajectory_receipt"])
    initial_request = deepcopy(example["lifecycle_request"])
    initial_state = deepcopy(example["lifecycle_state"])
    lifecycle_policy = deepcopy(example["lifecycle_policy"])
    commit_message = "bounded continuation fixture"
    commit_message_digest = canonical_digest({"commit_message": commit_message})
    initial_request["commit_message_digest"] = commit_message_digest
    initial_state["commit_message_digest"] = commit_message_digest
    initial_request = reseal_lifecycle_request(initial_request)
    initial_state = reseal_lifecycle_state(initial_state)
    initial = build_codeai_autonomous_git_lifecycle_envelope(
        source_trajectory_receipt=trajectory,
        lifecycle_request=initial_request,
        lifecycle_state=initial_state,
        lifecycle_policy=lifecycle_policy,
    )
    assert initial.receipt and initial.receipt["next_effect_phase"] == PHASE_LOCAL_COMMIT
    source_lifecycle_receipt = initial.receipt

    execution_request = {
        "execution_id": "continuation-source-effect-execution-001",
        "execution_revision": "1",
        "execution_session_id": "continuation-source-effect-session-001",
        "execution_nonce_digest": "9" * 64,
        "source_lifecycle_receipt_digest": source_lifecycle_receipt[LIFECYCLE_RECEIPT_DIGEST_FIELD],
        "lifecycle_id": source_lifecycle_receipt["lifecycle_id"],
        "executor_id": source_lifecycle_receipt["executor_id"],
        "repository_full_name": source_lifecycle_receipt["repository_full_name"],
        "source_commit_sha": source_lifecycle_receipt["source_commit_sha"],
        "base_branch": source_lifecycle_receipt["base_branch"],
        "head_branch": source_lifecycle_receipt["head_branch"],
        "remote_name": source_lifecycle_receipt["remote_name"],
        "merge_method": source_lifecycle_receipt["merge_method"],
        "change_set_digest": source_lifecycle_receipt["change_set_digest"],
        "commit_message": commit_message,
        "commit_message_digest": source_lifecycle_receipt["commit_message_digest"],
        "pull_request_title": "",
        "pull_request_body": "",
        "pull_request_body_digest": canonical_digest({"pull_request_body": ""}),
        "pull_request_draft": False,
        "pull_request_number": 0,
        "expected_head_sha": source_lifecycle_receipt["source_commit_sha"],
        "requested_effect_phase": PHASE_LOCAL_COMMIT,
        "request_created_epoch": 100,
        "provenance_integrity_confirmed": True,
        "source_correspondence_confirmed": True,
    }
    execution_request = seal(execution_request, EXECUTION_REQUEST_DIGEST_FIELD)
    execution_policy = {
        "expected_source_lifecycle_receipt_digest": source_lifecycle_receipt[LIFECYCLE_RECEIPT_DIGEST_FIELD],
        "expected_repository_full_name": source_lifecycle_receipt["repository_full_name"],
        "authorized_executor_ids": [source_lifecycle_receipt["executor_id"]],
        "allowed_effect_phases": [PHASE_LOCAL_COMMIT],
        "allowed_base_branches": [source_lifecycle_receipt["base_branch"]],
        "allowed_head_branch_prefixes": ["agent/"],
        "allowed_remote_names": [source_lifecycle_receipt["remote_name"]],
        "allowed_merge_methods": [source_lifecycle_receipt["merge_method"]],
        "allow_local_commit": True,
        "allow_push": True,
        "allow_pull_request_creation": True,
        "allow_pull_request_readiness": True,
        "allow_merge": True,
        "allow_force_push": False,
        "allow_remote_branch_deletion": False,
        "allow_admin_merge_bypass": False,
        "allow_deployment": False,
        "allow_secret_material_read": False,
        "allow_opaque_token_use": True,
        "maximum_command_count": 3,
        "maximum_output_bytes": 16384,
        "maximum_timeout_seconds": 120,
        "maximum_request_age": 20,
        "maximum_registry_entries": 16,
        "evaluation_epoch": 110,
    }
    execution_policy = seal(execution_policy, EXECUTION_POLICY_DIGEST_FIELD)
    execution_registry = seal({
        "registry_id": "continuation-source-effect-registry",
        "registry_revision": 0,
        "consumed_lifecycle_receipt_digests": [],
        "consumed_execution_nonce_digests": [],
        "consumed_count": 0,
        "last_execution_epoch": 0,
    }, EXECUTION_REGISTRY_DIGEST_FIELD)
    execution = build_codeai_autonomous_git_effect_execution(
        source_lifecycle_receipt=source_lifecycle_receipt,
        execution_request=execution_request,
        execution_policy=execution_policy,
        execution_registry=execution_registry,
        adapter=execution_adapter,
    )
    assert execution.receipt and execution.evidence

    reobservation_request = {
        "reobservation_id": "continuation-source-reobservation-001",
        "reobservation_revision": "1",
        "reobservation_session_id": "continuation-source-reobservation-session-001",
        "reobservation_nonce_digest": "7" * 64,
        "source_lifecycle_receipt_digest": source_lifecycle_receipt[LIFECYCLE_RECEIPT_DIGEST_FIELD],
        "source_execution_receipt_digest": execution.receipt["codeai_autonomous_git_effect_execution_receipt_digest"],
        "source_execution_evidence_digest": execution.evidence["codeai_autonomous_git_effect_execution_evidence_digest"],
        "lifecycle_id": source_lifecycle_receipt["lifecycle_id"],
        "observer_id": "continuation-read-only-observer",
        "repository_full_name": source_lifecycle_receipt["repository_full_name"],
        "source_commit_sha": source_lifecycle_receipt["source_commit_sha"],
        "base_branch": source_lifecycle_receipt["base_branch"],
        "head_branch": source_lifecycle_receipt["head_branch"],
        "remote_name": source_lifecycle_receipt["remote_name"],
        "change_set_digest": source_lifecycle_receipt["change_set_digest"],
        "commit_message_digest": source_lifecycle_receipt["commit_message_digest"],
        "merge_method": source_lifecycle_receipt["merge_method"],
        "effect_phase": PHASE_LOCAL_COMMIT,
        "request_created_epoch": 200,
        "provenance_integrity_confirmed": True,
        "source_correspondence_confirmed": True,
    }
    reobservation_request = seal(reobservation_request, REOBSERVATION_REQUEST_DIGEST_FIELD)
    reobservation_policy = {
        "expected_source_lifecycle_receipt_digest": source_lifecycle_receipt[LIFECYCLE_RECEIPT_DIGEST_FIELD],
        "expected_source_execution_receipt_digest": execution.receipt["codeai_autonomous_git_effect_execution_receipt_digest"],
        "expected_source_execution_evidence_digest": execution.evidence["codeai_autonomous_git_effect_execution_evidence_digest"],
        "expected_repository_full_name": source_lifecycle_receipt["repository_full_name"],
        "authorized_observer_ids": ["continuation-read-only-observer"],
        "allowed_effect_phases": [PHASE_LOCAL_COMMIT],
        "required_check_names": list(lifecycle_policy["required_check_names"]),
        "maximum_command_count": 8,
        "maximum_output_bytes": 32768,
        "maximum_request_age": 20,
        "maximum_observation_age": 20,
        "maximum_registry_entries": 16,
        "evaluation_epoch": 210,
        "network_access_allowed": False,
        "secret_access_allowed": False,
        "git_write_allowed": False,
        "deployment_allowed": False,
    }
    reobservation_policy = seal(reobservation_policy, REOBSERVATION_POLICY_DIGEST_FIELD)
    reobservation_registry = seal({
        "registry_id": "continuation-source-reobservation-registry",
        "registry_revision": 0,
        "consumed_execution_receipt_digests": [],
        "consumed_reobservation_nonce_digests": [],
        "consumed_count": 0,
        "last_reobservation_epoch": 0,
    }, REOBSERVATION_REGISTRY_DIGEST_FIELD)
    reobservation = build_codeai_autonomous_git_effect_reobservation(
        source_lifecycle_receipt=source_lifecycle_receipt,
        source_execution_receipt=execution.receipt,
        source_execution_evidence=execution.evidence,
        reobservation_request=reobservation_request,
        reobservation_policy=reobservation_policy,
        reobservation_registry=reobservation_registry,
        adapter=lambda invocation: observation_adapter(invocation, source_lifecycle_receipt),
    )
    assert reobservation.receipt and reobservation.evidence and reobservation.lifecycle_state

    delegated_request = deepcopy(initial_request)
    delegated_request["lifecycle_revision"] = "2"
    delegated_request["execution_session_id"] = "codeai-git-session-002"
    delegated_request["execution_nonce_digest"] = "a" * 64
    delegated_request["request_created_epoch"] = 205
    delegated_request["prior_execution_session_ids"] = [
        *initial_request["prior_execution_session_ids"], initial_request["execution_session_id"]
    ]
    delegated_request["prior_execution_nonce_digests"] = [
        *initial_request["prior_execution_nonce_digests"], initial_request["execution_nonce_digest"]
    ]
    delegated_request["prior_lifecycle_receipt_digests"] = [
        *initial_request["prior_lifecycle_receipt_digests"],
        source_lifecycle_receipt[LIFECYCLE_RECEIPT_DIGEST_FIELD],
    ]
    delegated_request = reseal_lifecycle_request(delegated_request)
    delegated_policy = deepcopy(lifecycle_policy)
    delegated_policy["evaluation_epoch"] = 230
    delegated_policy["maximum_request_age"] = 30
    delegated_policy["maximum_state_age"] = 30
    delegated_policy = reseal_lifecycle_policy(delegated_policy)

    continuation_request = {
        "continuation_id": "reobservation-gated-continuation-001",
        "continuation_revision": "1",
        "continuation_session_id": "reobservation-gated-continuation-session-001",
        "continuation_nonce_digest": CONTINUATION_NONCE,
        "source_reobservation_receipt_digest": reobservation.receipt["codeai_autonomous_git_effect_reobservation_receipt_digest"],
        "source_reobservation_evidence_digest": reobservation.evidence["codeai_autonomous_git_effect_reobservation_evidence_digest"],
        "source_lifecycle_receipt_digest": source_lifecycle_receipt[LIFECYCLE_RECEIPT_DIGEST_FIELD],
        "source_lifecycle_state_digest": reobservation.lifecycle_state["codeai_autonomous_git_lifecycle_state_digest"],
        "source_trajectory_receipt_digest": trajectory["codeai_autonomous_trajectory_receipt_digest"],
        "delegated_lifecycle_request_digest": delegated_request["codeai_autonomous_git_lifecycle_request_digest"],
        "delegated_lifecycle_policy_digest": delegated_policy["codeai_autonomous_git_lifecycle_policy_digest"],
        "lifecycle_id": source_lifecycle_receipt["lifecycle_id"],
        "executor_id": source_lifecycle_receipt["executor_id"],
        "repository_full_name": source_lifecycle_receipt["repository_full_name"],
        "request_created_epoch": 220,
        "provenance_integrity_confirmed": True,
        "source_correspondence_confirmed": True,
    }
    continuation_request = seal(continuation_request, REQUEST_DIGEST_FIELD)
    continuation_policy = {
        "expected_source_reobservation_receipt_digest": reobservation.receipt["codeai_autonomous_git_effect_reobservation_receipt_digest"],
        "expected_source_reobservation_evidence_digest": reobservation.evidence["codeai_autonomous_git_effect_reobservation_evidence_digest"],
        "expected_source_lifecycle_receipt_digest": source_lifecycle_receipt[LIFECYCLE_RECEIPT_DIGEST_FIELD],
        "expected_source_lifecycle_state_digest": reobservation.lifecycle_state["codeai_autonomous_git_lifecycle_state_digest"],
        "expected_source_trajectory_receipt_digest": trajectory["codeai_autonomous_trajectory_receipt_digest"],
        "expected_repository_full_name": source_lifecycle_receipt["repository_full_name"],
        "authorized_executor_ids": [source_lifecycle_receipt["executor_id"]],
        "maximum_request_age": 30,
        "maximum_state_age": 30,
        "maximum_registry_entries": 16,
        "evaluation_epoch": 230,
        "allow_lifecycle_evaluation": True,
        "allow_state_projection": True,
        "allow_automatic_effect_execution": False,
    }
    continuation_policy = seal(continuation_policy, POLICY_DIGEST_FIELD)
    continuation_registry = seal({
        "registry_id": "reobservation-gated-continuation-registry-001",
        "registry_revision": 0,
        "consumed_reobservation_receipt_digests": [],
        "consumed_continuation_nonce_digests": [],
        "consumed_count": 0,
        "last_continuation_epoch": 0,
    }, REGISTRY_DIGEST_FIELD)
    return {
        "source_trajectory_receipt": trajectory,
        "source_reobservation_receipt": reobservation.receipt,
        "source_reobservation_evidence": reobservation.evidence,
        "source_lifecycle_state": reobservation.lifecycle_state,
        "continuation_request": continuation_request,
        "continuation_policy": continuation_policy,
        "continuation_registry": continuation_registry,
        "delegated_lifecycle_request": delegated_request,
        "delegated_lifecycle_policy": delegated_policy,
    }


def build(values: dict):
    return build_codeai_reobservation_gated_git_lifecycle_continuation(**values)


class ReobservationGatedGitLifecycleContinuationTests(unittest.TestCase):
    def test_completed_reobservation_reenters_lifecycle_and_authorizes_push(self):
        result = build(fixture())
        self.assertEqual(STATUS_READY, result.status)
        self.assertEqual(PHASE_PUSH, result.receipt["next_effect_phase"])
        self.assertTrue(result.receipt["push_authority_granted"])
        self.assertTrue(result.receipt["one_effect_lease_issued"])

    def test_projection_only_clears_unobserved_required_check_names(self):
        values = fixture()
        source = values["source_lifecycle_state"]
        result = build(values)
        self.assertTrue(result.receipt["state_projection_performed"])
        self.assertFalse(result.receipt["state_projection_factual_fields_changed"])
        self.assertEqual([], result.delegated_lifecycle_state["required_check_names"])
        for field in source:
            if field not in {"required_check_names", "codeai_autonomous_git_lifecycle_state_digest"}:
                self.assertEqual(source[field], result.delegated_lifecycle_state[field])

    def test_consumes_source_receipt_and_nonce_once(self):
        result = build(fixture())
        self.assertTrue(result.receipt["source_reobservation_receipt_consumed"])
        self.assertTrue(result.receipt["continuation_nonce_consumed"])
        self.assertEqual(1, result.next_registry["registry_revision"])
        self.assertEqual(1, result.next_registry["consumed_count"])

    def test_performs_no_automatic_effect(self):
        result = build(fixture())
        self.assertFalse(result.receipt["automatic_effect_execution_performed"])
        self.assertFalse(result.receipt["general_git_authority_granted"])
        self.assertFalse(result.receipt["general_successor_stage_authority_granted"])
        self.assertFalse(result.receipt["reobservation_state_treated_as_authority"])

    def test_source_receipt_replay_is_blocked(self):
        values = fixture()
        digest = values["continuation_request"]["source_reobservation_receipt_digest"]
        registry = values["continuation_registry"]
        registry["consumed_reobservation_receipt_digests"] = [digest]
        registry["consumed_continuation_nonce_digests"] = ["f" * 64]
        registry["consumed_count"] = 1
        values["continuation_registry"] = seal(registry, REGISTRY_DIGEST_FIELD)
        self.assertIn("continuation_source_reobservation_receipt_replay", build(values).issues)

    def test_nonce_replay_is_blocked(self):
        values = fixture()
        registry = values["continuation_registry"]
        registry["consumed_reobservation_receipt_digests"] = ["f" * 64]
        registry["consumed_continuation_nonce_digests"] = [CONTINUATION_NONCE]
        registry["consumed_count"] = 1
        values["continuation_registry"] = seal(registry, REGISTRY_DIGEST_FIELD)
        self.assertIn("continuation_nonce_replay", build(values).issues)

    def test_tampered_reobservation_receipt_is_blocked(self):
        values = fixture()
        values["source_reobservation_receipt"]["lifecycle_id"] = "tampered"
        self.assertIn("source_reobservation_receipt_digest_mismatch", build(values).issues)

    def test_tampered_reobservation_evidence_is_blocked(self):
        values = fixture()
        values["source_reobservation_evidence"]["fresh_lifecycle_state_issued"] = False
        self.assertEqual(STATUS_BLOCKED, build(values).status)

    def test_tampered_state_is_blocked(self):
        values = fixture()
        values["source_lifecycle_state"]["local_commit_sha"] = "c" * 40
        self.assertIn("source_lifecycle_state_digest_mismatch", build(values).issues)

    def test_wrong_source_correspondence_is_blocked(self):
        values = fixture()
        request = values["continuation_request"]
        request["repository_full_name"] = "other/repository"
        values["continuation_request"] = seal(request, REQUEST_DIGEST_FIELD)
        self.assertIn("continuation_source_correspondence_mismatch", build(values).issues)

    def test_stale_request_is_blocked(self):
        values = fixture()
        request = values["continuation_request"]
        request["request_created_epoch"] = 1
        values["continuation_request"] = seal(request, REQUEST_DIGEST_FIELD)
        self.assertIn("continuation_freshness_window_violation", build(values).issues)

    def test_stale_state_is_blocked(self):
        values = fixture()
        policy = values["continuation_policy"]
        policy["evaluation_epoch"] = 1000
        values["continuation_policy"] = seal(policy, POLICY_DIGEST_FIELD)
        self.assertIn("continuation_freshness_window_violation", build(values).issues)

    def test_registry_capacity_is_fail_closed(self):
        values = fixture()
        policy = values["continuation_policy"]
        policy["maximum_registry_entries"] = 1
        values["continuation_policy"] = seal(policy, POLICY_DIGEST_FIELD)
        registry = values["continuation_registry"]
        registry["consumed_reobservation_receipt_digests"] = ["1" * 64]
        registry["consumed_continuation_nonce_digests"] = ["2" * 64]
        registry["consumed_count"] = 1
        values["continuation_registry"] = seal(registry, REGISTRY_DIGEST_FIELD)
        self.assertIn("continuation_registry_capacity_exhausted", build(values).issues)

    def test_lifecycle_evaluation_must_be_explicitly_allowed(self):
        values = fixture()
        policy = values["continuation_policy"]
        policy["allow_lifecycle_evaluation"] = False
        values["continuation_policy"] = seal(policy, POLICY_DIGEST_FIELD)
        self.assertIn("continuation_lifecycle_evaluation_not_allowed", build(values).issues)

    def test_automatic_execution_must_be_denied(self):
        values = fixture()
        policy = values["continuation_policy"]
        policy["allow_automatic_effect_execution"] = True
        values["continuation_policy"] = seal(policy, POLICY_DIGEST_FIELD)
        self.assertIn("continuation_automatic_effect_execution_not_denied", build(values).issues)

    def test_projection_requires_explicit_policy(self):
        values = fixture()
        policy = values["continuation_policy"]
        policy["allow_state_projection"] = False
        values["continuation_policy"] = seal(policy, POLICY_DIGEST_FIELD)
        self.assertIn("continuation_state_projection_not_allowed", build(values).issues)

    def test_prior_lifecycle_receipt_must_be_recorded_once(self):
        values = fixture()
        request = values["delegated_lifecycle_request"]
        source_digest = values["continuation_request"]["source_lifecycle_receipt_digest"]
        request["prior_lifecycle_receipt_digests"] = [x for x in request["prior_lifecycle_receipt_digests"] if x != source_digest]
        values["delegated_lifecycle_request"] = reseal_lifecycle_request(request)
        continuation = values["continuation_request"]
        continuation["delegated_lifecycle_request_digest"] = values["delegated_lifecycle_request"]["codeai_autonomous_git_lifecycle_request_digest"]
        values["continuation_request"] = seal(continuation, REQUEST_DIGEST_FIELD)
        self.assertIn("continuation_prior_lifecycle_receipt_not_recorded_once", build(values).issues)

    def test_delegated_request_tamper_is_blocked(self):
        values = fixture()
        values["delegated_lifecycle_request"]["execution_session_id"] = "tampered"
        self.assertEqual(STATUS_BLOCKED, build(values).status)

    def test_delegated_policy_tamper_is_blocked(self):
        values = fixture()
        values["delegated_lifecycle_policy"]["allow_push"] = False
        self.assertEqual(STATUS_BLOCKED, build(values).status)

    def test_receipt_is_canonically_sealed(self):
        result = build(fixture())
        receipt = deepcopy(result.receipt)
        digest = receipt.pop(RECEIPT_DIGEST_FIELD)
        self.assertEqual(digest, canonical_digest(receipt))


if __name__ == "__main__":
    unittest.main()
