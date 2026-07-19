#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
import unittest

from runtime.kuuos_codeai_autonomous_git_lifecycle_envelope_v0_1 import (
    POLICY_DIGEST_FIELD as LIFECYCLE_POLICY_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as LIFECYCLE_RECEIPT_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD as LIFECYCLE_REQUEST_DIGEST_FIELD,
    STATE_DIGEST_FIELD as LIFECYCLE_STATE_DIGEST_FIELD,
    PHASE_CREATE_PR,
    PHASE_LOCAL_COMMIT,
    PHASE_MARK_PR_READY,
    PHASE_MERGE,
    PHASE_PUSH,
    build_codeai_autonomous_git_lifecycle_envelope,
    canonical_digest,
)
from runtime.kuuos_codeai_autonomous_git_effect_execution_v0_1 import (
    POLICY_DIGEST_FIELD as EXECUTION_POLICY_DIGEST_FIELD,
    REGISTRY_DIGEST_FIELD as EXECUTION_REGISTRY_DIGEST_FIELD,
)
from runtime.kuuos_codeai_autonomous_git_effect_reobservation_v0_1 import (
    REGISTRY_DIGEST_FIELD as REOBSERVATION_REGISTRY_DIGEST_FIELD,
)
from runtime.kuuos_codeai_reobservation_gated_git_lifecycle_continuation_v0_1 import (
    REGISTRY_DIGEST_FIELD as CONTINUATION_REGISTRY_DIGEST_FIELD,
)
from runtime.kuuos_codeai_bounded_autonomous_git_lifecycle_loop_orchestration_v0_1 import (
    DISPOSITION_COMPLETED,
    DISPOSITION_EFFECT_BUDGET_EXHAUSTED,
    DISPOSITION_EXECUTION_FAILED,
    DISPOSITION_REOBSERVATION_QUARANTINED,
    POLICY_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD,
    REGISTRY_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    STATUS_BLOCKED,
    STATUS_READY,
    build_codeai_bounded_autonomous_git_lifecycle_loop_orchestration,
)
from scripts.check_codeai_autonomous_git_lifecycle_envelope_v0_1 import (
    load_example,
    reseal_policy as reseal_lifecycle_policy,
    reseal_request as reseal_lifecycle_request,
    reseal_state as reseal_lifecycle_state,
)
from tests.test_kuuos_codeai_reobservation_gated_git_lifecycle_continuation_v0_1 import (
    COMMIT_SHA,
)

SOURCE_SHA = "9956181589fe575277697f7c3538785de6962c1a"
MERGE_SHA = "c" * 40
D64 = {"url": "8" * 64}


def source_trajectory() -> dict:
    return deepcopy(load_example()["source_trajectory_receipt"])


def lifecycle_request(source: dict) -> dict:
    request = deepcopy(load_example()["lifecycle_request"])
    request["source_trajectory_receipt_digest"] = source[
        "codeai_autonomous_trajectory_receipt_digest"
    ]
    request["repository_full_name"] = source["repository_full_name"]
    request["source_commit_sha"] = source["source_commit_sha"]
    return reseal_lifecycle_request(request)


def lifecycle_policy(source: dict, *, evaluation_epoch: int) -> dict:
    policy = deepcopy(load_example()["lifecycle_policy"])
    policy["expected_source_trajectory_receipt_digest"] = source[
        "codeai_autonomous_trajectory_receipt_digest"
    ]
    policy["expected_repository_full_name"] = source["repository_full_name"]
    policy["expected_source_commit_sha"] = source["source_commit_sha"]
    policy["evaluation_epoch"] = evaluation_epoch
    policy["maximum_request_age"] = 100
    policy["maximum_state_age"] = 100
    return reseal_lifecycle_policy(policy)


def lifecycle_state(source: dict, *, local_commit: bool, observed_at: int) -> dict:
    state = deepcopy(load_example()["lifecycle_state"])
    state["source_trajectory_receipt_digest"] = source[
        "codeai_autonomous_trajectory_receipt_digest"
    ]
    state["repository_full_name"] = source["repository_full_name"]
    state["source_commit_sha"] = source["source_commit_sha"]
    state["observed_at_epoch"] = observed_at
    state["local_commit_created"] = local_commit
    state["local_commit_sha"] = COMMIT_SHA if local_commit else ""
    state["local_commit_parent_sha"] = source["source_commit_sha"] if local_commit else ""
    return reseal_lifecycle_state(state)


def seal(value: dict, field: str) -> dict:
    out = deepcopy(value)
    out.pop(field, None)
    out[field] = canonical_digest(out)
    return out


def text_digest(label: str, value: str) -> str:
    return canonical_digest({label: value})


def fixture(*, max_effects: int = 5):
    source = source_trajectory()
    message = "bounded autonomous lifecycle"
    message_digest = text_digest("commit_message", message)
    lifecycle_req = lifecycle_request(source)
    lifecycle_req["commit_message_digest"] = message_digest
    lifecycle_req["request_created_epoch"] = 300
    lifecycle_req[LIFECYCLE_REQUEST_DIGEST_FIELD] = canonical_digest(
        {k: v for k, v in lifecycle_req.items() if k != LIFECYCLE_REQUEST_DIGEST_FIELD}
    )
    lifecycle_pol = lifecycle_policy(source, evaluation_epoch=300)
    state = lifecycle_state(source, local_commit=False, observed_at=300)
    state["commit_message_digest"] = message_digest
    state[LIFECYCLE_STATE_DIGEST_FIELD] = canonical_digest(
        {k: v for k, v in state.items() if k != LIFECYCLE_STATE_DIGEST_FIELD}
    )
    initial = build_codeai_autonomous_git_lifecycle_envelope(
        source_trajectory_receipt=source,
        lifecycle_request=lifecycle_req,
        lifecycle_state=state,
        lifecycle_policy=lifecycle_pol,
    )
    assert initial.status == STATUS_READY and initial.receipt is not None
    initial_receipt = initial.receipt
    request = {
        "loop_id": "git-loop-001",
        "loop_revision": "1",
        "loop_session_id": "git-loop-session-001",
        "loop_nonce_digest": "7" * 64,
        "source_trajectory_receipt_digest": source["codeai_autonomous_trajectory_receipt_digest"],
        "initial_lifecycle_receipt_digest": initial_receipt[LIFECYCLE_RECEIPT_DIGEST_FIELD],
        "lifecycle_id": initial_receipt["lifecycle_id"],
        "executor_id": initial_receipt["executor_id"],
        "observer_id": "codeai-git-observer",
        "repository_full_name": initial_receipt["repository_full_name"],
        "source_commit_sha": initial_receipt["source_commit_sha"],
        "base_branch": initial_receipt["base_branch"],
        "head_branch": initial_receipt["head_branch"],
        "remote_name": initial_receipt["remote_name"],
        "change_set_digest": initial_receipt["change_set_digest"],
        "commit_message": message,
        "commit_message_digest": message_digest,
        "merge_method": initial_receipt["merge_method"],
        "pull_request_title": "Bounded lifecycle PR",
        "pull_request_body": "Exercise the bounded lifecycle.",
        "pull_request_body_digest": text_digest(
            "pull_request_body", "Exercise the bounded lifecycle."
        ),
        "requested_max_effect_count": max_effects,
        "prior_lifecycle_execution_session_ids": [initial_receipt["execution_session_id"]],
        "prior_lifecycle_execution_nonce_digests": [lifecycle_req["execution_nonce_digest"]],
        "prior_lifecycle_receipt_digests": [initial_receipt[LIFECYCLE_RECEIPT_DIGEST_FIELD]],
        "request_created_epoch": 300,
        "provenance_integrity_confirmed": True,
        "source_correspondence_confirmed": True,
    }
    request = seal(request, REQUEST_DIGEST_FIELD)
    policy = {
        "expected_source_trajectory_receipt_digest": source["codeai_autonomous_trajectory_receipt_digest"],
        "expected_initial_lifecycle_receipt_digest": initial_receipt[LIFECYCLE_RECEIPT_DIGEST_FIELD],
        "expected_repository_full_name": initial_receipt["repository_full_name"],
        "authorized_executor_ids": [initial_receipt["executor_id"]],
        "authorized_observer_ids": ["codeai-git-observer"],
        "allowed_effect_phases": [
            PHASE_LOCAL_COMMIT, PHASE_PUSH, PHASE_CREATE_PR, PHASE_MARK_PR_READY, PHASE_MERGE
        ],
        "allowed_base_branches": [initial_receipt["base_branch"]],
        "allowed_head_branch_prefixes": ["agent/"],
        "allowed_remote_names": [initial_receipt["remote_name"]],
        "allowed_merge_methods": [initial_receipt["merge_method"]],
        "required_check_names": list(lifecycle_pol["required_check_names"]),
        "maximum_effect_count": 5,
        "maximum_total_execution_command_count": 10,
        "maximum_total_execution_output_bytes": 10000,
        "maximum_total_reobservation_command_count": 25,
        "maximum_total_reobservation_output_bytes": 50000,
        "maximum_execution_command_count_per_effect": 2,
        "maximum_execution_output_bytes_per_effect": 2000,
        "maximum_execution_timeout_seconds_per_effect": 120,
        "maximum_reobservation_command_count_per_effect": 5,
        "maximum_reobservation_output_bytes_per_effect": 10000,
        "maximum_request_age": 100,
        "maximum_observation_age": 100,
        "maximum_state_age": 100,
        "maximum_registry_entries": 16,
        "evaluation_epoch": 300,
        "allow_local_commit": True,
        "allow_push": True,
        "allow_pull_request_creation": True,
        "allow_pull_request_readiness": True,
        "allow_merge": True,
        "allow_opaque_token_use": True,
        "allow_effect_execution": True,
        "allow_reobservation": True,
        "allow_continuation_evaluation": True,
        "allow_force_push": False,
        "allow_remote_branch_deletion": False,
        "allow_admin_merge_bypass": False,
        "allow_deployment": False,
        "allow_secret_material_read": False,
        "allow_networked_reobservation": False,
        "allow_human_handover": False,
        "allow_unbounded_continuation": False,
    }
    policy = seal(policy, POLICY_DIGEST_FIELD)
    loop_registry = seal({
        "registry_id": "git-loop-registry-001",
        "registry_revision": 0,
        "consumed_initial_lifecycle_receipt_digests": [],
        "consumed_loop_nonce_digests": [],
        "completed_loop_count": 0,
        "total_effect_count": 0,
        "last_loop_epoch": 0,
    }, REGISTRY_DIGEST_FIELD)
    execution_registry = seal({
        "registry_id": "git-effect-registry-001",
        "registry_revision": 0,
        "consumed_lifecycle_receipt_digests": [],
        "consumed_execution_nonce_digests": [],
        "consumed_count": 0,
        "last_execution_epoch": 0,
    }, EXECUTION_REGISTRY_DIGEST_FIELD)
    reobservation_registry = seal({
        "registry_id": "git-reobservation-registry-001",
        "registry_revision": 0,
        "consumed_execution_receipt_digests": [],
        "consumed_reobservation_nonce_digests": [],
        "consumed_count": 0,
        "last_reobservation_epoch": 0,
    }, REOBSERVATION_REGISTRY_DIGEST_FIELD)
    continuation_registry = seal({
        "registry_id": "git-continuation-registry-001",
        "registry_revision": 0,
        "consumed_reobservation_receipt_digests": [],
        "consumed_continuation_nonce_digests": [],
        "consumed_count": 0,
        "last_continuation_epoch": 0,
    }, CONTINUATION_REGISTRY_DIGEST_FIELD)
    return source, initial_receipt, request, policy, loop_registry, execution_registry, reobservation_registry, continuation_registry


class Simulation:
    def __init__(self):
        self.local_commit = False
        self.pushed = False
        self.pr_created = False
        self.draft = False
        self.checks = False
        self.merged = False
        self.execution_failure_phase: str | None = None
        self.bad_observation = False
        self.source_trajectory_digest = ""
        self.executor_id = ""
        self.source_commit_sha = SOURCE_SHA
        self.base_branch = "main"

    def execute(self, invocation):
        phase = invocation.effect_phase
        failed = phase == self.execution_failure_phase
        result = {
            "adapter_id": "simulated-git-adapter",
            "adapter_session_id": "simulated-execution-session",
            "effect_phase": phase,
            "status": "failed" if failed else "completed",
            "exit_code": 1 if failed else 0,
            "command_count": 1,
            "stdout": "" if failed else "ok",
            "stderr": "failed" if failed else "",
            "completed_epoch": 300,
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
        if failed:
            return result
        if phase == PHASE_LOCAL_COMMIT:
            self.local_commit = True
            result.update(local_commit_created=True, local_commit_sha=COMMIT_SHA, local_commit_parent_sha=self.source_commit_sha)
        elif phase == PHASE_PUSH:
            self.pushed = True
            result.update(branch_pushed=True, pushed_head_sha=COMMIT_SHA)
        elif phase == PHASE_CREATE_PR:
            self.pr_created = True
            self.draft = True
            result.update(
                pull_request_created=True, pull_request_number=1309,
                pull_request_url_digest=D64["url"], pull_request_draft=True,
                pr_head_sha=COMMIT_SHA, pr_base_branch=self.base_branch,
            )
        elif phase == PHASE_MARK_PR_READY:
            self.draft = False
            self.checks = True
            result.update(
                pull_request_number=1309, pull_request_draft=False,
                pr_head_sha=COMMIT_SHA, pr_base_branch=self.base_branch,
                pull_request_marked_ready=True,
            )
        elif phase == PHASE_MERGE:
            self.merged = True
            result.update(
                pull_request_number=1309, merge_performed=True,
                merged_head_sha=COMMIT_SHA, merge_commit_sha=MERGE_SHA,
            )
        return result

    def observe(self, invocation):
        required = list(invocation.required_check_names)
        result = {
            "adapter_id": "simulated-read-only-observer",
            "adapter_session_id": "simulated-observation-session",
            "status": "observed",
            "command_count": 1,
            "output_bytes": 512,
            "completed_epoch": 300,
            "network_accessed": False,
            "secret_material_read": False,
            "git_write_performed": False,
            "deployment_performed": False,
            "exception_type": "",
            "lifecycle_id": invocation.lifecycle_id,
            "source_trajectory_receipt_digest": self.source_trajectory_digest,
            "repository_full_name": invocation.repository_full_name,
            "source_commit_sha": invocation.source_commit_sha,
            "executor_id": self.executor_id,
            "base_branch": invocation.base_branch,
            "head_branch": invocation.head_branch,
            "remote_name": invocation.remote_name,
            "change_set_digest": invocation.change_set_digest,
            "commit_message_digest": invocation.commit_message_digest,
            "merge_method": invocation.merge_method,
            "local_commit_created": self.local_commit,
            "local_commit_sha": COMMIT_SHA if self.local_commit else "",
            "local_commit_parent_sha": self.source_commit_sha if self.local_commit else "",
            "branch_pushed": self.pushed,
            "pushed_head_sha": COMMIT_SHA if self.pushed else "",
            "pull_request_created": self.pr_created,
            "pull_request_number": 1309 if self.pr_created else 0,
            "pull_request_url_digest": D64["url"] if self.pr_created else "",
            "pull_request_draft": self.draft if self.pr_created else False,
            "pr_head_sha": COMMIT_SHA if self.pr_created else "",
            "pr_base_branch": self.base_branch if self.pr_created else "",
            "checks_observed": self.checks,
            "required_check_names": required,
            "successful_check_names": required if self.checks else [],
            "pending_check_names": [],
            "failed_check_names": [],
            "mergeable": self.checks,
            "unresolved_blocker_count": 0,
            "merge_performed": self.merged,
            "merged_head_sha": COMMIT_SHA if self.merged else "",
            "merge_commit_sha": MERGE_SHA if self.merged else "",
            "force_push_performed": False,
            "remote_branch_deleted": False,
            "admin_merge_bypass_used": False,
            "human_handover_performed": False,
            "external_authority_handover_performed": False,
            "observed_at_epoch": 300,
            "provenance_integrity_confirmed": True,
            "source_correspondence_confirmed": True,
        }
        if self.bad_observation:
            result["git_write_performed"] = True
        return result


def run_loop(*, max_effects=5, mutate=None, simulation=None):
    values = list(fixture(max_effects=max_effects))
    if mutate is not None:
        mutate(values)
    sim = simulation or Simulation()
    sim.source_trajectory_digest = values[0]["codeai_autonomous_trajectory_receipt_digest"]
    sim.executor_id = values[1]["executor_id"]
    sim.source_commit_sha = values[1]["source_commit_sha"]
    sim.base_branch = values[1]["base_branch"]
    return build_codeai_bounded_autonomous_git_lifecycle_loop_orchestration(
        source_trajectory_receipt=values[0],
        initial_lifecycle_receipt=values[1],
        loop_request=values[2],
        loop_policy=values[3],
        loop_registry=values[4],
        execution_registry=values[5],
        reobservation_registry=values[6],
        continuation_registry=values[7],
        execution_adapter=sim.execute,
        reobservation_adapter=sim.observe,
    )


class BoundedAutonomousGitLifecycleLoopTests(unittest.TestCase):
    def test_five_effect_lifecycle_completes(self):
        result = run_loop()
        self.assertEqual(result.status, STATUS_READY, result.issues)
        self.assertEqual(result.receipt["codeai_disposition"], DISPOSITION_COMPLETED)
        self.assertEqual(result.receipt["effect_count"], 5)
        self.assertTrue(result.receipt["final_lifecycle_completed"])
        self.assertFalse(result.receipt["final_execution_lease_issued"])
        self.assertEqual(len(result.evidence["iteration_records"]), 5)
        self.assertFalse(result.receipt["automatic_unbounded_continuation_performed"])
        self.assertFalse(result.receipt["general_git_authority_granted"])
        self.assertEqual(
            result.next_loop_registry["total_effect_count"], 5
        )

    def test_effect_count_budget_stops_with_fresh_active_lease(self):
        result = run_loop(max_effects=2)
        self.assertEqual(result.status, STATUS_READY, result.issues)
        self.assertEqual(
            result.receipt["codeai_disposition"], DISPOSITION_EFFECT_BUDGET_EXHAUSTED
        )
        self.assertEqual(result.receipt["effect_count"], 2)
        self.assertTrue(result.receipt["final_execution_lease_issued"])
        self.assertEqual(result.final_lifecycle_receipt["next_effect_phase"], PHASE_CREATE_PR)

    def test_failed_execution_is_reobserved_then_stops_without_retry(self):
        sim = Simulation()
        sim.execution_failure_phase = PHASE_PUSH
        result = run_loop(simulation=sim)
        self.assertEqual(result.status, STATUS_READY, result.issues)
        self.assertEqual(result.receipt["codeai_disposition"], DISPOSITION_EXECUTION_FAILED)
        self.assertEqual(result.receipt["effect_count"], 2)
        self.assertTrue(result.receipt["final_execution_lease_issued"])
        self.assertEqual(result.final_lifecycle_receipt["next_effect_phase"], PHASE_PUSH)

    def test_effect_bearing_reobservation_is_quarantined(self):
        sim = Simulation()
        sim.bad_observation = True
        result = run_loop(simulation=sim)
        self.assertEqual(result.status, STATUS_READY, result.issues)
        self.assertEqual(
            result.receipt["codeai_disposition"], DISPOSITION_REOBSERVATION_QUARANTINED
        )
        self.assertEqual(result.receipt["effect_count"], 0)

    def test_request_tamper_blocks_before_adapter(self):
        def mutate(values):
            values[2]["repository_full_name"] = "other/repo"
        result = run_loop(mutate=mutate)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIsNone(result.receipt)

    def test_request_digest_reseal_still_fails_correspondence(self):
        def mutate(values):
            values[2]["repository_full_name"] = "other/repo"
            values[2] = seal(values[2], REQUEST_DIGEST_FIELD)
        result = run_loop(mutate=mutate)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("bounded_git_lifecycle_loop_correspondence_mismatch", result.issues)

    def test_loop_nonce_replay_blocks(self):
        def mutate(values):
            values[4]["consumed_initial_lifecycle_receipt_digests"] = [
                values[1][LIFECYCLE_RECEIPT_DIGEST_FIELD]
            ]
            values[4]["consumed_loop_nonce_digests"] = [values[2]["loop_nonce_digest"]]
            values[4]["completed_loop_count"] = 1
            values[4] = seal(values[4], REGISTRY_DIGEST_FIELD)
        result = run_loop(mutate=mutate)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("bounded_git_lifecycle_loop_freshness_or_replay_violation", result.issues)

    def test_unbounded_policy_is_rejected(self):
        def mutate(values):
            values[3]["allow_unbounded_continuation"] = True
            values[3] = seal(values[3], POLICY_DIGEST_FIELD)
        result = run_loop(mutate=mutate)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("bounded_git_lifecycle_loop_policy_not_safe", result.issues)

    def test_destructive_policy_is_rejected(self):
        def mutate(values):
            values[3]["allow_force_push"] = True
            values[3] = seal(values[3], POLICY_DIGEST_FIELD)
        result = run_loop(mutate=mutate)
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_budget_cannot_exceed_policy(self):
        def mutate(values):
            values[2]["requested_max_effect_count"] = 6
            values[2] = seal(values[2], REQUEST_DIGEST_FIELD)
        result = run_loop(mutate=mutate)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("bounded_git_lifecycle_loop_policy_not_safe", result.issues)

    def test_initial_lifecycle_receipt_replay_blocks(self):
        def mutate(values):
            values[4]["consumed_initial_lifecycle_receipt_digests"] = [
                values[1][LIFECYCLE_RECEIPT_DIGEST_FIELD]
            ]
            values[4]["consumed_loop_nonce_digests"] = ["8" * 64]
            values[4]["completed_loop_count"] = 1
            values[4] = seal(values[4], REGISTRY_DIGEST_FIELD)
        result = run_loop(mutate=mutate)
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_registry_parallel_history_mismatch_blocks(self):
        def mutate(values):
            values[4]["consumed_loop_nonce_digests"] = ["8" * 64]
            values[4] = seal(values[4], REGISTRY_DIGEST_FIELD)
        result = run_loop(mutate=mutate)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertTrue(any("parallel_history_mismatch" in item for item in result.issues))

    def test_source_trajectory_tamper_blocks(self):
        def mutate(values):
            values[0]["verification_outcome"] = "failed"
        result = run_loop(mutate=mutate)
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_initial_lifecycle_tamper_blocks(self):
        def mutate(values):
            values[1]["merge_method"] = "merge"
        result = run_loop(mutate=mutate)
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_missing_request_field_blocks(self):
        def mutate(values):
            del values[2]["observer_id"]
        result = run_loop(mutate=mutate)
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_extra_policy_field_blocks(self):
        def mutate(values):
            values[3]["extra"] = True
        result = run_loop(mutate=mutate)
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_invalid_execution_registry_blocks(self):
        def mutate(values):
            values[5]["consumed_count"] = 1
            values[5] = seal(values[5], EXECUTION_REGISTRY_DIGEST_FIELD)
        result = run_loop(mutate=mutate)
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_invalid_reobservation_registry_blocks(self):
        def mutate(values):
            values[6]["registry_revision"] = -1
            values[6] = seal(values[6], REOBSERVATION_REGISTRY_DIGEST_FIELD)
        result = run_loop(mutate=mutate)
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_invalid_continuation_registry_blocks(self):
        def mutate(values):
            values[7]["consumed_count"] = 1
            values[7] = seal(values[7], CONTINUATION_REGISTRY_DIGEST_FIELD)
        result = run_loop(mutate=mutate)
        self.assertEqual(result.status, STATUS_BLOCKED)

    def test_receipt_digest_is_canonical(self):
        result = run_loop()
        expected = canonical_digest({k: v for k, v in result.receipt.items() if k != RECEIPT_DIGEST_FIELD})
        self.assertEqual(result.receipt[RECEIPT_DIGEST_FIELD], expected)

    def test_final_receipt_grants_no_general_successor_authority(self):
        result = run_loop(max_effects=1)
        self.assertFalse(result.receipt["general_successor_stage_authority_granted"])
        self.assertFalse(result.receipt["active_now"])
        self.assertFalse(result.receipt["concurrent_effect_leases_executed"])


if __name__ == "__main__":
    unittest.main()
