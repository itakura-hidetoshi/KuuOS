#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_nonmarkov_memory_kernel_v0_72 import MemoryKernelDeformation

VERSION = "kuuos_memory_family_v0_73"


@dataclass(frozen=True)
class MemoryFamilyMember:
    member_id: str
    deformation: MemoryKernelDeformation

    def __post_init__(self) -> None:
        if not self.member_id:
            raise ValueError("memory_family_member_id_missing")

    def to_dict(self) -> dict[str, Any]:
        return {
            "member_id": self.member_id,
            "deformation": self.deformation.to_dict(),
        }

    @property
    def digest(self) -> str:
        return canonical_digest(self.to_dict())


@dataclass(frozen=True)
class MemoryFamily:
    family_id: str
    source_kernel_digest: str
    members: tuple[MemoryFamilyMember, ...]
    version: str = VERSION

    def __post_init__(self) -> None:
        if not self.family_id:
            raise ValueError("memory_family_id_missing")
        if not self.source_kernel_digest:
            raise ValueError("memory_family_source_missing")
        if not self.members:
            raise ValueError("memory_family_empty")
        ids = tuple(member.member_id for member in self.members)
        if len(set(ids)) != len(ids):
            raise ValueError("memory_family_member_id_duplicate")
        for member in self.members:
            if member.deformation.source_kernel_digest != self.source_kernel_digest:
                raise ValueError("memory_family_source_mismatch")

    def to_dict(self) -> dict[str, Any]:
        return {
            "family_id": self.family_id,
            "source_kernel_digest": self.source_kernel_digest,
            "members": [member.to_dict() for member in self.members],
            "version": self.version,
        }

    @property
    def digest(self) -> str:
        return canonical_digest(self.to_dict())
