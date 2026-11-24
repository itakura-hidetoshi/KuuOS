#!/usr/bin/env python3
"""Independent pinned Lean and full public-axiom audit of research-only v1.77 candidate.
NO CANONICAL ADOPTION; prior PR#3542 source is advisory and must be retested
against the current adopted v1.76 typed signatures (different Git blob).
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

from scripts.ci_kuuos_v176_exact_source_audit_v1 import (
    AuditFailure, ROOT, STANDARD_AXIOMS, blob, run_logged, verify_inputs,
)
from scripts.kuuos_lean_mcp_repair_loop_v1 import mask_lean_comments

MODULE = "KUOS.DependentOriginationStandardABCPostEndpointCanonicalComparisonV1_78"
SOURCE = ROOT / "formal/KUOS/DependentOriginationStandardABCPostEndpointCanonicalComparisonV1_78.lean"
EXPECTED_SOURCE_BLOB = "b406155d78506527b53549f0cf232d55f084ac86"
RESEARCH_ORIGINAL_BLOB = "b406155d78506527b53549f0cf232d55f084ac86"
RESEARCH_ORIGINAL_HEAD = "baf4d5ba6d9a7b99dbaa364e6101db6636c72a16"
EXPECTED_DECLARATIONS = 11
DECL_PATTERN = re.compile(
    r"(?m)^(?:@\[[^\]]+\]\s*)?(?:noncomputable\s+)?"
    r"(?:def|theorem|lemma|structure|instance|abbrev)\s+([^\s(:]+)"
)

def run(out: Path) -> dict:
    verify_inputs()  # exact certified 41-declaration v1.76 prerequisite
    imported_v177 = ROOT / "formal/KUOS/DependentOriginationStandardTypeAEndpointOppositeCellCertificateV1_77.lean"
    if blob(imported_v177.read_bytes()) != "d786495a68268e01634f6f8143ebe09241bffc3e":
        raise AuditFailure("DEPENDENCY_V177_EXACT_SOURCE_MISMATCH")
    head = os.environ.get("SOURCE_HEAD", "")
    if not re.fullmatch(r"[a-f0-9]{40}", head):
        raise AuditFailure("NO_DATA_EXACT_GITHUB_HEAD")
    candidate_text = (ROOT / "formal/KUOS/DependentOriginationStandardABCPostEndpointCodeAICandidateV1_78.lean").read_text(encoding="utf8")
    adopted_text = SOURCE.read_text(encoding="utf8")
    if candidate_text.replace("KUOS.DependentOriginationStandardABCPostEndpointCodeAICandidateV1_78", "KUOS.DependentOriginationStandardABCPostEndpointCanonicalComparisonV1_78") != adopted_text:
        raise AuditFailure("CERTIFIED_CANDIDATE_ORIGINAL_NAME_EQUIVALENCE_FAIL")
    raw = SOURCE.read_bytes()
    if blob(raw) != EXPECTED_SOURCE_BLOB:
        raise AuditFailure("CANDIDATE_SOURCE_MISMATCH " + blob(raw))
    text = mask_lean_comments(raw.decode("utf8"))
    if re.search(r"(?m)^\s*(?:axiom|sorry|admit)\b", text):
        raise AuditFailure("PROOF_BYPASS")
    decls = DECL_PATTERN.findall(text)
    if len(decls) != EXPECTED_DECLARATIONS or len(set(decls)) != EXPECTED_DECLARATIONS:
        raise AuditFailure("DECLARATION_INVENTORY_MISMATCH " + str(len(decls)))
    out.mkdir(parents=True,exist_ok=True)
    if list(out.iterdir()):
        raise AuditFailure("APPEND_ONLY_VIOLATION")
    run_logged(["lake","-KleanArgs=-DwarningAsError=true",
         "-KleanArgs=-DsorryAsError=true", "build", MODULE],out/"strict-build.log",4800)
    with tempfile.TemporaryDirectory(dir=ROOT,prefix=".kuuos-v177-research-audit-") as temp:
        f=Path(temp)/"axioms.lean"
        f.write_text("import "+MODULE+"\n"+
            "".join("#print axioms "+MODULE+"."+n+"\n" for n in decls),encoding="utf8")
        run_logged(["lake","env","lean","-DwarningAsError=true",
                    "-Dweak.sorryAsError=true",str(f)],out/"axiom-audit.log",2400)
    log=(out/"axiom-audit.log").read_text(errors="replace")
    reports={}
    for n in decls:
        fullname=MODULE+"."+n
        m=re.search(r"'"+re.escape(fullname)+r"'\s+depends on axioms:\s*\[([^\]]*)\]",log,re.S)
        if m: reports[n]=sorted(x.strip() for x in m.group(1).split(",") if x.strip())
        elif re.search(r"'"+re.escape(fullname)+r"'\s+does not depend on any axioms",log):
            reports[n]=[]
        else: raise AuditFailure("AXIOM_NO_DATA "+fullname)
    all_ax=set(ax for a in reports.values() for ax in a)
    if all_ax-STANDARD_AXIOMS or "sorryAx" in log:
        raise AuditFailure("AXIOM_OBSTRUCTION "+",".join(sorted(all_ax-STANDARD_AXIOMS)))
    rec={
      "kind":"KUUOS_V178_ADOPTED_EXACT_SOURCE_INDEPENDENT_AUDIT_V1",
      "candidate_not_adopted":False,"adoption_is_PR_source_not_main":True,"head":head,
      "source_blob":EXPECTED_SOURCE_BLOB,
      "source_sha256":hashlib.sha256(raw).hexdigest(),
      "research_origin_head":RESEARCH_ORIGINAL_HEAD,
      "research_origin_blob":RESEARCH_ORIGINAL_BLOB,
      "lean_pin":"leanprover/lean4:v4.30.0-rc2",
      "mathlib_pin":"5450b53e5ddc75d46418fabb605edbf36bd0beb6",
      "public_declarations":len(decls),"axioms":sorted(all_ax),
      "sorryAx":False,"warnings":0,"errors":0,
      "full_governance":"SEPARATE","canonical_source_adoption":"PR_SOURCE_SUBJECT_TO_THIS_EXACT_HEAD_CI",
      "independent_approval":"PENDING_UNTIL_GITHUB_JOB_SUCCESS",
      "general_canonical_KuuOS_RLP":False,"merged":False}
    (out/"receipt.json").write_text(json.dumps(rec,ensure_ascii=False,indent=2)+"\n")
    print("KUUOS_V178_ADOPTED_SOURCE_KERNEL_GREEN "+json.dumps(rec,ensure_ascii=False),flush=True)
    return rec

def main()->int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args()
    try:
        run(args.out.resolve())
        return 0
    except (OSError, ValueError, AuditFailure) as exc:
        print("KUUOS_V178_ADOPTED_SOURCE_HOLD "+json.dumps({
          "status":"UNAUTHENTICATED","obstruction":str(exc),
          "adopted":False,"merged":False}),file=sys.stderr,flush=True)
        return 2

if __name__=="__main__":
    sys.exit(main())
