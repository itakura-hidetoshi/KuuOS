#!/usr/bin/env python3
"""Strict pinned exact-original-name audit of v1.80 adopted source in PR #3555.
Original-name PR adoption is NOT canonical main approval; external comparisons remain conditional.
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

MODULE = "KUOS.DependentOriginationGeneratedPresentationEndpointInvariantV1_80"
SOURCE = ROOT / "formal/KUOS/DependentOriginationGeneratedPresentationEndpointInvariantV1_80.lean"
ORIGINAL = ROOT / "formal/KUOS/DependentOriginationGeneratedPresentationEndpointCodeAICandidateV1_80.lean"
SOURCE_BLOB = "7be90de61f5c05456de6fa74dd1f262430486d84"
ORIGINAL_BLOB = "329dc28d69b120f400925d7cf6257b8afe9f4a27"
EXPECTED_PARENTS = {
    "DependentOriginationStandardTypeAEndpointOppositeCellCertificateV1_77": "d786495a68268e01634f6f8143ebe09241bffc3e",
    "DependentOriginationStandardABCPostEndpointCanonicalComparisonV1_78": "b406155d78506527b53549f0cf232d55f084ac86",
    "DependentOriginationStandardABCPositiveCanonicalResidualSplitV1_79": "cd9a58880341e70a2290387d21d144613464c8c0",
}
NAMES = [
    "GeneratedScaledAnodynePresentationEquivalence",
    "GeneratedScaledAnodynePresentationEquivalence.generatedAnodyne_eq",
    "GeneratedScaledAnodynePresentationEquivalence.ofGeneratedAnodyneEq",
    "GeneratedScaledAnodynePresentationEquivalence.iff_generatedAnodyne_eq",
    "GeneratedScaledAnodynePresentationEquivalence.refl",
    "GeneratedScaledAnodynePresentationEquivalence.symm",
    "GeneratedScaledAnodynePresentationEquivalence.trans",
    "GeneratedScaledAnodynePresentationEquivalence.generatedFibration_eq",
    "GeneratedScaledAnodynePresentationEquivalence.generatedAnodyne_mem_iff",
    "GeneratedScaledAnodynePresentationEquivalence.generatedFibration_mem_iff",
    "GeneratedScaledAnodynePresentationEquivalence.weakFactorizationSystem_iff",
    "GeneratedScaledAnodynePresentationEquivalence.TypeAEndpointLeibnizGeneratorsGeneratedBy",
    "GeneratedScaledAnodynePresentationEquivalence.TypeAEndpointLeibnizStableForPresentation",
    "GeneratedScaledAnodynePresentationEquivalence.TypeAEndpointLeibnizLiftingForPresentation",
    "GeneratedScaledAnodynePresentationEquivalence.typeAEndpointLeibnizGeneratorsGenerated_iff",
    "GeneratedScaledAnodynePresentationEquivalence.typeAEndpointLeibnizStable_iff",
    "GeneratedScaledAnodynePresentationEquivalence.typeAEndpointLeibnizLifting_iff",
    "GeneratedScaledAnodynePresentationEquivalence.fibrantForExternalGenerators_iff",
    "standardABC_typeAEndpointLeibnizGeneratorsGenerated",
    "standardABC_typeAEndpointLeibnizStable",
    "standardABC_typeAEndpointLeibnizLifting",
    "GeneratedScaledAnodynePresentationEquivalence.typeAEndpointLeibnizGeneratorsGenerated_of_standardEquivalent",
    "GeneratedScaledAnodynePresentationEquivalence.typeAEndpointLeibnizStable_of_standardEquivalent",
    "GeneratedScaledAnodynePresentationEquivalence.typeAEndpointLeibnizLifting_of_standardEquivalent",
    "GeneratedScaledAnodynePresentationEquivalence.standardTypeAExternalComparison_of_standardEquivalent",
    "GeneratedScaledAnodynePresentationEquivalence.inducedTypeAAttachments_le_of_standardEquivalent",
    "GeneratedScaledAnodynePresentationEquivalence.endpointPushoutProducts_le_of_standardEquivalent",
    "StandardABCCanonicalPositiveComparisonCertificate.toGeneratedPresentationEquivalence",
    "canonical_typeAEndpointLeibnizStable_of_positiveComparison",
    "canonical_typeAEndpointLeibnizLifting_of_positiveComparison"
]
PATCHES = [
  [
    "theorem generatedAnodyne_eq :",
    "theorem generatedAnodyne_eq (K : GeneratedScaledAnodynePresentationEquivalence E F) :"
  ],
  [
    "def symm :",
    "def symm (K : GeneratedScaledAnodynePresentationEquivalence E F) :"
  ],
  [
    "def trans\n    (L : GeneratedScaledAnodynePresentationEquivalence F G) :",
    "def trans\n    (K : GeneratedScaledAnodynePresentationEquivalence E F)\n    (L : GeneratedScaledAnodynePresentationEquivalence F G) :"
  ],
  [
    "theorem generatedFibration_eq :",
    "theorem generatedFibration_eq (K : GeneratedScaledAnodynePresentationEquivalence E F) :"
  ],
  [
    "theorem generatedAnodyne_mem_iff\n    {A B :",
    "theorem generatedAnodyne_mem_iff\n    (K : GeneratedScaledAnodynePresentationEquivalence E F)\n    {A B :"
  ],
  [
    "theorem generatedFibration_mem_iff\n    {A B :",
    "theorem generatedFibration_mem_iff\n    (K : GeneratedScaledAnodynePresentationEquivalence E F)\n    {A B :"
  ],
  [
    "theorem weakFactorizationSystem_iff :",
    "theorem weakFactorizationSystem_iff (K : GeneratedScaledAnodynePresentationEquivalence E F) :"
  ],
  [
    "theorem typeAEndpointLeibnizGeneratorsGenerated_iff :",
    "theorem typeAEndpointLeibnizGeneratorsGenerated_iff (K : GeneratedScaledAnodynePresentationEquivalence E F) :"
  ],
  [
    "theorem typeAEndpointLeibnizStable_iff :",
    "theorem typeAEndpointLeibnizStable_iff (K : GeneratedScaledAnodynePresentationEquivalence E F) :"
  ],
  [
    "theorem typeAEndpointLeibnizLifting_iff :",
    "theorem typeAEndpointLeibnizLifting_iff (K : GeneratedScaledAnodynePresentationEquivalence E F) :"
  ],
  [
    "theorem fibrantForExternalGenerators_iff\n    (X :",
    "theorem fibrantForExternalGenerators_iff\n    (K : GeneratedScaledAnodynePresentationEquivalence E F)\n    (X :"
  ],
  [
    "  (K.standardTypeAExternalComparison_of_standardEquivalent)\n    .inducedTypeAAttachments_le_externalGenerated",
    "  (K.standardTypeAExternalComparison_of_standardEquivalent).inducedTypeAAttachments_le_externalGenerated"
  ],
  [
    "  (K.standardTypeAExternalComparison_of_standardEquivalent)\n    .endpointPushoutProducts_le_externalGenerated",
    "  (K.standardTypeAExternalComparison_of_standardEquivalent).endpointPushoutProducts_le_externalGenerated"
  ],
  [
    "  K.toGeneratedPresentationEquivalence\n    .typeAEndpointLeibnizStable_of_standardEquivalent",
    "  GeneratedScaledAnodynePresentationEquivalence.typeAEndpointLeibnizStable_of_standardEquivalent\n    (StandardABCCanonicalPositiveComparisonCertificate.toGeneratedPresentationEquivalence K)"
  ],
  [
    "  K.toGeneratedPresentationEquivalence\n    .typeAEndpointLeibnizLifting_of_standardEquivalent",
    "  GeneratedScaledAnodynePresentationEquivalence.typeAEndpointLeibnizLifting_of_standardEquivalent\n    (StandardABCCanonicalPositiveComparisonCertificate.toGeneratedPresentationEquivalence K)"
  ]
]

BARE_NAMES = ["GeneratedScaledAnodynePresentationEquivalence","generatedAnodyne_eq","ofGeneratedAnodyneEq","iff_generatedAnodyne_eq","refl","symm","trans","generatedFibration_eq","generatedAnodyne_mem_iff","generatedFibration_mem_iff","weakFactorizationSystem_iff","TypeAEndpointLeibnizGeneratorsGeneratedBy","TypeAEndpointLeibnizStableForPresentation","TypeAEndpointLeibnizLiftingForPresentation","typeAEndpointLeibnizGeneratorsGenerated_iff","typeAEndpointLeibnizStable_iff","typeAEndpointLeibnizLifting_iff","fibrantForExternalGenerators_iff","standardABC_typeAEndpointLeibnizGeneratorsGenerated","standardABC_typeAEndpointLeibnizStable","standardABC_typeAEndpointLeibnizLifting","typeAEndpointLeibnizGeneratorsGenerated_of_standardEquivalent","typeAEndpointLeibnizStable_of_standardEquivalent","typeAEndpointLeibnizLifting_of_standardEquivalent","standardTypeAExternalComparison_of_standardEquivalent","inducedTypeAAttachments_le_of_standardEquivalent","endpointPushoutProducts_le_of_standardEquivalent","StandardABCCanonicalPositiveComparisonCertificate.toGeneratedPresentationEquivalence","canonical_typeAEndpointLeibnizStable_of_positiveComparison","canonical_typeAEndpointLeibnizLifting_of_positiveComparison"]
DECL_PATTERN = re.compile(r"(?m)^(?:@\[[^\]]+\]\s*)?(?:(?:private|noncomputable|protected|partial|unsafe)\s+)*(?:theorem|def|lemma|structure|instance|abbrev)\s+([^\s(:]+)")

def execute(out: Path) -> dict:
    verify_inputs()
    for module, expected in EXPECTED_PARENTS.items():
        path = ROOT / "formal/KUOS" / (module + ".lean")
        got = blob(path.read_bytes())
        if got != expected:
            raise AuditFailure("DEPENDENCY_BLOB_MISMATCH " + module + " " + got)
    if blob(ORIGINAL.read_bytes()) != ORIGINAL_BLOB:
        raise AuditFailure("INDEPENDENTLY_CERTIFIED_V180_CANDIDATE_MISSING_OR_CHANGED")
    current = SOURCE.read_bytes()
    if blob(current) != SOURCE_BLOB:
        raise AuditFailure("EXACT_CANDIDATE_BLOB_MISMATCH " + blob(current))
    text = current.decode("utf8")
    expected = ORIGINAL.read_text(encoding="utf8").replace("KUOS.DependentOriginationGeneratedPresentationEndpointCodeAICandidateV1_80", "KUOS.DependentOriginationGeneratedPresentationEndpointInvariantV1_80")
    if text != expected:
        raise AuditFailure("ADOPTED_V180_NOT_NAMESPACE_EQUIVALENT_TO_CERTIFIED_CANDIDATE")
    masked = mask_lean_comments(text)
    if re.search(r"(?m)^\s*(?:sorry|admit|axiom)\b", masked):
        raise AuditFailure("PROOF_BYPASS")
    actual = DECL_PATTERN.findall(masked)
    if actual != BARE_NAMES or len(NAMES) != 30 or len(set(NAMES)) != 30:
        raise AuditFailure("DECLARATION_OR_SCOPE_INVENTORY_MISMATCH")
    head = os.environ.get("SOURCE_HEAD", "")
    if not re.fullmatch("[a-f0-9]{40}", head):
        raise AuditFailure("NO_DATA_SOURCE_HEAD")
    out.mkdir(parents=True, exist_ok=True)
    if list(out.iterdir()):
        raise AuditFailure("APPEND_ONLY_VIOLATION")
    run_logged(["lake", "-KleanArgs=-DwarningAsError=true",
                "-KleanArgs=-DsorryAsError=true", "build", MODULE],
               out / "strict-build.log", 4800)
    with tempfile.TemporaryDirectory(dir=ROOT, prefix=".kuuos-v180-axioms-") as d:
        audit = Path(d) / "all-30.lean"
        audit.write_text(
            "import " + MODULE + "\n" +
            "".join("#print axioms " + MODULE + "." + n + "\n" for n in NAMES),
            encoding="utf8"
        )
        run_logged(["lake", "env", "lean", "-DwarningAsError=true",
                    "-Dweak.sorryAsError=true", str(audit)],
                   out / "axiom-audit.log", 1800)
    log = (out / "axiom-audit.log").read_text(errors="replace")
    reports = {}
    for name in NAMES:
        fq = MODULE + "." + name
        m = re.search(r"'" + re.escape(fq) + r"'\s+depends on axioms:\s*\[([^\]]*)\]", log, re.S)
        if m:
            reports[name] = sorted(x.strip() for x in m.group(1).split(",") if x.strip())
        elif re.search(r"'" + re.escape(fq) + r"'\s+does not depend on any axioms", log):
            reports[name] = []
        else:
            raise AuditFailure("AXIOM_NO_DATA " + fq)
    union = set(ax for v in reports.values() for ax in v)
    if union - STANDARD_AXIOMS or "sorryAx" in log:
        raise AuditFailure("EXTRA_AXIOM " + ",".join(sorted(union - STANDARD_AXIOMS)))
    result = {
        "kind": "KUUOS_V180_ADOPTED_EXACT_SOURCE_30_AXIOM_AUDIT",
        "head": head, "certified_candidate_head": "4696f8a5b17490189852151d5fc90c3f5e14c995",
        "source_blob": SOURCE_BLOB,
        "original_blob": ORIGINAL_BLOB,
        "source_sha256": hashlib.sha256(current).hexdigest(),
        "lean_pin": "leanprover/lean4:v4.30.0-rc2",
        "mathlib_pin": "5450b53e5ddc75d46418fabb605edbf36bd0beb6",
        "public_declarations": len(reports), "axioms": sorted(union),
        "sorryAx": False, "warnings": 0, "errors": 0,
        "source_adopted_in_PR": True, "source_adopted_on_main": False, "canonical_general_endpoint_RLP": False,
        "external_approval": "PENDING_UNTIL_WORKFLOW_JOB_SUCCESS",
    }
    (out / "receipt.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print("KUUOS_V180_ADOPTED_KERNEL_GREEN " + json.dumps(result, ensure_ascii=False), flush=True)
    return result

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    try:
        execute(args.out.resolve())
        return 0
    except (AuditFailure, OSError, ValueError) as e:
        print("KUUOS_V180_ADOPTED_HOLD " + json.dumps({
            "status": "UNAUTHENTICATED", "obstruction": str(e),
            "source_adopted_in_PR": True, "merged": False,
        }), file=sys.stderr, flush=True)
        return 2

if __name__ == "__main__":
    sys.exit(main())
