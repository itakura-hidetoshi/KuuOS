#!/usr/bin/env python3
from __future__ import annotations

from collections import deque
from dataclasses import replace

from runtime.kuuos_repository_alignment_normal_form_types_v0_80 import (
    AlignmentNormalFormCertificate,
    AlignmentTrace,
    AlignmentTransition,
    alignment_trace_digest,
    normal_form_certificate_digest,
)
from runtime.kuuos_repository_repair_candidates_v0_79 import (
    generate_repository_repair_candidates,
)
from runtime.kuuos_repository_shadow_repair_v0_79 import (
    evaluate_repository_candidates,
    select_repository_candidate,
)
from runtime.kuuos_repository_structure_observer_v0_79 import (
    observe_repository_structure,
)
from runtime.kuuos_repository_structure_types_v0_79 import RepositorySnapshot


def _evaluated_candidates(snapshot: RepositorySnapshot):
    observation = observe_repository_structure(snapshot)
    candidates = generate_repository_repair_candidates(snapshot, observation)
    evaluated = evaluate_repository_candidates(snapshot, observation, candidates)
    return observation, tuple(
        sorted(evaluated, key=lambda entry: entry[2].digest)
    )


def run_deterministic_alignment_trace(
    initial_snapshot: RepositorySnapshot,
    max_cycles: int = 256,
) -> tuple[RepositorySnapshot, AlignmentTrace]:
    if max_cycles <= 0:
        raise ValueError("max_cycles_invalid")

    snapshot = initial_snapshot
    initial_observation = observe_repository_structure(snapshot)
    score_sequence = [initial_observation.weighted_defect_score]
    transitions: list[AlignmentTransition] = []
    fixed_point = False

    for _ in range(max_cycles):
        observation, evaluated = _evaluated_candidates(snapshot)
        selected = select_repository_candidate(evaluated)
        if selected is None:
            fixed_point = True
            break
        target_snapshot, target_observation, candidate, assessment = selected
        transition = AlignmentTransition(
            snapshot.digest,
            target_snapshot.digest,
            candidate.digest,
            observation.weighted_defect_score,
            target_observation.weighted_defect_score,
        )
        if not assessment.admissible:
            raise ValueError("deterministic_selection_not_admissible")
        if transition.target_score >= transition.source_score:
            raise ValueError("deterministic_transition_not_strict")
        transitions.append(transition)
        snapshot = target_snapshot
        score_sequence.append(target_observation.weighted_defect_score)

    if not fixed_point:
        _, remaining = _evaluated_candidates(snapshot)
        fixed_point = select_repository_candidate(remaining) is None

    trace = AlignmentTrace(
        initial_snapshot.digest,
        snapshot.digest,
        initial_observation.weighted_defect_score,
        score_sequence[-1],
        tuple(transition.digest for transition in transitions),
        tuple(score_sequence),
        fixed_point,
        max_cycles,
        "",
    )
    return snapshot, replace(trace, trace_digest=alignment_trace_digest(trace))


def certify_repository_alignment_normal_form(
    initial_snapshot: RepositorySnapshot,
    max_states: int = 4096,
    deterministic_max_cycles: int = 256,
) -> AlignmentNormalFormCertificate:
    if max_states <= 0:
        raise ValueError("max_states_invalid")

    initial_observation = observe_repository_structure(initial_snapshot)
    queue: deque[RepositorySnapshot] = deque((initial_snapshot,))
    visited: dict[str, RepositorySnapshot] = {
        initial_snapshot.digest: initial_snapshot,
    }
    transitions: dict[str, AlignmentTransition] = {}
    terminals: dict[str, int] = {}

    while queue:
        snapshot = queue.popleft()
        observation, evaluated = _evaluated_candidates(snapshot)
        admissible = tuple(entry for entry in evaluated if entry[3].admissible)
        if not admissible:
            terminals[snapshot.digest] = observation.weighted_defect_score
            continue

        for target_snapshot, target_observation, candidate, assessment in admissible:
            transition = AlignmentTransition(
                snapshot.digest,
                target_snapshot.digest,
                candidate.digest,
                observation.weighted_defect_score,
                target_observation.weighted_defect_score,
            )
            if transition.target_score >= transition.source_score:
                raise ValueError("alignment_transition_not_strict")
            transitions.setdefault(transition.digest, transition)
            if target_snapshot.digest in visited:
                continue
            if len(visited) >= max_states:
                raise ValueError("alignment_state_bound_exceeded")
            visited[target_snapshot.digest] = target_snapshot
            queue.append(target_snapshot)

    terminal_digests = tuple(sorted(terminals))
    terminal_scores = tuple(terminals[digest] for digest in terminal_digests)
    unique_terminal = len(terminal_digests) == 1
    unique_terminal_digest = terminal_digests[0] if unique_terminal else ""
    final_snapshot, deterministic_trace = run_deterministic_alignment_trace(
        initial_snapshot,
        max_cycles=deterministic_max_cycles,
    )

    certificate = AlignmentNormalFormCertificate(
        initial_snapshot.digest,
        initial_observation.weighted_defect_score,
        tuple(sorted(visited)),
        tuple(sorted(transitions)),
        terminal_digests,
        terminal_scores,
        len(visited),
        len(transitions),
        max_states,
        all(
            transition.target_score < transition.source_score
            for transition in transitions.values()
        ),
        all(
            select_repository_candidate(
                _evaluated_candidates(visited[digest])[1]
            ) is None
            for digest in terminal_digests
        ),
        unique_terminal,
        unique_terminal_digest,
        unique_terminal and final_snapshot.digest == unique_terminal_digest
        and deterministic_trace.fixed_point_reached,
        False,
        "",
    )
    return replace(
        certificate,
        certificate_digest=normal_form_certificate_digest(certificate),
    )
