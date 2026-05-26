#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_daemon_qi_actuation_license_gate_v0_1 import build_qi_actuation_license_candidate


def read_json(path: pathlib.Path) -> dict:
    if not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def write_json(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Write KuuOS Qi actuation license candidate v0.1")
    parser.add_argument("--trend-summary", type=pathlib.Path, required=True)
    parser.add_argument("--finality-packet", type=pathlib.Path, required=True)
    parser.add_argument("--requested-actuation-mode", type=str, default="dry_run_probe_simulation")
    parser.add_argument("--write", type=pathlib.Path, required=True)
    parser.add_argument("--quiet", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    candidate = build_qi_actuation_license_candidate(
        trend_summary=read_json(args.trend_summary),
        finality_packet=read_json(args.finality_packet),
        requested_actuation_mode=args.requested_actuation_mode,
    )
    write_json(args.write, candidate.to_dict())
    if not args.quiet:
        print(json.dumps(candidate.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if candidate.gate_status == "QI_ACTUATION_LICENSE_DRY_RUN_CANDIDATE_READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
