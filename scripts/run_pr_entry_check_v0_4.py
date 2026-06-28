#!/usr/bin/env python3
"""Run a migrated pull-request check and preserve subsystem evidence.

This runner centralizes scheduling only. It does not weaken subsystem validators
or expand execution, theorem, release, clinical, institutional, or truth
authority.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import shutil
import subprocess
import sys
import time
from collections.abc import Sequence
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CHECK_IDS = {
    "memoryos-json",
    "qi-process-review",
    "kustring-finality",
}


def build_commands(check_id: str, output_dir: pathlib.Path) -> list[list[str]]:
    python = sys.executable
    if check_id == "memoryos-json":
        return [[
            python,
            "tools/memoryos/json_governance_guard.py",
            "--repo-root",
            ".",
            "--current",
            "memoryos/ops/current",
            "--prev",
            "memoryos/ops/prev",
            "--out-dir",
            str(output_dir / "domain"),
        ]]
    if check_id == "qi-process-review":
        return [
            [
                python,
                "scripts/run_qi_process_tensor_review_checks_v0_1.py",
                "--write-json",
                str(output_dir / "process_tensor_review_check_suite.json"),
            ],
            [python, "scripts/run_qi_cf_lattice_checks_v0_1.py"],
            [python, "scripts/run_qi_process_tensor_scheduler_checks_v0_1.py"],
            [python, "scripts/run_qi_v02_memoryos_replay_loop_closure_checks.py"],
            [
                python,
                "scripts/check_qi_process_tensor_review_v02_closed_loop_workflow_addendum_v0_1.py",
            ],
            [python, "scripts/check_kuuos_causal_world_model_os_v14_0.py"],
        ]
    if check_id == "kustring-finality":
        return [
            [python, "scripts/run_kustring_runtime_finality_suite_v0_2.py"],
            [python, "scripts/build_kustring_runtime_finality_report_v0_2.py"],
        ]
    raise ValueError(f"unsupported check id: {check_id}")


def run_command(command: Sequence[str]) -> dict[str, Any]:
    started = dt.datetime.now(dt.timezone.utc)
    start_clock = time.monotonic()
    print("\n>>> " + " ".join(command), flush=True)
    completed = subprocess.run(list(command), cwd=ROOT, check=False)
    finished = dt.datetime.now(dt.timezone.utc)
    return {
        "command": list(command),
        "status": "passed" if completed.returncode == 0 else "failed",
        "return_code": completed.returncode,
        "duration_seconds": round(time.monotonic() - start_clock, 3),
        "started_at": started.isoformat(),
        "finished_at": finished.isoformat(),
    }


def preserve_generated_outputs(check_id: str, output_dir: pathlib.Path) -> list[str]:
    preserved: list[str] = []
    if check_id == "kustring-finality":
        source = ROOT / "specs/kustring_runtime_finality_report_v0_2.generated.json"
        if source.is_file():
            target = output_dir / source.name
            shutil.copy2(source, target)
            preserved.append(str(target.relative_to(ROOT)))
    return preserved


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-id", required=True, choices=sorted(CHECK_IDS))
    parser.add_argument("--output-root", type=pathlib.Path, default=ROOT / "artifacts/checks")
    args = parser.parse_args()

    output_root = args.output_root if args.output_root.is_absolute() else ROOT / args.output_root
    output_dir = output_root / args.check_id
    output_dir.mkdir(parents=True, exist_ok=True)
    commands = build_commands(args.check_id, output_dir)
    results = [run_command(command) for command in commands]
    preserved = preserve_generated_outputs(args.check_id, output_dir)
    failures = [result for result in results if result["status"] != "passed"]

    summary = {
        "schema_version": "0.4",
        "check_id": args.check_id,
        "status": "passed" if not failures else "failed",
        "command_count": len(results),
        "results": results,
        "failed_commands": [result["command"] for result in failures],
        "preserved_outputs": preserved,
        "authority_boundary": (
            "central scheduling != validator weakening; validation != truth; "
            "CI pass != theorem or institutional authority"
        ),
    }
    summary_path = output_dir / "subsystem-summary.json"
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
