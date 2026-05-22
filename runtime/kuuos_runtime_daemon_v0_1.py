#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
import argparse
import json
import time
from typing import Any

try:
    from runtime.kuuos_state_io_runner_v0_1 import run_state_io
    from runtime.kuuos_runtime_daemon_yinyang_polarity_gauge_v0_1 import read_and_evaluate_daemon_yinyang_polarity
    from runtime.kuuos_runtime_daemon_four_image_phase_gauge_v0_1 import read_and_evaluate_daemon_four_image_phase
    from runtime.kuuos_runtime_daemon_qi_policy_v0_1 import read_and_evaluate_daemon_qi_policy
    from runtime.kuuos_runtime_daemon_emptiness_gate_v0_1 import read_and_evaluate_daemon_emptiness_gate
    from runtime.kuuos_runtime_daemon_wa_function_v0_1 import read_and_evaluate_daemon_wa_function
except ModuleNotFoundError:
    from kuuos_state_io_runner_v0_1 import run_state_io
    from kuuos_runtime_daemon_yinyang_polarity_gauge_v0_1 import read_and_evaluate_daemon_yinyang_polarity
    from kuuos_runtime_daemon_four_image_phase_gauge_v0_1 import read_and_evaluate_daemon_four_image_phase
    from kuuos_runtime_daemon_qi_policy_v0_1 import read_and_evaluate_daemon_qi_policy
    from kuuos_runtime_daemon_emptiness_gate_v0_1 import read_and_evaluate_daemon_emptiness_gate
    from kuuos_runtime_daemon_wa_function_v0_1 import read_and_evaluate_daemon_wa_function

NON_AUTHORITY_FLAGS = {
    "grants_execution_authority": False,
    "grants_truth_authority": False,
    "grants_final_commitment_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_clinical_authority": False,
    "grants_theorem_authority": False,
    "grants_completed_identity_authority": False,
}

STOP_REASONS = {
    "WAITING_FOR_MORE_EVIDENCE",
    "QUARANTINE_RETAINED",
    "UNKNOWN_RESULT_HELD",
}

@dataclass(frozen=True)
class KuuOSDaemonResult:
    daemon_status: str
    stop_reason: str
    ticks_run: int
    daemon_dir: str
    tick_log_path: str
    final_raw_state_path: str | None
    final_state_bundle_path: str | None
    yinyang_polarity_result_path: str | None = None
    yinyang_polarity_state: str | None = None
    four_image_phase_result_path: str | None = None
    four_image_phase: str | None = None
    qi_policy_result_path: str | None = None
    qi_policy_recommended_tick_mode: str | None = None
    emptiness_gate_result_path: str | None = None
    emptiness_recommended_action: str | None = None
    wa_function_result_path: str | None = None
    recommended_runtime_posture: str | None = None
    grants_execution_authority: bool = False
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


def _utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _tick_output_dir(daemon_dir: Path, tick_index: int) -> Path:
    return daemon_dir / f"tick_{tick_index:04d}_{_utc_stamp()}"


def _daemon_status_from_stop_reason(stop_reason: str) -> str:
    if stop_reason == "MAX_TICKS_REACHED":
        return "DAEMON_MAX_TICKS_REACHED_APPEND_ONLY"
    if stop_reason == "WAITING_FOR_MORE_EVIDENCE":
        return "DAEMON_WAITING_APPEND_ONLY"
    if stop_reason == "QUARANTINE_RETAINED":
        return "DAEMON_QUARANTINE_RETAINED_APPEND_ONLY"
    return "DAEMON_STOPPED_APPEND_ONLY"


def run_runtime_daemon(
    *,
    raw_state_path: Path,
    evidence_path: Path,
    daemon_dir: Path,
    max_ticks: int = 3,
    max_steps_per_tick: int = 1,
    sleep_seconds: float = 0.0,
    state_bundle_path: Path | None = None,
) -> KuuOSDaemonResult:
    if max_ticks < 1:
        max_ticks = 1
    if max_ticks > 100:
        max_ticks = 100
    if max_steps_per_tick < 1:
        max_steps_per_tick = 1
    if max_steps_per_tick > 25:
        max_steps_per_tick = 25
    if sleep_seconds < 0:
        sleep_seconds = 0.0

    daemon_dir.mkdir(parents=True, exist_ok=True)
    current_raw_path = raw_state_path
    current_bundle_path = state_bundle_path
    tick_log: list[dict[str, Any]] = []
    stop_reason = "MAX_TICKS_REACHED"
    final_raw: Path | None = None
    final_bundle: Path | None = None

    for tick_index in range(max_ticks):
        out_dir = _tick_output_dir(daemon_dir, tick_index)
        manifest = run_state_io(
            raw_state_path=current_raw_path,
            evidence_path=evidence_path,
            output_dir=out_dir,
            max_steps=max_steps_per_tick,
            state_bundle_path=current_bundle_path,
        )
        entry = {
            "tick_index": tick_index,
            "started_raw_state_path": str(current_raw_path),
            "input_state_bundle_path": str(current_bundle_path) if current_bundle_path else None,
            "output_dir": str(out_dir),
            "run_status": manifest.run_status,
            "stop_reason": manifest.stop_reason,
            "steps_run": manifest.steps_run,
            "next_raw_state_path": manifest.next_raw_state_path,
            "state_bundle_path": manifest.state_bundle_path,
            "step_trace_path": manifest.step_trace_path,
            **NON_AUTHORITY_FLAGS,
        }
        tick_log.append(entry)
        final_raw = Path(manifest.next_raw_state_path)
        final_bundle = Path(manifest.state_bundle_path)
        current_raw_path = final_raw
        current_bundle_path = final_bundle
        if manifest.stop_reason in STOP_REASONS:
            stop_reason = manifest.stop_reason
            break
        if tick_index < max_ticks - 1 and sleep_seconds:
            time.sleep(sleep_seconds)
    else:
        stop_reason = "MAX_TICKS_REACHED"

    tick_log_path = daemon_dir / "daemon_tick_log_v0_1.json"
    _write_json(tick_log_path, tick_log)
    daemon_status = _daemon_status_from_stop_reason(stop_reason)
    daemon_result_path = daemon_dir / "daemon_result_v0_1.json"

    provisional_result = KuuOSDaemonResult(
        daemon_status=daemon_status,
        stop_reason=stop_reason,
        ticks_run=len(tick_log),
        daemon_dir=str(daemon_dir),
        tick_log_path=str(tick_log_path),
        final_raw_state_path=str(final_raw) if final_raw else None,
        final_state_bundle_path=str(final_bundle) if final_bundle else None,
    )
    _write_json(daemon_result_path, provisional_result.to_dict())

    yinyang_result = read_and_evaluate_daemon_yinyang_polarity(daemon_dir)
    yinyang_result_path = daemon_dir / "daemon_yinyang_polarity_result_v0_1.json"
    _write_json(yinyang_result_path, yinyang_result.to_dict())

    four_image_result = read_and_evaluate_daemon_four_image_phase(daemon_dir)
    four_image_result_path = daemon_dir / "daemon_four_image_phase_result_v0_1.json"
    _write_json(four_image_result_path, four_image_result.to_dict())

    policy_result = read_and_evaluate_daemon_qi_policy(daemon_dir)
    policy_result_path = daemon_dir / "daemon_qi_policy_result_v0_1.json"
    _write_json(policy_result_path, policy_result.to_dict())

    emptiness_result = read_and_evaluate_daemon_emptiness_gate(daemon_dir)
    emptiness_result_path = daemon_dir / "daemon_emptiness_gate_result_v0_1.json"
    _write_json(emptiness_result_path, emptiness_result.to_dict())

    wa_result = read_and_evaluate_daemon_wa_function(daemon_dir)
    wa_result_path = daemon_dir / "daemon_wa_function_result_v0_1.json"
    _write_json(wa_result_path, wa_result.to_dict())

    result = KuuOSDaemonResult(
        daemon_status=daemon_status,
        stop_reason=stop_reason,
        ticks_run=len(tick_log),
        daemon_dir=str(daemon_dir),
        tick_log_path=str(tick_log_path),
        final_raw_state_path=str(final_raw) if final_raw else None,
        final_state_bundle_path=str(final_bundle) if final_bundle else None,
        yinyang_polarity_result_path=str(yinyang_result_path),
        yinyang_polarity_state=yinyang_result.yinyang_polarity_state,
        four_image_phase_result_path=str(four_image_result_path),
        four_image_phase=four_image_result.four_image_phase,
        qi_policy_result_path=str(policy_result_path),
        qi_policy_recommended_tick_mode=policy_result.recommended_tick_mode,
        emptiness_gate_result_path=str(emptiness_result_path),
        emptiness_recommended_action=emptiness_result.recommended_emptiness_action,
        wa_function_result_path=str(wa_result_path),
        recommended_runtime_posture=wa_result.recommended_runtime_posture,
    )
    _write_json(daemon_result_path, result.to_dict())
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run bounded KuuOS runtime daemon v0.1")
    parser.add_argument("--raw-state", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--daemon-dir", type=Path, required=True)
    parser.add_argument("--max-ticks", type=int, default=3)
    parser.add_argument("--max-steps-per-tick", type=int, default=1)
    parser.add_argument("--sleep-seconds", type=float, default=0.0)
    parser.add_argument("--state-bundle", type=Path, default=None)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = run_runtime_daemon(
        raw_state_path=args.raw_state,
        evidence_path=args.evidence,
        daemon_dir=args.daemon_dir,
        max_ticks=args.max_ticks,
        max_steps_per_tick=args.max_steps_per_tick,
        sleep_seconds=args.sleep_seconds,
        state_bundle_path=args.state_bundle,
    )
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
