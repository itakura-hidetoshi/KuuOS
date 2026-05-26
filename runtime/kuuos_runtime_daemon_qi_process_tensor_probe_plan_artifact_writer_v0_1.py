#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class QiProcessTensorProbePlanArtifact:
    artifact_version: str
    artifact_status: str
    source_status_view_status: str | None
    source_out_dir: str | None
    latest_controlled_loop_result_path: str | None
    recommended_probe_type: str | None
    probe_target_time_slice: str | None
    probe_risk_level: str | None
    probe_expected_recoverability_gain: float | None
    probe_expected_observation_debt_reduction: float | None
    latest_process_tensor_probe_plan: dict[str, Any]
    artifact_blockers: list[str]
    artifact_warnings: list[str]
    proposal_artifact_only: bool
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


def _float_or_none(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _str_or_none(value: Any) -> str | None:
    return str(value) if value is not None else None


def build_qi_process_tensor_probe_plan_artifact(*, status_view: Mapping[str, Any]) -> QiProcessTensorProbePlanArtifact:
    view = _mapping(status_view)
    probe_plan = dict(_mapping(view.get("latest_process_tensor_probe_plan")))
    blockers: list[str] = []
    warnings: list[str] = []

    if not view:
        blockers.append("status_view_missing")
    if view.get("status_view_status") != "QI_PERSISTENT_SUPERVISOR_STATUS_VIEW_READY":
        blockers.append("status_view_not_ready")
    if not probe_plan:
        blockers.append("latest_process_tensor_probe_plan_missing")
    if probe_plan.get("probe_plan_status") == "QI_PROCESS_TENSOR_PROBE_PLAN_BLOCKED":
        blockers.append("probe_plan_blocked")

    if probe_plan and probe_plan.get("probe_plan_only") is not True:
        blockers.append("probe_plan_only_not_true")
    if probe_plan and probe_plan.get("read_only") is not True:
        blockers.append("probe_plan_read_only_not_true")
    if probe_plan and probe_plan.get("authority") != "none":
        blockers.append("probe_plan_authority_not_none")
    if probe_plan and probe_plan.get("grants_probe_execution_authority") is not False:
        blockers.append("probe_plan_execution_authority_not_false")
    if view.get("grants_probe_execution_authority") is not False:
        blockers.append("status_view_probe_execution_authority_not_false")

    if not _mapping(view.get("latest_process_tensor_advantage_metrics")):
        warnings.append("latest_process_tensor_advantage_metrics_missing")

    status = "QI_PROCESS_TENSOR_PROBE_PLAN_ARTIFACT_READY" if not blockers else "QI_PROCESS_TENSOR_PROBE_PLAN_ARTIFACT_BLOCKED"
    return QiProcessTensorProbePlanArtifact(
        artifact_version="kuuos_runtime_daemon_qi_process_tensor_probe_plan_artifact_writer_v0_1",
        artifact_status=status,
        source_status_view_status=_str_or_none(view.get("status_view_status")),
        source_out_dir=_str_or_none(view.get("out_dir")),
        latest_controlled_loop_result_path=_str_or_none(view.get("latest_controlled_loop_result_path")),
        recommended_probe_type=_str_or_none(view.get("recommended_probe_type") or probe_plan.get("recommended_probe_type")),
        probe_target_time_slice=_str_or_none(view.get("probe_target_time_slice") or probe_plan.get("probe_target_time_slice")),
        probe_risk_level=_str_or_none(view.get("probe_risk_level") or probe_plan.get("probe_risk_level")),
        probe_expected_recoverability_gain=_float_or_none(probe_plan.get("probe_expected_recoverability_gain")),
        probe_expected_observation_debt_reduction=_float_or_none(probe_plan.get("probe_expected_observation_debt_reduction")),
        latest_process_tensor_probe_plan=probe_plan,
        artifact_blockers=blockers,
        artifact_warnings=warnings,
        proposal_artifact_only=True,
        read_only=True,
    )
