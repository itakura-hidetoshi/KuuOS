#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "write_qi_license_candidate_phase_v0_1.py"
PHASE = ROOT / "packets" / "qi_process_tensor_review_phase_boundary_packet_v0_1.json"


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def require_no_authority(payload: dict, errors: list[str], prefix: str) -> None:
    if payload.get("authority") != "none":
        errors.append(f"{prefix}:authority_not_none")
    for key in [
        "grants_execution_authority",
        "grants_probe_execution_authority",
        "grants_dry_run_execution_authority",
        "grants_next_tick_execution_authority",
        "grants_control_packet_authority",
        "grants_memory_overwrite_authority",
        "grants_world_update_authority",
    ]:
        if payload.get(key) is not False:
            errors.append(f"{prefix}:{key}_not_false")


def main() -> int:
    errors: list[str] = []
    for path in [CLI, PHASE]:
        if not path.is_file():
            errors.append(f"missing:{path}")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1

    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        summary = root / "summary.json"
        ready_candidate = root / "candidate_ready.json"
        blocked_candidate = root / "candidate_blocked.json"
        dump(summary, {
            "summary_status": "QI_PROCESS_TENSOR_PROBE_PLAN_TREND_SUMMARY_READY",
            "qi_process_tensor_characterization": "observation_debt_limited_qi_process_tensor",
            "summary_only": True,
            "read_only": True,
            "authority": "none",
            "grants_execution_authority": False,
            "grants_probe_execution_authority": False,
            "grants_next_tick_execution_authority": False,
            "grants_control_packet_authority": False,
            "grants_memory_overwrite_authority": False,
        })

        ok = subprocess.run([
            sys.executable, str(CLI),
            "--trend-summary", str(summary),
            "--phase-packet", str(PHASE),
            "--mode", "dry_run_probe_simulation",
            "--write", str(ready_candidate),
            "--quiet",
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if ok.returncode != 0:
            errors.append(f"ready_candidate_returned:{ok.returncode}")
            errors.append(ok.stderr.strip() or ok.stdout.strip())
        if ready_candidate.is_file():
            candidate = load(ready_candidate)
            if candidate.get("gate_status") != "QI_ACTUATION_LICENSE_DRY_RUN_CANDIDATE_READY":
                errors.append("ready_candidate_status_mismatch")
            if candidate.get("source_phase_status") != "QI_PROCESS_TENSOR_REVIEW_PHASE_BOUNDARY_READY":
                errors.append("source_phase_status_mismatch")
            require_no_authority(candidate, errors, "ready_candidate")
        else:
            errors.append("ready_candidate_missing")

        bad = subprocess.run([
            sys.executable, str(CLI),
            "--trend-summary", str(summary),
            "--phase-packet", str(PHASE),
            "--mode", "probe_execution",
            "--write", str(blocked_candidate),
            "--quiet",
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if bad.returncode == 0:
            errors.append("blocked_candidate_should_return_nonzero")
        if blocked_candidate.is_file():
            blocked = load(blocked_candidate)
            if blocked.get("gate_status") != "QI_ACTUATION_LICENSE_GATE_BLOCKED":
                errors.append("blocked_candidate_status_mismatch")
            if "non_dry_run_actuation_not_allowed_v0_1" not in blocked.get("gate_blockers", []):
                errors.append("blocked_candidate_reason_missing")
            require_no_authority(blocked, errors, "blocked_candidate")
        else:
            errors.append("blocked_candidate_missing")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi phase-boundary license gate check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
