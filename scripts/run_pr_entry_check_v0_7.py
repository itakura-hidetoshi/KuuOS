#!/usr/bin/env python3
"""Run focused checks migrated from independent pull-request workflows."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import subprocess
import sys
import time
from collections.abc import Sequence
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CHECK_IDS = {"core-autonomy-v01", "belief-os-v01", "review-seal-v01"}


def build_commands(check_id: str, output_dir: pathlib.Path) -> list[list[str]]:
    python = sys.executable
    if check_id == "core-autonomy-v01":
        return [
            [python, "scripts/validate_kuuos_core_autonomy_contract_v0_1.py"],
            [
                python,
                "scripts/run_kuuos_core_autonomy_v0_1.py",
                "--mode",
                "contract-check",
                "--audit-log",
                str(output_dir / "contract-check.jsonl"),
            ],
            [
                python,
                "scripts/run_kuuos_core_autonomy_v0_1.py",
                "--mode",
                "once",
                "--self-test-check",
                "--audit-log",
                str(output_dir / "once-self-test.jsonl"),
            ],
        ]
    if check_id == "belief-os-v01":
        return [
            [
                python,
                "-m",
                "compileall",
                "-q",
                "runtime",
                "scripts/check_belief_os_relational_conditional_kernel_v0_1.py",
            ],
            [python, "-m", "runtime.v01_belief_os_relational_conditional_kernel"],
            [python, "scripts/check_belief_os_relational_conditional_kernel_v0_1.py"],
        ]
    if check_id == "review-seal-v01":
        return [[python, "scripts/validate_kuuos_review_seal_os_bridge_v0_1_min.py"]]
    raise ValueError(f"unsupported check id: {check_id}")


def run_command(command: Sequence[str], log_path: pathlib.Path) -> dict[str, Any]:
    started = dt.datetime.now(dt.timezone.utc)
    start_clock = time.monotonic()
    print("\n>>> " + " ".join(command), flush=True)
    with log_path.open("a", encoding="utf-8") as log:
        log.write("\n>>> " + " ".join(command) + "\n")
        completed = subprocess.run(
            list(command),
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        output = completed.stdout or ""
        print(output, end="", flush=True)
        log.write(output)
    return {
        "command": list(command),
        "status": "passed" if completed.returncode == 0 else "failed",
        "return_code": completed.returncode,
        "duration_seconds": round(time.monotonic() - start_clock, 3),
        "started_at": started.isoformat(),
        "finished_at": dt.datetime.now(dt.timezone.utc).isoformat(),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-id", required=True, choices=sorted(CHECK_IDS))
    parser.add_argument("--output-root", type=pathlib.Path, default=ROOT / "artifacts/checks")
    args = parser.parse_args()

    output_root = args.output_root if args.output_root.is_absolute() else ROOT / args.output_root
    output_dir = output_root / args.check_id
    output_dir.mkdir(parents=True, exist_ok=True)
    log_path = output_dir / "focused-check.log"
    results = [
        run_command(command, log_path)
        for command in build_commands(args.check_id, output_dir)
    ]
    failures = [result for result in results if result["status"] != "passed"]
    summary = {
        "schema_version": "0.7",
        "check_id": args.check_id,
        "status": "passed" if not failures else "failed",
        "command_count": len(results),
        "results": results,
        "failed_commands": [result["command"] for result in failures],
        "authority_boundary": (
            "central scheduling != validator weakening; validation != truth; "
            "CI pass != theorem, execution, clinical, or institutional authority"
        ),
    }
    (output_dir / "subsystem-summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
