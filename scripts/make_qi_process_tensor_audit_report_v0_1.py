#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import dataclass, asdict
import json
from pathlib import Path
from typing import Any, Mapping

NON_AUTHORITY_FLAGS = {
    "grants_execution_authority": False,
    "grants_truth_authority": False,
    "grants_final_commitment_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_clinical_authority": False,
    "grants_theorem_authority": False,
    "grants_completed_identity_authority": False,
}

SUMMARY_KEYS = [
    "process_tensor_visible",
    "transition_continuity_visible",
    "memory_continuity_visible",
    "nonmarkov_memory_visible",
    "process_history_length",
    "transition_support_count",
    "memory_support_count",
    "nonmarkov_support_count",
    "missing_process_requirements",
    "process_tensor_reason",
]


@dataclass(frozen=True)
class QiProcessTensorAuditReport:
    report_version: str
    report_status: str
    source_step_trace_path: str | None
    source_state_bundle_path: str | None
    steps_seen: int
    visible_steps: int
    nonmarkov_visible_steps: int
    blocked_steps: int
    waiting_steps: int
    step_summaries: list[dict[str, Any]]
    aggregate_reasons: dict[str, int]
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


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _compact_summary(summary: Mapping[str, Any] | None) -> dict[str, Any]:
    summary = summary or {}
    compact = {key: summary.get(key) for key in SUMMARY_KEYS}
    compact["process_tensor_visible"] = bool(compact.get("process_tensor_visible", False))
    compact["transition_continuity_visible"] = bool(compact.get("transition_continuity_visible", False))
    compact["memory_continuity_visible"] = bool(compact.get("memory_continuity_visible", False))
    compact["nonmarkov_memory_visible"] = bool(compact.get("nonmarkov_memory_visible", False))
    compact["process_history_length"] = int(compact.get("process_history_length") or 0)
    compact["transition_support_count"] = int(compact.get("transition_support_count") or 0)
    compact["memory_support_count"] = int(compact.get("memory_support_count") or 0)
    compact["nonmarkov_support_count"] = int(compact.get("nonmarkov_support_count") or 0)
    compact["missing_process_requirements"] = list(compact.get("missing_process_requirements") or [])
    compact["process_tensor_reason"] = str(compact.get("process_tensor_reason") or "missing_process_tensor_summary")
    compact.update(NON_AUTHORITY_FLAGS)
    return compact


def _steps_from_trace(trace: Any) -> list[Mapping[str, Any]]:
    if isinstance(trace, list):
        return [item for item in trace if isinstance(item, Mapping)]
    return []


def _steps_from_bundle(bundle: Any) -> list[Mapping[str, Any]]:
    if isinstance(bundle, Mapping):
        log = bundle.get("loop_log", [])
        if isinstance(log, list):
            return [item for item in log if isinstance(item, Mapping)]
    return []


def _step_summary(step: Mapping[str, Any], index: int) -> dict[str, Any]:
    summary = _compact_summary(step.get("qi_process_tensor_summary"))
    return {
        "step_index": int(step.get("step_index", index) or index),
        "raw_cycle_id": step.get("raw_cycle_id"),
        "next_cycle_id": step.get("next_cycle_id"),
        "loop_status": step.get("loop_status"),
        "queue_target": step.get("queue_target"),
        "task_queue": step.get("task_queue"),
        "task_status": step.get("task_status") or step.get("task_result_status"),
        "qi_process_tensor_summary": summary,
        **NON_AUTHORITY_FLAGS,
    }


def make_audit_report(
    *,
    step_trace_path: Path | None = None,
    state_bundle_path: Path | None = None,
) -> QiProcessTensorAuditReport:
    steps: list[Mapping[str, Any]] = []
    if step_trace_path is not None:
        steps.extend(_steps_from_trace(load_json(step_trace_path)))
    if not steps and state_bundle_path is not None:
        steps.extend(_steps_from_bundle(load_json(state_bundle_path)))

    step_summaries = [_step_summary(step, index) for index, step in enumerate(steps)]
    visible_steps = 0
    nonmarkov_visible_steps = 0
    blocked_steps = 0
    waiting_steps = 0
    reasons: dict[str, int] = {}

    for item in step_summaries:
        summary = item["qi_process_tensor_summary"]
        if summary.get("process_tensor_visible") is True:
            visible_steps += 1
        if summary.get("nonmarkov_memory_visible") is True:
            nonmarkov_visible_steps += 1
        reason = str(summary.get("process_tensor_reason") or "missing_process_tensor_summary")
        reasons[reason] = reasons.get(reason, 0) + 1
        if reason.startswith("boundary_blocks") or reason.startswith("candidate_nonfinal"):
            blocked_steps += 1
        if summary.get("missing_process_requirements"):
            waiting_steps += 1

    status = "AUDIT_REPORT_READY"
    if not step_summaries:
        status = "AUDIT_REPORT_EMPTY"

    return QiProcessTensorAuditReport(
        report_version="qi_process_tensor_audit_report_v0_1",
        report_status=status,
        source_step_trace_path=str(step_trace_path) if step_trace_path else None,
        source_state_bundle_path=str(state_bundle_path) if state_bundle_path else None,
        steps_seen=len(step_summaries),
        visible_steps=visible_steps,
        nonmarkov_visible_steps=nonmarkov_visible_steps,
        blocked_steps=blocked_steps,
        waiting_steps=waiting_steps,
        step_summaries=step_summaries,
        aggregate_reasons=reasons,
        allowed_projection=["qi_process_tensor_audit_report", "step_summary_projection"],
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Make Qi process tensor audit report v0.1")
    parser.add_argument("--step-trace", type=Path, default=None)
    parser.add_argument("--state-bundle", type=Path, default=None)
    parser.add_argument("--output", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.step_trace is None and args.state_bundle is None:
        print("ERROR: provide --step-trace or --state-bundle")
        return 2
    report = make_audit_report(step_trace_path=args.step_trace, state_bundle_path=args.state_bundle)
    write_json(args.output, report.to_dict())
    print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report.report_status == "AUDIT_REPORT_READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
