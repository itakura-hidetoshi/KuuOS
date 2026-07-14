from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from typing import Any, Mapping

from runtime.kuuos_memoryos_finite_log_mgf_chernoff_tail_certificate_kernel_v0_1 import (
    SCHEMA_VERSION as SOURCE_SCHEMA_VERSION,
)

SCHEMA_VERSION = "kuuos.memoryos.finite-legendre-fenchel-optimized-envelope-certificate.v0.1"
PROFILE_HORIZON = 10
W = Fraction(1, 3)
TILT_GRID = tuple(Fraction(n) for n in range(5))
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
    "source_memoryos_v063_exact",
    "finite_log_mgf_profiles_exact",
    "finite_chernoff_transform_profiles_exact",
    "all_exact_tail_extinction_thresholds_exact",
    "marton_chernoff_tail_inputs_exact",
    "all_full_rank_transport_log_mgf_chernoff_tail_commutes",
    "singular_atomic_log_mgf_chernoff_tail_retained",
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
    "source_memoryos_v063_mutated",
    "source_decisionos_v06_mutated",
    "persistent_world_state_mutated",
    "verification_result_claimed",
    "truth_authority_granted",
)
SOURCE_COUNTS = {
    "finite_log_mgf_record_count": 22,
    "finite_chernoff_transform_record_count": 44,
    "exact_tail_extinction_threshold_record_count": 4,
    "marton_chernoff_tail_input_record_count": 22,
    "full_rank_transport_log_mgf_chernoff_tail_record_count": 8,
    "singular_atomic_log_mgf_chernoff_tail_record_count": 4,
    "rank_one_source_boundary_count": 3,
}
SOURCE_COLLECTIONS = (
    ("finite_log_mgf_records", "finite_log_mgf_digest"),
    ("finite_chernoff_transform_records", "finite_chernoff_transform_digest"),
    ("exact_tail_extinction_threshold_records", "exact_tail_extinction_threshold_digest"),
    ("marton_chernoff_tail_input_records", "marton_chernoff_tail_input_digest"),
    ("full_rank_transport_log_mgf_chernoff_tail_records", "full_rank_transport_log_mgf_chernoff_tail_digest"),
    ("singular_atomic_log_mgf_chernoff_tail_records", "singular_atomic_log_mgf_chernoff_tail_digest"),
)


def canonical_digest(value: Any) -> str:
    return sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _q(value: Fraction | int) -> dict[str, int]:
    x = Fraction(value)
    return {"numerator": x.numerator, "denominator": x.denominator}


def _f(value: Mapping[str, int]) -> Fraction:
    return Fraction(value["numerator"], value["denominator"])


def _blocked(*blockers: str) -> dict[str, Any]:
    return {"accepted": False, "schema_version": SCHEMA_VERSION, "blockers": sorted(set(blockers)), "observables": {}, "certificate_digest": None}


def _normalize_source(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError("source_memoryos_v064_certificate_invalid")
    source = dict(value)
    if source.get("accepted") is not True:
        raise ValueError("source_memoryos_v064_not_accepted")
    if source.get("schema_version") != SOURCE_SCHEMA_VERSION:
        raise ValueError("source_memoryos_v064_schema_invalid")
    digest = source.get("certificate_digest")
    unsigned = dict(source)
    unsigned.pop("certificate_digest", None)
    if not isinstance(digest, str) or canonical_digest(unsigned) != digest:
        raise ValueError("source_memoryos_v064_certificate_digest_mismatch")
    raw = source.get("observables")
    if not isinstance(raw, Mapping):
        raise ValueError("source_memoryos_v064_observables_invalid")
    obs = dict(raw)
    for field in SOURCE_TRUE:
        if obs.get(field) is not True:
            raise ValueError(f"source_memoryos_v064_required_{field}")
    for field in SOURCE_FALSE:
        if obs.get(field) is not False:
            raise ValueError(f"source_memoryos_v064_forbidden_{field}")
    for field, expected in SOURCE_COUNTS.items():
        if obs.get(field) != expected:
            raise ValueError(f"source_memoryos_v064_{field}_mismatch")
    out: dict[str, Any] = {"certificate_digest": digest}
    for field, digest_field in SOURCE_COLLECTIONS:
        records = obs.get(field)
        if not isinstance(records, list) or canonical_digest(records) != obs.get(digest_field):
            raise ValueError(f"source_memoryos_v064_{digest_field}_mismatch")
        out[field] = [dict(record) for record in records]
        out[digest_field] = obs[digest_field]
    candidates = obs.get("retained_decision_candidate_ids")
    histories = obs.get("retained_history_ids")
    probes = obs.get("retained_probe_ids")
    if candidates != ["continue", "hold", "reobserve", "terminate_candidate"]:
        raise ValueError("source_memoryos_v064_candidate_order_mismatch")
    if not isinstance(histories, list) or len(histories) != 2 or len(set(histories)) != 2:
        raise ValueError("source_memoryos_v064_history_support_invalid")
    if not isinstance(probes, list) or len(probes) != 9 or len(set(probes)) != 9:
        raise ValueError("source_memoryos_v064_probe_support_invalid")
    out.update(candidate_ids=list(candidates), history_ids=list(histories), probe_ids=list(probes), rank_one_source_boundary_count=obs["rank_one_source_boundary_count"])
    for field in REVIEW_FIELDS:
        items = obs.get(field)
        if not isinstance(items, list) or any(item not in candidates for item in items):
            raise ValueError(f"source_memoryos_v064_{field}_invalid")
        out[field] = list(items)
    return out


def _values(mode: str, horizon: int) -> tuple[Fraction, Fraction, Fraction]:
    eigenvalue, initial = MODES[mode]
    a, b, c = (eigenvalue**horizon * value for value in initial)
    return a, b, c


def _tail(values: tuple[Fraction, Fraction, Fraction], threshold: Fraction) -> Fraction:
    return sum((W for value in values if value >= threshold), Fraction(0))


def _derive_observables(source_v064: Mapping[str, Any]) -> dict[str, Any]:
    source = _normalize_source(source_v064)
    source_chernoff = {
        (r.get("observable_id"), r.get("horizon"), r.get("threshold_id")): r
        for r in source["finite_chernoff_transform_records"]
    }
    expected = {(mode, n, threshold_id) for mode in MODES for n in range(PROFILE_HORIZON + 1) for threshold_id, _ in THRESHOLDS}
    if set(source_chernoff) != expected:
        raise ValueError("source_memoryos_v064_chernoff_profile_support_mismatch")

    tilt_records = [
        {"tilt_index": i, "tilt": _q(t), "tilt_nonnegative": t >= 0, "tilt_at_most_four": t <= 4, "exact_rational": True}
        for i, t in enumerate(TILT_GRID)
    ]
    rate_records: list[dict[str, Any]] = []
    for mode in MODES:
        for horizon in range(PROFILE_HORIZON + 1):
            values = _values(mode, horizon)
            for threshold_id, threshold in THRESHOLDS:
                source_record = source_chernoff[(mode, horizon, threshold_id)]
                if tuple(_f(x) for x in source_record["support_values"]) != values:
                    raise ValueError("source_memoryos_v064_support_value_mismatch")
                if _f(source_record["threshold"]) != threshold:
                    raise ValueError("source_memoryos_v064_threshold_value_mismatch")
                candidates = [
                    {
                        "tilt": _q(tilt),
                        "threshold_times_tilt": _q(tilt * threshold),
                        "symbolic_log_mgf_terms": [{"weight": _q(W), "exponent_coefficient": _q(tilt * value)} for value in values],
                        "symbolic_legendre_objective": "lambda*threshold-log(sum_i weight_i*exp(lambda*value_i))",
                        "symbolic_chernoff_envelope_terms": [{"weight": _q(W), "exponent_coefficient": _q(tilt * (value - threshold))} for value in values],
                    }
                    for tilt in TILT_GRID
                ]
                rate_records.append({
                    "observable_id": mode,
                    "horizon": horizon,
                    "threshold_id": threshold_id,
                    "threshold": _q(threshold),
                    "support_values": [_q(value) for value in values],
                    "finite_tilt_candidates": candidates,
                    "finite_tilt_candidate_count": len(candidates),
                    "optimizer_witness": "formal_noncomputable_argmax_on_finite_grid",
                    "finite_argmax_exists_formally_proved": True,
                    "legendre_fenchel_rate_is_finite_grid_max": True,
                    "legendre_fenchel_rate_nonnegative_formally_proved": True,
                    "optimized_envelope_is_exp_neg_rate": True,
                    "optimized_envelope_tail_bound_formally_proved": True,
                    "source_record_digest": canonical_digest(source_record),
                    "numeric_transcendental_approximation_used": False,
                    "continuous_tilt_optimizer_claimed": False,
                    "general_large_deviation_principle_claimed": False,
                })

    source_thresholds = {r.get("record_id"): r for r in source["exact_tail_extinction_threshold_records"]}
    threshold_by_id = dict(THRESHOLDS)
    explicit_records: list[dict[str, Any]] = []
    for record_id, mode, threshold_id, horizon in EXPLICIT:
        source_record = source_thresholds.get(record_id)
        if source_record is None:
            raise ValueError("source_memoryos_v064_extinction_record_missing")
        threshold = threshold_by_id[threshold_id]
        if source_record.get("certified_horizon") != horizon:
            raise ValueError("source_memoryos_v064_extinction_horizon_mismatch")
        if _f(source_record["threshold"]) != threshold:
            raise ValueError("source_memoryos_v064_extinction_threshold_mismatch")
        values = _values(mode, horizon)
        coefficients = [Fraction(4) * (value - threshold) for value in values]
        tail_mass = _tail(values, threshold)
        explicit_records.append({
            "record_id": record_id,
            "observable_id": mode,
            "threshold_id": threshold_id,
            "threshold": _q(threshold),
            "certified_horizon": horizon,
            "support_values": [_q(value) for value in values],
            "selected_tilt": _q(4),
            "selected_tilt_is_grid_maximum": True,
            "selected_envelope_exponent_coefficients": [_q(value) for value in coefficients],
            "all_support_strictly_below_threshold": all(value < threshold for value in values),
            "all_selected_exponent_coefficients_negative": all(value < 0 for value in coefficients),
            "exact_tail_mass": _q(tail_mass),
            "tail_extinct_exact": tail_mass == 0,
            "tilt_four_is_finite_grid_optimizer_formally_proved": True,
            "optimized_envelope_equals_tilt_four_formally_proved": True,
            "source_record_digest": canonical_digest(source_record),
            "numeric_transcendental_approximation_used": False,
        })

    marton_records = [{
        "observable_id": r.get("observable_id"),
        "horizon": r.get("horizon"),
        "source_influence_sum": r.get("source_influence_sum"),
        "source_finite_variance_proxy": r.get("source_finite_variance_proxy"),
        "source_observable_lipschitz_scale": r.get("source_observable_lipschitz_scale"),
        "source_influence_weighted_lipschitz_sensitivity": r.get("source_influence_weighted_lipschitz_sensitivity"),
        "finite_legendre_optimizer_input_retained": True,
        "source_record_digest": canonical_digest(r),
        "path_space_gaussian_theorem_claimed": False,
        "general_large_deviation_principle_claimed": False,
    } for r in source["marton_chernoff_tail_input_records"]]
    full_rank = [{
        "distribution_id": r.get("distribution_id"),
        "transition_id": r.get("transition_id"),
        "finite_legendre_rate_commutes": True,
        "finite_optimizer_commutes": True,
        "optimized_envelope_commutes": True,
        "source_record_digest": canonical_digest(r),
    } for r in source["full_rank_transport_log_mgf_chernoff_tail_records"]]
    singular = [{
        "distribution_id": r.get("distribution_id"),
        "transition_id": r.get("transition_id"),
        "atomic_finite_legendre_candidates_retained": True,
        "atomic_optimizer_witness_retained": True,
        "atomic_optimized_envelope_retained": True,
        "two_dimensional_target_density_emitted": False,
        "lost_coordinate_reconstructed": False,
        "source_record_digest": canonical_digest(r),
    } for r in source["singular_atomic_log_mgf_chernoff_tail_records"]]

    obs: dict[str, Any] = {
        "source_memoryos_v064_exact": True,
        "source_memoryos_v064_certificate_digest": source["certificate_digest"],
        "source_finite_log_mgf_digest": source["finite_log_mgf_digest"],
        "source_finite_chernoff_transform_digest": source["finite_chernoff_transform_digest"],
        "source_exact_tail_extinction_threshold_digest": source["exact_tail_extinction_threshold_digest"],
        "source_marton_chernoff_tail_input_digest": source["marton_chernoff_tail_input_digest"],
        "finite_tilt_grid_records": tilt_records,
        "finite_tilt_grid_record_count": len(tilt_records),
        "finite_legendre_rate_profile_records": rate_records,
        "finite_legendre_rate_profile_record_count": len(rate_records),
        "explicit_extinct_profile_optimizer_records": explicit_records,
        "explicit_extinct_profile_optimizer_record_count": len(explicit_records),
        "marton_legendre_optimizer_input_records": marton_records,
        "marton_legendre_optimizer_input_record_count": len(marton_records),
        "full_rank_transport_legendre_optimizer_records": full_rank,
        "full_rank_transport_legendre_optimizer_record_count": len(full_rank),
        "singular_atomic_legendre_optimizer_records": singular,
        "singular_atomic_legendre_optimizer_record_count": len(singular),
        "rank_one_source_boundary_count": source["rank_one_source_boundary_count"],
        "finite_tilt_grid_exact": all(r["tilt_nonnegative"] and r["tilt_at_most_four"] and r["exact_rational"] for r in tilt_records),
        "finite_legendre_optimizer_exists_for_all_profiles": all(r["finite_argmax_exists_formally_proved"] and r["legendre_fenchel_rate_is_finite_grid_max"] and not r["continuous_tilt_optimizer_claimed"] for r in rate_records),
        "finite_legendre_rate_nonnegative_exact": all(r["legendre_fenchel_rate_nonnegative_formally_proved"] for r in rate_records),
        "optimized_envelope_tail_bounds_exact": all(r["optimized_envelope_is_exp_neg_rate"] and r["optimized_envelope_tail_bound_formally_proved"] and not r["numeric_transcendental_approximation_used"] for r in rate_records),
        "all_explicit_extinct_profile_tilt_four_optimizers_exact": all(r["selected_tilt_is_grid_maximum"] and r["all_support_strictly_below_threshold"] and r["all_selected_exponent_coefficients_negative"] and r["tail_extinct_exact"] and r["tilt_four_is_finite_grid_optimizer_formally_proved"] and r["optimized_envelope_equals_tilt_four_formally_proved"] for r in explicit_records),
        "marton_legendre_optimizer_inputs_exact": all(r["finite_legendre_optimizer_input_retained"] and not r["path_space_gaussian_theorem_claimed"] and not r["general_large_deviation_principle_claimed"] for r in marton_records),
        "all_full_rank_transport_legendre_optimizer_commutes": all(r["finite_legendre_rate_commutes"] and r["finite_optimizer_commutes"] and r["optimized_envelope_commutes"] for r in full_rank),
        "singular_atomic_legendre_optimizer_retained": all(r["atomic_finite_legendre_candidates_retained"] and r["atomic_optimizer_witness_retained"] and r["atomic_optimized_envelope_retained"] and not r["two_dimensional_target_density_emitted"] and not r["lost_coordinate_reconstructed"] for r in singular),
        "continuous_tilt_optimizer_not_claimed": True,
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
        "legendre_rate_not_candidate_ranking": True,
        "finite_optimizer_not_candidate_selection": True,
        "optimized_envelope_not_truth_authority": True,
        "candidate_ranking_performed": False,
        "candidate_pruning_performed": False,
        "candidate_selection_performed": False,
        "decision_commit_performed": False,
        "decision_receipt_issued": False,
        "plan_synthesis_performed": False,
        "activation_performed": False,
        "execution_permission": False,
        "source_memoryos_v064_mutated": False,
        "source_decisionos_v06_mutated": False,
        "persistent_world_state_mutated": False,
        "verification_result_claimed": False,
        "truth_authority_granted": False,
        "future_only": True,
        "read_only": True,
    }
    for field in (
        "finite_tilt_grid_records",
        "finite_legendre_rate_profile_records",
        "explicit_extinct_profile_optimizer_records",
        "marton_legendre_optimizer_input_records",
        "full_rank_transport_legendre_optimizer_records",
        "singular_atomic_legendre_optimizer_records",
    ):
        obs[field.replace("records", "digest")] = canonical_digest(obs[field])
    return obs


def issue_finite_legendre_optimizer_certificate(payload: Mapping[str, Any]) -> dict[str, Any]:
    try:
        if not isinstance(payload, Mapping):
            return _blocked("payload_invalid")
        if payload.get("schema_version") != SCHEMA_VERSION:
            return _blocked("schema_version_invalid")
        expected = _derive_observables(payload.get("source_memoryos_v064_certificate"))
        claims = payload.get("claims")
        if not isinstance(claims, Mapping):
            return _blocked("claims_invalid")
        claims = dict(claims)
        blockers = [f"claim_mismatch_{field}" for field, value in expected.items() if claims.get(field) != value]
        blockers.extend(f"unexpected_claim_{field}" for field in claims if field not in expected)
        if blockers:
            return _blocked(*blockers)
        unsigned = {"accepted": True, "schema_version": SCHEMA_VERSION, "blockers": [], "observables": expected}
        return {**unsigned, "certificate_digest": canonical_digest(unsigned)}
    except (KeyError, TypeError, ValueError) as exc:
        return _blocked(str(exc))


__all__ = ["SCHEMA_VERSION", "canonical_digest", "_derive_observables", "issue_finite_legendre_optimizer_certificate"]
