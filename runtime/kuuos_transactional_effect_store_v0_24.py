from __future__ import annotations

import json
import os
from copy import deepcopy
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, Mapping

from runtime.kuuos_transactional_effect_reconciliation_kernel_v0_24 import (
    apply_transaction_event,
    validate_transaction_state,
)


class TransactionStoreError(ValueError):
    pass


class TransactionStore:
    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.initial_path = self.root / "transaction-initial.json"
        self.snapshot_path = self.root / "transaction-snapshot.json"
        self.ledger_path = self.root / "transaction-ledger.jsonl"

    @staticmethod
    def _write_json_atomic(path: Path, value: Mapping[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with NamedTemporaryFile(
            "w", encoding="utf-8", dir=path.parent, delete=False
        ) as handle:
            json.dump(value, handle, ensure_ascii=False, sort_keys=True, indent=2)
            handle.write("\n")
            temporary = Path(handle.name)
        os.replace(temporary, path)

    @staticmethod
    def _read_json(path: Path) -> dict[str, Any]:
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise TransactionStoreError(f"transaction_json_invalid:{path.name}") from exc
        if not isinstance(value, dict):
            raise TransactionStoreError(f"transaction_json_root_invalid:{path.name}")
        return value

    def initialize(self, initial_state: Mapping[str, Any]) -> dict[str, Any]:
        errors = validate_transaction_state(initial_state)
        if errors:
            raise TransactionStoreError(
                "transaction_initial_state_invalid:" + ";".join(errors)
            )
        self.root.mkdir(parents=True, exist_ok=True)
        if any(
            path.exists()
            for path in (self.initial_path, self.snapshot_path, self.ledger_path)
        ):
            raise TransactionStoreError("transaction_store_already_initialized")
        state = deepcopy(dict(initial_state))
        self._write_json_atomic(self.initial_path, state)
        self._write_json_atomic(self.snapshot_path, state)
        self.ledger_path.write_text("", encoding="utf-8")
        return deepcopy(state)

    def ledger_commit_count(self) -> int:
        if not self.ledger_path.exists():
            return 0
        return sum(
            1
            for line in self.ledger_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        )

    def recover(self, *, require_snapshot_match: bool = True) -> dict[str, Any]:
        if not self.initial_path.exists() or not self.ledger_path.exists():
            raise TransactionStoreError("transaction_store_not_initialized")
        state = self._read_json(self.initial_path)
        errors = validate_transaction_state(state)
        if errors:
            raise TransactionStoreError(
                "transaction_initial_state_invalid:" + ";".join(errors)
            )
        for line_number, line in enumerate(
            self.ledger_path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            if not line.strip():
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError as exc:
                raise TransactionStoreError(
                    f"transaction_ledger_json_invalid:{line_number}"
                ) from exc
            if not isinstance(event, dict):
                raise TransactionStoreError(
                    f"transaction_ledger_event_invalid:{line_number}"
                )
            result = apply_transaction_event(state, event)
            if result.get("status") != "APPLIED":
                raise TransactionStoreError(
                    f"transaction_ledger_replay_rejected:{line_number}:"
                    + ";".join(result.get("errors", []))
                )
            state = result["state"]
        if self.snapshot_path.exists():
            snapshot = self._read_json(self.snapshot_path)
            if require_snapshot_match and snapshot != state:
                raise TransactionStoreError("transaction_snapshot_ledger_mismatch")
        elif require_snapshot_match:
            raise TransactionStoreError("transaction_snapshot_missing")
        return deepcopy(state)

    def repair_snapshot(self) -> dict[str, Any]:
        state = self.recover(require_snapshot_match=False)
        self._write_json_atomic(self.snapshot_path, state)
        return deepcopy(state)

    def apply(self, event: Mapping[str, Any]) -> dict[str, Any]:
        state = self.recover(require_snapshot_match=True)
        result = apply_transaction_event(state, event)
        if result.get("status") != "APPLIED":
            return deepcopy(result)
        with self.ledger_path.open("a", encoding="utf-8") as handle:
            handle.write(
                json.dumps(
                    dict(event),
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                )
                + "\n"
            )
            handle.flush()
            os.fsync(handle.fileno())
        self._write_json_atomic(self.snapshot_path, result["state"])
        return deepcopy(result)


__all__ = ["TransactionStore", "TransactionStoreError"]
