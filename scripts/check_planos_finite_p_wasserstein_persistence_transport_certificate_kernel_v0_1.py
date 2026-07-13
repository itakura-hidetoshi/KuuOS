#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_planos_finite_p_wasserstein_persistence_transport_certificate_kernel_v0_1 import (
    STATUS_READY,
    build_finite_p_wasserstein_persistence_transport_certificate,
)
from runtime.kuuos_planos_finite_p_wasserstein_persistence_transport_certificate_support_v0_1 import (
    compute_p_wasserstein_transport_input_digest,
    cost_moment_profile,
    integer_nth_root_bounds,
    optimal_bottleneck_matching,
    optimal_p_wasserstein_transport,
    tail_profile,
)


def diagram_a() -> list[dict]:
    return [
        {
            "interval_id": "A-H0-finite",
            "dimension": 0,
            "birth": 0,
            "death": 2,
            "birth_simplex_id": "vertex-B",
            "death_simplex_id": "edge-AB",
            "source_interval_digest": "source-A-H0-finite",
        },
        {
            "interval_id": "A-H0-infinite",
            "dimension": 0,
            "birth": 0,
            "death": None,
            "birth_simplex_id": "vertex-A",
            "death_simplex_id": "",
            "source_interval_digest": "source-A-H0-infinite",
        },
        {
            "interval_id": "A-H1-main",
            "dimension": 1,
            "birth": 2,
            "death": 6,
            "birth_simplex_id": "edge-main",
            "death_simplex_id": "triangle-main",
            "source_interval_digest": "source-A-H1-main",
        },
    ]


def diagram_b() -> list[dict]:
    return [
        {
            "interval_id": "B-H0-finite",
            "dimension": 0,
            "birth": 1,
            "death": 3,
            "birth_simplex_id": "vertex-B",
            "death_simplex_id": "edge-AB",
            "source_interval_digest": "source-B-H0-finite",
        },
        {
            "interval_id": "B-H0-infinite",
            "dimension": 0,
            "birth": 1,
            "death": None,
            "birth_simplex_id": "vertex-A",
            "death_simplex_id": "",
            "source_interval_digest": "source-B-H0-infinite",
        },
        {
            "interval_id": "B-H1-main",
            "dimension": 1,
            "birth": 3,
            "death": 7,
            "birth_simplex_id": "edge-main",
            "death_simplex_id": "triangle-main",
            "source_interval_digest": "source-B-H1-main",
        },
        {
            "interval_id": "B-H1-extra",
            "dimension": 1,
            "birth": 4,
            "death": 6,
            "birth_simplex_id": "edge-extra",
            "death_simplex_id": "triangle-extra",
            "source_interval_digest": "source-B-H1-extra",
        },
    ]


def perturbation_records() -> list[dict]:
    return [
        {
            "simplex_id": "vertex-A",
            "dimension": 0,
            "filtration_a": 0,
            "filtration_b": 1,
            "source_simplex_digest_a": "source-A-vertex-A",
            "source_simplex_digest_b": "source-B-vertex-A",
        },
        {
            "simplex_id": "vertex-B",
            "dimension": 0,
            "filtration_a": 0,
            "filtration_b": 1,
            "source_simplex_digest_a": "source-A-vertex-B",
            "source_simplex_digest_b": "source-B-vertex-B",
        },
        {
            "simplex_id": "edge-AB",
            "dimension": 1,
            "filtration_a": 2,
            "filtration_b": 3,
            "source_simplex_digest_a": "source-A-edge-AB",
            "source_simplex_digest_b": "source-B-edge-AB",
        },
        {
            "simplex_id": "edge-extra",
            "dimension": 1,
            "filtration_a": 5,
            "filtration_b": 4,
            "source_simplex_digest_a": "source-A-edge-extra",
            "source_simplex_digest_b": "source-B-edge-extra",
        },
        {
            "simplex_id": "edge-main",
            "dimension": 1,
            "filtration_a": 2,
            "filtration_b": 3,
            "source_simplex_digest_a": "source-A-edge-main",
            "source_simplex_digest_b": "source-B-edge-main",
        },
        {
            "simplex_id": "triangle-extra",
            "dimension": 2,
            "filtration_a": 5,
            "filtration_b": 6,
            "source_simplex_digest_a": "source-A-triangle-extra",
            "source_simplex_digest_b": "source-B-triangle-extra",
        },
        {
            "simplex_id": "triangle-main",
            "dimension": 2,
            "filtration_a": 6,
            "filtration_b": 7,
            "source_simplex_digest_a": "source-A-triangle-main",
            "source_simplex_digest_b": "source-B-triangle-main",
        },
    ]


def reference_claims(p_exponent: int):
    left, right = diagram_a(), diagram_b()
    total, _, matching = optimal_p_wasserstein_transport(left, right, p_exponent)
    root_floor, root_ceil = integer_nth_root_bounds(total, p_exponent)
    bottleneck, _ = optimal_bottleneck_matching(left, right)
    thresholds = [1, 2, 3]
    return {
        "matching": matching,
        "total": total,
        "root_floor": root_floor,
        "root_ceil": root_ceil,
        "bottleneck": bottleneck,
        "moments": cost_moment_profile(matching, p_exponent),
        "thresholds": thresholds,
        "tail": tail_profile(matching, thresholds, p_exponent),
    }


def build(**overrides):
    left = overrides.pop("diagram_a_intervals", diagram_a())
    right = overrides.pop("diagram_b_intervals", diagram_b())
    records = overrides.pop("simplex_perturbation_records", perturbation_records())
    p_exponent = overrides.pop("p_exponent", 2)
    defaults = reference_claims(p_exponent) if 1 <= p_exponent <= 4 else reference_claims(2)
    thresholds = overrides.pop("tail_thresholds_twice", defaults["thresholds"])
    matching = overrides.pop("claimed_optimal_transport_matching", defaults["matching"])
    total = overrides.pop("claimed_transport_power_sum_twice_units", defaults["total"])
    root_floor = overrides.pop("claimed_wasserstein_root_floor_twice", defaults["root_floor"])
    root_ceil = overrides.pop("claimed_wasserstein_root_ceil_twice", defaults["root_ceil"])
    bottleneck = overrides.pop("claimed_bottleneck_distance_twice", defaults["bottleneck"])
    sup_norm = overrides.pop("claimed_filtration_sup_norm", 1)
    moments = overrides.pop("claimed_cost_moment_profile", defaults["moments"])
    tail = overrides.pop("claimed_tail_profile", defaults["tail"])
    digest = overrides.pop(
        "p_wasserstein_transport_input_digest",
        compute_p_wasserstein_transport_input_digest(
            diagram_a_intervals=left,
            diagram_b_intervals=right,
            simplex_perturbation_records=records,
            p_exponent=p_exponent,
            tail_thresholds_twice=thresholds,
            claimed_optimal_transport_matching=matching,
            claimed_transport_power_sum_twice_units=total,
            claimed_wasserstein_root_floor_twice=root_floor,
            claimed_wasserstein_root_ceil_twice=root_ceil,
            claimed_bottleneck_distance_twice=bottleneck,
            claimed_filtration_sup_norm=sup_norm,
            claimed_cost_moment_profile=moments,
            claimed_tail_profile=tail,
        ),
    )
    args = {
        "source_persistent_homology_certificate_digest_a": "planos-v1-17-source-A",
        "source_persistent_homology_certificate_digest_b": "planos-v1-17-source-B",
        "source_bottleneck_stability_certificate_digest": "planos-v1-18-bottleneck-certificate",
        "p_wasserstein_transport_input_digest": digest,
        "diagram_a_intervals": left,
        "diagram_b_intervals": right,
        "simplex_perturbation_records": records,
        "p_exponent": p_exponent,
        "tail_thresholds_twice": thresholds,
        "claimed_optimal_transport_matching": matching,
        "claimed_transport_power_sum_twice_units": total,
        "claimed_wasserstein_root_floor_twice": root_floor,
        "claimed_wasserstein_root_ceil_twice": root_ceil,
        "claimed_bottleneck_distance_twice": bottleneck,
        "claimed_filtration_sup_norm": sup_norm,
        "claimed_cost_moment_profile": moments,
        "claimed_tail_profile": tail,
        "maximum_p_exponent": 4,
        "maximum_coordinate_value": 10,
        "maximum_interval_count": 10,
        "maximum_simplex_record_count": 10,
        "maximum_tail_threshold_count": 5,
    }
    args.update(overrides)
    return build_finite_p_wasserstein_persistence_transport_certificate(**args)


def main() -> int:
    result = build()
    assert result.status == STATUS_READY and result.certificate is not None
    cert = result.certificate
    assert cert["p_exponent"] == 2
    assert cert["transport_power_sum_twice_units"] == 16
    assert cert["transport_maximum_cost_twice"] == 2
    assert cert["wasserstein_distance_twice_root_bounds"] == {"floor": 4, "ceil": 4}
    assert cert["wasserstein_distance_rational"] == {"numerator": 4, "denominator": 2}
    assert cert["bottleneck_distance_twice"] == 2
    assert cert["bottleneck_lower_bound_power_twice_units"] == 4
    assert cert["bottleneck_cardinality_upper_bound_power_twice_units"] == 16
    assert cert["filtration_cardinality_transport_budget_power_twice_units"] == 16
    assert cert["cost_moment_profile"] == [
        {"order": 1, "power_sum_twice_units": 8},
        {"order": 2, "power_sum_twice_units": 16},
    ]
    assert cert["tail_profile"] == [
        {"threshold_twice": 1, "count_at_or_above": 4, "p_power_lower_bound": 4},
        {"threshold_twice": 2, "count_at_or_above": 4, "p_power_lower_bound": 16},
        {"threshold_twice": 3, "count_at_or_above": 0, "p_power_lower_bound": 0},
    ]
    assert cert["transport_match_count"] == 4
    assert cert["point_to_point_match_count"] == 3
    assert cert["diagonal_match_count"] == 1

    cubic = build(p_exponent=3)
    assert cubic.status == STATUS_READY and cubic.certificate is not None
    assert cubic.certificate["transport_power_sum_twice_units"] == 32
    assert cubic.certificate["wasserstein_distance_twice_root_bounds"] == {"floor": 3, "ceil": 4}
    assert cubic.certificate["wasserstein_distance_rational"] is None

    for name in (
        "interval_endpoint_bindings_verified",
        "optimal_transport_matching_recomputed",
        "transport_power_sum_recomputed",
        "integer_root_bounds_recomputed",
        "bottleneck_distance_recomputed",
        "filtration_sup_norm_recomputed",
        "cost_moment_profile_recomputed",
        "tail_profile_recomputed",
        "tail_markov_power_bounds_verified",
        "bottleneck_to_wasserstein_power_bounds_verified",
        "finite_perturbation_transport_budget_verified",
        "infinite_intervals_never_matched_to_diagonal",
        "finite_diagram_pair_only",
        "bounded_p_exponent_only",
        "dimensions_above_two_not_compared",
        "irrational_wasserstein_roots_not_decimal_approximated",
        "source_filtration_to_barcode_relation_not_recomputed",
        "full_p_wasserstein_stability_theorem_not_claimed",
        "unbounded_diagram_transport_not_computed",
        "wasserstein_transport_does_not_rank_candidates",
        "tail_profile_does_not_rank_candidates",
        "moment_profile_does_not_rank_candidates",
        "candidate_identity_retained",
        "source_persistent_homology_certificate_a_not_mutated",
        "source_persistent_homology_certificate_b_not_mutated",
        "source_bottleneck_stability_certificate_not_mutated",
        "persistent_world_state_unchanged",
        "history_read_only",
        "p_wasserstein_distance_grants_no_authority",
        "transport_matching_grants_no_authority",
        "tail_moment_evidence_grants_no_authority",
        "future_only",
    ):
        assert cert[name] is True
    assert cert["decision_selection_performed"] is False
    assert cert["active_now"] is False
    assert cert["execution_permission"] is False

    blocked = [
        build(source_persistent_homology_certificate_digest_a=""),
        build(source_persistent_homology_certificate_digest_b=""),
        build(source_bottleneck_stability_certificate_digest=""),
        build(p_wasserstein_transport_input_digest="stale"),
        build(p_exponent=0),
        build(p_exponent=5),
        build(claimed_transport_power_sum_twice_units=15),
        build(claimed_wasserstein_root_floor_twice=3),
        build(claimed_wasserstein_root_ceil_twice=5),
        build(claimed_bottleneck_distance_twice=1),
        build(claimed_filtration_sup_norm=2),
        build(tail_thresholds_twice=[2, 1]),
        build(tail_thresholds_twice=[0, 1]),
        build(maximum_interval_count=4),
        build(maximum_simplex_record_count=3),
        build(maximum_tail_threshold_count=2),
    ]

    wrong_matching = reference_claims(2)["matching"]
    wrong_matching[-1]["cost_power"] = 3
    blocked.append(build(claimed_optimal_transport_matching=wrong_matching))

    wrong_moments = reference_claims(2)["moments"]
    wrong_moments[-1]["power_sum_twice_units"] = 15
    blocked.append(build(claimed_cost_moment_profile=wrong_moments))

    wrong_tail = reference_claims(2)["tail"]
    wrong_tail[1]["count_at_or_above"] = 3
    blocked.append(build(claimed_tail_profile=wrong_tail))

    duplicate_interval = diagram_a()
    duplicate_interval[1]["interval_id"] = duplicate_interval[0]["interval_id"]
    blocked.append(build(diagram_a_intervals=duplicate_interval))

    missing_infinite_partner = [
        item for item in diagram_b() if item["interval_id"] != "B-H0-infinite"
    ]
    blocked.append(build(diagram_b_intervals=missing_infinite_partner))

    bad_binding = diagram_b()
    bad_binding[-1]["birth_simplex_id"] = "missing-simplex"
    blocked.append(build(diagram_b_intervals=bad_binding))

    for item in blocked:
        assert item.status != STATUS_READY
        assert item.blockers
        assert item.certificate is None

    tampered = deepcopy(perturbation_records())
    claims = reference_claims(2)
    stale_digest = compute_p_wasserstein_transport_input_digest(
        diagram_a_intervals=diagram_a(),
        diagram_b_intervals=diagram_b(),
        simplex_perturbation_records=tampered,
        p_exponent=2,
        tail_thresholds_twice=claims["thresholds"],
        claimed_optimal_transport_matching=claims["matching"],
        claimed_transport_power_sum_twice_units=claims["total"],
        claimed_wasserstein_root_floor_twice=claims["root_floor"],
        claimed_wasserstein_root_ceil_twice=claims["root_ceil"],
        claimed_bottleneck_distance_twice=claims["bottleneck"],
        claimed_filtration_sup_norm=1,
        claimed_cost_moment_profile=claims["moments"],
        claimed_tail_profile=claims["tail"],
    )
    tampered[0]["source_simplex_digest_a"] = "tampered"
    item = build(
        simplex_perturbation_records=tampered,
        p_wasserstein_transport_input_digest=stale_digest,
    )
    assert item.status != STATUS_READY and item.certificate is None

    print("PASS: PlanOS Finite p-Wasserstein Persistence Transport Certificate Kernel v0.1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
