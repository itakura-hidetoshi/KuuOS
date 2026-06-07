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

from runtime.kuuos_runtime_daemon_tri_os_compatibility_handoff_emitter_v8_9 import build_tri_os_compatibility_handoff_emitter


def read_json(path: pathlib.Path | None) -> dict[str, Any]:
    if path is None or not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Tri-OS compatibility handoff emitter v8.9")
    parser.add_argument("--context", type=pathlib.Path, required=True)
    parser.add_argument("--license", type=pathlib.Path, required=True)
    parser.add_argument("--write", type=pathlib.Path, required=True)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)
    result = build_tri_os_compatibility_handoff_emitter(
        runtime_context=read_json(args.context),
        tri_os_handoff_license=read_json(args.license),
    )
    payload = result.to_dict()
    args.write.parent.mkdir(parents=True, exist_ok=True)
    args.write.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if not args.quiet:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.status == "TRI_OS_COMPATIBILITY_HANDOFF_EMITTER_READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
