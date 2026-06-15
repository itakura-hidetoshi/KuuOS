#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import math
import os
import pathlib
from typing import Any, Mapping

VERSION = "kuuos_adapter_portfolio_shadow_v0_7"
PLAN_VERSION = "kuuos_adapter_portfolio_shadow_plan_v0_7"
LICENSE_VERSION = "kuuos_adapter_portfolio_shadow_license_v0_7"
BUNDLE_VERSION = "kuuos_adapter_portfolio_bundle_v0_7"
SECTION_VERSION = "kuuos_adapter_portfolio_section_v0_7"
SELECTION_VERSION = "kuuos_adapter_portfolio_selection_v0_7"
PROJECTION_VERSION = "kuuos_adapter_shadow_projection_v0_7"
RESOLUTION_VERSION = "kuuos_adapter_shadow_resolution_v0_7"
STATE_VERSION = "kuuos_adapter_portfolio_state_v0_7"
LEDGER_VERSION = "kuuos_adapter_portfolio_ledger_record_v0_7"
READY = "KUUOS_ADAPTER_PORTFOLIO_SHADOW_V0_7_READY"
BLOCKED = "KUUOS_ADAPTER_PORTFOLIO_SHADOW_V0_7_BLOCKED"
REPLAYED = "KUUOS_ADAPTER_PORTFOLIO_SHADOW_V0_7_REPLAYED"

REQUIRED_BOUNDARY = {
    "one_live_adapter_per_cycle": True,
    "one_v0_6_cycle_per_portfolio_run": True,
    "shadow_candidates_non_actuating": True,
    "shadow_candidates_share_live_context": True,
    "shadow_prediction_not_truth": True,
    "shadow_prediction_not_capability_evidence": True,
    "shadow_prediction_does_not_update_v0_6_connection": True,
    "only_realized_shadow_error_updates_portfolio_bias": True,
    "portfolio_adjustment_bounded": True,
    "pending_shadow_prediction_has_no_execution_authority": True,
    "live_effect_digest_exact": True,
    "deterministic_replay_required": True,
    "static_priority_tie_break_only": True,
    "source_authority_unchanged": True,
    "adapter_authority_unchanged": True,
    "external_network_effect_not_inferred": True,
    "non_markov_portfolio_holonomy_preserved": True,
}
FORBIDDEN_GRAPH_KEYS = {"nodes", "edges", "dependencies", "commitment_graph_digest"}


@dataclass(frozen=True)
class AdapterPortfolioShadowResult:
    version: str
    status: str
    packet_id: str
    portfolio_run_id: str
    cycle_index: int
    runtime_root: str
    context_key: str
    live_adapter_id: str
    live_adapter_profile_digest: str
    live_base_score: float
    live_portfolio_adjustment: float
    live_adjusted_score: float
    live_observed_utility: float
    shadow_projection_count: int
    resolved_shadow_count: int
    pending_shadow_count: int
    child_capability_status: str
    child_capability_run_id: str
    live_effect_receipt_digest: str
    portfolio_bundle_digest: str
    idempotent_replay: bool
    recovered_pending_run: bool
    state_path: str
    bundle_path: str
    selection_path: str
    projection_path: str
    resolution_path: str
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


def digest_for(field: str, value: Mapping[str, Any]) -> str:
    return sha(without(value, field))


def plan_digest(value: Mapping[str, Any]) -> str:
    return digest_for("portfolio_plan_digest", value)


def bundle_digest(value: Mapping[str, Any]) -> str:
    return digest_for("portfolio_bundle_digest", value)


def section_digest(value: Mapping[str, Any]) -> str:
    return digest_for("portfolio_section_digest", value)


def selection_digest(value: Mapping[str, Any]) -> str:
    return digest_for("portfolio_selection_digest", value)


def projection_digest(value: Mapping[str, Any]) -> str:
    return digest_for("shadow_projection_digest", value)


def resolution_digest(value: Mapping[str, Any]) -> str:
    return digest_for("shadow_resolution_digest", value)


def state_digest(value: Mapping[str, Any]) -> str:
    return digest_for("portfolio_state_digest", value)


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
