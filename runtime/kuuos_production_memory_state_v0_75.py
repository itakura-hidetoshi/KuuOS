#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_nonmarkov_memory_connection_v0_72 import NonMarkovMemoryConnection
from runtime.kuuos_nonmarkov_memory_kernel_v0_72 import FiniteMemoryKernel

VERSION = "kuuos_production_memory_state_v0_75"


@dataclass(frozen=True)
class ProductionMemoryState:
    state_id: str
    revision: int
    history_digest: str
    module_digest: str
    current_kernel: FiniteMemoryKernel
    current_connection: NonMarkovMemoryConnection
    consumed_review_receipts: tuple[str, ...] = ()
    previous_state_digest: str = ""
    version: str = VERSION

    def __post_init__(self) -> None:
        if not self.state_id:
            raise ValueError("production_memory_state_id_missing")
        if self.revision < 0:
            raise ValueError("production_memory_revision_invalid")
        if not self.history_digest or not self.module_digest:
            raise ValueError("production_memory_binding_missing")
        if self.current_kernel.source_history_digest != self.history_digest:
            raise ValueError("production_memory_history_binding_mismatch")
        if self.current_kernel.source_module_digest != self.module_digest:
            raise ValueError("production_memory_module_binding_mismatch")
        if self.current_connection.memory_kernel.digest != self.current_kernel.digest:
            raise ValueError("production_memory_connection_kernel_mismatch")
        if (
            self.current_connection.base_connection.module_connection.source_module_digest
            != self.module_digest
        ):
            raise ValueError("production_memory_base_module_binding_mismatch")
        if len(set(self.consumed_review_receipts)) != len(self.consumed_review_receipts):
            raise ValueError("production_memory_consumption_duplicate")

    def to_dict(self) -> dict[str, Any]:
        return {
            "state_id": self.state_id,
            "revision": self.revision,
            "history_digest": self.history_digest,
            "module_digest": self.module_digest,
            "current_kernel": self.current_kernel.to_dict(),
            "current_connection": self.current_connection.to_dict(),
            "consumed_review_receipts": list(self.consumed_review_receipts),
            "previous_state_digest": self.previous_state_digest,
            "version": self.version,
        }

    @property
    def digest(self) -> str:
        return canonical_digest(self.to_dict())
