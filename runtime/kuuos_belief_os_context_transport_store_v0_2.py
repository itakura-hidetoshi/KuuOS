from __future__ import annotations

import json
import os
import tempfile
from contextlib import contextmanager
from copy import deepcopy
from pathlib import Path
from typing import Any, Iterator, Mapping

import fcntl

from runtime.kuuos_belief_os_context_transport_types_v0_2 import (
    APPLY_RESULT_VERSION,
    STATE_VERSION,
    STORE_COMMIT_VERSION,
    apply_result_digest,
    canonical_json,
    copy_boundary,
    copy_non_authority,
    packet_digest,
    receipt_digest,
    require_nonempty_string,
    require_nonnegative_int,
    sha,
    state_digest,
    store_commit_digest,
)
from runtime.kuuos_belief_os_context_transport_v0_2 import transport_belief_sections


class BeliefTransportStoreError(RuntimeError):
    pass


def build_initial_transport_state(*, lineage_id: str, now_ms: int) -> dict[str, Any]:
    state = {
        "version": STATE_VERSION,
        "lineage_id": require_nonempty_string(lineage_id, "lineage_id"),
        "event_count": 0,
        "run_count": 0,
        "processed_packet_digests": [],
        "latest_receipt_digest": "",
        "holonomy_chain_digest": sha(
            {"lineage_id": lineage_id, "kind": "belief_transport_genesis"}
        ),
        "receipt_history": [],
        "predecessor_transport_state_digest": "",
        "updated_at_ms": require_nonnegative_int(now_ms, "now_ms"),
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "belief_transport_state_digest": "",
    }
    state["belief_transport_state_digest"] = state_digest(state)
    return state


def validate_transport_state(state: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if state.get("version") != STATE_VERSION:
            errors.append("transport_state_version_invalid")
        require_nonempty_string(state.get("lineage_id"), "lineage_id")
        event_count = require_nonnegative_int(state.get("event_count"), "event_count")
        run_count = require_nonnegative_int(state.get("run_count"), "run_count")
        require_nonnegative_int(state.get("updated_at_ms"), "updated_at_ms")
        processed = list(state.get("processed_packet_digests", []))
        if len(processed) != len(set(processed)):
            errors.append("processed_packet_digest_duplicate")
        history = list(state.get("receipt_history", []))
        if event_count != len(history):
            errors.append("transport_event_history_count_mismatch")
        if run_count != event_count:
            errors.append("transport_run_count_mismatch")
        if len(processed) != event_count:
            errors.append("transport_processed_count_mismatch")
        require_nonempty_string(
            state.get("holonomy_chain_digest"), "holonomy_chain_digest"
        )
        if dict(state.get("non_authority", {})) != copy_non_authority():
            errors.append("transport_state_authority_escalation")
        if dict(state.get("boundary", {})) != copy_boundary():
            errors.append("transport_state_boundary_invalid")
        if state.get("belief_transport_state_digest") != state_digest(state):
            errors.append("transport_state_digest_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def _result(
    *,
    status: str,
    state: Mapping[str, Any],
    packet_id: str,
    receipt: Mapping[str, Any] | None,
    errors: list[str],
) -> dict[str, Any]:
    result = {
        "version": APPLY_RESULT_VERSION,
        "status": status,
        "packet_id": packet_id,
        "belief_transport_packet_digest": (
            packet_digest(receipt) if False else ""
        ),
        "receipt": deepcopy(dict(receipt)) if receipt is not None else None,
        "state": deepcopy(dict(state)),
        "errors": list(errors),
        "belief_transport_apply_result_digest": "",
    }
    result["belief_transport_apply_result_digest"] = apply_result_digest(result)
    return result


def apply_transport_packet(
    state: Mapping[str, Any], packet: Mapping[str, Any]
) -> dict[str, Any]:
    state_errors = validate_transport_state(state)
    if state_errors:
        raise ValueError("invalid_transport_state:" + ";".join(state_errors))
    packet_id = str(packet.get("packet_id", ""))
    packet_id_digest = str(packet.get("belief_transport_packet_digest", ""))
    if packet_id_digest in set(state.get("processed_packet_digests", [])):
        prior = next(
            (
                item
                for item in state.get("receipt_history", [])
                if item.get("belief_transport_packet_digest") == packet_id_digest
            ),
            None,
        )
        result = _result(
            status="REPLAYED",
            state=state,
            packet_id=packet_id,
            receipt=None,
            errors=[],
        )
        result["belief_transport_packet_digest"] = packet_id_digest
        result["replayed_receipt_digest"] = (
            prior.get("belief_transport_receipt_digest", "") if prior else ""
        )
        result["belief_transport_apply_result_digest"] = ""
        result["belief_transport_apply_result_digest"] = apply_result_digest(result)
        return result

    if packet.get("lineage_id") != state.get("lineage_id"):
        return _result(
            status="REJECTED",
            state=state,
            packet_id=packet_id,
            receipt=None,
            errors=["transport_packet_lineage_mismatch"],
        )
    if int(packet.get("created_at_ms", -1)) < int(state.get("updated_at_ms", 0)):
        return _result(
            status="REJECTED",
            state=state,
            packet_id=packet_id,
            receipt=None,
            errors=["transport_packet_time_regression"],
        )
    try:
        receipt = transport_belief_sections(packet)
    except (TypeError, ValueError) as exc:
        return _result(
            status="REJECTED",
            state=state,
            packet_id=packet_id,
            receipt=None,
            errors=[str(exc)],
        )

    next_state = deepcopy(dict(state))
    predecessor = str(state["belief_transport_state_digest"])
    next_state["predecessor_transport_state_digest"] = predecessor
    next_state["event_count"] = int(state["event_count"]) + 1
    next_state["run_count"] = int(state["run_count"]) + 1
    next_state["processed_packet_digests"] = list(
        state["processed_packet_digests"]
    ) + [packet_id_digest]
    next_state["latest_receipt_digest"] = receipt[
        "belief_transport_receipt_digest"
    ]
    next_state["holonomy_chain_digest"] = sha(
        {
            "previous_holonomy_chain_digest": state["holonomy_chain_digest"],
            "belief_transport_receipt_digest": receipt[
                "belief_transport_receipt_digest"
            ],
            "declared_paths": [
                item["declared_path"] for item in receipt["transported_sections"]
            ],
            "aggregate_holonomy_residual": receipt[
                "aggregate_holonomy_residual"
            ],
        }
    )
    next_state["receipt_history"] = list(state["receipt_history"]) + [
        {
            "event_index": next_state["event_count"],
            "packet_id": packet_id,
            "belief_transport_packet_digest": packet_id_digest,
            "belief_transport_receipt_digest": receipt[
                "belief_transport_receipt_digest"
            ],
            "route": receipt["route"],
            "target_context_id": receipt["target_context_id"],
            "aggregate_interval": deepcopy(receipt["aggregate_interval"]),
            "conflict_index": receipt["conflict_index"],
            "holonomy_chain_digest": next_state["holonomy_chain_digest"],
        }
    ]
    next_state["updated_at_ms"] = int(packet["created_at_ms"])
    next_state["belief_transport_state_digest"] = ""
    next_state["belief_transport_state_digest"] = state_digest(next_state)
    next_errors = validate_transport_state(next_state)
    if next_errors:
        raise ValueError("next_transport_state_invalid:" + ";".join(next_errors))

    result = _result(
        status="APPLIED",
        state=next_state,
        packet_id=packet_id,
        receipt=receipt,
        errors=[],
    )
    result["belief_transport_packet_digest"] = packet_id_digest
    result["belief_transport_apply_result_digest"] = ""
    result["belief_transport_apply_result_digest"] = apply_result_digest(result)
    return result


class BeliefTransportStore:
    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.genesis_path = self.root / "belief-transport-genesis.json"
        self.ledger_path = self.root / "belief-transport-ledger.jsonl"
        self.snapshot_path = self.root / "belief-transport-snapshot.json"
        self.lock_path = self.root / ".belief-transport.lock"

    @contextmanager
    def _locked(self) -> Iterator[None]:
        self.root.mkdir(parents=True, exist_ok=True)
        with self.lock_path.open("a+", encoding="utf-8") as handle:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)

    @staticmethod
    def _write_atomic(path: Path, value: Mapping[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(canonical_json(value))
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(tmp_name, path)
        finally:
            if os.path.exists(tmp_name):
                os.unlink(tmp_name)

    @staticmethod
    def _read_json(path: Path) -> dict[str, Any]:
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise BeliefTransportStoreError(f"json_read_failed:{path.name}") from exc
        if not isinstance(value, dict):
            raise BeliefTransportStoreError(f"json_object_required:{path.name}")
        return value

    def initialize(self, initial_state: Mapping[str, Any]) -> dict[str, Any]:
        errors = validate_transport_state(initial_state)
        if errors:
            raise BeliefTransportStoreError(
                "initial_transport_state_invalid:" + ";".join(errors)
            )
        with self._locked():
            if self.genesis_path.exists() or self.ledger_path.exists():
                raise BeliefTransportStoreError("transport_store_already_initialized")
            self._write_atomic(self.genesis_path, initial_state)
            self.ledger_path.touch(exist_ok=False)
            with self.ledger_path.open("a", encoding="utf-8") as handle:
                handle.flush()
                os.fsync(handle.fileno())
            self._write_atomic(self.snapshot_path, initial_state)
        return deepcopy(dict(initial_state))

    def _read_ledger(self) -> list[dict[str, Any]]:
        commits: list[dict[str, Any]] = []
        try:
            with self.ledger_path.open("r", encoding="utf-8") as handle:
                for line_number, raw in enumerate(handle, start=1):
                    line = raw.strip()
                    if not line:
                        raise BeliefTransportStoreError(
                            f"transport_ledger_blank_line:{line_number}"
                        )
                    try:
                        item = json.loads(line)
                    except json.JSONDecodeError as exc:
                        raise BeliefTransportStoreError(
                            f"transport_ledger_malformed_json:{line_number}"
                        ) from exc
                    if not isinstance(item, dict):
                        raise BeliefTransportStoreError(
                            f"transport_ledger_object_required:{line_number}"
                        )
                    commits.append(item)
        except OSError as exc:
            raise BeliefTransportStoreError("transport_ledger_read_failed") from exc
        return commits

    def _recover_unlocked(self) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        if not self.genesis_path.exists() or not self.ledger_path.exists():
            raise BeliefTransportStoreError("transport_store_not_initialized")
        state = self._read_json(self.genesis_path)
        errors = validate_transport_state(state)
        if errors:
            raise BeliefTransportStoreError(
                "transport_genesis_invalid:" + ";".join(errors)
            )
        commits = self._read_ledger()
        previous_commit_digest = ""
        for index, commit in enumerate(commits, start=1):
            if commit.get("version") != STORE_COMMIT_VERSION:
                raise BeliefTransportStoreError(
                    f"transport_ledger_version_invalid:{index}"
                )
            if commit.get("belief_transport_store_commit_digest") != store_commit_digest(
                commit
            ):
                raise BeliefTransportStoreError(
                    f"transport_ledger_commit_digest_invalid:{index}"
                )
            if commit.get("predecessor_commit_digest") != previous_commit_digest:
                raise BeliefTransportStoreError(
                    f"transport_ledger_chain_broken:{index}"
                )
            if commit.get("predecessor_transport_state_digest") != state.get(
                "belief_transport_state_digest"
            ):
                raise BeliefTransportStoreError(
                    f"transport_state_chain_broken:{index}"
                )
            packet = commit.get("packet")
            if not isinstance(packet, dict):
                raise BeliefTransportStoreError(
                    f"transport_ledger_packet_invalid:{index}"
                )
            result = apply_transport_packet(state, packet)
            if result.get("status") != "APPLIED":
                raise BeliefTransportStoreError(
                    f"transport_ledger_packet_not_applicable:{index}"
                )
            receipt = result.get("receipt")
            if not isinstance(receipt, dict):
                raise BeliefTransportStoreError(
                    f"transport_ledger_receipt_missing:{index}"
                )
            if commit.get("belief_transport_receipt_digest") != receipt.get(
                "belief_transport_receipt_digest"
            ):
                raise BeliefTransportStoreError(
                    f"transport_ledger_receipt_digest_mismatch:{index}"
                )
            if receipt.get("belief_transport_receipt_digest") != receipt_digest(receipt):
                raise BeliefTransportStoreError(
                    f"transport_ledger_receipt_corrupt:{index}"
                )
            state = result["state"]
            if commit.get("result_transport_state_digest") != state.get(
                "belief_transport_state_digest"
            ):
                raise BeliefTransportStoreError(
                    f"transport_ledger_result_state_mismatch:{index}"
                )
            previous_commit_digest = commit[
                "belief_transport_store_commit_digest"
            ]
        return state, commits

    def recover(self, *, require_snapshot_match: bool = True) -> dict[str, Any]:
        with self._locked():
            state, _ = self._recover_unlocked()
            if require_snapshot_match:
                if not self.snapshot_path.exists():
                    raise BeliefTransportStoreError("transport_snapshot_missing")
                snapshot = self._read_json(self.snapshot_path)
                if snapshot.get("belief_transport_state_digest") != state.get(
                    "belief_transport_state_digest"
                ):
                    raise BeliefTransportStoreError(
                        "transport_snapshot_ledger_mismatch"
                    )
            return deepcopy(state)

    def apply(self, packet: Mapping[str, Any]) -> dict[str, Any]:
        with self._locked():
            state, commits = self._recover_unlocked()
            result = apply_transport_packet(state, packet)
            if result.get("status") != "APPLIED":
                return result
            receipt = result["receipt"]
            predecessor_commit_digest = (
                commits[-1]["belief_transport_store_commit_digest"]
                if commits
                else ""
            )
            commit = {
                "version": STORE_COMMIT_VERSION,
                "commit_index": len(commits) + 1,
                "predecessor_commit_digest": predecessor_commit_digest,
                "predecessor_transport_state_digest": state[
                    "belief_transport_state_digest"
                ],
                "result_transport_state_digest": result["state"][
                    "belief_transport_state_digest"
                ],
                "belief_transport_packet_digest": packet[
                    "belief_transport_packet_digest"
                ],
                "belief_transport_receipt_digest": receipt[
                    "belief_transport_receipt_digest"
                ],
                "packet": deepcopy(dict(packet)),
                "belief_transport_store_commit_digest": "",
            }
            commit["belief_transport_store_commit_digest"] = store_commit_digest(
                commit
            )
            try:
                with self.ledger_path.open("a", encoding="utf-8") as handle:
                    handle.write(canonical_json(commit))
                    handle.write("\n")
                    handle.flush()
                    os.fsync(handle.fileno())
            except OSError as exc:
                raise BeliefTransportStoreError(
                    "transport_ledger_append_failed"
                ) from exc
            self._write_atomic(self.snapshot_path, result["state"])
            return result

    def repair_snapshot(self) -> dict[str, Any]:
        with self._locked():
            state, _ = self._recover_unlocked()
            self._write_atomic(self.snapshot_path, state)
            return deepcopy(state)

    def ledger_commit_count(self) -> int:
        with self._locked():
            _, commits = self._recover_unlocked()
            return len(commits)
