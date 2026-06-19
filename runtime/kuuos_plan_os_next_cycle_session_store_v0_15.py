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
from runtime.kuuos_plan_os_materialized_chain_activation_kernel_v0_14 import (
    validate_materialized_chain_activation_receipt,
)
from runtime.kuuos_plan_os_rerotation_materialization_kernel_v0_13 import (
    validate_rerotation_materialization_receipt,
)
from runtime.kuuos_plan_os_next_cycle_session_kernel_v0_15 import (
    validate_next_cycle_plan_session,
)
from runtime.kuuos_plan_os_next_cycle_session_types_v0_15 import (
    STORE_COMMIT_VERSION,
    require_int,
    store_commit_digest,
)


class NextCycleSessionStoreError(RuntimeError):
    pass


class NextCycleSessionStore:
    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.genesis_path = self.root / "session-genesis.json"
        self.ledger_path = self.root / "session-ledger.jsonl"
        self.snapshot_path = self.root / "session-snapshot.json"
        self.lock_path = self.root / ".plan-os-v015-session.lock"

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
            raise NextCycleSessionStoreError(
                f"session_json_read_failed:{path.name}"
            ) from exc
        if not isinstance(value, dict):
            raise NextCycleSessionStoreError(
                f"session_json_object_required:{path.name}"
            )
        return value

    def initialize(
        self,
        *,
        activation_receipt: Mapping[str, Any],
        materialization_receipt: Mapping[str, Any],
    ) -> dict[str, Any]:
        activation_errors = validate_materialized_chain_activation_receipt(
            activation_receipt
        )
        materialization_errors = validate_rerotation_materialization_receipt(
            materialization_receipt
        )
        if activation_errors:
            raise NextCycleSessionStoreError(
                "session_genesis_activation_invalid:"
                + ";".join(activation_errors)
            )
        if materialization_errors:
            raise NextCycleSessionStoreError(
                "session_genesis_materialization_invalid:"
                + ";".join(materialization_errors)
            )
        genesis = {
            "activation_receipt": deepcopy(dict(activation_receipt)),
            "materialization_receipt": deepcopy(dict(materialization_receipt)),
        }
        with self._locked():
            if self.genesis_path.exists() or self.ledger_path.exists():
                raise NextCycleSessionStoreError("session_store_already_initialized")
            self._write_atomic(self.genesis_path, genesis)
            self.ledger_path.touch(exist_ok=False)
            self._write_atomic(self.snapshot_path, genesis)
        return deepcopy(genesis)

    def _read_commits(self) -> list[dict[str, Any]]:
        commits: list[dict[str, Any]] = []
        try:
            for line_number, raw in enumerate(
                self.ledger_path.read_text(encoding="utf-8").splitlines(),
                start=1,
            ):
                if not raw.strip():
                    raise NextCycleSessionStoreError(
                        f"session_ledger_blank_line:{line_number}"
                    )
                value = json.loads(raw)
                if not isinstance(value, dict):
                    raise NextCycleSessionStoreError(
                        f"session_ledger_object_required:{line_number}"
                    )
                commits.append(value)
        except (OSError, json.JSONDecodeError) as exc:
            raise NextCycleSessionStoreError("session_ledger_read_failed") from exc
        return commits

    def _recover_unlocked(self) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        if not self.genesis_path.exists() or not self.ledger_path.exists():
            raise NextCycleSessionStoreError("session_store_not_initialized")
        genesis = self._read_json(self.genesis_path)
        activation = dict(genesis.get("activation_receipt", {}))
        materialization = dict(genesis.get("materialization_receipt", {}))
        if validate_materialized_chain_activation_receipt(activation):
            raise NextCycleSessionStoreError("session_genesis_activation_invalid")
        if validate_rerotation_materialization_receipt(materialization):
            raise NextCycleSessionStoreError("session_genesis_materialization_invalid")
        commits = self._read_commits()
        if len(commits) > 1:
            raise NextCycleSessionStoreError("session_multiple_commits_forbidden")
        if not commits:
            return genesis, commits
        commit = commits[0]
        if commit.get("version") != STORE_COMMIT_VERSION:
            raise NextCycleSessionStoreError("session_commit_version_invalid")
        if commit.get("plan_control_session_store_commit_digest") != store_commit_digest(
            commit
        ):
            raise NextCycleSessionStoreError("session_commit_digest_invalid")
        if commit.get("source_activation_receipt_digest") != activation.get(
            "materialized_chain_activation_receipt_digest"
        ):
            raise NextCycleSessionStoreError("session_activation_chain_broken")
        if commit.get("source_materialization_receipt_digest") != materialization.get(
            "rerotation_materialization_receipt_digest"
        ):
            raise NextCycleSessionStoreError("session_materialization_chain_broken")
        session = dict(commit.get("session", {}))
        if validate_next_cycle_plan_session(session):
            raise NextCycleSessionStoreError("session_recovery_state_invalid")
        return session, commits

    def commit(self, *, session: Mapping[str, Any], now_ms: int) -> dict[str, Any]:
        with self._locked():
            current, commits = self._recover_unlocked()
            session_id = str(session.get("plan_control_session_digest", ""))
            if commits:
                existing_id = str(current.get("plan_control_session_digest", ""))
                if session_id == existing_id:
                    return {
                        "status": "REPLAYED",
                        "session": deepcopy(current),
                        "errors": [],
                    }
                return {
                    "status": "REJECTED",
                    "session": deepcopy(current),
                    "errors": ["session_already_bootstrapped"],
                }
            errors = validate_next_cycle_plan_session(session)
            if errors:
                return {
                    "status": "REJECTED",
                    "session": deepcopy(dict(session)),
                    "errors": errors,
                }
            activation = current["activation_receipt"]
            materialization = current["materialization_receipt"]
            if session.get("activation_receipt_digest") != activation.get(
                "materialized_chain_activation_receipt_digest"
            ):
                return {
                    "status": "REJECTED",
                    "session": deepcopy(dict(session)),
                    "errors": ["session_source_activation_mismatch"],
                }
            if session.get("materialization_receipt_digest") != materialization.get(
                "rerotation_materialization_receipt_digest"
            ):
                return {
                    "status": "REJECTED",
                    "session": deepcopy(dict(session)),
                    "errors": ["session_source_materialization_mismatch"],
                }
            commit = {
                "version": STORE_COMMIT_VERSION,
                "source_activation_receipt_digest": activation[
                    "materialized_chain_activation_receipt_digest"
                ],
                "source_materialization_receipt_digest": materialization[
                    "rerotation_materialization_receipt_digest"
                ],
                "session": deepcopy(dict(session)),
                "committed_at_ms": require_int(now_ms, "now_ms"),
                "plan_control_session_store_commit_digest": "",
            }
            commit["plan_control_session_store_commit_digest"] = store_commit_digest(
                commit
            )
            with self.ledger_path.open("a", encoding="utf-8") as handle:
                handle.write(canonical_json(commit) + "\n")
                handle.flush()
                os.fsync(handle.fileno())
            self._write_atomic(self.snapshot_path, dict(session))
            return {
                "status": "APPLIED",
                "session": deepcopy(dict(session)),
                "commit": deepcopy(commit),
                "errors": [],
            }

    def recover(self, *, require_snapshot_match: bool = True) -> dict[str, Any]:
        with self._locked():
            current, commits = self._recover_unlocked()
            if not commits:
                return deepcopy(current)
            if require_snapshot_match:
                snapshot = self._read_json(self.snapshot_path)
                if snapshot.get("plan_control_session_digest") != current.get(
                    "plan_control_session_digest"
                ):
                    raise NextCycleSessionStoreError(
                        "session_snapshot_ledger_mismatch"
                    )
            return deepcopy(current)

    def repair_snapshot(self) -> dict[str, Any]:
        with self._locked():
            current, _ = self._recover_unlocked()
            self._write_atomic(self.snapshot_path, current)
            return deepcopy(current)
