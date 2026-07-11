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
    assert result.status == SOURCE_READY and result.certificate is not None
    return result.certificate


def evidence_items(source: dict) -> list[dict]:
    rank_map = {
        record["candidate_id"]: record["rank"]
        for record in source["ranking_records"]
    }
    admissible = set(source["admissible_candidate_ids"])
    values: list[dict] = []
    for candidate_id in sorted(source["candidate_world_projection_digests"]):
        is_admissible = candidate_id in admissible
        item = {
            "candidate_id": candidate_id,
            "candidate_world_projection_digest": source[
                "candidate_world_projection_digests"
            ][candidate_id],
            "probability_mass": source["next_distribution"][candidate_id],
            "combined_transition_action": source[
                "combined_transition_action_map"
            ][candidate_id],
            "advisory_rank": rank_map.get(candidate_id, 0),
            "admissible": is_admissible,
            "wa_evidence_digests": [f"wa-{candidate_id}"] if is_admissible else [],
            "stakeholder_evidence_digests": (
                [f"stakeholder-{candidate_id}"] if is_admissible else []
            ),
            "relational_evidence_digests": (
                [f"relational-{candidate_id}"] if is_admissible else []
            ),
            "dissent_evidence_digests": (
                ["dissent-continue"] if candidate_id == "continue" else []
            ),
            "dissent_absence_attested": candidate_id != "continue",
            "minority_evidence_digests": (
                ["minority-hold"] if candidate_id == "hold" else []
            ),
            "minority_absence_attested": candidate_id != "hold",
            "zero_mass_reason_digest": (
                "" if is_admissible else "constraint-exclusion-reason"
            ),
            "candidate_intake_digest": "",
        }
        item["candidate_intake_digest"] = compute_candidate_intake_digest(item)
        values.append(item)
    return values


def resign(source: dict) -> dict:
    value = deepcopy(source)
    value.pop("decision_handoff_certificate_digest", None)
    value["decision_handoff_certificate_digest"] = canonical_digest(value)
    return value


def build(**overrides):
    source = overrides.pop("source_handoff_certificate", None)
    if source is None:
        source = source_certificate()
    items = overrides.pop("candidate_evidence_items", None)
    if items is None:
        items = evidence_items(source) if source else []
    contexts = {
        "stakeholder_context_digest": "stakeholder-context-v1",
        "relational_context_digest": "relational-context-v1",
        "wa_context_digest": "wa-context-v1",
        "dissent_registry_digest": "dissent-registry-v1",
        "minority_registry_digest": "minority-registry-v1",
    }
    for key in tuple(contexts):
        if key in overrides:
            contexts[key] = overrides.pop(key)
    bundle = overrides.pop("evidence_bundle_digest", None)
    if bundle is None:
        bundle = compute_evidence_bundle_digest(
            **contexts,
            candidate_evidence_items=items,
        )
    assert not overrides
    return build_decisionos_world_conditioned_distribution_handoff_intake_receipt(
        source_handoff_certificate=source,
        candidate_evidence_items=items,
        evidence_bundle_digest=bundle,
        **contexts,
    )


def changed_item(items: list[dict], candidate_id: str, **changes) -> list[dict]:
    result = deepcopy(items)
    item = next(item for item in result if item["candidate_id"] == candidate_id)
    item.update(changes)
    item["candidate_intake_digest"] = compute_candidate_intake_digest(item)
    return result


def main() -> int:
    result = build()
    assert result.status == STATUS_READY and result.receipt is not None
    receipt = result.receipt
    assert receipt["status"] == "DECISIONOS_WORLD_CONDITIONED_HANDOFF_INTAKE_READY"
    assert receipt["all_candidates_considered"] is True
    assert receipt["retained_alternatives_preserved"] is True
    assert receipt["dissent_visibility_preserved"] is True
    assert receipt["minority_visibility_preserved"] is True
    assert receipt["ranking_is_advisory_only"] is True
    assert receipt["selection_authority_granted_by_intake"] is False
    assert receipt["decision_selection_performed"] is False
    assert receipt["selected_candidate_id"] == ""
    assert receipt["decision_receipt_issued"] is False
    assert receipt["persistent_world_state_unchanged"] is True
    assert receipt["execution_permission"] is False
    assert receipt["retained_nonadmissible_candidate_ids"] == [
        "terminate_candidate"
    ]
    assert receipt["dissent_present_candidate_ids"] == ["continue"]
    assert receipt["minority_present_candidate_ids"] == ["hold"]

    source = source_certificate()
    items = evidence_items(source)

    bad_digest = deepcopy(source)
    bad_digest["decision_handoff_certificate_digest"] = "wrong"
    promoted = deepcopy(source)
    promoted["decision_selection_performed"] = True
    promoted = resign(promoted)
    selected = deepcopy(source)
    selected["selected_candidate_id"] = "continue"
    selected = resign(selected)
    bad_ranking = deepcopy(source)
    bad_ranking["ranked_candidate_ids"] = list(
        reversed(bad_ranking["ranked_candidate_ids"])
    )
    bad_ranking = resign(bad_ranking)

    blocked = [
        build(source_handoff_certificate={}),
        build(source_handoff_certificate=bad_digest),
        build(source_handoff_certificate=promoted),
        build(source_handoff_certificate=selected),
        build(source_handoff_certificate=bad_ranking),
        build(stakeholder_context_digest=""),
        build(evidence_bundle_digest="wrong"),
        build(candidate_evidence_items=items[:-1]),
        build(
            candidate_evidence_items=changed_item(
                items, "continue", wa_evidence_digests=[]
            )
        ),
        build(
            candidate_evidence_items=changed_item(
                items, "reobserve", dissent_absence_attested=False
            )
        ),
        build(
            candidate_evidence_items=changed_item(
                items, "hold", minority_absence_attested=True
            )
        ),
        build(
            candidate_evidence_items=changed_item(
                items, "terminate_candidate", zero_mass_reason_digest=""
            )
        ),
    ]
    for value in blocked:
        assert value.status != STATUS_READY
        assert value.blockers and value.receipt is None

    print(
        "PASS: DecisionOS WORLD-Conditioned Distribution Handoff Intake "
        "Validation v0.5"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
