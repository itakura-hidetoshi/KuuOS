#!/usr/bin/env python3
from __future__ import annotations

import pathlib
from typing import Any, Mapping

from runtime.kuuos_open_horizon_commitment_gauge_core_v0_2 import (
    EFFECT_VERSION,
    effect_digest,
)
from runtime.kuuos_event_adapter_federation_core_v0_5 import (
    BLOCKED as FEDERATION_BLOCKED,
    READY as FEDERATION_READY,
    REPLAYED as FEDERATION_REPLAYED,
    build_event_adapter_federation,
)
from runtime.kuuos_event_adapter_federation_types_v0_5 import (
    EVIDENCE_VERSION,
    evidence_digest,
)
from runtime.kuuos_adapter_capability_federation_bridge_v0_6 import (
    build_child_packets,
)
from runtime.kuuos_adapter_capability_gauge_types_v0_6 import as_list, mapping, read_json


def run_federation_child(
    *,
    root: pathlib.Path,
    runtime_context: Mapping[str, Any],
    capability_plan: Mapping[str, Any],
    source_packets: list[Mapping[str, Any]],
    root_principles_packet: Mapping[str, Any],
    registry: Mapping[str, Any],
    selection: Mapping[str, Any],
    selected_entry: Mapping[str, Any],
    selected_profile: Mapping[str, Any],
    previous_federation_state: Mapping[str, Any],
    blockers: list[str],
) -> dict[str, Any]:
    child_registry, child_plan, child_license = build_child_packets(
        capability_plan=capability_plan,
        source_packets=source_packets,
        root_principles_packet=root_principles_packet,
        selected_entry=selected_entry,
        selection=selection,
        registry=registry,
        previous_federation_state=previous_federation_state,
    )
    raw = build_event_adapter_federation(
        runtime_context={
            "runtime_root": str(root),
            "event_adapter_federation_enabled": True,
            "execute_one_federated_cycle": True,
            "allowed_domain_actions": as_list(
                runtime_context.get("allowed_domain_actions")
            ),
        },
        source_packets=source_packets,
        root_principles_packet=root_principles_packet,
        adapter_registry=child_registry,
        federation_plan=child_plan,
        federation_license=child_license,
    )
    result = raw.to_dict()
    if raw.status == FEDERATION_BLOCKED:
        blockers.extend([f"federation_{item}" for item in raw.blockers])
    elif raw.status not in {FEDERATION_READY, FEDERATION_REPLAYED}:
        blockers.append("federation_child_status_unknown")
    if result.get("selected_federation_adapter_id") != selection.get(
        "selected_federation_adapter_id"
    ):
        blockers.append("capability_selection_child_adapter_mismatch")
    if result.get("selected_adapter_profile_digest") != selected_profile.get(
        "adapter_profile_digest"
    ):
        blockers.append("capability_selection_child_profile_mismatch")
    return result


def validate_child_evidence_and_effect(
    *,
    root: pathlib.Path,
    child_result: Mapping[str, Any],
    require_effect: bool,
    blockers: list[str],
) -> tuple[dict[str, Any], dict[str, Any]]:
    evidence = read_json(root / "kuuos_federated_effect_evidence_v0_5.json")
    if evidence.get("version") != EVIDENCE_VERSION:
        blockers.append("federated_evidence_version_invalid")
    elif evidence.get("evidence_digest") != evidence_digest(evidence):
        blockers.append("federated_evidence_digest_invalid")
    if evidence.get("evidence_digest") != child_result.get("evidence_digest"):
        blockers.append("federated_evidence_result_mismatch")

    effect = read_json(root / "kuuos_active_gauge_effect_receipt_v0_3.json")
    intervention_applied = child_result.get("intervention_applied") is True
    if require_effect and not intervention_applied:
        blockers.append("capability_cycle_effect_observation_missing")
    if intervention_applied:
        if effect.get("version") != EFFECT_VERSION:
            blockers.append("capability_effect_version_invalid")
        elif effect.get("effect_receipt_digest") != effect_digest(effect):
            blockers.append("capability_effect_digest_invalid")
        if effect.get("effect_receipt_digest") != child_result.get(
            "effect_receipt_digest"
        ):
            blockers.append("capability_effect_result_mismatch")
        if effect.get("adapter_execution_committed") is not True:
            blockers.append("capability_effect_not_committed")
    return evidence, effect
