from __future__ import annotations

from copy import deepcopy
import unittest

from runtime.kuuos_codeai_candidate_patch_envelope_v0_1 import canonical_digest, seal
from runtime.kuuos_codeai_autonomous_verification_execution_v0_1 import (
    APPLICATION_RECEIPT_DIGEST_FIELD,
    CANDIDATE_DIGEST_FIELD,
    CANDIDATE_RECEIPT_DIGEST_FIELD,
    DISPOSITION_ABORTED_BY_BUDGET,
    DISPOSITION_COMPLETED,
    DISPOSITION_COMPLETED_WITH_FAILURES,
    EVIDENCE_BUNDLE_DIGEST_FIELD,
    INDEPENDENT_EVIDENCE_DIGEST_FIELD,
    PLAN_DIGEST_FIELD,
    POLICY_DIGEST_FIELD,
    PROFILE_VERSION,
    RECEIPT_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    STATUS_BLOCKED,
    STATUS_READY,
    build_codeai_autonomous_verification_execution,
)

EPOCH = 1784430000
SOURCE_SHA = "2cfb04b737379d5605f57e97e67da1a005ccdae5"
HEX64 = "1" * 64


def candidate_receipt():
    value = {
        "schema_version": "v0.1",
        "profile_version": "CodeAI Candidate Patch v0.1",
        CANDIDATE_DIGEST_FIELD: "2" * 64,
        "patch_artifact_digest": "3" * 64,
        "repository_full_name": "itakura-hidetoshi/KuuOS",
        "source_commit_sha": SOURCE_SHA,
        "codeai_disposition": "candidate_patch_supported",
        "candidate_patch_ready": True,
        "verification_lease_issued": False,
        "execution_lease_issued": False,
        "repository_mutation_performed": False,
        "git_ref_changed": False,
        "branch_created": False,
        "commit_created": False,
        "push_performed": False,
        "pull_request_created": False,
        "merge_performed": False,
        "deployment_performed": False,
        "secret_access_performed": False,
    }
    return seal(value, CANDIDATE_RECEIPT_DIGEST_FIELD)


def fixture(checks=None, *, output_limit=4096):
    candidate = candidate_receipt()
    repository = {
        "docs/CodeAI/EXISTING.md": "# Existing\n\nChanged in isolated snapshot.\n",
        "tests/smoke.py": "print('ok')\n",
    }
    source_snapshot_digest = canonical_digest(
        {"docs/CodeAI/EXISTING.md": "# Existing\n\nOriginal text.\n", "tests/smoke.py": "print('ok')\n"}
    )
    application = seal(
        {
            "schema_version": "v0.1",
            "profile_version": "CodeAI Autonomous Isolated Candidate Application v0.1",
            "source_candidate_receipt_digest": candidate[CANDIDATE_RECEIPT_DIGEST_FIELD],
            "selected_candidate_digest": candidate[CANDIDATE_DIGEST_FIELD],
            "selected_patch_artifact_digest": candidate["patch_artifact_digest"],
            "source_repository_snapshot_digest": source_snapshot_digest,
            "resulting_repository_snapshot_digest": canonical_digest(repository),
            "repository_full_name": candidate["repository_full_name"],
            "source_commit_sha": candidate["source_commit_sha"],
            "isolated_patch_applied": True,
            "isolated_snapshot_materialized": True,
            "verification_workspace_ready": True,
            "source_snapshot_verified": True,
            "candidate_correspondence_verified": True,
            "input_repository_snapshot_mutated": False,
            "live_repository_patch_applied": False,
            "repository_mutation_performed": False,
            "git_ref_changed": False,
            "branch_created": False,
            "commit_created": False,
            "push_performed": False,
            "pull_request_created": False,
            "merge_performed": False,
            "deployment_performed": False,
            "secret_access_performed": False,
            "verification_executed": False,
            "verification_lease_issued": False,
            "execution_lease_issued": False,
        },
        APPLICATION_RECEIPT_DIGEST_FIELD,
    )
    if checks is None:
        checks = [
            {
                "check_id": "python-smoke",
                "executable": "python3",
                "arguments": ["tests/smoke.py"],
                "workdir": ".",
                "timeout_seconds": 30,
                "expected_exit_codes": [0],
                "environment": {"PYTHONPATH": "."},
            },
            {
                "check_id": "manifest-json",
                "executable": "python3",
                "arguments": ["-m", "json.tool", "manifest.json"],
                "workdir": ".",
                "timeout_seconds": 20,
                "expected_exit_codes": [0],
                "environment": {},
            },
        ]
    plan = seal(
        {
            "plan_id": "codeai-verification-plan-v0-1-001",
            "plan_revision": "r1",
            "checks": checks,
            "plan_created_epoch": EPOCH - 20,
        },
        PLAN_DIGEST_FIELD,
    )
    request = seal(
        {
            "execution_request_id": "codeai-verification-execution-v0-1-001",
            "execution_request_revision": "r1",
            "source_candidate_receipt_digest": candidate[CANDIDATE_RECEIPT_DIGEST_FIELD],
            "source_application_receipt_digest": application[APPLICATION_RECEIPT_DIGEST_FIELD],
            "candidate_digest": candidate[CANDIDATE_DIGEST_FIELD],
            "patch_artifact_digest": candidate["patch_artifact_digest"],
            "source_repository_snapshot_digest": source_snapshot_digest,
            "resulting_repository_snapshot_digest": canonical_digest(repository),
            "repository_full_name": candidate["repository_full_name"],
            "source_commit_sha": candidate["source_commit_sha"],
            "verification_plan_digest": plan[PLAN_DIGEST_FIELD],
            "verification_id": "verification-v0-1-001",
            "verifier_id": "runner-neutral-verifier",
            "reviewer_id": "independent-reviewer",
            "verification_session_id": "verification-session-v0-1-001",
            "verification_nonce_digest": "4" * 64,
            "evidence_format": "codeai_execution_evidence_v0_1",
            "toolchain_digest": "5" * 64,
            "environment_digest": "6" * 64,
            "verification_protocol_digest": "7" * 64,
            "requested_by_actor_id": "codeai-orchestrator",
            "request_created_epoch": EPOCH - 10,
        },
        REQUEST_DIGEST_FIELD,
    )
    policy = seal(
        {
            "expected_source_candidate_receipt_digest": candidate[CANDIDATE_RECEIPT_DIGEST_FIELD],
            "expected_source_application_receipt_digest": application[APPLICATION_RECEIPT_DIGEST_FIELD],
            "expected_candidate_digest": candidate[CANDIDATE_DIGEST_FIELD],
            "expected_patch_artifact_digest": candidate["patch_artifact_digest"],
            "expected_source_repository_snapshot_digest": source_snapshot_digest,
            "expected_resulting_repository_snapshot_digest": canonical_digest(repository),
            "expected_repository_full_name": candidate["repository_full_name"],
            "expected_source_commit_sha": candidate["source_commit_sha"],
            "expected_verification_plan_digest": plan[PLAN_DIGEST_FIELD],
            "allowed_check_ids": [check["check_id"] for check in checks],
            "allowed_executable_prefixes": ["python3"],
            "allowed_workdir_prefixes": ["."],
            "environment_allowlist": ["PYTHONPATH"],
            "maximum_command_count": 4,
            "maximum_timeout_seconds_per_check": 60,
            "maximum_total_timeout_seconds": 120,
            "maximum_stdout_bytes_per_check": 1024,
            "maximum_stderr_bytes_per_check": 1024,
            "maximum_total_output_bytes": output_limit,
            "maximum_repository_path_count": 20,
            "maximum_repository_snapshot_bytes": 65536,
            "network_access_allowed": False,
            "secrets_allowed": False,
            "live_repository_access_allowed": False,
            "git_operations_allowed": False,
            "evaluation_epoch": EPOCH,
            "maximum_request_age": 300,
        },
        POLICY_DIGEST_FIELD,
    )
    return candidate, application, repository, plan, request, policy


def runner_result(invocation, *, exit_code=0, stdout="ok\n", stderr="", timed_out=False, exception_type=None, effects=False):
    return {
        "runner_id": "in-memory-runner",
        "runner_session_id": "runner-session-" + invocation.check_id,
        "check_id": invocation.check_id,
        "exit_code": exit_code,
        "stdout": stdout,
        "stderr": stderr,
        "duration_ms": 12,
        "timed_out": timed_out,
        "exception_type": exception_type,
        "started_epoch": EPOCH - 5,
        "completed_epoch": EPOCH - 4,
        "network_used": effects,
        "secret_accessed": False,
        "live_repository_accessed": False,
        "git_effect_performed": False,
    }


def build(data, adapter):
    candidate, application, repository, plan, request, policy = data
    return build_codeai_autonomous_verification_execution(
        source_candidate_receipt=candidate,
        source_application_receipt=application,
        resulting_repository_files=repository,
        verification_plan=plan,
        execution_request=request,
        execution_policy=policy,
        runner_adapter=adapter,
    )


class AutonomousVerificationExecutionTests(unittest.TestCase):
    def test_01_executes_declared_checks_and_seals_evidence(self):
        data = fixture()
        result = build(data, lambda invocation: runner_result(invocation))
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.receipt["codeai_disposition"], DISPOSITION_COMPLETED)
        self.assertEqual(result.evidence_bundle["passed_check_count"], 2)
        self.assertEqual(result.receipt["failed_check_count"], 0)
        self.assertEqual(result.receipt[RECEIPT_DIGEST_FIELD], canonical_digest({k: v for k, v in result.receipt.items() if k != RECEIPT_DIGEST_FIELD}))

    def test_02_nonzero_exit_is_failed_evidence_not_block(self):
        data = fixture()
        result = build(data, lambda invocation: runner_result(invocation, exit_code=1, stderr="failed\n"))
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.receipt["codeai_disposition"], DISPOSITION_COMPLETED_WITH_FAILURES)
        self.assertEqual(result.evidence_bundle["failed_check_count"], 2)

    def test_03_timeout_is_not_success(self):
        data = fixture()
        result = build(data, lambda invocation: runner_result(invocation, exit_code=None, timed_out=True))
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.evidence_bundle["records"][0]["execution_status"], "timed_out")
        self.assertNotIn("python-smoke", result.evidence_bundle["passed_check_ids"])

    def test_04_runner_exception_isolated_and_sibling_preserved(self):
        data = fixture()
        calls = []
        def adapter(invocation):
            calls.append(invocation.check_id)
            if invocation.check_id == "python-smoke":
                raise RuntimeError("runner unavailable")
            return runner_result(invocation)
        result = build(data, adapter)
        self.assertEqual(calls, ["python-smoke", "manifest-json"])
        self.assertEqual(result.evidence_bundle["runner_exception_check_ids"], ["python-smoke"])
        self.assertIn("manifest-json", result.evidence_bundle["passed_check_ids"])

    def test_05_candidate_correspondence_mismatch_blocks_before_runner(self):
        data = list(fixture())
        request = dict(data[4])
        request["candidate_digest"] = "8" * 64
        data[4] = seal({k: v for k, v in request.items() if k != REQUEST_DIGEST_FIELD}, REQUEST_DIGEST_FIELD)
        calls = []
        result = build(tuple(data), lambda invocation: calls.append(invocation))
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertEqual(calls, [])

    def test_06_application_receipt_tamper_blocks(self):
        data = list(fixture())
        data[1] = dict(data[1])
        data[1]["verification_workspace_ready"] = False
        result = build(tuple(data), lambda invocation: runner_result(invocation))
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertTrue(any("source_application" in issue for issue in result.issues))

    def test_07_resulting_snapshot_mismatch_blocks(self):
        data = list(fixture())
        data[2] = dict(data[2])
        data[2]["extra.txt"] = "drift\n"
        result = build(tuple(data), lambda invocation: runner_result(invocation))
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertTrue(any("result_snapshot" in issue for issue in result.issues))

    def test_08_stale_request_blocks(self):
        data = list(fixture())
        request = dict(data[4])
        request["request_created_epoch"] = EPOCH - 1000
        data[4] = seal({k: v for k, v in request.items() if k != REQUEST_DIGEST_FIELD}, REQUEST_DIGEST_FIELD)
        result = build(tuple(data), lambda invocation: runner_result(invocation))
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("verification_execution_request_window_invalid", result.issues)

    def test_09_command_count_budget_blocks(self):
        data = list(fixture())
        policy = dict(data[5])
        policy["maximum_command_count"] = 1
        data[5] = seal({k: v for k, v in policy.items() if k != POLICY_DIGEST_FIELD}, POLICY_DIGEST_FIELD)
        result = build(tuple(data), lambda invocation: runner_result(invocation))
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("verification_command_count_budget_exceeded", result.issues)

    def test_10_disallowed_executable_blocks(self):
        checks = [{
            "check_id": "shell-check", "executable": "bash", "arguments": ["-lc", "true"],
            "workdir": ".", "timeout_seconds": 5, "expected_exit_codes": [0], "environment": {},
        }]
        data = fixture(checks)
        result = build(data, lambda invocation: runner_result(invocation))
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("verification_executable_not_allowed:shell-check", result.issues)

    def test_11_environment_allowlist_is_fail_closed(self):
        checks = [{
            "check_id": "python-smoke", "executable": "python3", "arguments": ["tests/smoke.py"],
            "workdir": ".", "timeout_seconds": 5, "expected_exit_codes": [0],
            "environment": {"OPENAI_API_KEY": "forbidden"},
        }]
        data = fixture(checks)
        result = build(data, lambda invocation: runner_result(invocation))
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("verification_environment_not_allowed:python-smoke", result.issues)

    def test_12_runner_reported_effect_is_rejected(self):
        data = fixture()
        result = build(data, lambda invocation: runner_result(invocation, effects=True))
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.evidence_bundle["records"][0]["execution_status"], "runner_effect_rejected")
        self.assertFalse(result.receipt["network_access_performed"])
        self.assertFalse(result.receipt["git_ref_changed"])

    def test_13_output_bounds_projection_and_no_authority(self):
        data = fixture(output_limit=1500)
        result = build(data, lambda invocation: runner_result(invocation, stdout="x" * 2000))
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.receipt["codeai_disposition"], DISPOSITION_ABORTED_BY_BUDGET)
        self.assertTrue(result.evidence_bundle["records"][0]["stdout_truncated"])
        self.assertEqual(result.independent_verification_evidence[INDEPENDENT_EVIDENCE_DIGEST_FIELD], canonical_digest({k: v for k, v in result.independent_verification_evidence.items() if k != INDEPENDENT_EVIDENCE_DIGEST_FIELD}))
        self.assertTrue(result.receipt["independent_verification_evidence_projected"])
        for field in (
            "selection_authority_granted", "verification_authority_granted",
            "execution_authority_granted", "merge_authority_granted",
            "deployment_authority_granted", "secret_access_authority_granted",
            "successor_stage_authority_granted",
        ):
            self.assertFalse(result.receipt[field])
        self.assertFalse(result.receipt["tests_passing_treated_as_proof"])
        self.assertFalse(result.receipt["verification_evidence_treated_as_merge_authority"])


if __name__ == "__main__":
    unittest.main()
