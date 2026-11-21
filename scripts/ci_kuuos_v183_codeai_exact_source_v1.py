#!/usr/bin/env python3
"""KuuOS v1.83 CodeAI isolated pinned strict Lean and 18 named public-axiom audit.

The one original anonymous instance is given a unique local name for exact audit.
Candidate only: no original-name adoption, main merge or canonical equivalence.
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

MODULE = "KUOS.DependentOriginationGeneratedPresentationPosetalReflectionCodeAICandidateV1_83"
CANDIDATE = ROOT / "formal/KUOS/DependentOriginationGeneratedPresentationPosetalReflectionCodeAICandidateV1_83.lean"
ORIGINAL = ROOT / "formal/KUOS/DependentOriginationGeneratedPresentationPosetalReflectionV1_83.lean"
CANDIDATE_BLOB = "2a1a67c3793a618d69fb7d45d7d876e7428b59a4"
ORIGINAL_BLOB = "677031aa601d232ff11ba8aaba26653fd68134ee"
PARENTS = {"DependentOriginationGeneratedPresentationEndpointInvariantV1_80":"7be90de61f5c05456de6fa74dd1f262430486d84","DependentOriginationGeneratedPresentationQuotientInvariantV1_81":"8ba7b0e6034a2e24b44587fb477c2192cffffeca","DependentOriginationCanonicalEndpointLeibnizEpiDescentV1_82":"a1acb5e5c4c5fc41229e595441e7ad826d3e9c31"}
QUALIFIED = ["generatedAnodyneClass_rlp","generatedFibrationClass_llp","eq_of_generatedAnodyneClass_eq","eq_iff_generatedAnodyneClass_eq","generatedPresentationPartialOrder","le_iff_generatedAnodyneClass_le","generatedFibrationClass_antitone","le_of_generatedFibrationClass_reverse","le_iff_generatedFibrationClass_reverse_le","eq_iff_generatedFibrationClass_eq","eq_iff_le_and_le","typeAEndpointGeneratorsGenerated_iff","typeAEndpointLifting_iff","isFibrant_iff","typeAEndpointGeneratorsGenerated_mono","typeAEndpointLifting_mono","isFibrant_antitone","standardABC_eq_canonical_iff_mutual_le"]
BARE = ["generatedAnodyneClass_rlp","generatedFibrationClass_llp","eq_of_generatedAnodyneClass_eq","eq_iff_generatedAnodyneClass_eq","generatedPresentationPartialOrder","le_iff_generatedAnodyneClass_le","generatedFibrationClass_antitone","le_of_generatedFibrationClass_reverse","le_iff_generatedFibrationClass_reverse_le","eq_iff_generatedFibrationClass_eq","eq_iff_le_and_le","typeAEndpointGeneratorsGenerated_iff","typeAEndpointLifting_iff","isFibrant_iff","typeAEndpointGeneratorsGenerated_mono","typeAEndpointLifting_mono","isFibrant_antitone","standardABC_eq_canonical_iff_mutual_le"]
PATCHES = [["open KUOS.DependentOriginationGeneratedPresentationEndpointInvariantV1_80.\n  GeneratedScaledAnodynePresentationEquivalence","open KUOS.DependentOriginationGeneratedPresentationEndpointInvariantV1_80.GeneratedScaledAnodynePresentationEquivalence"],["open KUOS.DependentOriginationGeneratedPresentationQuotientInvariantV1_81","open KUOS.DependentOriginationGeneratedPresentationQuotientInvariantV1_81\nopen KUOS.DependentOriginationScaledTerminalRLPV1_41"],["instance : PartialOrder GeneratedScaledAnodynePresentation.{u} where","instance generatedPresentationPartialOrder : PartialOrder GeneratedScaledAnodynePresentation.{u} where"],["theorem standardABC_eq_canonical_iff_mutual_le :\n    standardABCPresentation = canonicalKuuOSPresentation ↔","theorem standardABC_eq_canonical_iff_mutual_le :\n    standardABCPresentation.{u} = canonicalKuuOSPresentation.{u} ↔"],["      standardABCPresentation ≤ canonicalKuuOSPresentation ∧\n        canonicalKuuOSPresentation ≤ standardABCPresentation :=","      standardABCPresentation.{u} ≤ canonicalKuuOSPresentation.{u} ∧\n        canonicalKuuOSPresentation.{u} ≤ standardABCPresentation.{u} :="],["  eq_iff_le_and_le _ _","  eq_iff_le_and_le.{u} _ _"]]
DECL = re.compile(r"(?m)^(?:@\[[^\]]+\]\s*)?(?:(?:private|noncomputable|protected|partial|unsafe)\s+)*(?:theorem|def|lemma|structure|instance|abbrev)\s+([^\s(:]+)")

def execute(out: Path) -> dict:
    verify_inputs()
    for name, expected in PARENTS.items():
        path = ROOT / "formal/KUOS" / (name + ".lean")
        if blob(path.read_bytes()) != expected:
            raise AuditFailure("V183_PARENT_BLOB_MISMATCH " + name)
    initial = ORIGINAL.read_bytes()
    if blob(initial) != ORIGINAL_BLOB:
        raise AuditFailure("V183_ORIGINAL_MODIFIED")
    raw = CANDIDATE.read_bytes()
    if blob(raw) != CANDIDATE_BLOB:
        raise AuditFailure("V183_CODEAI_CANDIDATE_MODIFIED")
    actual = raw.decode("utf8")
    expected = initial.decode("utf8").replace(
        "KUOS.DependentOriginationGeneratedPresentationPosetalReflectionV1_83", "KUOS.DependentOriginationGeneratedPresentationPosetalReflectionCodeAICandidateV1_83")
    for old, new in PATCHES:
        if expected.count(old) != 1:
            raise AuditFailure("V183_CODEAI_EDIT_PRECONDITION " + old[:60])
        expected = expected.replace(old, new)
    if actual != expected:
        raise AuditFailure("V183_UNREVIEWED_SOURCE_EDIT")
    masked = mask_lean_comments(actual)
    if re.search(r"(?m)^\s*(?:axiom|sorry|admit)\b", masked):
        raise AuditFailure("V183_TRUST_BYPASS")
    declarations = DECL.findall(masked)
    if declarations != BARE or len(QUALIFIED) != 18 or len(set(QUALIFIED)) != 18:
        raise AuditFailure("V183_PUBLIC_DECLARATION_INVENTORY " + repr(declarations))
    head = os.environ.get("SOURCE_HEAD", "")
    if re.fullmatch(r"[a-f0-9]{40}", head) is None:
        raise AuditFailure("NO_DATA_HEAD")
    out.mkdir(parents=True, exist_ok=True)
    if list(out.iterdir()):
        raise AuditFailure("APPEND_ONLY_RECEIPT_EXISTS")
    run_logged(["lake", "-KleanArgs=-DwarningAsError=true",
        "-KleanArgs=-DsorryAsError=true", "build", MODULE],
        out / "strict-build.log", 4800)
    with tempfile.TemporaryDirectory(dir=ROOT,prefix=".kuuos-v183-axioms-") as d:
        audit = Path(d) / "all-18.lean"
        audit.write_text("import " + MODULE + "\n" +
          "".join("#print axioms " + MODULE + "." + name + "\n"
                  for name in QUALIFIED), encoding="utf8")
        run_logged(["lake", "env", "lean", "-DwarningAsError=true",
            "-Dweak.sorryAsError=true", str(audit)],
            out / "axiom-audit.log", 1800)
    log = (out / "axiom-audit.log").read_text(errors="replace")
    reports = {}
    for name in QUALIFIED:
        full = MODULE + "." + name
        m = re.search(r"'" + re.escape(full) +
            r"'\s+depends on axioms:\s*\[([^\]]*)\]", log, re.S)
        if m:
            reports[name] = sorted(x.strip() for x in m.group(1).split(",") if x.strip())
        elif re.search(r"'" + re.escape(full) +
            r"'\s+does not depend on any axioms", log):
            reports[name] = []
        else:
            raise AuditFailure("V183_AXIOM_NO_DATA " + full)
    axioms = set(x for xs in reports.values() for x in xs)
    if axioms - STANDARD_AXIOMS or "sorryAx" in log:
        raise AuditFailure("V183_EXTRA_AXIOM " + repr(sorted(axioms - STANDARD_AXIOMS)))
    receipt = {
      "kind":"KUUOS_V183_CODEAI_EXACT_SOURCE_18_AXIOM_AUDIT",
      "head":head, "source_blob":CANDIDATE_BLOB,
      "original_blob":ORIGINAL_BLOB, "declared_public_constants":len(reports),
      "sha256":hashlib.sha256(raw).hexdigest(),
      "lean_pin":"leanprover/lean4:v4.30.0-rc2",
      "mathlib_pin":"5450b53e5ddc75d46418fabb605edbf36bd0beb6",
      "axioms":sorted(axioms),"sorryAx":False,"warnings":0,"errors":0,
      "source_adopted_in_PR":False,
      "full_canonical_standard_equivalence_asserted":False,
      "general_endpoint_RLP_asserted":False
    }
    (out/"receipt.json").write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+"\n")
    print("KUUOS_V183_CODEAI_KERNEL_GREEN "+json.dumps(receipt,ensure_ascii=False),flush=True)
    return receipt

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out",type=Path,required=True)
    args = ap.parse_args()
    try:
        execute(args.out.resolve())
        return 0
    except (AuditFailure,OSError,ValueError) as e:
        print("KUUOS_V183_CODEAI_HOLD "+json.dumps(
          {"status":"UNAUTHENTICATED","obstruction":str(e),"merged":False}),
          file=sys.stderr,flush=True)
        return 2

if __name__=="__main__":
    sys.exit(main())
