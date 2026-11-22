#!/usr/bin/env python3
"""Version-sealed F112 elaboration probe: precompile a generic 14-cell critical helper.

All files generated in the disposable CI checkout have distinct diagnostic
names; the original Lean file, its signature, and public imports are untouched.
The helper is exactly the same raw pasting term, not an axiom or admission.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from scripts import codeai_v061_f112_strict_olean_split_probe as previous

ROOT=Path(__file__).resolve().parents[1]
SOURCE=previous.SOURCE
BLOB=previous.EXPECTED_BLOB
MATHLIB=previous.MATHLIB
CORE="CodeAIV061F112CriticalHelperCoreProbe"
TAIL="CodeAIV061F112CriticalHelperTailProbe"
LEFT="""def nativeK5PentagonatorFifteenLeftFirst :=
  nativeK5FourteenPastingLeftThenRight
    (nativeK5PentagonatorFifteenExchangeFourteen t1 t2 t3 t4 t5)"""

HELPER=r"""
section CodeAIDiagnosticOriginalCriticalHelper
variable {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
variable {f g : NativeF55StructuralComparison p r s}
variable {alpha beta : NativeK5StructuralFourCell p f g}
variable {w z : NativeK5StructuralFiveCell p alpha beta}
variable {u v : NativeK5StructuralSixCell p w z}
variable {h k : NativeK5StructuralSevenCell p u v}
variable {e d : NativeK5StructuralEightCell p h k}
variable {q t : NativeK5StructuralNineCell p e d}
variable {P Q : NativeK5StructuralTenCell p q t}
variable {H K : NativeK5StructuralElevenCell p P Q}
variable {U V : NativeK5StructuralTwelveCell p H K}

/-- Identical raw left-first 14-cell term specialized at a generic 13-cell.
This is a diagnostic helper, not a replacement of any canonical declaration. -/
def codeaiF112CriticalLeftGeneric
    (W : NativeK5StructuralThirteenCell p U V) :
    NativeK5StructuralFourteenCell p
      (.trans (nativeK5ThirteenPastingLeftThenRight W)
        (.symm (nativeK5ThirteenPastingLeftThenRight W)))
      (.trans (nativeK5ThirteenPastingRightThenLeft W)
        (.symm (nativeK5ThirteenPastingRightThenLeft W))) :=
  nativeK5FourteenPastingLeftThenRight
    (NativeK5StructuralFourteenCell.squareExchange W)

end CodeAIDiagnosticOriginalCriticalHelper
"""

REPLACEMENTS={
    "generic-helper": """def nativeK5PentagonatorFifteenLeftFirst :=
  codeaiF112CriticalLeftGeneric
    (nativeK5PentagonatorFourteenExchangeThirteen t1 t2 t3 t4 t5)""",
    "named-argument": """def nativeK5PentagonatorFifteenLeftFirst :=
  let W := nativeK5PentagonatorFourteenExchangeThirteen t1 t2 t3 t4 t5
  nativeK5FourteenPastingLeftThenRight
    (NativeK5StructuralFourteenCell.squareExchange W)""",
}

def sha(v: str)->str:
    return hashlib.sha256(v.encode()).hexdigest()

def prepare(variant: str)->dict:
    data=SOURCE.read_bytes()
    assert previous.blob(data)==BLOB, "original source blob changed"
    assert previous.blob((ROOT/"formal/KuuOSFormal.lean").read_bytes())==previous.ROOT_BLOB
    assert previous.blob((ROOT/"formal/KUOS/Architecture/LeanPythonTwoStagePrivateAppendModelCandidateAV0_61.lean").read_bytes())==previous.CANDIDATE_BLOB
    assert (ROOT/"lean-toolchain").read_text().strip()=="leanprover/lean4:v4.30.0-rc2"
    deps=json.loads((ROOT/"lake-manifest.json").read_text())["packages"]
    assert [p["rev"] for p in deps if p["name"]=="mathlib"]==[MATHLIB]
    src=data.decode()
    assert src.endswith("\n") and len(src.splitlines())==352 and src.count(LEFT)==1
    marker="section GenuineFiveStage\n"
    assert src.count(marker)==1
    prefix,following=src.split(marker)
    stage_end="def nativeK5PentagonatorFifteenRightFirst :="
    assert following.count(stage_end)==1
    stage=following.split(stage_end,1)[0]
    assert stage.count(LEFT)==1
    original_staged=marker+stage
    original_core=prefix+"\nend\nend Kuu.F112.Physical\n"
    core=prefix+(HELPER if variant=="generic-helper" else "")+"\nend\nend Kuu.F112.Physical\n"
    # Preserve header and entire five-stage context, replacing only a named
    # diagnostic expression. No theorem statement, assumptions, or imports
    # of the authoritative original are edited.
    namespace_header="namespace Kuu.F112.Physical\n"+src.split(
        "namespace Kuu.F112.Physical\n",1)[1].split(
        "abbrev NativeK5FourteenHistoryWord",1)[0]
    tail=(
        f"import Kuu.F112.{CORE}\n"+
        namespace_header+
        original_staged.replace(LEFT, REPLACEMENTS[variant])+
        "\nend GenuineFiveStage\n\nend\nend Kuu.F112.Physical\n"
    )
    assert core.count("end GenuineFourteenPasting")==1
    assert original_core in src or original_core.startswith(prefix)
    assert "sorry" not in core and "admit" not in core and "sorry" not in tail and "admit" not in tail
    where=ROOT/"formal/Kuu/F112"
    a,b=where/(CORE+".lean"),where/(TAIL+".lean")
    assert not a.exists() and not b.exists(),"no overwrite even in ephemeral checkout"
    a.write_text(core)
    b.write_text(tail)
    out=ROOT/"artifacts/codeai-v061-f112-critical-helper"/variant
    out.mkdir(parents=True,exist_ok=True)
    receipt={
        "schema":"codeai.v061.f112.critical_generic_helper.v1",
        "variant":variant,"source_blob":BLOB,
        "original_source_sha256":sha(src),
        "diagnostic_core_sha256":sha(core),
        "diagnostic_tail_sha256":sha(tail),
        "core_path":str(a.relative_to(ROOT)),
        "tail_path":str(b.relative_to(ROOT)),
        "original_five_stage_left_sha256":sha(LEFT),
        "original_source_unmodified":True,
        "original_14_cell_pasting_unmodified":True,
        "mathematical_statement_unchanged":True,
        "diagnostic_only":True,"admitted":False,
        "lean":"v4.30.0-rc2","mathlib":MATHLIB,
        "strict_lean":"TEST_REQUIRED","public_root":"HOLD",
        "verified_useful_memory":"HOLD","merge_authority":False,
    }
    (out/"manifest.json").write_text(json.dumps(receipt,sort_keys=True,indent=2)+"\n")
    return receipt

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--variant",choices=sorted(REPLACEMENTS),required=True)
    a=p.parse_args()
    print("CODEAI_F112_PREPARED",json.dumps(prepare(a.variant),sort_keys=True))
