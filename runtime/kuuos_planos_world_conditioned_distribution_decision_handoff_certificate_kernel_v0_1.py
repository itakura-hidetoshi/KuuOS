#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import math
from typing import Any

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
TOL = 1e-10
CANDIDATE_FIELD = (
    "continue",
    "strengthen",
    "repair",
    "slow_down",
    "reobserve",
    "reroute",
    "hold",
    "terminate_candidate",
)


@dataclass
class DistributionDecisionHandoffCertificateResult:
    status: str
    blockers: list[str]
    certificate: dict | None


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


def compute_next_distribution_digest(next_distribution: dict[str, float]) -> str:
    return canonical_digest(next_distribution)


def _rank_candidates(
    *,
    admissible_candidate_ids: list[str],
    next_distribution: dict[str, float],
    combined_transition_action_map: dict[str, float],
) -> list[str]:
    return sorted(
        admissible_candidate_ids,
        key=lambda candidate_id: (
            -float(next_distribution[candidate_id]),
            float(combined_transition_action_map[candidate_id]),
            candidate_id,
        ),
    )


def _entropy(probabilities: list[float]) -> float:
    return -sum(value * math.log(value) for value in probabilities if value > 0.0)


def build_world_conditioned_distribution_decision_handoff_certificate(
    *,
    source_distribution_update_digest: str,
    source_next_distribution_digest: str,
    source_world_conditioned_action_bundle_digest: str,
    source_world_binding_digest: str,
    source_world_model_state_digest: str,
    source_world_model_revision: int,
    source_world_lineage_digest: str,
    candidate_world_projection_digests: dict[str, str],
    combined_transition_action_map: dict[str, float],
    next_distribution: dict[str, float],
    admissible_candidate_ids: list[str],
    minimum_lead_margin: float,
    maximum_normalized_entropy: float,
    hold_review_threshold: float,
) -> DistributionDecisionHandoffCertificateResult:
    blockers: list[str] = []

    text_fields = {
        "source_distribution_update_digest": source_distribution_update_digest,
        "source_next_distribution_digest": source_next_distribution_digest,
        "source_world_conditioned_action_bundle_digest": source_world_conditioned_action_bundle_digest,
        "source_world_binding_digest": source_world_binding_digest,
        "source_world_model_state_digest": source_world_model_state_digest,
        "source_world_lineage_digest": source_world_lineage_digest,
    }
    blockers.extend(
        f"missing_{name}"
        for name, value in text_fields.items()
        if not isinstance(value, str) or not value
    )

    if (
        not isinstance(source_world_model_revision, int)
        or isinstance(source_world_model_revision, bool)
        or source_world_model_revision < 0
    ):
        blockers.append("invalid_source_world_model_revision")

    threshold_fields = {
        "minimum_lead_margin": minimum_lead_margin,
        "maximum_normalized_entropy": maximum_normalized_entropy,
        "hold_review_threshold": hold_review_threshold,
    }
    for name, value in threshold_fields.items():
        if not finite(value) or not 0.0 <= float(value) <= 1.0:
            blockers.append(f"invalid_{name}")

    maps = {
        "candidate_world_projection_digests": candidate_world_projection_digests,
        "combined_transition_action_map": combined_transition_action_map,
        "next_distribution": next_distribution,
    }
    for name, value in maps.items():
        if not isinstance(value, dict) or not value:
            blockers.append(f"invalid_{name}")

    candidate_ids: set[str] = set()
    if isinstance(candidate_world_projection_digests, dict):
        candidate_ids = set(candidate_world_projection_digests)
        if any(
            not isinstance(candidate_id, str)
            or not candidate_id
            or candidate_id not in CANDIDATE_FIELD
            for candidate_id in candidate_ids
        ):
            blockers.append("invalid_source_candidate_id")
        if any(
            not isinstance(digest, str) or not digest
            for digest in candidate_world_projection_digests.values()
        ):
            blockers.append("invalid_candidate_world_projection_digest")
        if len(set(candidate_world_projection_digests.values())) != len(
            candidate_world_projection_digests
        ):
            blockers.append("duplicate_candidate_world_projection_digest")

    if isinstance(combined_transition_action_map, dict):
        if set(combined_transition_action_map) != candidate_ids:
            blockers.append("combined_transition_action_map_candidate_set_mismatch")
        for candidate_id, value in combined_transition_action_map.items():
            if not finite(value) or float(value) < 0.0:
                blockers.append(f"invalid_combined_action_{candidate_id}")

    if isinstance(next_distribution, dict):
        if set(next_distribution) != candidate_ids:
            blockers.append("next_distribution_candidate_set_mismatch")
        distribution_total = 0.0
        for candidate_id, value in next_distribution.items():
            if not finite(value) or float(value) < 0.0:
                blockers.append(f"invalid_next_mass_{candidate_id}")
                continue
            distribution_total += float(value)
        if not close(distribution_total, 1.0):
            blockers.append("next_distribution_not_normalized")

    if not isinstance(admissible_candidate_ids, list):
        blockers.append("invalid_admissible_candidate_ids")
        admissible: list[str] = []
    else:
        admissible = list(admissible_candidate_ids)
        if not admissible or len(admissible) != len(set(admissible)):
            blockers.append("invalid_admissible_candidate_ids")
        if any(candidate_id not in candidate_ids for candidate_id in admissible):
            blockers.append("admissible_candidate_outside_source_field")

    if isinstance(next_distribution, dict):
        for candidate_id in admissible:
            value = next_distribution.get(candidate_id)
            if not finite(value) or float(value) <= 0.0:
                blockers.append(f"admissible_support_missing_{candidate_id}")
        for candidate_id in candidate_ids:
            if candidate_id not in admissible:
                value = next_distribution.get(candidate_id)
                if finite(value) and abs(float(value)) > TOL:
                    blockers.append(f"nonadmissible_candidate_has_mass_{candidate_id}")

    if (
        isinstance(next_distribution, dict)
        and isinstance(source_next_distribution_digest, str)
        and source_next_distribution_digest
        and source_next_distribution_digest
        != compute_next_distribution_digest(next_distribution)
    ):
        blockers.append("source_next_distribution_digest_mismatch")

    if blockers:
        return DistributionDecisionHandoffCertificateResult(
            STATUS_BLOCKED, sorted(set(blockers)), None
        )

    ranked_candidate_ids = _rank_candidates(
        admissible_candidate_ids=admissible,
        next_distribution=next_distribution,
        combined_transition_action_map=combined_transition_action_map,
    )
    probabilities = [
        float(next_distribution[candidate_id])
        for candidate_id in ranked_candidate_ids
    ]
    top_mass = probabilities[0]
    runner_up_mass = probabilities[1] if len(probabilities) > 1 else 0.0
    lead_margin = top_mass - runner_up_mass
    top_mass_candidate_ids = [
        candidate_id
        for candidate_id in ranked_candidate_ids
        if close(float(next_distribution[candidate_id]), top_mass)
    ]
    shannon_entropy = _entropy(probabilities)
    normalized_entropy = (
        shannon_entropy / math.log(len(probabilities))
        if len(probabilities) > 1
        else 0.0
    )
    concentration = sum(value * value for value in probabilities)
    effective_support = 1.0 / concentration
    effective_support_ratio = effective_support / len(probabilities)
    hold_mass = float(next_distribution.get("hold", 0.0))
    top_mass_is_tied = len(top_mass_candidate_ids) > 1
    lead_margin_sufficient = (
        len(probabilities) == 1
        or lead_margin + TOL >= float(minimum_lead_margin)
    )
    entropy_within_review_limit = (
        normalized_entropy <= float(maximum_normalized_entropy) + TOL
    )
    hold_review_guard_active = (
        "hold" in admissible
        and hold_mass + TOL >= float(hold_review_threshold)
    )
    decision_review_ready = (
        not top_mass_is_tied
        and lead_margin_sufficient
        and entropy_within_review_limit
    )

    if len(probabilities) == 1:
        handoff_disposition = "single_supported_candidate_review"
    elif top_mass_is_tied:
        handoff_disposition = "top_mass_tie_review"
    elif not lead_margin_sufficient:
        handoff_disposition = "insufficient_lead_margin_review"
    elif not entropy_within_review_limit:
        handoff_disposition = "diffuse_distribution_review"
    elif hold_review_guard_active:
        handoff_disposition = "hold_guarded_review"
    else:
        handoff_disposition = "separated_distribution_review"

    ranking_records = [
        {
            "rank": index + 1,
            "candidate_id": candidate_id,
            "probability_mass": float(next_distribution[candidate_id]),
            "combined_transition_action": float(
                combined_transition_action_map[candidate_id]
            ),
            "candidate_world_projection_digest": (
                candidate_world_projection_digests[candidate_id]
            ),
        }
        for index, candidate_id in enumerate(ranked_candidate_ids)
    ]

    certificate = {
        "kernel": (
            "PlanOS WORLD-Conditioned Distribution Decision Handoff "
            "Certificate Kernel"
        ),
        "kernel_version": "v0.1",
        "planos_version": "v1.02",
        "source_distribution_update_digest": source_distribution_update_digest,
        "source_next_distribution_digest": source_next_distribution_digest,
        "source_world_conditioned_action_bundle_digest": (
            source_world_conditioned_action_bundle_digest
        ),
        "source_world_binding_digest": source_world_binding_digest,
        "source_world_model_state_digest": source_world_model_state_digest,
        "source_world_model_revision": source_world_model_revision,
        "source_world_lineage_digest": source_world_lineage_digest,
        "candidate_world_projection_digests": dict(
            sorted(candidate_world_projection_digests.items())
        ),
        "combined_transition_action_map": dict(
            sorted(
                (candidate_id, float(value))
                for candidate_id, value in combined_transition_action_map.items()
            )
        ),
        "next_distribution": dict(
            sorted(
                (candidate_id, float(value))
                for candidate_id, value in next_distribution.items()
            )
        ),
        "admissible_candidate_ids": sorted(admissible),
        "ranking_records": ranking_records,
        "ranked_candidate_ids": ranked_candidate_ids,
        "top_mass_candidate_ids": top_mass_candidate_ids,
        "top_mass": top_mass,
        "runner_up_mass": runner_up_mass,
        "lead_margin": lead_margin,
        "minimum_lead_margin": float(minimum_lead_margin),
        "lead_margin_sufficient": lead_margin_sufficient,
        "shannon_entropy": shannon_entropy,
        "normalized_entropy": normalized_entropy,
        "maximum_normalized_entropy": float(maximum_normalized_entropy),
        "entropy_within_review_limit": entropy_within_review_limit,
        "concentration": concentration,
        "effective_support": effective_support,
        "effective_support_ratio": effective_support_ratio,
        "hold_mass": hold_mass,
        "hold_review_threshold": float(hold_review_threshold),
        "hold_review_guard_active": hold_review_guard_active,
        "top_mass_is_tied": top_mass_is_tied,
        "decision_review_ready": decision_review_ready,
        "handoff_disposition": handoff_disposition,
        "ranking_is_advisory_only": True,
        "candidate_field_retained": True,
        "persistent_world_state_unchanged": True,
        "world_model_prediction_not_truth": True,
        "world_mutation_not_granted": True,
        "history_read_only": True,
        "qi_grants_no_authority": True,
        "decision_selection_performed": False,
        "selected_candidate_id": "",
        "decision_authority_granted": False,
        "future_only": True,
        "active_now": False,
        "execution_permission": False,
    }
    certificate["decision_handoff_input_digest"] = canonical_digest(
        {
            "source_distribution_update_digest": source_distribution_update_digest,
            "source_next_distribution_digest": source_next_distribution_digest,
            "source_world_conditioned_action_bundle_digest": (
                source_world_conditioned_action_bundle_digest
            ),
            "source_world_binding_digest": source_world_binding_digest,
            "source_world_model_state_digest": source_world_model_state_digest,
            "source_world_model_revision": source_world_model_revision,
            "source_world_lineage_digest": source_world_lineage_digest,
            "candidate_world_projection_digests": (
                candidate_world_projection_digests
            ),
            "combined_transition_action_map": combined_transition_action_map,
            "next_distribution": next_distribution,
            "admissible_candidate_ids": sorted(admissible),
            "minimum_lead_margin": float(minimum_lead_margin),
            "maximum_normalized_entropy": float(maximum_normalized_entropy),
            "hold_review_threshold": float(hold_review_threshold),
        }
    )
    certificate["decision_handoff_certificate_digest"] = canonical_digest(certificate)

    return DistributionDecisionHandoffCertificateResult(
        STATUS_READY, [], certificate
    )
