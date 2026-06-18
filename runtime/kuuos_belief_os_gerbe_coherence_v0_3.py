from __future__ import annotations

from copy import deepcopy
from itertools import combinations
from typing import Any, Mapping, Sequence

from runtime.kuuos_belief_os_context_transport_types_v0_2 import (
    RECEIPT_VERSION as TRANSPORT_RECEIPT_VERSION,
    NON_AUTHORITY_FLAGS as TRANSPORT_NON_AUTHORITY_FLAGS,
    receipt_digest as transport_receipt_digest,
)
from runtime.kuuos_belief_os_gerbe_types_v0_3 import (
    ACTIVATION_RECEIPT_VERSION,
    PACKET_VERSION,
    RECEIPT_VERSION,
    activation_receipt_digest,
    clamp01,
    copy_non_authority,
    packet_digest,
    receipt_digest,
    require_mapping,
    require_nonempty_string,
    require_nonnegative_int,
    sha,
    validate_packet_shell,
    validate_thresholds,
)
from runtime.kuuos_context_gerbe_coherence_types_v0_14 import (
    DECISION_VERSION as GERBE_DECISION_VERSION,
    decision_digest as gerbe_decision_digest,
)


def append_unique(existing: list[str], incoming: Sequence[str]) -> list[str]:
    result = list(existing)
    seen = set(result)
    for item in incoming:
        value = str(item)
        if value and value not in seen:
            result.append(value)
            seen.add(value)
    return result


def build_gerbe_packet(
    *,
    packet_id: str,
    lineage_id: str,
    target_context_id: str,
    source_transport_receipts: Sequence[Mapping[str, Any]],
    source_gerbe_decision: Mapping[str, Any],
    candidate_max_width: float,
    observe_max_width: float,
    candidate_max_two_cell_residue: float,
    candidate_max_higher_defect: float,
    hold_min_defect: float,
    minimum_triple_overlap: float,
    minimum_quadruple_overlap: float,
    created_at_ms: int,
) -> dict[str, Any]:
    packet = {
        "version": PACKET_VERSION,
        "packet_id": require_nonempty_string(packet_id, "packet_id"),
        "lineage_id": require_nonempty_string(lineage_id, "lineage_id"),
        "target_context_id": require_nonempty_string(
            target_context_id, "target_context_id"
        ),
        "source_transport_receipts": [
            deepcopy(dict(item)) for item in source_transport_receipts
        ],
        "source_gerbe_decision": deepcopy(dict(source_gerbe_decision)),
        "thresholds": {
            "candidate_max_width": clamp01(
                candidate_max_width, "candidate_max_width"
            ),
            "observe_max_width": clamp01(observe_max_width, "observe_max_width"),
            "candidate_max_two_cell_residue": clamp01(
                candidate_max_two_cell_residue,
                "candidate_max_two_cell_residue",
            ),
            "candidate_max_higher_defect": clamp01(
                candidate_max_higher_defect,
                "candidate_max_higher_defect",
            ),
            "hold_min_defect": clamp01(hold_min_defect, "hold_min_defect"),
            "minimum_triple_overlap": clamp01(
                minimum_triple_overlap, "minimum_triple_overlap"
            ),
            "minimum_quadruple_overlap": clamp01(
                minimum_quadruple_overlap, "minimum_quadruple_overlap"
            ),
        },
        "path_search_used": False,
        "global_chart_ranking_used": False,
        "universal_winner_selected": False,
        "global_trivialization_used": False,
        "created_at_ms": require_nonnegative_int(created_at_ms, "created_at_ms"),
        "non_authority": copy_non_authority(),
        "belief_gerbe_packet_digest": "",
    }
    validate_thresholds(packet["thresholds"])
    packet["belief_gerbe_packet_digest"] = packet_digest(packet)
    return packet


def validate_transport_receipt(
    receipt: Mapping[str, Any], *, lineage_id: str, target_context_id: str
) -> list[str]:
    errors: list[str] = []
    try:
        if receipt.get("version") != TRANSPORT_RECEIPT_VERSION:
            errors.append("source_transport_receipt_version_invalid")
        if receipt.get("belief_transport_receipt_digest") != transport_receipt_digest(
            receipt
        ):
            errors.append("source_transport_receipt_digest_invalid")
        if receipt.get("lineage_id") != lineage_id:
            errors.append("source_transport_lineage_mismatch")
        if receipt.get("target_context_id") != target_context_id:
            errors.append("source_transport_target_mismatch")
        if receipt.get("paramartha_non_reified") is not True:
            errors.append("source_transport_reification")
        if receipt.get("two_truths_separated") is not True:
            errors.append("source_transport_two_truths_collapsed")
        if receipt.get("locality_preserved") is not True:
            errors.append("source_transport_locality_lost")
        if receipt.get("plurality_preserved") is not True:
            errors.append("source_transport_plurality_lost")
        if receipt.get("path_search_used") is not False:
            errors.append("source_transport_path_search_forbidden")
        if receipt.get("global_chart_ranking_used") is not False:
            errors.append("source_transport_global_ranking_forbidden")
        if receipt.get("universal_winner_selected") is not False:
            errors.append("source_transport_universal_winner_forbidden")
        if dict(receipt.get("non_authority", {})) != TRANSPORT_NON_AUTHORITY_FLAGS:
            errors.append("source_transport_authority_escalation")
        sections = receipt.get("transported_sections")
        if not isinstance(sections, list) or not sections:
            errors.append("source_transport_sections_missing")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def validate_source_gerbe_decision(
    decision: Mapping[str, Any], *, target_context_id: str
) -> list[str]:
    errors: list[str] = []
    try:
        if decision.get("version") != GERBE_DECISION_VERSION:
            errors.append("source_gerbe_decision_version_invalid")
        if decision.get("gerbe_decision_digest") != gerbe_decision_digest(decision):
            errors.append("source_gerbe_decision_digest_invalid")
        if decision.get("target_context_key") != target_context_id:
            errors.append("source_gerbe_target_mismatch")
        require_nonempty_string(
            decision.get("source_atlas_bundle_digest"),
            "source_atlas_bundle_digest",
        )
        require_nonempty_string(
            decision.get("source_atlas_decision_digest"),
            "source_atlas_decision_digest",
        )
        clamp01(decision.get("gerbe_two_curvature"), "gerbe_two_curvature")
        clamp01(
            decision.get("higher_cocycle_defect"),
            "higher_cocycle_defect",
        )
        if decision.get("two_cell_residue_is_not_a_veto") is not True:
            errors.append("source_gerbe_two_cell_veto_escalation")
        if decision.get("higher_cocycle_defect_is_not_a_veto") is not True:
            errors.append("source_gerbe_higher_defect_veto_escalation")
        if decision.get("global_trivialization_forbidden") is not True:
            errors.append("source_gerbe_global_trivialization_enabled")
        if decision.get("surface_holonomy_append_only") is not True:
            errors.append("source_gerbe_surface_holonomy_not_append_only")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def interval_residue(left: Mapping[str, Any], right: Mapping[str, Any]) -> float:
    left_lower = clamp01(left.get("lower_probability"), "left_lower_probability")
    left_upper = clamp01(left.get("upper_probability"), "left_upper_probability")
    right_lower = clamp01(
        right.get("lower_probability"), "right_lower_probability"
    )
    right_upper = clamp01(
        right.get("upper_probability"), "right_upper_probability"
    )
    if left_lower > left_upper:
        raise ValueError("left_interval_inverted")
    if right_lower > right_upper:
        raise ValueError("right_interval_inverted")
    return max(abs(left_lower - right_lower), abs(left_upper - right_upper))


def path_support(record: Mapping[str, Any]) -> float:
    return min(
        clamp01(record.get("overlap"), "path_overlap"),
        clamp01(record.get("transport_reliability"), "transport_reliability"),
        clamp01(
            record.get("qi_history_compatibility"),
            "qi_history_compatibility",
        ),
    )


def _path_role(path: Sequence[str]) -> str:
    return "direct" if len(path) == 2 else "composite"


def _flatten_path_records(
    receipts: Sequence[Mapping[str, Any]], *, target_context_id: str
) -> tuple[list[dict[str, Any]], list[str], list[str], list[str], list[str]]:
    records: list[dict[str, Any]] = []
    evidence: list[str] = []
    counterevidence: list[str] = []
    source_state_digests: list[str] = []
    source_routes: list[str] = []
    seen: set[str] = set()

    for receipt in receipts:
        transport_receipt_id = str(receipt["belief_transport_receipt_digest"])
        evidence = append_unique(evidence, receipt.get("evidence_digests", []))
        counterevidence = append_unique(
            counterevidence, receipt.get("counterevidence_digests", [])
        )
        source_routes.append(str(receipt.get("route", "")))
        for raw_section in receipt["transported_sections"]:
            section = dict(require_mapping(raw_section, "transported_section"))
            source_context_id = require_nonempty_string(
                section.get("source_context_id"), "source_context_id"
            )
            source_state_digest = require_nonempty_string(
                section.get("source_belief_state_digest"),
                "source_belief_state_digest",
            )
            source_state_digests = append_unique(
                source_state_digests, [source_state_digest]
            )
            path = [str(item) for item in section.get("declared_path", [])]
            if len(path) < 2:
                raise ValueError("gerbe_declared_path_too_short")
            if path[0] != source_context_id:
                raise ValueError("gerbe_declared_path_source_mismatch")
            if path[-1] != target_context_id:
                raise ValueError("gerbe_declared_path_target_mismatch")
            if len(path) != len(set(path)):
                raise ValueError("gerbe_declared_path_repeats_context")
            transported_interval = dict(
                require_mapping(
                    section.get("transported_interval"),
                    "transported_interval",
                )
            )
            lower = clamp01(
                transported_interval.get("lower_probability"),
                "transported_lower_probability",
            )
            upper = clamp01(
                transported_interval.get("upper_probability"),
                "transported_upper_probability",
            )
            if lower > upper:
                raise ValueError("gerbe_path_interval_inverted")
            path_digest = sha(
                {
                    "source_belief_state_digest": source_state_digest,
                    "source_context_id": source_context_id,
                    "target_context_id": target_context_id,
                    "declared_path": path,
                    "transport_receipt_digest": transport_receipt_id,
                }
            )
            if path_digest in seen:
                raise ValueError("gerbe_path_record_duplicate")
            seen.add(path_digest)
            section_evidence = [str(item) for item in section.get("evidence_digests", [])]
            section_counterevidence = [
                str(item) for item in section.get("counterevidence_digests", [])
            ]
            evidence = append_unique(evidence, section_evidence)
            counterevidence = append_unique(
                counterevidence, section_counterevidence
            )
            records.append(
                {
                    "path_digest": path_digest,
                    "source_belief_id": section.get("source_belief_id", ""),
                    "source_belief_state_digest": source_state_digest,
                    "source_committed_belief_digest": section.get(
                        "source_committed_belief_digest", ""
                    ),
                    "source_context_id": source_context_id,
                    "target_context_id": target_context_id,
                    "declared_path": path,
                    "path_role": _path_role(path),
                    "transport_receipt_digest": transport_receipt_id,
                    "transported_interval": {
                        "lower_probability": lower,
                        "upper_probability": upper,
                        "ignorance_width": upper - lower,
                    },
                    "transport_reliability": clamp01(
                        section.get("transport_reliability"),
                        "transport_reliability",
                    ),
                    "overlap": clamp01(section.get("overlap"), "overlap"),
                    "curvature": clamp01(section.get("curvature"), "curvature"),
                    "cocycle_defect": clamp01(
                        section.get("cocycle_defect"), "cocycle_defect"
                    ),
                    "holonomy_residual": clamp01(
                        section.get("holonomy_residual"),
                        "holonomy_residual",
                    ),
                    "qi_history_compatibility": clamp01(
                        section.get("qi_history_compatibility"),
                        "qi_history_compatibility",
                    ),
                    "evidence_digests": section_evidence,
                    "counterevidence_digests": section_counterevidence,
                }
            )
    return records, evidence, counterevidence, source_state_digests, source_routes


def _group_paths(records: Sequence[Mapping[str, Any]]) -> dict[tuple[str, str], list[dict[str, Any]]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for raw in records:
        record = dict(raw)
        key = (
            str(record["source_context_id"]),
            str(record["source_belief_state_digest"]),
        )
        grouped.setdefault(key, []).append(record)
    return grouped


def _build_two_cells(
    grouped: Mapping[tuple[str, str], list[dict[str, Any]]],
    *,
    minimum_triple_overlap: float,
    source_gerbe_decision_digest: str,
) -> list[dict[str, Any]]:
    cells: list[dict[str, Any]] = []
    for (source_context_id, source_state_digest), records in grouped.items():
        for left, right in combinations(records, 2):
            support = min(path_support(left), path_support(right))
            if support < minimum_triple_overlap:
                continue
            residue = interval_residue(
                left["transported_interval"], right["transported_interval"]
            )
            cells.append(
                {
                    "two_cell_id": "belief-gerbe-two-cell-"
                    + sha(
                        {
                            "left": left["path_digest"],
                            "right": right["path_digest"],
                            "source_gerbe_decision_digest": source_gerbe_decision_digest,
                        }
                    )[:20],
                    "source_context_id": source_context_id,
                    "source_belief_state_digest": source_state_digest,
                    "target_context_id": left["target_context_id"],
                    "left_path_digest": left["path_digest"],
                    "right_path_digest": right["path_digest"],
                    "left_declared_path": list(left["declared_path"]),
                    "right_declared_path": list(right["declared_path"]),
                    "left_path_role": left["path_role"],
                    "right_path_role": right["path_role"],
                    "left_interval": deepcopy(left["transported_interval"]),
                    "right_interval": deepcopy(right["transported_interval"]),
                    "triple_overlap_support": support,
                    "coherence_residue": residue,
                    "localized_on_triple_overlap": True,
                    "source_transport_receipts_preserved": True,
                    "residue_is_not_veto": True,
                }
            )
    return cells


def _build_higher_witnesses(
    grouped: Mapping[tuple[str, str], list[dict[str, Any]]],
    *,
    minimum_quadruple_overlap: float,
    source_gerbe_decision_digest: str,
) -> list[dict[str, Any]]:
    witnesses: list[dict[str, Any]] = []
    for (source_context_id, source_state_digest), records in grouped.items():
        for first, second, third in combinations(records, 3):
            support = min(
                path_support(first), path_support(second), path_support(third)
            )
            if support < minimum_quadruple_overlap:
                continue
            defects = [
                interval_residue(
                    first["transported_interval"], second["transported_interval"]
                ),
                interval_residue(
                    first["transported_interval"], third["transported_interval"]
                ),
                interval_residue(
                    second["transported_interval"], third["transported_interval"]
                ),
            ]
            witnesses.append(
                {
                    "higher_witness_id": "belief-gerbe-higher-"
                    + sha(
                        {
                            "paths": sorted(
                                [
                                    first["path_digest"],
                                    second["path_digest"],
                                    third["path_digest"],
                                ]
                            ),
                            "source_gerbe_decision_digest": source_gerbe_decision_digest,
                        }
                    )[:20],
                    "source_context_id": source_context_id,
                    "source_belief_state_digest": source_state_digest,
                    "target_context_id": first["target_context_id"],
                    "path_digests": [
                        first["path_digest"],
                        second["path_digest"],
                        third["path_digest"],
                    ],
                    "declared_paths": [
                        list(first["declared_path"]),
                        list(second["declared_path"]),
                        list(third["declared_path"]),
                    ],
                    "quadruple_overlap_support": support,
                    "pairwise_residues": defects,
                    "higher_coherence_defect": max(defects),
                    "localized_on_quadruple_overlap": True,
                    "global_trivialization_used": False,
                    "higher_defect_is_not_prohibition": True,
                }
            )
    return witnesses


def coherence_widen_interval(
    *, lower: float, upper: float, defect: float
) -> dict[str, float]:
    lower_value = clamp01(lower, "hull_lower_probability")
    upper_value = clamp01(upper, "hull_upper_probability")
    defect_value = clamp01(defect, "coherence_defect")
    if lower_value > upper_value:
        raise ValueError("gerbe_hull_interval_inverted")
    coherent_lower = max(0.0, lower_value - defect_value)
    coherent_upper = min(1.0, upper_value + defect_value)
    if coherent_lower > lower_value + 1e-12:
        raise ValueError("coherence_lower_not_conservative")
    if coherent_upper + 1e-12 < upper_value:
        raise ValueError("coherence_upper_not_conservative")
    return {
        "lower_probability": coherent_lower,
        "upper_probability": coherent_upper,
        "ignorance_width": coherent_upper - coherent_lower,
    }


def build_gerbe_coherence_receipt(packet: Mapping[str, Any]) -> dict[str, Any]:
    shell_errors = validate_packet_shell(packet)
    if shell_errors:
        raise ValueError("invalid_gerbe_packet:" + ";".join(shell_errors))

    lineage_id = str(packet["lineage_id"])
    target_context_id = str(packet["target_context_id"])
    receipts = [
        dict(require_mapping(item, "source_transport_receipt"))
        for item in packet["source_transport_receipts"]
    ]
    transport_errors: list[str] = []
    for receipt in receipts:
        transport_errors.extend(
            validate_transport_receipt(
                receipt,
                lineage_id=lineage_id,
                target_context_id=target_context_id,
            )
        )
    if transport_errors:
        raise ValueError("invalid_source_transport:" + ";".join(transport_errors))

    gerbe_decision = dict(
        require_mapping(packet["source_gerbe_decision"], "source_gerbe_decision")
    )
    gerbe_errors = validate_source_gerbe_decision(
        gerbe_decision, target_context_id=target_context_id
    )
    if gerbe_errors:
        raise ValueError("invalid_source_gerbe:" + ";".join(gerbe_errors))

    thresholds = validate_thresholds(dict(packet["thresholds"]))
    (
        path_records,
        evidence_digests,
        counterevidence_digests,
        source_state_digests,
        source_routes,
    ) = _flatten_path_records(receipts, target_context_id=target_context_id)
    if not path_records:
        raise ValueError("gerbe_path_records_missing")
    grouped = _group_paths(path_records)
    source_gerbe_receipt_id = str(gerbe_decision["gerbe_decision_digest"])
    two_cells = _build_two_cells(
        grouped,
        minimum_triple_overlap=thresholds["minimum_triple_overlap"],
        source_gerbe_decision_digest=source_gerbe_receipt_id,
    )
    higher_witnesses = _build_higher_witnesses(
        grouped,
        minimum_quadruple_overlap=thresholds["minimum_quadruple_overlap"],
        source_gerbe_decision_digest=source_gerbe_receipt_id,
    )

    path_lowers = [
        float(record["transported_interval"]["lower_probability"])
        for record in path_records
    ]
    path_uppers = [
        float(record["transported_interval"]["upper_probability"])
        for record in path_records
    ]
    hull_lower = min(path_lowers)
    hull_upper = max(path_uppers)
    local_two_cell_residue = max(
        (float(cell["coherence_residue"]) for cell in two_cells), default=0.0
    )
    local_higher_defect = max(
        (
            float(witness["higher_coherence_defect"])
            for witness in higher_witnesses
        ),
        default=0.0,
    )
    source_two_curvature = clamp01(
        gerbe_decision["gerbe_two_curvature"], "gerbe_two_curvature"
    )
    source_higher_defect = clamp01(
        gerbe_decision["higher_cocycle_defect"], "higher_cocycle_defect"
    )
    total_defect = max(
        local_two_cell_residue,
        local_higher_defect,
        source_two_curvature,
        source_higher_defect,
    )
    coherent_interval = coherence_widen_interval(
        lower=hull_lower, upper=hull_upper, defect=total_defect
    )

    if "QUARANTINE" in source_routes:
        route = "QUARANTINE"
    elif source_routes and all(route == "REJECT" for route in source_routes):
        route = "REJECT"
    elif total_defect >= thresholds["hold_min_defect"]:
        route = "HOLD"
    elif coherent_interval["ignorance_width"] > thresholds["observe_max_width"]:
        route = "REPAIR"
    elif (
        coherent_interval["ignorance_width"] > thresholds["candidate_max_width"]
        or local_two_cell_residue
        > thresholds["candidate_max_two_cell_residue"]
        or local_higher_defect > thresholds["candidate_max_higher_defect"]
    ):
        route = "OBSERVE"
    else:
        route = "CANDIDATE"

    source_transport_receipt_digests = [
        str(receipt["belief_transport_receipt_digest"]) for receipt in receipts
    ]
    basis = {
        "lineage_id": lineage_id,
        "target_context_id": target_context_id,
        "source_transport_receipt_digests": source_transport_receipt_digests,
        "source_belief_state_digests": source_state_digests,
        "source_gerbe_decision_digest": source_gerbe_receipt_id,
        "coherent_interval": coherent_interval,
        "total_coherence_defect": total_defect,
        "route": route,
        "evidence_digests": evidence_digests,
        "counterevidence_digests": counterevidence_digests,
    }
    next_revision_basis_digest = sha(basis)

    receipt = {
        "version": RECEIPT_VERSION,
        "packet_id": packet["packet_id"],
        "lineage_id": lineage_id,
        "target_context_id": target_context_id,
        "belief_gerbe_packet_digest": packet["belief_gerbe_packet_digest"],
        "source_transport_receipt_digests": source_transport_receipt_digests,
        "source_belief_state_digests": source_state_digests,
        "source_gerbe_decision_digest": source_gerbe_receipt_id,
        "source_gerbe_bundle_digest": gerbe_decision[
            "source_atlas_bundle_digest"
        ],
        "source_atlas_decision_digest": gerbe_decision[
            "source_atlas_decision_digest"
        ],
        "source_gerbe_class": gerbe_decision.get("gerbe_class", ""),
        "path_records": path_records,
        "path_count": len(path_records),
        "two_cells": two_cells,
        "two_cell_count": len(two_cells),
        "higher_witnesses": higher_witnesses,
        "higher_witness_count": len(higher_witnesses),
        "path_hull_interval": {
            "lower_probability": hull_lower,
            "upper_probability": hull_upper,
            "ignorance_width": hull_upper - hull_lower,
        },
        "coherent_interval": coherent_interval,
        "local_two_cell_residue": local_two_cell_residue,
        "local_higher_defect": local_higher_defect,
        "source_gerbe_two_curvature": source_two_curvature,
        "source_higher_cocycle_defect": source_higher_defect,
        "total_coherence_defect": total_defect,
        "evidence_digests": evidence_digests,
        "counterevidence_digests": counterevidence_digests,
        "route": route,
        "reasoning_license": route in {"CANDIDATE", "OBSERVE"},
        "planning_support_license": route == "CANDIDATE",
        "next_revision_basis_digest": next_revision_basis_digest,
        "pending_replan_activation": route == "CANDIDATE",
        "locality_preserved": True,
        "plurality_preserved": True,
        "paramartha_non_reified": True,
        "two_truths_separated": True,
        "two_cell_residue_is_not_veto": True,
        "higher_defect_is_not_prohibition": True,
        "global_trivialization_used": False,
        "path_search_used": False,
        "global_chart_ranking_used": False,
        "universal_winner_selected": False,
        "surface_holonomy_append_only": True,
        "future_only": True,
        "memory_overwrite": False,
        "non_authority": copy_non_authority(),
        "created_at_ms": packet["created_at_ms"],
        "belief_gerbe_receipt_digest": "",
    }
    receipt["belief_gerbe_receipt_digest"] = receipt_digest(receipt)
    return receipt


def build_replan_gerbe_activation_receipt(
    *,
    gerbe_receipt: Mapping[str, Any],
    mission_cycle_phase: str,
    mission_cycle_state_digest: str,
    replan_receipt_digest: str,
    next_plan_basis_digest: str,
    now_ms: int,
) -> dict[str, Any]:
    if gerbe_receipt.get("version") != RECEIPT_VERSION:
        raise ValueError("gerbe_receipt_version_invalid")
    if gerbe_receipt.get("belief_gerbe_receipt_digest") != receipt_digest(
        gerbe_receipt
    ):
        raise ValueError("gerbe_receipt_digest_invalid")
    if gerbe_receipt.get("route") != "CANDIDATE":
        raise ValueError("gerbe_candidate_route_required")
    if gerbe_receipt.get("pending_replan_activation") is not True:
        raise ValueError("gerbe_not_pending_replan_activation")
    if mission_cycle_phase != "replan":
        raise ValueError("mission_replan_required")
    if gerbe_receipt.get("future_only") is not True:
        raise ValueError("gerbe_not_future_only")
    if gerbe_receipt.get("memory_overwrite") is not False:
        raise ValueError("gerbe_memory_overwrite_forbidden")

    activation = {
        "version": ACTIVATION_RECEIPT_VERSION,
        "lineage_id": gerbe_receipt["lineage_id"],
        "belief_gerbe_receipt_digest": gerbe_receipt[
            "belief_gerbe_receipt_digest"
        ],
        "gerbe_next_revision_basis_digest": gerbe_receipt[
            "next_revision_basis_digest"
        ],
        "mission_cycle_phase": "replan",
        "mission_cycle_state_digest": require_nonempty_string(
            mission_cycle_state_digest, "mission_cycle_state_digest"
        ),
        "replan_receipt_digest": require_nonempty_string(
            replan_receipt_digest, "replan_receipt_digest"
        ),
        "next_plan_basis_digest": require_nonempty_string(
            next_plan_basis_digest, "next_plan_basis_digest"
        ),
        "future_only": True,
        "memory_overwrite": False,
        "non_authority": copy_non_authority(),
        "created_at_ms": require_nonnegative_int(now_ms, "now_ms"),
        "belief_gerbe_activation_receipt_digest": "",
    }
    activation["belief_gerbe_activation_receipt_digest"] = (
        activation_receipt_digest(activation)
    )
    return activation
