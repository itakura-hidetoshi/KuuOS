#!/usr/bin/env python3
"""Run one selected CI check and emit a compact audit receipt."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import pathlib
import shlex
import subprocess
import sys
import time
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_digest(path: pathlib.Path) -> str | None:
    try:
        return sha256_bytes(path.read_bytes())
    except OSError:
        return None


def load_selection(path: pathlib.Path | None) -> dict[str, Any] | None:
    if path is None:
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-id", required=True)
    parser.add_argument("--command", required=True)
    parser.add_argument("--selection", type=pathlib.Path)
    parser.add_argument("--output-root", type=pathlib.Path, default=ROOT / "artifacts" / "checks")
    return parser.parse_args()


def validator_digest(argv: list[str]) -> str | None:
    if len(argv) >= 2 and argv[0].endswith("python3"):
        candidate = ROOT / argv[1]
        if candidate.is_file():
            return file_digest(candidate)
    return None


def main() -> int:
    args = parse_args()
    argv = shlex.split(args.command)
    if not argv:
        print("ERROR: empty CI command", file=sys.stderr)
        return 2

    check_dir = args.output_root / args.check_id
    check_dir.mkdir(parents=True, exist_ok=True)
    log_path = check_dir / "check.log"
    receipt_path = check_dir / "receipt.json"

    selection_digest = file_digest(args.selection) if args.selection else None
    selection = load_selection(args.selection)
    input_material = json.dumps(
        {
            "check_id": args.check_id,
            "command": argv,
            "selection_digest": selection_digest,
            "sha": os.environ.get("GITHUB_SHA", ""),
        },
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

    started = dt.datetime.now(dt.timezone.utc)
    start_clock = time.monotonic()
    env = os.environ.copy()
    env.setdefault("PYTHONPATH", str(ROOT))
    env.setdefault("PYTHONUNBUFFERED", "1")
    if args.selection:
        env["KUUOS_CI_SELECTION"] = str(args.selection.resolve())
    if (
        args.check_id == "workflow-integrity"
        and selection is not None
        and bool(selection.get("full_audit_required", False))
    ):
        env["KUUOS_FULL_WORKFLOW_SCAN"] = "1"

    return_code = 1
    launch_error: str | None = None
    with log_path.open("w", encoding="utf-8") as log:
        log.write(f">>> {' '.join(argv)}\n")
        log.flush()
        try:
            process = subprocess.Popen(
                argv,
                cwd=ROOT,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )
            assert process.stdout is not None
            for line in process.stdout:
                sys.stdout.write(line)
                log.write(line)
            return_code = process.wait()
        except OSError as exc:
            launch_error = str(exc)
            message = f"ERROR: cannot launch check: {exc}\n"
            sys.stderr.write(message)
            log.write(message)
            return_code = 127

    finished = dt.datetime.now(dt.timezone.utc)
    receipt: dict[str, Any] = {
        "schema_version": "0.1",
        "check_id": args.check_id,
        "status": "passed" if return_code == 0 else "failed",
        "return_code": return_code,
        "command": argv,
        "duration_seconds": round(time.monotonic() - start_clock, 3),
        "started_at": started.isoformat(),
        "finished_at": finished.isoformat(),
        "git_sha": os.environ.get("GITHUB_SHA"),
        "run_id": os.environ.get("GITHUB_RUN_ID"),
        "run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
        "input_digest": sha256_bytes(input_material),
        "selection_digest": selection_digest,
        "validator_digest": validator_digest(argv),
        "full_workflow_scan": env.get("KUUOS_FULL_WORKFLOW_SCAN") == "1",
        "log": str(log_path.relative_to(ROOT)),
        "launch_error": launch_error,
        "authority_boundary": "validation != truth; CI pass != theorem authority",
    }
    receipt_path.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(receipt, ensure_ascii=False, indent=2))
    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
