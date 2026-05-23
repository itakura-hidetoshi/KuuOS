#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_daemon_qi_process_tensor_bounded_tick_executor_v0_1 import (  # noqa: E402
    read_and_run_qi_process_tensor_bounded_tick_executor,
)


def _write_json(path: pathlib.Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Manually invoke one Qi Process Tensor bounded tick from daemon receipts v0.1"
    )
    parser.add_argument("--daemon-dir", type=pathlib.Path, required=True)
    parser.add_argument("--raw-state", type=pathlib.Path, required=True)
    parser.add_argument("--evidence", type=pathlib.Path, required=True)
    parser.add_argument("--output-dir", type=pathlib.Path, required=True)
    parser.add_argument("--state-bundle", type=pathlib.Path, default=None)
    parser.add_argument("--requested-invocation-depth", type=int, default=0)
    parser.add_argument("--write", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    receipt = read_and_run_qi_process_tensor_bounded_tick_executor(
        daemon_dir=args.daemon_dir,
        raw_state_path=args.raw_state,
        evidence_path=args.evidence,
        output_dir=args.output_dir,
        state_bundle_path=args.state_bundle,
        requested_invocation_depth=args.requested_invocation_depth,
    )
    payload = receipt.to_dict()
    if args.write:
        _write_json(
            args.daemon_dir / "daemon_qi_process_tensor_bounded_tick_executor_receipt_v0_1.json",
            payload,
        )
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
