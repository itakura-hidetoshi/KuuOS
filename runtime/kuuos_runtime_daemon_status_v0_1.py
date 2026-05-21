#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import argparse
import json
from typing import Any, Mapping

NON_AUTHORITY_FLAGS = {
    "grants_execution_authority": False,
    "grants_truth_authority": False,
    "grants_final_commitment_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_clinical_authority": False,
    "grants_theorem_authority": False,
    "grants_completed_identity_authority": False,
}

@dataclass(frozen=True)
class KuuOSDaemonStatus:
    status_reader_version: str
    daemon_dir: str
    status: str
    stop_reason: str | None
    ticks_run: int
    latest_tick_index: int | None
    latest_tick_dir: str | None
    latest_step_trace_path: str | None
    latest_state_bundle_path: str | None
    latest_raw_state_path: str | None
    latest_qi_process_tensor_summary: dict[str, Any] | None
    daemon_result_path: str | None
    tick_log_path: str | None
    missing_files: list[str]
    grants_execution_authority: bool = False
    grants_truth_authority: bool = False
    grants_final_commitment_authority: bool = False
    grants_memory_overwrite_authority: bool = False
    grants_clinical_authority: bool = False
    grants_theorem_authority: bool = False
    grants_completed_identity_authority: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _summary_from_trace(trace_path: Path | None) -> dict[str, Any] | None:
    if trace_path is None or not trace_path.is_file():
        return None
    trace = _read_json(trace_path)
    if not isinstance(trace, list) or not trace:
        return None
    last = trace[-1]
    if not isinstance(last, Mapping):
        return None
    summary = last.get("qi_process_tensor_summary")
    if isinstance(summary, Mapping):
        return dict(summary)
    return None


def read_runtime_daemon_status(daemon_dir: Path) -> KuuOSDaemonStatus:
    daemon_dir = Path(daemon_dir)
    missing: list[str] = []
    tick_log_path = daemon_dir / "daemon_tick_log_v0_1.json"
    daemon_result_path = daemon_dir / "daemon_result_v0_1.json"

    if not daemon_dir.exists():
        return KuuOSDaemonStatus(
            status_reader_version="kuuos_runtime_daemon_status_v0_1",
            daemon_dir=str(daemon_dir),
            status="DAEMON_DIR_MISSING",
            stop_reason=None,
            ticks_run=0,
            latest_tick_index=None,
            latest_tick_dir=None,
            latest_step_trace_path=None,
            latest_state_bundle_path=None,
            latest_raw_state_path=None,
            latest_qi_process_tensor_summary=None,
            daemon_result_path=None,
            tick_log_path=None,
            missing_files=[str(daemon_dir)],
        )

    if not tick_log_path.is_file():
        missing.append(str(tick_log_path))
    if not daemon_result_path.is_file():
        missing.append(str(daemon_result_path))

    tick_log = []
    if tick_log_path.is_file():
        raw_log = _read_json(tick_log_path)
        if isinstance(raw_log, list):
            tick_log = raw_log
    daemon_result = {}
    if daemon_result_path.is_file():
        raw_result = _read_json(daemon_result_path)
        if isinstance(raw_result, Mapping):
            daemon_result = dict(raw_result)

    latest = tick_log[-1] if tick_log and isinstance(tick_log[-1], Mapping) else None
    latest_tick_index = latest.get("tick_index") if latest else None
    latest_tick_dir = latest.get("output_dir") if latest else None
    latest_trace = Path(latest.get("step_trace_path")) if latest and latest.get("step_trace_path") else None
    latest_bundle = Path(latest.get("state_bundle_path")) if latest and latest.get("state_bundle_path") else None
    latest_raw = Path(latest.get("next_raw_state_path")) if latest and latest.get("next_raw_state_path") else None

    for maybe_path in [latest_trace, latest_bundle, latest_raw]:
        if maybe_path is not None and not maybe_path.is_file():
            missing.append(str(maybe_path))

    summary = _summary_from_trace(latest_trace)
    status = "DAEMON_STATUS_READY" if not missing else "DAEMON_STATUS_INCOMPLETE"
    return KuuOSDaemonStatus(
        status_reader_version="kuuos_runtime_daemon_status_v0_1",
        daemon_dir=str(daemon_dir),
        status=status,
        stop_reason=daemon_result.get("stop_reason"),
        ticks_run=int(daemon_result.get("ticks_run", len(tick_log)) or 0),
        latest_tick_index=int(latest_tick_index) if latest_tick_index is not None else None,
        latest_tick_dir=str(latest_tick_dir) if latest_tick_dir else None,
        latest_step_trace_path=str(latest_trace) if latest_trace else None,
        latest_state_bundle_path=str(latest_bundle) if latest_bundle else None,
        latest_raw_state_path=str(latest_raw) if latest_raw else None,
        latest_qi_process_tensor_summary=summary,
        daemon_result_path=str(daemon_result_path) if daemon_result_path.is_file() else None,
        tick_log_path=str(tick_log_path) if tick_log_path.is_file() else None,
        missing_files=missing,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Read KuuOS runtime daemon status v0.1")
    parser.add_argument("--daemon-dir", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    status = read_runtime_daemon_status(args.daemon_dir)
    print(json.dumps(status.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if status.status == "DAEMON_STATUS_READY" else 1

if __name__ == "__main__":
    raise SystemExit(main())
