#!/usr/bin/env python3
"""Exact v1.84 PR-adopted source: fixed Lean and all 13 public axiom audit.

The original-name source must be namespace-only equivalent to independently
certified CodeAI candidate. Historical root remains frozen.
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

MODULE = "KUOS.DependentOriginationGeneratedPresentationOrderReflectionV1_84"
ADOPTED = ROOT / "formal/KUOS/DependentOriginationGeneratedPresentationOrderReflectionV1_84.lean"
CERTIFIED = ROOT / "formal/KUOS/DependentOriginationGeneratedPresentationOrderReflectionCodeAICandidateV1_84.lean"
HISTORICAL = ROOT / "legacy/v5.291/formal/KUOS/DependentOriginationGeneratedPresentationOrderReflectionV1_84.lean"
ADOPTED_BLOB = "5c1f7e9dc8fbb12bb901f4c67f0aad99543d49b9"
CERTIFIED_BLOB = "2dc4ab85f1b471a50ae508dd7a6ee0160d1a0535"
HISTORICAL_BLOB = "baf70fc20347e881054fb86180de849ebf92f71f"
SOURCE_CANDIDATE_HEAD = "3fdb35b172eb6531a9b602647b30210ded905934"
SOURCE_CANDIDATE_RUN = 44950775715
PARENTS = {
    "DependentOriginationGeneratedPresentationPosetalReflectionV1_83": "3bc1f096876f8c7b799ae48f29419e6686e33c87",
    "DependentOriginationGeneratedPresentationQuotientInvariantV1_81": "8ba7b0e6034a2e24b44587fb477c2192cffffeca",
    "DependentOriginationGeneratedPresentationEndpointInvariantV1_80": "7be90de61f5c05456de6fa74dd1f262430486d84",
    "DependentOriginationStandardABCPositiveCanonicalResidualSplitV1_79": "cd9a58880341e70a2290387d21d144613464c8c0",
}
PUBLIC = ["GeneratedPresentationPreorderLE","generatedPresentationPreorderLE_refl","generatedPresentationPreorderLE_trans","presentationClass_le_iff_generators_le_generated","presentationClass_eq_iff_mutual_preorder","generatedPresentationEquivalence_iff_mutual_preorder","presentationClass_eq_iff_generatedPresentationEquivalence","canonicalKuuOS_le_standardABC_iff_canonicalGenerators_le_standardGenerated","standardABC_le_canonicalKuuOS_iff_standardGenerators_le_canonicalGenerated","canonicalKuuOS_le_standardABC_of_positiveResidual","standardABC_le_canonicalKuuOS_iff_generatorwiseReverse","standardABC_eq_canonicalKuuOS_iff_direct_generator_inclusions","standardABC_eq_canonicalKuuOS_of_positiveComparison_via_order"]
DECL = re.compile(r"(?m)^(?:@\[[^\]]+\]\s*)?(?:(?:private|noncomputable|protected|partial|unsafe)\s+)*(?:theorem|def|lemma|structure|instance|abbrev)\s+([^\s(:]+)")

def execute(out: Path) -> dict:
    verify_inputs()
    for module, expected_sha in PARENTS.items():
        actual = blob((ROOT / "formal/KUOS" / (module + ".lean")).read_bytes())
        if actual != expected_sha:
            raise AuditFailure("V184_PARENT_BLOB_MISMATCH " + module)
    if blob(HISTORICAL.read_bytes()) != HISTORICAL_BLOB:
        raise AuditFailure("V184_HISTORICAL_ROOT_CHANGED")
    certified = CERTIFIED.read_bytes()
    if blob(certified) != CERTIFIED_BLOB:
        raise AuditFailure("V184_CERTIFIED_CANDIDATE_MODIFIED")
    raw = ADOPTED.read_bytes()
    if blob(raw) != ADOPTED_BLOB:
        raise AuditFailure("V184_ADOPTED_BLOB_MISMATCH")
    expected = certified.decode("utf8").replace("KUOS.DependentOriginationGeneratedPresentationOrderReflectionCodeAICandidateV1_84", "KUOS.DependentOriginationGeneratedPresentationOrderReflectionV1_84")
    actual = raw.decode("utf8")
    if actual != expected:
        raise AuditFailure("V184_ADOPTION_NOT_EXACT_NAMESPACE_EQUIVALENT")
    masked = mask_lean_comments(actual)
    if re.search(r"(?m)^\s*(?:axiom|sorry|admit)\b", masked):
        raise AuditFailure("V184_ADOPTED_TRUST_BYPASS")
    inventory = DECL.findall(masked)
    if inventory != PUBLIC or len(PUBLIC) != 13 or len(set(PUBLIC)) != 13:
        raise AuditFailure("V184_PUBLIC_DECLARATION_INVENTORY " + repr(inventory))
    head = os.environ.get("SOURCE_HEAD", "")
    if not re.fullmatch(r"[a-f0-9]{40}", head):
        raise AuditFailure("V184_SOURCE_HEAD_NO_DATA")
    out.mkdir(parents=True, exist_ok=True)
    if list(out.iterdir()):
        raise AuditFailure("V184_APPEND_ONLY_RECEIPT_EXISTS")
    run_logged(
        ["lake","-KleanArgs=-DwarningAsError=true",
         "-KleanArgs=-DsorryAsError=true","build",MODULE],
        out / "strict-build.log",4800)
    with tempfile.TemporaryDirectory(dir=ROOT,prefix=".kuuos-v184-adopted-axioms-") as d:
        f=Path(d) / "all-13.lean"
        f.write_text("import " + MODULE + "\n" +
            "".join("#print axioms " + MODULE + "." + name + "\n" for name in PUBLIC),
            encoding="utf8")
        run_logged(
            ["lake","env","lean","-DwarningAsError=true",
             "-Dweak.sorryAsError=true",str(f)],
            out / "axiom-audit.log",1800)
    log=(out/"axiom-audit.log").read_text(errors="replace")
    reports={}
    for name in PUBLIC:
        full=MODULE+"."+name
        m=re.search(r"'" + re.escape(full) +
            r"'\s+depends on axioms:\s*\[([^\]]*)\]",log,re.S)
        if m:
            reports[name]=sorted(a.strip() for a in m.group(1).split(",") if a.strip())
        elif re.search(r"'" + re.escape(full) + r"'\s+does not depend on any axioms",log):
            reports[name]=[]
        else:
            raise AuditFailure("V184_AXIOM_NO_DATA " + full)
    axioms=set(a for xs in reports.values() for a in xs)
    if axioms - STANDARD_AXIOMS or "sorryAx" in log:
        raise AuditFailure("V184_NONSTANDARD_AXIOM " + repr(sorted(axioms - STANDARD_AXIOMS)))
    receipt={
        "kind":"KUUOS_V184_PR_ADOPTED_EXACT_SOURCE_13_AXIOM_AUDIT",
        "head":head,"adopted_blob":ADOPTED_BLOB,
        "certified_candidate_blob":CERTIFIED_BLOB,
        "certified_candidate_head":SOURCE_CANDIDATE_HEAD,
        "certified_candidate_run":SOURCE_CANDIDATE_RUN,
        "historical_blob":HISTORICAL_BLOB,
        "sha256":hashlib.sha256(raw).hexdigest(),
        "public_declarations":len(reports),
        "lean_pin":"leanprover/lean4:v4.30.0-rc2",
        "mathlib_pin":"5450b53e5ddc75d46418fabb605edbf36bd0beb6",
        "axioms":sorted(axioms),"sorryAx":False,"warnings":0,"errors":0,
        "adopted_on_pr":True,"adopted_on_main":False,
        "standard_equals_canonical_asserted":False,
        "general_forward_endpoint_RLP_asserted":False,
    }
    (out/"receipt.json").write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+"\n")
    print("KUUOS_V184_PR_ADOPTED_KERNEL_GREEN "+json.dumps(receipt,ensure_ascii=False),flush=True)
    return receipt

def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args()
    try:
        execute(args.out.resolve())
        return 0
    except (AuditFailure,OSError,ValueError) as exc:
        print("KUUOS_V184_PR_ADOPTED_HOLD "+json.dumps({
            "status":"UNAUTHENTICATED","obstruction":str(exc),"merged":False,
        }),file=sys.stderr,flush=True)
        return 2

if __name__ == "__main__":
    sys.exit(main())
