#!/usr/bin/env python3
"""v1.84 CodeAI isolated exact source, pinned Lean4 and 13-declaration axiom audit.

Candidate source is constrained to two exact repairs, and kept separate from
original-name module until this exact-head independent gate is SUCCESS.
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

MODULE = "KUOS.DependentOriginationGeneratedPresentationOrderReflectionCodeAICandidateV1_84"
ORIGINAL = ROOT / "formal/KUOS/DependentOriginationGeneratedPresentationOrderReflectionV1_84.lean"
CANDIDATE = ROOT / "formal/KUOS/DependentOriginationGeneratedPresentationOrderReflectionCodeAICandidateV1_84.lean"
HISTORICAL = ROOT / "legacy/v5.291/formal/KUOS/DependentOriginationGeneratedPresentationOrderReflectionV1_84.lean"
ORIGINAL_BLOB = "baf70fc20347e881054fb86180de849ebf92f71f"
CANDIDATE_BLOB = "2dc4ab85f1b471a50ae508dd7a6ee0160d1a0535"
PARENTS = {
    "DependentOriginationGeneratedPresentationPosetalReflectionV1_83": "3bc1f096876f8c7b799ae48f29419e6686e33c87",
    "DependentOriginationGeneratedPresentationQuotientInvariantV1_81": "8ba7b0e6034a2e24b44587fb477c2192cffffeca",
    "DependentOriginationGeneratedPresentationEndpointInvariantV1_80": "7be90de61f5c05456de6fa74dd1f262430486d84",
    "DependentOriginationStandardABCPositiveCanonicalResidualSplitV1_79": "cd9a58880341e70a2290387d21d144613464c8c0",
}
PUBLIC = ["GeneratedPresentationPreorderLE","generatedPresentationPreorderLE_refl","generatedPresentationPreorderLE_trans","presentationClass_le_iff_generators_le_generated","presentationClass_eq_iff_mutual_preorder","generatedPresentationEquivalence_iff_mutual_preorder","presentationClass_eq_iff_generatedPresentationEquivalence","canonicalKuuOS_le_standardABC_iff_canonicalGenerators_le_standardGenerated","standardABC_le_canonicalKuuOS_iff_standardGenerators_le_canonicalGenerated","canonicalKuuOS_le_standardABC_of_positiveResidual","standardABC_le_canonicalKuuOS_iff_generatorwiseReverse","standardABC_eq_canonicalKuuOS_iff_direct_generator_inclusions","standardABC_eq_canonicalKuuOS_of_positiveComparison_via_order"]
PATCHES = [["open KUOS.DependentOriginationGeneratedPresentationPosetalReflectionV1_83","open KUOS.DependentOriginationGeneratedPresentationPosetalReflectionV1_83\nopen KUOS.DependentOriginationScaledTerminalRLPV1_41"],["  · intro h\n    subst F\n    exact\n      <| And.intro\n        (generatedPresentationPreorderLE_refl E)\n        (generatedPresentationPreorderLE_refl E)","  · intro h\n    constructor\n    · exact\n        (presentationClass_le_iff_generators_le_generated E F).mp\n          (le_of_eq h)\n    · exact\n        (presentationClass_le_iff_generators_le_generated F E).mp\n          (le_of_eq h.symm)"],["theorem canonicalKuuOS_le_standardABC_iff_canonicalGenerators_le_standardGenerated :\n    canonicalKuuOSPresentation <= standardABCPresentation <->","theorem canonicalKuuOS_le_standardABC_iff_canonicalGenerators_le_standardGenerated :\n    canonicalKuuOSPresentation.{u} <= standardABCPresentation.{u} <->"],["theorem standardABC_le_canonicalKuuOS_iff_standardGenerators_le_canonicalGenerated :\n    standardABCPresentation <= canonicalKuuOSPresentation <->","theorem standardABC_le_canonicalKuuOS_iff_standardGenerators_le_canonicalGenerated :\n    standardABCPresentation.{u} <= canonicalKuuOSPresentation.{u} <->"],["    (K : StandardABCCanonicalPositiveResidualComparison.{u}) :\n    canonicalKuuOSPresentation <= standardABCPresentation := by","    (K : StandardABCCanonicalPositiveResidualComparison.{u}) :\n    canonicalKuuOSPresentation.{u} <= standardABCPresentation.{u} := by"],["theorem standardABC_le_canonicalKuuOS_iff_generatorwiseReverse :\n    standardABCPresentation <= canonicalKuuOSPresentation <->","theorem standardABC_le_canonicalKuuOS_iff_generatorwiseReverse :\n    standardABCPresentation.{u} <= canonicalKuuOSPresentation.{u} <->"],["theorem standardABC_eq_canonicalKuuOS_iff_direct_generator_inclusions :\n    standardABCPresentation = canonicalKuuOSPresentation <->","theorem standardABC_eq_canonicalKuuOS_iff_direct_generator_inclusions :\n    standardABCPresentation.{u} = canonicalKuuOSPresentation.{u} <->"],["    (K : StandardABCCanonicalPositiveComparisonCertificate.{u}) :\n    standardABCPresentation = canonicalKuuOSPresentation := by","    (K : StandardABCCanonicalPositiveComparisonCertificate.{u}) :\n    standardABCPresentation.{u} = canonicalKuuOSPresentation.{u} := by"]]
DECL = re.compile(r"(?m)^(?:@\[[^\]]+\]\s*)?(?:(?:private|noncomputable|protected|partial|unsafe)\s+)*(?:theorem|def|lemma|structure|instance|abbrev)\s+([^\s(:]+)")

def execute(out: Path) -> dict:
    verify_inputs()
    for module, expected_blob in PARENTS.items():
        actual = blob((ROOT / "formal/KUOS" / (module + ".lean")).read_bytes())
        if actual != expected_blob:
            raise AuditFailure("V184_PARENT_BLOB_MISMATCH " + module)
    initial = ORIGINAL.read_bytes()
    if blob(initial) != ORIGINAL_BLOB or blob(HISTORICAL.read_bytes()) != ORIGINAL_BLOB:
        raise AuditFailure("V184_ORIGINAL_OR_HISTORICAL_CHANGED")
    raw = CANDIDATE.read_bytes()
    if blob(raw) != CANDIDATE_BLOB:
        raise AuditFailure("V184_CANDIDATE_BLOB_CHANGED")
    actual = raw.decode("utf8")
    expected = initial.decode("utf8").replace(
        "KUOS.DependentOriginationGeneratedPresentationOrderReflectionV1_84", "KUOS.DependentOriginationGeneratedPresentationOrderReflectionCodeAICandidateV1_84")
    for old, new in PATCHES:
        if expected.count(old) != 1:
            raise AuditFailure("V184_CODEAI_EDIT_PRECONDITION " + old[:60])
        expected = expected.replace(old, new)
    if actual != expected:
        raise AuditFailure("V184_CODEAI_UNREVIEWED_SOURCE_EDIT")
    masked = mask_lean_comments(actual)
    if re.search(r"(?m)^\s*(?:sorry|admit|axiom)\b", masked):
        raise AuditFailure("V184_TRUST_BYPASS")
    declarations = DECL.findall(masked)
    if declarations != PUBLIC or len(PUBLIC) != 13 or len(set(PUBLIC)) != 13:
        raise AuditFailure("V184_DECLARATION_INVENTORY " + repr(declarations))
    head = os.environ.get("SOURCE_HEAD", "")
    if not re.fullmatch(r"[a-f0-9]{40}", head):
        raise AuditFailure("V184_NO_DATA_HEAD")
    out.mkdir(parents=True, exist_ok=True)
    if list(out.iterdir()):
        raise AuditFailure("V184_APPEND_ONLY_RECEIPT_EXISTS")
    run_logged(
        ["lake", "-KleanArgs=-DwarningAsError=true",
         "-KleanArgs=-DsorryAsError=true", "build", MODULE],
        out / "strict-build.log", 4800)
    with tempfile.TemporaryDirectory(dir=ROOT,prefix=".kuuos-v184-axioms-") as d:
        audit = Path(d) / "all-13.lean"
        audit.write_text("import " + MODULE + "\n" +
            "".join("#print axioms " + MODULE + "." + name + "\n" for name in PUBLIC),
            encoding="utf8")
        run_logged(
            ["lake", "env", "lean", "-DwarningAsError=true",
             "-Dweak.sorryAsError=true", str(audit)],
            out / "axiom-audit.log", 1800)
    log = (out / "axiom-audit.log").read_text(errors="replace")
    reports = {}
    for name in PUBLIC:
        full = MODULE + "." + name
        match = re.search(r"'" + re.escape(full) +
            r"'\s+depends on axioms:\s*\[([^\]]*)\]", log, re.S)
        if match:
            reports[name] = sorted(a.strip() for a in match.group(1).split(",") if a.strip())
        elif re.search(r"'" + re.escape(full) + r"'\s+does not depend on any axioms", log):
            reports[name] = []
        else:
            raise AuditFailure("V184_AXIOM_NO_DATA " + full)
    axioms = set(a for values in reports.values() for a in values)
    if axioms - STANDARD_AXIOMS or "sorryAx" in log:
        raise AuditFailure("V184_NONSTANDARD_AXIOM " + repr(sorted(axioms - STANDARD_AXIOMS)))
    receipt = {
        "kind": "KUUOS_V184_CODEAI_EXACT_SOURCE_13_AXIOM_AUDIT",
        "head":head,"source_blob":CANDIDATE_BLOB,"original_blob":ORIGINAL_BLOB,
        "source_sha256":hashlib.sha256(raw).hexdigest(),
        "public_declarations":len(reports),
        "lean_pin":"leanprover/lean4:v4.30.0-rc2",
        "mathlib_pin":"5450b53e5ddc75d46418fabb605edbf36bd0beb6",
        "axioms":sorted(axioms),"sorryAx":False,"warnings":0,"errors":0,
        "adopted_in_PR":False,"canonical_eq_standard_asserted":False,
        "arbitrary_scaling_endpoint_RLP_asserted":False,
    }
    (out / "receipt.json").write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+"\n")
    print("KUUOS_V184_CODEAI_KERNEL_GREEN "+json.dumps(receipt,ensure_ascii=False),flush=True)
    return receipt

def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args()
    try:
        execute(args.out.resolve())
        return 0
    except (AuditFailure,OSError,ValueError) as exc:
        print("KUUOS_V184_CODEAI_HOLD "+json.dumps({
            "status":"UNAUTHENTICATED","obstruction":str(exc),"merged":False,
        }),file=sys.stderr,flush=True)
        return 2

if __name__ == "__main__":
    sys.exit(main())
