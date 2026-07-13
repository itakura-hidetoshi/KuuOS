from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from typing import Any, Sequence


def canonical_digest(value: Any) -> str:
    return sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
    ).hexdigest()


def canonical_edge(vertices: Sequence[str]) -> tuple[str, str]:
    left, right = sorted(vertices)
    return left, right


def triangle_boundary_pairs(vertices: Sequence[str]) -> dict[tuple[str, str], int]:
    first, second, third = sorted(vertices)
    return {
        canonical_edge((first, second)): 1,
        canonical_edge((first, third)): -1,
        canonical_edge((second, third)): 1,
    }


def _unique_string(value: Any, seen: set[str], invalid: str, duplicate: str):
    if not isinstance(value, str) or not value:
        return False, invalid
    if value in seen:
        return False, duplicate
    seen.add(value)
    return True, ""


def normalize_vertices(values: Any):
    if not isinstance(values, list) or len(values) < 2:
        return ["vertex_records_insufficient"], []
    fields = {"vertex_id", "source_vertex_digest"}
    blockers: list[str] = []
    out: list[dict] = []
    seen_ids: set[str] = set()
    seen_digests: set[str] = set()
    for index, item in enumerate(values):
        if not isinstance(item, dict) or set(item) != fields:
            blockers.append(f"vertex_schema_invalid_{index}")
            continue
        vertex_id = item["vertex_id"]
        ok, reason = _unique_string(
            vertex_id,
            seen_ids,
            f"vertex_id_invalid_{index}",
            "duplicate_vertex_id",
        )
        if not ok:
            blockers.append(reason)
            continue
        digest = item["source_vertex_digest"]
        ok, reason = _unique_string(
            digest,
            seen_digests,
            f"source_vertex_digest_missing_{vertex_id}",
            "duplicate_source_vertex_digest",
        )
        if not ok:
            blockers.append(reason)
        out.append({"vertex_id": vertex_id, "source_vertex_digest": digest})
    return blockers, sorted(out, key=lambda item: item["vertex_id"])


def normalize_edges(values: Any):
    if not isinstance(values, list) or not values:
        return ["oriented_edge_records_empty"], []
    fields = {"edge_id", "vertex_ids", "source_edge_digest"}
    blockers: list[str] = []
    out: list[dict] = []
    seen_ids: set[str] = set()
    seen_pairs: set[tuple[str, str]] = set()
    seen_digests: set[str] = set()
    for index, item in enumerate(values):
        if not isinstance(item, dict) or set(item) != fields:
            blockers.append(f"oriented_edge_schema_invalid_{index}")
            continue
        edge_id = item["edge_id"]
        ok, reason = _unique_string(
            edge_id,
            seen_ids,
            f"edge_id_invalid_{index}",
            "duplicate_edge_id",
        )
        if not ok:
            blockers.append(reason)
            continue
        vertices = item["vertex_ids"]
        if (
            not isinstance(vertices, list)
            or len(vertices) != 2
            or any(not isinstance(v, str) or not v for v in vertices)
            or len(set(vertices)) != 2
        ):
            blockers.append(f"edge_vertices_invalid_{edge_id}")
            continue
        pair = canonical_edge(vertices)
        if pair in seen_pairs:
            blockers.append("duplicate_unoriented_edge")
        seen_pairs.add(pair)
        digest = item["source_edge_digest"]
        ok, reason = _unique_string(
            digest,
            seen_digests,
            f"source_edge_digest_missing_{edge_id}",
            "duplicate_source_edge_digest",
        )
        if not ok:
            blockers.append(reason)
        out.append(
            {
                "edge_id": edge_id,
                "vertex_ids": list(pair),
                "source_edge_digest": digest,
            }
        )
    return blockers, sorted(out, key=lambda item: item["edge_id"])


def normalize_triangles(values: Any):
    if not isinstance(values, list) or not values:
        return ["oriented_triangle_records_empty"], []
    fields = {"triangle_id", "vertex_ids", "source_triangle_digest"}
    blockers: list[str] = []
    out: list[dict] = []
    seen_ids: set[str] = set()
    seen_vertices: set[tuple[str, str, str]] = set()
    seen_digests: set[str] = set()
    for index, item in enumerate(values):
        if not isinstance(item, dict) or set(item) != fields:
            blockers.append(f"oriented_triangle_schema_invalid_{index}")
            continue
        triangle_id = item["triangle_id"]
        ok, reason = _unique_string(
            triangle_id,
            seen_ids,
            f"triangle_id_invalid_{index}",
            "duplicate_triangle_id",
        )
        if not ok:
            blockers.append(reason)
            continue
        vertices = item["vertex_ids"]
        if (
            not isinstance(vertices, list)
            or len(vertices) != 3
            or any(not isinstance(v, str) or not v for v in vertices)
            or len(set(vertices)) != 3
        ):
            blockers.append(f"triangle_vertices_invalid_{triangle_id}")
            continue
        canonical = tuple(sorted(vertices))
        if canonical in seen_vertices:
            blockers.append("duplicate_unoriented_triangle")
        seen_vertices.add(canonical)
        digest = item["source_triangle_digest"]
        ok, reason = _unique_string(
            digest,
            seen_digests,
            f"source_triangle_digest_missing_{triangle_id}",
            "duplicate_source_triangle_digest",
        )
        if not ok:
            blockers.append(reason)
        out.append(
            {
                "triangle_id": triangle_id,
                "vertex_ids": list(canonical),
                "source_triangle_digest": digest,
            }
        )
    return blockers, sorted(out, key=lambda item: item["triangle_id"])


def _normalize_coefficients(
    value: Any,
    basis_ids: Sequence[str],
    maximum_absolute_coefficient: int,
    prefix: str,
):
    if not isinstance(value, dict):
        return [f"{prefix}_coefficients_schema_invalid"], {}
    unknown = set(value) - set(basis_ids)
    if unknown:
        return [f"{prefix}_unknown_basis_id"], {}
    blockers: list[str] = []
    out: dict[str, int] = {}
    for basis_id in basis_ids:
        coefficient = value.get(basis_id, 0)
        if not isinstance(coefficient, int) or isinstance(coefficient, bool):
            blockers.append(f"{prefix}_coefficient_not_integer_{basis_id}")
            continue
        if abs(coefficient) > maximum_absolute_coefficient:
            blockers.append(f"{prefix}_coefficient_bound_exceeded_{basis_id}")
        out[basis_id] = coefficient
    return blockers, out


def normalize_one_chains(values: Any, edge_ids: Sequence[str], maximum: int):
    if not isinstance(values, list) or len(values) < 2:
        return ["one_chain_records_insufficient"], []
    fields = {"chain_id", "edge_coefficients", "chain_role", "source_chain_digest"}
    roles = {"exact_cycle", "nontrivial_cycle"}
    blockers: list[str] = []
    out: list[dict] = []
    seen_ids: set[str] = set()
    seen_digests: set[str] = set()
    for index, item in enumerate(values):
        if not isinstance(item, dict) or set(item) != fields:
            blockers.append(f"one_chain_schema_invalid_{index}")
            continue
        chain_id = item["chain_id"]
        ok, reason = _unique_string(
            chain_id,
            seen_ids,
            f"one_chain_id_invalid_{index}",
            "duplicate_one_chain_id",
        )
        if not ok:
            blockers.append(reason)
            continue
        role = item["chain_role"]
        if role not in roles:
            blockers.append(f"one_chain_role_invalid_{chain_id}")
        digest = item["source_chain_digest"]
        ok, reason = _unique_string(
            digest,
            seen_digests,
            f"source_one_chain_digest_missing_{chain_id}",
            "duplicate_source_one_chain_digest",
        )
        if not ok:
            blockers.append(reason)
        errors, coefficients = _normalize_coefficients(
            item["edge_coefficients"], edge_ids, maximum, f"one_chain_{chain_id}"
        )
        blockers.extend(errors)
        if not errors:
            out.append(
                {
                    "chain_id": chain_id,
                    "edge_coefficients": coefficients,
                    "chain_role": role,
                    "source_chain_digest": digest,
                }
            )
    return blockers, sorted(out, key=lambda item: item["chain_id"])


def normalize_two_chains(values: Any, triangle_ids: Sequence[str], maximum: int):
    if not isinstance(values, list) or not values:
        return ["two_chain_records_empty"], []
    fields = {"chain_id", "triangle_coefficients", "source_chain_digest"}
    blockers: list[str] = []
    out: list[dict] = []
    seen_ids: set[str] = set()
    seen_digests: set[str] = set()
    for index, item in enumerate(values):
        if not isinstance(item, dict) or set(item) != fields:
            blockers.append(f"two_chain_schema_invalid_{index}")
            continue
        chain_id = item["chain_id"]
        ok, reason = _unique_string(
            chain_id,
            seen_ids,
            f"two_chain_id_invalid_{index}",
            "duplicate_two_chain_id",
        )
        if not ok:
            blockers.append(reason)
            continue
        digest = item["source_chain_digest"]
        ok, reason = _unique_string(
            digest,
            seen_digests,
            f"source_two_chain_digest_missing_{chain_id}",
            "duplicate_source_two_chain_digest",
        )
        if not ok:
            blockers.append(reason)
        errors, coefficients = _normalize_coefficients(
            item["triangle_coefficients"],
            triangle_ids,
            maximum,
            f"two_chain_{chain_id}",
        )
        blockers.extend(errors)
        if not errors:
            out.append(
                {
                    "chain_id": chain_id,
                    "triangle_coefficients": coefficients,
                    "source_chain_digest": digest,
                }
            )
    return blockers, sorted(out, key=lambda item: item["chain_id"])


def normalize_witnesses(values: Any, kind: str):
    if not isinstance(values, list) or not values:
        return [f"{kind}_witnesses_empty"], []
    if kind == "exactness":
        fields = {
            "witness_id",
            "one_chain_id",
            "two_chain_id",
            "source_witness_digest",
        }
    else:
        fields = {
            "witness_id",
            "one_chain_id",
            "coefficient_field",
            "source_witness_digest",
        }
    blockers: list[str] = []
    out: list[dict] = []
    seen_ids: set[str] = set()
    seen_digests: set[str] = set()
    for index, item in enumerate(values):
        if not isinstance(item, dict) or set(item) != fields:
            blockers.append(f"{kind}_witness_schema_invalid_{index}")
            continue
        witness_id = item["witness_id"]
        ok, reason = _unique_string(
            witness_id,
            seen_ids,
            f"{kind}_witness_id_invalid_{index}",
            f"duplicate_{kind}_witness_id",
        )
        if not ok:
            blockers.append(reason)
            continue
        for name in fields - {"source_witness_digest"}:
            if name == "witness_id":
                continue
            if not isinstance(item[name], str) or not item[name]:
                blockers.append(f"{kind}_{name}_invalid_{witness_id}")
        if kind == "nontriviality" and item["coefficient_field"] != "Q":
            blockers.append(f"nontriviality_coefficient_field_invalid_{witness_id}")
        digest = item["source_witness_digest"]
        ok, reason = _unique_string(
            digest,
            seen_digests,
            f"source_{kind}_witness_digest_missing_{witness_id}",
            f"duplicate_source_{kind}_witness_digest",
        )
        if not ok:
            blockers.append(reason)
        out.append(dict(item))
    return blockers, sorted(out, key=lambda item: item["witness_id"])


def boundary_matrices(vertices: Sequence[dict], edges: Sequence[dict], triangles: Sequence[dict]):
    vertex_ids = [item["vertex_id"] for item in vertices]
    edge_ids = [item["edge_id"] for item in edges]
    edge_index = {edge_id: index for index, edge_id in enumerate(edge_ids)}
    edge_by_pair = {tuple(edge["vertex_ids"]): edge["edge_id"] for edge in edges}
    boundary_one = [[0 for _ in edges] for _ in vertices]
    vertex_index = {vertex_id: index for index, vertex_id in enumerate(vertex_ids)}
    for column, edge in enumerate(edges):
        source, target = edge["vertex_ids"]
        boundary_one[vertex_index[source]][column] = -1
        boundary_one[vertex_index[target]][column] = 1

    boundary_two = [[0 for _ in triangles] for _ in edges]
    missing_boundaries: list[str] = []
    for column, triangle in enumerate(triangles):
        coefficients = triangle_boundary_pairs(triangle["vertex_ids"])
        for pair, coefficient in coefficients.items():
            edge_id = edge_by_pair.get(pair)
            if edge_id is None:
                missing_boundaries.append(
                    f"triangle_boundary_edge_missing_{triangle['triangle_id']}_{pair[0]}_{pair[1]}"
                )
                continue
            boundary_two[edge_index[edge_id]][column] = coefficient
    return missing_boundaries, boundary_one, boundary_two


def matrix_multiply(left: Sequence[Sequence[int]], right: Sequence[Sequence[int]]):
    if not left:
        return []
    if not right:
        return [[] for _ in left]
    shared = len(right)
    columns = len(right[0])
    return [
        [sum(left[i][k] * right[k][j] for k in range(shared)) for j in range(columns)]
        for i in range(len(left))
    ]


def matrix_vector(matrix: Sequence[Sequence[int]], vector: Sequence[int]):
    return [sum(entry * coefficient for entry, coefficient in zip(row, vector)) for row in matrix]


def rational_rank(matrix: Sequence[Sequence[int | Fraction]]) -> int:
    rows = [list(map(Fraction, row)) for row in matrix]
    if not rows:
        return 0
    row_count = len(rows)
    column_count = len(rows[0]) if rows else 0
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if rows[row][column] != 0),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        pivot_value = rows[pivot_row][column]
        rows[pivot_row] = [value / pivot_value for value in rows[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or rows[row][column] == 0:
                continue
            factor = rows[row][column]
            rows[row] = [
                rows[row][index] - factor * rows[pivot_row][index]
                for index in range(column_count)
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def augment_with_column(matrix: Sequence[Sequence[int]], column: Sequence[int]):
    return [list(row) + [column[index]] for index, row in enumerate(matrix)]


def compute_chain_complex_input_digest(
    *,
    vertex_records,
    oriented_edge_records,
    oriented_triangle_records,
    one_chain_records,
    two_chain_records,
    exactness_witnesses,
    nontriviality_witnesses,
):
    return canonical_digest(
        {
            "vertex_records": vertex_records,
            "oriented_edge_records": oriented_edge_records,
            "oriented_triangle_records": oriented_triangle_records,
            "one_chain_records": one_chain_records,
            "two_chain_records": two_chain_records,
            "exactness_witnesses": exactness_witnesses,
            "nontriviality_witnesses": nontriviality_witnesses,
        }
    )
