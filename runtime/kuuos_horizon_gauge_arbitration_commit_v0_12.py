#!/usr/bin/env python3
from __future__ import annotations
from typing import Any, Mapping
from runtime.kuuos_horizon_gauge_arbitration_bundle_update_v0_12 import update_bundle
from runtime.kuuos_horizon_gauge_arbitration_outcome_packet_v0_12 import build_outcome_packet
from runtime.kuuos_horizon_gauge_arbitration_section_update_v0_12 import update_arbitration_section
from runtime.kuuos_horizon_gauge_arbitration_types_v0_12 import as_list, mapping

def commit_arbitration_outcome(*, arbitration_run_id: str, cycle_index: int, previous_bundle: Mapping[str, Any], child_horizon_bundle: Mapping[str, Any], child_horizon_outcome: Mapping[str, Any], decision: Mapping[str, Any], gauge_bundle: Mapping[str, Any], plan: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any], bool]:
    child_digest = str(child_horizon_outcome.get("horizon_outcome_digest", ""))
    processed = {str(item) for item in as_list(previous_bundle.get("processed_child_horizon_outcome_digests"))}
    if child_digest in processed:
        existing = next((dict(mapping(item)) for item in reversed(as_list(previous_bundle.get("outcomes"))) if mapping(item).get("child_horizon_outcome_digest") == child_digest), {})
        return dict(previous_bundle), existing, True
    outcome = build_outcome_packet(
        arbitration_run_id=arbitration_run_id,
        cycle_index=cycle_index,
        child_horizon_bundle=child_horizon_bundle,
        child_horizon_outcome=child_horizon_outcome,
        decision=decision,
        gauge_bundle=gauge_bundle,
        plan=plan,
    )
    section = update_arbitration_section(
        previous_bundle=previous_bundle,
        decision=decision,
        outcome=outcome,
    )
    updated = update_bundle(
        previous_bundle=previous_bundle,
        section=section,
        outcome=outcome,
        child_horizon_bundle=child_horizon_bundle,
        gauge_bundle=gauge_bundle,
        plan=plan,
    )
    return updated, outcome, False
