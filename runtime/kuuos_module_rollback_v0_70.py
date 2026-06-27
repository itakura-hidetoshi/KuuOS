#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from typing import Any

from runtime.kuuos_connection_deformation_v0_70 import ConnectionDeformation
from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_module_connection_v0_70 import ModuleConnection

VERSION = "kuuos_module_rollback_v0_70"


@dataclass(frozen=True)
class ModuleRollbackReceipt:
    source_connection_digest: str
    candidate_connection_digest: str
    deformation_digest: str
    recovered_connection_digest: str
    algebraic_exact: bool
    structural_exact: bool
    digest_exact: bool
    receipt_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def rollback_receipt_digest(receipt: ModuleRollbackReceipt) -> str:
    payload = receipt.to_dict()
    payload.pop("receipt_digest", None)
    return canonical_digest(payload)


def rollback_connection(
    source: ModuleConnection,
    candidate: ModuleConnection,
    deformation: ConnectionDeformation,
) -> tuple[ModuleConnection, ModuleRollbackReceipt]:
    if source.digest != deformation.source_connection_digest:
        raise ValueError("rollback_source_connection_mismatch")
    candidate.connection_form.require_same_space(deformation.alpha)
    recovered = ModuleConnection(
        candidate.connection_form.subtract(deformation.alpha),
        candidate.source_module_digest,
        candidate.gauge_group_digest,
    )
    algebraic_exact = recovered.connection_form == source.connection_form
    structural_exact = (
        recovered.source_module_digest == source.source_module_digest
        and recovered.gauge_group_digest == source.gauge_group_digest
        and recovered.connection_form.direction_labels == source.connection_form.direction_labels
        and recovered.connection_form.module_rank == source.connection_form.module_rank
    )
    digest_exact = recovered.digest == source.digest
    receipt = ModuleRollbackReceipt(
        source.digest,
        candidate.digest,
        deformation.digest,
        recovered.digest,
        algebraic_exact,
        structural_exact,
        digest_exact,
        "",
    )
    return recovered, replace(receipt, receipt_digest=rollback_receipt_digest(receipt))
