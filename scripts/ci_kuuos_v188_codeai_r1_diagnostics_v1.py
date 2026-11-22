#!/usr/bin/env python3
"""KuuOS CodeAI v1.88 direct kernel trial; record all elaboration errors, never adopt.

R1 candidate is exactly the v1.88 original source with:
- correctly scoped native scaled-simplicial definitions;
- literal Unicode Delta simplex notation used by the pinned mathlib.
No proof declaration or shape is silently weakened. A diagnostic is not a proof.
"""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from scripts.ci_kuuos_v176_exact_source_audit_v1 import blob, verify_inputs
ROOT=Path(__file__).resolve().parents[1]
TARGET=ROOT/"formal/KUOS/DependentOriginationCanonicalAttachmentScalingObstructionRetractV1_88.lean"
FROZEN=ROOT/"legacy/v5.291/formal/KUOS/DependentOriginationCanonicalAttachmentScalingObstructionRetractV1_88.lean"
MODULE="KUOS.DependentOriginationCanonicalAttachmentScalingObstructionRetractV1_88"
SOURCE_BLOB="e555c9eae00f348ef6b5fb7ed4827f0d8ec99a53"
BASE_BLOB="ba6190c2b2f9dac0febfb6357e908e81601c79a1"
def main():
    verify_inputs()
    original=FROZEN.read_bytes().decode()
    raw=TARGET.read_bytes()
    assert blob(FROZEN.read_bytes())==BASE_BLOB
    assert blob(raw)==SOURCE_BLOB
    assert original.count("Delta[")==15
    assert original.count("open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22")==1
    expected=original.replace("open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22",
        "open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19\nopen KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22"
    ).replace("Delta[","Δ[")
    assert raw.decode()==expected, "V188 unreviewed code modification"
    assert not re.search(r"(?m)^\s*(sorry|admit|axiom|unsafe)\b", raw.decode())
    head=os.environ.get("SOURCE_HEAD","")
    assert re.fullmatch(r"[0-9a-f]{40}",head)
    cmd=["lake","-KleanArgs=-DwarningAsError=true","-KleanArgs=-DsorryAsError=true","build",MODULE]
    run=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,errors="replace",timeout=3600)
    out=Path("/tmp/kuuos-v188-codeai-r1");out.mkdir(parents=True,exist_ok=True)
    (out/"strict-build.log").write_text(run.stdout)
    failures=[l for l in run.stdout.splitlines() if l.startswith("error: ")]
    classified=[]
    for line in failures:
        kind=("UNKNOWN_IDENTIFIER" if "Unknown identifier" in line else
              "UNIVERSE_OR_TYPE_ERROR" if "type mismatch" in line.lower() else
              "ELABORATION_DIAGNOSTIC")
        classified.append({"kind":kind,"diagnostic":line[:600]})
    receipt={"head":head,"source_blob":SOURCE_BLOB,"original_blob":BASE_BLOB,
      "source_sha256":hashlib.sha256(raw).hexdigest(),"lean":"v4.30.0-rc2",
      "mathlib":"5450b53e5ddc75d46418fabb605edbf36bd0beb6",
      "build_exit":run.returncode,"direct_diagnostics":len(failures),
      "typed_feedback":classified,"source_adopted":False,"merge_authorized":False}
    (out/"receipt.json").write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+"\n")
    print("V188_CODEAI_R1_RECEIPT "+json.dumps({k:v for k,v in receipt.items() if k!="typed_feedback"},ensure_ascii=False))
    print("V188_CODEAI_R1_DIAGNOSTICS_START")
    for line in failures[:70]:print(line)
    print("V188_CODEAI_R1_DIAGNOSTICS_END")
    return 0 if run.returncode==0 and len(failures)==0 else 2
if __name__=="__main__":
    sys.exit(main())
