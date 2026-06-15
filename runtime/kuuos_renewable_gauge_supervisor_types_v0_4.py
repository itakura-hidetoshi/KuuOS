#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
from typing import Any, Mapping

VERSION = "kuuos_renewable_gauge_supervisor_v0_4"
WAKE_VERSION = "kuuos_renewable_gauge_wake_event_v0_4"
PLAN_VERSION = "kuuos_renewable_gauge_supervisor_plan_v0_4"
LICENSE_VERSION = "kuuos_renewable_gauge_supervisor_license_v0_4"
STATE_VERSION = "kuuos_renewable_gauge_supervisor_state_v0_4"
NEXT_WAKE_VERSION = "kuuos_renewable_gauge_next_wake_v0_4"
LEDGER_VERSION = "kuuos_renewable_gauge_supervisor_ledger_record_v0_4"
READY = "KUUOS_RENEWABLE_GAUGE_SUPERVISOR_V0_4_READY"
BLOCKED = "KUUOS_RENEWABLE_GAUGE_SUPERVISOR_V0_4_BLOCKED"
REPLAYED = "KUUOS_RENEWABLE_GAUGE_SUPERVISOR_V0_4_REPLAYED"

ALLOWED_WAKE_KINDS = {
    "bootstrap", "observation", "timer", "effect_followup",
    "resource_change", "relationship_change", "recovery", "manual",
}
RENEWAL_WAKE_KINDS = {
    "bootstrap", "observation", "resource_change", "relationship_change", "recovery",
}
REQUIRED_BOUNDARY = {
    "wake_driven_supervision": True,
    "one_finite_cycle_per_invocation": True,
    "at_most_one_local_intervention": True,
    "telos_renewal_when_context_changes": True,
    "gauge_bundle_extended_not_replaced": True,
    "curvature_feedback_reenters_same_field": True,
    "next_wake_is_explicit": True,
    "local_recovery_idempotent": True,
    "root_principles_unchanged": True,
    "non_markov_holonomy_preserved": True,
    "candidate_weighting_not_truth": True,
}
FORBIDDEN_GRAPH_KEYS = {"nodes", "edges", "dependencies", "commitment_graph_digest"}


@dataclass(frozen=True)
class RenewableGaugeSupervisorResult:
    version: str
    status: str
    packet_id: str
    supervisor_run_id: str
    cycle_index: int
    runtime_root: str
    wake_event_id: str
    wake_kind: str
    telos_renewal_applied: bool
    telos_generation: int
    gauge_synchronization_applied: bool
    intervention_applied: bool
    intervention_status: str
    effect_receipt_digest: str
    next_action_ready: bool
    next_action_digest: str
    next_wake_kind: str
    next_wake_digest: str
    local_steps_since_telos: int
    total_interventions: int
    idempotent_replay: bool
    recovered_pending_run: bool
    state_path: str
    next_wake_path: str
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


def wake_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "wake_event_digest"))


def plan_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "supervisor_plan_digest"))


def state_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "supervisor_state_digest"))


def next_wake_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "next_wake_digest"))


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
