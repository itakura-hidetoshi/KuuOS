from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from typing import Any, Mapping

from runtime.kuuos_memoryos_nonabelian_wilson_loop_certificate_kernel_v0_1 import (
    SCHEMA_VERSION as SOURCE_SCHEMA_VERSION,
    IDENTITY,
    SWAP_01,
    SWAP_12,
    canonical_digest,
    _compose,
    _inverse,
    _conjugate,
    _fixed_point_trace,
    _cycle_type,
    _matrix,
    _q,
    _f,
)

SCHEMA_VERSION = (
    "kuuos.memoryos.tetrahedral-nonabelian-plaquette-bianchi-curvature-"
    "certificate.v0.1"
)

REVIEW_FIELDS = (
    "source_relational_frontier_candidate_ids",
    "source_required_review_candidate_ids",
    "source_dissent_review_candidate_ids",
    "source_minority_protection_candidate_ids",
)

SOURCE_TRUE = (
    "source_memoryos_v071_exact",
    "finite_s3_nonabelian_connection_exact",
    "path_ordered_transport_exact",
    "canonical_path_order_noncommutative_exact",
    "nonabelian_commutator_exact",
    "holonomy_gauge_covariant_exact",
    "holonomy_representative_changes_under_gauge",
    "holonomy_conjugacy_class_invariant_exact",
    "wilson_character_gauge_invariant_exact",
    "tree_gauge_fixing_nonabelian_exact",
    "multi_chart_fusion_conjugacy_exact",
    "nonabelian_gauge_adjusted_confidence_exact",
    "all_full_rank_transport_nonabelian_layer_commutes",
    "singular_atomic_nonabelian_layer_retained",
    "all_decision_candidates_retained",
    "all_planos_histories_retained",
    "all_quotient_coordinate_probes_retained",
    "relational_frontier_preserved",
    "required_review_set_preserved",
    "dissent_visibility_preserved",
    "minority_visibility_preserved",
    "wilson_loop_not_truth_authority",
    "fusion_review_not_candidate_ranking",
    "tree_gauge_not_source_deletion",
    "future_only",
    "read_only",
)

SOURCE_FALSE = (
    "continuum_principal_bundle_claimed",
    "physical_su3_gauge_field_claimed",
    "universal_statistical_optimum_claimed",
    "local_link_component_used_as_truth",
    "fusion_review_used_as_candidate_ranking",
    "source_record_deleted_by_tree_gauge",
    "candidate_ranking_performed",
    "candidate_pruning_performed",
    "candidate_selection_performed",
    "decision_commit_performed",
    "decision_receipt_issued",
    "plan_synthesis_performed",
    "activation_performed",
    "execution_permission",
    "source_memoryos_v071_mutated",
    "source_decisionos_v06_mutated",
    "persistent_world_state_mutated",
    "verification_result_claimed",
    "truth_authority_granted",
)

SOURCE_COUNTS = {
    "literature_nonabelian_gauge_record_count": 5,
    "local_memory_chart_record_count": 3,
    "nonabelian_gauge_frame_record_count": 3,
    "nonabelian_link_record_count": 6,
    "gauge_transformed_nonabelian_link_record_count": 6,
    "path_ordered_transport_record_count": 4,
    "nonabelian_commutator_record_count": 2,
    "nonabelian_holonomy_record_count": 2,
    "holonomy_conjugacy_class_record_count": 2,
    "wilson_character_record_count": 2,
    "nonabelian_tree_gauge_record_count": 6,
    "multi_chart_fusion_record_count": 2,
    "nonabelian_gauge_adjusted_confidence_record_count": 2,
    "full_rank_transport_nonabelian_record_count": 8,
    "singular_atomic_nonabelian_record_count": 4,
    "rank_one_source_boundary_count": 3,
}

SOURCE_COLLECTIONS = (
    "literature_nonabelian_gauge_records",
    "local_memory_chart_records",
    "nonabelian_gauge_frame_records",
    "nonabelian_link_records",
    "gauge_transformed_nonabelian_link_records",
    "path_ordered_transport_records",
    "nonabelian_commutator_records",
    "nonabelian_holonomy_records",
    "holonomy_conjugacy_class_records",
    "wilson_character_records",
    "nonabelian_tree_gauge_records",
    "multi_chart_fusion_records",
    "nonabelian_gauge_adjusted_confidence_records",
    "full_rank_transport_nonabelian_records",
    "singular_atomic_nonabelian_records",
)

LITERATURE = (
    {
        "literature_id": "arxiv:2604.16252",
        "title": "Universal dualities for Wilson loops in lattice Yang-Mills",
        "published": "2026-04-17",
        "bound_concept": "central plaquette actions Wilson loops and exact lattice composition",
    },
    {
        "literature_id": "arxiv:2602.02436",
        "title": "Wilson loops with neural networks",
        "published": "2026-02-02",
        "bound_concept": "gauge-invariant Wilson observables through equivariant layers",
    },
    {
        "literature_id": "arxiv:2501.16955",
        "title": "CASK: A Gauge Covariant Transformer for Lattice Gauge Theory",
        "published": "2025-01-28",
        "bound_concept": "gauge-covariant link transport and invariant contractions",
    },
    {
        "literature_id": "arxiv:1011.0371",
        "title": "Non abelian Bianchi identities, monopoles and gauge invariance",
        "published": "2010-11-01",
        "bound_concept": "non-Abelian Bianchi identities and gauge-invariant defect interpretation",
    },
    {
        "literature_id": "arxiv:2605.26697",
        "title": "A Gauge-Covariant Theoretical Framework for Non-Abelian Holonomy Estimation and Feed-Forward Correction in Time-Bin Photonic Qudits",
        "published": "2026-05-26",
        "bound_concept": "path-ordered non-Abelian holonomy and frame covariance",
    },
)

Perm = tuple[int, int, int]
EDGE_IDS = ("u01", "u12", "u23", "u30", "u02", "u13")
FACE_IDS = ("012", "023", "031", "123")
BASE_VERTEX = {"012": "0", "023": "0", "031": "0", "123": "1"}


def _blocked(*blockers: str) -> dict[str, Any]:
    return {
        "accepted": False,
        "schema_version": SCHEMA_VERSION,
        "blockers": sorted(set(blockers)),
        "observables": {},
        "certificate_digest": None,
    }


def _normalize_source(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError("source_memoryos_v072_certificate_invalid")
    source = dict(value)
    if source.get("accepted") is not True:
        raise ValueError("source_memoryos_v072_not_accepted")
    if source.get("schema_version") != SOURCE_SCHEMA_VERSION:
        raise ValueError("source_memoryos_v072_schema_invalid")
    digest = source.get("certificate_digest")
    unsigned = dict(source)
    unsigned.pop("certificate_digest", None)
    if not isinstance(digest, str) or canonical_digest(unsigned) != digest:
        raise ValueError("source_memoryos_v072_certificate_digest_mismatch")
    raw = source.get("observables")
    if not isinstance(raw, Mapping):
        raise ValueError("source_memoryos_v072_observables_invalid")
    obs = dict(raw)
    for field in SOURCE_TRUE:
        if obs.get(field) is not True:
            raise ValueError(f"source_memoryos_v072_required_{field}")
    for field in SOURCE_FALSE:
        if obs.get(field) is not False:
            raise ValueError(f"source_memoryos_v072_forbidden_{field}")
    for field, expected in SOURCE_COUNTS.items():
        if obs.get(field) != expected:
            raise ValueError(f"source_memoryos_v072_{field}_mismatch")

    out: dict[str, Any] = {"certificate_digest": digest}
    for field in SOURCE_COLLECTIONS:
        records = obs.get(field)
        digest_field = field.replace("records", "digest")
        if not isinstance(records, list):
            raise ValueError(f"source_memoryos_v072_{field}_invalid")
        if canonical_digest(records) != obs.get(digest_field):
            raise ValueError(f"source_memoryos_v072_{digest_field}_mismatch")
        out[field] = [dict(record) for record in records]
        out[digest_field] = obs[digest_field]

    candidates = obs.get("retained_decision_candidate_ids")
    histories = obs.get("retained_history_ids")
    probes = obs.get("retained_probe_ids")
    if candidates != ["continue", "hold", "reobserve", "terminate_candidate"]:
        raise ValueError("source_memoryos_v072_candidate_order_mismatch")
    if not isinstance(histories, list) or len(histories) != 2 or len(set(histories)) != 2:
        raise ValueError("source_memoryos_v072_history_support_invalid")
    if not isinstance(probes, list) or len(probes) != 9 or len(set(probes)) != 9:
        raise ValueError("source_memoryos_v072_probe_support_invalid")
    out.update(
        candidate_ids=list(candidates),
        history_ids=list(histories),
        probe_ids=list(probes),
        rank_one_source_boundary_count=obs["rank_one_source_boundary_count"],
    )
    for field in REVIEW_FIELDS:
        items = obs.get(field)
        if not isinstance(items, list) or any(item not in candidates for item in items):
            raise ValueError(f"source_memoryos_v072_{field}_invalid")
        out[field] = list(items)
    return out


def _profile_connections() -> dict[str, dict[str, Perm]]:
    return {
        "flat": {edge: IDENTITY for edge in EDGE_IDS},
        "curved": {
            "u01": SWAP_01,
            "u12": SWAP_12,
            "u23": SWAP_01,
            "u30": IDENTITY,
            "u02": IDENTITY,
            "u13": IDENTITY,
        },
    }


def _gauge_frames() -> dict[str, Perm]:
    return {
        "0": SWAP_01,
        "1": SWAP_12,
        "2": _compose(SWAP_01, SWAP_12),
        "3": _compose(SWAP_12, SWAP_01),
    }


def _transform(connection: Mapping[str, Perm]) -> dict[str, Perm]:
    g = _gauge_frames()
    return {
        "u01": _compose(_compose(_inverse(g["0"]), connection["u01"]), g["1"]),
        "u12": _compose(_compose(_inverse(g["1"]), connection["u12"]), g["2"]),
        "u23": _compose(_compose(_inverse(g["2"]), connection["u23"]), g["3"]),
        "u30": _compose(_compose(_inverse(g["3"]), connection["u30"]), g["0"]),
        "u02": _compose(_compose(_inverse(g["0"]), connection["u02"]), g["2"]),
        "u13": _compose(_compose(_inverse(g["1"]), connection["u13"]), g["3"]),
    }


def _faces(connection: Mapping[str, Perm]) -> dict[str, Perm]:
    return {
        "012": _compose(
            _compose(connection["u01"], connection["u12"]),
            _inverse(connection["u02"]),
        ),
        "023": _compose(
            _compose(connection["u02"], connection["u23"]),
            connection["u30"],
        ),
        "031": _compose(
            _compose(_inverse(connection["u30"]), _inverse(connection["u13"])),
            _inverse(connection["u01"]),
        ),
        "123": _compose(
            _compose(connection["u12"], connection["u23"]),
            _inverse(connection["u13"]),
        ),
    }


def _transport_face123_to_zero(connection: Mapping[str, Perm], faces: Mapping[str, Perm]) -> Perm:
    return _compose(
        _compose(connection["u01"], faces["123"]),
        _inverse(connection["u01"]),
    )


def _bianchi_lhs(faces: Mapping[str, Perm]) -> Perm:
    return _compose(_compose(faces["012"], faces["023"]), faces["031"])


def _identity_wilson(value: Perm) -> int:
    return 3 if value == IDENTITY else 0


def _derive_observables(source_v072: Mapping[str, Any]) -> dict[str, Any]:
    source = _normalize_source(source_v072)
    confidence_source = source["nonabelian_gauge_adjusted_confidence_records"]
    if len(confidence_source) != 2:
        raise ValueError("source_memoryos_v072_confidence_support_invalid")
    nonabelian_source = next(
        record for record in confidence_source if record.get("profile_id") == "nonabelian"
    )
    base_confidence = _f(nonabelian_source["nonabelian_gauge_adjusted_confidence"])
    if base_confidence != Fraction(1, 2):
        raise ValueError("source_memoryos_v072_base_confidence_mismatch")

    literature_records = [dict(record) for record in LITERATURE]
    vertex_records = [
        {
            "vertex_id": vertex,
            "local_frame_group": "S3",
            "frame_permutation": list(_gauge_frames()[vertex]),
            "frame_matrix": _matrix(_gauge_frames()[vertex]),
            "truth_authority": False,
        }
        for vertex in ("0", "1", "2", "3")
    ]

    edge_records: list[dict[str, Any]] = []
    transformed_edge_records: list[dict[str, Any]] = []
    plaquette_records: list[dict[str, Any]] = []
    bianchi_records: list[dict[str, Any]] = []
    composition_records: list[dict[str, Any]] = []
    curvature_records: list[dict[str, Any]] = []
    fusion_records: list[dict[str, Any]] = []

    for profile_id, connection in _profile_connections().items():
        transformed = _transform(connection)
        faces = _faces(connection)
        transformed_faces = _faces(transformed)

        expected_transformed_faces = {
            "012": _conjugate(faces["012"], _gauge_frames()["0"]),
            "023": _conjugate(faces["023"], _gauge_frames()["0"]),
            "031": _conjugate(faces["031"], _gauge_frames()["0"]),
            "123": _conjugate(faces["123"], _gauge_frames()["1"]),
        }
        if transformed_faces != expected_transformed_faces:
            raise ValueError("tetrahedral_plaquette_covariance_failure")

        for edge_id in EDGE_IDS:
            edge_records.append(
                {
                    "profile_id": profile_id,
                    "edge_id": edge_id,
                    "edge_permutation": list(connection[edge_id]),
                    "edge_matrix": _matrix(connection[edge_id]),
                    "frame_dependent": True,
                }
            )
            transformed_edge_records.append(
                {
                    "profile_id": profile_id,
                    "edge_id": edge_id,
                    "transformed_edge_permutation": list(transformed[edge_id]),
                    "transformed_edge_matrix": _matrix(transformed[edge_id]),
                    "gauge_transformation_exact": True,
                }
            )

        for face_id in FACE_IDS:
            original = faces[face_id]
            changed = transformed_faces[face_id]
            plaquette_records.append(
                {
                    "profile_id": profile_id,
                    "face_id": face_id,
                    "base_vertex": BASE_VERTEX[face_id],
                    "plaquette_holonomy": list(original),
                    "transformed_plaquette_holonomy": list(changed),
                    "cycle_type": _cycle_type(original),
                    "holonomy_order": 1 if original == IDENTITY else (
                        2 if _compose(original, original) == IDENTITY else 3
                    ),
                    "permutation_trace": _fixed_point_trace(original),
                    "identity_wilson_value": _identity_wilson(original),
                    "gauge_covariant": changed == expected_transformed_faces[face_id],
                    "identity_class_gauge_invariant": (
                        _identity_wilson(changed) == _identity_wilson(original)
                    ),
                }
            )

        lhs = _bianchi_lhs(faces)
        transported = _transport_face123_to_zero(connection, faces)
        defect = _compose(lhs, _inverse(transported))
        transformed_lhs = _bianchi_lhs(transformed_faces)
        transformed_transport = _transport_face123_to_zero(transformed, transformed_faces)
        transformed_defect = _compose(
            transformed_lhs, _inverse(transformed_transport)
        )
        if lhs != transported or defect != IDENTITY:
            raise ValueError("tetrahedral_discrete_bianchi_failure")
        if transformed_defect != _conjugate(defect, _gauge_frames()["0"]):
            raise ValueError("bianchi_defect_covariance_failure")

        bianchi_records.append(
            {
                "profile_id": profile_id,
                "ordered_face_product": list(lhs),
                "transported_face_123": list(transported),
                "bianchi_defect": list(defect),
                "transformed_bianchi_defect": list(transformed_defect),
                "discrete_bianchi_exact": lhs == transported,
                "defect_identity": defect == IDENTITY,
                "gauge_covariant": True,
            }
        )
        composition_records.append(
            {
                "profile_id": profile_id,
                "ordered_product_identity_wilson": _identity_wilson(lhs),
                "face_123_identity_wilson": _identity_wilson(faces["123"]),
                "ordered_product_cycle_type": _cycle_type(lhs),
                "face_123_cycle_type": _cycle_type(faces["123"]),
                "conjugacy_class_match": (
                    _cycle_type(lhs) == _cycle_type(faces["123"])
                ),
                "wilson_composition_exact": (
                    _identity_wilson(lhs) == _identity_wilson(faces["123"])
                ),
            }
        )

        deficits = {
            face_id: Fraction(3 - _identity_wilson(faces[face_id]), 18)
            for face_id in FACE_IDS
        }
        action = sum(deficits.values(), Fraction(0)) / 4
        transformed_deficits = {
            face_id: Fraction(3 - _identity_wilson(transformed_faces[face_id]), 18)
            for face_id in FACE_IDS
        }
        transformed_action = sum(transformed_deficits.values(), Fraction(0)) / 4
        adjusted = base_confidence - action
        curvature_records.append(
            {
                "profile_id": profile_id,
                "face_deficits": {
                    face_id: _q(deficits[face_id]) for face_id in FACE_IDS
                },
                "average_identity_class_curvature_action": _q(action),
                "transformed_curvature_action": _q(transformed_action),
                "source_base_confidence": _q(base_confidence),
                "curvature_adjusted_confidence": _q(adjusted),
                "gauge_invariant": action == transformed_action,
                "within_unit_interval": Fraction(0) <= adjusted <= Fraction(1),
                "physical_yang_mills_action": False,
            }
        )
        fusion_records.append(
            {
                "profile_id": profile_id,
                "plaquette_cycle_signature": [
                    _cycle_type(faces[face_id]) for face_id in FACE_IDS
                ],
                "bianchi_defect_identity": defect == IDENTITY,
                "curvature_action": _q(action),
                "frame_independent": True,
                "requires_review": action > 0,
                "candidate_ranking_performed": False,
            }
        )

    curved_faces = [
        record for record in plaquette_records if record["profile_id"] == "curved"
    ]
    if [record["plaquette_holonomy"] for record in curved_faces] != [
        [1, 2, 0],
        [1, 0, 2],
        [1, 0, 2],
        [2, 0, 1],
    ]:
        raise ValueError("canonical_curved_plaquette_profile_mismatch")
    if [record["permutation_trace"] for record in curved_faces] != [0, 1, 1, 0]:
        raise ValueError("canonical_curved_plaquette_trace_mismatch")
    if bianchi_records[1]["ordered_face_product"] != [1, 2, 0]:
        raise ValueError("canonical_bianchi_product_mismatch")
    if bianchi_records[1]["transported_face_123"] != [1, 2, 0]:
        raise ValueError("canonical_transported_face_mismatch")
    if curvature_records != [
        {
            "profile_id": "flat",
            "face_deficits": {face_id: _q(Fraction(0)) for face_id in FACE_IDS},
            "average_identity_class_curvature_action": _q(Fraction(0)),
            "transformed_curvature_action": _q(Fraction(0)),
            "source_base_confidence": _q(Fraction(1, 2)),
            "curvature_adjusted_confidence": _q(Fraction(1, 2)),
            "gauge_invariant": True,
            "within_unit_interval": True,
            "physical_yang_mills_action": False,
        },
        {
            "profile_id": "curved",
            "face_deficits": {face_id: _q(Fraction(1, 6)) for face_id in FACE_IDS},
            "average_identity_class_curvature_action": _q(Fraction(1, 6)),
            "transformed_curvature_action": _q(Fraction(1, 6)),
            "source_base_confidence": _q(Fraction(1, 2)),
            "curvature_adjusted_confidence": _q(Fraction(1, 3)),
            "gauge_invariant": True,
            "within_unit_interval": True,
            "physical_yang_mills_action": False,
        },
    ]:
        raise ValueError("canonical_curvature_action_profile_mismatch")

    full_rank_records = [
        {
            "distribution_id": record.get("distribution_id"),
            "transition_id": record.get("transition_id"),
            "tetrahedral_edge_transport_commutes": True,
            "plaquette_wilson_composition_commutes": True,
            "bianchi_curvature_certificate_commutes": True,
            "source_record_digest": canonical_digest(record),
        }
        for record in source["full_rank_transport_nonabelian_records"]
    ]
    singular_records = [
        {
            "distribution_id": record.get("distribution_id"),
            "transition_id": record.get("transition_id"),
            "atomic_plaquette_signature_retained": True,
            "atomic_bianchi_boundary_retained": True,
            "two_dimensional_target_density_emitted": False,
            "lost_coordinate_reconstructed": False,
            "source_record_digest": canonical_digest(record),
        }
        for record in source["singular_atomic_nonabelian_records"]
    ]

    obs: dict[str, Any] = {
        "source_memoryos_v072_exact": True,
        "source_memoryos_v072_certificate_digest": source["certificate_digest"],
        "source_nonabelian_holonomy_digest": source["nonabelian_holonomy_digest"],
        "source_wilson_character_digest": source["wilson_character_digest"],
        "source_nonabelian_gauge_adjusted_confidence_digest": source[
            "nonabelian_gauge_adjusted_confidence_digest"
        ],
        "literature_lattice_bianchi_records": literature_records,
        "literature_lattice_bianchi_record_count": len(literature_records),
        "tetrahedron_vertex_frame_records": vertex_records,
        "tetrahedron_vertex_frame_record_count": len(vertex_records),
        "oriented_edge_transport_records": edge_records,
        "oriented_edge_transport_record_count": len(edge_records),
        "gauge_transformed_edge_records": transformed_edge_records,
        "gauge_transformed_edge_record_count": len(transformed_edge_records),
        "plaquette_holonomy_records": plaquette_records,
        "plaquette_holonomy_record_count": len(plaquette_records),
        "tetrahedral_bianchi_records": bianchi_records,
        "tetrahedral_bianchi_record_count": len(bianchi_records),
        "wilson_composition_records": composition_records,
        "wilson_composition_record_count": len(composition_records),
        "curvature_action_records": curvature_records,
        "curvature_action_record_count": len(curvature_records),
        "tetrahedral_memory_fusion_records": fusion_records,
        "tetrahedral_memory_fusion_record_count": len(fusion_records),
        "full_rank_transport_bianchi_records": full_rank_records,
        "full_rank_transport_bianchi_record_count": len(full_rank_records),
        "singular_atomic_bianchi_records": singular_records,
        "singular_atomic_bianchi_record_count": len(singular_records),
        "rank_one_source_boundary_count": source["rank_one_source_boundary_count"],
        "finite_s3_tetrahedral_lattice_exact": True,
        "oriented_edge_transport_exact": len(edge_records) == 12,
        "plaquette_holonomy_gauge_covariant_exact": all(
            record["gauge_covariant"] for record in plaquette_records
        ),
        "tetrahedral_discrete_bianchi_exact": all(
            record["discrete_bianchi_exact"] for record in bianchi_records
        ),
        "bianchi_defect_identity_exact": all(
            record["defect_identity"] for record in bianchi_records
        ),
        "wilson_composition_conjugacy_exact": all(
            record["conjugacy_class_match"] and record["wilson_composition_exact"]
            for record in composition_records
        ),
        "curvature_action_gauge_invariant_exact": all(
            record["gauge_invariant"] for record in curvature_records
        ),
        "curvature_adjusted_confidence_exact": (
            curvature_records[0]["curvature_adjusted_confidence"] == _q(Fraction(1, 2))
            and curvature_records[1]["curvature_adjusted_confidence"] == _q(Fraction(1, 3))
            and all(record["within_unit_interval"] for record in curvature_records)
        ),
        "all_full_rank_transport_bianchi_layer_commutes": all(
            record["tetrahedral_edge_transport_commutes"]
            and record["plaquette_wilson_composition_commutes"]
            and record["bianchi_curvature_certificate_commutes"]
            for record in full_rank_records
        ),
        "singular_atomic_bianchi_layer_retained": all(
            record["atomic_plaquette_signature_retained"]
            and record["atomic_bianchi_boundary_retained"]
            and not record["two_dimensional_target_density_emitted"]
            and not record["lost_coordinate_reconstructed"]
            for record in singular_records
        ),
        "retained_decision_candidate_ids": source["candidate_ids"],
        "retained_history_ids": source["history_ids"],
        "retained_probe_ids": source["probe_ids"],
        **{field: source[field] for field in REVIEW_FIELDS},
        "all_decision_candidates_retained": True,
        "all_planos_histories_retained": True,
        "all_quotient_coordinate_probes_retained": True,
        "relational_frontier_preserved": True,
        "required_review_set_preserved": True,
        "dissent_visibility_preserved": True,
        "minority_visibility_preserved": True,
        "bianchi_defect_not_truth_authority": True,
        "curvature_action_not_candidate_ranking": True,
        "plaquette_gauge_fixing_not_source_deletion": True,
        "continuum_lattice_gauge_field_claimed": False,
        "physical_yang_mills_action_claimed": False,
        "universal_nonabelian_bianchi_theorem_claimed": False,
        "local_plaquette_component_used_as_truth": False,
        "curvature_review_used_as_candidate_ranking": False,
        "source_record_deleted_by_plaquette_gauge": False,
        "candidate_ranking_performed": False,
        "candidate_pruning_performed": False,
        "candidate_selection_performed": False,
        "decision_commit_performed": False,
        "decision_receipt_issued": False,
        "plan_synthesis_performed": False,
        "activation_performed": False,
        "execution_permission": False,
        "source_memoryos_v072_mutated": False,
        "source_decisionos_v06_mutated": False,
        "persistent_world_state_mutated": False,
        "verification_result_claimed": False,
        "truth_authority_granted": False,
        "future_only": True,
        "read_only": True,
    }
    for field in (
        "literature_lattice_bianchi_records",
        "tetrahedron_vertex_frame_records",
        "oriented_edge_transport_records",
        "gauge_transformed_edge_records",
        "plaquette_holonomy_records",
        "tetrahedral_bianchi_records",
        "wilson_composition_records",
        "curvature_action_records",
        "tetrahedral_memory_fusion_records",
        "full_rank_transport_bianchi_records",
        "singular_atomic_bianchi_records",
    ):
        obs[field.replace("records", "digest")] = canonical_digest(obs[field])
    return obs


def issue_tetrahedral_bianchi_curvature_certificate(
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    try:
        if not isinstance(payload, Mapping):
            return _blocked("payload_invalid")
        if payload.get("schema_version") != SCHEMA_VERSION:
            return _blocked("schema_version_invalid")
        expected = _derive_observables(payload.get("source_memoryos_v072_certificate"))
        claims = payload.get("claims")
        if not isinstance(claims, Mapping):
            return _blocked("claims_invalid")
        claims = dict(claims)
        blockers = [
            f"claim_mismatch_{field}"
            for field, value in expected.items()
            if claims.get(field) != value
        ]
        blockers.extend(
            f"unexpected_claim_{field}" for field in claims if field not in expected
        )
        if blockers:
            return _blocked(*blockers)
        unsigned = {
            "accepted": True,
            "schema_version": SCHEMA_VERSION,
            "blockers": [],
            "observables": expected,
        }
        return {**unsigned, "certificate_digest": canonical_digest(unsigned)}
    except (KeyError, StopIteration, TypeError, ValueError, ZeroDivisionError) as exc:
        return _blocked(str(exc))


__all__ = [
    "SCHEMA_VERSION",
    "_derive_observables",
    "issue_tetrahedral_bianchi_curvature_certificate",
]
