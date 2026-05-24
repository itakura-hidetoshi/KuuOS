#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import argparse
import json
from typing import Any

try:
    from runtime.kuuos_runtime_daemon_qi_runtime_output_action_router_v0_1 import (
        read_and_route_qi_runtime_output_surface,
    )
    from runtime.kuuos_runtime_daemon_qi_managed_reentry_chain_runner_v0_1 import (
        run_qi_managed_reentry_chain,
    )
except ModuleNotFoundError:
    from kuuos_runtime_daemon_qi_runtime_output_action_router_v0_1 import (
        read_and_route_qi_runtime_output_surface,
    )
    from kuuos_runtime_daemon_qi_managed_reentry_chain_runner_v0_1 import (
        run_qi_managed_reentry_chain,
    )


@dataclass(frozen=True)
class KuuOSQiRuntimeOutputActionDispatchResult:
    dispatcher_version: str
    dispatcher_status: str
    daemon_dir: str
    dispatch_dir: str
    route_decision: str
    route_reason: str
    next_outer_action: str
    route_priority: str
    route_path: str
    action_invoked: bool
    invoked_action: str | None
    managed_chain_result_path: str | None
    managed_chain_status: str | None
    reentry_cycles_run: int
    reentry_ticks_invoked: int
    final_raw_state_path: str | None
    final_state_bundle_path: str | None
    dispatch_reason: str
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


def dispatch_qi_runtime_output_action(
    *,
    daemon_dir: Path,
    dispatch_dir: Path,
    raw_state_path: Path | None = None,
    evidence_path: Path | None = None,
    state_bundle_path: Path | None = None,
    requested_max_reentry_cycles: int = 2,
    refresh_before_first: bool = True,
    refresh_after_each: bool = True,
) -> KuuOSQiRuntimeOutputActionDispatchResult:
    daemon_dir = Path(daemon_dir)
    dispatch_dir = Path(dispatch_dir)
    dispatch_dir.mkdir(parents=True, exist_ok=True)

    route = read_and_route_qi_runtime_output_surface(daemon_dir)
    route_path = dispatch_dir / "qi_runtime_output_action_route_v0_1.json"
    _write_json(route_path, route.to_dict())

    if route.next_outer_action == "managed_reentry_chain":
        if raw_state_path is None or evidence_path is None:
            return KuuOSQiRuntimeOutputActionDispatchResult(
                dispatcher_version="kuuos_runtime_daemon_qi_runtime_output_action_dispatcher_v0_1",
                dispatcher_status="QI_RUNTIME_OUTPUT_ACTION_NOT_DISPATCHED",
                daemon_dir=str(daemon_dir),
                dispatch_dir=str(dispatch_dir),
                route_decision=route.route_decision,
                route_reason=route.route_reason,
                next_outer_action=route.next_outer_action,
                route_priority=route.route_priority,
                route_path=str(route_path),
                action_invoked=False,
                invoked_action=None,
                managed_chain_result_path=None,
                managed_chain_status=None,
                reentry_cycles_run=0,
                reentry_ticks_invoked=0,
                final_raw_state_path=None,
                final_state_bundle_path=None,
                dispatch_reason="managed_reentry_requires_raw_state_and_evidence",
                grants_execution_authority=False,
            )
        chain = run_qi_managed_reentry_chain(
            daemon_dir=daemon_dir,
            raw_state_path=Path(raw_state_path),
            evidence_path=Path(evidence_path),
            chain_dir=dispatch_dir / "managed_reentry_chain",
            state_bundle_path=Path(state_bundle_path) if state_bundle_path else None,
            requested_max_cycles=requested_max_reentry_cycles,
            refresh_before_first=refresh_before_first,
            refresh_after_each=refresh_after_each,
        )
        chain_path = dispatch_dir / "qi_managed_reentry_chain_result_v0_1.json"
        _write_json(chain_path, chain.to_dict())
        return KuuOSQiRuntimeOutputActionDispatchResult(
            dispatcher_version="kuuos_runtime_daemon_qi_runtime_output_action_dispatcher_v0_1",
            dispatcher_status="QI_RUNTIME_OUTPUT_ACTION_DISPATCHED",
            daemon_dir=str(daemon_dir),
            dispatch_dir=str(dispatch_dir),
            route_decision=route.route_decision,
            route_reason=route.route_reason,
            next_outer_action=route.next_outer_action,
            route_priority=route.route_priority,
            route_path=str(route_path),
            action_invoked=True,
            invoked_action="managed_reentry_chain",
            managed_chain_result_path=str(chain_path),
            managed_chain_status=chain.managed_runner_status,
            reentry_cycles_run=chain.cycles_run,
            reentry_ticks_invoked=chain.ticks_invoked,
            final_raw_state_path=chain.final_raw_state_path,
            final_state_bundle_path=chain.final_state_bundle_path,
            dispatch_reason=chain.managed_stop_reason,
            grants_execution_authority=chain.grants_execution_authority,
        )

    return KuuOSQiRuntimeOutputActionDispatchResult(
        dispatcher_version="kuuos_runtime_daemon_qi_runtime_output_action_dispatcher_v0_1",
        dispatcher_status="QI_RUNTIME_OUTPUT_ACTION_NOT_DISPATCHED",
        daemon_dir=str(daemon_dir),
        dispatch_dir=str(dispatch_dir),
        route_decision=route.route_decision,
        route_reason=route.route_reason,
        next_outer_action=route.next_outer_action,
        route_priority=route.route_priority,
        route_path=str(route_path),
        action_invoked=False,
        invoked_action=None,
        managed_chain_result_path=None,
        managed_chain_status=None,
        reentry_cycles_run=0,
        reentry_ticks_invoked=0,
        final_raw_state_path=None,
        final_state_bundle_path=None,
        dispatch_reason="route_is_non_executing_or_not_supported_by_dispatcher",
        grants_execution_authority=False,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Dispatch KuuOS Qi runtime output action v0.1")
    parser.add_argument("--daemon-dir", type=Path, required=True)
    parser.add_argument("--dispatch-dir", type=Path, required=True)
    parser.add_argument("--raw-state", type=Path, default=None)
    parser.add_argument("--evidence", type=Path, default=None)
    parser.add_argument("--state-bundle", type=Path, default=None)
    parser.add_argument("--requested-max-reentry-cycles", type=int, default=2)
    parser.add_argument("--no-refresh-before-first", action="store_true")
    parser.add_argument("--no-refresh-after-each", action="store_true")
    parser.add_argument("--write-summary", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = dispatch_qi_runtime_output_action(
        daemon_dir=args.daemon_dir,
        dispatch_dir=args.dispatch_dir,
        raw_state_path=args.raw_state,
        evidence_path=args.evidence,
        state_bundle_path=args.state_bundle,
        requested_max_reentry_cycles=args.requested_max_reentry_cycles,
        refresh_before_first=not args.no_refresh_before_first,
        refresh_after_each=not args.no_refresh_after_each,
    )
    if args.write_summary:
        _write_json(args.dispatch_dir / "qi_runtime_output_action_dispatch_result_v0_1.json", result.to_dict())
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
