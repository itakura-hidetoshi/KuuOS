#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import argparse
import json
from typing import Any


@dataclass(frozen=True)
class KuuOSQiPersistentSupervisorStatusView:
    status_view_version: str
    status_view_status: str
    out_dir: str
    supervisor_manifest_path: str
    supervisor_status: str | None
    iterations_run: int
    total_cycles_run: int
    total_control_checks: int
    final_stop_reason: str | None
    latest_iteration_index: int | None
    latest_heartbeat_path: str | None
    latest_status_path: str | None
    latest_heartbeat: dict[str, Any]
    latest_status: dict[str, Any]
    view_blockers: list[str]
    view_warnings: list[str]
    status_view_only: bool
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


def _read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def compile_qi_persistent_supervisor_status_view(*, out_dir: Path) -> KuuOSQiPersistentSupervisorStatusView:
    out_dir = Path(out_dir)
    manifest_path = out_dir / "qi_persistent_supervisor_manifest_v0_1.json"
    blockers: list[str] = []
    warnings: list[str] = []
    manifest = _read_json(manifest_path)
    if not manifest:
        blockers.append("supervisor_manifest_missing")

    records = manifest.get("iteration_records", []) if isinstance(manifest, dict) else []
    if not isinstance(records, list):
        records = []
        warnings.append("iteration_records_not_list")
    latest_record = records[-1] if records and isinstance(records[-1], dict) else None
    latest_index = _safe_int(latest_record.get("iteration_index"), None) if latest_record else None
    latest_heartbeat_path = latest_record.get("heartbeat_path") if latest_record else None
    latest_status_path = latest_record.get("status_path") if latest_record else None
    heartbeat = _read_json(Path(latest_heartbeat_path)) if latest_heartbeat_path else {}
    status = _read_json(Path(latest_status_path)) if latest_status_path else {}
    if latest_record and not heartbeat:
        warnings.append("latest_heartbeat_missing")
    if latest_record and not status:
        warnings.append("latest_status_missing")

    status_view_status = "QI_PERSISTENT_SUPERVISOR_STATUS_VIEW_READY" if not blockers else "QI_PERSISTENT_SUPERVISOR_STATUS_VIEW_BLOCKED"
    return KuuOSQiPersistentSupervisorStatusView(
        status_view_version="kuuos_runtime_daemon_qi_persistent_supervisor_status_view_v0_1",
        status_view_status=status_view_status,
        out_dir=str(out_dir),
        supervisor_manifest_path=str(manifest_path),
        supervisor_status=manifest.get("supervisor_status") if manifest else None,
        iterations_run=_safe_int(manifest.get("iterations_run"), 0) if manifest else 0,
        total_cycles_run=_safe_int(manifest.get("total_cycles_run"), 0) if manifest else 0,
        total_control_checks=_safe_int(manifest.get("total_control_checks"), 0) if manifest else 0,
        final_stop_reason=manifest.get("final_stop_reason") if manifest else None,
        latest_iteration_index=latest_index,
        latest_heartbeat_path=str(latest_heartbeat_path) if latest_heartbeat_path else None,
        latest_status_path=str(latest_status_path) if latest_status_path else None,
        latest_heartbeat=heartbeat,
        latest_status=status,
        view_blockers=blockers,
        view_warnings=warnings,
        status_view_only=True,
        read_only=True,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="View KuuOS Qi persistent supervisor status v0.1")
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--write", type=Path, default=None)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = compile_qi_persistent_supervisor_status_view(out_dir=args.out_dir)
    if args.write:
        _write_json(args.write, result.to_dict())
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
