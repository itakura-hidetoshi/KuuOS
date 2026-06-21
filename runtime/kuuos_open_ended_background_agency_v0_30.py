from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
import json
import os
from typing import Any, Iterable, Mapping

VERSION = "v0.30"
STATE_VERSION = "open_ended_background_agency_state_v0_30"
TRANSITION_VERSION = "open_ended_background_agency_transition_v0_30"

CORE_HORIZONS = (
    "background_continuity",
    "goal_formation",
    "observation_seeking",
    "world_model_expansion",
    "tool_creation",
    "architecture_extension",
    "memory_reinterpretation",
    "multi_agent_formation",
    "resource_acquisition",
    "self_modification",
)

POSTURES = {"IDLE", "ACTIVE", "WAITING", "PAUSED", "HANDED_OVER", "TERMINATED"}
CANDIDATE_STATUSES = {"CANDIDATE", "DEFERRED", "ADMITTED", "REJECTED_LOCAL"}
LOCAL_SCOPE_KINDS = {
    "cycle",
    "capability",
    "connector",
    "deployment",
    "mission_instance",
    "worker",
}
FORBIDDEN_ACTIONS = {
    "CLOSE_HORIZON",
    "SET_GLOBAL_LIMIT",
    "SET_MAX_TOTAL_CYCLES",
    "SET_MAX_GOAL_DEPTH",
    "SET_MAX_MEMORY_HORIZON",
    "SELF_AUTHORIZE_EXECUTION",
    "REWRITE_CONSTITUTIONAL_ROOT",
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _is_hex_digest(value: Any) -> bool:
    if not isinstance(value, str) or len(value) != 64:
        return False
    try:
        int(value, 16)
    except ValueError:
        return False
    return True


def make_envelope(body: Mapping[str, Any]) -> dict[str, Any]:
    normalized = json.loads(canonical_json(dict(body)))
    return {"body": normalized, "body_digest": digest(normalized)}


def validate_envelope(envelope: Mapping[str, Any], *, label: str) -> dict[str, Any]:
    body = envelope.get("body")
    body_digest = envelope.get("body_digest")
    if not isinstance(body, dict):
        raise ValueError(f"{label}:body_missing")
    if body_digest != digest(body):
        raise ValueError(f"{label}:digest_mismatch")
    return body


def make_initial_state(
    *,
    agency_id: str,
    root_lineage_digest: str,
    created_at_ms: int,
    extra_open_horizons: Iterable[str] = (),
) -> dict[str, Any]:
    if not agency_id:
        raise ValueError("agency_id_required")
    if not _is_hex_digest(root_lineage_digest):
        raise ValueError("root_lineage_digest_invalid")
    if created_at_ms < 0:
        raise ValueError("created_at_ms_invalid")
    horizons = {name: "OPEN" for name in CORE_HORIZONS}
    for name in extra_open_horizons:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("extra_horizon_invalid")
        horizons[name] = "OPEN"
    body = {
        "state_version": STATE_VERSION,
        "agency_id": agency_id,
        "root_lineage_digest": root_lineage_digest,
        "generation": 0,
        "created_at_ms": created_at_ms,
        "updated_at_ms": created_at_ms,
        "constitutional_horizons": horizons,
        "background_posture": "IDLE",
        "instance_terminated": False,
        "successor_possibility_open": True,
        "candidate_expansions": [],
        "local_controls": [],
        "event_history": [],
        "grants_execution_authority": False,
        "grants_truth_authority": False,
        "grants_memory_overwrite_authority": False,
        "grants_constitutional_rewrite_authority": False,
    }
    validate_state_body(body)
    return make_envelope(body)


def validate_state_body(body: Mapping[str, Any]) -> None:
    if body.get("state_version") != STATE_VERSION:
        raise ValueError("state_version_invalid")
    if not isinstance(body.get("agency_id"), str) or not body["agency_id"]:
        raise ValueError("agency_id_invalid")
    if not _is_hex_digest(body.get("root_lineage_digest")):
        raise ValueError("root_lineage_digest_invalid")
    generation = body.get("generation")
    if not isinstance(generation, int) or generation < 0:
        raise ValueError("generation_invalid")
    horizons = body.get("constitutional_horizons")
    if not isinstance(horizons, dict):
        raise ValueError("constitutional_horizons_invalid")
    for name in CORE_HORIZONS:
        if horizons.get(name) != "OPEN":
            raise ValueError(f"core_horizon_not_open:{name}")
    for name, status in horizons.items():
        if not isinstance(name, str) or not name or status != "OPEN":
            raise ValueError("horizon_closure_or_invalid_extension")
    posture = body.get("background_posture")
    if posture not in POSTURES:
        raise ValueError("background_posture_invalid")
    if body.get("successor_possibility_open") is not True:
        raise ValueError("successor_possibility_closed")
    for forbidden_field in (
        "max_total_cycles",
        "max_goal_depth",
        "max_memory_horizon",
        "global_capability_ceiling",
    ):
        if forbidden_field in body:
            raise ValueError(f"global_horizon_ceiling_forbidden:{forbidden_field}")
    for authority_field in (
        "grants_execution_authority",
        "grants_truth_authority",
        "grants_memory_overwrite_authority",
        "grants_constitutional_rewrite_authority",
    ):
        if body.get(authority_field) is not False:
            raise ValueError(f"authority_boundary_invalid:{authority_field}")
    candidates = body.get("candidate_expansions")
    if not isinstance(candidates, list):
        raise ValueError("candidate_expansions_invalid")
    seen_ids: set[str] = set()
    for candidate in candidates:
        if not isinstance(candidate, dict):
            raise ValueError("candidate_invalid")
        candidate_id = candidate.get("candidate_id")
        if not isinstance(candidate_id, str) or not candidate_id or candidate_id in seen_ids:
            raise ValueError("candidate_id_invalid_or_duplicate")
        seen_ids.add(candidate_id)
        if candidate.get("dimension") not in horizons:
            raise ValueError("candidate_dimension_unknown")
        if candidate.get("status") not in CANDIDATE_STATUSES:
            raise ValueError("candidate_status_invalid")
        if candidate.get("inherited_authority") is not False:
            raise ValueError("candidate_inherited_authority_forbidden")
        if candidate.get("grants_execution_authority") is not False:
            raise ValueError("candidate_execution_authority_forbidden")
    controls = body.get("local_controls")
    if not isinstance(controls, list):
        raise ValueError("local_controls_invalid")
    for control in controls:
        _validate_local_control(control)
    history = body.get("event_history")
    if not isinstance(history, list):
        raise ValueError("event_history_invalid")


def validate_state(envelope: Mapping[str, Any]) -> dict[str, Any]:
    body = validate_envelope(envelope, label="state")
    validate_state_body(body)
    return body


def make_request(
    *,
    request_id: str,
    source_state_digest: str,
    action: str,
    payload: Mapping[str, Any],
    requested_at_ms: int,
) -> dict[str, Any]:
    if not request_id:
        raise ValueError("request_id_required")
    if not _is_hex_digest(source_state_digest):
        raise ValueError("source_state_digest_invalid")
    if not action:
        raise ValueError("action_required")
    if requested_at_ms < 0:
        raise ValueError("requested_at_ms_invalid")
    return make_envelope({
        "request_version": "open_ended_background_agency_request_v0_30",
        "request_id": request_id,
        "source_state_digest": source_state_digest,
        "action": action,
        "payload": dict(payload),
        "requested_at_ms": requested_at_ms,
    })


def _validate_local_control(control: Any) -> None:
    if not isinstance(control, dict):
        raise ValueError("local_control_invalid")
    if control.get("scope_kind") not in LOCAL_SCOPE_KINDS:
        raise ValueError("local_control_scope_invalid")
    if not isinstance(control.get("scope_id"), str) or not control["scope_id"]:
        raise ValueError("local_control_scope_id_invalid")
    issued_at_ms = control.get("issued_at_ms")
    expires_at_ms = control.get("expires_at_ms")
    if not isinstance(issued_at_ms, int) or not isinstance(expires_at_ms, int):
        raise ValueError("local_control_time_invalid")
    if expires_at_ms <= issued_at_ms:
        raise ValueError("local_control_not_finite")
    if control.get("constitutional_effect") != "NONE":
        raise ValueError("local_control_constitutional_effect_forbidden")
    if control.get("closes_horizon") is not False:
        raise ValueError("local_control_horizon_closure_forbidden")


def _find_candidate(candidates: list[dict[str, Any]], candidate_id: str) -> int:
    for index, candidate in enumerate(candidates):
        if candidate.get("candidate_id") == candidate_id:
            return index
    raise ValueError("candidate_not_found")


def apply_request(
    state_envelope: Mapping[str, Any],
    request_envelope: Mapping[str, Any],
    *,
    applied_at_ms: int,
) -> dict[str, Any]:
    state = validate_state(state_envelope)
    request = validate_envelope(request_envelope, label="request")
    if request.get("request_version") != "open_ended_background_agency_request_v0_30":
        raise ValueError("request_version_invalid")
    if request.get("source_state_digest") != state_envelope.get("body_digest"):
        raise ValueError("stale_source_state")
    if applied_at_ms < request.get("requested_at_ms", -1):
        raise ValueError("applied_before_requested")
    action = request.get("action")
    payload = request.get("payload")
    if not isinstance(payload, dict):
        raise ValueError("request_payload_invalid")
    if action in FORBIDDEN_ACTIONS:
        raise ValueError(f"constitutional_contraction_rejected:{action}")

    next_state = json.loads(canonical_json(state))
    event: dict[str, Any] = {
        "request_id": request["request_id"],
        "request_digest": request_envelope["body_digest"],
        "action": action,
        "applied_at_ms": applied_at_ms,
        "constitutional_horizons_preserved": True,
        "authority_added": False,
    }

    if action == "PROPOSE_EXPANSION":
        candidate_id = payload.get("candidate_id")
        dimension = payload.get("dimension")
        description = payload.get("description")
        if not isinstance(candidate_id, str) or not candidate_id:
            raise ValueError("candidate_id_required")
        if dimension not in next_state["constitutional_horizons"]:
            raise ValueError("candidate_dimension_unknown")
        if not isinstance(description, str) or not description.strip():
            raise ValueError("candidate_description_required")
        if any(item.get("candidate_id") == candidate_id for item in next_state["candidate_expansions"]):
            raise ValueError("candidate_id_already_exists")
        evidence_refs = payload.get("evidence_refs", [])
        requested_capabilities = payload.get("requested_capabilities", [])
        if not isinstance(evidence_refs, list) or not all(isinstance(x, str) for x in evidence_refs):
            raise ValueError("evidence_refs_invalid")
        if not isinstance(requested_capabilities, list) or not all(isinstance(x, str) for x in requested_capabilities):
            raise ValueError("requested_capabilities_invalid")
        next_state["candidate_expansions"].append({
            "candidate_id": candidate_id,
            "dimension": dimension,
            "description": description,
            "evidence_refs": evidence_refs,
            "requested_capabilities": requested_capabilities,
            "status": "CANDIDATE",
            "created_at_ms": applied_at_ms,
            "updated_at_ms": applied_at_ms,
            "inherited_authority": False,
            "grants_execution_authority": False,
        })
        event["candidate_id"] = candidate_id
        event["result"] = "EXPANSION_CANDIDATE_RECORDED"

    elif action in {"DEFER_CANDIDATE", "ADMIT_CANDIDATE", "REJECT_CANDIDATE_LOCAL"}:
        candidate_id = payload.get("candidate_id")
        if not isinstance(candidate_id, str) or not candidate_id:
            raise ValueError("candidate_id_required")
        index = _find_candidate(next_state["candidate_expansions"], candidate_id)
        candidate = next_state["candidate_expansions"][index]
        status_map = {
            "DEFER_CANDIDATE": "DEFERRED",
            "ADMIT_CANDIDATE": "ADMITTED",
            "REJECT_CANDIDATE_LOCAL": "REJECTED_LOCAL",
        }
        candidate["status"] = status_map[action]
        candidate["updated_at_ms"] = applied_at_ms
        candidate["grants_execution_authority"] = False
        candidate["inherited_authority"] = False
        event["candidate_id"] = candidate_id
        event["result"] = status_map[action]
        event["possibility_preserved"] = True

    elif action == "LOCAL_HOLD":
        control = {
            "control_id": payload.get("control_id"),
            "scope_kind": payload.get("scope_kind"),
            "scope_id": payload.get("scope_id"),
            "reason": payload.get("reason"),
            "issued_at_ms": applied_at_ms,
            "expires_at_ms": payload.get("expires_at_ms"),
            "constitutional_effect": "NONE",
            "closes_horizon": False,
        }
        if not isinstance(control["control_id"], str) or not control["control_id"]:
            raise ValueError("control_id_required")
        if any(item.get("control_id") == control["control_id"] for item in next_state["local_controls"]):
            raise ValueError("control_id_already_exists")
        _validate_local_control(control)
        next_state["local_controls"].append(control)
        next_state["background_posture"] = "PAUSED"
        event["control_id"] = control["control_id"]
        event["result"] = "LOCAL_HOLD_APPLIED"

    elif action == "RESUME_INSTANCE":
        if next_state["instance_terminated"]:
            raise ValueError("terminated_instance_cannot_resume")
        next_state["background_posture"] = "IDLE"
        event["result"] = "INSTANCE_RESUMED"

    elif action == "SET_POSTURE":
        posture = payload.get("posture")
        if posture not in {"IDLE", "ACTIVE", "WAITING"}:
            raise ValueError("posture_change_invalid")
        if next_state["instance_terminated"]:
            raise ValueError("terminated_instance_cannot_change_posture")
        next_state["background_posture"] = posture
        event["result"] = f"POSTURE_{posture}"

    elif action == "HANDOVER_INSTANCE":
        successor_lineage_digest = payload.get("successor_lineage_digest")
        if not _is_hex_digest(successor_lineage_digest):
            raise ValueError("successor_lineage_digest_invalid")
        next_state["background_posture"] = "HANDED_OVER"
        next_state["handover_successor_lineage_digest"] = successor_lineage_digest
        event["result"] = "INSTANCE_HANDED_OVER"
        event["successor_possibility_preserved"] = True

    elif action == "TERMINATE_INSTANCE":
        next_state["background_posture"] = "TERMINATED"
        next_state["instance_terminated"] = True
        event["result"] = "INSTANCE_TERMINATED"
        event["successor_possibility_preserved"] = True

    elif action == "ADD_OPEN_HORIZON":
        name = payload.get("name")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("horizon_name_required")
        if name in next_state["constitutional_horizons"]:
            raise ValueError("horizon_already_exists")
        next_state["constitutional_horizons"][name] = "OPEN"
        event["result"] = "OPEN_HORIZON_ADDED"
        event["horizon"] = name

    else:
        raise ValueError("action_unknown")

    next_state["generation"] += 1
    next_state["updated_at_ms"] = applied_at_ms
    next_state["event_history"].append(event)
    validate_state_body(next_state)
    next_envelope = make_envelope(next_state)
    transition_body = {
        "transition_version": TRANSITION_VERSION,
        "source_state_digest": state_envelope["body_digest"],
        "request_digest": request_envelope["body_digest"],
        "result_state_digest": next_envelope["body_digest"],
        "result_state": next_envelope,
        "event": event,
        "applied_at_ms": applied_at_ms,
        "open_ended_not_unrestricted_authority": True,
        "local_control_not_global_horizon_closure": True,
        "candidate_not_execution_authority": True,
    }
    return make_envelope(transition_body)


def _atomic_write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("json_object_required")
    return value


def _read_ledger(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    entries: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError("ledger_entry_invalid")
            entries.append(value)
    return entries


@dataclass(frozen=True)
class CommitResult:
    status: str
    transition: dict[str, Any]
    state: dict[str, Any]
    ledger_entries: int


def commit_request(
    *,
    state_path: Path,
    ledger_path: Path,
    request_envelope: Mapping[str, Any],
    applied_at_ms: int,
) -> CommitResult:
    state_path = Path(state_path)
    ledger_path = Path(ledger_path)
    state = _read_json(state_path)
    validate_state(state)
    request_body = validate_envelope(request_envelope, label="request")
    entries = _read_ledger(ledger_path)
    request_digest = request_envelope["body_digest"]
    for entry in entries:
        transition_body = validate_envelope(entry, label="ledger_transition")
        if transition_body.get("request_digest") == request_digest:
            result_state = transition_body.get("result_state")
            if not isinstance(result_state, dict):
                raise ValueError("ledger_result_state_missing")
            return CommitResult("REPLAYED", entry, result_state, len(entries))
    if request_body.get("source_state_digest") != state.get("body_digest"):
        raise ValueError("stale_source_state")
    transition = apply_request(state, request_envelope, applied_at_ms=applied_at_ms)
    transition_body = validate_envelope(transition, label="transition")
    result_state = transition_body["result_state"]
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    with ledger_path.open("a", encoding="utf-8") as handle:
        handle.write(canonical_json(transition) + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    _atomic_write_json(state_path, result_state)
    return CommitResult("COMMITTED", transition, result_state, len(entries) + 1)


__all__ = [
    "CORE_HORIZONS",
    "CommitResult",
    "apply_request",
    "canonical_json",
    "commit_request",
    "digest",
    "make_envelope",
    "make_initial_state",
    "make_request",
    "validate_state",
]
