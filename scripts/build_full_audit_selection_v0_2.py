#!/usr/bin/env python3
import argparse
import json
import pathlib

parser = argparse.ArgumentParser()
parser.add_argument("--output", type=pathlib.Path, required=True)
parser.add_argument("--count", type=int, default=8)
args = parser.parse_args()

checks = [{"id": "workflow-integrity"}]
checks += [{"id": f"full-governance-{i:02d}"} for i in range(args.count)]
payload = {
    "schema_version": "0.2",
    "full_audit_required": True,
    "changed_paths": [],
    "direct_checks": [],
    "selected_checks": checks,
    "unknown_paths": [],
    "unmapped_paths": [],
    "reasons": ["post-merge full audit"],
    "boundaries": ["validation != truth", "sharding != authority expansion"],
}
args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
