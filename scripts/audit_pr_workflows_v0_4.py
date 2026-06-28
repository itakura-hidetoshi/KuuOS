#!/usr/bin/env python3
"""Inventory direct pull-request workflow entry points."""

from __future__ import annotations

import argparse
import json
import pathlib
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github/workflows"
CANONICAL_GATE = ".github/workflows/pr-governance-gate.yml"


def build_inventory() -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    pull_request_target: list[str] = []
    for path in sorted(WORKFLOWS.glob("*.y*ml")):
        text = path.read_text(encoding="utf-8")
        relative = str(path.relative_to(ROOT))
        if "pull_request_target:" in text:
            pull_request_target.append(relative)
        if "pull_request:" not in text:
            continue
        entries.append(
            {
                "path": relative,
                "canonical": relative == CANONICAL_GATE,
                "path_scoped": "paths:" in text or "paths-ignore:" in text,
                "workflow_dispatch": "workflow_dispatch:" in text,
                "push": "push:" in text,
            }
        )
    direct = [entry for entry in entries if not entry["canonical"]]
    return {
        "schema_version": "0.4",
        "canonical_gate": CANONICAL_GATE,
        "pull_request_workflow_count": len(entries),
        "direct_pull_request_workflow_count": len(direct),
        "unscoped_direct_count": sum(not entry["path_scoped"] for entry in direct),
        "pull_request_target": pull_request_target,
        "entries": entries,
        "boundary": "inventory != approval; trigger count != validation quality",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=pathlib.Path)
    args = parser.parse_args()
    inventory = build_inventory()
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(inventory, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(inventory, ensure_ascii=False, indent=2))
    return 1 if inventory["pull_request_target"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
