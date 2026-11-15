#!/usr/bin/env python3
"""Source-bound, read-only Lean kernel probe for v1.96 Hom/universe mismatch.

Run with `lake env lean` only after v1.95 .olean exists. Every test is a
standalone temporary file and retains full stderr/stdout, including failures.
NO theorem-file edits, hidden axioms, sorry or Git writes.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

from scripts.check_kuuos_lean_mcp_fullsource_v1 import git_blob, sha256

ROOT = Path(__file__).resolve().parents[1]
REPO = "itakura-hidetoshi/KuuOS"
TARGET = "formal/KUOS/DependentOriginationDoubleDeloopingThinComparisonZeroV1_96.lean"
SOURCE_BLOB = "0c2c9f3599692613ea0c81d61b73e2a2b8d2d102"
PROMOTED_SOURCE_BLOB = "c931af7699061a67e73f52e12d4a233f98cb1a5c"
PREFIX = """import KUOS.DependentOriginationDoubleDeloopingNatNonthinDuskinWitnessV1_95
open CategoryTheory
open CategoryTheory.Category
open KUOS.DependentOriginationDoubleDeloopingNatNonthinDuskinWitnessV1_95
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
set_option pp.universes true
"""

TESTS = {
    "onecell_plain": """
example (f g : NatOneCell) : (f ⟶ g) = Nat := rfl
example (f g : NatOneCell) : (Quiver.Hom.{0} f g) = Nat := rfl
example (f g : NatOneCell) : OfNat (f ⟶ g) 0 := inferInstance
example (f g : NatOneCell) : OfNat (Quiver.Hom.{0} f g) 0 := inferInstance
example (f g : NatOneCell) (alpha : f ⟶ g) : alpha = alpha := rfl
""",
    "onecell_in_namespace": """
namespace KUOS.DependentOriginationDoubleDeloopingThinComparisonZeroV1_96
namespace NatDoubleDelooping
example (f g : NatOneCell) : (f ⟶ g) = Nat := rfl
example (f g : NatOneCell) : OfNat (f ⟶ g) 0 := inferInstance
example (f g : NatOneCell) (alpha : f ⟶ g) : alpha = (alpha : Quiver.Hom.{0} f g) := rfl
end NatDoubleDelooping
end KUOS.DependentOriginationDoubleDeloopingThinComparisonZeroV1_96
""",
    "sigma_plain": """
namespace KUOS.DependentOriginationDoubleDeloopingThinComparisonZeroV1_96
example {n : Nat} (sigma : DuskinSimplex NatDoubleDelooping n)
    {a b : DuskinOrdinal n} (f : a ⟶ b) :
    (sigma.map f ⟶ sigma.map f) = Nat := rfl
example {n : Nat} (sigma : DuskinSimplex NatDoubleDelooping n)
    {a b : DuskinOrdinal n} (f : a ⟶ b) :
    OfNat (sigma.map f ⟶ sigma.map f) 0 := inferInstance
end KUOS.DependentOriginationDoubleDeloopingThinComparisonZeroV1_96
""",
    "sigma_explicit": """
namespace KUOS.DependentOriginationDoubleDeloopingThinComparisonZeroV1_96
example {n : Nat} (sigma : DuskinSimplex NatDoubleDelooping n)
    {a b : DuskinOrdinal n} (f : a ⟶ b) :
    (Quiver.Hom.{0} (sigma.map f) (sigma.map f)) = Nat := rfl
example {n : Nat} (sigma : DuskinSimplex NatDoubleDelooping n)
    {a b : DuskinOrdinal n} (f : a ⟶ b) :
    OfNat (Quiver.Hom.{0} (sigma.map f) (sigma.map f)) 0 := inferInstance
example {n : Nat} (sigma : DuskinSimplex NatDoubleDelooping n)
    {a b : DuskinOrdinal n} (f : a ⟶ b) :
    ((sigma.map f ⟶ sigma.map f) =
      (Quiver.Hom.{0} (sigma.map f) (sigma.map f))) := rfl
end KUOS.DependentOriginationDoubleDeloopingThinComparisonZeroV1_96
""",
}

def main() -> int:
    if os.environ.get("GITHUB_EVENT_NAME") != "pull_request":
        raise RuntimeError("run only for exact PR")
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8"))
    if event.get("number") != 3522 or event.get("repository",{}).get("full_name") != REPO:
        raise RuntimeError("wrong target PR")
    head = event["pull_request"]["head"]["sha"]
    source = (ROOT/TARGET).read_bytes()
    current_blob = git_blob(source)
    if current_blob not in (SOURCE_BLOB, PROMOTED_SOURCE_BLOB):
        raise RuntimeError("source blob drift")
    out = Path("/tmp/kuuos-v196-hom-universe-probes")
    out.mkdir(parents=True,exist_ok=False)
    receipt = {
        "schema": "kuuos-v196-source-bound-hom-probe-v1",
        "source_head": head,
        "source_git_blob": current_blob,
        "source_sha256": sha256(source),
        "source_restored": None,
        "git_mutated": False,
        "independent_ci_certified": False,
        "results": [],
    }
    for name,tail in TESTS.items():
        with tempfile.TemporaryDirectory(prefix="kuuos-hom-lean-") as tmp:
            path = Path(tmp)/"Probe.lean"
            path.write_text(PREFIX+tail,encoding="utf-8")
            result = subprocess.run(
                ["lake","env","lean","-DwarningAsError=true",
                 "-Dweak.sorryAsError=true",str(path)],
                cwd=ROOT, text=True, capture_output=True, timeout=150,check=False)
            log=result.stdout+"\n"+result.stderr
            (out/(name+".log")).write_text(log,encoding="utf-8")
            errors=[z for z in log.splitlines() if "error:" in z or "error(" in z]
            record = {"probe":name,"exit_code":result.returncode,
                "status":"SUCCESS" if result.returncode==0 else "FAILURE",
                "log_sha256":sha256(log.encode("utf-8")),
                "error_count":len(errors),"error_headers":errors[:15]}
            receipt["results"].append(record)
            print("KUUOS_V196_HOM_UNIVERSE_KERNEL_PROBE "+json.dumps(record,sort_keys=True))
    receipt["source_restored"]=(ROOT/TARGET).read_bytes()==source
    (out/"receipt.json").write_text(
        json.dumps(receipt,indent=2,ensure_ascii=False,sort_keys=True)+"\n",encoding="utf-8")
    print("KUUOS_V196_HOM_UNIVERSE_PROBE_SUMMARY "+
          json.dumps({"head":head,"source_restored":receipt["source_restored"],
                      "probes":len(receipt["results"]),
                      "green":sum(x["status"]=="SUCCESS" for x in receipt["results"])},sort_keys=True))
    return 0 if receipt["source_restored"] else 2

if __name__=="__main__":
    raise SystemExit(main())
