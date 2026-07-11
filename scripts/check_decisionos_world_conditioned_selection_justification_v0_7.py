#!/usr/bin/env python3
from copy import deepcopy

from runtime.kuuos_decisionos_world_conditioned_selection_justification_v0_7 import (
    STATUS_READY,
    build_decisionos_world_conditioned_selection_justification_receipt,
    canonical_digest,
    compute_candidate_selection_justification_digest,
    compute_selection_bundle_digest,
    compute_source_deliberation_record_digest,
)


def _record(
    candidate_id: str,
    *,
    admissible: bool,
    reviewable: bool,
    classification: str,
    dissent: bool = False,
    minority: bool = False,
    uncertainty: bool = False,
    evidence_blocked: bool = False,
) -> dict:
    return {
        "candidate_id": candidate_id,
        "source_candidate_intake_digest": f"intake-{candidate_id}",
        "candidate_deliberation_input_digest": f"deliberation-input-{candidate_id}",
        "source_admissible": admissible,
        "source_probability_mass": {
            "continue": 0.34,
            "repair": 0.26,
            "reobserve": 0.18,
            "hold": 0.22,
            "terminate_candidate": 0.0,
        }[candidate_id],
        "source_combined_transition_action": {
            "continue": 0.35,
            "repair": 0.42,
            "reobserve": 0.28,
            "hold": 0.10,
            "terminate_candidate": 1.20,
        }[candidate_id],
        "source_advisory_rank": {
            "continue": 1,
            "repair": 2,
            "hold": 3,
            "reobserve": 4,
            "terminate_candidate": 0,
        }[candidate_id],
        "wa_support": 0.80 if admissible else 0.20,
        "stakeholder_support": 0.78 if admissible else 0.20,
        "relational_support": 0.76 if admissible else 0.20,
        "dissent_pressure": 0.70 if dissent else 0.20,
        "minority_impact_risk": 0.75 if minority else 0.20,
        "uncertainty_burden": 0.70 if uncertainty else 0.20,
        "wa_gate_passed": admissible,
        "stakeholder_gate_passed": admissible,
        "relational_gate_passed": admissible,
        "dissent_review_required": dissent,
        "minority_protection_required": minority,
        "uncertainty_review_required": uncertainty,
        "evidence_blocked": evidence_blocked,
        "relationally_reviewable": reviewable,
        "deliberation_classification": classification,
        "review_blocker_digests": (
            ["missing-evidence"] if evidence_blocked else []
        ),
        "exclusion_review_digest": (
            "" if admissible else f"exclusion-{candidate_id}"
        ),
    }


def _source() -> dict:
    records = [
        _record(
            "continue",
            admissible=True,
            reviewable=True,
            classification="relationally_reviewable",
        ),
        _record(
            "repair",
            admissible=True,
            reviewable=True,
            classification="relationally_reviewable",
        ),
        _record(
            "reobserve",
            admissible=True,
            reviewable=False,
            classification="dissent_review_required",
            dissent=True,
        ),
        _record(
            "hold",
            admissible=True,
            reviewable=False,
            classification="minority_protection_required",
            minority=True,
        ),
        _record(
            "terminate_candidate",
            admissible=False,
            reviewable=False,
            classification="nonadmissible_retained",
        ),
    ]
    source = {
        "kernel": "DecisionOS WORLD-Conditioned Relational Deliberation Kernel",
        "kernel_version": "v0.1",
        "decisionos_version": "v0.6",
        "status": "DECISIONOS_WORLD_CONDITIONED_RELATIONAL_DELIBERATION_READY",
        "source_decisionos_version": "v0.5",
        "source_intake_receipt_digest": "intake-v05",
        "source_planos_handoff_certificate_digest": "planos-v102",
        "source_world_binding_digest": "world-binding-v14",
        "source_world_model_state_digest": "world-state-v14-r8",
        "source_world_model_revision": 8,
        "source_world_lineage_digest": "world-lineage-v14-r8",
        "source_handoff_disposition": "hold_guarded_review",
        "source_decision_review_ready": True,
        "deliberation_policy_digest": "relational-policy-v06",
        "threshold_config": {
            "minimum_wa_support": 0.50,
            "minimum_stakeholder_support": 0.50,
            "minimum_relational_support": 0.50,
            "maximum_dissent_pressure_before_review": 0.50,
            "maximum_minority_impact_risk": 0.50,
            "maximum_uncertainty_burden": 0.50,
            "dominance_tolerance": 1e-10,
        },
        "candidate_deliberation_inputs": [],
        "deliberation_bundle_digest": "deliberation-bundle-v06",
        "candidate_deliberation_records": records,
        "all_candidate_ids": [
            "continue",
            "repair",
            "reobserve",
            "hold",
            "terminate_candidate",
        ],
        "admissible_candidate_ids": [
            "continue",
            "repair",
            "reobserve",
            "hold",
        ],
        "retained_nonadmissible_candidate_ids": [
            "terminate_candidate"
        ],
        "relationally_reviewable_candidate_ids": [
            "continue",
            "repair",
        ],
        "relational_frontier_candidate_ids": [
            "continue",
            "repair",
        ],
        "dissent_review_candidate_ids": ["reobserve"],
        "minority_protection_candidate_ids": ["hold"],
        "uncertainty_review_candidate_ids": [],
        "evidence_blocked_candidate_ids": [],
        "required_review_candidate_ids": [
            "continue",
            "repair",
            "reobserve",
            "hold",
        ],
        "dominates_map": {"continue": [], "repair": []},
        "dominated_by_map": {"continue": [], "repair": []},
        "hold_guard_active": True,
        "deliberation_disposition": "minority_protection_review",
        "source_probability_used_as_advisory_only": True,
        "source_action_used_as_advisory_only": True,
        "relational_partial_order_used": True,
        "single_scalar_utility_selection_forbidden": True,
        "all_candidates_considered": True,
        "candidate_identity_preserved": True,
        "retained_alternatives_preserved": True,
        "wa_evidence_preserved": True,
        "stakeholder_context_preserved": True,
        "relational_context_preserved": True,
        "dissent_visibility_preserved": True,
        "minority_visibility_preserved": True,
        "silent_substitution_detected": False,
        "relational_deliberation_performed": True,
        "decisionos_owns_selection": True,
        "selection_authority_granted_by_deliberation": False,
        "decision_selection_performed": False,
        "selected_candidate_id": "",
        "decision_receipt_issued": False,
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
    source["decisionos_relational_deliberation_receipt_digest"] = (
        canonical_digest(source)
    )
    return source


def _item(
    source: dict,
    candidate_id: str,
    *,
    selected: bool = False,
) -> dict:
    record_map = {
        record["candidate_id"]: record
        for record in source["candidate_deliberation_records"]
    }
    item = {
        "candidate_id": candidate_id,
        "source_deliberation_record_digest": (
            compute_source_deliberation_record_digest(
                record_map[candidate_id]
            )
        ),
        "selected": selected,
        "support_rationale_digests": (
            [f"support-{candidate_id}"] if selected else []
        ),
        "opposition_rationale_digests": (
            [] if selected else [f"opposition-{candidate_id}"]
        ),
        "dissent_preservation_digests": (
            [f"dissent-preserved-{candidate_id}"]
            if candidate_id == "reobserve"
            else []
        ),
        "minority_preservation_digests": (
            [f"minority-preserved-{candidate_id}"]
            if candidate_id == "hold"
            else []
        ),
        "review_resolution_digests": (
            [f"review-resolution-{candidate_id}"]
            if candidate_id in {"reobserve", "hold"}
            else []
        ),
        "nonselection_reason_digest": (
            "" if selected else f"nonselection-{candidate_id}"
        ),
        "candidate_selection_justification_digest": "",
    }
    item["candidate_selection_justification_digest"] = (
        compute_candidate_selection_justification_digest(item)
    )
    return item


def _build(**overrides):
    source = overrides.pop("source_deliberation_receipt", _source())
    selected = overrides.pop(
        "requested_selected_candidate_id", "continue"
    )
    items = overrides.pop(
        "candidate_selection_justification_items",
        [
            _item(
                source,
                candidate_id,
                selected=(candidate_id == selected),
            )
            for candidate_id in source.get("all_candidate_ids", [])
        ],
    )
    policy = overrides.pop(
        "selection_policy_digest", "selection-policy-v07"
    )
    responsibility = overrides.pop(
        "selector_responsibility_digest",
        "decision-owner-v07",
    )
    hold_resolution = overrides.pop(
        "hold_guard_resolution_digest",
        "hold-guard-reviewed-v07",
    )
    source_digest = source.get(
        "decisionos_relational_deliberation_receipt_digest",
        "",
    )
    bundle = overrides.pop(
        "selection_bundle_digest",
        compute_selection_bundle_digest(
            source_deliberation_receipt_digest=source_digest,
            selection_policy_digest=policy,
            selector_responsibility_digest=responsibility,
            requested_selected_candidate_id=selected,
            hold_guard_resolution_digest=hold_resolution,
            candidate_selection_justification_items=items,
        ),
    )
    args = {
        "source_deliberation_receipt": source,
        "selection_policy_digest": policy,
        "selector_responsibility_digest": responsibility,
        "requested_selected_candidate_id": selected,
        "hold_guard_resolution_digest": hold_resolution,
        "candidate_selection_justification_items": items,
        "selection_bundle_digest": bundle,
    }
    args.update(overrides)
    return build_decisionos_world_conditioned_selection_justification_receipt(
        **args
    )


def _redigest(item: dict) -> dict:
    value = deepcopy(item)
    value["candidate_selection_justification_digest"] = (
        compute_candidate_selection_justification_digest(value)
    )
    return value


def main() -> int:
    result = _build()
    assert result.status == STATUS_READY
    assert result.receipt is not None
    receipt = result.receipt
    assert receipt["selected_candidate_id"] == "continue"
    assert receipt["decision_selection_performed"] is True
    assert receipt["decision_receipt_issued"] is True
    assert receipt["selection_authority_exercised_by_decision_os"] is True
    assert receipt["selection_authority_inherited_from_planos"] is False
    assert receipt["selection_authority_inherited_from_world_model"] is False
    assert receipt["selection_authority_inherited_from_qi"] is False
    assert receipt["selected_candidate_from_relational_frontier"] is True
    assert receipt["retained_alternative_candidate_ids"] == [
        "hold",
        "reobserve",
        "repair",
    ]
    assert receipt["retained_nonadmissible_candidate_ids"] == [
        "terminate_candidate"
    ]
    assert receipt["dissent_preservation_map"]["reobserve"]
    assert receipt["minority_preservation_map"]["hold"]
    assert receipt["selection_is_not_plan_synthesis"] is True
    assert receipt["selection_is_not_execution"] is True
    assert receipt["plan_synthesis_performed"] is False
    assert receipt["active_now"] is False
    assert receipt["execution_permission"] is False
    assert receipt["persistent_world_state_unchanged"] is True

    source = _source()
    items = [
        _item(
            source,
            candidate_id,
            selected=(candidate_id == "continue"),
        )
        for candidate_id in source["all_candidate_ids"]
    ]

    bad_support = deepcopy(items)
    bad_support[0]["support_rationale_digests"] = []
    bad_support[0] = _redigest(bad_support[0])

    bad_reason = deepcopy(items)
    repair_index = next(
        index
        for index, item in enumerate(bad_reason)
        if item["candidate_id"] == "repair"
    )
    bad_reason[repair_index]["nonselection_reason_digest"] = ""
    bad_reason[repair_index] = _redigest(bad_reason[repair_index])

    bad_dissent = deepcopy(items)
    reobserve_index = next(
        index
        for index, item in enumerate(bad_dissent)
        if item["candidate_id"] == "reobserve"
    )
    bad_dissent[reobserve_index]["dissent_preservation_digests"] = []
    bad_dissent[reobserve_index] = _redigest(
        bad_dissent[reobserve_index]
    )

    bad_minority = deepcopy(items)
    hold_index = next(
        index
        for index, item in enumerate(bad_minority)
        if item["candidate_id"] == "hold"
    )
    bad_minority[hold_index]["minority_preservation_digests"] = []
    bad_minority[hold_index] = _redigest(bad_minority[hold_index])

    bad_record = deepcopy(items)
    bad_record[0]["source_deliberation_record_digest"] = "wrong"
    bad_record[0] = _redigest(bad_record[0])

    double_selected = deepcopy(items)
    double_selected[repair_index]["selected"] = True
    double_selected[repair_index]["support_rationale_digests"] = [
        "support-repair"
    ]
    double_selected[repair_index]["nonselection_reason_digest"] = ""
    double_selected[repair_index] = _redigest(
        double_selected[repair_index]
    )

    wrong_digest = deepcopy(items)
    wrong_digest[0]["candidate_selection_justification_digest"] = "wrong"

    blocked = [
        _build(source_deliberation_receipt={}),
        _build(selection_policy_digest=""),
        _build(selector_responsibility_digest=""),
        _build(requested_selected_candidate_id="reobserve"),
        _build(requested_selected_candidate_id="terminate_candidate"),
        _build(hold_guard_resolution_digest=""),
        _build(candidate_selection_justification_items=[]),
        _build(candidate_selection_justification_items=bad_support),
        _build(candidate_selection_justification_items=bad_reason),
        _build(candidate_selection_justification_items=bad_dissent),
        _build(candidate_selection_justification_items=bad_minority),
        _build(candidate_selection_justification_items=bad_record),
        _build(candidate_selection_justification_items=double_selected),
        _build(candidate_selection_justification_items=wrong_digest),
        _build(selection_bundle_digest="wrong"),
    ]

    tampered_source = _source()
    tampered_source["relational_frontier_candidate_ids"] = ["repair"]
    blocked.append(
        _build(source_deliberation_receipt=tampered_source)
    )

    incomplete = deepcopy(items[:-1])
    blocked.append(
        _build(candidate_selection_justification_items=incomplete)
    )

    duplicate = deepcopy(items)
    duplicate[-1] = deepcopy(duplicate[0])
    duplicate[-1] = _redigest(duplicate[-1])
    blocked.append(
        _build(candidate_selection_justification_items=duplicate)
    )

    for item in blocked:
        assert item.status != STATUS_READY
        assert item.blockers
        assert item.receipt is None

    print(
        "PASS: DecisionOS WORLD-Conditioned Selection "
        "Justification v0.7"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
