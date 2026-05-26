#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class QiProcessTensorProbePlanTrendSummary:
    summary_version: str
    summary_status: str
    source_index_status: str | None
    dominant_probe_type: str | None
    latest_recommended_probe_type: str | None
    latest_probe_target_time_slice: str | None
    repeated_probe_types: list[str]
    qi_process_tensor_characterization: str
    trend_interpretation: str
    recommended_operator_focus: str
    summary_blockers: list[str]
    summary_warnings: list[str]
    summary_only: bool
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


def _as_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value]


def _characterize(probe_type: str | None) -> tuple[str, str, str]:
    if probe_type == "observation_debt_probe":
        return (
            "observation_debt_limited_qi_process_tensor",
            "observation debt is repeatedly limiting process-tensor recoverability visibility",
            "review observation debt slices before considering any future probe executor",
        )
    if probe_type == "recoverability_branch_probe":
        return (
            "recoverability_branch_limited_qi_process_tensor",
            "recoverability branching is the main constrained process-tensor feature",
            "review recovery branches and keep probe planning proposal-only",
        )
    if probe_type == "memory_kernel_probe":
        return (
            "memory_kernel_fragile_qi_process_tensor",
            "memory-kernel preservation is the main fragile process-tensor feature",
            "review memory-kernel lineage before any future execution surface",
        )
    if probe_type == "safe_reentry_window_probe":
        return (
            "safe_reentry_window_narrow_qi_process_tensor",
            "safe reentry is narrow and should be widened before acting",
            "review safe reentry windows and keep control authority closed",
        )
    if probe_type == "nonmarkov_memory_link_probe":
        return (
            "nonmarkov_link_sparse_qi_process_tensor",
            "non-Markov memory links are sparse or weakly visible",
            "review non-Markov linkage evidence without executing probes",
        )
    if probe_type == "multi_time_correlation_probe":
        return (
            "multi_time_correlation_low_visibility_qi_process_tensor",
            "multi-time correlation visibility is the current limiting feature",
            "review multi-time correlation evidence and preserve read-only mode",
        )
    if probe_type == "continue_process_tensor_supervision_probe":
        return (
            "stable_supervision_qi_process_tensor",
            "process tensor supervision can continue without a new limiting probe focus",
            "continue read-only supervision and artifact indexing",
        )
    return (
        "undetermined_qi_process_tensor",
        "no dominant process-tensor feature is determined from the index",
        "collect more proposal artifacts before changing any runtime surface",
    )


def build_qi_process_tensor_probe_plan_trend_summary(*, artifact_index: Mapping[str, Any]) -> QiProcessTensorProbePlanTrendSummary:
    index = _mapping(artifact_index)
    blockers: list[str] = []
    warnings: list[str] = []
    if not index:
        blockers.append("artifact_index_missing")
    if index.get("index_status") != "QI_PROCESS_TENSOR_PROBE_PLAN_ARTIFACT_INDEX_READY":
        blockers.append("artifact_index_not_ready")
    if index.get("index_only") is not True:
        blockers.append("artifact_index_only_not_true")
    if index.get("read_only") is not True:
        blockers.append("artifact_index_read_only_not_true")
    if index.get("authority") != "none":
        blockers.append("artifact_index_authority_not_none")
    for key in ("grants_probe_execution_authority", "grants_next_tick_execution_authority", "grants_control_packet_authority", "grants_memory_overwrite_authority"):
        if index.get(key) is not False:
            blockers.append(f"artifact_index_{key}_not_false")

    dominant = str(index.get("dominant_probe_type")) if index.get("dominant_probe_type") else None
    latest = str(index.get("latest_recommended_probe_type")) if index.get("latest_recommended_probe_type") else None
    repeated = _as_list(index.get("repeated_probe_types"))
    if dominant and dominant in repeated:
        warnings.append("dominant_probe_type_repeated")
    characterization, interpretation, focus = _characterize(dominant or latest)

    status = "QI_PROCESS_TENSOR_PROBE_PLAN_TREND_SUMMARY_READY" if not blockers else "QI_PROCESS_TENSOR_PROBE_PLAN_TREND_SUMMARY_BLOCKED"
    return QiProcessTensorProbePlanTrendSummary(
        summary_version="kuuos_runtime_daemon_qi_process_tensor_probe_plan_trend_summary_v0_1",
        summary_status=status,
        source_index_status=str(index.get("index_status")) if index.get("index_status") else None,
        dominant_probe_type=dominant,
        latest_recommended_probe_type=latest,
        latest_probe_target_time_slice=str(index.get("latest_probe_target_time_slice")) if index.get("latest_probe_target_time_slice") else None,
        repeated_probe_types=repeated,
        qi_process_tensor_characterization=characterization,
        trend_interpretation=interpretation,
        recommended_operator_focus=focus,
        summary_blockers=blockers,
        summary_warnings=warnings,
        summary_only=True,
        read_only=True,
    )
