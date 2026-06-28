#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_memory_rollback_v0_76"


@dataclass(frozen=True)
class MemoryRollbackLedger:
    ledger_id: str
    revision: int
    rolled_back_commit_receipts: tuple[str, ...] = ()
    previous_ledger_digest: str = ""
    version: str = VERSION

    def __post_init__(self) -> None:
        if not self.ledger_id:
            raise ValueError("memory_rollback_ledger_id_missing")
        if self.revision < 0:
            raise ValueError("memory_rollback_ledger_revision_invalid")
        if len(set(self.rolled_back_commit_receipts)) != len(
            self.rolled_back_commit_receipts
        ):
            raise ValueError("memory_rollback_ledger_duplicate_commit")

    def to_dict(self) -> dict[str, Any]:
        return {
            "ledger_id": self.ledger_id,
            "revision": self.revision,
            "rolled_back_commit_receipts": list(self.rolled_back_commit_receipts),
            "previous_ledger_digest": self.previous_ledger_digest,
            "version": self.version,
        }

    @property
    def digest(self) -> str:
        return canonical_digest(self.to_dict())
