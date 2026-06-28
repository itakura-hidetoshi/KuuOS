#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
from typing import Iterable

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_self_organization_types_v0_78 import (
    ADOPTED,
    NO_CHANGE,
    ROLLED_BACK,
    FiniteStructureCandidate,
    ObservationContext,
    ObservationSnapshot,
    SelfOrganizationCycleReceipt,
    SelfOrganizationPolicy,
    ShadowAssessment,
    StructuralDiagnosis,
    StructureState,
    cycle_receipt_digest,
)


def _pairs(values: dict[str, float]) -> tuple[tuple[str, float], ...]:
    return tuple(sorted((name, float(value)) for name, value in values.items()))


def observe_structure(
    state: StructureState,
    context: ObservationContext,
) -> ObservationSnapshot:
    values = state.values
    targets = context.target_map
    weights = context.weight_map
    if tuple(sorted(values)) != tuple(sorted(targets)):
        raise ValueError("observation_state_context_domain_mismatch")
    score = sum(
        weights[name] * (values[name] - targets[name]) ** 2
        for name in sorted(values)
    )
    return ObservationSnapshot(
        context.context_id,
        context.digest,
        state.digest,
        state.revision,
        state.coordinates,
        float(score),
    )


def diagnose_structure(
    state: StructureState,
    observation: ObservationSnapshot,
    context: ObservationContext,
) -> StructuralDiagnosis:
    if observation.state_digest != state.digest:
        raise ValueError("diagnosis_observation_state_mismatch")
    if observation.context_digest != context.digest:
        raise ValueError("diagnosis_observation_context_mismatch")
    values = state.values
    targets = context.target_map
    weights = context.weight_map
    pressure_map = {
        name: weights[name] * (targets[name] - values[name])
        for name in sorted(values)
    }
    mutable = [
        (name, pressure)
        for name, pressure in pressure_map.items()
        if name not in state.protected_coordinates
    ]
    mutable.sort(key=lambda item: (-abs(item[1]), item[0]))
    protected_pressure_detected = any(
        abs(pressure_map[name]) > 0.0
        for name in state.protected_coordinates
    )
    return StructuralDiagnosis(
        observation.digest,
        _pairs(pressure_map),
        tuple(mutable),
        protected_pressure_detected,
    )


def generate_finite_candidates(
    state: StructureState,
    diagnosis: StructuralDiagnosis,
    policy: SelfOrganizationPolicy,
) -> tuple[FiniteStructureCandidate, ...]:
    pressure_by_name = dict(diagnosis.mutable_pressures)
    ranked_names = tuple(name for name, _ in diagnosis.mutable_pressures)
    raw_changes: list[tuple[tuple[str, float], ...]] = []

    for name in ranked_names:
        for step in policy.step_fractions:
            delta = pressure_by_name[name] * step
            if abs(delta) > policy.tolerance:
                raw_changes.append(((name, float(delta)),))

    if policy.max_changed_coordinates >= 2 and len(ranked_names) >= 2:
        pair_names = tuple(sorted(ranked_names[:2]))
        for step in policy.step_fractions:
            changes = tuple(
                (name, float(pressure_by_name[name] * step))
                for name in pair_names
                if abs(pressure_by_name[name] * step) > policy.tolerance
            )
            if len(changes) == 2:
                raw_changes.append(changes)

    unique: dict[str, tuple[tuple[str, float], ...]] = {}
    for changes in raw_changes:
        canonical_changes = tuple(sorted(changes))
        unique.setdefault(canonical_digest(canonical_changes), canonical_changes)

    candidates: list[FiniteStructureCandidate] = []
    for index, (_, changes) in enumerate(sorted(unique.items())):
        if len(candidates) >= policy.max_candidates:
            break
        if len(changes) > policy.max_changed_coordinates:
            continue
        if any(name in state.protected_coordinates for name, _ in changes):
            continue
        candidates.append(FiniteStructureCandidate(
            f"finite-candidate-{index:02d}",
            state.digest,
            changes,
            diagnosis.digest,
        ))
    return tuple(candidates)


def materialize_candidate_state(
    source: StructureState,
    candidate: FiniteStructureCandidate,
    policy: SelfOrganizationPolicy,
) -> StructureState:
    if candidate.source_state_digest != source.digest:
        raise ValueError("candidate_source_binding_mismatch")
    if len(candidate.changes) > policy.max_changed_coordinates:
        raise ValueError("candidate_change_budget_exceeded")
    values = source.values
    for name, delta in candidate.changes:
        if name not in values:
            raise ValueError("candidate_coordinate_missing")
        if name in source.protected_coordinates:
            raise ValueError("candidate_protected_coordinate_change")
        values[name] = values[name] + float(delta)
    return StructureState(
        source.revision + 1,
        _pairs(values),
        source.protected_coordinates,
        source.lineage + (source.digest,),
    )


def compare_candidate_in_shadow(
    source: StructureState,
    candidate: FiniteStructureCandidate,
    contexts: tuple[ObservationContext, ...],
    policy: SelfOrganizationPolicy,
) -> tuple[StructureState, ShadowAssessment]:
    if not contexts:
        raise ValueError("shadow_contexts_empty")
    candidate_state = materialize_candidate_state(source, candidate, policy)
    source_scores: list[float] = []
    candidate_scores: list[float] = []
    deltas: list[float] = []
    for context in contexts:
        source_score = observe_structure(source, context).score
        candidate_score = observe_structure(candidate_state, context).score
        source_scores.append(source_score)
        candidate_scores.append(candidate_score)
        deltas.append(candidate_score - source_score)

    protected_preserved = all(
        source.values[name] == candidate_state.values[name]
        for name in source.protected_coordinates
    )
    nonworsening = all(delta <= policy.tolerance for delta in deltas)
    strict_improvement = any(delta < -policy.tolerance for delta in deltas)
    admissible = (
        protected_preserved
        and (nonworsening or not policy.require_shadow_nonworsening)
        and (strict_improvement or not policy.require_strict_shadow_improvement)
    )
    assessment = ShadowAssessment(
        candidate.digest,
        candidate_state.digest,
        float(sum(source_scores)),
        float(sum(candidate_scores)),
        float(max(deltas)),
        nonworsening,
        strict_improvement,
        protected_preserved,
        admissible,
    )
    return candidate_state, assessment


def evaluate_finite_candidates(
    source: StructureState,
    candidates: Iterable[FiniteStructureCandidate],
    contexts: tuple[ObservationContext, ...],
    policy: SelfOrganizationPolicy,
) -> tuple[tuple[StructureState, FiniteStructureCandidate, ShadowAssessment], ...]:
    evaluated: list[tuple[StructureState, FiniteStructureCandidate, ShadowAssessment]] = []
    for candidate in candidates:
        candidate_state, assessment = compare_candidate_in_shadow(
            source,
            candidate,
            contexts,
            policy,
        )
        evaluated.append((candidate_state, candidate, assessment))
    return tuple(evaluated)


def select_internal_candidate(
    evaluated: tuple[tuple[StructureState, FiniteStructureCandidate, ShadowAssessment], ...],
) -> tuple[StructureState, FiniteStructureCandidate, ShadowAssessment] | None:
    admissible = [entry for entry in evaluated if entry[2].admissible]
    if not admissible:
        return None
    return min(
        admissible,
        key=lambda entry: (
            entry[2].aggregate_candidate_score,
            len(entry[1].changes),
            entry[1].digest,
        ),
    )


def run_self_organization_cycle(
    cycle_id: str,
    source: StructureState,
    observation_context: ObservationContext,
    shadow_contexts: tuple[ObservationContext, ...],
    reobservation_context: ObservationContext,
    policy: SelfOrganizationPolicy,
) -> tuple[StructureState, SelfOrganizationCycleReceipt]:
    if not cycle_id:
        raise ValueError("cycle_id_missing")

    initial_observation = observe_structure(source, observation_context)
    diagnosis = diagnose_structure(source, initial_observation, observation_context)
    candidates = generate_finite_candidates(source, diagnosis, policy)
    evaluated = evaluate_finite_candidates(source, candidates, shadow_contexts, policy)
    selected = select_internal_candidate(evaluated)

    selected_candidate_digest = ""
    provisional_state_digest = source.digest
    reobservation_digest = ""
    rollback_performed = False
    source_restored = False

    if selected is None:
        final_state = source
        status = NO_CHANGE
    else:
        provisional_state, selected_candidate, _ = selected
        selected_candidate_digest = selected_candidate.digest
        provisional_state_digest = provisional_state.digest
        source_reobservation = observe_structure(source, reobservation_context)
        candidate_reobservation = observe_structure(
            provisional_state,
            reobservation_context,
        )
        reobservation_digest = canonical_digest({
            "source": source_reobservation.to_dict(),
            "candidate": candidate_reobservation.to_dict(),
        })
        protected_preserved = all(
            source.values[name] == provisional_state.values[name]
            for name in source.protected_coordinates
        )
        reobservation_nonworsening = (
            candidate_reobservation.score
            <= source_reobservation.score + policy.tolerance
        )
        retain = (
            protected_preserved
            and (
                reobservation_nonworsening
                or not policy.require_reobservation_nonworsening
            )
        )
        if retain:
            final_state = provisional_state
            status = ADOPTED
        else:
            final_state = source
            status = ROLLED_BACK
            rollback_performed = True
            source_restored = True

    receipt = SelfOrganizationCycleReceipt(
        cycle_id,
        status,
        source.digest,
        source.revision,
        initial_observation.digest,
        diagnosis.digest,
        tuple(candidate.digest for candidate in candidates),
        tuple(assessment.digest for _, _, assessment in evaluated),
        selected_candidate_digest,
        provisional_state_digest,
        final_state.digest,
        final_state.revision,
        reobservation_digest,
        rollback_performed,
        source_restored,
        True,
        False,
        False,
        False,
        "",
    )
    return final_state, replace(
        receipt,
        receipt_digest=cycle_receipt_digest(receipt),
    )
