#!/usr/bin/env python3
"""KuuOS-native CodeAI v1.87 repair round 2: typed-feedback, source-bound verification.

Failure 44961548765 and PR Strict Lean 44962018083 are REJECTED evidence.
R2 is a distinct candidate, not a replacement of the original, the frozen
v5.291, or the R1 candidate. Independent kernel, not model ranking, decides.
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

MODULE = "KUOS.DependentOriginationStandardCanonicalPresentationGapCodeAICandidateR2V1_87"
ORIGINAL_MODULE = r1.MODULE
ORIGINAL = r1.ORIGINAL
PREVIOUS = r1.CANDIDATE
CANDIDATE = ROOT / "formal/KUOS/DependentOriginationStandardCanonicalPresentationGapCodeAICandidateR2V1_87.lean"
ORIGINAL_BLOB = r1.ORIGINAL_BLOB
PREVIOUS_BLOB = r1.CANDIDATE_BLOB
CANDIDATE_BLOB = "1ba284fa92c153bb28defc4c84d1bd23d4e01522"
PUBLIC = r1.PUBLIC
TYPED_REPAIR = (
    "NONCOMPUTABLE_COMPLETE_LATTICE",
    "UNIVERSE_UNIFICATION_STANDARD_CANONICAL",
    "ORDER_LATTICE_REWRITE_DIRECTION",
    "SCALED_SSET_NAMESPACE_RESOLUTION",
)
OLD_NS = "KUOS.DependentOriginationStandardCanonicalPresentationGapCodeAICandidateV1_87"
NEW_NS = "KUOS.DependentOriginationStandardCanonicalPresentationGapCodeAICandidateR2V1_87"

def replace_once(s: str, old: str, new: str, count: int = 1) -> str:
    if s.count(old) != count:
        raise AuditFailure("V187_R2_TYPED_HUNK_PRECONDITION " + repr(old[:80]))
    return s.replace(old, new)

def reconstruct_from_rejected_candidate(source: str) -> str:
    s = replace_once(source, OLD_NS, NEW_NS, 2)
    s = replace_once(s, "\nuniverse u\n", "\nuniverse u\n\nnoncomputable section\n")
    s = re.sub(r"\bstandardABCPresentation\b(?!\.\{u\})", "standardABCPresentation.{u}", s)
    s = re.sub(r"\bcanonicalKuuOSPresentation\b(?!\.\{u\})", "canonicalKuuOSPresentation.{u}", s)
    fixes = [
      (
        "    exact inf_eq_right.mpr h\n  · intro h\n    rw [← h]\n    exact lowerEnvelope_le_standardABC",
        "    change (standardABCPresentation.{u} ⊓ canonicalKuuOSPresentation.{u}) =\n"
        "      canonicalKuuOSPresentation.{u}\n"
        "    exact inf_eq_right.mpr h\n  · intro h\n"
        "    calc\n"
        "      canonicalKuuOSPresentation.{u} = standardCanonicalLowerEnvelope.{u} := h.symm\n"
        "      _ ≤ standardABCPresentation.{u} := lowerEnvelope_le_standardABC",
      ),
      (
        "    exact sup_eq_left.mpr h\n  · intro h\n    rw [← h]\n    exact canonicalKuuOS_le_upperEnvelope",
        "    change (standardABCPresentation.{u} ⊔ canonicalKuuOSPresentation.{u}) =\n"
        "      standardABCPresentation.{u}\n"
        "    exact sup_eq_left.mpr h\n  · intro h\n"
        "    calc\n"
        "      canonicalKuuOSPresentation.{u} ≤ standardCanonicalUpperEnvelope.{u} :=\n"
        "        canonicalKuuOS_le_upperEnvelope\n"
        "      _ = standardABCPresentation.{u} := h",
      ),
      (
        "    exact inf_eq_left.mpr h\n  · intro h\n    rw [← h]\n    exact lowerEnvelope_le_canonicalKuuOS",
        "    change (standardABCPresentation.{u} ⊓ canonicalKuuOSPresentation.{u}) =\n"
        "      standardABCPresentation.{u}\n"
        "    exact inf_eq_left.mpr h\n  · intro h\n"
        "    calc\n"
        "      standardABCPresentation.{u} = standardCanonicalLowerEnvelope.{u} := h.symm\n"
        "      _ ≤ canonicalKuuOSPresentation.{u} := lowerEnvelope_le_canonicalKuuOS",
      ),
      (
        "    exact sup_eq_right.mpr h\n  · intro h\n    rw [← h]\n    exact standardABC_le_upperEnvelope",
        "    change (standardABCPresentation.{u} ⊔ canonicalKuuOSPresentation.{u}) =\n"
        "      canonicalKuuOSPresentation.{u}\n"
        "    exact sup_eq_right.mpr h\n  · intro h\n"
        "    calc\n"
        "      standardABCPresentation.{u} ≤ standardCanonicalUpperEnvelope.{u} :=\n"
        "        standardABC_le_upperEnvelope\n"
        "      _ = canonicalKuuOSPresentation.{u} := h",
      ),
    ]
    for old, new in fixes:
        s = replace_once(s, old, new)
    return replace_once(s, "\nend " + NEW_NS + "\n",
                        "\nend\nend " + NEW_NS + "\n")

def execute(out: Path) -> dict:
    verify_inputs()
    for name, expected in r1.PARENTS.items():
        f = ROOT / "formal/KUOS" / (name + ".lean")
        if blob(f.read_bytes()) != expected:
            raise AuditFailure("V187_R2_PARENT_CHANGED " + name)
    if blob(ORIGINAL.read_bytes()) != ORIGINAL_BLOB or blob(r1.HISTORICAL.read_bytes()) != ORIGINAL_BLOB:
        raise AuditFailure("V187_R2_ORIGINAL_OR_HISTORY_CHANGED")
    if blob(PREVIOUS.read_bytes()) != PREVIOUS_BLOB:
        raise AuditFailure("V187_R2_REJECTED_CANDIDATE_CHANGED")
    source = CANDIDATE.read_bytes()
    if blob(source) != CANDIDATE_BLOB:
        raise AuditFailure("V187_R2_CANDIDATE_BLOB_MISMATCH")
    if source.decode("utf8") != reconstruct_from_rejected_candidate(PREVIOUS.read_text(encoding="utf8")):
        raise AuditFailure("V187_R2_UNREVIEWED_CHANGE")
    masked = mask_lean_comments(source.decode("utf8"))
    if re.search(r"(?m)^\s*(?:sorry|admit|axiom)\b", masked):
        raise AuditFailure("V187_R2_TRUST_BYPASS")
    declarations = r1.DECL.findall(masked)
    if declarations != PUBLIC or len(PUBLIC) != 27:
        raise AuditFailure("V187_R2_INVENTORY " + repr(declarations))
    head = os.getenv("SOURCE_HEAD", "")
    if not re.fullmatch(r"[a-f0-9]{40}", head):
        raise AuditFailure("V187_R2_HEAD_NO_DATA")
    out.mkdir(parents=True, exist_ok=True)
    if list(out.iterdir()):
        raise AuditFailure("V187_R2_NONEMPTY_APPEND_ONLY_RECEIPT")
    run_logged(["lake", "-KleanArgs=-DwarningAsError=true", "-KleanArgs=-DsorryAsError=true",
                "build", MODULE], out / "strict-build.log", 4800)
    with tempfile.TemporaryDirectory(dir=ROOT, prefix=".kuuos-v187-r2-axioms-") as temp:
        audit = Path(temp) / "all-27.lean"
        audit.write_text("import " + MODULE + "\n" +
            "".join("#print axioms " + MODULE + "." + name + "\n" for name in PUBLIC),
            encoding="utf8")
        run_logged(["lake", "env", "lean", "-DwarningAsError=true",
                    "-Dweak.sorryAsError=true", str(audit)], out / "axiom-audit.log", 1800)
    log = (out / "axiom-audit.log").read_text(errors="replace")
    reports = {}
    for name in PUBLIC:
        match = re.search(r"'" + re.escape(MODULE + "." + name) +
           r"'\s+depends on axioms:\s*\[([^\]]*)\]", log, re.S)
        if match:
            reports[name] = sorted(x.strip() for x in match.group(1).split(",") if x.strip())
        elif re.search(r"'" + re.escape(MODULE + "." + name) + r"'\s+does not depend on any axioms", log):
            reports[name] = []
        else:
            raise AuditFailure("V187_R2_AXIOM_RECEIPT_MISSING " + name)
    used = {a for values in reports.values() for a in values}
    if used - STANDARD_AXIOMS or "sorryAx" in log:
        raise AuditFailure("V187_R2_NONSTANDARD_AXIOMS " + repr(sorted(used - STANDARD_AXIOMS)))
    receipt = {
      "kind": "KUUOS_CODEAI_V187_R2_EXACT_SOURCE_27_AXIOMS",
      "source_head": head, "source_blob": CANDIDATE_BLOB,
      "rejected_r1_blob": PREVIOUS_BLOB, "original_blob": ORIGINAL_BLOB,
      "source_sha256": hashlib.sha256(source).hexdigest(),
      "typed_feedback": TYPED_REPAIR, "public_declarations": 27,
      "axioms": sorted(used), "sorryAx": False, "warnings": 0, "errors": 0,
      "lean_pin": "leanprover/lean4:v4.30.0-rc2",
      "mathlib_pin": "5450b53e5ddc75d46418fabb605edbf36bd0beb6",
      "candidate_proposal_only": True, "original_changed": False,
      "adopted_on_PR": False, "global_gap_closed": False,
      "general_forward_endpoint_RLP_proven": False,
      "memory_promoted": False, "merge_authorized": False,
    }
    (out / "receipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
    print("KUUOS_V187_R2_INDEPENDENT_27_GREEN " + json.dumps(receipt, ensure_ascii=False), flush=True)
    return receipt

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--out", required=True, type=Path)
    args = p.parse_args()
    try:
        execute(args.out.resolve())
        return 0
    except (AuditFailure, ValueError, OSError) as e:
        print("KUUOS_V187_R2_HOLD " + json.dumps({
           "status": "UNAUTHENTICATED", "reason": str(e),
           "merged": False, "memory_promoted": False
        }), file=sys.stderr, flush=True)
        return 2

if __name__ == "__main__":
    sys.exit(main())
