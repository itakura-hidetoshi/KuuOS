#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_post_transition_verification_v0_77"
COMMIT_KIND = "COMMIT"
ROLLBACK_KIND = "ROLLBACK"
VERIFIED = "MEMORY_TRANSITION_VERIFIED"
BLOCKED = "MEMORY_TRANSITION_VERIFICATION_BLOCKED"


@dataclass(frozen=True)
class MemoryVerificationRecord:
    status: str
    transition_kind: str
    operation_receipt_digest: str
    commit_receipt_digest: str
    rollback_receipt_digest: str
    observed_state_digest: str
    observed_state_revision: int
    observed_kernel_digest: str
    observed_connection_digest: str
    observed_ledger_digest: str
    observed_ledger_revision: int
    exact_state_binding: bool
    exact_payload_binding: bool
    revision_successor: bool
    state_chain_preserved: bool
    authority_consumption_preserved: bool
    ledger_binding_preserved: bool
    record_only: bool
    writes_enabled: bool
    live_application_enabled: bool
    permission_expansion_enabled: bool
    issues: tuple[str, ...]
    record_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["issues"] = list(self.issues)
        return payload


def verification_record_digest(record: MemoryVerificationRecord) -> str:
    payload = record.to_dict()
    payload.pop("record_digest", None)
    return canonical_digest(payload)
