from __future__ import annotations

from typing import Any

from runtime.kuuos_planos_smith_normal_form_integer_homology_certificate_support_v0_1 import (
    canonical_digest,
    divisibility_chain,
)


def _nat(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _unique(value: Any, seen: set[str], invalid: str, duplicate: str):
    if not isinstance(value, str) or not value:
        return False, invalid
    if value in seen:
        return False, duplicate
    seen.add(value)
    return True, ""


def normalize_vertices(values: Any, maximum: int):
    if not isinstance(values, list) or not values:
        return ["filtered_vertex_records_empty"], []
    fields = {"vertex_id", "filtration", "source_vertex_digest"}
    blockers, out, ids, digests = [], [], set(), set()
    for index, item in enumerate(values):
        if not isinstance(item, dict) or set(item) != fields:
            blockers.append(f"filtered_vertex_schema_invalid_{index}")
            continue
        vertex_id = item["vertex_id"]
        ok, reason = _unique(vertex_id, ids, f"filtered_vertex_id_invalid_{index}", "duplicate_filtered_vertex_id")
        if not ok:
            blockers.append(reason)
            continue
        filtration = item["filtration"]
        if not _nat(filtration) or filtration > maximum:
            blockers.append(f"filtered_vertex_filtration_invalid_{vertex_id}")
            continue
        digest = item["source_vertex_digest"]
        ok, reason = _unique(digest, digests, f"source_filtered_vertex_digest_missing_{vertex_id}", "duplicate_source_filtered_vertex_digest")
        if not ok:
            blockers.append(reason)
        out.append({"vertex_id": vertex_id, "filtration": filtration, "source_vertex_digest": digest})
    return blockers, sorted(out, key=lambda item: item["vertex_id"])


def normalize_edges(values: Any, maximum: int):
    if not isinstance(values, list):
        return ["filtered_edge_records_not_list"], []
    fields = {"edge_id", "vertex_ids", "filtration", "source_edge_digest"}
    blockers, out, ids, pairs, digests = [], [], set(), set(), set()
    for index, item in enumerate(values):
        if not isinstance(item, dict) or set(item) != fields:
            blockers.append(f"filtered_edge_schema_invalid_{index}")
            continue
        edge_id = item["edge_id"]
        ok, reason = _unique(edge_id, ids, f"filtered_edge_id_invalid_{index}", "duplicate_filtered_edge_id")
        if not ok:
            blockers.append(reason)
            continue
        vertices = item["vertex_ids"]
        if not isinstance(vertices, list) or len(vertices) != 2 or any(not isinstance(v, str) or not v for v in vertices) or len(set(vertices)) != 2:
            blockers.append(f"filtered_edge_vertices_invalid_{edge_id}")
            continue
        pair = tuple(sorted(vertices))
        if pair in pairs:
            blockers.append("duplicate_filtered_unoriented_edge")
        pairs.add(pair)
        filtration = item["filtration"]
        if not _nat(filtration) or filtration > maximum:
            blockers.append(f"filtered_edge_filtration_invalid_{edge_id}")
            continue
        digest = item["source_edge_digest"]
        ok, reason = _unique(digest, digests, f"source_filtered_edge_digest_missing_{edge_id}", "duplicate_source_filtered_edge_digest")
        if not ok:
            blockers.append(reason)
        out.append({"edge_id": edge_id, "vertex_ids": list(pair), "filtration": filtration, "source_edge_digest": digest})
    return blockers, sorted(out, key=lambda item: item["edge_id"])


def normalize_triangles(values: Any, maximum: int):
    if not isinstance(values, list):
        return ["filtered_triangle_records_not_list"], []
    fields = {"triangle_id", "vertex_ids", "filtration", "source_triangle_digest"}
    blockers, out, ids, triples, digests = [], [], set(), set(), set()
    for index, item in enumerate(values):
        if not isinstance(item, dict) or set(item) != fields:
            blockers.append(f"filtered_triangle_schema_invalid_{index}")
            continue
        triangle_id = item["triangle_id"]
        ok, reason = _unique(triangle_id, ids, f"filtered_triangle_id_invalid_{index}", "duplicate_filtered_triangle_id")
        if not ok:
            blockers.append(reason)
            continue
        vertices = item["vertex_ids"]
        if not isinstance(vertices, list) or len(vertices) != 3 or any(not isinstance(v, str) or not v for v in vertices) or len(set(vertices)) != 3:
            blockers.append(f"filtered_triangle_vertices_invalid_{triangle_id}")
            continue
        triple = tuple(sorted(vertices))
        if triple in triples:
            blockers.append("duplicate_filtered_unoriented_triangle")
        triples.add(triple)
        filtration = item["filtration"]
        if not _nat(filtration) or filtration > maximum:
            blockers.append(f"filtered_triangle_filtration_invalid_{triangle_id}")
            continue
        digest = item["source_triangle_digest"]
        ok, reason = _unique(digest, digests, f"source_filtered_triangle_digest_missing_{triangle_id}", "duplicate_source_filtered_triangle_digest")
        if not ok:
            blockers.append(reason)
        out.append({"triangle_id": triangle_id, "vertex_ids": list(triple), "filtration": filtration, "source_triangle_digest": digest})
    return blockers, sorted(out, key=lambda item: item["triangle_id"])


def normalize_filtration_stages(values: Any, maximum: int):
    if not isinstance(values, list) or not values or any(not _nat(v) or v > maximum for v in values) or values != sorted(set(values)):
        return ["filtration_stages_invalid"], []
    return [], list(values)


def normalize_stage_claims(values: Any):
    fields = {"stage", "vertex_count", "edge_count", "triangle_count", "h0_free_rank", "h1_free_rank", "h2_free_rank", "h1_smith_diagonal", "h1_torsion_invariant_factors"}
    if not isinstance(values, list) or not values:
        return ["stage_smith_claims_empty"], []
    blockers, out, seen = [], [], set()
    for index, item in enumerate(values):
        if not isinstance(item, dict) or set(item) != fields:
            blockers.append(f"stage_smith_claim_schema_invalid_{index}")
            continue
        stage = item["stage"]
        if not _nat(stage):
            blockers.append(f"stage_smith_claim_stage_invalid_{index}")
            continue
        if stage in seen:
            blockers.append("duplicate_stage_smith_claim")
        seen.add(stage)
        numeric = fields - {"h1_smith_diagonal", "h1_torsion_invariant_factors"}
        if any(not _nat(item[name]) for name in numeric):
            blockers.append(f"stage_smith_claim_numeric_field_invalid_{stage}")
            continue
        diagonal, torsion = item["h1_smith_diagonal"], item["h1_torsion_invariant_factors"]
        if not isinstance(diagonal, list) or any(not isinstance(v, int) or isinstance(v, bool) or v <= 0 for v in diagonal) or not divisibility_chain(diagonal):
            blockers.append(f"stage_smith_diagonal_invalid_{stage}")
            continue
        if not isinstance(torsion, list) or torsion != [v for v in diagonal if v > 1]:
            blockers.append(f"stage_torsion_factors_invalid_{stage}")
            continue
        out.append({name: (list(item[name]) if name in {"h1_smith_diagonal", "h1_torsion_invariant_factors"} else item[name]) for name in fields})
    return blockers, sorted(out, key=lambda item: item["stage"])


def normalize_barcode_claims(values: Any):
    fields = {"interval_id", "dimension", "birth", "death", "birth_simplex_id", "death_simplex_id"}
    if not isinstance(values, list) or not values:
        return ["barcode_interval_claims_empty"], []
    blockers, out, seen = [], [], set()
    for index, item in enumerate(values):
        if not isinstance(item, dict) or set(item) != fields:
            blockers.append(f"barcode_interval_claim_schema_invalid_{index}")
            continue
        interval_id = item["interval_id"]
        ok, reason = _unique(interval_id, seen, f"barcode_interval_id_invalid_{index}", "duplicate_barcode_interval_id")
        if not ok:
            blockers.append(reason)
            continue
        dimension, birth, death = item["dimension"], item["birth"], item["death"]
        if not _nat(dimension) or dimension > 2 or not _nat(birth) or (death is not None and (not _nat(death) or death <= birth)):
            blockers.append(f"barcode_interval_numeric_invalid_{interval_id}")
            continue
        birth_id, death_id = item["birth_simplex_id"], item["death_simplex_id"]
        if not isinstance(birth_id, str) or not birth_id or not isinstance(death_id, str) or (death is None) != (death_id == ""):
            blockers.append(f"barcode_simplex_binding_invalid_{interval_id}")
            continue
        out.append(dict(item))
    key = lambda item: (item["dimension"], item["birth"], item["death"] is None, item["death"] if item["death"] is not None else 10**18, item["birth_simplex_id"])
    return blockers, sorted(out, key=key)


def normalize_persistent_betti_claims(values: Any):
    fields = {"stage", "beta0", "beta1", "beta2"}
    if not isinstance(values, list) or not values:
        return ["persistent_betti_claims_empty"], []
    blockers, out, seen = [], [], set()
    for index, item in enumerate(values):
        if not isinstance(item, dict) or set(item) != fields or any(not _nat(item.get(name)) for name in fields):
            blockers.append(f"persistent_betti_claim_invalid_{index}")
            continue
        if item["stage"] in seen:
            blockers.append("duplicate_persistent_betti_stage")
        seen.add(item["stage"])
        out.append(dict(item))
    return blockers, sorted(out, key=lambda item: item["stage"])


def compute_persistent_homology_input_digest(**payload):
    return canonical_digest(payload)
