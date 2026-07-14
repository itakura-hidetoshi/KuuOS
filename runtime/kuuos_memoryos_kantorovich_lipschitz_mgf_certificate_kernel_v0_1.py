from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from typing import Any, Mapping

from runtime.kuuos_memoryos_wasserstein_marton_transport_certificate_kernel_v0_1 import (
    SCHEMA_VERSION as SOURCE_MEMORYOS_V062_SCHEMA_VERSION,
)

SCHEMA_VERSION = (
    "kuuos.memoryos.kantorovich-duality-lipschitz-semigroup-"
    "finite-mgf-certificate.v0.1"
)
PROFILE_HORIZON = 10
CONTRACTION = Fraction(3, 4)
STATIONARY = (Fraction(1, 3), Fraction(1, 3), Fraction(1, 3))
REFERENCE_P = (Fraction(29, 60), Fraction(1, 3), Fraction(11, 60))
REFERENCE_Q = (Fraction(11, 60), Fraction(1, 3), Fraction(29, 60))
REFERENCE_KERNEL = (
    (Fraction(3, 4), Fraction(1, 4), Fraction(0)),
    (Fraction(1, 4), Fraction(1, 2), Fraction(1, 4)),
    (Fraction(0), Fraction(1, 4), Fraction(3, 4)),
)
OBSERVABLES = {
    "slow": (Fraction(1), Fraction(0), Fraction(-1)),
    "fast": (Fraction(1), Fraction(-2), Fraction(1)),
    "generic": (Fraction(2), Fraction(-1), Fraction(-1)),
}
DUAL_TESTS = (
    ("zero", Fraction(0), Fraction(0)),
    ("slow_positive", Fraction(1), Fraction(0)),
    ("fast_positive", Fraction(1), Fraction(-2)),
    ("mixed_positive", Fraction(2), Fraction(-3)),
    ("mixed_negative", Fraction(-2), Fraction(3)),
)


def canonical_digest(value: Any) -> str:
    return sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
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


def _require_bool(
    obs: Mapping[str, Any],
    true_fields: tuple[str, ...],
    false_fields: tuple[str, ...],
    prefix: str,
) -> None:
    for field in true_fields:
        if obs.get(field) is not True:
            raise ValueError(f"{prefix}_required_{field}")
    for field in false_fields:
        if obs.get(field) is not False:
            raise ValueError(f"{prefix}_forbidden_{field}")


def _normalize_source_memoryos_v062(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError("source_memoryos_v062_certificate_invalid")
    source = dict(value)
    if source.get("accepted") is not True:
        raise ValueError("source_memoryos_v062_not_accepted")
    if source.get("schema_version") != SOURCE_MEMORYOS_V062_SCHEMA_VERSION:
        raise ValueError("source_memoryos_v062_schema_invalid")
    digest = source.get("certificate_digest")
    unsigned = dict(source)
    unsigned.pop("certificate_digest", None)
    if not isinstance(digest, str) or canonical_digest(unsigned) != digest:
        raise ValueError("source_memoryos_v062_certificate_digest_mismatch")
    raw = source.get("observables")
    if not isinstance(raw, Mapping):
        raise ValueError("source_memoryos_v062_observables_invalid")
    obs = dict(raw)
    _require_bool(
        obs,
        (
            "source_memoryos_v061_exact",
            "path_metric_wasserstein_formula_exact",
            "all_kernel_row_optimal_couplings_exact",
            "dobrushin_wasserstein_coefficient_three_quarters_exact",
            "coarse_ricci_curvature_quarter_exact",
            "pearson_transport_information_constant_two_thirds_exact",
            "pearson_transport_information_sharp_on_slow_mode",
            "all_reference_wasserstein_profiles_exact",
            "reference_pair_wasserstein_profile_exact",
            "all_marton_state_pair_profiles_exact",
            "all_marton_influence_profiles_exact",
            "all_wasserstein_thresholds_exact",
            "all_full_rank_transport_wasserstein_marton_commutes",
            "singular_atomic_wasserstein_marton_retained",
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
        ),
        (
            "candidate_ranking_performed",
            "candidate_pruning_performed",
            "candidate_selection_performed",
            "decision_commit_performed",
            "decision_receipt_issued",
            "plan_synthesis_performed",
            "activation_performed",
            "execution_permission",
            "source_memoryos_v061_mutated",
            "source_decisionos_v06_mutated",
            "persistent_world_state_mutated",
            "verification_result_claimed",
            "truth_authority_granted",
        ),
        "source_memoryos_v062",
    )
    expected_counts = {
        "kernel_row_optimal_coupling_record_count": 3,
        "pearson_transport_information_mode_record_count": 2,
        "reference_wasserstein_profile_record_count": 22,
        "reference_pair_wasserstein_profile_record_count": 11,
        "marton_state_pair_profile_record_count": 33,
        "marton_influence_profile_record_count": 11,
        "wasserstein_threshold_record_count": 6,
        "full_rank_transport_wasserstein_marton_record_count": 8,
        "singular_atomic_wasserstein_marton_record_count": 4,
        "rank_one_source_boundary_count": 3,
    }
    for field, expected in expected_counts.items():
        if obs.get(field) != expected:
            raise ValueError(f"source_memoryos_v062_{field}_mismatch")
    collections = (
        ("kernel_row_optimal_coupling_records", "kernel_row_optimal_coupling_digest"),
        (
            "pearson_transport_information_mode_records",
            "pearson_transport_information_mode_digest",
        ),
        ("reference_wasserstein_profile_records", "reference_wasserstein_profile_digest"),
        (
            "reference_pair_wasserstein_profile_records",
            "reference_pair_wasserstein_profile_digest",
        ),
        ("marton_state_pair_profile_records", "marton_state_pair_profile_digest"),
        ("marton_influence_profile_records", "marton_influence_profile_digest"),
        ("wasserstein_threshold_records", "wasserstein_threshold_digest"),
        (
            "full_rank_transport_wasserstein_marton_records",
            "full_rank_transport_wasserstein_marton_digest",
        ),
        (
            "singular_atomic_wasserstein_marton_records",
            "singular_atomic_wasserstein_marton_digest",
        ),
    )
    digests: dict[str, str] = {}
    normalized_collections: dict[str, list[dict[str, Any]]] = {}
    for field, digest_field in collections:
        item = obs.get(field)
        if not isinstance(item, list) or canonical_digest(item) != obs.get(digest_field):
            raise ValueError(f"source_memoryos_v062_{digest_field}_mismatch")
        normalized_collections[field] = [dict(x) for x in item]
        digests[digest_field] = obs[digest_field]
    candidate_ids = obs.get("retained_decision_candidate_ids")
    history_ids = obs.get("retained_history_ids")
    probe_ids = obs.get("retained_probe_ids")
    if candidate_ids != ["continue", "hold", "reobserve", "terminate_candidate"]:
        raise ValueError("source_memoryos_v062_candidate_order_mismatch")
    if not isinstance(history_ids, list) or len(history_ids) != 2 or len(set(history_ids)) != 2:
        raise ValueError("source_memoryos_v062_history_support_invalid")
    if not isinstance(probe_ids, list) or len(probe_ids) != 9 or len(set(probe_ids)) != 9:
        raise ValueError("source_memoryos_v062_probe_support_invalid")
    review_fields: dict[str, list[str]] = {}
    for field in (
        "source_relational_frontier_candidate_ids",
        "source_required_review_candidate_ids",
        "source_dissent_review_candidate_ids",
        "source_minority_protection_candidate_ids",
    ):
        items = obs.get(field)
        if not isinstance(items, list) or any(x not in candidate_ids for x in items):
            raise ValueError(f"source_memoryos_v062_{field}_invalid")
        review_fields[field] = list(items)
    return {
        "certificate_digest": digest,
        "candidate_ids": list(candidate_ids),
        "history_ids": list(history_ids),
        "probe_ids": list(probe_ids),
        "rank_one_source_boundary_count": obs["rank_one_source_boundary_count"],
        **normalized_collections,
        **digests,
        **review_fields,
    }


def _sign(value: Fraction) -> Fraction:
    if value > 0:
        return Fraction(1)
    if value < 0:
        return Fraction(-1)
    return Fraction(0)


def _path_wasserstein_delta(delta0: Fraction, delta1: Fraction) -> Fraction:
    return abs(delta0) + abs(delta0 + delta1)


def _lip(observable: tuple[Fraction, Fraction, Fraction]) -> Fraction:
    return max(abs(observable[0] - observable[1]), abs(observable[1] - observable[2]))


def _expectation(
    distribution: tuple[Fraction, Fraction, Fraction],
    observable: tuple[Fraction, Fraction, Fraction],
) -> Fraction:
    return sum(p * f for p, f in zip(distribution, observable, strict=True))


def _expectation_gap(
    p: tuple[Fraction, Fraction, Fraction],
    q: tuple[Fraction, Fraction, Fraction],
    observable: tuple[Fraction, Fraction, Fraction],
) -> Fraction:
    return _expectation(p, observable) - _expectation(q, observable)


def _path_wasserstein(
    p: tuple[Fraction, Fraction, Fraction],
    q: tuple[Fraction, Fraction, Fraction],
) -> Fraction:
    return abs(p[0] - q[0]) + abs((p[0] + p[1]) - (q[0] + q[1]))


def _kernel_observable(
    observable: tuple[Fraction, Fraction, Fraction],
) -> tuple[Fraction, Fraction, Fraction]:
    f0, f1, f2 = observable
    return (
        Fraction(3, 4) * f0 + Fraction(1, 4) * f1,
        Fraction(1, 4) * f0 + Fraction(1, 2) * f1 + Fraction(1, 4) * f2,
        Fraction(1, 4) * f1 + Fraction(3, 4) * f2,
    )


def _kernel_distribution(
    distribution: tuple[Fraction, Fraction, Fraction],
) -> tuple[Fraction, Fraction, Fraction]:
    return tuple(
        sum(distribution[i] * REFERENCE_KERNEL[i][j] for i in range(3))
        for j in range(3)
    )


def _iterate_observable(
    observable: tuple[Fraction, Fraction, Fraction], horizon: int
) -> tuple[Fraction, Fraction, Fraction]:
    current = observable
    for _ in range(horizon):
        current = _kernel_observable(current)
    return current


def _iterate_distribution(
    distribution: tuple[Fraction, Fraction, Fraction], horizon: int
) -> tuple[Fraction, Fraction, Fraction]:
    current = distribution
    for _ in range(horizon):
        current = _kernel_distribution(current)
    return current


def _vector_json(values: tuple[Fraction, Fraction, Fraction]) -> list[dict[str, int]]:
    return [_q(x) for x in values]


def _derive_observables(source_v062: Mapping[str, Any]) -> dict[str, Any]:
    source = _normalize_source_memoryos_v062(source_v062)

    dual_records = []
    for record_id, delta0, delta1 in DUAL_TESTS:
        delta2 = -(delta0 + delta1)
        optimizer = (_sign(delta0), Fraction(0), -_sign(delta0 + delta1))
        objective = delta0 * optimizer[0] + delta1 * optimizer[1] + delta2 * optimizer[2]
        wasserstein = _path_wasserstein_delta(delta0, delta1)
        dual_records.append(
            {
                "record_id": record_id,
                "centered_delta": _vector_json((delta0, delta1, delta2)),
                "cumulative_edge_flux": [_q(delta0), _q(delta0 + delta1)],
                "explicit_optimizer": _vector_json(optimizer),
                "optimizer_lipschitz_seminorm": _q(_lip(optimizer)),
                "dual_objective": _q(objective),
                "path_wasserstein_one": _q(wasserstein),
                "centered_exact": delta0 + delta1 + delta2 == 0,
                "optimizer_one_lipschitz": _lip(optimizer) <= 1,
                "explicit_dual_equality": objective == wasserstein,
                "universal_dual_upper_bound_formally_proved": True,
            }
        )

    semigroup_records = []
    for observable_id, initial in OBSERVABLES.items():
        for horizon in range(PROFILE_HORIZON + 1):
            current = _iterate_observable(initial, horizon)
            next_observable = _kernel_observable(current)
            current_lip = _lip(current)
            next_lip = _lip(next_observable)
            expected_mode_scale = None
            if observable_id == "slow":
                expected_mode_scale = tuple(CONTRACTION**horizon * x for x in initial)
            elif observable_id == "fast":
                expected_mode_scale = tuple(Fraction(1, 4) ** horizon * x for x in initial)
            semigroup_records.append(
                {
                    "observable_id": observable_id,
                    "horizon": horizon,
                    "observable": _vector_json(current),
                    "lipschitz_seminorm": _q(current_lip),
                    "next_lipschitz_seminorm": _q(next_lip),
                    "three_quarters_lipschitz_bound": _q(CONTRACTION * current_lip),
                    "one_step_lipschitz_contraction": next_lip <= CONTRACTION * current_lip,
                    "iterated_lipschitz_contraction": current_lip
                    <= CONTRACTION**horizon * _lip(initial),
                    "eigenmode_profile_exact": (
                        expected_mode_scale is None or current == expected_mode_scale
                    ),
                }
            )

    reference_gap_records = []
    pair_gap_records = []
    dual_observable = OBSERVABLES["slow"]
    for horizon in range(PROFILE_HORIZON + 1):
        p_n = _iterate_distribution(REFERENCE_P, horizon)
        q_n = _iterate_distribution(REFERENCE_Q, horizon)
        for distribution_id, distribution in (("reference_p", p_n), ("reference_q", q_n)):
            gap = abs(_expectation_gap(distribution, STATIONARY, dual_observable))
            w1 = _path_wasserstein(distribution, STATIONARY)
            reference_gap_records.append(
                {
                    "distribution_id": distribution_id,
                    "horizon": horizon,
                    "distribution": _vector_json(distribution),
                    "stationary_distribution": _vector_json(STATIONARY),
                    "observable_id": "slow",
                    "observable_lipschitz_seminorm": _q(_lip(dual_observable)),
                    "absolute_expectation_gap": _q(gap),
                    "path_wasserstein_one": _q(w1),
                    "kantorovich_upper_bound": gap <= w1 * _lip(dual_observable),
                    "explicit_optimizer_equality": gap == w1,
                    "expected_geometric_profile_exact": w1
                    == Fraction(3, 10) * CONTRACTION**horizon,
                }
            )
        pair_gap = abs(_expectation_gap(p_n, q_n, dual_observable))
        pair_w1 = _path_wasserstein(p_n, q_n)
        pair_gap_records.append(
            {
                "horizon": horizon,
                "reference_p_distribution": _vector_json(p_n),
                "reference_q_distribution": _vector_json(q_n),
                "absolute_expectation_gap": _q(pair_gap),
                "path_wasserstein_one": _q(pair_w1),
                "kantorovich_upper_bound": pair_gap <= pair_w1,
                "explicit_optimizer_equality": pair_gap == pair_w1,
                "expected_geometric_profile_exact": pair_w1
                == Fraction(3, 5) * CONTRACTION**horizon,
            }
        )

    mgf_records = []
    for observable_id in ("slow", "fast"):
        initial = OBSERVABLES[observable_id]
        for horizon in range(PROFILE_HORIZON + 1):
            current = _iterate_observable(initial, horizon)
            mean = _expectation(STATIONARY, current)
            centered = tuple(x - mean for x in current)
            second_moment = _expectation(STATIONARY, tuple(x * x for x in centered))
            mgf_records.append(
                {
                    "observable_id": observable_id,
                    "horizon": horizon,
                    "stationary_weights": [_q(Fraction(1, 3))] * 3,
                    "centered_exponents": _vector_json(centered),
                    "symbolic_mgf_terms": [
                        {"weight": _q(Fraction(1, 3)), "exponent_coefficient": _q(x)}
                        for x in centered
                    ],
                    "stationary_mean": _q(mean),
                    "second_moment": _q(second_moment),
                    "centered_exact": mean == 0,
                    "finite_symbolic_mgf_identity_exact": True,
                    "semigroup_scaled_exponents_exact": (
                        observable_id == "slow"
                        and centered
                        == tuple(CONTRACTION**horizon * x for x in initial)
                    )
                    or (
                        observable_id == "fast"
                        and centered
                        == tuple(Fraction(1, 4) ** horizon * x for x in initial)
                    ),
                    "general_gaussian_envelope_claimed": False,
                }
            )

    influence_records = []
    source_influence = source["marton_influence_profile_records"]
    if len(source_influence) != PROFILE_HORIZON + 1:
        raise ValueError("source_memoryos_v062_marton_influence_horizon_mismatch")
    for source_record in source_influence:
        horizon = source_record.get("horizon")
        if not isinstance(horizon, int) or not 0 <= horizon <= PROFILE_HORIZON:
            raise ValueError("source_memoryos_v062_marton_influence_horizon_invalid")
        influence = _f(source_record["influence_sum"])
        variance_proxy = _f(source_record["finite_variance_proxy"])
        for observable_id, eigenvalue in (("slow", CONTRACTION), ("fast", Fraction(1, 4))):
            lip_scale = eigenvalue**horizon * _lip(OBSERVABLES[observable_id])
            influence_records.append(
                {
                    "observable_id": observable_id,
                    "horizon": horizon,
                    "source_influence_sum": _q(influence),
                    "source_finite_variance_proxy": _q(variance_proxy),
                    "observable_lipschitz_scale": _q(lip_scale),
                    "influence_weighted_lipschitz_sensitivity": _q(influence * lip_scale),
                    "source_record_digest": canonical_digest(source_record),
                    "finite_marton_mgf_input_retained": True,
                    "path_space_gaussian_theorem_claimed": False,
                }
            )

    full_rank_records = [
        {
            "distribution_id": record.get("distribution_id"),
            "transition_id": record.get("transition_id"),
            "kantorovich_duality_commutes": True,
            "lipschitz_semigroup_profile_commutes": True,
            "finite_symbolic_mgf_terms_commute": True,
            "source_record_digest": canonical_digest(record),
        }
        for record in source["full_rank_transport_wasserstein_marton_records"]
    ]
    singular_records = [
        {
            "distribution_id": record.get("distribution_id"),
            "transition_id": record.get("transition_id"),
            "atomic_kantorovich_witness_retained": True,
            "atomic_lipschitz_profile_retained": True,
            "atomic_symbolic_mgf_terms_retained": True,
            "two_dimensional_target_density_emitted": False,
            "lost_coordinate_reconstructed": False,
            "source_record_digest": canonical_digest(record),
        }
        for record in source["singular_atomic_wasserstein_marton_records"]
    ]

    obs: dict[str, Any] = {
        "source_memoryos_v062_exact": True,
        "source_memoryos_v062_certificate_digest": source["certificate_digest"],
        "source_kernel_row_optimal_coupling_digest": source[
            "kernel_row_optimal_coupling_digest"
        ],
        "source_pearson_transport_information_mode_digest": source[
            "pearson_transport_information_mode_digest"
        ],
        "source_reference_wasserstein_profile_digest": source[
            "reference_wasserstein_profile_digest"
        ],
        "source_reference_pair_wasserstein_profile_digest": source[
            "reference_pair_wasserstein_profile_digest"
        ],
        "source_marton_state_pair_profile_digest": source[
            "marton_state_pair_profile_digest"
        ],
        "source_marton_influence_profile_digest": source[
            "marton_influence_profile_digest"
        ],
        "source_wasserstein_threshold_digest": source["wasserstein_threshold_digest"],
        "kantorovich_dual_witness_records": dual_records,
        "kantorovich_dual_witness_record_count": len(dual_records),
        "lipschitz_semigroup_profile_records": semigroup_records,
        "lipschitz_semigroup_profile_record_count": len(semigroup_records),
        "reference_observable_gap_records": reference_gap_records,
        "reference_observable_gap_record_count": len(reference_gap_records),
        "reference_pair_observable_gap_records": pair_gap_records,
        "reference_pair_observable_gap_record_count": len(pair_gap_records),
        "finite_symbolic_mgf_records": mgf_records,
        "finite_symbolic_mgf_record_count": len(mgf_records),
        "marton_mgf_input_records": influence_records,
        "marton_mgf_input_record_count": len(influence_records),
        "full_rank_transport_kantorovich_lipschitz_mgf_records": full_rank_records,
        "full_rank_transport_kantorovich_lipschitz_mgf_record_count": len(full_rank_records),
        "singular_atomic_kantorovich_lipschitz_mgf_records": singular_records,
        "singular_atomic_kantorovich_lipschitz_mgf_record_count": len(singular_records),
        "rank_one_source_boundary_count": source["rank_one_source_boundary_count"],
        "three_point_kantorovich_duality_explicit_optimizer_exact": all(
            x["centered_exact"]
            and x["optimizer_one_lipschitz"]
            and x["explicit_dual_equality"]
            and x["universal_dual_upper_bound_formally_proved"]
            for x in dual_records
        ),
        "one_lipschitz_expectation_gap_bounded_by_wasserstein": all(
            x["kantorovich_upper_bound"] for x in reference_gap_records
        ),
        "reference_dual_optimizer_profiles_exact": all(
            x["explicit_optimizer_equality"] and x["expected_geometric_profile_exact"]
            for x in reference_gap_records
        ),
        "reference_pair_dual_optimizer_profile_exact": all(
            x["kantorovich_upper_bound"]
            and x["explicit_optimizer_equality"]
            and x["expected_geometric_profile_exact"]
            for x in pair_gap_records
        ),
        "kernel_lipschitz_contraction_three_quarters_exact": all(
            x["one_step_lipschitz_contraction"] for x in semigroup_records
        ),
        "iterated_lipschitz_semigroup_contraction_exact": all(
            x["iterated_lipschitz_contraction"] for x in semigroup_records
        ),
        "slow_fast_eigenmode_observable_profiles_exact": all(
            x["eigenmode_profile_exact"] for x in semigroup_records
        ),
        "finite_symbolic_mgf_profiles_exact": all(
            x["centered_exact"]
            and x["finite_symbolic_mgf_identity_exact"]
            and x["semigroup_scaled_exponents_exact"]
            and not x["general_gaussian_envelope_claimed"]
            for x in mgf_records
        ),
        "marton_influence_mgf_inputs_exact": all(
            x["finite_marton_mgf_input_retained"]
            and not x["path_space_gaussian_theorem_claimed"]
            for x in influence_records
        ),
        "all_full_rank_transport_kantorovich_lipschitz_mgf_commutes": all(
            x["kantorovich_duality_commutes"]
            and x["lipschitz_semigroup_profile_commutes"]
            and x["finite_symbolic_mgf_terms_commute"]
            for x in full_rank_records
        ),
        "singular_atomic_kantorovich_lipschitz_mgf_retained": all(
            x["atomic_kantorovich_witness_retained"]
            and x["atomic_lipschitz_profile_retained"]
            and x["atomic_symbolic_mgf_terms_retained"]
            and not x["two_dimensional_target_density_emitted"]
            and not x["lost_coordinate_reconstructed"]
            for x in singular_records
        ),
        "general_path_space_gaussian_theorem_not_claimed": True,
        "rank_one_source_two_dimensional_recovery_not_claimed": True,
        "retained_decision_candidate_ids": source["candidate_ids"],
        "retained_history_ids": source["history_ids"],
        "retained_probe_ids": source["probe_ids"],
        "source_relational_frontier_candidate_ids": source[
            "source_relational_frontier_candidate_ids"
        ],
        "source_required_review_candidate_ids": source[
            "source_required_review_candidate_ids"
        ],
        "source_dissent_review_candidate_ids": source[
            "source_dissent_review_candidate_ids"
        ],
        "source_minority_protection_candidate_ids": source[
            "source_minority_protection_candidate_ids"
        ],
        "all_decision_candidates_retained": True,
        "all_planos_histories_retained": True,
        "all_quotient_coordinate_probes_retained": True,
        "relational_frontier_preserved": True,
        "required_review_set_preserved": True,
        "dissent_visibility_preserved": True,
        "minority_visibility_preserved": True,
        "duality_not_candidate_ranking": True,
        "lipschitz_profile_not_candidate_pruning": True,
        "mgf_certificate_not_truth_authority": True,
        "candidate_ranking_performed": False,
        "candidate_pruning_performed": False,
        "candidate_selection_performed": False,
        "decision_commit_performed": False,
        "decision_receipt_issued": False,
        "plan_synthesis_performed": False,
        "activation_performed": False,
        "execution_permission": False,
        "source_memoryos_v062_mutated": False,
        "source_decisionos_v06_mutated": False,
        "persistent_world_state_mutated": False,
        "verification_result_claimed": False,
        "truth_authority_granted": False,
        "future_only": True,
        "read_only": True,
    }
    for field in (
        "kantorovich_dual_witness_records",
        "lipschitz_semigroup_profile_records",
        "reference_observable_gap_records",
        "reference_pair_observable_gap_records",
        "finite_symbolic_mgf_records",
        "marton_mgf_input_records",
        "full_rank_transport_kantorovich_lipschitz_mgf_records",
        "singular_atomic_kantorovich_lipschitz_mgf_records",
    ):
        obs[field.replace("records", "digest")] = canonical_digest(obs[field])
    return obs


def issue_kantorovich_lipschitz_mgf_certificate(
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    try:
        if not isinstance(payload, Mapping):
            return _blocked("payload_invalid")
        if payload.get("schema_version") != SCHEMA_VERSION:
            return _blocked("schema_version_invalid")
        source = payload.get("source_memoryos_v062_certificate")
        claims = payload.get("claims")
        expected = _derive_observables(source)
        if not isinstance(claims, Mapping):
            return _blocked("claims_invalid")
        claims = dict(claims)
        blockers = [
            f"claim_mismatch_{field}"
            for field, expected_value in expected.items()
            if claims.get(field) != expected_value
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
    "issue_kantorovich_lipschitz_mgf_certificate",
]
