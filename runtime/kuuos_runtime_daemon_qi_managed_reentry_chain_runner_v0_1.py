#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import argparse
import json
from typing import Any

try:
    from runtime.kuuos_runtime_daemon_qi_reentry_chain_controller_v0_1 import (
        read_and_decide_qi_reentry_chain_controller,
    )
    from runtime.kuuos_runtime_daemon_qi_reentry_handoff_chain_runner_v0_1 import (
        run_qi_reentry_handoff_chain,
    )
except ModuleNotFoundError:
    from kuuos_runtime_daemon_qi_reentry_chain_controller_v0_1 import (
        read_and_decide_qi_reentry_chain_controller,
    )
    from kuuos_runtime_daemon_qi_reentry_handoff_chain_runner_v0_1 import (
        run_qi_reentry_handoff_chain,
    )


@dataclass(frozen=True)
class KuuOSQiManagedReentryChainResult:
    managed_runner_version: str
    managed_runner_status: str
    daemon_dir: str
    chain_dir: str
    requested_max_cycles: int
    allowed_max_cycles: int
    controller_decision: str
    controller_reason: str
    controller_decision_path: str
    chain_result_path: str | None
    chain_invoked: bool
    cycles_run: int
    ticks_invoked: int
    final_raw_state_path: str | None
    final_state_bundle_path: str | None
    final_daemon_health_status: str | None
    final_next_operator_action: str | None
    final_recoverability_status: str | None
    managed_stop_reason: str
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


def run_qi_managed_reentry_chain(
    *,
    daemon_dir: Path,
    raw_state_path: Path,
    evidence_path: Path,
    chain_dir: Path,
    state_bundle_path: Path | None = None,
    requested_max_cycles: int = 2,
    refresh_before_first: bool = True,
    refresh_after_each: bool = True,
) -> KuuOSQiManagedReentryChainResult:
    daemon_dir = Path(daemon_dir)
    chain_dir = Path(chain_dir)
    chain_dir.mkdir(parents=True, exist_ok=True)

    controller = read_and_decide_qi_reentry_chain_controller(
        daemon_dir=daemon_dir,
        requested_max_cycles=requested_max_cycles,
    )
    controller_path = chain_dir / "qi_reentry_chain_controller_decision_v0_1.json"
    _write_json(controller_path, controller.to_dict())

    if controller.allowed_max_cycles <= 0 or not controller.chain_invocation_allowed:
        return KuuOSQiManagedReentryChainResult(
            managed_runner_version="kuuos_runtime_daemon_qi_managed_reentry_chain_runner_v0_1",
            managed_runner_status="QI_MANAGED_REENTRY_CHAIN_NOT_INVOKED",
            daemon_dir=str(daemon_dir),
            chain_dir=str(chain_dir),
            requested_max_cycles=controller.requested_max_cycles,
            allowed_max_cycles=controller.allowed_max_cycles,
            controller_decision=controller.controller_decision,
            controller_reason=controller.controller_reason,
            controller_decision_path=str(controller_path),
            chain_result_path=None,
            chain_invoked=False,
            cycles_run=0,
            ticks_invoked=0,
            final_raw_state_path=None,
            final_state_bundle_path=None,
            final_daemon_health_status=controller.daemon_health_status,
            final_next_operator_action=controller.next_operator_action,
            final_recoverability_status=controller.recoverability_status,
            managed_stop_reason=controller.controller_reason,
            grants_execution_authority=False,
        )

    chain = run_qi_reentry_handoff_chain(
        daemon_dir=daemon_dir,
        raw_state_path=raw_state_path,
        evidence_path=evidence_path,
        chain_dir=chain_dir / "handoff_chain",
        state_bundle_path=state_bundle_path,
        max_cycles=controller.allowed_max_cycles,
        refresh_before_first=refresh_before_first,
        refresh_after_each=refresh_after_each,
    )
    chain_path = chain_dir / "qi_reentry_handoff_chain_result_v0_1.json"
    _write_json(chain_path, chain.to_dict())

    return KuuOSQiManagedReentryChainResult(
        managed_runner_version="kuuos_runtime_daemon_qi_managed_reentry_chain_runner_v0_1",
        managed_runner_status="QI_MANAGED_REENTRY_CHAIN_INVOKED" if chain.ticks_invoked else "QI_MANAGED_REENTRY_CHAIN_STOPPED",
        daemon_dir=str(daemon_dir),
        chain_dir=str(chain_dir),
        requested_max_cycles=controller.requested_max_cycles,
        allowed_max_cycles=controller.allowed_max_cycles,
        controller_decision=controller.controller_decision,
        controller_reason=controller.controller_reason,
        controller_decision_path=str(controller_path),
        chain_result_path=str(chain_path),
        chain_invoked=True,
        cycles_run=chain.cycles_run,
        ticks_invoked=chain.ticks_invoked,
        final_raw_state_path=chain.final_raw_state_path,
        final_state_bundle_path=chain.final_state_bundle_path,
        final_daemon_health_status=chain.final_daemon_health_status,
        final_next_operator_action=chain.final_next_operator_action,
        final_recoverability_status=chain.final_recoverability_status,
        managed_stop_reason=chain.stop_reason,
        grants_execution_authority=chain.grants_execution_authority,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run KuuOS Qi managed reentry chain v0.1")
    parser.add_argument("--daemon-dir", type=Path, required=True)
    parser.add_argument("--raw-state", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--chain-dir", type=Path, required=True)
    parser.add_argument("--state-bundle", type=Path, default=None)
    parser.add_argument("--requested-max-cycles", type=int, default=2)
    parser.add_argument("--no-refresh-before-first", action="store_true")
    parser.add_argument("--no-refresh-after-each", action="store_true")
    parser.add_argument("--write-summary", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = run_qi_managed_reentry_chain(
        daemon_dir=args.daemon_dir,
        raw_state_path=args.raw_state,
        evidence_path=args.evidence,
        chain_dir=args.chain_dir,
        state_bundle_path=args.state_bundle,
        requested_max_cycles=args.requested_max_cycles,
        refresh_before_first=not args.no_refresh_before_first,
        refresh_after_each=not args.no_refresh_after_each,
    )
    if args.write_summary:
        _write_json(args.chain_dir / "qi_managed_reentry_chain_result_v0_1.json", result.to_dict())
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
