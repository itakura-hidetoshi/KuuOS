#!/usr/bin/env python3
from __future__ import annotations
import copy
from runtime.kuuos_planos_jacobi_geodesic_deviation_certificate_kernel_v0_1 import (
    STATUS_BLOCKED, STATUS_READY, build_jacobi_geodesic_deviation_certificate,
    compute_jacobi_input_digest,
)

def fixture():
    c=["x","y"]
    metric={"x":{"x":1.0,"y":0.0},"y":{"x":0.0,"y":1.0}}
    curvature={i:{j:{k:{l:0.0 for l in c} for k in c} for j in c} for i in c}
    K=0.2
    curvature["y"]["x"]["y"]["x"]=K
    curvature["y"]["x"]["x"]["y"]=-K
    curvature["x"]["y"]["x"]["y"]=K
    curvature["x"]["y"]["y"]["x"]=-K
    candidates=[{
        "candidate_id":"candidate-a","velocity":{"x":1.0,"y":0.0},
        "covariant_acceleration":{"x":0.0,"y":0.0},
        "jacobi_field":{"x":0.0,"y":1.0},
        "first_covariant_derivative":{"x":0.0,"y":-1.0},
        "second_covariant_derivative":{"x":0.0,"y":-K},
        "endpoint_jacobi_field":{"x":0.0,"y":0.0},
        "source_candidate_digest":"source-a",
    }]
    digest=compute_jacobi_input_digest(metric=metric,curvature=curvature,candidates=candidates)
    return dict(source_atlas_certificate_digest="atlas-digest",jacobi_input_digest=digest,
        metric_matrix=metric,riemann_tensor=curvature,candidate_variations=candidates,
        maximum_absolute_covariant_acceleration=1.0,maximum_absolute_tidal_acceleration=1.0,
        maximum_absolute_jacobi_residual=1e-8,minimum_nonzero_variation_norm=0.1,
        conjugate_point_tolerance=1e-8)

def main() -> int:
    base=fixture()
    result=build_jacobi_geodesic_deviation_certificate(**base)
    assert result.status==STATUS_READY and result.certificate
    cert=result.certificate
    assert cert["jacobi_equation_satisfied"] is True
    assert cert["local_conjugate_point_candidate_ids"]==["candidate-a"]
    assert cert["candidate_variation_records"][0]["tidal_acceleration"]["y"]==0.2
    assert cert["execution_permission"] is False
    bad=copy.deepcopy(base); bad["jacobi_input_digest"]="tampered"
    assert build_jacobi_geodesic_deviation_certificate(**bad).status==STATUS_BLOCKED
    bad=copy.deepcopy(base); bad["candidate_variations"][0]["second_covariant_derivative"]["y"]=1.0
    bad["jacobi_input_digest"]=compute_jacobi_input_digest(metric=bad["metric_matrix"],curvature=bad["riemann_tensor"],candidates=bad["candidate_variations"])
    assert build_jacobi_geodesic_deviation_certificate(**bad).status==STATUS_BLOCKED
    bad=copy.deepcopy(base); bad["candidate_variations"].append(copy.deepcopy(bad["candidate_variations"][0]))
    bad["jacobi_input_digest"]=compute_jacobi_input_digest(metric=bad["metric_matrix"],curvature=bad["riemann_tensor"],candidates=bad["candidate_variations"])
    assert build_jacobi_geodesic_deviation_certificate(**bad).status==STATUS_BLOCKED
    print("PASS: PlanOS v1.09 Jacobi field and geodesic deviation certificate")
    return 0

if __name__=="__main__": raise SystemExit(main())
