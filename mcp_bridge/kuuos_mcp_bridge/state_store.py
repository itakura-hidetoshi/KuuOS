from __future__ import annotations

import json
import os
import tempfile
import threading
from contextlib import contextmanager
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator, Mapping

try:
    import fcntl
except ImportError:  # pragma: no cover - non-POSIX local development
    fcntl = None


SCHEMA_VERSION = 1


class StateConflictError(RuntimeError):
    """Raised when optimistic concurrency detects a stale writer."""


class InvalidStatePatch(ValueError):
    """Raised when a patch attempts to mutate protected state fields."""


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


class JsonStateStore:
    """Atomic JSON store with optimistic compare-and-swap updates.

    The file is the shared canonical state for all MCP clients. Writers must
    supply the version they read. A stale writer gets StateConflictError
    rather than silently overwriting a newer Chat/Work update.
    """

    _PROTECTED = frozenset({"schema_version", "version", "updated_at", "updated_by"})

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
            self._validate_loaded(state)
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
            if current["version"] != expected_version:
                raise StateConflictError(
                    f"stale state version: expected {expected_version}, "
                    f"current {current['version']}"
                )

            protected = self._PROTECTED.intersection(patch)
            if protected:
                names = ", ".join(sorted(protected))
                raise InvalidStatePatch(f"protected fields cannot be patched: {names}")

            updated = deepcopy(current)
            for key, value in patch.items():
                updated[key] = deepcopy(value)

            updated["schema_version"] = SCHEMA_VERSION
            updated["version"] = current["version"] + 1
            updated["updated_at"] = utc_now_iso()
            updated["updated_by"] = actor
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
        for field in self._PROTECTED:
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

    @staticmethod
    def _validate_loaded(state: Any) -> None:
        if not isinstance(state, dict):
            raise ValueError("state file must contain a JSON object")
        if state.get("schema_version") != SCHEMA_VERSION:
            raise ValueError(
                f"unsupported schema_version: {state.get('schema_version')!r}"
            )
        version = state.get("version")
        if not isinstance(version, int) or version < 0:
            raise ValueError("state version must be a non-negative integer")
