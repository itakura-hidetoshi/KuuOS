#!/usr/bin/env python3
import argparse
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--index", type=int, required=True)
parser.add_argument("--count", type=int, default=8)
args = parser.parse_args()
if args.index < 0 or args.index >= args.count:
    raise SystemExit("invalid shard index")

check_id = f"full-governance-{args.index:02d}"
command = (
    "python3 scripts/run_all_governance_shard_v0_2.py "
    f"--index {args.index} --count {args.count} "
    f"--output artifacts/governance-shards/{args.index}/summary.json"
)
result = subprocess.run(
    [
        sys.executable,
        "scripts/run_ci_check.py",
        "--check-id",
        check_id,
        "--command",
        command,
    ],
    cwd=ROOT,
    check=False,
)
raise SystemExit(result.returncode)
