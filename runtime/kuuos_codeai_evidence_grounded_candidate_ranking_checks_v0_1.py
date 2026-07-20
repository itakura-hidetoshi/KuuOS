from __future__ import annotations

import copy
from typing import Any, Mapping

from runtime.kuuos_codeai_evidence_grounded_candidate_ranking_schema_v0_1 import (
    CLASSIFICATION_PRIORITY,
    DISPOSITION_ADMISSIBLE,
    DISPOSITION_HOLD,
    DISPOSITION_REJECTED,
    DISPOSITION_REPAIRABLE,
)


def evidence_burden(candidate: Mapping[str, Any]) -> dict[str, int]:
    counts = candidate["finding_counts"]
    return {
        "reject_findings": int(counts.get("reject", 0)),
        "hold_findings": int(counts.get("hold", 0)),
        "repairable_findings": int(counts.get("repairable", 0)),
        "total_findings": len(candidate["findings"]),
        "operation_count": int(candidate["operation_count"]),
        "changed_path_count": len(candidate["changed_paths"]),
    }


def ranking_key(candidate: Mapping[str, Any]) -> tuple[int, int, int, int, int, int, int, int, str]:
    burden = evidence_burden(candidate)
    return (
        CLASSIFICATION_PRIORITY[candidate["classification"]],
        burden["reject_findings"],
        burden["hold_findings"],
        burden["repairable_findings"],
        burden["total_findings"],
        burden["operation_count"],
        burden["changed_path_count"],
        int(candidate["candidate_sequence"]),
        str(candidate["candidate_id"]),
    )


def rank_candidates(candidates: list[Mapping[str, Any]]) -> list[dict[str, Any]]:
    ordered = sorted(candidates, key=ranking_key)
    ranked: list[dict[str, Any]] = []
    for position, candidate in enumerate(ordered, start=1):
        ranked.append(
            {
                "ranking_position": position,
                "candidate_id": candidate["candidate_id"],
                "candidate_sequence": candidate["candidate_sequence"],
                "classification": candidate["classification"],
                "evidence_route": candidate["evidence_route"],
                "classification_priority": CLASSIFICATION_PRIORITY[candidate["classification"]],
                "evidence_burden": evidence_burden(candidate),
                "ranking_key": list(ranking_key(candidate)),
                "source_candidate_evidence": copy.deepcopy(dict(candidate)),
                "rank_assigned": True,
                "candidate_selected": False,
                "verification_runner_invoked": False,
                "repair_executed": False,
                "repository_mutation_performed": False,
                "execution_authority_granted": False,
                "git_authority_granted": False,
            }
        )
    return ranked


def classification_counts(candidates: list[Mapping[str, Any]]) -> dict[str, int]:
    counts = {
        "admissible": 0,
        "repairable": 0,
        "hold": 0,
        "rejected": 0,
    }
    names = {
        DISPOSITION_ADMISSIBLE: "admissible",
        DISPOSITION_REPAIRABLE: "repairable",
        DISPOSITION_HOLD: "hold",
        DISPOSITION_REJECTED: "rejected",
    }
    for candidate in candidates:
        counts[names[candidate["classification"]]] += 1
    return counts


def total_finding_count(candidates: list[Mapping[str, Any]]) -> int:
    return sum(len(candidate["findings"]) for candidate in candidates)


def total_changed_path_count(candidates: list[Mapping[str, Any]]) -> int:
    paths: set[str] = set()
    for candidate in candidates:
        paths.update(candidate["changed_paths"])
    return len(paths)


__all__ = [
    "classification_counts",
    "evidence_burden",
    "rank_candidates",
    "ranking_key",
    "total_changed_path_count",
    "total_finding_count",
]
