#!/usr/bin/env python3
"""KuuOS v1.85 original-name adopted source, pinned Strict Lean and all 20 axioms.

Exact CodeAI candidate CI #44954822314 green; independent adopted-world source
and kernel/axiom rerun required. This does not authorize main/PR merge.
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

MODULE = "KUOS.DependentOriginationGeneratedPresentationFixedPointOrderIsoV1_85"
ADOPTED = ROOT / "formal/KUOS/DependentOriginationGeneratedPresentationFixedPointOrderIsoV1_85.lean"
CERTIFIED_CANDIDATE = ROOT / "formal/KUOS/DependentOriginationGeneratedPresentationFixedPointOrderIsoCodeAICandidateV1_85.lean"
HISTORICAL = ROOT / "legacy/v5.291/formal/KUOS/DependentOriginationGeneratedPresentationFixedPointOrderIsoV1_85.lean"
ADOPTED_BLOB = "eff1b6d74800c4d3e1f37a6806ebf88ff8b6cd0e"
CANDIDATE_BLOB = "ae934472e704fd5c0bab7a464d9f0c444a1880fd"
HISTORICAL_BLOB = "97e364b48eb5632ab7f9f79b051f5b665445c682"
SOURCE_CANDIDATE_HEAD = "af61e13913d22ea8e1b2e32fc680adc9f9066c99"
SOURCE_CANDIDATE_RUN = 44954822314
PARENTS = {
    "DependentOriginationGeneratedPresentationOrderReflectionV1_84":"5c1f7e9dc8fbb12bb901f4c67f0aad99543d49b9",
    "DependentOriginationGeneratedPresentationPosetalReflectionV1_83":"3bc1f096876f8c7b799ae48f29419e6686e33c87",
    "DependentOriginationGeneratedPresentationQuotientInvariantV1_81":"8ba7b0e6034a2e24b44587fb477c2192cffffeca",
}
PUBLIC = ["OrthogonallySaturatedScaledAnodyne","IsRightOrthogonallySaturated","OrthogonallySaturatedScaledFibration","generatedAnodyneClass_isOrthogonallySaturated","generatedFibrationClass_isRightOrthogonallySaturated","presentationToSaturatedAnodyne","saturatedAnodyneToPresentation","saturatedAnodyneToPresentation_presentationToSaturatedAnodyne","presentationToSaturatedAnodyne_saturatedAnodyneToPresentation","generatedPresentationSaturatedAnodyneOrderIso","generatedPresentationSaturatedAnodyneOrderIso_apply_val","presentationToSaturatedFibration","saturatedFibrationToPresentation","saturatedFibrationToPresentation_presentationToSaturatedFibration","presentationToSaturatedFibration_saturatedFibrationToPresentation","generatedPresentationSaturatedFibrationOrderIso","generatedPresentationSaturatedFibrationOrderIso_apply_val","saturatedAnodyneFibrationOrderIso","presentation_eq_iff_saturatedAnodyne_eq","presentation_eq_iff_saturatedFibration_eq"]
DECL = re.compile(r"(?m)^(?:@\[[^\]]+\]\s*)?(?:(?:private|noncomputable|protected|partial|unsafe)\s+)*(?:theorem|def|lemma|structure|instance|abbrev)\s+([^\s(:]+)")

def execute(out: Path) -> dict:
    verify_inputs()
    for mod, expected in PARENTS.items():
        path = ROOT / "formal/KUOS" / (mod + ".lean")
        if blob(path.read_bytes()) != expected:
            raise AuditFailure("V185_PARENT_SOURCE_BLOB_MISMATCH "+mod)
    if blob(HISTORICAL.read_bytes()) != HISTORICAL_BLOB:
        raise AuditFailure("V185_FROZEN_LEGACY_CHANGED")
    original = CERTIFIED_CANDIDATE.read_bytes()
    if blob(original) != CANDIDATE_BLOB:
        raise AuditFailure("V185_CERTIFIED_CANDIDATE_CHANGED")
    raw = ADOPTED.read_bytes()
    if blob(raw) != ADOPTED_BLOB:
        raise AuditFailure("V185_ADOPTED_BLOB_MISMATCH")
    predicted = original.decode("utf8").replace("KUOS.DependentOriginationGeneratedPresentationFixedPointOrderIsoCodeAICandidateV1_85", "KUOS.DependentOriginationGeneratedPresentationFixedPointOrderIsoV1_85")
    if raw.decode("utf8") != predicted:
        raise AuditFailure("V185_ADOPTION_NOT_NAMESPACE_ONLY")
    masked = mask_lean_comments(raw.decode("utf8"))
    if re.search(r"(?m)^\s*(?:sorry|admit|axiom)\b", masked):
        raise AuditFailure("V185_TRUST_BYPASS")
    declarations = DECL.findall(masked)
    if declarations != PUBLIC or len(PUBLIC) != 20 or len(set(PUBLIC)) != 20:
        raise AuditFailure("V185_PUBLIC_INVENTORY "+repr(declarations))
    head = os.environ.get("SOURCE_HEAD", "")
    if not re.fullmatch(r"[a-f0-9]{40}", head):
        raise AuditFailure("V185_NO_DATA_SOURCE_HEAD")
    out.mkdir(parents=True, exist_ok=True)
    if list(out.iterdir()):
        raise AuditFailure("V185_APPEND_ONLY_RECEIPT_EXISTS")
    run_logged(
        ["lake","-KleanArgs=-DwarningAsError=true",
         "-KleanArgs=-DsorryAsError=true","build",MODULE],
        out / "strict-build.log",4800)
    with tempfile.TemporaryDirectory(dir=ROOT,prefix=".kuuos-v185-adopted-axioms-") as d:
        file=Path(d)/"all-20.lean"
        file.write_text("import "+MODULE+"\n"+
            "".join("#print axioms "+MODULE+"."+name+"\n" for name in PUBLIC),
            encoding="utf8")
        run_logged(["lake","env","lean","-DwarningAsError=true",
                   "-Dweak.sorryAsError=true",str(file)],
                   out / "axiom-audit.log",1800)
    log = (out / "axiom-audit.log").read_text(errors="replace")
    reports = {}
    for name in PUBLIC:
        full=MODULE+"."+name
        hit=re.search(r"'" + re.escape(full) +
            r"'\s+depends on axioms:\s*\[([^\]]*)\]", log, re.S)
        if hit:
            reports[name]=sorted(x.strip() for x in hit.group(1).split(",") if x.strip())
        elif re.search(r"'" + re.escape(full)+r"'\s+does not depend on any axioms",log):
            reports[name]=[]
        else:
            raise AuditFailure("V185_PUBLIC_AXIOM_NO_DATA "+full)
    axioms=set(a for names in reports.values() for a in names)
    if axioms-STANDARD_AXIOMS or "sorryAx" in log:
        raise AuditFailure("V185_NONSTANDARD_AXIOM "+repr(sorted(axioms-STANDARD_AXIOMS)))
    receipt={
      "kind":"KUUOS_V185_PR_ADOPTED_EXACT_SOURCE_20_AXIOM_AUDIT",
      "head":head,"adopted_source_blob":ADOPTED_BLOB,
      "certified_candidate_blob":CANDIDATE_BLOB,
      "certified_candidate_head":SOURCE_CANDIDATE_HEAD,
      "certified_candidate_run":SOURCE_CANDIDATE_RUN,
      "historical_blob":HISTORICAL_BLOB,
      "source_sha256":hashlib.sha256(raw).hexdigest(),
      "public_declarations":len(reports),
      "lean_pin":"leanprover/lean4:v4.30.0-rc2",
      "mathlib_pin":"5450b53e5ddc75d46418fabb605edbf36bd0beb6",
      "axioms":sorted(axioms),"sorryAx":False,"warnings":0,"errors":0,
      "source_adopted_on_PR":True,"source_adopted_on_main":False,
      "standard_equals_canonical_asserted":False,
      "general_forward_endpoint_RLP_asserted":False,
    }
    (out/"receipt.json").write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+"\n")
    print("KUUOS_V185_PR_ADOPTED_KERNEL_GREEN "+json.dumps(receipt,ensure_ascii=False),flush=True)
    return receipt

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",required=True,type=Path)
    args=ap.parse_args()
    try:
        execute(args.out.resolve())
        return 0
    except (AuditFailure,OSError,ValueError) as err:
        print("KUUOS_V185_PR_ADOPTED_HOLD "+json.dumps(
            {"status":"UNAUTHENTICATED","obstruction":str(err),"merged":False}),
            file=sys.stderr,flush=True)
        return 2

if __name__=="__main__":
    sys.exit(main())
