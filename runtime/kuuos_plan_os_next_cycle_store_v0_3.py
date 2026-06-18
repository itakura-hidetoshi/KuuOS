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
from runtime.kuuos_plan_os_next_cycle_types_v0_3 import (
    COMPILER_RECEIPT_VERSION,
    NON_AUTHORITY_FLAGS,
    STORE_COMMIT_VERSION,
    STORE_STATE_VERSION,
    adapter_store_commit_digest,
    adapter_store_state_digest,
    copy_non_authority,
    next_cycle_compiler_receipt_digest,
)


class NextCycleAdapterStoreError(RuntimeError):
    pass


def build_initial_adapter_store_state(*, adapter_id: str, now_ms: int) -> dict[str, Any]:
    if not isinstance(adapter_id, str) or not adapter_id.strip():
        raise ValueError("adapter_id_required")
    if isinstance(now_ms, bool) or not isinstance(now_ms, int) or now_ms < 0:
        raise ValueError("now_ms_nonnegative_int_required")
    state = {
        "version": STORE_STATE_VERSION,
        "adapter_id": adapter_id,
        "committed_records": 0,
        "updated_at_ms": now_ms,
        "consumed_replan_receipt_digests": [],
        "consumed_next_plan_basis_digests": [],
        "compiler_receipt_digests": [],
        "records": [],
        "non_authority": copy_non_authority(),
        "adapter_store_state_digest": "",
    }
    state["adapter_store_state_digest"] = adapter_store_state_digest(state)
    return state


def validate_adapter_store_state(state: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if state.get("version") != STORE_STATE_VERSION:
        errors.append("adapter_store_state_version_invalid")
    if not isinstance(state.get("adapter_id"), str) or not state.get("adapter_id"):
        errors.append("adapter_store_id_invalid")
    committed = state.get("committed_records")
    if isinstance(committed, bool) or not isinstance(committed, int) or committed < 0:
        errors.append("adapter_store_committed_records_invalid")
    if dict(state.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
        errors.append("adapter_store_authority_escalation")
    for field in (
        "consumed_replan_receipt_digests",
        "consumed_next_plan_basis_digests",
        "compiler_receipt_digests",
        "records",
    ):
        if not isinstance(state.get(field), list):
            errors.append(f"adapter_store_{field}_invalid")
    if len(state.get("records", [])) != committed:
        errors.append("adapter_store_record_count_mismatch")
    for field in (
        "consumed_replan_receipt_digests",
        "consumed_next_plan_basis_digests",
        "compiler_receipt_digests",
    ):
        values = list(state.get(field, []))
        if len(values) != len(set(values)):
            errors.append(f"adapter_store_{field}_duplicate")
        if len(values) != committed:
            errors.append(f"adapter_store_{field}_count_mismatch")
    if state.get("adapter_store_state_digest") != adapter_store_state_digest(state):
        errors.append("adapter_store_state_digest_invalid")
    return errors


class NextCycleAdapterStore:
    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.genesis_path = self.root / "next-cycle-adapter-genesis.json"
        self.ledger_path = self.root / "next-cycle-adapter-ledger.jsonl"
        self.snapshot_path = self.root / "next-cycle-adapter-snapshot.json"
        self.lock_path = self.root / ".plan-os-v03-adapter.lock"

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
            raise NextCycleAdapterStoreError(
                f"adapter_json_read_failed:{path.name}"
            ) from exc
        if not isinstance(value, dict):
            raise NextCycleAdapterStoreError(f"adapter_json_object_required:{path.name}")
        return value

    def initialize(self, state: Mapping[str, Any]) -> dict[str, Any]:
        errors = validate_adapter_store_state(state)
        if errors:
            raise NextCycleAdapterStoreError("adapter_initial_state_invalid:" + ";".join(errors))
        with self._locked():
            if self.genesis_path.exists() or self.ledger_path.exists():
                raise NextCycleAdapterStoreError("adapter_store_already_initialized")
            self._write_atomic(self.genesis_path, dict(state))
            self.ledger_path.touch(exist_ok=False)
            with self.ledger_path.open("a", encoding="utf-8") as handle:
                handle.flush()
                os.fsync(handle.fileno())
            self._write_atomic(self.snapshot_path, dict(state))
        return deepcopy(dict(state))

    def _read_ledger(self) -> list[dict[str, Any]]:
        commits: list[dict[str, Any]] = []
        try:
            with self.ledger_path.open("r", encoding="utf-8") as handle:
                for line_number, raw in enumerate(handle, start=1):
                    line = raw.strip()
                    if not line:
                        raise NextCycleAdapterStoreError(
                            f"adapter_ledger_blank_line:{line_number}"
                        )
                    item = json.loads(line)
                    if not isinstance(item, dict):
                        raise NextCycleAdapterStoreError(
                            f"adapter_ledger_object_required:{line_number}"
                        )
                    commits.append(item)
        except (OSError, json.JSONDecodeError) as exc:
            raise NextCycleAdapterStoreError("adapter_ledger_read_failed") from exc
        return commits

    def _recover_unlocked(self) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        if not self.genesis_path.exists() or not self.ledger_path.exists():
            raise NextCycleAdapterStoreError("adapter_store_not_initialized")
        state = self._read_json(self.genesis_path)
        errors = validate_adapter_store_state(state)
        if errors:
            raise NextCycleAdapterStoreError("adapter_genesis_invalid:" + ";".join(errors))
        commits = self._read_ledger()
        previous_commit_digest = ""
        for index, commit in enumerate(commits, start=1):
            if commit.get("version") != STORE_COMMIT_VERSION:
                raise NextCycleAdapterStoreError(f"adapter_commit_version_invalid:{index}")
            if commit.get("adapter_store_commit_digest") != adapter_store_commit_digest(commit):
                raise NextCycleAdapterStoreError(f"adapter_commit_digest_invalid:{index}")
            if commit.get("predecessor_commit_digest") != previous_commit_digest:
                raise NextCycleAdapterStoreError(f"adapter_commit_chain_broken:{index}")
            if commit.get("predecessor_state_digest") != state.get(
                "adapter_store_state_digest"
            ):
                raise NextCycleAdapterStoreError(f"adapter_state_chain_broken:{index}")
            receipt = commit.get("compiler_receipt")
            if not isinstance(receipt, dict):
                raise NextCycleAdapterStoreError(f"adapter_receipt_invalid:{index}")
            state = self._apply_to_state(state, receipt)
            if commit.get("result_state_digest") != state.get("adapter_store_state_digest"):
                raise NextCycleAdapterStoreError(f"adapter_result_digest_mismatch:{index}")
            previous_commit_digest = commit["adapter_store_commit_digest"]
        return state, commits

    @staticmethod
    def _validate_receipt(receipt: Mapping[str, Any]) -> None:
        if receipt.get("version") != COMPILER_RECEIPT_VERSION:
            raise NextCycleAdapterStoreError("adapter_compiler_receipt_version_invalid")
        if receipt.get("next_cycle_compiler_receipt_digest") != next_cycle_compiler_receipt_digest(
            receipt
        ):
            raise NextCycleAdapterStoreError("adapter_compiler_receipt_digest_invalid")
        required = {
            "single_use_activation": True,
            "plan_committed": True,
            "plan_not_execution": True,
            "host_license_granted": False,
            "memory_overwrite": False,
            "previous_plan_unchanged": True,
        }
        for field, expected in required.items():
            if receipt.get(field) != expected:
                raise NextCycleAdapterStoreError(f"adapter_receipt_{field}_invalid")
        if dict(receipt.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            raise NextCycleAdapterStoreError("adapter_receipt_authority_escalation")

    @classmethod
    def _apply_to_state(
        cls, state: Mapping[str, Any], receipt: Mapping[str, Any]
    ) -> dict[str, Any]:
        cls._validate_receipt(receipt)
        replan_receipt = str(receipt["replan_phase_receipt_digest"])
        basis = str(receipt["next_plan_basis_digest"])
        compiler_digest = str(receipt["next_cycle_compiler_receipt_digest"])
        if replan_receipt in set(state["consumed_replan_receipt_digests"]):
            raise NextCycleAdapterStoreError("adapter_replan_receipt_already_consumed")
        if basis in set(state["consumed_next_plan_basis_digests"]):
            raise NextCycleAdapterStoreError("adapter_next_plan_basis_already_consumed")
        if compiler_digest in set(state["compiler_receipt_digests"]):
            raise NextCycleAdapterStoreError("adapter_compiler_receipt_duplicate")
        next_state = deepcopy(dict(state))
        next_state["committed_records"] += 1
        next_state["updated_at_ms"] = int(receipt["issued_at_ms"])
        next_state["consumed_replan_receipt_digests"].append(replan_receipt)
        next_state["consumed_next_plan_basis_digests"].append(basis)
        next_state["compiler_receipt_digests"].append(compiler_digest)
        next_state["records"].append(
            {
                "replan_phase_receipt_digest": replan_receipt,
                "next_plan_activation_receipt_digest": receipt[
                    "next_plan_activation_receipt_digest"
                ],
                "next_plan_basis_digest": basis,
                "compiled_plan_state_digest": receipt["compiled_plan_state_digest"],
                "compiled_plan_basis_digest": receipt["compiled_plan_basis_digest"],
                "next_cycle_compiler_receipt_digest": compiler_digest,
            }
        )
        next_state["adapter_store_state_digest"] = ""
        next_state["adapter_store_state_digest"] = adapter_store_state_digest(next_state)
        errors = validate_adapter_store_state(next_state)
        if errors:
            raise NextCycleAdapterStoreError("adapter_next_state_invalid:" + ";".join(errors))
        return next_state

    def recover(self, *, require_snapshot_match: bool = True) -> dict[str, Any]:
        with self._locked():
            state, _ = self._recover_unlocked()
            if require_snapshot_match:
                snapshot = self._read_json(self.snapshot_path)
                if snapshot.get("adapter_store_state_digest") != state.get(
                    "adapter_store_state_digest"
                ):
                    raise NextCycleAdapterStoreError("adapter_snapshot_ledger_mismatch")
            return deepcopy(state)

    def commit(self, receipt: Mapping[str, Any]) -> dict[str, Any]:
        with self._locked():
            state, commits = self._recover_unlocked()
            digest = str(receipt.get("next_cycle_compiler_receipt_digest", ""))
            if digest and digest in set(state["compiler_receipt_digests"]):
                return {
                    "status": "REPLAYED",
                    "state": deepcopy(state),
                    "next_cycle_compiler_receipt_digest": digest,
                }
            next_state = self._apply_to_state(state, receipt)
            commit = {
                "version": STORE_COMMIT_VERSION,
                "commit_index": len(commits) + 1,
                "predecessor_commit_digest": commits[-1]["adapter_store_commit_digest"]
                if commits
                else "",
                "predecessor_state_digest": state["adapter_store_state_digest"],
                "result_state_digest": next_state["adapter_store_state_digest"],
                "compiler_receipt": deepcopy(dict(receipt)),
                "adapter_store_commit_digest": "",
            }
            commit["adapter_store_commit_digest"] = adapter_store_commit_digest(commit)
            with self.ledger_path.open("a", encoding="utf-8") as handle:
                handle.write(canonical_json(commit) + "\n")
                handle.flush()
                os.fsync(handle.fileno())
            self._write_atomic(self.snapshot_path, next_state)
            return {
                "status": "COMMITTED",
                "state": next_state,
                "next_cycle_compiler_receipt_digest": digest,
            }

    def repair_snapshot(self) -> dict[str, Any]:
        with self._locked():
            state, _ = self._recover_unlocked()
            self._write_atomic(self.snapshot_path, state)
            return deepcopy(state)

    def ledger_commit_count(self) -> int:
        with self._locked():
            _, commits = self._recover_unlocked()
            return len(commits)
