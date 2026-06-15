#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_open_horizon_telos_genesis_core_v0_1 import ALLOWED_SIGNAL_KINDS
from runtime.kuuos_active_gauge_intervention_types_v0_3 import (
    ADAPTER_PROFILE_VERSION,
    LOCAL_ACTIONS,
    valid_digest as valid_adapter_digest,
)
from runtime.kuuos_renewable_gauge_supervisor_types_v0_4 import (
    WAKE_VERSION,
    wake_digest,
)
from runtime.kuuos_event_adapter_federation_types_v0_5 import (
    ALLOWED_SOURCE_KINDS,
    REGISTRY_VERSION,
    RENEWAL_SOURCE_KINDS,
    SOURCE_VERSION,
    WAKE_KIND_ORDER,
    as_list,
    batch_digest,
    clamp,
    mapping,
    sha,
    valid_digest,
)


def validate_source_packets(
    source_packets: list[Mapping[str, Any]],
    *,
    max_sources: int,
    max_signals_per_source: int,
    max_total_signals: int,
    blockers: list[str],
) -> None:
    if not source_packets:
        blockers.append("source_packets_missing")
        return
    if len(source_packets) > max_sources:
        blockers.append("source_count_exceeds_limit")
    source_ids: set[str] = set()
    event_keys: set[tuple[str, str]] = set()
    total_signals = 0
    for raw in source_packets:
        packet = mapping(raw)
        if packet.get("version") != SOURCE_VERSION:
            blockers.append("source_packet_version_invalid")
        if not valid_digest(packet, "source_packet_digest"):
            blockers.append("source_packet_digest_invalid")
        source_id = str(packet.get("source_id", ""))
        event_id = str(packet.get("source_event_id", ""))
        if not source_id:
            blockers.append("source_id_missing")
        if not event_id:
            blockers.append("source_event_id_missing")
        if source_id in source_ids:
            blockers.append("source_id_repeated_in_batch")
        source_ids.add(source_id)
        key = (source_id, event_id)
        if key in event_keys:
            blockers.append("source_event_repeated_in_batch")
        event_keys.add(key)
        kind = str(packet.get("source_kind", ""))
        if kind not in ALLOWED_SOURCE_KINDS:
            blockers.append("source_kind_invalid")
        for field in ("trust_weight", "priority"):
            if clamp(packet.get(field), -1.0) < 0.0:
                blockers.append(f"source_{field}_invalid")
        if packet.get("telos_renewal_requested") not in {True, False}:
            blockers.append("source_telos_renewal_requested_invalid")
        if packet.get("intervention_requested") not in {True, False}:
            blockers.append("source_intervention_requested_invalid")
        signals = as_list(packet.get("signals"))
        total_signals += len(signals)
        if len(signals) > max_signals_per_source:
            blockers.append("source_signal_count_exceeds_limit")
        signal_ids: set[str] = set()
        for raw_signal in signals:
            signal = mapping(raw_signal)
            signal_id = str(signal.get("signal_id", ""))
            if not signal_id or signal_id in signal_ids:
                blockers.append("source_signal_id_missing_or_repeated")
            signal_ids.add(signal_id)
            if str(signal.get("kind", "")) not in ALLOWED_SIGNAL_KINDS:
                blockers.append("source_signal_kind_invalid")
            if not str(signal.get("target", "")).strip():
                blockers.append("source_signal_target_missing")
            for field in (
                "magnitude", "urgency", "evidence", "uncertainty",
                "irreversibility", "recoverability", "relational_benefit", "autonomy_gain",
            ):
                if clamp(signal.get(field), -1.0) < 0.0:
                    blockers.append(f"source_signal_{field}_invalid")
    if total_signals > max_total_signals:
        blockers.append("total_signal_count_exceeds_limit")


def validate_adapter_registry(
    registry: Mapping[str, Any],
    blockers: list[str],
) -> None:
    if registry.get("version") != REGISTRY_VERSION:
        blockers.append("adapter_registry_version_invalid")
    if not valid_digest(registry, "adapter_registry_digest"):
        blockers.append("adapter_registry_digest_invalid")
    if not str(registry.get("registry_id", "")):
        blockers.append("adapter_registry_id_missing")
    adapters = as_list(registry.get("adapters"))
    if not adapters:
        blockers.append("adapter_registry_empty")
        return
    federation_ids: set[str] = set()
    profile_ids: set[str] = set()
    for raw in adapters:
        entry = mapping(raw)
        federation_id = str(entry.get("federation_adapter_id", ""))
        if not federation_id or federation_id in federation_ids:
            blockers.append("federation_adapter_id_missing_or_repeated")
        federation_ids.add(federation_id)
        if entry.get("enabled") not in {True, False}:
            blockers.append("federation_adapter_enabled_invalid")
        priority = entry.get("priority")
        if isinstance(priority, bool):
            blockers.append("federation_adapter_priority_invalid")
        else:
            try:
                int(priority)
            except (TypeError, ValueError):
                blockers.append("federation_adapter_priority_invalid")
        kinds = {str(item) for item in as_list(entry.get("accepted_source_kinds"))}
        if not kinds or not kinds.issubset(ALLOWED_SOURCE_KINDS):
            blockers.append("federation_adapter_source_kinds_invalid")
        if entry.get("external_network_effect_allowed") is not False:
            blockers.append("federation_adapter_external_network_effect_not_denied")
        profile = mapping(entry.get("adapter_profile"))
        if profile.get("version") != ADAPTER_PROFILE_VERSION:
            blockers.append("federation_adapter_profile_version_invalid")
        if not valid_adapter_digest(profile, "adapter_profile_digest"):
            blockers.append("federation_adapter_profile_digest_invalid")
        profile_id = str(profile.get("adapter_id", ""))
        if not profile_id or profile_id in profile_ids:
            blockers.append("federation_adapter_profile_id_missing_or_repeated")
        profile_ids.add(profile_id)
        if profile.get("backend") != "qi_local_execution_adapter_v0_2":
            blockers.append("federation_adapter_backend_unsupported")
        supported = {str(item) for item in as_list(profile.get("supported_domain_actions"))}
        if not supported or not supported.issubset(LOCAL_ACTIONS):
            blockers.append("federation_adapter_actions_invalid")


def _source_sort_key(packet: Mapping[str, Any]) -> tuple[Any, ...]:
    kind = str(packet.get("source_kind", "manual"))
    try:
        kind_index = WAKE_KIND_ORDER.index(kind)
    except ValueError:
        kind_index = len(WAKE_KIND_ORDER)
    return (
        -clamp(packet.get("priority")),
        -clamp(packet.get("trust_weight")),
        kind_index,
        str(packet.get("source_id", "")),
        str(packet.get("source_event_id", "")),
    )


def normalize_sources(source_packets: list[Mapping[str, Any]]) -> dict[str, Any]:
    ordered = sorted((dict(mapping(item)) for item in source_packets), key=_source_sort_key)
    source_batch = batch_digest(ordered)
    dominant_kind = str(ordered[0].get("source_kind", "manual"))
    normalized_signals: list[dict[str, Any]] = []
    provenance: list[dict[str, Any]] = []
    for packet in ordered:
        source_id = str(packet.get("source_id", ""))
        event_id = str(packet.get("source_event_id", ""))
        trust = clamp(packet.get("trust_weight"))
        priority = clamp(packet.get("priority"))
        provenance.append(
            {
                "source_id": source_id,
                "source_event_id": event_id,
                "source_kind": packet.get("source_kind"),
                "source_packet_digest": packet.get("source_packet_digest"),
                "trust_weight": trust,
                "priority": priority,
            }
        )
        for raw_signal in sorted(
            as_list(packet.get("signals")),
            key=lambda item: str(mapping(item).get("signal_id", "")),
        ):
            signal = dict(mapping(raw_signal))
            signal_id = str(signal.get("signal_id", ""))
            signal["signal_id"] = f"{source_id}:{signal_id}"
            signal["evidence"] = round(clamp(signal.get("evidence")) * trust, 6)
            signal["source_id"] = source_id
            signal["source_event_id"] = event_id
            signal["source_packet_digest"] = packet.get("source_packet_digest")
            signal["source_priority"] = priority
            signal["source_trust_weight"] = trust
            normalized_signals.append(signal)
    context_lineage = [
        {
            "source_id": str(packet.get("source_id", "")),
            "world": str(packet.get("world_context_digest", "")),
            "process": str(packet.get("process_tensor_context_digest", "")),
            "memory": str(packet.get("non_markov_context_digest", "")),
        }
        for packet in ordered
    ]
    wake = {
        "version": WAKE_VERSION,
        "wake_event_id": "federated-wake-" + source_batch[:18],
        "wake_kind": dominant_kind,
        "world_context_digest": sha({"kind": "world", "lineage": context_lineage}),
        "process_tensor_context_digest": sha({"kind": "process", "lineage": context_lineage}),
        "non_markov_context_digest": sha({"kind": "memory", "lineage": context_lineage}),
        "signals": normalized_signals,
        "telos_renewal_requested": any(
            packet.get("telos_renewal_requested") is True
            or str(packet.get("source_kind", "")) in RENEWAL_SOURCE_KINDS
            for packet in ordered
        ),
        "intervention_requested": any(
            packet.get("intervention_requested") is True for packet in ordered
        ),
        "federated_source_batch_digest": source_batch,
        "federated_source_provenance": provenance,
    }
    wake["wake_event_digest"] = wake_digest(wake)
    return wake


def select_adapter(
    registry: Mapping[str, Any],
    source_packets: list[Mapping[str, Any]],
    wake: Mapping[str, Any],
    blockers: list[str],
) -> tuple[dict[str, Any], dict[str, Any]]:
    source_ids = {str(packet.get("source_id", "")) for packet in source_packets}
    source_kinds = {str(packet.get("source_kind", "")) for packet in source_packets}
    dominant_kind = str(wake.get("wake_kind", ""))
    candidates: list[tuple[tuple[Any, ...], dict[str, Any], dict[str, Any]]] = []
    for raw in as_list(registry.get("adapters")):
        entry = dict(mapping(raw))
        if entry.get("enabled") is not True:
            continue
        accepted_kinds = {str(item) for item in as_list(entry.get("accepted_source_kinds"))}
        accepted_ids = {str(item) for item in as_list(entry.get("accepted_source_ids"))}
        if dominant_kind not in accepted_kinds:
            continue
        if accepted_ids and not source_ids.intersection(accepted_ids):
            continue
        profile = dict(mapping(entry.get("adapter_profile")))
        kind_coverage = len(source_kinds.intersection(accepted_kinds))
        id_coverage = len(source_ids.intersection(accepted_ids)) if accepted_ids else 0
        action_coverage = len(as_list(profile.get("supported_domain_actions")))
        score = (
            -id_coverage,
            -kind_coverage,
            -int(entry.get("priority", 0)),
            -action_coverage,
            str(entry.get("federation_adapter_id", "")),
        )
        candidates.append((score, entry, profile))
    if not candidates:
        blockers.append("no_eligible_federated_adapter")
        return {}, {}
    candidates.sort(key=lambda item: item[0])
    _, entry, profile = candidates[0]
    return entry, profile
