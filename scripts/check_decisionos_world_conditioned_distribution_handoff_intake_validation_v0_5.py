#!/usr/bin/env python3
from copy import deepcopy

from runtime.kuuos_planos_world_conditioned_distribution_decision_handoff_certificate_kernel_v0_1 import (
    STATUS_READY as SOURCE_READY,
    build_world_conditioned_distribution_decision_handoff_certificate,
    canonical_digest as source_digest,
)
from runtime.kuuos_decisionos_world_conditioned_distribution_handoff_intake_validation_v0_5 import (
    STATUS_READY,
    build_decisionos_world_conditioned_distribution_handoff_intake_receipt,
    canonical_digest,
    compute_candidate_intake_digest,
    compute_evidence_bundle_digest,
)


def source_certificate() -> dict:
    projections = {
        "continue": "projection-continue",
        "reobserve": "projection-reobserve",
        "hold": "projection-hold",
        "terminate_candidate": "projection-terminate",
    }
    actions = {
        "continue": 0.70,
        "reobserve": 0.35,
        "hold": 0.10,
        "terminate_candidate": 1.40,
    }
    distribution = {
        "continue": 0.40,
        "reobserve": 0.35,
        "hold": 0.25,
        "terminate_candidate": 0.00,
    }
    result = build_world_conditioned_distribution_decision_handoff_certificate(
        source_distribution_update_digest="planos-v101-distribution-update",
        source_next_distribution_digest=source_digest(distribution),
        source_world_conditioned_action_bundle_digest="world-action-bundle-v100",
        source_world_binding_digest="world-binding-v14-rev7",
        source_world_model_state_digest="world-state-v14-rev7",
        source_world_model_revision=7,
        source_world_lineage_digest="world-lineage-v14-rev7",
        candidate_world_projection_digests=projections,
        combined_transition_action_map=actions,
        next_distribution=distribution,
        admissible_candidate_ids=["continue", "reobserve", "hold"],
        minimum_lead_margin=0.03,
        maximum_normalized_entropy=1.0,
        hold_review_threshold=0.30,
    )
    assert result.status == SOURCE_READY
    assert result.certificate is not None
    return result.certificate


def evidence_items(source: dict) -> list[dict]:
    rank_map = {
        record["candidate_id"]: record["rank"]
        for record in source["ranking_records"]
    }
    admissible = set(source["admissible_candidate_ids"])
    items: list[dict] = []
    for candidate_id in sorted(source["candidate_world_projection_digests"]):
        is_admissible = candidate_id in admissible
        item = {
            "candidate_id": candidate_id,
            "candidate_world_projection_digest": (
                source["candidate_world_projection_digests"][candidate_id]
            ),
            "probability_mass": source["next_distribution"][candidate_id],
            "combined_transition_action": (
                source["combined_transition_action_map"][candidate_id]
            ),
            "advisory_rank": rank_map.get(candidate_id, 0),
            "admissible": is_admissible,
            "wa_evidence_digests": (
                [f"wa-evidence-{candidate_id}"] if is_admissible else []
            ),
            "stakeholder_evidence_digests": (
                [f"stakeholder-evidence-{candidate_id}"]
                if is_admissible
                else []
            ),
            "relational_evidence_digests": (
                [f"relational-evidence-{candidate_id}"]
                if is_admissible
                else []
            ),
            "dissent_evidence_digests": (
                ["dissent-evidence-continue"]
                if candidate_id == "continue"
                else []
            ),
            "dissent_absence_attested": candidate_id != "continue",
            "minority_evidence_digests": (
                ["minority-evidence-hold"] if candidate_id == "hold" else []
            ),
            "minority_absence_attested": candidate_id != "hold",
            "zero_mass_reason_digest": (
                "" if is_admissible else "constraint-exclusion-reason"
            ),
            "candidate_intake_digest": "",
        }
        item["candidate_intake_digest"] = compute_candidate_intake_digest(item)
        items.append(item)
    return items


def resign_source(source: dict) -> dict:
    value = deepcopy(source)
    value.pop("decision_handoff_certificate_digest", None)
    value["decision_handoff_certificate_digest"] = canonical_digest(value)
    return value


def build(**overrides):
    source = overrides.pop("source_handoff_certificate", source_certificate())
    items = overrides.pop("candidate_evidence_items", evidence_items(source))
    contexts = {
        "stakeholder_context_digest": "stakeholder-context-v1",
        "relational_context_digest": "relational-context-v1",
        "wa_context_digest": "wa-context-v1",
        "dissent_registry_digest": "dissent-registry-v1",
        "minority_registry_digest": "minority-registry-v1",
    }
    contexts.update(
        {
            key: overrides.pop(key)
            for key in list(contexts)
            if key in overrides
        }
    )
    evidence_bundle_digest = overrides.pop(
        "evidence_bundle_digest",
        compute_evidence_bundle_digest(
            **contexts,
            candidate_evidence_items=items,
        ),
    )
    assert not overrides
    return build_decisionos_world_conditioned_distribution_handoff_intake_receipt(
        source_handoff_certificate=source,
        candidate_evidence_items=items,
        evidence_bundle_digest=evidence_bundle_digest,
        **contexts,
    )


def replace_item(items: list[dict], candidate_id: str, **changes) -> list[dict]:
    values = deepcopy(items)
    for item in values:
        if item["candidate_id"] == candidate_id:
            item.update(changes)
            item["candidate_intake_digest"] = compute_candidate_intake_digest(item)
            return values
    raise AssertionError(candidate_id)


def main() -> int:
    result = build()
    assert result.status == STATUS_READY
    assert result.receipt is not None
    receipt = result.receipt
    assert receipt["status"] == "DECISIONOS_WORLD_CONDITIONED_HANDOFF_INTAKE_READY"
    for name in (
        "intake_owned_by_decision_os",
        "source_owned_by_plan_os",
        "deliberation_intake_ready",
        "all_candidates_considered",
        "candidate_identity_preserved",
        "retained_alternatives_preserved",
        "wa_evidence_preserved",
        "stakeholder_context_preserved",
        "relational_context_preserved",
        "dissent_visibility_preserved",
        "minority_visibility_preserved",
        "ranking_is_advisory_only",
        "decisionos_owns_selection",
        "persistent_world_state_unchanged",
        "world_model_prediction_not_truth",
        "world_mutation_not_granted",
        "history_read_only",
        "qi_grants_no_authority",
    ):
        assert receipt[name] is True
    for name in (
        "silent_substitution_detected",
        "selection_authority_granted_by_intake",
        "decision_selection_performed",
        "decision_receipt_issued",
        "plan_synthesis_performed",
        "active_now",
        "execution_permission",
    ):
        assert receipt[name] is False
    assert receipt["selected_candidate_id"] == ""
    assert set(receipt["all_candidate_ids"]) == {
        "continue",
        "reobserve",
        "hold",
        "terminate_candidate",
    }
    assert receipt["retained_nonadmissible_candidate_ids"] == [
        "terminate_candidate"
    ]
    assert receipt["dissent_present_candidate_ids"] == ["continue"]
    assert receipt["minority_present_candidate_ids"] == ["hold"]

    source = source_certificate()
    bad_source_digest = deepcopy(source)
    bad_source_digest["decision_handoff_certificate_digest"] = "wrong"

    promoted_selection = deepcopy(source)
    promoted_selection["decision_selection_performed"] = True
    promoted_selection = resign_source(promoted_selection)

    selected_candidate = deepcopy(source)
    selected_candidate["selected_candidate_id"] = "continue"
    selected_candidate = resign_source(selected_candidate)

    bad_ranking = deepcopy(source)
    bad_ranking["ranked_candidate_ids"] = list(
        reversed(bad_ranking["ranked_candidate_ids"])
    )
    bad_ranking = resign_source(bad_ranking)

    base_items = evidence_items(source)
    duplicate_items = base_items + [deepcopy(base_items[0])]
    missing_items = base_items[:-1]
    wrong_projection = replace_item(
        base_items,
        "continue",
        candidate_world_projection_digest="wrong",
    )
    wrong_mass = replace_item(
        base_items,
        "continue",
        probability_mass=0.39,
    )
    wrong_rank = replace_item(
        base_items,
        "continue",
        advisory_rank=2,
    )
    missing_wa = replace_item(
        base_items,
        "continue",
        wa_evidence_digests=[],
    )
    dissent_unattested = replace_item(
        base_items,
        "reobserve",
        dissent_absence_attested=False,
    )
    minority_conflict = replace_item(
        base_items,
        "hold",
        minority_absence_attested=True,
    )
    missing_zero_reason = replace_item(
        base_items,
        "terminate_candidate",
        zero_mass_reason_digest="",
    )

    blocked = [
        build(source_handoff_certificate={}),
        build(source_handoff_certificate=bad_source_digest),
        build(source_handoff_certificate=promoted_selection),
        build(source_handoff_certificate=selected_candidate),
        build(source_handoff_certificate=bad_ranking),
        build(stakeholder_context_digest=""),
        build(evidence_bundle_digest="wrong"),
        build(candidate_evidence_items=duplicate_items),
        build(candidate_evidence_items=missing_items),
        build(candidate_evidence_items=wrong_projection),
        build(candidate_evidence_items=wrong_mass),
        build(candidate_evidence_items=wrong_rank),
        build(candidate_evidence_items=missing_wa),
        build(candidate_evidence_items=dissent_unattested),
        build(candidate_evidence_items=minority_conflict),
        build(candidate_evidence_items=missing_zero_reason),
    ]
    for item in blocked:
        assert item.status != STATUS_READY
        assert item.blockers
        assert item.receipt is None

    print(
        "PASS: DecisionOS WORLD-Conditioned Distribution Handoff Intake "
        "Validation v0.5"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
