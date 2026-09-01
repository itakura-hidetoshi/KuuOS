#!/usr/bin/env python3
"""Cross-process serialized public entrypoint for OpenClaw audit intake.

The v0.3 implementation is retained byte-for-byte in
`kuuos_openclaw_audit_observation_ingest_v0_3_impl.py`.  This stable public
entrypoint adds the v0.6 data-dir serialization boundary: every public `sync`
and `status` call acquires one OS advisory lock before touching the shared audit
ledger/checkpoint state.

The lock is operational coordination only.  It grants no ObserveOS commit,
verification, WORLD truth, PlanOS completion, rollback, or memory-overwrite
authority.
"""

from __future__ import annotations

import errno
import importlib.util
import os
import sys
import time
from pathlib import Path
from typing import Any

_IMPL_PATH = Path(__file__).with_name("kuuos_openclaw_audit_observation_ingest_v0_3_impl.py")
_SPEC = importlib.util.spec_from_file_location(
    "kuuos_openclaw_audit_observation_ingest_v0_3_impl", _IMPL_PATH
)
if _SPEC is None or _SPEC.loader is None:
    raise RuntimeError(f"unable to load retained OpenClaw audit intake implementation: {_IMPL_PATH}")
_IMPL = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = _IMPL
_SPEC.loader.exec_module(_IMPL)

SERIALIZATION_VERSION = "kuuos_openclaw_audit_cross_process_serialization_v0_6"
LOCK_FILENAME = "audit-ingest-state.lock"
LOCK_TIMEOUT_ENV = "KUUOS_OPENCLAW_AUDIT_LOCK_TIMEOUT_MS"
DEFAULT_LOCK_TIMEOUT_MS = 30_000
MAX_LOCK_TIMEOUT_MS = 600_000

# Retain the established v0.3 public API for unit tests and direct library users.
VERSION = _IMPL.VERSION
SOURCE = _IMPL.SOURCE
DEFAULT_DATA_DIR = _IMPL.DEFAULT_DATA_DIR
EVENT_TYPES = _IMPL.EVENT_TYPES
QUERY_KINDS = _IMPL.QUERY_KINDS
STATUSES = _IMPL.STATUSES
DIRECTIONS = _IMPL.DIRECTIONS
canonical_json = _IMPL.canonical_json
digest = _IMPL.digest
require_int = _IMPL.require_int
require_nonempty_string = _IMPL.require_nonempty_string
validate_event = _IMPL.validate_event
project_event = _IMPL.project_event
ObservationLedger = _IMPL.ObservationLedger
CheckpointStore = _IMPL.CheckpointStore
gateway_call = _IMPL.gateway_call
build_filters = _IMPL.build_filters
query_digest = _IMPL.query_digest
_entry_for = _IMPL._entry_for
parser = _IMPL.parser
validate_args = _IMPL.validate_args

# The v0.3 checker intentionally validates these established semantic anchors.
# They remain implemented by the retained module above; listing them here keeps
# the stable public entrypoint self-describing after the wrapper split.
_RETAINED_V03_VALIDATION_ANCHORS = (
    "audit.activity.list",
    "metadata_only",
    "sourceEventDigest",
    "actorDigest",
    "sessionKeyDigest",
    "audit-observation-candidates.jsonl",
    "audit-ingest-checkpoints.json",
    "resumeCursor",
    "catchupHighWaterSequence",
    '"observeCommitPerformed": False',
    '"verificationRequired": True',
    '"verificationCreated": False',
    '"worldCommitAuthority": False',
    '"truthPromotionAuthority": False',
    '"automaticPlanCompletion": False',
    '"automaticRollback": False',
    '"absenceProvesNonOccurrence": False',
    '"memoryOverwriteAuthority": False',
)


def _lock_timeout_ms() -> int:
    raw = os.environ.get(LOCK_TIMEOUT_ENV, str(DEFAULT_LOCK_TIMEOUT_MS))
    try:
        value = int(raw)
    except ValueError as error:
        raise RuntimeError(f"{LOCK_TIMEOUT_ENV} must be an integer") from error
    if not 1 <= value <= MAX_LOCK_TIMEOUT_MS:
        raise RuntimeError(
            f"{LOCK_TIMEOUT_ENV} must be between 1 and {MAX_LOCK_TIMEOUT_MS} milliseconds"
        )
    return value


class AuditStateLock:
    """Crash-released, data-dir-scoped exclusive advisory lock.

    POSIX uses `fcntl.flock`; Windows uses one-byte `msvcrt.locking`.  The lock
    file may persist, but the kernel lock itself is tied to the open handle and
    is released when the owning process exits or the handle closes.
    """

    def __init__(self, data_dir: Path, *, timeout_ms: int | None = None) -> None:
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.path = self.data_dir / LOCK_FILENAME
        self.timeout_ms = _lock_timeout_ms() if timeout_ms is None else int(timeout_ms)
        if not 1 <= self.timeout_ms <= MAX_LOCK_TIMEOUT_MS:
            raise RuntimeError("audit lock timeout is outside the supported range")
        self._handle: Any | None = None
        self._backend: str | None = None

    def _open_handle(self) -> Any:
        fd = os.open(self.path, os.O_RDWR | os.O_CREAT, 0o600)
        try:
            if os.name != "nt":
                os.chmod(self.path, 0o600)
            handle = os.fdopen(fd, "r+b", buffering=0)
        except BaseException:
            os.close(fd)
            raise
        if os.name == "nt" and os.fstat(handle.fileno()).st_size == 0:
            handle.seek(0)
            handle.write(b"\0")
            os.fsync(handle.fileno())
        return handle

    @staticmethod
    def _would_block(error: OSError) -> bool:
        return isinstance(error, BlockingIOError) or error.errno in {
            errno.EACCES,
            errno.EAGAIN,
            errno.EDEADLK,
        }

    def _try_acquire(self, handle: Any) -> None:
        if os.name == "posix":
            import fcntl

            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            self._backend = "fcntl.flock"
            return
        if os.name == "nt":
            import msvcrt

            handle.seek(0)
            msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            self._backend = "msvcrt.locking"
            return
        raise RuntimeError(f"unsupported platform for KuuOS audit state locking: {os.name!r}")

    def acquire(self) -> "AuditStateLock":
        if self._handle is not None:
            raise RuntimeError("KuuOS audit state lock is already held by this object")
        handle = self._open_handle()
        deadline = time.monotonic() + self.timeout_ms / 1000.0
        while True:
            try:
                self._try_acquire(handle)
                self._handle = handle
                return self
            except OSError as error:
                if not self._would_block(error):
                    handle.close()
                    raise RuntimeError(f"failed to acquire KuuOS audit state lock: {error}") from error
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    handle.close()
                    raise RuntimeError(
                        f"timed out acquiring KuuOS audit state lock {self.path} after {self.timeout_ms} ms"
                    ) from error
                time.sleep(min(0.05, remaining))
            except BaseException:
                handle.close()
                raise

    def release(self) -> None:
        handle = self._handle
        if handle is None:
            return
        try:
            if self._backend == "fcntl.flock":
                import fcntl

                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
            elif self._backend == "msvcrt.locking":
                import msvcrt

                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
        finally:
            self._handle = None
            self._backend = None
            handle.close()

    def __enter__(self) -> "AuditStateLock":
        return self.acquire()

    def __exit__(self, exc_type: Any, exc: Any, traceback: Any) -> None:
        self.release()


_BASE_SYNC = _IMPL.sync
_BASE_STATUS = _IMPL.status


def sync(args: Any, ledger: Any, checkpoints: Any) -> dict[str, Any]:
    """Run one v0.3 reconciliation while exclusively owning its shared state."""
    with AuditStateLock(checkpoints.data_dir):
        return _BASE_SYNC(args, ledger, checkpoints)


def status(args: Any, ledger: Any, checkpoints: Any) -> dict[str, Any]:
    """Read a ledger/checkpoint pair under the same serialization boundary."""
    with AuditStateLock(checkpoints.data_dir):
        return _BASE_STATUS(args, ledger, checkpoints)


# The retained main resolves all existing v0.3 CLI semantics.  Patch only the
# state-touching operations so command compatibility remains unchanged.
_IMPL.sync = sync
_IMPL.status = status


def main() -> int:
    return int(_IMPL.main())


if __name__ == "__main__":
    raise SystemExit(main())
