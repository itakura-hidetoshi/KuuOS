#!/usr/bin/env python3
"""Exact pinned conditional descent bridge audit: proves an implication, NOT raw A existence."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile

from scripts.ci_kuuos_v176_exact_source_audit_v1 import (
    AuditFailure, ROOT, STANDARD_AXIOMS, blob, run_logged, verify_inputs,
)
from scripts.kuuos_lean_mcp_repair_loop_v1 import mask_lean_comments

MODULE = "KUOS.DependentOriginationStandardTypeAEndpointConditionalDescentV1_77A"
NAMESPACE = MODULE
SOURCE = ROOT / "formal/KUOS/DependentOriginationStandardTypeAEndpointConditionalDescentV1_77A.lean"
EXPECTED_BLOB = "6d6b3af0726f68206d46ae60420cba5ddcb302a7"
DECLARATIONS = (
    "standardABCTypeAEndpointLeibnizLifting_of_missingRawA",
    "standardABCTypeAEndpointLeibnizStability_of_missingRawA",
)
ALLOWED = STANDARD_AXIOMS

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    out = args.out.resolve()
    try:
        verify_inputs()  # preserves exact, separately certified v1.76 prerequisite
        raw = SOURCE.read_bytes()
        if blob(raw) != EXPECTED_BLOB:
            raise AuditFailure("V177A_SOURCE_BLOB_MISMATCH " + blob(raw))
        masked = mask_lean_comments(raw.decode("utf8"))
        if re.search(r"(?m)^\s*(?:axiom|sorry|admit)\b", masked):
            raise AuditFailure("PROOF_BYPASS")
        decls = re.findall(r"(?m)^theorem\s+([^\s:(]+)", masked)
        if tuple(decls) != DECLARATIONS:
            raise AuditFailure("V177A_DECLARATION_INVENTORY_MISMATCH")
        head = os.environ.get("SOURCE_HEAD", "")
        if not re.fullmatch(r"[a-f0-9]{40}", head):
            raise AuditFailure("HEAD_PROVENANCE_MISSING")
        out.mkdir(parents=True, exist_ok=True)
        if list(out.iterdir()):
            raise AuditFailure("APPEND_ONLY_VIOLATION")
        run_logged(
            ["lake", "-KleanArgs=-DwarningAsError=true",
             "-KleanArgs=-DsorryAsError=true", "build", MODULE],
            out / "strict-build.log", 4800)
        with tempfile.TemporaryDirectory(prefix=".kuuos-v177a-audit-",dir=ROOT) as t:
            f = Path(t) / "audit.lean"
            f.write_text("import " + MODULE + "\n" +
                "".join("#print axioms " + NAMESPACE + "." + n + "\n" for n in DECLARATIONS))
            run_logged(["lake", "env", "lean", "-DwarningAsError=true",
                        "-Dweak.sorryAsError=true", str(f)],
                       out / "axioms.log", 1200)
        log = (out / "axioms.log").read_text()
        reports = {}
        for name in DECLARATIONS:
            key = NAMESPACE + "." + name
            q = re.search(r"'" + re.escape(key) +
                          r"'\s+depends on axioms:\s*\[([^\]]*)\]", log, re.S)
            if q:
                reports[name] = sorted(t.strip() for t in q.group(1).split(",") if t.strip())
            elif re.search(r"'" + re.escape(key) + r"'\s+does not depend on any axioms", log):
                reports[name] = []
            else:
                raise AuditFailure("AXIOM_NO_DATA " + name)
        all_ax = set(x for ax in reports.values() for x in ax)
        if (all_ax - ALLOWED) or "sorryAx" in log:
            raise AuditFailure("AXIOM_OBSTRUCTION " + ",".join(sorted(all_ax-ALLOWED)))
        result = {
            "kind": "KUUOS_V177A_CONDITIONAL_DESCENT_AUDIT_V1",
            "source_head": head,
            "source_blob": EXPECTED_BLOB,
            "sha256": hashlib.sha256(raw).hexdigest(),
            "pinned_lean": "leanprover/lean4:v4.30.0-rc2",
            "pinned_mathlib": "5450b53e5ddc75d46418fabb605edbf36bd0beb6",
            "declarations": len(reports),
            "axioms": sorted(all_ax), "sorryAx": False, "errors": 0, "warnings": 0,
            "first_raw_A_cell": "UNPROVED_REQUIRED_PREMISE",
            "unconditional_endpoint_RLP": False,
            "full_PR_governance": "SEPARATE",
            "external_approval": "PENDING_UNTIL_WORKFLOW_SUCCESS",
        }
        (out / "receipt.json").write_text(json.dumps(result,indent=2)+"\n")
        print("KUUOS_V177A_CONDITIONAL_KERNEL_OK " + json.dumps(result),flush=True)
        return 0
    except (AuditFailure, OSError, ValueError) as exc:
        print("KUUOS_V177A_HOLD " + json.dumps({"obstruction":str(exc),
            "proof":False,"merged":False}),file=sys.stderr,flush=True)
        return 2

if __name__ == "__main__":
    sys.exit(main())
