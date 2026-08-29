from __future__ import annotations

import json
import os
import tempfile
import threading
from contextlib import contextmanager
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator, Mapping, Protocol

try:
    import fcntl
except ImportError:  # pragma: no cover - non-POSIX local development
    fcntl = None


SCHEMA_VERSION = 1
PROTECTED_FIELDS = frozenset({"schema_version", "version", "updated_at", "updated_by"})


class StateConflictError(RuntimeError):
    """Raised when optimistic concurrency detects a stale writer."""


class InvalidStatePatch(ValueError):
    """Raised when a patch attempts to mutate protected state fields."""


class StateStore(Protocol):
    """Storage contract used by the MCP surface."""

    def read(self) -> dict[str, Any]: ...

    def update(
        self,
        patch: Mapping[str, Any],
        *,
        expected_version: int,
        actor: str,
    ) -> dict[str, Any]: ...

    def replace(
        self,
        state: Mapping[str, Any],
        *,
        expected_version: int,
        actor: str,
    ) -> dict[str, Any]: ...


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def default_state() -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "version": 0,
        "project": "KuuOS",
        "repository": "itakura-hidetoshi/KuuOS",
        "canonical_branch": "main",
        "canonical_sha": None,
        "active_pr": None,
        "ci": None,
        "mathematical_frontier": None,
        "next_actions": [],
        "continuation": {},
        "updated_at": None,
        "updated_by": None,
    }


def validate_loaded_state(state: Any) -> None:
    if not isinstance(state, dict):
        raise ValueError("state store must contain a JSON object")
    if state.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(f"unsupported schema_version: {state.get('schema_version')!r}")
    version = state.get("version")
    if not isinstance(version, int) or version < 0:
        raise ValueError("state version must be a non-negative integer")


def apply_patch(
    current: Mapping[str, Any],
    patch: Mapping[str, Any],
    *,
    expected_version: int,
    actor: str,
) -> dict[str, Any]:
    """Apply one validated CAS transition independently of the storage backend."""
    current_dict = dict(current)
    validate_loaded_state(current_dict)
    if current_dict["version"] != expected_version:
        raise StateConflictError(
            f"stale state version: expected {expected_version}, "
            f"current {current_dict['version']}"
        )

    protected = PROTECTED_FIELDS.intersection(patch)
    if protected:
        names = ", ".join(sorted(protected))
        raise InvalidStatePatch(f"protected fields cannot be patched: {names}")

    updated = deepcopy(current_dict)
    for key, value in patch.items():
        updated[key] = deepcopy(value)

    updated["schema_version"] = SCHEMA_VERSION
    updated["version"] = current_dict["version"] + 1
    updated["updated_at"] = utc_now_iso()
    updated["updated_by"] = actor
    return updated


class JsonStateStore:
    """Atomic JSON store for one host or a shared POSIX filesystem."""

    def __init__(self, path: str | os.PathLike[str]):
        self.path = Path(path)
        self.lock_path = self.path.with_suffix(self.path.suffix + ".lock")
        self._lock = threading.RLock()

    def read(self) -> dict[str, Any]:
        with self._lock:
            if not self.path.exists():
                return default_state()
            with self.path.open("r", encoding="utf-8") as handle:
                state = json.load(handle)
            validate_loaded_state(state)
            return deepcopy(state)

    def update(
        self,
        patch: Mapping[str, Any],
        *,
        expected_version: int,
        actor: str,
    ) -> dict[str, Any]:
        with self._lock, self._exclusive_file_lock():
            current = self.read()
            updated = apply_patch(
                current,
                patch,
                expected_version=expected_version,
                actor=actor,
            )
            self._atomic_write(updated)
            return deepcopy(updated)

    def replace(
        self,
        state: Mapping[str, Any],
        *,
        expected_version: int,
        actor: str,
    ) -> dict[str, Any]:
        replacement = dict(state)
        for field in PROTECTED_FIELDS:
            replacement.pop(field, None)
        return self.update(replacement, expected_version=expected_version, actor=actor)

    @contextmanager
    def _exclusive_file_lock(self) -> Iterator[None]:
        """Serialize compare-and-swap across server processes on POSIX hosts."""
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)
        with self.lock_path.open("a+", encoding="utf-8") as lock_handle:
            if fcntl is not None:
                fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                if fcntl is not None:
                    fcntl.flock(lock_handle.fileno(), fcntl.LOCK_UN)

    def _atomic_write(self, state: Mapping[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_name = tempfile.mkstemp(
            prefix=f".{self.path.name}.",
            suffix=".tmp",
            dir=self.path.parent,
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(state, handle, ensure_ascii=False, indent=2, sort_keys=True)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(tmp_name, self.path)
        finally:
            if os.path.exists(tmp_name):
                os.unlink(tmp_name)


class PostgresStateStore:
    """PostgreSQL-backed CAS store for replicated or serverless MCP deployments."""

    _TABLE = "kuuos_mcp_state"

    def __init__(self, database_url: str, *, state_key: str = "project"):
        if not database_url:
            raise ValueError("database_url must be non-empty")
        self.database_url = database_url
        self.state_key = state_key
        self._ensure_schema()

    def _connect(self):
        try:
            import psycopg
        except ImportError as exc:  # pragma: no cover - depends on deploy extra
            raise RuntimeError(
                "PostgreSQL backend requires `pip install 'kuuos-mcp-bridge[postgres]'`"
            ) from exc
        return psycopg.connect(self.database_url)

    @staticmethod
    def _jsonb(value: Mapping[str, Any]):
        try:
            from psycopg.types.json import Jsonb
        except ImportError as exc:  # pragma: no cover - depends on deploy extra
            raise RuntimeError(
                "PostgreSQL backend requires `pip install 'kuuos-mcp-bridge[postgres]'`"
            ) from exc
        return Jsonb(dict(value))

    def _ensure_schema(self) -> None:
        with self._connect() as conn:
            conn.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {self._TABLE} (
                    state_key TEXT PRIMARY KEY,
                    version BIGINT NOT NULL,
                    payload JSONB NOT NULL
                )
                """
            )

    def read(self) -> dict[str, Any]:
        with self._connect() as conn:
            row = conn.execute(
                f"SELECT version, payload FROM {self._TABLE} WHERE state_key = %s",
                (self.state_key,),
            ).fetchone()
        if row is None:
            return default_state()
        version, payload = row
        state = dict(payload)
        validate_loaded_state(state)
        if state["version"] != version:
            raise ValueError("PostgreSQL state version column and payload disagree")
        return deepcopy(state)

    def update(
        self,
        patch: Mapping[str, Any],
        *,
        expected_version: int,
        actor: str,
    ) -> dict[str, Any]:
        with self._connect() as conn:
            initial = default_state()
            conn.execute(
                f"""
                INSERT INTO {self._TABLE} (state_key, version, payload)
                VALUES (%s, %s, %s)
                ON CONFLICT (state_key) DO NOTHING
                """,
                (self.state_key, initial["version"], self._jsonb(initial)),
            )
            row = conn.execute(
                f"""
                SELECT version, payload
                FROM {self._TABLE}
                WHERE state_key = %s
                FOR UPDATE
                """,
                (self.state_key,),
            ).fetchone()
            if row is None:  # pragma: no cover - invariant after INSERT
                raise RuntimeError("failed to initialize PostgreSQL state row")

            version, payload = row
            current = dict(payload)
            validate_loaded_state(current)
            if current["version"] != version:
                raise ValueError("PostgreSQL state version column and payload disagree")

            updated = apply_patch(
                current,
                patch,
                expected_version=expected_version,
                actor=actor,
            )
            cursor = conn.execute(
                f"""
                UPDATE {self._TABLE}
                SET version = %s, payload = %s
                WHERE state_key = %s AND version = %s
                """,
                (
                    updated["version"],
                    self._jsonb(updated),
                    self.state_key,
                    version,
                ),
            )
            if cursor.rowcount != 1:
                raise StateConflictError("state changed during PostgreSQL CAS update")
            return deepcopy(updated)

    def replace(
        self,
        state: Mapping[str, Any],
        *,
        expected_version: int,
        actor: str,
    ) -> dict[str, Any]:
        replacement = dict(state)
        for field in PROTECTED_FIELDS:
            replacement.pop(field, None)
        return self.update(replacement, expected_version=expected_version, actor=actor)
