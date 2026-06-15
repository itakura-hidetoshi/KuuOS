#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping, Sequence

VERSION = "kuuos_open_horizon_commitment_gauge_v0_2"
PLAN_VERSION = "kuuos_open_horizon_commitment_gauge_plan_v0_2"
LICENSE_VERSION = "kuuos_open_horizon_commitment_gauge_license_v0_2"
EFFECT_VERSION = "kuuos_open_horizon_effect_receipt_v0_2"
STATE_VERSION = "kuuos_open_horizon_commitment_gauge_state_v0_2"
BUNDLE_VERSION = "kuuos_open_horizon_commitment_gauge_bundle_v0_2"
ACTION_VERSION = "kuuos_open_horizon_covariant_action_v0_2"
LEDGER_VERSION = "kuuos_open_horizon_commitment_gauge_ledger_record_v0_2"
READY = "KUUOS_OPEN_HORIZON_COMMITMENT_GAUGE_V0_2_READY"
BLOCKED = "KUUOS_OPEN_HORIZON_COMMITMENT_GAUGE_V0_2_BLOCKED"

TELOS_STATE_VERSION = "kuuos_open_horizon_telos_state_v0_1"
GOAL_SET_VERSION = "kuuos_open_horizon_goal_set_v0_1"
COMMITMENT_SEED_VERSION = "kuuos_open_horizon_commitment_seed_v0_1"

ALLOWED_OUTCOMES = {"success", "partial", "failure", "blocked", "uncertain"}
ALLOWED_CONTINUATIONS = {"continue", "complete", "reobserve", "repair", "expand"}
TERMINAL_SECTION_STATES = {"flat_complete", "handed_over", "superseded"}
REQUIRED_BOUNDARY = {
    "gauge_bundle_runtime": True,
    "local_sections_not_global_graph": True,
    "connection_parallel_transport": True,
    "effect_receipt_interpreted_as_curvature": True,
    "gauge_covariant_replanning": True,
    "holonomy_preserves_non_markov_memory": True,
    "gauge_invariant_action_selection": True,
    "one_covariant_action_per_invocation": True,
    "renewable_horizon": True,
    "repair_by_local_gauge_correction": True,
    "new_telos_generations_extend_bundle": True,
    "candidate_weighting_not_truth": True,
    "process_tensor_context_preserved": True,
}


@dataclass(frozen=True)
class OpenHorizonCommitmentGaugeResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    epoch_index: int
    source_telos_generation: int
    section_count: int
    ready_section_count: int
    terminal_section_count: int
    integrated_section_count: int
    curvature_update_count: int
    holonomy_depth: int
    effect_applied: bool
    action_ready: bool
    covariant_step_kind: str
    active_section_id: str
    execution_posture: str
    stop_reason: str
    state_path: str
    bundle_path: str
    action_path: str
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
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    output = dict(value)
    output.pop(field, None)
    return output


def _valid_digest(value: Mapping[str, Any], field: str) -> bool:
    digest = str(value.get(field, ""))
    return bool(digest) and digest == _sha(_without(value, field))


def plan_digest(value: Mapping[str, Any]) -> str:
    return _sha(_without(value, "gauge_plan_digest"))


def effect_digest(value: Mapping[str, Any]) -> str:
    return _sha(_without(value, "effect_receipt_digest"))


def bundle_digest(value: Mapping[str, Any]) -> str:
    return _sha(_without(value, "gauge_bundle_digest"))


def state_digest(value: Mapping[str, Any]) -> str:
    return _sha(_without(value, "gauge_state_digest"))


def action_digest(value: Mapping[str, Any]) -> str:
    return _sha(_without(value, "covariant_action_digest"))


def _integer(value: Any, default: int = 0) -> int:
    if isinstance(value, bool):
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _clamp(value: Any, default: float = 0.0) -> float:
    if isinstance(value, bool):
        return default
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return max(0.0, min(1.0, number))


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


def _validate_plan(plan: Mapping[str, Any], blockers: list[str]) -> tuple[int, int, int, float]:
    if plan.get("version") != PLAN_VERSION:
        blockers.append("gauge_plan_version_invalid")
    if not _valid_digest(plan, "gauge_plan_digest"):
        blockers.append("gauge_plan_digest_invalid")
    if not str(plan.get("gauge_run_id", "")):
        blockers.append("gauge_run_id_missing")
    if not str(plan.get("agent_id", "")):
        blockers.append("agent_id_missing")
    boundary = _mapping(plan.get("boundary"))
    for field, expected in REQUIRED_BOUNDARY.items():
        if boundary.get(field) is not expected:
            blockers.append(f"boundary_{field}_invalid")
    max_sections = _integer(plan.get("max_bundle_sections"), 0)
    max_new = _integer(plan.get("max_new_sections_per_run"), 0)
    max_attempts = _integer(plan.get("max_transports_per_section"), 0)
    min_scale = _clamp(plan.get("min_action_scale"), -1.0)
    if not 2 <= max_sections <= 4096:
        blockers.append("max_bundle_sections_invalid")
    if not 1 <= max_new <= 32:
        blockers.append("max_new_sections_per_run_invalid")
    if not 1 <= max_attempts <= 20:
        blockers.append("max_transports_per_section_invalid")
    if min_scale < 0.0 or min_scale > 0.25:
        blockers.append("min_action_scale_invalid")
    return max_sections, max_new, max_attempts, min_scale


def _validate_source(
    telos_state: Mapping[str, Any],
    goal_set: Mapping[str, Any],
    seed: Mapping[str, Any],
    plan: Mapping[str, Any],
    blockers: list[str],
) -> None:
    if telos_state.get("version") != TELOS_STATE_VERSION or not _valid_digest(telos_state, "telos_state_digest"):
        blockers.append("source_telos_state_invalid")
    if goal_set.get("version") != GOAL_SET_VERSION or not _valid_digest(goal_set, "goal_set_digest"):
        blockers.append("source_goal_set_invalid")
    if seed.get("version") != COMMITMENT_SEED_VERSION or not _valid_digest(seed, "commitment_seed_digest"):
        blockers.append("source_commitment_seed_invalid")
    for field, expected in {
        "expected_telos_state_digest": telos_state.get("telos_state_digest"),
        "expected_goal_set_digest": goal_set.get("goal_set_digest"),
        "expected_commitment_seed_digest": seed.get("commitment_seed_digest"),
    }.items():
        if plan.get(field) != expected:
            blockers.append(f"{field}_mismatch")
    if goal_set.get("telos_run_id") != telos_state.get("telos_run_id"):
        blockers.append("source_goal_state_run_mismatch")
    if seed.get("telos_run_id") != telos_state.get("telos_run_id"):
        blockers.append("source_seed_state_run_mismatch")
    if goal_set.get("generation_index") != telos_state.get("generation_index"):
        blockers.append("source_goal_state_generation_mismatch")
    if seed.get("generation_index") != telos_state.get("generation_index"):
        blockers.append("source_seed_state_generation_mismatch")
    if seed.get("goal_set_digest") != goal_set.get("goal_set_digest"):
        blockers.append("source_seed_goal_set_digest_mismatch")
    if telos_state.get("commitment_seed_digest") != seed.get("commitment_seed_digest"):
        blockers.append("source_state_seed_digest_mismatch")
    if telos_state.get("goal_set_digest") != goal_set.get("goal_set_digest"):
        blockers.append("source_state_goal_set_digest_mismatch")
    if telos_state.get("open_horizon") is not True or telos_state.get("renewable_horizon") is not True:
        blockers.append("source_open_horizon_not_active")
    agent_id = str(plan.get("agent_id", ""))
    for label, packet in (("telos", telos_state), ("goal_set", goal_set), ("seed", seed)):
        if agent_id != str(packet.get("agent_id", "")):
            blockers.append(f"plan_agent_{label}_agent_mismatch")


def _validate_license(
    license_packet: Mapping[str, Any],
    plan: Mapping[str, Any],
    telos_state: Mapping[str, Any],
    goal_set: Mapping[str, Any],
    seed: Mapping[str, Any],
    effect: Mapping[str, Any],
    blockers: list[str],
) -> None:
    if license_packet.get("version") != LICENSE_VERSION:
        blockers.append("gauge_license_version_invalid")
    for field, expected in {
        "bound_plan_digest": plan.get("gauge_plan_digest"),
        "bound_telos_state_digest": telos_state.get("telos_state_digest"),
        "bound_goal_set_digest": goal_set.get("goal_set_digest"),
        "bound_commitment_seed_digest": seed.get("commitment_seed_digest"),
        "bound_effect_receipt_digest": effect.get("effect_receipt_digest", ""),
    }.items():
        if license_packet.get(field, "") != expected:
            blockers.append(f"license_{field}_mismatch")
    for field in (
        "source_read_allowed",
        "bundle_initialize_allowed",
        "telos_section_extension_allowed",
        "parallel_transport_allowed",
        "curvature_update_allowed",
        "local_gauge_correction_allowed",
        "holonomy_append_allowed",
        "covariant_action_prepare_allowed",
        "state_write_allowed",
        "bundle_write_allowed",
        "action_write_allowed",
        "ledger_append_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if license_packet.get(field) is not True:
            blockers.append(field.replace("allowed", "not_allowed"))


def _validate_existing_bundle(bundle: Mapping[str, Any], state: Mapping[str, Any], blockers: list[str]) -> None:
    if not bundle and not state:
        return
    if not bundle or not state:
        blockers.append("gauge_bundle_state_pair_incomplete")
        return
    if bundle.get("version") != BUNDLE_VERSION or not _valid_digest(bundle, "gauge_bundle_digest"):
        blockers.append("existing_gauge_bundle_invalid")
    if state.get("version") != STATE_VERSION or not _valid_digest(state, "gauge_state_digest"):
        blockers.append("existing_gauge_state_invalid")
    if state.get("gauge_bundle_digest") != bundle.get("gauge_bundle_digest"):
        blockers.append("existing_state_bundle_digest_mismatch")
    if state.get("agent_id") != bundle.get("agent_id"):
        blockers.append("existing_state_bundle_agent_mismatch")
    section_ids: set[str] = set()
    commitment_ids: set[str] = set()
    for raw in _list(bundle.get("local_sections")):
        section = _mapping(raw)
        section_id = str(section.get("section_id", ""))
        commitment_id = str(section.get("source_commitment_id", ""))
        if not section_id or section_id in section_ids:
            blockers.append("section_id_missing_or_repeated")
        if not commitment_id or commitment_id in commitment_ids:
            blockers.append("source_commitment_id_missing_or_repeated")
        section_ids.add(section_id)
        commitment_ids.add(commitment_id)
        if "nodes" in section or "dependencies" in section:
            blockers.append("graph_semantics_present_in_section")
    for raw in _list(bundle.get("holonomy_trace")):
        if not str(_mapping(raw).get("effect_receipt_digest", "")):
            blockers.append("holonomy_effect_digest_missing")


def _validate_current_action(bundle: Mapping[str, Any], action: Mapping[str, Any], blockers: list[str]) -> None:
    active_action_id = str(bundle.get("active_action_id", ""))
    active_section_id = str(bundle.get("active_section_id", ""))
    if not bundle and not action:
        return
    if active_action_id:
        if not action:
            blockers.append("outstanding_covariant_action_missing")
            return
        if action.get("version") != ACTION_VERSION or not _valid_digest(action, "covariant_action_digest"):
            blockers.append("outstanding_covariant_action_invalid")
        if action.get("action_ready") is not True:
            blockers.append("outstanding_covariant_action_not_ready")
        if str(action.get("action_id", "")) != active_action_id:
            blockers.append("outstanding_covariant_action_id_mismatch")
        if str(action.get("section_id", "")) != active_section_id:
            blockers.append("outstanding_covariant_section_mismatch")
    elif action and action.get("action_ready") is True:
        blockers.append("stale_covariant_action_without_active_transport")


def _validate_source_continuity(state: Mapping[str, Any], telos_state: Mapping[str, Any], blockers: list[str]) -> bool:
    if not state:
        return True
    current_digest = str(telos_state.get("telos_state_digest", ""))
    last_digest = str(state.get("last_integrated_telos_state_digest", ""))
    current_generation = _integer(telos_state.get("generation_index"), 0)
    last_generation = _integer(state.get("last_integrated_telos_generation"), 0)
    if current_digest == last_digest:
        return False
    if current_generation != last_generation + 1:
        blockers.append("new_telos_generation_not_contiguous")
    if telos_state.get("previous_telos_state_digest") != last_digest:
        blockers.append("new_telos_previous_state_digest_mismatch")
    return True


def _validate_effect(
    effect: Mapping[str, Any],
    plan: Mapping[str, Any],
    current_action: Mapping[str, Any],
    blockers: list[str],
) -> None:
    expected = str(plan.get("expected_effect_receipt_digest", ""))
    actual = str(effect.get("effect_receipt_digest", ""))
    if not effect:
        if expected:
            blockers.append("expected_effect_receipt_missing")
        return
    if effect.get("version") != EFFECT_VERSION or not _valid_digest(effect, "effect_receipt_digest"):
        blockers.append("effect_receipt_invalid")
    if expected != actual:
        blockers.append("effect_receipt_digest_mismatch")
    if not current_action or current_action.get("action_ready") is not True:
        blockers.append("effect_without_outstanding_covariant_action")
        return
    if effect.get("source_action_digest") != current_action.get("covariant_action_digest"):
        blockers.append("effect_source_action_digest_mismatch")
    if effect.get("action_id") != current_action.get("action_id"):
        blockers.append("effect_action_id_mismatch")
    if effect.get("section_id") != current_action.get("section_id"):
        blockers.append("effect_section_id_mismatch")
    if str(effect.get("outcome", "")) not in ALLOWED_OUTCOMES:
        blockers.append("effect_outcome_invalid")
    if str(effect.get("continuation_signal", "")) not in ALLOWED_CONTINUATIONS:
        blockers.append("effect_continuation_signal_invalid")
    for field in ("progress_delta", "observed_benefit", "observed_harm", "recoverability", "confidence"):
        if _clamp(effect.get(field), -1.0) < 0.0:
            blockers.append(f"effect_{field}_invalid")


def _goal_index(goal_set: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(_mapping(goal).get("goal_id", "")): dict(_mapping(goal))
        for goal in _list(goal_set.get("selected_goals"))
        if str(_mapping(goal).get("goal_id", ""))
    }


def _initial_transport_kind(next_move: str) -> str:
    return {
        "advance": "covariant_advance",
        "micro_intervention": "covariant_micro_intervention",
        "explore": "curvature_probe",
    }.get(next_move, "curvature_probe")


def _missing_commitment_count(bundle: Mapping[str, Any], seed: Mapping[str, Any]) -> int:
    existing = {
        str(_mapping(section).get("source_commitment_id", ""))
        for section in _list(bundle.get("local_sections"))
    }
    return sum(
        1
        for raw in _list(seed.get("commitments"))
        if str(_mapping(raw).get("commitment_id", ""))
        and str(_mapping(raw).get("commitment_id", "")) not in existing
    )


def _extend_bundle_sections(
    bundle: dict[str, Any],
    goal_set: Mapping[str, Any],
    seed: Mapping[str, Any],
    epoch: int,
    maximum: int,
    blockers: list[str],
) -> int:
    goals = _goal_index(goal_set)
    sections = [dict(_mapping(section)) for section in _list(bundle.get("local_sections"))]
    existing = {str(section.get("source_commitment_id", "")) for section in sections}
    added = 0
    for raw in _list(seed.get("commitments")):
        commitment = _mapping(raw)
        commitment_id = str(commitment.get("commitment_id", ""))
        goal_id = str(commitment.get("goal_id", ""))
        if not commitment_id or commitment_id in existing:
            continue
        goal = goals.get(goal_id)
        if goal is None:
            blockers.append("commitment_goal_missing_from_goal_set")
            continue
        if added >= maximum:
            break
        section_id = "section-" + _sha({"commitment": commitment_id, "seed": seed.get("commitment_seed_digest")})[:18]
        chart_id = "chart-" + _sha({"goal_kind": goal.get("kind"), "generation": seed.get("generation_index")})[:12]
        gauge_invariant_signature = _sha(
            {
                "goal_id": goal_id,
                "priority_score": _clamp(goal.get("priority_score")),
                "action_scale": _clamp(commitment.get("action_scale")),
                "source_commitment_id": commitment_id,
            }
        )
        sections.append(
            {
                "section_id": section_id,
                "chart_id": chart_id,
                "goal_id": goal_id,
                "goal_kind": str(goal.get("kind", "unknown")),
                "source_commitment_id": commitment_id,
                "source_seed_digest": seed.get("commitment_seed_digest"),
                "local_frame": f"{goal.get('kind', 'unknown')}:frame:0",
                "gauge_frame_index": 0,
                "gauge_invariant_signature": gauge_invariant_signature,
                "connection_potential": _clamp(goal.get("priority_score")),
                "curvature_norm": 0.0,
                "transport_kind": _initial_transport_kind(str(commitment.get("next_move", "explore"))),
                "status": "ready",
                "action_scale": _clamp(commitment.get("action_scale")),
                "progress": 0.0,
                "transport_count": 0,
                "created_epoch": epoch,
                "last_updated_epoch": epoch,
                "repairable": commitment.get("repairable") is True,
                "replan_after_effect": commitment.get("replan_after_effect") is True,
                "candidate_weighting_not_truth": True,
            }
        )
        existing.add(commitment_id)
        added += 1
    bundle["local_sections"] = sections
    return added


def _find_section(sections: list[dict[str, Any]], section_id: str) -> dict[str, Any] | None:
    for section in sections:
        if str(section.get("section_id", "")) == section_id:
            return section
    return None


def _curvature_norm(effect: Mapping[str, Any]) -> float:
    benefit = _clamp(effect.get("observed_benefit"))
    harm = _clamp(effect.get("observed_harm"))
    recoverability = _clamp(effect.get("recoverability"))
    confidence = _clamp(effect.get("confidence"))
    outcome_bias = {
        "success": 0.0,
        "partial": 0.08,
        "failure": 0.28,
        "blocked": 0.32,
        "uncertain": 0.22,
    }.get(str(effect.get("outcome", "")), 0.25)
    value = 0.34 * harm + 0.22 * (1.0 - benefit) + 0.16 * (1.0 - confidence) + 0.10 * (1.0 - recoverability) + outcome_bias
    return round(max(0.0, min(1.0, value)), 6)


def _correction_kind(outcome: str, continuation: str, harm: float, transport_count: int, maximum: int) -> str | None:
    if outcome == "success" and continuation == "complete" and harm < 0.5:
        return None
    if harm >= 0.7 or continuation == "repair":
        return "local_repair_gauge" if transport_count < maximum else "handover_or_redesign"
    if continuation == "reobserve":
        return "curvature_reobservation"
    if continuation == "expand":
        return "section_extension"
    if outcome == "success":
        return "effect_integration_transport"
    if outcome == "partial":
        return "scaled_parallel_transport"
    if outcome == "failure":
        return "local_repair_gauge" if transport_count < maximum else "handover_or_redesign"
    if outcome == "blocked":
        return "chart_transition" if transport_count < maximum else "handover_or_redesign"
    return "curvature_reobservation"


def _next_scale(old: float, correction: str | None, minimum: float) -> float:
    factor = {
        "effect_integration_transport": 1.0,
        "scaled_parallel_transport": 0.75,
        "local_repair_gauge": 0.50,
        "chart_transition": 0.45,
        "curvature_reobservation": 0.35,
        "section_extension": 0.80,
        "handover_or_redesign": 0.25,
    }.get(correction or "", 0.0)
    if correction is None:
        return 0.0
    return round(max(minimum, min(1.0, old * factor)), 6)


def _apply_effect_as_curvature(
    bundle: dict[str, Any],
    effect: Mapping[str, Any],
    epoch: int,
    max_transports: int,
    min_scale: float,
    blockers: list[str],
) -> int:
    sections = [dict(_mapping(section)) for section in _list(bundle.get("local_sections"))]
    section_id = str(effect.get("section_id", ""))
    section = _find_section(sections, section_id)
    if section is None:
        blockers.append("effect_target_section_missing")
        return 0
    if section.get("status") != "awaiting_effect":
        blockers.append("effect_target_section_not_awaiting")
        return 0

    outcome = str(effect.get("outcome", ""))
    continuation = str(effect.get("continuation_signal", "continue"))
    harm = _clamp(effect.get("observed_harm"))
    benefit = _clamp(effect.get("observed_benefit"))
    recoverability = _clamp(effect.get("recoverability"))
    confidence = _clamp(effect.get("confidence"))
    transport_count = _integer(section.get("transport_count"), 0)
    curvature = _curvature_norm(effect)
    correction = _correction_kind(outcome, continuation, harm, transport_count, max_transports)

    section["progress"] = round(min(1.0, _clamp(section.get("progress")) + _clamp(effect.get("progress_delta"))), 6)
    section["curvature_norm"] = curvature
    section["last_effect_receipt_digest"] = effect.get("effect_receipt_digest")
    section["last_effect_outcome"] = outcome
    section["observed_benefit"] = benefit
    section["observed_harm"] = harm
    section["effect_confidence"] = confidence
    section["last_updated_epoch"] = epoch
    section["connection_potential"] = round(
        max(0.0, min(1.0, _clamp(section.get("connection_potential")) + 0.10 * benefit - 0.18 * harm - 0.12 * curvature)),
        6,
    )

    if correction is None:
        section["status"] = "flat_complete"
        section["transport_kind"] = "none"
        section["action_scale"] = 0.0
        section["gauge_correction_applied"] = False
    elif correction == "handover_or_redesign":
        section["status"] = "handed_over"
        section["transport_kind"] = correction
        section["action_scale"] = _next_scale(_clamp(section.get("action_scale")), correction, min_scale)
        section["gauge_correction_applied"] = True
    else:
        section["status"] = "ready"
        section["transport_kind"] = correction
        section["action_scale"] = _next_scale(_clamp(section.get("action_scale")), correction, min_scale)
        section["gauge_frame_index"] = _integer(section.get("gauge_frame_index"), 0) + 1
        section["local_frame"] = f"{section.get('goal_kind', 'unknown')}:frame:{section['gauge_frame_index']}"
        section["gauge_correction_applied"] = True

    correction_id = "gauge-transform-" + _sha(
        {"section": section_id, "effect": effect.get("effect_receipt_digest"), "correction": correction}
    )[:18]
    section["last_gauge_transform_id"] = correction_id

    for index, candidate in enumerate(sections):
        if candidate.get("section_id") == section_id:
            sections[index] = section
            break
    bundle["local_sections"] = sections
    bundle["active_action_id"] = ""
    bundle["active_section_id"] = ""
    bundle["last_effect_receipt_digest"] = effect.get("effect_receipt_digest")
    bundle.setdefault("curvature_history", []).append(
        {
            "effect_receipt_digest": effect.get("effect_receipt_digest"),
            "section_id": section_id,
            "outcome": outcome,
            "curvature_norm": curvature,
            "correction_kind": correction or "flat_completion",
            "gauge_transform_id": correction_id,
            "epoch_index": epoch,
        }
    )
    bundle.setdefault("holonomy_trace", []).append(
        {
            "transport_action_digest": effect.get("source_action_digest"),
            "effect_receipt_digest": effect.get("effect_receipt_digest"),
            "section_id": section_id,
            "chart_id": section.get("chart_id"),
            "frame_after_transport": section.get("local_frame"),
            "curvature_norm": curvature,
            "path_dependent_memory_preserved": True,
        }
    )
    return 1


def _covariant_selection_score(section: Mapping[str, Any], epoch: int, last_goal_id: str) -> float:
    age = max(0, epoch - _integer(section.get("created_epoch"), epoch))
    curvature_pressure = 0.22 * _clamp(section.get("curvature_norm"))
    correction_boost = 0.08 if str(section.get("transport_kind", "")) in {
        "local_repair_gauge",
        "curvature_reobservation",
        "chart_transition",
    } else 0.0
    plurality_boost = 0.05 if str(section.get("goal_id", "")) != last_goal_id else 0.0
    return (
        _clamp(section.get("connection_potential"))
        + curvature_pressure
        + min(0.12, age * 0.015)
        + correction_boost
        + plurality_boost
    )


def _prepare_covariant_action(bundle: dict[str, Any], epoch: int, min_scale: float) -> dict[str, Any]:
    sections = [dict(_mapping(section)) for section in _list(bundle.get("local_sections"))]
    ready = [section for section in sections if section.get("status") == "ready"]
    if not ready:
        bundle["local_sections"] = sections
        return {
            "version": ACTION_VERSION,
            "action_ready": False,
            "action_id": "",
            "section_id": "",
            "goal_id": "",
            "covariant_step_kind": "none",
            "action_scale": 0.0,
            "transport_index": 0,
            "execution_posture": "awaiting_new_telos_or_curvature_event",
            "source_bundle_digest": "",
            "covariant_action_digest": "",
        }
    last_goal_id = str(bundle.get("last_transported_goal_id", ""))
    selected = sorted(
        ready,
        key=lambda section: (-_covariant_selection_score(section, epoch, last_goal_id), str(section.get("section_id", ""))),
    )[0]
    selected["status"] = "awaiting_effect"
    selected["transport_count"] = _integer(selected.get("transport_count"), 0) + 1
    selected["last_updated_epoch"] = epoch
    for index, candidate in enumerate(sections):
        if candidate.get("section_id") == selected.get("section_id"):
            sections[index] = selected
            break
    action_id = "action-" + _sha(
        {"section": selected.get("section_id"), "transport": selected.get("transport_count"), "epoch": epoch}
    )[:18]
    connection_digest = _sha(
        {
            "section_id": selected.get("section_id"),
            "chart_id": selected.get("chart_id"),
            "gauge_invariant_signature": selected.get("gauge_invariant_signature"),
            "connection_potential": selected.get("connection_potential"),
            "curvature_norm": selected.get("curvature_norm"),
            "transport_kind": selected.get("transport_kind"),
        }
    )
    bundle["local_sections"] = sections
    bundle["active_action_id"] = action_id
    bundle["active_section_id"] = selected.get("section_id")
    bundle["last_transported_goal_id"] = selected.get("goal_id")
    return {
        "version": ACTION_VERSION,
        "action_ready": True,
        "action_id": action_id,
        "section_id": selected.get("section_id"),
        "chart_id": selected.get("chart_id"),
        "goal_id": selected.get("goal_id"),
        "goal_kind": selected.get("goal_kind"),
        "covariant_step_kind": selected.get("transport_kind"),
        "action_scale": max(min_scale, _clamp(selected.get("action_scale"))),
        "transport_index": selected.get("transport_count"),
        "connection_digest": connection_digest,
        "gauge_invariant_signature": selected.get("gauge_invariant_signature"),
        "curvature_before_action": selected.get("curvature_norm"),
        "progress_before_action": selected.get("progress"),
        "execution_posture": "covariant_action_prepared",
        "effect_receipt_required": True,
        "gauge_frame_representation_only": selected.get("local_frame"),
        "candidate_weighting_not_truth": True,
        "source_bundle_digest": "",
        "covariant_action_digest": "",
    }


def _count_sections(sections: Sequence[Any]) -> tuple[int, int]:
    ready = 0
    terminal = 0
    for raw in sections:
        status = str(_mapping(raw).get("status", ""))
        if status == "ready":
            ready += 1
        if status in TERMINAL_SECTION_STATES:
            terminal += 1
    return ready, terminal


def build_open_horizon_commitment_gauge(
    *,
    runtime_context: Mapping[str, Any],
    gauge_plan: Mapping[str, Any],
    gauge_license: Mapping[str, Any],
    effect_receipt: Mapping[str, Any] | None = None,
) -> OpenHorizonCommitmentGaugeResult:
    context = _mapping(runtime_context)
    plan = _mapping(gauge_plan)
    license_packet = _mapping(gauge_license)
    effect = _mapping(effect_receipt)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root_path(context.get("runtime_root"), blockers)

    telos_state_path = root / "kuuos_open_horizon_telos_state_v0_1.json"
    goal_set_path = root / "kuuos_open_horizon_goal_set_v0_1.json"
    seed_path = root / "kuuos_open_horizon_commitment_seed_v0_1.json"
    bundle_path = root / "kuuos_open_horizon_commitment_gauge_bundle_v0_2.json"
    state_path = root / "kuuos_open_horizon_commitment_gauge_state_v0_2.json"
    action_path = root / "kuuos_open_horizon_covariant_action_v0_2.json"
    receipt_path = root / "kuuos_open_horizon_commitment_gauge_receipt_v0_2.json"
    ledger_path = root / "kuuos_open_horizon_commitment_gauge_ledger_v0_2.jsonl"
    audit_path = root / "kuuos_open_horizon_commitment_gauge_audit_v0_2.jsonl"

    if context.get("open_horizon_commitment_gauge_enabled") is not True:
        blockers.append("open_horizon_commitment_gauge_enabled_not_true")
    if context.get("apply_open_horizon_commitment_gauge") is not True:
        blockers.append("apply_open_horizon_commitment_gauge_not_true")

    telos_state = _read_json(telos_state_path)
    goal_set = _read_json(goal_set_path)
    seed = _read_json(seed_path)
    existing_bundle = _read_json(bundle_path)
    existing_state = _read_json(state_path)
    current_action = _read_json(action_path)
    ledger = _read_jsonl(ledger_path)

    max_sections, max_new, max_transports, min_scale = _validate_plan(plan, blockers)
    _validate_source(telos_state, goal_set, seed, plan, blockers)
    _validate_existing_bundle(existing_bundle, existing_state, blockers)
    _validate_current_action(existing_bundle, current_action, blockers)
    source_is_new = _validate_source_continuity(existing_state, telos_state, blockers)
    _validate_effect(effect, plan, current_action, blockers)
    _validate_license(license_packet, plan, telos_state, goal_set, seed, effect, blockers)

    expected_previous = str(plan.get("expected_previous_gauge_state_digest", ""))
    if existing_state:
        if expected_previous != existing_state.get("gauge_state_digest"):
            blockers.append("previous_gauge_state_digest_mismatch")
    elif expected_previous:
        blockers.append("previous_gauge_state_missing")

    run_id = str(plan.get("gauge_run_id", ""))
    if any(row.get("_invalid") for row in ledger):
        blockers.append("gauge_ledger_invalid")
    if any(str(row.get("gauge_run_id", "")) == run_id for row in ledger):
        blockers.append("gauge_run_replay_detected")
    effect_sha = str(effect.get("effect_receipt_digest", ""))
    if effect_sha and any(str(row.get("effect_receipt_digest", "")) == effect_sha for row in ledger):
        blockers.append("effect_receipt_replay_detected")

    epoch = _integer(existing_state.get("epoch_index"), 0) + 1 if existing_state else 1
    bundle = dict(existing_bundle) if existing_bundle else {
        "version": BUNDLE_VERSION,
        "bundle_id": "bundle-" + _sha(
            {"agent": plan.get("agent_id"), "first_telos_state": telos_state.get("telos_state_digest")}
        )[:18],
        "agent_id": plan.get("agent_id"),
        "base_manifold": {
            "coordinates": ["telos_generation", "commitment_phase", "effect_epoch"],
            "open_horizon": True,
            "global_task_list_fixed": False,
        },
        "structure_group": "contextual_commitment_gauge_group",
        "local_sections": [],
        "curvature_history": [],
        "holonomy_trace": [],
        "integrated_telos_lineage": [],
        "active_action_id": "",
        "active_section_id": "",
        "last_transported_goal_id": "",
        "last_effect_receipt_digest": "",
    }

    integrated_count = 0
    curvature_updates = 0
    effect_applied = False
    action = dict(current_action) if current_action else {}
    state: dict[str, Any] = {}
    execution_posture = "blocked"
    stop_reason = "validation_blocked"
    mutated = False
    preserve_existing_action = False
    outstanding = (
        bool(existing_bundle)
        and bool(current_action)
        and current_action.get("action_ready") is True
        and str(existing_bundle.get("active_action_id", "")) == str(current_action.get("action_id", ""))
    )

    if not blockers:
        if len(_list(bundle.get("local_sections"))) > max_sections:
            blockers.append("gauge_bundle_section_budget_exceeded")

        if not blockers and effect:
            curvature_updates = _apply_effect_as_curvature(
                bundle, effect, epoch, max_transports, min_scale, blockers
            )
            effect_applied = not blockers
            mutated = mutated or effect_applied
            outstanding = False

        missing = _missing_commitment_count(bundle, seed)
        if not blockers and missing > 0:
            integrated_count = _extend_bundle_sections(
                bundle,
                goal_set,
                seed,
                epoch,
                min(max_new, max_sections - len(_list(bundle.get("local_sections")))),
                blockers,
            )
            lineage = bundle.setdefault("integrated_telos_lineage", [])
            matching = next(
                (
                    entry
                    for entry in lineage
                    if _mapping(entry).get("telos_state_digest") == telos_state.get("telos_state_digest")
                ),
                None,
            )
            if matching is None:
                lineage.append(
                    {
                        "generation_index": telos_state.get("generation_index"),
                        "telos_state_digest": telos_state.get("telos_state_digest"),
                        "goal_set_digest": goal_set.get("goal_set_digest"),
                        "commitment_seed_digest": seed.get("commitment_seed_digest"),
                        "integrated_section_count": integrated_count,
                    }
                )
            else:
                matching["integrated_section_count"] = _integer(
                    _mapping(matching).get("integrated_section_count"), 0
                ) + integrated_count
            mutated = mutated or integrated_count > 0
        elif not blockers and source_is_new:
            bundle.setdefault("integrated_telos_lineage", []).append(
                {
                    "generation_index": telos_state.get("generation_index"),
                    "telos_state_digest": telos_state.get("telos_state_digest"),
                    "goal_set_digest": goal_set.get("goal_set_digest"),
                    "commitment_seed_digest": seed.get("commitment_seed_digest"),
                    "integrated_section_count": 0,
                }
            )
            mutated = True

        if not blockers:
            if outstanding and not effect:
                action = current_action
                execution_posture = "awaiting_curvature_receipt"
                stop_reason = "outstanding_covariant_action_preserved"
                preserve_existing_action = True
            else:
                action = _prepare_covariant_action(bundle, epoch, min_scale)
                execution_posture = str(action.get("execution_posture", "unknown"))
                stop_reason = (
                    "next_covariant_action_prepared"
                    if action.get("action_ready") is True
                    else "local_sections_flat_or_empty_horizon_open"
                )
                mutated = True

        if not blockers and mutated:
            bundle["version"] = BUNDLE_VERSION
            bundle["agent_id"] = plan.get("agent_id")
            bundle["epoch_index"] = epoch
            bundle["last_integrated_telos_generation"] = telos_state.get("generation_index")
            bundle["last_integrated_telos_state_digest"] = telos_state.get("telos_state_digest")
            bundle["last_integrated_goal_set_digest"] = goal_set.get("goal_set_digest")
            bundle["last_integrated_commitment_seed_digest"] = seed.get("commitment_seed_digest")
            bundle["gauge_covariant"] = True
            bundle["gauge_bundle_digest"] = bundle_digest(bundle)
            if preserve_existing_action:
                action = dict(current_action)
            else:
                action["source_bundle_digest"] = bundle["gauge_bundle_digest"]
                action["covariant_action_digest"] = action_digest(action)
            state = {
                "version": STATE_VERSION,
                "agent_id": plan.get("agent_id"),
                "gauge_run_id": run_id,
                "epoch_index": epoch,
                "previous_gauge_state_digest": existing_state.get("gauge_state_digest", ""),
                "gauge_bundle_digest": bundle["gauge_bundle_digest"],
                "covariant_action_digest": action["covariant_action_digest"],
                "last_integrated_telos_generation": telos_state.get("generation_index"),
                "last_integrated_telos_state_digest": telos_state.get("telos_state_digest"),
                "last_integrated_goal_set_digest": goal_set.get("goal_set_digest"),
                "last_integrated_commitment_seed_digest": seed.get("commitment_seed_digest"),
                "last_effect_receipt_digest": effect_sha,
                "open_horizon": True,
                "renewable_horizon": True,
                "gauge_covariant": True,
                "global_task_list_fixed": False,
                "one_covariant_action_prepared": action.get("action_ready") is True,
                "execution_posture": execution_posture,
                "stop_reason": stop_reason,
                "epoch": int(time.time()),
            }
            state["gauge_state_digest"] = state_digest(state)
            _write_json(bundle_path, bundle)
            if not preserve_existing_action:
                _write_json(action_path, action)
            _write_json(state_path, state)
            record = {
                "version": LEDGER_VERSION,
                "gauge_run_id": run_id,
                "epoch_index": epoch,
                "source_telos_state_digest": telos_state.get("telos_state_digest"),
                "effect_receipt_digest": effect_sha,
                "previous_gauge_state_digest": existing_state.get("gauge_state_digest", ""),
                "gauge_state_digest": state["gauge_state_digest"],
                "gauge_bundle_digest": bundle["gauge_bundle_digest"],
                "covariant_action_digest": action["covariant_action_digest"],
                "integrated_section_count": integrated_count,
                "curvature_update_count": curvature_updates,
                "record_digest": "",
            }
            record["record_digest"] = _sha(_without(record, "record_digest"))
            _append_jsonl(ledger_path, record)
        elif not blockers and not mutated:
            state = existing_state
            poll = {
                "version": LEDGER_VERSION,
                "gauge_run_id": run_id,
                "epoch_index": _integer(existing_state.get("epoch_index"), 0),
                "record_kind": "awaiting_curvature_poll",
                "source_telos_state_digest": telos_state.get("telos_state_digest"),
                "effect_receipt_digest": "",
                "previous_gauge_state_digest": existing_state.get("previous_gauge_state_digest", ""),
                "gauge_state_digest": existing_state.get("gauge_state_digest", ""),
                "gauge_bundle_digest": existing_bundle.get("gauge_bundle_digest", ""),
                "covariant_action_digest": current_action.get("covariant_action_digest", ""),
                "integrated_section_count": 0,
                "curvature_update_count": 0,
                "record_digest": "",
            }
            poll["record_digest"] = _sha(_without(poll, "record_digest"))
            _append_jsonl(ledger_path, poll)

    if blockers:
        execution_posture = "blocked"
        stop_reason = "validation_blocked"

    sections = _list(bundle.get("local_sections"))
    ready_count, terminal_count = _count_sections(sections)
    status = READY if not blockers else BLOCKED
    packet_id = "kuuos-open-horizon-gauge-" + _sha(
        {"run": run_id, "epoch": epoch, "effect": effect_sha, "blockers": blockers}
    )[:18]
    receipt = {
        "version": VERSION,
        "status": status,
        "packet_id": packet_id,
        "gauge_run_id": run_id,
        "epoch_index": epoch,
        "source_telos_generation": _integer(telos_state.get("generation_index"), 0),
        "section_count": len(sections),
        "ready_section_count": ready_count,
        "terminal_section_count": terminal_count,
        "integrated_section_count": integrated_count,
        "curvature_update_count": curvature_updates,
        "holonomy_depth": len(_list(bundle.get("holonomy_trace"))),
        "effect_applied": effect_applied,
        "action_ready": action.get("action_ready") is True,
        "covariant_step_kind": str(action.get("covariant_step_kind", "none")),
        "active_section_id": str(action.get("section_id", "")),
        "execution_posture": execution_posture,
        "stop_reason": stop_reason,
        "state_digest": state.get("gauge_state_digest", ""),
        "bundle_digest": bundle.get("gauge_bundle_digest", ""),
        "action_digest": action.get("covariant_action_digest", ""),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if license_packet.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if license_packet.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})

    return OpenHorizonCommitmentGaugeResult(
        VERSION,
        status,
        packet_id,
        str(root),
        epoch,
        _integer(telos_state.get("generation_index"), 0),
        len(sections),
        ready_count,
        terminal_count,
        integrated_count,
        curvature_updates,
        len(_list(bundle.get("holonomy_trace"))),
        effect_applied,
        action.get("action_ready") is True,
        str(action.get("covariant_step_kind", "none")),
        str(action.get("section_id", "")),
        execution_posture,
        stop_reason,
        str(state_path),
        str(bundle_path),
        str(action_path),
        str(receipt_path),
        str(ledger_path),
        str(audit_path),
        blockers,
        warnings,
    )
