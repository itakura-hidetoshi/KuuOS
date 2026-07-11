#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_verifyos_bounded_plan_middle_way_verification_kernel_v0_1 import (
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
    assert result.status == STATUS_READY, result.blockers
    assert result.receipt is not None
    return deepcopy(result.receipt)


def _redigest(source: dict) -> dict:
    value = deepcopy(source)
    value.pop("planos_bounded_synthesis_receipt_digest", None)
    value["planos_bounded_synthesis_receipt_digest"] = canonical_digest(value)
    return value


def _concrete_plan_payload(source: dict) -> dict:
    return {
        "plan_id": source["plan_id"],
        "plan_revision": source["plan_revision"],
        "selected_candidate_id": source["selected_candidate_id"],
        "selected_candidate_plan_intent_digest": source[
            "selected_candidate_plan_intent_digest"
        ],
        "source_world_model_state_digest": source[
            "source_world_model_state_digest"
        ],
        "plan_steps": source["plan_steps"],
        "stop_condition_digests": source["stop_condition_digests"],
        "retained_alternative_records": source[
            "retained_alternative_records"
        ],
        "preserved_evidence_lineage_digests": source[
            "preserved_evidence_lineage_digests"
        ],
    }


def _redigest_plan(source: dict) -> dict:
    value = deepcopy(source)
    value["concrete_plan_digest"] = canonical_digest(
        _concrete_plan_payload(value)
    )
    return _redigest(value)


def _build(**overrides):
    source = deepcopy(overrides.pop("source_plan_receipt", _source_receipt()))
    source_digest = source.get("planos_bounded_synthesis_receipt_digest", "")
    current_world_binding = overrides.pop(
        "current_world_binding_digest",
        source.get("source_world_binding_digest", "world-binding-missing"),
    )
    current_world_state = overrides.pop(
        "current_world_model_state_digest",
        source.get("source_world_model_state_digest", "world-state-missing"),
    )
    current_world_revision = overrides.pop(
        "current_world_model_revision",
        source.get("source_world_model_revision", 0),
    )
    current_world_lineage = overrides.pop(
        "current_world_lineage_digest",
        source.get("source_world_lineage_digest", "world-lineage-missing"),
    )
    candidate = overrides.pop(
        "expected_selected_candidate_id",
        source.get("selected_candidate_id", "candidate-missing"),
    )
    intent = overrides.pop(
        "expected_selected_candidate_plan_intent_digest",
        source.get(
            "selected_candidate_plan_intent_digest",
            "plan-intent-missing",
        ),
    )
    policy = overrides.pop(
        "verification_policy_digest",
        "verifyos-plan-policy-v05",
    )
    owner = overrides.pop(
        "verification_owner_responsibility_digest",
        "verifyos-plan-owner-v05",
    )
    request_id = overrides.pop(
        "verification_request_id",
        "verify-plan-v05-001",
    )
    expected_source_digest = overrides.pop(
        "expected_source_plan_receipt_digest",
        source_digest or "source-receipt-missing",
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
    return build_verifyos_bounded_plan_middle_way_verification_certificate(
        **args
    )


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
    broken_sequence["plan_steps"][1]["sequence_index"] = 4
    broken_sequence = _redigest_plan(broken_sequence)

    broken_checkpoint = _source_receipt()
    irreversible = next(
        step for step in broken_checkpoint["plan_steps"] if step["irreversible"]
    )
    irreversible["checkpoint_step_id"] = "missing-checkpoint"
    broken_checkpoint = _redigest_plan(broken_checkpoint)

    forbidden = _source_receipt()
    forbidden["plan_steps"][0]["effect_tags"] = ["tool_invocation"]
    forbidden = _redigest_plan(forbidden)

    dissent_erased = _source_receipt()
    dissent_erased["dissent_evidence_preserved"] = False
    dissent_erased = _redigest(dissent_erased)

    minority_erased = _source_receipt()
    minority_erased["minority_evidence_preserved"] = False
    minority_erased = _redigest(minority_erased)

    alternative_erased = _source_receipt()
    alternative_erased["retained_alternative_records"] = []
    alternative_erased = _redigest_plan(alternative_erased)

    constraints_changed = _source_receipt()
    constraints_changed["synthesis_constraints"]["maximum_plan_steps"] = 0
    changed_constraint_digest = canonical_digest(
        constraints_changed["synthesis_constraints"]
    )
    constraints_changed["synthesis_constraint_digest"] = (
        changed_constraint_digest
    )
    constraints_changed["source_synthesis_constraint_digest"] = (
        changed_constraint_digest
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
        _build(source_plan_receipt=dissent_erased),
        _build(source_plan_receipt=minority_erased),
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
