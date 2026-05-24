#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import argparse
import json
from typing import Any

try:
    from runtime.kuuos_runtime_daemon_qi_projection_output_writer_v0_1 import write_qi_projection_outputs
    from runtime.kuuos_runtime_daemon_qi_process_tensor_bounded_tick_executor_v0_1 import (
        compile_denied_bounded_tick_executor_receipt,
        read_and_run_qi_process_tensor_bounded_tick_executor,
    )
except ModuleNotFoundError:
    from kuuos_runtime_daemon_qi_projection_output_writer_v0_1 import write_qi_projection_outputs
    from kuuos_runtime_daemon_qi_process_tensor_bounded_tick_executor_v0_1 import (
        compile_denied_bounded_tick_executor_receipt,
        read_and_run_qi_process_tensor_bounded_tick_executor,
    )


@dataclass(frozen=True)
class KuuOSQiBoundedReentryCycleResult:
    cycle_version: str
    cycle_status: str
    daemon_dir: str
    output_dir: str
    pre_health_projection_path: str | None
    pre_daemon_health_status: str | None
    pre_next_operator_action: str | None
    pre_recoverability_status: str | None
    pre_recovery_unsafe: bool | None
    executor_receipt_path: str
    executor_status: str
    tick_invoked: bool
    denied_reason: str | None
    post_health_projection_path: str | None
    post_daemon_health_status: str | None
    post_next_operator_action: str | None
    post_recoverability_status: str | None
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


def _read_json(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else None


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _health_allows_reentry(health: dict[str, Any] | None) -> tuple[bool, str | None]:
    if health is None:
        return False, "health_projection_missing"
    if bool(health.get("recovery_unsafe")):
        return False, "health_projection_recovery_unsafe"
    if health.get("next_operator_action") != "invoke_manual_runner":
        return False, "health_projection_next_operator_action_not_invoke_manual_runner"
    if health.get("recoverability_status") != "RECOVERABLE_BY_MANUAL_RUNNER":
        return False, "health_projection_not_recoverable_by_manual_runner"
    if health.get("local_recovery_allowed") is not True:
        return False, "health_projection_local_recovery_not_allowed"
    return True, None


def _denied_receipt(
    *,
    daemon_dir: Path,
    raw_state_path: Path,
    evidence_path: Path,
    output_dir: Path,
    state_bundle_path: Path | None,
    denied_reason: str,
):
    license_gate = _read_json(daemon_dir / "daemon_qi_process_tensor_reentry_license_gate_v0_1.json") or {}
    boundary = _read_json(daemon_dir / "daemon_qi_process_tensor_bounded_tick_invocation_boundary_v0_1.json") or {}
    boundary = dict(boundary)
    boundary["boundary_status"] = "QI_PROCESS_TENSOR_INVOCATION_BOUNDARY_DENIED_BY_REENTRY_CYCLE"
    boundary["invocation_decision"] = "NO_SINGLE_TICK_INVOCATION_TOKEN"
    boundary["single_tick_invocation_token"] = False
    boundary["denied_reason"] = denied_reason
    return compile_denied_bounded_tick_executor_receipt(
        license_gate,
        boundary,
        raw_state_path=raw_state_path,
        evidence_path=evidence_path,
        state_bundle_path=state_bundle_path,
        output_dir=output_dir,
    )


def run_qi_bounded_reentry_cycle(
    *,
    daemon_dir: Path,
    raw_state_path: Path,
    evidence_path: Path,
    output_dir: Path,
    state_bundle_path: Path | None = None,
    requested_invocation_depth: int = 0,
    refresh_before: bool = True,
    refresh_after: bool = True,
) -> KuuOSQiBoundedReentryCycleResult:
    daemon_dir = Path(daemon_dir)
    if refresh_before:
        write_qi_projection_outputs(daemon_dir)
    health_path = daemon_dir / "daemon_qi_process_tensor_health_projection_v0_1.json"
    pre_health = _read_json(health_path)
    allowed, denied_reason = _health_allows_reentry(pre_health)
    if allowed:
        receipt = read_and_run_qi_process_tensor_bounded_tick_executor(
            daemon_dir=daemon_dir,
            raw_state_path=raw_state_path,
            evidence_path=evidence_path,
            output_dir=output_dir,
            state_bundle_path=state_bundle_path,
            requested_invocation_depth=requested_invocation_depth,
        )
        cycle_status = "QI_BOUNDED_REENTRY_CYCLE_INVOKED"
        cycle_reason = "health_projection_allowed_manual_runner"
    else:
        receipt = _denied_receipt(
            daemon_dir=daemon_dir,
            raw_state_path=raw_state_path,
            evidence_path=evidence_path,
            output_dir=output_dir,
            state_bundle_path=state_bundle_path,
            denied_reason=str(denied_reason),
        )
        cycle_status = "QI_BOUNDED_REENTRY_CYCLE_NOT_INVOKED"
        cycle_reason = str(denied_reason)

    receipt_path = daemon_dir / "daemon_qi_process_tensor_bounded_tick_executor_receipt_v0_1.json"
    _write_json(receipt_path, receipt.to_dict())

    if refresh_after:
        write_qi_projection_outputs(daemon_dir)
    post_health = _read_json(health_path)

    return KuuOSQiBoundedReentryCycleResult(
        cycle_version="kuuos_runtime_daemon_qi_bounded_reentry_cycle_runner_v0_1",
        cycle_status=cycle_status,
        daemon_dir=str(daemon_dir),
        output_dir=str(output_dir),
        pre_health_projection_path=str(health_path) if pre_health else None,
        pre_daemon_health_status=str(pre_health.get("daemon_health_status")) if pre_health else None,
        pre_next_operator_action=str(pre_health.get("next_operator_action")) if pre_health else None,
        pre_recoverability_status=str(pre_health.get("recoverability_status")) if pre_health else None,
        pre_recovery_unsafe=bool(pre_health.get("recovery_unsafe")) if pre_health else None,
        executor_receipt_path=str(receipt_path),
        executor_status=receipt.executor_status,
        tick_invoked=receipt.tick_invoked,
        denied_reason=receipt.denied_reason,
        post_health_projection_path=str(health_path) if post_health else None,
        post_daemon_health_status=str(post_health.get("daemon_health_status")) if post_health else None,
        post_next_operator_action=str(post_health.get("next_operator_action")) if post_health else None,
        post_recoverability_status=str(post_health.get("recoverability_status")) if post_health else None,
        cycle_reason=cycle_reason,
        grants_execution_authority=receipt.grants_execution_authority,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run one KuuOS Qi bounded reentry cycle v0.1")
    parser.add_argument("--daemon-dir", type=Path, required=True)
    parser.add_argument("--raw-state", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--state-bundle", type=Path, default=None)
    parser.add_argument("--requested-invocation-depth", type=int, default=0)
    parser.add_argument("--no-refresh-before", action="store_true")
    parser.add_argument("--no-refresh-after", action="store_true")
    parser.add_argument("--write-summary", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = run_qi_bounded_reentry_cycle(
        daemon_dir=args.daemon_dir,
        raw_state_path=args.raw_state,
        evidence_path=args.evidence,
        output_dir=args.output_dir,
        state_bundle_path=args.state_bundle,
        requested_invocation_depth=args.requested_invocation_depth,
        refresh_before=not args.no_refresh_before,
        refresh_after=not args.no_refresh_after,
    )
    if args.write_summary:
        _write_json(args.daemon_dir / "daemon_qi_bounded_reentry_cycle_result_v0_1.json", result.to_dict())
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
