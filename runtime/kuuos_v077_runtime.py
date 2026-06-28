#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_v077_types import (
    MemoryVerificationRecord,
    verification_record_digest,
)


def seal_verification_record(
    record: MemoryVerificationRecord,
) -> MemoryVerificationRecord:
    return replace(record, record_digest=verification_record_digest(record))
