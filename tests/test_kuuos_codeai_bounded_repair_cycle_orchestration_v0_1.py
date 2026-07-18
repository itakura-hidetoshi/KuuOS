#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from runtime.kuuos_codeai_candidate_patch_envelope_v0_1 import (
    CANDIDATE_DIGEST_FIELD,
    seal,
)
from runtime.kuuos_codeai_autonomous_unified_diff_candidates_v0_1 import (
    GeneratedUnifiedDiffCandidate,
)
from runtime.kuuos_codeai_autonomous_verification_execution_v0_1 import (
    PLAN_DIGEST_FIELD,
)
from runtime.kuuos_codeai_autonomous_candidate_regeneration_common_v0_1 import (
    RECEIPT_DIGEST_FIELD as REGENERATION_RECEIPT_DIGEST_FIELD,
)
from runtime.kuuos_codeai_verification_guided_candidate_repair_regeneration_v0_1 import (
    RECEIPT_DIGEST_FIELD as REPAIR_RECEIPT_DIGEST_FIELD,
)
from runtime.kuuos_codeai_bounded_repair_cycle_orchestration_v0_1 import (
    DISPOSITION_FAILED,
    DISPOSITION_PASSED,
    POLICY_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    STATUS_BLOCKED,
    STATUS_READY,
    build_codeai_bounded_repair_cycle_orchestration,
    repair_candidate_set_digest,
)
from tests.test_kuuos_codeai_verification_guided_candidate_repair_regeneration_v0_1 import (
    build_fixture,
    execute_fixture,
)

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "codeai_bounded_repair_cycle_orchestration_v0_1.json"


def _load_example():
    return json.loads(EXAMPLE.read_text(encoding="utf-8"))


def _rerank(items):
    return tuple(
        GeneratedUnifiedDiffCandidate(
            rank=index,
            proposal_id=item.proposal_id,
            patch_candidate=copy.deepcopy(item.patch_candidate),
            patch_artifact=item.patch_artifact,
            candidate_receipt=copy.deepcopy(item.candidate_receipt),
        )
        for index, item in enumerate(items, start=1)
    )


def _runner(*, passing: bool = True, exception: bool = False):
    def run(invocation):
        if exception and invocation.check_id == "python-syntax":
            raise RuntimeError("bounded cycle runner exception")
        return {
            "runner_id": "bounded-cycle-test-runner",
            "runner_session_id": "bounded-cycle-" + invocation.check_id,
            "check_id": invocation.check_id,
            "exit_code": 0 if passing else 1,
            "stdout": "PASS\n" if passing else "",
            "stderr": "" if passing else "bounded cycle verification failure\n",
            "duration_ms": 5,
            "timed_out": False,
            "exception_type": None,
            "started_epoch": 1784318996,
            "completed_epoch": 1784318997,
            "network_used": False,
            "secret_accessed": False,
            "live_repository_accessed": False,
            "git_effect_performed": False,
        }
    return run


def build_cycle_inputs(
    *,
    passing: bool = True,
    exception: bool = False,
    cycle_index: int = 1,
    maximum_cycle_count: int = 2,
):
    fixture_inputs = build_fixture()
    repair = execute_fixture(fixture_inputs)
    assert repair.status == STATUS_READY, repair.issues
    assert repair.receipt is not None
    assert repair.downstream_regeneration is not None
    assert repair.downstream_regeneration.receipt is not None
    candidates = tuple(copy.deepcopy(repair.downstream_regeneration.combined_candidates))
    repository = copy.deepcopy(fixture_inputs["repository_files"])
    example = _load_example()
    plan = copy.deepcopy(example["verification_plan"])
    candidate_set_digest = repair_candidate_set_digest(candidates)

    request = copy.deepcopy(example["cycle_request"])
    request.update(
        {
            "cycle_index": cycle_index,
            "source_repair_receipt_digest":
                repair.receipt[REPAIR_RECEIPT_DIGEST_FIELD],
            "source_regeneration_receipt_digest":
                repair.downstream_regeneration.receipt[REGENERATION_RECEIPT_DIGEST_FIELD],
            "repair_candidate_set_digest": candidate_set_digest,
            "verification_plan_digest": plan[PLAN_DIGEST_FIELD],
        }
    )
    request = seal(request, REQUEST_DIGEST_FIELD)

    first = candidates[0].patch_candidate
    policy = copy.deepcopy(example["cycle_policy"])
    policy.update(
        {
            "expected_source_repair_receipt_digest":
                repair.receipt[REPAIR_RECEIPT_DIGEST_FIELD],
            "expected_source_regeneration_receipt_digest":
                repair.downstream_regeneration.receipt[REGENERATION_RECEIPT_DIGEST_FIELD],
            "expected_repair_candidate_set_digest": candidate_set_digest,
            "expected_repository_full_name": first["repository_full_name"],
            "expected_source_commit_sha": first["source_commit_sha"],
            "expected_verification_plan_digest": plan[PLAN_DIGEST_FIELD],
            "maximum_cycle_count": maximum_cycle_count,
        }
    )
    policy = seal(policy, POLICY_DIGEST_FIELD)

    return {
        "source_repair_receipt": copy.deepcopy(repair.receipt),
        "source_regeneration_receipt":
            copy.deepcopy(repair.downstream_regeneration.receipt),
        "repair_candidates": candidates,
        "repository_files": repository,
        "cycle_request": request,
        "cycle_policy": policy,
        "verification_plan": plan,
        "runner_adapter": _runner(passing=passing, exception=exception),
    }


class BoundedRepairCycleOrchestrationTests(unittest.TestCase):
    def test_passing_repair_cycle_is_ready_and_stops(self):
        result = build_codeai_bounded_repair_cycle_orchestration(
            **build_cycle_inputs()
        )
        self.assertEqual(result.status, STATUS_READY, result.issues)
        self.assertEqual(result.receipt["codeai_disposition"], DISPOSITION_PASSED)
        self.assertTrue(result.receipt["cycle_verification_passed"])
        self.assertFalse(result.receipt["next_cycle_eligible"])

    def test_failed_cycle_is_ready_but_only_eligible_for_next_cycle(self):
        result = build_codeai_bounded_repair_cycle_orchestration(
            **build_cycle_inputs(passing=False)
        )
        self.assertEqual(result.status, STATUS_READY, result.issues)
        self.assertEqual(result.receipt["codeai_disposition"], DISPOSITION_FAILED)
        self.assertTrue(result.receipt["next_cycle_eligible"])
        self.assertFalse(result.receipt["next_cycle_authority_granted"])

    def test_cycle_limit_prevents_next_cycle_eligibility(self):
        result = build_codeai_bounded_repair_cycle_orchestration(
            **build_cycle_inputs(
                passing=False, cycle_index=1, maximum_cycle_count=1
            )
        )
        self.assertEqual(result.status, STATUS_READY, result.issues)
        self.assertTrue(result.receipt["cycle_limit_reached"])
        self.assertFalse(result.receipt["next_cycle_eligible"])

    def test_failed_source_candidate_is_excluded_before_reselection(self):
        inputs = build_cycle_inputs()
        failed_digest = inputs["source_repair_receipt"]["candidate_digest"]
        result = build_codeai_bounded_repair_cycle_orchestration(**inputs)
        self.assertEqual(result.status, STATUS_READY, result.issues)
        self.assertNotEqual(
            result.selected_candidate.patch_candidate[CANDIDATE_DIGEST_FIELD],
            failed_digest,
        )
        self.assertTrue(result.receipt["failed_candidate_excluded_from_reselection"])

    def test_tampered_repair_receipt_blocks(self):
        inputs = build_cycle_inputs()
        inputs["source_repair_receipt"]["candidate_digest"] = "tampered"
        result = build_codeai_bounded_repair_cycle_orchestration(**inputs)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("source_repair_receipt_digest_mismatch", result.issues)

    def test_repair_to_regeneration_digest_mismatch_blocks(self):
        inputs = build_cycle_inputs()
        repair = dict(inputs["source_repair_receipt"])
        repair["downstream_regeneration_receipt_digest"] = "f" * 64
        inputs["source_repair_receipt"] = seal(repair, REPAIR_RECEIPT_DIGEST_FIELD)
        result = build_codeai_bounded_repair_cycle_orchestration(**inputs)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn(
            "repair_cycle_correspondence_mismatch:repair_regeneration",
            result.issues,
        )

    def test_candidate_set_correspondence_mismatch_blocks(self):
        inputs = build_cycle_inputs()
        policy = dict(inputs["cycle_policy"])
        policy["expected_repair_candidate_set_digest"] = "e" * 64
        inputs["cycle_policy"] = seal(policy, POLICY_DIGEST_FIELD)
        result = build_codeai_bounded_repair_cycle_orchestration(**inputs)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn(
            "repair_cycle_correspondence_mismatch:policy_candidate_set",
            result.issues,
        )

    def test_stale_cycle_request_blocks(self):
        inputs = build_cycle_inputs()
        request = dict(inputs["cycle_request"])
        request["request_created_epoch"] = 1
        inputs["cycle_request"] = seal(request, REQUEST_DIGEST_FIELD)
        result = build_codeai_bounded_repair_cycle_orchestration(**inputs)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("repair_cycle_request_window_invalid", result.issues)

    def test_cycle_index_above_policy_blocks(self):
        inputs = build_cycle_inputs(cycle_index=3, maximum_cycle_count=2)
        result = build_codeai_bounded_repair_cycle_orchestration(**inputs)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("repair_cycle_index_exceeds_policy", result.issues)

    def test_network_capability_policy_blocks(self):
        inputs = build_cycle_inputs()
        policy = dict(inputs["cycle_policy"])
        policy["network_access_allowed"] = True
        inputs["cycle_policy"] = seal(policy, POLICY_DIGEST_FIELD)
        result = build_codeai_bounded_repair_cycle_orchestration(**inputs)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn(
            "cycle_policy_required_false:network_access_allowed",
            result.issues,
        )

    def test_tampered_verification_plan_blocks(self):
        inputs = build_cycle_inputs()
        inputs["verification_plan"]["checks"][0]["timeout_seconds"] += 1
        result = build_codeai_bounded_repair_cycle_orchestration(**inputs)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("verification_plan_digest_mismatch", result.issues)

    def test_runner_exception_is_failed_evidence_not_success(self):
        result = build_codeai_bounded_repair_cycle_orchestration(
            **build_cycle_inputs(exception=True)
        )
        self.assertEqual(result.status, STATUS_READY, result.issues)
        self.assertEqual(result.receipt["codeai_disposition"], DISPOSITION_FAILED)
        self.assertGreater(result.receipt["failed_check_count"], 0)
        self.assertFalse(result.receipt["cycle_pass_treated_as_proof"])

    def test_no_eligible_candidate_after_exclusion_blocks(self):
        inputs = build_cycle_inputs()
        failed_digest = inputs["source_repair_receipt"]["candidate_digest"]
        failed = [
            item for item in inputs["repair_candidates"]
            if item.patch_candidate[CANDIDATE_DIGEST_FIELD] == failed_digest
        ]
        inputs["repair_candidates"] = _rerank(failed)
        digest = repair_candidate_set_digest(inputs["repair_candidates"])
        request = dict(inputs["cycle_request"])
        request["repair_candidate_set_digest"] = digest
        inputs["cycle_request"] = seal(request, REQUEST_DIGEST_FIELD)
        policy = dict(inputs["cycle_policy"])
        policy["expected_repair_candidate_set_digest"] = digest
        inputs["cycle_policy"] = seal(policy, POLICY_DIGEST_FIELD)
        regeneration = dict(inputs["source_regeneration_receipt"])
        regeneration["combined_candidate_count"] = 1
        regeneration["combined_candidate_ids"] = [
            inputs["repair_candidates"][0].patch_candidate["candidate_id"]
        ]
        regeneration["combined_candidate_digests"] = [failed_digest]
        inputs["source_regeneration_receipt"] = seal(
            regeneration, REGENERATION_RECEIPT_DIGEST_FIELD
        )
        repair = dict(inputs["source_repair_receipt"])
        repair["downstream_regeneration_receipt_digest"] = inputs[
            "source_regeneration_receipt"
        ][REGENERATION_RECEIPT_DIGEST_FIELD]
        repair["combined_candidate_count"] = 1
        inputs["source_repair_receipt"] = seal(repair, REPAIR_RECEIPT_DIGEST_FIELD)
        request = dict(inputs["cycle_request"])
        request["source_repair_receipt_digest"] = inputs["source_repair_receipt"][
            REPAIR_RECEIPT_DIGEST_FIELD
        ]
        request["source_regeneration_receipt_digest"] = inputs[
            "source_regeneration_receipt"
        ][REGENERATION_RECEIPT_DIGEST_FIELD]
        inputs["cycle_request"] = seal(request, REQUEST_DIGEST_FIELD)
        policy = dict(inputs["cycle_policy"])
        policy["expected_source_repair_receipt_digest"] = inputs[
            "source_repair_receipt"
        ][REPAIR_RECEIPT_DIGEST_FIELD]
        policy["expected_source_regeneration_receipt_digest"] = inputs[
            "source_regeneration_receipt"
        ][REGENERATION_RECEIPT_DIGEST_FIELD]
        inputs["cycle_policy"] = seal(policy, POLICY_DIGEST_FIELD)
        result = build_codeai_bounded_repair_cycle_orchestration(**inputs)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn(
            "repair_cycle_has_no_candidate_after_failed_candidate_exclusion",
            result.issues,
        )

    def test_repository_snapshot_remains_immutable_and_no_authority_is_granted(self):
        inputs = build_cycle_inputs()
        before = copy.deepcopy(inputs["repository_files"])
        result = build_codeai_bounded_repair_cycle_orchestration(**inputs)
        self.assertEqual(result.status, STATUS_READY, result.issues)
        self.assertEqual(inputs["repository_files"], before)
        for field in (
            "repository_mutation_performed",
            "git_ref_changed",
            "merge_performed",
            "deployment_performed",
            "secret_access_performed",
            "network_access_performed",
            "successor_stage_authority_granted",
        ):
            self.assertFalse(result.receipt[field], field)


if __name__ == "__main__":
    unittest.main()
