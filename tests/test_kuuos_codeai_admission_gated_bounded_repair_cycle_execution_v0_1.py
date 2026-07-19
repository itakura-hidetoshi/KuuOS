#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from runtime.kuuos_codeai_candidate_patch_envelope_v0_1 import seal
from runtime.kuuos_codeai_repair_cycle_continuation_admission_v0_1 import (
    RECEIPT_DIGEST_FIELD as ADMISSION_RECEIPT_DIGEST_FIELD,
)
from runtime.kuuos_codeai_repair_cycle_admission_consumption_v0_1 import (
    EXECUTION_INPUT_DIGEST_FIELD,
    POLICY_DIGEST_FIELD as CONSUMPTION_POLICY_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as CONSUMPTION_RECEIPT_DIGEST_FIELD,
    REGISTRY_DIGEST_FIELD as CONSUMPTION_REGISTRY_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD as CONSUMPTION_REQUEST_DIGEST_FIELD,
    STATUS_READY as CONSUMPTION_STATUS_READY,
    build_codeai_repair_cycle_admission_consumption,
)
from runtime.kuuos_codeai_bounded_repair_cycle_orchestration_v0_1 import (
    POLICY_DIGEST_FIELD as INNER_POLICY_DIGEST_FIELD,
)
from runtime.kuuos_codeai_autonomous_verification_execution_v0_1 import (
    PLAN_DIGEST_FIELD,
)
from runtime.kuuos_codeai_admission_gated_bounded_repair_cycle_execution_v0_1 import (
    DISPOSITION_ABORTED,
    DISPOSITION_FAILED,
    DISPOSITION_PASSED,
    POLICY_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD,
    REGISTRY_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    STATUS_BLOCKED,
    STATUS_READY,
    build_codeai_admission_gated_bounded_repair_cycle_execution,
)
from tests.test_kuuos_codeai_bounded_repair_cycle_orchestration_v0_1 import (
    build_cycle_inputs,
)

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "codeai_admission_gated_bounded_repair_cycle_execution_v0_1.json"
CONSUMPTION_EXAMPLE = ROOT / "examples" / "codeai_repair_cycle_admission_consumption_v0_1.json"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _reseal(value: dict, field: str) -> dict:
    return seal({key: item for key, item in value.items() if key != field}, field)


def _runner(*, passing: bool = True, huge_output: bool = False):
    def run(invocation):
        output = "x" * 40000 if huge_output else ("PASS\n" if passing else "")
        error = "" if passing else "admitted cycle verification failure\n"
        return {
            "runner_id": "admission-gated-cycle-test-runner",
            "runner_session_id": "admission-gated-" + invocation.check_id,
            "check_id": invocation.check_id,
            "exit_code": 0 if passing else 1,
            "stdout": output,
            "stderr": error,
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


def build_execution_inputs(*, passing: bool = True, huge_output: bool = False) -> dict:
    example = _load(EXAMPLE)
    cycle = build_cycle_inputs(passing=passing, cycle_index=2, maximum_cycle_count=3)
    plan = copy.deepcopy(cycle["verification_plan"])
    candidates = tuple(copy.deepcopy(cycle["repair_candidates"]))

    consumption_payload = _load(CONSUMPTION_EXAMPLE)
    admission = copy.deepcopy(consumption_payload["admission_receipt"])
    budget = example["admission_budget"]
    admission.update(
        {
            "current_cycle_index": 1,
            "admitted_cycle_index": 2,
            "maximum_cycle_count": 3,
            "reserved_candidate": budget["candidate"],
            "remaining_candidate_before_reservation": budget["candidate"] + 8,
            "remaining_candidate_after_reservation": 8,
            "reserved_provider_call": budget["provider_call"],
            "remaining_provider_call_before_reservation": budget["provider_call"] + 4,
            "remaining_provider_call_after_reservation": 4,
            "reserved_command": budget["command"],
            "remaining_command_before_reservation": budget["command"] + 16,
            "remaining_command_after_reservation": 16,
            "reserved_timeout_seconds": budget["timeout_seconds"],
            "remaining_timeout_seconds_before_reservation": budget["timeout_seconds"] + 600,
            "remaining_timeout_seconds_after_reservation": 600,
            "reserved_output_bytes": budget["output_bytes"],
            "remaining_output_bytes_before_reservation": budget["output_bytes"] + 65536,
            "remaining_output_bytes_after_reservation": 65536,
        }
    )
    admission = _reseal(admission, ADMISSION_RECEIPT_DIGEST_FIELD)

    consumption_request = copy.deepcopy(consumption_payload["consumption_request"])
    consumption_request.update(
        {
            "admission_receipt_digest": admission[ADMISSION_RECEIPT_DIGEST_FIELD],
            "admitted_cycle_index": 2,
            "source_cycle_receipt_digest": admission["source_cycle_receipt_digest"],
            "source_selected_candidate_digest": admission["source_selected_candidate_digest"],
            "source_repair_receipt_digest": cycle["cycle_request"]["source_repair_receipt_digest"],
            "source_regeneration_receipt_digest": cycle["cycle_request"]["source_regeneration_receipt_digest"],
            "repair_candidate_set_digest": cycle["cycle_request"]["repair_candidate_set_digest"],
            "verification_plan_digest": plan[PLAN_DIGEST_FIELD],
            "execution_session_id": example["execution_request"]["execution_session_id"],
            "execution_nonce_digest": "1" * 64,
            "requested_by_actor_id": example["execution_request"]["executor_actor_id"],
            "request_created_epoch": 1784318990,
        }
    )
    consumption_request = _reseal(consumption_request, CONSUMPTION_REQUEST_DIGEST_FIELD)
    consumption_policy = copy.deepcopy(consumption_payload["consumption_policy"])
    consumption_policy.update(
        {
            "expected_admission_receipt_digest": admission[ADMISSION_RECEIPT_DIGEST_FIELD],
            "expected_admitted_cycle_index": 2,
            "expected_source_cycle_receipt_digest": admission["source_cycle_receipt_digest"],
            "expected_source_selected_candidate_digest": admission["source_selected_candidate_digest"],
            "expected_source_repair_receipt_digest": cycle["cycle_request"]["source_repair_receipt_digest"],
            "expected_source_regeneration_receipt_digest": cycle["cycle_request"]["source_regeneration_receipt_digest"],
            "expected_repair_candidate_set_digest": cycle["cycle_request"]["repair_candidate_set_digest"],
            "expected_verification_plan_digest": plan[PLAN_DIGEST_FIELD],
            "expected_consumer_actor_id": example["execution_request"]["executor_actor_id"],
            "evaluation_epoch": 1784319000,
            "maximum_request_age": 3600,
        }
    )
    consumption_policy = _reseal(consumption_policy, CONSUMPTION_POLICY_DIGEST_FIELD)
    consumption_registry = copy.deepcopy(consumption_payload["consumption_registry"])
    consumption_registry.update({"registry_created_epoch": 1784318990})
    consumption_registry = _reseal(consumption_registry, CONSUMPTION_REGISTRY_DIGEST_FIELD)
    consumption = build_codeai_repair_cycle_admission_consumption(
        admission_receipt=admission,
        consumption_request=consumption_request,
        consumption_policy=consumption_policy,
        consumption_registry=consumption_registry,
    )
    assert consumption.status == CONSUMPTION_STATUS_READY, consumption.issues
    assert consumption.execution_input is not None
    assert consumption.next_registry is not None
    assert consumption.receipt is not None

    request = copy.deepcopy(example["execution_request"])
    request.update(
        {
            "execution_input_digest": consumption.execution_input[EXECUTION_INPUT_DIGEST_FIELD],
            "admission_consumption_receipt_digest": consumption.receipt[CONSUMPTION_RECEIPT_DIGEST_FIELD],
            "consumption_registry_digest": consumption.next_registry[CONSUMPTION_REGISTRY_DIGEST_FIELD],
            "cycle_index": consumption.execution_input["cycle_index"],
            "execution_session_id": consumption.execution_input["execution_session_id"],
            "executor_actor_id": consumption.execution_input["consumer_actor_id"],
        }
    )
    request = _reseal(request, REQUEST_DIGEST_FIELD)

    first = candidates[0].patch_candidate
    policy = copy.deepcopy(example["execution_policy"])
    policy.update(
        {
            "expected_execution_input_digest": consumption.execution_input[EXECUTION_INPUT_DIGEST_FIELD],
            "expected_admission_consumption_receipt_digest": consumption.receipt[CONSUMPTION_RECEIPT_DIGEST_FIELD],
            "expected_consumption_registry_digest": consumption.next_registry[CONSUMPTION_REGISTRY_DIGEST_FIELD],
            "expected_cycle_index": consumption.execution_input["cycle_index"],
            "expected_repository_full_name": first["repository_full_name"],
            "expected_source_commit_sha": first["source_commit_sha"],
            "expected_executor_actor_id": consumption.execution_input["consumer_actor_id"],
        }
    )
    policy = _reseal(policy, POLICY_DIGEST_FIELD)

    registry = copy.deepcopy(example["execution_registry"])
    registry = _reseal(registry, REGISTRY_DIGEST_FIELD)

    inner_policy = copy.deepcopy(cycle["cycle_policy"])
    inner_policy.update(example["bounded_cycle_policy_overrides"])
    inner_policy = _reseal(inner_policy, INNER_POLICY_DIGEST_FIELD)

    provider_template = copy.deepcopy(example["provider_result"])
    provider_template["generated_candidate_count"] = len(candidates)

    def provider(_invocation):
        return {
            **copy.deepcopy(provider_template),
            "source_repair_receipt": copy.deepcopy(cycle["source_repair_receipt"]),
            "source_regeneration_receipt": copy.deepcopy(cycle["source_regeneration_receipt"]),
            "repair_candidates": tuple(copy.deepcopy(candidates)),
        }

    return {
        "admission_consumption_receipt": copy.deepcopy(consumption.receipt),
        "execution_input": copy.deepcopy(consumption.execution_input),
        "consumption_registry_receipt": copy.deepcopy(consumption.next_registry),
        "execution_request": request,
        "execution_policy": policy,
        "execution_registry": registry,
        "isolated_repository_files": copy.deepcopy(cycle["repository_files"]),
        "verification_plan": plan,
        "bounded_cycle_policy": inner_policy,
        "provider_adapter": provider,
        "runner_adapter": _runner(passing=passing, huge_output=huge_output),
    }


class AdmissionGatedBoundedRepairCycleExecutionTests(unittest.TestCase):
    def _run(self, inputs: dict | None = None):
        return build_codeai_admission_gated_bounded_repair_cycle_execution(
            **(build_execution_inputs() if inputs is None else inputs)
        )

    def test_passing_cycle_consumes_input_and_advances_registry(self):
        result = self._run()
        self.assertEqual(result.status, STATUS_READY, result.issues)
        self.assertEqual(result.receipt["codeai_disposition"], DISPOSITION_PASSED)
        self.assertTrue(result.receipt["execution_input_consumed"])
        self.assertEqual(result.next_registry["registry_revision"], 2)
        self.assertEqual(result.next_registry["last_executed_cycle_index"], 2)

    def test_failed_verification_is_completed_failure_not_blocked(self):
        result = self._run(build_execution_inputs(passing=False))
        self.assertEqual(result.status, STATUS_READY, result.issues)
        self.assertEqual(result.receipt["codeai_disposition"], DISPOSITION_FAILED)
        self.assertTrue(result.receipt["next_cycle_eligible"])
        self.assertFalse(result.receipt["next_cycle_authority_granted"])

    def test_runtime_output_budget_abort_is_recorded(self):
        result = self._run(build_execution_inputs(huge_output=True))
        self.assertEqual(result.status, STATUS_READY, result.issues)
        self.assertEqual(result.receipt["codeai_disposition"], DISPOSITION_ABORTED)
        self.assertTrue(result.receipt["cycle_aborted_by_budget"])

    def test_output_surfaces_are_sealed(self):
        result = self._run()
        self.assertEqual(_reseal(result.receipt, RECEIPT_DIGEST_FIELD), result.receipt)
        self.assertEqual(_reseal(result.next_registry, REGISTRY_DIGEST_FIELD), result.next_registry)

    def test_execution_input_replay_blocks(self):
        inputs = build_execution_inputs()
        digest = inputs["execution_input"][EXECUTION_INPUT_DIGEST_FIELD]
        registry = dict(inputs["execution_registry"])
        registry["consumed_execution_input_digests"] = [digest]
        registry["consumed_cycle_execution_nonce_digests"] = ["9" * 64]
        inputs["execution_registry"] = _reseal(registry, REGISTRY_DIGEST_FIELD)
        result = self._run(inputs)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("admission_gated_execution_input_replay_detected", result.issues)

    def test_execution_nonce_replay_blocks(self):
        inputs = build_execution_inputs()
        registry = dict(inputs["execution_registry"])
        registry["consumed_execution_input_digests"] = ["8" * 64]
        registry["consumed_cycle_execution_nonce_digests"] = [inputs["execution_request"]["cycle_execution_nonce_digest"]]
        inputs["execution_registry"] = _reseal(registry, REGISTRY_DIGEST_FIELD)
        result = self._run(inputs)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("admission_gated_execution_nonce_replay_detected", result.issues)

    def test_execution_registry_capacity_blocks(self):
        inputs = build_execution_inputs()
        policy = dict(inputs["execution_policy"])
        policy["maximum_executed_input_count"] = 1
        inputs["execution_policy"] = _reseal(policy, POLICY_DIGEST_FIELD)
        registry = dict(inputs["execution_registry"])
        registry["consumed_execution_input_digests"] = ["8" * 64]
        registry["consumed_cycle_execution_nonce_digests"] = ["9" * 64]
        inputs["execution_registry"] = _reseal(registry, REGISTRY_DIGEST_FIELD)
        result = self._run(inputs)
        self.assertIn("admission_gated_execution_registry_capacity_exhausted", result.issues)

    def test_nonmonotone_cycle_blocks(self):
        inputs = build_execution_inputs()
        registry = dict(inputs["execution_registry"])
        registry["last_executed_cycle_index"] = 2
        inputs["execution_registry"] = _reseal(registry, REGISTRY_DIGEST_FIELD)
        result = self._run(inputs)
        self.assertIn("admission_gated_execution_cycle_not_strictly_after_registry_frontier", result.issues)

    def test_tampered_execution_input_digest_blocks(self):
        inputs = build_execution_inputs()
        inputs["execution_input"]["cycle_index"] = 3
        result = self._run(inputs)
        self.assertIn("execution_input_digest_mismatch", result.issues)

    def test_inactive_execution_input_blocks(self):
        inputs = build_execution_inputs()
        value = dict(inputs["execution_input"])
        value["execution_input_active"] = False
        inputs["execution_input"] = _reseal(value, EXECUTION_INPUT_DIGEST_FIELD)
        result = self._run(inputs)
        self.assertIn("execution_input_required_true:execution_input_active", result.issues)

    def test_reusable_execution_input_blocks(self):
        inputs = build_execution_inputs()
        value = dict(inputs["execution_input"])
        value["execution_input_reusable"] = True
        inputs["execution_input"] = _reseal(value, EXECUTION_INPUT_DIGEST_FIELD)
        result = self._run(inputs)
        self.assertIn("execution_input_required_false:execution_input_reusable", result.issues)

    def test_consumed_execution_input_blocks(self):
        inputs = build_execution_inputs()
        value = dict(inputs["execution_input"])
        value["execution_input_consumed"] = True
        inputs["execution_input"] = _reseal(value, EXECUTION_INPUT_DIGEST_FIELD)
        result = self._run(inputs)
        self.assertIn("execution_input_required_false:execution_input_consumed", result.issues)

    def test_consumption_receipt_digest_mismatch_blocks(self):
        inputs = build_execution_inputs()
        inputs["admission_consumption_receipt"]["cycle_execution_performed"] = True
        result = self._run(inputs)
        self.assertIn("admission_consumption_receipt_digest_mismatch", result.issues)

    def test_consumption_registry_correspondence_mismatch_blocks(self):
        inputs = build_execution_inputs()
        registry = dict(inputs["consumption_registry_receipt"])
        registry["registry_id"] = "other"
        inputs["consumption_registry_receipt"] = _reseal(registry, CONSUMPTION_REGISTRY_DIGEST_FIELD)
        result = self._run(inputs)
        self.assertIn("admission_gated_execution_correspondence_mismatch:consumption_registry", result.issues)

    def test_request_digest_mismatch_blocks(self):
        inputs = build_execution_inputs()
        inputs["execution_request"]["executor_actor_id"] = "other"
        result = self._run(inputs)
        self.assertIn("execution_request_digest_mismatch", result.issues)

    def test_policy_digest_mismatch_blocks(self):
        inputs = build_execution_inputs()
        inputs["execution_policy"]["maximum_command_count"] += 1
        result = self._run(inputs)
        self.assertIn("execution_policy_digest_mismatch", result.issues)

    def test_actor_mismatch_blocks(self):
        inputs = build_execution_inputs()
        request = dict(inputs["execution_request"])
        request["executor_actor_id"] = "other"
        inputs["execution_request"] = _reseal(request, REQUEST_DIGEST_FIELD)
        result = self._run(inputs)
        self.assertIn("admission_gated_execution_correspondence_mismatch:request_actor", result.issues)

    def test_execution_input_correspondence_mismatch_blocks(self):
        inputs = build_execution_inputs()
        request = dict(inputs["execution_request"])
        request["execution_input_digest"] = "e" * 64
        inputs["execution_request"] = _reseal(request, REQUEST_DIGEST_FIELD)
        result = self._run(inputs)
        self.assertIn("admission_gated_execution_correspondence_mismatch:request_execution_input", result.issues)

    def test_allowed_stage_set_must_be_exact(self):
        inputs = build_execution_inputs()
        policy = dict(inputs["execution_policy"])
        policy["allowed_stage_ids"] = list(policy["allowed_stage_ids"]) + ["git_push"]
        inputs["execution_policy"] = _reseal(policy, POLICY_DIGEST_FIELD)
        result = self._run(inputs)
        self.assertIn("execution_policy_allowed_stage_ids_not_exact", result.issues)

    def test_outer_policy_cannot_exceed_input_budget(self):
        inputs = build_execution_inputs()
        policy = dict(inputs["execution_policy"])
        policy["maximum_candidate_count"] = inputs["execution_input"]["maximum_candidate_count"] + 1
        inputs["execution_policy"] = _reseal(policy, POLICY_DIGEST_FIELD)
        result = self._run(inputs)
        self.assertIn("admission_gated_execution_policy_exceeds_input_budget:maximum_candidate_count", result.issues)

    def test_inner_policy_cannot_exceed_admitted_budget(self):
        inputs = build_execution_inputs()
        policy = dict(inputs["bounded_cycle_policy"])
        policy["maximum_command_count"] = inputs["execution_policy"]["maximum_command_count"] + 1
        inputs["bounded_cycle_policy"] = _reseal(policy, INNER_POLICY_DIGEST_FIELD)
        result = self._run(inputs)
        self.assertIn("bounded_cycle_policy_exceeds_admitted_budget:maximum_command_count", result.issues)

    def test_live_repository_authority_policy_blocks(self):
        inputs = build_execution_inputs()
        policy = dict(inputs["execution_policy"])
        policy["live_repository_access_allowed"] = True
        inputs["execution_policy"] = _reseal(policy, POLICY_DIGEST_FIELD)
        result = self._run(inputs)
        self.assertIn("execution_policy_required_false:live_repository_access_allowed", result.issues)

    def test_provider_forbidden_effect_blocks(self):
        inputs = build_execution_inputs()
        original = inputs["provider_adapter"]
        def provider(invocation):
            value = dict(original(invocation))
            value["network_used"] = True
            return value
        inputs["provider_adapter"] = provider
        result = self._run(inputs)
        self.assertIn("provider_result_forbidden_effect:network_used", result.issues)

    def test_provider_candidate_count_mismatch_blocks(self):
        inputs = build_execution_inputs()
        original = inputs["provider_adapter"]
        def provider(invocation):
            value = dict(original(invocation))
            value["generated_candidate_count"] += 1
            return value
        inputs["provider_adapter"] = provider
        result = self._run(inputs)
        self.assertIn("provider_generated_candidate_count_mismatch", result.issues)

    def test_provider_output_budget_blocks(self):
        inputs = build_execution_inputs()
        original = inputs["provider_adapter"]
        def provider(invocation):
            value = dict(original(invocation))
            value["provider_output_bytes"] = inputs["execution_policy"]["maximum_total_output_bytes"] + 1
            return value
        inputs["provider_adapter"] = provider
        result = self._run(inputs)
        self.assertIn("provider_output_budget_exceeded", result.issues)

    def test_provider_repair_lineage_mismatch_blocks(self):
        inputs = build_execution_inputs()
        original = inputs["provider_adapter"]
        def provider(invocation):
            value = dict(original(invocation))
            receipt = dict(value["source_repair_receipt"])
            receipt["codeai_verification_guided_candidate_repair_regeneration_receipt_digest"] = "f" * 64
            value["source_repair_receipt"] = receipt
            return value
        inputs["provider_adapter"] = provider
        result = self._run(inputs)
        self.assertIn("admission_gated_execution_lineage_mismatch:repair_receipt", result.issues)

    def test_verification_plan_lineage_mismatch_blocks(self):
        inputs = build_execution_inputs()
        value = dict(inputs["execution_input"])
        value["verification_plan_digest"] = "f" * 64
        inputs["execution_input"] = _reseal(value, EXECUTION_INPUT_DIGEST_FIELD)
        result = self._run(inputs)
        self.assertIn("admission_gated_execution_correspondence_mismatch:verification_plan", result.issues)

    def test_provider_exception_blocks_without_registry_transition(self):
        inputs = build_execution_inputs()
        def provider(_invocation):
            raise RuntimeError("provider failure")
        inputs["provider_adapter"] = provider
        result = self._run(inputs)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIsNone(result.next_registry)
        self.assertIn("provider_adapter_exception:RuntimeError", result.issues)

    def test_repository_snapshot_is_immutable_and_no_external_authority_is_granted(self):
        inputs = build_execution_inputs()
        before = copy.deepcopy(inputs["isolated_repository_files"])
        result = self._run(inputs)
        self.assertEqual(inputs["isolated_repository_files"], before)
        for field in (
            "repository_mutation_performed",
            "git_ref_changed",
            "merge_performed",
            "deployment_performed",
            "network_access_performed",
            "secret_access_performed",
            "general_successor_stage_authority_granted",
        ):
            self.assertFalse(result.receipt[field], field)


if __name__ == "__main__":
    unittest.main()
