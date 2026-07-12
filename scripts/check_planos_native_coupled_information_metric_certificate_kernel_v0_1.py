#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_planos_native_coupled_information_metric_certificate_kernel_v0_1 import (
    STATUS_READY,
    build_native_coupled_information_metric_certificate,
    canonical_digest,
    compute_base_diagonal_metric_digest,
    compute_candidate_delta_bundle_digest,
    compute_coupling_factor_digest,
    compute_plan_coordinate_schema_digest,
)


def base_weights() -> list[dict]:
    return [
        {"coordinate": "goal", "weight": 1.0},
        {"coordinate": "reroute", "weight": 0.8},
        {"coordinate": "verification", "weight": 1.2},
    ]


def coupling_rows() -> list[dict]:
    return [
        {
            "factor_id": "resource-risk-coupling",
            "coefficients": {
                "goal": 0.30,
                "reroute": -0.20,
                "verification": 0.10,
            },
            "provenance_digest": "coupling-provenance-resource-risk",
        },
        {
            "factor_id": "verification-coherence-coupling",
            "coefficients": {
                "goal": 0.05,
                "reroute": 0.25,
                "verification": 0.35,
            },
            "provenance_digest": "coupling-provenance-verification-coherence",
        },
    ]


def candidate_deltas() -> list[dict]:
    return [
        {
            "candidate_id": "continue",
            "parameter_delta": {
                "goal": 0.20,
                "reroute": -0.10,
                "verification": 0.30,
            },
            "source_candidate_digest": "candidate-continue-digest",
        },
        {
            "candidate_id": "hold",
            "parameter_delta": {
                "goal": 0.0,
                "reroute": 0.0,
                "verification": 0.0,
            },
            "source_candidate_digest": "candidate-hold-digest",
        },
        {
            "candidate_id": "reroute",
            "parameter_delta": {
                "goal": -0.15,
                "reroute": 0.30,
                "verification": 0.10,
            },
            "source_candidate_digest": "candidate-reroute-digest",
        },
    ]


def build(**overrides):
    weights = overrides.pop("base_metric_weights", base_weights())
    coordinates = sorted(entry["coordinate"] for entry in weights)
    rows = overrides.pop("coupling_factor_rows", coupling_rows())
    candidates = overrides.pop("candidate_deltas", candidate_deltas())

    def safe_digest(function, *values):
        try:
            return function(*values)
        except (KeyError, TypeError, ValueError):
            return canonical_digest(values)

    args = {
        "source_qi_conditioned_metric_certificate_digest": (
            "planos-v0-99-qi-conditioned-metric-certificate"
        ),
        "source_world_conditioned_metric_certificate_digest": (
            "planos-v1-00-world-conditioned-metric-certificate"
        ),
        "plan_coordinate_schema_digest": safe_digest(
            compute_plan_coordinate_schema_digest, weights
        ),
        "base_diagonal_metric_digest": safe_digest(
            compute_base_diagonal_metric_digest, weights
        ),
        "base_metric_weights": weights,
        "coupling_factor_digest": safe_digest(
            compute_coupling_factor_digest, rows, coordinates
        ),
        "coupling_factor_rows": rows,
        "candidate_delta_bundle_digest": safe_digest(
            compute_candidate_delta_bundle_digest, candidates, coordinates
        ),
        "candidate_deltas": candidates,
        "minimum_metric_eigenvalue_bound": 0.75,
        "maximum_metric_eigenvalue_bound": 2.0,
    }
    args.update(overrides)
    return build_native_coupled_information_metric_certificate(**args)


def main() -> int:
    result = build()
    assert result.status == STATUS_READY and result.certificate is not None
    certificate = result.certificate

    for name in (
        "metric_symmetric",
        "metric_positive_definite",
        "metric_floor_preserved",
        "metric_ceiling_preserved",
        "non_diagonal_coupling_present",
        "diagonal_metric_recoverable_as_zero_coupling",
        "pairwise_interactions_retained",
        "interaction_sign_direction_aware",
        "world_pullback_composition_preserves_positive_definiteness",
        "source_metric_not_mutated",
        "candidate_field_retained",
        "history_read_only",
        "qi_grants_no_authority",
        "world_projection_grants_no_authority",
        "future_only",
    ):
        assert certificate[name] is True
    assert certificate["decision_selection_performed"] is False
    assert certificate["active_now"] is False
    assert certificate["execution_permission"] is False

    metric = certificate["coupled_metric"]
    assert metric["goal"]["reroute"] != 0.0
    assert metric["reroute"]["verification"] != 0.0
    assert certificate["computed_metric_lower_bound"] >= 0.75
    assert certificate["computed_metric_upper_bound"] <= 2.0

    for candidate_id, total in certificate["candidate_action_map"].items():
        base = certificate["candidate_base_diagonal_action_map"][candidate_id]
        coupling = certificate["candidate_gram_coupling_action_map"][candidate_id]
        diagonal = certificate["candidate_diagonal_component_action_map"][
            candidate_id
        ]
        pairwise = certificate["candidate_pairwise_interaction_action_map"][
            candidate_id
        ]
        assert total >= -1e-10
        assert coupling >= -1e-10
        assert abs(total - (base + coupling)) < 1e-10
        assert abs(total - (diagonal + pairwise)) < 1e-10
        for interaction in certificate["candidate_pairwise_interaction_map"][
            candidate_id
        ]:
            contribution = interaction["interaction_contribution"]
            disposition = interaction["interaction_disposition"]
            if contribution < -1e-10:
                assert disposition == "synergy"
            elif contribution > 1e-10:
                assert disposition == "tradeoff"
            else:
                assert disposition == "neutral"

    bad_weight = base_weights()
    bad_weight[0]["weight"] = 0.0

    duplicate_weight = base_weights()
    duplicate_weight[1]["coordinate"] = duplicate_weight[0]["coordinate"]

    bad_row_coordinates = coupling_rows()
    bad_row_coordinates[0]["coefficients"].pop("goal")

    zero_rows = coupling_rows()
    for row in zero_rows:
        for coordinate in row["coefficients"]:
            row["coefficients"][coordinate] = 0.0

    diagonal_only_rows = [
        {
            "factor_id": "goal-only",
            "coefficients": {
                "goal": 0.3,
                "reroute": 0.0,
                "verification": 0.0,
            },
            "provenance_digest": "goal-only-provenance",
        }
    ]

    duplicate_factor = coupling_rows()
    duplicate_factor[1]["factor_id"] = duplicate_factor[0]["factor_id"]

    duplicate_candidate = candidate_deltas()
    duplicate_candidate[1]["candidate_id"] = duplicate_candidate[0]["candidate_id"]

    bad_candidate_delta = candidate_deltas()
    bad_candidate_delta[0]["parameter_delta"].pop("goal")

    blocked = [
        build(source_qi_conditioned_metric_certificate_digest=""),
        build(source_world_conditioned_metric_certificate_digest=""),
        build(plan_coordinate_schema_digest="wrong"),
        build(base_diagonal_metric_digest="wrong"),
        build(coupling_factor_digest="wrong"),
        build(candidate_delta_bundle_digest="wrong"),
        build(minimum_metric_eigenvalue_bound=0.0),
        build(maximum_metric_eigenvalue_bound=0.7),
        build(maximum_metric_eigenvalue_bound=1.3),
        build(base_metric_weights=[]),
        build(base_metric_weights=bad_weight),
        build(base_metric_weights=duplicate_weight),
        build(coupling_factor_rows=[]),
        build(coupling_factor_rows=bad_row_coordinates),
        build(coupling_factor_rows=zero_rows),
        build(coupling_factor_rows=diagonal_only_rows),
        build(coupling_factor_rows=duplicate_factor),
        build(candidate_deltas=[]),
        build(candidate_deltas=duplicate_candidate),
        build(candidate_deltas=bad_candidate_delta),
    ]

    duplicate_provenance = coupling_rows()
    duplicate_provenance[1]["provenance_digest"] = duplicate_provenance[0][
        "provenance_digest"
    ]
    blocked.append(build(coupling_factor_rows=duplicate_provenance))

    duplicate_source_digest = candidate_deltas()
    duplicate_source_digest[1]["source_candidate_digest"] = duplicate_source_digest[0][
        "source_candidate_digest"
    ]
    blocked.append(build(candidate_deltas=duplicate_source_digest))

    nonfinite = candidate_deltas()
    nonfinite[0]["parameter_delta"]["goal"] = float("nan")
    blocked.append(build(candidate_deltas=nonfinite))

    for item in blocked:
        assert item.status != STATUS_READY
        assert item.blockers
        assert item.certificate is None

    tampered_candidates = deepcopy(candidate_deltas())
    stale_digest = compute_candidate_delta_bundle_digest(
        tampered_candidates,
        sorted(entry["coordinate"] for entry in base_weights()),
    )
    tampered_candidates[0]["parameter_delta"]["goal"] += 0.1
    item = build(
        candidate_deltas=tampered_candidates,
        candidate_delta_bundle_digest=stale_digest,
    )
    assert item.status != STATUS_READY and item.certificate is None

    print(
        "PASS: PlanOS Native Coupled Information Metric Certificate Kernel v0.1"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
