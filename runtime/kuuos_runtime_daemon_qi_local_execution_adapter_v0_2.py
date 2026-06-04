#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


REAL_ACTIONS = {"advance_tick", "notify", "ticket", "handover", "hold", "observe", "freeze"}
OUTBOX_ACTIONS = {"notify", "ticket", "handover", "observe"}
STATE_ACTIONS = {"advance_tick", "hold", "freeze"}

FORBIDDEN_EXTERNAL_EFFECT_KEYS = [
    "external_notification_sent",
    "external_ticket_created",
    "external_handover_performed",
    "scheduler_bypass_performed",
    "os_process_spawned",
    "network_call_performed",
    "probe_execution_performed",
    "world_update_performed",
    "memory_overwrite_performed",
]


@dataclass(frozen=True)
class QiLocalExecutionAdapterResult:
    adapter_version: str
    adapter_status: str
    adapter_packet_id: str
    action: str
    local_execution_id: str
    idempotency_key: str
    runtime_root: str
    state_path: str
    ledger_path: str
    outbox_path: str | None
    state_before_digest: str
    state_after_digest: str
    ledger_entry_digest: str
    effect_summary: dict[str, Any]
    execution_committed: bool
    local_runtime_state_updated: bool
    local_execution_ledger_appended: bool
    local_outbox_appended: bool
    idempotent_replay: bool
    external_notification_sent: bool
    external_ticket_created: bool
    external_handover_performed: bool
    scheduler_bypass_performed: bool
    os_process_spawned: bool
    network_call_performed: bool
    probe_execution_performed: bool
    world_update_performed: bool
    memory_overwrite_performed: bool
    blockers: list[str]
    warnings: list[str]
    authority: str = "qi_local_execution_adapter_v0_2_committed_local_effects"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _sha_obj(value: Mapping[str, Any] | list[Any]) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _read_json(path: pathlib.Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}


def _write_json_atomic(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def _append_jsonl(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")


def _read_jsonl(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            rows.append(value)
    return rows


def _safe_root(value: Any, blockers: list[str]) -> pathlib.Path:
    if not value:
        blockers.append("runtime_root_missing")
        return pathlib.Path(".").resolve()
    root = pathlib.Path(str(value)).expanduser().resolve()
    forbidden = {pathlib.Path("/").resolve()}
    if root in forbidden:
        blockers.append("runtime_root_forbidden")
    return root


def _action(value: Any) -> str:
    text = str(value or "hold")
    return text if text in REAL_ACTIONS else "hold"


def _require_false(prefix: str, packet: Mapping[str, Any], blockers: list[str]) -> None:
    for key in FORBIDDEN_EXTERNAL_EFFECT_KEYS:
        if key in packet and packet.get(key) is not False:
            blockers.append(f"{prefix}_{key}_not_false")


def _engine_source(packet: Mapping[str, Any]) -> Mapping[str, Any]:
    nested = packet.get("execution_intent_packet")
    if isinstance(nested, Mapping) and nested:
        return nested
    return packet


def _finality_source(packet: Mapping[str, Any]) -> Mapping[str, Any]:
    nested = packet.get("finality_packet")
    if isinstance(nested, Mapping) and nested:
        return nested
    return packet


def _effect_paths(root: pathlib.Path, action: str) -> tuple[pathlib.Path, pathlib.Path, pathlib.Path | None]:
    state_path = root / "runtime_state.json"
    ledger_path = root / "execution_ledger.jsonl"
    outbox: pathlib.Path | None = None
    if action == "notify":
        outbox = root / "outbox" / "notifications.jsonl"
    elif action == "ticket":
        outbox = root / "outbox" / "tickets.jsonl"
    elif action == "handover":
        outbox = root / "outbox" / "handovers.jsonl"
    elif action == "observe":
        outbox = root / "outbox" / "observations.jsonl"
    return state_path, ledger_path, outbox


def _state_after(state: Mapping[str, Any], action: str, local_execution_id: str) -> dict[str, Any]:
    next_state = dict(state)
    next_state.setdefault("tick", 0)
    next_state["last_local_execution_id"] = local_execution_id
    next_state["last_action"] = action
    next_state["updated_at_epoch"] = int(time.time())
    if action == "advance_tick":
        try:
            next_state["tick"] = int(next_state.get("tick", 0)) + 1
        except (TypeError, ValueError):
            next_state["tick"] = 1
    elif action == "freeze":
        next_state["frozen"] = True
    elif action == "hold":
        next_state["held"] = True
    return next_state


def build_qi_local_execution_adapter(
    *,
    engine_packet: Mapping[str, Any],
    health_packet_chain: Mapping[str, Any],
    execution_license_packet: Mapping[str, Any],
    runtime_context: Mapping[str, Any] | None = None,
) -> QiLocalExecutionAdapterResult:
    raw_engine = _mapping(engine_packet)
    engine = _engine_source(raw_engine)
    chain = _mapping(health_packet_chain)
    finality = _finality_source(chain)
    license_packet = _mapping(execution_license_packet)
    ctx = _mapping(runtime_context)
    blockers: list[str] = []
    warnings: list[str] = []

    runtime_root = _safe_root(ctx.get("runtime_root"), blockers)
    action = _action(raw_engine.get("selected_action", engine.get("selected_action")))
    state_path, ledger_path, outbox_path = _effect_paths(runtime_root, action)

    if ctx.get("qi_local_execution_adapter_enabled") is not True:
        blockers.append("qi_local_execution_adapter_enabled_not_true")
    if ctx.get("commit_local_effects") is not True:
        blockers.append("commit_local_effects_not_true")
    if action not in {str(item) for item in _list(ctx.get("allowed_actions"))}:
        blockers.append("action_not_allowed")

    if license_packet.get("license_status") != "QI_LOCAL_EXECUTION_LICENSE_READY":
        blockers.append("execution_license_not_ready")
    if license_packet.get("local_runtime_state_write_allowed") is not True:
        blockers.append("state_write_not_licensed")
    if license_packet.get("local_execution_ledger_append_allowed") is not True:
        blockers.append("ledger_append_not_licensed")
    if action in OUTBOX_ACTIONS and license_packet.get("local_outbox_append_allowed") is not True:
        blockers.append("outbox_append_not_licensed")
    if license_packet.get("external_side_effects_allowed") is True:
        warnings.append("external_side_effects_flag_ignored_by_local_adapter")

    if raw_engine.get("engine_status") != "QI_AUTONOMOUS_EXECUTION_ENGINE_READY":
        blockers.append("engine_status_not_ready")
    if raw_engine.get("execution_intent_staged") is not True and action in {"advance_tick", "notify", "ticket", "handover"}:
        blockers.append("executable_action_without_staged_intent")
    if raw_engine.get("execution_committed") is not False:
        blockers.append("engine_already_committed")

    if chain.get("chain_status") != "QI_EXECUTION_HEALTH_PACKET_CHAIN_READY":
        blockers.append("health_packet_chain_not_ready")
    if finality.get("packet_status") != "QI_EXECUTION_HEALTH_FINALITY_PACKET_READY":
        blockers.append("health_finality_not_ready")

    _require_false("engine", raw_engine, blockers)
    _require_false("finality", finality, blockers)

    source_engine_packet_id = raw_engine.get("engine_packet_id", engine.get("engine_packet_id"))
    source_finality_packet_id = finality.get("packet_id", chain.get("finality_packet_id"))
    nonce = str(ctx.get("execution_nonce") or "default")
    idempotency_key = _sha_obj({
        "source_engine_packet_id": source_engine_packet_id,
        "source_finality_packet_id": source_finality_packet_id,
        "action": action,
        "nonce": nonce,
    })
    local_execution_id = "qi-local-exec-" + idempotency_key[:16]
    adapter_packet_id = "qi-local-adapter-" + _sha_obj({"local_execution_id": local_execution_id, "action": action})[:16]

    existing = _read_jsonl(ledger_path)
    replay_rows = [row for row in existing if row.get("idempotency_key") == idempotency_key]
    idempotent_replay = bool(replay_rows)

    state_before = _read_json(state_path)
    state_before_digest = _sha_obj(state_before)
    state_after = _state_after(state_before, action, local_execution_id)
    state_after_digest = _sha_obj(state_after)

    ledger_entry = {
        "local_execution_id": local_execution_id,
        "idempotency_key": idempotency_key,
        "adapter_packet_id": adapter_packet_id,
        "action": action,
        "source_engine_packet_id": source_engine_packet_id,
        "source_finality_packet_id": source_finality_packet_id,
        "state_before_digest": state_before_digest,
        "state_after_digest": state_after_digest,
        "runtime_root": str(runtime_root),
        "execution_committed": True,
        "local_runtime_state_updated": action in STATE_ACTIONS,
        "local_execution_ledger_appended": True,
        "local_outbox_appended": action in OUTBOX_ACTIONS,
        "external_notification_sent": False,
        "external_ticket_created": False,
        "external_handover_performed": False,
        "scheduler_bypass_performed": False,
        "os_process_spawned": False,
        "network_call_performed": False,
        "probe_execution_performed": False,
        "world_update_performed": False,
        "memory_overwrite_performed": False,
    }
    ledger_entry_digest = _sha_obj(ledger_entry)
    ledger_entry["ledger_entry_digest"] = ledger_entry_digest

    outbox_entry: dict[str, Any] | None = None
    if action in OUTBOX_ACTIONS:
        outbox_entry = {
            "local_execution_id": local_execution_id,
            "idempotency_key": idempotency_key,
            "action": action,
            "status": "queued",
            "queue_kind": action,
            "source_engine_packet_id": source_engine_packet_id,
            "external_send_performed": False,
        }

    ready = not blockers
    local_runtime_state_updated = False
    local_execution_ledger_appended = False
    local_outbox_appended = False
    if ready and not idempotent_replay:
        if action in STATE_ACTIONS:
            _write_json_atomic(state_path, state_after)
            local_runtime_state_updated = True
        _append_jsonl(ledger_path, ledger_entry)
        local_execution_ledger_appended = True
        if outbox_path is not None and outbox_entry is not None:
            _append_jsonl(outbox_path, outbox_entry)
            local_outbox_appended = True
    elif ready and idempotent_replay:
        warnings.append("idempotent_replay_no_new_write")

    effect_summary = {
        "action": action,
        "state_path": str(state_path),
        "ledger_path": str(ledger_path),
        "outbox_path": str(outbox_path) if outbox_path else None,
        "state_updated": local_runtime_state_updated,
        "ledger_appended": local_execution_ledger_appended,
        "outbox_appended": local_outbox_appended,
        "idempotent_replay": idempotent_replay,
    }

    return QiLocalExecutionAdapterResult(
        adapter_version="kuuos_runtime_daemon_qi_local_execution_adapter_v0_2",
        adapter_status="QI_LOCAL_EXECUTION_ADAPTER_COMMITTED" if ready and not idempotent_replay else ("QI_LOCAL_EXECUTION_ADAPTER_REPLAYED" if ready else "QI_LOCAL_EXECUTION_ADAPTER_BLOCKED"),
        adapter_packet_id=adapter_packet_id,
        action=action,
        local_execution_id=local_execution_id,
        idempotency_key=idempotency_key,
        runtime_root=str(runtime_root),
        state_path=str(state_path),
        ledger_path=str(ledger_path),
        outbox_path=str(outbox_path) if outbox_path else None,
        state_before_digest=state_before_digest,
        state_after_digest=state_after_digest,
        ledger_entry_digest=ledger_entry_digest,
        effect_summary=effect_summary,
        execution_committed=ready,
        local_runtime_state_updated=local_runtime_state_updated,
        local_execution_ledger_appended=local_execution_ledger_appended,
        local_outbox_appended=local_outbox_appended,
        idempotent_replay=idempotent_replay,
        external_notification_sent=False,
        external_ticket_created=False,
        external_handover_performed=False,
        scheduler_bypass_performed=False,
        os_process_spawned=False,
        network_call_performed=False,
        probe_execution_performed=False,
        world_update_performed=False,
        memory_overwrite_performed=False,
        blockers=blockers,
        warnings=warnings,
    )
