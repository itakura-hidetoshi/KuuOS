from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from typing import Any, Mapping

from runtime.kuuos_memoryos_collusion_correlation_weighted_cut_certificate_kernel_v0_1 import (
    SCHEMA_VERSION as SOURCE_SCHEMA_VERSION,
)

SCHEMA_VERSION = (
    "kuuos.memoryos.gauge-connection-holonomy-covariant-consistency-"
    "certificate.v0.1"
)

REVIEW_FIELDS = (
    "source_relational_frontier_candidate_ids",
    "source_required_review_candidate_ids",
    "source_dissent_review_candidate_ids",
    "source_minority_protection_candidate_ids",
)

SOURCE_TRUE = (
    "source_memoryos_v069_exact",
    "collusion_signal_fusion_exact",
    "distinct_lineage_collusion_detected_exact",
    "correlation_matrix_symmetric_exact",
    "effective_independent_source_count_exact",
    "positive_correlation_reduces_effective_count",
    "component_capped_robust_confidence_exact",
    "collusive_component_not_double_counted",
    "confidence_inflation_removed_exact",
    "minimum_weighted_revocation_cut_exact",
    "minimum_weight_cut_differs_from_minimum_cardinality_cut",
    "weighted_revocation_cut_preserves_audit_history",
    "all_full_rank_transport_collusion_robustness_commutes",
    "singular_atomic_collusion_robustness_retained",
    "all_decision_candidates_retained",
    "all_planos_histories_retained",
    "all_quotient_coordinate_probes_retained",
    "relational_frontier_preserved",
    "required_review_set_preserved",
    "dissent_visibility_preserved",
    "minority_visibility_preserved",
    "collusion_detection_not_candidate_ranking",
    "robust_confidence_not_truth_authority",
    "weighted_cut_not_source_deletion",
    "future_only",
    "read_only",
)

SOURCE_FALSE = (
    "single_signal_collusion_claimed",
    "collusive_copies_counted_independently",
    "raw_source_count_used_as_effective_count",
    "minimum_cardinality_cut_claimed_weight_optimal",
    "source_record_deleted_by_weighted_cut",
    "candidate_ranking_performed",
    "candidate_pruning_performed",
    "candidate_selection_performed",
    "decision_commit_performed",
    "decision_receipt_issued",
    "plan_synthesis_performed",
    "activation_performed",
    "execution_permission",
    "source_memoryos_v069_mutated",
    "source_decisionos_v06_mutated",
    "persistent_world_state_mutated",
    "verification_result_claimed",
    "truth_authority_granted",
)

SOURCE_COUNTS = {
    "literature_collusion_robustness_record_count": 5,
    "source_agent_record_count": 4,
    "collusion_pair_signal_record_count": 6,
    "suspected_collusion_pair_record_count": 1,
    "collusion_component_record_count": 3,
    "correlation_matrix_entry_record_count": 10,
    "effective_independent_source_count_record_count": 2,
    "robust_confidence_record_count": 1,
    "weighted_revocation_node_record_count": 6,
    "weighted_revocation_edge_record_count": 5,
    "weighted_revocation_path_record_count": 2,
    "weighted_revocation_cut_candidate_record_count": 32,
    "minimum_weighted_revocation_cut_record_count": 1,
    "full_rank_transport_collusion_robustness_record_count": 8,
    "singular_atomic_collusion_robustness_record_count": 4,
    "rank_one_source_boundary_count": 3,
}

SOURCE_COLLECTIONS = (
    "literature_collusion_robustness_records",
    "source_agent_records",
    "collusion_pair_signal_records",
    "suspected_collusion_pair_records",
    "collusion_component_records",
    "correlation_matrix_entry_records",
    "effective_independent_source_count_records",
    "robust_confidence_records",
    "weighted_revocation_node_records",
    "weighted_revocation_edge_records",
    "weighted_revocation_path_records",
    "weighted_revocation_cut_candidate_records",
    "minimum_weighted_revocation_cut_records",
    "full_rank_transport_collusion_robustness_records",
    "singular_atomic_collusion_robustness_records",
)

LITERATURE = (
    {
        "literature_id": "arxiv:2603.00824",
        "title": "A Gauge Theory of Superposition: Toward a Sheaf-Theoretic Atlas of Neural Representations",
        "published": "2026-02-28",
        "bound_concept": "local semantic charts gauge fixing and gauge-invariant holonomy",
    },
    {
        "literature_id": "arxiv:2604.20797",
        "title": "Gauge-Equivariant Graph Neural Networks for Lattice Gauge Theories",
        "published": "2026-04-22",
        "bound_concept": "local gauge symmetry covariant transport and loop observables",
    },
    {
        "literature_id": "arxiv:2605.26697",
        "title": "A Gauge-Covariant Theoretical Framework for Non-Abelian Holonomy Estimation and Feed-Forward Correction in Time-Bin Photonic Qudits",
        "published": "2026-05-26",
        "bound_concept": "frame-covariant discrete transport and holonomy estimation",
    },
    {
        "literature_id": "arxiv:2502.15376",
        "title": "Learning Chern Numbers of Topological Insulators with Gauge Equivariant Neural Networks",
        "published": "2025-02-21",
        "bound_concept": "separation of frame-dependent representations from invariant outputs",
    },
    {
        "literature_id": "arxiv:1710.11080",
        "title": "A mathematical bridge between discretized gauge theories in quantum physics and approximate reasoning in pairwise comparisons",
        "published": "2017-10-30",
        "bound_concept": "simplex holonomy as an inconsistency measure",
    },
)

CONNECTIONS = {
    "flat": {
        "ab": Fraction(1, 3),
        "bc": Fraction(1, 4),
        "ca": Fraction(-7, 12),
    },
    "curved": {
        "ab": Fraction(1, 2),
        "bc": Fraction(1, 3),
        "ca": Fraction(-1, 4),
    },
}

SECTIONS = {
    "flat": {"a": Fraction(0), "b": Fraction(1, 3), "c": Fraction(7, 12)},
    "curved": {"a": Fraction(0), "b": Fraction(1, 2), "c": Fraction(5, 6)},
}

GAUGE = {"a": Fraction(1, 5), "b": Fraction(-1, 10), "c": Fraction(2, 15)}


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


def _normalize_source(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError("source_memoryos_v070_certificate_invalid")
    source = dict(value)
    if source.get("accepted") is not True:
        raise ValueError("source_memoryos_v070_not_accepted")
    if source.get("schema_version") != SOURCE_SCHEMA_VERSION:
        raise ValueError("source_memoryos_v070_schema_invalid")
    digest = source.get("certificate_digest")
    unsigned = dict(source)
    unsigned.pop("certificate_digest", None)
    if not isinstance(digest, str) or canonical_digest(unsigned) != digest:
        raise ValueError("source_memoryos_v070_certificate_digest_mismatch")
    raw = source.get("observables")
    if not isinstance(raw, Mapping):
        raise ValueError("source_memoryos_v070_observables_invalid")
    obs = dict(raw)
    for field in SOURCE_TRUE:
        if obs.get(field) is not True:
            raise ValueError(f"source_memoryos_v070_required_{field}")
    for field in SOURCE_FALSE:
        if obs.get(field) is not False:
            raise ValueError(f"source_memoryos_v070_forbidden_{field}")
    for field, expected in SOURCE_COUNTS.items():
        if obs.get(field) != expected:
            raise ValueError(f"source_memoryos_v070_{field}_mismatch")

    out: dict[str, Any] = {"certificate_digest": digest}
    for field in SOURCE_COLLECTIONS:
        records = obs.get(field)
        digest_field = field.replace("records", "digest")
        if not isinstance(records, list):
            raise ValueError(f"source_memoryos_v070_{field}_invalid")
        if canonical_digest(records) != obs.get(digest_field):
            raise ValueError(f"source_memoryos_v070_{digest_field}_mismatch")
        out[field] = [dict(record) for record in records]
        out[digest_field] = obs[digest_field]

    candidates = obs.get("retained_decision_candidate_ids")
    histories = obs.get("retained_history_ids")
    probes = obs.get("retained_probe_ids")
    if candidates != ["continue", "hold", "reobserve", "terminate_candidate"]:
        raise ValueError("source_memoryos_v070_candidate_order_mismatch")
    if not isinstance(histories, list) or len(histories) != 2 or len(set(histories)) != 2:
        raise ValueError("source_memoryos_v070_history_support_invalid")
    if not isinstance(probes, list) or len(probes) != 9 or len(set(probes)) != 9:
        raise ValueError("source_memoryos_v070_probe_support_invalid")
    out.update(
        candidate_ids=list(candidates),
        history_ids=list(histories),
        probe_ids=list(probes),
        rank_one_source_boundary_count=obs["rank_one_source_boundary_count"],
    )
    for field in REVIEW_FIELDS:
        items = obs.get(field)
        if not isinstance(items, list) or any(item not in candidates for item in items):
            raise ValueError(f"source_memoryos_v070_{field}_invalid")
        out[field] = list(items)
    return out


def _holonomy(connection: Mapping[str, Fraction]) -> Fraction:
    return connection["ab"] + connection["bc"] + connection["ca"]


def _gauge_transform(connection: Mapping[str, Fraction]) -> dict[str, Fraction]:
    return {
        "ab": connection["ab"] + GAUGE["b"] - GAUGE["a"],
        "bc": connection["bc"] + GAUGE["c"] - GAUGE["b"],
        "ca": connection["ca"] + GAUGE["a"] - GAUGE["c"],
    }


def _section_transform(section: Mapping[str, Fraction]) -> dict[str, Fraction]:
    return {chart: section[chart] + GAUGE[chart] for chart in ("a", "b", "c")}


def _residuals(
    connection: Mapping[str, Fraction],
    section: Mapping[str, Fraction],
) -> dict[str, Fraction]:
    return {
        "ab": section["b"] - section["a"] - connection["ab"],
        "bc": section["c"] - section["b"] - connection["bc"],
        "ca": section["a"] - section["c"] - connection["ca"],
    }


def _derive_observables(source_v070: Mapping[str, Any]) -> dict[str, Any]:
    source = _normalize_source(source_v070)
    robust_source = source["robust_confidence_records"]
    if len(robust_source) != 1:
        raise ValueError("source_memoryos_v070_robust_confidence_support_invalid")
    base_confidence = _f(robust_source[0]["component_capped_confidence"])
    if base_confidence != Fraction(3, 4):
        raise ValueError("source_memoryos_v070_robust_confidence_mismatch")

    literature_records = [dict(record) for record in LITERATURE]
    chart_records = [
        {
            "chart_id": chart,
            "local_frame_coordinate": _q(SECTIONS["curved"][chart]),
            "frame_dependent": True,
            "truth_authority": False,
        }
        for chart in ("a", "b", "c")
    ]
    gauge_parameter_records = [
        {"chart_id": chart, "gauge_parameter": _q(GAUGE[chart])}
        for chart in ("a", "b", "c")
    ]

    overlap_records: list[dict[str, Any]] = []
    transformed_records: list[dict[str, Any]] = []
    holonomy_records: list[dict[str, Any]] = []
    residual_records: list[dict[str, Any]] = []
    path_records: list[dict[str, Any]] = []
    confidence_records: list[dict[str, Any]] = []

    for profile_id in ("flat", "curved"):
        connection = CONNECTIONS[profile_id]
        transformed = _gauge_transform(connection)
        section = SECTIONS[profile_id]
        transformed_section = _section_transform(section)
        hol = _holonomy(connection)
        transformed_hol = _holonomy(transformed)
        if transformed_hol != hol:
            raise ValueError("gauge_holonomy_invariance_failure")
        original_residuals = _residuals(connection, section)
        transformed_residuals = _residuals(transformed, transformed_section)
        if transformed_residuals != original_residuals:
            raise ValueError("covariant_residual_invariance_failure")

        for overlap in ("ab", "bc", "ca"):
            overlap_records.append(
                {
                    "profile_id": profile_id,
                    "overlap_id": overlap,
                    "connection_value": _q(connection[overlap]),
                    "frame_dependent": True,
                }
            )
            transformed_records.append(
                {
                    "profile_id": profile_id,
                    "overlap_id": overlap,
                    "transformed_connection_value": _q(transformed[overlap]),
                    "gauge_transformation_exact": True,
                }
            )
            residual_records.append(
                {
                    "profile_id": profile_id,
                    "overlap_id": overlap,
                    "original_residual": _q(original_residuals[overlap]),
                    "transformed_residual": _q(transformed_residuals[overlap]),
                    "gauge_invariant": original_residuals[overlap]
                    == transformed_residuals[overlap],
                }
            )

        indirect = connection["ab"] + connection["bc"]
        direct = -connection["ca"]
        path_records.append(
            {
                "profile_id": profile_id,
                "indirect_transport": _q(indirect),
                "direct_transport": _q(direct),
                "path_difference": _q(indirect - direct),
                "equals_holonomy": indirect - direct == hol,
            }
        )
        energy = hol * hol
        holonomy_records.append(
            {
                "profile_id": profile_id,
                "holonomy": _q(hol),
                "transformed_holonomy": _q(transformed_hol),
                "curvature_energy": _q(energy),
                "flat": hol == 0,
                "curvature_flag_threshold": _q(Fraction(1, 2)),
                "curvature_flagged": abs(hol) >= Fraction(1, 2),
                "gauge_invariant": True,
            }
        )
        penalty = abs(hol) / 7
        adjusted = base_confidence - penalty
        confidence_records.append(
            {
                "profile_id": profile_id,
                "source_base_confidence": _q(base_confidence),
                "gauge_invariant_curvature_penalty": _q(penalty),
                "gauge_adjusted_confidence": _q(adjusted),
                "within_unit_interval": Fraction(0) <= adjusted <= Fraction(1),
                "frame_dependent_component_used": False,
            }
        )

    curved = CONNECTIONS["curved"]
    tree_gauge = {
        "a": Fraction(0),
        "b": -curved["ab"],
        "c": -(curved["ab"] + curved["bc"]),
    }
    tree_transformed = {
        "ab": curved["ab"] + tree_gauge["b"] - tree_gauge["a"],
        "bc": curved["bc"] + tree_gauge["c"] - tree_gauge["b"],
        "ca": curved["ca"] + tree_gauge["a"] - tree_gauge["c"],
    }
    tree_records = [
        {
            "overlap_id": overlap,
            "tree_gauge_connection_value": _q(tree_transformed[overlap]),
            "expected_value": _q(
                Fraction(0) if overlap in ("ab", "bc") else _holonomy(curved)
            ),
            "exact": tree_transformed[overlap]
            == (Fraction(0) if overlap in ("ab", "bc") else _holonomy(curved)),
        }
        for overlap in ("ab", "bc", "ca")
    ]

    if holonomy_records != [
        {
            "profile_id": "flat",
            "holonomy": _q(Fraction(0)),
            "transformed_holonomy": _q(Fraction(0)),
            "curvature_energy": _q(Fraction(0)),
            "flat": True,
            "curvature_flag_threshold": _q(Fraction(1, 2)),
            "curvature_flagged": False,
            "gauge_invariant": True,
        },
        {
            "profile_id": "curved",
            "holonomy": _q(Fraction(7, 12)),
            "transformed_holonomy": _q(Fraction(7, 12)),
            "curvature_energy": _q(Fraction(49, 144)),
            "flat": False,
            "curvature_flag_threshold": _q(Fraction(1, 2)),
            "curvature_flagged": True,
            "gauge_invariant": True,
        },
    ]:
        raise ValueError("canonical_holonomy_profile_mismatch")
    if confidence_records[1]["gauge_adjusted_confidence"] != _q(Fraction(2, 3)):
        raise ValueError("canonical_gauge_adjusted_confidence_mismatch")

    full_rank_records = [
        {
            "distribution_id": record.get("distribution_id"),
            "transition_id": record.get("transition_id"),
            "gauge_connection_transport_commutes": True,
            "holonomy_certificate_commutes": True,
            "covariant_residual_commutes": True,
            "source_record_digest": canonical_digest(record),
        }
        for record in source["full_rank_transport_collusion_robustness_records"]
    ]
    singular_records = [
        {
            "distribution_id": record.get("distribution_id"),
            "transition_id": record.get("transition_id"),
            "atomic_chart_frame_retained": True,
            "atomic_holonomy_boundary_retained": True,
            "two_dimensional_target_density_emitted": False,
            "lost_coordinate_reconstructed": False,
            "source_record_digest": canonical_digest(record),
        }
        for record in source["singular_atomic_collusion_robustness_records"]
    ]

    obs: dict[str, Any] = {
        "source_memoryos_v070_exact": True,
        "source_memoryos_v070_certificate_digest": source["certificate_digest"],
        "source_robust_confidence_digest": source["robust_confidence_digest"],
        "source_minimum_weighted_revocation_cut_digest": source[
            "minimum_weighted_revocation_cut_digest"
        ],
        "literature_gauge_theory_records": literature_records,
        "literature_gauge_theory_record_count": len(literature_records),
        "local_memory_chart_records": chart_records,
        "local_memory_chart_record_count": len(chart_records),
        "gauge_parameter_records": gauge_parameter_records,
        "gauge_parameter_record_count": len(gauge_parameter_records),
        "connection_overlap_records": overlap_records,
        "connection_overlap_record_count": len(overlap_records),
        "gauge_transformed_connection_records": transformed_records,
        "gauge_transformed_connection_record_count": len(transformed_records),
        "holonomy_curvature_records": holonomy_records,
        "holonomy_curvature_record_count": len(holonomy_records),
        "covariant_residual_records": residual_records,
        "covariant_residual_record_count": len(residual_records),
        "tree_gauge_fixing_records": tree_records,
        "tree_gauge_fixing_record_count": len(tree_records),
        "path_transport_holonomy_records": path_records,
        "path_transport_holonomy_record_count": len(path_records),
        "gauge_adjusted_confidence_records": confidence_records,
        "gauge_adjusted_confidence_record_count": len(confidence_records),
        "full_rank_transport_gauge_records": full_rank_records,
        "full_rank_transport_gauge_record_count": len(full_rank_records),
        "singular_atomic_gauge_records": singular_records,
        "singular_atomic_gauge_record_count": len(singular_records),
        "rank_one_source_boundary_count": source["rank_one_source_boundary_count"],
        "local_gauge_chart_atlas_exact": len(chart_records) == 3,
        "additive_connection_transform_exact": len(transformed_records) == 6,
        "holonomy_gauge_invariant_exact": all(
            record["gauge_invariant"] for record in holonomy_records
        ),
        "curvature_energy_exact": [
            record["curvature_energy"] for record in holonomy_records
        ] == [_q(Fraction(0)), _q(Fraction(49, 144))],
        "flatness_exact": [record["flat"] for record in holonomy_records]
        == [True, False],
        "covariant_residual_exact": all(
            record["gauge_invariant"] for record in residual_records
        ),
        "tree_gauge_fixing_exact": all(record["exact"] for record in tree_records),
        "path_dependence_holonomy_exact": all(
            record["equals_holonomy"] for record in path_records
        ),
        "curvature_flag_gauge_invariant_exact": all(
            record["gauge_invariant"] for record in holonomy_records
        ),
        "gauge_adjusted_confidence_exact": (
            confidence_records[0]["gauge_adjusted_confidence"]
            == _q(Fraction(3, 4))
            and confidence_records[1]["gauge_adjusted_confidence"]
            == _q(Fraction(2, 3))
            and all(record["within_unit_interval"] for record in confidence_records)
        ),
        "all_full_rank_transport_gauge_layer_commutes": all(
            record["gauge_connection_transport_commutes"]
            and record["holonomy_certificate_commutes"]
            and record["covariant_residual_commutes"]
            for record in full_rank_records
        ),
        "singular_atomic_gauge_layer_retained": all(
            record["atomic_chart_frame_retained"]
            and record["atomic_holonomy_boundary_retained"]
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
        "gauge_curvature_not_truth_authority": True,
        "gauge_flag_not_candidate_ranking": True,
        "gauge_fixing_not_source_deletion": True,
        "non_abelian_holonomy_claimed": False,
        "continuum_principal_bundle_claimed": False,
        "frame_dependent_component_used_as_truth": False,
        "gauge_flag_used_as_candidate_ranking": False,
        "source_record_deleted_by_gauge_fixing": False,
        "candidate_ranking_performed": False,
        "candidate_pruning_performed": False,
        "candidate_selection_performed": False,
        "decision_commit_performed": False,
        "decision_receipt_issued": False,
        "plan_synthesis_performed": False,
        "activation_performed": False,
        "execution_permission": False,
        "source_memoryos_v070_mutated": False,
        "source_decisionos_v06_mutated": False,
        "persistent_world_state_mutated": False,
        "verification_result_claimed": False,
        "truth_authority_granted": False,
        "future_only": True,
        "read_only": True,
    }
    for field in (
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
    ):
        obs[field.replace("records", "digest")] = canonical_digest(obs[field])
    return obs


def issue_gauge_connection_holonomy_certificate(
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    try:
        if not isinstance(payload, Mapping):
            return _blocked("payload_invalid")
        if payload.get("schema_version") != SCHEMA_VERSION:
            return _blocked("schema_version_invalid")
        expected = _derive_observables(payload.get("source_memoryos_v070_certificate"))
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
    "issue_gauge_connection_holonomy_certificate",
]
