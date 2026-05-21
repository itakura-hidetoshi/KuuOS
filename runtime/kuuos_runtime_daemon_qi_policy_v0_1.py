#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import argparse
import json
from typing import Any, Mapping

try:
    from runtime.kuuos_runtime_daemon_status_v0_1 import read_runtime_daemon_status
    from runtime.kuuos_runtime_daemon_qique_gauge_v0_1 import evaluate_daemon_qique_gauge
except ModuleNotFoundError:
    from kuuos_runtime_daemon_status_v0_1 import read_runtime_daemon_status
    from kuuos_runtime_daemon_qique_gauge_v0_1 import evaluate_daemon_qique_gauge

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
class KuuOSDaemonQiPolicyResult:
    policy_version: str
    daemon_status: str
    stop_reason: str | None
    recommended_tick_mode: str
    policy_reason: str
    required_operator_attention: bool
    qi_process_tensor_summary: dict[str, Any] | None
    daemon_qique_gauge: dict[str, Any]
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


def _missing_requirements(summary: Mapping[str, Any] | None) -> list[str]:
    if not isinstance(summary, Mapping):
        return ["qi_process_tensor_summary"]
    value = summary.get("missing_process_requirements", [])
    return list(value) if isinstance(value, list) else ["missing_process_requirements_malformed"]


def _mode_from_qique_hint(hint: str, fallback_mode: str) -> str:
    if hint in {
        "HOLD_FOR_DAEMON_REPAIR",
        "QUARANTINE_REVIEW",
        "REQUEST_MORE_EVIDENCE",
        "REOBSERVE_QI_PROCESS",
    }:
        return hint
    if hint == "SLOW_DOWN_OR_HOLD":
        return "SLOW_DOWN_OR_HOLD"
    if hint == "FOCUS_OR_REOBSERVE":
        return "FOCUS_OR_REOBSERVE"
    if hint == "BRANCH_EXPLORE_OR_MONITOR":
        return "BRANCH_EXPLORE_OR_MONITOR"
    if hint == "CONTINUE_WITH_QI_MEMORY_MONITOR":
        return "CONTINUE_WITH_QI_MEMORY_MONITOR"
    if hint == "CONTINUE_BOUNDED":
        return fallback_mode
    return fallback_mode


def evaluate_daemon_qi_policy(status: Mapping[str, Any]) -> KuuOSDaemonQiPolicyResult:
    daemon_status = str(status.get("status", "UNKNOWN_STATUS"))
    stop_reason = status.get("stop_reason")
    missing_files = list(status.get("missing_files", []))
    summary = status.get("latest_qi_process_tensor_summary")
    summary_dict = dict(summary) if isinstance(summary, Mapping) else None
    missing_requirements = _missing_requirements(summary_dict)
    qique = evaluate_daemon_qique_gauge(status).to_dict()

    if daemon_status in {"DAEMON_DIR_MISSING", "DAEMON_STATUS_INCOMPLETE"} or missing_files:
        mode = "HOLD_FOR_DAEMON_REPAIR"
        reason = "daemon_status_or_files_incomplete"
        attention = True
    elif stop_reason == "QUARANTINE_RETAINED":
        mode = "QUARANTINE_REVIEW"
        reason = "daemon_stop_reason_quarantine_retained"
        attention = True
    elif stop_reason == "WAITING_FOR_MORE_EVIDENCE":
        mode = "REQUEST_MORE_EVIDENCE"
        reason = "daemon_stop_reason_waiting_for_evidence"
        attention = True
    elif summary_dict is None:
        mode = "REOBSERVE_QI_PROCESS"
        reason = "missing_qi_process_tensor_summary"
        attention = True
    elif summary_dict.get("process_tensor_visible") is not True:
        mode = "REOBSERVE_QI_PROCESS"
        reason = str(summary_dict.get("process_tensor_reason", "process_tensor_not_visible"))
        attention = True
    elif summary_dict.get("nonmarkov_memory_visible") is True and int(summary_dict.get("process_history_length", 0) or 0) >= 3:
        mode = "CONTINUE_WITH_QI_MEMORY_MONITOR"
        reason = "process_tensor_and_nonmarkov_memory_visible"
        attention = False
    elif summary_dict.get("memory_continuity_visible") is True:
        mode = "CONTINUE_WITH_MEMORY_MONITOR"
        reason = "process_tensor_and_memory_continuity_visible"
        attention = False
    elif missing_requirements:
        mode = "REOBSERVE_QI_PROCESS"
        reason = "process_tensor_requirements_missing"
        attention = True
    else:
        mode = "CONTINUE_BOUNDED"
        reason = "process_tensor_visible_bounded_continue"
        attention = False

    qique_hint = str(qique.get("recommended_policy_hint", ""))
    qique_regime = str(qique.get("qique_regime", "UNKNOWN_QIQUE_REGIME"))
    final_mode = _mode_from_qique_hint(qique_hint, mode)
    if final_mode != mode:
        reason = f"qique_{qique_regime.lower()}"
        attention = final_mode not in {"CONTINUE_WITH_QI_MEMORY_MONITOR", "CONTINUE_WITH_MEMORY_MONITOR", "CONTINUE_BOUNDED"}

    return KuuOSDaemonQiPolicyResult(
        policy_version="kuuos_runtime_daemon_qi_policy_v0_1",
        daemon_status=daemon_status,
        stop_reason=str(stop_reason) if stop_reason is not None else None,
        recommended_tick_mode=final_mode,
        policy_reason=reason,
        required_operator_attention=attention,
        qi_process_tensor_summary=summary_dict,
        daemon_qique_gauge=qique,
        missing_files=missing_files,
        allowed_projection=["daemon_qi_policy_result", "daemon_qique_gauge_result", "status_advisory"],
    )


def read_and_evaluate_daemon_qi_policy(daemon_dir: Path) -> KuuOSDaemonQiPolicyResult:
    status = read_runtime_daemon_status(daemon_dir)
    return evaluate_daemon_qi_policy(status.to_dict())


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evaluate KuuOS daemon Qi policy v0.1")
    parser.add_argument("--daemon-dir", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = read_and_evaluate_daemon_qi_policy(args.daemon_dir)
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not result.required_operator_attention else 1

if __name__ == "__main__":
    raise SystemExit(main())
