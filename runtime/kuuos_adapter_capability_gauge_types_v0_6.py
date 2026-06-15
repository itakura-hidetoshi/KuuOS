#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import math
import os
import pathlib
from typing import Any, Mapping

VERSION = "kuuos_adapter_capability_gauge_v0_6"
PLAN_VERSION = "kuuos_adapter_capability_gauge_plan_v0_6"
LICENSE_VERSION = "kuuos_adapter_capability_gauge_license_v0_6"
BUNDLE_VERSION = "kuuos_adapter_capability_bundle_v0_6"
SECTION_VERSION = "kuuos_adapter_capability_section_v0_6"
SELECTION_VERSION = "kuuos_adapter_capability_selection_v0_6"
CALIBRATION_VERSION = "kuuos_adapter_capability_calibration_v0_6"
STATE_VERSION = "kuuos_adapter_capability_state_v0_6"
LEDGER_VERSION = "kuuos_adapter_capability_ledger_record_v0_6"
READY = "KUUOS_ADAPTER_CAPABILITY_GAUGE_V0_6_READY"
BLOCKED = "KUUOS_ADAPTER_CAPABILITY_GAUGE_V0_6_BLOCKED"
REPLAYED = "KUUOS_ADAPTER_CAPABILITY_GAUGE_V0_6_REPLAYED"

REQUIRED_BOUNDARY = {
    "context_local_capability_sections": True,
    "observed_effect_updates_connection": True,
    "effect_difference_is_capability_curvature": True,
    "static_priority_tie_break_only": True,
    "bounded_exploration_bonus": True,
    "single_adapter_selection_per_cycle": True,
    "one_v0_5_cycle_per_capability_run": True,
    "shared_gauge_evidence_preserved": True,
    "capability_estimate_not_truth": True,
    "source_authority_unchanged": True,
    "adapter_authority_unchanged": True,
    "external_network_effect_not_inferred": True,
    "non_markov_holonomy_preserved": True,
}
FORBIDDEN_GRAPH_KEYS = {"nodes", "edges", "dependencies", "commitment_graph_digest"}


@dataclass(frozen=True)
class AdapterCapabilityGaugeResult:
    version: str
    status: str
    packet_id: str
    capability_run_id: str
    cycle_index: int
    runtime_root: str
    context_key: str
    selected_federation_adapter_id: str
    selected_adapter_profile_digest: str
    selection_score: float
    prior_connection: float
    observed_utility: float
    updated_connection: float
    capability_curvature: float
    observation_count: int
    child_federation_status: str
    child_federation_run_id: str
    child_evidence_digest: str
    effect_receipt_digest: str
    next_wake_digest: str
    idempotent_replay: bool
    recovered_pending_run: bool
    state_path: str
    bundle_path: str
    selection_path: str
    calibration_path: str
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
    return sha(without(value, "capability_plan_digest"))


def bundle_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "capability_bundle_digest"))


def section_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "capability_section_digest"))


def selection_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "selection_digest"))


def calibration_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "calibration_digest"))


def state_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "capability_state_digest"))


def clamp(value: Any, default: float = 0.0) -> float:
    if isinstance(value, bool):
        return default
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    if not math.isfinite(number):
        return default
    return max(0.0, min(1.0, number))


def signed(value: Any, default: float = 0.0) -> float:
    if isinstance(value, bool):
        return default
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    if not math.isfinite(number):
        return default
    return max(-1.0, min(1.0, number))


def integer(value: Any, default: int = 0) -> int:
    if isinstance(value, bool):
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


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
