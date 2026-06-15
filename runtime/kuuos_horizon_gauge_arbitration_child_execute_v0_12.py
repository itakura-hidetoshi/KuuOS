#!/usr/bin/env python3
from __future__ import annotations
from typing import Any, Mapping
from runtime.kuuos_delayed_credit_multihorizon_cycle_v0_11 import build_delayed_credit_multihorizon
from runtime.kuuos_delayed_credit_multihorizon_types_v0_11 import OUTCOME_VERSION, READY, REPLAYED, outcome_digest
from runtime.kuuos_horizon_gauge_arbitration_types_v0_12 import as_list, read_json

def execute_child(*, root: Any, context: Mapping[str, Any], sources: list[Mapping[str, Any]], root_packet: Mapping[str, Any], registry: Mapping[str, Any], child_plan: Mapping[str, Any], child_license: Mapping[str, Any], paths: Mapping[str, Any], blockers: list[str]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    child = build_delayed_credit_multihorizon(
        runtime_context={
            "runtime_root": str(root),
            "delayed_credit_multihorizon_enabled": True,
            "execute_one_horizon_cycle": True,
            "allowed_domain_actions": as_list(context.get("allowed_domain_actions")),
        },
        source_packets=sources,
        root_principles_packet=root_packet,
        adapter_registry=registry,
        horizon_plan=child_plan,
        horizon_license=child_license,
    )
    result = child.to_dict()
    if child.status not in {READY, REPLAYED}:
        blockers.extend([f"horizon_{item}" for item in child.blockers])
    horizon_bundle = read_json(paths["horizon_bundle"])
    horizon_outcome = read_json(paths["horizon_outcome"])
    gauge_bundle = read_json(paths["gauge_bundle"])
    if not blockers:
        if horizon_outcome.get("version") != OUTCOME_VERSION:
            blockers.append("child_horizon_outcome_version_invalid")
        if horizon_outcome.get("horizon_outcome_digest") != outcome_digest(horizon_outcome):
            blockers.append("child_horizon_outcome_digest_invalid")
        if horizon_bundle.get("horizon_bundle_digest") != result.get("horizon_bundle_digest"):
            blockers.append("child_horizon_bundle_digest_mismatch")
        if horizon_outcome.get("child_effect_receipt_digest") != result.get("child_effect_receipt_digest"):
            blockers.append("child_effect_receipt_digest_mismatch")
    return result, horizon_bundle, horizon_outcome, gauge_bundle
