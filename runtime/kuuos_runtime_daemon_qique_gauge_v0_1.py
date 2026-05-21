#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import argparse
import json
from typing import Any, Mapping

try:
    from runtime.kuuos_runtime_daemon_status_v0_1 import read_runtime_daemon_status
except ModuleNotFoundError:
    from kuuos_runtime_daemon_status_v0_1 import read_runtime_daemon_status

NON_AUTHORITY_FLAGS = {
    "grants_execution_authority": False,
    "grants_truth_authority": False,
    "grants_final_commitment_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_clinical_authority": False,
    "grants_theorem_authority": False,
    "grants_completed_identity_authority": False,
}

@dataclass(frozen=True)
class KuuOSDaemonQiQueGaugeResult:
    gauge_version: str
    daemon_status: str
    stop_reason: str | None
    qique_regime: str
    localization_score: float
    overdiffusion_score: float
    stagnation_score: float
    branch_energy: float
    scar_reentry_score: float
    recovery_budget_pressure: float
    qique_reason: str
    recommended_policy_hint: str
    qi_process_tensor_summary: dict[str, Any] | None
    missing_files: list[str]
    allowed_projection: list[str]
    grants_execution_authority: bool = False
    grants_truth_authority: bool = False
    grants_final_commitment_authority: bool = False
    grants_memory_overwrite_authority: bool = False
    grants_clinical_authority: bool = False
    grants_theorem_authority: bool = False
    grants_completed_identity_authority: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def _summary(status: Mapping[str, Any]) -> dict[str, Any] | None:
    value = status.get("latest_qi_process_tensor_summary")
    return dict(value) if isinstance(value, Mapping) else None


def evaluate_daemon_qique_gauge(status: Mapping[str, Any]) -> KuuOSDaemonQiQueGaugeResult:
    daemon_status = str(status.get("status", "UNKNOWN_STATUS"))
    stop_reason = status.get("stop_reason")
    missing_files = list(status.get("missing_files", []))
    summary = _summary(status)

    if daemon_status != "DAEMON_STATUS_READY" or missing_files:
        return KuuOSDaemonQiQueGaugeResult(
            gauge_version="kuuos_runtime_daemon_qique_gauge_v0_1",
            daemon_status=daemon_status,
            stop_reason=str(stop_reason) if stop_reason is not None else None,
            qique_regime="INFRA_HOLD",
            localization_score=0.0,
            overdiffusion_score=0.0,
            stagnation_score=1.0,
            branch_energy=0.0,
            scar_reentry_score=0.0,
            recovery_budget_pressure=1.0,
            qique_reason="daemon_status_or_files_incomplete",
            recommended_policy_hint="HOLD_FOR_DAEMON_REPAIR",
            qi_process_tensor_summary=summary,
            missing_files=missing_files,
            allowed_projection=["daemon_qique_gauge_result", "status_advisory"],
        )

    if summary is None:
        return KuuOSDaemonQiQueGaugeResult(
            gauge_version="kuuos_runtime_daemon_qique_gauge_v0_1",
            daemon_status=daemon_status,
            stop_reason=str(stop_reason) if stop_reason is not None else None,
            qique_regime="OBSERVATION_GAP",
            localization_score=0.0,
            overdiffusion_score=0.0,
            stagnation_score=0.8,
            branch_energy=0.0,
            scar_reentry_score=0.0,
            recovery_budget_pressure=0.8,
            qique_reason="missing_qi_process_tensor_summary",
            recommended_policy_hint="REOBSERVE_QI_PROCESS",
            qi_process_tensor_summary=None,
            missing_files=missing_files,
            allowed_projection=["daemon_qique_gauge_result", "status_advisory"],
        )

    history_len = int(summary.get("process_history_length", 0) or 0)
    transition_count = int(summary.get("transition_support_count", 0) or 0)
    memory_count = int(summary.get("memory_support_count", 0) or 0)
    nonmarkov_count = int(summary.get("nonmarkov_support_count", 0) or 0)
    missing_requirements = list(summary.get("missing_process_requirements", []))
    visible = bool(summary.get("process_tensor_visible", False))
    memory_visible = bool(summary.get("memory_continuity_visible", False))
    nonmarkov_visible = bool(summary.get("nonmarkov_memory_visible", False))

    localization = _clamp(memory_count / max(history_len, 1))
    overdiffusion = _clamp((history_len - transition_count) / max(history_len, 1))
    stagnation = _clamp(1.0 if missing_requirements else (0.35 if visible else 0.75))
    branch_energy = _clamp((transition_count + nonmarkov_count) / max(history_len + 1, 1))
    scar_reentry = _clamp(nonmarkov_count / max(history_len, 1))
    recovery_pressure = _clamp((len(missing_requirements) / 4.0) + (0.5 if stop_reason in {"WAITING_FOR_MORE_EVIDENCE", "QUARANTINE_RETAINED"} else 0.0))

    if stop_reason == "QUARANTINE_RETAINED":
        regime = "BOUNDARY_QUARANTINE"
        hint = "QUARANTINE_REVIEW"
        reason = "quarantine_retained"
    elif stop_reason == "WAITING_FOR_MORE_EVIDENCE":
        regime = "EVIDENCE_WAITING"
        hint = "REQUEST_MORE_EVIDENCE"
        reason = "waiting_for_more_evidence"
    elif not visible:
        regime = "PROCESS_OBSERVATION_GAP"
        hint = "REOBSERVE_QI_PROCESS"
        reason = str(summary.get("process_tensor_reason", "process_tensor_not_visible"))
    elif recovery_pressure >= 0.75:
        regime = "RECOVERY_PRESSURE_HIGH"
        hint = "SLOW_DOWN_OR_HOLD"
        reason = "recovery_budget_pressure_high"
    elif scar_reentry >= 0.34 and nonmarkov_visible:
        regime = "NONMARKOV_MEMORY_ACTIVE"
        hint = "CONTINUE_WITH_QI_MEMORY_MONITOR"
        reason = "nonmarkov_memory_active"
    elif overdiffusion >= 0.5:
        regime = "OVERDIFFUSION"
        hint = "FOCUS_OR_REOBSERVE"
        reason = "transition_support_sparse"
    elif localization >= 0.67 and memory_visible:
        regime = "LOCALIZED_MEMORY_CHANNEL"
        hint = "BRANCH_EXPLORE_OR_MONITOR"
        reason = "memory_support_localized"
    else:
        regime = "BALANCED_BOUNDED_FLOW"
        hint = "CONTINUE_BOUNDED"
        reason = "bounded_qique_flow"

    return KuuOSDaemonQiQueGaugeResult(
        gauge_version="kuuos_runtime_daemon_qique_gauge_v0_1",
        daemon_status=daemon_status,
        stop_reason=str(stop_reason) if stop_reason is not None else None,
        qique_regime=regime,
        localization_score=localization,
        overdiffusion_score=overdiffusion,
        stagnation_score=stagnation,
        branch_energy=branch_energy,
        scar_reentry_score=scar_reentry,
        recovery_budget_pressure=recovery_pressure,
        qique_reason=reason,
        recommended_policy_hint=hint,
        qi_process_tensor_summary=summary,
        missing_files=missing_files,
        allowed_projection=["daemon_qique_gauge_result", "status_advisory"],
    )


def read_and_evaluate_daemon_qique_gauge(daemon_dir: Path) -> KuuOSDaemonQiQueGaugeResult:
    status = read_runtime_daemon_status(daemon_dir)
    return evaluate_daemon_qique_gauge(status.to_dict())


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evaluate KuuOS daemon Qi-QUE gauge v0.1")
    parser.add_argument("--daemon-dir", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = read_and_evaluate_daemon_qique_gauge(args.daemon_dir)
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.recommended_policy_hint not in {"HOLD_FOR_DAEMON_REPAIR", "QUARANTINE_REVIEW"} else 1

if __name__ == "__main__":
    raise SystemExit(main())
