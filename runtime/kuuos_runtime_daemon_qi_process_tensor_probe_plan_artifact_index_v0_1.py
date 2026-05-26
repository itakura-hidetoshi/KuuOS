#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
from statistics import mean
from typing import Any, Mapping, Sequence


@dataclass(frozen=True)
class QiProcessTensorProbePlanArtifactIndex:
    index_version: str
    index_status: str
    artifact_count: int
    ready_artifact_count: int
    blocked_artifact_count: int
    probe_type_counts: dict[str, int]
    risk_level_counts: dict[str, int]
    dominant_probe_type: str | None
    latest_recommended_probe_type: str | None
    latest_probe_target_time_slice: str | None
    repeated_probe_types: list[str]
    mean_expected_recoverability_gain: float | None
    mean_expected_observation_debt_reduction: float | None
    index_blockers: list[str]
    index_warnings: list[str]
    index_only: bool
    read_only: bool
    authority: str = "none"
    grants_execution_authority: bool = False
    grants_probe_execution_authority: bool = False
    grants_next_tick_execution_authority: bool = False
    grants_control_packet_authority: bool = False
    grants_memory_overwrite_authority: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _num(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _safe_mean(values: list[float]) -> float | None:
    return round(mean(values), 6) if values else None


def build_qi_process_tensor_probe_plan_artifact_index(*, artifacts: Sequence[Mapping[str, Any]]) -> QiProcessTensorProbePlanArtifactIndex:
    rows = [dict(_mapping(item)) for item in artifacts]
    blockers: list[str] = []
    warnings: list[str] = []
    if not rows:
        blockers.append("probe_plan_artifacts_missing")

    ready: list[dict[str, Any]] = []
    blocked_count = 0
    for i, artifact in enumerate(rows):
        if artifact.get("artifact_status") == "QI_PROCESS_TENSOR_PROBE_PLAN_ARTIFACT_READY":
            ready.append(artifact)
        else:
            blocked_count += 1
            warnings.append(f"artifact_{i}_not_ready")
        if artifact.get("proposal_artifact_only") is not True:
            blockers.append(f"artifact_{i}_proposal_artifact_only_not_true")
        if artifact.get("read_only") is not True:
            blockers.append(f"artifact_{i}_read_only_not_true")
        if artifact.get("authority") != "none":
            blockers.append(f"artifact_{i}_authority_not_none")
        for key in ("grants_probe_execution_authority", "grants_next_tick_execution_authority", "grants_control_packet_authority", "grants_memory_overwrite_authority"):
            if artifact.get(key) is not False:
                blockers.append(f"artifact_{i}_{key}_not_false")

    probe_types = [str(a.get("recommended_probe_type")) for a in ready if a.get("recommended_probe_type")]
    risks = [str(a.get("probe_risk_level")) for a in ready if a.get("probe_risk_level")]
    gain_values = [v for v in (_num(a.get("probe_expected_recoverability_gain")) for a in ready) if v is not None]
    debt_values = [v for v in (_num(a.get("probe_expected_observation_debt_reduction")) for a in ready) if v is not None]
    probe_counter = Counter(probe_types)
    risk_counter = Counter(risks)
    dominant = probe_counter.most_common(1)[0][0] if probe_counter else None
    repeated = sorted([name for name, count in probe_counter.items() if count >= 2])
    latest = ready[-1] if ready else {}

    status = "QI_PROCESS_TENSOR_PROBE_PLAN_ARTIFACT_INDEX_READY" if not blockers else "QI_PROCESS_TENSOR_PROBE_PLAN_ARTIFACT_INDEX_BLOCKED"
    return QiProcessTensorProbePlanArtifactIndex(
        index_version="kuuos_runtime_daemon_qi_process_tensor_probe_plan_artifact_index_v0_1",
        index_status=status,
        artifact_count=len(rows),
        ready_artifact_count=len(ready),
        blocked_artifact_count=blocked_count,
        probe_type_counts=dict(sorted(probe_counter.items())),
        risk_level_counts=dict(sorted(risk_counter.items())),
        dominant_probe_type=dominant,
        latest_recommended_probe_type=str(latest.get("recommended_probe_type")) if latest.get("recommended_probe_type") else None,
        latest_probe_target_time_slice=str(latest.get("probe_target_time_slice")) if latest.get("probe_target_time_slice") else None,
        repeated_probe_types=repeated,
        mean_expected_recoverability_gain=_safe_mean(gain_values),
        mean_expected_observation_debt_reduction=_safe_mean(debt_values),
        index_blockers=blockers,
        index_warnings=warnings,
        index_only=True,
        read_only=True,
    )
