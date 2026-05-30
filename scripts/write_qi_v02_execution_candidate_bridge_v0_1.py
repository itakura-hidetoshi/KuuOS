#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_daemon_qi_v02_execution_candidate_bridge_v0_1 import build_qi_v02_execution_candidate_bridge


def read_json(path: pathlib.Path | None) -> dict:
    if path is None or not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Write Qi v0.2 execution candidate bridge v0.1")
    parser.add_argument("--v02-scheduler", type=pathlib.Path, required=True)
    parser.add_argument("--write", type=pathlib.Path, required=True)
    parser.add_argument("--write-candidate", type=pathlib.Path, default=None)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)
    result = build_qi_v02_execution_candidate_bridge(v02_scheduler_surface=read_json(args.v02_scheduler))
    payload = result.to_dict()
    args.write.parent.mkdir(parents=True, exist_ok=True)
    args.write.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_candidate is not None and result.bridge_status == "QI_V02_EXECUTION_CANDIDATE_BRIDGE_READY":
        args.write_candidate.parent.mkdir(parents=True, exist_ok=True)
        args.write_candidate.write_text(json.dumps(result.candidate_packet, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if not args.quiet:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.bridge_status == "QI_V02_EXECUTION_CANDIDATE_BRIDGE_READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
