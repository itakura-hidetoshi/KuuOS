#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from runtime.kuuos_codeai_candidate_patch_envelope_v0_1 import (
    CANDIDATE_DIGEST_FIELD as PATCH_CANDIDATE_DIGEST_FIELD,
    canonical_digest,
    seal,
)
from runtime.kuuos_codeai_autonomous_structured_edit_synthesis_v0_1 import (
    ProviderAdapter,
    RECEIPT_DIGEST_FIELD as STRUCTURED_RECEIPT_DIGEST_FIELD,
    STATUS_READY as SYNTHESIS_READY,
    build_codeai_autonomous_structured_edit_synthesis,
)
from runtime.kuuos_codeai_autonomous_candidate_portfolio_selection_v0_1 import (
    POLICY_DIGEST_FIELD as SELECTION_POLICY_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as SELECTION_RECEIPT_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD as SELECTION_REQUEST_DIGEST_FIELD,
    STATUS_READY as SELECTION_READY,
    build_codeai_autonomous_candidate_portfolio_selection,
)
from runtime.kuuos_codeai_autonomous_isolated_candidate_application_v0_1 import (
    POLICY_DIGEST_FIELD as APPLICATION_POLICY_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD as APPLICATION_REQUEST_DIGEST_FIELD,
    STATUS_READY as APPLICATION_READY,
    build_codeai_autonomous_isolated_candidate_application,
)
from runtime.kuuos_codeai_autonomous_verification_execution_v0_1 import (
    APPLICATION_RECEIPT_DIGEST_FIELD,
    CANDIDATE_DIGEST_FIELD,
    CANDIDATE_RECEIPT_DIGEST_FIELD,
    EVIDENCE_BUNDLE_DIGEST_FIELD,
    INDEPENDENT_EVIDENCE_DIGEST_FIELD,
    PLAN_DIGEST_FIELD,
    POLICY_DIGEST_FIELD as EXECUTION_POLICY_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as EXECUTION_RECEIPT_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD as EXECUTION_REQUEST_DIGEST_FIELD,
    STATUS_READY as EXECUTION_READY,
    build_codeai_autonomous_verification_execution,
)
from runtime.kuuos_codeai_verification_guided_candidate_repair_regeneration_v0_1 import (
    POLICY_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    STATUS_BLOCKED,
    STATUS_READY,
    build_codeai_verification_guided_candidate_repair_regeneration,
)

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str):
    return json.loads((ROOT / "examples" / name).read_text(encoding="utf-8"))


def _adapter(item):
    responses = [copy.deepcopy(value) for value in item["responses"]]
    return ProviderAdapter(
        item["adapter_id"], item["provider_id"], item["model_id"],
        lambda _prompt, queue=responses: queue.pop(0),
    )


def build_fixture(*, exception_failure: bool = False):
    structured = _load("codeai_autonomous_structured_edit_synthesis_v0_1.json")
    candidate_data = _load("codeai_candidate_patch_envelope_v0_1.json")
    selection_data = _load("codeai_autonomous_candidate_portfolio_selection_v0_1.json")
    application_data = _load("codeai_autonomous_isolated_candidate_application_v0_1.json")
    execution_data = _load("codeai_autonomous_verification_execution_v0_1.json")
    repair_data = _load(
        "codeai_verification_guided_candidate_repair_regeneration_v0_1.json"
    )

    seed_item = structured["provider_adapters"][0]
    seed_adapter = ProviderAdapter(
        seed_item["adapter_id"], seed_item["provider_id"], seed_item["model_id"],
        lambda _prompt, response=seed_item["response"]: copy.deepcopy(response),
    )
    seed = build_codeai_autonomous_structured_edit_synthesis(
        source_observation_receipt=candidate_data["source_observation_receipt"],
        repository_files=structured["repository_files"],
        synthesis_request=structured["synthesis_request"],
        provider_adapters=[seed_adapter],
        synthesis_policy=structured["synthesis_policy"],
        candidate_policy=candidate_data["candidate_policy"],
    )
    assert seed.status == SYNTHESIS_READY, seed.issues
    assert seed.receipt is not None and len(seed.candidates) == 1

    selection_request = dict(selection_data["selection_request"])
    selection_request["source_portfolio_receipt_digest"] = seed.receipt[
        STRUCTURED_RECEIPT_DIGEST_FIELD
    ]
    selection_request = seal(selection_request, SELECTION_REQUEST_DIGEST_FIELD)
    selection_policy = dict(selection_data["selection_policy"])
    selection_policy["expected_source_portfolio_receipt_digest"] = seed.receipt[
        STRUCTURED_RECEIPT_DIGEST_FIELD
    ]
    selection_policy = seal(selection_policy, SELECTION_POLICY_DIGEST_FIELD)
    selection = build_codeai_autonomous_candidate_portfolio_selection(
        source_portfolio_receipt=seed.receipt,
        candidates=seed.candidates,
        selection_request=selection_request,
        selection_policy=selection_policy,
    )
    assert selection.status == SELECTION_READY, selection.issues
    assert selection.receipt is not None and selection.selected_candidate is not None
    selected = selection.selected_candidate
    candidate = selected.patch_candidate
    repository_files = structured["repository_files"]

    application_request = dict(application_data["application_request"])
    application_request.update({
        "source_selection_receipt_digest":
            selection.receipt[SELECTION_RECEIPT_DIGEST_FIELD],
        "selected_candidate_digest": candidate[PATCH_CANDIDATE_DIGEST_FIELD],
        "source_repository_snapshot_digest": canonical_digest(repository_files),
    })
    application_request = seal(application_request, APPLICATION_REQUEST_DIGEST_FIELD)
    application_policy = dict(application_data["application_policy"])
    application_policy.update({
        "expected_source_selection_receipt_digest":
            selection.receipt[SELECTION_RECEIPT_DIGEST_FIELD],
        "expected_selected_candidate_digest": candidate[PATCH_CANDIDATE_DIGEST_FIELD],
        "expected_patch_artifact_digest": candidate["patch_artifact_digest"],
        "expected_repository_full_name": candidate["repository_full_name"],
        "expected_source_commit_sha": candidate["source_commit_sha"],
        "expected_source_repository_snapshot_digest": canonical_digest(repository_files),
    })
    application_policy = seal(application_policy, APPLICATION_POLICY_DIGEST_FIELD)
    application = build_codeai_autonomous_isolated_candidate_application(
        source_selection_receipt=selection.receipt,
        selected_candidate=selected,
        repository_files=repository_files,
        application_request=application_request,
        application_policy=application_policy,
    )
    assert application.status == APPLICATION_READY, application.issues
    assert application.receipt is not None
    assert application.resulting_repository_files is not None

    plan = execution_data["verification_plan"]
    execution_request = dict(execution_data["execution_request"])
    execution_request.update({
        "source_candidate_receipt_digest":
            selected.candidate_receipt[CANDIDATE_RECEIPT_DIGEST_FIELD],
        "source_application_receipt_digest":
            application.receipt[APPLICATION_RECEIPT_DIGEST_FIELD],
        "candidate_digest": selected.candidate_receipt[CANDIDATE_DIGEST_FIELD],
        "patch_artifact_digest": selected.candidate_receipt["patch_artifact_digest"],
        "source_repository_snapshot_digest":
            application.receipt["source_repository_snapshot_digest"],
        "resulting_repository_snapshot_digest":
            canonical_digest(application.resulting_repository_files),
        "repository_full_name": selected.candidate_receipt["repository_full_name"],
        "source_commit_sha": selected.candidate_receipt["source_commit_sha"],
        "verification_plan_digest": plan[PLAN_DIGEST_FIELD],
    })
    execution_request = seal(execution_request, EXECUTION_REQUEST_DIGEST_FIELD)
    execution_policy = dict(execution_data["execution_policy"])
    execution_policy.update({
        "expected_source_candidate_receipt_digest":
            selected.candidate_receipt[CANDIDATE_RECEIPT_DIGEST_FIELD],
        "expected_source_application_receipt_digest":
            application.receipt[APPLICATION_RECEIPT_DIGEST_FIELD],
        "expected_candidate_digest":
            selected.candidate_receipt[CANDIDATE_DIGEST_FIELD],
        "expected_patch_artifact_digest":
            selected.candidate_receipt["patch_artifact_digest"],
        "expected_source_repository_snapshot_digest":
            application.receipt["source_repository_snapshot_digest"],
        "expected_resulting_repository_snapshot_digest":
            canonical_digest(application.resulting_repository_files),
        "expected_repository_full_name":
            selected.candidate_receipt["repository_full_name"],
        "expected_source_commit_sha":
            selected.candidate_receipt["source_commit_sha"],
        "expected_verification_plan_digest": plan[PLAN_DIGEST_FIELD],
    })
    execution_policy = seal(execution_policy, EXECUTION_POLICY_DIGEST_FIELD)

    def runner(invocation):
        if invocation.check_id == "python-syntax":
            if exception_failure:
                raise RuntimeError("bounded repair fixture runner exception")
            return {
                "runner_id": "repair-fixture-runner",
                "runner_session_id": "repair-fixture-python-syntax",
                "check_id": invocation.check_id,
                "exit_code": 1,
                "stdout": "",
                "stderr": "SyntaxError: bounded fixture failure\n",
                "duration_ms": 5,
                "timed_out": False,
                "exception_type": None,
                "started_epoch": 1784429995,
                "completed_epoch": 1784429996,
                "network_used": False,
                "secret_accessed": False,
                "live_repository_accessed": False,
                "git_effect_performed": False,
            }
        return {
            "runner_id": "repair-fixture-runner",
            "runner_session_id": "repair-fixture-unit-tests",
            "check_id": invocation.check_id,
            "exit_code": 0,
            "stdout": "PASS\n",
            "stderr": "",
            "duration_ms": 5,
            "timed_out": False,
            "exception_type": None,
            "started_epoch": 1784429995,
            "completed_epoch": 1784429996,
            "network_used": False,
            "secret_accessed": False,
            "live_repository_accessed": False,
            "git_effect_performed": False,
        }

    execution = build_codeai_autonomous_verification_execution(
        source_candidate_receipt=selected.candidate_receipt,
        source_application_receipt=application.receipt,
        resulting_repository_files=application.resulting_repository_files,
        verification_plan=plan,
        execution_request=execution_request,
        execution_policy=execution_policy,
        runner_adapter=runner,
    )
    assert execution.status == EXECUTION_READY, execution.issues
    assert execution.receipt is not None
    assert execution.evidence_bundle is not None
    assert execution.independent_verification_evidence is not None
    assert execution.receipt["failed_check_count"] == 1

    generation_digest = seed.receipt[STRUCTURED_RECEIPT_DIGEST_FIELD]
    observation_digest = candidate_data["source_observation_receipt"][
        "codeai_intent_repository_observation_receipt_digest"
    ]
    repair_request = dict(repair_data["repair_request"])
    repair_request.update({
        "source_verification_execution_receipt_digest":
            execution.receipt[EXECUTION_RECEIPT_DIGEST_FIELD],
        "source_evidence_bundle_digest":
            execution.evidence_bundle[EVIDENCE_BUNDLE_DIGEST_FIELD],
        "source_independent_verification_evidence_digest":
            execution.independent_verification_evidence[INDEPENDENT_EVIDENCE_DIGEST_FIELD],
        "source_candidate_receipt_digest":
            selected.candidate_receipt[CANDIDATE_RECEIPT_DIGEST_FIELD],
        "source_application_receipt_digest":
            application.receipt[APPLICATION_RECEIPT_DIGEST_FIELD],
        "source_generation_receipt_digest": generation_digest,
        "source_observation_receipt_digest": observation_digest,
        "candidate_digest": selected.candidate_receipt[CANDIDATE_DIGEST_FIELD],
        "patch_artifact_digest": selected.candidate_receipt["patch_artifact_digest"],
        "repository_full_name": selected.candidate_receipt["repository_full_name"],
        "source_commit_sha": selected.candidate_receipt["source_commit_sha"],
    })
    repair_request = seal(repair_request, REQUEST_DIGEST_FIELD)
    repair_policy = dict(repair_data["repair_policy"])
    repair_policy.update({
        "expected_source_verification_execution_receipt_digest":
            execution.receipt[EXECUTION_RECEIPT_DIGEST_FIELD],
        "expected_source_evidence_bundle_digest":
            execution.evidence_bundle[EVIDENCE_BUNDLE_DIGEST_FIELD],
        "expected_source_independent_verification_evidence_digest":
            execution.independent_verification_evidence[INDEPENDENT_EVIDENCE_DIGEST_FIELD],
        "expected_source_candidate_receipt_digest":
            selected.candidate_receipt[CANDIDATE_RECEIPT_DIGEST_FIELD],
        "expected_source_application_receipt_digest":
            application.receipt[APPLICATION_RECEIPT_DIGEST_FIELD],
        "expected_source_generation_receipt_digest": generation_digest,
        "expected_source_observation_receipt_digest": observation_digest,
        "expected_candidate_digest":
            selected.candidate_receipt[CANDIDATE_DIGEST_FIELD],
        "expected_patch_artifact_digest":
            selected.candidate_receipt["patch_artifact_digest"],
        "expected_repository_full_name":
            selected.candidate_receipt["repository_full_name"],
        "expected_source_commit_sha":
            selected.candidate_receipt["source_commit_sha"],
    })
    repair_policy = seal(repair_policy, POLICY_DIGEST_FIELD)
    adapters = [_adapter(item) for item in repair_data["provider_adapters"]]
    inputs = {
        "source_verification_execution_receipt": execution.receipt,
        "source_evidence_bundle": execution.evidence_bundle,
        "source_independent_verification_evidence":
            execution.independent_verification_evidence,
        "source_generation_receipt": seed.receipt,
        "source_observation_receipt": candidate_data["source_observation_receipt"],
        "source_candidate_receipt": selected.candidate_receipt,
        "source_application_receipt": application.receipt,
        "repository_files": repository_files,
        "seed_candidates": seed.candidates,
        "repair_request": repair_request,
        "provider_adapters": adapters,
        "repair_policy": repair_policy,
        "candidate_policy": candidate_data["candidate_policy"],
    }
    return inputs


def execute_fixture(inputs):
    return build_codeai_verification_guided_candidate_repair_regeneration(**inputs)


class VerificationGuidedRepairRegenerationTests(unittest.TestCase):
    def test_failed_evidence_generates_one_unselected_candidate(self):
        inputs = build_fixture()
        before = copy.deepcopy(inputs["repository_files"])
        result = execute_fixture(inputs)
        self.assertEqual(result.status, STATUS_READY, result.issues)
        self.assertEqual(len(result.downstream_regeneration.regenerated_candidates), 1)
        self.assertEqual(len(result.downstream_regeneration.combined_candidates), 2)
        self.assertEqual(result.normalized_feedback["feedback_record_count"], 1)
        self.assertFalse(result.receipt["candidate_selected"])
        self.assertFalse(result.receipt["repository_mutation_performed"])
        self.assertFalse(result.receipt["successor_stage_authority_granted"])
        self.assertEqual(inputs["repository_files"], before)

    def test_runner_exception_is_failure_context_not_success(self):
        result = execute_fixture(build_fixture(exception_failure=True))
        self.assertEqual(result.status, STATUS_READY, result.issues)
        record = result.normalized_feedback["feedback_records"][0]
        self.assertEqual(record["execution_status"], "runner_exception")
        self.assertIn("exception_type:RuntimeError", record["failure_reason_ids"])

    def test_tampered_request_digest_blocks(self):
        inputs = build_fixture()
        inputs["repair_request"] = dict(inputs["repair_request"])
        inputs["repair_request"]["repair_intent_text"] += " tampered"
        result = execute_fixture(inputs)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("repair_request_digest_mismatch", result.issues)

    def test_network_permission_escalation_blocks(self):
        inputs = build_fixture()
        policy = dict(inputs["repair_policy"])
        policy["network_access_allowed"] = True
        inputs["repair_policy"] = seal(policy, POLICY_DIGEST_FIELD)
        result = execute_fixture(inputs)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("repair_policy_required_false:network_access_allowed", result.issues)

    def test_candidate_lineage_mismatch_blocks(self):
        inputs = build_fixture()
        request = dict(inputs["repair_request"])
        request["candidate_digest"] = "f" * 64
        inputs["repair_request"] = seal(request, REQUEST_DIGEST_FIELD)
        result = execute_fixture(inputs)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("repair_correspondence_mismatch:request_candidate", result.issues)

    def test_evidence_digest_tamper_blocks(self):
        inputs = build_fixture()
        evidence = dict(inputs["source_evidence_bundle"])
        evidence["failed_check_count"] = 2
        inputs["source_evidence_bundle"] = evidence
        result = execute_fixture(inputs)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("source_evidence_digest_mismatch", result.issues)

    def test_failed_check_allowlist_is_enforced(self):
        inputs = build_fixture()
        policy = dict(inputs["repair_policy"])
        policy["allowed_check_ids"] = ["unit-tests"]
        inputs["repair_policy"] = seal(policy, POLICY_DIGEST_FIELD)
        result = execute_fixture(inputs)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("repair_feedback_check_not_allowed:python-syntax", result.issues)

    def test_failure_status_allowlist_is_enforced(self):
        inputs = build_fixture()
        policy = dict(inputs["repair_policy"])
        policy["allowed_execution_statuses"] = ["timed_out"]
        inputs["repair_policy"] = seal(policy, POLICY_DIGEST_FIELD)
        result = execute_fixture(inputs)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("repair_feedback_status_not_allowed:failed", result.issues)

    def test_feedback_byte_budget_is_fail_closed(self):
        inputs = build_fixture()
        policy = dict(inputs["repair_policy"])
        policy["maximum_total_feedback_bytes"] = 1
        inputs["repair_policy"] = seal(policy, POLICY_DIGEST_FIELD)
        result = execute_fixture(inputs)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("repair_feedback_total_byte_budget_exceeded", result.issues)

    def test_stale_repair_request_blocks(self):
        inputs = build_fixture()
        request = dict(inputs["repair_request"])
        request["request_created_epoch"] = 1
        inputs["repair_request"] = seal(request, REQUEST_DIGEST_FIELD)
        result = execute_fixture(inputs)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("repair_request_window_invalid", result.issues)

    def test_no_candidate_capacity_blocks(self):
        inputs = build_fixture()
        policy = dict(inputs["repair_policy"])
        policy["maximum_total_candidates"] = 1
        inputs["repair_policy"] = seal(policy, POLICY_DIGEST_FIELD)
        result = execute_fixture(inputs)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("repair_no_candidate_capacity", result.issues)

    def test_generation_receipt_digest_tamper_blocks(self):
        inputs = build_fixture()
        generation = dict(inputs["source_generation_receipt"])
        generation["generated_candidate_count"] = 99
        inputs["source_generation_receipt"] = generation
        result = execute_fixture(inputs)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("source_generation_receipt_digest_mismatch", result.issues)


if __name__ == "__main__":
    unittest.main()
