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
from runtime.kuuos_plan_os_lease_monitor_kernel_v0_16 import (
    validate_lease_monitor_tick,
)
from runtime.kuuos_plan_os_next_cycle_session_kernel_v0_15 import (
    validate_next_cycle_plan_session,
)
from runtime.kuuos_plan_os_rerotation_materialization_kernel_v0_13 import (
    validate_rerotation_materialization_receipt,
)
from runtime.kuuos_plan_os_suspension_recovery_kernel_v0_17 import (
    validate_suspension_recovery_handoff,
)
from runtime.kuuos_plan_os_suspension_recovery_types_v0_17 import (
    STORE_COMMIT_VERSION,
    require_int,
    store_commit_digest,
)


class SuspensionRecoveryStoreError(RuntimeError):
    pass


class SuspensionRecoveryStore:
    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.genesis = self.root / "recovery-genesis.json"
        self.ledger = self.root / "recovery-ledger.jsonl"
        self.snapshot = self.root / "recovery-snapshot.json"
        self.lock = self.root / ".plan-os-v017-recovery.lock"

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
    def _read(path: Path) -> dict[str, Any]:
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise SuspensionRecoveryStoreError("recovery_json_invalid") from exc
        if not isinstance(value, dict):
            raise SuspensionRecoveryStoreError("recovery_json_object_required")
        return value

    def initialize(
        self,
        *,
        session: Mapping[str, Any],
        suspension_tick: Mapping[str, Any],
        materialization_receipt: Mapping[str, Any],
    ) -> dict[str, Any]:
        if validate_next_cycle_plan_session(session):
            raise SuspensionRecoveryStoreError("recovery_genesis_session_invalid")
        if validate_lease_monitor_tick(suspension_tick):
            raise SuspensionRecoveryStoreError("recovery_genesis_tick_invalid")
        if validate_rerotation_materialization_receipt(materialization_receipt):
            raise SuspensionRecoveryStoreError(
                "recovery_genesis_materialization_invalid"
            )
        genesis = {
            "session": deepcopy(dict(session)),
            "suspension_tick": deepcopy(dict(suspension_tick)),
            "materialization_receipt": deepcopy(dict(materialization_receipt)),
        }
        with self._locked():
            if self.genesis.exists() or self.ledger.exists():
                raise SuspensionRecoveryStoreError("recovery_store_exists")
            self._atomic(self.genesis, genesis)
            self.ledger.touch(exist_ok=False)
            self._atomic(self.snapshot, genesis)
        return deepcopy(genesis)

    def _commits(self) -> list[dict[str, Any]]:
        try:
            values = [
                json.loads(raw)
                for raw in self.ledger.read_text(encoding="utf-8").splitlines()
            ]
        except (OSError, json.JSONDecodeError) as exc:
            raise SuspensionRecoveryStoreError("recovery_ledger_invalid") from exc
        if not all(isinstance(value, dict) for value in values):
            raise SuspensionRecoveryStoreError("recovery_commit_object_required")
        return values

    def _recover(
        self,
    ) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any] | None]:
        if not self.genesis.exists() or not self.ledger.exists():
            raise SuspensionRecoveryStoreError("recovery_store_missing")
        genesis = self._read(self.genesis)
        if validate_next_cycle_plan_session(dict(genesis.get("session", {}))):
            raise SuspensionRecoveryStoreError("recovery_genesis_session_invalid")
        if validate_lease_monitor_tick(dict(genesis.get("suspension_tick", {}))):
            raise SuspensionRecoveryStoreError("recovery_genesis_tick_invalid")
        if validate_rerotation_materialization_receipt(
            dict(genesis.get("materialization_receipt", {}))
        ):
            raise SuspensionRecoveryStoreError(
                "recovery_genesis_materialization_invalid"
            )
        commits = self._commits()
        if len(commits) > 1:
            raise SuspensionRecoveryStoreError(
                "recovery_multiple_commits_forbidden"
            )
        if not commits:
            return genesis, commits, None
        commit = commits[0]
        if commit.get("version") != STORE_COMMIT_VERSION:
            raise SuspensionRecoveryStoreError("recovery_commit_version_invalid")
        if commit.get(
            "suspension_recovery_store_commit_digest"
        ) != store_commit_digest(commit):
            raise SuspensionRecoveryStoreError("recovery_commit_digest_invalid")
        handoff = dict(commit.get("handoff", {}))
        if validate_suspension_recovery_handoff(handoff):
            raise SuspensionRecoveryStoreError("recovery_handoff_invalid")
        session = genesis["session"]
        tick = genesis["suspension_tick"]
        materialization = genesis["materialization_receipt"]
        if handoff.get("source_session_digest") != session.get(
            "plan_control_session_digest"
        ):
            raise SuspensionRecoveryStoreError("recovery_session_chain_invalid")
        if handoff.get("source_tick_digest") != tick.get(
            "lease_monitor_tick_digest"
        ):
            raise SuspensionRecoveryStoreError("recovery_tick_chain_invalid")
        if handoff.get(
            "source_materialization_receipt_digest"
        ) != materialization.get("rerotation_materialization_receipt_digest"):
            raise SuspensionRecoveryStoreError(
                "recovery_materialization_chain_invalid"
            )
        return genesis, commits, handoff

    def commit(
        self, *, handoff: Mapping[str, Any], now_ms: int
    ) -> dict[str, Any]:
        with self._locked():
            genesis, _, existing = self._recover()
            handoff_id = str(
                handoff.get("suspension_recovery_handoff_digest", "")
            )
            if existing is not None:
                if existing.get("suspension_recovery_handoff_digest") == handoff_id:
                    return {
                        "status": "REPLAYED",
                        "handoff": deepcopy(existing),
                        "errors": [],
                    }
                return {
                    "status": "REJECTED",
                    "handoff": deepcopy(dict(handoff)),
                    "errors": ["recovery_already_routed"],
                }
            errors = validate_suspension_recovery_handoff(handoff)
            if errors:
                return {
                    "status": "REJECTED",
                    "handoff": deepcopy(dict(handoff)),
                    "errors": errors,
                }
            if handoff.get("source_session_digest") != genesis["session"].get(
                "plan_control_session_digest"
            ):
                return {
                    "status": "REJECTED",
                    "handoff": deepcopy(dict(handoff)),
                    "errors": ["recovery_source_session_mismatch"],
                }
            if handoff.get("source_tick_digest") != genesis[
                "suspension_tick"
            ].get("lease_monitor_tick_digest"):
                return {
                    "status": "REJECTED",
                    "handoff": deepcopy(dict(handoff)),
                    "errors": ["recovery_source_tick_mismatch"],
                }
            commit = {
                "version": STORE_COMMIT_VERSION,
                "handoff": deepcopy(dict(handoff)),
                "committed_at_ms": require_int(now_ms, "now_ms"),
                "suspension_recovery_store_commit_digest": "",
            }
            commit[
                "suspension_recovery_store_commit_digest"
            ] = store_commit_digest(commit)
            with self.ledger.open("a", encoding="utf-8") as handle:
                handle.write(canonical_json(commit) + "\n")
                handle.flush()
                os.fsync(handle.fileno())
            self._atomic(self.snapshot, dict(handoff))
            return {
                "status": "APPLIED",
                "handoff": deepcopy(dict(handoff)),
                "commit": deepcopy(commit),
                "errors": [],
            }

    def recover(self, *, require_snapshot_match: bool = True) -> dict[str, Any]:
        with self._locked():
            genesis, _, handoff = self._recover()
            value = handoff if handoff is not None else genesis
            if require_snapshot_match and handoff is not None:
                snapshot = self._read(self.snapshot)
                if snapshot.get(
                    "suspension_recovery_handoff_digest"
                ) != handoff.get("suspension_recovery_handoff_digest"):
                    raise SuspensionRecoveryStoreError(
                        "recovery_snapshot_ledger_mismatch"
                    )
            return deepcopy(value)

    def repair_snapshot(self) -> dict[str, Any]:
        with self._locked():
            genesis, _, handoff = self._recover()
            value = handoff if handoff is not None else genesis
            self._atomic(self.snapshot, value)
            return deepcopy(value)
