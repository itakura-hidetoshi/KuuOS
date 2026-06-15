#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping, Sequence

VERSION = "kuuos_open_horizon_telos_genesis_v0_1"
OBSERVATION_VERSION = "kuuos_open_horizon_observation_packet_v0_1"
ROOT_VERSION = "kuuos_open_horizon_root_principles_v0_1"
PLAN_VERSION = "kuuos_open_horizon_telos_genesis_plan_v0_1"
LICENSE_VERSION = "kuuos_open_horizon_telos_genesis_license_v0_1"
STATE_VERSION = "kuuos_open_horizon_telos_state_v0_1"
GOAL_SET_VERSION = "kuuos_open_horizon_goal_set_v0_1"
COMMITMENT_VERSION = "kuuos_open_horizon_commitment_seed_v0_1"
LEDGER_VERSION = "kuuos_open_horizon_telos_ledger_record_v0_1"
READY = "KUUOS_OPEN_HORIZON_TELOS_GENESIS_V0_1_READY"
BLOCKED = "KUUOS_OPEN_HORIZON_TELOS_GENESIS_V0_1_BLOCKED"

REQUIRED_ROOT_PRINCIPLES = (
    "emptiness",
    "dependent_origination",
    "harmony",
    "contemplation",
    "repairability",
    "benefit_others",
)

ALLOWED_SIGNAL_KINDS = {
    "deficit",
    "opportunity",
    "relationship",
    "maintenance",
    "threat",
    "unknown",
}

REQUIRED_BOUNDARY = {
    "open_horizon_enabled": True,
    "local_step_bounded": True,
    "renewable_horizon": True,
    "self_generated_subgoals_allowed": True,
    "root_principles_self_rewrite_forbidden": True,
    "contextual_default_allow": True,
    "uncertainty_scales_action_not_automatic_stop": True,
    "repair_before_abandonment": True,
    "candidate_weighting_not_truth": True,
    "non_markov_lineage_preserved": True,
    "process_tensor_context_preserved": True,
}


@dataclass(frozen=True)
class OpenHorizonTelosGenesisResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    generation_index: int
    generated_goal_count: int
    selected_goal_count: int
    action_ready_count: int
    exploration_goal_count: int
    execution_posture: str
    stop_reason: str
    state_path: str
    goal_set_path: str
    commitment_seed_path: str
    receipt_path: str
    ledger_path: str
    audit_path: str
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _sha(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    output = dict(value)
    output.pop(field, None)
    return output


def _valid_digest(value: Mapping[str, Any], field: str) -> bool:
    digest = str(value.get(field, ""))
    return bool(digest) and digest == _sha(_without(value, field))


def observation_digest(value: Mapping[str, Any]) -> str:
    return _sha(_without(value, "observation_digest"))


def root_digest(value: Mapping[str, Any]) -> str:
    return _sha(_without(value, "root_principles_digest"))


def plan_digest(value: Mapping[str, Any]) -> str:
    return _sha(_without(value, "telos_plan_digest"))


def state_digest(value: Mapping[str, Any]) -> str:
    return _sha(_without(value, "telos_state_digest"))


def _clamp(value: Any, default: float = 0.0) -> float:
    if isinstance(value, bool):
        return default
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return max(0.0, min(1.0, number))


def _integer(value: Any, default: int = 0) -> int:
    if isinstance(value, bool):
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _root_path(value: Any, blockers: list[str]) -> pathlib.Path:
    if not value:
        blockers.append("runtime_root_missing")
        return pathlib.Path(".").resolve()
    root = pathlib.Path(str(value)).expanduser().resolve()
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")
    return root


def _read_json(path: pathlib.Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return dict(value) if isinstance(value, Mapping) else {}


def _read_jsonl(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    output: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            value = {"_invalid": True}
        output.append(dict(value) if isinstance(value, Mapping) else {"_invalid": True})
    return output


def _write_json(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def _append_jsonl(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")


def _validate_root(root_packet: Mapping[str, Any], plan: Mapping[str, Any], blockers: list[str]) -> None:
    if root_packet.get("version") != ROOT_VERSION:
        blockers.append("root_principles_version_invalid")
    if not _valid_digest(root_packet, "root_principles_digest"):
        blockers.append("root_principles_digest_invalid")
    if plan.get("expected_root_principles_digest") != root_packet.get("root_principles_digest"):
        blockers.append("root_principles_digest_mismatch")
    principles = tuple(str(item) for item in _list(root_packet.get("principles")))
    missing = [item for item in REQUIRED_ROOT_PRINCIPLES if item not in principles]
    if missing:
        blockers.append("required_root_principles_missing")
    if root_packet.get("protected") is not True:
        blockers.append("root_principles_not_protected")
    if root_packet.get("self_rewrite_allowed") is not False:
        blockers.append("root_principles_self_rewrite_not_denied")


def _validate_observation(observation: Mapping[str, Any], plan: Mapping[str, Any], blockers: list[str]) -> None:
    if observation.get("version") != OBSERVATION_VERSION:
        blockers.append("observation_version_invalid")
    if not _valid_digest(observation, "observation_digest"):
        blockers.append("observation_digest_invalid")
    if plan.get("expected_observation_digest") != observation.get("observation_digest"):
        blockers.append("observation_digest_mismatch")
    signals = _list(observation.get("signals"))
    if not signals:
        blockers.append("observation_signals_missing")
    seen: set[str] = set()
    for raw in signals:
        signal = _mapping(raw)
        signal_id = str(signal.get("signal_id", ""))
        if not signal_id or signal_id in seen:
            blockers.append("signal_id_missing_or_repeated")
            continue
        seen.add(signal_id)
        if str(signal.get("kind", "")) not in ALLOWED_SIGNAL_KINDS:
            blockers.append("signal_kind_invalid")
        if not str(signal.get("target", "")).strip():
            blockers.append("signal_target_missing")
        for field in (
            "magnitude",
            "urgency",
            "evidence",
            "uncertainty",
            "irreversibility",
            "recoverability",
            "relational_benefit",
            "autonomy_gain",
        ):
            raw_value = signal.get(field)
            value = _clamp(raw_value, -1.0)
            if value < 0.0:
                blockers.append(f"signal_{field}_invalid")


def _validate_plan(plan: Mapping[str, Any], blockers: list[str]) -> tuple[int, int, float, float, int]:
    if plan.get("version") != PLAN_VERSION:
        blockers.append("telos_plan_version_invalid")
    if not _valid_digest(plan, "telos_plan_digest"):
        blockers.append("telos_plan_digest_invalid")
    if not str(plan.get("telos_run_id", "")):
        blockers.append("telos_run_id_missing")
    if not str(plan.get("agent_id", "")):
        blockers.append("agent_id_missing")
    boundary = _mapping(plan.get("boundary"))
    for field, expected in REQUIRED_BOUNDARY.items():
        if boundary.get(field) is not expected:
            blockers.append(f"boundary_{field}_invalid")
    max_generated = _integer(plan.get("max_generated_goals"), 0)
    max_selected = _integer(plan.get("max_selected_goals"), 0)
    renewal_steps = _integer(plan.get("renewal_window_steps"), 0)
    min_score = _clamp(plan.get("min_goal_score"), -1.0)
    min_action_scale = _clamp(plan.get("min_action_scale"), -1.0)
    if not 1 <= max_generated <= 32:
        blockers.append("max_generated_goals_invalid")
    if not 1 <= max_selected <= min(max_generated, 8):
        blockers.append("max_selected_goals_invalid")
    if not 1 <= renewal_steps <= 1000:
        blockers.append("renewal_window_steps_invalid")
    if min_score < 0.0:
        blockers.append("min_goal_score_invalid")
    if min_action_scale < 0.0:
        blockers.append("min_action_scale_invalid")
    return max_generated, max_selected, min_score, min_action_scale, renewal_steps


def _validate_license(
    license_packet: Mapping[str, Any],
    plan: Mapping[str, Any],
    observation: Mapping[str, Any],
    root_packet: Mapping[str, Any],
    blockers: list[str],
) -> None:
    if license_packet.get("version") != LICENSE_VERSION:
        blockers.append("telos_license_version_invalid")
    bindings = {
        "bound_plan_digest": plan.get("telos_plan_digest"),
        "bound_observation_digest": observation.get("observation_digest"),
        "bound_root_principles_digest": root_packet.get("root_principles_digest"),
    }
    for field, expected in bindings.items():
        if license_packet.get(field) != expected:
            blockers.append(f"license_{field}_mismatch")
    for field in (
        "goal_generation_allowed",
        "subgoal_synthesis_allowed",
        "goal_selection_allowed",
        "commitment_seed_write_allowed",
        "state_write_allowed",
        "ledger_append_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
        "domain_action_preparation_allowed",
    ):
        if license_packet.get(field) is not True:
            blockers.append(field.replace("allowed", "not_allowed"))
    if license_packet.get("root_principles_rewrite_allowed") is not False:
        blockers.append("root_principles_rewrite_not_denied")


def _goal_verb(kind: str) -> str:
    return {
        "deficit": "reduce",
        "opportunity": "develop",
        "relationship": "strengthen",
        "maintenance": "sustain",
        "threat": "mitigate",
        "unknown": "clarify",
    }.get(kind, "explore")


def _goal_score(signal: Mapping[str, Any]) -> tuple[float, float]:
    magnitude = _clamp(signal.get("magnitude"))
    urgency = _clamp(signal.get("urgency"))
    evidence = _clamp(signal.get("evidence"))
    uncertainty = _clamp(signal.get("uncertainty"))
    irreversibility = _clamp(signal.get("irreversibility"))
    recoverability = _clamp(signal.get("recoverability"))
    relational_benefit = _clamp(signal.get("relational_benefit"))
    autonomy_gain = _clamp(signal.get("autonomy_gain"))
    positive = (
        0.22 * urgency
        + 0.24 * relational_benefit
        + 0.18 * recoverability
        + 0.16 * autonomy_gain
        + 0.12 * evidence
        + 0.08 * magnitude
    )
    score = max(0.0, min(1.0, positive - 0.12 * uncertainty - 0.18 * irreversibility))
    numerator = max(0.01, relational_benefit) * max(0.05, recoverability) * (0.5 + 0.5 * evidence)
    denominator = 0.5 + uncertainty + irreversibility
    action_scale = max(0.02, min(1.0, numerator / denominator))
    return round(score, 6), round(action_scale, 6)


def _build_goal(
    *,
    agent_id: str,
    observation_id: str,
    signal: Mapping[str, Any],
    min_score: float,
    min_action_scale: float,
) -> dict[str, Any]:
    kind = str(signal.get("kind", "unknown"))
    target = str(signal.get("target", "unknown")).strip().lower().replace(" ", "_")
    score, action_scale = _goal_score(signal)
    if score >= min_score and action_scale >= min_action_scale:
        posture = "advance"
    elif score >= min_score or _clamp(signal.get("urgency")) >= 0.7:
        posture = "micro_intervention"
    else:
        posture = "explore"
    goal_id = "goal-" + _sha(
        {
            "agent_id": agent_id,
            "observation_id": observation_id,
            "signal_id": signal.get("signal_id"),
            "kind": kind,
            "target": target,
        }
    )[:16]
    return {
        "goal_id": goal_id,
        "source_signal_id": str(signal.get("signal_id", "")),
        "origin": "self_generated_from_relational_observation",
        "kind": kind,
        "target": target,
        "goal_statement": f"{_goal_verb(kind)}_{target}",
        "priority_score": score,
        "action_scale": action_scale,
        "progress_posture": posture,
        "desired_world_difference": {
            "direction": "increase" if kind in {"opportunity", "relationship", "maintenance"} else "decrease",
            "target": target,
            "magnitude_hint": _clamp(signal.get("magnitude")),
        },
        "evidence": _clamp(signal.get("evidence")),
        "uncertainty": _clamp(signal.get("uncertainty")),
        "irreversibility": _clamp(signal.get("irreversibility")),
        "recoverability": _clamp(signal.get("recoverability")),
        "relational_benefit": _clamp(signal.get("relational_benefit")),
        "autonomy_gain": _clamp(signal.get("autonomy_gain")),
        "abandonment_condition": "benefit_exhausted_or_relation_harmed_after_repair_attempt",
        "repair_strategy": "reduce_action_scale_reobserve_and_replan",
        "root_principles_unchanged": True,
        "candidate_weighting_not_truth": True,
    }


def _select_plural(goals: Sequence[Mapping[str, Any]], maximum: int) -> list[dict[str, Any]]:
    ranked = [dict(goal) for goal in sorted(goals, key=lambda item: (-float(item["priority_score"]), str(item["goal_id"])))]
    selected: list[dict[str, Any]] = []
    represented: set[str] = set()
    for goal in ranked:
        kind = str(goal.get("kind", "unknown"))
        if kind not in represented:
            selected.append(goal)
            represented.add(kind)
            if len(selected) >= maximum:
                return selected
    selected_ids = {str(goal["goal_id"]) for goal in selected}
    for goal in ranked:
        if str(goal["goal_id"]) not in selected_ids:
            selected.append(goal)
            selected_ids.add(str(goal["goal_id"]))
            if len(selected) >= maximum:
                break
    return selected


def _validate_previous_state(root: pathlib.Path, plan: Mapping[str, Any], blockers: list[str]) -> tuple[int, str]:
    state_path = root / "kuuos_open_horizon_telos_state_v0_1.json"
    previous = _read_json(state_path)
    expected = str(plan.get("expected_previous_state_digest", ""))
    if not previous:
        if expected:
            blockers.append("previous_state_missing")
        return 1, ""
    if previous.get("version") != STATE_VERSION or not _valid_digest(previous, "telos_state_digest"):
        blockers.append("previous_state_invalid")
        return 0, ""
    previous_digest = str(previous.get("telos_state_digest", ""))
    if expected != previous_digest:
        blockers.append("previous_state_digest_mismatch")
    return _integer(previous.get("generation_index"), 0) + 1, previous_digest


def build_open_horizon_telos_genesis(
    *,
    runtime_context: Mapping[str, Any],
    observation_packet: Mapping[str, Any],
    root_principles_packet: Mapping[str, Any],
    telos_plan: Mapping[str, Any],
    telos_license: Mapping[str, Any],
) -> OpenHorizonTelosGenesisResult:
    context = _mapping(runtime_context)
    observation = _mapping(observation_packet)
    root_packet = _mapping(root_principles_packet)
    plan = _mapping(telos_plan)
    license_packet = _mapping(telos_license)
    blockers: list[str] = []
    warnings: list[str] = []
    runtime_root = _root_path(context.get("runtime_root"), blockers)

    state_path = runtime_root / "kuuos_open_horizon_telos_state_v0_1.json"
    goal_set_path = runtime_root / "kuuos_open_horizon_goal_set_v0_1.json"
    commitment_path = runtime_root / "kuuos_open_horizon_commitment_seed_v0_1.json"
    receipt_path = runtime_root / "kuuos_open_horizon_telos_genesis_receipt_v0_1.json"
    ledger_path = runtime_root / "kuuos_open_horizon_telos_ledger_v0_1.jsonl"
    audit_path = runtime_root / "kuuos_open_horizon_telos_audit_v0_1.jsonl"

    if context.get("open_horizon_telos_genesis_enabled") is not True:
        blockers.append("open_horizon_telos_genesis_enabled_not_true")
    if context.get("apply_open_horizon_telos_genesis") is not True:
        blockers.append("apply_open_horizon_telos_genesis_not_true")

    max_generated, max_selected, min_score, min_action_scale, renewal_steps = _validate_plan(plan, blockers)
    _validate_root(root_packet, plan, blockers)
    _validate_observation(observation, plan, blockers)
    _validate_license(license_packet, plan, observation, root_packet, blockers)
    generation_index, previous_state_digest = _validate_previous_state(runtime_root, plan, blockers)

    ledger = _read_jsonl(ledger_path)
    run_id = str(plan.get("telos_run_id", ""))
    observation_id = str(observation.get("observation_id", ""))
    observation_sha = str(observation.get("observation_digest", ""))
    if any(row.get("_invalid") for row in ledger):
        blockers.append("telos_ledger_invalid")
    if any(str(row.get("telos_run_id", "")) == run_id for row in ledger):
        blockers.append("telos_run_replay_detected")
    if any(str(row.get("observation_digest", "")) == observation_sha for row in ledger):
        blockers.append("observation_replay_detected")

    generated: list[dict[str, Any]] = []
    selected: list[dict[str, Any]] = []
    state: dict[str, Any] = {}
    goal_set: dict[str, Any] = {}
    commitment: dict[str, Any] = {}
    execution_posture = "blocked"
    stop_reason = "validation_blocked"

    if not blockers:
        agent_id = str(plan.get("agent_id", ""))
        for raw_signal in _list(observation.get("signals"))[:max_generated]:
            generated.append(
                _build_goal(
                    agent_id=agent_id,
                    observation_id=observation_id,
                    signal=_mapping(raw_signal),
                    min_score=min_score,
                    min_action_scale=min_action_scale,
                )
            )
        selected = _select_plural(generated, max_selected)
        action_ready = [goal for goal in selected if goal["progress_posture"] in {"advance", "micro_intervention"}]
        exploration = [goal for goal in selected if goal["progress_posture"] == "explore"]
        execution_posture = "commitment_seed_ready" if action_ready else "exploration_commitment_ready"
        stop_reason = "local_generation_complete_horizon_renewable"

        goal_set = {
            "version": GOAL_SET_VERSION,
            "telos_run_id": run_id,
            "agent_id": agent_id,
            "generation_index": generation_index,
            "source_observation_digest": observation_sha,
            "root_principles_digest": root_packet.get("root_principles_digest"),
            "generated_goals": generated,
            "selected_goals": selected,
            "selection_rule": "plural_kind_first_then_priority",
            "self_generated_subgoals": True,
            "root_principles_unchanged": True,
            "contextual_default_allow": True,
            "uncertainty_response": "scale_or_explore_not_automatic_stop",
        }
        goal_set["goal_set_digest"] = _sha(goal_set)

        next_wake = {
            "renew_after_local_steps": renewal_steps,
            "events": [
                "new_observation",
                "effect_receipt",
                "commitment_progress",
                "resource_change",
                "relationship_change",
                "repair_request",
            ],
            "global_horizon_fixed": False,
            "local_invocation_finite": True,
        }
        commitment = {
            "version": COMMITMENT_VERSION,
            "telos_run_id": run_id,
            "agent_id": agent_id,
            "generation_index": generation_index,
            "goal_set_digest": goal_set["goal_set_digest"],
            "commitments": [
                {
                    "commitment_id": "commit-" + _sha({"run": run_id, "goal": goal["goal_id"]})[:16],
                    "goal_id": goal["goal_id"],
                    "next_move": goal["progress_posture"],
                    "action_scale": goal["action_scale"],
                    "repairable": True,
                    "replan_after_effect": True,
                    "status": "prepared",
                }
                for goal in selected
            ],
            "execution_posture": execution_posture,
            "next_wake": next_wake,
            "domain_action_prepared": bool(selected),
            "external_effect_not_required_for_telos_generation": True,
        }
        commitment["commitment_seed_digest"] = _sha(commitment)

        state = {
            "version": STATE_VERSION,
            "agent_id": agent_id,
            "telos_run_id": run_id,
            "generation_index": generation_index,
            "previous_telos_state_digest": previous_state_digest,
            "source_observation_id": observation_id,
            "source_observation_digest": observation_sha,
            "root_principles_digest": root_packet.get("root_principles_digest"),
            "goal_set_digest": goal_set["goal_set_digest"],
            "commitment_seed_digest": commitment["commitment_seed_digest"],
            "generated_goal_count": len(generated),
            "selected_goal_count": len(selected),
            "action_ready_count": len(action_ready),
            "exploration_goal_count": len(exploration),
            "open_horizon": True,
            "renewable_horizon": True,
            "local_step_bounded": True,
            "global_generation_cap_declared": False,
            "self_generated_subgoals_active": True,
            "root_principles_unchanged": True,
            "execution_posture": execution_posture,
            "next_wake": next_wake,
            "epoch": int(time.time()),
        }
        state["telos_state_digest"] = state_digest(state)

        _write_json(goal_set_path, goal_set)
        _write_json(commitment_path, commitment)
        _write_json(state_path, state)
        ledger_record = {
            "version": LEDGER_VERSION,
            "telos_run_id": run_id,
            "agent_id": agent_id,
            "generation_index": generation_index,
            "observation_digest": observation_sha,
            "previous_telos_state_digest": previous_state_digest,
            "telos_state_digest": state["telos_state_digest"],
            "goal_set_digest": goal_set["goal_set_digest"],
            "commitment_seed_digest": commitment["commitment_seed_digest"],
            "record_digest": "",
        }
        ledger_record["record_digest"] = _sha(_without(ledger_record, "record_digest"))
        _append_jsonl(ledger_path, ledger_record)

    status = READY if not blockers else BLOCKED
    packet_id = "kuuos-open-horizon-telos-" + _sha(
        {
            "plan": plan,
            "observation": observation_sha,
            "generation_index": generation_index,
            "blockers": blockers,
        }
    )[:16]
    receipt = {
        "version": VERSION,
        "status": status,
        "packet_id": packet_id,
        "telos_run_id": run_id,
        "generation_index": generation_index,
        "generated_goal_count": len(generated),
        "selected_goal_count": len(selected),
        "action_ready_count": sum(1 for goal in selected if goal.get("progress_posture") in {"advance", "micro_intervention"}),
        "exploration_goal_count": sum(1 for goal in selected if goal.get("progress_posture") == "explore"),
        "execution_posture": execution_posture,
        "stop_reason": stop_reason,
        "state_digest": state.get("telos_state_digest", ""),
        "goal_set_digest": goal_set.get("goal_set_digest", ""),
        "commitment_seed_digest": commitment.get("commitment_seed_digest", ""),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if license_packet.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if license_packet.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})

    return OpenHorizonTelosGenesisResult(
        VERSION,
        status,
        packet_id,
        str(runtime_root),
        generation_index,
        len(generated),
        len(selected),
        sum(1 for goal in selected if goal.get("progress_posture") in {"advance", "micro_intervention"}),
        sum(1 for goal in selected if goal.get("progress_posture") == "explore"),
        execution_posture,
        stop_reason,
        str(state_path),
        str(goal_set_path),
        str(commitment_path),
        str(receipt_path),
        str(ledger_path),
        str(audit_path),
        blockers,
        warnings,
    )
