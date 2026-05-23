#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import argparse
import json
from typing import Any, Mapping

try:
    from runtime.kuuos_state_io_runner_v0_1 import run_state_io
    from runtime.kuuos_runtime_daemon_qi_process_tensor_bounded_tick_invocation_boundary_v0_1 import (
        compile_qi_process_tensor_bounded_tick_invocation_boundary,
    )
except ModuleNotFoundError:
    from kuuos_state_io_runner_v0_1 import run_state_io
    from kuuos_runtime_daemon_qi_process_tensor_bounded_tick_invocation_boundary_v0_1 import (
        compile_qi_process_tensor_bounded_tick_invocation_boundary,
    )

NON_AUTHORITY_FLAGS = {
    "grants_truth_authority": False,
    "grants_final_commitment_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_clinical_authority": False,
    "grants_theorem_authority": False,
    "grants_completed_identity_authority": False,
}

@dataclass(frozen=True)
class KuuOSQiProcessTensorBoundedTickExecutorReceipt:
    executor_version: str
    executor_status: str
    source_gate_status: str
    source_license_decision: str
    source_boundary_status: str
    source_invocation_decision: str
    bounded_tick_license: bool
    single_tick_invocation_token: bool
    tick_invoked: bool
    denied_reason: str | None
    required_preconditions: list[str]
    raw_state_path: str | None
    evidence_path: str | None
    input_state_bundle_path: str | None
    output_dir: str | None
    run_manifest_path: str | None
    next_raw_state_path: str | None
    state_bundle_path: str | None
    step_trace_path: str | None
    steps_run: int
    stop_reason: str | None
    licensed_max_steps_per_tick: int
    runtime_hot_path_tier: str
    validation_tier: str
    executor_reason: str
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


def _as_bool(value: Any) -> bool:
    return bool(value)


def _as_int(value: Any, default: int = 1) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def compile_denied_bounded_tick_executor_receipt(
    license_gate: Mapping[str, Any],
    invocation_boundary: Mapping[str, Any] | None = None,
    *,
    raw_state_path: Path | None = None,
    evidence_path: Path | None = None,
    state_bundle_path: Path | None = None,
    output_dir: Path | None = None,
) -> KuuOSQiProcessTensorBoundedTickExecutorReceipt:
    invocation_boundary = invocation_boundary or {}
    boundary_denial = invocation_boundary.get("denied_reason")
    gate_denial = license_gate.get("denied_reason")
    denied_reason = str(boundary_denial or gate_denial or "single_tick_invocation_token_not_granted")
    return KuuOSQiProcessTensorBoundedTickExecutorReceipt(
        executor_version="kuuos_runtime_daemon_qi_process_tensor_bounded_tick_executor_v0_1",
        executor_status="QI_PROCESS_TENSOR_BOUNDED_TICK_NOT_INVOKED",
        source_gate_status=str(license_gate.get("gate_status") or "UNKNOWN_GATE_STATUS"),
        source_license_decision=str(license_gate.get("license_decision") or "NO_BOUNDED_TICK_LICENSE"),
        source_boundary_status=str(invocation_boundary.get("boundary_status") or "UNKNOWN_INVOCATION_BOUNDARY_STATUS"),
        source_invocation_decision=str(invocation_boundary.get("invocation_decision") or "NO_SINGLE_TICK_INVOCATION_TOKEN"),
        bounded_tick_license=_as_bool(license_gate.get("bounded_tick_license")),
        single_tick_invocation_token=_as_bool(invocation_boundary.get("single_tick_invocation_token")),
        tick_invoked=False,
        denied_reason=denied_reason,
        required_preconditions=list(license_gate.get("required_preconditions") or []),
        raw_state_path=str(raw_state_path) if raw_state_path else None,
        evidence_path=str(evidence_path) if evidence_path else None,
        input_state_bundle_path=str(state_bundle_path) if state_bundle_path else None,
        output_dir=str(output_dir) if output_dir else None,
        run_manifest_path=None,
        next_raw_state_path=None,
        state_bundle_path=None,
        step_trace_path=None,
        steps_run=0,
        stop_reason=None,
        licensed_max_steps_per_tick=0,
        runtime_hot_path_tier="T0_hot_path_guard",
        validation_tier="T3_runtime_full_check",
        executor_reason="invocation_boundary_denied_or_missing_single_tick_token",
        grants_execution_authority=False,
    )


def run_qi_process_tensor_bounded_tick_executor(
    *,
    license_gate: Mapping[str, Any],
    raw_state_path: Path,
    evidence_path: Path,
    output_dir: Path,
    state_bundle_path: Path | None = None,
    invocation_boundary: Mapping[str, Any] | None = None,
    requested_invocation_depth: int = 0,
) -> KuuOSQiProcessTensorBoundedTickExecutorReceipt:
    boundary = dict(invocation_boundary or compile_qi_process_tensor_bounded_tick_invocation_boundary(
        license_gate,
        requested_invocation_depth=requested_invocation_depth,
        max_allowed_invocation_depth=0,
    ).to_dict())

    if not _as_bool(boundary.get("single_tick_invocation_token")):
        return compile_denied_bounded_tick_executor_receipt(
            license_gate,
            boundary,
            raw_state_path=raw_state_path,
            evidence_path=evidence_path,
            state_bundle_path=state_bundle_path,
            output_dir=output_dir,
        )

    if str(boundary.get("invocation_decision")) != "SINGLE_TICK_INVOCATION_TOKEN_GRANTED":
        return compile_denied_bounded_tick_executor_receipt(
            license_gate,
            boundary,
            raw_state_path=raw_state_path,
            evidence_path=evidence_path,
            state_bundle_path=state_bundle_path,
            output_dir=output_dir,
        )

    max_steps = max(1, _as_int(boundary.get("licensed_max_steps_per_tick"), 1))
    max_steps = min(max_steps, 25)
    manifest = run_state_io(
        raw_state_path=raw_state_path,
        evidence_path=evidence_path,
        output_dir=output_dir,
        max_steps=max_steps,
        state_bundle_path=state_bundle_path,
    )
    return KuuOSQiProcessTensorBoundedTickExecutorReceipt(
        executor_version="kuuos_runtime_daemon_qi_process_tensor_bounded_tick_executor_v0_1",
        executor_status="QI_PROCESS_TENSOR_BOUNDED_TICK_INVOKED",
        source_gate_status=str(license_gate.get("gate_status") or "UNKNOWN_GATE_STATUS"),
        source_license_decision=str(license_gate.get("license_decision") or "UNKNOWN_LICENSE_DECISION"),
        source_boundary_status=str(boundary.get("boundary_status") or "UNKNOWN_INVOCATION_BOUNDARY_STATUS"),
        source_invocation_decision=str(boundary.get("invocation_decision") or "UNKNOWN_INVOCATION_DECISION"),
        bounded_tick_license=_as_bool(license_gate.get("bounded_tick_license")),
        single_tick_invocation_token=True,
        tick_invoked=True,
        denied_reason=None,
        required_preconditions=[],
        raw_state_path=str(raw_state_path),
        evidence_path=str(evidence_path),
        input_state_bundle_path=str(state_bundle_path) if state_bundle_path else None,
        output_dir=str(output_dir),
        run_manifest_path=str(output_dir / "run_manifest_v0_1.json"),
        next_raw_state_path=manifest.next_raw_state_path,
        state_bundle_path=manifest.state_bundle_path,
        step_trace_path=manifest.step_trace_path,
        steps_run=manifest.steps_run,
        stop_reason=manifest.stop_reason,
        licensed_max_steps_per_tick=max_steps,
        runtime_hot_path_tier="T0_hot_path_guard",
        validation_tier="T3_runtime_full_check",
        executor_reason="single_tick_invocation_token_granted_and_state_io_invoked_once",
        grants_execution_authority=True,
    )


def read_and_run_qi_process_tensor_bounded_tick_executor(
    *,
    daemon_dir: Path,
    raw_state_path: Path,
    evidence_path: Path,
    output_dir: Path,
    state_bundle_path: Path | None = None,
    requested_invocation_depth: int = 0,
) -> KuuOSQiProcessTensorBoundedTickExecutorReceipt:
    license_gate = _read_json(daemon_dir / "daemon_qi_process_tensor_reentry_license_gate_v0_1.json") or {}
    invocation_boundary = _read_json(daemon_dir / "daemon_qi_process_tensor_bounded_tick_invocation_boundary_v0_1.json")
    return run_qi_process_tensor_bounded_tick_executor(
        license_gate=license_gate,
        invocation_boundary=invocation_boundary,
        requested_invocation_depth=requested_invocation_depth,
        raw_state_path=raw_state_path,
        evidence_path=evidence_path,
        output_dir=output_dir,
        state_bundle_path=state_bundle_path,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run KuuOS Qi process tensor bounded tick executor v0.1")
    parser.add_argument("--daemon-dir", type=Path, required=True)
    parser.add_argument("--raw-state", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--state-bundle", type=Path, default=None)
    parser.add_argument("--requested-invocation-depth", type=int, default=0)
    parser.add_argument("--write", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = read_and_run_qi_process_tensor_bounded_tick_executor(
        daemon_dir=args.daemon_dir,
        raw_state_path=args.raw_state,
        evidence_path=args.evidence,
        output_dir=args.output_dir,
        state_bundle_path=args.state_bundle,
        requested_invocation_depth=args.requested_invocation_depth,
    )
    if args.write:
        _write_json(args.daemon_dir / "daemon_qi_process_tensor_bounded_tick_executor_receipt_v0_1.json", result.to_dict())
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
