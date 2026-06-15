#!/usr/bin/env python3
from __future__ import annotations

import math
from typing import Any, Mapping

from runtime.kuuos_event_adapter_federation_types_v0_5 import as_list as v5_as_list
from runtime.kuuos_adapter_capability_gauge_types_v0_6 import (
    BUNDLE_VERSION,
    CALIBRATION_VERSION,
    SECTION_VERSION,
    SELECTION_VERSION,
    as_list,
    bundle_digest,
    calibration_digest,
    clamp,
    integer,
    mapping,
    section_digest,
    selection_digest,
    sha,
)


def context_signature(
    source_packets: list[Mapping[str, Any]], wake: Mapping[str, Any]
) -> tuple[str, dict[str, Any]]:
    signature = {
        "wake_kind": str(wake.get("wake_kind", "")),
        "source_kinds": sorted(
            {str(packet.get("source_kind", "")) for packet in source_packets}
        ),
        "source_ids": sorted(
            {str(packet.get("source_id", "")) for packet in source_packets}
        ),
        "signal_kinds": sorted(
            {
                str(mapping(signal).get("kind", ""))
                for packet in source_packets
                for signal in as_list(packet.get("signals"))
            }
        ),
    }
    return "cap-context-" + sha(signature)[:18], signature


def empty_bundle(agent_id: str) -> dict[str, Any]:
    bundle = {
        "version": BUNDLE_VERSION,
        "agent_id": agent_id,
        "generation": 0,
        "sections": [],
        "holonomy_trace": [],
        "processed_evidence_digests": [],
    }
    bundle["capability_bundle_digest"] = bundle_digest(bundle)
    return bundle


def section_for(
    bundle: Mapping[str, Any], adapter_id: str, context_key: str
) -> dict[str, Any]:
    for raw in as_list(bundle.get("sections")):
        section = dict(mapping(raw))
        if (
            section.get("federation_adapter_id") == adapter_id
            and section.get("context_key") == context_key
        ):
            return section
    return {}


def initial_section(
    *,
    adapter_id: str,
    profile_digest: str,
    context_key: str,
    context: Mapping[str, Any],
    prior: float,
) -> dict[str, Any]:
    section = {
        "version": SECTION_VERSION,
        "section_id": "cap-section-" + sha(
            {"adapter": adapter_id, "context": context_key}
        )[:18],
        "federation_adapter_id": adapter_id,
        "adapter_profile_digest": profile_digest,
        "context_key": context_key,
        "context_signature": dict(context),
        "observation_count": 0,
        "selection_count": 0,
        "success_count": 0,
        "partial_count": 0,
        "blocked_count": 0,
        "mean_progress": 0.0,
        "mean_benefit": 0.0,
        "mean_harm": 0.0,
        "mean_recoverability": 0.0,
        "mean_confidence": 0.0,
        "mean_utility": prior,
        "connection_coefficient": prior,
        "last_capability_curvature": 0.0,
        "cumulative_abs_curvature": 0.0,
        "last_effect_receipt_digest": "",
        "last_federated_evidence_digest": "",
    }
    section["capability_section_digest"] = section_digest(section)
    return section


def eligible_entries(
    registry: Mapping[str, Any],
    source_packets: list[Mapping[str, Any]],
    wake: Mapping[str, Any],
) -> list[dict[str, Any]]:
    source_ids = {str(packet.get("source_id", "")) for packet in source_packets}
    dominant_kind = str(wake.get("wake_kind", ""))
    output: list[dict[str, Any]] = []
    for raw in v5_as_list(registry.get("adapters")):
        entry = dict(mapping(raw))
        if entry.get("enabled") is not True:
            continue
        accepted_kinds = {str(item) for item in as_list(entry.get("accepted_source_kinds"))}
        accepted_ids = {str(item) for item in as_list(entry.get("accepted_source_ids"))}
        if dominant_kind not in accepted_kinds:
            continue
        if accepted_ids and not source_ids.intersection(accepted_ids):
            continue
        output.append(entry)
    return output


def build_selection(
    *,
    capability_run_id: str,
    bundle: Mapping[str, Any],
    registry: Mapping[str, Any],
    source_packets: list[Mapping[str, Any]],
    wake: Mapping[str, Any],
    exploration_weight: float,
    max_exploration_bonus: float,
    curvature_penalty: float,
    blockers: list[str],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    context_key, context = context_signature(source_packets, wake)
    candidates: list[dict[str, Any]] = []
    entries = eligible_entries(registry, source_packets, wake)
    for entry in entries:
        adapter_id = str(entry.get("federation_adapter_id", ""))
        profile = dict(mapping(entry.get("adapter_profile")))
        prior = clamp(entry.get("capability_prior"), 0.5)
        section = section_for(bundle, adapter_id, context_key) or initial_section(
            adapter_id=adapter_id,
            profile_digest=str(profile.get("adapter_profile_digest", "")),
            context_key=context_key,
            context=context,
            prior=prior,
        )
        observations = integer(section.get("observation_count"), 0)
        exploration = min(
            max_exploration_bonus,
            exploration_weight / math.sqrt(observations + 1.0),
        )
        connection = clamp(section.get("connection_coefficient"), prior)
        curvature = abs(float(section.get("last_capability_curvature", 0.0)))
        score = max(
            0.0,
            min(1.5, connection + exploration - curvature_penalty * curvature),
        )
        candidates.append(
            {
                "federation_adapter_id": adapter_id,
                "adapter_profile_digest": profile.get("adapter_profile_digest", ""),
                "context_key": context_key,
                "observation_count": observations,
                "connection_coefficient": round(connection, 6),
                "exploration_bonus": round(exploration, 6),
                "curvature_penalty": round(curvature_penalty * curvature, 6),
                "selection_score": round(score, 6),
                "static_priority_tie_break": int(entry.get("priority", 0)),
                "capability_section_digest": section.get(
                    "capability_section_digest", ""
                ),
            }
        )
    if not candidates:
        blockers.append("no_eligible_capability_adapter")
        return {}, {}, {}
    candidates.sort(
        key=lambda item: (
            -float(item["selection_score"]),
            -int(item["static_priority_tie_break"]),
            str(item["federation_adapter_id"]),
        )
    )
    selected = candidates[0]
    selected_entry = next(
        entry
        for entry in entries
        if entry.get("federation_adapter_id")
        == selected.get("federation_adapter_id")
    )
    packet = {
        "version": SELECTION_VERSION,
        "capability_run_id": capability_run_id,
        "source_batch_digest": wake.get("federated_source_batch_digest", ""),
        "normalized_wake_digest": wake.get("wake_event_digest", ""),
        "capability_bundle_digest": bundle.get("capability_bundle_digest", ""),
        "context_key": context_key,
        "context_signature": context,
        "candidates": candidates,
        "selected_federation_adapter_id": selected.get(
            "federation_adapter_id", ""
        ),
        "selected_adapter_profile_digest": selected.get(
            "adapter_profile_digest", ""
        ),
        "selected_score": selected.get("selection_score", 0.0),
        "static_priority_used_only_as_tie_break": True,
        "capability_estimate_not_truth": True,
    }
    packet["selection_digest"] = selection_digest(packet)
    return packet, dict(selected_entry), dict(mapping(selected_entry.get("adapter_profile")))


def observed_utility(effect: Mapping[str, Any]) -> float:
    outcome_score = {
        "success": 1.0,
        "partial": 0.5,
        "blocked": 0.0,
    }.get(str(effect.get("outcome", "")), 0.0)
    utility = (
        0.35 * clamp(effect.get("observed_benefit"))
        + 0.20 * clamp(effect.get("progress_delta"))
        + 0.20 * clamp(effect.get("recoverability"))
        + 0.15 * clamp(effect.get("confidence"))
        + 0.10 * outcome_score
        - 0.50 * clamp(effect.get("observed_harm"))
    )
    return clamp(utility)


def _mean(previous: float, count: int, observed: float) -> float:
    return round((previous * count + observed) / (count + 1), 6)


def calibrate(
    *,
    capability_run_id: str,
    bundle: Mapping[str, Any],
    selection: Mapping[str, Any],
    selected_profile: Mapping[str, Any],
    effect: Mapping[str, Any],
    federated_evidence_digest: str,
    learning_rate: float,
) -> tuple[dict[str, Any], dict[str, Any], bool]:
    processed = {str(item) for item in as_list(bundle.get("processed_evidence_digests"))}
    if federated_evidence_digest and federated_evidence_digest in processed:
        section = section_for(
            bundle,
            str(selection.get("selected_federation_adapter_id", "")),
            str(selection.get("context_key", "")),
        )
        return dict(bundle), section, True

    adapter_id = str(selection.get("selected_federation_adapter_id", ""))
    context_key = str(selection.get("context_key", ""))
    prior = 0.5
    candidate = next(
        (
            item
            for item in as_list(selection.get("candidates"))
            if mapping(item).get("federation_adapter_id") == adapter_id
        ),
        {},
    )
    prior = clamp(mapping(candidate).get("connection_coefficient"), 0.5)
    old_section = section_for(bundle, adapter_id, context_key) or initial_section(
        adapter_id=adapter_id,
        profile_digest=str(selected_profile.get("adapter_profile_digest", "")),
        context_key=context_key,
        context=mapping(selection.get("context_signature")),
        prior=prior,
    )
    count = integer(old_section.get("observation_count"), 0)
    utility = observed_utility(effect)
    confidence = clamp(effect.get("confidence"))
    alpha = clamp(learning_rate) * confidence
    old_connection = clamp(old_section.get("connection_coefficient"), prior)
    curvature = utility - old_connection
    new_connection = clamp(old_connection + alpha * curvature)
    outcome = str(effect.get("outcome", ""))
    section = dict(old_section)
    section.update(
        {
            "observation_count": count + 1,
            "selection_count": integer(old_section.get("selection_count"), 0) + 1,
            "success_count": integer(old_section.get("success_count"), 0)
            + (1 if outcome == "success" else 0),
            "partial_count": integer(old_section.get("partial_count"), 0)
            + (1 if outcome == "partial" else 0),
            "blocked_count": integer(old_section.get("blocked_count"), 0)
            + (1 if outcome == "blocked" else 0),
            "mean_progress": _mean(
                float(old_section.get("mean_progress", 0.0)),
                count,
                clamp(effect.get("progress_delta")),
            ),
            "mean_benefit": _mean(
                float(old_section.get("mean_benefit", 0.0)),
                count,
                clamp(effect.get("observed_benefit")),
            ),
            "mean_harm": _mean(
                float(old_section.get("mean_harm", 0.0)),
                count,
                clamp(effect.get("observed_harm")),
            ),
            "mean_recoverability": _mean(
                float(old_section.get("mean_recoverability", 0.0)),
                count,
                clamp(effect.get("recoverability")),
            ),
            "mean_confidence": _mean(
                float(old_section.get("mean_confidence", 0.0)),
                count,
                confidence,
            ),
            "mean_utility": _mean(
                float(old_section.get("mean_utility", old_connection)),
                count,
                utility,
            ),
            "connection_coefficient": round(new_connection, 6),
            "last_capability_curvature": round(curvature, 6),
            "cumulative_abs_curvature": round(
                float(old_section.get("cumulative_abs_curvature", 0.0))
                + abs(curvature),
                6,
            ),
            "last_effect_receipt_digest": effect.get("effect_receipt_digest", ""),
            "last_federated_evidence_digest": federated_evidence_digest,
        }
    )
    section["capability_section_digest"] = section_digest(section)

    sections = [
        dict(mapping(item))
        for item in as_list(bundle.get("sections"))
        if not (
            mapping(item).get("federation_adapter_id") == adapter_id
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
    holonomy = as_list(bundle.get("holonomy_trace")) + [
        {
            "capability_run_id": capability_run_id,
            "federation_adapter_id": adapter_id,
            "context_key": context_key,
            "effect_receipt_digest": effect.get("effect_receipt_digest", ""),
            "federated_evidence_digest": federated_evidence_digest,
            "prior_connection": round(old_connection, 6),
            "observed_utility": round(utility, 6),
            "capability_curvature": round(curvature, 6),
            "updated_connection": round(new_connection, 6),
        }
    ]
    updated = {
        "version": BUNDLE_VERSION,
        "agent_id": bundle.get("agent_id", ""),
        "generation": integer(bundle.get("generation"), 0) + 1,
        "sections": sections,
        "holonomy_trace": holonomy,
        "processed_evidence_digests": sorted(
            processed | ({federated_evidence_digest} if federated_evidence_digest else set())
        ),
    }
    updated["capability_bundle_digest"] = bundle_digest(updated)
    calibration = {
        "version": CALIBRATION_VERSION,
        "capability_run_id": capability_run_id,
        "federation_adapter_id": adapter_id,
        "adapter_profile_digest": selected_profile.get("adapter_profile_digest", ""),
        "context_key": context_key,
        "effect_receipt_digest": effect.get("effect_receipt_digest", ""),
        "federated_evidence_digest": federated_evidence_digest,
        "outcome": outcome,
        "prior_connection": round(old_connection, 6),
        "observed_utility": round(utility, 6),
        "effective_learning_rate": round(alpha, 6),
        "capability_curvature": round(curvature, 6),
        "updated_connection": round(new_connection, 6),
        "observation_count": count + 1,
        "capability_section_digest": section.get("capability_section_digest", ""),
        "capability_bundle_digest": updated.get("capability_bundle_digest", ""),
    }
    calibration["calibration_digest"] = calibration_digest(calibration)
    return updated, calibration, False
