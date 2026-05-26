#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_daemon_qi_persistent_supervisor_status_view_v0_1 import compile_qi_persistent_supervisor_status_view
from runtime.kuuos_runtime_daemon_qi_process_tensor_probe_plan_artifact_writer_v0_1 import build_qi_process_tensor_probe_plan_artifact


def read_json(path: pathlib.Path) -> dict:
    if not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def write_json(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Write KuuOS Qi process tensor probe plan artifact v0.1")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--status-view", type=pathlib.Path)
    source.add_argument("--out-dir", type=pathlib.Path)
    parser.add_argument("--write", type=pathlib.Path, required=True)
    parser.add_argument("--quiet", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.status_view:
        status_view = read_json(args.status_view)
    else:
        status_view = compile_qi_persistent_supervisor_status_view(out_dir=args.out_dir).to_dict()
    artifact = build_qi_process_tensor_probe_plan_artifact(status_view=status_view)
    write_json(args.write, artifact.to_dict())
    if not args.quiet:
        print(json.dumps(artifact.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if artifact.artifact_status == "QI_PROCESS_TENSOR_PROBE_PLAN_ARTIFACT_READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
