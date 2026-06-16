from __future__ import annotations
from typing import Any, Mapping
from runtime.kuuos_context_gauge_atlas_types_v0_13 import LICENSE_VERSION


def check_license(*, license_packet: Mapping[str, Any], plan: Mapping[str, Any], atlas_bundle: Mapping[str, Any], source_batch_digest: str, root_digest: str, registry_digest: str, blockers: list[str]) -> None:
    if license_packet.get("version") != LICENSE_VERSION:
        blockers.append("atlas_license_version_invalid")
    bindings = {
        "bound_atlas_plan_digest": plan.get("atlas_plan_digest", ""),
        "bound_source_batch_digest": source_batch_digest,
        "bound_root_principles_digest": root_digest,
        "bound_adapter_registry_digest": registry_digest,
        "bound_previous_atlas_bundle_digest": atlas_bundle.get("atlas_bundle_digest", ""),
    }
    for field, value in bindings.items():
        if license_packet.get(field) != value:
            blockers.append(f"atlas_license_{field}_mismatch")
    required = (
        "source_read_allowed", "atlas_read_allowed", "atlas_transport_allowed",
        "one_local_cycle_allowed", "atlas_bundle_write_allowed",
        "atlas_state_write_allowed", "decision_write_allowed",
        "outcome_write_allowed", "child_packet_write_allowed",
        "ledger_append_allowed", "receipt_write_allowed", "audit_append_allowed",
    )
    for field in required:
        if license_packet.get(field) is not True:
            blockers.append(field.replace("allowed", "not_allowed"))
    denied = (
        "multiple_local_cycles_allowed", "chart_locality_bypass_allowed",
        "cocycle_veto_allowed", "external_network_effect_allowed",
        "world_update_allowed", "memory_overwrite_allowed",
    )
    for field in denied:
        if license_packet.get(field) is not False:
            blockers.append(field.replace("allowed", "not_denied"))
