#!/usr/bin/env python3
"""Exact source-bound v1.87 original-name adoption check, from independently certified CodeAI R2.

Only the two namespace delimiters may change from candidate to original. No
claims of standard/canonical equality, general endpoint RLP, or global fibrancy.
Preflight is not itself PR/main adoption and never authorizes merge.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile

from scripts import ci_kuuos_v187_codeai_exact_source_v1 as r1
from scripts.ci_kuuos_v176_exact_source_audit_v1 import (
    AuditFailure, ROOT, STANDARD_AXIOMS, blob, run_logged, verify_inputs,
)
from scripts.kuuos_lean_mcp_repair_loop_v1 import mask_lean_comments

MODULE = "KUOS.DependentOriginationStandardCanonicalPresentationGapV1_87"
ADOPTED = ROOT / "formal/KUOS/DependentOriginationStandardCanonicalPresentationGapV1_87.lean"
CANDIDATE = ROOT / "formal/KUOS/DependentOriginationStandardCanonicalPresentationGapCodeAICandidateR2V1_87.lean"
HISTORICAL = ROOT / "legacy/v5.291/formal/KUOS/DependentOriginationStandardCanonicalPresentationGapV1_87.lean"
ADOPTED_BLOB = "9718e8dcb1e366774374ddb3d084c5a80391d7e0"
CANDIDATE_BLOB = "1ba284fa92c153bb28defc4c84d1bd23d4e01522"
HISTORICAL_BLOB = "88181c3c721c129e2aa628406e3fbf77a89d4f91"
CERTIFIED_CANDIDATE_HEAD = "c91890d14b966addfd55dcaeff6c5e198eb8f49e"
CERTIFIED_CANDIDATE_RUN = 44964695827
PARENTS = r1.PARENTS
PUBLIC = r1.PUBLIC
DECL = r1.DECL
OLD_NS = "KUOS.DependentOriginationStandardCanonicalPresentationGapCodeAICandidateR2V1_87"
NEW_NS = "KUOS.DependentOriginationStandardCanonicalPresentationGapV1_87"

def execute(out: Path) -> dict:
    verify_inputs()
    for name, expected in PARENTS.items():
        f = ROOT / "formal/KUOS" / (name + ".lean")
        if blob(f.read_bytes()) != expected:
            raise AuditFailure("V187_ADOPTED_PARENT_CHANGED " + name)
    if blob(HISTORICAL.read_bytes()) != HISTORICAL_BLOB:
        raise AuditFailure("V187_ADOPTED_FROZEN_HISTORY_CHANGED")
    raw_candidate = CANDIDATE.read_bytes()
    if blob(raw_candidate) != CANDIDATE_BLOB:
        raise AuditFailure("V187_ADOPTED_CERTIFIED_CANDIDATE_BLOB_MISMATCH")
    raw = ADOPTED.read_bytes()
    if blob(raw) != ADOPTED_BLOB:
        raise AuditFailure("V187_ADOPTED_ORIGINAL_NAME_BLOB_MISMATCH")
    s = raw_candidate.decode("utf8")
    if s.count(OLD_NS) != 2 or NEW_NS in s:
        raise AuditFailure("V187_ADOPTED_NAMESPACE_EXPECTATION_MISMATCH")
    if raw.decode("utf8") != s.replace(OLD_NS, NEW_NS):
        raise AuditFailure("V187_ADOPTED_NOT_EXACT_NAMESPACE_ONLY")
    masked = mask_lean_comments(raw.decode("utf8"))
    if re.search(r"(?m)^\s*(?:sorry|admit|axiom|unsafe|native_decide)\b", masked):
        raise AuditFailure("V187_ADOPTED_TRUST_BYPASS")
    decl = DECL.findall(masked)
    if decl != PUBLIC or len(PUBLIC) != 27 or len(set(PUBLIC)) != 27:
        raise AuditFailure("V187_ADOPTED_PUBLIC_INVENTORY " + repr(decl))
    head = os.environ.get("SOURCE_HEAD", "")
    if not re.fullmatch(r"[a-f0-9]{40}", head):
        raise AuditFailure("V187_ADOPTED_EXACT_HEAD_NO_DATA")
    out.mkdir(parents=True, exist_ok=True)
    if any(out.iterdir()):
        raise AuditFailure("V187_ADOPTED_APPEND_ONLY_RECEIPT_ALREADY_EXISTS")
    run_logged(
        ["lake", "-KleanArgs=-DwarningAsError=true", "-KleanArgs=-DsorryAsError=true",
         "build", MODULE], out / "strict-build.log", 4800,
    )
    with tempfile.TemporaryDirectory(dir=ROOT, prefix=".kuuos-v187-adopted-axioms-") as temp:
        audit = Path(temp) / "all-27.lean"
        audit.write_text("import " + MODULE + "\n" +
            "".join("#print axioms " + MODULE + "." + name + "\n" for name in PUBLIC),
            encoding="utf8")
        run_logged(["lake", "env", "lean", "-DwarningAsError=true",
                    "-Dweak.sorryAsError=true", str(audit)], out / "axiom-audit.log", 1800)
    log = (out / "axiom-audit.log").read_text(errors="replace")
    reports = {}
    for name in PUBLIC:
        full = MODULE + "." + name
        match = re.search(r"'" + re.escape(full) + r"'\s+depends on axioms:\s*\[([^\]]*)\]", log, re.S)
        if match:
            reports[name] = sorted(x.strip() for x in match.group(1).split(",") if x.strip())
        elif re.search(r"'" + re.escape(full) + r"'\s+does not depend on any axioms", log):
            reports[name] = []
        else:
            raise AuditFailure("V187_ADOPTED_AXIOM_NO_DATA " + full)
    axioms = {x for entries in reports.values() for x in entries}
    if axioms - STANDARD_AXIOMS or "sorryAx" in log:
        raise AuditFailure("V187_ADOPTED_NONSTANDARD_AXIOMS " + repr(sorted(axioms - STANDARD_AXIOMS)))
    receipt = {
        "kind": "KUUOS_V187_CODEAI_R2_ORIGINAL_NAME_EXACT_SOURCE_27_AXIOMS",
        "source_head": head,
        "adopted_original_name_blob": ADOPTED_BLOB,
        "certified_r2_candidate_blob": CANDIDATE_BLOB,
        "certified_r2_candidate_head": CERTIFIED_CANDIDATE_HEAD,
        "certified_r2_candidate_run": CERTIFIED_CANDIDATE_RUN,
        "frozen_historical_blob": HISTORICAL_BLOB,
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "declarations": len(reports),
        "axioms": sorted(axioms),
        "sorryAx": False, "warnings": 0, "errors": 0,
        "lean_pin": "leanprover/lean4:v4.30.0-rc2",
        "mathlib_pin": "5450b53e5ddc75d46418fabb605edbf36bd0beb6",
        "candidate_to_original_namespace_only": True,
        "global_gap_closed": False,
        "arbitrary_scaling_forward_endpoint_RLP_proven": False,
        "merge_authorized": False,
    }
    (out / "receipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
    print("KUUOS_V187_R2_ORIGINAL_NAME_KERNEL_GREEN " + json.dumps(receipt, ensure_ascii=False), flush=True)
    return receipt

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--out", required=True, type=Path)
    args = p.parse_args()
    try:
        execute(args.out.resolve())
        return 0
    except (AuditFailure, OSError, ValueError) as exc:
        print("KUUOS_V187_R2_ORIGINAL_NAME_HOLD " + json.dumps({
            "status": "UNAUTHENTICATED", "obstruction": str(exc), "merged": False
        }), file=sys.stderr, flush=True)
        return 2

if __name__ == "__main__":
    sys.exit(main())
