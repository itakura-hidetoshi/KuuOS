#!/usr/bin/env python3
"""Research-only v1.104 R1 direct Lean candidate cycle. No independent CI or PR mutation."""
from __future__ import annotations
import json
import os
from pathlib import Path
from scripts import kuuos_sandbox_lean_cycle_v1 as cycle

ROOT = Path(__file__).resolve().parents[1]
BRANCH = "research/v1104-codeai-r1b-20261124"
ORIGINAL = ROOT / "formal/KUOS/DependentOriginationDoubleDeloopingTypeADimensionFourFamilyRLPV1_104.lean"
CANDIDATE = ROOT / "research/codeai/v1104/r1/DependentOriginationDoubleDeloopingTypeADimensionFourFamilyRLPV1_104.lean"
V103 = ROOT / "formal/KUOS/DependentOriginationDoubleDeloopingTypeAHighDimensionalFillersV1_103.lean"
V102 = ROOT / "formal/KUOS/DependentOriginationDoubleDeloopingTypeALowDimensionalFillersV1_102.lean"
OUT = Path("/tmp/kuuos-v1104-codeai-r1b")
NAMESPACE = "KUOS.DependentOriginationDoubleDeloopingTypeADimensionFourFamilyRLPV1_104"
EXPECTED = {
    ORIGINAL: "dc75c6d91c317bc8d350c7c45d4268dce38bf06c",
    CANDIDATE: "7f0b83da16509faf83ab132107ea4091b55fe99d",
    V103: "dbec61c9798481709f2deda0028e84b7515f209e",
    V102: "f8b492b210e5525990aa587fa2eb5c8648a5ff19",
}

def main() -> int:
    if os.environ.get("GITHUB_ACTIONS") != "true" or os.environ.get("GITHUB_REF_NAME") != BRANCH:
        raise cycle.Hold("WRONG_WORLD_OR_RUNTIME")
    for path, expected in EXPECTED.items():
        if path.is_symlink() or not path.is_file() or cycle.git_blob(path.read_bytes()) != expected:
            raise cycle.Hold("SOURCE_BLOB_MISMATCH: " + str(path))
    pins = cycle.require_pins(ROOT)
    origin, candidate = ORIGINAL.read_text(), CANDIDATE.read_text()
    before, after = cycle.declarations(origin), cycle.declarations(candidate)
    if len(before) != 21 or list(before) != list(after) or list(after)[-1] != "natDoubleDelooping_standardTypeA_rlp":
        raise cycle.Hold("21_DECLARATION_NAME_ORDER_OBSTRUCTION")
    changes = {name: "Only the proof-term witness by decide -> by omega; proposition unchanged"
        for name in before if before[name] != after[name]}
    for name in changes:
        old, new = before[name], after[name]
        allowed = old.replace("(by decide)", "(by omega)")
        if name == "natTypeAHornLabel_tetrahedron_of_hornSimplex":
            allowed = allowed.replace("(Λ[g.n, g.i] : SSet)", "(Λ[g.n, g.i] : SSet.{0})")
            changes[name] = "Make horn carrier universe Type0 explicit for certified target map; other changes are proof-term witnesses only"
        if name == "natTypeAFourCocycle_distinguished_zero":
            expected_old = "(natTypeAFourCocycle i h0 h4 f).TypeADistinguishedZero i"
            expected_new = ("KUOS.DependentOriginationDoubleDeloopingTypeACocycleLiftingV1_101."
                "NatNormalizedDuskinCocycle.TypeADistinguishedZero "
                "(natTypeAFourCocycle i h0 h4 f) i")
            allowed = allowed.replace(expected_old, expected_new)
            changes[name] = ("Replace an invalid projected field with the explicitly qualified "
                "v1.101 TypeADistinguishedZero predicate; tracked statement repair, not a proof assumption")
        if allowed != new:
            raise cycle.Hold("SIGNATURE_OBSTRUCTION: " + name)
    contract = cycle.source_contract(origin, candidate, changes, {})
    if cycle.imports(candidate) != ["KUOS.DependentOriginationDoubleDeloopingTypeAHighDimensionalFillersV1_103"]:
        raise cycle.Hold("IMPORT_OBSTRUCTION")
    if OUT.exists():
        raise cycle.Hold("APPEND_ONLY_OBSTRUCTION")
    OUT.mkdir(parents=True)
    rec = {
        "schema": "kuuos-v1104-codeai-r1b-local-direct-v2",
        "status": "LOCAL_NOT_CERTIFIED",
        "source_sha": os.environ.get("GITHUB_SHA"),
        "original_blob": EXPECTED[ORIGINAL],
        "candidate_blob": EXPECTED[CANDIDATE],
        "v103_blob": EXPECTED[V103],
        "v102_blob": EXPECTED[V102],
        "pins": pins,
        "contract": contract,
        "independent_ci_started": False,
        "PR_3555_mutated": False,
        "merge_authorized": False,
    }
    direct = cycle.run_lean(ROOT, CANDIDATE, OUT / "direct", seconds=900)
    rec["direct_lean"] = direct
    if not direct["direct_success"]:
        rec["status"] = "DIRECT_RED_UNCERTIFIED" if not direct["timed_out"] else "NO_DATA_TIMEOUT"
    else:
        audit = OUT / "axioms.lean"
        audit.write_text(candidate + "\n" + "\n".join("#print axioms " + NAMESPACE + "." + x for x in before) + "\n")
        audit_result = cycle.run_lean(ROOT, audit, OUT / "axiom_audit", seconds=900)
        rec["axiom_direct"] = audit_result
        if audit_result["direct_success"]:
            try:
                rec["axioms"] = cycle.audit_axioms(
                    (OUT / "axiom_audit" / "stdout.log").read_text(), list(before), NAMESPACE)
                rec["status"] = "LOCAL_DIRECT_GREEN_AXIOM_21_OF_21"
            except cycle.Hold as exc:
                rec["status"] = "AXIOM_OBSTRUCTION"
                rec["axiom_obstruction"] = str(exc)
        else:
            rec["status"] = "AXIOM_AUDIT_RED"
    (OUT / "receipt.json").write_text(json.dumps(rec, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
    print("KUUOS_V1104_CODEAI_R1B_SANDBOX_RECEIPT", json.dumps({
        "status":rec["status"],"direct":direct,"axioms":rec.get("axioms"),
        "independent_ci_started":False,"PR_3555_mutated":False},sort_keys=True))
    for path, sha in EXPECTED.items():
        if cycle.git_blob(path.read_bytes()) != sha:
            raise cycle.Hold("SOURCE_MUTATION_OBSTRUCTION")
    return 0 if rec["status"] == "LOCAL_DIRECT_GREEN_AXIOM_21_OF_21" else 1

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / "obstruction.txt").write_text(type(exc).__name__ + ": " + str(exc) + "\n")
        print("KUUOS_V1104_R1B_HOLD", type(exc).__name__, str(exc))
        raise SystemExit(2)
