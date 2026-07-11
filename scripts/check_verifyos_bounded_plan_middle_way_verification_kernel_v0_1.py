#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_verifyos_bounded_plan_middle_way_verification_kernel_v0_1 import (
    CONSTRAINT_FIELDS,
    PLAN_FIELDS,
    STATUS_READY,
    build_verifyos_bounded_plan_middle_way_verification_certificate,
    canonical_digest,
    compute_verifyos_bounded_plan_verification_bundle_digest,
)
from scripts.check_planos_bounded_synthesis_receipt_kernel_v0_1 import (
    _build as build_planos_v104_receipt,
)


def _source_receipt() -> dict:
    result = build_planos_v104_receipt()
    assert result.status == STATUS_READY
    assert result.receipt is not None
    return deepcopy(result.receipt)


def _digest_field(source: dict) -> str:
    for field in (
        "planos_bounded_synthesis_receipt_digest",
        "bounded_synthesis_receipt_digest",
        "plan_receipt_digest",
    ):
        if isinstance(source.get(field), str) and source[field]:
            return field
    candidates = [
        field
        for field, value in source.items()
        if field.endswith("receipt_digest") and isinstance(value, str) and value
    ]
    assert len(candidates) == 1
    return candidates[0]


def _mapping_field(source: dict, required: set[str]) -> str:
    candidates = [
        field
        for field, value in source.items()
        if isinstance(value, dict) and set(value) == required
    ]
    assert len(candidates) == 1
    return candidates[0]


def _redigest(source: dict) -> dict:
    value = deepcopy(source)
    field = _digest_field(value)
    value.pop(field, None)
    value[field] = canonical_digest(value)
    return value


def _redigest_plan(source: dict) -> dict:
    value = deepcopy(source)
    plan_field = _mapping_field(value, PLAN_FIELDS)
    plan_digest = canonical_digest(value[plan_field])
    for field in ("proposed_plan_digest", "bounded_plan_digest", "plan_digest"):
        if field in value:
            value[field] = plan_digest
    return _redigest(value)


def _build(**overrides):
    source = deepcopy(overrides.pop("source_plan_receipt", _source_receipt()))
    digest_field = _digest_field(source)
    source_digest = source[digest_field]
    current_world_binding = overrides.pop(
        "current_world_binding_digest", source["source_world_binding_digest"]
    )
    current_world_state = overrides.pop(
        "current_world_model_state_digest", source["source_world_model_state_digest"]
    )
    current_world_revision = overrides.pop(
        "current_world_model_revision", source["source_world_model_revision"]
    )
    current_world_lineage = overrides.pop(
        "current_world_lineage_digest", source["source_world_lineage_digest"]
    )
    candidate = overrides.pop("expected_selected_candidate_id", source["selected_candidate_id"])
    intent = overrides.pop(
        "expected_selected_candidate_plan_intent_digest",
        source["selected_candidate_plan_intent_digest"],
    )
    policy = overrides.pop("verification_policy_digest", "verifyos-plan-policy-v05")
    owner = overrides.pop(
        "verification_owner_responsibility_digest", "verifyos-plan-owner-v05"
    )
    request_id = overrides.pop("verification_request_id", "verify-plan-v05-001")
    expected_source_digest = overrides.pop(
        "expected_source_plan_receipt_digest", source_digest
    )
    bundle = overrides.pop(
        "verification_bundle_digest",
        compute_verifyos_bounded_plan_verification_bundle_digest(
            source_plan_receipt_digest=source_digest,
            expected_source_plan_receipt_digest=expected_source_digest,
            current_world_binding_digest=current_world_binding,
            current_world_model_state_digest=current_world_state,
            current_world_model_revision=current_world_revision,
            current_world_lineage_digest=current_world_lineage,
            expected_selected_candidate_id=candidate,
            expected_selected_candidate_plan_intent_digest=intent,
            verification_policy_digest=policy,
            verification_owner_responsibility_digest=owner,
            verification_request_id=request_id,
        ),
    )
    args = {
        "source_plan_receipt": source,
        "expected_source_plan_receipt_digest": expected_source_digest,
        "current_world_binding_digest": current_world_binding,
        "current_world_model_state_digest": current_world_state,
        "current_world_model_revision": current_world_revision,
        "current_world_lineage_digest": current_world_lineage,
        "expected_selected_candidate_id": candidate,
        "expected_selected_candidate_plan_intent_digest": intent,
        "verification_policy_digest": policy,
        "verification_owner_responsibility_digest": owner,
        "verification_request_id": request_id,
        "verification_bundle_digest": bundle,
    }
    args.update(overrides)
    return build_verifyos_bounded_plan_middle_way_verification_certificate(**args)


def main() -> int:
    valid = _build()
    assert valid.status == STATUS_READY, valid.blockers
    assert valid.certificate is not None
    certificate = valid.certificate
    assert certificate["verifyos_version"] == "v0.5"
    assert certificate["conditional_validity_status"] == "valid"
    assert certificate["verification_disposition"] == (
        "bounded_plan_verified_for_materialization_intake"
    )
    assert certificate["materialization_intake_admitted"] is True
    assert certificate["structural_verification_passed"] is True
    assert certificate["finite_plan_verified"] is True
    assert certificate["checkpoint_order_verified"] is True
    assert certificate["alternative_candidates_preserved"] is True
    assert certificate["dissent_evidence_preserved"] is True
    assert certificate["minority_evidence_preserved"] is True
    assert certificate["plan_remains_conditionally_binding"] is True
    assert certificate["plan_not_reified"] is True
    assert certificate["plan_not_erased"] is True
    assert certificate["selection_authority_granted_to_verifyos"] is False
    assert certificate["plan_revision_authority_granted_to_verifyos"] is False
    assert certificate["plan_activated"] is False
    assert certificate["materialization_performed"] is False
    assert certificate["execution_authority_granted"] is False
    assert certificate["execution_permission"] is False
    assert certificate["active_now"] is False

    changed_world = _build(current_world_model_revision=9)
    assert changed_world.status == STATUS_READY, changed_world.blockers
    assert changed_world.certificate is not None
    assert changed_world.certificate["conditional_validity_status"] == (
        "revision_required"
    )
    assert changed_world.certificate["verification_disposition"] == (
        "return_to_planos_revision"
    )
    assert changed_world.certificate["materialization_intake_admitted"] is False
    assert changed_world.certificate["plan_revision_required"] is True
    assert changed_world.certificate["source_lineage_preserved"] is True

    promoted = _source_receipt()
    promoted["execution_permission"] = True
    promoted = _redigest(promoted)

    broken_sequence = _source_receipt()
    plan_field = _mapping_field(broken_sequence, PLAN_FIELDS)
    broken_sequence[plan_field]["steps"][1]["sequence_index"] = 4
    broken_sequence = _redigest_plan(broken_sequence)

    broken_checkpoint = _source_receipt()
    plan_field = _mapping_field(broken_checkpoint, PLAN_FIELDS)
    irreversible = next(
        step for step in broken_checkpoint[plan_field]["steps"] if step["irreversible"]
    )
    irreversible["checkpoint_step_id"] = "missing-checkpoint"
    broken_checkpoint = _redigest_plan(broken_checkpoint)

    forbidden = _source_receipt()
    plan_field = _mapping_field(forbidden, PLAN_FIELDS)
    forbidden[plan_field]["steps"][0]["effect_tags"] = ["tool_invocation"]
    forbidden = _redigest_plan(forbidden)

    evidence_erased = _source_receipt()
    plan_field = _mapping_field(evidence_erased, PLAN_FIELDS)
    dissent = evidence_erased.get("preserved_dissent_evidence_digests", [])
    if dissent:
        evidence_erased[plan_field]["preserved_evidence_lineage_digests"] = [
            item
            for item in evidence_erased[plan_field][
                "preserved_evidence_lineage_digests"
            ]
            if item not in set(dissent)
        ]
    evidence_erased = _redigest_plan(evidence_erased)

    alternative_erased = _source_receipt()
    plan_field = _mapping_field(alternative_erased, PLAN_FIELDS)
    alternative_erased[plan_field]["retained_alternative_records"] = []
    alternative_erased = _redigest_plan(alternative_erased)

    constraints_changed = _source_receipt()
    constraint_field = _mapping_field(constraints_changed, CONSTRAINT_FIELDS)
    constraints_changed[constraint_field]["maximum_plan_steps"] = 0
    for field in ("synthesis_constraint_digest", "source_synthesis_constraint_digest"):
        if field in constraints_changed:
            constraints_changed[field] = canonical_digest(
                constraints_changed[constraint_field]
            )
    constraints_changed = _redigest(constraints_changed)

    blocked = [
        _build(source_plan_receipt={}),
        _build(expected_source_plan_receipt_digest="wrong"),
        _build(verification_bundle_digest="wrong"),
        _build(expected_selected_candidate_id="hold"),
        _build(source_plan_receipt=promoted),
        _build(source_plan_receipt=broken_sequence),
        _build(source_plan_receipt=broken_checkpoint),
        _build(source_plan_receipt=forbidden),
        _build(source_plan_receipt=evidence_erased),
        _build(source_plan_receipt=alternative_erased),
        _build(source_plan_receipt=constraints_changed),
    ]
    for result in blocked:
        assert result.status != STATUS_READY
        assert result.blockers
        assert result.certificate is None

    print("PASS: VerifyOS Bounded Plan Middle-Way Verification Kernel v0.1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
