#!/usr/bin/env python3
from copy import deepcopy

from runtime.kuuos_decisionos_bounded_plan_synthesis_request_handoff_v0_8 import (
    FORBIDDEN_EFFECTS,
    STATUS_READY,
    build_decisionos_bounded_plan_synthesis_request_handoff_receipt,
    canonical_digest,
    compute_source_candidate_selection_justification_digest,
    compute_source_selection_bundle_digest,
    compute_synthesis_constraint_digest,
    compute_synthesis_handoff_bundle_digest,
)


def _source_item(candidate_id: str, *, selected: bool = False) -> dict:
    item = {
        "candidate_id": candidate_id,
        "source_deliberation_record_digest": f"record-{candidate_id}",
        "selected": selected,
        "support_rationale_digests": (
            [f"support-{candidate_id}"] if selected else []
        ),
        "opposition_rationale_digests": (
            [f"opposition-{candidate_id}"] if selected else [f"oppose-{candidate_id}"]
        ),
        "dissent_preservation_digests": (
            ["dissent-preserved-reobserve"] if candidate_id == "reobserve" else []
        ),
        "minority_preservation_digests": (
            ["minority-preserved-hold"] if candidate_id == "hold" else []
        ),
        "review_resolution_digests": (
            [f"review-{candidate_id}"]
            if candidate_id in {"continue", "repair", "reobserve", "hold"}
            else []
        ),
        "nonselection_reason_digest": (
            "" if selected else f"nonselection-{candidate_id}"
        ),
        "candidate_selection_justification_digest": "",
    }
    item["candidate_selection_justification_digest"] = (
        compute_source_candidate_selection_justification_digest(item)
    )
    return item


def _source() -> dict:
    candidate_ids = [
        "continue",
        "repair",
        "reobserve",
        "hold",
        "terminate_candidate",
    ]
    items = [
        _source_item(candidate_id, selected=(candidate_id == "continue"))
        for candidate_id in candidate_ids
    ]
    source = {
        "kernel": "DecisionOS WORLD-Conditioned Selection Justification Kernel",
        "kernel_version": "v0.1",
        "decisionos_version": "v0.7",
        "status": "DECISIONOS_WORLD_CONDITIONED_SELECTION_JUSTIFICATION_ISSUED",
        "source_decisionos_version": "v0.6",
        "source_deliberation_receipt_digest": "deliberation-v06",
        "source_intake_receipt_digest": "intake-v05",
        "source_planos_handoff_certificate_digest": "planos-v102",
        "source_world_binding_digest": "world-binding-v14",
        "source_world_model_state_digest": "world-state-v14-r8",
        "source_world_model_revision": 8,
        "source_world_lineage_digest": "world-lineage-v14-r8",
        "selection_policy_digest": "selection-policy-v07",
        "selector_responsibility_digest": "decision-owner-v07",
        "selection_bundle_digest": "",
        "hold_guard_resolution_digest": "hold-reviewed-v07",
        "candidate_selection_justification_items": items,
        "selected_candidate_id": "continue",
        "selected_candidate_source_record_digest": "record-continue",
        "selected_candidate_support_rationale_digests": ["support-continue"],
        "selected_candidate_opposition_rationale_digests": [
            "opposition-continue"
        ],
        "relational_frontier_candidate_ids": ["continue", "repair"],
        "required_review_candidate_ids": [
            "continue",
            "repair",
            "reobserve",
            "hold",
        ],
        "retained_alternative_candidate_ids": [
            "hold",
            "reobserve",
            "repair",
        ],
        "retained_nonadmissible_candidate_ids": ["terminate_candidate"],
        "nonselection_reason_map": {
            item["candidate_id"]: item["nonselection_reason_digest"]
            for item in items
            if not item["selected"]
        },
        "dissent_preservation_map": {
            "reobserve": ["dissent-preserved-reobserve"]
        },
        "minority_preservation_map": {
            "hold": ["minority-preserved-hold"]
        },
        "review_resolution_map": {
            candidate_id: [f"review-{candidate_id}"]
            for candidate_id in ["continue", "repair", "reobserve", "hold"]
        },
        "all_candidates_considered": True,
        "candidate_identity_preserved": True,
        "retained_alternatives_preserved": True,
        "nonselected_reasons_preserved": True,
        "dissent_visibility_preserved": True,
        "minority_visibility_preserved": True,
        "required_review_field_preserved": True,
        "silent_substitution_detected": False,
        "source_probability_used_as_advisory_only": True,
        "source_action_used_as_advisory_only": True,
        "relational_partial_order_used": True,
        "single_scalar_utility_selection_forbidden": True,
        "selected_candidate_from_relational_frontier": True,
        "selection_authority_exercised_by_decision_os": True,
        "selection_authority_inherited_from_planos": False,
        "selection_authority_inherited_from_world_model": False,
        "selection_authority_inherited_from_qi": False,
        "decision_selection_performed": True,
        "selected_candidate_present": True,
        "decision_receipt_issued": True,
        "selection_is_not_plan_synthesis": True,
        "selection_is_not_execution": True,
        "persistent_world_state_unchanged": True,
        "world_model_prediction_not_truth": True,
        "world_mutation_not_granted": True,
        "history_read_only": True,
        "qi_grants_no_authority": True,
        "plan_synthesis_performed": False,
        "future_only": True,
        "active_now": False,
        "execution_permission": False,
    }
    source["selection_bundle_digest"] = compute_source_selection_bundle_digest(source)
    source["decisionos_selection_justification_receipt_digest"] = canonical_digest(
        source
    )
    return source


def _required_evidence(source: dict) -> list[str]:
    return sorted(
        {
            source["decisionos_selection_justification_receipt_digest"],
            source["selected_candidate_source_record_digest"],
            source["source_planos_handoff_certificate_digest"],
            source["source_world_binding_digest"],
            source["source_world_model_state_digest"],
            source["source_world_lineage_digest"],
            *source["selected_candidate_support_rationale_digests"],
            *source["selected_candidate_opposition_rationale_digests"],
        }
    )


def _spec(source: dict) -> dict:
    return {
        "planning_horizon_steps": 12,
        "maximum_plan_steps": 8,
        "maximum_branching_factor": 3,
        "maximum_revision_cycles": 2,
        "require_reversible_actions": True,
        "require_checkpoint_before_irreversible_step": True,
        "required_checkpoint_digests": sorted(
            ["checkpoint-before-commit", "checkpoint-before-side-effect"]
        ),
        "stop_condition_digests": sorted(
            ["stop-on-boundary-breach", "stop-on-evidence-conflict"]
        ),
        "preserved_evidence_digests": _required_evidence(source),
        "forbidden_effects": sorted(FORBIDDEN_EFFECTS),
    }


def _redigest_source(source: dict) -> dict:
    value = deepcopy(source)
    value.pop("decisionos_selection_justification_receipt_digest", None)
    value["selection_bundle_digest"] = compute_source_selection_bundle_digest(value)
    value["decisionos_selection_justification_receipt_digest"] = canonical_digest(value)
    return value


def _build(**overrides):
    source = overrides.pop("source_selection_receipt", _source())
    if "synthesis_constraint_spec" in overrides:
        spec = overrides.pop("synthesis_constraint_spec")
    else:
        spec = _spec(source) if source else {}
    policy = overrides.pop("synthesis_policy_digest", "synthesis-policy-v08")
    recipient = overrides.pop("planos_recipient_digest", "planos-recipient-v08")
    owner = overrides.pop(
        "request_owner_responsibility_digest", "decision-owner-v08"
    )
    request_id = overrides.pop("synthesis_request_id", "synthesis-request-v08-001")
    selected = overrides.pop(
        "requested_selected_candidate_id", source.get("selected_candidate_id", "")
    )
    intent = overrides.pop(
        "selected_candidate_plan_intent_digest", "plan-intent-continue-v08"
    )
    constraint_digest = overrides.pop(
        "synthesis_constraint_digest", compute_synthesis_constraint_digest(spec)
    )
    bundle = overrides.pop(
        "synthesis_handoff_bundle_digest",
        compute_synthesis_handoff_bundle_digest(
            source_selection_receipt_digest=source.get(
                "decisionos_selection_justification_receipt_digest", ""
            ),
            synthesis_policy_digest=policy,
            planos_recipient_digest=recipient,
            request_owner_responsibility_digest=owner,
            synthesis_request_id=request_id,
            requested_selected_candidate_id=selected,
            selected_candidate_plan_intent_digest=intent,
            synthesis_constraint_digest=constraint_digest,
            synthesis_constraint_spec=spec,
        ),
    )
    args = {
        "source_selection_receipt": source,
        "synthesis_policy_digest": policy,
        "planos_recipient_digest": recipient,
        "request_owner_responsibility_digest": owner,
        "synthesis_request_id": request_id,
        "requested_selected_candidate_id": selected,
        "selected_candidate_plan_intent_digest": intent,
        "synthesis_constraint_spec": spec,
        "synthesis_constraint_digest": constraint_digest,
        "synthesis_handoff_bundle_digest": bundle,
    }
    args.update(overrides)
    return build_decisionos_bounded_plan_synthesis_request_handoff_receipt(**args)


def main() -> int:
    result = _build()
    assert result.status == STATUS_READY
    assert result.receipt is not None
    receipt = result.receipt
    assert receipt["selected_candidate_id"] == "continue"
    assert receipt["selected_candidate_not_substituted"] is True
    assert receipt["selection_remains_decisionos_owned"] is True
    assert receipt["plan_synthesis_request_issued"] is True
    assert receipt["planos_synthesis_scope_bounded"] is True
    assert receipt["planos_receives_request_not_selection_authority"] is True
    assert receipt["selection_authority_transferred_to_planos"] is False
    assert receipt["execution_authority_granted_to_planos"] is False
    assert receipt["plan_synthesis_performed"] is False
    assert receipt["concrete_plan_issued"] is False
    assert receipt["plan_receipt_issued"] is False
    assert receipt["persistent_world_state_unchanged"] is True
    assert receipt["active_now"] is False
    assert receipt["execution_permission"] is False
    assert receipt["synthesis_constraint_spec"]["maximum_plan_steps"] == 8
    assert receipt["retained_alternative_candidate_ids"] == [
        "hold",
        "reobserve",
        "repair",
    ]

    source = _source()
    spec = _spec(source)
    blocked = [
        _build(source_selection_receipt={}),
        _build(synthesis_policy_digest=""),
        _build(planos_recipient_digest=""),
        _build(request_owner_responsibility_digest=""),
        _build(synthesis_request_id=""),
        _build(requested_selected_candidate_id="repair"),
        _build(selected_candidate_plan_intent_digest=""),
        _build(synthesis_constraint_spec={}),
        _build(synthesis_constraint_digest="wrong"),
        _build(synthesis_handoff_bundle_digest="wrong"),
    ]

    for field, value in (
        ("planning_horizon_steps", 0),
        ("maximum_plan_steps", 20),
        ("maximum_branching_factor", 0),
        ("maximum_revision_cycles", -1),
        ("require_reversible_actions", False),
        ("require_checkpoint_before_irreversible_step", False),
        ("required_checkpoint_digests", []),
        ("stop_condition_digests", []),
    ):
        bad = deepcopy(spec)
        bad[field] = value
        blocked.append(_build(synthesis_constraint_spec=bad))

    bad_evidence = deepcopy(spec)
    bad_evidence["preserved_evidence_digests"] = sorted(
        set(bad_evidence["preserved_evidence_digests"])
        - {source["decisionos_selection_justification_receipt_digest"]}
    )
    blocked.append(_build(synthesis_constraint_spec=bad_evidence))

    bad_forbidden = deepcopy(spec)
    bad_forbidden["forbidden_effects"] = sorted(FORBIDDEN_EFFECTS - {"tool_invocation"})
    blocked.append(_build(synthesis_constraint_spec=bad_forbidden))

    noncanonical = deepcopy(spec)
    noncanonical["required_checkpoint_digests"] = list(
        reversed(noncanonical["required_checkpoint_digests"])
    )
    blocked.append(_build(synthesis_constraint_spec=noncanonical))

    tampered = _source()
    tampered["decisionos_selection_justification_receipt_digest"] = "wrong"
    blocked.append(_build(source_selection_receipt=tampered))

    promoted = _source()
    promoted["execution_permission"] = True
    promoted = _redigest_source(promoted)
    blocked.append(_build(source_selection_receipt=promoted))

    alternative_substitution = _source()
    alternative_substitution["retained_alternative_candidate_ids"].append("continue")
    alternative_substitution = _redigest_source(alternative_substitution)
    blocked.append(_build(source_selection_receipt=alternative_substitution))

    bad_source_bundle = _source()
    bad_source_bundle["selection_bundle_digest"] = "wrong"
    bad_source_bundle.pop("decisionos_selection_justification_receipt_digest")
    bad_source_bundle["decisionos_selection_justification_receipt_digest"] = (
        canonical_digest(bad_source_bundle)
    )
    blocked.append(_build(source_selection_receipt=bad_source_bundle))

    double_selected = _source()
    repair = next(
        item
        for item in double_selected["candidate_selection_justification_items"]
        if item["candidate_id"] == "repair"
    )
    repair["selected"] = True
    repair["support_rationale_digests"] = ["support-repair"]
    repair["nonselection_reason_digest"] = ""
    repair["candidate_selection_justification_digest"] = (
        compute_source_candidate_selection_justification_digest(repair)
    )
    double_selected = _redigest_source(double_selected)
    blocked.append(_build(source_selection_receipt=double_selected))

    for item in blocked:
        assert item.status != STATUS_READY
        assert item.blockers
        assert item.receipt is None

    print("PASS: DecisionOS Bounded Plan Synthesis Request Handoff v0.8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
