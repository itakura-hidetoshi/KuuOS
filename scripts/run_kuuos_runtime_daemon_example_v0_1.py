#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import sys
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_daemon_v0_1 import run_runtime_daemon

DEFAULT_RAW = ROOT / "examples" / "qi_process_tensor_v0_1" / "raw_state_process_history.json"
DEFAULT_EVIDENCE = ROOT / "examples" / "qi_process_tensor_v0_1" / "evidence.json"
DEFAULT_RUN_ROOT = ROOT / "runs" / "runtime_daemon_v0_1"


def default_daemon_dir() -> pathlib.Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return DEFAULT_RUN_ROOT / stamp


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run bounded KuuOS runtime daemon example v0.1")
    parser.add_argument("--raw-state", type=pathlib.Path, default=DEFAULT_RAW)
    parser.add_argument("--evidence", type=pathlib.Path, default=DEFAULT_EVIDENCE)
    parser.add_argument("--daemon-dir", type=pathlib.Path, default=None)
    parser.add_argument("--state-bundle", type=pathlib.Path, default=None)
    parser.add_argument("--max-ticks", type=int, default=2)
    parser.add_argument("--max-steps-per-tick", type=int, default=1)
    parser.add_argument("--sleep-seconds", type=float, default=0.0)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    daemon_dir = args.daemon_dir or default_daemon_dir()
    result = run_runtime_daemon(
        raw_state_path=args.raw_state,
        evidence_path=args.evidence,
        daemon_dir=daemon_dir,
        max_ticks=args.max_ticks,
        max_steps_per_tick=args.max_steps_per_tick,
        sleep_seconds=args.sleep_seconds,
        state_bundle_path=args.state_bundle,
    )
    payload = result.to_dict()
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    print()
    print("KuuOS runtime daemon example completed.")
    print(f"daemon_dir: {payload['daemon_dir']}")
    print(f"tick_log: {payload['tick_log_path']}")
    print(f"final_raw_state: {payload['final_raw_state_path']}")
    print(f"final_state_bundle: {payload['final_state_bundle_path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
