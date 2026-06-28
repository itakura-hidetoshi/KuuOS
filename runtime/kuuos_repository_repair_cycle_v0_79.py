#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_repository_repair_candidates_v0_79 import generate_repository_repair_candidates
from runtime.kuuos_repository_shadow_repair_v0_79 import evaluate_repository_candidates, select_repository_candidate
from runtime.kuuos_repository_structure_observer_v0_79 import observe_repository_structure
from runtime.kuuos_repository_structure_types_v0_79 import (
    APPLIED,
    NO_CHANGE,
    RepositoryRepairCycleReceipt,
    RepositorySnapshot,
    repair_cycle_receipt_digest,
)


def run_repository_repair_cycle(
    cycle_id: str,
    snapshot: RepositorySnapshot,
    max_candidates: int = 32,
) -> tuple[RepositorySnapshot, RepositoryRepairCycleReceipt]:
    observation = observe_repository_structure(snapshot)
    candidates = generate_repository_repair_candidates(snapshot, observation, max_candidates)
    evaluated = evaluate_repository_candidates(snapshot, observation, candidates)
    selected = select_repository_candidate(evaluated)
    if selected is None:
        final_snapshot = snapshot
        final_observation = observation
        selected_digest = ""
        status = NO_CHANGE
    else:
        final_snapshot, final_observation, candidate, _ = selected
        selected_digest = candidate.digest
        status = APPLIED
    receipt = RepositoryRepairCycleReceipt(
        cycle_id,
        status,
        snapshot.digest,
        observation.digest,
        tuple(item.digest for item in candidates),
        tuple(item[3].digest for item in evaluated),
        selected_digest,
        final_snapshot.digest,
        final_observation.digest,
        False,
        False,
        False,
        False,
        "",
    )
    return final_snapshot, replace(receipt, receipt_digest=repair_cycle_receipt_digest(receipt))
