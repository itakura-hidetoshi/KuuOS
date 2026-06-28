#!/usr/bin/env python3
"""Run one deterministic shard of the repository-wide governance audit.

The command inventory remains defined by run_all_governance_full_checks_v0_1.
Sharding changes execution scheduling only. It does not change validation,
truth, theorem, release, institutional, or execution authority.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import pathlib
import subprocess
import sys
import time
from collections.abc import Sequence
from typing import Any

from run_all_governance_full_checks_v0_1 import COMMANDS

ROOT = pathlib.Path(__file__).resolve().parents[1]


def partition_commands(
    commands: Sequence[Sequence[str]],
    shard_count: int,
) -> list[list[list[str]]]:
    if shard_count <= 0:
        raise ValueError("shard_count must be positive")
    shards: list[list[list[str]]] = [[] for _ in range(shard_count)]
    for index, command in enumerate(commands):
        shards[index % shard_count].append(list(command))
    return shards


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", type=int, required=True)
    parser.add_argument("--count", type=int, required=True)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    return parser.parse_args()


def run_command(command: Sequence[str], env: dict[str, str]) -> dict[str, Any]:
    started = dt.datetime.now(dt.timezone.utc)
    start_clock = time.monotonic()
    print("\n>>> " + " ".join(command), flush=True)
    completed = subprocess.run(list(command), cwd=ROOT, env=env, check=False)
    finished = dt.datetime.now(dt.timezone.utc)
    return {
        "command": list(command),
        "status": "passed" if completed.returncode == 0 else "failed",
        "return_code": completed.returncode,
        "duration_seconds": round(time.monotonic() - start_clock, 3),
        "started_at": started.isoformat(),
        "finished_at": finished.isoformat(),
    }


def main() -> int:
    args = parse_args()
    try:
        shards = partition_commands(COMMANDS, args.count)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if args.index < 0 or args.index >= args.count:
        print("ERROR: shard index outside [0, count)", file=sys.stderr)
        return 2

    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(
        item for item in (str(ROOT), env.get("PYTHONPATH", "")) if item
    )
    env.setdefault("PYTHONUNBUFFERED", "1")

    results = [run_command(command, env) for command in shards[args.index]]
    failures = [result for result in results if result["status"] != "passed"]
    summary = {
        "schema_version": "0.2",
        "shard_index": args.index,
        "shard_count": args.count,
        "inventory_size": len(COMMANDS),
        "selected_count": len(results),
        "status": "passed" if not failures else "failed",
        "results": results,
        "failed_commands": [result["command"] for result in failures],
        "authority_boundary": (
            "validation != truth; CI pass != theorem authority; "
            "sharding != authority expansion"
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
