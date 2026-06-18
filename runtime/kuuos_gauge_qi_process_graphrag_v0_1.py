from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from math import exp, isfinite, sqrt
from typing import Any, Mapping, Sequence

VERSION = "kuuos_gauge_qi_process_graphrag_v0_1"
RECEIPT_VERSION = "kuuos_gauge_qi_process_graphrag_receipt_v0_1"
ROUTES = {"CANDIDATE", "OBSERVE", "HOLD", "REPAIR", "QUARANTINE"}
REQUIRED_BOUNDARY = {
    "query_specific_evidence_bundle": True,
    "persistent_global_context_graph": False,
    "shortest_path_search_used": False,
    "global_winner_selected": False,
    "global_truth_granted": False,
    "execution_authority_granted": False,
    "clinical_authority_granted": False,
    "theorem_authority_granted": False,
}
NON_AUTHORITY = {
    "evidence_bundle_is_truth": False,
    "path_score_is_truth": False,
    "curvature_is_veto": False,
    "qi_history_is_authority": False,
    "receipt_is_execution_license": False,
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest_payload(value: Any) -> str:
    return sha256(canonical_json(value).encode("utf-8")).hexdigest()


def clamp01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def _number(value: Any, name: str, *, unit_interval: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name}_must_be_number")
    result = float(value)
    if not isfinite(result):
        raise ValueError(f"{name}_must_be_finite")
    if unit_interval and not 0.0 <= result <= 1.0:
        raise ValueError(f"{name}_must_be_in_unit_interval")
    return result


def _nonempty(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name}_must_be_nonempty_string")
    return value


def _matrix2(value: Any, name: str) -> list[list[float]]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)) or len(value) != 2:
        raise ValueError(f"{name}_must_be_2x2_matrix")
    rows: list[list[float]] = []
    for row_index, row in enumerate(value):
        if not isinstance(row, Sequence) or isinstance(row, (str, bytes)) or len(row) != 2:
            raise ValueError(f"{name}_must_be_2x2_matrix")
        rows.append([
            _number(row[0], f"{name}_{row_index}_0"),
            _number(row[1], f"{name}_{row_index}_1"),
        ])
    return rows


def _vector2(value: Any, name: str) -> list[float]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)) or len(value) != 2:
        raise ValueError(f"{name}_must_be_vector2")
    return [_number(value[0], f"{name}_0"), _number(value[1], f"{name}_1")]


def identity2() -> list[list[float]]:
    return [[1.0, 0.0], [0.0, 1.0]]


def transpose2(matrix: Sequence[Sequence[float]]) -> list[list[float]]:
    return [[float(matrix[0][0]), float(matrix[1][0])], [float(matrix[0][1]), float(matrix[1][1])]]


def matmul2(left: Sequence[Sequence[float]], right: Sequence[Sequence[float]]) -> list[list[float]]:
    return [
        [
            float(left[row][0]) * float(right[0][column])
            + float(left[row][1]) * float(right[1][column])
            for column in range(2)
        ]
        for row in range(2)
    ]


def matvec2(matrix: Sequence[Sequence[float]], vector: Sequence[float]) -> list[float]:
    return [
        float(matrix[0][0]) * float(vector[0]) + float(matrix[0][1]) * float(vector[1]),
        float(matrix[1][0]) * float(vector[0]) + float(matrix[1][1]) * float(vector[1]),
    ]


def vector_norm2(vector: Sequence[float]) -> float:
    return sqrt(float(vector[0]) ** 2 + float(vector[1]) ** 2)


def matrix_distance2(left: Sequence[Sequence[float]], right: Sequence[Sequence[float]]) -> float:
    return sqrt(sum((float(left[i][j]) - float(right[i][j])) ** 2 for i in range(2) for j in range(2)))


def orthogonality_residual(matrix: Sequence[Sequence[float]]) -> float:
    gram = matmul2(transpose2(matrix), matrix)
    return clamp01(matrix_distance2(gram, identity2()) / (2.0 * sqrt(2.0)))


def holonomy_residual(matrix: Sequence[Sequence[float]]) -> float:
    return clamp01(matrix_distance2(matrix, identity2()) / (2.0 * sqrt(2.0)))


def _unique(items: Sequence[Mapping[str, Any]], key: str, name: str) -> None:
    values = [_nonempty(item.get(key), f"{name}_{key}") for item in items]
    if len(values) != len(set(values)):
        raise ValueError(f"{name}_{key}_must_be_unique")


def _validate_boundary(boundary: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    for key, expected in REQUIRED_BOUNDARY.items():
        if boundary.get(key) is not expected:
            errors.append(f"boundary_{key}_must_be_{str(expected).lower()}")
    return errors


def validate_bundle(bundle: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if bundle.get("version") != VERSION:
            errors.append("version_invalid")
        _nonempty(bundle.get("query_id"), "query_id")
        _nonempty(bundle.get("query_digest"), "query_digest")
        if digest_payload(bundle.get("query_text", "")) != bundle.get("query_digest"):
            errors.append("query_digest_mismatch")

        patches = bundle.get("patches")
        connections = bundle.get("connections")
        paths = bundle.get("declared_paths")
        cycles = bundle.get("declared_cycles")
        if not isinstance(patches, list) or not patches:
            raise ValueError("patches_must_be_nonempty_list")
        if not isinstance(connections, list):
            raise ValueError("connections_must_be_list")
        if not isinstance(paths, list) or not paths:
            raise ValueError("declared_paths_must_be_nonempty_list")
        if not isinstance(cycles, list):
            raise ValueError("declared_cycles_must_be_list")

        _unique(patches, "patch_id", "patches")
        _unique(connections, "connection_id", "connections")
        _unique(paths, "path_id", "declared_paths")
        _unique(cycles, "cycle_id", "declared_cycles")
        patch_ids = {item["patch_id"] for item in patches}
        connection_ids = {item["connection_id"] for item in connections}
        connection_by_id = {item["connection_id"]: item for item in connections}

        for patch in patches:
            _nonempty(patch.get("context_id"), "patch_context_id")
            _nonempty(patch.get("evidence_digest"), "patch_evidence_digest")
            _nonempty(patch.get("source_digest"), "patch_source_digest")
            _vector2(patch.get("local_vector"), "patch_local_vector")
            for field in (
                "relevance",
                "source_confidence",
                "provenance_completeness",
                "uncertainty",
            ):
                _number(patch.get(field), f"patch_{field}", unit_interval=True)
            _number(patch.get("observed_at"), "patch_observed_at")
            rollback_ref = patch.get("rollback_ref", "")
            if not isinstance(rollback_ref, str):
                raise ValueError("patch_rollback_ref_must_be_string")

        for connection in connections:
            source = _nonempty(connection.get("source_patch"), "connection_source_patch")
            target = _nonempty(connection.get("target_patch"), "connection_target_patch")
            if source not in patch_ids or target not in patch_ids:
                raise ValueError("connection_patch_reference_missing")
            matrix = _matrix2(connection.get("transport"), "connection_transport")
            if orthogonality_residual(matrix) > 1e-6:
                errors.append(f"connection_{connection['connection_id']}_not_orthogonal")
            _number(connection.get("overlap"), "connection_overlap", unit_interval=True)
            _number(connection.get("confidence"), "connection_confidence", unit_interval=True)
            _nonempty(connection.get("provenance_digest"), "connection_provenance_digest")

        def validate_walk(item: Mapping[str, Any], item_name: str, closed: bool) -> None:
            patch_sequence = item.get("patch_sequence")
            connection_sequence = item.get("connection_sequence")
            if not isinstance(patch_sequence, list) or len(patch_sequence) < 2:
                raise ValueError(f"{item_name}_patch_sequence_invalid")
            if not isinstance(connection_sequence, list) or len(connection_sequence) != len(patch_sequence) - 1:
                raise ValueError(f"{item_name}_connection_sequence_invalid")
            if any(patch_id not in patch_ids for patch_id in patch_sequence):
                raise ValueError(f"{item_name}_patch_reference_missing")
            if any(connection_id not in connection_ids for connection_id in connection_sequence):
                raise ValueError(f"{item_name}_connection_reference_missing")
            for index, connection_id in enumerate(connection_sequence):
                connection = connection_by_id[connection_id]
                if connection["source_patch"] != patch_sequence[index]:
                    raise ValueError(f"{item_name}_source_alignment_invalid")
                if connection["target_patch"] != patch_sequence[index + 1]:
                    raise ValueError(f"{item_name}_target_alignment_invalid")
            if closed and patch_sequence[0] != patch_sequence[-1]:
                raise ValueError(f"{item_name}_must_be_closed")

        for path in paths:
            validate_walk(path, f"path_{path['path_id']}", False)
            _nonempty(path.get("declared_by"), "path_declared_by")
        for cycle in cycles:
            validate_walk(cycle, f"cycle_{cycle['cycle_id']}", True)

        qi = bundle.get("qi_process")
        if not isinstance(qi, Mapping):
            raise ValueError("qi_process_must_be_object")
        _nonempty(qi.get("process_tensor_digest"), "process_tensor_digest")
        _nonempty(qi.get("history_window_digest"), "history_window_digest")
        history_depth = qi.get("history_depth")
        if isinstance(history_depth, bool) or not isinstance(history_depth, int) or history_depth < 1:
            raise ValueError("history_depth_must_be_positive_int")
        for field in (
            "transition_continuity",
            "memory_continuity",
            "nonmarkov_link_density",
            "recoverability_branching_capacity",
            "observation_debt_pressure",
            "intervention_residue",
        ):
            _number(qi.get(field), field, unit_interval=True)

        boundary = bundle.get("boundary")
        if not isinstance(boundary, Mapping):
            raise ValueError("boundary_must_be_object")
        for key in REQUIRED_BOUNDARY:
            if not isinstance(boundary.get(key), bool):
                errors.append(f"boundary_{key}_must_be_bool")
    except ValueError as exc:
        errors.append(str(exc))
    return errors


def _path_transport(path: Mapping[str, Any], connection_by_id: Mapping[str, Mapping[str, Any]]) -> list[list[float]]:
    total = identity2()
    for connection_id in path["connection_sequence"]:
        total = matmul2(connection_by_id[connection_id]["transport"], total)
    return total


def qi_history_compatibility(qi: Mapping[str, Any]) -> float:
    base = (
        0.25 * float(qi["transition_continuity"])
        + 0.25 * float(qi["memory_continuity"])
        + 0.20 * float(qi["recoverability_branching_capacity"])
        + 0.15 * (1.0 - float(qi["observation_debt_pressure"]))
        + 0.15 * (1.0 - float(qi["intervention_residue"]))
    )
    visibility_modifier = 0.75 + 0.25 * float(qi["nonmarkov_link_density"])
    return clamp01(base * visibility_modifier)


def evaluate_declared_path(
    path: Mapping[str, Any],
    patch_by_id: Mapping[str, Mapping[str, Any]],
    connection_by_id: Mapping[str, Mapping[str, Any]],
    qi: Mapping[str, Any],
) -> dict[str, Any]:
    patches = [patch_by_id[patch_id] for patch_id in path["patch_sequence"]]
    connections = [connection_by_id[connection_id] for connection_id in path["connection_sequence"]]
    total_transport = _path_transport(path, connection_by_id)
    transported_start = matvec2(total_transport, patches[0]["local_vector"])
    endpoint_vector = patches[-1]["local_vector"]
    difference = [transported_start[0] - endpoint_vector[0], transported_start[1] - endpoint_vector[1]]
    alignment_residual = clamp01(
        vector_norm2(difference)
        / (1.0 + vector_norm2(transported_start) + vector_norm2(endpoint_vector))
    )

    transport_reliability = 1.0
    for connection in connections:
        transport_reliability *= float(connection["overlap"]) * float(connection["confidence"])
    transport_reliability = clamp01(transport_reliability)

    semantic_relevance = sum(float(patch["relevance"]) for patch in patches) / len(patches)
    source_confidence = min(float(patch["source_confidence"]) for patch in patches)
    provenance = min(float(patch["provenance_completeness"]) for patch in patches)
    rollback_fraction = sum(bool(patch.get("rollback_ref")) for patch in patches) / len(patches)
    recoverability = clamp01(float(qi["recoverability_branching_capacity"]) * rollback_fraction)
    time_regressions = sum(
        float(patches[index + 1]["observed_at"]) < float(patches[index]["observed_at"])
        for index in range(len(patches) - 1)
    )
    temporal_consistency = 1.0 - time_regressions / max(1, len(patches) - 1)
    qi_compatibility = qi_history_compatibility(qi)

    action = clamp01(
        0.20 * (1.0 - semantic_relevance)
        + 0.15 * (1.0 - source_confidence)
        + 0.15 * (1.0 - provenance)
        + 0.15 * (1.0 - transport_reliability)
        + 0.10 * alignment_residual
        + 0.05 * (1.0 - temporal_consistency)
        + 0.10 * (1.0 - qi_compatibility)
        + 0.10 * (1.0 - recoverability)
    )
    evidence_sufficiency = clamp01(
        0.30 * semantic_relevance
        + 0.25 * source_confidence
        + 0.20 * provenance
        + 0.15 * transport_reliability
        + 0.10 * qi_compatibility
    )
    return {
        "path_id": path["path_id"],
        "patch_sequence": list(path["patch_sequence"]),
        "connection_sequence": list(path["connection_sequence"]),
        "total_transport": total_transport,
        "transported_start_vector": transported_start,
        "alignment_residual": alignment_residual,
        "transport_reliability": transport_reliability,
        "semantic_relevance": semantic_relevance,
        "source_confidence": source_confidence,
        "provenance_completeness": provenance,
        "temporal_consistency": temporal_consistency,
        "qi_history_compatibility": qi_compatibility,
        "recoverability": recoverability,
        "path_action": action,
        "path_weight": exp(-3.0 * action),
        "evidence_sufficiency": evidence_sufficiency,
    }


def evaluate_declared_cycle(
    cycle: Mapping[str, Any], connection_by_id: Mapping[str, Mapping[str, Any]]
) -> dict[str, Any]:
    total = _path_transport(cycle, connection_by_id)
    return {
        "cycle_id": cycle["cycle_id"],
        "patch_sequence": list(cycle["patch_sequence"]),
        "connection_sequence": list(cycle["connection_sequence"]),
        "holonomy": total,
        "curvature_residual": holonomy_residual(total),
    }


def _next_observation_target(
    path_results: Sequence[Mapping[str, Any]], cycle_results: Sequence[Mapping[str, Any]], qi: Mapping[str, Any]
) -> str:
    deficits = {
        "source_provenance": max(1.0 - float(item["provenance_completeness"]) for item in path_results),
        "gauge_connection": max(1.0 - float(item["transport_reliability"]) for item in path_results),
        "semantic_alignment": max(float(item["alignment_residual"]) for item in path_results),
        "recoverability": max(1.0 - float(item["recoverability"]) for item in path_results),
        "qi_history": 1.0 - qi_history_compatibility(qi),
        "cycle_curvature": max(
            [float(item["curvature_residual"]) for item in cycle_results] or [0.0]
        ),
    }
    return max(deficits, key=deficits.get)


def evaluate_evidence_bundle(bundle: Mapping[str, Any]) -> dict[str, Any]:
    errors = validate_bundle(bundle)
    if errors:
        raise ValueError(";".join(errors))

    patch_by_id = {item["patch_id"]: item for item in bundle["patches"]}
    connection_by_id = {item["connection_id"]: item for item in bundle["connections"]}
    qi = bundle["qi_process"]
    path_results = [
        evaluate_declared_path(path, patch_by_id, connection_by_id, qi)
        for path in bundle["declared_paths"]
    ]
    cycle_results = [
        evaluate_declared_cycle(cycle, connection_by_id)
        for cycle in bundle["declared_cycles"]
    ]

    max_curvature = max([item["curvature_residual"] for item in cycle_results] or [0.0])
    max_action = max(item["path_action"] for item in path_results)
    min_evidence = min(item["evidence_sufficiency"] for item in path_results)
    min_provenance = min(item["provenance_completeness"] for item in path_results)
    min_recoverability = min(item["recoverability"] for item in path_results)

    if _validate_boundary(bundle["boundary"]):
        route = "QUARANTINE"
    elif min_provenance < 0.50 or min_recoverability < 0.35:
        route = "REPAIR"
    elif max_curvature > 0.65 or float(qi["observation_debt_pressure"]) > 0.75:
        route = "HOLD"
    elif max_action <= 0.30 and min_evidence >= 0.65:
        route = "CANDIDATE"
    else:
        route = "OBSERVE"

    admissible_paths = [
        item["path_id"]
        for item in path_results
        if item["path_action"] <= 0.45 and item["evidence_sufficiency"] >= 0.55
    ]
    receipt = {
        "version": RECEIPT_VERSION,
        "source_bundle_digest": digest_payload(bundle),
        "query_id": bundle["query_id"],
        "query_digest": bundle["query_digest"],
        "route": route,
        "path_results": path_results,
        "cycle_results": cycle_results,
        "admissible_paths": admissible_paths,
        "plurality_preserved": len(path_results) > 1,
        "max_curvature_residual": max_curvature,
        "max_path_action": max_action,
        "minimum_evidence_sufficiency": min_evidence,
        "next_observation_target": _next_observation_target(path_results, cycle_results, qi),
        "process_tensor_digest": qi["process_tensor_digest"],
        "history_window_digest": qi["history_window_digest"],
        "boundary": deepcopy(REQUIRED_BOUNDARY),
        "non_authority": deepcopy(NON_AUTHORITY),
        "receipt_digest": "",
    }
    receipt["receipt_digest"] = digest_payload({k: v for k, v in receipt.items() if k != "receipt_digest"})
    return receipt


def gauge_transform_bundle(
    bundle: Mapping[str, Any], gauges: Mapping[str, Sequence[Sequence[float]]]
) -> dict[str, Any]:
    transformed = deepcopy(bundle)
    patch_ids = {patch["patch_id"] for patch in transformed["patches"]}
    if set(gauges) != patch_ids:
        raise ValueError("gauges_must_cover_exactly_all_patches")
    checked_gauges: dict[str, list[list[float]]] = {}
    for patch_id, matrix in gauges.items():
        checked = _matrix2(matrix, f"gauge_{patch_id}")
        if orthogonality_residual(checked) > 1e-6:
            raise ValueError(f"gauge_{patch_id}_must_be_orthogonal")
        checked_gauges[patch_id] = checked

    for patch in transformed["patches"]:
        patch["local_vector"] = matvec2(checked_gauges[patch["patch_id"]], patch["local_vector"])
    for connection in transformed["connections"]:
        source_gauge_inverse = transpose2(checked_gauges[connection["source_patch"]])
        target_gauge = checked_gauges[connection["target_patch"]]
        connection["transport"] = matmul2(
            matmul2(target_gauge, connection["transport"]), source_gauge_inverse
        )
    return transformed


def build_evidence_bundle(
    *,
    query_id: str,
    query_text: str,
    patches: Sequence[Mapping[str, Any]],
    connections: Sequence[Mapping[str, Any]],
    declared_paths: Sequence[Mapping[str, Any]],
    declared_cycles: Sequence[Mapping[str, Any]],
    qi_process: Mapping[str, Any],
) -> dict[str, Any]:
    bundle = {
        "version": VERSION,
        "query_id": _nonempty(query_id, "query_id"),
        "query_text": _nonempty(query_text, "query_text"),
        "query_digest": digest_payload(query_text),
        "patches": deepcopy(list(patches)),
        "connections": deepcopy(list(connections)),
        "declared_paths": deepcopy(list(declared_paths)),
        "declared_cycles": deepcopy(list(declared_cycles)),
        "qi_process": deepcopy(dict(qi_process)),
        "boundary": deepcopy(REQUIRED_BOUNDARY),
    }
    errors = validate_bundle(bundle)
    if errors:
        raise ValueError(";".join(errors))
    return bundle
