#!/usr/bin/env python3
from copy import deepcopy

from runtime.kuuos_verifyos_middle_way_conditional_continuity_verification_v0_4 import (
    STATUS_READY,
    build_verifyos_middle_way_conditional_continuity_certificate,
    canonical_digest,
    compute_transition_spec_digest,
    compute_verification_bundle_digest,
)


def _source() -> dict:
    source = {
        "kernel": "DecisionOS Bounded Plan Synthesis Request Handoff Kernel",
        "kernel_version": "v0.1",
        "decisionos_version": "v0.8",
        "status": "DECISIONOS_BOUNDED_PLAN_SYNTHESIS_REQUEST_HANDOFF_ISSUED",
        "source_selection_receipt_digest": "selection-v07",
        "source_world_binding_digest": "world-binding-v14",
        "source_world_model_state_digest": "world-state-v14-r8",
        "source_world_model_revision": 8,
        "source_world_lineage_digest": "world-lineage-v14-r8",
        "synthesis_constraint_digest": "constraints-v08",
        "synthesis_handoff_bundle_digest": "handoff-bundle-v08",
        "selected_candidate_id": "continue",
        "selected_candidate_plan_intent_digest": "plan-intent-v08",
        "dissent_preservation_map": {
            "reobserve": ["dissent-reobserve"]
        },
        "minority_preservation_map": {"hold": ["minority-hold"]},
        "selected_candidate_not_substituted": True,
        "selection_remains_decisionos_owned": True,
        "candidate_evidence_lineage_preserved": True,
        "retained_alternatives_visible_to_synthesis": True,
        "retained_nonadmissible_candidates_visible": True,
        "nonselection_reasons_preserved": True,
        "dissent_visibility_preserved": True,
        "minority_visibility_preserved": True,
        "required_review_field_preserved": True,
        "planning_horizon_bounded": True,
        "plan_step_count_bounded": True,
        "branching_factor_bounded": True,
        "revision_cycles_bounded": True,
        "reversible_actions_required": True,
        "irreversible_step_requires_checkpoint": True,
        "stop_conditions_present": True,
        "forbidden_effects_fixed": True,
        "plan_synthesis_request_issued": True,
        "planos_synthesis_scope_bounded": True,
        "planos_receives_request_not_selection_authority": True,
        "selection_authority_transferred_to_planos": False,
        "execution_authority_granted_to_planos": False,
        "planos_plan_receipt_required": True,
        "plan_synthesis_result_not_accepted_without_receipt": True,
        "plan_synthesis_performed": False,
        "concrete_plan_issued": False,
        "plan_receipt_issued": False,
        "persistent_world_state_unchanged": True,
        "world_model_prediction_not_truth": True,
        "world_mutation_not_granted": True,
        "history_read_only": True,
        "qi_grants_no_authority": True,
        "future_only": True,
        "active_now": False,
        "execution_permission": False,
    }
    source[
        "decisionos_bounded_plan_synthesis_request_handoff_receipt_digest"
    ] = canonical_digest(source)
    return source


def _spec(source: dict, transition_kind: str = "retain") -> dict:
    source_conditions = [
        "condition-evidence-current",
        "condition-world-revision-r8",
    ]
    current_conditions = list(source_conditions)
    status = "valid"
    if transition_kind == "suspend":
        current_conditions = [
            "condition-evidence-conflict",
            "condition-world-revision-r8",
        ]
        status = "suspended"
    elif transition_kind == "request_revision":
        current_conditions = [
            "condition-evidence-current",
            "condition-world-revision-r9",
        ]
        status = "revision_required"
    elif transition_kind == "supersede_with_lineage":
        current_conditions = [
            "condition-new-selection",
            "condition-world-revision-r9",
        ]
        status = "superseded"
    elif transition_kind == "complete":
        current_conditions = [
            "condition-objective-completed",
            "condition-world-revision-r8",
        ]
        status = "completed"
    elif transition_kind == "terminate":
        current_conditions = [
            "condition-stop-triggered",
            "condition-world-revision-r8",
        ]
        status = "terminated"
    changed = sorted(set(source_conditions).symmetric_difference(current_conditions))
    source_digest = source[
        "decisionos_bounded_plan_synthesis_request_handoff_receipt_digest"
    ]
    return {
        "source_object_digest": source_digest,
        "predecessor_state_digest": "state-before-v04",
        "proposed_state_digest": f"state-after-{transition_kind}-v04",
        "source_condition_digests": sorted(source_conditions),
        "current_condition_digests": sorted(current_conditions),
        "changed_condition_digests": changed,
        "source_lineage_digests": sorted(
            [source_digest, "lineage-selection-v07"]
        ),
        "resulting_lineage_digests": sorted(
            [
                source_digest,
                "lineage-selection-v07",
                "predecessor-reference-v04",
                f"transition-{transition_kind}-v04",
            ]
        ),
        "predecessor_reference_digest": "predecessor-reference-v04",
        "source_responsibility_lineage_digests": ["decision-owner-v08"],
        "resulting_responsibility_lineage_digests": sorted(
            ["decision-owner-v08", "verify-owner-v04"]
        ),
        "transition_kind": transition_kind,
        "transition_reason_digest": f"reason-{transition_kind}-v04",
        "conditional_validity_status": status,
        "preserved_dissent_evidence_digests": ["dissent-reobserve"],
        "preserved_minority_evidence_digests": ["minority-hold"],
        "object_eternal_truth_claimed": False,
        "object_disposable_null_claimed": False,
        "silent_rewrite_requested": False,
        "history_erasure_requested": False,
        "authority_expansion_requested": False,
        "execution_permission_requested": False,
        "persistent_world_mutation_requested": False,
    }


def _build(transition_kind: str = "retain", **overrides):
    source = overrides.pop("source_handoff_receipt", _source())
    if "transition_spec" in overrides:
        spec = overrides.pop("transition_spec")
    else:
        spec = _spec(source, transition_kind) if source else {}
    policy = overrides.pop(
        "verification_policy_digest", "middle-way-policy-v04"
    )
    owner = overrides.pop(
        "verification_owner_responsibility_digest", "verify-owner-v04"
    )
    request_id = overrides.pop(
        "verification_request_id", "verify-request-v04-001"
    )
    spec_digest = overrides.pop(
        "transition_spec_digest", compute_transition_spec_digest(spec)
    )
    bundle = overrides.pop(
        "verification_bundle_digest",
        compute_verification_bundle_digest(
            source_handoff_receipt_digest=source.get(
                "decisionos_bounded_plan_synthesis_request_handoff_receipt_digest",
                "",
            ),
            verification_policy_digest=policy,
            verification_owner_responsibility_digest=owner,
            verification_request_id=request_id,
            transition_spec_digest=spec_digest,
            transition_spec=spec,
        ),
    )
    args = {
        "source_handoff_receipt": source,
        "verification_policy_digest": policy,
        "verification_owner_responsibility_digest": owner,
        "verification_request_id": request_id,
        "transition_spec": spec,
        "transition_spec_digest": spec_digest,
        "verification_bundle_digest": bundle,
    }
    args.update(overrides)
    return build_verifyos_middle_way_conditional_continuity_certificate(**args)


def _redigest_source(source: dict) -> dict:
    value = deepcopy(source)
    value.pop(
        "decisionos_bounded_plan_synthesis_request_handoff_receipt_digest",
        None,
    )
    value[
        "decisionos_bounded_plan_synthesis_request_handoff_receipt_digest"
    ] = canonical_digest(value)
    return value


def main() -> int:
    for kind, expected in (
        ("retain", "valid"),
        ("suspend", "suspended"),
        ("request_revision", "revision_required"),
        ("supersede_with_lineage", "superseded"),
        ("complete", "completed"),
        ("terminate", "terminated"),
    ):
        result = _build(kind)
        assert result.status == STATUS_READY
        assert result.certificate is not None
        certificate = result.certificate
        assert certificate["conditional_validity_status"] == expected
        assert certificate["verification_passed"] is True
        assert certificate["object_not_reified"] is True
        assert certificate["object_not_erased"] is True
        assert certificate["lineage_monotone"] is True
        assert certificate["termination_does_not_erase_history"] is True
        assert certificate["selection_remains_decisionos_owned"] is True
        assert certificate["plan_synthesis_performed"] is False
        assert certificate["active_now"] is False
        assert certificate["execution_permission"] is False

    source = _source()
    bad_status = _spec(source, "retain")
    bad_status["conditional_validity_status"] = "terminated"

    missing_lineage = _spec(source, "request_revision")
    missing_lineage["resulting_lineage_digests"].remove(
        "lineage-selection-v07"
    )

    erased_dissent = _spec(source, "request_revision")
    erased_dissent["preserved_dissent_evidence_digests"] = []

    reified = _spec(source, "retain")
    reified["object_eternal_truth_claimed"] = True

    erased = _spec(source, "terminate")
    erased["history_erasure_requested"] = True

    silent = _spec(source, "request_revision")
    silent["silent_rewrite_requested"] = True

    authority = _spec(source, "retain")
    authority["authority_expansion_requested"] = True

    unchanged_nonretain = _spec(source, "request_revision")
    unchanged_nonretain["current_condition_digests"] = list(
        unchanged_nonretain["source_condition_digests"]
    )
    unchanged_nonretain["changed_condition_digests"] = []

    promoted = _source()
    promoted["execution_permission"] = True
    promoted = _redigest_source(promoted)

    blocked = [
        _build(source_handoff_receipt={}),
        _build(verification_policy_digest=""),
        _build(verification_owner_responsibility_digest=""),
        _build(verification_request_id=""),
        _build(transition_spec={}),
        _build(transition_spec_digest="wrong"),
        _build(verification_bundle_digest="wrong"),
        _build(transition_spec=bad_status),
        _build(transition_spec=missing_lineage),
        _build(transition_spec=erased_dissent),
        _build(transition_spec=reified),
        _build(transition_spec=erased),
        _build(transition_spec=silent),
        _build(transition_spec=authority),
        _build(transition_spec=unchanged_nonretain),
        _build(source_handoff_receipt=promoted),
    ]
    for result in blocked:
        assert result.status != STATUS_READY
        assert result.blockers
        assert result.certificate is None

    print(
        "PASS: VerifyOS Middle-Way Conditional Continuity "
        "Verification Kernel v0.1"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
