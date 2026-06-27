#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_leibniz_module_connection_v0_71 import (
    FreeLeftModuleSection,
    section_left_action,
)
from runtime.kuuos_module_connection_v0_70 import Matrix

VERSION = "kuuos_read_only_memory_history_v0_72"


@dataclass(frozen=True)
class MemoryHistoryFrame:
    epoch: int
    section: FreeLeftModuleSection
    source_capsule_digest: str

    def __post_init__(self) -> None:
        if self.epoch < 0:
            raise ValueError("memory_history_epoch_invalid")
        if not self.source_capsule_digest:
            raise ValueError("memory_history_source_capsule_digest_missing")

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["section"] = self.section.to_dict()
        return payload


@dataclass(frozen=True)
class ReadOnlyMemoryHistory:
    history_id: str
    source_capsule_digest: str
    frames: tuple[MemoryHistoryFrame, ...]
    version: str = VERSION

    def __post_init__(self) -> None:
        if not self.history_id:
            raise ValueError("memory_history_id_missing")
        if not self.source_capsule_digest:
            raise ValueError("memory_history_capsule_digest_missing")
        if not self.frames:
            raise ValueError("memory_history_frames_empty")
        epochs = tuple(frame.epoch for frame in self.frames)
        if epochs != tuple(sorted(epochs)) or len(set(epochs)) != len(epochs):
            raise ValueError("memory_history_epochs_not_strict")
        first = self.frames[0].section
        for frame in self.frames:
            if frame.source_capsule_digest != self.source_capsule_digest:
                raise ValueError("memory_history_frame_capsule_binding_mismatch")
            if frame.section.context_dimension != first.context_dimension:
                raise ValueError("memory_history_context_dimension_mismatch")
            if frame.section.module_rank != first.module_rank:
                raise ValueError("memory_history_module_rank_mismatch")

    def to_dict(self) -> dict[str, Any]:
        return {
            "history_id": self.history_id,
            "source_capsule_digest": self.source_capsule_digest,
            "frames": [frame.to_dict() for frame in self.frames],
            "version": self.version,
        }

    @property
    def digest(self) -> str:
        return canonical_digest(self.to_dict())

    @property
    def context_dimension(self) -> int:
        return self.frames[0].section.context_dimension

    @property
    def module_rank(self) -> int:
        return self.frames[0].section.module_rank

    def frame_at(self, epoch: int) -> MemoryHistoryFrame | None:
        for frame in self.frames:
            if frame.epoch == epoch:
                return frame
        return None

    def acted_sections(self, algebra_element: Matrix) -> tuple[MemoryHistoryFrame, ...]:
        return tuple(
            MemoryHistoryFrame(
                frame.epoch,
                section_left_action(algebra_element, frame.section),
                frame.source_capsule_digest,
            )
            for frame in self.frames
        )
