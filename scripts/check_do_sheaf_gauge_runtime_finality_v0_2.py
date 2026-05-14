#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLOSURE_RUNNER = ROOT / "scripts" / "run_do_sheaf_gauge_runtime_closure_checks_v0_2.py"
DOC = ROOT / "docs" / "DO_SHEAF_GAUGE_RUNTIME_FINALITY_PACKET_v0_2.md"
ATTEST = ROOT / "specs" / "do_sheaf_gauge_runtime_attestation_v0_2.generated.json"

REQUIRED = [
    "docs/DO_SHEAF_GAUGE_RUNTIME_CLOSURE_PACKET_v0_2.md",
    "docs/DO_SHEAF_GAUGE_RUNTIME_FINALITY_PACKET_v0_2.md",
    "specs/do_sheaf_gauge_runtime_attestation_v0_2.generated.json",
    "specs/do_sheaf_gauge_runtime_bundle_v0_2.generated.json",
    "specs/do_sheaf_gauge_runtime_worm_receipt_v0_2.generated.json",
    "scripts/check_do_sheaf_gauge_runtime_closure_v0_2.py",
    "scripts/run_do_sheaf_gauge_runtime_closure_checks_v0_2.py",
]

TRUE_FIELDS = [
    "site_cover_required",
    "gluing_required",
    "gauge_connection_required",
    "holonomy_record_required",
    "curvature_visibility_required",
]


def main() -> int:
    code = subprocess.run([sys.executable, str(CLOSURE_RUNNER)], cwd=ROOT).returncode
    if code != 0:
        return code
    errors: list[str] = []
    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            errors.append(f"missing: {rel}")
    text = DOC.read_text(encoding="utf-8") if DOC.is_file() else ""
    for token in [
        "implementation finality only",
        "not a flat graph model",
        "site/cover",
        "gauge connection",
        "holonomy record",
        "curvature visibility",
        "not proof, truth, essence authority, Ten'i authority, clinical authority, or execution authority",
    ]:
        if token not in text:
            errors.append(f"finality doc missing: {token}")
    att = json.loads(ATTEST.read_text(encoding="utf-8")) if ATTEST.is_file() else {}
    if att.get("graph_only_model_allowed") is not False:
        errors.append("attestation must keep graph_only_model_allowed=false")
    for field in TRUE_FIELDS:
        if att.get(field) is not True:
            errors.append(f"attestation {field} must be true")
    if errors:
        for e in errors:
            print("ERROR:", e)
        return 1
    print("PASS: DO sheaf gauge runtime finality checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
