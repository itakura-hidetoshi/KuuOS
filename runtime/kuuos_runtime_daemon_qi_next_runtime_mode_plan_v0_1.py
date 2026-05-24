#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import argparse
import json
from typing import Any, Mapping


@dataclass(frozen=True)
class KuuOSQiNextRuntimeModePlan:
    plan_version: str
    plan_status: str
    plan_decision: str
    plan_reason: str
    source_runtime_mode: str | None
    next_tick_preparation: str
    required_pre_tick_actions: list[str]
    forbidden_actions: list[str]
    carry_forward_blockers: list[str]
    carry_forward_warnings: list[str]
    carry_forward_positive_signals: list[str]
    plan_packet: dict[str, Any]
    source_operational_summary_path: str | None
    plan_only: bool
    read_only: bool
    nonexecuting: bool
    grants_next_tick_execution_authority: bool = False
    grants_execution_authority: bool = False
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


def _s(payload: Mapping[str, Any], key: str) -> str | None:
    value = payload.get(key)
    return str(value) if value is not None else None


def _lst(payload: Mapping[str, Any], key: str) -> list[str]:
    value = payload.get(key)
    return [str(item) for item in value] if isinstance(value, list) else []


FORBIDDEN_ACTIONS = [
    "execute_next_tick_without_independent_runner",
    "mutate_policy_flow",
    "update_belief_state",
    "overwrite_memory",
    "grant_authority",
    "treat_shadow_result_as_execution_permission",
]


def compile_qi_next_runtime_mode_plan(
    *,
    operational_summary: Mapping[str, Any] | None = None,
    source_operational_summary_path: Path | None = None,
) -> KuuOSQiNextRuntimeModePlan:
    summary = operational_summary or {}
    mode = _s(summary, "recommended_next_runtime_mode")
    reason = _s(summary, "recommended_next_reason") or "summary_reason_missing"
    blockers = _lst(summary, "operational_blockers")
    warnings = _lst(summary, "operational_warnings")
    positives = _lst(summary, "operational_positive_signals")

    if not summary:
        decision = "QI_NEXT_RUNTIME_MODE_PLAN_BLOCKED"
        plan_reason = "operational_summary_missing"
        preparation = "hold_reobserve"
        required = ["recover_operational_summary", "reobserve_before_next_tick"]
    elif mode == "HOLD_REOBSERVE":
        decision = "QI_NEXT_RUNTIME_MODE_PLAN_PREPARED"
        plan_reason = reason
        preparation = "hold_reobserve"
        required = ["hold_next_tick", "prepare_reobservation", "preserve_blockers"]
    elif mode == "REOBSERVE":
        decision = "QI_NEXT_RUNTIME_MODE_PLAN_PREPARED"
        plan_reason = reason
        preparation = "prepare_observation"
        required = ["prepare_observation_packet", "collect_missing_observation", "do_not_execute_tick"]
    elif mode == "COMPACT_TRACE":
        decision = "QI_NEXT_RUNTIME_MODE_PLAN_PREPARED"
        plan_reason = reason
        preparation = "prepare_compaction"
        required = ["prepare_trace_compaction", "preserve_blocker_visibility", "revalidate_after_compaction"]
    elif mode == "SHADOW_READY_FOR_POLICY_FLOW_REVIEW":
        decision = "QI_NEXT_RUNTIME_MODE_PLAN_PREPARED"
        plan_reason = reason
        preparation = "prepare_shadow_review"
        required = ["prepare_policy_flow_review_packet", "keep_shadow_only", "do_not_mutate_policy"]
    elif mode == "BOUNDED_REENTRY_REVIEW":
        decision = "QI_NEXT_RUNTIME_MODE_PLAN_PREPARED"
        plan_reason = reason
        preparation = "prepare_bounded_reentry_review"
        required = ["check_reentry_cap", "check_invocation_boundary", "do_not_execute_without_runner"]
    else:
        decision = "QI_NEXT_RUNTIME_MODE_PLAN_PREPARED"
        plan_reason = reason
        preparation = "observe_only"
        required = ["observe_only", "keep_daemon_idle", "await_next_valid_summary"]

    packet = {
        "next_tick_preparation": preparation,
        "required_pre_tick_actions": required,
        "forbidden_actions": FORBIDDEN_ACTIONS,
        "source_runtime_mode": mode,
        "source_reason": reason,
        "blockers": blockers,
        "warnings": warnings,
        "positive_signals": positives,
        "plan_only": True,
        "read_only": True,
        "nonexecuting": True,
        "source": "qi_next_runtime_mode_plan_v0_1",
    }

    return KuuOSQiNextRuntimeModePlan(
        plan_version="kuuos_runtime_daemon_qi_next_runtime_mode_plan_v0_1",
        plan_status="QI_NEXT_RUNTIME_MODE_PLAN_COMPILED",
        plan_decision=decision,
        plan_reason=plan_reason,
        source_runtime_mode=mode,
        next_tick_preparation=preparation,
        required_pre_tick_actions=required,
        forbidden_actions=FORBIDDEN_ACTIONS,
        carry_forward_blockers=blockers,
        carry_forward_warnings=warnings,
        carry_forward_positive_signals=positives,
        plan_packet=packet,
        source_operational_summary_path=str(source_operational_summary_path) if source_operational_summary_path else None,
        plan_only=True,
        read_only=True,
        nonexecuting=True,
    )


def read_and_compile_qi_next_runtime_mode_plan(dispatch_dir: Path) -> KuuOSQiNextRuntimeModePlan:
    dispatch_dir = Path(dispatch_dir)
    summary_path = dispatch_dir / "qi_routed_cycle_operational_summary_v0_1.json"
    return compile_qi_next_runtime_mode_plan(
        operational_summary=_read_json(summary_path),
        source_operational_summary_path=summary_path if summary_path.is_file() else None,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compile KuuOS Qi next runtime mode plan v0.1")
    parser.add_argument("--dispatch-dir", type=Path, required=True)
    parser.add_argument("--write", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    plan = read_and_compile_qi_next_runtime_mode_plan(args.dispatch_dir)
    if args.write:
        _write_json(args.dispatch_dir / "qi_next_runtime_mode_plan_v0_1.json", plan.to_dict())
    print(json.dumps(plan.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
