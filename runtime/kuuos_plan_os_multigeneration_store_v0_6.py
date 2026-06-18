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
from runtime.kuuos_plan_os_multigeneration_kernel_v0_6 import (
    apply_multi_generation_event,
    validate_multi_generation_state,
)
from runtime.kuuos_plan_os_multigeneration_types_v0_6 import (
    STORE_COMMIT_VERSION,
    require_int,
    store_commit_digest,
)


class MultiGenerationStoreError(RuntimeError):
    pass


class MultiGenerationSupervisorStore:
    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.genesis_path = self.root / "multi-generation-genesis.json"
        self.ledger_path = self.root / "multi-generation-ledger.jsonl"
        self.snapshot_path = self.root / "multi-generation-snapshot.json"
        self.lock_path = self.root / ".plan-os-v06-supervisor.lock"

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
        fd, temporary = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(canonical_json(value) + "\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, path)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)

    @staticmethod
    def _read_json(path: Path) -> dict[str, Any]:
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise MultiGenerationStoreError(
                f"multi_generation_json_read_failed:{path.name}"
            ) from exc
        if not isinstance(value, dict):
            raise MultiGenerationStoreError(
                f"multi_generation_json_object_required:{path.name}"
            )
        return value

    def initialize(self, initial_state: Mapping[str, Any]) -> dict[str, Any]:
        errors = validate_multi_generation_state(initial_state)
        if errors:
            raise MultiGenerationStoreError(
                "multi_generation_initial_state_invalid:" + ";".join(errors)
            )
        with self._locked():
            if self.genesis_path.exists() or self.ledger_path.exists():
                raise MultiGenerationStoreError(
                    "multi_generation_store_already_initialized"
                )
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
                        raise MultiGenerationStoreError(
                            f"multi_generation_ledger_blank_line:{line_number}"
                        )
                    item = json.loads(line)
                    if not isinstance(item, dict):
                        raise MultiGenerationStoreError(
                            f"multi_generation_ledger_object_required:{line_number}"
                        )
                    commits.append(item)
        except (OSError, json.JSONDecodeError) as exc:
            raise MultiGenerationStoreError(
                "multi_generation_ledger_read_failed"
            ) from exc
        return commits

    def _recover_unlocked(self) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        if not self.genesis_path.exists() or not self.ledger_path.exists():
            raise MultiGenerationStoreError("multi_generation_store_not_initialized")
        state = self._read_json(self.genesis_path)
        errors = validate_multi_generation_state(state)
        if errors:
            raise MultiGenerationStoreError(
                "multi_generation_genesis_invalid:" + ";".join(errors)
            )
        commits = self._read_ledger()
        previous_commit = ""
        for index, commit in enumerate(commits, start=1):
            if commit.get("version") != STORE_COMMIT_VERSION:
                raise MultiGenerationStoreError(
                    f"multi_generation_commit_version_invalid:{index}"
                )
            if commit.get("multi_generation_store_commit_digest") != store_commit_digest(
                commit
            ):
                raise MultiGenerationStoreError(
                    f"multi_generation_commit_digest_invalid:{index}"
                )
            if commit.get("predecessor_commit_digest") != previous_commit:
                raise MultiGenerationStoreError(
                    f"multi_generation_commit_chain_broken:{index}"
                )
            if commit.get("predecessor_state_digest") != state.get(
                "multi_generation_supervisor_state_digest"
            ):
                raise MultiGenerationStoreError(
                    f"multi_generation_state_chain_broken:{index}"
                )
            result = apply_multi_generation_event(state, dict(commit.get("event", {})))
            if result.get("status") != "APPLIED":
                raise MultiGenerationStoreError(
                    f"multi_generation_recovery_event_rejected:{index}:"
                    + ";".join(result.get("errors", []))
                )
            state = result["state"]
            if commit.get("result_state_digest") != state.get(
                "multi_generation_supervisor_state_digest"
            ):
                raise MultiGenerationStoreError(
                    f"multi_generation_result_digest_mismatch:{index}"
                )
            previous_commit = commit["multi_generation_store_commit_digest"]
        return state, commits

    def apply(self, event: Mapping[str, Any]) -> dict[str, Any]:
        with self._locked():
            state, commits = self._recover_unlocked()
            result = apply_multi_generation_event(state, event)
            if result.get("status") != "APPLIED":
                return deepcopy(result)
            next_state = result["state"]
            commit = {
                "version": STORE_COMMIT_VERSION,
                "commit_index": len(commits) + 1,
                "predecessor_commit_digest": commits[-1][
                    "multi_generation_store_commit_digest"
                ]
                if commits
                else "",
                "predecessor_state_digest": state[
                    "multi_generation_supervisor_state_digest"
                ],
                "event": deepcopy(dict(event)),
                "committed_at_ms": require_int(
                    event.get("created_at_ms"), "committed_at_ms"
                ),
                "result_state_digest": next_state[
                    "multi_generation_supervisor_state_digest"
                ],
                "multi_generation_store_commit_digest": "",
            }
            commit["multi_generation_store_commit_digest"] = store_commit_digest(
                commit
            )
            with self.ledger_path.open("a", encoding="utf-8") as handle:
                handle.write(canonical_json(commit) + "\n")
                handle.flush()
                os.fsync(handle.fileno())
            self._write_atomic(self.snapshot_path, next_state)
            return {
                "status": "APPLIED",
                "state": deepcopy(next_state),
                "commit": deepcopy(commit),
                "errors": [],
            }

    def recover(self, *, require_snapshot_match: bool = True) -> dict[str, Any]:
        with self._locked():
            state, _ = self._recover_unlocked()
            if require_snapshot_match:
                snapshot = self._read_json(self.snapshot_path)
                if snapshot.get(
                    "multi_generation_supervisor_state_digest"
                ) != state.get("multi_generation_supervisor_state_digest"):
                    raise MultiGenerationStoreError(
                        "multi_generation_snapshot_ledger_mismatch"
                    )
            return deepcopy(state)

    def repair_snapshot(self) -> dict[str, Any]:
        with self._locked():
            state, _ = self._recover_unlocked()
            self._write_atomic(self.snapshot_path, state)
            return deepcopy(state)

    def ledger_commit_count(self) -> int:
        with self._locked():
            _, commits = self._recover_unlocked()
            return len(commits)
