#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_daemon_qi_process_tensor_bounded_tick_executor_v0_1 import (  # noqa: E402
    compile_denied_bounded_tick_executor_receipt,
    read_and_run_qi_process_tensor_bounded_tick_executor,
)


def _read_json(path: pathlib.Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else None


def _write_json(path: pathlib.Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _health_allows_manual_runner(health: dict[str, Any] | None) -> tuple[bool, str | None]:
    if health is None:
        return True, None
    if bool(health.get("recovery_unsafe")):
        return False, "health_projection_recovery_unsafe"
    if health.get("next_operator_action") != "invoke_manual_runner":
        return False, "health_projection_next_operator_action_not_invoke_manual_runner"
    if health.get("recoverability_status") != "RECOVERABLE_BY_MANUAL_RUNNER":
        return False, "health_projection_not_recoverable_by_manual_runner"
    if health.get("local_recovery_allowed") is not True:
        return False, "health_projection_local_recovery_not_allowed"
    return True, None


def _health_denied_receipt(
    *,
    daemon_dir: pathlib.Path,
    raw_state_path: pathlib.Path,
    evidence_path: pathlib.Path,
    output_dir: pathlib.Path,
    state_bundle_path: pathlib.Path | None,
    denied_reason: str,
):
    license_gate = _read_json(daemon_dir / "daemon_qi_process_tensor_reentry_license_gate_v0_1.json") or {}
    boundary = _read_json(daemon_dir / "daemon_qi_process_tensor_bounded_tick_invocation_boundary_v0_1.json") or {}
    boundary = dict(boundary)
    boundary["boundary_status"] = "QI_PROCESS_TENSOR_INVOCATION_BOUNDARY_DENIED_BY_HEALTH_PROJECTION"
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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Manually invoke one Qi Process Tensor bounded tick from daemon receipts v0.1"
    )
    parser.add_argument("--daemon-dir", type=pathlib.Path, required=True)
    parser.add_argument("--raw-state", type=pathlib.Path, required=True)
    parser.add_argument("--evidence", type=pathlib.Path, required=True)
    parser.add_argument("--output-dir", type=pathlib.Path, required=True)
    parser.add_argument("--state-bundle", type=pathlib.Path, default=None)
    parser.add_argument("--requested-invocation-depth", type=int, default=0)
    parser.add_argument("--write", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    health = _read_json(args.daemon_dir / "daemon_qi_process_tensor_health_projection_v0_1.json")
    allowed, denied_reason = _health_allows_manual_runner(health)
    if allowed:
        receipt = read_and_run_qi_process_tensor_bounded_tick_executor(
            daemon_dir=args.daemon_dir,
            raw_state_path=args.raw_state,
            evidence_path=args.evidence,
            output_dir=args.output_dir,
            state_bundle_path=args.state_bundle,
            requested_invocation_depth=args.requested_invocation_depth,
        )
    else:
        receipt = _health_denied_receipt(
            daemon_dir=args.daemon_dir,
            raw_state_path=args.raw_state,
            evidence_path=args.evidence,
            output_dir=args.output_dir,
            state_bundle_path=args.state_bundle,
            denied_reason=str(denied_reason),
        )
    payload = receipt.to_dict()
    if args.write:
        _write_json(
            args.daemon_dir / "daemon_qi_process_tensor_bounded_tick_executor_receipt_v0_1.json",
            payload,
        )
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
