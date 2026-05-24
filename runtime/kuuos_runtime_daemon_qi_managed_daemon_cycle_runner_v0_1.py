#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import argparse
import json
from typing import Any

try:
    from runtime.kuuos_runtime_daemon_v0_1 import run_runtime_daemon
    from runtime.kuuos_runtime_daemon_qi_managed_reentry_chain_runner_v0_1 import (
        run_qi_managed_reentry_chain,
    )
except ModuleNotFoundError:
    from kuuos_runtime_daemon_v0_1 import run_runtime_daemon
    from kuuos_runtime_daemon_qi_managed_reentry_chain_runner_v0_1 import (
        run_qi_managed_reentry_chain,
    )


@dataclass(frozen=True)
class KuuOSQiManagedDaemonCycleResult:
    cycle_version: str
    cycle_status: str
    daemon_dir: str
    chain_dir: str
    daemon_result_path: str
    daemon_status: str
    daemon_stop_reason: str
    daemon_ticks_run: int
    daemon_final_raw_state_path: str | None
    daemon_final_state_bundle_path: str | None
    daemon_health_projection_path: str | None
    daemon_health_status: str | None
    daemon_next_operator_action: str | None
    daemon_recoverability_status: str | None
    requested_max_reentry_cycles: int
    managed_chain_result_path: str
    managed_chain_status: str
    managed_chain_invoked: bool
    controller_decision: str
    controller_reason: str
    allowed_max_cycles: int
    reentry_cycles_run: int
    reentry_ticks_invoked: int
    final_raw_state_path: str | None
    final_state_bundle_path: str | None
    final_daemon_health_status: str | None
    final_next_operator_action: str | None
    final_recoverability_status: str | None
    cycle_reason: str
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


def run_qi_managed_daemon_cycle(
    *,
    raw_state_path: Path,
    evidence_path: Path,
    daemon_dir: Path,
    chain_dir: Path,
    max_daemon_ticks: int = 1,
    max_steps_per_tick: int = 1,
    sleep_seconds: float = 0.0,
    state_bundle_path: Path | None = None,
    requested_max_reentry_cycles: int = 2,
    refresh_before_first_reentry: bool = True,
    refresh_after_each_reentry: bool = True,
) -> KuuOSQiManagedDaemonCycleResult:
    daemon_result = run_runtime_daemon(
        raw_state_path=raw_state_path,
        evidence_path=evidence_path,
        daemon_dir=daemon_dir,
        max_ticks=max_daemon_ticks,
        max_steps_per_tick=max_steps_per_tick,
        sleep_seconds=sleep_seconds,
        state_bundle_path=state_bundle_path,
    )
    daemon_result_path = Path(daemon_dir) / "daemon_result_v0_1.json"
    chain_input_raw = Path(daemon_result.final_raw_state_path) if daemon_result.final_raw_state_path else Path(raw_state_path)
    chain_input_bundle = Path(daemon_result.final_state_bundle_path) if daemon_result.final_state_bundle_path else state_bundle_path

    managed_chain = run_qi_managed_reentry_chain(
        daemon_dir=daemon_dir,
        raw_state_path=chain_input_raw,
        evidence_path=evidence_path,
        chain_dir=chain_dir,
        state_bundle_path=chain_input_bundle,
        requested_max_cycles=requested_max_reentry_cycles,
        refresh_before_first=refresh_before_first_reentry,
        refresh_after_each=refresh_after_each_reentry,
    )
    managed_chain_path = Path(chain_dir) / "qi_managed_reentry_chain_result_v0_1.json"
    _write_json(managed_chain_path, managed_chain.to_dict())

    final_raw = managed_chain.final_raw_state_path or daemon_result.final_raw_state_path
    final_bundle = managed_chain.final_state_bundle_path or daemon_result.final_state_bundle_path
    if managed_chain.chain_invoked and managed_chain.ticks_invoked > 0:
        cycle_status = "QI_MANAGED_DAEMON_CYCLE_REENTRY_INVOKED"
        cycle_reason = managed_chain.managed_stop_reason
    elif managed_chain.chain_invoked:
        cycle_status = "QI_MANAGED_DAEMON_CYCLE_REENTRY_STOPPED"
        cycle_reason = managed_chain.managed_stop_reason
    else:
        cycle_status = "QI_MANAGED_DAEMON_CYCLE_DAEMON_ONLY"
        cycle_reason = managed_chain.managed_stop_reason

    return KuuOSQiManagedDaemonCycleResult(
        cycle_version="kuuos_runtime_daemon_qi_managed_daemon_cycle_runner_v0_1",
        cycle_status=cycle_status,
        daemon_dir=str(daemon_dir),
        chain_dir=str(chain_dir),
        daemon_result_path=str(daemon_result_path),
        daemon_status=daemon_result.daemon_status,
        daemon_stop_reason=daemon_result.stop_reason,
        daemon_ticks_run=daemon_result.ticks_run,
        daemon_final_raw_state_path=daemon_result.final_raw_state_path,
        daemon_final_state_bundle_path=daemon_result.final_state_bundle_path,
        daemon_health_projection_path=daemon_result.qi_process_tensor_health_projection_path,
        daemon_health_status=daemon_result.daemon_health_status,
        daemon_next_operator_action=daemon_result.next_operator_action,
        daemon_recoverability_status=daemon_result.recoverability_status,
        requested_max_reentry_cycles=requested_max_reentry_cycles,
        managed_chain_result_path=str(managed_chain_path),
        managed_chain_status=managed_chain.managed_runner_status,
        managed_chain_invoked=managed_chain.chain_invoked,
        controller_decision=managed_chain.controller_decision,
        controller_reason=managed_chain.controller_reason,
        allowed_max_cycles=managed_chain.allowed_max_cycles,
        reentry_cycles_run=managed_chain.cycles_run,
        reentry_ticks_invoked=managed_chain.ticks_invoked,
        final_raw_state_path=final_raw,
        final_state_bundle_path=final_bundle,
        final_daemon_health_status=managed_chain.final_daemon_health_status or daemon_result.daemon_health_status,
        final_next_operator_action=managed_chain.final_next_operator_action or daemon_result.next_operator_action,
        final_recoverability_status=managed_chain.final_recoverability_status or daemon_result.recoverability_status,
        cycle_reason=cycle_reason,
        grants_execution_authority=managed_chain.grants_execution_authority,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run KuuOS Qi managed daemon cycle v0.1")
    parser.add_argument("--raw-state", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--daemon-dir", type=Path, required=True)
    parser.add_argument("--chain-dir", type=Path, required=True)
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
    result = run_qi_managed_daemon_cycle(
        raw_state_path=args.raw_state,
        evidence_path=args.evidence,
        daemon_dir=args.daemon_dir,
        chain_dir=args.chain_dir,
        max_daemon_ticks=args.max_daemon_ticks,
        max_steps_per_tick=args.max_steps_per_tick,
        sleep_seconds=args.sleep_seconds,
        state_bundle_path=args.state_bundle,
        requested_max_reentry_cycles=args.requested_max_reentry_cycles,
        refresh_before_first_reentry=not args.no_refresh_before_first_reentry,
        refresh_after_each_reentry=not args.no_refresh_after_each_reentry,
    )
    if args.write_summary:
        _write_json(args.chain_dir / "qi_managed_daemon_cycle_result_v0_1.json", result.to_dict())
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
