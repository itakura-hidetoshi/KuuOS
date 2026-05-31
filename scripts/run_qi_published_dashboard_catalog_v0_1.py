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

from runtime.kuuos_runtime_daemon_qi_published_dashboard_catalog_v0_1 import build_qi_published_dashboard_catalog


def read_json(path: pathlib.Path | None) -> Any:
    if path is None or not path.is_file():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def read_context(path: pathlib.Path | None) -> dict[str, Any]:
    value = read_json(path)
    return value if isinstance(value, dict) else {}


def normalize_entries(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    if isinstance(value, dict):
        raw = value.get("registry_entries")
        if isinstance(raw, list):
            return [item for item in raw if isinstance(item, dict)]
        return [value]
    return []


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build Qi published dashboard catalog v0.1")
    parser.add_argument("--registry-entries", type=pathlib.Path, required=True)
    parser.add_argument("--context", type=pathlib.Path, default=None)
    parser.add_argument("--write", type=pathlib.Path, required=True)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)

    catalog = build_qi_published_dashboard_catalog(
        registry_entries=normalize_entries(read_json(args.registry_entries)),
        catalog_context=read_context(args.context),
    )
    payload = catalog.to_dict()
    args.write.parent.mkdir(parents=True, exist_ok=True)
    args.write.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if not args.quiet:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if catalog.catalog_status == "QI_PUBLISHED_DASHBOARD_CATALOG_READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
