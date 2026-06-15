#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import math
import os
import pathlib
from typing import Any, Mapping

VERSION = "kuuos_experiment_outcome_policy_v0_9"
PLAN_VERSION = "kuuos_experiment_outcome_policy_plan_v0_9"
LICENSE_VERSION = "kuuos_experiment_outcome_policy_license_v0_9"
BUNDLE_VERSION = "kuuos_experiment_outcome_policy_bundle_v0_9"
SECTION_VERSION = "kuuos_experiment_outcome_policy_section_v0_9"
DECISION_VERSION = "kuuos_experiment_outcome_policy_decision_v0_9"
OUTCOME_VERSION = "kuuos_experiment_outcome_policy_outcome_v0_9"
STATE_VERSION = "kuuos_experiment_outcome_policy_state_v0_9"
LEDGER_VERSION = "kuuos_experiment_outcome_policy_ledger_record_v0_9"
READY = "KUUOS_EXPERIMENT_OUTCOME_POLICY_V0_9_READY"
BLOCKED = "KUUOS_EXPERIMENT_OUTCOME_POLICY_V0_9_BLOCKED"
REPLAYED = "KUUOS_EXPERIMENT_OUTCOME_POLICY_V0_9_REPLAYED"

REQUIRED_BOUNDARY = {
    "v0_8_hard_gates_preserved": True,
    "policy_may_adjust_cadence_not_authority": True,
    "policy_threshold_has_hard_floor": True,
    "policy_cooldown_has_hard_floor": True,
    "one_v0_8_cycle_per_policy_run": True,
    "one_live_adapter_per_cycle": True,
    "reobserve_is_local_observation_action": True,
    "reobserve_disables_live_trial_for_that_cycle": True,
    "exploit_disables_live_trial_for_that_cycle": True,
    "experiment_requires_v0_8_eligibility": True,
    "actual_outcome_required_for_policy_update": True,
    "compatible_resolution_only": True,
    "step_incompatible_prediction_remains_pending": True,
    "trial_budget_debited_only_by_v0_8": True,
    "source_authority_unchanged": True,
    "adapter_authority_unchanged": True,
    "shadow_candidates_non_actuating": True,
    "external_network_effect_not_inferred": True,
    "world_update_not_inferred": True,
    "memory_overwrite_not_inferred": True,
    "deterministic_replay_required": True,
    "non_markov_policy_holonomy_preserved": True,
}
FORBIDDEN_GRAPH_KEYS = {"nodes", "edges", "dependencies", "commitment_graph_digest"}


@dataclass(frozen=True)
class ExperimentOutcomePolicyResult:
    version: str
    status: str
    packet_id: str
    policy_run_id: str
    cycle_index: int
    runtime_root: str
    context_key: str
    policy_mode: str
    policy_reason: str
    preview_baseline_adapter_id: str
    preview_experiment_adapter_id: str
    child_decision_mode: str
    child_live_adapter_id: str
    adapted_minimum_information_gain: float
    adapted_trial_cooldown_cycles: int
    experiment_pressure: float
    reobserve_pressure: float
    posterior_experiment_success: float
    mean_net_experiment_value: float
    live_observed_utility: float
    live_domain_action: str
    compatible_shadow_resolved: bool
    policy_bundle_digest: str
    child_experiment_bundle_digest: str
    child_effect_receipt_digest: str
    idempotent_replay: bool
    recovered_pending_run: bool
    state_path: str
    bundle_path: str
    decision_path: str
    outcome_path: str
    child_plan_path: str
    child_license_path: str
    child_registry_path: str
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
    return sha(without(value, "policy_plan_digest"))


def bundle_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "policy_bundle_digest"))


def section_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "policy_section_digest"))


def decision_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "policy_decision_digest"))


def outcome_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "policy_outcome_digest"))


def state_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "policy_state_digest"))


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
