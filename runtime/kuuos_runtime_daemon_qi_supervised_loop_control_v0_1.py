#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
import argparse
import json
from typing import Any, Mapping


@dataclass(frozen=True)
class KuuOSQiSupervisedLoopControl:
    control_version: str
    control_status: str
    loop_allowed: bool
    stop_requested: bool
    enabled: bool
    max_cycles: int
    sleep_seconds_between_cycles: float
    control_reason: str
    heartbeat_utc: str
    source_control_path: str | None
    control_blockers: list[str]
    control_warnings: list[str]
    control_only: bool
    read_only: bool
    grants_execution_authority: bool = False
    grants_next_tick_execution_authority: bool = False
    grants_truth_authority: bool = False
    grants_final_commitment_authority: bool = False
    grants_memory_overwrite_authority: bool = False
    grants_clinical_authority: bool = False
    grants_theorem_authority: bool = False
    grants_completed_identity_authority: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _bool(payload: Mapping[str, Any], key: str, default: bool) -> bool:
    value = payload.get(key, default)
    return bool(value)


def _int(payload: Mapping[str, Any], key: str, default: int) -> int:
    try:
        return int(payload.get(key, default))
    except (TypeError, ValueError):
        return default


def _float(payload: Mapping[str, Any], key: str, default: float) -> float:
    try:
        return float(payload.get(key, default))
    except (TypeError, ValueError):
        return default


def compile_qi_supervised_loop_control(
    *,
    control_packet: Mapping[str, Any] | None = None,
    source_control_path: Path | None = None,
    heartbeat_utc: str | None = None,
) -> KuuOSQiSupervisedLoopControl:
    packet = control_packet or {}
    enabled = _bool(packet, "enabled", True)
    stop_requested = _bool(packet, "stop_requested", False)
    max_cycles = _int(packet, "max_cycles", 1)
    sleep_seconds = _float(packet, "sleep_seconds_between_cycles", 0.0)
    blockers: list[str] = []
    warnings: list[str] = []

    if max_cycles < 1:
        blockers.append("max_cycles_below_one")
    if sleep_seconds < 0:
        blockers.append("sleep_seconds_below_zero")
    if not enabled:
        blockers.append("loop_disabled")
    if stop_requested:
        blockers.append("stop_requested")
    if not packet:
        warnings.append("control_packet_missing_using_safe_defaults")

    loop_allowed = len(blockers) == 0
    if loop_allowed:
        status = "QI_SUPERVISED_LOOP_CONTROL_ALLOWED"
        reason = "control_packet_allows_bounded_loop"
    else:
        status = "QI_SUPERVISED_LOOP_CONTROL_BLOCKED"
        reason = blockers[0]

    return KuuOSQiSupervisedLoopControl(
        control_version="kuuos_runtime_daemon_qi_supervised_loop_control_v0_1",
        control_status=status,
        loop_allowed=loop_allowed,
        stop_requested=stop_requested,
        enabled=enabled,
        max_cycles=max_cycles if max_cycles >= 1 else 1,
        sleep_seconds_between_cycles=sleep_seconds if sleep_seconds >= 0 else 0.0,
        control_reason=reason,
        heartbeat_utc=heartbeat_utc or _utc_now(),
        source_control_path=str(source_control_path) if source_control_path else None,
        control_blockers=blockers,
        control_warnings=warnings,
        control_only=True,
        read_only=True,
    )


def read_and_compile_qi_supervised_loop_control(path: Path) -> KuuOSQiSupervisedLoopControl:
    path = Path(path)
    return compile_qi_supervised_loop_control(
        control_packet=_read_json(path),
        source_control_path=path if path.is_file() else None,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compile KuuOS Qi supervised loop control surface v0.1")
    parser.add_argument("--control", type=Path, required=True)
    parser.add_argument("--write", type=Path, default=None)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = read_and_compile_qi_supervised_loop_control(args.control)
    if args.write:
        _write_json(args.write, result.to_dict())
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
