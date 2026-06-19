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
from runtime.kuuos_plan_os_next_cycle_session_kernel_v0_15 import validate_next_cycle_plan_session
from runtime.kuuos_plan_os_lease_monitor_kernel_v0_16 import validate_lease_monitor_tick
from runtime.kuuos_plan_os_lease_monitor_types_v0_16 import (
    SESSION_SUSPENDED,
    STORE_COMMIT_VERSION,
    require_int,
    store_commit_digest,
)


class LeaseMonitorStoreError(RuntimeError):
    pass


class LeaseMonitorStore:
    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.genesis = self.root / "monitor-genesis.json"
        self.ledger = self.root / "monitor-ledger.jsonl"
        self.snapshot = self.root / "monitor-snapshot.json"
        self.lock = self.root / ".monitor.lock"

    @contextmanager
    def _locked(self) -> Iterator[None]:
        self.root.mkdir(parents=True, exist_ok=True)
        with self.lock.open("a+", encoding="utf-8") as handle:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)

    @staticmethod
    def _atomic(path: Path, value: Mapping[str, Any]) -> None:
        fd, temporary = tempfile.mkstemp(prefix=path.name, dir=path.parent)
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
    def _json(path: Path) -> dict[str, Any]:
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise LeaseMonitorStoreError("monitor_json_invalid") from exc
        if not isinstance(value, dict):
            raise LeaseMonitorStoreError("monitor_json_object_required")
        return value

    def initialize(self, session: Mapping[str, Any]) -> dict[str, Any]:
        errors = validate_next_cycle_plan_session(session)
        if errors:
            raise LeaseMonitorStoreError("monitor_session_invalid")
        with self._locked():
            if self.genesis.exists() or self.ledger.exists():
                raise LeaseMonitorStoreError("monitor_store_exists")
            self._atomic(self.genesis, dict(session))
            self.ledger.touch(exist_ok=False)
            self._atomic(self.snapshot, {"session": dict(session), "latest_tick": None})
        return deepcopy(dict(session))

    def _commits(self) -> list[dict[str, Any]]:
        values: list[dict[str, Any]] = []
        try:
            lines = self.ledger.read_text(encoding="utf-8").splitlines()
            for raw in lines:
                value = json.loads(raw)
                if not isinstance(value, dict):
                    raise LeaseMonitorStoreError("monitor_commit_object_required")
                values.append(value)
        except (OSError, json.JSONDecodeError) as exc:
            raise LeaseMonitorStoreError("monitor_ledger_invalid") from exc
        return values

    def _recover(self) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any] | None]:
        if not self.genesis.exists() or not self.ledger.exists():
            raise LeaseMonitorStoreError("monitor_store_missing")
        session = self._json(self.genesis)
        if validate_next_cycle_plan_session(session):
            raise LeaseMonitorStoreError("monitor_genesis_invalid")
        commits = self._commits()
        previous_digest = ""
        previous_tick: dict[str, Any] | None = None
        for index, commit in enumerate(commits, start=1):
            if commit.get("version") != STORE_COMMIT_VERSION:
                raise LeaseMonitorStoreError("monitor_commit_version_invalid")
            if commit.get("lease_monitor_store_commit_digest") != store_commit_digest(commit):
                raise LeaseMonitorStoreError("monitor_commit_digest_invalid")
            if commit.get("predecessor_commit_digest") != previous_digest:
                raise LeaseMonitorStoreError("monitor_commit_chain_invalid")
            tick = dict(commit.get("tick", {}))
            if validate_lease_monitor_tick(tick):
                raise LeaseMonitorStoreError("monitor_tick_invalid")
            if tick.get("source_session_digest") != session.get("plan_control_session_digest"):
                raise LeaseMonitorStoreError("monitor_session_chain_invalid")
            if tick.get("tick_index") != index:
                raise LeaseMonitorStoreError("monitor_tick_index_invalid")
            if previous_tick is not None:
                if previous_tick.get("session_status_after") == SESSION_SUSPENDED:
                    raise LeaseMonitorStoreError("monitor_tick_after_suspension")
                if int(tick["tick_at_ms"]) <= int(previous_tick["tick_at_ms"]):
                    raise LeaseMonitorStoreError("monitor_tick_time_invalid")
            previous_tick = tick
            previous_digest = commit["lease_monitor_store_commit_digest"]
        return session, commits, previous_tick

    def commit(self, *, tick: Mapping[str, Any], now_ms: int) -> dict[str, Any]:
        with self._locked():
            session, commits, latest = self._recover()
            tick_id = str(tick.get("lease_monitor_tick_digest", ""))
            for commit in commits:
                existing = dict(commit["tick"])
                if existing.get("lease_monitor_tick_digest") == tick_id and tick_id:
                    return {"status": "REPLAYED", "tick": existing, "errors": []}
            if latest is not None and latest.get("session_status_after") == SESSION_SUSPENDED:
                return {"status": "REJECTED", "tick": dict(tick), "errors": ["monitor_session_suspended"]}
            errors = validate_lease_monitor_tick(tick)
            if errors:
                return {"status": "REJECTED", "tick": dict(tick), "errors": errors}
            if tick.get("tick_index") != len(commits) + 1:
                return {"status": "REJECTED", "tick": dict(tick), "errors": ["monitor_tick_index_mismatch"]}
            if tick.get("source_session_digest") != session.get("plan_control_session_digest"):
                return {"status": "REJECTED", "tick": dict(tick), "errors": ["monitor_session_mismatch"]}
            if latest is not None and int(tick["tick_at_ms"]) <= int(latest["tick_at_ms"]):
                return {"status": "REJECTED", "tick": dict(tick), "errors": ["monitor_tick_time_not_monotone"]}
            commit = {
                "version": STORE_COMMIT_VERSION,
                "predecessor_commit_digest": commits[-1]["lease_monitor_store_commit_digest"] if commits else "",
                "source_session_digest": session["plan_control_session_digest"],
                "tick": deepcopy(dict(tick)),
                "committed_at_ms": require_int(now_ms, "now_ms"),
                "lease_monitor_store_commit_digest": "",
            }
            commit["lease_monitor_store_commit_digest"] = store_commit_digest(commit)
            with self.ledger.open("a", encoding="utf-8") as handle:
                handle.write(canonical_json(commit) + "\n")
                handle.flush()
                os.fsync(handle.fileno())
            state = {"session": session, "latest_tick": dict(tick)}
            self._atomic(self.snapshot, state)
            return {"status": "APPLIED", "tick": dict(tick), "commit": commit, "errors": []}

    def recover(self, *, require_snapshot_match: bool = True) -> dict[str, Any]:
        with self._locked():
            session, _, latest = self._recover()
            state = {"session": session, "latest_tick": latest}
            if require_snapshot_match:
                snapshot = self._json(self.snapshot)
                expected = latest.get("lease_monitor_tick_digest") if latest else session.get("plan_control_session_digest")
                actual = snapshot.get("latest_tick", {}).get("lease_monitor_tick_digest") if isinstance(snapshot.get("latest_tick"), dict) else snapshot.get("session", {}).get("plan_control_session_digest")
                if actual != expected:
                    raise LeaseMonitorStoreError("monitor_snapshot_ledger_mismatch")
            return deepcopy(state)

    def repair_snapshot(self) -> dict[str, Any]:
        with self._locked():
            session, _, latest = self._recover()
            state = {"session": session, "latest_tick": latest}
            self._atomic(self.snapshot, state)
            return deepcopy(state)
