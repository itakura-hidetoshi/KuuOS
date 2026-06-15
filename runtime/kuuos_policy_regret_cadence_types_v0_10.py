#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import math
import os
import pathlib
from typing import Any, Mapping

VERSION = "kuuos_policy_regret_cadence_v0_10"
PLAN_VERSION = "kuuos_policy_regret_cadence_plan_v0_10"
LICENSE_VERSION = "kuuos_policy_regret_cadence_license_v0_10"
BUNDLE_VERSION = "kuuos_policy_regret_cadence_bundle_v0_10"
SECTION_VERSION = "kuuos_policy_regret_cadence_section_v0_10"
DECISION_VERSION = "kuuos_policy_regret_cadence_decision_v0_10"
OUTCOME_VERSION = "kuuos_policy_regret_cadence_outcome_v0_10"
STATE_VERSION = "kuuos_policy_regret_cadence_state_v0_10"
LEDGER_VERSION = "kuuos_policy_regret_cadence_ledger_record_v0_10"
READY = "KUUOS_POLICY_REGRET_CADENCE_V0_10_READY"
BLOCKED = "KUUOS_POLICY_REGRET_CADENCE_V0_10_BLOCKED"
REPLAYED = "KUUOS_POLICY_REGRET_CADENCE_V0_10_REPLAYED"

REQUIRED_BOUNDARY = {
    "one_v0_9_child_cycle_per_regret_run": True,
    "counterfactual_estimate_not_truth": True,
    "unexecuted_alternative_not_outcome": True,
    "positive_regret_requires_credible_alternative": True,
    "regret_is_confidence_discounted": True,
    "regret_is_bounded_per_cycle": True,
    "delayed_compatible_outcome_may_update_credibility": True,
    "step_incompatible_prediction_remains_pending": True,
    "pending_shadow_is_discounted_not_promoted": True,
    "cadence_threshold_has_lower_and_upper_bounds": True,
    "cadence_interval_has_lower_and_upper_bounds": True,
    "v0_9_policy_authority_unchanged": True,
    "v0_8_hard_gates_preserved": True,
    "one_live_adapter_per_descendant_cycle": True,
    "shadow_candidates_non_actuating": True,
    "trial_budget_debited_only_by_v0_8": True,
    "source_authority_unchanged": True,
    "adapter_authority_unchanged": True,
    "external_network_effect_not_inferred": True,
    "world_update_not_inferred": True,
    "memory_overwrite_not_inferred": True,
    "deterministic_replay_required": True,
    "non_markov_regret_holonomy_preserved": True,
}
FORBIDDEN_GRAPH_KEYS = {"nodes", "edges", "dependencies", "commitment_graph_digest"}


@dataclass(frozen=True)
class PolicyRegretCadenceResult:
    version: str
    status: str
    packet_id: str
    regret_run_id: str
    cycle_index: int
    runtime_root: str
    context_key: str
    child_policy_mode: str
    child_policy_reason: str
    child_live_adapter_id: str
    child_live_domain_action: str
    chosen_value: float
    best_alternative_mode: str
    best_alternative_value: float
    best_alternative_confidence: float
    bounded_regret: float
    experiment_regret_credit: float
    reobserve_regret_credit: float
    exploit_regret_credit: float
    adapted_experiment_pressure_threshold: float
    adapted_reobserve_pressure_threshold: float
    adapted_experiment_interval: int
    adapted_reobserve_interval: int
    delayed_compatible_evidence_count: int
    pending_counterfactual_evidence_count: int
    regret_bundle_digest: str
    child_policy_bundle_digest: str
    child_policy_outcome_digest: str
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
    return sha(without(value, "regret_plan_digest"))


def bundle_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "regret_bundle_digest"))


def section_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "regret_section_digest"))


def decision_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "regret_decision_digest"))


def outcome_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "regret_outcome_digest"))


def state_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "regret_state_digest"))


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
