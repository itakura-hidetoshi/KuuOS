#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
from typing import Any, Mapping

VERSION = "kuuos_active_gauge_intervention_loop_v0_3"
PLAN_VERSION = "kuuos_active_gauge_intervention_plan_v0_3"
LICENSE_VERSION = "kuuos_active_gauge_intervention_license_v0_3"
ADAPTER_PROFILE_VERSION = "kuuos_active_gauge_adapter_profile_v0_3"
STATE_VERSION = "kuuos_active_gauge_intervention_state_v0_3"
LEDGER_VERSION = "kuuos_active_gauge_intervention_ledger_record_v0_3"
READY = "KUUOS_ACTIVE_GAUGE_INTERVENTION_LOOP_V0_3_READY"
BLOCKED = "KUUOS_ACTIVE_GAUGE_INTERVENTION_LOOP_V0_3_BLOCKED"
REPLAYED = "KUUOS_ACTIVE_GAUGE_INTERVENTION_LOOP_V0_3_REPLAYED"

DEFAULT_ROUTING = {
    "covariant_advance": "advance_tick",
    "covariant_micro_intervention": "observe",
    "curvature_probe": "observe",
    "effect_integration_transport": "advance_tick",
    "scaled_parallel_transport": "advance_tick",
    "local_repair_gauge": "observe",
    "chart_transition": "handover",
    "curvature_reobservation": "observe",
    "section_extension": "advance_tick",
    "handover_or_redesign": "handover",
}
LOCAL_ACTIONS = {"advance_tick", "notify", "ticket", "handover", "hold", "observe", "freeze"}
FORBIDDEN_GRAPH_KEYS = {"nodes", "edges", "dependencies", "commitment_graph_digest"}
REQUIRED_BOUNDARY = {
    "active_domain_intervention": True,
    "covariant_action_is_executable_intent": True,
    "exact_action_binding": True,
    "adapter_effect_is_observed_evidence": True,
    "effect_receipt_generated": True,
    "immediate_gauge_reentry": True,
    "next_covariant_action_continues_loop": True,
    "idempotent_intervention": True,
    "local_adapter_initial_backend": True,
    "external_adapter_replaceable": True,
    "non_markov_holonomy_preserved": True,
    "candidate_weighting_not_truth": True,
}


@dataclass(frozen=True)
class ActiveGaugeInterventionResult:
    version: str
    status: str
    packet_id: str
    intervention_run_id: str
    intervention_id: str
    runtime_root: str
    adapter_id: str
    covariant_step_kind: str
    routed_domain_action: str
    source_action_digest: str
    local_execution_committed: bool
    local_execution_id: str
    effect_receipt_ready: bool
    effect_receipt_digest: str
    effect_outcome: str
    curvature_reentry_applied: bool
    gauge_reentry_status: str
    next_action_ready: bool
    next_covariant_step_kind: str
    next_action_digest: str
    idempotent_replay: bool
    recovered_pending_run: bool
    state_path: str
    effect_receipt_path: str
    receipt_path: str
    ledger_path: str
    audit_path: str
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def sha(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    output = dict(value)
    output.pop(field, None)
    return output


def valid_digest(value: Mapping[str, Any], field: str) -> bool:
    digest = str(value.get(field, ""))
    return bool(digest) and digest == sha(without(value, field))


def plan_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "intervention_plan_digest"))


def profile_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "adapter_profile_digest"))


def state_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "intervention_state_digest"))


def integer(value: Any, default: int = 0) -> int:
    if isinstance(value, bool):
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def clamp(value: Any, default: float = 0.0) -> float:
    if isinstance(value, bool):
        return default
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return max(0.0, min(1.0, number))


def read_json(path: pathlib.Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return dict(value) if isinstance(value, Mapping) else {}


def read_jsonl(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    output: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            value = {"_invalid": True}
        output.append(dict(value) if isinstance(value, Mapping) else {"_invalid": True})
    return output


def write_json(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def append_jsonl(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")


def safe_root(value: Any, blockers: list[str]) -> pathlib.Path:
    if not value:
        blockers.append("runtime_root_missing")
        return pathlib.Path(".").resolve()
    root = pathlib.Path(str(value)).expanduser().resolve()
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")
    return root


def contains_graph_keys(value: Any) -> bool:
    if isinstance(value, Mapping):
        if FORBIDDEN_GRAPH_KEYS.intersection(value.keys()):
            return True
        return any(contains_graph_keys(child) for child in value.values())
    if isinstance(value, list):
        return any(contains_graph_keys(child) for child in value)
    return False
