#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=pathlib.Path, required=True)
    parser.add_argument("--count", type=int, default=8)
    args = parser.parse_args()
    if args.count <= 0:
        parser.error("--count must be positive")

    checks = [{"id": "workflow-integrity"}]
    checks.extend(
        {"id": f"full-governance-{index:02d}"}
        for index in range(args.count)
    )
    payload = {
        "schema_version": "0.2",
        "full_audit_required": True,
        "changed_paths": [],
        "direct_checks": [],
        "selected_checks": checks,
        "unknown_paths": [],
        "unmapped_paths": [],
        "reasons": ["post-merge full audit"],
        "boundaries": [
            "validation != truth",
            "CI pass != theorem authority",
            "sharding != authority expansion",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
