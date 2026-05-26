#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class QiActuationLicenseCandidate:
    gate_version: str
    gate_status: str
    requested_actuation_mode: str
    candidate_license_kind: str | None
    allowed_next_surface: str | None
    source_summary_status: str | None
    source_characterization: str | None
    source_finality_status: str | None
    gate_blockers: list[str]
    gate_warnings: list[str]
    license_candidate_only: bool
    dry_run_candidate_only: bool
    requires_governor_approval: bool
    requires_operator_review: bool
    authority: str = "none"
    grants_execution_authority: bool = False
    grants_probe_execution_authority: bool = False
    grants_dry_run_execution_authority: bool = False
    grants_next_tick_execution_authority: bool = False
    grants_control_packet_authority: bool = False
    grants_memory_overwrite_authority: bool = False
    grants_world_update_authority: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _no_authority(prefix: str, payload: Mapping[str, Any], blockers: list[str]) -> None:
    if payload.get("authority") != "none":
        blockers.append(f"{prefix}_authority_not_none")
    for key in [
        "grants_execution_authority",
        "grants_probe_execution_authority",
        "grants_next_tick_execution_authority",
        "grants_control_packet_authority",
        "grants_memory_overwrite_authority",
    ]:
        if payload.get(key) is not False:
            blockers.append(f"{prefix}_{key}_not_false")


def build_qi_actuation_license_candidate(
    *,
    trend_summary: Mapping[str, Any],
    finality_packet: Mapping[str, Any],
    requested_actuation_mode: str,
) -> QiActuationLicenseCandidate:
    summary = _mapping(trend_summary)
    finality = _mapping(finality_packet)
    blockers: list[str] = []
    warnings: list[str] = []

    if requested_actuation_mode != "dry_run_probe_simulation":
        blockers.append("non_dry_run_actuation_not_allowed_v0_1")
    if summary.get("summary_status") != "QI_PROCESS_TENSOR_PROBE_PLAN_TREND_SUMMARY_READY":
        blockers.append("trend_summary_not_ready")
    if summary.get("summary_only") is not True or summary.get("read_only") is not True:
        blockers.append("trend_summary_boundary_flags_invalid")
    _no_authority("trend_summary", summary, blockers)

    if finality.get("packet_status") != "QI_PROCESS_TENSOR_REVIEW_FINALITY_READY":
        blockers.append("review_finality_not_ready")
    for key in ["finality_only", "release_only", "review_only", "read_only", "additive_only_future", "overwrite_forbidden"]:
        if finality.get(key) is not True:
            blockers.append(f"review_finality_{key}_not_true")
    _no_authority("review_finality", finality, blockers)

    characterization = summary.get("qi_process_tensor_characterization")
    if characterization in (None, "undetermined_qi_process_tensor"):
        warnings.append("qi_process_tensor_characterization_undetermined")

    ready = not blockers
    return QiActuationLicenseCandidate(
        gate_version="kuuos_runtime_daemon_qi_actuation_license_gate_v0_1",
        gate_status="QI_ACTUATION_LICENSE_DRY_RUN_CANDIDATE_READY" if ready else "QI_ACTUATION_LICENSE_GATE_BLOCKED",
        requested_actuation_mode=requested_actuation_mode,
        candidate_license_kind="dry_run_probe_simulation_candidate" if ready else None,
        allowed_next_surface="dry_run_probe_executor_candidate_review" if ready else None,
        source_summary_status=str(summary.get("summary_status")) if summary.get("summary_status") else None,
        source_characterization=str(characterization) if characterization else None,
        source_finality_status=str(finality.get("packet_status")) if finality.get("packet_status") else None,
        gate_blockers=blockers,
        gate_warnings=warnings,
        license_candidate_only=True,
        dry_run_candidate_only=True,
        requires_governor_approval=True,
        requires_operator_review=True,
    )
