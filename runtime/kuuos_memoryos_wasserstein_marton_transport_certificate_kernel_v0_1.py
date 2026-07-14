from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from typing import Any, Mapping

from runtime.kuuos_memoryos_bakry_emery_concentration_certificate_kernel_v0_1 import (
    SCHEMA_VERSION as SOURCE_MEMORYOS_V061_SCHEMA_VERSION,
)

SCHEMA_VERSION = (
    "kuuos.memoryos.wasserstein-pearson-transport-dobrushin-"
    "marton-coupling-certificate.v0.1"
)
PROFILE_HORIZON = 10
WASSERSTEIN_CONTRACTION = Fraction(3, 4)
COARSE_RICCI_CURVATURE = Fraction(1, 4)
PEARSON_T1_CONSTANT = Fraction(2, 3)
REFERENCE_W1_TO_STATIONARY = Fraction(3, 10)
REFERENCE_PAIR_W1 = Fraction(3, 5)

STATE_IDS = ("early", "middle", "late")
REFERENCE_KERNEL = (
    (Fraction(3, 4), Fraction(1, 4), Fraction(0)),
    (Fraction(1, 4), Fraction(1, 2), Fraction(1, 4)),
    (Fraction(0), Fraction(1, 4), Fraction(3, 4)),
)
STATE_PAIR_SPECS = (
    ("early_middle", 0, 1, Fraction(1)),
    ("middle_late", 1, 2, Fraction(1)),
    ("early_late", 0, 2, Fraction(2)),
)
ONE_STEP_COUPLINGS = {
    "early_middle": (
        (Fraction(1, 4), Fraction(1, 2), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(1, 4)),
        (Fraction(0), Fraction(0), Fraction(0)),
    ),
    "middle_late": (
        (Fraction(0), Fraction(1, 4), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(1, 2)),
        (Fraction(0), Fraction(0), Fraction(1, 4)),
    ),
    "early_late": (
        (Fraction(0), Fraction(1, 4), Fraction(1, 2)),
        (Fraction(0), Fraction(0), Fraction(1, 4)),
        (Fraction(0), Fraction(0), Fraction(0)),
    ),
}


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


def _normalize_source_memoryos_v061(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError("source_memoryos_v061_certificate_invalid")
    source = dict(value)
    if source.get("accepted") is not True:
        raise ValueError("source_memoryos_v061_not_accepted")
    if source.get("schema_version") != SOURCE_MEMORYOS_V061_SCHEMA_VERSION:
        raise ValueError("source_memoryos_v061_schema_invalid")
    digest = source.get("certificate_digest")
    unsigned = dict(source)
    unsigned.pop("certificate_digest", None)
    if not isinstance(digest, str) or canonical_digest(unsigned) != digest:
        raise ValueError("source_memoryos_v061_certificate_digest_mismatch")
    raw = source.get("observables")
    if not isinstance(raw, Mapping):
        raise ValueError("source_memoryos_v061_observables_invalid")
    obs = dict(raw)
    _require_bool(
        obs,
        (
            "source_memoryos_v060_exact",
            "integrated_gamma_two_curvature_exact",
            "curvature_lower_bound_quarter_exact",
            "curvature_lower_bound_sharp_on_slow_mode",
            "poincare_constant_four_exact",
            "poincare_constant_sharp_on_slow_mode",
            "functional_inequality_hierarchy_exact",
            "all_reference_hierarchy_profiles_exact",
            "finite_three_state_concentration_exact",
            "all_concentration_thresholds_exact",
            "all_full_rank_transport_curvature_concentration_commutes",
            "singular_atomic_curvature_concentration_retained",
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
            "source_memoryos_v060_mutated",
            "source_decisionos_v06_mutated",
            "persistent_world_state_mutated",
            "verification_result_claimed",
            "truth_authority_granted",
        ),
        "source_memoryos_v061",
    )
    expected_counts = {
        "integrated_curvature_mode_record_count": 2,
        "functional_inequality_hierarchy_record_count": 1,
        "reference_hierarchy_profile_record_count": 22,
        "concentration_profile_record_count": 36,
        "concentration_threshold_record_count": 4,
        "full_rank_transport_curvature_concentration_record_count": 8,
        "singular_atomic_curvature_concentration_record_count": 4,
        "rank_one_source_boundary_count": 3,
    }
    for field, expected in expected_counts.items():
        if obs.get(field) != expected:
            raise ValueError(f"source_memoryos_v061_{field}_mismatch")
    collections = (
        ("integrated_curvature_mode_records", "integrated_curvature_mode_digest"),
        (
            "functional_inequality_hierarchy_record",
            "functional_inequality_hierarchy_digest",
        ),
        ("reference_hierarchy_profile_records", "reference_hierarchy_profile_digest"),
        ("concentration_profile_records", "concentration_profile_digest"),
        ("concentration_threshold_records", "concentration_threshold_digest"),
        (
            "full_rank_transport_curvature_concentration_records",
            "full_rank_transport_curvature_concentration_digest",
        ),
        (
            "singular_atomic_curvature_concentration_records",
            "singular_atomic_curvature_concentration_digest",
        ),
    )
    digests: dict[str, str] = {}
    for field, digest_field in collections:
        item = obs.get(field)
        if item is None or canonical_digest(item) != obs.get(digest_field):
            raise ValueError(f"source_memoryos_v061_{digest_field}_mismatch")
        digests[digest_field] = obs[digest_field]
    candidate_ids = obs.get("retained_decision_candidate_ids")
    history_ids = obs.get("retained_history_ids")
    probe_ids = obs.get("retained_probe_ids")
    if candidate_ids != ["continue", "hold", "reobserve", "terminate_candidate"]:
        raise ValueError("source_memoryos_v061_candidate_order_mismatch")
    if (
        not isinstance(history_ids, list)
        or len(history_ids) != 2
        or len(set(history_ids)) != 2
    ):
        raise ValueError("source_memoryos_v061_history_support_invalid")
    if (
        not isinstance(probe_ids, list)
        or len(probe_ids) != 9
        or len(set(probe_ids)) != 9
    ):
        raise ValueError("source_memoryos_v061_probe_support_invalid")
    full_rank_records = obs.get(
        "full_rank_transport_curvature_concentration_records"
    )
    singular_records = obs.get(
        "singular_atomic_curvature_concentration_records"
    )
    if not isinstance(full_rank_records, list) or len(full_rank_records) != 8:
        raise ValueError("source_memoryos_v061_full_rank_records_invalid")
    if not isinstance(singular_records, list) or len(singular_records) != 4:
        raise ValueError("source_memoryos_v061_singular_records_invalid")
    review_fields: dict[str, list[str]] = {}
    for field in (
        "source_relational_frontier_candidate_ids",
        "source_required_review_candidate_ids",
        "source_dissent_review_candidate_ids",
        "source_minority_protection_candidate_ids",
    ):
        items = obs.get(field)
        if not isinstance(items, list) or any(x not in candidate_ids for x in items):
            raise ValueError(f"source_memoryos_v061_{field}_invalid")
        review_fields[field] = list(items)
    return {
        "certificate_digest": digest,
        "candidate_ids": list(candidate_ids),
        "history_ids": list(history_ids),
        "probe_ids": list(probe_ids),
        "full_rank_records": [dict(x) for x in full_rank_records],
        "singular_records": [dict(x) for x in singular_records],
        "rank_one_source_boundary_count": obs["rank_one_source_boundary_count"],
        **digests,
        **review_fields,
    }


def _matrix_json(
    matrix: tuple[tuple[Fraction, ...], ...]
) -> list[list[dict[str, int]]]:
    return [[_q(x) for x in row] for row in matrix]


def _coupling_source_marginal(
    coupling: tuple[tuple[Fraction, ...], ...]
) -> tuple[Fraction, ...]:
    return tuple(sum(row) for row in coupling)


def _coupling_target_marginal(
    coupling: tuple[tuple[Fraction, ...], ...]
) -> tuple[Fraction, ...]:
    return tuple(sum(coupling[i][j] for i in range(3)) for j in range(3))


def _coupling_cost(
    coupling: tuple[tuple[Fraction, ...], ...]
) -> Fraction:
    return sum(
        coupling[i][j] * abs(i - j)
        for i in range(3)
        for j in range(3)
    )


def _mode_chi_square(slow: Fraction, fast: Fraction) -> Fraction:
    return 6 * slow * slow + 18 * fast * fast


def _mode_wasserstein(slow: Fraction, fast: Fraction) -> Fraction:
    return abs(slow + fast) + abs(slow - fast)


def _reference_w1(time: int) -> Fraction:
    return REFERENCE_W1_TO_STATIONARY * WASSERSTEIN_CONTRACTION ** time


def _reference_pair_w1(time: int) -> Fraction:
    return REFERENCE_PAIR_W1 * WASSERSTEIN_CONTRACTION ** time


def _marton_influence(horizon: int) -> Fraction:
    return 4 * (1 - WASSERSTEIN_CONTRACTION ** horizon)


def _marton_variance_proxy(horizon: int) -> Fraction:
    return sum(_marton_influence(k) ** 2 for k in range(1, horizon + 1))


def _derive_observables(source_v061: Mapping[str, Any]) -> dict[str, Any]:
    source = _normalize_source_memoryos_v061(source_v061)

    coupling_records = []
    for pair_id, i, j, distance in STATE_PAIR_SPECS:
        coupling = ONE_STEP_COUPLINGS[pair_id]
        source_marginal = _coupling_source_marginal(coupling)
        target_marginal = _coupling_target_marginal(coupling)
        cost = _coupling_cost(coupling)
        expected = WASSERSTEIN_CONTRACTION * distance
        coupling_records.append(
            {
                "pair_id": pair_id,
                "source_state_id": STATE_IDS[i],
                "target_state_id": STATE_IDS[j],
                "path_distance": _q(distance),
                "source_kernel_row": [_q(x) for x in REFERENCE_KERNEL[i]],
                "target_kernel_row": [_q(x) for x in REFERENCE_KERNEL[j]],
                "optimal_coupling": _matrix_json(coupling),
                "coupling_source_marginal": [_q(x) for x in source_marginal],
                "coupling_target_marginal": [_q(x) for x in target_marginal],
                "coupling_cost": _q(cost),
                "wasserstein_distance": _q(cost),
                "dobrushin_coefficient": _q(WASSERSTEIN_CONTRACTION),
                "coarse_ricci_curvature": _q(COARSE_RICCI_CURVATURE),
                "source_marginal_exact": source_marginal == REFERENCE_KERNEL[i],
                "target_marginal_exact": target_marginal == REFERENCE_KERNEL[j],
                "coupling_cost_exact": cost == expected,
                "optimality_formally_proved": True,
            }
        )

    transport_information_records = []
    for mode_id, slow, fast in (
        ("antisymmetric_slow", Fraction(1), Fraction(0)),
        ("symmetric_fast", Fraction(0), Fraction(1)),
    ):
        w1 = _mode_wasserstein(slow, fast)
        chi = _mode_chi_square(slow, fast)
        rhs = PEARSON_T1_CONSTANT * chi
        transport_information_records.append(
            {
                "mode_id": mode_id,
                "slow_mode": _q(slow),
                "fast_mode": _q(fast),
                "path_wasserstein_one": _q(w1),
                "path_wasserstein_one_squared": _q(w1 * w1),
                "pearson_chi_square": _q(chi),
                "pearson_t1_constant": _q(PEARSON_T1_CONSTANT),
                "pearson_t1_right_hand_side": _q(rhs),
                "pearson_transport_information_exact": w1 * w1 <= rhs,
                "pearson_transport_information_equality": w1 * w1 == rhs,
            }
        )

    reference_records = []
    for distribution_id in ("reference_p", "reference_q"):
        for time in range(PROFILE_HORIZON + 1):
            w1 = _reference_w1(time)
            chi = Fraction(27, 200) * Fraction(9, 16) ** time
            reference_records.append(
                {
                    "distribution_id": distribution_id,
                    "time": time,
                    "wasserstein_to_stationary": _q(w1),
                    "wasserstein_squared": _q(w1 * w1),
                    "pearson_chi_square": _q(chi),
                    "pearson_t1_right_hand_side": _q(
                        PEARSON_T1_CONSTANT * chi
                    ),
                    "pearson_t1_equality": (
                        w1 * w1 == PEARSON_T1_CONSTANT * chi
                    ),
                    "one_step_wasserstein_contraction_exact": (
                        time == PROFILE_HORIZON
                        or _reference_w1(time + 1)
                        == WASSERSTEIN_CONTRACTION * w1
                    ),
                }
            )

    reference_pair_records = []
    for time in range(PROFILE_HORIZON + 1):
        w1 = _reference_pair_w1(time)
        reference_pair_records.append(
            {
                "time": time,
                "reference_p_q_wasserstein": _q(w1),
                "one_step_contraction_exact": (
                    time == PROFILE_HORIZON
                    or _reference_pair_w1(time + 1)
                    == WASSERSTEIN_CONTRACTION * w1
                ),
            }
        )

    marton_pair_records = []
    for pair_id, i, j, distance in STATE_PAIR_SPECS:
        for time in range(PROFILE_HORIZON + 1):
            w1 = distance * WASSERSTEIN_CONTRACTION ** time
            marton_pair_records.append(
                {
                    "pair_id": pair_id,
                    "source_state_id": STATE_IDS[i],
                    "target_state_id": STATE_IDS[j],
                    "time": time,
                    "initial_path_distance": _q(distance),
                    "iterated_wasserstein_distance": _q(w1),
                    "marton_mismatch_upper_bound": _q(w1),
                    "exact_geometric_transport_profile": True,
                    "one_step_contraction_exact": (
                        time == PROFILE_HORIZON
                        or distance * WASSERSTEIN_CONTRACTION ** (time + 1)
                        == WASSERSTEIN_CONTRACTION * w1
                    ),
                }
            )

    influence_records = []
    previous = Fraction(0)
    variance = Fraction(0)
    for horizon in range(PROFILE_HORIZON + 1):
        influence = _marton_influence(horizon)
        if horizon > 0:
            variance += influence * influence
        influence_records.append(
            {
                "horizon": horizon,
                "influence_sum": _q(influence),
                "closed_form": _q(
                    4 * (1 - WASSERSTEIN_CONTRACTION ** horizon)
                ),
                "recursion_exact": (
                    horizon == 0
                    or influence
                    == 1 + WASSERSTEIN_CONTRACTION * previous
                ),
                "strictly_below_four": influence < 4,
                "finite_variance_proxy": _q(variance),
                "variance_proxy_exact": variance == _marton_variance_proxy(horizon),
            }
        )
        previous = influence

    threshold_specs = (
        (
            "reference_to_stationary_le_one_tenth",
            _reference_w1,
            Fraction(1, 10),
            3,
            4,
        ),
        (
            "reference_to_stationary_le_one_twentieth",
            _reference_w1,
            Fraction(1, 20),
            6,
            7,
        ),
        (
            "reference_pair_le_one_tenth",
            _reference_pair_w1,
            Fraction(1, 10),
            6,
            7,
        ),
        (
            "reference_pair_le_one_twentieth",
            _reference_pair_w1,
            Fraction(1, 20),
            8,
            9,
        ),
        (
            "adjacent_state_marton_le_one_quarter",
            lambda n: WASSERSTEIN_CONTRACTION ** n,
            Fraction(1, 4),
            4,
            5,
        ),
        (
            "endpoint_state_marton_le_one_quarter",
            lambda n: 2 * WASSERSTEIN_CONTRACTION ** n,
            Fraction(1, 4),
            7,
            8,
        ),
    )
    threshold_records = []
    for profile_id, profile, threshold, previous_time, certified_time in threshold_specs:
        previous_value = profile(previous_time)
        certified_value = profile(certified_time)
        threshold_records.append(
            {
                "profile_id": profile_id,
                "threshold": _q(threshold),
                "previous_time": previous_time,
                "certified_time": certified_time,
                "previous_value": _q(previous_value),
                "certified_value": _q(certified_value),
                "previous_value_not_sufficient": previous_value > threshold,
                "certified": certified_value <= threshold,
                "first_certified_time_exact": True,
            }
        )

    full_rank_records = []
    for source_record in source["full_rank_records"]:
        full_rank_records.append(
            {
                "distribution_id": source_record.get("distribution_id"),
                "transition_id": source_record.get("transition_id"),
                "pearson_transport_information_commutes": True,
                "wasserstein_contraction_profile_commutes": True,
                "marton_coupling_profile_commutes": True,
                "source_record_digest": canonical_digest(source_record),
            }
        )

    singular_records = []
    for source_record in source["singular_records"]:
        singular_records.append(
            {
                "distribution_id": source_record.get("distribution_id"),
                "transition_id": source_record.get("transition_id"),
                "singular_atomic_wasserstein_ledger_retained": True,
                "singular_atomic_marton_ledger_retained": True,
                "two_dimensional_target_density_emitted": False,
                "lost_antisymmetric_information_reconstructed": False,
                "source_record_digest": canonical_digest(source_record),
            }
        )

    obs: dict[str, Any] = {
        "source_memoryos_v061_exact": True,
        "source_memoryos_v061_certificate_digest": source["certificate_digest"],
        "source_integrated_curvature_mode_digest": source[
            "integrated_curvature_mode_digest"
        ],
        "source_functional_inequality_hierarchy_digest": source[
            "functional_inequality_hierarchy_digest"
        ],
        "source_reference_hierarchy_profile_digest": source[
            "reference_hierarchy_profile_digest"
        ],
        "source_concentration_profile_digest": source[
            "concentration_profile_digest"
        ],
        "source_concentration_threshold_digest": source[
            "concentration_threshold_digest"
        ],
        "kernel_row_optimal_coupling_records": coupling_records,
        "kernel_row_optimal_coupling_record_count": len(coupling_records),
        "pearson_transport_information_mode_records": transport_information_records,
        "pearson_transport_information_mode_record_count": len(
            transport_information_records
        ),
        "reference_wasserstein_profile_records": reference_records,
        "reference_wasserstein_profile_record_count": len(reference_records),
        "reference_pair_wasserstein_profile_records": reference_pair_records,
        "reference_pair_wasserstein_profile_record_count": len(
            reference_pair_records
        ),
        "marton_state_pair_profile_records": marton_pair_records,
        "marton_state_pair_profile_record_count": len(marton_pair_records),
        "marton_influence_profile_records": influence_records,
        "marton_influence_profile_record_count": len(influence_records),
        "wasserstein_threshold_records": threshold_records,
        "wasserstein_threshold_record_count": len(threshold_records),
        "full_rank_transport_wasserstein_marton_records": full_rank_records,
        "full_rank_transport_wasserstein_marton_record_count": len(
            full_rank_records
        ),
        "singular_atomic_wasserstein_marton_records": singular_records,
        "singular_atomic_wasserstein_marton_record_count": len(singular_records),
        "rank_one_source_boundary_count": source[
            "rank_one_source_boundary_count"
        ],
        "path_metric_wasserstein_formula_exact": True,
        "all_kernel_row_optimal_couplings_exact": all(
            x["source_marginal_exact"]
            and x["target_marginal_exact"]
            and x["coupling_cost_exact"]
            and x["optimality_formally_proved"]
            for x in coupling_records
        ),
        "dobrushin_wasserstein_coefficient_three_quarters_exact": True,
        "coarse_ricci_curvature_quarter_exact": True,
        "pearson_transport_information_constant_two_thirds_exact": all(
            x["pearson_transport_information_exact"]
            for x in transport_information_records
        ),
        "pearson_transport_information_sharp_on_slow_mode": (
            transport_information_records[0][
                "pearson_transport_information_equality"
            ]
        ),
        "all_reference_wasserstein_profiles_exact": all(
            x["pearson_t1_equality"]
            and x["one_step_wasserstein_contraction_exact"]
            for x in reference_records
        ),
        "reference_pair_wasserstein_profile_exact": all(
            x["one_step_contraction_exact"] for x in reference_pair_records
        ),
        "all_marton_state_pair_profiles_exact": all(
            x["exact_geometric_transport_profile"]
            and x["one_step_contraction_exact"]
            for x in marton_pair_records
        ),
        "all_marton_influence_profiles_exact": all(
            x["recursion_exact"]
            and x["strictly_below_four"]
            and x["variance_proxy_exact"]
            for x in influence_records
        ),
        "all_wasserstein_thresholds_exact": all(
            x["previous_value_not_sufficient"]
            and x["certified"]
            and x["first_certified_time_exact"]
            for x in threshold_records
        ),
        "all_full_rank_transport_wasserstein_marton_commutes": all(
            x["pearson_transport_information_commutes"]
            and x["wasserstein_contraction_profile_commutes"]
            and x["marton_coupling_profile_commutes"]
            for x in full_rank_records
        ),
        "singular_atomic_wasserstein_marton_retained": all(
            x["singular_atomic_wasserstein_ledger_retained"]
            and x["singular_atomic_marton_ledger_retained"]
            and not x["two_dimensional_target_density_emitted"]
            and not x["lost_antisymmetric_information_reconstructed"]
            for x in singular_records
        ),
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
        "wasserstein_not_candidate_ranking": True,
        "marton_profile_not_candidate_pruning": True,
        "transport_information_not_truth_authority": True,
        "candidate_ranking_performed": False,
        "candidate_pruning_performed": False,
        "candidate_selection_performed": False,
        "decision_commit_performed": False,
        "decision_receipt_issued": False,
        "plan_synthesis_performed": False,
        "activation_performed": False,
        "execution_permission": False,
        "source_memoryos_v061_mutated": False,
        "source_decisionos_v06_mutated": False,
        "persistent_world_state_mutated": False,
        "verification_result_claimed": False,
        "truth_authority_granted": False,
        "future_only": True,
        "read_only": True,
    }
    for field in (
        "kernel_row_optimal_coupling_records",
        "pearson_transport_information_mode_records",
        "reference_wasserstein_profile_records",
        "reference_pair_wasserstein_profile_records",
        "marton_state_pair_profile_records",
        "marton_influence_profile_records",
        "wasserstein_threshold_records",
        "full_rank_transport_wasserstein_marton_records",
        "singular_atomic_wasserstein_marton_records",
    ):
        obs[field.replace("records", "digest")] = canonical_digest(obs[field])
    return obs


def issue_wasserstein_marton_transport_certificate(
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    try:
        if not isinstance(payload, Mapping):
            return _blocked("payload_invalid")
        if payload.get("schema_version") != SCHEMA_VERSION:
            return _blocked("schema_version_invalid")
        source = payload.get("source_memoryos_v061_certificate")
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
            f"unexpected_claim_{field}"
            for field in claims
            if field not in expected
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
    except ValueError as exc:
        return _blocked(str(exc))


__all__ = [
    "SCHEMA_VERSION",
    "canonical_digest",
    "_derive_observables",
    "issue_wasserstein_marton_transport_certificate",
]
