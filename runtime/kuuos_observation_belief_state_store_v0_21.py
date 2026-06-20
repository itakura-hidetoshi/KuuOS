from __future__ import annotations

import json
import os
from copy import deepcopy
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, Mapping

from runtime.kuuos_observation_belief_state_kernel_v0_21 import (
    apply_observation,
    build_initial_belief_state,
    validate_belief_state,
)


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


def initialize_belief_store(
    *,
    store_dir: str | Path,
    contract: Mapping[str, Any],
    mission_state: Mapping[str, Any],
    chart_id: str,
    now_ms: int,
) -> dict[str, Any]:
    root = Path(store_dir)
    root.mkdir(parents=True, exist_ok=True)
    state = build_initial_belief_state(
        contract=contract,
        mission_state=mission_state,
        chart_id=chart_id,
        now_ms=now_ms,
    )
    _atomic_write_json(root / "initial.json", state)
    _atomic_write_json(root / "snapshot.json", state)
    (root / "observation-ledger.jsonl").write_text("", encoding="utf-8")
    return deepcopy(state)


def recover_belief_store(
    *,
    store_dir: str | Path,
    contract: Mapping[str, Any],
    mission_state: Mapping[str, Any],
    repair_snapshot: bool = False,
) -> dict[str, Any]:
    root = Path(store_dir)
    initial = _read_json(root / "initial.json")
    errors = validate_belief_state(initial, contract, mission_state)
    if errors:
        raise ValueError("initial_invalid:" + ";".join(errors))
    state = initial
    ledger_path = root / "observation-ledger.jsonl"
    for line_number, line in enumerate(
        ledger_path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        if not line.strip():
            continue
        try:
            observation = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"ledger_json_invalid:{line_number}") from exc
        result = apply_observation(
            contract=contract,
            mission_state=mission_state,
            belief_state=state,
            observation=observation,
        )
        if result["status"] != "APPLIED":
            raise ValueError(f"ledger_replay_not_applied:{line_number}")
        state = result["result_state"]

    snapshot = _read_json(root / "snapshot.json")
    if snapshot != state:
        if not repair_snapshot:
            raise ValueError("snapshot_ledger_mismatch")
        _atomic_write_json(root / "snapshot.json", state)
    return deepcopy(state)


def apply_observation_persisted(
    *,
    store_dir: str | Path,
    contract: Mapping[str, Any],
    mission_state: Mapping[str, Any],
    observation: Mapping[str, Any],
) -> dict[str, Any]:
    root = Path(store_dir)
    state = recover_belief_store(
        store_dir=root,
        contract=contract,
        mission_state=mission_state,
    )
    result = apply_observation(
        contract=contract,
        mission_state=mission_state,
        belief_state=state,
        observation=observation,
    )
    if result["status"] == "APPLIED":
        ledger_path = root / "observation-ledger.jsonl"
        with ledger_path.open("a", encoding="utf-8") as handle:
            handle.write(
                json.dumps(
                    observation,
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                )
                + "\n"
            )
        _atomic_write_json(root / "snapshot.json", result["result_state"])
    return result


__all__ = [
    "apply_observation_persisted",
    "initialize_belief_store",
    "recover_belief_store",
]
