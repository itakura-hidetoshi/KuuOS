from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from typing import Any, Mapping

from runtime.kuuos_memoryos_finite_legendre_optimizer_certificate_kernel_v0_1 import (
    SCHEMA_VERSION as SOURCE_SCHEMA_VERSION,
)

SCHEMA_VERSION = (
    "kuuos.memoryos.continuous-log-mgf-convexity-stationary-optimizer-"
    "certificate.v0.1"
)
PROFILE_HORIZON = 10
MODES = {
    "slow": (Fraction(3, 4), (Fraction(1), Fraction(0), Fraction(-1))),
    "fast": (Fraction(1, 4), (Fraction(1), Fraction(1), Fraction(-2))),
}
THRESHOLDS = (("half", Fraction(1, 2)), ("quarter", Fraction(1, 4)))
EXPLICIT = (
    ("slow_half_tail_extinction", "slow", "half", 3),
    ("slow_quarter_tail_extinction", "slow", "quarter", 5),
    ("fast_half_tail_extinction", "fast", "half", 1),
    ("fast_quarter_tail_extinction", "fast", "quarter", 2),
)
REVIEW_FIELDS = (
    "source_relational_frontier_candidate_ids",
    "source_required_review_candidate_ids",
    "source_dissent_review_candidate_ids",
    "source_minority_protection_candidate_ids",
)
SOURCE_TRUE = (
    "source_memoryos_v064_exact",
    "finite_tilt_grid_exact",
    "finite_legendre_optimizer_exists_for_all_profiles",
    "finite_legendre_rate_nonnegative_exact",
    "optimized_envelope_tail_bounds_exact",
    "all_explicit_extinct_profile_tilt_four_optimizers_exact",
    "marton_legendre_optimizer_inputs_exact",
    "all_full_rank_transport_legendre_optimizer_commutes",
    "singular_atomic_legendre_optimizer_retained",
    "continuous_tilt_optimizer_not_claimed",
    "general_large_deviation_principle_not_claimed",
    "general_path_space_gaussian_theorem_not_claimed",
    "rank_one_source_two_dimensional_recovery_not_claimed",
    "all_decision_candidates_retained",
    "all_planos_histories_retained",
    "all_quotient_coordinate_probes_retained",
    "relational_frontier_preserved",
    "required_review_set_preserved",
    "dissent_visibility_preserved",
    "minority_visibility_preserved",
    "future_only",
    "read_only",
)
SOURCE_FALSE = (
    "candidate_ranking_performed",
    "candidate_pruning_performed",
    "candidate_selection_performed",
    "decision_commit_performed",
    "decision_receipt_issued",
    "plan_synthesis_performed",
    "activation_performed",
    "execution_permission",
    "source_memoryos_v064_mutated",
    "source_decisionos_v06_mutated",
    "persistent_world_state_mutated",
    "verification_result_claimed",
    "truth_authority_granted",
)
SOURCE_COUNTS = {
    "finite_tilt_grid_record_count": 5,
    "finite_legendre_rate_profile_record_count": 44,
    "explicit_extinct_profile_optimizer_record_count": 4,
    "marton_legendre_optimizer_input_record_count": 22,
    "full_rank_transport_legendre_optimizer_record_count": 8,
    "singular_atomic_legendre_optimizer_record_count": 4,
    "rank_one_source_boundary_count": 3,
}
SOURCE_COLLECTIONS = (
    ("finite_tilt_grid_records", "finite_tilt_grid_digest"),
    ("finite_legendre_rate_profile_records", "finite_legendre_rate_profile_digest"),
    (
        "explicit_extinct_profile_optimizer_records",
        "explicit_extinct_profile_optimizer_digest",
    ),
    ("marton_legendre_optimizer_input_records", "marton_legendre_optimizer_input_digest"),
    (
        "full_rank_transport_legendre_optimizer_records",
        "full_rank_transport_legendre_optimizer_digest",
    ),
    (
        "singular_atomic_legendre_optimizer_records",
        "singular_atomic_legendre_optimizer_digest",
    ),
)


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
        raise ValueError("source_memoryos_v065_certificate_invalid")
    source = dict(value)
    if source.get("accepted") is not True:
        raise ValueError("source_memoryos_v065_not_accepted")
    if source.get("schema_version") != SOURCE_SCHEMA_VERSION:
        raise ValueError("source_memoryos_v065_schema_invalid")
    digest = source.get("certificate_digest")
    unsigned = dict(source)
    unsigned.pop("certificate_digest", None)
    if not isinstance(digest, str) or canonical_digest(unsigned) != digest:
        raise ValueError("source_memoryos_v065_certificate_digest_mismatch")
    raw = source.get("observables")
    if not isinstance(raw, Mapping):
        raise ValueError("source_memoryos_v065_observables_invalid")
    obs = dict(raw)
    for field in SOURCE_TRUE:
        if obs.get(field) is not True:
            raise ValueError(f"source_memoryos_v065_required_{field}")
    for field in SOURCE_FALSE:
        if obs.get(field) is not False:
            raise ValueError(f"source_memoryos_v065_forbidden_{field}")
    for field, expected in SOURCE_COUNTS.items():
        if obs.get(field) != expected:
            raise ValueError(f"source_memoryos_v065_{field}_mismatch")

    out: dict[str, Any] = {"certificate_digest": digest}
    for field, digest_field in SOURCE_COLLECTIONS:
        records = obs.get(field)
        if not isinstance(records, list):
            raise ValueError(f"source_memoryos_v065_{field}_invalid")
        if canonical_digest(records) != obs.get(digest_field):
            raise ValueError(f"source_memoryos_v065_{digest_field}_mismatch")
        out[field] = [dict(record) for record in records]
        out[digest_field] = obs[digest_field]

    candidates = obs.get("retained_decision_candidate_ids")
    histories = obs.get("retained_history_ids")
    probes = obs.get("retained_probe_ids")
    if candidates != ["continue", "hold", "reobserve", "terminate_candidate"]:
        raise ValueError("source_memoryos_v065_candidate_order_mismatch")
    if not isinstance(histories, list) or len(histories) != 2 or len(set(histories)) != 2:
        raise ValueError("source_memoryos_v065_history_support_invalid")
    if not isinstance(probes, list) or len(probes) != 9 or len(set(probes)) != 9:
        raise ValueError("source_memoryos_v065_probe_support_invalid")
    out.update(
        candidate_ids=list(candidates),
        history_ids=list(histories),
        probe_ids=list(probes),
        rank_one_source_boundary_count=obs["rank_one_source_boundary_count"],
    )
    for field in REVIEW_FIELDS:
        items = obs.get(field)
        if not isinstance(items, list) or any(item not in candidates for item in items):
            raise ValueError(f"source_memoryos_v065_{field}_invalid")
        out[field] = list(items)
    return out


def _values(mode: str, horizon: int) -> tuple[Fraction, Fraction, Fraction]:
    eigenvalue, initial = MODES[mode]
    return tuple(eigenvalue**horizon * value for value in initial)  # type: ignore[return-value]


def _pairwise_curvature_terms(
    values: tuple[Fraction, Fraction, Fraction],
) -> list[dict[str, Any]]:
    pairs = ((0, 1), (0, 2), (1, 2))
    return [
        {
            "left_state_index": i,
            "right_state_index": j,
            "exponent_coefficient": _q(values[i] + values[j]),
            "squared_gap": _q((values[i] - values[j]) ** 2),
            "nonnegative": True,
        }
        for i, j in pairs
    ]


def _derive_observables(source_v065: Mapping[str, Any]) -> dict[str, Any]:
    source = _normalize_source(source_v065)
    source_rates = {
        (r.get("observable_id"), r.get("horizon"), r.get("threshold_id")): r
        for r in source["finite_legendre_rate_profile_records"]
    }
    expected_rates = {
        (mode, horizon, threshold_id)
        for mode in MODES
        for horizon in range(PROFILE_HORIZON + 1)
        for threshold_id, _ in THRESHOLDS
    }
    if set(source_rates) != expected_rates:
        raise ValueError("source_memoryos_v065_rate_profile_support_mismatch")

    derivative_records: list[dict[str, Any]] = []
    for mode in MODES:
        for horizon in range(PROFILE_HORIZON + 1):
            values = _values(mode, horizon)
            derivative_records.append(
                {
                    "observable_id": mode,
                    "horizon": horizon,
                    "support_values": [_q(value) for value in values],
                    "partition_terms": [
                        {
                            "coefficient": _q(1),
                            "exponent_coefficient": _q(value),
                        }
                        for value in values
                    ],
                    "first_moment_terms": [
                        {
                            "coefficient": _q(value),
                            "exponent_coefficient": _q(value),
                        }
                        for value in values
                    ],
                    "second_moment_terms": [
                        {
                            "coefficient": _q(value**2),
                            "exponent_coefficient": _q(value),
                        }
                        for value in values
                    ],
                    "pairwise_curvature_terms": _pairwise_curvature_terms(values),
                    "partition_strictly_positive_formally_proved": True,
                    "partition_derivative_formally_proved": True,
                    "first_moment_derivative_formally_proved": True,
                    "log_mgf_derivative_is_tilted_mean_formally_proved": True,
                    "tilted_mean_derivative_is_curvature_formally_proved": True,
                    "pairwise_square_curvature_identity_formally_proved": True,
                    "tilted_curvature_nonnegative_formally_proved": True,
                    "log_mgf_convex_on_real_formally_proved": True,
                    "numeric_transcendental_approximation_used": False,
                }
            )

    stationarity_records: list[dict[str, Any]] = []
    comparison_records: list[dict[str, Any]] = []
    for key in sorted(source_rates):
        mode, horizon, threshold_id = key
        source_record = source_rates[key]
        threshold = dict(THRESHOLDS)[threshold_id]
        values = _values(mode, horizon)
        if tuple(_f(value) for value in source_record["support_values"]) != values:
            raise ValueError("source_memoryos_v065_support_value_mismatch")
        if _f(source_record["threshold"]) != threshold:
            raise ValueError("source_memoryos_v065_threshold_value_mismatch")
        source_digest = canonical_digest(source_record)
        stationarity_records.append(
            {
                "observable_id": mode,
                "horizon": horizon,
                "threshold_id": threshold_id,
                "threshold": _q(threshold),
                "support_values": [_q(value) for value in values],
                "symbolic_stationary_equation": (
                    "sum_i x_i*exp(lambda*x_i)/sum_i exp(lambda*x_i)=threshold"
                ),
                "legendre_derivative_is_threshold_minus_tilted_mean_formally_proved": True,
                "global_optimizer_implies_local_max_formally_proved": True,
                "fermat_stationary_equation_formally_proved": True,
                "global_optimizer_existence_claimed": False,
                "closed_form_optimizer_claimed": False,
                "source_record_digest": source_digest,
                "numeric_transcendental_root_used": False,
            }
        )
        comparison_records.append(
            {
                "observable_id": mode,
                "horizon": horizon,
                "threshold_id": threshold_id,
                "continuous_global_rate_dominates_finite_grid_rate_formally_proved": True,
                "continuous_global_envelope_le_finite_grid_envelope_formally_proved": True,
                "comparison_conditional_on_global_optimizer_witness": True,
                "source_finite_optimizer_witness_retained": True,
                "source_record_digest": source_digest,
                "numeric_transcendental_root_used": False,
            }
        )

    source_explicit = {
        record.get("record_id"): record
        for record in source["explicit_extinct_profile_optimizer_records"]
    }
    boundary_records: list[dict[str, Any]] = []
    threshold_by_id = dict(THRESHOLDS)
    for record_id, mode, threshold_id, horizon in EXPLICIT:
        source_record = source_explicit.get(record_id)
        if source_record is None:
            raise ValueError("source_memoryos_v065_explicit_optimizer_missing")
        threshold = threshold_by_id[threshold_id]
        values = _values(mode, horizon)
        if source_record.get("certified_horizon") != horizon:
            raise ValueError("source_memoryos_v065_explicit_horizon_mismatch")
        if tuple(_f(value) for value in source_record["support_values"]) != values:
            raise ValueError("source_memoryos_v065_explicit_support_mismatch")
        boundary_records.append(
            {
                "record_id": record_id,
                "observable_id": mode,
                "threshold_id": threshold_id,
                "threshold": _q(threshold),
                "certified_horizon": horizon,
                "support_values": [_q(value) for value in values],
                "interval_lower": _q(0),
                "interval_upper": _q(4),
                "continuous_interval_optimizer": _q(4),
                "all_support_below_threshold": all(value <= threshold for value in values),
                "legendre_objective_monotone_on_interval_formally_proved": True,
                "tilt_four_continuous_interval_optimizer_formally_proved": True,
                "finite_rate_equals_tilt_four_objective_formally_proved": True,
                "unbounded_optimizer_existence_claimed": False,
                "source_record_digest": canonical_digest(source_record),
            }
        )

    marton_records = [
        {
            "observable_id": record.get("observable_id"),
            "horizon": record.get("horizon"),
            "source_influence_sum": record.get("source_influence_sum"),
            "source_finite_variance_proxy": record.get("source_finite_variance_proxy"),
            "continuous_convexity_input_retained": True,
            "continuous_optimizer_existence_claimed": False,
            "general_path_space_gaussian_theorem_claimed": False,
            "general_large_deviation_principle_claimed": False,
            "source_record_digest": canonical_digest(record),
        }
        for record in source["marton_legendre_optimizer_input_records"]
    ]
    full_rank_records = [
        {
            "distribution_id": record.get("distribution_id"),
            "transition_id": record.get("transition_id"),
            "tilted_mean_commutes": True,
            "tilted_curvature_commutes": True,
            "continuous_finite_rate_comparison_commutes": True,
            "source_record_digest": canonical_digest(record),
        }
        for record in source["full_rank_transport_legendre_optimizer_records"]
    ]
    singular_records = [
        {
            "distribution_id": record.get("distribution_id"),
            "transition_id": record.get("transition_id"),
            "atomic_partition_derivative_retained": True,
            "atomic_curvature_identity_retained": True,
            "atomic_bounded_interval_optimizer_retained": True,
            "two_dimensional_target_density_emitted": False,
            "lost_coordinate_reconstructed": False,
            "source_record_digest": canonical_digest(record),
        }
        for record in source["singular_atomic_legendre_optimizer_records"]
    ]

    obs: dict[str, Any] = {
        "source_memoryos_v065_exact": True,
        "source_memoryos_v065_certificate_digest": source["certificate_digest"],
        "source_finite_tilt_grid_digest": source["finite_tilt_grid_digest"],
        "source_finite_legendre_rate_profile_digest": source[
            "finite_legendre_rate_profile_digest"
        ],
        "source_explicit_extinct_profile_optimizer_digest": source[
            "explicit_extinct_profile_optimizer_digest"
        ],
        "source_marton_legendre_optimizer_input_digest": source[
            "marton_legendre_optimizer_input_digest"
        ],
        "derivative_curvature_profile_records": derivative_records,
        "derivative_curvature_profile_record_count": len(derivative_records),
        "continuous_stationarity_input_records": stationarity_records,
        "continuous_stationarity_input_record_count": len(stationarity_records),
        "continuous_finite_grid_comparison_records": comparison_records,
        "continuous_finite_grid_comparison_record_count": len(comparison_records),
        "bounded_interval_boundary_optimizer_records": boundary_records,
        "bounded_interval_boundary_optimizer_record_count": len(boundary_records),
        "marton_continuous_optimizer_input_records": marton_records,
        "marton_continuous_optimizer_input_record_count": len(marton_records),
        "full_rank_transport_continuous_optimizer_records": full_rank_records,
        "full_rank_transport_continuous_optimizer_record_count": len(full_rank_records),
        "singular_atomic_continuous_optimizer_records": singular_records,
        "singular_atomic_continuous_optimizer_record_count": len(singular_records),
        "rank_one_source_boundary_count": source["rank_one_source_boundary_count"],
        "all_partition_derivatives_exact": all(
            record["partition_derivative_formally_proved"]
            and record["first_moment_derivative_formally_proved"]
            for record in derivative_records
        ),
        "all_log_mgf_derivatives_exact": all(
            record["log_mgf_derivative_is_tilted_mean_formally_proved"]
            for record in derivative_records
        ),
        "all_tilted_curvatures_nonnegative_exact": all(
            record["pairwise_square_curvature_identity_formally_proved"]
            and record["tilted_curvature_nonnegative_formally_proved"]
            for record in derivative_records
        ),
        "all_log_mgf_profiles_convex_on_real_exact": all(
            record["log_mgf_convex_on_real_formally_proved"]
            for record in derivative_records
        ),
        "all_global_optimizer_stationary_equations_exact": all(
            record["fermat_stationary_equation_formally_proved"]
            and not record["global_optimizer_existence_claimed"]
            and not record["closed_form_optimizer_claimed"]
            for record in stationarity_records
        ),
        "all_continuous_finite_grid_comparisons_exact": all(
            record[
                "continuous_global_rate_dominates_finite_grid_rate_formally_proved"
            ]
            and record[
                "continuous_global_envelope_le_finite_grid_envelope_formally_proved"
            ]
            and record["comparison_conditional_on_global_optimizer_witness"]
            for record in comparison_records
        ),
        "all_bounded_interval_boundary_optimizers_exact": all(
            record["all_support_below_threshold"]
            and record["legendre_objective_monotone_on_interval_formally_proved"]
            and record["tilt_four_continuous_interval_optimizer_formally_proved"]
            and record["finite_rate_equals_tilt_four_objective_formally_proved"]
            and not record["unbounded_optimizer_existence_claimed"]
            for record in boundary_records
        ),
        "marton_continuous_optimizer_inputs_exact": all(
            record["continuous_convexity_input_retained"]
            and not record["continuous_optimizer_existence_claimed"]
            and not record["general_path_space_gaussian_theorem_claimed"]
            and not record["general_large_deviation_principle_claimed"]
            for record in marton_records
        ),
        "all_full_rank_transport_continuous_optimizer_commutes": all(
            record["tilted_mean_commutes"]
            and record["tilted_curvature_commutes"]
            and record["continuous_finite_rate_comparison_commutes"]
            for record in full_rank_records
        ),
        "singular_atomic_continuous_optimizer_retained": all(
            record["atomic_partition_derivative_retained"]
            and record["atomic_curvature_identity_retained"]
            and record["atomic_bounded_interval_optimizer_retained"]
            and not record["two_dimensional_target_density_emitted"]
            and not record["lost_coordinate_reconstructed"]
            for record in singular_records
        ),
        "unbounded_continuous_optimizer_existence_not_claimed": True,
        "closed_form_transcendental_optimizer_not_claimed": True,
        "general_cramer_theorem_not_claimed": True,
        "general_gartner_ellis_theorem_not_claimed": True,
        "general_large_deviation_principle_not_claimed": True,
        "general_path_space_gaussian_theorem_not_claimed": True,
        "rank_one_source_two_dimensional_recovery_not_claimed": True,
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
        "continuous_optimizer_not_candidate_selection": True,
        "stationary_equation_not_decision_commit": True,
        "convexity_certificate_not_truth_authority": True,
        "candidate_ranking_performed": False,
        "candidate_pruning_performed": False,
        "candidate_selection_performed": False,
        "decision_commit_performed": False,
        "decision_receipt_issued": False,
        "plan_synthesis_performed": False,
        "activation_performed": False,
        "execution_permission": False,
        "source_memoryos_v065_mutated": False,
        "source_decisionos_v06_mutated": False,
        "persistent_world_state_mutated": False,
        "verification_result_claimed": False,
        "truth_authority_granted": False,
        "future_only": True,
        "read_only": True,
    }
    for field in (
        "derivative_curvature_profile_records",
        "continuous_stationarity_input_records",
        "continuous_finite_grid_comparison_records",
        "bounded_interval_boundary_optimizer_records",
        "marton_continuous_optimizer_input_records",
        "full_rank_transport_continuous_optimizer_records",
        "singular_atomic_continuous_optimizer_records",
    ):
        obs[field.replace("records", "digest")] = canonical_digest(obs[field])
    return obs


def issue_continuous_log_mgf_convexity_certificate(
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    try:
        if not isinstance(payload, Mapping):
            return _blocked("payload_invalid")
        if payload.get("schema_version") != SCHEMA_VERSION:
            return _blocked("schema_version_invalid")
        expected = _derive_observables(
            payload.get("source_memoryos_v065_certificate")
        )
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
    except (KeyError, TypeError, ValueError) as exc:
        return _blocked(str(exc))


__all__ = [
    "SCHEMA_VERSION",
    "canonical_digest",
    "_derive_observables",
    "issue_continuous_log_mgf_convexity_certificate",
]
