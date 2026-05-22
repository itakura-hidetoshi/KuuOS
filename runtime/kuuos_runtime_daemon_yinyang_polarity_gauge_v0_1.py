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
class KuuOSDaemonYinYangPolarityResult:
    gauge_version: str
    daemon_status: str
    stop_reason: str | None
    yinyang_polarity_state: str
    yin_load: float
    yang_drive: float
    polarity_balance: float
    switch_risk: float
    false_yang_risk: float
    false_yin_risk: float
    yinyang_reason: str
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


def evaluate_daemon_yinyang_polarity(status: Mapping[str, Any]) -> KuuOSDaemonYinYangPolarityResult:
    daemon_status = str(status.get("status", "UNKNOWN_STATUS"))
    stop_reason = status.get("stop_reason")
    missing_files = list(status.get("missing_files", []))
    summary = _summary(status)

    if daemon_status != "DAEMON_STATUS_READY" or missing_files:
        return KuuOSDaemonYinYangPolarityResult(
            gauge_version="kuuos_runtime_daemon_yinyang_polarity_gauge_v0_1",
            daemon_status=daemon_status,
            stop_reason=str(stop_reason) if stop_reason is not None else None,
            yinyang_polarity_state="BOUNDARY_YIN_REQUIRED",
            yin_load=1.0,
            yang_drive=0.0,
            polarity_balance=0.0,
            switch_risk=0.7,
            false_yang_risk=0.0,
            false_yin_risk=0.0,
            yinyang_reason="daemon_status_or_files_incomplete",
            recommended_policy_hint="HOLD_FOR_DAEMON_REPAIR",
            qi_process_tensor_summary=summary,
            missing_files=missing_files,
            allowed_projection=["daemon_yinyang_polarity_result", "polarity_advisory"],
        )

    if summary is None:
        return KuuOSDaemonYinYangPolarityResult(
            gauge_version="kuuos_runtime_daemon_yinyang_polarity_gauge_v0_1",
            daemon_status=daemon_status,
            stop_reason=str(stop_reason) if stop_reason is not None else None,
            yinyang_polarity_state="YIN_REOBSERVE_REQUIRED",
            yin_load=0.8,
            yang_drive=0.1,
            polarity_balance=0.3,
            switch_risk=0.5,
            false_yang_risk=0.0,
            false_yin_risk=0.2,
            yinyang_reason="missing_qi_process_tensor_summary",
            recommended_policy_hint="REOBSERVE_QI_PROCESS",
            qi_process_tensor_summary=None,
            missing_files=missing_files,
            allowed_projection=["daemon_yinyang_polarity_result", "polarity_advisory"],
        )

    history_len = int(summary.get("process_history_length", 0) or 0)
    transition_count = int(summary.get("transition_support_count", 0) or 0)
    memory_count = int(summary.get("memory_support_count", 0) or 0)
    nonmarkov_count = int(summary.get("nonmarkov_support_count", 0) or 0)
    missing_requirements = list(summary.get("missing_process_requirements", []))
    visible = bool(summary.get("process_tensor_visible", False))
    transition_visible = bool(summary.get("transition_continuity_visible", False))
    memory_visible = bool(summary.get("memory_continuity_visible", False))
    nonmarkov_visible = bool(summary.get("nonmarkov_memory_visible", False))

    yang_drive = _clamp((transition_count + (0.5 if transition_visible else 0.0)) / max(history_len + 1, 1))
    yin_load = _clamp((memory_count + nonmarkov_count + (0.5 if memory_visible else 0.0)) / max(history_len + 1, 1))
    if stop_reason in {"WAITING_FOR_MORE_EVIDENCE", "QUARANTINE_RETAINED"}:
        yin_load = _clamp(yin_load + 0.35)
    if not visible:
        yang_drive = _clamp(yang_drive * 0.35)
        yin_load = _clamp(yin_load + 0.25)

    polarity_balance = _clamp(1.0 - abs(yang_drive - yin_load))
    switch_risk = _clamp((0.35 if nonmarkov_visible else 0.0) + (0.25 if missing_requirements else 0.0) + (0.25 if not visible else 0.0))
    false_yang_risk = _clamp((0.7 if not visible and transition_count > 0 else 0.0) + (0.25 if missing_requirements and transition_visible else 0.0))
    false_yin_risk = _clamp((0.45 if visible and transition_count >= max(history_len, 1) and memory_count == 0 else 0.0) + (0.25 if stop_reason == "WAITING_FOR_MORE_EVIDENCE" and visible else 0.0))

    if stop_reason == "QUARANTINE_RETAINED":
        state = "BOUNDARY_YIN_REQUIRED"
        hint = "QUARANTINE_REVIEW"
        reason = "quarantine_retained_requires_yin_boundary"
    elif stop_reason == "WAITING_FOR_MORE_EVIDENCE":
        state = "YIN_REOBSERVE_REQUIRED"
        hint = "REQUEST_MORE_EVIDENCE"
        reason = "evidence_gap_requires_yin_observation"
    elif not visible:
        state = "FALSE_YANG"
        hint = "REOBSERVE_QI_PROCESS"
        reason = str(summary.get("process_tensor_reason", "process_tensor_not_visible"))
    elif false_yang_risk >= 0.5:
        state = "FALSE_YANG"
        hint = "REOBSERVE_QI_PROCESS"
        reason = "transition_claim_without_boundary_support"
    elif switch_risk >= 0.6:
        state = "SWITCHING_UNSTABLE"
        hint = "HOLD_WITH_RECOVERY"
        reason = "nonmarkov_or_missing_requirement_switch_risk"
    elif yang_drive - yin_load >= 0.45:
        state = "YANG_OVERDRIVE"
        hint = "SLOW_DOWN_AND_REOBSERVE"
        reason = "yang_drive_exceeds_yin_boundary"
    elif yin_load - yang_drive >= 0.45:
        state = "YIN_STAGNATION"
        hint = "BRANCH_EXPLORE_LIGHTLY"
        reason = "yin_load_exceeds_yang_recovery"
    elif false_yin_risk >= 0.45:
        state = "FALSE_YIN"
        hint = "CONTINUE_WITH_COMPACT_MONITOR"
        reason = "hold_bias_despite_visible_transition"
    elif nonmarkov_visible and nonmarkov_count > 0:
        state = "RECOVERY_YANG_PRESENT"
        hint = "CONTINUE_WITH_QI_MEMORY_MONITOR"
        reason = "nonmarkov_memory_with_recovery_yang"
    else:
        state = "BALANCED_FLOW"
        hint = "CONTINUE_HARMONIZED"
        reason = "yin_yang_balanced_qi_process_flow"

    return KuuOSDaemonYinYangPolarityResult(
        gauge_version="kuuos_runtime_daemon_yinyang_polarity_gauge_v0_1",
        daemon_status=daemon_status,
        stop_reason=str(stop_reason) if stop_reason is not None else None,
        yinyang_polarity_state=state,
        yin_load=yin_load,
        yang_drive=yang_drive,
        polarity_balance=polarity_balance,
        switch_risk=switch_risk,
        false_yang_risk=false_yang_risk,
        false_yin_risk=false_yin_risk,
        yinyang_reason=reason,
        recommended_policy_hint=hint,
        qi_process_tensor_summary=summary,
        missing_files=missing_files,
        allowed_projection=["daemon_yinyang_polarity_result", "polarity_advisory"],
    )


def read_and_evaluate_daemon_yinyang_polarity(daemon_dir: Path) -> KuuOSDaemonYinYangPolarityResult:
    status = read_runtime_daemon_status(daemon_dir)
    return evaluate_daemon_yinyang_polarity(status.to_dict())


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evaluate KuuOS daemon Yin-Yang polarity gauge v0.1")
    parser.add_argument("--daemon-dir", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = read_and_evaluate_daemon_yinyang_polarity(args.daemon_dir)
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.recommended_policy_hint not in {"HOLD_FOR_DAEMON_REPAIR", "QUARANTINE_REVIEW"} else 1

if __name__ == "__main__":
    raise SystemExit(main())
