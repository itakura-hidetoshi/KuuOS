#!/usr/bin/env python3
"""Exact v1.83 PR-adopted source: pinned Strict Lean and 18-public-declaration axiom audit.

The original-name module is byte-bound to independent-green CodeAI candidate
except for its namespace. No general scaled fibrancy or presentation equality.
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

MODULE = "KUOS.DependentOriginationGeneratedPresentationPosetalReflectionV1_83"
ADOPTED = ROOT / "formal/KUOS/DependentOriginationGeneratedPresentationPosetalReflectionV1_83.lean"
CERTIFIED_CANDIDATE = ROOT / "formal/KUOS/DependentOriginationGeneratedPresentationPosetalReflectionCodeAICandidateV1_83.lean"
HISTORICAL = ROOT / "legacy/v5.291/formal/KUOS/DependentOriginationGeneratedPresentationPosetalReflectionV1_83.lean"
ADOPTED_BLOB = "3bc1f096876f8c7b799ae48f29419e6686e33c87"
CERTIFIED_CANDIDATE_BLOB = "b7ea6b8f672234000d5bef235055c853cddfb5b6"
HISTORICAL_BLOB = "677031aa601d232ff11ba8aaba26653fd68134ee"
CERTIFIED_CANDIDATE_HEAD = "c53a82e12ed631452fa62e2bff4d0897299a0df2"
CERTIFIED_CANDIDATE_RUN = 44941314882
PARENTS = {
    "DependentOriginationGeneratedPresentationEndpointInvariantV1_80": "7be90de61f5c05456de6fa74dd1f262430486d84",
    "DependentOriginationGeneratedPresentationQuotientInvariantV1_81": "8ba7b0e6034a2e24b44587fb477c2192cffffeca",
    "DependentOriginationCanonicalEndpointLeibnizEpiDescentV1_82": "a1acb5e5c4c5fc41229e595441e7ad826d3e9c31",
}
PUBLIC = ["generatedAnodyneClass_rlp","generatedFibrationClass_llp","eq_of_generatedAnodyneClass_eq","eq_iff_generatedAnodyneClass_eq","generatedPresentationPartialOrder","le_iff_generatedAnodyneClass_le","generatedFibrationClass_antitone","le_of_generatedFibrationClass_reverse","le_iff_generatedFibrationClass_reverse_le","eq_iff_generatedFibrationClass_eq","eq_iff_le_and_le","typeAEndpointGeneratorsGenerated_iff","typeAEndpointLifting_iff","isFibrant_iff","typeAEndpointGeneratorsGenerated_mono","typeAEndpointLifting_mono","isFibrant_antitone","standardABC_eq_canonical_iff_mutual_le"]
DECL = re.compile(r"(?m)^(?:@\[[^\]]+\]\s*)?(?:(?:private|noncomputable|protected|partial|unsafe)\s+)*(?:theorem|def|lemma|structure|instance|abbrev)\s+([^\s(:]+)")


def execute(out: Path) -> dict:
    verify_inputs()
    for module, expected in PARENTS.items():
        actual = blob((ROOT / "formal/KUOS" / (module + ".lean")).read_bytes())
        if actual != expected:
            raise AuditFailure("V183_ADOPTED_PARENT_BLOB_MISMATCH " + module)
    if blob(HISTORICAL.read_bytes()) != HISTORICAL_BLOB:
        raise AuditFailure("V183_HISTORICAL_ROOT_MODIFIED")
    certified = CERTIFIED_CANDIDATE.read_bytes()
    if blob(certified) != CERTIFIED_CANDIDATE_BLOB:
        raise AuditFailure("V183_CERTIFIED_CANDIDATE_CHANGED")
    raw = ADOPTED.read_bytes()
    if blob(raw) != ADOPTED_BLOB:
        raise AuditFailure("V183_ADOPTED_BLOB_MISMATCH")
    expected = certified.decode("utf8").replace(
        "KUOS.DependentOriginationGeneratedPresentationPosetalReflectionCodeAICandidateV1_83", "KUOS.DependentOriginationGeneratedPresentationPosetalReflectionV1_83")
    if raw.decode("utf8") != expected:
        raise AuditFailure("V183_NOT_NAMESPACE_ONLY_ADOPTION")
    masked = mask_lean_comments(raw.decode("utf8"))
    if re.search(r"(?m)^\s*(?:axiom|sorry|admit)\b", masked):
        raise AuditFailure("V183_ADOPTED_TRUST_BYPASS")
    inventory = DECL.findall(masked)
    if inventory != PUBLIC or len(PUBLIC) != 18 or len(set(PUBLIC)) != 18:
        raise AuditFailure("V183_ADOPTED_PUBLIC_INVENTORY " + repr(inventory))
    head = os.environ.get("SOURCE_HEAD", "")
    if re.fullmatch(r"[a-f0-9]{40}", head) is None:
        raise AuditFailure("V183_NO_DATA_HEAD")
    out.mkdir(parents=True, exist_ok=True)
    if list(out.iterdir()):
        raise AuditFailure("V183_APPEND_ONLY_RECEIPT_EXISTS")
    run_logged(
        ["lake", "-KleanArgs=-DwarningAsError=true",
         "-KleanArgs=-DsorryAsError=true", "build", MODULE],
        out / "strict-build.log", 4800,
    )
    with tempfile.TemporaryDirectory(dir=ROOT,prefix=".kuuos-v183-adopted-axioms-") as d:
        proof = Path(d) / "all-18.lean"
        proof.write_text("import " + MODULE + "\n" +
            "".join("#print axioms " + MODULE + "." + name + "\n" for name in PUBLIC),
            encoding="utf8")
        run_logged(
            ["lake", "env", "lean", "-DwarningAsError=true",
             "-Dweak.sorryAsError=true", str(proof)],
            out / "axiom-audit.log", 1800,
        )
    log = (out / "axiom-audit.log").read_text(errors="replace")
    reports = {}
    for name in PUBLIC:
        full = MODULE + "." + name
        m = re.search(r"'" + re.escape(full) +
            r"'\s+depends on axioms:\s*\[([^\]]*)\]", log, re.S)
        if m:
            reports[name] = sorted(x.strip() for x in m.group(1).split(",") if x.strip())
        elif re.search(r"'" + re.escape(full) +
                       r"'\s+does not depend on any axioms", log):
            reports[name] = []
        else:
            raise AuditFailure("V183_ADOPTED_AXIOM_NO_DATA " + full)
    axioms = set(a for values in reports.values() for a in values)
    if axioms - STANDARD_AXIOMS or "sorryAx" in log:
        raise AuditFailure("V183_ADOPTED_EXTRA_AXIOM " + repr(sorted(axioms - STANDARD_AXIOMS)))
    receipt = {
        "kind":"KUUOS_V183_PR_ADOPTED_EXACT_SOURCE_18_AXIOM_AUDIT",
        "head":head, "adopted_blob":ADOPTED_BLOB,
        "certified_candidate_blob":CERTIFIED_CANDIDATE_BLOB,
        "certified_candidate_head":CERTIFIED_CANDIDATE_HEAD,
        "certified_candidate_run":CERTIFIED_CANDIDATE_RUN,
        "historical_blob":HISTORICAL_BLOB,
        "source_sha256":hashlib.sha256(raw).hexdigest(),
        "declared_public_constants":len(reports),
        "lean_pin":"leanprover/lean4:v4.30.0-rc2",
        "mathlib_pin":"5450b53e5ddc75d46418fabb605edbf36bd0beb6",
        "axioms":sorted(axioms), "sorryAx":False, "warnings":0,"errors":0,
        "source_adopted_in_PR":True, "source_adopted_on_main":False,
        "standard_canonical_equivalence_asserted":False,
        "general_forward_endpoint_RLP_asserted":False,
    }
    (out / "receipt.json").write_text(json.dumps(receipt,indent=2,ensure_ascii=False) + "\n")
    print("KUUOS_V183_PR_ADOPTED_KERNEL_GREEN " +
          json.dumps(receipt,ensure_ascii=False), flush=True)
    return receipt


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out",type=Path,required=True)
    args = ap.parse_args()
    try:
        execute(args.out.resolve())
        return 0
    except (AuditFailure,OSError,ValueError) as exc:
        print("KUUOS_V183_PR_ADOPTED_HOLD " + json.dumps({
            "status":"UNAUTHENTICATED", "obstruction":str(exc), "merged":False,
        }),file=sys.stderr,flush=True)
        return 2


if __name__ == "__main__":
    sys.exit(main())
