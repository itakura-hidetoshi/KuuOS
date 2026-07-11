#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_actos_dukkha_supported_bounded_plan_materialization_intake_v0_1 import (
    STATUS_READY,
    build_actos_dukkha_supported_bounded_plan_materialization_intake,
    canonical_digest,
    compute_concrete_plan_digest,
    compute_materialization_intake_bundle_digest,
)
from scripts.check_verifyos_dukkha_reduction_claim_verification_kernel_v0_1 import (
    _build as build_verifyos_v06_certificate,
)
from scripts.check_verifyos_bounded_plan_middle_way_verification_kernel_v0_1 import (
    _source_receipt as build_planos_v104_receipt,
)


SOURCE_DIGEST_FIELD = (
    "verifyos_dukkha_reduction_claim_verification_certificate_digest"
)
PLAN_DIGEST_FIELD = "planos_bounded_synthesis_receipt_digest"


def _source_certificate() -> dict:
    result = build_verifyos_v06_certificate()
    assert result.status == STATUS_READY, result.blockers
    assert result.certificate is not None
    return deepcopy(result.certificate)


def _source_plan_receipt() -> dict:
    return deepcopy(build_planos_v104_receipt())


def _redigest_source(source: dict) -> dict:
    value = deepcopy(source)
    value.pop(SOURCE_DIGEST_FIELD, None)
    value[SOURCE_DIGEST_FIELD] = canonical_digest(value)
    return value


def _redigest_plan(plan: dict) -> dict:
    value = deepcopy(plan)
    value["concrete_plan_digest"] = compute_concrete_plan_digest(value)
    value.pop(PLAN_DIGEST_FIELD, None)
    value[PLAN_DIGEST_FIELD] = canonical_digest(value)
    return value


def _rebind_source_to_plan(source: dict, plan: dict) -> dict:
    value = deepcopy(source)
    value["source_plan_receipt_digest"] = plan[PLAN_DIGEST_FIELD]
    value["source_concrete_plan_digest"] = plan["concrete_plan_digest"]
    return _redigest_source(value)


def _build(**overrides):
    source_override = overrides.pop("source_verifyos_dukkha_certificate", None)
    source = deepcopy(
        _source_certificate() if source_override is None else source_override
    )
    plan_override = overrides.pop("source_plan_receipt", None)
    plan = deepcopy(_source_plan_receipt() if plan_override is None else plan_override)
    source_digest = source.get(SOURCE_DIGEST_FIELD, "source-v06-missing")
    plan_digest = plan.get(PLAN_DIGEST_FIELD, "plan-v104-missing")
    expected_source = overrides.pop(
        "expected_source_verifyos_dukkha_certificate_digest", source_digest
    )
    expected_plan = overrides.pop(
        "expected_source_plan_receipt_digest", plan_digest
    )
    policy = overrides.pop(
        "materialization_policy_digest", "actos-materialization-policy-v05"
    )
    owner = overrides.pop(
        "actos_materialization_responsibility_digest",
        "actos-materialization-owner-v05",
    )
    request_id = overrides.pop(
        "materialization_request_id", "actos-materialization-v05-001"
    )
    bundle = overrides.pop(
        "materialization_bundle_digest",
        compute_materialization_intake_bundle_digest(
            source_verifyos_dukkha_certificate_digest=source_digest,
            expected_source_verifyos_dukkha_certificate_digest=expected_source,
            source_plan_receipt_digest=plan_digest,
            expected_source_plan_receipt_digest=expected_plan,
            source_concrete_plan_digest=plan.get(
                "concrete_plan_digest", "concrete-plan-missing"
            ),
            materialization_policy_digest=policy,
            actos_materialization_responsibility_digest=owner,
            materialization_request_id=request_id,
        ),
    )
    args = {
        "source_verifyos_dukkha_certificate": source,
        "expected_source_verifyos_dukkha_certificate_digest": expected_source,
        "source_plan_receipt": plan,
        "expected_source_plan_receipt_digest": expected_plan,
        "materialization_policy_digest": policy,
        "actos_materialization_responsibility_digest": owner,
        "materialization_request_id": request_id,
        "materialization_bundle_digest": bundle,
    }
    args.update(overrides)
    return build_actos_dukkha_supported_bounded_plan_materialization_intake(**args)


def main() -> int:
    ready = _build()
    assert ready.status == STATUS_READY, ready.blockers
    assert ready.receipt is not None
    receipt = ready.receipt
    assert receipt["actos_version"] == "v0.5"
    assert receipt["status"] == (
        "ACTOS_DUKKHA_SUPPORTED_BOUNDED_PLAN_MATERIALIZATION_INTAKE_READY"
    )
    assert receipt["materialization_candidate_count"] == 4
    assert receipt["materialization_intake_performed"] is True
    assert receipt["materialization_candidates_issued"] is True
    assert receipt["all_plan_steps_materialized"] is True
    assert receipt["one_to_one_step_mapping_preserved"] is True
    assert receipt["step_sequence_preserved"] is True
    assert receipt["checkpoint_guards_preserved"] is True
    assert receipt["dukkha_reduction_support_preserved"] is True
    assert receipt["protected_group_nonexternalization_preserved"] is True
    assert receipt["future_nonexternalization_preserved"] is True
    assert receipt["selection_authority_granted_to_actos"] is False
    assert receipt["plan_activated"] is False
    assert receipt["adapter_binding_performed"] is False
    assert receipt["adapter_invocation_performed"] is False
    assert receipt["tool_invocation_performed"] is False
    assert receipt["external_side_effect_performed"] is False
    assert receipt["execution_permission"] is False
    assert all(
        candidate["candidate_state"] == "prepared_not_activated"
        and candidate["adapter_binding_digest"] == ""
        and candidate["tool_invocation_requested"] is False
        and candidate["execution_permission_requested"] is False
        for candidate in receipt["materialization_candidates"]
    )

    promoted_source = _source_certificate()
    promoted_source["execution_permission"] = True
    promoted_source = _redigest_source(promoted_source)

    indeterminate_source = _source_certificate()
    indeterminate_source["dukkha_reduction_claim_status"] = "indeterminate"
    indeterminate_source["verification_disposition"] = "additional_evidence_required"
    indeterminate_source["materialization_intake_admitted"] = False
    indeterminate_source["additional_evidence_required"] = True
    indeterminate_source = _redigest_source(indeterminate_source)

    broken_sequence_plan = _source_plan_receipt()
    broken_sequence_plan["plan_steps"][1]["sequence_index"] = 4
    broken_sequence_plan = _redigest_plan(broken_sequence_plan)
    broken_sequence_source = _rebind_source_to_plan(
        _source_certificate(), broken_sequence_plan
    )

    forbidden_plan = _source_plan_receipt()
    forbidden_plan["plan_steps"][0]["effect_tags"] = ["tool_invocation"]
    forbidden_plan = _redigest_plan(forbidden_plan)
    forbidden_source = _rebind_source_to_plan(_source_certificate(), forbidden_plan)

    missing_step_plan = _source_plan_receipt()
    missing_step_plan["plan_steps"] = missing_step_plan["plan_steps"][:-1]
    missing_step_plan = _redigest_plan(missing_step_plan)
    missing_step_source = _rebind_source_to_plan(
        _source_certificate(), missing_step_plan
    )

    blocked = [
        _build(source_verifyos_dukkha_certificate={}),
        _build(source_plan_receipt={}),
        _build(expected_source_verifyos_dukkha_certificate_digest="wrong"),
        _build(expected_source_plan_receipt_digest="wrong"),
        _build(materialization_bundle_digest="wrong"),
        _build(source_verifyos_dukkha_certificate=promoted_source),
        _build(source_verifyos_dukkha_certificate=indeterminate_source),
        _build(
            source_verifyos_dukkha_certificate=broken_sequence_source,
            source_plan_receipt=broken_sequence_plan,
        ),
        _build(
            source_verifyos_dukkha_certificate=forbidden_source,
            source_plan_receipt=forbidden_plan,
        ),
        _build(
            source_verifyos_dukkha_certificate=missing_step_source,
            source_plan_receipt=missing_step_plan,
        ),
    ]
    for result in blocked:
        assert result.status != STATUS_READY
        assert result.blockers
        assert result.receipt is None

    print(
        "PASS: ActOS Dukkha-Supported Bounded Plan "
        "Materialization Intake Kernel v0.1"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
