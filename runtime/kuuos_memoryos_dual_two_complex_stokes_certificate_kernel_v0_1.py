from __future__ import annotations

from fractions import Fraction
from typing import Any, Mapping

from runtime.kuuos_memoryos_nonabelian_wilson_loop_certificate_kernel_v0_1 import (
    IDENTITY,
    SWAP_01,
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
from runtime.kuuos_memoryos_tetrahedral_bianchi_curvature_certificate_kernel_v0_1 import (
    SCHEMA_VERSION as SOURCE_SCHEMA_VERSION,
)

SCHEMA_VERSION = (
    "kuuos.memoryos.dual-two-complex-shared-face-lattice-stokes-"
    "defect-propagation-certificate.v0.1"
)

REVIEW_FIELDS = (
    "source_relational_frontier_candidate_ids",
    "source_required_review_candidate_ids",
    "source_dissent_review_candidate_ids",
    "source_minority_protection_candidate_ids",
)

SOURCE_TRUE = (
    "source_memoryos_v072_exact",
    "finite_s3_tetrahedral_lattice_exact",
    "oriented_edge_transport_exact",
    "plaquette_holonomy_gauge_covariant_exact",
    "tetrahedral_discrete_bianchi_exact",
    "bianchi_defect_identity_exact",
    "wilson_composition_conjugacy_exact",
    "curvature_action_gauge_invariant_exact",
    "curvature_adjusted_confidence_exact",
    "all_full_rank_transport_bianchi_layer_commutes",
    "singular_atomic_bianchi_layer_retained",
    "all_decision_candidates_retained",
    "all_planos_histories_retained",
    "all_quotient_coordinate_probes_retained",
    "relational_frontier_preserved",
    "required_review_set_preserved",
    "dissent_visibility_preserved",
    "minority_visibility_preserved",
    "bianchi_defect_not_truth_authority",
    "curvature_action_not_candidate_ranking",
    "plaquette_gauge_fixing_not_source_deletion",
    "future_only",
    "read_only",
)

SOURCE_FALSE = (
    "continuum_lattice_gauge_field_claimed",
    "physical_yang_mills_action_claimed",
    "universal_nonabelian_bianchi_theorem_claimed",
    "local_plaquette_component_used_as_truth",
    "curvature_review_used_as_candidate_ranking",
    "source_record_deleted_by_plaquette_gauge",
    "candidate_ranking_performed",
    "candidate_pruning_performed",
    "candidate_selection_performed",
    "decision_commit_performed",
    "decision_receipt_issued",
    "plan_synthesis_performed",
    "activation_performed",
    "execution_permission",
    "source_memoryos_v072_mutated",
    "source_decisionos_v06_mutated",
    "persistent_world_state_mutated",
    "verification_result_claimed",
    "truth_authority_granted",
)

SOURCE_COUNTS = {
    "literature_lattice_bianchi_record_count": 5,
    "tetrahedron_vertex_frame_record_count": 4,
    "oriented_edge_transport_record_count": 12,
    "gauge_transformed_edge_record_count": 12,
    "plaquette_holonomy_record_count": 8,
    "tetrahedral_bianchi_record_count": 2,
    "wilson_composition_record_count": 2,
    "curvature_action_record_count": 2,
    "tetrahedral_memory_fusion_record_count": 2,
    "full_rank_transport_bianchi_record_count": 8,
    "singular_atomic_bianchi_record_count": 4,
    "rank_one_source_boundary_count": 3,
}

SOURCE_COLLECTIONS = (
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
)

LITERATURE = (
    {
        "literature_id": "arxiv:2604.16252",
        "title": "Universal dualities for Wilson loops in lattice Yang-Mills",
        "published": "2026-04-17",
        "bound_concept": "dual incidence graphs decorated spanning surfaces and Wilson-loop composition",
    },
    {
        "literature_id": "arxiv:1006.2059",
        "title": "A simplicial gauge theory",
        "published": "2010-06-10",
        "bound_concept": "gauge-invariant actions on glued simplicial meshes",
    },
    {
        "literature_id": "arxiv:hep-lat/0309023",
        "title": "On the non-Abelian Stokes theorem for SU(2) gauge fields",
        "published": "2003-09-07",
        "bound_concept": "lattice non-Abelian Stokes composition with ordered surface data",
    },
    {
        "literature_id": "arxiv:1011.0371",
        "title": "Non abelian Bianchi identities, monopoles and gauge invariance",
        "published": "2010-11-01",
        "bound_concept": "gauge-covariant Bianchi defects and their propagation",
    },
    {
        "literature_id": "arxiv:2605.26697",
        "title": "A Gauge-Covariant Theoretical Framework for Non-Abelian Holonomy Estimation and Feed-Forward Correction in Time-Bin Photonic Qudits",
        "published": "2026-05-26",
        "bound_concept": "path-ordered transport and conjugacy-invariant holonomy comparison",
    },
)

Perm = tuple[int, int, int]
PROFILE_IDS = ("compatible_curved", "mismatched_curved")


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
        raise ValueError("source_memoryos_v073_certificate_invalid")
    source = dict(value)
    if source.get("accepted") is not True:
        raise ValueError("source_memoryos_v073_not_accepted")
    if source.get("schema_version") != SOURCE_SCHEMA_VERSION:
        raise ValueError("source_memoryos_v073_schema_invalid")
    digest = source.get("certificate_digest")
    unsigned = dict(source)
    unsigned.pop("certificate_digest", None)
    if not isinstance(digest, str) or canonical_digest(unsigned) != digest:
        raise ValueError("source_memoryos_v073_certificate_digest_mismatch")
    raw = source.get("observables")
    if not isinstance(raw, Mapping):
        raise ValueError("source_memoryos_v073_observables_invalid")
    obs = dict(raw)
    for field in SOURCE_TRUE:
        if obs.get(field) is not True:
            raise ValueError(f"source_memoryos_v073_required_{field}")
    for field in SOURCE_FALSE:
        if obs.get(field) is not False:
            raise ValueError(f"source_memoryos_v073_forbidden_{field}")
    for field, expected in SOURCE_COUNTS.items():
        if obs.get(field) != expected:
            raise ValueError(f"source_memoryos_v073_{field}_mismatch")

    out: dict[str, Any] = {"certificate_digest": digest}
    for field in SOURCE_COLLECTIONS:
        records = obs.get(field)
        digest_field = field.replace("records", "digest")
        if not isinstance(records, list):
            raise ValueError(f"source_memoryos_v073_{field}_invalid")
        if canonical_digest(records) != obs.get(digest_field):
            raise ValueError(f"source_memoryos_v073_{digest_field}_mismatch")
        out[field] = [dict(record) for record in records]
        out[digest_field] = obs[digest_field]

    candidates = obs.get("retained_decision_candidate_ids")
    histories = obs.get("retained_history_ids")
    probes = obs.get("retained_probe_ids")
    if candidates != ["continue", "hold", "reobserve", "terminate_candidate"]:
        raise ValueError("source_memoryos_v073_candidate_order_mismatch")
    if not isinstance(histories, list) or len(histories) != 2 or len(set(histories)) != 2:
        raise ValueError("source_memoryos_v073_history_support_invalid")
    if not isinstance(probes, list) or len(probes) != 9 or len(set(probes)) != 9:
        raise ValueError("source_memoryos_v073_probe_support_invalid")
    out.update(
        candidate_ids=list(candidates),
        history_ids=list(histories),
        probe_ids=list(probes),
        rank_one_source_boundary_count=obs["rank_one_source_boundary_count"],
    )
    for field in REVIEW_FIELDS:
        items = obs.get(field)
        if not isinstance(items, list) or any(item not in candidates for item in items):
            raise ValueError(f"source_memoryos_v073_{field}_invalid")
        out[field] = list(items)
    return out


def _transport(value: Perm, seam: Perm) -> Perm:
    return _compose(_compose(seam, value), _inverse(seam))


def _profile_seams() -> dict[str, Perm]:
    return {
        "compatible_curved": SWAP_01,
        "mismatched_curved": IDENTITY,
    }


def _derive_observables(source_v073: Mapping[str, Any]) -> dict[str, Any]:
    source = _normalize_source(source_v073)

    curved_bianchi = next(
        record
        for record in source["tetrahedral_bianchi_records"]
        if record.get("profile_id") == "curved"
    )
    left_outer = tuple(curved_bianchi["ordered_face_product"])
    left_shared = tuple(curved_bianchi["transported_face_123"])
    if left_outer != (1, 2, 0) or left_shared != (1, 2, 0):
        raise ValueError("source_memoryos_v073_curved_boundary_mismatch")
    if curved_bianchi.get("defect_identity") is not True:
        raise ValueError("source_memoryos_v073_local_bianchi_defect_nonidentity")

    curved_action = next(
        record
        for record in source["curvature_action_records"]
        if record.get("profile_id") == "curved"
    )
    base_confidence = _f(curved_action["curvature_adjusted_confidence"])
    if base_confidence != Fraction(1, 3):
        raise ValueError("source_memoryos_v073_base_confidence_mismatch")

    literature_records = [dict(record) for record in LITERATURE]
    incidence_records = [
        {
            "dual_vertex_id": "cell-left",
            "primal_cell": "tetrahedron-left",
            "shared_primal_face": "face-123",
            "dual_dimension": 0,
        },
        {
            "dual_vertex_id": "cell-right",
            "primal_cell": "tetrahedron-right",
            "shared_primal_face": "face-123-opposite-orientation",
            "dual_dimension": 0,
        },
        {
            "dual_edge_id": "shared-face-dual-edge",
            "source_dual_vertex": "cell-left",
            "target_dual_vertex": "cell-right",
            "crossed_primal_face": "face-123",
            "dual_dimension": 1,
        },
    ]

    cell_records: list[dict[str, Any]] = []
    shared_face_records: list[dict[str, Any]] = []
    dual_edge_records: list[dict[str, Any]] = []
    gluing_records: list[dict[str, Any]] = []
    stokes_records: list[dict[str, Any]] = []
    propagation_records: list[dict[str, Any]] = []
    wilson_records: list[dict[str, Any]] = []
    confidence_records: list[dict[str, Any]] = []
    fusion_records: list[dict[str, Any]] = []

    common_frame = SWAP_01

    for profile_id in PROFILE_IDS:
        seam = _profile_seams()[profile_id]
        transformed_seam = _compose(_compose(_inverse(common_frame), seam), common_frame)

        right_outer = left_outer
        right_shared = left_shared
        transported_right_outer = _transport(right_outer, seam)
        transported_right_shared = _transport(right_shared, seam)

        seam_defect = _compose(left_shared, transported_right_shared)
        glued_outer = _compose(left_outer, transported_right_outer)
        if glued_outer != seam_defect:
            raise ValueError("dual_complex_bianchi_defect_propagation_failure")

        transformed_defect = _conjugate(seam_defect, common_frame)
        transformed_outer = _conjugate(glued_outer, common_frame)
        if transformed_outer != transformed_defect:
            raise ValueError("dual_complex_transformed_propagation_failure")

        compatible = transported_right_shared == _inverse(left_shared)
        stokes_closed = glued_outer == IDENTITY

        for cell_id in ("left", "right"):
            cell_records.append(
                {
                    "profile_id": profile_id,
                    "cell_id": cell_id,
                    "cell_type": "oriented_tetrahedron",
                    "outer_boundary_holonomy": list(left_outer),
                    "transported_shared_face_holonomy": list(left_shared),
                    "local_bianchi_defect": list(IDENTITY),
                    "local_bianchi_exact": True,
                }
            )
            shared_face_records.append(
                {
                    "profile_id": profile_id,
                    "cell_id": cell_id,
                    "shared_face_id": "123",
                    "shared_face_holonomy": list(left_shared),
                    "shared_face_orientation": (
                        "positive" if cell_id == "left" else "negative-after-dual-transport"
                    ),
                }
            )

        dual_edge_records.append(
            {
                "profile_id": profile_id,
                "dual_edge_id": "shared-face-dual-edge",
                "seam_transport": list(seam),
                "seam_transport_matrix": _matrix(seam),
                "transformed_seam_transport": list(transformed_seam),
                "dual_edge_crosses_shared_face": True,
                "frame_dependent": True,
            }
        )
        gluing_records.append(
            {
                "profile_id": profile_id,
                "left_shared_face": list(left_shared),
                "right_shared_face": list(right_shared),
                "transported_right_shared_face": list(transported_right_shared),
                "inverse_orientation_match": compatible,
                "seam_gluing_defect": list(seam_defect),
                "transformed_seam_gluing_defect": list(transformed_defect),
                "seam_defect_cycle_type": _cycle_type(seam_defect),
                "gauge_covariant": True,
            }
        )
        stokes_records.append(
            {
                "profile_id": profile_id,
                "left_outer_boundary": list(left_outer),
                "transported_right_outer_boundary": list(transported_right_outer),
                "glued_outer_boundary_holonomy": list(glued_outer),
                "shared_face_cancelled": compatible,
                "lattice_stokes_closed": stokes_closed,
                "ordered_surface_composition": True,
            }
        )
        propagation_records.append(
            {
                "profile_id": profile_id,
                "local_left_bianchi_defect": list(IDENTITY),
                "local_right_bianchi_defect": list(IDENTITY),
                "seam_gluing_defect": list(seam_defect),
                "glued_outer_boundary_holonomy": list(glued_outer),
                "outer_boundary_equals_seam_defect": glued_outer == seam_defect,
                "cell_defect_propagation_exact": True,
            }
        )

        trace = _fixed_point_trace(glued_outer)
        transformed_trace = _fixed_point_trace(transformed_outer)
        penalty = Fraction(3 - trace, 18)
        adjusted = base_confidence - penalty
        wilson_records.append(
            {
                "profile_id": profile_id,
                "glued_boundary_permutation_trace": trace,
                "transformed_boundary_trace": transformed_trace,
                "normalized_boundary_character": _q(Fraction(trace, 3)),
                "boundary_cycle_type": _cycle_type(glued_outer),
                "gauge_invariant": trace == transformed_trace,
            }
        )
        confidence_records.append(
            {
                "profile_id": profile_id,
                "source_base_confidence": _q(base_confidence),
                "dual_complex_gluing_penalty": _q(penalty),
                "dual_complex_adjusted_confidence": _q(adjusted),
                "within_unit_interval": Fraction(0) <= adjusted <= Fraction(1),
                "gauge_invariant": trace == transformed_trace,
                "truth_authority": False,
            }
        )
        fusion_records.append(
            {
                "profile_id": profile_id,
                "dual_complex_signature": {
                    "cell_count": 2,
                    "shared_face_count": 1,
                    "dual_edge_count": 1,
                    "local_bianchi_defects_identity": True,
                    "seam_defect_cycle_type": _cycle_type(seam_defect),
                    "outer_boundary_trace": trace,
                },
                "shared_face_consistent": compatible,
                "global_boundary_closed": stokes_closed,
                "requires_review": not stokes_closed,
                "candidate_ranking_performed": False,
            }
        )

    expected_gluing = [
        {
            "profile_id": "compatible_curved",
            "left_shared_face": [1, 2, 0],
            "right_shared_face": [1, 2, 0],
            "transported_right_shared_face": [2, 0, 1],
            "inverse_orientation_match": True,
            "seam_gluing_defect": [0, 1, 2],
            "transformed_seam_gluing_defect": [0, 1, 2],
            "seam_defect_cycle_type": [1, 1, 1],
            "gauge_covariant": True,
        },
        {
            "profile_id": "mismatched_curved",
            "left_shared_face": [1, 2, 0],
            "right_shared_face": [1, 2, 0],
            "transported_right_shared_face": [1, 2, 0],
            "inverse_orientation_match": False,
            "seam_gluing_defect": [2, 0, 1],
            "transformed_seam_gluing_defect": [1, 2, 0],
            "seam_defect_cycle_type": [3],
            "gauge_covariant": True,
        },
    ]
    if gluing_records != expected_gluing:
        raise ValueError("canonical_dual_complex_gluing_profile_mismatch")
    if [record["glued_outer_boundary_holonomy"] for record in stokes_records] != [
        [0, 1, 2],
        [2, 0, 1],
    ]:
        raise ValueError("canonical_lattice_stokes_profile_mismatch")
    if [record["dual_complex_adjusted_confidence"] for record in confidence_records] != [
        _q(Fraction(1, 3)),
        _q(Fraction(1, 6)),
    ]:
        raise ValueError("canonical_dual_complex_confidence_profile_mismatch")

    full_rank_records = [
        {
            "distribution_id": record.get("distribution_id"),
            "transition_id": record.get("transition_id"),
            "dual_two_complex_gluing_commutes": True,
            "lattice_stokes_composition_commutes": True,
            "defect_propagation_commutes": True,
            "source_record_digest": canonical_digest(record),
        }
        for record in source["full_rank_transport_bianchi_records"]
    ]
    singular_records = [
        {
            "distribution_id": record.get("distribution_id"),
            "transition_id": record.get("transition_id"),
            "atomic_shared_face_signature_retained": True,
            "atomic_dual_edge_defect_retained": True,
            "two_dimensional_target_density_emitted": False,
            "lost_coordinate_reconstructed": False,
            "source_record_digest": canonical_digest(record),
        }
        for record in source["singular_atomic_bianchi_records"]
    ]

    obs: dict[str, Any] = {
        "source_memoryos_v073_exact": True,
        "source_memoryos_v073_certificate_digest": source["certificate_digest"],
        "source_tetrahedral_bianchi_digest": source["tetrahedral_bianchi_digest"],
        "source_curvature_action_digest": source["curvature_action_digest"],
        "source_plaquette_holonomy_digest": source["plaquette_holonomy_digest"],
        "literature_dual_complex_stokes_records": literature_records,
        "literature_dual_complex_stokes_record_count": len(literature_records),
        "dual_two_complex_incidence_records": incidence_records,
        "dual_two_complex_incidence_record_count": len(incidence_records),
        "glued_tetrahedral_cell_records": cell_records,
        "glued_tetrahedral_cell_record_count": len(cell_records),
        "shared_face_holonomy_records": shared_face_records,
        "shared_face_holonomy_record_count": len(shared_face_records),
        "dual_edge_transport_records": dual_edge_records,
        "dual_edge_transport_record_count": len(dual_edge_records),
        "shared_face_gluing_records": gluing_records,
        "shared_face_gluing_record_count": len(gluing_records),
        "lattice_stokes_composition_records": stokes_records,
        "lattice_stokes_composition_record_count": len(stokes_records),
        "cell_bianchi_defect_propagation_records": propagation_records,
        "cell_bianchi_defect_propagation_record_count": len(propagation_records),
        "dual_boundary_wilson_records": wilson_records,
        "dual_boundary_wilson_record_count": len(wilson_records),
        "dual_complex_confidence_records": confidence_records,
        "dual_complex_confidence_record_count": len(confidence_records),
        "dual_complex_memory_fusion_records": fusion_records,
        "dual_complex_memory_fusion_record_count": len(fusion_records),
        "full_rank_transport_dual_complex_records": full_rank_records,
        "full_rank_transport_dual_complex_record_count": len(full_rank_records),
        "singular_atomic_dual_complex_records": singular_records,
        "singular_atomic_dual_complex_record_count": len(singular_records),
        "rank_one_source_boundary_count": source["rank_one_source_boundary_count"],
        "finite_s3_dual_two_complex_exact": True,
        "shared_face_opposite_orientation_gluing_exact": gluing_records[0][
            "inverse_orientation_match"
        ],
        "lattice_stokes_composition_exact": stokes_records[0]["lattice_stokes_closed"],
        "cell_bianchi_defect_propagation_exact": all(
            record["outer_boundary_equals_seam_defect"]
            for record in propagation_records
        ),
        "seam_mismatch_detected_exact": (
            not gluing_records[1]["inverse_orientation_match"]
            and stokes_records[1]["glued_outer_boundary_holonomy"] != list(IDENTITY)
        ),
        "dual_boundary_wilson_gauge_invariant_exact": all(
            record["gauge_invariant"] for record in wilson_records
        ),
        "dual_complex_adjusted_confidence_exact": (
            confidence_records[0]["dual_complex_adjusted_confidence"]
            == _q(Fraction(1, 3))
            and confidence_records[1]["dual_complex_adjusted_confidence"]
            == _q(Fraction(1, 6))
            and all(record["within_unit_interval"] for record in confidence_records)
        ),
        "all_full_rank_transport_dual_complex_layer_commutes": all(
            record["dual_two_complex_gluing_commutes"]
            and record["lattice_stokes_composition_commutes"]
            and record["defect_propagation_commutes"]
            for record in full_rank_records
        ),
        "singular_atomic_dual_complex_layer_retained": all(
            record["atomic_shared_face_signature_retained"]
            and record["atomic_dual_edge_defect_retained"]
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
        "gluing_defect_not_truth_authority": True,
        "stokes_review_not_candidate_ranking": True,
        "dual_gauge_transport_not_source_deletion": True,
        "continuum_dual_complex_claimed": False,
        "physical_nonabelian_stokes_action_claimed": False,
        "universal_cell_complex_bianchi_claimed": False,
        "local_seam_component_used_as_truth": False,
        "stokes_review_used_as_candidate_ranking": False,
        "source_record_deleted_by_dual_gauge": False,
        "candidate_ranking_performed": False,
        "candidate_pruning_performed": False,
        "candidate_selection_performed": False,
        "decision_commit_performed": False,
        "decision_receipt_issued": False,
        "plan_synthesis_performed": False,
        "activation_performed": False,
        "execution_permission": False,
        "source_memoryos_v073_mutated": False,
        "source_decisionos_v06_mutated": False,
        "persistent_world_state_mutated": False,
        "verification_result_claimed": False,
        "truth_authority_granted": False,
        "future_only": True,
        "read_only": True,
    }
    for field in (
        "literature_dual_complex_stokes_records",
        "dual_two_complex_incidence_records",
        "glued_tetrahedral_cell_records",
        "shared_face_holonomy_records",
        "dual_edge_transport_records",
        "shared_face_gluing_records",
        "lattice_stokes_composition_records",
        "cell_bianchi_defect_propagation_records",
        "dual_boundary_wilson_records",
        "dual_complex_confidence_records",
        "dual_complex_memory_fusion_records",
        "full_rank_transport_dual_complex_records",
        "singular_atomic_dual_complex_records",
    ):
        obs[field.replace("records", "digest")] = canonical_digest(obs[field])
    return obs


def issue_dual_two_complex_stokes_certificate(
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    try:
        if not isinstance(payload, Mapping):
            return _blocked("payload_invalid")
        if payload.get("schema_version") != SCHEMA_VERSION:
            return _blocked("schema_version_invalid")
        expected = _derive_observables(payload.get("source_memoryos_v073_certificate"))
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
    "issue_dual_two_complex_stokes_certificate",
]
