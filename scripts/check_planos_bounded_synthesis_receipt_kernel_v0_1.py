#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_planos_bounded_synthesis_receipt_kernel_v0_1 import (
    FIXED_FORBIDDEN_EFFECTS,
    STATUS_READY,
    build_planos_bounded_synthesis_receipt,
    canonical_digest,
    compute_bounded_synthesis_bundle_digest,
    compute_proposed_plan_digest,
    compute_synthesis_constraint_digest,
)


def _source_intake() -> dict:
    transition_spec = {
        "source_object_digest": "decisionos-handoff-v08",
        "predecessor_state_digest": "state-before-retain-v04",
        "proposed_state_digest": "state-after-retain-v04",
        "source_condition_digests": [
            "condition-evidence-current",
            "condition-world-revision-r8",
        ],
        "current_condition_digests": [
            "condition-evidence-current",
            "condition-world-revision-r8",
        ],
        "changed_condition_digests": [],
        "source_lineage_digests": [
            "decisionos-handoff-v08",
            "lineage-selection-v07",
        ],
        "resulting_lineage_digests": [
            "decisionos-handoff-v08",
            "lineage-selection-v07",
            "predecessor-reference-v04",
            "transition-retain-v04",
        ],
        "predecessor_reference_digest": "predecessor-reference-v04",
        "source_responsibility_lineage_digests": ["decision-owner-v08"],
        "resulting_responsibility_lineage_digests": [
            "decision-owner-v08",
            "verify-owner-v04",
        ],
        "transition_kind": "retain",
        "transition_reason_digest": "reason-retain-v04",
        "conditional_validity_status": "valid",
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
    source = {
        "kernel": "PlanOS Middle-Way Bounded Synthesis Intake Kernel",
        "kernel_version": "v0.1",
        "planos_version": "v1.03",
        "status": "PLANOS_MIDDLE_WAY_BOUNDED_SYNTHESIS_INTAKE_ROUTED",
        "source_verifyos_version": "v0.4",
        "source_verifyos_certificate_digest": "verifyos-certificate-v04",
        "expected_source_verifyos_certificate_digest": "verifyos-certificate-v04",
        "source_decisionos_handoff_receipt_digest": "decisionos-handoff-v08",
        "source_selection_receipt_digest": "selection-receipt-v07",
        "source_world_binding_digest": "world-binding-v14",
        "source_world_model_state_digest": "world-state-v14-r8",
        "source_world_model_revision": 8,
        "source_world_lineage_digest": "world-lineage-v14-r8",
        "source_synthesis_constraint_digest": "",
        "source_synthesis_handoff_bundle_digest": "handoff-bundle-v08",
        "selected_candidate_id": "continue",
        "selected_candidate_plan_intent_digest": "plan-intent-continue-v08",
        "source_transition_spec": transition_spec,
        "source_transition_spec_digest": canonical_digest(transition_spec),
        "conditional_validity_status": "valid",
        "transition_kind": "retain",
        "transition_reason_digest": "reason-retain-v04",
        "intake_disposition": "bounded_synthesis_intake_ready",
        "intake_policy_digest": "planos-intake-policy-v103",
        "planos_intake_responsibility_digest": "planos-intake-owner-v103",
        "intake_request_id": "planos-intake-v103-001",
        "intake_bundle_digest": "planos-intake-bundle-v103",
        "bounded_synthesis_request_admitted": True,
        "bounded_synthesis_intake_ready": True,
        "awaiting_condition_change": False,
        "decisionos_revision_required": False,
        "successor_lineage_reverification_required": False,
        "close_without_synthesis": False,
        "terminate_without_synthesis": False,
        "conditional_validity_enforced": True,
        "only_valid_status_admitted": True,
        "nonvalid_status_not_synthesized": True,
        "source_conditions_preserved": True,
        "source_changed_conditions_preserved": True,
        "source_lineage_preserved": True,
        "source_predecessor_preserved": True,
        "source_responsibility_preserved": True,
        "source_dissent_preserved": True,
        "source_minority_evidence_preserved": True,
        "resulting_responsibility_lineage_digests": [
            "decision-owner-v08",
            "planos-intake-owner-v103",
            "verify-owner-v04",
        ],
        "responsibility_extended_not_replaced": True,
        "selection_remains_decisionos_owned": True,
        "selection_authority_granted_to_planos": False,
        "plan_synthesis_performed": False,
        "concrete_plan_issued": False,
        "plan_receipt_issued": False,
        "execution_authority_granted": False,
        "execution_permission": False,
        "persistent_world_state_unchanged": True,
        "world_model_prediction_not_truth": True,
        "world_mutation_not_granted": True,
        "history_read_only": True,
        "qi_grants_no_authority": True,
        "future_only": True,
        "active_now": False,
    }
    return source


def _constraints() -> dict:
    return {
        "planning_horizon": 6,
        "maximum_plan_steps": 6,
        "maximum_branching_factor": 3,
        "maximum_revision_cycles": 2,
        "reversible_actions_required": True,
        "irreversible_step_requires_checkpoint": True,
        "stop_condition_digests": [
            "stop-evidence-conflict",
            "stop-world-revision-change",
        ],
        "forbidden_effects": list(FIXED_FORBIDDEN_EFFECTS),
    }


def _plan() -> dict:
    stops = ["stop-evidence-conflict", "stop-world-revision-change"]
    evidence = [
        "dissent-reobserve",
        "minority-hold",
        "selected-support-rationale",
    ]
    return {
        "plan_id": "bounded-plan-v104-001",
        "plan_revision": 0,
        "selected_candidate_id": "continue",
        "selected_candidate_plan_intent_digest": "plan-intent-continue-v08",
        "world_state_dependency_digest": "world-state-v14-r8",
        "stop_condition_digests": stops,
        "retained_alternative_records": [
            {
                "candidate_id": "hold",
                "nonselection_reason_digest": "reason-hold-not-selected",
                "retained_for_revision": True,
            },
            {
                "candidate_id": "reobserve",
                "nonselection_reason_digest": "reason-reobserve-not-selected",
                "retained_for_revision": True,
            },
        ],
        "preserved_evidence_lineage_digests": evidence,
        "steps": [
            {
                "step_id": "step-01",
                "sequence_index": 1,
                "action_class": "evidence_collection",
                "action_spec_digest": "action-collect-evidence",
                "precondition_digests": ["condition-evidence-current"],
                "expected_effect_digests": ["effect-evidence-refreshed"],
                "effect_tags": ["internal_evidence_update"],
                "evidence_lineage_digests": ["selected-support-rationale"],
                "stop_condition_digests": stops,
                "reversible": True,
                "irreversible": False,
                "checkpoint_step_id": "",
                "branch_ids": ["branch-continue", "branch-hold"],
            },
            {
                "step_id": "step-02",
                "sequence_index": 2,
                "action_class": "review_checkpoint",
                "action_spec_digest": "action-review-checkpoint",
                "precondition_digests": ["effect-evidence-refreshed"],
                "expected_effect_digests": ["effect-checkpoint-recorded"],
                "effect_tags": ["internal_review_checkpoint"],
                "evidence_lineage_digests": [
                    "dissent-reobserve",
                    "minority-hold",
                ],
                "stop_condition_digests": stops,
                "reversible": True,
                "irreversible": False,
                "checkpoint_step_id": "",
                "branch_ids": [],
            },
            {
                "step_id": "step-03",
                "sequence_index": 3,
                "action_class": "prepare_reversible",
                "action_spec_digest": "action-prepare-reversible",
                "precondition_digests": ["effect-checkpoint-recorded"],
                "expected_effect_digests": ["effect-plan-prepared"],
                "effect_tags": ["internal_plan_preparation"],
                "evidence_lineage_digests": ["selected-support-rationale"],
                "stop_condition_digests": stops,
                "reversible": True,
                "irreversible": False,
                "checkpoint_step_id": "",
                "branch_ids": ["branch-continue"],
            },
            {
                "step_id": "step-04",
                "sequence_index": 4,
                "action_class": "analyze",
                "action_spec_digest": "action-finalize-bounded-plan",
                "precondition_digests": ["effect-plan-prepared"],
                "expected_effect_digests": ["effect-bounded-plan-finalized"],
                "effect_tags": ["future_plan_finalization"],
                "evidence_lineage_digests": [
                    "dissent-reobserve",
                    "minority-hold",
                    "selected-support-rationale",
                ],
                "stop_condition_digests": stops,
                "reversible": False,
                "irreversible": True,
                "checkpoint_step_id": "step-02",
                "branch_ids": [],
            },
        ],
    }


def _redigest_source(source: dict) -> dict:
    value = deepcopy(source)
    value.pop("planos_middle_way_bounded_synthesis_intake_certificate_digest", None)
    value["planos_middle_way_bounded_synthesis_intake_certificate_digest"] = (
        canonical_digest(value)
    )
    return value


def _build(**overrides):
    constraints = deepcopy(overrides.pop("synthesis_constraints", _constraints()))
    constraint_digest = overrides.pop(
        "synthesis_constraint_digest", compute_synthesis_constraint_digest(constraints)
    )
    source = deepcopy(overrides.pop("source_intake_certificate", _source_intake()))
    source["source_synthesis_constraint_digest"] = constraint_digest
    source = _redigest_source(source)
    plan = deepcopy(overrides.pop("proposed_plan", _plan()))
    plan_digest = overrides.pop(
        "proposed_plan_digest", compute_proposed_plan_digest(plan)
    )
    alt_digest = overrides.pop(
        "alternative_lineage_bundle_digest",
        canonical_digest(plan.get("retained_alternative_records")),
    )
    policy = overrides.pop("synthesis_policy_digest", "synthesis-policy-v104")
    owner = overrides.pop(
        "planos_synthesis_responsibility_digest", "planos-synthesis-owner-v104"
    )
    request_id = overrides.pop("synthesis_request_id", "synthesis-request-v104-001")
    expected_source_digest = overrides.pop(
        "expected_source_intake_certificate_digest",
        source.get("planos_middle_way_bounded_synthesis_intake_certificate_digest", ""),
    )
    bundle = overrides.pop(
        "synthesis_bundle_digest",
        compute_bounded_synthesis_bundle_digest(
            source_intake_certificate_digest=source.get(
                "planos_middle_way_bounded_synthesis_intake_certificate_digest", ""
            ),
            expected_source_intake_certificate_digest=expected_source_digest,
            expected_world_binding_digest="world-binding-v14",
            expected_world_model_state_digest="world-state-v14-r8",
            expected_world_model_revision=8,
            expected_world_lineage_digest="world-lineage-v14-r8",
            expected_selected_candidate_id="continue",
            expected_selected_candidate_plan_intent_digest=(
                "plan-intent-continue-v08"
            ),
            expected_synthesis_constraint_digest=constraint_digest,
            synthesis_constraint_digest=constraint_digest,
            synthesis_policy_digest=policy,
            planos_synthesis_responsibility_digest=owner,
            synthesis_request_id=request_id,
            proposed_plan_digest=plan_digest,
            alternative_lineage_bundle_digest=alt_digest,
        ),
    )
    args = {
        "source_intake_certificate": source,
        "expected_source_intake_certificate_digest": expected_source_digest,
        "expected_world_binding_digest": "world-binding-v14",
        "expected_world_model_state_digest": "world-state-v14-r8",
        "expected_world_model_revision": 8,
        "expected_world_lineage_digest": "world-lineage-v14-r8",
        "expected_selected_candidate_id": "continue",
        "expected_selected_candidate_plan_intent_digest": (
            "plan-intent-continue-v08"
        ),
        "expected_synthesis_constraint_digest": constraint_digest,
        "synthesis_constraints": constraints,
        "synthesis_constraint_digest": constraint_digest,
        "synthesis_policy_digest": policy,
        "planos_synthesis_responsibility_digest": owner,
        "synthesis_request_id": request_id,
        "proposed_plan": plan,
        "proposed_plan_digest": plan_digest,
        "alternative_lineage_bundle_digest": alt_digest,
        "synthesis_bundle_digest": bundle,
    }
    args.update(overrides)
    return build_planos_bounded_synthesis_receipt(**args)


def main() -> int:
    result = _build()
    assert result.status == STATUS_READY
    assert result.receipt is not None
    receipt = result.receipt
    assert receipt["planos_version"] == "v1.04"
    assert receipt["plan_step_count"] == 4
    assert receipt["finite_plan_constructed"] is True
    assert receipt["plan_synthesis_performed"] is True
    assert receipt["concrete_plan_issued"] is True
    assert receipt["plan_receipt_issued"] is True
    assert receipt["selected_candidate_not_substituted"] is True
    assert receipt["alternative_candidates_retained"] is True
    assert receipt["dissent_evidence_preserved"] is True
    assert receipt["minority_evidence_preserved"] is True
    assert receipt["irreversible_steps_checkpoint_guarded"] is True
    assert receipt["selection_remains_decisionos_owned"] is True
    assert receipt["selection_authority_granted_to_planos"] is False
    assert receipt["plan_activated"] is False
    assert receipt["materialization_performed"] is False
    assert receipt["execution_authority_granted"] is False
    assert receipt["execution_permission"] is False
    assert receipt["persistent_world_state_unchanged"] is True
    assert receipt["active_now"] is False

    nonvalid_source = _source_intake()
    nonvalid_source["conditional_validity_status"] = "suspended"
    nonvalid_source["transition_kind"] = "suspend"
    nonvalid_source["intake_disposition"] = "await_condition_change"
    nonvalid_source["bounded_synthesis_request_admitted"] = False
    nonvalid_source["bounded_synthesis_intake_ready"] = False
    nonvalid_source["awaiting_condition_change"] = True
    nonvalid_source = _redigest_source(nonvalid_source)

    substituted = _plan()
    substituted["selected_candidate_id"] = "hold"

    too_many = _plan()
    too_many["steps"] = too_many["steps"] * 2
    for index, step in enumerate(too_many["steps"]):
        step = deepcopy(step)
        step["step_id"] = f"duplicate-expanded-{index + 1:02d}"
        step["sequence_index"] = index + 1
        step["action_spec_digest"] = f"expanded-action-{index + 1:02d}"
        too_many["steps"][index] = step

    missing_checkpoint = _plan()
    missing_checkpoint["steps"][-1]["checkpoint_step_id"] = ""

    forbidden_effect = _plan()
    forbidden_effect["steps"][0]["effect_tags"] = ["tool_invocation"]

    erased_evidence = _plan()
    erased_evidence["preserved_evidence_lineage_digests"] = [
        "selected-support-rationale"
    ]

    bad_alternative = _plan()
    bad_alternative["retained_alternative_records"][0][
        "nonselection_reason_digest"
    ] = ""

    promoted_source = _source_intake()
    promoted_source["execution_permission"] = True
    promoted_source = _redigest_source(promoted_source)

    bad_constraints = _constraints()
    bad_constraints["forbidden_effects"] = list(FIXED_FORBIDDEN_EFFECTS[:-1])

    blocked = [
        _build(source_intake_certificate={}),
        _build(expected_source_intake_certificate_digest="wrong"),
        _build(source_intake_certificate=nonvalid_source),
        _build(proposed_plan=substituted),
        _build(proposed_plan=too_many),
        _build(proposed_plan=missing_checkpoint),
        _build(proposed_plan=forbidden_effect),
        _build(proposed_plan=erased_evidence),
        _build(proposed_plan=bad_alternative),
        _build(source_intake_certificate=promoted_source),
        _build(synthesis_constraints=bad_constraints),
        _build(proposed_plan_digest="wrong"),
        _build(alternative_lineage_bundle_digest="wrong"),
        _build(synthesis_bundle_digest="wrong"),
    ]
    for item in blocked:
        assert item.status != STATUS_READY
        assert item.blockers
        assert item.receipt is None

    print("PASS: PlanOS Bounded Synthesis Receipt Kernel v0.1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
