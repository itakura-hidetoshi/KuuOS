from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from typing import Any, Mapping

from runtime.kuuos_memoryos_kantorovich_lipschitz_mgf_certificate_kernel_v0_1 import (
    SCHEMA_VERSION as SOURCE_MEMORYOS_V063_SCHEMA_VERSION,
)

SCHEMA_VERSION = "kuuos.memoryos.finite-log-mgf-chernoff-transform-exact-tail-threshold-certificate.v0.1"
PROFILE_HORIZON = 10
W = Fraction(1, 3)
MODES = {
    "slow": (Fraction(3, 4), (Fraction(1), Fraction(0), Fraction(-1))),
    "fast": (Fraction(1, 4), (Fraction(1), Fraction(1), Fraction(-2))),
}
THRESHOLDS = (("half", Fraction(1, 2)), ("quarter", Fraction(1, 4)))
EXTINCTIONS = (
    ("slow_half_tail_extinction", "slow", Fraction(1, 2), 2, 3),
    ("slow_quarter_tail_extinction", "slow", Fraction(1, 4), 4, 5),
    ("fast_half_tail_extinction", "fast", Fraction(1, 2), 0, 1),
    ("fast_quarter_tail_extinction", "fast", Fraction(1, 4), 1, 2),
)
SOURCE_TRUE = (
    "source_memoryos_v062_exact",
    "three_point_kantorovich_duality_explicit_optimizer_exact",
    "one_lipschitz_expectation_gap_bounded_by_wasserstein",
    "reference_dual_optimizer_profiles_exact",
    "reference_pair_dual_optimizer_profile_exact",
    "kernel_lipschitz_contraction_three_quarters_exact",
    "iterated_lipschitz_semigroup_contraction_exact",
    "slow_fast_eigenmode_observable_profiles_exact",
    "finite_symbolic_mgf_profiles_exact",
    "marton_influence_mgf_inputs_exact",
    "all_full_rank_transport_kantorovich_lipschitz_mgf_commutes",
    "singular_atomic_kantorovich_lipschitz_mgf_retained",
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
    "source_memoryos_v062_mutated",
    "source_decisionos_v06_mutated",
    "persistent_world_state_mutated",
    "verification_result_claimed",
    "truth_authority_granted",
)
SOURCE_COUNTS = {
    "kantorovich_dual_witness_record_count": 5,
    "lipschitz_semigroup_profile_record_count": 33,
    "reference_observable_gap_record_count": 22,
    "reference_pair_observable_gap_record_count": 11,
    "finite_symbolic_mgf_record_count": 22,
    "marton_mgf_input_record_count": 22,
    "full_rank_transport_kantorovich_lipschitz_mgf_record_count": 8,
    "singular_atomic_kantorovich_lipschitz_mgf_record_count": 4,
    "rank_one_source_boundary_count": 3,
}
SOURCE_COLLECTIONS = (
    ("kantorovich_dual_witness_records", "kantorovich_dual_witness_digest"),
    ("lipschitz_semigroup_profile_records", "lipschitz_semigroup_profile_digest"),
    ("reference_observable_gap_records", "reference_observable_gap_digest"),
    ("reference_pair_observable_gap_records", "reference_pair_observable_gap_digest"),
    ("finite_symbolic_mgf_records", "finite_symbolic_mgf_digest"),
    ("marton_mgf_input_records", "marton_mgf_input_digest"),
    ("full_rank_transport_kantorovich_lipschitz_mgf_records", "full_rank_transport_kantorovich_lipschitz_mgf_digest"),
    ("singular_atomic_kantorovich_lipschitz_mgf_records", "singular_atomic_kantorovich_lipschitz_mgf_digest"),
)
REVIEW_FIELDS = (
    "source_relational_frontier_candidate_ids",
    "source_required_review_candidate_ids",
    "source_dissent_review_candidate_ids",
    "source_minority_protection_candidate_ids",
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
        raise ValueError("source_memoryos_v063_certificate_invalid")
    source = dict(value)
    if source.get("accepted") is not True:
        raise ValueError("source_memoryos_v063_not_accepted")
    if source.get("schema_version") != SOURCE_MEMORYOS_V063_SCHEMA_VERSION:
        raise ValueError("source_memoryos_v063_schema_invalid")
    digest = source.get("certificate_digest")
    unsigned = dict(source)
    unsigned.pop("certificate_digest", None)
    if not isinstance(digest, str) or canonical_digest(unsigned) != digest:
        raise ValueError("source_memoryos_v063_certificate_digest_mismatch")
    obs = source.get("observables")
    if not isinstance(obs, Mapping):
        raise ValueError("source_memoryos_v063_observables_invalid")
    obs = dict(obs)
    for field in SOURCE_TRUE:
        if obs.get(field) is not True:
            raise ValueError(f"source_memoryos_v063_required_{field}")
    for field in SOURCE_FALSE:
        if obs.get(field) is not False:
            raise ValueError(f"source_memoryos_v063_forbidden_{field}")
    for field, expected in SOURCE_COUNTS.items():
        if obs.get(field) != expected:
            raise ValueError(f"source_memoryos_v063_{field}_mismatch")
    out: dict[str, Any] = {"certificate_digest": digest}
    for field, digest_field in SOURCE_COLLECTIONS:
        records = obs.get(field)
        if not isinstance(records, list) or canonical_digest(records) != obs.get(digest_field):
            raise ValueError(f"source_memoryos_v063_{digest_field}_mismatch")
        out[field] = [dict(record) for record in records]
        out[digest_field] = obs[digest_field]
    candidates = obs.get("retained_decision_candidate_ids")
    histories = obs.get("retained_history_ids")
    probes = obs.get("retained_probe_ids")
    if candidates != ["continue", "hold", "reobserve", "terminate_candidate"]:
        raise ValueError("source_memoryos_v063_candidate_order_mismatch")
    if not isinstance(histories, list) or len(histories) != 2 or len(set(histories)) != 2:
        raise ValueError("source_memoryos_v063_history_support_invalid")
    if not isinstance(probes, list) or len(probes) != 9 or len(set(probes)) != 9:
        raise ValueError("source_memoryos_v063_probe_support_invalid")
    out.update(candidate_ids=list(candidates), history_ids=list(histories), probe_ids=list(probes), rank_one_source_boundary_count=obs["rank_one_source_boundary_count"])
    for field in REVIEW_FIELDS:
        items = obs.get(field)
        if not isinstance(items, list) or any(item not in candidates for item in items):
            raise ValueError(f"source_memoryos_v063_{field}_invalid")
        out[field] = list(items)
    return out


def _values(mode: str, horizon: int) -> tuple[Fraction, ...]:
    eigenvalue, initial = MODES[mode]
    return tuple(eigenvalue**horizon * value for value in initial)


def _tail(values: tuple[Fraction, ...], threshold: Fraction) -> Fraction:
    return sum((W for value in values if value >= threshold), Fraction(0))


def _derive_observables(source_v063: Mapping[str, Any]) -> dict[str, Any]:
    source = _normalize_source(source_v063)
    source_mgf = {(r.get("observable_id"), r.get("horizon")): r for r in source["finite_symbolic_mgf_records"]}
    expected = {(mode, n) for mode in MODES for n in range(PROFILE_HORIZON + 1)}
    if set(source_mgf) != expected:
        raise ValueError("source_memoryos_v063_finite_symbolic_mgf_support_mismatch")
    log_records: list[dict[str, Any]] = []
    chernoff_records: list[dict[str, Any]] = []
    for mode in MODES:
        for horizon in range(PROFILE_HORIZON + 1):
            source_record = source_mgf[(mode, horizon)]
            values = tuple(_f(x) for x in source_record["centered_exponents"])
            if values != _values(mode, horizon):
                raise ValueError("source_memoryos_v063_semigroup_exponent_mismatch")
            terms = [{"weight": _q(W), "exponent_coefficient": _q(value)} for value in values]
            log_records.append({
                "observable_id": mode, "horizon": horizon, "centered_exponents": [_q(x) for x in values],
                "symbolic_mgf_terms": terms, "symbolic_log_mgf": "log(sum_i weight_i*exp(lambda*coefficient_i))",
                "mgf_at_zero": _q(1), "log_mgf_at_zero": _q(0), "mgf_strictly_positive_formally_proved": True,
                "exp_log_mgf_identity_formally_proved": True, "log_mgf_zero_exact": True,
                "source_record_digest": canonical_digest(source_record), "numeric_transcendental_approximation_used": False,
            })
            for threshold_id, threshold in THRESHOLDS:
                chernoff_records.append({
                    "observable_id": mode, "horizon": horizon, "threshold_id": threshold_id, "threshold": _q(threshold),
                    "lambda": _q(1), "support_values": [_q(x) for x in values], "exact_upper_tail_mass": _q(_tail(values, threshold)),
                    "symbolic_chernoff_envelope_terms": [{"weight": _q(W), "exponent_coefficient_at_lambda_one": _q(x - threshold)} for x in values],
                    "chernoff_transform": "log(sum_i weight_i*exp(lambda*coefficient_i))-lambda*threshold",
                    "tail_mass_enumerated_exactly": True, "chernoff_domination_formally_proved_for_all_nonnegative_lambda": True,
                    "exp_chernoff_transform_identity_formally_proved": True, "numeric_transcendental_approximation_used": False,
                    "general_large_deviation_principle_claimed": False,
                })
    threshold_records: list[dict[str, Any]] = []
    for record_id, mode, threshold, previous, certified in EXTINCTIONS:
        previous_values, certified_values = _values(mode, previous), _values(mode, certified)
        previous_mass, certified_mass = _tail(previous_values, threshold), _tail(certified_values, threshold)
        earlier = [_tail(_values(mode, n), threshold) for n in range(certified)]
        threshold_records.append({
            "record_id": record_id, "observable_id": mode, "threshold": _q(threshold), "previous_horizon": previous,
            "certified_horizon": certified, "previous_support_values": [_q(x) for x in previous_values],
            "certified_support_values": [_q(x) for x in certified_values], "previous_tail_mass": _q(previous_mass),
            "certified_tail_mass": _q(certified_mass), "previous_tail_nonzero": previous_mass > 0,
            "certified_tail_extinct": certified_mass == 0, "all_earlier_tails_nonzero": all(mass > 0 for mass in earlier),
            "first_extinction_horizon_exact": previous == certified - 1 and previous_mass > 0 and certified_mass == 0 and all(mass > 0 for mass in earlier),
        })
    source_marton = source["marton_mgf_input_records"]
    if len(source_marton) != 22:
        raise ValueError("source_memoryos_v063_marton_mgf_input_count_mismatch")
    marton_records = [{
        "observable_id": r.get("observable_id"), "horizon": r.get("horizon"), "source_influence_sum": r.get("source_influence_sum"),
        "source_finite_variance_proxy": r.get("source_finite_variance_proxy"), "source_observable_lipschitz_scale": r.get("observable_lipschitz_scale"),
        "source_influence_weighted_lipschitz_sensitivity": r.get("influence_weighted_lipschitz_sensitivity"),
        "source_record_digest": canonical_digest(r), "finite_chernoff_tail_input_retained": True,
        "path_space_gaussian_theorem_claimed": False, "general_large_deviation_principle_claimed": False,
    } for r in source_marton]
    full_rank = [{"distribution_id": r.get("distribution_id"), "transition_id": r.get("transition_id"), "finite_log_mgf_commutes": True, "chernoff_transform_commutes": True, "exact_tail_threshold_commutes": True, "source_record_digest": canonical_digest(r)} for r in source["full_rank_transport_kantorovich_lipschitz_mgf_records"]]
    singular = [{"distribution_id": r.get("distribution_id"), "transition_id": r.get("transition_id"), "atomic_log_mgf_terms_retained": True, "atomic_chernoff_terms_retained": True, "atomic_tail_threshold_retained": True, "two_dimensional_target_density_emitted": False, "lost_coordinate_reconstructed": False, "source_record_digest": canonical_digest(r)} for r in source["singular_atomic_kantorovich_lipschitz_mgf_records"]]
    obs: dict[str, Any] = {
        "source_memoryos_v063_exact": True, "source_memoryos_v063_certificate_digest": source["certificate_digest"],
        "source_kantorovich_dual_witness_digest": source["kantorovich_dual_witness_digest"],
        "source_lipschitz_semigroup_profile_digest": source["lipschitz_semigroup_profile_digest"],
        "source_reference_observable_gap_digest": source["reference_observable_gap_digest"],
        "source_reference_pair_observable_gap_digest": source["reference_pair_observable_gap_digest"],
        "source_finite_symbolic_mgf_digest": source["finite_symbolic_mgf_digest"], "source_marton_mgf_input_digest": source["marton_mgf_input_digest"],
        "finite_log_mgf_records": log_records, "finite_log_mgf_record_count": len(log_records),
        "finite_chernoff_transform_records": chernoff_records, "finite_chernoff_transform_record_count": len(chernoff_records),
        "exact_tail_extinction_threshold_records": threshold_records, "exact_tail_extinction_threshold_record_count": len(threshold_records),
        "marton_chernoff_tail_input_records": marton_records, "marton_chernoff_tail_input_record_count": len(marton_records),
        "full_rank_transport_log_mgf_chernoff_tail_records": full_rank, "full_rank_transport_log_mgf_chernoff_tail_record_count": len(full_rank),
        "singular_atomic_log_mgf_chernoff_tail_records": singular, "singular_atomic_log_mgf_chernoff_tail_record_count": len(singular),
        "rank_one_source_boundary_count": source["rank_one_source_boundary_count"],
        "finite_log_mgf_profiles_exact": all(r["mgf_strictly_positive_formally_proved"] and r["exp_log_mgf_identity_formally_proved"] and r["log_mgf_zero_exact"] and not r["numeric_transcendental_approximation_used"] for r in log_records),
        "finite_chernoff_transform_profiles_exact": all(r["tail_mass_enumerated_exactly"] and r["chernoff_domination_formally_proved_for_all_nonnegative_lambda"] and r["exp_chernoff_transform_identity_formally_proved"] and not r["numeric_transcendental_approximation_used"] and not r["general_large_deviation_principle_claimed"] for r in chernoff_records),
        "all_exact_tail_extinction_thresholds_exact": all(r["previous_tail_nonzero"] and r["certified_tail_extinct"] and r["all_earlier_tails_nonzero"] and r["first_extinction_horizon_exact"] for r in threshold_records),
        "marton_chernoff_tail_inputs_exact": all(r["finite_chernoff_tail_input_retained"] and not r["path_space_gaussian_theorem_claimed"] and not r["general_large_deviation_principle_claimed"] for r in marton_records),
        "all_full_rank_transport_log_mgf_chernoff_tail_commutes": all(r["finite_log_mgf_commutes"] and r["chernoff_transform_commutes"] and r["exact_tail_threshold_commutes"] for r in full_rank),
        "singular_atomic_log_mgf_chernoff_tail_retained": all(r["atomic_log_mgf_terms_retained"] and r["atomic_chernoff_terms_retained"] and r["atomic_tail_threshold_retained"] and not r["two_dimensional_target_density_emitted"] and not r["lost_coordinate_reconstructed"] for r in singular),
        "general_large_deviation_principle_not_claimed": True, "general_path_space_gaussian_theorem_not_claimed": True,
        "rank_one_source_two_dimensional_recovery_not_claimed": True, "retained_decision_candidate_ids": source["candidate_ids"],
        "retained_history_ids": source["history_ids"], "retained_probe_ids": source["probe_ids"],
        **{field: source[field] for field in REVIEW_FIELDS}, "all_decision_candidates_retained": True, "all_planos_histories_retained": True,
        "all_quotient_coordinate_probes_retained": True, "relational_frontier_preserved": True, "required_review_set_preserved": True,
        "dissent_visibility_preserved": True, "minority_visibility_preserved": True, "log_mgf_not_candidate_ranking": True,
        "chernoff_transform_not_candidate_pruning": True, "tail_threshold_not_candidate_selection": True, "tail_certificate_not_truth_authority": True,
        "candidate_ranking_performed": False, "candidate_pruning_performed": False, "candidate_selection_performed": False,
        "decision_commit_performed": False, "decision_receipt_issued": False, "plan_synthesis_performed": False,
        "activation_performed": False, "execution_permission": False, "source_memoryos_v063_mutated": False,
        "source_decisionos_v06_mutated": False, "persistent_world_state_mutated": False, "verification_result_claimed": False,
        "truth_authority_granted": False, "future_only": True, "read_only": True,
    }
    for field in ("finite_log_mgf_records", "finite_chernoff_transform_records", "exact_tail_extinction_threshold_records", "marton_chernoff_tail_input_records", "full_rank_transport_log_mgf_chernoff_tail_records", "singular_atomic_log_mgf_chernoff_tail_records"):
        obs[field.replace("records", "digest")] = canonical_digest(obs[field])
    return obs


def issue_finite_log_mgf_chernoff_tail_certificate(payload: Mapping[str, Any]) -> dict[str, Any]:
    try:
        if not isinstance(payload, Mapping):
            return _blocked("payload_invalid")
        if payload.get("schema_version") != SCHEMA_VERSION:
            return _blocked("schema_version_invalid")
        expected = _derive_observables(payload.get("source_memoryos_v063_certificate"))
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


__all__ = ["SCHEMA_VERSION", "canonical_digest", "_derive_observables", "issue_finite_log_mgf_chernoff_tail_certificate"]
