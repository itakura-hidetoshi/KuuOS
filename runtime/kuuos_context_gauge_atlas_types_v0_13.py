#!/usr/bin/env python3
from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Any, Mapping
from runtime.kuuos_horizon_gauge_arbitration_types_v0_12 import append_jsonl, as_list, clamp, contains_graph_keys, integer, mapping, nonnegative, read_json, read_jsonl, safe_root, sha, without, write_json

VERSION = "kuuos_context_gauge_atlas_v0_13"
PLAN_VERSION = "kuuos_context_gauge_atlas_plan_v0_13"
LICENSE_VERSION = "kuuos_context_gauge_atlas_license_v0_13"
BUNDLE_VERSION = "kuuos_context_gauge_atlas_bundle_v0_13"
CHART_VERSION = "kuuos_context_gauge_atlas_chart_v0_13"
DECISION_VERSION = "kuuos_context_gauge_atlas_decision_v0_13"
OUTCOME_VERSION = "kuuos_context_gauge_atlas_outcome_v0_13"
STATE_VERSION = "kuuos_context_gauge_atlas_state_v0_13"
LEDGER_VERSION = "kuuos_context_gauge_atlas_ledger_record_v0_13"
READY = "KUUOS_CONTEXT_GAUGE_ATLAS_V0_13_READY"
BLOCKED = "KUUOS_CONTEXT_GAUGE_ATLAS_V0_13_BLOCKED"
REPLAYED = "KUUOS_CONTEXT_GAUGE_ATLAS_V0_13_REPLAYED"
HORIZONS = ("short", "medium", "long")

REQUIRED_BOUNDARY = {
    "contexts_are_local_charts": True,
    "transition_functions_require_overlap": True,
    "atlas_parallel_transport_enabled": True,
    "cocycle_defect_is_not_a_veto": True,
    "chart_locality_preserved": True,
    "one_v0_12_child_cycle_per_atlas_run": True,
    "effect_grounded_chart_update": True,
    "deterministic_replay_required": True,
    "atlas_holonomy_preserved": True,
    "graph_semantics_forbidden": True,
}

@dataclass(frozen=True)
class ContextGaugeAtlasResult:
    version: str
    status: str
    packet_id: str
    atlas_run_id: str
    cycle_index: int
    runtime_root: str
    target_context_key: str
    atlas_class: str
    compatible_chart_count: int
    atlas_curvature: float
    cocycle_defect: float
    transported_short_weight: float
    transported_medium_weight: float
    transported_long_weight: float
    child_arbitration_class: str
    child_commitment_outcome_class: str
    child_policy_mode: str
    child_live_adapter_id: str
    child_live_domain_action: str
    atlas_bundle_digest: str
    child_arbitration_bundle_digest: str
    child_arbitration_outcome_digest: str
    child_effect_receipt_digest: str
    idempotent_replay: bool
    recovered_pending_run: bool
    state_path: str
    bundle_path: str
    decision_path: str
    outcome_path: str
    child_plan_path: str
    child_license_path: str
    receipt_path: str
    ledger_path: str
    audit_path: str
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

def valid_digest(value: Mapping[str, Any], field: str) -> bool:
    digest = str(value.get(field, ""))
    return bool(digest) and digest == sha(without(value, field))

def plan_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "atlas_plan_digest"))

def bundle_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "atlas_bundle_digest"))

def chart_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "chart_digest"))

def decision_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "atlas_decision_digest"))

def outcome_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "atlas_outcome_digest"))

def state_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "atlas_state_digest"))
