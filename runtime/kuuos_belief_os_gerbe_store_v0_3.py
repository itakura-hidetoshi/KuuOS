from __future__ import annotations

import json
import os
import tempfile
from contextlib import contextmanager
from copy import deepcopy
from pathlib import Path
from typing import Any, Iterator, Mapping

import fcntl

from runtime.kuuos_belief_os_gerbe_coherence_v0_3 import (
    build_gerbe_coherence_receipt,
)
from runtime.kuuos_belief_os_gerbe_types_v0_3 import (
    APPLY_RESULT_VERSION,
    STATE_VERSION,
    STORE_COMMIT_VERSION,
    apply_result_digest,
    canonical_json,
    copy_boundary,
    copy_non_authority,
    receipt_digest,
    require_nonempty_string,
    require_nonnegative_int,
    sha,
    state_digest,
    store_commit_digest,
)


class BeliefGerbeStoreError(RuntimeError):
    pass


def build_initial_gerbe_state(*, lineage_id: str, now_ms: int) -> dict[str, Any]:
    state = {
        "version": STATE_VERSION,
        "lineage_id": require_nonempty_string(lineage_id, "lineage_id"),
        "event_count": 0,
        "run_count": 0,
        "processed_packet_digests": [],
        "latest_receipt_digest": "",
        "surface_holonomy_chain_digest": sha(
            {"lineage_id": lineage_id, "kind": "belief_gerbe_genesis"}
        ),
        "receipt_history": [],
        "predecessor_gerbe_state_digest": "",
        "updated_at_ms": require_nonnegative_int(now_ms, "now_ms"),
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "belief_gerbe_state_digest": "",
    }
    state["belief_gerbe_state_digest"] = state_digest(state)
    return state


def validate_gerbe_state(state: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if state.get("version") != STATE_VERSION:
            errors.append("gerbe_state_version_invalid")
        require_nonempty_string(state.get("lineage_id"), "lineage_id")
        event_count = require_nonnegative_int(state.get("event_count"), "event_count")
        run_count = require_nonnegative_int(state.get("run_count"), "run_count")
        require_nonnegative_int(state.get("updated_at_ms"), "updated_at_ms")
        processed = list(state.get("processed_packet_digests", []))
        history = list(state.get("receipt_history", []))
        if len(processed) != len(set(processed)):
            errors.append("gerbe_processed_packet_duplicate")
        if event_count != len(history):
            errors.append("gerbe_event_history_count_mismatch")
        if run_count != event_count:
            errors.append("gerbe_run_count_mismatch")
        if len(processed) != event_count:
            errors.append("gerbe_processed_count_mismatch")
        require_nonempty_string(
            state.get("surface_holonomy_chain_digest"),
            "surface_holonomy_chain_digest",
        )
        if dict(state.get("non_authority", {})) != copy_non_authority():
            errors.append("gerbe_state_authority_escalation")
        if dict(state.get("boundary", {})) != copy_boundary():
            errors.append("gerbe_state_boundary_invalid")
        if state.get("belief_gerbe_state_digest") != state_digest(state):
            errors.append("gerbe_state_digest_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def _result(
    *,
    status: str,
    state: Mapping[str, Any],
    packet_id: str,
    packet_digest_value: str,
    receipt: Mapping[str, Any] | None,
    errors: list[str],
    replayed_receipt_digest: str = "",
) -> dict[str, Any]:
    result = {
        "version": APPLY_RESULT_VERSION,
        "status": status,
        "packet_id": packet_id,
        "belief_gerbe_packet_digest": packet_digest_value,
        "replayed_receipt_digest": replayed_receipt_digest,
        "receipt": deepcopy(dict(receipt)) if receipt is not None else None,
        "state": deepcopy(dict(state)),
        "errors": list(errors),
        "belief_gerbe_apply_result_digest": "",
    }
    result["belief_gerbe_apply_result_digest"] = apply_result_digest(result)
    return result


def apply_gerbe_packet(
    state: Mapping[str, Any], packet: Mapping[str, Any]
) -> dict[str, Any]:
    state_errors = validate_gerbe_state(state)
    if state_errors:
        raise ValueError("invalid_gerbe_state:" + ";".join(state_errors))

    packet_id = str(packet.get("packet_id", ""))
    packet_digest_value = str(packet.get("belief_gerbe_packet_digest", ""))
    if packet_digest_value in set(state.get("processed_packet_digests", [])):
        prior = next(
            (
                item
                for item in state.get("receipt_history", [])
                if item.get("belief_gerbe_packet_digest") == packet_digest_value
            ),
            None,
        )
        return _result(
            status="REPLAYED",
            state=state,
            packet_id=packet_id,
            packet_digest_value=packet_digest_value,
            receipt=None,
            errors=[],
            replayed_receipt_digest=(
                str(prior.get("belief_gerbe_receipt_digest", ""))
                if prior
                else ""
            ),
        )

    if packet.get("lineage_id") != state.get("lineage_id"):
        return _result(
            status="REJECTED",
            state=state,
            packet_id=packet_id,
            packet_digest_value=packet_digest_value,
            receipt=None,
            errors=["gerbe_packet_lineage_mismatch"],
        )
    try:
        packet_time = int(packet.get("created_at_ms", -1))
    except (TypeError, ValueError):
        packet_time = -1
    if packet_time < int(state.get("updated_at_ms", 0)):
        return _result(
            status="REJECTED",
            state=state,
            packet_id=packet_id,
            packet_digest_value=packet_digest_value,
            receipt=None,
            errors=["gerbe_packet_time_regression"],
        )

    try:
        receipt = build_gerbe_coherence_receipt(packet)
    except (TypeError, ValueError) as exc:
        return _result(
            status="REJECTED",
            state=state,
            packet_id=packet_id,
            packet_digest_value=packet_digest_value,
            receipt=None,
            errors=[str(exc)],
        )

    next_state = deepcopy(dict(state))
    predecessor = str(state["belief_gerbe_state_digest"])
    next_state["predecessor_gerbe_state_digest"] = predecessor
    next_state["event_count"] = int(state["event_count"]) + 1
    next_state["run_count"] = int(state["run_count"]) + 1
    next_state["processed_packet_digests"] = list(
        state["processed_packet_digests"]
    ) + [packet_digest_value]
    next_state["latest_receipt_digest"] = receipt[
        "belief_gerbe_receipt_digest"
    ]
    next_state["surface_holonomy_chain_digest"] = sha(
        {
            "previous_surface_holonomy_chain_digest": state[
                "surface_holonomy_chain_digest"
            ],
            "belief_gerbe_receipt_digest": receipt[
                "belief_gerbe_receipt_digest"
            ],
            "source_gerbe_decision_digest": receipt[
                "source_gerbe_decision_digest"
            ],
            "path_digests": [
                item["path_digest"] for item in receipt["path_records"]
            ],
            "two_cell_count": receipt["two_cell_count"],
            "higher_witness_count": receipt["higher_witness_count"],
            "total_coherence_defect": receipt["total_coherence_defect"],
        }
    )
    next_state["receipt_history"] = list(state["receipt_history"]) + [
        {
            "event_index": next_state["event_count"],
            "packet_id": packet_id,
            "belief_gerbe_packet_digest": packet_digest_value,
            "belief_gerbe_receipt_digest": receipt[
                "belief_gerbe_receipt_digest"
            ],
            "source_gerbe_decision_digest": receipt[
                "source_gerbe_decision_digest"
            ],
            "target_context_id": receipt["target_context_id"],
            "route": receipt["route"],
            "coherent_interval": deepcopy(receipt["coherent_interval"]),
            "two_cell_count": receipt["two_cell_count"],
            "higher_witness_count": receipt["higher_witness_count"],
            "total_coherence_defect": receipt["total_coherence_defect"],
            "surface_holonomy_chain_digest": next_state[
                "surface_holonomy_chain_digest"
            ],
        }
    ]
    next_state["updated_at_ms"] = packet_time
    next_state["belief_gerbe_state_digest"] = ""
    next_state["belief_gerbe_state_digest"] = state_digest(next_state)
    next_errors = validate_gerbe_state(next_state)
    if next_errors:
        raise ValueError("next_gerbe_state_invalid:" + ";".join(next_errors))

    return _result(
        status="APPLIED",
        state=next_state,
        packet_id=packet_id,
        packet_digest_value=packet_digest_value,
        receipt=receipt,
        errors=[],
    )


class BeliefGerbeStore:
    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.genesis_path = self.root / "belief-gerbe-genesis.json"
        self.ledger_path = self.root / "belief-gerbe-ledger.jsonl"
        self.snapshot_path = self.root / "belief-gerbe-snapshot.json"
        self.lock_path = self.root / ".belief-gerbe.lock"

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
            raise BeliefGerbeStoreError(f"gerbe_json_read_failed:{path.name}") from exc
        if not isinstance(value, dict):
            raise BeliefGerbeStoreError(f"gerbe_json_object_required:{path.name}")
        return value

    def initialize(self, initial_state: Mapping[str, Any]) -> dict[str, Any]:
        errors = validate_gerbe_state(initial_state)
        if errors:
            raise BeliefGerbeStoreError(
                "initial_gerbe_state_invalid:" + ";".join(errors)
            )
        with self._locked():
            if self.genesis_path.exists() or self.ledger_path.exists():
                raise BeliefGerbeStoreError("gerbe_store_already_initialized")
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
                        raise BeliefGerbeStoreError(
                            f"gerbe_ledger_blank_line:{line_number}"
                        )
                    try:
                        item = json.loads(line)
                    except json.JSONDecodeError as exc:
                        raise BeliefGerbeStoreError(
                            f"gerbe_ledger_malformed_json:{line_number}"
                        ) from exc
                    if not isinstance(item, dict):
                        raise BeliefGerbeStoreError(
                            f"gerbe_ledger_object_required:{line_number}"
                        )
                    commits.append(item)
        except OSError as exc:
            raise BeliefGerbeStoreError("gerbe_ledger_read_failed") from exc
        return commits

    def _recover_unlocked(self) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        if not self.genesis_path.exists() or not self.ledger_path.exists():
            raise BeliefGerbeStoreError("gerbe_store_not_initialized")
        state = self._read_json(self.genesis_path)
        errors = validate_gerbe_state(state)
        if errors:
            raise BeliefGerbeStoreError(
                "gerbe_genesis_invalid:" + ";".join(errors)
            )
        commits = self._read_ledger()
        previous_commit_digest = ""
        for index, commit in enumerate(commits, start=1):
            if commit.get("version") != STORE_COMMIT_VERSION:
                raise BeliefGerbeStoreError(
                    f"gerbe_ledger_version_invalid:{index}"
                )
            if commit.get("belief_gerbe_store_commit_digest") != store_commit_digest(
                commit
            ):
                raise BeliefGerbeStoreError(
                    f"gerbe_ledger_commit_digest_invalid:{index}"
                )
            if commit.get("predecessor_commit_digest") != previous_commit_digest:
                raise BeliefGerbeStoreError(
                    f"gerbe_ledger_chain_broken:{index}"
                )
            if commit.get("predecessor_gerbe_state_digest") != state.get(
                "belief_gerbe_state_digest"
            ):
                raise BeliefGerbeStoreError(
                    f"gerbe_state_chain_broken:{index}"
                )
            packet = commit.get("packet")
            if not isinstance(packet, dict):
                raise BeliefGerbeStoreError(
                    f"gerbe_ledger_packet_invalid:{index}"
                )
            result = apply_gerbe_packet(state, packet)
            if result.get("status") != "APPLIED":
                raise BeliefGerbeStoreError(
                    f"gerbe_ledger_packet_not_applicable:{index}"
                )
            receipt = result.get("receipt")
            if not isinstance(receipt, dict):
                raise BeliefGerbeStoreError(
                    f"gerbe_ledger_receipt_missing:{index}"
                )
            if receipt.get("belief_gerbe_receipt_digest") != receipt_digest(receipt):
                raise BeliefGerbeStoreError(
                    f"gerbe_ledger_receipt_corrupt:{index}"
                )
            if commit.get("belief_gerbe_receipt_digest") != receipt.get(
                "belief_gerbe_receipt_digest"
            ):
                raise BeliefGerbeStoreError(
                    f"gerbe_ledger_receipt_digest_mismatch:{index}"
                )
            state = result["state"]
            if commit.get("result_gerbe_state_digest") != state.get(
                "belief_gerbe_state_digest"
            ):
                raise BeliefGerbeStoreError(
                    f"gerbe_ledger_result_state_mismatch:{index}"
                )
            previous_commit_digest = commit[
                "belief_gerbe_store_commit_digest"
            ]
        return state, commits

    def recover(self, *, require_snapshot_match: bool = True) -> dict[str, Any]:
        with self._locked():
            state, _ = self._recover_unlocked()
            if require_snapshot_match:
                if not self.snapshot_path.exists():
                    raise BeliefGerbeStoreError("gerbe_snapshot_missing")
                snapshot = self._read_json(self.snapshot_path)
                if snapshot.get("belief_gerbe_state_digest") != state.get(
                    "belief_gerbe_state_digest"
                ):
                    raise BeliefGerbeStoreError("gerbe_snapshot_ledger_mismatch")
            return deepcopy(state)

    def apply(self, packet: Mapping[str, Any]) -> dict[str, Any]:
        with self._locked():
            state, commits = self._recover_unlocked()
            result = apply_gerbe_packet(state, packet)
            if result.get("status") != "APPLIED":
                return result
            receipt = result["receipt"]
            predecessor_commit_digest = (
                commits[-1]["belief_gerbe_store_commit_digest"]
                if commits
                else ""
            )
            commit = {
                "version": STORE_COMMIT_VERSION,
                "commit_index": len(commits) + 1,
                "predecessor_commit_digest": predecessor_commit_digest,
                "predecessor_gerbe_state_digest": state[
                    "belief_gerbe_state_digest"
                ],
                "result_gerbe_state_digest": result["state"][
                    "belief_gerbe_state_digest"
                ],
                "belief_gerbe_packet_digest": packet[
                    "belief_gerbe_packet_digest"
                ],
                "belief_gerbe_receipt_digest": receipt[
                    "belief_gerbe_receipt_digest"
                ],
                "packet": deepcopy(dict(packet)),
                "belief_gerbe_store_commit_digest": "",
            }
            commit["belief_gerbe_store_commit_digest"] = store_commit_digest(commit)
            try:
                with self.ledger_path.open("a", encoding="utf-8") as handle:
                    handle.write(canonical_json(commit))
                    handle.write("\n")
                    handle.flush()
                    os.fsync(handle.fileno())
            except OSError as exc:
                raise BeliefGerbeStoreError("gerbe_ledger_append_failed") from exc
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
