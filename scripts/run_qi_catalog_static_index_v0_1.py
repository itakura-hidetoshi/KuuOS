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

from runtime.kuuos_runtime_daemon_qi_catalog_static_index_v0_1 import build_qi_catalog_static_index


def read_json(path: pathlib.Path | None) -> dict[str, Any]:
    if path is None or not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build Qi catalog static index v0.1")
    parser.add_argument("--catalog", type=pathlib.Path, required=True)
    parser.add_argument("--context", type=pathlib.Path, default=None)
    parser.add_argument("--write", type=pathlib.Path, required=True)
    parser.add_argument("--write-html", type=pathlib.Path, default=None)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)

    index = build_qi_catalog_static_index(
        published_catalog=read_json(args.catalog),
        render_context=read_json(args.context),
    )
    payload = index.to_dict()
    args.write.parent.mkdir(parents=True, exist_ok=True)
    args.write.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_html is not None:
        args.write_html.parent.mkdir(parents=True, exist_ok=True)
        args.write_html.write_text(index.html, encoding="utf-8")
    if not args.quiet:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if index.multi_dashboard_index_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
