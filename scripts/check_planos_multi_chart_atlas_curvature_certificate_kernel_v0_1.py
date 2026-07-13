#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
import math

from runtime.kuuos_planos_multi_chart_atlas_curvature_certificate_kernel_v0_1 import (
    STATUS_BLOCKED,
    STATUS_READY,
    build_multi_chart_atlas_curvature_certificate,
    canonical_digest,
    invert,
    pullback_metric,
    pushforward_inverse,
    transform_riemann,
)


def zero_curvature(n: int) -> list:
    return [[[[0.0 for _ in range(n)] for _ in range(n)] for _ in range(n)] for _ in range(n)]


def fixture() -> dict:
    metric = [[1.0, 0.0], [0.0, 1.0]]
    inverse = [[1.0, 0.0], [0.0, 1.0]]
    curvature = zero_curvature(2)
    curvature[0][1][0][1] = 0.25
    curvature[0][1][1][0] = -0.25
    curvature[1][0][0][1] = -0.25
    curvature[1][0][1][0] = 0.25
    identity = [[1.0, 0.0], [0.0, 1.0]]
    jacobian = [[2.0, 0.0], [0.0, 0.5]]
    inverse_jacobian = invert(jacobian)
    assert inverse_jacobian is not None
    charts = [
        {
            "chart_id": "A-reference",
            "jacobian_from_reference": identity,
            "metric": metric,
            "inverse_metric": inverse,
            "riemann": curvature,
        },
        {
            "chart_id": "B-scaled",
            "jacobian_from_reference": jacobian,
            "metric": pullback_metric(jacobian, metric),
            "inverse_metric": pushforward_inverse(inverse_jacobian, inverse),
            "riemann": transform_riemann(inverse_jacobian, jacobian, curvature),
        },
    ]
    return {
        "source_curvature_certificate_digest": "v1.07-curvature-digest",
        "atlas_digest": canonical_digest(sorted(charts, key=lambda chart: chart["chart_id"])),
        "charts": charts,
        "maximum_absolute_jacobian": 3.0,
        "maximum_absolute_curvature": 2.0,
    }


def expect_blocked(payload: dict, blocker: str) -> None:
    result = build_multi_chart_atlas_curvature_certificate(**payload)
    assert result.status == STATUS_BLOCKED, result
    assert blocker in result.blockers, result.blockers


def main() -> int:
    payload = fixture()
    result = build_multi_chart_atlas_curvature_certificate(**payload)
    assert result.status == STATUS_READY, result.blockers
    assert result.certificate is not None
    certificate = result.certificate
    assert certificate["atlas_present"] is True
    assert certificate["atlas_cocycle_preserved"] is True
    assert certificate["metric_transform_preserved"] is True
    assert certificate["riemann_tensor_transform_preserved"] is True
    assert certificate["scalar_curvature_invariant"] is True
    assert certificate["decision_selection_performed"] is False
    assert certificate["execution_permission"] is False

    tampered = deepcopy(payload)
    tampered["atlas_digest"] = "tampered"
    expect_blocked(tampered, "atlas_digest_mismatch")

    duplicate = deepcopy(payload)
    duplicate["charts"][1]["chart_id"] = duplicate["charts"][0]["chart_id"]
    duplicate["atlas_digest"] = canonical_digest(sorted(duplicate["charts"], key=lambda chart: chart["chart_id"]))
    expect_blocked(duplicate, "duplicate_chart_id")

    singular = deepcopy(payload)
    singular["charts"][1]["jacobian_from_reference"] = [[1.0, 0.0], [0.0, 0.0]]
    singular["atlas_digest"] = canonical_digest(sorted(singular["charts"], key=lambda chart: chart["chart_id"]))
    expect_blocked(singular, "singular_chart_transition_B-scaled")

    bad_metric = deepcopy(payload)
    bad_metric["charts"][1]["metric"][0][0] += 0.5
    bad_metric["atlas_digest"] = canonical_digest(sorted(bad_metric["charts"], key=lambda chart: chart["chart_id"]))
    expect_blocked(bad_metric, "metric_transform_mismatch_B-scaled")

    bad_curvature = deepcopy(payload)
    bad_curvature["charts"][1]["riemann"][0][1][0][1] += 0.5
    bad_curvature["atlas_digest"] = canonical_digest(sorted(bad_curvature["charts"], key=lambda chart: chart["chart_id"]))
    expect_blocked(bad_curvature, "riemann_transform_mismatch_B-scaled")

    nonfinite = deepcopy(payload)
    nonfinite["charts"][1]["metric"][0][0] = math.nan
    nonfinite["atlas_digest"] = canonical_digest(sorted(nonfinite["charts"], key=lambda chart: chart["chart_id"]))
    expect_blocked(nonfinite, "metric_1_nonfinite")

    print("PASS: PlanOS v1.08 multi-chart atlas curvature certificate kernel")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
