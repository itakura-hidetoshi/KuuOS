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
from runtime.kuuos_plan_os_renewal_escalation_decision_v0_12 import (
    apply_escalation_decision,
)
from runtime.kuuos_plan_os_renewal_escalation_state_v0_12 import (
    validate_renewal_escalation_state,
)
from runtime.kuuos_plan_os_renewal_escalation_types_v0_12 import (
    STORE_COMMIT_VERSION,
    require_int,
    store_commit_digest,
)


class RenewalEscalationStoreError(RuntimeError):
    pass


class RenewalEscalationStore:
    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.genesis_path = self.root / "escalation-genesis.json"
        self.ledger_path = self.root / "escalation-ledger.jsonl"
        self.snapshot_path = self.root / "escalation-snapshot.json"
        self.lock_path = self.root / ".plan-os-v012-escalation.lock"

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
            raise RenewalEscalationStoreError(
                f"escalation_json_read_failed:{path.name}"
            ) from exc
        if not isinstance(value, dict):
            raise RenewalEscalationStoreError(
                f"escalation_json_object_required:{path.name}"
            )
        return value

    def initialize(self, state: Mapping[str, Any]) -> dict[str, Any]:
        errors = validate_renewal_escalation_state(state)
        if errors:
            raise RenewalEscalationStoreError(
                "escalation_initial_state_invalid:" + ";".join(errors)
            )
        with self._locked():
            if self.genesis_path.exists() or self.ledger_path.exists():
                raise RenewalEscalationStoreError("escalation_store_already_initialized")
            self._write_atomic(self.genesis_path, dict(state))
            self.ledger_path.touch(exist_ok=False)
            self._write_atomic(self.snapshot_path, dict(state))
        return deepcopy(dict(state))

    def _read_commits(self) -> list[dict[str, Any]]:
        commits: list[dict[str, Any]] = []
        try:
            for line_number, raw in enumerate(
                self.ledger_path.read_text(encoding="utf-8").splitlines(),
                start=1,
            ):
                if not raw.strip():
                    raise RenewalEscalationStoreError(
                        f"escalation_ledger_blank_line:{line_number}"
                    )
                value = json.loads(raw)
                if not isinstance(value, dict):
                    raise RenewalEscalationStoreError(
                        f"escalation_ledger_object_required:{line_number}"
                    )
                commits.append(value)
        except (OSError, json.JSONDecodeError) as exc:
            raise RenewalEscalationStoreError("escalation_ledger_read_failed") from exc
        return commits

    def _recover_unlocked(self) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        if not self.genesis_path.exists() or not self.ledger_path.exists():
            raise RenewalEscalationStoreError("escalation_store_not_initialized")
        state = self._read_json(self.genesis_path)
        errors = validate_renewal_escalation_state(state)
        if errors:
            raise RenewalEscalationStoreError(
                "escalation_genesis_invalid:" + ";".join(errors)
            )
        commits = self._read_commits()
        previous_commit = ""
        for index, commit in enumerate(commits, start=1):
            if commit.get("version") != STORE_COMMIT_VERSION:
                raise RenewalEscalationStoreError(
                    f"escalation_commit_version_invalid:{index}"
                )
            if commit.get("renewal_escalation_store_commit_digest") != store_commit_digest(commit):
                raise RenewalEscalationStoreError(
                    f"escalation_commit_digest_invalid:{index}"
                )
            if commit.get("predecessor_commit_digest") != previous_commit:
                raise RenewalEscalationStoreError(
                    f"escalation_commit_chain_broken:{index}"
                )
            if commit.get("predecessor_state_digest") != state.get(
                "renewal_escalation_state_digest"
            ):
                raise RenewalEscalationStoreError(
                    f"escalation_state_chain_broken:{index}"
                )
            result = apply_escalation_decision(
                state, dict(commit.get("decision", {}))
            )
            if result.get("status") != "APPLIED":
                raise RenewalEscalationStoreError(
                    f"escalation_recovery_decision_rejected:{index}"
                )
            state = result["state"]
            if commit.get("result_state_digest") != state.get(
                "renewal_escalation_state_digest"
            ):
                raise RenewalEscalationStoreError(
                    f"escalation_result_digest_mismatch:{index}"
                )
            previous_commit = commit[
                "renewal_escalation_store_commit_digest"
            ]
        return state, commits

    def commit(self, *, decision: Mapping[str, Any], now_ms: int) -> dict[str, Any]:
        with self._locked():
            state, commits = self._recover_unlocked()
            result = apply_escalation_decision(state, decision)
            if result.get("status") != "APPLIED":
                return deepcopy(result)
            next_state = result["state"]
            commit = {
                "version": STORE_COMMIT_VERSION,
                "commit_index": len(commits) + 1,
                "predecessor_commit_digest": (
                    commits[-1]["renewal_escalation_store_commit_digest"]
                    if commits
                    else ""
                ),
                "predecessor_state_digest": state[
                    "renewal_escalation_state_digest"
                ],
                "decision": deepcopy(dict(decision)),
                "committed_at_ms": require_int(now_ms, "now_ms"),
                "result_state_digest": next_state[
                    "renewal_escalation_state_digest"
                ],
                "renewal_escalation_store_commit_digest": "",
            }
            commit["renewal_escalation_store_commit_digest"] = store_commit_digest(
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
                if snapshot.get("renewal_escalation_state_digest") != state.get(
                    "renewal_escalation_state_digest"
                ):
                    raise RenewalEscalationStoreError(
                        "escalation_snapshot_ledger_mismatch"
                    )
            return deepcopy(state)

    def repair_snapshot(self) -> dict[str, Any]:
        with self._locked():
            state, _ = self._recover_unlocked()
            self._write_atomic(self.snapshot_path, state)
            return deepcopy(state)
