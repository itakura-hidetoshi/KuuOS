from __future__ import annotations

import json
import os
from copy import deepcopy
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, Mapping

from runtime.kuuos_mission_contract_types_v0_20 import sha, validate_mission_contract
from runtime.kuuos_mission_state_v0_20 import validate_mission_state
from runtime.kuuos_nonmarkov_cognitive_loop_kernel_v0_23 import (
    NON_AUTHORITY,
    REQUIRED_BOUNDARY,
    validate_nonmarkov_cognitive_episode,
)

STORE_VERSION = "kuuos_nonmarkov_cognitive_loop_store_v0_23"
EVENT_VERSION = "kuuos_nonmarkov_cognitive_loop_event_v0_23"


def _without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    result = deepcopy(dict(value))
    result.pop(field, None)
    return result


def store_digest(value: Mapping[str, Any]) -> str:
    return sha(_without(value, "cognitive_loop_store_digest"))


def event_digest(value: Mapping[str, Any]) -> str:
    return sha(_without(value, "cognitive_loop_event_digest"))


def _write_json_atomic(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False
    ) as handle:
        json.dump(value, handle, ensure_ascii=False, sort_keys=True, indent=2)
        handle.write("\n")
        temporary = Path(handle.name)
    os.replace(temporary, path)


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("json_root_not_object")
    return value


def build_initial_store(
    *,
    contract: Mapping[str, Any],
    mission_state: Mapping[str, Any],
    chart_id: str,
    now_ms: int,
) -> dict[str, Any]:
    errors = validate_mission_state(mission_state, contract)
    if errors:
        raise ValueError(";".join(errors))
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
        "episodes": {},
        "ordered_episode_digests": [],
        "processed_event_digests": [],
        "event_history": [],
        "updated_at_ms": int(now_ms),
        "append_only": True,
        "memory_overwrite": False,
        "non_authority": deepcopy(NON_AUTHORITY),
        "boundary": deepcopy(REQUIRED_BOUNDARY),
        "cognitive_loop_store_digest": "",
    }
    state["cognitive_loop_store_digest"] = store_digest(state)
    return state


def build_episode_event(episode: Mapping[str, Any]) -> dict[str, Any]:
    event = {
        "version": EVENT_VERSION,
        "event_type": "episode_append",
        "mission_id": episode["mission_id"],
        "contract_digest": episode["contract_digest"],
        "chart_id": episode["chart_id"],
        "episode_digest": episode["cognitive_episode_digest"],
        "event_at_ms": int(episode["created_at_ms"]),
        "episode": deepcopy(dict(episode)),
        "cognitive_loop_event_digest": "",
    }
    event["cognitive_loop_event_digest"] = event_digest(event)
    return event


def validate_event(event: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if event.get("version") != EVENT_VERSION:
        errors.append("event_version_invalid")
    if event.get("event_type") != "episode_append":
        errors.append("event_type_invalid")
    episode = event.get("episode")
    if not isinstance(episode, Mapping):
        errors.append("event_episode_invalid")
        return errors
    errors.extend("episode:" + item for item in validate_nonmarkov_cognitive_episode(episode))
    for field in ("mission_id", "contract_digest", "chart_id"):
        if event.get(field) != episode.get(field):
            errors.append(f"event_{field}_mismatch")
    if event.get("episode_digest") != episode.get("cognitive_episode_digest"):
        errors.append("event_episode_digest_mismatch")
    try:
        if int(event.get("event_at_ms", -1)) != int(episode.get("created_at_ms", -2)):
            errors.append("event_time_mismatch")
    except (TypeError, ValueError):
        errors.append("event_time_invalid")
    if event.get("cognitive_loop_event_digest") != event_digest(event):
        errors.append("event_digest_invalid")
    return errors


def validate_store(
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
        errors.append("store_version_invalid")
    for field, expected in (
        ("mission_id", contract.get("mission_id")),
        ("lineage_id", contract.get("lineage_id")),
        ("contract_digest", contract.get("mission_contract_digest")),
        ("mission_state_digest", mission_state.get("mission_state_digest")),
    ):
        if state.get(field) != expected:
            errors.append(f"store_{field}_mismatch")
    if not str(state.get("chart_id", "")).strip():
        errors.append("store_chart_missing")
    episodes = state.get("episodes")
    ordered = state.get("ordered_episode_digests")
    processed = state.get("processed_event_digests")
    history = state.get("event_history")
    if not isinstance(episodes, Mapping):
        errors.append("store_episodes_invalid")
        episodes = {}
    if not isinstance(ordered, list):
        errors.append("store_ordered_digests_invalid")
        ordered = []
    if not isinstance(processed, list):
        errors.append("store_processed_events_invalid")
        processed = []
    if not isinstance(history, list):
        errors.append("store_event_history_invalid")
        history = []
    if len(ordered) != len(set(str(item) for item in ordered)):
        errors.append("store_episode_digest_duplicate")
    if set(str(item) for item in ordered) != set(str(item) for item in episodes):
        errors.append("store_episode_index_mismatch")
    for digest_value, episode in episodes.items():
        if str(digest_value) != str(episode.get("cognitive_episode_digest", "")):
            errors.append("store_episode_key_mismatch")
        errors.extend(
            "episode:" + item for item in validate_nonmarkov_cognitive_episode(episode)
        )
    history_digests = [str(item.get("cognitive_loop_event_digest", "")) for item in history]
    if history_digests != [str(item) for item in processed]:
        errors.append("store_history_processed_mismatch")
    for event in history:
        errors.extend("event:" + item for item in validate_event(event))
    try:
        if int(state.get("revision", -1)) != len(history):
            errors.append("store_revision_mismatch")
        if int(state.get("updated_at_ms", -1)) < 0:
            errors.append("store_updated_at_invalid")
    except (TypeError, ValueError):
        errors.append("store_numeric_invalid")
    if state.get("append_only") is not True:
        errors.append("store_append_only_invalid")
    if state.get("memory_overwrite") is not False:
        errors.append("store_memory_overwrite_forbidden")
    if dict(state.get("non_authority", {})) != NON_AUTHORITY:
        errors.append("store_non_authority_invalid")
    if dict(state.get("boundary", {})) != REQUIRED_BOUNDARY:
        errors.append("store_boundary_invalid")
    if state.get("cognitive_loop_store_digest") != store_digest(state):
        errors.append("store_digest_invalid")
    return errors


def apply_event(
    *,
    state: Mapping[str, Any],
    contract: Mapping[str, Any],
    mission_state: Mapping[str, Any],
    event: Mapping[str, Any],
) -> dict[str, Any]:
    errors = validate_store(state, contract, mission_state)
    errors.extend("event:" + item for item in validate_event(event))
    if errors:
        raise ValueError(";".join(errors))
    if event.get("mission_id") != state.get("mission_id"):
        raise ValueError("event_mission_mismatch")
    if event.get("contract_digest") != state.get("contract_digest"):
        raise ValueError("event_contract_mismatch")
    if event.get("chart_id") != state.get("chart_id"):
        raise ValueError("event_chart_mismatch")
    event_id = str(event["cognitive_loop_event_digest"])
    if event_id in set(str(item) for item in state["processed_event_digests"]):
        return {"status": "REPLAYED", "result_state": deepcopy(dict(state))}
    episode_id = str(event["episode_digest"])
    if episode_id in state["episodes"]:
        raise ValueError("episode_digest_collision")
    result = deepcopy(dict(state))
    result["episodes"][episode_id] = deepcopy(dict(event["episode"]))
    result["ordered_episode_digests"] = list(result["ordered_episode_digests"]) + [
        episode_id
    ]
    result["processed_event_digests"] = list(result["processed_event_digests"]) + [
        event_id
    ]
    result["event_history"] = list(result["event_history"]) + [deepcopy(dict(event))]
    result["revision"] = int(result["revision"]) + 1
    result["updated_at_ms"] = max(
        int(result["updated_at_ms"]), int(event["event_at_ms"])
    )
    result["cognitive_loop_store_digest"] = ""
    result["cognitive_loop_store_digest"] = store_digest(result)
    return {"status": "APPLIED", "result_state": result}


def initialize_store(
    *,
    store_dir: str | Path,
    contract: Mapping[str, Any],
    mission_state: Mapping[str, Any],
    chart_id: str,
    now_ms: int,
) -> dict[str, Any]:
    root = Path(store_dir)
    root.mkdir(parents=True, exist_ok=True)
    state = build_initial_store(
        contract=contract,
        mission_state=mission_state,
        chart_id=chart_id,
        now_ms=now_ms,
    )
    _write_json_atomic(root / "initial.json", state)
    _write_json_atomic(root / "snapshot.json", state)
    (root / "nonmarkov-cognitive-loop-ledger.jsonl").write_text("", encoding="utf-8")
    return deepcopy(state)


def recover_store(
    *,
    store_dir: str | Path,
    contract: Mapping[str, Any],
    mission_state: Mapping[str, Any],
    repair_snapshot: bool = False,
) -> dict[str, Any]:
    root = Path(store_dir)
    state = _read_json(root / "initial.json")
    initial_errors = validate_store(state, contract, mission_state)
    if initial_errors:
        raise ValueError("initial_invalid:" + ";".join(initial_errors))
    ledger_path = root / "nonmarkov-cognitive-loop-ledger.jsonl"
    for line_number, line in enumerate(
        ledger_path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"ledger_json_invalid:{line_number}") from exc
        result = apply_event(
            state=state,
            contract=contract,
            mission_state=mission_state,
            event=event,
        )
        if result["status"] != "APPLIED":
            raise ValueError(f"ledger_replay_not_applied:{line_number}")
        state = result["result_state"]
    snapshot = _read_json(root / "snapshot.json")
    if snapshot != state:
        if not repair_snapshot:
            raise ValueError("snapshot_ledger_mismatch")
        _write_json_atomic(root / "snapshot.json", state)
    return deepcopy(state)


def persist_episode(
    *,
    store_dir: str | Path,
    contract: Mapping[str, Any],
    mission_state: Mapping[str, Any],
    episode: Mapping[str, Any],
) -> dict[str, Any]:
    episode_errors = validate_nonmarkov_cognitive_episode(episode)
    if episode_errors:
        raise ValueError(";".join(episode_errors))
    root = Path(store_dir)
    state = recover_store(
        store_dir=root,
        contract=contract,
        mission_state=mission_state,
    )
    event = build_episode_event(episode)
    result = apply_event(
        state=state,
        contract=contract,
        mission_state=mission_state,
        event=event,
    )
    if result["status"] == "APPLIED":
        with (root / "nonmarkov-cognitive-loop-ledger.jsonl").open(
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
        _write_json_atomic(root / "snapshot.json", result["result_state"])
    return result


__all__ = [
    "EVENT_VERSION",
    "STORE_VERSION",
    "apply_event",
    "build_episode_event",
    "build_initial_store",
    "event_digest",
    "initialize_store",
    "persist_episode",
    "recover_store",
    "store_digest",
    "validate_event",
    "validate_store",
]
