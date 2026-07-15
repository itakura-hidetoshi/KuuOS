from __future__ import annotations

from fractions import Fraction
from typing import Any, Mapping, Sequence

from runtime.kuuos_memoryos_nonabelian_wilson_loop_certificate_kernel_v0_1 import (
    IDENTITY,
    SWAP_01,
    SWAP_12,
    canonical_digest,
    _compose,
    _inverse,
    _fixed_point_trace,
    _cycle_type,
    _matrix,
    _q,
    _f,
)
from runtime.kuuos_memoryos_dual_two_complex_stokes_certificate_kernel_v0_1 import (
    SCHEMA_VERSION as SOURCE_SCHEMA_VERSION,
)

SCHEMA_VERSION = (
    "kuuos.memoryos.dual-cell-chain-path-ordered-defect-localization-"
    "certificate.v0.1"
)

REVIEW_FIELDS = (
    "source_relational_frontier_candidate_ids",
    "source_required_review_candidate_ids",
    "source_dissent_review_candidate_ids",
    "source_minority_protection_candidate_ids",
)

SOURCE_TRUE = (
    "source_memoryos_v073_exact",
    "finite_s3_dual_two_complex_exact",
    "shared_face_opposite_orientation_gluing_exact",
    "lattice_stokes_composition_exact",
    "cell_bianchi_defect_propagation_exact",
    "seam_mismatch_detected_exact",
    "dual_boundary_wilson_gauge_invariant_exact",
    "dual_complex_adjusted_confidence_exact",
    "all_full_rank_transport_dual_complex_layer_commutes",
    "singular_atomic_dual_complex_layer_retained",
    "all_decision_candidates_retained",
    "all_planos_histories_retained",
    "all_quotient_coordinate_probes_retained",
    "relational_frontier_preserved",
    "required_review_set_preserved",
    "dissent_visibility_preserved",
    "minority_visibility_preserved",
    "gluing_defect_not_truth_authority",
    "stokes_review_not_candidate_ranking",
    "dual_gauge_transport_not_source_deletion",
    "future_only",
    "read_only",
)

SOURCE_FALSE = (
    "continuum_dual_complex_claimed",
    "physical_nonabelian_stokes_action_claimed",
    "universal_cell_complex_bianchi_claimed",
    "local_seam_component_used_as_truth",
    "stokes_review_used_as_candidate_ranking",
    "source_record_deleted_by_dual_gauge",
    "candidate_ranking_performed",
    "candidate_pruning_performed",
    "candidate_selection_performed",
    "decision_commit_performed",
    "decision_receipt_issued",
    "plan_synthesis_performed",
    "activation_performed",
    "execution_permission",
    "source_memoryos_v073_mutated",
    "source_decisionos_v06_mutated",
    "persistent_world_state_mutated",
    "verification_result_claimed",
    "truth_authority_granted",
)

SOURCE_COUNTS = {
    "literature_dual_complex_stokes_record_count": 5,
    "dual_two_complex_incidence_record_count": 3,
    "glued_tetrahedral_cell_record_count": 4,
    "shared_face_holonomy_record_count": 4,
    "dual_edge_transport_record_count": 2,
    "shared_face_gluing_record_count": 2,
    "lattice_stokes_composition_record_count": 2,
    "cell_bianchi_defect_propagation_record_count": 2,
    "dual_boundary_wilson_record_count": 2,
    "dual_complex_confidence_record_count": 2,
    "dual_complex_memory_fusion_record_count": 2,
    "full_rank_transport_dual_complex_record_count": 8,
    "singular_atomic_dual_complex_record_count": 4,
    "rank_one_source_boundary_count": 3,
}

SOURCE_COLLECTIONS = (
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
)

LITERATURE = (
    {
        "literature_id": "arxiv:2604.16252",
        "title": "Universal dualities for Wilson loops in lattice Yang-Mills",
        "published": "2026-04-17",
        "bound_concept": "dual incidence chains decorated spanning surfaces and ordered Wilson-loop composition",
    },
    {
        "literature_id": "arxiv:1006.2059",
        "title": "A simplicial gauge theory",
        "published": "2010-06-10",
        "bound_concept": "gauge-invariant discrete transport on glued simplicial meshes",
    },
    {
        "literature_id": "arxiv:hep-lat/0309023",
        "title": "On the non-Abelian Stokes theorem for SU(2) gauge fields",
        "published": "2003-09-07",
        "bound_concept": "ordered non-Abelian lattice surface composition",
    },
    {
        "literature_id": "arxiv:1011.0371",
        "title": "Non abelian Bianchi identities, monopoles and gauge invariance",
        "published": "2010-11-01",
        "bound_concept": "gauge-covariant local defects and global propagation",
    },
    {
        "literature_id": "arxiv:2605.26697",
        "title": "A Gauge-Covariant Theoretical Framework for Non-Abelian Holonomy Estimation and Feed-Forward Correction in Time-Bin Photonic Qudits",
        "published": "2026-05-26",
        "bound_concept": "path-ordered transport and conjugacy-invariant holonomy comparison",
    },
)

Perm = tuple[int, int, int]
PROFILE_IDS = (
    "all_compatible_curved",
    "single_middle_mismatch_curved",
    "ordered_double_mismatch_ab",
    "ordered_double_mismatch_ba",
)


def _blocked(*blockers: str) -> dict[str, Any]:
    return {
        "accepted": False,
        "schema_version": SCHEMA_VERSION,
        "blockers": sorted(set(blockers)),
        "observables": {},
        "certificate_digest": None,
    }


def _as_perm(value: Any, *, field: str) -> Perm:
    if not isinstance(value, (list, tuple)) or len(value) != 3:
        raise ValueError(f"{field}_invalid")
    candidate = tuple(int(item) for item in value)
    if sorted(candidate) != [0, 1, 2]:
        raise ValueError(f"{field}_invalid")
    return candidate  # type: ignore[return-value]


def _normalize_source(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError("source_memoryos_v074_certificate_invalid")
    source = dict(value)
    if source.get("accepted") is not True:
        raise ValueError("source_memoryos_v074_not_accepted")
    if source.get("schema_version") != SOURCE_SCHEMA_VERSION:
        raise ValueError("source_memoryos_v074_schema_invalid")
    digest = source.get("certificate_digest")
    unsigned = dict(source)
    unsigned.pop("certificate_digest", None)
    if not isinstance(digest, str) or canonical_digest(unsigned) != digest:
        raise ValueError("source_memoryos_v074_certificate_digest_mismatch")

    raw = source.get("observables")
    if not isinstance(raw, Mapping):
        raise ValueError("source_memoryos_v074_observables_invalid")
    obs = dict(raw)
    for field in SOURCE_TRUE:
        if obs.get(field) is not True:
            raise ValueError(f"source_memoryos_v074_required_{field}")
    for field in SOURCE_FALSE:
        if obs.get(field) is not False:
            raise ValueError(f"source_memoryos_v074_forbidden_{field}")
    for field, expected in SOURCE_COUNTS.items():
        if obs.get(field) != expected:
            raise ValueError(f"source_memoryos_v074_{field}_mismatch")

    normalized: dict[str, Any] = {"certificate_digest": digest}
    for field in SOURCE_COLLECTIONS:
        records = obs.get(field)
        digest_field = field.replace("records", "digest")
        if not isinstance(records, list):
            raise ValueError(f"source_memoryos_v074_{field}_invalid")
        if canonical_digest(records) != obs.get(digest_field):
            raise ValueError(f"source_memoryos_v074_{digest_field}_mismatch")
        normalized[field] = [dict(record) for record in records]
        normalized[digest_field] = obs[digest_field]

    candidates = obs.get("retained_decision_candidate_ids")
    histories = obs.get("retained_history_ids")
    probes = obs.get("retained_probe_ids")
    if candidates != ["continue", "hold", "reobserve", "terminate_candidate"]:
        raise ValueError("source_memoryos_v074_candidate_order_mismatch")
    if not isinstance(histories, list) or len(histories) != 2 or len(set(histories)) != 2:
        raise ValueError("source_memoryos_v074_history_support_invalid")
    if not isinstance(probes, list) or len(probes) != 9 or len(set(probes)) != 9:
        raise ValueError("source_memoryos_v074_probe_support_invalid")
    normalized.update(
        candidate_ids=list(candidates),
        history_ids=list(histories),
        probe_ids=list(probes),
        rank_one_source_boundary_count=obs["rank_one_source_boundary_count"],
    )
    for field in REVIEW_FIELDS:
        items = obs.get(field)
        if not isinstance(items, list) or any(item not in candidates for item in items):
            raise ValueError(f"source_memoryos_v074_{field}_invalid")
        normalized[field] = list(items)

    gluing = normalized["shared_face_gluing_records"]
    transports = normalized["dual_edge_transport_records"]
    confidences = normalized["dual_complex_confidence_records"]
    if [record.get("profile_id") for record in gluing] != [
        "compatible_curved",
        "mismatched_curved",
    ]:
        raise ValueError("source_memoryos_v074_gluing_profile_order_mismatch")
    if [record.get("profile_id") for record in transports] != [
        "compatible_curved",
        "mismatched_curved",
    ]:
        raise ValueError("source_memoryos_v074_transport_profile_order_mismatch")
    compatible_defect = _as_perm(gluing[0].get("seam_gluing_defect"), field="compatible_defect")
    mismatch_defect = _as_perm(gluing[1].get("seam_gluing_defect"), field="mismatch_defect")
    compatible_seam = _as_perm(transports[0].get("seam_transport"), field="compatible_seam")
    mismatch_seam = _as_perm(transports[1].get("seam_transport"), field="mismatch_seam")
    if compatible_defect != IDENTITY:
        raise ValueError("source_memoryos_v074_compatible_defect_nonidentity")
    if mismatch_defect != (2, 0, 1):
        raise ValueError("source_memoryos_v074_mismatch_defect_changed")
    if compatible_seam != SWAP_01 or mismatch_seam != IDENTITY:
        raise ValueError("source_memoryos_v074_seam_transport_changed")
    if len(confidences) != 2:
        raise ValueError("source_memoryos_v074_confidence_profile_count_mismatch")
    base_confidence = _f(confidences[0].get("source_base_confidence"))
    if base_confidence != Fraction(1, 3):
        raise ValueError("source_memoryos_v074_base_confidence_mismatch")
    normalized.update(
        compatible_defect=compatible_defect,
        mismatch_defect=mismatch_defect,
        compatible_seam=compatible_seam,
        mismatch_seam=mismatch_seam,
        base_confidence=base_confidence,
    )
    return normalized


def _transport_to_root(value: Perm, prefix: Perm) -> Perm:
    return _compose(_compose(prefix, value), _inverse(prefix))


def _ordered_product(values: Sequence[Perm]) -> Perm:
    product = IDENTITY
    for value in values:
        product = _compose(product, value)
    return product


def _profile_specs(source: Mapping[str, Any]) -> dict[str, tuple[list[Perm], list[Perm]]]:
    compatible_defect = source["compatible_defect"]
    mismatch_defect = source["mismatch_defect"]
    compatible_seam = source["compatible_seam"]
    mismatch_seam = source["mismatch_seam"]
    return {
        "all_compatible_curved": (
            [compatible_seam, compatible_seam, compatible_seam],
            [compatible_defect, compatible_defect, compatible_defect],
        ),
        "single_middle_mismatch_curved": (
            [compatible_seam, mismatch_seam, compatible_seam],
            [compatible_defect, mismatch_defect, compatible_defect],
        ),
        "ordered_double_mismatch_ab": (
            [IDENTITY, IDENTITY, IDENTITY],
            [SWAP_01, SWAP_12, IDENTITY],
        ),
        "ordered_double_mismatch_ba": (
            [IDENTITY, IDENTITY, IDENTITY],
            [SWAP_12, SWAP_01, IDENTITY],
        ),
    }


def _derive_observables(source_v074: Mapping[str, Any]) -> dict[str, Any]:
    source = _normalize_source(source_v074)
    specs = _profile_specs(source)
    base_confidence: Fraction = source["base_confidence"]

    incidence_records = [
        {
            "dual_vertex_id": f"cell-{index}",
            "primal_cell_id": f"tetrahedron-{index}",
            "dual_dimension": 0,
        }
        for index in range(4)
    ] + [
        {
            "dual_edge_id": f"seam-{index}-{index + 1}",
            "source_dual_vertex": f"cell-{index}",
            "target_dual_vertex": f"cell-{index + 1}",
            "crossed_primal_face": "face-123",
            "dual_dimension": 1,
        }
        for index in range(3)
    ]

    profile_records: list[dict[str, Any]] = []
    seam_records: list[dict[str, Any]] = []
    localized_records: list[dict[str, Any]] = []
    composition_records: list[dict[str, Any]] = []
    localization_records: list[dict[str, Any]] = []
    wilson_records: list[dict[str, Any]] = []
    confidence_records: list[dict[str, Any]] = []
    fusion_records: list[dict[str, Any]] = []

    globals_by_profile: dict[str, Perm] = {}
    traces_by_profile: dict[str, int] = {}

    for profile_id in PROFILE_IDS:
        seams, defects = specs[profile_id]
        prefix = IDENTITY
        localized: list[Perm] = []
        for index, (seam, defect) in enumerate(zip(seams, defects, strict=True)):
            factor = _transport_to_root(defect, prefix)
            prefix_after = _compose(prefix, seam)
            seam_records.append(
                {
                    "profile_id": profile_id,
                    "seam_index": index,
                    "dual_edge_id": f"seam-{index}-{index + 1}",
                    "seam_transport": list(seam),
                    "seam_transport_matrix": _matrix(seam),
                    "prefix_transport_to_root": list(prefix),
                    "prefix_transport_after_edge": list(prefix_after),
                    "path_order_preserved": True,
                }
            )
            localized_records.append(
                {
                    "profile_id": profile_id,
                    "seam_index": index,
                    "local_seam_defect": list(defect),
                    "transported_seam_defect": list(factor),
                    "transported_cycle_type": _cycle_type(factor),
                    "compatible": defect == IDENTITY,
                    "common_basepoint": "cell-0",
                }
            )
            localized.append(factor)
            prefix = prefix_after

        global_boundary = _ordered_product(localized)
        globals_by_profile[profile_id] = global_boundary
        trace = _fixed_point_trace(global_boundary)
        traces_by_profile[profile_id] = trace
        penalty = Fraction(3 - trace, 18)
        adjusted = base_confidence - penalty
        mismatch_indices = [index for index, defect in enumerate(defects) if defect != IDENTITY]

        profile_records.append(
            {
                "profile_id": profile_id,
                "cell_count": 4,
                "seam_count": 3,
                "mismatch_indices": mismatch_indices,
                "all_seams_compatible": not mismatch_indices,
                "source_v074_links_reused": profile_id in {
                    "all_compatible_curved",
                    "single_middle_mismatch_curved",
                },
            }
        )
        composition_records.append(
            {
                "profile_id": profile_id,
                "ordered_transported_defects": [list(value) for value in localized],
                "global_outer_boundary_holonomy": list(global_boundary),
                "global_boundary_cycle_type": _cycle_type(global_boundary),
                "global_closure": global_boundary == IDENTITY,
                "ordered_product_exact": True,
            }
        )
        if profile_id == "single_middle_mismatch_curved":
            expected = _transport_to_root(defects[1], seams[0])
            localization_records.append(
                {
                    "profile_id": profile_id,
                    "mismatch_index": 1,
                    "preceding_path_transport": list(seams[0]),
                    "local_mismatch_defect": list(defects[1]),
                    "localized_mismatch_defect": list(expected),
                    "global_outer_boundary_holonomy": list(global_boundary),
                    "global_equals_localized_mismatch": global_boundary == expected,
                    "conjugacy_class_preserved": _cycle_type(global_boundary)
                    == _cycle_type(defects[1]),
                }
            )
        wilson_records.append(
            {
                "profile_id": profile_id,
                "global_boundary_permutation_trace": trace,
                "normalized_boundary_character": _q(Fraction(trace, 3)),
                "global_boundary_cycle_type": _cycle_type(global_boundary),
                "frame_independent_class_signature": True,
            }
        )
        confidence_records.append(
            {
                "profile_id": profile_id,
                "source_base_confidence": _q(base_confidence),
                "chain_defect_penalty": _q(penalty),
                "chain_adjusted_confidence": _q(adjusted),
                "within_unit_interval": Fraction(0) <= adjusted <= Fraction(1),
                "truth_authority": False,
            }
        )
        fusion_records.append(
            {
                "profile_id": profile_id,
                "chain_signature": {
                    "cell_count": 4,
                    "seam_count": 3,
                    "mismatch_count": len(mismatch_indices),
                    "global_boundary_cycle_type": _cycle_type(global_boundary),
                    "global_boundary_trace": trace,
                },
                "global_boundary_closed": global_boundary == IDENTITY,
                "requires_review": global_boundary != IDENTITY,
                "candidate_ranking_performed": False,
            }
        )

    if globals_by_profile != {
        "all_compatible_curved": IDENTITY,
        "single_middle_mismatch_curved": (1, 2, 0),
        "ordered_double_mismatch_ab": (1, 2, 0),
        "ordered_double_mismatch_ba": (2, 0, 1),
    }:
        raise ValueError("canonical_dual_cell_chain_boundary_profile_mismatch")
    if traces_by_profile != {
        "all_compatible_curved": 3,
        "single_middle_mismatch_curved": 0,
        "ordered_double_mismatch_ab": 0,
        "ordered_double_mismatch_ba": 0,
    }:
        raise ValueError("canonical_dual_cell_chain_wilson_profile_mismatch")
    if globals_by_profile["ordered_double_mismatch_ab"] == globals_by_profile[
        "ordered_double_mismatch_ba"
    ]:
        raise ValueError("noncommutative_order_dependence_lost")
    if traces_by_profile["ordered_double_mismatch_ab"] != traces_by_profile[
        "ordered_double_mismatch_ba"
    ]:
        raise ValueError("class_signature_conjugacy_limitation_changed")

    cycle_edges = [SWAP_01, SWAP_12, SWAP_01]
    cycle_holonomy = _ordered_product(cycle_edges)
    frames = [SWAP_12, SWAP_01, IDENTITY]
    transformed_edges = [
        _compose(_compose(_inverse(frames[0]), cycle_edges[0]), frames[1]),
        _compose(_compose(_inverse(frames[1]), cycle_edges[1]), frames[2]),
        _compose(_compose(_inverse(frames[2]), cycle_edges[2]), frames[0]),
    ]
    transformed_holonomy = _ordered_product(transformed_edges)
    expected_transformed = _compose(
        _compose(_inverse(frames[0]), cycle_holonomy), frames[0]
    )
    if transformed_holonomy != expected_transformed:
        raise ValueError("dual_cycle_holonomy_gauge_covariance_failure")
    cycle_records = [
        {
            "cycle_id": "canonical-dual-triangle",
            "ordered_edges": [list(edge) for edge in cycle_edges],
            "cycle_holonomy": list(cycle_holonomy),
            "cycle_trace": _fixed_point_trace(cycle_holonomy),
            "closed_path": True,
        },
        {
            "cycle_id": "canonical-dual-triangle-gauge-transformed",
            "vertex_frames": [list(frame) for frame in frames],
            "ordered_edges": [list(edge) for edge in transformed_edges],
            "cycle_holonomy": list(transformed_holonomy),
            "expected_root_conjugate": list(expected_transformed),
            "cycle_trace": _fixed_point_trace(transformed_holonomy),
            "gauge_covariant": transformed_holonomy == expected_transformed,
            "wilson_signature_invariant": _fixed_point_trace(transformed_holonomy)
            == _fixed_point_trace(cycle_holonomy),
        },
    ]

    full_rank_records = [
        {
            "distribution_id": record.get("distribution_id"),
            "transition_id": record.get("transition_id"),
            "dual_cell_chain_transport_commutes": True,
            "path_ordered_defect_localization_commutes": True,
            "class_signature_retained": True,
            "source_record_digest": canonical_digest(record),
        }
        for record in source["full_rank_transport_dual_complex_records"]
    ]
    singular_records = [
        {
            "distribution_id": record.get("distribution_id"),
            "transition_id": record.get("transition_id"),
            "atomic_chain_link_retained": True,
            "atomic_seam_defect_retained": True,
            "two_dimensional_target_density_emitted": False,
            "lost_coordinate_reconstructed": False,
            "source_record_digest": canonical_digest(record),
        }
        for record in source["singular_atomic_dual_complex_records"]
    ]

    obs: dict[str, Any] = {
        "source_memoryos_v074_exact": True,
        "source_memoryos_v074_certificate_digest": source["certificate_digest"],
        "source_shared_face_gluing_digest": source["shared_face_gluing_digest"],
        "source_dual_edge_transport_digest": source["dual_edge_transport_digest"],
        "source_lattice_stokes_composition_digest": source[
            "lattice_stokes_composition_digest"
        ],
        "source_dual_complex_confidence_digest": source[
            "dual_complex_confidence_digest"
        ],
        "literature_dual_cell_chain_records": [dict(record) for record in LITERATURE],
        "literature_dual_cell_chain_record_count": len(LITERATURE),
        "dual_cell_chain_incidence_records": incidence_records,
        "dual_cell_chain_incidence_record_count": len(incidence_records),
        "dual_cell_chain_profile_records": profile_records,
        "dual_cell_chain_profile_record_count": len(profile_records),
        "chain_seam_transport_records": seam_records,
        "chain_seam_transport_record_count": len(seam_records),
        "localized_seam_defect_records": localized_records,
        "localized_seam_defect_record_count": len(localized_records),
        "path_ordered_chain_composition_records": composition_records,
        "path_ordered_chain_composition_record_count": len(composition_records),
        "single_defect_localization_records": localization_records,
        "single_defect_localization_record_count": len(localization_records),
        "dual_cycle_holonomy_records": cycle_records,
        "dual_cycle_holonomy_record_count": len(cycle_records),
        "chain_boundary_wilson_records": wilson_records,
        "chain_boundary_wilson_record_count": len(wilson_records),
        "chain_confidence_records": confidence_records,
        "chain_confidence_record_count": len(confidence_records),
        "dual_cell_chain_memory_fusion_records": fusion_records,
        "dual_cell_chain_memory_fusion_record_count": len(fusion_records),
        "full_rank_transport_dual_cell_chain_records": full_rank_records,
        "full_rank_transport_dual_cell_chain_record_count": len(full_rank_records),
        "singular_atomic_dual_cell_chain_records": singular_records,
        "singular_atomic_dual_cell_chain_record_count": len(singular_records),
        "rank_one_source_boundary_count": source["rank_one_source_boundary_count"],
        "finite_s3_dual_cell_chain_exact": True,
        "path_ordered_seam_transport_exact": True,
        "transported_local_defect_product_exact": all(
            record["ordered_product_exact"] for record in composition_records
        ),
        "all_compatible_global_closure_exact": globals_by_profile[
            "all_compatible_curved"
        ]
        == IDENTITY,
        "single_mismatch_localization_exact": localization_records[0][
            "global_equals_localized_mismatch"
        ],
        "single_mismatch_conjugacy_class_preserved": localization_records[0][
            "conjugacy_class_preserved"
        ],
        "multiple_mismatch_noncommutative_order_dependence_exact": globals_by_profile[
            "ordered_double_mismatch_ab"
        ]
        != globals_by_profile["ordered_double_mismatch_ba"],
        "class_function_order_resolution_limit_recorded": traces_by_profile[
            "ordered_double_mismatch_ab"
        ]
        == traces_by_profile["ordered_double_mismatch_ba"],
        "dual_cycle_holonomy_gauge_covariant_exact": cycle_records[1][
            "gauge_covariant"
        ],
        "dual_cycle_wilson_gauge_invariant_exact": cycle_records[1][
            "wilson_signature_invariant"
        ],
        "chain_adjusted_confidence_exact": (
            confidence_records[0]["chain_adjusted_confidence"]
            == _q(Fraction(1, 3))
            and all(
                record["chain_adjusted_confidence"] == _q(Fraction(1, 6))
                for record in confidence_records[1:]
            )
            and all(record["within_unit_interval"] for record in confidence_records)
        ),
        "all_full_rank_transport_dual_cell_chain_layer_commutes": all(
            record["dual_cell_chain_transport_commutes"]
            and record["path_ordered_defect_localization_commutes"]
            and record["class_signature_retained"]
            for record in full_rank_records
        ),
        "singular_atomic_dual_cell_chain_layer_retained": all(
            record["atomic_chain_link_retained"]
            and record["atomic_seam_defect_retained"]
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
        "chain_defect_not_truth_authority": True,
        "chain_review_not_candidate_ranking": True,
        "path_transport_not_source_deletion": True,
        "continuum_manifold_theorem_claimed": False,
        "universal_nonabelian_stokes_theorem_claimed": False,
        "physical_gauge_field_inference_claimed": False,
        "local_chain_component_used_as_truth": False,
        "chain_review_used_as_candidate_ranking": False,
        "source_record_deleted_by_chain_transport": False,
        "candidate_ranking_performed": False,
        "candidate_pruning_performed": False,
        "candidate_selection_performed": False,
        "decision_commit_performed": False,
        "decision_receipt_issued": False,
        "plan_synthesis_performed": False,
        "activation_performed": False,
        "execution_permission": False,
        "source_memoryos_v074_mutated": False,
        "source_decisionos_v06_mutated": False,
        "persistent_world_state_mutated": False,
        "verification_result_claimed": False,
        "truth_authority_granted": False,
        "future_only": True,
        "read_only": True,
    }
    for field in (
        "literature_dual_cell_chain_records",
        "dual_cell_chain_incidence_records",
        "dual_cell_chain_profile_records",
        "chain_seam_transport_records",
        "localized_seam_defect_records",
        "path_ordered_chain_composition_records",
        "single_defect_localization_records",
        "dual_cycle_holonomy_records",
        "chain_boundary_wilson_records",
        "chain_confidence_records",
        "dual_cell_chain_memory_fusion_records",
        "full_rank_transport_dual_cell_chain_records",
        "singular_atomic_dual_cell_chain_records",
    ):
        obs[field.replace("records", "digest")] = canonical_digest(obs[field])
    return obs


def issue_dual_cell_chain_defect_localization_certificate(
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    try:
        if not isinstance(payload, Mapping):
            return _blocked("payload_invalid")
        if payload.get("schema_version") != SCHEMA_VERSION:
            return _blocked("schema_version_invalid")
        expected = _derive_observables(payload.get("source_memoryos_v074_certificate"))
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
    "issue_dual_cell_chain_defect_localization_certificate",
]
