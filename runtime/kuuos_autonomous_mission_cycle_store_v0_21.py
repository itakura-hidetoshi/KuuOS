from __future__ import annotations

import fcntl
import json
import os
from contextlib import contextmanager
from copy import deepcopy
from pathlib import Path
from typing import Any, Iterator, Mapping

from runtime.kuuos_autonomous_mission_cycle_kernel_v0_21 import (
    apply_mission_cycle_event,
    validate_mission_cycle_state,
)
from runtime.kuuos_autonomous_mission_cycle_types_v0_21 import (
    STORE_COMMIT_VERSION,
    store_commit_digest,
)
from runtime.kuuos_mission_io_v0_20 import append_jsonl, read_json, write_json_atomic

GENESIS_FILE = "genesis.json"
SNAPSHOT_FILE = "snapshot.json"
LEDGER_FILE = "cycle-ledger.jsonl"
LOCK_FILE = ".mission-cycle.lock"


@contextmanager
def _exclusive_store_lock(store_dir: Path) -> Iterator[None]:
    store_dir.mkdir(parents=True, exist_ok=True)
    lock_path = store_dir / LOCK_FILE
    descriptor = os.open(lock_path, os.O_CREAT | os.O_RDWR, 0o600)
    try:
        with os.fdopen(descriptor, "r+") as handle:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            handle.seek(0)
            handle.truncate()
            handle.write(str(os.getpid()))
            handle.flush()
            os.fsync(handle.fileno())
            yield
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
    finally:
        try:
            lock_path.unlink()
        except FileNotFoundError:
            pass


def _read_jsonl_strict(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    result: list[dict[str, Any]] = []
    for index, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            raise ValueError(f"ledger_blank_line:{index}")
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"ledger_json_invalid:{index}") from exc
        if not isinstance(value, dict):
            raise ValueError(f"ledger_object_required:{index}")
        result.append(value)
    return result


def initialize_mission_cycle_store(
    *,
    store_dir: str | os.PathLike[str],
    contract: Mapping[str, Any],
    mission_state: Mapping[str, Any],
    initial_cycle_state: Mapping[str, Any],
) -> dict[str, Any]:
    root = Path(store_dir)
    errors = validate_mission_cycle_state(initial_cycle_state, contract, mission_state)
    if errors:
        raise ValueError(";".join(errors))
    if initial_cycle_state.get("event_count") != 0:
        raise ValueError("initial_cycle_state_not_genesis")
    with _exclusive_store_lock(root):
        targets = [root / GENESIS_FILE, root / SNAPSHOT_FILE, root / LEDGER_FILE]
        if any(path.exists() for path in targets):
            raise FileExistsError("mission_cycle_store_exists")
        genesis = {
            "contract_digest": contract["mission_contract_digest"],
            "mission_id": contract["mission_id"],
            "mission_state": deepcopy(dict(mission_state)),
            "initial_cycle_state": deepcopy(dict(initial_cycle_state)),
        }
        write_json_atomic(root / GENESIS_FILE, genesis)
        write_json_atomic(root / SNAPSHOT_FILE, initial_cycle_state)
        (root / LEDGER_FILE).touch(exist_ok=False)
    return deepcopy(dict(initial_cycle_state))


def _validate_store_commit(commit: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if commit.get("version") != STORE_COMMIT_VERSION:
        errors.append("store_commit_version_invalid")
    for field in (
        "mission_id",
        "contract_digest",
        "source_state_digest",
        "event_digest",
        "result_state_digest",
    ):
        if not str(commit.get(field, "")).strip():
            errors.append(f"store_commit_{field}_missing")
    if not isinstance(commit.get("mission_state"), Mapping):
        errors.append("store_commit_mission_state_missing")
    if not isinstance(commit.get("event"), Mapping):
        errors.append("store_commit_event_missing")
    if commit.get("mission_cycle_store_commit_digest") != store_commit_digest(commit):
        errors.append("store_commit_digest_invalid")
    return errors


def recover_mission_cycle_store(
    *,
    store_dir: str | os.PathLike[str],
    contract: Mapping[str, Any],
    repair_snapshot: bool = False,
) -> dict[str, Any]:
    root = Path(store_dir)
    genesis = read_json(root / GENESIS_FILE)
    if genesis.get("contract_digest") != contract.get("mission_contract_digest"):
        raise ValueError("store_contract_digest_mismatch")
    state = deepcopy(dict(genesis["initial_cycle_state"]))
    initial_mission_state = genesis.get("mission_state")
    if not isinstance(initial_mission_state, Mapping):
        raise ValueError("store_genesis_mission_state_missing")
    errors = validate_mission_cycle_state(state, contract, initial_mission_state)
    if errors:
        raise ValueError(";".join("genesis:" + item for item in errors))

    for index, commit in enumerate(
        _read_jsonl_strict(root / LEDGER_FILE), start=1
    ):
        commit_errors = _validate_store_commit(commit)
        if commit_errors:
            raise ValueError(
                ";".join(f"commit_{index}:" + item for item in commit_errors)
            )
        if commit.get("mission_id") != contract.get("mission_id"):
            raise ValueError(f"commit_{index}:mission_mismatch")
        if commit.get("contract_digest") != contract.get("mission_contract_digest"):
            raise ValueError(f"commit_{index}:contract_mismatch")
        if commit.get("source_state_digest") != state.get(
            "mission_cycle_state_digest"
        ):
            raise ValueError(f"commit_{index}:source_state_chain_broken")
        mission_state = commit["mission_state"]
        event = commit["event"]
        result = apply_mission_cycle_event(
            contract=contract,
            mission_state=mission_state,
            cycle_state=state,
            event=event,
        )
        if result["status"] != "APPLIED":
            raise ValueError(f"commit_{index}:unexpected_replay")
        if commit.get("event_digest") != event.get("mission_cycle_event_digest"):
            raise ValueError(f"commit_{index}:event_digest_mismatch")
        if commit.get("result_state_digest") != result.get("result_state_digest"):
            raise ValueError(f"commit_{index}:result_state_digest_mismatch")
        state = result["result_state"]

    snapshot_path = root / SNAPSHOT_FILE
    snapshot = read_json(snapshot_path) if snapshot_path.exists() else None
    if snapshot != state:
        if not repair_snapshot:
            raise ValueError("snapshot_ledger_mismatch")
        write_json_atomic(snapshot_path, state, allow_overwrite=True)
    return deepcopy(dict(state))


def apply_mission_cycle_event_persisted(
    *,
    store_dir: str | os.PathLike[str],
    contract: Mapping[str, Any],
    mission_state: Mapping[str, Any],
    event: Mapping[str, Any],
) -> dict[str, Any]:
    root = Path(store_dir)
    with _exclusive_store_lock(root):
        current = recover_mission_cycle_store(
            store_dir=root, contract=contract, repair_snapshot=True
        )
        result = apply_mission_cycle_event(
            contract=contract,
            mission_state=mission_state,
            cycle_state=current,
            event=event,
        )
        if result["status"] == "REPLAYED":
            return result
        commit = {
            "version": STORE_COMMIT_VERSION,
            "mission_id": contract["mission_id"],
            "contract_digest": contract["mission_contract_digest"],
            "source_state_digest": current["mission_cycle_state_digest"],
            "event_digest": event["mission_cycle_event_digest"],
            "result_state_digest": result["result_state_digest"],
            "mission_state": deepcopy(dict(mission_state)),
            "event": deepcopy(dict(event)),
            "mission_usage_delta": deepcopy(dict(result["mission_usage_delta"])),
            "mission_cycle_store_commit_digest": "",
        }
        commit["mission_cycle_store_commit_digest"] = store_commit_digest(commit)
        append_jsonl(root / LEDGER_FILE, commit)
        write_json_atomic(
            root / SNAPSHOT_FILE, result["result_state"], allow_overwrite=True
        )
        return result
