#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_daemon_qi_process_tensor_probe_plan_artifact_index_v0_1 import build_qi_process_tensor_probe_plan_artifact_index


def read_json(path: pathlib.Path) -> dict:
    if not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def write_json(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Write KuuOS Qi process tensor probe plan artifact index v0.1")
    parser.add_argument("--artifact", type=pathlib.Path, action="append", required=True)
    parser.add_argument("--write", type=pathlib.Path, required=True)
    parser.add_argument("--quiet", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    artifacts = [read_json(path) for path in args.artifact]
    index = build_qi_process_tensor_probe_plan_artifact_index(artifacts=artifacts)
    write_json(args.write, index.to_dict())
    if not args.quiet:
        print(json.dumps(index.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if index.index_status == "QI_PROCESS_TENSOR_PROBE_PLAN_ARTIFACT_INDEX_READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
