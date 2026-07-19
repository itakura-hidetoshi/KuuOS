from __future__ import annotations

from copy import deepcopy
import unittest

from runtime.kuuos_codeai_autonomous_git_effect_execution_v0_1 import (
    DISPOSITION_FAILED as SOURCE_DISPOSITION_FAILED,
    PHASE_CREATE_PR,
    PHASE_LOCAL_COMMIT,
    PHASE_MARK_PR_READY,
    PHASE_MERGE,
    PHASE_PUSH,
    build_codeai_autonomous_git_effect_execution,
)
from runtime.kuuos_codeai_autonomous_git_lifecycle_envelope_v0_1 import (
    _validate_state as validate_lifecycle_state,
)
from runtime.kuuos_codeai_autonomous_git_effect_reobservation_v0_1 import (
    DISPOSITION_COMPLETED,
    DISPOSITION_EVIDENCE_QUARANTINED,
    DISPOSITION_FAILED,
    POLICY_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD,
    REGISTRY_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    SOURCE_EXECUTION_RECEIPT_DIGEST_FIELD,
    STATUS_BLOCKED,
    STATUS_READY,
    GitEffectReobservationInvocation,
    build_codeai_autonomous_git_effect_reobservation,
    canonical_digest,
)
from tests.test_kuuos_codeai_autonomous_git_effect_execution_v0_1 import (
    SHA_A,
    SHA_B,
    base_adapter_result,
    completed_result,
    make_policy as make_execution_policy,
    make_registry as make_execution_registry,
    make_request as make_execution_request,
    make_source,
)

REQUIRED_CHECK = "KuuOS PR Governance Gate"


def seal(value: dict, field: str) -> dict:
    result = deepcopy(value)
    result[field] = canonical_digest(result)
    return result


def build_source_execution(phase: str, *, outcome: str = "completed"):
    lifecycle = make_source(phase)
    request = make_execution_request(lifecycle)
    policy = make_execution_policy(lifecycle)
    registry = make_execution_registry()
    if outcome == "completed":
        adapter = completed_result
    elif outcome == "failed":
        def adapter(invocation):
            result = base_adapter_result(invocation.effect_phase)
            result.update(status="failed", exit_code=1, stderr="bounded failure")
            return result
    else:
        def adapter(_invocation):
            return {"malformed": True}
    result = build_codeai_autonomous_git_effect_execution(
        source_lifecycle_receipt=lifecycle,
        execution_request=request,
        execution_policy=policy,
        execution_registry=registry,
        adapter=adapter,
    )
    assert result.status == STATUS_READY
    assert result.receipt and result.evidence
    return lifecycle, result.receipt, result.evidence


def make_request(lifecycle: dict, execution: dict, evidence: dict) -> dict:
    request = {
        "reobservation_id": "git-effect-reobservation-001",
        "reobservation_revision": "r1",
        "reobservation_session_id": "git-effect-reobservation-session-001",
        "reobservation_nonce_digest": "7" * 64,
        "source_lifecycle_receipt_digest": lifecycle["codeai_autonomous_git_lifecycle_receipt_digest"],
        "source_execution_receipt_digest": execution[SOURCE_EXECUTION_RECEIPT_DIGEST_FIELD],
        "source_execution_evidence_digest": evidence["codeai_autonomous_git_effect_execution_evidence_digest"],
        "lifecycle_id": lifecycle["lifecycle_id"],
        "observer_id": "codeai-git-state-observer",
        "repository_full_name": lifecycle["repository_full_name"],
        "source_commit_sha": lifecycle["source_commit_sha"],
        "base_branch": lifecycle["base_branch"],
        "head_branch": lifecycle["head_branch"],
        "remote_name": lifecycle["remote_name"],
        "change_set_digest": lifecycle["change_set_digest"],
        "commit_message_digest": lifecycle["commit_message_digest"],
        "merge_method": lifecycle["merge_method"],
        "effect_phase": execution["effect_phase"],
        "request_created_epoch": 200,
        "provenance_integrity_confirmed": True,
        "source_correspondence_confirmed": True,
    }
    return seal(request, REQUEST_DIGEST_FIELD)


def make_policy(lifecycle: dict, execution: dict, evidence: dict) -> dict:
    policy = {
        "expected_source_lifecycle_receipt_digest": lifecycle["codeai_autonomous_git_lifecycle_receipt_digest"],
        "expected_source_execution_receipt_digest": execution[SOURCE_EXECUTION_RECEIPT_DIGEST_FIELD],
        "expected_source_execution_evidence_digest": evidence["codeai_autonomous_git_effect_execution_evidence_digest"],
        "expected_repository_full_name": lifecycle["repository_full_name"],
        "authorized_observer_ids": ["codeai-git-state-observer"],
        "allowed_effect_phases": [execution["effect_phase"]],
        "required_check_names": [REQUIRED_CHECK],
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
    return seal(policy, POLICY_DIGEST_FIELD)


def make_registry() -> dict:
    registry = {
        "registry_id": "git-effect-reobservation-registry-001",
        "registry_revision": 0,
        "consumed_execution_receipt_digests": [],
        "consumed_reobservation_nonce_digests": [],
        "consumed_count": 0,
        "last_reobservation_epoch": 0,
    }
    return seal(registry, REGISTRY_DIGEST_FIELD)


def observation_result(
    invocation: GitEffectReobservationInvocation,
    lifecycle: dict,
    execution: dict,
    evidence: dict,
) -> dict:
    source_result = evidence["adapter_result"]
    local_created = lifecycle["local_commit_created_observed"]
    local_sha = lifecycle["local_commit_sha"]
    local_parent = lifecycle["source_commit_sha"] if local_created else ""
    branch_pushed = lifecycle["branch_pushed_observed"]
    pushed_head = lifecycle["pushed_head_sha"]
    pr_created = lifecycle["pull_request_created_observed"]
    pr_number = lifecycle["pull_request_number"]
    pr_url_digest = "8" * 64 if pr_created else ""
    pr_draft = lifecycle["pull_request_draft_observed"]
    pr_head = lifecycle["pushed_head_sha"] if pr_created else ""
    pr_base = lifecycle["base_branch"] if pr_created else ""
    checks_observed = lifecycle["required_checks_observed"]
    success = list(lifecycle["successful_check_names"])
    pending = list(lifecycle["pending_check_names"])
    failed = list(lifecycle["failed_check_names"])
    mergeable = lifecycle["mergeable_observed"]
    blockers = lifecycle["unresolved_blocker_count"]
    merge_performed = lifecycle["merge_performed_observed"]
    merged_head = lifecycle["local_commit_sha"] if merge_performed else ""
    merge_commit = lifecycle["merge_commit_sha"]

    phase = execution["effect_phase"]
    if execution["effect_completion_confirmed"]:
        if phase == PHASE_LOCAL_COMMIT:
            local_created = True
            local_sha = source_result["local_commit_sha"]
            local_parent = source_result["local_commit_parent_sha"]
        elif phase == PHASE_PUSH:
            branch_pushed = True
            pushed_head = source_result["pushed_head_sha"]
        elif phase == PHASE_CREATE_PR:
            pr_created = True
            pr_number = source_result["pull_request_number"]
            pr_url_digest = source_result["pull_request_url_digest"]
            pr_draft = source_result["pull_request_draft"]
            pr_head = source_result["pr_head_sha"]
            pr_base = source_result["pr_base_branch"]
        elif phase == PHASE_MARK_PR_READY:
            pr_created = True
            pr_number = source_result["pull_request_number"]
            pr_url_digest = "8" * 64
            pr_draft = False
            pr_head = source_result["pr_head_sha"]
            pr_base = source_result["pr_base_branch"]
        elif phase == PHASE_MERGE:
            merge_performed = True
            merged_head = source_result["merged_head_sha"]
            merge_commit = source_result["merge_commit_sha"]

    return {
        "adapter_id": "read-only-git-state-observer",
        "adapter_session_id": "observer-session-001",
        "status": "observed",
        "command_count": 4,
        "output_bytes": 4096,
        "completed_epoch": 209,
        "network_accessed": False,
        "secret_material_read": False,
        "git_write_performed": False,
        "deployment_performed": False,
        "exception_type": "",
        "lifecycle_id": lifecycle["lifecycle_id"],
        "source_trajectory_receipt_digest": lifecycle["source_trajectory_receipt_digest"],
        "repository_full_name": lifecycle["repository_full_name"],
        "source_commit_sha": lifecycle["source_commit_sha"],
        "executor_id": lifecycle["executor_id"],
        "base_branch": lifecycle["base_branch"],
        "head_branch": lifecycle["head_branch"],
        "remote_name": lifecycle["remote_name"],
        "change_set_digest": lifecycle["change_set_digest"],
        "commit_message_digest": lifecycle["commit_message_digest"],
        "merge_method": lifecycle["merge_method"],
        "local_commit_created": local_created,
        "local_commit_sha": local_sha,
        "local_commit_parent_sha": local_parent,
        "branch_pushed": branch_pushed,
        "pushed_head_sha": pushed_head,
        "pull_request_created": pr_created,
        "pull_request_number": pr_number,
        "pull_request_url_digest": pr_url_digest,
        "pull_request_draft": pr_draft,
        "pr_head_sha": pr_head,
        "pr_base_branch": pr_base,
        "checks_observed": checks_observed,
        "required_check_names": list(invocation.required_check_names),
        "successful_check_names": success,
        "pending_check_names": pending,
        "failed_check_names": failed,
        "mergeable": mergeable,
        "unresolved_blocker_count": blockers,
        "merge_performed": merge_performed,
        "merged_head_sha": merged_head,
        "merge_commit_sha": merge_commit,
        "force_push_performed": False,
        "remote_branch_deleted": False,
        "admin_merge_bypass_used": False,
        "human_handover_performed": False,
        "external_authority_handover_performed": False,
        "observed_at_epoch": 209,
        "provenance_integrity_confirmed": True,
        "source_correspondence_confirmed": True,
    }


def run_case(phase: str, *, source_outcome: str = "completed", adapter_mutator=None):
    lifecycle, execution, evidence = build_source_execution(phase, outcome=source_outcome)
    request = make_request(lifecycle, execution, evidence)
    policy = make_policy(lifecycle, execution, evidence)
    registry = make_registry()

    def adapter(invocation):
        result = observation_result(invocation, lifecycle, execution, evidence)
        if adapter_mutator:
            adapter_mutator(result)
        return result

    result = build_codeai_autonomous_git_effect_reobservation(
        source_lifecycle_receipt=lifecycle,
        source_execution_receipt=execution,
        source_execution_evidence=evidence,
        reobservation_request=request,
        reobservation_policy=policy,
        reobservation_registry=registry,
        adapter=adapter,
    )
    return lifecycle, execution, evidence, request, policy, registry, result


class GitEffectReobservationTests(unittest.TestCase):
    def test_completed_local_commit_reobserves_fresh_state(self):
        *_, result = run_case(PHASE_LOCAL_COMMIT)
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.receipt["codeai_disposition"], DISPOSITION_COMPLETED)
        self.assertTrue(result.lifecycle_state["local_commit_created"])
        self.assertEqual(result.lifecycle_state["local_commit_sha"], SHA_B)

    def test_completed_push_reobserves_remote_head(self):
        *_, result = run_case(PHASE_PUSH)
        self.assertTrue(result.lifecycle_state["branch_pushed"])
        self.assertEqual(result.lifecycle_state["pushed_head_sha"], SHA_B)

    def test_completed_pr_creation_reobserves_draft_pr(self):
        *_, result = run_case(PHASE_CREATE_PR)
        self.assertTrue(result.lifecycle_state["pull_request_created"])
        self.assertTrue(result.lifecycle_state["pull_request_draft"])
        self.assertEqual(result.lifecycle_state["pull_request_number"], 1303)

    def test_completed_readiness_reobserves_non_draft_pr(self):
        *_, result = run_case(PHASE_MARK_PR_READY)
        self.assertTrue(result.lifecycle_state["pull_request_created"])
        self.assertFalse(result.lifecycle_state["pull_request_draft"])

    def test_completed_merge_reobserves_merge_commit(self):
        *_, result = run_case(PHASE_MERGE)
        self.assertTrue(result.lifecycle_state["merge_performed"])
        self.assertEqual(result.lifecycle_state["merge_commit_sha"], "c" * 40)

    def test_issued_state_is_accepted_by_existing_lifecycle_validator(self):
        *_, result = run_case(PHASE_MERGE)
        self.assertEqual(validate_lifecycle_state(result.lifecycle_state), [])

    def test_failed_source_can_be_reobserved_without_retry_authority(self):
        *_, result = run_case(PHASE_PUSH, source_outcome="failed")
        self.assertEqual(result.receipt["source_execution_disposition"], SOURCE_DISPOSITION_FAILED)
        self.assertEqual(result.receipt["codeai_disposition"], DISPOSITION_COMPLETED)
        self.assertFalse(result.receipt["automatic_successor_effect_authority_granted"])

    def test_source_receipt_replay_is_blocked(self):
        lifecycle, execution, evidence = build_source_execution(PHASE_PUSH)
        request = make_request(lifecycle, execution, evidence)
        policy = make_policy(lifecycle, execution, evidence)
        registry = make_registry()
        registry["consumed_execution_receipt_digests"] = [execution[SOURCE_EXECUTION_RECEIPT_DIGEST_FIELD]]
        registry["consumed_reobservation_nonce_digests"] = ["6" * 64]
        registry["consumed_count"] = 1
        registry = seal(registry, REGISTRY_DIGEST_FIELD)
        result = build_codeai_autonomous_git_effect_reobservation(
            source_lifecycle_receipt=lifecycle,
            source_execution_receipt=execution,
            source_execution_evidence=evidence,
            reobservation_request=request,
            reobservation_policy=policy,
            reobservation_registry=registry,
            adapter=lambda invocation: observation_result(invocation, lifecycle, execution, evidence),
        )
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_nonce_replay_is_blocked(self):
        lifecycle, execution, evidence = build_source_execution(PHASE_PUSH)
        request = make_request(lifecycle, execution, evidence)
        policy = make_policy(lifecycle, execution, evidence)
        registry = make_registry()
        registry["consumed_execution_receipt_digests"] = ["6" * 64]
        registry["consumed_reobservation_nonce_digests"] = [request["reobservation_nonce_digest"]]
        registry["consumed_count"] = 1
        registry = seal(registry, REGISTRY_DIGEST_FIELD)
        result = build_codeai_autonomous_git_effect_reobservation(
            source_lifecycle_receipt=lifecycle,
            source_execution_receipt=execution,
            source_execution_evidence=evidence,
            reobservation_request=request,
            reobservation_policy=policy,
            reobservation_registry=registry,
            adapter=lambda invocation: observation_result(invocation, lifecycle, execution, evidence),
        )
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_tampered_source_execution_receipt_is_blocked(self):
        lifecycle, execution, evidence = build_source_execution(PHASE_PUSH)
        execution["repository_full_name"] = "other/repo"
        request = make_request(lifecycle, execution, evidence)
        policy = make_policy(lifecycle, execution, evidence)
        result = build_codeai_autonomous_git_effect_reobservation(
            source_lifecycle_receipt=lifecycle,
            source_execution_receipt=execution,
            source_execution_evidence=evidence,
            reobservation_request=request,
            reobservation_policy=policy,
            reobservation_registry=make_registry(),
            adapter=lambda invocation: observation_result(invocation, lifecycle, execution, evidence),
        )
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_tampered_source_evidence_is_blocked(self):
        lifecycle, execution, evidence = build_source_execution(PHASE_PUSH)
        evidence["effect_phase"] = PHASE_MERGE
        result = build_codeai_autonomous_git_effect_reobservation(
            source_lifecycle_receipt=lifecycle,
            source_execution_receipt=execution,
            source_execution_evidence=evidence,
            reobservation_request=make_request(lifecycle, execution, evidence),
            reobservation_policy=make_policy(lifecycle, execution, evidence),
            reobservation_registry=make_registry(),
            adapter=lambda invocation: observation_result(invocation, lifecycle, execution, evidence),
        )
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_stale_request_is_blocked(self):
        lifecycle, execution, evidence = build_source_execution(PHASE_PUSH)
        request = make_request(lifecycle, execution, evidence)
        request["request_created_epoch"] = 100
        request = seal(request, REQUEST_DIGEST_FIELD)
        result = build_codeai_autonomous_git_effect_reobservation(
            source_lifecycle_receipt=lifecycle,
            source_execution_receipt=execution,
            source_execution_evidence=evidence,
            reobservation_request=request,
            reobservation_policy=make_policy(lifecycle, execution, evidence),
            reobservation_registry=make_registry(),
            adapter=lambda invocation: observation_result(invocation, lifecycle, execution, evidence),
        )
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_effect_authorizing_policy_is_blocked(self):
        lifecycle, execution, evidence = build_source_execution(PHASE_PUSH)
        policy = make_policy(lifecycle, execution, evidence)
        policy["git_write_allowed"] = True
        policy = seal(policy, POLICY_DIGEST_FIELD)
        result = build_codeai_autonomous_git_effect_reobservation(
            source_lifecycle_receipt=lifecycle,
            source_execution_receipt=execution,
            source_execution_evidence=evidence,
            reobservation_request=make_request(lifecycle, execution, evidence),
            reobservation_policy=policy,
            reobservation_registry=make_registry(),
            adapter=lambda invocation: observation_result(invocation, lifecycle, execution, evidence),
        )
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_adapter_exception_is_failed_and_consumes_reobservation_nonce(self):
        lifecycle, execution, evidence = build_source_execution(PHASE_PUSH)
        result = build_codeai_autonomous_git_effect_reobservation(
            source_lifecycle_receipt=lifecycle,
            source_execution_receipt=execution,
            source_execution_evidence=evidence,
            reobservation_request=make_request(lifecycle, execution, evidence),
            reobservation_policy=make_policy(lifecycle, execution, evidence),
            reobservation_registry=make_registry(),
            adapter=lambda _invocation: (_ for _ in ()).throw(RuntimeError("observer failed")),
        )
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.receipt["codeai_disposition"], DISPOSITION_FAILED)
        self.assertIsNone(result.lifecycle_state)
        self.assertEqual(result.next_registry["consumed_count"], 1)

    def test_malformed_adapter_evidence_is_quarantined(self):
        lifecycle, execution, evidence = build_source_execution(PHASE_PUSH)
        result = build_codeai_autonomous_git_effect_reobservation(
            source_lifecycle_receipt=lifecycle,
            source_execution_receipt=execution,
            source_execution_evidence=evidence,
            reobservation_request=make_request(lifecycle, execution, evidence),
            reobservation_policy=make_policy(lifecycle, execution, evidence),
            reobservation_registry=make_registry(),
            adapter=lambda _invocation: {"malformed": True},
        )
        self.assertEqual(result.receipt["codeai_disposition"], DISPOSITION_EVIDENCE_QUARANTINED)
        self.assertIsNone(result.lifecycle_state)

    def test_git_write_observation_is_quarantined(self):
        def mutate(result):
            result["git_write_performed"] = True
        *_, result = run_case(PHASE_PUSH, adapter_mutator=mutate)
        self.assertEqual(result.receipt["codeai_disposition"], DISPOSITION_EVIDENCE_QUARANTINED)

    def test_completed_effect_mismatch_is_quarantined(self):
        def mutate(result):
            result["pushed_head_sha"] = "d" * 40
        *_, result = run_case(PHASE_PUSH, adapter_mutator=mutate)
        self.assertEqual(result.receipt["codeai_disposition"], DISPOSITION_EVIDENCE_QUARANTINED)
        self.assertFalse(result.receipt["source_effect_correspondence_confirmed"])

    def test_registry_advances_exactly_once(self):
        *_, registry, result = run_case(PHASE_MERGE)
        self.assertEqual(result.next_registry["registry_revision"], registry["registry_revision"] + 1)
        self.assertEqual(result.next_registry["consumed_count"], registry["consumed_count"] + 1)

    def test_receipt_is_sealed_and_grants_no_authority(self):
        *_, result = run_case(PHASE_MERGE)
        receipt = result.receipt
        self.assertEqual(receipt[RECEIPT_DIGEST_FIELD], canonical_digest({k: v for k, v in receipt.items() if k != RECEIPT_DIGEST_FIELD}))
        self.assertFalse(receipt["general_git_authority_granted"])
        self.assertFalse(receipt["general_successor_stage_authority_granted"])
        self.assertFalse(receipt["automatic_successor_effect_authority_granted"])
        self.assertFalse(receipt["effect_execution_performed"])


if __name__ == "__main__":
    unittest.main()
