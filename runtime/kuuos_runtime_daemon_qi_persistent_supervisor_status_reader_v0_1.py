#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import argparse
import json
from typing import Any


@dataclass(frozen=True)
class KuuOSQiPersistentSupervisorStatusReadout:
    readout_version: str
    readout_status: str
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
    persistent_supervisor_active_like: bool
    readout_only: bool
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


def read_qi_persistent_supervisor_status(*, supervisor_manifest_path: Path) -> KuuOSQiPersistentSupervisorStatusReadout:
    manifest_path = Path(supervisor_manifest_path)
    manifest = _read_json(manifest_path)
    records = manifest.get("iteration_records")
    records = records if isinstance(records, list) else []
    latest = records[-1] if records and isinstance(records[-1], dict) else {}
    heartbeat_path = latest.get("heartbeat_path")
    status_path = latest.get("status_path")
    heartbeat = _read_json(Path(heartbeat_path)) if heartbeat_path else {}
    status = _read_json(Path(status_path)) if status_path else {}
    supervisor_status = manifest.get("supervisor_status")
    final_stop_reason = manifest.get("final_stop_reason")
    iterations_run = int(manifest.get("iterations_run", 0) or 0)
    total_cycles_run = int(manifest.get("total_cycles_run", 0) or 0)
    total_control_checks = int(manifest.get("total_control_checks", 0) or 0)
    readout_status = "QI_PERSISTENT_SUPERVISOR_STATUS_READ" if manifest else "QI_PERSISTENT_SUPERVISOR_STATUS_MISSING"
    active_like = bool(manifest) and final_stop_reason == "max_outer_iterations_reached"

    return KuuOSQiPersistentSupervisorStatusReadout(
        readout_version="kuuos_runtime_daemon_qi_persistent_supervisor_status_reader_v0_1",
        readout_status=readout_status,
        supervisor_manifest_path=str(manifest_path),
        supervisor_status=str(supervisor_status) if supervisor_status is not None else None,
        iterations_run=iterations_run,
        total_cycles_run=total_cycles_run,
        total_control_checks=total_control_checks,
        final_stop_reason=str(final_stop_reason) if final_stop_reason is not None else None,
        latest_iteration_index=latest.get("iteration_index") if latest else None,
        latest_heartbeat_path=str(heartbeat_path) if heartbeat_path else None,
        latest_status_path=str(status_path) if status_path else None,
        latest_heartbeat=heartbeat,
        latest_status=status,
        persistent_supervisor_active_like=active_like,
        readout_only=True,
        read_only=True,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Read KuuOS Qi persistent supervisor status v0.1")
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--write", type=Path, default=None)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = read_qi_persistent_supervisor_status(supervisor_manifest_path=args.manifest)
    if args.write:
        _write_json(args.write, result.to_dict())
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
