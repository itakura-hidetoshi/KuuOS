#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import argparse
import json
from typing import Any, Mapping


@dataclass(frozen=True)
class QiProcessTensorFocusPlan:
    plan_version: str
    plan_status: str
    source_metrics_status: str | None
    source_advantage_score: float | None
    source_advantage_level: str | None
    source_recommended_next_process_focus: str | None
    operator_focus: str
    proposal_kind: str
    proposal_label: str
    proposed_operator_actions: list[str]
    required_preconditions: list[str]
    hold_reasons: list[str]
    audit_notes: list[str]
    blockers: list[str]
    warnings: list[str]
    focus_plan_only: bool
    read_only: bool
    grants_execution_authority: bool = False
    grants_next_tick_execution_authority: bool = False
    grants_truth_authority: bool = False
    grants_final_commitment_authority: bool = False
    grants_memory_overwrite_authority: bool = False
    grants_clinical_authority: bool = False
    grants_theorem_authority: bool = False
    grants_completed_identity_authority: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _as_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _metrics_payload(source: Mapping[str, Any]) -> Mapping[str, Any]:
    nested = source.get("latest_process_tensor_advantage_metrics")
    if isinstance(nested, dict) and nested:
        return nested
    return source


def _proposal_for_focus(focus: str | None) -> tuple[str, str, str, list[str], list[str], list[str], list[str]]:
    if focus == "resolve_observation_debt":
        return (
            "observation_debt_resolution",
            "add_evidence_request",
            "Request process-tensor observation debt probe",
            [
                "identify_missing_multi_time_correlation_slice",
                "add_observability_probe_for_missing_history_link",
                "rerun_status_view_after_probe_result",
            ],
            [
                "probe_is_read_only",
                "raw_observation_does_not_grant_intervention",
                "observation_receipt_required",
            ],
            ["hold_execution_until_observation_debt_rechecked"],
            ["focus derived from process tensor advantage observation debt priority"],
        )
    if focus == "open_recoverability_branch":
        return (
            "recoverability_branch_opening",
            "add_repair_stub",
            "Open conservative recoverability branch proposal",
            [
                "request_recoverability_branch_witness",
                "compare_safe_reentry_candidates_against_barrier",
                "route_to_hold_if_branch_witness_missing",
            ],
            [
                "recovery_branch_is_candidate_only",
                "barrier_witness_required_before_reentry",
                "no_raw_rollout_to_decision",
            ],
            ["hold_reentry_until_recoverability_witness"],
            ["focus derived from low recoverability branching capacity"],
        )
    if focus == "preserve_memory_kernel":
        return (
            "memory_kernel_preservation",
            "add_guard",
            "Preserve process-tensor memory kernel before compaction",
            [
                "freeze_nonmarkov_history_links_before_compaction",
                "mark_future_response_relevant_history",
                "deny_trace_compaction_if_memory_kernel_unwitnessed",
            ],
            [
                "memory_kernel_witness_required",
                "trace_compaction_must_not_hide_blockers",
                "semantic_overwrite_forbidden",
            ],
            ["hold_compaction_until_memory_kernel_preserved"],
            ["focus derived from weak memory kernel preservation score"],
        )
    if focus == "widen_safe_reentry_window":
        return (
            "safe_reentry_window_widening",
            "add_conservative_route",
            "Widen safe reentry window conservatively",
            [
                "request_safe_reentry_window_witness",
                "tighten_reentry_barrier_thresholds_before_retry",
                "fallback_to_hold_if_window_not_witnessed",
            ],
            [
                "safe_reentry_window_witness_required",
                "next_tick_execution_authority_not_granted",
                "baseline_fallback_required",
            ],
            ["hold_next_tick_until_safe_reentry_window_witness"],
            ["focus derived from low safe reentry window score"],
        )
    if focus == "continue_process_tensor_supervision":
        return (
            "continue_supervision",
            "add_monitor_metric",
            "Continue process tensor supervision with advantage tracking",
            [
                "keep_advantage_metrics_in_status_view",
                "monitor_nonmarkov_link_density_drift",
                "recheck_observation_debt_each_cycle",
            ],
            [
                "bounded_supervisor_control_required",
                "status_view_read_only",
                "no_direct_execution_authority",
            ],
            [],
            ["focus indicates no immediate process tensor repair route required"],
        )
    return (
        "repair_process_tensor_inputs",
        "add_evidence_request",
        "Repair process tensor inputs before focus planning",
        [
            "restore_process_history_payload",
            "restore_projection_summary_or_status_view_payload",
            "rerun_advantage_metrics_after_repair",
        ],
        [
            "process_history_required",
            "metrics_status_ready_required_for_nonrepair_focus",
            "read_only_repair_request_only",
        ],
        ["hold_focus_plan_until_metrics_ready"],
        ["focus missing or metrics blocked"],
    )


def compile_qi_process_tensor_focus_plan(*, metrics_source: Mapping[str, Any]) -> QiProcessTensorFocusPlan:
    metrics = _metrics_payload(metrics_source)
    blockers: list[str] = []
    warnings: list[str] = []
    metrics_status = metrics.get("metrics_status")
    advantage_score = _as_float(metrics.get("process_tensor_advantage_score"))
    advantage_level = metrics.get("process_tensor_advantage_level")
    focus = metrics.get("recommended_next_process_focus")

    if not metrics:
        blockers.append("metrics_payload_missing")
    if metrics_status == "QI_PROCESS_TENSOR_ADVANTAGE_BLOCKED":
        blockers.append("advantage_metrics_blocked")
    if focus is None:
        blockers.append("recommended_next_process_focus_missing")
    if advantage_score is None and metrics:
        warnings.append("advantage_score_missing_or_non_numeric")
    if advantage_level is None and metrics:
        warnings.append("advantage_level_missing")

    operator_focus, proposal_kind, proposal_label, actions, preconditions, holds, audit_notes = _proposal_for_focus(str(focus) if focus is not None else None)
    status = "QI_PROCESS_TENSOR_FOCUS_PLAN_READY" if not blockers else "QI_PROCESS_TENSOR_FOCUS_PLAN_BLOCKED"

    return QiProcessTensorFocusPlan(
        plan_version="kuuos_runtime_daemon_qi_process_tensor_focus_plan_v0_1",
        plan_status=status,
        source_metrics_status=str(metrics_status) if metrics_status is not None else None,
        source_advantage_score=advantage_score,
        source_advantage_level=str(advantage_level) if advantage_level is not None else None,
        source_recommended_next_process_focus=str(focus) if focus is not None else None,
        operator_focus=operator_focus,
        proposal_kind=proposal_kind,
        proposal_label=proposal_label,
        proposed_operator_actions=actions,
        required_preconditions=preconditions,
        hold_reasons=holds,
        audit_notes=audit_notes,
        blockers=blockers,
        warnings=warnings,
        focus_plan_only=True,
        read_only=True,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compile KuuOS Qi process tensor focus plan v0.1")
    parser.add_argument("--metrics", type=Path, required=True)
    parser.add_argument("--write", type=Path, default=None)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    source = _read_json(args.metrics)
    result = compile_qi_process_tensor_focus_plan(metrics_source=source)
    if args.write:
        _write_json(args.write, result.to_dict())
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.plan_status == "QI_PROCESS_TENSOR_FOCUS_PLAN_READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
