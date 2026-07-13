#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import math
from typing import Any, Mapping, Sequence

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
TOL = 1e-9

@dataclass
class JacobiGeodesicDeviationCertificateResult:
    status: str
    blockers: list[str]
    certificate: dict | None

def canonical_digest(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return sha256(payload).hexdigest()

def finite(x: Any) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(float(x))

def close(a: float, b: float, tol: float = TOL) -> bool:
    return math.isclose(a, b, rel_tol=0.0, abs_tol=tol)

def _coords(metric: Mapping[str, Any]) -> list[str]:
    return sorted(str(k) for k in metric)

def _matrix_ok(name: str, value: Any, c: Sequence[str]) -> tuple[list[str], dict]:
    if not isinstance(value, dict) or set(value) != set(c):
        return [f"{name}_row_schema_invalid"], {}
    out: dict[str, dict[str, float]] = {}
    errors: list[str] = []
    for i in c:
        row = value.get(i)
        if not isinstance(row, dict) or set(row) != set(c):
            errors.append(f"{name}_column_schema_invalid_{i}")
            continue
        if any(not finite(row[j]) for j in c):
            errors.append(f"{name}_nonfinite_{i}")
            continue
        out[i] = {j: float(row[j]) for j in c}
    return errors, out

def _vector_ok(name: str, value: Any, c: Sequence[str]) -> tuple[list[str], dict]:
    if not isinstance(value, dict) or set(value) != set(c):
        return [f"{name}_schema_invalid"], {}
    if any(not finite(value[i]) for i in c):
        return [f"{name}_nonfinite"], {}
    return [], {i: float(value[i]) for i in c}

def _tensor4_ok(name: str, value: Any, c: Sequence[str]) -> tuple[list[str], dict]:
    try:
        out = {i:{j:{k:{l:float(value[i][j][k][l]) for l in c} for k in c} for j in c} for i in c}
    except (KeyError, TypeError, ValueError):
        return [f"{name}_schema_invalid"], {}
    if any(not finite(out[i][j][k][l]) for i in c for j in c for k in c for l in c):
        return [f"{name}_nonfinite"], {}
    return [], out

def _dot(metric: dict, u: dict, v: dict, c: Sequence[str]) -> float:
    return sum(u[i] * metric[i][j] * v[j] for i in c for j in c)

def _curvature_action(curvature: dict, velocity: dict, jacobi: dict, c: Sequence[str]) -> dict:
    return {i: sum(curvature[i][j][k][l] * velocity[j] * jacobi[k] * velocity[l]
                   for j in c for k in c for l in c) for i in c}

def compute_jacobi_input_digest(*, metric: dict, curvature: dict, candidates: list[dict]) -> str:
    return canonical_digest({"metric": metric, "curvature": curvature, "candidates": candidates})

def build_jacobi_geodesic_deviation_certificate(
    *,
    source_atlas_certificate_digest: str,
    jacobi_input_digest: str,
    metric_matrix: dict,
    riemann_tensor: dict,
    candidate_variations: list[dict],
    maximum_absolute_covariant_acceleration: float,
    maximum_absolute_tidal_acceleration: float,
    maximum_absolute_jacobi_residual: float,
    minimum_nonzero_variation_norm: float,
    conjugate_point_tolerance: float,
) -> JacobiGeodesicDeviationCertificateResult:
    blockers: list[str] = []
    if not isinstance(source_atlas_certificate_digest, str) or not source_atlas_certificate_digest:
        blockers.append("source_atlas_certificate_digest_missing")
    if not isinstance(jacobi_input_digest, str) or not jacobi_input_digest:
        blockers.append("jacobi_input_digest_missing")
    bounds = {
        "maximum_absolute_covariant_acceleration": maximum_absolute_covariant_acceleration,
        "maximum_absolute_tidal_acceleration": maximum_absolute_tidal_acceleration,
        "maximum_absolute_jacobi_residual": maximum_absolute_jacobi_residual,
        "minimum_nonzero_variation_norm": minimum_nonzero_variation_norm,
        "conjugate_point_tolerance": conjugate_point_tolerance,
    }
    for name, value in bounds.items():
        if not finite(value) or float(value) <= 0:
            blockers.append(f"{name}_invalid")
    if not isinstance(metric_matrix, dict) or not metric_matrix:
        blockers.append("metric_matrix_empty")
        c: list[str] = []
    else:
        c = _coords(metric_matrix)
    e, metric = _matrix_ok("metric_matrix", metric_matrix, c); blockers.extend(e)
    e, curvature = _tensor4_ok("riemann_tensor", riemann_tensor, c); blockers.extend(e)
    if not isinstance(candidate_variations, list) or not candidate_variations:
        blockers.append("candidate_variations_empty")
        candidates: list[dict] = []
    else:
        candidates = []
        seen: set[str] = set()
        fields = {"candidate_id","velocity","covariant_acceleration","jacobi_field","first_covariant_derivative","second_covariant_derivative","endpoint_jacobi_field","source_candidate_digest"}
        for idx, item in enumerate(candidate_variations):
            if not isinstance(item, dict) or set(item) != fields:
                blockers.append(f"candidate_schema_invalid_{idx}"); continue
            cid = item["candidate_id"]
            if not isinstance(cid, str) or not cid:
                blockers.append(f"candidate_id_invalid_{idx}"); continue
            if cid in seen: blockers.append("duplicate_candidate_id")
            seen.add(cid)
            normalized = {"candidate_id":cid,"source_candidate_digest":item["source_candidate_digest"]}
            if not isinstance(item["source_candidate_digest"], str) or not item["source_candidate_digest"]:
                blockers.append(f"source_candidate_digest_missing_{idx}")
            bad = False
            for name in ("velocity","covariant_acceleration","jacobi_field","first_covariant_derivative","second_covariant_derivative","endpoint_jacobi_field"):
                ee, vv = _vector_ok(f"candidate_{name}_{idx}", item[name], c)
                blockers.extend(ee); bad = bad or bool(ee); normalized[name] = vv
            if not bad: candidates.append(normalized)
        candidates.sort(key=lambda x: x["candidate_id"])
    if blockers:
        return JacobiGeodesicDeviationCertificateResult(STATUS_BLOCKED, sorted(set(blockers)), None)
    if any(not close(metric[i][j], metric[j][i]) for i in c for j in c):
        blockers.append("metric_not_symmetric")
    expected = compute_jacobi_input_digest(metric=metric, curvature=curvature, candidates=candidates)
    if jacobi_input_digest != expected:
        blockers.append("jacobi_input_digest_mismatch")
    records: list[dict] = []
    conjugate_candidates: list[str] = []
    max_cov_acc = max_tidal = max_residual = 0.0
    for cand in candidates:
        cid = cand["candidate_id"]
        velocity = cand["velocity"]
        acceleration = cand["covariant_acceleration"]
        jacobi = cand["jacobi_field"]
        second = cand["second_covariant_derivative"]
        endpoint = cand["endpoint_jacobi_field"]
        tidal = _curvature_action(curvature, velocity, jacobi, c)
        residual = {i: second[i] + tidal[i] for i in c}
        cov_acc_abs = max(abs(v) for v in acceleration.values())
        tidal_abs = max(abs(v) for v in tidal.values())
        residual_abs = max(abs(v) for v in residual.values())
        max_cov_acc = max(max_cov_acc, cov_acc_abs)
        max_tidal = max(max_tidal, tidal_abs)
        max_residual = max(max_residual, residual_abs)
        if cov_acc_abs > maximum_absolute_covariant_acceleration + TOL:
            blockers.append(f"covariant_acceleration_bound_exceeded_{cid}")
        if tidal_abs > maximum_absolute_tidal_acceleration + TOL:
            blockers.append(f"tidal_acceleration_bound_exceeded_{cid}")
        if residual_abs > maximum_absolute_jacobi_residual + TOL:
            blockers.append(f"jacobi_equation_residual_exceeded_{cid}")
        variation_norm_sq = _dot(metric, jacobi, jacobi, c)
        endpoint_norm_sq = _dot(metric, endpoint, endpoint, c)
        if variation_norm_sq < minimum_nonzero_variation_norm ** 2 - TOL:
            blockers.append(f"initial_variation_too_small_{cid}")
        endpoint_vanishes = endpoint_norm_sq <= conjugate_point_tolerance ** 2
        if endpoint_vanishes: conjugate_candidates.append(cid)
        records.append({
            "candidate_id": cid,
            "source_candidate_digest": cand["source_candidate_digest"],
            "velocity": velocity,
            "covariant_acceleration": acceleration,
            "jacobi_field": jacobi,
            "first_covariant_derivative": cand["first_covariant_derivative"],
            "second_covariant_derivative": second,
            "tidal_acceleration": tidal,
            "jacobi_equation_residual": residual,
            "variation_norm_squared": variation_norm_sq,
            "endpoint_jacobi_field": endpoint,
            "endpoint_variation_norm_squared": endpoint_norm_sq,
            "local_conjugate_point_candidate": endpoint_vanishes,
        })
    if blockers:
        return JacobiGeodesicDeviationCertificateResult(STATUS_BLOCKED, sorted(set(blockers)), None)
    cert = {
        "kernel":"PlanOS Jacobi Field and Geodesic Deviation Certificate Kernel",
        "kernel_version":"v0.1","planos_version":"v1.09",
        "source_atlas_certificate_digest":source_atlas_certificate_digest,
        "jacobi_input_digest":jacobi_input_digest,
        "metric_matrix":metric,"riemann_tensor":curvature,
        "candidate_variation_records":records,
        "local_conjugate_point_candidate_ids":conjugate_candidates,
        "computed_maximum_absolute_covariant_acceleration":max_cov_acc,
        "computed_maximum_absolute_tidal_acceleration":max_tidal,
        "computed_maximum_absolute_jacobi_residual":max_residual,
        "geodesic_covariant_acceleration_bounded":True,
        "jacobi_equation_satisfied":True,
        "tidal_acceleration_retained":True,
        "conjugate_point_candidates_local_only":True,
        "candidate_identity_retained":True,
        "source_atlas_not_mutated":True,
        "persistent_world_state_unchanged":True,
        "decision_selection_performed":False,
        "history_read_only":True,
        "curvature_grants_no_authority":True,
        "jacobi_field_grants_no_authority":True,
        "conjugate_point_grants_no_authority":True,
        "future_only":True,"active_now":False,"execution_permission":False,
    }
    cert["jacobi_certificate_digest"] = canonical_digest(cert)
    return JacobiGeodesicDeviationCertificateResult(STATUS_READY, [], cert)
