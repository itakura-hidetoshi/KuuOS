#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_repository_alignment_normal_form_v0_80"


@dataclass(frozen=True)
class AlignmentTransition:
    source_snapshot_digest: str
    target_snapshot_digest: str
    candidate_digest: str
    source_score: int
    target_score: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @property
    def digest(self) -> str:
        return canonical_digest(self.to_dict())


@dataclass(frozen=True)
class AlignmentTrace:
    initial_snapshot_digest: str
    final_snapshot_digest: str
    initial_score: int
    final_score: int
    transition_digests: tuple[str, ...]
    score_sequence: tuple[int, ...]
    fixed_point_reached: bool
    max_cycles: int
    trace_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def alignment_trace_digest(trace: AlignmentTrace) -> str:
    payload = trace.to_dict()
    payload.pop("trace_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class AlignmentNormalFormCertificate:
    initial_snapshot_digest: str
    initial_score: int
    explored_snapshot_digests: tuple[str, ...]
    transition_digests: tuple[str, ...]
    terminal_snapshot_digests: tuple[str, ...]
    terminal_scores: tuple[int, ...]
    explored_state_count: int
    explored_transition_count: int
    max_states: int
    all_transitions_strictly_decreasing: bool
    all_terminals_fixed_points: bool
    unique_terminal: bool
    unique_terminal_digest: str
    deterministic_trace_matches_terminal: bool
    external_approval_required: bool
    certificate_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def normal_form_certificate_digest(
    certificate: AlignmentNormalFormCertificate,
) -> str:
    payload = certificate.to_dict()
    payload.pop("certificate_digest", None)
    return canonical_digest(payload)
