from __future__ import annotations

from runtime.kuuos_planos_smith_normal_form_integer_homology_certificate_support_v0_1 import (
    boundary_matrices,
    cycle_presentation_matrix,
    divisibility_chain,
    rational_rank,
    smith_normal_form_diagonal,
    spanning_forest_cycle_basis,
)


def validate_face_closure_and_filtration(vertices, edges, triangles):
    blockers: list[str] = []
    vertex_filtration = {item["vertex_id"]: item["filtration"] for item in vertices}
    edge_by_pair = {tuple(item["vertex_ids"]): item for item in edges}
    for edge in edges:
        for vertex in edge["vertex_ids"]:
            if vertex not in vertex_filtration:
                blockers.append(f"filtered_edge_vertex_missing_{edge['edge_id']}_{vertex}")
            elif vertex_filtration[vertex] > edge["filtration"]:
                blockers.append(f"filtered_edge_precedes_vertex_{edge['edge_id']}_{vertex}")
    for triangle in triangles:
        a, b, c = triangle["vertex_ids"]
        for pair in ((a, b), (a, c), (b, c)):
            edge = edge_by_pair.get(tuple(sorted(pair)))
            if edge is None:
                blockers.append(f"filtered_triangle_boundary_edge_missing_{triangle['triangle_id']}_{pair[0]}_{pair[1]}")
            elif edge["filtration"] > triangle["filtration"]:
                blockers.append(f"filtered_triangle_precedes_edge_{triangle['triangle_id']}_{edge['edge_id']}")
    return blockers


def compute_stage_smith_data(vertices, edges, triangles, stages):
    output: list[dict] = []
    for stage in stages:
        active_vertices = [item for item in vertices if item["filtration"] <= stage]
        active_edges = [item for item in edges if item["filtration"] <= stage]
        active_triangles = [item for item in triangles if item["filtration"] <= stage]
        missing, boundary_one, boundary_two = boundary_matrices(active_vertices, active_edges, active_triangles)
        if missing:
            raise ValueError("stage_triangle_boundary_edge_missing")
        rank_one, rank_two = rational_rank(boundary_one), rational_rank(boundary_two)
        cycles = spanning_forest_cycle_basis(active_vertices, active_edges)
        presentation, reconstructed = cycle_presentation_matrix(active_edges, active_triangles, boundary_two, cycles)
        for column, vector in enumerate(reconstructed):
            if vector != [row[column] for row in boundary_two]:
                raise ValueError("stage_triangle_boundary_reconstruction_mismatch")
        diagonal, _ = smith_normal_form_diagonal(presentation)
        if not divisibility_chain(diagonal):
            raise ValueError("stage_smith_divisibility_chain_invalid")
        output.append({
            "stage": stage,
            "vertex_count": len(active_vertices),
            "edge_count": len(active_edges),
            "triangle_count": len(active_triangles),
            "h0_free_rank": len(active_vertices) - rank_one,
            "h1_free_rank": len(cycles["cycle_basis"]) - len(diagonal),
            "h2_free_rank": len(active_triangles) - rank_two,
            "h1_smith_diagonal": diagonal,
            "h1_torsion_invariant_factors": [value for value in diagonal if value > 1],
        })
    return output


def filtration_order(vertices, edges, triangles):
    simplices = [
        {"simplex_id": f"vertex-{item['vertex_id']}", "dimension": 0, "filtration": item["filtration"], "vertices": [item["vertex_id"]]}
        for item in vertices
    ]
    simplices += [
        {"simplex_id": item["edge_id"], "dimension": 1, "filtration": item["filtration"], "vertices": list(item["vertex_ids"])}
        for item in edges
    ]
    simplices += [
        {"simplex_id": item["triangle_id"], "dimension": 2, "filtration": item["filtration"], "vertices": list(item["vertex_ids"])}
        for item in triangles
    ]
    return sorted(simplices, key=lambda item: (item["filtration"], item["dimension"], item["simplex_id"]))


def persistent_barcode_f2(vertices, edges, triangles):
    simplices = filtration_order(vertices, edges, triangles)
    index_by_id = {item["simplex_id"]: index for index, item in enumerate(simplices)}
    vertex_ids = {item["vertex_id"]: f"vertex-{item['vertex_id']}" for item in vertices}
    edge_by_pair = {tuple(item["vertex_ids"]): item["edge_id"] for item in edges}
    boundaries: list[set[int]] = []
    for simplex in simplices:
        if simplex["dimension"] == 0:
            boundary: set[int] = set()
        elif simplex["dimension"] == 1:
            boundary = {index_by_id[vertex_ids[vertex]] for vertex in simplex["vertices"]}
        else:
            a, b, c = simplex["vertices"]
            boundary = {index_by_id[edge_by_pair[tuple(sorted(pair))]] for pair in ((a, b), (a, c), (b, c))}
        if any(index >= len(boundaries) for index in boundary):
            raise ValueError("filtration_boundary_not_preceding_simplex")
        boundaries.append(boundary)

    reduced: list[set[int]] = []
    pivot_to_column: dict[int, int] = {}
    for original in boundaries:
        column = set(original)
        while column and max(column) in pivot_to_column:
            column ^= reduced[pivot_to_column[max(column)]]
        if column:
            pivot_to_column[max(column)] = len(reduced)
        reduced.append(column)

    intervals: list[dict] = []
    for birth_index, column in enumerate(reduced):
        if column:
            continue
        birth_simplex = simplices[birth_index]
        death_index = pivot_to_column.get(birth_index)
        death_simplex = simplices[death_index] if death_index is not None else None
        death = death_simplex["filtration"] if death_simplex is not None else None
        if death is not None and death <= birth_simplex["filtration"]:
            raise ValueError("nonpositive_persistence_interval")
        death_id = death_simplex["simplex_id"] if death_simplex is not None else ""
        intervals.append({
            "interval_id": f"H{birth_simplex['dimension']}:{birth_simplex['simplex_id']}->{death_id or 'inf'}",
            "dimension": birth_simplex["dimension"],
            "birth": birth_simplex["filtration"],
            "death": death,
            "birth_simplex_id": birth_simplex["simplex_id"],
            "death_simplex_id": death_id,
        })
    key = lambda item: (item["dimension"], item["birth"], item["death"] is None, item["death"] if item["death"] is not None else 10**18, item["birth_simplex_id"])
    return simplices, reduced, sorted(intervals, key=key)


def persistent_betti_from_barcode(intervals, stages):
    return [
        {
            "stage": stage,
            **{
                f"beta{dimension}": sum(
                    1 for interval in intervals
                    if interval["dimension"] == dimension
                    and interval["birth"] <= stage
                    and (interval["death"] is None or stage < interval["death"])
                )
                for dimension in range(3)
            },
        }
        for stage in stages
    ]
