from __future__ import annotations

from collections import deque
from typing import Sequence

from runtime.kuuos_planos_finite_simplicial_chain_homology_certificate_support_v0_1 import (
    boundary_matrices,
    canonical_digest,
    matrix_multiply,
    matrix_vector,
    normalize_edges,
    normalize_triangles,
    normalize_vertices,
    rational_rank,
)

__all__ = [
    "boundary_matrices",
    "canonical_digest",
    "compute_smith_input_digest",
    "cycle_presentation_matrix",
    "divisibility_chain",
    "matrix_multiply",
    "matrix_vector",
    "normalize_edges",
    "normalize_triangles",
    "normalize_vertices",
    "rational_rank",
    "smith_normal_form_diagonal",
    "spanning_forest_cycle_basis",
]


def _swap_rows(matrix: list[list[int]], left: int, right: int) -> None:
    matrix[left], matrix[right] = matrix[right], matrix[left]


def _swap_columns(matrix: list[list[int]], left: int, right: int) -> None:
    for row in matrix:
        row[left], row[right] = row[right], row[left]


def _add_row_multiple(matrix: list[list[int]], target: int, source: int, factor: int) -> None:
    matrix[target] = [
        value + factor * source_value
        for value, source_value in zip(matrix[target], matrix[source])
    ]


def _add_column_multiple(
    matrix: list[list[int]], target: int, source: int, factor: int
) -> None:
    for row in matrix:
        row[target] += factor * row[source]


def smith_normal_form_diagonal(
    matrix: Sequence[Sequence[int]],
) -> tuple[list[int], list[list[int]]]:
    """Diagonalize an integer matrix using unimodular row and column operations."""

    work = [list(map(int, row)) for row in matrix]
    row_count = len(work)
    column_count = len(work[0]) if work else 0
    if any(len(row) != column_count for row in work):
        raise ValueError("ragged_integer_matrix")

    pivot_index = 0
    while pivot_index < row_count and pivot_index < column_count:
        position = None
        for row in range(pivot_index, row_count):
            for column in range(pivot_index, column_count):
                if work[row][column] != 0 and (
                    position is None
                    or abs(work[row][column])
                    < abs(work[position[0]][position[1]])
                ):
                    position = (row, column)
        if position is None:
            break
        _swap_rows(work, pivot_index, position[0])
        _swap_columns(work, pivot_index, position[1])

        while True:
            changed = False
            pivot = work[pivot_index][pivot_index]
            for row in range(pivot_index + 1, row_count):
                if work[row][pivot_index] == 0:
                    continue
                quotient = work[row][pivot_index] // pivot
                _add_row_multiple(work, row, pivot_index, -quotient)
                if work[row][pivot_index] != 0 and abs(work[row][pivot_index]) < abs(
                    work[pivot_index][pivot_index]
                ):
                    _swap_rows(work, row, pivot_index)
                changed = True
                break
            if changed:
                continue

            pivot = work[pivot_index][pivot_index]
            for column in range(pivot_index + 1, column_count):
                if work[pivot_index][column] == 0:
                    continue
                quotient = work[pivot_index][column] // pivot
                _add_column_multiple(work, column, pivot_index, -quotient)
                if work[pivot_index][column] != 0 and abs(
                    work[pivot_index][column]
                ) < abs(work[pivot_index][pivot_index]):
                    _swap_columns(work, column, pivot_index)
                changed = True
                break
            if changed:
                continue

            pivot = work[pivot_index][pivot_index]
            offending = None
            for row in range(pivot_index + 1, row_count):
                for column in range(pivot_index + 1, column_count):
                    if work[row][column] % pivot != 0:
                        offending = (row, column)
                        break
                if offending is not None:
                    break
            if offending is None:
                break
            _add_row_multiple(work, pivot_index, offending[0], 1)

        if work[pivot_index][pivot_index] < 0:
            work[pivot_index] = [-value for value in work[pivot_index]]
        pivot_index += 1

    diagonal = [
        abs(work[index][index])
        for index in range(min(row_count, column_count))
        if work[index][index] != 0
    ]
    return diagonal, work


def divisibility_chain(values: Sequence[int]) -> bool:
    return all(value > 0 for value in values) and all(
        right % left == 0 for left, right in zip(values, values[1:])
    )


def spanning_forest_cycle_basis(vertices: Sequence[dict], edges: Sequence[dict]):
    vertex_ids = [item["vertex_id"] for item in vertices]
    edge_ids = [item["edge_id"] for item in edges]
    edge_index = {edge_id: index for index, edge_id in enumerate(edge_ids)}
    parent = {vertex_id: vertex_id for vertex_id in vertex_ids}
    rank = {vertex_id: 0 for vertex_id in vertex_ids}

    def find(vertex: str) -> str:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    def union(left: str, right: str) -> bool:
        root_left, root_right = find(left), find(right)
        if root_left == root_right:
            return False
        if rank[root_left] < rank[root_right]:
            root_left, root_right = root_right, root_left
        parent[root_right] = root_left
        if rank[root_left] == rank[root_right]:
            rank[root_left] += 1
        return True

    tree_edges: list[dict] = []
    chord_edges: list[dict] = []
    for edge in sorted(edges, key=lambda item: item["edge_id"]):
        left, right = edge["vertex_ids"]
        if union(left, right):
            tree_edges.append(edge)
        else:
            chord_edges.append(edge)

    adjacency: dict[str, list[tuple[str, dict]]] = {vertex: [] for vertex in vertex_ids}
    for edge in tree_edges:
        left, right = edge["vertex_ids"]
        adjacency[left].append((right, edge))
        adjacency[right].append((left, edge))
    for neighbors in adjacency.values():
        neighbors.sort(key=lambda item: item[1]["edge_id"])

    basis: list[dict] = []
    for chord in chord_edges:
        source, target = chord["vertex_ids"]
        predecessor: dict[str, tuple[str, dict] | None] = {target: None}
        queue = deque([target])
        while queue and source not in predecessor:
            current = queue.popleft()
            for neighbor, edge in adjacency[current]:
                if neighbor in predecessor:
                    continue
                predecessor[neighbor] = (current, edge)
                queue.append(neighbor)
        if source not in predecessor:
            raise ValueError("spanning_forest_path_missing")

        vector = [0 for _ in edges]
        vector[edge_index[chord["edge_id"]]] = 1
        current = source
        while current != target:
            previous, edge = predecessor[current]
            oriented_source, oriented_target = edge["vertex_ids"]
            vector[edge_index[edge["edge_id"]]] += (
                -1
                if (current, previous) == (oriented_source, oriented_target)
                else 1
            )
            current = previous
        basis.append(
            {
                "basis_id": f"cycle-{chord['edge_id']}",
                "chord_edge_id": chord["edge_id"],
                "edge_coefficients": {
                    edge_id: vector[index] for index, edge_id in enumerate(edge_ids)
                },
                "vector": vector,
            }
        )

    component_count = len({find(vertex) for vertex in vertex_ids})
    return {
        "tree_edge_ids": [edge["edge_id"] for edge in tree_edges],
        "chord_edge_ids": [edge["edge_id"] for edge in chord_edges],
        "connected_component_count": component_count,
        "cycle_basis": basis,
    }


def cycle_presentation_matrix(
    edges: Sequence[dict],
    triangles: Sequence[dict],
    boundary_two: Sequence[Sequence[int]],
    cycle_basis_data: dict,
):
    edge_ids = [edge["edge_id"] for edge in edges]
    edge_index = {edge_id: index for index, edge_id in enumerate(edge_ids)}
    presentation = [
        [
            boundary_two[edge_index[chord_id]][column]
            for column in range(len(triangles))
        ]
        for chord_id in cycle_basis_data["chord_edge_ids"]
    ]

    reconstructed_columns: list[list[int]] = []
    for column in range(len(triangles)):
        reconstructed = [0 for _ in edges]
        for row, basis in enumerate(cycle_basis_data["cycle_basis"]):
            coefficient = presentation[row][column]
            reconstructed = [
                value + coefficient * basis_value
                for value, basis_value in zip(reconstructed, basis["vector"])
            ]
        reconstructed_columns.append(reconstructed)
    return presentation, reconstructed_columns


def compute_smith_input_digest(
    *,
    vertex_records,
    oriented_edge_records,
    oriented_triangle_records,
    claimed_smith_diagonal,
    expected_h0_free_rank,
    expected_h1_free_rank,
    expected_h2_free_rank,
    expected_torsion_invariant_factors,
):
    return canonical_digest(
        {
            "vertex_records": vertex_records,
            "oriented_edge_records": oriented_edge_records,
            "oriented_triangle_records": oriented_triangle_records,
            "claimed_smith_diagonal": claimed_smith_diagonal,
            "expected_h0_free_rank": expected_h0_free_rank,
            "expected_h1_free_rank": expected_h1_free_rank,
            "expected_h2_free_rank": expected_h2_free_rank,
            "expected_torsion_invariant_factors": expected_torsion_invariant_factors,
        }
    )
