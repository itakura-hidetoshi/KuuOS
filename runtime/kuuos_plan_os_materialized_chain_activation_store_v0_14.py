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
from runtime.kuuos_plan_os_materialized_chain_activation_types_v0_14 import (
    STORE_COMMIT_VERSION,
    require_int,
    store_commit_digest,
)
from runtime.kuuos_plan_os_rerotation_materialization_kernel_v0_13 import (
    validate_rerotation_materialization_receipt,
)


class MaterializedChainActivationStoreError(RuntimeError):
    pass


class MaterializedChainActivationStore:
    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.genesis_path = self.root / "activation-genesis.json"
        self.ledger_path = self.root / "activation-ledger.jsonl"
        self.snapshot_path = self.root / "activation-snapshot.json"
        self.lock_path = self.root / ".plan-os-v014-activation.lock"

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
            raise MaterializedChainActivationStoreError(
                f"activation_json_read_failed:{path.name}"
            ) from exc
        if not isinstance(value, dict):
            raise MaterializedChainActivationStoreError(
                f"activation_json_object_required:{path.name}"
            )
        return value

    def initialize(
        self, materialization_receipt: Mapping[str, Any]
    ) -> dict[str, Any]:
        errors = validate_rerotation_materialization_receipt(
            materialization_receipt
        )
        if errors:
            raise MaterializedChainActivationStoreError(
                "activation_genesis_invalid:" + ";".join(errors)
            )
        with self._locked():
            if self.genesis_path.exists() or self.ledger_path.exists():
                raise MaterializedChainActivationStoreError(
                    "activation_store_already_initialized"
                )
            self._write_atomic(self.genesis_path, dict(materialization_receipt))
            self.ledger_path.touch(exist_ok=False)
            self._write_atomic(self.snapshot_path, dict(materialization_receipt))
        return deepcopy(dict(materialization_receipt))

    def _read_commits(self) -> list[dict[str, Any]]:
        commits: list[dict[str, Any]] = []
        try:
            for line_number, raw in enumerate(
                self.ledger_path.read_text(encoding="utf-8").splitlines(),
                start=1,
            ):
                if not raw.strip():
                    raise MaterializedChainActivationStoreError(
                        f"activation_ledger_blank_line:{line_number}"
                    )
                value = json.loads(raw)
                if not isinstance(value, dict):
                    raise MaterializedChainActivationStoreError(
                        f"activation_ledger_object_required:{line_number}"
                    )
                commits.append(value)
        except (OSError, json.JSONDecodeError) as exc:
            raise MaterializedChainActivationStoreError(
                "activation_ledger_read_failed"
            ) from exc
        return commits

    def _recover_unlocked(self) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        if not self.genesis_path.exists() or not self.ledger_path.exists():
            raise MaterializedChainActivationStoreError(
                "activation_store_not_initialized"
            )
        genesis = self._read_json(self.genesis_path)
        if validate_rerotation_materialization_receipt(genesis):
            raise MaterializedChainActivationStoreError(
                "activation_genesis_invalid"
            )
        commits = self._read_commits()
        if len(commits) > 1:
            raise MaterializedChainActivationStoreError(
                "activation_multiple_commits_forbidden"
            )
        if not commits:
            return genesis, commits
        commit = commits[0]
        if commit.get("version") != STORE_COMMIT_VERSION:
            raise MaterializedChainActivationStoreError(
                "activation_commit_version_invalid"
            )
        if commit.get(
            "materialized_chain_activation_store_commit_digest"
        ) != store_commit_digest(commit):
            raise MaterializedChainActivationStoreError(
                "activation_commit_digest_invalid"
            )
        if commit.get("source_materialization_receipt_digest") != genesis.get(
            "rerotation_materialization_receipt_digest"
        ):
            raise MaterializedChainActivationStoreError(
                "activation_source_chain_broken"
            )
        receipt = dict(commit.get("receipt", {}))
        if validate_materialized_chain_activation_receipt(receipt):
            raise MaterializedChainActivationStoreError(
                "activation_recovery_receipt_invalid"
            )
        return receipt, commits

    def commit(
        self, *, receipt: Mapping[str, Any], now_ms: int
    ) -> dict[str, Any]:
        with self._locked():
            current, commits = self._recover_unlocked()
            receipt_id = str(
                receipt.get(
                    "materialized_chain_activation_receipt_digest", ""
                )
            )
            if commits:
                existing_id = str(
                    current.get(
                        "materialized_chain_activation_receipt_digest", ""
                    )
                )
                if receipt_id == existing_id:
                    return {
                        "status": "REPLAYED",
                        "receipt": deepcopy(current),
                        "errors": [],
                    }
                return {
                    "status": "REJECTED",
                    "receipt": deepcopy(current),
                    "errors": ["activation_already_committed"],
                }
            errors = validate_materialized_chain_activation_receipt(receipt)
            if errors:
                return {
                    "status": "REJECTED",
                    "receipt": deepcopy(dict(receipt)),
                    "errors": errors,
                }
            if receipt.get("materialization_receipt_digest") != current.get(
                "rerotation_materialization_receipt_digest"
            ):
                return {
                    "status": "REJECTED",
                    "receipt": deepcopy(dict(receipt)),
                    "errors": ["activation_source_materialization_mismatch"],
                }
            commit = {
                "version": STORE_COMMIT_VERSION,
                "source_materialization_receipt_digest": current[
                    "rerotation_materialization_receipt_digest"
                ],
                "receipt": deepcopy(dict(receipt)),
                "committed_at_ms": require_int(now_ms, "now_ms"),
                "materialized_chain_activation_store_commit_digest": "",
            }
            commit[
                "materialized_chain_activation_store_commit_digest"
            ] = store_commit_digest(commit)
            with self.ledger_path.open("a", encoding="utf-8") as handle:
                handle.write(canonical_json(commit) + "\n")
                handle.flush()
                os.fsync(handle.fileno())
            self._write_atomic(self.snapshot_path, dict(receipt))
            return {
                "status": "APPLIED",
                "receipt": deepcopy(dict(receipt)),
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
                if snapshot.get(
                    "materialized_chain_activation_receipt_digest"
                ) != current.get(
                    "materialized_chain_activation_receipt_digest"
                ):
                    raise MaterializedChainActivationStoreError(
                        "activation_snapshot_ledger_mismatch"
                    )
            return deepcopy(current)

    def repair_snapshot(self) -> dict[str, Any]:
        with self._locked():
            current, _ = self._recover_unlocked()
            self._write_atomic(self.snapshot_path, current)
            return deepcopy(current)
