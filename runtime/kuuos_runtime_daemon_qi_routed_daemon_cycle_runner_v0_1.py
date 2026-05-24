#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import argparse
import json
from typing import Any

try:
    from runtime.kuuos_runtime_daemon_v0_1 import run_runtime_daemon
    from runtime.kuuos_runtime_daemon_qi_runtime_output_surface_v0_1 import compile_qi_runtime_output_surface
    from runtime.kuuos_runtime_daemon_qi_runtime_output_action_router_v0_1 import route_qi_runtime_output_surface
    from runtime.kuuos_runtime_daemon_qi_runtime_output_action_dispatcher_v0_1 import dispatch_qi_runtime_output_action
    from runtime.kuuos_runtime_daemon_qi_recovery_feedback_bridge_v0_1 import compile_qi_recovery_feedback
    from runtime.kuuos_runtime_daemon_qi_policy_feedback_surface_v0_1 import compile_qi_policy_feedback_surface
    from runtime.kuuos_runtime_daemon_qi_policy_feedback_candidate_adapter_v0_1 import compile_qi_policy_feedback_candidate_adapter
    from runtime.kuuos_runtime_daemon_qi_policy_candidate_admission_gate_v0_1 import compile_qi_policy_candidate_admission
    from runtime.kuuos_runtime_daemon_qi_admitted_policy_candidate_handoff_v0_1 import compile_qi_admitted_policy_candidate_handoff
    from runtime.kuuos_runtime_daemon_qi_policy_flow_handoff_receiver_v0_1 import compile_qi_policy_flow_handoff_receiver
    from runtime.kuuos_runtime_daemon_qi_policy_flow_candidate_inbox_v0_1 import compile_qi_policy_flow_candidate_inbox
except ModuleNotFoundError:
    from kuuos_runtime_daemon_v0_1 import run_runtime_daemon
    from kuuos_runtime_daemon_qi_runtime_output_surface_v0_1 import compile_qi_runtime_output_surface
    from kuuos_runtime_daemon_qi_runtime_output_action_router_v0_1 import route_qi_runtime_output_surface
    from kuuos_runtime_daemon_qi_runtime_output_action_dispatcher_v0_1 import dispatch_qi_runtime_output_action
    from kuuos_runtime_daemon_qi_recovery_feedback_bridge_v0_1 import compile_qi_recovery_feedback
    from kuuos_runtime_daemon_qi_policy_feedback_surface_v0_1 import compile_qi_policy_feedback_surface
    from kuuos_runtime_daemon_qi_policy_feedback_candidate_adapter_v0_1 import compile_qi_policy_feedback_candidate_adapter
    from kuuos_runtime_daemon_qi_policy_candidate_admission_gate_v0_1 import compile_qi_policy_candidate_admission
    from kuuos_runtime_daemon_qi_admitted_policy_candidate_handoff_v0_1 import compile_qi_admitted_policy_candidate_handoff
    from kuuos_runtime_daemon_qi_policy_flow_handoff_receiver_v0_1 import compile_qi_policy_flow_handoff_receiver
    from kuuos_runtime_daemon_qi_policy_flow_candidate_inbox_v0_1 import compile_qi_policy_flow_candidate_inbox


@dataclass(frozen=True)
class KuuOSQiRoutedDaemonCycleResult:
    runner_version: str
    runner_status: str
    daemon_dir: str
    dispatch_dir: str
    daemon_result_path: str
    surface_path: str
    route_path: str
    dispatch_result_path: str
    feedback_path: str
    policy_feedback_surface_path: str
    policy_candidate_adapter_path: str
    policy_candidate_admission_path: str
    admitted_policy_candidate_handoff_path: str
    policy_flow_handoff_receiver_path: str
    policy_flow_candidate_inbox_path: str
    daemon_status: str
    daemon_stop_reason: str
    daemon_ticks_run: int
    route_decision: str
    next_outer_action: str
    route_priority: str
    dispatcher_status: str
    action_invoked: bool
    invoked_action: str | None
    reentry_cycles_run: int
    reentry_ticks_invoked: int
    feedback_signal: str
    feedback_priority: str
    policy_adjustment_hint: str
    active_inference_hint: str
    policy_feedback_class: str
    policy_flow_candidate_signal: str
    active_inference_candidate_signal: str
    candidate_adjustment_class: str
    recommended_candidate_action: str
    candidate_priority: str
    admission_decision: str
    admission_reason: str
    admitted_candidate_action: str | None
    handoff_decision: str
    handoff_reason: str
    policy_flow_handoff_ready: bool
    policy_flow_intake_decision: str
    policy_flow_candidate_available: bool
    policy_flow_candidate_action: str | None
    policy_flow_inbox_decision: str
    policy_flow_inbox_queued: bool
    policy_flow_inbox_action: str | None
    final_raw_state_path: str | None
    final_state_bundle_path: str | None
    runner_reason: str
    grants_execution_authority: bool
    grants_truth_authority: bool = False
    grants_final_commitment_authority: bool = False
    grants_memory_overwrite_authority: bool = False
    grants_clinical_authority: bool = False
    grants_theorem_authority: bool = False
    grants_completed_identity_authority: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_qi_routed_daemon_cycle(
    *,
    raw_state_path: Path,
    evidence_path: Path,
    daemon_dir: Path,
    dispatch_dir: Path,
    max_daemon_ticks: int = 1,
    max_steps_per_tick: int = 1,
    sleep_seconds: float = 0.0,
    state_bundle_path: Path | None = None,
    requested_max_reentry_cycles: int = 2,
    refresh_before_first_reentry: bool = True,
    refresh_after_each_reentry: bool = True,
) -> KuuOSQiRoutedDaemonCycleResult:
    daemon_dir = Path(daemon_dir)
    dispatch_dir = Path(dispatch_dir)
    dispatch_dir.mkdir(parents=True, exist_ok=True)

    daemon_result = run_runtime_daemon(
        raw_state_path=Path(raw_state_path),
        evidence_path=Path(evidence_path),
        daemon_dir=daemon_dir,
        max_ticks=max_daemon_ticks,
        max_steps_per_tick=max_steps_per_tick,
        sleep_seconds=sleep_seconds,
        state_bundle_path=state_bundle_path,
    )
    daemon_result_path = daemon_dir / "daemon_result_v0_1.json"

    surface = compile_qi_runtime_output_surface(daemon_dir)
    surface_path = daemon_dir / "daemon_qi_runtime_output_surface_v0_1.json"
    _write_json(surface_path, surface.to_dict())

    route = route_qi_runtime_output_surface(surface=surface.to_dict(), daemon_dir=daemon_dir, surface_path=surface_path)
    route_path = dispatch_dir / "qi_runtime_output_action_route_v0_1.json"
    _write_json(route_path, route.to_dict())

    chain_raw = Path(daemon_result.final_raw_state_path) if daemon_result.final_raw_state_path else Path(raw_state_path)
    chain_bundle = Path(daemon_result.final_state_bundle_path) if daemon_result.final_state_bundle_path else state_bundle_path
    dispatch = dispatch_qi_runtime_output_action(
        daemon_dir=daemon_dir,
        dispatch_dir=dispatch_dir,
        raw_state_path=chain_raw,
        evidence_path=Path(evidence_path),
        state_bundle_path=chain_bundle,
        requested_max_reentry_cycles=requested_max_reentry_cycles,
        refresh_before_first=refresh_before_first_reentry,
        refresh_after_each=refresh_after_each_reentry,
    )
    dispatch_path = dispatch_dir / "qi_runtime_output_action_dispatch_result_v0_1.json"
    _write_json(dispatch_path, dispatch.to_dict())

    feedback = compile_qi_recovery_feedback(
        routed_cycle_result={},
        dispatch_result=dispatch.to_dict(),
        route_result=route.to_dict(),
    )
    feedback_path = dispatch_dir / "qi_recovery_feedback_v0_1.json"
    _write_json(feedback_path, feedback.to_dict())

    policy_feedback = compile_qi_policy_feedback_surface(
        recovery_feedback=feedback.to_dict(),
        source_feedback_path=feedback_path,
    )
    policy_feedback_path = dispatch_dir / "qi_policy_feedback_surface_v0_1.json"
    _write_json(policy_feedback_path, policy_feedback.to_dict())

    candidate_adapter = compile_qi_policy_feedback_candidate_adapter(
        policy_feedback_surface=policy_feedback.to_dict(),
        source_policy_feedback_surface_path=policy_feedback_path,
    )
    candidate_adapter_path = dispatch_dir / "qi_policy_feedback_candidate_adapter_v0_1.json"
    _write_json(candidate_adapter_path, candidate_adapter.to_dict())

    admission = compile_qi_policy_candidate_admission(
        candidate_adapter=candidate_adapter.to_dict(),
        source_candidate_adapter_path=candidate_adapter_path,
    )
    admission_path = dispatch_dir / "qi_policy_candidate_admission_gate_v0_1.json"
    _write_json(admission_path, admission.to_dict())

    handoff = compile_qi_admitted_policy_candidate_handoff(
        candidate_adapter=candidate_adapter.to_dict(),
        admission_gate=admission.to_dict(),
        source_candidate_adapter_path=candidate_adapter_path,
        source_admission_gate_path=admission_path,
    )
    handoff_path = dispatch_dir / "qi_admitted_policy_candidate_handoff_v0_1.json"
    _write_json(handoff_path, handoff.to_dict())

    receiver = compile_qi_policy_flow_handoff_receiver(
        admitted_policy_candidate_handoff=handoff.to_dict(),
        source_handoff_path=handoff_path,
    )
    receiver_path = dispatch_dir / "qi_policy_flow_handoff_receiver_v0_1.json"
    _write_json(receiver_path, receiver.to_dict())

    inbox = compile_qi_policy_flow_candidate_inbox(
        receiver_result=receiver.to_dict(),
        source_receiver_path=receiver_path,
    )
    inbox_path = dispatch_dir / "qi_policy_flow_candidate_inbox_v0_1.json"
    _write_json(inbox_path, inbox.to_dict())

    final_raw = dispatch.final_raw_state_path or daemon_result.final_raw_state_path
    final_bundle = dispatch.final_state_bundle_path or daemon_result.final_state_bundle_path
    runner_status = "QI_ROUTED_DAEMON_CYCLE_DISPATCHED" if dispatch.action_invoked else "QI_ROUTED_DAEMON_CYCLE_ROUTED_NON_EXECUTING"

    return KuuOSQiRoutedDaemonCycleResult(
        runner_version="kuuos_runtime_daemon_qi_routed_daemon_cycle_runner_v0_1",
        runner_status=runner_status,
        daemon_dir=str(daemon_dir),
        dispatch_dir=str(dispatch_dir),
        daemon_result_path=str(daemon_result_path),
        surface_path=str(surface_path),
        route_path=str(route_path),
        dispatch_result_path=str(dispatch_path),
        feedback_path=str(feedback_path),
        policy_feedback_surface_path=str(policy_feedback_path),
        policy_candidate_adapter_path=str(candidate_adapter_path),
        policy_candidate_admission_path=str(admission_path),
        admitted_policy_candidate_handoff_path=str(handoff_path),
        policy_flow_handoff_receiver_path=str(receiver_path),
        policy_flow_candidate_inbox_path=str(inbox_path),
        daemon_status=daemon_result.daemon_status,
        daemon_stop_reason=daemon_result.stop_reason,
        daemon_ticks_run=daemon_result.ticks_run,
        route_decision=route.route_decision,
        next_outer_action=route.next_outer_action,
        route_priority=route.route_priority,
        dispatcher_status=dispatch.dispatcher_status,
        action_invoked=dispatch.action_invoked,
        invoked_action=dispatch.invoked_action,
        reentry_cycles_run=dispatch.reentry_cycles_run,
        reentry_ticks_invoked=dispatch.reentry_ticks_invoked,
        feedback_signal=feedback.feedback_signal,
        feedback_priority=feedback.feedback_priority,
        policy_adjustment_hint=feedback.policy_adjustment_hint,
        active_inference_hint=feedback.active_inference_hint,
        policy_feedback_class=policy_feedback.policy_feedback_class,
        policy_flow_candidate_signal=policy_feedback.policy_flow_candidate_signal,
        active_inference_candidate_signal=policy_feedback.active_inference_candidate_signal,
        candidate_adjustment_class=candidate_adapter.candidate_adjustment_class,
        recommended_candidate_action=candidate_adapter.recommended_candidate_action,
        candidate_priority=candidate_adapter.candidate_priority,
        admission_decision=admission.admission_decision,
        admission_reason=admission.admission_reason,
        admitted_candidate_action=admission.admitted_candidate_action,
        handoff_decision=handoff.handoff_decision,
        handoff_reason=handoff.handoff_reason,
        policy_flow_handoff_ready=handoff.handoff_decision == "QI_POLICY_CANDIDATE_HANDOFF_READY",
        policy_flow_intake_decision=receiver.intake_decision,
        policy_flow_candidate_available=receiver.policy_flow_candidate_available,
        policy_flow_candidate_action=receiver.policy_flow_candidate_action,
        policy_flow_inbox_decision=inbox.inbox_decision,
        policy_flow_inbox_queued=inbox.queued_candidate_available,
        policy_flow_inbox_action=inbox.queued_candidate_action,
        final_raw_state_path=final_raw,
        final_state_bundle_path=final_bundle,
        runner_reason=dispatch.dispatch_reason,
        grants_execution_authority=dispatch.grants_execution_authority,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run KuuOS Qi routed daemon cycle v0.1")
    parser.add_argument("--raw-state", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--daemon-dir", type=Path, required=True)
    parser.add_argument("--dispatch-dir", type=Path, required=True)
    parser.add_argument("--max-daemon-ticks", type=int, default=1)
    parser.add_argument("--max-steps-per-tick", type=int, default=1)
    parser.add_argument("--sleep-seconds", type=float, default=0.0)
    parser.add_argument("--state-bundle", type=Path, default=None)
    parser.add_argument("--requested-max-reentry-cycles", type=int, default=2)
    parser.add_argument("--no-refresh-before-first-reentry", action="store_true")
    parser.add_argument("--no-refresh-after-each-reentry", action="store_true")
    parser.add_argument("--write-summary", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = run_qi_routed_daemon_cycle(
        raw_state_path=args.raw_state,
        evidence_path=args.evidence,
        daemon_dir=args.daemon_dir,
        dispatch_dir=args.dispatch_dir,
        max_daemon_ticks=args.max_daemon_ticks,
        max_steps_per_tick=args.max_steps_per_tick,
        sleep_seconds=args.sleep_seconds,
        state_bundle_path=args.state_bundle,
        requested_max_reentry_cycles=args.requested_max_reentry_cycles,
        refresh_before_first_reentry=not args.no_refresh_before_first_reentry,
        refresh_after_each_reentry=not args.no_refresh_after_each_reentry,
    )
    if args.write_summary:
        _write_json(args.dispatch_dir / "qi_routed_daemon_cycle_result_v0_1.json", result.to_dict())
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
