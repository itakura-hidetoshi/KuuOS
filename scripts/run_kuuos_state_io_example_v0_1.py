#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import sys
from datetime import datetime, timezone
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_state_io_runner_v0_1 import run_state_io

DEFAULT_RAW = ROOT / "examples" / "qi_state_io_v0_1" / "raw_state.json"
DEFAULT_EVIDENCE = ROOT / "examples" / "qi_state_io_v0_1" / "evidence.json"
DEFAULT_RUN_ROOT = ROOT / "runs" / "qi_state_io_v0_1"


def _default_output_dir() -> pathlib.Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return DEFAULT_RUN_ROOT / stamp


def _print_summary(manifest: Any) -> None:
    payload = manifest.to_dict()
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    print()
    print("KuuOS state IO example completed.")
    print(f"result: {payload['result_path']}")
    print(f"next_raw_state: {payload['next_raw_state_path']}")
    print(f"state_bundle: {payload['state_bundle_path']}")
    print(f"step_trace: {payload['step_trace_path']}")
    print(f"run_manifest: {pathlib.Path(payload['result_path']).parent / 'run_manifest_v0_1.json'}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the KuuOS Qi state IO example v0.1")
    parser.add_argument("--raw-state", type=pathlib.Path, default=DEFAULT_RAW)
    parser.add_argument("--evidence", type=pathlib.Path, default=DEFAULT_EVIDENCE)
    parser.add_argument("--output-dir", type=pathlib.Path, default=None)
    parser.add_argument("--state-bundle", type=pathlib.Path, default=None)
    parser.add_argument("--max-steps", type=int, default=2)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    output_dir = args.output_dir or _default_output_dir()
    manifest = run_state_io(
        raw_state_path=args.raw_state,
        evidence_path=args.evidence,
        output_dir=output_dir,
        max_steps=args.max_steps,
        state_bundle_path=args.state_bundle,
    )
    _print_summary(manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
