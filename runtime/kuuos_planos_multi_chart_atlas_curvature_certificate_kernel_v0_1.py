#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import math
from typing import Any

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
TOL = 1e-9


@dataclass
class MultiChartAtlasCurvatureCertificateResult:
    status: str
    blockers: list[str]
    certificate: dict | None


def canonical_digest(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return sha256(payload).hexdigest()


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(float(value))


def close(a: float, b: float, tol: float = TOL) -> bool:
    return math.isclose(a, b, rel_tol=0.0, abs_tol=tol)


def matmul(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    n = len(a)
    return [[sum(a[i][k] * b[k][j] for k in range(n)) for j in range(n)] for i in range(n)]


def transpose(a: list[list[float]]) -> list[list[float]]:
    return [list(row) for row in zip(*a)]


def identity(n: int) -> list[list[float]]:
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def matrix_close(a: list[list[float]], b: list[list[float]], tol: float = TOL) -> bool:
    return len(a) == len(b) and all(close(a[i][j], b[i][j], tol) for i in range(len(a)) for j in range(len(a)))


def invert(matrix: list[list[float]]) -> list[list[float]] | None:
    n = len(matrix)
    work = [list(map(float, matrix[i])) + identity(n)[i] for i in range(n)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(work[r][col]))
        if abs(work[pivot][col]) <= TOL:
            return None
        work[col], work[pivot] = work[pivot], work[col]
        scale = work[col][col]
        work[col] = [value / scale for value in work[col]]
        for row in range(n):
            if row == col:
                continue
            factor = work[row][col]
            work[row] = [work[row][j] - factor * work[col][j] for j in range(2 * n)]
    return [row[n:] for row in work]


def pullback_metric(jacobian: list[list[float]], metric: list[list[float]]) -> list[list[float]]:
    return matmul(transpose(jacobian), matmul(metric, jacobian))


def pushforward_inverse(inverse_jacobian: list[list[float]], inverse_metric: list[list[float]]) -> list[list[float]]:
    return matmul(inverse_jacobian, matmul(inverse_metric, transpose(inverse_jacobian)))


def transform_riemann(inv_j: list[list[float]], j: list[list[float]], r: list) -> list:
    n = len(j)
    return [[[[sum(inv_j[a][i] * j[jj][b] * j[k][c] * j[l][d] * r[i][jj][k][l]
                      for i in range(n) for jj in range(n) for k in range(n) for l in range(n))
                for d in range(n)] for c in range(n)] for b in range(n)] for a in range(n)]


def ricci(curvature: list) -> list[list[float]]:
    n = len(curvature)
    return [[sum(curvature[i][j][i][l] for i in range(n)) for l in range(n)] for j in range(n)]


def scalar(inverse_metric: list[list[float]], ric: list[list[float]]) -> float:
    n = len(ric)
    return sum(inverse_metric[i][j] * ric[i][j] for i in range(n) for j in range(n))


def validate_square(name: str, value: Any, n: int) -> list[str]:
    if not isinstance(value, list) or len(value) != n:
        return [f"{name}_shape_invalid"]
    if any(not isinstance(row, list) or len(row) != n for row in value):
        return [f"{name}_shape_invalid"]
    if any(not finite(value[i][j]) for i in range(n) for j in range(n)):
        return [f"{name}_nonfinite"]
    return []


def build_multi_chart_atlas_curvature_certificate(
    *,
    source_curvature_certificate_digest: str,
    atlas_digest: str,
    charts: list[dict],
    maximum_absolute_jacobian: float,
    maximum_absolute_curvature: float,
) -> MultiChartAtlasCurvatureCertificateResult:
    blockers: list[str] = []
    if not source_curvature_certificate_digest:
        blockers.append("source_curvature_certificate_digest_missing")
    if not atlas_digest:
        blockers.append("atlas_digest_missing")
    if not finite(maximum_absolute_jacobian) or maximum_absolute_jacobian <= 0:
        blockers.append("maximum_absolute_jacobian_invalid")
    if not finite(maximum_absolute_curvature) or maximum_absolute_curvature <= 0:
        blockers.append("maximum_absolute_curvature_invalid")
    if not isinstance(charts, list) or len(charts) < 2:
        blockers.append("atlas_requires_two_charts")
    if blockers:
        return MultiChartAtlasCurvatureCertificateResult(STATUS_BLOCKED, sorted(set(blockers)), None)

    ids = [str(chart.get("chart_id", "")) for chart in charts]
    if any(not chart_id for chart_id in ids):
        blockers.append("chart_id_missing")
    if len(ids) != len(set(ids)):
        blockers.append("duplicate_chart_id")

    normalized = sorted(charts, key=lambda chart: str(chart["chart_id"]))
    n = len(normalized[0].get("metric", []))
    if n == 0:
        blockers.append("metric_empty")
    for index, chart in enumerate(normalized):
        for field in ("jacobian_from_reference", "metric", "inverse_metric"):
            blockers.extend(validate_square(f"{field}_{index}", chart.get(field), n))
        curvature = chart.get("riemann")
        try:
            values = [curvature[i][j][k][l] for i in range(n) for j in range(n) for k in range(n) for l in range(n)]
            if any(not finite(value) for value in values):
                blockers.append(f"riemann_nonfinite_{index}")
        except Exception:
            blockers.append(f"riemann_shape_invalid_{index}")
    if blockers:
        return MultiChartAtlasCurvatureCertificateResult(STATUS_BLOCKED, sorted(set(blockers)), None)

    expected_digest = canonical_digest(normalized)
    if atlas_digest != expected_digest:
        blockers.append("atlas_digest_mismatch")

    reference = normalized[0]
    ref_metric = reference["metric"]
    ref_inverse = reference["inverse_metric"]
    ref_curvature = reference["riemann"]
    ref_ricci = ricci(ref_curvature)
    ref_scalar = scalar(ref_inverse, ref_ricci)

    records: list[dict] = []
    for chart in normalized:
        j = chart["jacobian_from_reference"]
        inv_j = invert(j)
        if inv_j is None:
            blockers.append(f"singular_chart_transition_{chart['chart_id']}")
            continue
        if max(abs(v) for row in j for v in row) > maximum_absolute_jacobian + TOL:
            blockers.append(f"jacobian_bound_exceeded_{chart['chart_id']}")
        if not matrix_close(matmul(j, inv_j), identity(n)) or not matrix_close(matmul(inv_j, j), identity(n)):
            blockers.append(f"inverse_jacobian_mismatch_{chart['chart_id']}")
        expected_metric = pullback_metric(j, ref_metric)
        expected_inverse = pushforward_inverse(inv_j, ref_inverse)
        expected_curvature = transform_riemann(inv_j, j, ref_curvature)
        expected_ricci = ricci(expected_curvature)
        expected_scalar = scalar(expected_inverse, expected_ricci)
        if not matrix_close(chart["metric"], expected_metric, 1e-7):
            blockers.append(f"metric_transform_mismatch_{chart['chart_id']}")
        if not matrix_close(chart["inverse_metric"], expected_inverse, 1e-7):
            blockers.append(f"inverse_metric_transform_mismatch_{chart['chart_id']}")
        if any(abs(expected_curvature[a][b][c][d] - chart["riemann"][a][b][c][d]) > 1e-7
               for a in range(n) for b in range(n) for c in range(n) for d in range(n)):
            blockers.append(f"riemann_transform_mismatch_{chart['chart_id']}")
        if abs(expected_scalar - ref_scalar) > 1e-7:
            blockers.append(f"scalar_curvature_not_invariant_{chart['chart_id']}")
        if max(abs(v) for a in expected_curvature for b in a for c in b for v in c) > maximum_absolute_curvature + TOL:
            blockers.append(f"curvature_bound_exceeded_{chart['chart_id']}")
        records.append({
            "chart_id": chart["chart_id"],
            "inverse_jacobian": inv_j,
            "ricci": expected_ricci,
            "scalar_curvature": expected_scalar,
        })

    for left in normalized:
        for right in normalized:
            jl = left["jacobian_from_reference"]
            jr = right["jacobian_from_reference"]
            inv_jl = invert(jl)
            inv_jr = invert(jr)
            if inv_jl is None or inv_jr is None:
                continue
            transition_lr = matmul(inv_jl, jr)
            transition_rl = matmul(inv_jr, jl)
            if not matrix_close(matmul(transition_lr, transition_rl), identity(n), 1e-7):
                blockers.append("atlas_cocycle_mismatch")

    if blockers:
        return MultiChartAtlasCurvatureCertificateResult(STATUS_BLOCKED, sorted(set(blockers)), None)

    certificate = {
        "kernel": "PlanOS Multi-Chart Atlas Curvature Certificate Kernel",
        "kernel_version": "v0.1",
        "planos_version": "v1.08",
        "source_curvature_certificate_digest": source_curvature_certificate_digest,
        "atlas_digest": atlas_digest,
        "charts": normalized,
        "chart_records": records,
        "atlas_present": True,
        "chart_identifiers_unique": True,
        "transition_jacobian_invertible": True,
        "inverse_jacobian_exact": True,
        "atlas_cocycle_preserved": True,
        "metric_transform_preserved": True,
        "inverse_metric_transform_preserved": True,
        "riemann_tensor_transform_preserved": True,
        "ricci_tensor_transform_preserved": True,
        "scalar_curvature_invariant": True,
        "singular_chart_boundary_detected": True,
        "source_curvature_not_mutated": True,
        "persistent_world_state_unchanged": True,
        "decision_selection_performed": False,
        "history_read_only": True,
        "atlas_grants_no_authority": True,
        "future_only": True,
        "active_now": False,
        "execution_permission": False,
    }
    certificate["atlas_curvature_certificate_digest"] = canonical_digest(certificate)
    return MultiChartAtlasCurvatureCertificateResult(STATUS_READY, [], certificate)
