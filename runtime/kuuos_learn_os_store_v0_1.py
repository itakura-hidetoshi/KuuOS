from __future__ import annotations

import json
import os
import tempfile
from contextlib import contextmanager
from copy import deepcopy
from pathlib import Path
from typing import Any, Iterator, Mapping

import fcntl

from runtime.kuuos_belief_os_types_v0_1 import canonical_json
from runtime.kuuos_learn_os_kernel_v0_1 import apply_learn_event, validate_learn_state
from runtime.kuuos_learn_os_types_v0_1 import STORE_COMMIT_VERSION, store_commit_digest


class LearnStoreError(RuntimeError):
    pass


class LearnStore:
    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.genesis_path = self.root / "learn-genesis.json"
        self.ledger_path = self.root / "learn-ledger.jsonl"
        self.snapshot_path = self.root / "learn-snapshot.json"
        self.lock_path = self.root / ".learn-os.lock"

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
        fd, temporary = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(canonical_json(value))
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, path)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)

    @staticmethod
    def _read_json(path: Path) -> dict[str, Any]:
        try:
            with path.open("r", encoding="utf-8") as handle:
                value = json.load(handle)
        except (OSError, json.JSONDecodeError) as exc:
            raise LearnStoreError(f"learn_json_read_failed:{path.name}") from exc
        if not isinstance(value, dict):
            raise LearnStoreError(f"learn_json_object_required:{path.name}")
        return value

    def initialize(self, initial_state: Mapping[str, Any]) -> dict[str, Any]:
        errors = validate_learn_state(initial_state)
        if errors:
            raise LearnStoreError("initial_learn_state_invalid:" + ";".join(errors))
        with self._locked():
            if self.genesis_path.exists() or self.ledger_path.exists():
                raise LearnStoreError("learn_store_already_initialized")
            self._write_atomic(self.genesis_path, dict(initial_state))
            self.ledger_path.touch(exist_ok=False)
            with self.ledger_path.open("a", encoding="utf-8") as handle:
                handle.flush()
                os.fsync(handle.fileno())
            self._write_atomic(self.snapshot_path, dict(initial_state))
        return deepcopy(dict(initial_state))

    def _read_ledger(self) -> list[dict[str, Any]]:
        commits: list[dict[str, Any]] = []
        try:
            with self.ledger_path.open("r", encoding="utf-8") as handle:
                for line_number, raw in enumerate(handle, start=1):
                    line = raw.strip()
                    if not line:
                        raise LearnStoreError(f"learn_ledger_blank_line:{line_number}")
                    try:
                        value = json.loads(line)
                    except json.JSONDecodeError as exc:
                        raise LearnStoreError(
                            f"learn_ledger_malformed_json:{line_number}"
                        ) from exc
                    if not isinstance(value, dict):
                        raise LearnStoreError(
                            f"learn_ledger_object_required:{line_number}"
                        )
                    commits.append(value)
        except OSError as exc:
            raise LearnStoreError("learn_ledger_read_failed") from exc
        return commits

    def _recover_unlocked(self) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        if not self.genesis_path.exists() or not self.ledger_path.exists():
            raise LearnStoreError("learn_store_not_initialized")
        state = self._read_json(self.genesis_path)
        errors = validate_learn_state(state)
        if errors:
            raise LearnStoreError("learn_genesis_invalid:" + ";".join(errors))
        commits = self._read_ledger()
        previous_commit_digest = ""
        for index, commit in enumerate(commits, start=1):
            if commit.get("version") != STORE_COMMIT_VERSION:
                raise LearnStoreError(f"learn_ledger_version_invalid:{index}")
            if commit.get("learn_store_commit_digest") != store_commit_digest(commit):
                raise LearnStoreError(f"learn_ledger_commit_digest_invalid:{index}")
            if commit.get("predecessor_commit_digest") != previous_commit_digest:
                raise LearnStoreError(f"learn_ledger_chain_broken:{index}")
            if commit.get("predecessor_learn_state_digest") != state.get(
                "learn_state_digest"
            ):
                raise LearnStoreError(f"learn_state_chain_broken:{index}")
            event = commit.get("event")
            if not isinstance(event, dict):
                raise LearnStoreError(f"learn_ledger_event_invalid:{index}")
            result = apply_learn_event(state, event)
            if result.get("status") != "APPLIED":
                raise LearnStoreError(f"learn_ledger_event_not_applicable:{index}")
            state = result["state"]
            if commit.get("result_learn_state_digest") != state.get(
                "learn_state_digest"
            ):
                raise LearnStoreError(f"learn_ledger_result_digest_mismatch:{index}")
            previous_commit_digest = commit["learn_store_commit_digest"]
        return state, commits

    def recover(self, *, require_snapshot_match: bool = True) -> dict[str, Any]:
        with self._locked():
            state, _ = self._recover_unlocked()
            if require_snapshot_match:
                if not self.snapshot_path.exists():
                    raise LearnStoreError("learn_snapshot_missing")
                snapshot = self._read_json(self.snapshot_path)
                if snapshot.get("learn_state_digest") != state.get("learn_state_digest"):
                    raise LearnStoreError("learn_snapshot_ledger_mismatch")
            return deepcopy(state)

    def apply(self, event: Mapping[str, Any]) -> dict[str, Any]:
        with self._locked():
            state, commits = self._recover_unlocked()
            result = apply_learn_event(state, event)
            if result.get("status") != "APPLIED":
                return result
            commit = {
                "version": STORE_COMMIT_VERSION,
                "commit_index": len(commits) + 1,
                "predecessor_commit_digest": commits[-1]["learn_store_commit_digest"]
                if commits
                else "",
                "predecessor_learn_state_digest": state["learn_state_digest"],
                "result_learn_state_digest": result["state"]["learn_state_digest"],
                "event": deepcopy(dict(event)),
                "learn_store_commit_digest": "",
            }
            commit["learn_store_commit_digest"] = store_commit_digest(commit)
            try:
                with self.ledger_path.open("a", encoding="utf-8") as handle:
                    handle.write(canonical_json(commit))
                    handle.write("\n")
                    handle.flush()
                    os.fsync(handle.fileno())
            except OSError as exc:
                raise LearnStoreError("learn_ledger_append_failed") from exc
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
