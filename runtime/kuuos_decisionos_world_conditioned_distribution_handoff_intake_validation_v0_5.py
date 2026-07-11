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
PLANOS_VERSION = "v1.02"
ALLOWED_DISPOSITIONS = {
    "single_supported_candidate_review",
    "top_mass_tie_review",
    "insufficient_lead_margin_review",
    "diffuse_distribution_review",
    "hold_guarded_review",
    "separated_distribution_review",
}
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
class DecisionOSWorldConditionedHandoffIntakeResult:
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


def compute_candidate_intake_digest(item: Mapping[str, Any]) -> str:
    payload = dict(item)
    payload.pop("candidate_intake_digest", None)
    return canonical_digest(payload)


def compute_evidence_bundle_digest(
    *,
    stakeholder_context_digest: str,
    relational_context_digest: str,
    wa_context_digest: str,
    dissent_registry_digest: str,
    minority_registry_digest: str,
    candidate_evidence_items: list[dict],
) -> str:
    ordered = sorted(candidate_evidence_items, key=lambda item: str(item.get("candidate_id", "")))
    return canonical_digest(
        {
            "stakeholder_context_digest": stakeholder_context_digest,
            "relational_context_digest": relational_context_digest,
            "wa_context_digest": wa_context_digest,
            "dissent_registry_digest": dissent_registry_digest,
            "minority_registry_digest": minority_registry_digest,
            "candidate_evidence_items": ordered,
        }
    )


def _entropy(probabilities: list[float]) -> float:
    return -sum(value * math.log(value) for value in probabilities if value > 0.0)


def _expected_disposition(
    *,
    probabilities: list[float],
    top_mass_is_tied: bool,
    lead_margin_sufficient: bool,
    entropy_within_review_limit: bool,
    hold_review_guard_active: bool,
) -> str:
    if len(probabilities) == 1:
        return "single_supported_candidate_review"
    if top_mass_is_tied:
        return "top_mass_tie_review"
    if not lead_margin_sufficient:
        return "insufficient_lead_margin_review"
    if not entropy_within_review_limit:
        return "diffuse_distribution_review"
    if hold_review_guard_active:
        return "hold_guarded_review"
    return "separated_distribution_review"


def _string_list(value: Any) -> tuple[bool, list[str]]:
    if not isinstance(value, list):
        return False, []
    if any(not isinstance(item, str) or not item for item in value):
        return False, []
    if len(value) != len(set(value)):
        return False, []
    return True, list(value)


def build_decisionos_world_conditioned_distribution_handoff_intake_receipt(
    *,
    source_handoff_certificate: Mapping[str, Any],
    stakeholder_context_digest: str,
    relational_context_digest: str,
    wa_context_digest: str,
    dissent_registry_digest: str,
    minority_registry_digest: str,
    candidate_evidence_items: list[dict],
    evidence_bundle_digest: str,
) -> DecisionOSWorldConditionedHandoffIntakeResult:
    blockers: list[str] = []
    source = dict(source_handoff_certificate) if isinstance(source_handoff_certificate, Mapping) else {}
    if not source:
        blockers.append("source_handoff_certificate_missing")

    context_fields = {
        "stakeholder_context_digest": stakeholder_context_digest,
        "relational_context_digest": relational_context_digest,
        "wa_context_digest": wa_context_digest,
        "dissent_registry_digest": dissent_registry_digest,
        "minority_registry_digest": minority_registry_digest,
        "evidence_bundle_digest": evidence_bundle_digest,
    }
    blockers.extend(
        f"missing_{name}"
        for name, value in context_fields.items()
        if not isinstance(value, str) or not value
    )

    if source:
        source_digest = source.get("decision_handoff_certificate_digest")
        if not isinstance(source_digest, str) or not source_digest:
            blockers.append("source_handoff_certificate_digest_missing")
        else:
            unsigned = dict(source)
            unsigned.pop("decision_handoff_certificate_digest", None)
            if source_digest != canonical_digest(unsigned):
                blockers.append("source_handoff_certificate_digest_mismatch")
        if source.get("planos_version") != PLANOS_VERSION:
            blockers.append("source_planos_version_invalid")
        for name in (
            "source_distribution_update_digest",
            "source_next_distribution_digest",
            "source_world_conditioned_action_bundle_digest",
            "source_world_binding_digest",
            "source_world_model_state_digest",
            "source_world_lineage_digest",
            "decision_handoff_input_digest",
        ):
            if not isinstance(source.get(name), str) or not source.get(name):
                blockers.append(f"source_{name}_missing")
        revision = source.get("source_world_model_revision")
        if not isinstance(revision, int) or isinstance(revision, bool) or revision < 0:
            blockers.append("source_world_model_revision_invalid")
        required_true = (
            "ranking_is_advisory_only",
            "candidate_field_retained",
            "persistent_world_state_unchanged",
            "world_model_prediction_not_truth",
            "world_mutation_not_granted",
            "history_read_only",
            "qi_grants_no_authority",
            "future_only",
        )
        required_false = (
            "decision_selection_performed",
            "decision_authority_granted",
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
        if source.get("handoff_disposition") not in ALLOWED_DISPOSITIONS:
            blockers.append("source_handoff_disposition_invalid")
        for name in (
            "minimum_lead_margin",
            "maximum_normalized_entropy",
            "hold_review_threshold",
        ):
            value = source.get(name)
            if not finite(value) or not 0.0 <= float(value) <= 1.0:
                blockers.append(f"source_{name}_invalid")
        if not isinstance(source.get("decision_review_ready"), bool):
            blockers.append("source_decision_review_ready_invalid")

    projections = source.get("candidate_world_projection_digests", {})
    actions = source.get("combined_transition_action_map", {})
    distribution = source.get("next_distribution", {})
    admissible = source.get("admissible_candidate_ids", [])
    ranking_records = source.get("ranking_records", [])
    ranked_ids = source.get("ranked_candidate_ids", [])

    if not isinstance(projections, dict) or not projections:
        blockers.append("source_candidate_projection_map_invalid")
        candidate_ids: set[str] = set()
    else:
        candidate_ids = set(projections)
        if any(candidate_id not in CANDIDATE_FIELD for candidate_id in candidate_ids):
            blockers.append("source_candidate_id_invalid")
        if any(not isinstance(value, str) or not value for value in projections.values()):
            blockers.append("source_candidate_projection_digest_invalid")
        if len(set(projections.values())) != len(projections):
            blockers.append("source_candidate_projection_digest_duplicate")

    if not isinstance(actions, dict) or set(actions) != candidate_ids:
        blockers.append("source_combined_action_candidate_set_mismatch")
    else:
        for candidate_id, value in actions.items():
            if not finite(value) or float(value) < 0.0:
                blockers.append(f"source_combined_action_invalid_{candidate_id}")

    if not isinstance(distribution, dict) or set(distribution) != candidate_ids:
        blockers.append("source_distribution_candidate_set_mismatch")
    else:
        total = 0.0
        for candidate_id, value in distribution.items():
            if not finite(value) or float(value) < 0.0:
                blockers.append(f"source_distribution_mass_invalid_{candidate_id}")
                continue
            total += float(value)
        if not close(total, 1.0):
            blockers.append("source_distribution_not_normalized")
        if source.get("source_next_distribution_digest") != canonical_digest(distribution):
            blockers.append("source_next_distribution_digest_mismatch")

    if not isinstance(admissible, list) or not admissible or len(admissible) != len(set(admissible)):
        blockers.append("source_admissible_candidate_ids_invalid")
        admissible_ids: list[str] = []
    else:
        admissible_ids = list(admissible)
        if any(candidate_id not in candidate_ids for candidate_id in admissible_ids):
            blockers.append("source_admissible_candidate_outside_field")
    for candidate_id in candidate_ids:
        value = distribution.get(candidate_id)
        if candidate_id in admissible_ids:
            if not finite(value) or float(value) <= 0.0:
                blockers.append(f"source_admissible_support_missing_{candidate_id}")
        elif finite(value) and abs(float(value)) > TOL:
            blockers.append(f"source_nonadmissible_mass_present_{candidate_id}")

    expected_ranked = []
    if not blockers and admissible_ids:
        expected_ranked = sorted(
            admissible_ids,
            key=lambda candidate_id: (
                -float(distribution[candidate_id]),
                float(actions[candidate_id]),
                candidate_id,
            ),
        )
        if ranked_ids != expected_ranked:
            blockers.append("source_ranked_candidate_ids_mismatch")
        expected_records = [
            {
                "rank": index + 1,
                "candidate_id": candidate_id,
                "probability_mass": float(distribution[candidate_id]),
                "combined_transition_action": float(actions[candidate_id]),
                "candidate_world_projection_digest": projections[candidate_id],
            }
            for index, candidate_id in enumerate(expected_ranked)
        ]
        if ranking_records != expected_records:
            blockers.append("source_ranking_records_mismatch")

        probabilities = [float(distribution[candidate_id]) for candidate_id in expected_ranked]
        top_mass = probabilities[0]
        runner_up_mass = probabilities[1] if len(probabilities) > 1 else 0.0
        top_ids = [
            candidate_id
            for candidate_id in expected_ranked
            if close(float(distribution[candidate_id]), top_mass)
        ]
        lead_margin = top_mass - runner_up_mass
        shannon_entropy = _entropy(probabilities)
        normalized_entropy = shannon_entropy / math.log(len(probabilities)) if len(probabilities) > 1 else 0.0
        concentration = sum(value * value for value in probabilities)
        effective_support = 1.0 / concentration
        effective_support_ratio = effective_support / len(probabilities)
        expected_values = {
            "top_mass": top_mass,
            "runner_up_mass": runner_up_mass,
            "lead_margin": lead_margin,
            "shannon_entropy": shannon_entropy,
            "normalized_entropy": normalized_entropy,
            "concentration": concentration,
            "effective_support": effective_support,
            "effective_support_ratio": effective_support_ratio,
        }
        for name, expected in expected_values.items():
            if not finite(source.get(name)) or not close(float(source[name]), expected):
                blockers.append(f"source_{name}_mismatch")
        if source.get("top_mass_candidate_ids") != top_ids:
            blockers.append("source_top_mass_candidate_ids_mismatch")
        top_tied = len(top_ids) > 1
        lead_sufficient = len(probabilities) == 1 or lead_margin + TOL >= float(source["minimum_lead_margin"])
        entropy_ok = normalized_entropy <= float(source["maximum_normalized_entropy"]) + TOL
        hold_mass = float(distribution.get("hold", 0.0))
        hold_guard = "hold" in admissible_ids and hold_mass + TOL >= float(source["hold_review_threshold"])
        if source.get("top_mass_is_tied") is not top_tied:
            blockers.append("source_top_mass_tie_flag_mismatch")
        if source.get("lead_margin_sufficient") is not lead_sufficient:
            blockers.append("source_lead_margin_flag_mismatch")
        if source.get("entropy_within_review_limit") is not entropy_ok:
            blockers.append("source_entropy_review_flag_mismatch")
        if source.get("hold_review_guard_active") is not hold_guard:
            blockers.append("source_hold_review_guard_mismatch")
        expected_disposition = _expected_disposition(
            probabilities=probabilities,
            top_mass_is_tied=top_tied,
            lead_margin_sufficient=lead_sufficient,
            entropy_within_review_limit=entropy_ok,
            hold_review_guard_active=hold_guard,
        )
        if source.get("handoff_disposition") != expected_disposition:
            blockers.append("source_handoff_disposition_mismatch")

    if not isinstance(candidate_evidence_items, list) or not candidate_evidence_items:
        blockers.append("candidate_evidence_items_empty")
        evidence_items: list[dict] = []
    else:
        evidence_items = list(candidate_evidence_items)

    required_item_fields = {
        "candidate_id",
        "candidate_world_projection_digest",
        "probability_mass",
        "combined_transition_action",
        "advisory_rank",
        "admissible",
        "wa_evidence_digests",
        "stakeholder_evidence_digests",
        "relational_evidence_digests",
        "dissent_evidence_digests",
        "dissent_absence_attested",
        "minority_evidence_digests",
        "minority_absence_attested",
        "zero_mass_reason_digest",
        "candidate_intake_digest",
    }
    seen_items: set[str] = set()
    normalized_items: list[dict] = []
    dissent_present: list[str] = []
    dissent_absent: list[str] = []
    minority_present: list[str] = []
    minority_absent: list[str] = []

    rank_map = {candidate_id: index + 1 for index, candidate_id in enumerate(expected_ranked)}
    for index, raw_item in enumerate(evidence_items):
        if not isinstance(raw_item, dict) or set(raw_item) != required_item_fields:
            blockers.append(f"candidate_evidence_schema_invalid_{index}")
            continue
        item = dict(raw_item)
        candidate_id = item.get("candidate_id")
        if not isinstance(candidate_id, str) or candidate_id not in candidate_ids:
            blockers.append(f"candidate_evidence_id_invalid_{index}")
            continue
        if candidate_id in seen_items:
            blockers.append("candidate_evidence_id_duplicate")
        seen_items.add(candidate_id)
        if item.get("candidate_intake_digest") != compute_candidate_intake_digest(item):
            blockers.append(f"candidate_intake_digest_mismatch_{candidate_id}")
        if item.get("candidate_world_projection_digest") != projections.get(candidate_id):
            blockers.append(f"candidate_projection_digest_mismatch_{candidate_id}")
        if not finite(item.get("probability_mass")) or not close(float(item["probability_mass"]), float(distribution.get(candidate_id, -1.0))):
            blockers.append(f"candidate_probability_mass_mismatch_{candidate_id}")
        if not finite(item.get("combined_transition_action")) or not close(float(item["combined_transition_action"]), float(actions.get(candidate_id, -1.0))):
            blockers.append(f"candidate_combined_action_mismatch_{candidate_id}")
        expected_admissible = candidate_id in admissible_ids
        if item.get("admissible") is not expected_admissible:
            blockers.append(f"candidate_admissibility_mismatch_{candidate_id}")
        expected_rank = rank_map.get(candidate_id, 0)
        if item.get("advisory_rank") != expected_rank:
            blockers.append(f"candidate_advisory_rank_mismatch_{candidate_id}")

        list_values: dict[str, list[str]] = {}
        for field in (
            "wa_evidence_digests",
            "stakeholder_evidence_digests",
            "relational_evidence_digests",
            "dissent_evidence_digests",
            "minority_evidence_digests",
        ):
            valid, values = _string_list(item.get(field))
            if not valid:
                blockers.append(f"candidate_{field}_invalid_{candidate_id}")
            list_values[field] = values
        if expected_admissible:
            for field in (
                "wa_evidence_digests",
                "stakeholder_evidence_digests",
                "relational_evidence_digests",
            ):
                if not list_values[field]:
                    blockers.append(f"candidate_{field}_missing_{candidate_id}")
            if item.get("zero_mass_reason_digest") != "":
                blockers.append(f"candidate_zero_mass_reason_forbidden_{candidate_id}")
        else:
            if not isinstance(item.get("zero_mass_reason_digest"), str) or not item.get("zero_mass_reason_digest"):
                blockers.append(f"candidate_zero_mass_reason_missing_{candidate_id}")

        dissent_values = list_values["dissent_evidence_digests"]
        dissent_attested = item.get("dissent_absence_attested")
        if dissent_values:
            if dissent_attested is not False:
                blockers.append(f"candidate_dissent_absence_conflict_{candidate_id}")
            dissent_present.append(candidate_id)
        else:
            if dissent_attested is not True:
                blockers.append(f"candidate_dissent_absence_unattested_{candidate_id}")
            dissent_absent.append(candidate_id)

        minority_values = list_values["minority_evidence_digests"]
        minority_attested = item.get("minority_absence_attested")
        if minority_values:
            if minority_attested is not False:
                blockers.append(f"candidate_minority_absence_conflict_{candidate_id}")
            minority_present.append(candidate_id)
        else:
            if minority_attested is not True:
                blockers.append(f"candidate_minority_absence_unattested_{candidate_id}")
            minority_absent.append(candidate_id)
        normalized_items.append(item)

    if seen_items != candidate_ids:
        blockers.append("candidate_evidence_field_not_complete")

    if not blockers:
        expected_bundle = compute_evidence_bundle_digest(
            stakeholder_context_digest=stakeholder_context_digest,
            relational_context_digest=relational_context_digest,
            wa_context_digest=wa_context_digest,
            dissent_registry_digest=dissent_registry_digest,
            minority_registry_digest=minority_registry_digest,
            candidate_evidence_items=normalized_items,
        )
        if evidence_bundle_digest != expected_bundle:
            blockers.append("evidence_bundle_digest_mismatch")

    if blockers:
        return DecisionOSWorldConditionedHandoffIntakeResult(
            STATUS_BLOCKED, sorted(set(blockers)), None
        )

    normalized_items.sort(key=lambda item: item["candidate_id"])
    retained_nonadmissible = sorted(candidate_ids - set(admissible_ids))
    receipt = {
        "kernel": "DecisionOS WORLD-Conditioned Distribution Handoff Intake Validation Kernel",
        "kernel_version": "v0.1",
        "decisionos_version": "v0.5",
        "status": "DECISIONOS_WORLD_CONDITIONED_HANDOFF_INTAKE_READY",
        "source_planos_version": source["planos_version"],
        "source_handoff_certificate_digest": source["decision_handoff_certificate_digest"],
        "source_decision_handoff_input_digest": source["decision_handoff_input_digest"],
        "source_distribution_update_digest": source["source_distribution_update_digest"],
        "source_next_distribution_digest": source["source_next_distribution_digest"],
        "source_world_binding_digest": source["source_world_binding_digest"],
        "source_world_model_state_digest": source["source_world_model_state_digest"],
        "source_world_model_revision": source["source_world_model_revision"],
        "source_world_lineage_digest": source["source_world_lineage_digest"],
        "source_handoff_disposition": source["handoff_disposition"],
        "source_decision_review_ready": bool(source["decision_review_ready"]),
        "candidate_world_projection_digests": dict(sorted(projections.items())),
        "next_distribution": dict(sorted((key, float(value)) for key, value in distribution.items())),
        "combined_transition_action_map": dict(sorted((key, float(value)) for key, value in actions.items())),
        "advisory_ranking_records": list(ranking_records),
        "all_candidate_ids": sorted(candidate_ids),
        "admissible_candidate_ids": sorted(admissible_ids),
        "retained_nonadmissible_candidate_ids": retained_nonadmissible,
        "stakeholder_context_digest": stakeholder_context_digest,
        "relational_context_digest": relational_context_digest,
        "wa_context_digest": wa_context_digest,
        "dissent_registry_digest": dissent_registry_digest,
        "minority_registry_digest": minority_registry_digest,
        "candidate_evidence_items": normalized_items,
        "evidence_bundle_digest": evidence_bundle_digest,
        "dissent_present_candidate_ids": sorted(dissent_present),
        "dissent_absence_attested_candidate_ids": sorted(dissent_absent),
        "minority_present_candidate_ids": sorted(minority_present),
        "minority_absence_attested_candidate_ids": sorted(minority_absent),
        "intake_owned_by_decision_os": True,
        "source_owned_by_plan_os": True,
        "deliberation_intake_ready": True,
        "all_candidates_considered": True,
        "candidate_identity_preserved": True,
        "retained_alternatives_preserved": True,
        "wa_evidence_preserved": True,
        "stakeholder_context_preserved": True,
        "relational_context_preserved": True,
        "dissent_visibility_preserved": True,
        "minority_visibility_preserved": True,
        "silent_substitution_detected": False,
        "ranking_is_advisory_only": True,
        "decisionos_owns_selection": True,
        "selection_authority_granted_by_intake": False,
        "decision_selection_performed": False,
        "selected_candidate_id": "",
        "decision_receipt_issued": False,
        "persistent_world_state_unchanged": True,
        "world_model_prediction_not_truth": True,
        "world_mutation_not_granted": True,
        "history_read_only": True,
        "qi_grants_no_authority": True,
        "plan_synthesis_performed": False,
        "active_now": False,
        "execution_permission": False,
    }
    receipt["decisionos_intake_receipt_digest"] = canonical_digest(receipt)
    return DecisionOSWorldConditionedHandoffIntakeResult(STATUS_READY, [], receipt)
