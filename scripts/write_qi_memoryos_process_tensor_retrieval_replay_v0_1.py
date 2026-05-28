#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_daemon_qi_memoryos_process_tensor_retrieval_replay_v0_1 import build_qi_memoryos_process_tensor_retrieval_replay


def read_json(path: pathlib.Path | None):
    if path is None or not path.is_file():
        return []
    value = json.loads(path.read_text(encoding="utf-8"))
    return value


def normalize_entries(value) -> list[dict]:
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    if isinstance(value, dict):
        if isinstance(value.get("entries"), list):
            return [item for item in value["entries"] if isinstance(item, dict)]
        return [value]
    return []


def read_context(path: pathlib.Path | None) -> dict:
    if path is None or not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Write Qi MemoryOS process-tensor retrieval replay v0.1")
    parser.add_argument("--memory", type=pathlib.Path, required=True)
    parser.add_argument("--context", type=pathlib.Path, default=None)
    parser.add_argument("--write", type=pathlib.Path, required=True)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)
    result = build_qi_memoryos_process_tensor_retrieval_replay(
        memory_entries=normalize_entries(read_json(args.memory)),
        replay_context=read_context(args.context),
    )
    payload = result.to_dict()
    args.write.parent.mkdir(parents=True, exist_ok=True)
    args.write.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if not args.quiet:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.replay_status == "QI_MEMORYOS_PROCESS_TENSOR_RETRIEVAL_REPLAY_READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
