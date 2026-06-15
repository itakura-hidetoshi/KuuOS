#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import math
import os
import pathlib
from typing import Any, Mapping

VERSION = "kuuos_bounded_portfolio_experiment_v0_8"
PLAN_VERSION = "kuuos_bounded_portfolio_experiment_plan_v0_8"
LICENSE_VERSION = "kuuos_bounded_portfolio_experiment_license_v0_8"
BUNDLE_VERSION = "kuuos_bounded_portfolio_experiment_bundle_v0_8"
DECISION_VERSION = "kuuos_bounded_portfolio_experiment_decision_v0_8"
TRIAL_VERSION = "kuuos_bounded_portfolio_trial_record_v0_8"
STATE_VERSION = "kuuos_bounded_portfolio_experiment_state_v0_8"
LEDGER_VERSION = "kuuos_bounded_portfolio_experiment_ledger_record_v0_8"
READY = "KUUOS_BOUNDED_PORTFOLIO_EXPERIMENT_V0_8_READY"
BLOCKED = "KUUOS_BOUNDED_PORTFOLIO_EXPERIMENT_V0_8_BLOCKED"
REPLAYED = "KUUOS_BOUNDED_PORTFOLIO_EXPERIMENT_V0_8_REPLAYED"

REQUIRED_BOUNDARY = {
    "v0_7_portfolio_seed_read_only": True,
    "v0_8_working_portfolio_isolated": True,
    "one_live_adapter_per_cycle": True,
    "one_v0_6_cycle_per_experiment_run": True,
    "experiment_override_requires_information_gain": True,
    "experiment_override_requires_exact_license": True,
    "experiment_budget_finite": True,
    "experiment_cost_debited_only_after_live_effect": True,
    "experiment_trial_count_bounded": True,
    "experiment_cooldown_enforced": True,
    "experiment_risk_bounded": True,
    "experiment_recoverability_floor_enforced": True,
    "baseline_exploitation_preserved_when_trial_ineligible": True,
    "shadow_candidates_non_actuating": True,
    "shadow_prediction_not_truth": True,
    "shadow_prediction_not_capability_evidence": True,
    "only_live_effect_updates_v0_6_capability": True,
    "only_realized_shadow_error_updates_portfolio_bias": True,
    "deterministic_replay_required": True,
    "source_authority_unchanged": True,
    "adapter_authority_unchanged": True,
    "external_network_effect_not_inferred": True,
    "world_update_not_inferred": True,
    "memory_overwrite_not_inferred": True,
    "non_markov_experiment_holonomy_preserved": True,
}
FORBIDDEN_GRAPH_KEYS = {"nodes", "edges", "dependencies", "commitment_graph_digest"}


@dataclass(frozen=True)
class BoundedPortfolioExperimentResult:
    version: str
    status: str
    packet_id: str
    experiment_run_id: str
    cycle_index: int
    runtime_root: str
    context_key: str
    decision_mode: str
    baseline_adapter_id: str
    live_adapter_id: str
    experiment_adapter_id: str
    expected_information_gain: float
    trial_cost: float
    trial_risk: float
    trial_recoverability: float
    trial_budget_before: float
    trial_budget_after: float
    total_trial_count: int
    total_exploit_count: int
    shadow_projection_count: int
    resolved_shadow_count: int
    child_capability_status: str
    child_capability_run_id: str
    live_effect_receipt_digest: str
    experiment_bundle_digest: str
    idempotent_replay: bool
    recovered_pending_run: bool
    state_path: str
    bundle_path: str
    decision_path: str
    selection_path: str
    projection_path: str
    resolution_path: str
    trial_path: str
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
    return sha(without(value, "experiment_plan_digest"))


def bundle_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "experiment_bundle_digest"))


def decision_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "experiment_decision_digest"))


def trial_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "trial_record_digest"))


def state_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "experiment_state_digest"))


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


def nonnegative(value: Any, default: float = 0.0) -> float:
    if isinstance(value, bool):
        return default
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    if not math.isfinite(number):
        return default
    return max(0.0, number)


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
