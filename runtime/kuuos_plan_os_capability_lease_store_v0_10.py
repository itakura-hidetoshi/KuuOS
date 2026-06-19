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
from runtime.kuuos_plan_os_capability_consumption_v0_10 import apply_lease_consumption
from runtime.kuuos_plan_os_capability_renewal_v0_10 import apply_lease_renewal
from runtime.kuuos_plan_os_capability_lease_kernel_v0_10 import validate_capability_lease_state
from runtime.kuuos_plan_os_capability_lease_types_v0_10 import (
    STORE_COMMIT_VERSION,
    require_int,
    store_commit_digest,
)


class CapabilityLeaseStoreError(RuntimeError):
    pass


class CapabilityLeaseStore:
    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.genesis_path = self.root / "lease-genesis.json"
        self.ledger_path = self.root / "lease-ledger.jsonl"
        self.snapshot_path = self.root / "lease-snapshot.json"
        self.lock_path = self.root / ".plan-os-v010-lease.lock"

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
            raise CapabilityLeaseStoreError(f"lease_json_read_failed:{path.name}") from exc
        if not isinstance(value, dict):
            raise CapabilityLeaseStoreError(f"lease_json_object_required:{path.name}")
        return value

    def initialize(self, initial_state: Mapping[str, Any]) -> dict[str, Any]:
        errors = validate_capability_lease_state(initial_state)
        if errors:
            raise CapabilityLeaseStoreError("lease_initial_state_invalid:" + ";".join(errors))
        with self._locked():
            if self.genesis_path.exists() or self.ledger_path.exists():
                raise CapabilityLeaseStoreError("lease_store_already_initialized")
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
                    item = json.loads(raw)
                    if not isinstance(item, dict):
                        raise CapabilityLeaseStoreError(f"lease_ledger_object_required:{line_number}")
                    commits.append(item)
        except (OSError, json.JSONDecodeError) as exc:
            raise CapabilityLeaseStoreError("lease_ledger_read_failed") from exc
        return commits

    @staticmethod
    def _apply(state: Mapping[str, Any], event_type: str, receipt: Mapping[str, Any]) -> dict[str, Any]:
        if event_type == "CONSUME":
            return apply_lease_consumption(state, receipt)
        if event_type == "RENEW":
            return apply_lease_renewal(state, receipt)
        return {"status": "REJECTED", "state": deepcopy(dict(state)), "errors": ["lease_event_type_invalid"]}

    def _recover_unlocked(self) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        if not self.genesis_path.exists() or not self.ledger_path.exists():
            raise CapabilityLeaseStoreError("lease_store_not_initialized")
        state = self._read_json(self.genesis_path)
        commits = self._read_ledger()
        previous_commit = ""
        for index, commit in enumerate(commits, start=1):
            if commit.get("version") != STORE_COMMIT_VERSION:
                raise CapabilityLeaseStoreError(f"lease_commit_version_invalid:{index}")
            if commit.get("capability_lease_store_commit_digest") != store_commit_digest(commit):
                raise CapabilityLeaseStoreError(f"lease_commit_digest_invalid:{index}")
            if commit.get("predecessor_commit_digest") != previous_commit:
                raise CapabilityLeaseStoreError(f"lease_commit_chain_broken:{index}")
            if commit.get("predecessor_state_digest") != state.get("capability_lease_state_digest"):
                raise CapabilityLeaseStoreError(f"lease_state_chain_broken:{index}")
            result = self._apply(state, str(commit.get("event_type")), dict(commit.get("receipt", {})))
            if result.get("status") != "APPLIED":
                raise CapabilityLeaseStoreError(f"lease_recovery_event_rejected:{index}")
            state = result["state"]
            if commit.get("result_state_digest") != state.get("capability_lease_state_digest"):
                raise CapabilityLeaseStoreError(f"lease_result_digest_mismatch:{index}")
            previous_commit = commit["capability_lease_store_commit_digest"]
        return state, commits

    def commit(self, *, event_type: str, receipt: Mapping[str, Any], now_ms: int) -> dict[str, Any]:
        with self._locked():
            state, commits = self._recover_unlocked()
            result = self._apply(state, event_type, receipt)
            if result.get("status") != "APPLIED":
                return deepcopy(result)
            next_state = result["state"]
            commit = {
                "version": STORE_COMMIT_VERSION,
                "commit_index": len(commits) + 1,
                "predecessor_commit_digest": commits[-1]["capability_lease_store_commit_digest"] if commits else "",
                "predecessor_state_digest": state["capability_lease_state_digest"],
                "event_type": event_type,
                "receipt": deepcopy(dict(receipt)),
                "committed_at_ms": require_int(now_ms, "now_ms"),
                "result_state_digest": next_state["capability_lease_state_digest"],
                "capability_lease_store_commit_digest": "",
            }
            commit["capability_lease_store_commit_digest"] = store_commit_digest(commit)
            with self.ledger_path.open("a", encoding="utf-8") as handle:
                handle.write(canonical_json(commit) + "\n")
                handle.flush()
                os.fsync(handle.fileno())
            self._write_atomic(self.snapshot_path, next_state)
            return {"status": "APPLIED", "state": deepcopy(next_state), "commit": deepcopy(commit), "errors": []}

    def recover(self, *, require_snapshot_match: bool = True) -> dict[str, Any]:
        with self._locked():
            state, _ = self._recover_unlocked()
            if require_snapshot_match:
                snapshot = self._read_json(self.snapshot_path)
                if snapshot.get("capability_lease_state_digest") != state.get("capability_lease_state_digest"):
                    raise CapabilityLeaseStoreError("lease_snapshot_ledger_mismatch")
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
