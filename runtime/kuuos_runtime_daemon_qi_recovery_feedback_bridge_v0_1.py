#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import argparse
import json
from typing import Any, Mapping


@dataclass(frozen=True)
class KuuOSQiRecoveryFeedback:
    bridge_version: str
    bridge_status: str
    feedback_signal: str
    feedback_reason: str
    policy_adjustment_hint: str
    active_inference_hint: str
    observation_feedback: str
    compaction_feedback: str
    reentry_feedback: str
    safety_feedback: str
    route_decision: str | None
    next_outer_action: str | None
    dispatcher_status: str | None
    action_invoked: bool
    invoked_action: str | None
    reentry_cycles_run: int
    reentry_ticks_invoked: int
    final_raw_state_path: str | None
    final_state_bundle_path: str | None
    feedback_priority: str
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


def _i(payload: Mapping[str, Any], key: str) -> int:
    try:
        return int(payload.get(key, 0))
    except (TypeError, ValueError):
        return 0


def compile_qi_recovery_feedback(
    *,
    routed_cycle_result: Mapping[str, Any] | None = None,
    dispatch_result: Mapping[str, Any] | None = None,
    route_result: Mapping[str, Any] | None = None,
) -> KuuOSQiRecoveryFeedback:
    routed = routed_cycle_result or {}
    dispatch = dispatch_result or {}
    route = route_result or {}

    route_decision = _s(route, "route_decision") or _s(routed, "route_decision") or _s(dispatch, "route_decision")
    next_action = _s(route, "next_outer_action") or _s(routed, "next_outer_action") or _s(dispatch, "next_outer_action")
    dispatcher_status = _s(dispatch, "dispatcher_status") or _s(routed, "dispatcher_status")
    action_invoked = bool(dispatch.get("action_invoked", routed.get("action_invoked", False)))
    invoked_action = _s(dispatch, "invoked_action") or _s(routed, "invoked_action")
    reentry_cycles = _i(dispatch, "reentry_cycles_run") or _i(routed, "reentry_cycles_run")
    reentry_ticks = _i(dispatch, "reentry_ticks_invoked") or _i(routed, "reentry_ticks_invoked")
    final_raw = _s(dispatch, "final_raw_state_path") or _s(routed, "final_raw_state_path")
    final_bundle = _s(dispatch, "final_state_bundle_path") or _s(routed, "final_state_bundle_path")
    dispatch_reason = _s(dispatch, "dispatch_reason") or _s(routed, "runner_reason") or "not_available"

    feedback_signal = "QI_FEEDBACK_NO_ACTION"
    reason = "no_actionable_route"
    policy_hint = "keep_policy_flow_stable"
    active_hint = "maintain_current_precision"
    observation_feedback = "no_observation_debt"
    compaction_feedback = "no_compaction_debt"
    reentry_feedback = "no_reentry_performed"
    safety_feedback = "safe_non_authoritative_feedback"
    priority = "low"

    if next_action == "hold" or route_decision == "ROUTE_HOLD":
        feedback_signal = "QI_FEEDBACK_HOLD_REQUIRED"
        reason = "hold_or_unsafe_recovery_route"
        policy_hint = "raise_safety_barrier_and_request_review"
        active_hint = "increase_uncertainty_and_reduce_action_precision"
        safety_feedback = "hold_required"
        priority = "critical"
    elif next_action in {"observe", "reobserve"}:
        feedback_signal = "QI_FEEDBACK_OBSERVATION_REQUIRED"
        reason = "observation_or_reobservation_route"
        policy_hint = "prefer_information_gain_over_reentry"
        active_hint = "increase_epistemic_value_weight"
        observation_feedback = f"{next_action}_required"
        priority = "high"
    elif next_action in {"compact_trace", "summarize_trace"}:
        feedback_signal = "QI_FEEDBACK_COMPACTION_REQUIRED"
        reason = "trace_compaction_route"
        policy_hint = "reduce_trace_load_before_more_reentry"
        active_hint = "limit_planning_horizon_until_trace_compacted"
        compaction_feedback = f"{next_action}_required"
        priority = "medium"
    elif next_action == "managed_reentry_chain" and action_invoked and reentry_ticks > 0:
        feedback_signal = "QI_FEEDBACK_REENTRY_PERFORMED"
        reason = dispatch_reason
        policy_hint = "incorporate_reentry_result_as_candidate_rollout_feedback"
        active_hint = "update_expected_free_energy_landscape_candidate_only"
        reentry_feedback = "bounded_reentry_invoked"
        priority = "high"
    elif next_action == "managed_reentry_chain" and not action_invoked:
        feedback_signal = "QI_FEEDBACK_REENTRY_BLOCKED"
        reason = dispatch_reason
        policy_hint = "do_not_escalate_reentry_without_missing_inputs"
        active_hint = "maintain_hold_until_reentry_preconditions_met"
        reentry_feedback = "reentry_route_blocked"
        priority = "medium"

    return KuuOSQiRecoveryFeedback(
        bridge_version="kuuos_runtime_daemon_qi_recovery_feedback_bridge_v0_1",
        bridge_status="QI_RECOVERY_FEEDBACK_COMPILED",
        feedback_signal=feedback_signal,
        feedback_reason=reason,
        policy_adjustment_hint=policy_hint,
        active_inference_hint=active_hint,
        observation_feedback=observation_feedback,
        compaction_feedback=compaction_feedback,
        reentry_feedback=reentry_feedback,
        safety_feedback=safety_feedback,
        route_decision=route_decision,
        next_outer_action=next_action,
        dispatcher_status=dispatcher_status,
        action_invoked=action_invoked,
        invoked_action=invoked_action,
        reentry_cycles_run=reentry_cycles,
        reentry_ticks_invoked=reentry_ticks,
        final_raw_state_path=final_raw,
        final_state_bundle_path=final_bundle,
        feedback_priority=priority,
    )


def read_and_compile_qi_recovery_feedback(dispatch_dir: Path) -> KuuOSQiRecoveryFeedback:
    dispatch_dir = Path(dispatch_dir)
    return compile_qi_recovery_feedback(
        routed_cycle_result=_read_json(dispatch_dir / "qi_routed_daemon_cycle_result_v0_1.json"),
        dispatch_result=_read_json(dispatch_dir / "qi_runtime_output_action_dispatch_result_v0_1.json"),
        route_result=_read_json(dispatch_dir / "qi_runtime_output_action_route_v0_1.json"),
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compile KuuOS Qi recovery feedback v0.1")
    parser.add_argument("--dispatch-dir", type=Path, required=True)
    parser.add_argument("--write", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    feedback = read_and_compile_qi_recovery_feedback(args.dispatch_dir)
    if args.write:
        _write_json(args.dispatch_dir / "qi_recovery_feedback_v0_1.json", feedback.to_dict())
    print(json.dumps(feedback.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
