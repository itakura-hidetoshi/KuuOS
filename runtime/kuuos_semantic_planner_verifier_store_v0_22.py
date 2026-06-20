from __future__ import annotations

import json
import os
from copy import deepcopy
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, Mapping

from runtime.kuuos_mission_contract_types_v0_20 import sha, validate_mission_contract
from runtime.kuuos_mission_state_v0_20 import validate_mission_state
from runtime.kuuos_semantic_planner_verifier_kernel_v0_22 import (
    PLAN_NON_AUTHORITY,
    REQUIRED_BOUNDARY,
    VERIFICATION_NON_AUTHORITY,
    validate_invalidation_receipt_static,
    validate_semantic_plan,
    validate_semantic_plan_static,
    validate_verification_receipt_static,
)

STORE_VERSION = "kuuos_semantic_planner_verifier_store_state_v0_22"
EVENT_VERSION = "kuuos_semantic_planner_verifier_event_v0_22"
EVENT_TYPES = frozenset({"plan", "verification", "invalidation"})


def _without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    result = deepcopy(dict(value))
    result.pop(field, None)
    return result


def store_state_digest(value: Mapping[str, Any]) -> str:
    return sha(_without(value, "planner_verifier_store_digest"))


def event_digest(value: Mapping[str, Any]) -> str:
    return sha(_without(value, "planner_verifier_event_digest"))


def _atomic_write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False
    ) as handle:
        json.dump(value, handle, ensure_ascii=False, sort_keys=True, indent=2)
        handle.write("\n")
        temporary = Path(handle.name)
    os.replace(temporary, path)


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _packet_time(event_type: str, payload: Mapping[str, Any]) -> int:
    field = {
        "plan": "created_at_ms",
        "verification": "observed_at_ms",
        "invalidation": "checked_at_ms",
    }[event_type]
    return int(payload[field])


def _payload_digest(event_type: str, payload: Mapping[str, Any]) -> str:
    field = {
        "plan": "semantic_plan_digest",
        "verification": "verification_receipt_digest",
        "invalidation": "plan_invalidation_receipt_digest",
    }[event_type]
    return str(payload[field])


def build_initial_store_state(
    *,
    contract: Mapping[str, Any],
    mission_state: Mapping[str, Any],
    chart_id: str,
    now_ms: int,
) -> dict[str, Any]:
    errors = validate_mission_state(mission_state, contract)
    if errors:
        raise ValueError(";".join(errors))
    if mission_state.get("lifecycle_state") != "active":
        raise ValueError("mission_not_active")
    chart = str(chart_id).strip()
    if not chart:
        raise ValueError("chart_id_missing")
    state = {
        "version": STORE_VERSION,
        "mission_id": contract["mission_id"],
        "lineage_id": contract["lineage_id"],
        "contract_digest": contract["mission_contract_digest"],
        "mission_state_digest": mission_state["mission_state_digest"],
        "chart_id": chart,
        "revision": 0,
        "plans": {},
        "verifications": {},
        "invalidations": {},
        "processed_event_digests": [],
        "event_history": [],
        "updated_at_ms": int(now_ms),
        "plan_non_authority": deepcopy(PLAN_NON_AUTHORITY),
        "verification_non_authority": deepcopy(VERIFICATION_NON_AUTHORITY),
        "boundary": deepcopy(REQUIRED_BOUNDARY),
        "planner_verifier_store_digest": "",
    }
    state["planner_verifier_store_digest"] = store_state_digest(state)
    return state


def build_store_event(event_type: str, payload: Mapping[str, Any]) -> dict[str, Any]:
    normalized_type = str(event_type).strip()
    if normalized_type not in EVENT_TYPES:
        raise ValueError("planner_verifier_event_type_invalid")
    event = {
        "version": EVENT_VERSION,
        "event_type": normalized_type,
        "mission_id": payload["mission_id"],
        "contract_digest": payload["contract_digest"],
        "chart_id": payload["chart_id"],
        "payload_digest": _payload_digest(normalized_type, payload),
        "event_at_ms": _packet_time(normalized_type, payload),
        "payload": deepcopy(dict(payload)),
        "planner_verifier_event_digest": "",
    }
    event["planner_verifier_event_digest"] = event_digest(event)
    return event


def validate_store_event_static(event: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    event_type = str(event.get("event_type", ""))
    if event.get("version") != EVENT_VERSION:
        errors.append("store_event_version_invalid")
    if event_type not in EVENT_TYPES:
        errors.append("store_event_type_invalid")
        return errors
    payload = event.get("payload")
    if not isinstance(payload, Mapping):
        errors.append("store_event_payload_invalid")
        return errors
    validators = {
        "plan": validate_semantic_plan_static,
        "verification": validate_verification_receipt_static,
        "invalidation": validate_invalidation_receipt_static,
    }
    errors.extend(
        f"payload:{item}" for item in validators[event_type](payload)
    )
    for field in ("mission_id", "contract_digest", "chart_id"):
        if event.get(field) != payload.get(field):
            errors.append(f"store_event_{field}_mismatch")
    try:
        if int(event.get("event_at_ms", -1)) != _packet_time(event_type, payload):
            errors.append("store_event_time_mismatch")
    except (TypeError, ValueError, KeyError):
        errors.append("store_event_time_invalid")
    if event.get("payload_digest") != _payload_digest(event_type, payload):
        errors.append("store_event_payload_digest_mismatch")
    if event.get("planner_verifier_event_digest") != event_digest(event):
        errors.append("store_event_digest_invalid")
    return errors


def validate_store_state(
    state: Mapping[str, Any],
    contract: Mapping[str, Any],
    mission_state: Mapping[str, Any],
) -> list[str]:
    errors = ["contract:" + item for item in validate_mission_contract(contract)]
    errors.extend(
        "mission_state:" + item
        for item in validate_mission_state(mission_state, contract)
    )
    if state.get("version") != STORE_VERSION:
        errors.append("store_state_version_invalid")
    expected = {
        "mission_id": contract.get("mission_id"),
        "lineage_id": contract.get("lineage_id"),
        "contract_digest": contract.get("mission_contract_digest"),
        "mission_state_digest": mission_state.get("mission_state_digest"),
    }
    for field, value in expected.items():
        if state.get(field) != value:
            errors.append(f"store_state_{field}_mismatch")
    if not str(state.get("chart_id", "")).strip():
        errors.append("store_state_chart_missing")
    for field in ("plans", "verifications", "invalidations"):
        if not isinstance(state.get(field), Mapping):
            errors.append(f"store_state_{field}_invalid")
    if isinstance(state.get("plans"), Mapping):
        for digest_value, plan in state["plans"].items():
            if str(digest_value) != str(plan.get("semantic_plan_digest", "")):
                errors.append("store_plan_key_mismatch")
            errors.extend(
                "plan:" + item for item in validate_semantic_plan_static(plan)
            )
    if isinstance(state.get("verifications"), Mapping):
        for digest_value, receipt in state["verifications"].items():
            if str(digest_value) != str(
                receipt.get("verification_receipt_digest", "")
            ):
                errors.append("store_verification_key_mismatch")
            errors.extend(
                "verification:" + item
                for item in validate_verification_receipt_static(receipt)
            )
            if receipt.get("source_plan_digest") not in state.get("plans", {}):
                errors.append("store_verification_plan_missing")
    if isinstance(state.get("invalidations"), Mapping):
        for digest_value, receipt in state["invalidations"].items():
            if str(digest_value) != str(
                receipt.get("plan_invalidation_receipt_digest", "")
            ):
                errors.append("store_invalidation_key_mismatch")
            errors.extend(
                "invalidation:" + item
                for item in validate_invalidation_receipt_static(receipt)
            )
            if receipt.get("source_plan_digest") not in state.get("plans", {}):
                errors.append("store_invalidation_plan_missing")
    history = state.get("event_history")
    processed = state.get("processed_event_digests")
    if not isinstance(history, list):
        errors.append("store_event_history_invalid")
    if not isinstance(processed, list):
        errors.append("store_processed_events_invalid")
    elif len(processed) != len(set(str(item) for item in processed)):
        errors.append("store_processed_events_duplicate")
    if isinstance(history, list) and isinstance(processed, list):
        history_digests = [
            str(item.get("planner_verifier_event_digest", "")) for item in history
        ]
        if history_digests != [str(item) for item in processed]:
            errors.append("store_history_processed_mismatch")
        for item in history:
            errors.extend(
                "event:" + error for error in validate_store_event_static(item)
            )
    try:
        if int(state.get("revision", -1)) != len(history or []):
            errors.append("store_revision_mismatch")
        if int(state.get("updated_at_ms", -1)) < 0:
            errors.append("store_updated_at_invalid")
    except (TypeError, ValueError):
        errors.append("store_numeric_field_invalid")
    if dict(state.get("plan_non_authority", {})) != PLAN_NON_AUTHORITY:
        errors.append("store_plan_non_authority_invalid")
    if dict(state.get("verification_non_authority", {})) != VERIFICATION_NON_AUTHORITY:
        errors.append("store_verification_non_authority_invalid")
    if dict(state.get("boundary", {})) != REQUIRED_BOUNDARY:
        errors.append("store_boundary_invalid")
    if state.get("planner_verifier_store_digest") != store_state_digest(state):
        errors.append("store_state_digest_invalid")
    return errors


def apply_store_event(
    *,
    state: Mapping[str, Any],
    contract: Mapping[str, Any],
    mission_state: Mapping[str, Any],
    event: Mapping[str, Any],
) -> dict[str, Any]:
    errors = validate_store_state(state, contract, mission_state)
    errors.extend("event:" + item for item in validate_store_event_static(event))
    if errors:
        raise ValueError(";".join(errors))
    if event.get("mission_id") != state.get("mission_id"):
        raise ValueError("store_event_mission_mismatch")
    if event.get("contract_digest") != state.get("contract_digest"):
        raise ValueError("store_event_contract_mismatch")
    if event.get("chart_id") != state.get("chart_id"):
        raise ValueError("store_event_chart_mismatch")
    digest_value = str(event["planner_verifier_event_digest"])
    if digest_value in set(str(item) for item in state["processed_event_digests"]):
        return {"status": "REPLAYED", "result_state": deepcopy(dict(state))}

    result = deepcopy(dict(state))
    event_type = str(event["event_type"])
    payload = deepcopy(dict(event["payload"]))
    payload_digest = str(event["payload_digest"])
    if event_type == "plan":
        result["plans"][payload_digest] = payload
    elif event_type == "verification":
        if payload.get("source_plan_digest") not in result["plans"]:
            raise ValueError("verification_source_plan_missing")
        result["verifications"][payload_digest] = payload
    else:
        if payload.get("source_plan_digest") not in result["plans"]:
            raise ValueError("invalidation_source_plan_missing")
        result["invalidations"][payload_digest] = payload
    result["event_history"] = list(result["event_history"]) + [
        deepcopy(dict(event))
    ]
    result["processed_event_digests"] = list(result["processed_event_digests"]) + [
        digest_value
    ]
    result["revision"] = int(result["revision"]) + 1
    result["updated_at_ms"] = max(
        int(result["updated_at_ms"]), int(event["event_at_ms"])
    )
    result["planner_verifier_store_digest"] = ""
    result["planner_verifier_store_digest"] = store_state_digest(result)
    return {"status": "APPLIED", "result_state": result}


def initialize_planner_verifier_store(
    *,
    store_dir: str | Path,
    contract: Mapping[str, Any],
    mission_state: Mapping[str, Any],
    chart_id: str,
    now_ms: int,
) -> dict[str, Any]:
    root = Path(store_dir)
    root.mkdir(parents=True, exist_ok=True)
    state = build_initial_store_state(
        contract=contract,
        mission_state=mission_state,
        chart_id=chart_id,
        now_ms=now_ms,
    )
    _atomic_write_json(root / "initial.json", state)
    _atomic_write_json(root / "snapshot.json", state)
    (root / "planner-verifier-ledger.jsonl").write_text("", encoding="utf-8")
    return deepcopy(state)


def recover_planner_verifier_store(
    *,
    store_dir: str | Path,
    contract: Mapping[str, Any],
    mission_state: Mapping[str, Any],
    repair_snapshot: bool = False,
) -> dict[str, Any]:
    root = Path(store_dir)
    state = _read_json(root / "initial.json")
    errors = validate_store_state(state, contract, mission_state)
    if errors:
        raise ValueError("initial_invalid:" + ";".join(errors))
    ledger_path = root / "planner-verifier-ledger.jsonl"
    for line_number, line in enumerate(
        ledger_path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"ledger_json_invalid:{line_number}") from exc
        applied = apply_store_event(
            state=state,
            contract=contract,
            mission_state=mission_state,
            event=event,
        )
        if applied["status"] != "APPLIED":
            raise ValueError(f"ledger_replay_not_applied:{line_number}")
        state = applied["result_state"]
    snapshot = _read_json(root / "snapshot.json")
    if snapshot != state:
        if not repair_snapshot:
            raise ValueError("snapshot_ledger_mismatch")
        _atomic_write_json(root / "snapshot.json", state)
    return deepcopy(state)


def _persist_event(
    *,
    store_dir: str | Path,
    contract: Mapping[str, Any],
    mission_state: Mapping[str, Any],
    event: Mapping[str, Any],
) -> dict[str, Any]:
    root = Path(store_dir)
    state = recover_planner_verifier_store(
        store_dir=root,
        contract=contract,
        mission_state=mission_state,
    )
    result = apply_store_event(
        state=state,
        contract=contract,
        mission_state=mission_state,
        event=event,
    )
    if result["status"] == "APPLIED":
        with (root / "planner-verifier-ledger.jsonl").open(
            "a", encoding="utf-8"
        ) as handle:
            handle.write(
                json.dumps(
                    event,
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                )
                + "\n"
            )
        _atomic_write_json(root / "snapshot.json", result["result_state"])
    return result


def persist_plan(
    *,
    store_dir: str | Path,
    contract: Mapping[str, Any],
    mission_state: Mapping[str, Any],
    belief_state: Mapping[str, Any],
    goal: Mapping[str, Any],
    goal_portfolio: Mapping[str, Any],
    plan: Mapping[str, Any],
) -> dict[str, Any]:
    errors = validate_semantic_plan(
        plan, contract, mission_state, belief_state, goal, goal_portfolio
    )
    if errors:
        raise ValueError(";".join(errors))
    return _persist_event(
        store_dir=store_dir,
        contract=contract,
        mission_state=mission_state,
        event=build_store_event("plan", plan),
    )


def persist_verification(
    *,
    store_dir: str | Path,
    contract: Mapping[str, Any],
    mission_state: Mapping[str, Any],
    receipt: Mapping[str, Any],
) -> dict[str, Any]:
    errors = validate_verification_receipt_static(receipt)
    if errors:
        raise ValueError(";".join(errors))
    if receipt.get("mission_id") != contract.get("mission_id"):
        raise ValueError("verification_mission_mismatch")
    if receipt.get("source_mission_state_digest") != mission_state.get(
        "mission_state_digest"
    ):
        raise ValueError("verification_mission_state_stale")
    return _persist_event(
        store_dir=store_dir,
        contract=contract,
        mission_state=mission_state,
        event=build_store_event("verification", receipt),
    )


def persist_invalidation(
    *,
    store_dir: str | Path,
    contract: Mapping[str, Any],
    mission_state: Mapping[str, Any],
    receipt: Mapping[str, Any],
) -> dict[str, Any]:
    errors = validate_invalidation_receipt_static(receipt)
    if errors:
        raise ValueError(";".join(errors))
    if receipt.get("mission_id") != contract.get("mission_id"):
        raise ValueError("invalidation_mission_mismatch")
    return _persist_event(
        store_dir=store_dir,
        contract=contract,
        mission_state=mission_state,
        event=build_store_event("invalidation", receipt),
    )


__all__ = [
    "EVENT_TYPES",
    "EVENT_VERSION",
    "STORE_VERSION",
    "apply_store_event",
    "build_initial_store_state",
    "build_store_event",
    "event_digest",
    "initialize_planner_verifier_store",
    "persist_invalidation",
    "persist_plan",
    "persist_verification",
    "recover_planner_verifier_store",
    "store_state_digest",
    "validate_store_event_static",
    "validate_store_state",
]
