from __future__ import annotations

from copy import deepcopy
import unittest

from runtime.kuuos_codeai_autonomous_git_effect_execution_v0_1 import (
    DISPOSITION_COMPLETED,
    DISPOSITION_EVIDENCE_QUARANTINED,
    DISPOSITION_FAILED,
    PHASE_CREATE_PR,
    PHASE_LOCAL_COMMIT,
    PHASE_MARK_PR_READY,
    PHASE_MERGE,
    PHASE_PUSH,
    POLICY_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD,
    REGISTRY_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    SOURCE_RECEIPT_DIGEST_FIELD,
    STATUS_BLOCKED,
    STATUS_READY,
    GitEffectInvocation,
    build_codeai_autonomous_git_effect_execution,
    canonical_digest,
)

SHA_A = "a" * 40
SHA_B = "b" * 40
SHA_C = "c" * 40
D1 = "1" * 64
D2 = "2" * 64
D3 = "3" * 64
D4 = "4" * 64
D5 = "5" * 64


def seal(value: dict, field: str) -> dict:
    result = deepcopy(value)
    result[field] = canonical_digest(result)
    return result


def text_digest(label: str, value: str) -> str:
    return canonical_digest({label: value})


def make_source(phase: str) -> dict:
    commit_message_digest = text_digest("commit_message", "autonomous effect")
    source = {
        "schema_version": "v0.1",
        "profile_version": "CodeAI Autonomous Git Lifecycle v0.1",
        "source_trajectory_receipt_digest": D1,
        "git_lifecycle_request_digest": D2,
        "git_lifecycle_state_digest": D3,
        "git_lifecycle_policy_digest": D4,
        "lifecycle_id": "lifecycle-001",
        "execution_session_id": "lifecycle-session-001",
        "repository_full_name": "itakura-hidetoshi/KuuOS",
        "source_commit_sha": SHA_A,
        "executor_id": "codeai-git-executor",
        "base_branch": "main",
        "head_branch": "codeai/effect-test",
        "remote_name": "origin",
        "change_set_digest": D5,
        "commit_message_digest": commit_message_digest,
        "merge_method": "merge",
        "next_effect_phase": phase,
        "codeai_disposition": {
            PHASE_LOCAL_COMMIT: "autonomous_local_commit_authorized",
            PHASE_PUSH: "autonomous_branch_push_authorized",
            PHASE_CREATE_PR: "autonomous_pull_request_creation_authorized",
            PHASE_MARK_PR_READY: "autonomous_pull_request_readiness_authorized",
            PHASE_MERGE: "autonomous_pull_request_merge_authorized",
        }[phase],
        "operating_mode": {
            PHASE_LOCAL_COMMIT: "local_git_effect_authorized",
            PHASE_PUSH: "remote_git_effect_authorized",
            PHASE_CREATE_PR: "pull_request_effect_authorized",
            PHASE_MARK_PR_READY: "pull_request_effect_authorized",
            PHASE_MERGE: "merge_effect_authorized",
        }[phase],
        "route_receipt_recorded": True,
        "execution_lease_issued": True,
        "local_commit_authority_granted": phase == PHASE_LOCAL_COMMIT,
        "push_authority_granted": phase == PHASE_PUSH,
        "pull_request_authority_granted": phase == PHASE_CREATE_PR,
        "pull_request_readiness_authority_granted": phase == PHASE_MARK_PR_READY,
        "merge_authority_granted": phase == PHASE_MERGE,
        "checks_wait_required": False,
        "human_handover_deferred": False,
        "effect_execution_performed_by_kernel": False,
        "local_commit_created_observed": phase != PHASE_LOCAL_COMMIT,
        "local_commit_sha": "" if phase == PHASE_LOCAL_COMMIT else SHA_B,
        "branch_pushed_observed": phase in {PHASE_CREATE_PR, PHASE_MARK_PR_READY, PHASE_MERGE},
        "pushed_head_sha": SHA_B if phase in {PHASE_CREATE_PR, PHASE_MARK_PR_READY, PHASE_MERGE} else "",
        "pull_request_created_observed": phase in {PHASE_MARK_PR_READY, PHASE_MERGE},
        "pull_request_number": 1303 if phase in {PHASE_MARK_PR_READY, PHASE_MERGE} else 0,
        "pull_request_draft_observed": phase == PHASE_MARK_PR_READY,
        "required_checks_observed": phase == PHASE_MERGE,
        "all_required_checks_successful": phase == PHASE_MERGE,
        "no_pending_checks": True,
        "no_failed_checks": True,
        "successful_check_names": ["KuuOS PR Governance Gate"] if phase == PHASE_MERGE else [],
        "pending_check_names": [],
        "failed_check_names": [],
        "mergeable_observed": phase == PHASE_MERGE,
        "unresolved_blocker_count": 0,
        "head_sha_pinned": phase == PHASE_MERGE,
        "merge_performed_observed": False,
        "merge_commit_sha": "",
        "force_push_performed": False,
        "remote_branch_deleted": False,
        "admin_merge_bypass_used": False,
        "human_handover_performed": False,
        "external_authority_handover_performed": False,
        "deployment_authority_granted": False,
        "deployment_performed": False,
        "secret_access_authority_granted": False,
        "secret_access_performed": False,
        "source_receipt_treated_as_git_authority": False,
        "checks_treated_as_correctness_proof": False,
        "merge_treated_as_truth": False,
        "history_read_only": True,
        "future_only": True,
        "active_now": True,
    }
    return seal(source, SOURCE_RECEIPT_DIGEST_FIELD)


def make_request(source: dict) -> dict:
    phase = source["next_effect_phase"]
    title = "Autonomous effect PR" if phase == PHASE_CREATE_PR else ""
    body = "Bounded one-effect execution." if phase == PHASE_CREATE_PR else ""
    request = {
        "execution_id": "effect-execution-001",
        "execution_revision": "r1",
        "execution_session_id": "effect-session-001",
        "execution_nonce_digest": "9" * 64,
        "source_lifecycle_receipt_digest": source[SOURCE_RECEIPT_DIGEST_FIELD],
        "lifecycle_id": source["lifecycle_id"],
        "executor_id": source["executor_id"],
        "repository_full_name": source["repository_full_name"],
        "source_commit_sha": source["source_commit_sha"],
        "base_branch": source["base_branch"],
        "head_branch": source["head_branch"],
        "remote_name": source["remote_name"],
        "merge_method": source["merge_method"],
        "change_set_digest": source["change_set_digest"],
        "commit_message": "autonomous effect" if phase == PHASE_LOCAL_COMMIT else "",
        "commit_message_digest": source["commit_message_digest"],
        "pull_request_title": title,
        "pull_request_body": body,
        "pull_request_body_digest": text_digest("pull_request_body", body),
        "pull_request_draft": phase == PHASE_CREATE_PR,
        "pull_request_number": source["pull_request_number"] if phase in {PHASE_MARK_PR_READY, PHASE_MERGE} else 0,
        "expected_head_sha": source["source_commit_sha"] if phase == PHASE_LOCAL_COMMIT else SHA_B,
        "requested_effect_phase": phase,
        "request_created_epoch": 100,
        "provenance_integrity_confirmed": True,
        "source_correspondence_confirmed": True,
    }
    return seal(request, REQUEST_DIGEST_FIELD)


def make_policy(source: dict) -> dict:
    policy = {
        "expected_source_lifecycle_receipt_digest": source[SOURCE_RECEIPT_DIGEST_FIELD],
        "expected_repository_full_name": source["repository_full_name"],
        "authorized_executor_ids": [source["executor_id"]],
        "allowed_effect_phases": [source["next_effect_phase"]],
        "allowed_base_branches": ["main"],
        "allowed_head_branch_prefixes": ["codeai/"],
        "allowed_remote_names": ["origin"],
        "allowed_merge_methods": ["merge"],
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
    return seal(policy, POLICY_DIGEST_FIELD)


def make_registry() -> dict:
    registry = {
        "registry_id": "git-effect-registry-001",
        "registry_revision": 0,
        "consumed_lifecycle_receipt_digests": [],
        "consumed_execution_nonce_digests": [],
        "consumed_count": 0,
        "last_execution_epoch": 0,
    }
    return seal(registry, REGISTRY_DIGEST_FIELD)


def base_adapter_result(phase: str) -> dict:
    return {
        "adapter_id": "test-adapter",
        "adapter_session_id": "adapter-session-001",
        "effect_phase": phase,
        "status": "completed",
        "exit_code": 0,
        "command_count": 1,
        "stdout": "ok",
        "stderr": "",
        "completed_epoch": 109,
        "local_commit_created": False,
        "local_commit_sha": "",
        "local_commit_parent_sha": "",
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
        "opaque_token_used": phase in {PHASE_CREATE_PR, PHASE_MARK_PR_READY, PHASE_MERGE},
        "exception_type": "",
    }


def completed_result(invocation: GitEffectInvocation) -> dict:
    result = base_adapter_result(invocation.effect_phase)
    if invocation.effect_phase == PHASE_LOCAL_COMMIT:
        result.update(local_commit_created=True, local_commit_sha=SHA_B, local_commit_parent_sha=SHA_A)
    elif invocation.effect_phase == PHASE_PUSH:
        result.update(branch_pushed=True, pushed_head_sha=SHA_B)
    elif invocation.effect_phase == PHASE_CREATE_PR:
        result.update(pull_request_created=True, pull_request_number=1303, pull_request_url_digest="8" * 64, pull_request_draft=True, pr_head_sha=SHA_B, pr_base_branch="main")
    elif invocation.effect_phase == PHASE_MARK_PR_READY:
        result.update(pull_request_number=1303, pull_request_draft=False, pr_head_sha=SHA_B, pr_base_branch="main", pull_request_marked_ready=True)
    elif invocation.effect_phase == PHASE_MERGE:
        result.update(pull_request_number=1303, merge_performed=True, merged_head_sha=SHA_B, merge_commit_sha=SHA_C)
    return result


class GitEffectExecutionTests(unittest.TestCase):
    def run_phase(self, phase: str, adapter=completed_result):
        source = make_source(phase)
        return build_codeai_autonomous_git_effect_execution(
            source_lifecycle_receipt=source,
            execution_request=make_request(source),
            execution_policy=make_policy(source),
            execution_registry=make_registry(),
            adapter=adapter,
        )

    def test_all_five_effect_phases_complete_and_consume_once(self):
        for phase in (PHASE_LOCAL_COMMIT, PHASE_PUSH, PHASE_CREATE_PR, PHASE_MARK_PR_READY, PHASE_MERGE):
            with self.subTest(phase=phase):
                result = self.run_phase(phase)
                self.assertEqual(result.status, STATUS_READY)
                self.assertEqual(result.issues, ())
                self.assertEqual(result.receipt["codeai_disposition"], DISPOSITION_COMPLETED)
                self.assertTrue(result.receipt["source_one_effect_lease_consumed"])
                self.assertTrue(result.receipt["exactly_one_adapter_invocation"])
                self.assertFalse(result.receipt["automatic_successor_effect_authority_granted"])
                self.assertEqual(result.next_registry["registry_revision"], 1)
                self.assertEqual(result.next_registry["consumed_count"], 1)
                self.assertIn(RECEIPT_DIGEST_FIELD, result.receipt)

    def test_replay_is_blocked_before_adapter_invocation(self):
        source = make_source(PHASE_PUSH)
        request = make_request(source)
        registry = make_registry()
        registry["consumed_lifecycle_receipt_digests"] = [source[SOURCE_RECEIPT_DIGEST_FIELD]]
        registry["consumed_execution_nonce_digests"] = ["7" * 64]
        registry["consumed_count"] = 1
        registry = seal({k: v for k, v in registry.items() if k != REGISTRY_DIGEST_FIELD}, REGISTRY_DIGEST_FIELD)
        calls = []

        def adapter(invocation):
            calls.append(invocation)
            return completed_result(invocation)

        result = build_codeai_autonomous_git_effect_execution(
            source_lifecycle_receipt=source,
            execution_request=request,
            execution_policy=make_policy(source),
            execution_registry=registry,
            adapter=adapter,
        )
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertEqual(calls, [])

    def test_wrong_effect_phase_is_blocked(self):
        source = make_source(PHASE_PUSH)
        request = make_request(source)
        request["requested_effect_phase"] = PHASE_MERGE
        request = seal({k: v for k, v in request.items() if k != REQUEST_DIGEST_FIELD}, REQUEST_DIGEST_FIELD)
        result = build_codeai_autonomous_git_effect_execution(source_lifecycle_receipt=source, execution_request=request, execution_policy=make_policy(source), execution_registry=make_registry(), adapter=completed_result)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("git_effect_correspondence_mismatch", result.issues)

    def test_forbidden_adapter_effect_is_quarantined_and_lease_consumed(self):
        def bad_adapter(invocation):
            result = completed_result(invocation)
            result["force_push_performed"] = True
            return result

        result = self.run_phase(PHASE_PUSH, bad_adapter)
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.receipt["codeai_disposition"], DISPOSITION_EVIDENCE_QUARANTINED)
        self.assertTrue(result.receipt["source_one_effect_lease_consumed"])
        self.assertTrue(result.receipt["evidence_quarantined"])
        self.assertTrue(result.receipt["reobservation_required"])
        self.assertEqual(result.next_registry["consumed_count"], 1)

    def test_adapter_exception_becomes_failed_evidence_and_consumes_lease(self):
        def exploding_adapter(invocation):
            raise RuntimeError("adapter unavailable")

        result = self.run_phase(PHASE_CREATE_PR, exploding_adapter)
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.receipt["codeai_disposition"], DISPOSITION_FAILED)
        self.assertTrue(result.receipt["effect_failure_recorded"])
        self.assertFalse(result.receipt["effect_completion_confirmed"])
        self.assertEqual(result.evidence["adapter_result"]["exception_type"], "RuntimeError")

    def test_merge_requires_green_pinned_source_gate(self):
        source = make_source(PHASE_MERGE)
        source["all_required_checks_successful"] = False
        source = seal({k: v for k, v in source.items() if k != SOURCE_RECEIPT_DIGEST_FIELD}, SOURCE_RECEIPT_DIGEST_FIELD)
        result = build_codeai_autonomous_git_effect_execution(source_lifecycle_receipt=source, execution_request=make_request(source), execution_policy=make_policy(source), execution_registry=make_registry(), adapter=completed_result)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("git_effect_phase_request_invalid", result.issues)

    def test_secret_read_policy_is_rejected(self):
        source = make_source(PHASE_CREATE_PR)
        policy = make_policy(source)
        policy["allow_secret_material_read"] = True
        policy = seal({k: v for k, v in policy.items() if k != POLICY_DIGEST_FIELD}, POLICY_DIGEST_FIELD)
        result = build_codeai_autonomous_git_effect_execution(source_lifecycle_receipt=source, execution_request=make_request(source), execution_policy=policy, execution_registry=make_registry(), adapter=completed_result)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("git_effect_scope_not_allowed", result.issues)

    def test_source_disposition_mode_mismatch_is_blocked(self):
        source = make_source(PHASE_PUSH)
        source["operating_mode"] = "local_git_effect_authorized"
        source = seal({k: v for k, v in source.items() if k != SOURCE_RECEIPT_DIGEST_FIELD}, SOURCE_RECEIPT_DIGEST_FIELD)
        result = build_codeai_autonomous_git_effect_execution(source_lifecycle_receipt=source, execution_request=make_request(source), execution_policy=make_policy(source), execution_registry=make_registry(), adapter=completed_result)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("source_lifecycle_receipt_not_active_one_effect_lease", result.issues)

    def test_failed_evidence_claiming_an_effect_is_quarantined(self):
        source = make_source(PHASE_PUSH)

        def adapter(invocation):
            value = base_adapter_result(invocation.effect_phase)
            value.update(status="failed", exit_code=1, branch_pushed=True, pushed_head_sha=SHA_B)
            return value

        result = build_codeai_autonomous_git_effect_execution(source_lifecycle_receipt=source, execution_request=make_request(source), execution_policy=make_policy(source), execution_registry=make_registry(), adapter=adapter)
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.receipt["codeai_disposition"], DISPOSITION_EVIDENCE_QUARANTINED)
        self.assertTrue(result.receipt["source_one_effect_lease_consumed"])
        self.assertTrue(result.receipt["reobservation_required"])


if __name__ == "__main__":
    unittest.main()
