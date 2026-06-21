from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping
import os

from runtime import kuuos_open_ended_background_agency_v0_30 as core

CORE_HORIZONS = core.CORE_HORIZONS
CommitResult = core.CommitResult
apply_request = core.apply_request
canonical_json = core.canonical_json
digest = core.digest
make_envelope = core.make_envelope
make_initial_state = core.make_initial_state
make_request = core.make_request
validate_state = core.validate_state


def _entry_request_id(body: Mapping[str, Any]) -> str | None:
    event = body.get("event")
    if not isinstance(event, dict):
        return None
    value = event.get("request_id")
    return value if isinstance(value, str) else None


def commit_request(
    *,
    state_path: Path,
    ledger_path: Path,
    request_envelope: Mapping[str, Any],
    applied_at_ms: int,
) -> CommitResult:
    state_path = Path(state_path)
    ledger_path = Path(ledger_path)
    state = core._read_json(state_path)
    validate_state(state)
    request_body = core.validate_envelope(request_envelope, label="request")
    entries = core._read_ledger(ledger_path)
    request_digest = request_envelope["body_digest"]
    request_id = request_body["request_id"]

    for entry in entries:
        body = core.validate_envelope(entry, label="ledger_transition")
        recorded_digest = body.get("request_digest")
        recorded_id = _entry_request_id(body)
        if recorded_id == request_id and recorded_digest != request_digest:
            raise ValueError("request_id_reuse_with_different_content")
        if recorded_digest == request_digest:
            result_state = body.get("result_state")
            if not isinstance(result_state, dict):
                raise ValueError("ledger_result_state_missing")
            validate_state(result_state)
            current_digest = state.get("body_digest")
            if current_digest == body.get("source_state_digest"):
                core._atomic_write_json(state_path, result_state)
                return CommitResult("REPLAYED_REPAIRED", entry, result_state, len(entries))
            if current_digest == result_state.get("body_digest"):
                return CommitResult("REPLAYED", entry, result_state, len(entries))
            return CommitResult("REPLAYED_WITH_LATER_STATE", entry, state, len(entries))

    if request_body.get("source_state_digest") != state.get("body_digest"):
        raise ValueError("stale_source_state")

    transition = apply_request(state, request_envelope, applied_at_ms=applied_at_ms)
    body = core.validate_envelope(transition, label="transition")
    result_state = body["result_state"]
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    with ledger_path.open("a", encoding="utf-8") as handle:
        handle.write(canonical_json(transition) + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    core._atomic_write_json(state_path, result_state)
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
