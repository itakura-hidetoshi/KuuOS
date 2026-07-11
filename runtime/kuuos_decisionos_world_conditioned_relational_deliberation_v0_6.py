#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import math
from typing import Any, Mapping

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
TOL = 1e-10
SOURCE_DECISIONOS_VERSION = "v0.5"
SOURCE_STATUS = "DECISIONOS_WORLD_CONDITIONED_HANDOFF_INTAKE_READY"
CANDIDATE_FIELD = {
    "continue",
    "strengthen",
    "repair",
    "slow_down",
    "reobserve",
    "reroute",
    "hold",
    "terminate_candidate",
}


@dataclass
class DecisionOSWorldConditionedRelationalDeliberationResult:
    status: str
    blockers: list[str]
    receipt: dict | None


def canonical_digest(value: Any) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    return sha256(encoded).hexdigest()


def finite(value: Any) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(float(value))
    )


def close(left: float, right: float) -> bool:
    return math.isclose(left, right, rel_tol=0.0, abs_tol=TOL)


def _string_list(value: Any) -> tuple[bool, list[str]]:
    if not isinstance(value, list):
        return False, []
    if any(not isinstance(item, str) or not item for item in value):
        return False, []
    if len(value) != len(set(value)):
        return False, []
    return True, list(value)


def compute_source_candidate_intake_digest(item: Mapping[str, Any]) -> str:
    payload = dict(item)
    payload.pop("candidate_intake_digest", None)
    return canonical_digest(payload)


def compute_source_evidence_bundle_digest(source: Mapping[str, Any]) -> str:
    items = source.get("candidate_evidence_items", [])
    ordered = sorted(items, key=lambda item: str(item.get("candidate_id", "")))
    return canonical_digest(
        {
            "stakeholder_context_digest": source.get("stakeholder_context_digest", ""),
            "relational_context_digest": source.get("relational_context_digest", ""),
            "wa_context_digest": source.get("wa_context_digest", ""),
            "dissent_registry_digest": source.get("dissent_registry_digest", ""),
            "minority_registry_digest": source.get("minority_registry_digest", ""),
            "candidate_evidence_items": ordered,
        }
    )


def compute_candidate_deliberation_input_digest(item: Mapping[str, Any]) -> str:
    payload = dict(item)
    payload.pop("candidate_deliberation_input_digest", None)
    return canonical_digest(payload)


def compute_deliberation_bundle_digest(
    *,
    source_intake_receipt_digest: str,
    deliberation_policy_digest: str,
    threshold_config: Mapping[str, float],
    candidate_deliberation_inputs: list[dict],
) -> str:
    ordered = sorted(
        candidate_deliberation_inputs,
        key=lambda item: str(item.get("candidate_id", "")),
    )
    return canonical_digest(
        {
            "source_intake_receipt_digest": source_intake_receipt_digest,
            "deliberation_policy_digest": deliberation_policy_digest,
            "threshold_config": dict(sorted(threshold_config.items())),
            "candidate_deliberation_inputs": ordered,
        }
    )


def _dominates(left: Mapping[str, Any], right: Mapping[str, Any], tolerance: float) -> bool:
    positive = ("wa_support", "stakeholder_support", "relational_support")
    burdens = ("dissent_pressure", "minority_impact_risk", "uncertainty_burden")
    weak = all(float(left[name]) + tolerance >= float(right[name]) for name in positive)
    weak = weak and all(float(left[name]) <= float(right[name]) + tolerance for name in burdens)
    strict = any(float(left[name]) > float(right[name]) + tolerance for name in positive)
    strict = strict or any(float(left[name]) + tolerance < float(right[name]) for name in burdens)
    return weak and strict


def build_decisionos_world_conditioned_relational_deliberation_receipt(
    *,
    source_intake_receipt: Mapping[str, Any],
    deliberation_policy_digest: str,
    candidate_deliberation_inputs: list[dict],
    deliberation_bundle_digest: str,
    minimum_wa_support: float,
    minimum_stakeholder_support: float,
    minimum_relational_support: float,
    maximum_dissent_pressure_before_review: float,
    maximum_minority_impact_risk: float,
    maximum_uncertainty_burden: float,
    dominance_tolerance: float,
) -> DecisionOSWorldConditionedRelationalDeliberationResult:
    blockers: list[str] = []
    source = dict(source_intake_receipt) if isinstance(source_intake_receipt, Mapping) else {}
    if not source:
        blockers.append("source_intake_receipt_missing")

    if not isinstance(deliberation_policy_digest, str) or not deliberation_policy_digest:
        blockers.append("deliberation_policy_digest_missing")
    if not isinstance(deliberation_bundle_digest, str) or not deliberation_bundle_digest:
        blockers.append("deliberation_bundle_digest_missing")

    threshold_config = {
        "minimum_wa_support": minimum_wa_support,
        "minimum_stakeholder_support": minimum_stakeholder_support,
        "minimum_relational_support": minimum_relational_support,
        "maximum_dissent_pressure_before_review": maximum_dissent_pressure_before_review,
        "maximum_minority_impact_risk": maximum_minority_impact_risk,
        "maximum_uncertainty_burden": maximum_uncertainty_burden,
        "dominance_tolerance": dominance_tolerance,
    }
    for name, value in threshold_config.items():
        if not finite(value) or not 0.0 <= float(value) <= 1.0:
            blockers.append(f"invalid_{name}")

    source_candidate_ids: set[str] = set()
    source_admissible_ids: set[str] = set()
    source_evidence_map: dict[str, dict] = {}
    distribution: dict[str, float] = {}
    actions: dict[str, float] = {}
    advisory_rank_map: dict[str, int] = {}

    if source:
        if source.get("decisionos_version") != SOURCE_DECISIONOS_VERSION:
            blockers.append("source_decisionos_version_invalid")
        if source.get("status") != SOURCE_STATUS:
            blockers.append("source_intake_not_ready")
        source_digest = source.get("decisionos_intake_receipt_digest")
        if not isinstance(source_digest, str) or not source_digest:
            blockers.append("source_intake_receipt_digest_missing")
        else:
            unsigned = dict(source)
            unsigned.pop("decisionos_intake_receipt_digest", None)
            if source_digest != canonical_digest(unsigned):
                blockers.append("source_intake_receipt_digest_mismatch")

        required_true = (
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
        )
        required_false = (
            "silent_substitution_detected",
            "selection_authority_granted_by_intake",
            "decision_selection_performed",
            "decision_receipt_issued",
            "plan_synthesis_performed",
            "active_now",
            "execution_permission",
        )
        for name in required_true:
            if source.get(name) is not True:
                blockers.append(f"source_boundary_{name}_missing")
        for name in required_false:
            if source.get(name) is not False:
                blockers.append(f"source_boundary_{name}_promoted")
        if source.get("selected_candidate_id") != "":
            blockers.append("source_selected_candidate_forbidden")

        for name in (
            "source_handoff_certificate_digest",
            "source_world_binding_digest",
            "source_world_model_state_digest",
            "source_world_lineage_digest",
            "stakeholder_context_digest",
            "relational_context_digest",
            "wa_context_digest",
            "dissent_registry_digest",
            "minority_registry_digest",
            "evidence_bundle_digest",
        ):
            if not isinstance(source.get(name), str) or not source.get(name):
                blockers.append(f"source_{name}_missing")
        revision = source.get("source_world_model_revision")
        if not isinstance(revision, int) or isinstance(revision, bool) or revision < 0:
            blockers.append("source_world_model_revision_invalid")

        all_ids = source.get("all_candidate_ids")
        admissible_ids = source.get("admissible_candidate_ids")
        retained_nonadmissible_ids = source.get("retained_nonadmissible_candidate_ids")
        if (
            not isinstance(all_ids, list)
            or not all_ids
            or len(all_ids) != len(set(all_ids))
            or any(not isinstance(item, str) or item not in CANDIDATE_FIELD for item in all_ids)
        ):
            blockers.append("source_all_candidate_ids_invalid")
        else:
            source_candidate_ids = set(all_ids)
        if (
            not isinstance(admissible_ids, list)
            or not admissible_ids
            or len(admissible_ids) != len(set(admissible_ids))
            or any(item not in source_candidate_ids for item in admissible_ids)
        ):
            blockers.append("source_admissible_candidate_ids_invalid")
        else:
            source_admissible_ids = set(admissible_ids)
        if (
            not isinstance(retained_nonadmissible_ids, list)
            or set(retained_nonadmissible_ids) != source_candidate_ids - source_admissible_ids
        ):
            blockers.append("source_retained_nonadmissible_ids_mismatch")

        projections = source.get("candidate_world_projection_digests")
        raw_distribution = source.get("next_distribution")
        raw_actions = source.get("combined_transition_action_map")
        if not isinstance(projections, dict) or set(projections) != source_candidate_ids:
            blockers.append("source_projection_candidate_set_mismatch")
        elif any(not isinstance(value, str) or not value for value in projections.values()):
            blockers.append("source_projection_digest_invalid")
        if not isinstance(raw_distribution, dict) or set(raw_distribution) != source_candidate_ids:
            blockers.append("source_distribution_candidate_set_mismatch")
        else:
            total = 0.0
            for candidate_id, value in raw_distribution.items():
                if not finite(value) or float(value) < 0.0:
                    blockers.append(f"source_distribution_mass_invalid_{candidate_id}")
                else:
                    distribution[candidate_id] = float(value)
                    total += float(value)
            if not close(total, 1.0):
                blockers.append("source_distribution_not_normalized")
        if not isinstance(raw_actions, dict) or set(raw_actions) != source_candidate_ids:
            blockers.append("source_action_candidate_set_mismatch")
        else:
            for candidate_id, value in raw_actions.items():
                if not finite(value) or float(value) < 0.0:
                    blockers.append(f"source_action_invalid_{candidate_id}")
                else:
                    actions[candidate_id] = float(value)

        source_items = source.get("candidate_evidence_items")
        if not isinstance(source_items, list) or len(source_items) != len(source_candidate_ids):
            blockers.append("source_candidate_evidence_items_incomplete")
        else:
            for index, raw_item in enumerate(source_items):
                if not isinstance(raw_item, dict):
                    blockers.append(f"source_candidate_evidence_item_invalid_{index}")
                    continue
                candidate_id = raw_item.get("candidate_id")
                if not isinstance(candidate_id, str) or candidate_id not in source_candidate_ids:
                    blockers.append(f"source_candidate_evidence_id_invalid_{index}")
                    continue
                if candidate_id in source_evidence_map:
                    blockers.append("source_candidate_evidence_id_duplicate")
                item = dict(raw_item)
                source_evidence_map[candidate_id] = item
                if item.get("candidate_intake_digest") != compute_source_candidate_intake_digest(item):
                    blockers.append(f"source_candidate_intake_digest_mismatch_{candidate_id}")
                if item.get("admissible") is not (candidate_id in source_admissible_ids):
                    blockers.append(f"source_candidate_admissibility_mismatch_{candidate_id}")
                if candidate_id in distribution and (
                    not finite(item.get("probability_mass"))
                    or not close(float(item["probability_mass"]), distribution[candidate_id])
                ):
                    blockers.append(f"source_candidate_probability_mismatch_{candidate_id}")
                if candidate_id in actions and (
                    not finite(item.get("combined_transition_action"))
                    or not close(float(item["combined_transition_action"]), actions[candidate_id])
                ):
                    blockers.append(f"source_candidate_action_mismatch_{candidate_id}")
            if set(source_evidence_map) != source_candidate_ids:
                blockers.append("source_candidate_evidence_field_not_complete")

        if source.get("evidence_bundle_digest") != compute_source_evidence_bundle_digest(source):
            blockers.append("source_evidence_bundle_digest_mismatch")

        ranking_records = source.get("advisory_ranking_records")
        if not isinstance(ranking_records, list):
            blockers.append("source_advisory_ranking_records_invalid")
        else:
            seen_ranks: set[int] = set()
            seen_ranked_ids: set[str] = set()
            for record in ranking_records:
                if not isinstance(record, dict):
                    blockers.append("source_advisory_ranking_record_invalid")
                    continue
                candidate_id = record.get("candidate_id")
                rank = record.get("rank")
                if candidate_id not in source_admissible_ids:
                    blockers.append("source_advisory_rank_nonadmissible_candidate")
                    continue
                if not isinstance(rank, int) or isinstance(rank, bool) or rank <= 0:
                    blockers.append(f"source_advisory_rank_invalid_{candidate_id}")
                    continue
                if candidate_id in seen_ranked_ids or rank in seen_ranks:
                    blockers.append("source_advisory_ranking_duplicate")
                seen_ranked_ids.add(candidate_id)
                seen_ranks.add(rank)
                advisory_rank_map[candidate_id] = rank
            if seen_ranked_ids != source_admissible_ids:
                blockers.append("source_advisory_ranking_incomplete")
            if seen_ranks and seen_ranks != set(range(1, len(seen_ranks) + 1)):
                blockers.append("source_advisory_rank_sequence_invalid")

    if not isinstance(candidate_deliberation_inputs, list) or not candidate_deliberation_inputs:
        blockers.append("candidate_deliberation_inputs_empty")
        raw_inputs: list[dict] = []
    else:
        raw_inputs = list(candidate_deliberation_inputs)

    required_fields = {
        "candidate_id",
        "source_candidate_intake_digest",
        "source_admissible",
        "wa_assessment_digest",
        "stakeholder_assessment_digest",
        "relational_assessment_digest",
        "dissent_assessment_digest",
        "minority_assessment_digest",
        "wa_support",
        "stakeholder_support",
        "relational_support",
        "dissent_pressure",
        "minority_impact_risk",
        "uncertainty_burden",
        "review_blocker_digests",
        "exclusion_review_digest",
        "candidate_deliberation_input_digest",
    }
    input_map: dict[str, dict] = {}
    for index, raw_item in enumerate(raw_inputs):
        if not isinstance(raw_item, dict) or set(raw_item) != required_fields:
            blockers.append(f"candidate_deliberation_schema_invalid_{index}")
            continue
        item = dict(raw_item)
        candidate_id = item.get("candidate_id")
        if not isinstance(candidate_id, str) or candidate_id not in source_candidate_ids:
            blockers.append(f"candidate_deliberation_id_invalid_{index}")
            continue
        if candidate_id in input_map:
            blockers.append("candidate_deliberation_id_duplicate")
        input_map[candidate_id] = item
        source_item = source_evidence_map.get(candidate_id, {})
        if item.get("source_candidate_intake_digest") != source_item.get("candidate_intake_digest"):
            blockers.append(f"candidate_source_intake_digest_mismatch_{candidate_id}")
        expected_admissible = candidate_id in source_admissible_ids
        if item.get("source_admissible") is not expected_admissible:
            blockers.append(f"candidate_source_admissibility_mismatch_{candidate_id}")
        for digest_field in (
            "wa_assessment_digest",
            "stakeholder_assessment_digest",
            "relational_assessment_digest",
            "dissent_assessment_digest",
            "minority_assessment_digest",
        ):
            if not isinstance(item.get(digest_field), str) or not item.get(digest_field):
                blockers.append(f"candidate_{digest_field}_missing_{candidate_id}")
        for metric in (
            "wa_support",
            "stakeholder_support",
            "relational_support",
            "dissent_pressure",
            "minority_impact_risk",
            "uncertainty_burden",
        ):
            value = item.get(metric)
            if not finite(value) or not 0.0 <= float(value) <= 1.0:
                blockers.append(f"candidate_{metric}_invalid_{candidate_id}")
        valid_blockers, _ = _string_list(item.get("review_blocker_digests"))
        if not valid_blockers:
            blockers.append(f"candidate_review_blocker_digests_invalid_{candidate_id}")
        if expected_admissible:
            if item.get("exclusion_review_digest") != "":
                blockers.append(f"candidate_exclusion_review_digest_forbidden_{candidate_id}")
        elif not isinstance(item.get("exclusion_review_digest"), str) or not item.get("exclusion_review_digest"):
            blockers.append(f"candidate_exclusion_review_digest_missing_{candidate_id}")
        if item.get("candidate_deliberation_input_digest") != compute_candidate_deliberation_input_digest(item):
            blockers.append(f"candidate_deliberation_input_digest_mismatch_{candidate_id}")

    if set(input_map) != source_candidate_ids:
        blockers.append("candidate_deliberation_field_not_complete")

    if not blockers:
        expected_bundle = compute_deliberation_bundle_digest(
            source_intake_receipt_digest=source["decisionos_intake_receipt_digest"],
            deliberation_policy_digest=deliberation_policy_digest,
            threshold_config=threshold_config,
            candidate_deliberation_inputs=list(input_map.values()),
        )
        if deliberation_bundle_digest != expected_bundle:
            blockers.append("deliberation_bundle_digest_mismatch")

    if blockers:
        return DecisionOSWorldConditionedRelationalDeliberationResult(
            STATUS_BLOCKED,
            sorted(set(blockers)),
            None,
        )

    normalized_inputs = [input_map[candidate_id] for candidate_id in sorted(input_map)]
    records: list[dict] = []
    reviewable_ids: list[str] = []
    dissent_review_ids: list[str] = []
    minority_protection_ids: list[str] = []
    uncertainty_review_ids: list[str] = []
    evidence_blocked_ids: list[str] = []
    nonadmissible_ids: list[str] = []

    for item in normalized_inputs:
        candidate_id = item["candidate_id"]
        admissible = bool(item["source_admissible"])
        wa_gate = float(item["wa_support"]) + TOL >= float(minimum_wa_support)
        stakeholder_gate = (
            float(item["stakeholder_support"]) + TOL >= float(minimum_stakeholder_support)
        )
        relational_gate = (
            float(item["relational_support"]) + TOL >= float(minimum_relational_support)
        )
        dissent_review = (
            float(item["dissent_pressure"])
            > float(maximum_dissent_pressure_before_review) + TOL
            or bool(source_evidence_map[candidate_id].get("dissent_evidence_digests"))
        )
        minority_protection = (
            float(item["minority_impact_risk"])
            > float(maximum_minority_impact_risk) + TOL
            or bool(source_evidence_map[candidate_id].get("minority_evidence_digests"))
        )
        uncertainty_review = (
            float(item["uncertainty_burden"])
            > float(maximum_uncertainty_burden) + TOL
        )
        evidence_blocked = bool(item["review_blocker_digests"])
        relationally_reviewable = (
            admissible
            and wa_gate
            and stakeholder_gate
            and relational_gate
            and not dissent_review
            and not minority_protection
            and not uncertainty_review
            and not evidence_blocked
        )
        if not admissible:
            classification = "nonadmissible_retained"
            nonadmissible_ids.append(candidate_id)
        elif evidence_blocked:
            classification = "evidence_blocked"
            evidence_blocked_ids.append(candidate_id)
        elif minority_protection:
            classification = "minority_protection_required"
            minority_protection_ids.append(candidate_id)
        elif dissent_review:
            classification = "dissent_review_required"
            dissent_review_ids.append(candidate_id)
        elif uncertainty_review:
            classification = "uncertainty_review_required"
            uncertainty_review_ids.append(candidate_id)
        elif not (wa_gate and stakeholder_gate and relational_gate):
            classification = "relational_support_insufficient"
        else:
            classification = "relationally_reviewable"
            reviewable_ids.append(candidate_id)

        records.append(
            {
                "candidate_id": candidate_id,
                "source_candidate_intake_digest": item["source_candidate_intake_digest"],
                "candidate_deliberation_input_digest": item[
                    "candidate_deliberation_input_digest"
                ],
                "source_admissible": admissible,
                "source_probability_mass": float(distribution[candidate_id]),
                "source_combined_transition_action": float(actions[candidate_id]),
                "source_advisory_rank": advisory_rank_map.get(candidate_id, 0),
                "wa_support": float(item["wa_support"]),
                "stakeholder_support": float(item["stakeholder_support"]),
                "relational_support": float(item["relational_support"]),
                "dissent_pressure": float(item["dissent_pressure"]),
                "minority_impact_risk": float(item["minority_impact_risk"]),
                "uncertainty_burden": float(item["uncertainty_burden"]),
                "wa_gate_passed": wa_gate,
                "stakeholder_gate_passed": stakeholder_gate,
                "relational_gate_passed": relational_gate,
                "dissent_review_required": dissent_review,
                "minority_protection_required": minority_protection,
                "uncertainty_review_required": uncertainty_review,
                "evidence_blocked": evidence_blocked,
                "relationally_reviewable": relationally_reviewable,
                "deliberation_classification": classification,
                "review_blocker_digests": list(item["review_blocker_digests"]),
                "exclusion_review_digest": item["exclusion_review_digest"],
            }
        )

    record_map = {record["candidate_id"]: record for record in records}
    dominates_map: dict[str, list[str]] = {candidate_id: [] for candidate_id in reviewable_ids}
    dominated_by_map: dict[str, list[str]] = {candidate_id: [] for candidate_id in reviewable_ids}
    for left_id in reviewable_ids:
        for right_id in reviewable_ids:
            if left_id == right_id:
                continue
            if _dominates(record_map[left_id], record_map[right_id], float(dominance_tolerance)):
                dominates_map[left_id].append(right_id)
                dominated_by_map[right_id].append(left_id)
    for candidate_id in reviewable_ids:
        dominates_map[candidate_id].sort()
        dominated_by_map[candidate_id].sort()

    relational_frontier_ids = sorted(
        candidate_id
        for candidate_id in reviewable_ids
        if not dominated_by_map[candidate_id]
    )
    hold_guard_active = bool(source.get("source_handoff_disposition") == "hold_guarded_review")
    required_review_ids = set(relational_frontier_ids)
    required_review_ids.update(dissent_review_ids)
    required_review_ids.update(minority_protection_ids)
    required_review_ids.update(uncertainty_review_ids)
    required_review_ids.update(evidence_blocked_ids)
    if hold_guard_active and "hold" in source_admissible_ids:
        required_review_ids.add("hold")

    if minority_protection_ids:
        disposition = "minority_protection_review"
    elif dissent_review_ids:
        disposition = "dissent_review"
    elif evidence_blocked_ids:
        disposition = "evidence_completion_review"
    elif uncertainty_review_ids:
        disposition = "uncertainty_review"
    elif hold_guard_active:
        disposition = "hold_guarded_relational_review"
    elif not relational_frontier_ids:
        disposition = "no_relationally_reviewable_candidate"
    elif len(relational_frontier_ids) == 1:
        disposition = "single_relational_frontier_review"
    else:
        disposition = "plural_relational_frontier_review"

    receipt = {
        "kernel": "DecisionOS WORLD-Conditioned Relational Deliberation Kernel",
        "kernel_version": "v0.1",
        "decisionos_version": "v0.6",
        "status": "DECISIONOS_WORLD_CONDITIONED_RELATIONAL_DELIBERATION_READY",
        "source_decisionos_version": source["decisionos_version"],
        "source_intake_receipt_digest": source["decisionos_intake_receipt_digest"],
        "source_planos_handoff_certificate_digest": source[
            "source_handoff_certificate_digest"
        ],
        "source_world_binding_digest": source["source_world_binding_digest"],
        "source_world_model_state_digest": source["source_world_model_state_digest"],
        "source_world_model_revision": source["source_world_model_revision"],
        "source_world_lineage_digest": source["source_world_lineage_digest"],
        "source_handoff_disposition": source["source_handoff_disposition"],
        "source_decision_review_ready": bool(source["source_decision_review_ready"]),
        "deliberation_policy_digest": deliberation_policy_digest,
        "threshold_config": dict(sorted(threshold_config.items())),
        "candidate_deliberation_inputs": normalized_inputs,
        "deliberation_bundle_digest": deliberation_bundle_digest,
        "candidate_deliberation_records": records,
        "all_candidate_ids": sorted(source_candidate_ids),
        "admissible_candidate_ids": sorted(source_admissible_ids),
        "retained_nonadmissible_candidate_ids": sorted(nonadmissible_ids),
        "relationally_reviewable_candidate_ids": sorted(reviewable_ids),
        "relational_frontier_candidate_ids": relational_frontier_ids,
        "dissent_review_candidate_ids": sorted(dissent_review_ids),
        "minority_protection_candidate_ids": sorted(minority_protection_ids),
        "uncertainty_review_candidate_ids": sorted(uncertainty_review_ids),
        "evidence_blocked_candidate_ids": sorted(evidence_blocked_ids),
        "required_review_candidate_ids": sorted(required_review_ids),
        "dominates_map": {key: value for key, value in sorted(dominates_map.items())},
        "dominated_by_map": {key: value for key, value in sorted(dominated_by_map.items())},
        "hold_guard_active": hold_guard_active,
        "deliberation_disposition": disposition,
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
    receipt["decisionos_relational_deliberation_receipt_digest"] = canonical_digest(
        receipt
    )
    return DecisionOSWorldConditionedRelationalDeliberationResult(
        STATUS_READY,
        [],
        receipt,
    )
