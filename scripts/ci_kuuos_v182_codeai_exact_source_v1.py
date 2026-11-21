#!/usr/bin/env python3
"""v1.82 CodeAI exact source candidate, pinned Lean + full 12-declaration axiom audit.

This is a research candidate only; no original-name adoption or main approval.
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

MODULE = "KUOS.DependentOriginationCanonicalEndpointLeibnizEpiDescentCodeAICandidateV1_82"
CANDIDATE = ROOT / "formal/KUOS/DependentOriginationCanonicalEndpointLeibnizEpiDescentCodeAICandidateV1_82.lean"
ORIGINAL = ROOT / "formal/KUOS/DependentOriginationCanonicalEndpointLeibnizEpiDescentV1_82.lean"
CANDIDATE_BLOB = "dfd32edc58d437bedfc06599ccc1909c46c963f6"
ORIGINAL_BLOB = "7180226c2b202606871d1c2c3efd966442c50fff"
PARENTS = {"DependentOriginationGeneratedPresentationQuotientInvariantV1_81":"8ba7b0e6034a2e24b44587fb477c2192cffffeca","DependentOriginationStandardTypeAScaledPushoutSourceEnrichmentV1_53":"e1101bc30b4e30a00a43a0ca6125cb1165c79227","DependentOriginationStandardTypeAGeneratedPushoutLLPDescentV1_54":"72d318ccb09a307251d7f204b9c0120e78bc7e26","DependentOriginationStandardTypeAScaledLeibnizPushoutV1_55":"be2fb30122c82a086304845cedc9a0964b524148"}
QUALIFIED = ["standardTypeAEndpointMinimalToGenerated","standardTypeAEndpointMinimalToGenerated_map","standardTypeAEndpointMinimalToGenerated_epi","standardTypeAEndpointMinimalToGenerated_comp_scaledLeibniz","llp_mem_of_epi_precomp","standardTypeAEndpointScaledLeibniz_mem_canonicalGenerated","standardTypeAScaledLeibnizPushoutProductGenerators_le_canonicalGenerated","canonicalTypeAEndpointLeibnizStabilityUnconditional","canonicalTypeAEndpointLeibnizLiftingUnconditional","canonicalKuuOSPresentation_endpointGeneratorsGenerated_unconditional","canonicalKuuOSPresentation_endpointStable_unconditional","canonicalKuuOSPresentation_endpointLifting_unconditional"]
BARE = ["standardTypeAEndpointMinimalToGenerated","standardTypeAEndpointMinimalToGenerated_map","standardTypeAEndpointMinimalToGenerated_epi","standardTypeAEndpointMinimalToGenerated_comp_scaledLeibniz","llp_mem_of_epi_precomp","standardTypeAEndpointScaledLeibniz_mem_canonicalGenerated","standardTypeAScaledLeibnizPushoutProductGenerators_le_canonicalGenerated","canonicalTypeAEndpointLeibnizStabilityUnconditional","canonicalTypeAEndpointLeibnizLiftingUnconditional","canonicalKuuOSPresentation_endpointGeneratorsGenerated_unconditional","canonicalKuuOSPresentation_endpointStable_unconditional","canonicalKuuOSPresentation_endpointLifting_unconditional"]
PATCHES = [["open KUOS.DependentOriginationGeneratedPresentationEndpointInvariantV1_80.\n  GeneratedScaledAnodynePresentationEquivalence","open KUOS.DependentOriginationGeneratedPresentationEndpointInvariantV1_80.GeneratedScaledAnodynePresentationEquivalence"],["theorem canonicalKuuOSPresentation_endpointGeneratorsGenerated_unconditional :\n    typeAEndpointGeneratorsGenerated canonicalKuuOSPresentation := by","theorem canonicalKuuOSPresentation_endpointGeneratorsGenerated_unconditional :\n    typeAEndpointGeneratorsGenerated.{u} canonicalKuuOSPresentation.{u} := by"],["theorem canonicalKuuOSPresentation_endpointStable_unconditional :\n    typeAEndpointStable canonicalKuuOSPresentation := by","theorem canonicalKuuOSPresentation_endpointStable_unconditional :\n    typeAEndpointStable.{u} canonicalKuuOSPresentation.{u} := by"],["theorem canonicalKuuOSPresentation_endpointLifting_unconditional :\n    typeAEndpointLifting canonicalKuuOSPresentation := by","theorem canonicalKuuOSPresentation_endpointLifting_unconditional :\n    typeAEndpointLifting.{u} canonicalKuuOSPresentation.{u} := by"]]
DECL = re.compile(r"(?m)^(?:@\\[[^\\]]+\\]\\s*)?(?:(?:private|noncomputable|protected|partial|unsafe)\\s+)*(?:theorem|def|lemma|structure|instance|abbrev)\\s+([^\\s(:]+)")

def execute(out: Path) -> dict:
    verify_inputs()
    for module, expected_sha in PARENTS.items():
        path = ROOT / "formal/KUOS" / (module + ".lean")
        if blob(path.read_bytes()) != expected_sha:
            raise AuditFailure("V182_PARENT_BLOB_MISMATCH " + module)
    raw_original = ORIGINAL.read_bytes()
    if blob(raw_original) != ORIGINAL_BLOB:
        raise AuditFailure("V182_ORIGINAL_CHANGED")
    raw = CANDIDATE.read_bytes()
    if blob(raw) != CANDIDATE_BLOB:
        raise AuditFailure("V182_CANDIDATE_BLOB_MISMATCH")
    actual = raw.decode("utf8")
    expected = raw_original.decode("utf8").replace(
        "KUOS.DependentOriginationCanonicalEndpointLeibnizEpiDescentV1_82", "KUOS.DependentOriginationCanonicalEndpointLeibnizEpiDescentCodeAICandidateV1_82")
    for old, new in PATCHES:
        if expected.count(old) != 1:
            raise AuditFailure("V182_CODEAI_EDIT_PRECONDITION " + old[:60])
        expected = expected.replace(old, new)
    if actual != expected:
        raise AuditFailure("V182_CODEAI_UNREVIEWED_EDIT")
    masked = mask_lean_comments(actual)
    if re.search(r"(?m)^\\s*(?:sorry|admit|axiom)\\b", masked):
        raise AuditFailure("V182_TRUST_BYPASS")
    declarations = DECL.findall(masked)
    if declarations != BARE or len(QUALIFIED) != 12 or len(set(QUALIFIED)) != 12:
        raise AuditFailure("V182_DECLARATION_INVENTORY " + repr(declarations))
    head = os.environ.get("SOURCE_HEAD", "")
    if re.fullmatch(r"[a-f0-9]{40}", head) is None:
        raise AuditFailure("NO_DATA_SOURCE_HEAD")
    out.mkdir(parents=True, exist_ok=True)
    if list(out.iterdir()):
        raise AuditFailure("APPEND_ONLY_RECEIPT_EXISTS")
    run_logged(["lake", "-KleanArgs=-DwarningAsError=true",
        "-KleanArgs=-DsorryAsError=true", "build", MODULE],
        out / "strict-build.log", 4800)
    with tempfile.TemporaryDirectory(dir=ROOT,prefix=".kuuos-v182-axiom-") as d:
        f = Path(d) / "all-12.lean"
        f.write_text("import " + MODULE + "\n" +
            "".join("#print axioms " + MODULE + "." + n + "\n" for n in QUALIFIED),
            encoding="utf8")
        run_logged(["lake", "env", "lean", "-DwarningAsError=true",
            "-Dweak.sorryAsError=true", str(f)], out / "axiom-audit.log", 1800)
    log = (out / "axiom-audit.log").read_text(errors="replace")
    reports={}
    for name in QUALIFIED:
        full=MODULE+"."+name
        m=re.search(r"'" + re.escape(full) +
            r"'\\s+depends on axioms:\\s*\\[([^\\]]*)\\]",log,re.S)
        if m: reports[name]=sorted(x.strip() for x in m.group(1).split(",") if x.strip())
        elif re.search(r"'" + re.escape(full) +
                      r"'\\s+does not depend on any axioms",log):
            reports[name]=[]
        else: raise AuditFailure("V182_AX_NO_DATA "+full)
    axioms=set(a for v in reports.values() for a in v)
    if axioms - STANDARD_AXIOMS or "sorryAx" in log:
        raise AuditFailure("V182_EXTRA_AXIOM "+str(sorted(axioms-STANDARD_AXIOMS)))
    receipt={
      "kind":"KUUOS_V182_CODEAI_EXACT_SOURCE_12_AXIOM_AUDIT",
      "head":head, "candidate_blob":CANDIDATE_BLOB,
      "original_blob":ORIGINAL_BLOB, "public_declarations":len(reports),
      "source_sha256":hashlib.sha256(raw).hexdigest(),
      "lean_pin":"leanprover/lean4:v4.30.0-rc2",
      "mathlib_pin":"5450b53e5ddc75d46418fabb605edbf36bd0beb6",
      "axioms":sorted(axioms),"sorryAx":False,"warnings":0,"errors":0,
      "source_adopted_in_PR":False, "canonical_equivalence_asserted":False,
      "general_endpoint_RLP_asserted":False
    }
    (out/"receipt.json").write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+"\n")
    print("KUUOS_V182_CODEAI_KERNEL_GREEN "+json.dumps(receipt,ensure_ascii=False),flush=True)
    return receipt

def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    try:
        execute(a.out.resolve())
        return 0
    except (AuditFailure,OSError,ValueError) as e:
        print("KUUOS_V182_CODEAI_HOLD "+json.dumps(
            {"status":"UNAUTHENTICATED","obstruction":str(e),"merged":False}),
            file=sys.stderr,flush=True)
        return 2

if __name__=="__main__":
    sys.exit(main())
