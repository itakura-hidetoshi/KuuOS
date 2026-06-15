#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_adapter_capability_gauge_model_v0_6 import build_selection
from runtime.kuuos_adapter_capability_gauge_types_v0_6 import as_list as v6_list
from runtime.kuuos_adapter_portfolio_shadow_types_v0_7 import (
    BUNDLE_VERSION,
    PROJECTION_VERSION,
    RESOLUTION_VERSION,
    SECTION_VERSION,
    SELECTION_VERSION,
    as_list,
    bundle_digest,
    clamp,
    integer,
    mapping,
    projection_digest,
    resolution_digest,
    section_digest,
    selection_digest,
    sha,
    signed,
)


def empty_bundle(agent_id: str) -> dict[str, Any]:
    packet = {
        "version": BUNDLE_VERSION,
        "agent_id": agent_id,
        "generation": 0,
        "sections": [],
        "pending_predictions": [],
        "resolved_predictions": [],
        "portfolio_holonomy": [],
        "processed_live_effect_digests": [],
    }
    packet["portfolio_bundle_digest"] = bundle_digest(packet)
    return packet


def section_for(bundle: Mapping[str, Any], adapter_id: str, context_key: str) -> dict[str, Any]:
    for raw in as_list(bundle.get("sections")):
        section = dict(mapping(raw))
        if (
            section.get("federation_adapter_id") == adapter_id
            and section.get("context_key") == context_key
        ):
            return section
    return {}


def initial_section(adapter_id: str, context_key: str) -> dict[str, Any]:
    section = {
        "version": SECTION_VERSION,
        "section_id": "portfolio-section-" + sha(
            {"adapter": adapter_id, "context": context_key}
        )[:18],
        "federation_adapter_id": adapter_id,
        "context_key": context_key,
        "resolved_shadow_count": 0,
        "live_count": 0,
        "mean_realization_error": 0.0,
        "mean_absolute_realization_error": 0.0,
        "shadow_bias": 0.0,
        "reliability": 0.0,
        "last_predicted_utility": 0.0,
        "last_realized_utility": 0.0,
        "last_realization_error": 0.0,
        "last_prediction_id": "",
        "last_live_effect_receipt_digest": "",
    }
    section["portfolio_section_digest"] = section_digest(section)
    return section


def _entry_by_id(registry: Mapping[str, Any], adapter_id: str) -> dict[str, Any]:
    for raw in as_list(registry.get("adapters")):
        entry = dict(mapping(raw))
        if entry.get("federation_adapter_id") == adapter_id:
            return entry
    return {}


def _mean(previous: float, count: int, observed: float) -> float:
    return round((previous * count + observed) / (count + 1), 6)


def build_portfolio_selection(
    *,
    portfolio_run_id: str,
    capability_bundle: Mapping[str, Any],
    portfolio_bundle: Mapping[str, Any],
    registry: Mapping[str, Any],
    source_packets: list[Mapping[str, Any]],
    normalized_wake: Mapping[str, Any],
    exploration_weight: float,
    max_exploration_bonus: float,
    curvature_penalty: float,
    resolved_evidence_weight: float,
    max_portfolio_adjustment: float,
    blockers: list[str],
) -> tuple[dict[str, Any], dict[str, Any]]:
    base_selection, _, _ = build_selection(
        capability_run_id=portfolio_run_id + ":preselect",
        bundle=capability_bundle,
        registry=registry,
        source_packets=source_packets,
        wake=normalized_wake,
        exploration_weight=exploration_weight,
        max_exploration_bonus=max_exploration_bonus,
        curvature_penalty=curvature_penalty,
        blockers=blockers,
    )
    if blockers:
        return {}, {}
    context_key = str(base_selection.get("context_key", ""))
    candidates: list[dict[str, Any]] = []
    for raw in v6_list(base_selection.get("candidates")):
        candidate = dict(mapping(raw))
        adapter_id = str(candidate.get("federation_adapter_id", ""))
        section = section_for(portfolio_bundle, adapter_id, context_key)
        bias = signed(section.get("shadow_bias"), 0.0)
        reliability = clamp(section.get("reliability"), 0.0)
        adjustment = max(
            -max_portfolio_adjustment,
            min(
                max_portfolio_adjustment,
                resolved_evidence_weight * reliability * bias,
            ),
        )
        base_score = float(candidate.get("selection_score", 0.0))
        adjusted = max(0.0, min(1.5, base_score + adjustment))
        candidates.append(
            {
                **candidate,
                "portfolio_shadow_bias": round(bias, 6),
                "portfolio_reliability": round(reliability, 6),
                "portfolio_adjustment": round(adjustment, 6),
                "adjusted_selection_score": round(adjusted, 6),
                "resolved_shadow_count": integer(
                    section.get("resolved_shadow_count"), 0
                ),
            }
        )
    candidates.sort(
        key=lambda item: (
            -float(item.get("adjusted_selection_score", 0.0)),
            -int(item.get("static_priority_tie_break", 0)),
            str(item.get("federation_adapter_id", "")),
        )
    )
    if not candidates:
        blockers.append("portfolio_candidates_missing")
        return {}, {}
    selected = candidates[0]
    packet = {
        "version": SELECTION_VERSION,
        "portfolio_run_id": portfolio_run_id,
        "source_batch_digest": base_selection.get("source_batch_digest", ""),
        "normalized_wake_digest": base_selection.get("normalized_wake_digest", ""),
        "capability_bundle_digest": capability_bundle.get(
            "capability_bundle_digest", ""
        ),
        "portfolio_bundle_digest": portfolio_bundle.get(
            "portfolio_bundle_digest", ""
        ),
        "context_key": context_key,
        "context_signature": base_selection.get("context_signature", {}),
        "candidates": candidates,
        "live_adapter_id": selected.get("federation_adapter_id", ""),
        "live_adapter_profile_digest": selected.get(
            "adapter_profile_digest", ""
        ),
        "live_base_score": selected.get("selection_score", 0.0),
        "live_portfolio_adjustment": selected.get("portfolio_adjustment", 0.0),
        "live_adjusted_score": selected.get("adjusted_selection_score", 0.0),
        "shadow_candidates": [
            item.get("federation_adapter_id", "") for item in candidates[1:]
        ],
        "static_priority_used_only_as_tie_break": True,
        "pending_shadow_prediction_has_no_execution_authority": True,
        "shadow_prediction_not_truth": True,
    }
    packet["portfolio_selection_digest"] = selection_digest(packet)
    return packet, _entry_by_id(registry, str(packet["live_adapter_id"]))


def resolve_previous_shadow(
    *,
    portfolio_run_id: str,
    bundle: Mapping[str, Any],
    live_adapter_id: str,
    context_key: str,
    covariant_step_kind: str,
    live_observed_utility: float,
    live_effect_receipt_digest: str,
    shadow_learning_rate: float,
    reliability_prior_mass: float,
) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    pending = [dict(mapping(item)) for item in as_list(bundle.get("pending_predictions"))]
    matching = [
        item
        for item in pending
        if item.get("federation_adapter_id") == live_adapter_id
        and item.get("context_key") == context_key
        and item.get("covariant_step_kind") == covariant_step_kind
        and item.get("status") == "pending"
    ]
    matching.sort(key=lambda item: int(item.get("created_generation", 0)), reverse=True)
    resolved_prediction = matching[0] if matching else {}
    if not resolved_prediction:
        report = {
            "version": RESOLUTION_VERSION,
            "portfolio_run_id": portfolio_run_id,
            "live_adapter_id": live_adapter_id,
            "context_key": context_key,
            "covariant_step_kind": covariant_step_kind,
            "resolved": False,
            "resolved_prediction_id": "",
            "predicted_utility": 0.0,
            "live_observed_utility": round(live_observed_utility, 6),
            "realization_error": 0.0,
            "updated_shadow_bias": 0.0,
            "updated_reliability": 0.0,
            "live_effect_receipt_digest": live_effect_receipt_digest,
        }
        report["shadow_resolution_digest"] = resolution_digest(report)
        return dict(bundle), report, []

    prediction_id = str(resolved_prediction.get("prediction_id", ""))
    predicted = clamp(resolved_prediction.get("predicted_utility"), 0.0)
    confidence = clamp(resolved_prediction.get("prediction_confidence"), 0.0)
    error = signed(live_observed_utility - predicted)
    old = section_for(bundle, live_adapter_id, context_key) or initial_section(
        live_adapter_id, context_key
    )
    count = integer(old.get("resolved_shadow_count"), 0)
    old_bias = signed(old.get("shadow_bias"), 0.0)
    alpha = clamp(shadow_learning_rate) * confidence
    new_bias = signed(old_bias + alpha * (error - old_bias))
    reliability = clamp((count + 1) / (count + 1 + reliability_prior_mass))
    section = dict(old)
    section.update(
        {
            "resolved_shadow_count": count + 1,
            "mean_realization_error": _mean(
                float(old.get("mean_realization_error", 0.0)), count, error
            ),
            "mean_absolute_realization_error": _mean(
                float(old.get("mean_absolute_realization_error", 0.0)),
                count,
                abs(error),
            ),
            "shadow_bias": round(new_bias, 6),
            "reliability": round(reliability, 6),
            "last_predicted_utility": round(predicted, 6),
            "last_realized_utility": round(live_observed_utility, 6),
            "last_realization_error": round(error, 6),
            "last_prediction_id": prediction_id,
            "last_live_effect_receipt_digest": live_effect_receipt_digest,
        }
    )
    section["portfolio_section_digest"] = section_digest(section)

    sections = [
        dict(mapping(item))
        for item in as_list(bundle.get("sections"))
        if not (
            mapping(item).get("federation_adapter_id") == live_adapter_id
            and mapping(item).get("context_key") == context_key
        )
    ]
    sections.append(section)
    sections.sort(
        key=lambda item: (
            str(item.get("context_key", "")),
            str(item.get("federation_adapter_id", "")),
        )
    )
    remaining = [
        item for item in pending if item.get("prediction_id") != prediction_id
    ]
    resolved_entry = {
        **resolved_prediction,
        "status": "resolved",
        "resolved_by_portfolio_run_id": portfolio_run_id,
        "live_observed_utility": round(live_observed_utility, 6),
        "realization_error": round(error, 6),
        "live_effect_receipt_digest": live_effect_receipt_digest,
    }
    updated = dict(bundle)
    updated["sections"] = sections
    updated["pending_predictions"] = remaining
    updated["resolved_predictions"] = as_list(bundle.get("resolved_predictions")) + [
        resolved_entry
    ]
    report = {
        "version": RESOLUTION_VERSION,
        "portfolio_run_id": portfolio_run_id,
        "live_adapter_id": live_adapter_id,
        "context_key": context_key,
        "covariant_step_kind": covariant_step_kind,
        "resolved": True,
        "resolved_prediction_id": prediction_id,
        "predicted_utility": round(predicted, 6),
        "prediction_confidence": round(confidence, 6),
        "live_observed_utility": round(live_observed_utility, 6),
        "realization_error": round(error, 6),
        "effective_learning_rate": round(alpha, 6),
        "updated_shadow_bias": round(new_bias, 6),
        "updated_reliability": round(reliability, 6),
        "live_effect_receipt_digest": live_effect_receipt_digest,
        "portfolio_section_digest": section.get("portfolio_section_digest", ""),
    }
    report["shadow_resolution_digest"] = resolution_digest(report)
    return updated, report, [resolved_entry]


def build_shadow_projections(
    *,
    portfolio_run_id: str,
    selection: Mapping[str, Any],
    bundle: Mapping[str, Any],
    registry: Mapping[str, Any],
    covariant_step_kind: str,
    live_observed_utility: float,
    live_effect_receipt_digest: str,
    action_utility: Mapping[str, Any],
    shadow_model_weight: float,
    max_shadow_candidates: int,
    default_prediction_confidence: float,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    live_id = str(selection.get("live_adapter_id", ""))
    context_key = str(selection.get("context_key", ""))
    candidates = [
        dict(mapping(item))
        for item in as_list(selection.get("candidates"))
        if mapping(item).get("federation_adapter_id") != live_id
    ][:max_shadow_candidates]
    projections: list[dict[str, Any]] = []
    for candidate in candidates:
        adapter_id = str(candidate.get("federation_adapter_id", ""))
        entry = _entry_by_id(registry, adapter_id)
        route = mapping(entry.get("capability_routing_table"))
        predicted_action = str(route.get(covariant_step_kind, "hold"))
        action_prior = clamp(action_utility.get(predicted_action), 0.5)
        connection = clamp(candidate.get("connection_coefficient"), 0.5)
        section = section_for(bundle, adapter_id, context_key)
        reliability = clamp(section.get("reliability"), 0.0)
        bias = signed(section.get("shadow_bias"), 0.0)
        predictor = mapping(entry.get("shadow_predictor"))
        confidence = clamp(
            predictor.get("confidence"), default_prediction_confidence
        )
        predicted = clamp(
            (1.0 - shadow_model_weight) * connection
            + shadow_model_weight * action_prior
            + reliability * bias
        )
        relative_residual = signed(predicted - live_observed_utility)
        prediction = {
            "version": PROJECTION_VERSION,
            "prediction_id": "shadow-prediction-" + sha(
                {
                    "run": portfolio_run_id,
                    "adapter": adapter_id,
                    "context": context_key,
                    "step": covariant_step_kind,
                }
            )[:18],
            "portfolio_run_id": portfolio_run_id,
            "federation_adapter_id": adapter_id,
            "adapter_profile_digest": candidate.get(
                "adapter_profile_digest", ""
            ),
            "context_key": context_key,
            "covariant_step_kind": covariant_step_kind,
            "predicted_domain_action": predicted_action,
            "connection_component": round(connection, 6),
            "action_utility_component": round(action_prior, 6),
            "portfolio_bias_component": round(reliability * bias, 6),
            "predicted_utility": round(predicted, 6),
            "prediction_confidence": round(confidence, 6),
            "live_observed_utility_reference": round(live_observed_utility, 6),
            "counterfactual_relative_residual": round(relative_residual, 6),
            "source_live_effect_receipt_digest": live_effect_receipt_digest,
            "status": "pending",
            "created_generation": integer(bundle.get("generation"), 0) + 1,
            "shadow_non_actuating": True,
            "shadow_prediction_not_truth": True,
            "shadow_prediction_not_capability_evidence": True,
        }
        prediction["shadow_projection_digest"] = projection_digest(prediction)
        projections.append(prediction)
    packet = {
        "version": PROJECTION_VERSION,
        "portfolio_run_id": portfolio_run_id,
        "context_key": context_key,
        "live_adapter_id": live_id,
        "covariant_step_kind": covariant_step_kind,
        "live_observed_utility": round(live_observed_utility, 6),
        "live_effect_receipt_digest": live_effect_receipt_digest,
        "projection_count": len(projections),
        "projections": projections,
        "shadow_non_actuating": True,
        "shadow_prediction_not_truth": True,
        "shadow_prediction_not_capability_evidence": True,
    }
    packet["shadow_projection_digest"] = projection_digest(packet)
    return packet, projections


def commit_portfolio_update(
    *,
    portfolio_run_id: str,
    bundle: Mapping[str, Any],
    selection: Mapping[str, Any],
    resolution: Mapping[str, Any],
    projections: list[Mapping[str, Any]],
    live_observed_utility: float,
    live_effect_receipt_digest: str,
    max_pending_predictions: int,
    max_resolved_predictions: int,
    max_holonomy: int,
) -> tuple[dict[str, Any], bool]:
    processed = {
        str(item) for item in as_list(bundle.get("processed_live_effect_digests"))
    }
    if live_effect_receipt_digest in processed:
        return dict(bundle), True
    live_id = str(selection.get("live_adapter_id", ""))
    context_key = str(selection.get("context_key", ""))
    old = section_for(bundle, live_id, context_key) or initial_section(
        live_id, context_key
    )
    live_section = dict(old)
    live_section["live_count"] = integer(old.get("live_count"), 0) + 1
    live_section["last_realized_utility"] = round(live_observed_utility, 6)
    live_section["last_live_effect_receipt_digest"] = live_effect_receipt_digest
    live_section["portfolio_section_digest"] = section_digest(live_section)
    sections = [
        dict(mapping(item))
        for item in as_list(bundle.get("sections"))
        if not (
            mapping(item).get("federation_adapter_id") == live_id
            and mapping(item).get("context_key") == context_key
        )
    ]
    sections.append(live_section)
    sections.sort(
        key=lambda item: (
            str(item.get("context_key", "")),
            str(item.get("federation_adapter_id", "")),
        )
    )
    pending = as_list(bundle.get("pending_predictions")) + [dict(item) for item in projections]
    resolved = as_list(bundle.get("resolved_predictions"))
    holonomy = as_list(bundle.get("portfolio_holonomy")) + [
        {
            "portfolio_run_id": portfolio_run_id,
            "context_key": context_key,
            "live_adapter_id": live_id,
            "live_observed_utility": round(live_observed_utility, 6),
            "live_effect_receipt_digest": live_effect_receipt_digest,
            "portfolio_selection_digest": selection.get(
                "portfolio_selection_digest", ""
            ),
            "shadow_resolution_digest": resolution.get(
                "shadow_resolution_digest", ""
            ),
            "shadow_projection_digests": [
                mapping(item).get("shadow_projection_digest", "")
                for item in projections
            ],
        }
    ]
    updated = {
        "version": BUNDLE_VERSION,
        "agent_id": bundle.get("agent_id", ""),
        "generation": integer(bundle.get("generation"), 0) + 1,
        "sections": sections,
        "pending_predictions": pending[-max_pending_predictions:],
        "resolved_predictions": resolved[-max_resolved_predictions:],
        "portfolio_holonomy": holonomy[-max_holonomy:],
        "processed_live_effect_digests": sorted(
            processed | {live_effect_receipt_digest}
        ),
    }
    updated["portfolio_bundle_digest"] = bundle_digest(updated)
    return updated, False
