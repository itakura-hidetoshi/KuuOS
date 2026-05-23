#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import argparse
import json
from typing import Any, Mapping

@dataclass(frozen=True)
class KuuOSQiProcessTensorBoundedTickInvocationBoundary:
    boundary_version: str
    boundary_status: str
    invocation_decision: str
    source_gate_status: str
    source_license_decision: str
    bounded_tick_license: bool
    single_tick_invocation_token: bool
    recursive_invocation_denied: bool
    requested_invocation_depth: int
    max_allowed_invocation_depth: int
    licensed_max_steps_per_tick: int
    denied_reason: str | None
    boundary_reason: str
    runtime_hot_path_tier: str
    validation_tier: str
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


def _as_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def compile_qi_process_tensor_bounded_tick_invocation_boundary(
    license_gate: Mapping[str, Any],
    *,
    requested_invocation_depth: int = 0,
    max_allowed_invocation_depth: int = 0,
) -> KuuOSQiProcessTensorBoundedTickInvocationBoundary:
    gate_status = str(license_gate.get("gate_status") or "UNKNOWN_GATE_STATUS")
    license_decision = str(license_gate.get("license_decision") or "NO_BOUNDED_TICK_LICENSE")
    bounded_license = _as_bool(license_gate.get("bounded_tick_license"))
    may_invoke = _as_bool(license_gate.get("may_invoke_next_tick"))
    max_steps = max(1, _as_int(license_gate.get("licensed_max_steps_per_tick"), 1))
    max_steps = min(max_steps, 25)
    depth = max(0, requested_invocation_depth)
    depth_limit = max(0, max_allowed_invocation_depth)

    if depth > depth_limit:
        return KuuOSQiProcessTensorBoundedTickInvocationBoundary(
            boundary_version="kuuos_runtime_daemon_qi_process_tensor_bounded_tick_invocation_boundary_v0_1",
            boundary_status="QI_PROCESS_TENSOR_INVOCATION_BOUNDARY_DENIED_RECURSIVE",
            invocation_decision="NO_SINGLE_TICK_INVOCATION_TOKEN",
            source_gate_status=gate_status,
            source_license_decision=license_decision,
            bounded_tick_license=bounded_license,
            single_tick_invocation_token=False,
            recursive_invocation_denied=True,
            requested_invocation_depth=depth,
            max_allowed_invocation_depth=depth_limit,
            licensed_max_steps_per_tick=0,
            denied_reason="recursive_or_nested_invocation_denied",
            boundary_reason="requested_invocation_depth_exceeds_single_tick_boundary",
            runtime_hot_path_tier="T0_hot_path_guard",
            validation_tier="T3_runtime_full_check",
            allowed_projection=["qi_process_tensor_bounded_tick_invocation_boundary", "recursive_invocation_denial"],
        )

    if not bounded_license or not may_invoke or license_decision != "BOUNDED_TICK_LICENSE_GRANTED":
        return KuuOSQiProcessTensorBoundedTickInvocationBoundary(
            boundary_version="kuuos_runtime_daemon_qi_process_tensor_bounded_tick_invocation_boundary_v0_1",
            boundary_status="QI_PROCESS_TENSOR_INVOCATION_BOUNDARY_DENIED_NO_LICENSE",
            invocation_decision="NO_SINGLE_TICK_INVOCATION_TOKEN",
            source_gate_status=gate_status,
            source_license_decision=license_decision,
            bounded_tick_license=bounded_license,
            single_tick_invocation_token=False,
            recursive_invocation_denied=False,
            requested_invocation_depth=depth,
            max_allowed_invocation_depth=depth_limit,
            licensed_max_steps_per_tick=0,
            denied_reason="bounded_tick_license_missing_or_not_granted",
            boundary_reason="license_gate_did_not_grant_bounded_tick_invocation",
            runtime_hot_path_tier="T0_hot_path_guard",
            validation_tier="T3_runtime_full_check",
            allowed_projection=["qi_process_tensor_bounded_tick_invocation_boundary", "license_denial_boundary"],
        )

    return KuuOSQiProcessTensorBoundedTickInvocationBoundary(
        boundary_version="kuuos_runtime_daemon_qi_process_tensor_bounded_tick_invocation_boundary_v0_1",
        boundary_status="QI_PROCESS_TENSOR_INVOCATION_BOUNDARY_GRANTED_SINGLE_TICK",
        invocation_decision="SINGLE_TICK_INVOCATION_TOKEN_GRANTED",
        source_gate_status=gate_status,
        source_license_decision=license_decision,
        bounded_tick_license=True,
        single_tick_invocation_token=True,
        recursive_invocation_denied=False,
        requested_invocation_depth=depth,
        max_allowed_invocation_depth=depth_limit,
        licensed_max_steps_per_tick=max_steps,
        denied_reason=None,
        boundary_reason="bounded_license_passed_single_tick_invocation_boundary",
        runtime_hot_path_tier="T0_hot_path_guard",
        validation_tier="T3_runtime_full_check",
        allowed_projection=["qi_process_tensor_bounded_tick_invocation_boundary", "single_tick_invocation_token"],
    )


def read_and_compile_qi_process_tensor_bounded_tick_invocation_boundary(
    daemon_dir: Path,
    *,
    requested_invocation_depth: int = 0,
    max_allowed_invocation_depth: int = 0,
) -> KuuOSQiProcessTensorBoundedTickInvocationBoundary:
    license_gate = _read_json(daemon_dir / "daemon_qi_process_tensor_reentry_license_gate_v0_1.json") or {}
    return compile_qi_process_tensor_bounded_tick_invocation_boundary(
        license_gate,
        requested_invocation_depth=requested_invocation_depth,
        max_allowed_invocation_depth=max_allowed_invocation_depth,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compile KuuOS Qi bounded tick invocation boundary v0.1")
    parser.add_argument("--daemon-dir", type=Path, required=True)
    parser.add_argument("--requested-invocation-depth", type=int, default=0)
    parser.add_argument("--max-allowed-invocation-depth", type=int, default=0)
    parser.add_argument("--write", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = read_and_compile_qi_process_tensor_bounded_tick_invocation_boundary(
        args.daemon_dir,
        requested_invocation_depth=args.requested_invocation_depth,
        max_allowed_invocation_depth=args.max_allowed_invocation_depth,
    )
    if args.write:
        _write_json(args.daemon_dir / "daemon_qi_process_tensor_bounded_tick_invocation_boundary_v0_1.json", result.to_dict())
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
