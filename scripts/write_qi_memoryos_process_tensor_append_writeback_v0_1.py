#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_daemon_qi_memoryos_process_tensor_append_writeback_v0_1 import run_qi_memoryos_process_tensor_append_writeback


def read_json(path: pathlib.Path | None) -> dict:
    if path is None or not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Write Qi MemoryOS process-tensor append writeback v0.1")
    parser.add_argument("--probe-result", type=pathlib.Path, required=True)
    parser.add_argument("--context", type=pathlib.Path, default=None)
    parser.add_argument("--write", type=pathlib.Path, required=True)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)
    result = run_qi_memoryos_process_tensor_append_writeback(
        probe_result=read_json(args.probe_result),
        writeback_context=read_json(args.context),
    )
    payload = result.to_dict()
    args.write.parent.mkdir(parents=True, exist_ok=True)
    args.write.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if not args.quiet:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.writeback_status == "QI_MEMORYOS_PROCESS_TENSOR_APPEND_WRITEBACK_PERFORMED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
