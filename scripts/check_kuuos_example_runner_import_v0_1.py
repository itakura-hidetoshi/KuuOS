#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.run_kuuos_state_io_example_v0_1 import DEFAULT_EVIDENCE, DEFAULT_RAW, build_parser


def main() -> int:
    errors: list[str] = []
    if not DEFAULT_RAW.is_file():
        errors.append(f"missing default raw state: {DEFAULT_RAW}")
    if not DEFAULT_EVIDENCE.is_file():
        errors.append(f"missing default evidence: {DEFAULT_EVIDENCE}")
    parser = build_parser()
    args = parser.parse_args([])
    if args.max_steps != 2:
        errors.append("default max_steps must be 2")
    if args.raw_state != DEFAULT_RAW:
        errors.append("default raw_state path mismatch")
    if args.evidence != DEFAULT_EVIDENCE:
        errors.append("default evidence path mismatch")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: KuuOS example runner import check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
