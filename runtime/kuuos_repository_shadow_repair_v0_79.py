#!/usr/bin/env python3
from __future__ import annotations

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_repository_structure_observer_v0_79 import observe_repository_structure
from runtime.kuuos_repository_structure_types_v0_79 import (
    RepositoryObservation,
    RepositoryRepairCandidate,
    RepositoryShadowAssessment,
    RepositorySnapshot,
)

EvaluatedCandidate = tuple[
    RepositorySnapshot,
    RepositoryObservation,
    RepositoryRepairCandidate,
    RepositoryShadowAssessment,
]


def apply_candidate_to_snapshot(
    snapshot: RepositorySnapshot,
    candidate: RepositoryRepairCandidate,
) -> RepositorySnapshot:
    if candidate.source_snapshot_digest != snapshot.digest:
        raise ValueError("candidate_snapshot_binding_mismatch")
    if not candidate.protected_paths_preserved:
        raise ValueError("candidate_protected_path_violation")
    texts = snapshot.texts
    for patch in candidate.patches:
        current = texts.get(patch.path)
        if current is None:
            raise ValueError(f"candidate_target_missing:{patch.path}")
        if canonical_digest(current) != patch.before_digest:
            raise ValueError(f"candidate_before_digest_mismatch:{patch.path}")
        texts[patch.path] = patch.after_text
    return RepositorySnapshot(
        snapshot.root_label,
        snapshot.all_paths,
        tuple(sorted(texts.items())),
    )


def compare_repository_candidate_in_shadow(
    snapshot: RepositorySnapshot,
    observation: RepositoryObservation,
    candidate: RepositoryRepairCandidate,
) -> tuple[RepositorySnapshot, RepositoryObservation, RepositoryShadowAssessment]:
    if observation.snapshot_digest != snapshot.digest:
        raise ValueError("source_observation_snapshot_mismatch")
    if candidate.source_observation_digest != observation.digest:
        raise ValueError("candidate_observation_binding_mismatch")
    shadow = apply_candidate_to_snapshot(snapshot, candidate)
    shadow_observation = observe_repository_structure(shadow)
    nonworsening = (
        shadow_observation.weighted_defect_score
        <= observation.weighted_defect_score
    )
    strict_improvement = (
        shadow_observation.weighted_defect_score
        < observation.weighted_defect_score
    )
    assessment = RepositoryShadowAssessment(
        candidate.digest,
        shadow.digest,
        shadow_observation.digest,
        observation.weighted_defect_score,
        shadow_observation.weighted_defect_score,
        nonworsening,
        strict_improvement,
        candidate.protected_paths_preserved,
        nonworsening and strict_improvement and candidate.protected_paths_preserved,
    )
    return shadow, shadow_observation, assessment


def evaluate_repository_candidates(
    snapshot: RepositorySnapshot,
    observation: RepositoryObservation,
    candidates: tuple[RepositoryRepairCandidate, ...],
) -> tuple[EvaluatedCandidate, ...]:
    evaluated: list[EvaluatedCandidate] = []
    for candidate in candidates:
        shadow, shadow_observation, assessment = compare_repository_candidate_in_shadow(
            snapshot,
            observation,
            candidate,
        )
        evaluated.append((shadow, shadow_observation, candidate, assessment))
    return tuple(evaluated)


def select_repository_candidate(
    evaluated: tuple[EvaluatedCandidate, ...],
) -> EvaluatedCandidate | None:
    admissible = [entry for entry in evaluated if entry[3].admissible]
    if not admissible:
        return None
    return min(
        admissible,
        key=lambda entry: (
            entry[3].candidate_score,
            len(entry[2].patches),
            entry[2].digest,
        ),
    )
