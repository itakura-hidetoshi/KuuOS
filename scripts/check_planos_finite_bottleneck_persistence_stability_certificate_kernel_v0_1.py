#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_planos_finite_bottleneck_persistence_stability_certificate_kernel_v0_1 import (
    STATUS_READY,
    build_finite_bottleneck_persistence_stability_certificate,
)
from runtime.kuuos_planos_finite_bottleneck_persistence_stability_certificate_support_v0_1 import (
    compute_bottleneck_stability_input_digest,
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


def optimal_matching() -> list[dict]:
    return [
        {
            "match_id": "match-001",
            "dimension": 0,
            "match_kind": "point_to_point",
            "left_interval_id": "A-H0-finite",
            "right_interval_id": "B-H0-finite",
            "cost_twice": 2,
        },
        {
            "match_id": "match-002",
            "dimension": 0,
            "match_kind": "point_to_point",
            "left_interval_id": "A-H0-infinite",
            "right_interval_id": "B-H0-infinite",
            "cost_twice": 2,
        },
        {
            "match_id": "match-003",
            "dimension": 1,
            "match_kind": "point_to_point",
            "left_interval_id": "A-H1-main",
            "right_interval_id": "B-H1-main",
            "cost_twice": 2,
        },
        {
            "match_id": "match-004",
            "dimension": 1,
            "match_kind": "diagonal_to_right",
            "left_interval_id": "",
            "right_interval_id": "B-H1-extra",
            "cost_twice": 2,
        },
    ]


def build(**overrides):
    left = overrides.pop("diagram_a_intervals", diagram_a())
    right = overrides.pop("diagram_b_intervals", diagram_b())
    records = overrides.pop("simplex_perturbation_records", perturbation_records())
    matching = overrides.pop("claimed_optimal_matching", optimal_matching())
    distance_twice = overrides.pop("claimed_bottleneck_distance_twice", 2)
    sup_norm = overrides.pop("claimed_filtration_sup_norm", 1)
    digest = overrides.pop(
        "bottleneck_stability_input_digest",
        compute_bottleneck_stability_input_digest(
            diagram_a_intervals=left,
            diagram_b_intervals=right,
            simplex_perturbation_records=records,
            claimed_optimal_matching=matching,
            claimed_bottleneck_distance_twice=distance_twice,
            claimed_filtration_sup_norm=sup_norm,
        ),
    )
    args = {
        "source_persistent_homology_certificate_digest_a": "planos-v1-17-source-A",
        "source_persistent_homology_certificate_digest_b": "planos-v1-17-source-B",
        "bottleneck_stability_input_digest": digest,
        "diagram_a_intervals": left,
        "diagram_b_intervals": right,
        "simplex_perturbation_records": records,
        "claimed_optimal_matching": matching,
        "claimed_bottleneck_distance_twice": distance_twice,
        "claimed_filtration_sup_norm": sup_norm,
        "maximum_coordinate_value": 10,
        "maximum_interval_count": 10,
        "maximum_simplex_record_count": 10,
    }
    args.update(overrides)
    return build_finite_bottleneck_persistence_stability_certificate(**args)


def main() -> int:
    result = build()
    assert result.status == STATUS_READY and result.certificate is not None
    cert = result.certificate
    assert cert["diagram_metric"] == "L_infinity_with_diagonal"
    assert cert["distance_encoding"] == "twice_exact_integer"
    assert cert["optimal_matching"] == optimal_matching()
    assert cert["bottleneck_distance_twice"] == 2
    assert cert["bottleneck_distance_rational"] == {"numerator": 2, "denominator": 2}
    assert cert["filtration_sup_norm"] == 1
    assert cert["stability_budget_twice"] == 2
    assert cert["stability_slack_twice"] == 0
    assert cert["point_to_point_match_count"] == 3
    assert cert["diagonal_match_count"] == 1
    for name in (
        "interval_endpoint_bindings_verified",
        "point_matching_recomputed",
        "diagonal_matching_recomputed",
        "infinite_intervals_never_matched_to_diagonal",
        "bottleneck_distance_recomputed",
        "filtration_sup_norm_recomputed",
        "finite_stability_inequality_verified",
        "finite_diagram_pair_only",
        "dimensions_above_two_not_compared",
        "source_filtration_to_barcode_relation_not_recomputed",
        "full_persistence_stability_theorem_not_claimed",
        "wasserstein_distance_not_computed",
        "interleaving_distance_not_computed",
        "zigzag_distance_not_computed",
        "persistence_distance_does_not_rank_candidates",
        "candidate_identity_retained",
        "source_persistent_homology_certificate_a_not_mutated",
        "source_persistent_homology_certificate_b_not_mutated",
        "persistent_world_state_unchanged",
        "history_read_only",
        "bottleneck_distance_grants_no_authority",
        "stability_witness_grants_no_authority",
        "diagonal_matching_grants_no_authority",
        "future_only",
    ):
        assert cert[name] is True
    assert cert["decision_selection_performed"] is False
    assert cert["active_now"] is False
    assert cert["execution_permission"] is False

    blocked = [
        build(source_persistent_homology_certificate_digest_a=""),
        build(source_persistent_homology_certificate_digest_b=""),
        build(bottleneck_stability_input_digest="stale"),
        build(diagram_a_intervals=[]),
        build(diagram_b_intervals=[]),
        build(simplex_perturbation_records=[]),
        build(claimed_bottleneck_distance_twice=1),
        build(claimed_filtration_sup_norm=2),
        build(maximum_coordinate_value=5),
        build(maximum_interval_count=4),
        build(maximum_simplex_record_count=3),
    ]

    duplicate_interval = diagram_a()
    duplicate_interval[1]["interval_id"] = duplicate_interval[0]["interval_id"]
    blocked.append(build(diagram_a_intervals=duplicate_interval))

    duplicate_record = perturbation_records()
    duplicate_record[1]["simplex_id"] = duplicate_record[0]["simplex_id"]
    blocked.append(build(simplex_perturbation_records=duplicate_record))

    missing_infinite_partner = [
        item for item in diagram_b() if item["interval_id"] != "B-H0-infinite"
    ]
    blocked.append(build(diagram_b_intervals=missing_infinite_partner))

    bad_binding = diagram_b()
    bad_binding[-1]["birth_simplex_id"] = "missing-simplex"
    blocked.append(build(diagram_b_intervals=bad_binding))

    wrong_matching = optimal_matching()
    wrong_matching[-1]["cost_twice"] = 1
    blocked.append(build(claimed_optimal_matching=wrong_matching))

    for item in blocked:
        assert item.status != STATUS_READY
        assert item.blockers
        assert item.certificate is None

    tampered = deepcopy(perturbation_records())
    stale_digest = compute_bottleneck_stability_input_digest(
        diagram_a_intervals=diagram_a(),
        diagram_b_intervals=diagram_b(),
        simplex_perturbation_records=tampered,
        claimed_optimal_matching=optimal_matching(),
        claimed_bottleneck_distance_twice=2,
        claimed_filtration_sup_norm=1,
    )
    tampered[0]["source_simplex_digest_a"] = "tampered"
    item = build(
        simplex_perturbation_records=tampered,
        bottleneck_stability_input_digest=stale_digest,
    )
    assert item.status != STATUS_READY and item.certificate is None

    print("PASS: PlanOS Finite Bottleneck Persistence Stability Certificate Kernel v0.1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
