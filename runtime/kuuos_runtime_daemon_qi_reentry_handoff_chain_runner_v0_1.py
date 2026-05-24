#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import argparse
import json
from typing import Any

try:
    from runtime.kuuos_runtime_daemon_qi_bounded_reentry_cycle_runner_v0_1 import (
        run_qi_bounded_reentry_cycle,
    )
except ModuleNotFoundError:
    from kuuos_runtime_daemon_qi_bounded_reentry_cycle_runner_v0_1 import (
        run_qi_bounded_reentry_cycle,
    )


@dataclass(frozen=True)
class KuuOSQiReentryHandoffChainResult:
    chain_version: str
    chain_status: str
    daemon_dir: str
    chain_dir: str
    cycles_requested: int
    cycles_run: int
    ticks_invoked: int
    final_raw_state_path: str | None
    final_state_bundle_path: str | None
    final_executor_receipt_path: str | None
    final_health_projection_path: str | None
    final_daemon_health_status: str | None
    final_next_operator_action: str | None
    final_recoverability_status: str | None
    stop_reason: str
    cycle_result_paths: list[str]
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


def run_qi_reentry_handoff_chain(
    *,
    daemon_dir: Path,
    raw_state_path: Path,
    evidence_path: Path,
    chain_dir: Path,
    state_bundle_path: Path | None = None,
    max_cycles: int = 2,
    refresh_before_first: bool = True,
    refresh_after_each: bool = True,
) -> KuuOSQiReentryHandoffChainResult:
    daemon_dir = Path(daemon_dir)
    chain_dir = Path(chain_dir)
    chain_dir.mkdir(parents=True, exist_ok=True)
    max_cycles = max(1, min(int(max_cycles), 5))

    current_raw = Path(raw_state_path)
    current_bundle = Path(state_bundle_path) if state_bundle_path else None
    cycle_paths: list[str] = []
    ticks_invoked = 0
    final_receipt_path: str | None = None
    final_health_path: str | None = None
    final_health_status: str | None = None
    final_next_action: str | None = None
    final_recoverability_status: str | None = None
    stop_reason = "MAX_CYCLES_REACHED"
    granted_any_execution = False

    for index in range(max_cycles):
        out_dir = chain_dir / f"cycle_{index:04d}"
        cycle = run_qi_bounded_reentry_cycle(
            daemon_dir=daemon_dir,
            raw_state_path=current_raw,
            evidence_path=evidence_path,
            output_dir=out_dir,
            state_bundle_path=current_bundle,
            refresh_before=refresh_before_first,
            refresh_after=refresh_after_each,
        )
        cycle_path = out_dir / "qi_bounded_reentry_cycle_result_v0_1.json"
        _write_json(cycle_path, cycle.to_dict())
        cycle_paths.append(str(cycle_path))
        final_receipt_path = cycle.executor_receipt_path
        final_health_path = cycle.post_health_projection_path or cycle.pre_health_projection_path
        final_health_status = cycle.post_daemon_health_status or cycle.pre_daemon_health_status
        final_next_action = cycle.post_next_operator_action or cycle.pre_next_operator_action
        final_recoverability_status = cycle.post_recoverability_status or cycle.pre_recoverability_status
        if cycle.tick_invoked:
            ticks_invoked += 1
        if cycle.grants_execution_authority:
            granted_any_execution = True
        if not cycle.handoff_available:
            stop_reason = cycle.cycle_reason or "HANDOFF_NOT_AVAILABLE"
            break
        current_raw = Path(cycle.handoff_raw_state_path)
        current_bundle = Path(cycle.handoff_state_bundle_path) if cycle.handoff_state_bundle_path else None
    else:
        stop_reason = "MAX_CYCLES_REACHED"

    chain_status = "QI_REENTRY_HANDOFF_CHAIN_COMPLETED"
    if ticks_invoked == 0:
        chain_status = "QI_REENTRY_HANDOFF_CHAIN_NOT_INVOKED"
    elif stop_reason != "MAX_CYCLES_REACHED":
        chain_status = "QI_REENTRY_HANDOFF_CHAIN_STOPPED"

    return KuuOSQiReentryHandoffChainResult(
        chain_version="kuuos_runtime_daemon_qi_reentry_handoff_chain_runner_v0_1",
        chain_status=chain_status,
        daemon_dir=str(daemon_dir),
        chain_dir=str(chain_dir),
        cycles_requested=max_cycles,
        cycles_run=len(cycle_paths),
        ticks_invoked=ticks_invoked,
        final_raw_state_path=str(current_raw) if ticks_invoked else None,
        final_state_bundle_path=str(current_bundle) if current_bundle and ticks_invoked else None,
        final_executor_receipt_path=final_receipt_path,
        final_health_projection_path=final_health_path,
        final_daemon_health_status=final_health_status,
        final_next_operator_action=final_next_action,
        final_recoverability_status=final_recoverability_status,
        stop_reason=stop_reason,
        cycle_result_paths=cycle_paths,
        grants_execution_authority=granted_any_execution,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run KuuOS Qi reentry handoff chain v0.1")
    parser.add_argument("--daemon-dir", type=Path, required=True)
    parser.add_argument("--raw-state", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--chain-dir", type=Path, required=True)
    parser.add_argument("--state-bundle", type=Path, default=None)
    parser.add_argument("--max-cycles", type=int, default=2)
    parser.add_argument("--no-refresh-before-first", action="store_true")
    parser.add_argument("--no-refresh-after-each", action="store_true")
    parser.add_argument("--write-summary", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = run_qi_reentry_handoff_chain(
        daemon_dir=args.daemon_dir,
        raw_state_path=args.raw_state,
        evidence_path=args.evidence,
        chain_dir=args.chain_dir,
        state_bundle_path=args.state_bundle,
        max_cycles=args.max_cycles,
        refresh_before_first=not args.no_refresh_before_first,
        refresh_after_each=not args.no_refresh_after_each,
    )
    if args.write_summary:
        _write_json(args.chain_dir / "qi_reentry_handoff_chain_result_v0_1.json", result.to_dict())
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
