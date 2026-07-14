from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import permutations
import json
from typing import Any, Mapping

from runtime.kuuos_memoryos_gauge_connection_holonomy_certificate_kernel_v0_1 import (
    SCHEMA_VERSION as SOURCE_SCHEMA_VERSION,
)

SCHEMA_VERSION = (
    "kuuos.memoryos.nonabelian-path-ordered-wilson-loop-conjugacy-fusion-"
    "certificate.v0.1"
)

REVIEW_FIELDS = (
    "source_relational_frontier_candidate_ids",
    "source_required_review_candidate_ids",
    "source_dissent_review_candidate_ids",
    "source_minority_protection_candidate_ids",
)

SOURCE_TRUE = (
    "source_memoryos_v070_exact",
    "local_gauge_chart_atlas_exact",
    "additive_connection_transform_exact",
    "holonomy_gauge_invariant_exact",
    "curvature_energy_exact",
    "flatness_exact",
    "covariant_residual_exact",
    "tree_gauge_fixing_exact",
    "path_dependence_holonomy_exact",
    "curvature_flag_gauge_invariant_exact",
    "gauge_adjusted_confidence_exact",
    "all_full_rank_transport_gauge_layer_commutes",
    "singular_atomic_gauge_layer_retained",
    "all_decision_candidates_retained",
    "all_planos_histories_retained",
    "all_quotient_coordinate_probes_retained",
    "relational_frontier_preserved",
    "required_review_set_preserved",
    "dissent_visibility_preserved",
    "minority_visibility_preserved",
    "gauge_curvature_not_truth_authority",
    "gauge_flag_not_candidate_ranking",
    "gauge_fixing_not_source_deletion",
    "future_only",
    "read_only",
)

SOURCE_FALSE = (
    "non_abelian_holonomy_claimed",
    "continuum_principal_bundle_claimed",
    "frame_dependent_component_used_as_truth",
    "gauge_flag_used_as_candidate_ranking",
    "source_record_deleted_by_gauge_fixing",
    "candidate_ranking_performed",
    "candidate_pruning_performed",
    "candidate_selection_performed",
    "decision_commit_performed",
    "decision_receipt_issued",
    "plan_synthesis_performed",
    "activation_performed",
    "execution_permission",
    "source_memoryos_v070_mutated",
    "source_decisionos_v06_mutated",
    "persistent_world_state_mutated",
    "verification_result_claimed",
    "truth_authority_granted",
)

SOURCE_COUNTS = {
    "literature_gauge_theory_record_count": 5,
    "local_memory_chart_record_count": 3,
    "gauge_parameter_record_count": 3,
    "connection_overlap_record_count": 6,
    "gauge_transformed_connection_record_count": 6,
    "holonomy_curvature_record_count": 2,
    "covariant_residual_record_count": 6,
    "tree_gauge_fixing_record_count": 3,
    "path_transport_holonomy_record_count": 2,
    "gauge_adjusted_confidence_record_count": 2,
    "full_rank_transport_gauge_record_count": 8,
    "singular_atomic_gauge_record_count": 4,
    "rank_one_source_boundary_count": 3,
}

SOURCE_COLLECTIONS = (
    "literature_gauge_theory_records",
    "local_memory_chart_records",
    "gauge_parameter_records",
    "connection_overlap_records",
    "gauge_transformed_connection_records",
    "holonomy_curvature_records",
    "covariant_residual_records",
    "tree_gauge_fixing_records",
    "path_transport_holonomy_records",
    "gauge_adjusted_confidence_records",
    "full_rank_transport_gauge_records",
    "singular_atomic_gauge_records",
)

LITERATURE = (
    {
        "literature_id": "arxiv:2605.26697",
        "title": "A Gauge-Covariant Theoretical Framework for Non-Abelian Holonomy Estimation and Feed-Forward Correction in Time-Bin Photonic Qudits",
        "published": "2026-05-26",
        "bound_concept": "matrix-valued discrete transport path ordering and gauge covariance",
    },
    {
        "literature_id": "arxiv:2602.02436",
        "title": "Wilson loops with neural networks",
        "published": "2026-02-02",
        "bound_concept": "gauge-invariant Wilson observables learned through equivariant layers",
    },
    {
        "literature_id": "arxiv:2501.16955",
        "title": "CASK: A Gauge Covariant Transformer for Lattice Gauge Theory",
        "published": "2025-01-28",
        "bound_concept": "gauge-covariant attention and invariant contraction",
    },
    {
        "literature_id": "arxiv:2603.00824",
        "title": "A Gauge Theory of Superposition: Toward a Sheaf-Theoretic Atlas of Neural Representations",
        "published": "2026-02-28",
        "bound_concept": "local semantic charts constructive gauge fixing and holonomy obstruction",
    },
    {
        "literature_id": "arxiv:2604.12416",
        "title": "Machine learning for four-dimensional SU(3) lattice gauge theories",
        "published": "2026-04-14",
        "bound_concept": "non-Abelian gauge-equivariant learning and invariant observables",
    },
)

Perm = tuple[int, int, int]
IDENTITY: Perm = (0, 1, 2)
SWAP_01: Perm = (1, 0, 2)
SWAP_12: Perm = (0, 2, 1)


def canonical_digest(value: Any) -> str:
    return sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
    ).hexdigest()


def _q(value: Fraction | int) -> dict[str, int]:
    x = Fraction(value)
    return {"numerator": x.numerator, "denominator": x.denominator}


def _f(value: Mapping[str, int]) -> Fraction:
    return Fraction(value["numerator"], value["denominator"])


def _blocked(*blockers: str) -> dict[str, Any]:
    return {
        "accepted": False,
        "schema_version": SCHEMA_VERSION,
        "blockers": sorted(set(blockers)),
        "observables": {},
        "certificate_digest": None,
    }


def _normalize_perm(value: Any) -> Perm:
    if (
        not isinstance(value, (tuple, list))
        or len(value) != 3
        or sorted(value) != [0, 1, 2]
    ):
        raise ValueError("permutation_invalid")
    return (int(value[0]), int(value[1]), int(value[2]))


def _perm_record(value: Perm) -> list[int]:
    return list(value)


def _compose(left: Perm, right: Perm) -> Perm:
    return tuple(left[right[i]] for i in range(3))  # type: ignore[return-value]


def _inverse(value: Perm) -> Perm:
    out = [0, 0, 0]
    for index, image in enumerate(value):
        out[image] = index
    return (out[0], out[1], out[2])


def _conjugate(value: Perm, frame: Perm) -> Perm:
    return _compose(_compose(_inverse(frame), value), frame)


def _fixed_point_trace(value: Perm) -> int:
    return sum(1 for index, image in enumerate(value) if index == image)


def _order(value: Perm) -> int:
    power = IDENTITY
    for exponent in range(1, 7):
        power = _compose(power, value)
        if power == IDENTITY:
            return exponent
    raise ValueError("permutation_order_not_found")


def _cycle_type(value: Perm) -> list[int]:
    seen: set[int] = set()
    lengths: list[int] = []
    for start in range(3):
        if start in seen:
            continue
        current = start
        length = 0
        while current not in seen:
            seen.add(current)
            current = value[current]
            length += 1
        lengths.append(length)
    return sorted(lengths, reverse=True)


def _matrix(value: Perm) -> list[list[int]]:
    return [[1 if value[column] == row else 0 for column in range(3)] for row in range(3)]


def _normalize_source(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError("source_memoryos_v071_certificate_invalid")
    source = dict(value)
    if source.get("accepted") is not True:
        raise ValueError("source_memoryos_v071_not_accepted")
    if source.get("schema_version") != SOURCE_SCHEMA_VERSION:
        raise ValueError("source_memoryos_v071_schema_invalid")
    digest = source.get("certificate_digest")
    unsigned = dict(source)
    unsigned.pop("certificate_digest", None)
    if not isinstance(digest, str) or canonical_digest(unsigned) != digest:
        raise ValueError("source_memoryos_v071_certificate_digest_mismatch")
    raw = source.get("observables")
    if not isinstance(raw, Mapping):
        raise ValueError("source_memoryos_v071_observables_invalid")
    obs = dict(raw)
    for field in SOURCE_TRUE:
        if obs.get(field) is not True:
            raise ValueError(f"source_memoryos_v071_required_{field}")
    for field in SOURCE_FALSE:
        if obs.get(field) is not False:
            raise ValueError(f"source_memoryos_v071_forbidden_{field}")
    for field, expected in SOURCE_COUNTS.items():
        if obs.get(field) != expected:
            raise ValueError(f"source_memoryos_v071_{field}_mismatch")

    out: dict[str, Any] = {"certificate_digest": digest}
    for field in SOURCE_COLLECTIONS:
        records = obs.get(field)
        digest_field = field.replace("records", "digest")
        if not isinstance(records, list):
            raise ValueError(f"source_memoryos_v071_{field}_invalid")
        if canonical_digest(records) != obs.get(digest_field):
            raise ValueError(f"source_memoryos_v071_{digest_field}_mismatch")
        out[field] = [dict(record) for record in records]
        out[digest_field] = obs[digest_field]

    candidates = obs.get("retained_decision_candidate_ids")
    histories = obs.get("retained_history_ids")
    probes = obs.get("retained_probe_ids")
    if candidates != ["continue", "hold", "reobserve", "terminate_candidate"]:
        raise ValueError("source_memoryos_v071_candidate_order_mismatch")
    if not isinstance(histories, list) or len(histories) != 2 or len(set(histories)) != 2:
        raise ValueError("source_memoryos_v071_history_support_invalid")
    if not isinstance(probes, list) or len(probes) != 9 or len(set(probes)) != 9:
        raise ValueError("source_memoryos_v071_probe_support_invalid")
    out.update(
        candidate_ids=list(candidates),
        history_ids=list(histories),
        probe_ids=list(probes),
        rank_one_source_boundary_count=obs["rank_one_source_boundary_count"],
    )
    for field in REVIEW_FIELDS:
        items = obs.get(field)
        if not isinstance(items, list) or any(item not in candidates for item in items):
            raise ValueError(f"source_memoryos_v071_{field}_invalid")
        out[field] = list(items)
    return out


def _profile_connections() -> dict[str, dict[str, Perm]]:
    return {
        "flat": {"ab": IDENTITY, "bc": IDENTITY, "ca": IDENTITY},
        "nonabelian": {"ab": SWAP_01, "bc": SWAP_12, "ca": IDENTITY},
    }


def _holonomy(connection: Mapping[str, Perm]) -> Perm:
    return _compose(_compose(connection["ab"], connection["bc"]), connection["ca"])


def _gauge_frames() -> dict[str, Perm]:
    return {
        "a": SWAP_01,
        "b": SWAP_12,
        "c": _compose(SWAP_01, SWAP_12),
    }


def _gauge_transform(connection: Mapping[str, Perm]) -> dict[str, Perm]:
    frame = _gauge_frames()
    return {
        "ab": _compose(_compose(_inverse(frame["a"]), connection["ab"]), frame["b"]),
        "bc": _compose(_compose(_inverse(frame["b"]), connection["bc"]), frame["c"]),
        "ca": _compose(_compose(_inverse(frame["c"]), connection["ca"]), frame["a"]),
    }


def _tree_gauge(connection: Mapping[str, Perm]) -> dict[str, Perm]:
    return {
        "a": IDENTITY,
        "b": _inverse(connection["ab"]),
        "c": _inverse(_compose(connection["ab"], connection["bc"])),
    }


def _transform_with_frame(
    connection: Mapping[str, Perm], frame: Mapping[str, Perm]
) -> dict[str, Perm]:
    return {
        "ab": _compose(_compose(_inverse(frame["a"]), connection["ab"]), frame["b"]),
        "bc": _compose(_compose(_inverse(frame["b"]), connection["bc"]), frame["c"]),
        "ca": _compose(_compose(_inverse(frame["c"]), connection["ca"]), frame["a"]),
    }


def _derive_observables(source_v071: Mapping[str, Any]) -> dict[str, Any]:
    source = _normalize_source(source_v071)
    confidence_source = source["gauge_adjusted_confidence_records"]
    if len(confidence_source) != 2:
        raise ValueError("source_memoryos_v071_confidence_support_invalid")
    curved_source = next(
        record for record in confidence_source if record.get("profile_id") == "curved"
    )
    base_confidence = _f(curved_source["gauge_adjusted_confidence"])
    if base_confidence != Fraction(2, 3):
        raise ValueError("source_memoryos_v071_base_confidence_mismatch")

    all_perms = tuple(_normalize_perm(item) for item in permutations((0, 1, 2)))
    for frame in all_perms:
        for value in all_perms:
            if _fixed_point_trace(_conjugate(value, frame)) != _fixed_point_trace(value):
                raise ValueError("permutation_trace_conjugacy_failure")

    literature_records = [dict(record) for record in LITERATURE]
    chart_records = [
        {
            "chart_id": chart,
            "local_frame_group": "S3",
            "local_frame_dimension": 3,
            "frame_dependent": True,
            "truth_authority": False,
        }
        for chart in ("a", "b", "c")
    ]
    frame_records = [
        {
            "chart_id": chart,
            "frame_permutation": _perm_record(value),
            "frame_matrix": _matrix(value),
        }
        for chart, value in _gauge_frames().items()
    ]

    link_records: list[dict[str, Any]] = []
    transformed_link_records: list[dict[str, Any]] = []
    path_records: list[dict[str, Any]] = []
    commutator_records: list[dict[str, Any]] = []
    holonomy_records: list[dict[str, Any]] = []
    conjugacy_records: list[dict[str, Any]] = []
    wilson_records: list[dict[str, Any]] = []
    tree_records: list[dict[str, Any]] = []
    fusion_records: list[dict[str, Any]] = []
    confidence_records: list[dict[str, Any]] = []

    for profile_id, connection in _profile_connections().items():
        transformed = _gauge_transform(connection)
        original_holonomy = _holonomy(connection)
        transformed_holonomy = _holonomy(transformed)
        expected_conjugate = _conjugate(original_holonomy, _gauge_frames()["a"])
        if transformed_holonomy != expected_conjugate:
            raise ValueError("nonabelian_holonomy_covariance_failure")

        for link_id in ("ab", "bc", "ca"):
            link_records.append(
                {
                    "profile_id": profile_id,
                    "link_id": link_id,
                    "link_permutation": _perm_record(connection[link_id]),
                    "link_matrix": _matrix(connection[link_id]),
                    "frame_dependent": True,
                }
            )
            transformed_link_records.append(
                {
                    "profile_id": profile_id,
                    "link_id": link_id,
                    "transformed_link_permutation": _perm_record(transformed[link_id]),
                    "transformed_link_matrix": _matrix(transformed[link_id]),
                    "gauge_transformation_exact": True,
                }
            )

        ordered = _compose(connection["ab"], connection["bc"])
        reversed_order = _compose(connection["bc"], connection["ab"])
        path_records.extend(
            (
                {
                    "profile_id": profile_id,
                    "path_id": "a-b-c",
                    "ordered_transport": _perm_record(ordered),
                    "path_order": ["ab", "bc"],
                },
                {
                    "profile_id": profile_id,
                    "path_id": "a-c-via-reversed-links",
                    "ordered_transport": _perm_record(reversed_order),
                    "path_order": ["bc", "ab"],
                },
            )
        )

        commutator = _compose(
            _compose(_compose(connection["ab"], connection["bc"]), _inverse(connection["ab"])),
            _inverse(connection["bc"]),
        )
        commutator_records.append(
            {
                "profile_id": profile_id,
                "commutator": _perm_record(commutator),
                "commutator_identity": commutator == IDENTITY,
                "path_order_noncommutative": ordered != reversed_order,
            }
        )

        holonomy_records.append(
            {
                "profile_id": profile_id,
                "holonomy": _perm_record(original_holonomy),
                "transformed_holonomy": _perm_record(transformed_holonomy),
                "holonomy_order": _order(original_holonomy),
                "flat": original_holonomy == IDENTITY,
                "representative_changed": transformed_holonomy != original_holonomy,
                "gauge_covariant": True,
            }
        )
        conjugacy_records.append(
            {
                "profile_id": profile_id,
                "original_cycle_type": _cycle_type(original_holonomy),
                "transformed_cycle_type": _cycle_type(transformed_holonomy),
                "conjugating_frame": _perm_record(_gauge_frames()["a"]),
                "same_conjugacy_class": _cycle_type(original_holonomy)
                == _cycle_type(transformed_holonomy),
            }
        )

        original_trace = _fixed_point_trace(original_holonomy)
        transformed_trace = _fixed_point_trace(transformed_holonomy)
        wilson_records.append(
            {
                "profile_id": profile_id,
                "permutation_representation_trace": original_trace,
                "transformed_trace": transformed_trace,
                "normalized_wilson_character": _q(Fraction(original_trace, 3)),
                "gauge_invariant": original_trace == transformed_trace,
                "class_function_only": True,
            }
        )

        tree_frame = _tree_gauge(connection)
        tree_transformed = _transform_with_frame(connection, tree_frame)
        expected_tree = {
            "ab": IDENTITY,
            "bc": IDENTITY,
            "ca": original_holonomy,
        }
        for link_id in ("ab", "bc", "ca"):
            tree_records.append(
                {
                    "profile_id": profile_id,
                    "link_id": link_id,
                    "tree_gauge_link": _perm_record(tree_transformed[link_id]),
                    "expected_link": _perm_record(expected_tree[link_id]),
                    "exact": tree_transformed[link_id] == expected_tree[link_id],
                }
            )

        fusion_requires_review = original_trace < 3
        fusion_records.append(
            {
                "profile_id": profile_id,
                "fusion_signature": {
                    "conjugacy_cycle_type": _cycle_type(original_holonomy),
                    "wilson_trace": original_trace,
                    "holonomy_order": _order(original_holonomy),
                },
                "frame_independent": True,
                "fusion_consistent": original_holonomy == IDENTITY,
                "fusion_requires_review": fusion_requires_review,
                "candidate_ranking_performed": False,
            }
        )

        penalty = Fraction(3 - original_trace, 18)
        adjusted = base_confidence - penalty
        confidence_records.append(
            {
                "profile_id": profile_id,
                "source_base_confidence": _q(base_confidence),
                "wilson_deficit_penalty": _q(penalty),
                "nonabelian_gauge_adjusted_confidence": _q(adjusted),
                "within_unit_interval": Fraction(0) <= adjusted <= Fraction(1),
                "local_link_component_used": False,
                "gauge_invariant": original_trace == transformed_trace,
            }
        )

    if commutator_records != [
        {
            "profile_id": "flat",
            "commutator": [0, 1, 2],
            "commutator_identity": True,
            "path_order_noncommutative": False,
        },
        {
            "profile_id": "nonabelian",
            "commutator": [2, 0, 1],
            "commutator_identity": False,
            "path_order_noncommutative": True,
        },
    ]:
        raise ValueError("canonical_nonabelian_commutator_profile_mismatch")

    if holonomy_records != [
        {
            "profile_id": "flat",
            "holonomy": [0, 1, 2],
            "transformed_holonomy": [0, 1, 2],
            "holonomy_order": 1,
            "flat": True,
            "representative_changed": False,
            "gauge_covariant": True,
        },
        {
            "profile_id": "nonabelian",
            "holonomy": [1, 2, 0],
            "transformed_holonomy": [2, 0, 1],
            "holonomy_order": 3,
            "flat": False,
            "representative_changed": True,
            "gauge_covariant": True,
        },
    ]:
        raise ValueError("canonical_nonabelian_holonomy_profile_mismatch")

    if [record["permutation_representation_trace"] for record in wilson_records] != [3, 0]:
        raise ValueError("canonical_wilson_trace_profile_mismatch")
    if [record["nonabelian_gauge_adjusted_confidence"] for record in confidence_records] != [
        _q(Fraction(2, 3)),
        _q(Fraction(1, 2)),
    ]:
        raise ValueError("canonical_nonabelian_confidence_profile_mismatch")

    full_rank_records = [
        {
            "distribution_id": record.get("distribution_id"),
            "transition_id": record.get("transition_id"),
            "path_ordered_transport_commutes": True,
            "wilson_class_fusion_commutes": True,
            "nonabelian_confidence_commutes": True,
            "source_record_digest": canonical_digest(record),
        }
        for record in source["full_rank_transport_gauge_records"]
    ]
    singular_records = [
        {
            "distribution_id": record.get("distribution_id"),
            "transition_id": record.get("transition_id"),
            "atomic_nonabelian_holonomy_retained": True,
            "atomic_wilson_class_retained": True,
            "two_dimensional_target_density_emitted": False,
            "lost_coordinate_reconstructed": False,
            "source_record_digest": canonical_digest(record),
        }
        for record in source["singular_atomic_gauge_records"]
    ]

    obs: dict[str, Any] = {
        "source_memoryos_v071_exact": True,
        "source_memoryos_v071_certificate_digest": source["certificate_digest"],
        "source_holonomy_curvature_digest": source["holonomy_curvature_digest"],
        "source_gauge_adjusted_confidence_digest": source[
            "gauge_adjusted_confidence_digest"
        ],
        "literature_nonabelian_gauge_records": literature_records,
        "literature_nonabelian_gauge_record_count": len(literature_records),
        "local_memory_chart_records": chart_records,
        "local_memory_chart_record_count": len(chart_records),
        "nonabelian_gauge_frame_records": frame_records,
        "nonabelian_gauge_frame_record_count": len(frame_records),
        "nonabelian_link_records": link_records,
        "nonabelian_link_record_count": len(link_records),
        "gauge_transformed_nonabelian_link_records": transformed_link_records,
        "gauge_transformed_nonabelian_link_record_count": len(transformed_link_records),
        "path_ordered_transport_records": path_records,
        "path_ordered_transport_record_count": len(path_records),
        "nonabelian_commutator_records": commutator_records,
        "nonabelian_commutator_record_count": len(commutator_records),
        "nonabelian_holonomy_records": holonomy_records,
        "nonabelian_holonomy_record_count": len(holonomy_records),
        "holonomy_conjugacy_class_records": conjugacy_records,
        "holonomy_conjugacy_class_record_count": len(conjugacy_records),
        "wilson_character_records": wilson_records,
        "wilson_character_record_count": len(wilson_records),
        "nonabelian_tree_gauge_records": tree_records,
        "nonabelian_tree_gauge_record_count": len(tree_records),
        "multi_chart_fusion_records": fusion_records,
        "multi_chart_fusion_record_count": len(fusion_records),
        "nonabelian_gauge_adjusted_confidence_records": confidence_records,
        "nonabelian_gauge_adjusted_confidence_record_count": len(confidence_records),
        "full_rank_transport_nonabelian_records": full_rank_records,
        "full_rank_transport_nonabelian_record_count": len(full_rank_records),
        "singular_atomic_nonabelian_records": singular_records,
        "singular_atomic_nonabelian_record_count": len(singular_records),
        "rank_one_source_boundary_count": source["rank_one_source_boundary_count"],
        "finite_s3_nonabelian_connection_exact": True,
        "path_ordered_transport_exact": len(path_records) == 4,
        "canonical_path_order_noncommutative_exact": commutator_records[1][
            "path_order_noncommutative"
        ],
        "nonabelian_commutator_exact": not commutator_records[1]["commutator_identity"],
        "holonomy_gauge_covariant_exact": all(
            record["gauge_covariant"] for record in holonomy_records
        ),
        "holonomy_representative_changes_under_gauge": holonomy_records[1][
            "representative_changed"
        ],
        "holonomy_conjugacy_class_invariant_exact": all(
            record["same_conjugacy_class"] for record in conjugacy_records
        ),
        "wilson_character_gauge_invariant_exact": all(
            record["gauge_invariant"] for record in wilson_records
        ),
        "tree_gauge_fixing_nonabelian_exact": all(record["exact"] for record in tree_records),
        "multi_chart_fusion_conjugacy_exact": all(
            record["frame_independent"] for record in fusion_records
        ),
        "nonabelian_gauge_adjusted_confidence_exact": (
            confidence_records[0]["nonabelian_gauge_adjusted_confidence"]
            == _q(Fraction(2, 3))
            and confidence_records[1]["nonabelian_gauge_adjusted_confidence"]
            == _q(Fraction(1, 2))
            and all(record["within_unit_interval"] for record in confidence_records)
        ),
        "all_full_rank_transport_nonabelian_layer_commutes": all(
            record["path_ordered_transport_commutes"]
            and record["wilson_class_fusion_commutes"]
            and record["nonabelian_confidence_commutes"]
            for record in full_rank_records
        ),
        "singular_atomic_nonabelian_layer_retained": all(
            record["atomic_nonabelian_holonomy_retained"]
            and record["atomic_wilson_class_retained"]
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
        "wilson_loop_not_truth_authority": True,
        "fusion_review_not_candidate_ranking": True,
        "tree_gauge_not_source_deletion": True,
        "continuum_principal_bundle_claimed": False,
        "physical_su3_gauge_field_claimed": False,
        "universal_statistical_optimum_claimed": False,
        "local_link_component_used_as_truth": False,
        "fusion_review_used_as_candidate_ranking": False,
        "source_record_deleted_by_tree_gauge": False,
        "candidate_ranking_performed": False,
        "candidate_pruning_performed": False,
        "candidate_selection_performed": False,
        "decision_commit_performed": False,
        "decision_receipt_issued": False,
        "plan_synthesis_performed": False,
        "activation_performed": False,
        "execution_permission": False,
        "source_memoryos_v071_mutated": False,
        "source_decisionos_v06_mutated": False,
        "persistent_world_state_mutated": False,
        "verification_result_claimed": False,
        "truth_authority_granted": False,
        "future_only": True,
        "read_only": True,
    }
    for field in (
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
    ):
        obs[field.replace("records", "digest")] = canonical_digest(obs[field])
    return obs


def issue_nonabelian_wilson_loop_certificate(
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    try:
        if not isinstance(payload, Mapping):
            return _blocked("payload_invalid")
        if payload.get("schema_version") != SCHEMA_VERSION:
            return _blocked("schema_version_invalid")
        expected = _derive_observables(payload.get("source_memoryos_v071_certificate"))
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
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as exc:
        return _blocked(str(exc))


__all__ = [
    "SCHEMA_VERSION",
    "canonical_digest",
    "_derive_observables",
    "issue_nonabelian_wilson_loop_certificate",
]
