from __future__ import annotations

import json
import os
from copy import deepcopy
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, Mapping

from runtime.kuuos_cognitive_memory_credit_kernel_v0_23 import (
    NON_AUTHORITY,
    REQUIRED_BOUNDARY,
    validate_cognitive_memory_consolidation_static,
)
from runtime.kuuos_mission_contract_types_v0_20 import sha, validate_mission_contract
from runtime.kuuos_mission_state_v0_20 import validate_mission_state

STORE_VERSION = "kuuos_cognitive_memory_credit_store_state_v0_23"
EVENT_VERSION = "kuuos_cognitive_memory_credit_store_event_v0_23"
MEMORY_ENTRY_VERSION = "kuuos_cognitive_memoryos_committed_entry_v0_23"


def _without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    result = deepcopy(dict(value))
    result.pop(field, None)
    return result


def store_digest(value: Mapping[str, Any]) -> str:
    return sha(_without(value, "cognitive_memory_credit_store_digest"))


def event_digest(value: Mapping[str, Any]) -> str:
    return sha(_without(value, "cognitive_memory_credit_event_digest"))


def memory_entry_digest(value: Mapping[str, Any]) -> str:
    return sha(_without(value, "memory_entry_digest"))


def _atomic_write(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False
    ) as handle:
        json.dump(value, handle, ensure_ascii=False, sort_keys=True, indent=2)
        handle.write("\n")
        temporary = Path(handle.name)
    os.replace(temporary, path)


def _read(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_initial_cognitive_memory_store(
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
        "consolidation_receipts": {},
        "memory_entries": [],
        "processed_event_digests": [],
        "event_history": [],
        "updated_at_ms": int(now_ms),
        "memory_append_only": True,
        "memory_overwrite_performed": False,
        "non_authority": deepcopy(NON_AUTHORITY),
        "boundary": deepcopy(REQUIRED_BOUNDARY),
        "cognitive_memory_credit_store_digest": "",
    }
    state["cognitive_memory_credit_store_digest"] = store_digest(state)
    return state


def build_committed_memory_entry(receipt: Mapping[str, Any]) -> dict[str, Any]:
    candidate = receipt["memory_append_candidate"]
    if candidate.get("memory_append_requested") is not True:
        raise ValueError("memory_append_not_requested")
    entry = {
        "version": MEMORY_ENTRY_VERSION,
        "writeback_status": "QI_MEMORYOS_PROCESS_TENSOR_APPEND_WRITEBACK_PERFORMED",
        "source_execution_status": "COGNITIVE_MEMORY_CONSOLIDATION_COMMITTED",
        "source_probe_type": "cognitive_memory_credit_v0_23",
        "memory_entry_kind": "cognitive_memory_process_tensor_episode",
        "memory_entry_summary": (
            f"episode {receipt['episode_id']} consolidated with status {receipt['status']}"
        ),
        "memoryos_target_stream": "memoryos/cognitive_process_tensor/append_only",
        "episode_id": receipt["episode_id"],
        "mission_id": receipt["mission_id"],
        "chart_id": receipt["chart_id"],
        "source_consolidation_digest": receipt[
            "cognitive_memory_consolidation_digest"
        ],
        "source_plan_digest": receipt["source_plan_digest"],
        "source_belief_state_digest": receipt["source_belief_state_digest"],
        "source_verification_digest": receipt["source_verification_digest"],
        "belief_release_candidate_digest": receipt["belief_release_candidate"][
            "belief_release_candidate_digest"
        ],
        "plan_strategy_candidate_digest": receipt["plan_strategy_candidate"][
            "plan_strategy_candidate_digest"
        ],
        "credit_assignment_digests": [
            item["credit_assignment_digest"]
            for item in receipt["credit_assignments"]
        ],
        "counterevidence_digests": list(receipt["counterevidence_digests"]),
        "process_tensor_trace_preserved": candidate[
            "process_tensor_trace_preserved"
        ],
        "nonmarkov_trace_preserved": candidate["nonmarkov_trace_preserved"],
        "observation_debt_trace_preserved": candidate[
            "observation_debt_trace_preserved"
        ],
        "recoverability_trace_preserved": candidate[
            "recoverability_trace_preserved"
        ],
        "safe_reentry_trace_preserved": candidate[
            "safe_reentry_trace_preserved"
        ],
        "lineage_preserved": candidate["lineage_preserved"],
        "append_only": True,
        "memory_append_performed": True,
        "memory_write_performed": True,
        "memory_overwrite_performed": False,
        "memory_delete_performed": False,
        "world_update_performed": False,
        "control_packet_mutation_performed": False,
        "scheduler_state_mutation_performed": False,
        "grants_memory_append_authority": False,
        "grants_memory_overwrite_authority": False,
        "grants_world_update_authority": False,
        "grants_control_packet_authority": False,
        "grants_scheduler_authority": False,
        "grants_probe_execution_authority": False,
        "committed_at_ms": receipt["consolidated_at_ms"],
        "memory_entry_digest": "",
    }
    entry["memory_entry_digest"] = memory_entry_digest(entry)
    return entry


def build_cognitive_memory_event(receipt: Mapping[str, Any]) -> dict[str, Any]:
    errors = validate_cognitive_memory_consolidation_static(receipt)
    if errors:
        raise ValueError(";".join(errors))
    memory_entry = build_committed_memory_entry(receipt)
    event = {
        "version": EVENT_VERSION,
        "mission_id": receipt["mission_id"],
        "contract_digest": receipt["contract_digest"],
        "chart_id": receipt["chart_id"],
        "episode_id": receipt["episode_id"],
        "consolidation_digest": receipt[
            "cognitive_memory_consolidation_digest"
        ],
        "memory_entry_digest": memory_entry["memory_entry_digest"],
        "event_at_ms": receipt["consolidated_at_ms"],
        "receipt": deepcopy(dict(receipt)),
        "memory_entry": memory_entry,
        "cognitive_memory_credit_event_digest": "",
    }
    event["cognitive_memory_credit_event_digest"] = event_digest(event)
    return event


def validate_memory_entry_static(entry: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if entry.get("version") != MEMORY_ENTRY_VERSION:
        errors.append("memory_entry_version_invalid")
    if entry.get("writeback_status") != (
        "QI_MEMORYOS_PROCESS_TENSOR_APPEND_WRITEBACK_PERFORMED"
    ):
        errors.append("memory_entry_writeback_status_invalid")
    for field in (
        "episode_id",
        "mission_id",
        "chart_id",
        "source_consolidation_digest",
        "source_plan_digest",
        "source_belief_state_digest",
        "source_verification_digest",
    ):
        if not str(entry.get(field, "")).strip():
            errors.append(f"memory_entry_{field}_missing")
    for field in (
        "process_tensor_trace_preserved",
        "nonmarkov_trace_preserved",
        "observation_debt_trace_preserved",
        "recoverability_trace_preserved",
        "safe_reentry_trace_preserved",
        "lineage_preserved",
        "append_only",
        "memory_append_performed",
        "memory_write_performed",
    ):
        if entry.get(field) is not True:
            errors.append(f"memory_entry_{field}_not_true")
    for field in (
        "memory_overwrite_performed",
        "memory_delete_performed",
        "world_update_performed",
        "control_packet_mutation_performed",
        "scheduler_state_mutation_performed",
        "grants_memory_append_authority",
        "grants_memory_overwrite_authority",
        "grants_world_update_authority",
        "grants_control_packet_authority",
        "grants_scheduler_authority",
        "grants_probe_execution_authority",
    ):
        if entry.get(field) is not False:
            errors.append(f"memory_entry_{field}_not_false")
    if entry.get("memory_entry_digest") != memory_entry_digest(entry):
        errors.append("memory_entry_digest_invalid")
    return errors


def validate_event_static(event: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if event.get("version") != EVENT_VERSION:
        errors.append("event_version_invalid")
    receipt = event.get("receipt")
    memory_entry = event.get("memory_entry")
    if not isinstance(receipt, Mapping):
        errors.append("event_receipt_invalid")
        return errors
    if not isinstance(memory_entry, Mapping):
        errors.append("event_memory_entry_invalid")
        return errors
    errors.extend(
        "receipt:" + item
        for item in validate_cognitive_memory_consolidation_static(receipt)
    )
    errors.extend(
        "memory_entry:" + item
        for item in validate_memory_entry_static(memory_entry)
    )
    expected = {
        "mission_id": receipt.get("mission_id"),
        "contract_digest": receipt.get("contract_digest"),
        "chart_id": receipt.get("chart_id"),
        "episode_id": receipt.get("episode_id"),
        "consolidation_digest": receipt.get(
            "cognitive_memory_consolidation_digest"
        ),
        "memory_entry_digest": memory_entry.get("memory_entry_digest"),
        "event_at_ms": receipt.get("consolidated_at_ms"),
    }
    for field, value in expected.items():
        if event.get(field) != value:
            errors.append(f"event_{field}_mismatch")
    if memory_entry.get("source_consolidation_digest") != event.get(
        "consolidation_digest"
    ):
        errors.append("event_memory_consolidation_mismatch")
    if event.get("cognitive_memory_credit_event_digest") != event_digest(event):
        errors.append("event_digest_invalid")
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
        errors.append("store_version_invalid")
    expected = {
        "mission_id": contract.get("mission_id"),
        "lineage_id": contract.get("lineage_id"),
        "contract_digest": contract.get("mission_contract_digest"),
        "mission_state_digest": mission_state.get("mission_state_digest"),
    }
    for field, value in expected.items():
        if state.get(field) != value:
            errors.append(f"store_{field}_mismatch")
    if not str(state.get("chart_id", "")).strip():
        errors.append("store_chart_missing")
    receipts = state.get("consolidation_receipts")
    entries = state.get("memory_entries")
    history = state.get("event_history")
    processed = state.get("processed_event_digests")
    if not isinstance(receipts, Mapping):
        errors.append("store_receipts_invalid")
    else:
        for digest_value, receipt in receipts.items():
            if digest_value != receipt.get(
                "cognitive_memory_consolidation_digest"
            ):
                errors.append("store_receipt_key_mismatch")
            errors.extend(
                "receipt:" + item
                for item in validate_cognitive_memory_consolidation_static(receipt)
            )
    if not isinstance(entries, list):
        errors.append("store_memory_entries_invalid")
    else:
        entry_digests: list[str] = []
        for entry in entries:
            errors.extend(
                "memory_entry:" + item
                for item in validate_memory_entry_static(entry)
            )
            entry_digests.append(str(entry.get("memory_entry_digest", "")))
        if len(entry_digests) != len(set(entry_digests)):
            errors.append("store_memory_entry_duplicate")
    if not isinstance(history, list):
        errors.append("store_history_invalid")
    if not isinstance(processed, list):
        errors.append("store_processed_invalid")
    elif len(processed) != len(set(str(item) for item in processed)):
        errors.append("store_processed_duplicate")
    if isinstance(history, list) and isinstance(processed, list):
        history_digests = [
            str(item.get("cognitive_memory_credit_event_digest", ""))
            for item in history
        ]
        if history_digests != [str(item) for item in processed]:
            errors.append("store_history_processed_mismatch")
        for event in history:
            errors.extend("event:" + item for item in validate_event_static(event))
    try:
        if int(state.get("revision", -1)) != len(history or []):
            errors.append("store_revision_mismatch")
        if int(state.get("updated_at_ms", -1)) < 0:
            errors.append("store_updated_at_invalid")
    except (TypeError, ValueError):
        errors.append("store_numeric_field_invalid")
    if state.get("memory_append_only") is not True:
        errors.append("store_memory_append_only_missing")
    if state.get("memory_overwrite_performed") is not False:
        errors.append("store_memory_overwrite_forbidden")
    if dict(state.get("non_authority", {})) != NON_AUTHORITY:
        errors.append("store_non_authority_invalid")
    if dict(state.get("boundary", {})) != REQUIRED_BOUNDARY:
        errors.append("store_boundary_invalid")
    if state.get("cognitive_memory_credit_store_digest") != store_digest(state):
        errors.append("store_digest_invalid")
    return errors


def apply_event(
    *,
    state: Mapping[str, Any],
    contract: Mapping[str, Any],
    mission_state: Mapping[str, Any],
    event: Mapping[str, Any],
) -> dict[str, Any]:
    errors = validate_store_state(state, contract, mission_state)
    errors.extend("event:" + item for item in validate_event_static(event))
    if errors:
        raise ValueError(";".join(errors))
    for field in ("mission_id", "contract_digest", "chart_id"):
        if event.get(field) != state.get(field):
            raise ValueError(f"event_{field}_mismatch")
    event_id = str(event["cognitive_memory_credit_event_digest"])
    if event_id in set(str(item) for item in state["processed_event_digests"]):
        return {"status": "REPLAYED", "result_state": deepcopy(dict(state))}
    consolidation_id = str(event["consolidation_digest"])
    if consolidation_id in state["consolidation_receipts"]:
        raise ValueError("conflicting_consolidation_digest")
    episode_id = str(event["episode_id"])
    if any(
        str(item.get("episode_id", "")) == episode_id
        for item in state["memory_entries"]
    ):
        raise ValueError("episode_already_consolidated")
    result = deepcopy(dict(state))
    result["consolidation_receipts"][consolidation_id] = deepcopy(
        dict(event["receipt"])
    )
    result["memory_entries"] = list(result["memory_entries"]) + [
        deepcopy(dict(event["memory_entry"]))
    ]
    result["event_history"] = list(result["event_history"]) + [
        deepcopy(dict(event))
    ]
    result["processed_event_digests"] = list(
        result["processed_event_digests"]
    ) + [event_id]
    result["revision"] = int(result["revision"]) + 1
    result["updated_at_ms"] = max(
        int(result["updated_at_ms"]), int(event["event_at_ms"])
    )
    result["cognitive_memory_credit_store_digest"] = ""
    result["cognitive_memory_credit_store_digest"] = store_digest(result)
    return {"status": "APPLIED", "result_state": result}


def initialize_cognitive_memory_store(
    *,
    store_dir: str | Path,
    contract: Mapping[str, Any],
    mission_state: Mapping[str, Any],
    chart_id: str,
    now_ms: int,
) -> dict[str, Any]:
    root = Path(store_dir)
    root.mkdir(parents=True, exist_ok=True)
    state = build_initial_cognitive_memory_store(
        contract=contract,
        mission_state=mission_state,
        chart_id=chart_id,
        now_ms=now_ms,
    )
    _atomic_write(root / "initial.json", state)
    _atomic_write(root / "snapshot.json", state)
    (root / "cognitive-memory-ledger.jsonl").write_text("", encoding="utf-8")
    return deepcopy(state)


def recover_cognitive_memory_store(
    *,
    store_dir: str | Path,
    contract: Mapping[str, Any],
    mission_state: Mapping[str, Any],
    repair_snapshot: bool = False,
) -> dict[str, Any]:
    root = Path(store_dir)
    state = _read(root / "initial.json")
    errors = validate_store_state(state, contract, mission_state)
    if errors:
        raise ValueError("initial_invalid:" + ";".join(errors))
    ledger = root / "cognitive-memory-ledger.jsonl"
    for line_number, line in enumerate(
        ledger.read_text(encoding="utf-8").splitlines(), start=1
    ):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"ledger_json_invalid:{line_number}") from exc
        applied = apply_event(
            state=state,
            contract=contract,
            mission_state=mission_state,
            event=event,
        )
        if applied["status"] != "APPLIED":
            raise ValueError(f"ledger_event_not_applied:{line_number}")
        state = applied["result_state"]
    snapshot = _read(root / "snapshot.json")
    if snapshot != state:
        if not repair_snapshot:
            raise ValueError("snapshot_ledger_mismatch")
        _atomic_write(root / "snapshot.json", state)
    return deepcopy(state)


def persist_cognitive_memory_consolidation(
    *,
    store_dir: str | Path,
    contract: Mapping[str, Any],
    mission_state: Mapping[str, Any],
    receipt: Mapping[str, Any],
) -> dict[str, Any]:
    if receipt.get("status") == "blocked":
        raise ValueError("blocked_consolidation_cannot_persist")
    event = build_cognitive_memory_event(receipt)
    root = Path(store_dir)
    state = recover_cognitive_memory_store(
        store_dir=root,
        contract=contract,
        mission_state=mission_state,
    )
    result = apply_event(
        state=state,
        contract=contract,
        mission_state=mission_state,
        event=event,
    )
    if result["status"] == "APPLIED":
        with (root / "cognitive-memory-ledger.jsonl").open(
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
        _atomic_write(root / "snapshot.json", result["result_state"])
    return result


__all__ = [
    "EVENT_VERSION",
    "MEMORY_ENTRY_VERSION",
    "STORE_VERSION",
    "apply_event",
    "build_cognitive_memory_event",
    "build_committed_memory_entry",
    "build_initial_cognitive_memory_store",
    "event_digest",
    "initialize_cognitive_memory_store",
    "memory_entry_digest",
    "persist_cognitive_memory_consolidation",
    "recover_cognitive_memory_store",
    "store_digest",
    "validate_event_static",
    "validate_memory_entry_static",
    "validate_store_state",
]
