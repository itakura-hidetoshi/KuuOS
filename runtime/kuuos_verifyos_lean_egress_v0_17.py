"""Trusted-host egress: recheck signed evidence, actually run pinned Lean, compare values.
No model-supplied commands, admission flags, precomputed Lean output or prose.
"""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
import re
import subprocess
import tempfile
from runtime import kuuos_verifyos_diverse_ledger_audit_v0_13 as d
from runtime import kuuos_verifyos_claim_evidence_binding_v0_3 as c
from runtime import kuuos_verifyos_question_claim_contract_v0_4 as q
from runtime import kuuos_verifyos_execution_witness_v0_12 as w

b,p = c.b,c.p
SCHEMA = "kuuos.verifyos.lean-egress.v0.17"
MATCH = "LEAN_EXECUTED_EGRESS_MATCHED_ONLY"
BOUNDARY = {**w.BOUNDARY,**d.BOUNDARY,
    "complete_python_refinement_proved":False,"lean_toolchain_authenticity_proved":False,
    "historical_execution_attested":False,"publication_interception_verified":False}
ERRORS = (*w.ERRORS,subprocess.SubprocessError,OSError)
ROOT = Path(__file__).resolve().parents[1]
SOURCES = (
    ("MethodSoundCoverage","verifyos_method_sound_coverage_v0_14.lean","177867145b946edbc8851a8176571f0311c82ac4bf842d9812ddcae80a5eb9f5"),
    ("TypedProjection","verifyos_typed_projection_v0_15.lean","b0577bdc0a74e1108c60b445c7ed8fba4886a491630e06347e3465aec6ecc50c"),
    ("JsonProjection","verifyos_json_projection_v0_16.lean","c147594382ed7c2f309eaa594cdbfd7a03045134ab1b24d0491a6dbc10713cbe"),
    ("ProjectionCLI","verifyos_json_projection_cli_v0_16.lean","65c76b22d9e1d07d76003c53cf4413a61f8fa6f9a30c2035c6755b80a52033c0"),
)
PIN = "Lean (version 4.30.0-rc2, x86_64-unknown-linux-gnu, commit 3dc1a088b6d2d8eafe25a7cd7ec7b58d731bd7cc, Release)"
ORDER = tuple(q.ORDER)
MAX_INPUT = 262144


def hold(reason):
    return b.canonical({"schema":SCHEMA,"status":"HOLD","reason":reason,**BOUNDARY})


def exact_sources(root):
    out={}
    for module,name,digest in SOURCES:
        path=root/"scripts"/"lean_probes"/name
        b.require(path.is_file() and not path.is_symlink() and b.hex64(digest),"LEAN_SOURCE_PATH")
        raw=path.read_bytes()
        b.require(b.sha(raw)==digest,"LEAN_SOURCE_MISMATCH:"+module)
        out[module]=raw
    return out


def executable(path):
    b.require(isinstance(path,Path) and path.is_absolute() and path.is_file(),"TRUSTED_LEAN_PATH_REQUIRED")
    path=path.resolve()
    return path,b.sha(path.read_bytes())


def checked_run(argv,cwd,env):
    proc=subprocess.run(argv,cwd=cwd,env=env,stdin=subprocess.DEVNULL,
                        capture_output=True,timeout=180,check=False)
    b.require(proc.returncode==0 and not proc.stderr.strip(),"LEAN_PROCESS_FAILED")
    b.require(not re.search(rb"\b(?:warning:|error:|sorryAx)\b",proc.stdout),"LEAN_DIAGNOSTIC")
    return proc


def all_rows(raw,request,primary):
    receipt=p.strict(raw)["receipt"]
    return [{"claim_id":x,"value":r["value"] if r["status"]=="OBSERVED_IN_ADMITTED_RECEIPT" else None}
        for x in ORDER for r in [c.project(x,receipt,request,primary)]]


def run_lean(root,lean,raw,request,context,expected):
    """Only called after v0.13 actual replay. The runtime environment is trusted."""
    src=exact_sources(root)
    binary,binary_sha=executable(lean)
    b.require(type(raw) is bytes and len(raw)<=MAX_INPUT,"LEAN_INPUT_LIMIT")
    raw.decode("utf-8",errors="strict")
    req=b.sha(b.canonical(request)); binding=b.sha(b.canonical(context))
    with tempfile.TemporaryDirectory(prefix="verifyos-lean-egress-") as name:
        project=Path(name); env={**os.environ,"LEAN_PATH":str(project)}
        version=checked_run([str(binary),"--version"],project,env).stdout.decode().strip()
        b.require(version==PIN,"LEAN_VERSION_MISMATCH")
        stages=[]
        for module,source in src.items():
            path=project/(module+".lean"); path.write_bytes(source)
            proc=checked_run([str(binary),"-DwarningAsError=true","-Dweak.sorryAsError=true",
                              "-o",module+".olean",module+".lean"],project,env)
            b.require((project/(module+".olean")).is_file(),"LEAN_ARTIFACT_MISSING")
            stages.append({"module":module,"exit_code":proc.returncode,
                           "source_sha256":b.sha(source),"stdout_sha256":b.sha(proc.stdout)})
        data=project/"input.json"; data.write_bytes(raw)
        proc=checked_run([str(binary),"-DwarningAsError=true","-Dweak.sorryAsError=true",
                          "--run","ProjectionCLI.lean",str(data),req,binding,binding,request["tip"],"true"],project,env)
        lines=proc.stdout.decode("utf-8",errors="strict").splitlines()
        diagnostic=[x for x in lines if not x.startswith("{")]
        b.require(len(diagnostic)==2 and all(re.fullmatch(
            r"'(?:runCases|main)' (?:does not depend on any axioms|depends on axioms: \[[^\]]*\])",x)
            for x in diagnostic),"LEAN_OUTPUT_DIAGNOSTICS")
        outputs=[b.parse(x) for x in lines if x.startswith("{")]
        b.require(len(outputs)==1,"LEAN_OUTPUT_COUNT")
        result=outputs[0]
        b.require(set(result)=={"status","reason","claims","proof_authority","action_authority","complete_python_refinement_proved"},"LEAN_OUTPUT_SCHEMA")
        b.require(result["status"]=="TYPED_JSON_PROJECTION_ONLY" and result["reason"]=="" and
                  all(result[k] is False for k in ("proof_authority","action_authority","complete_python_refinement_proved")),"LEAN_PROJECTION_NOT_ADMITTED")
        b.require(b.canonical(result["claims"])==b.canonical(expected),"LEAN_PYTHON_VALUE_MISMATCH")
        b.require(data.read_bytes()==raw and all((project/(m+".lean")).read_bytes()==x for m,x in src.items()),"LEAN_INPUT_DRIFT")
        receipt={"lean_version":version,"lean_binary_sha256":binary_sha,"stages":stages,
                 "exit_code":proc.returncode,"stdout_sha256":b.sha(proc.stdout),
                 "input_sha256":b.sha(raw),"request_sha256":req,"context_sha256":binding,
                 "result":result}
    b.require(exact_sources(root)==src and executable(lean)==(binary,binary_sha),"LEAN_ENVIRONMENT_DRIFT")
    return receipt


def publication(snapshot,lean,**pair_inputs):
    """Recompute v0.13, execute the fixed Lean projection, then construct the packet."""
    try:
        verified=d.verify_diverse(snapshot,**pair_inputs)
        b.require(verified["status"]=="DIVERSE_FROZEN_PROFILE_AGREEMENT_ONLY","DIVERSE_EVIDENCE_NOT_ADMITTED")
        primary=verified["pair"]["primary"]
        raw=pair_inputs["primary_raw"]; request=pair_inputs["request"]; context=pair_inputs["context"]
        b.require(primary["bundle_sha256"]==b.sha(raw) and
                  primary["request_sha256"]==b.sha(b.canonical(request)) and
                  primary["context_sha256"]==b.sha(b.canonical(context)),"PRIMARY_BINDING_MISMATCH")
        expected=all_rows(raw,request,primary)
        values={x["claim_id"]:x["value"] for x in expected}
        ids=[x["claim_id"] for x in primary["claims"]]
        b.require(len(ids)==len(set(ids)) and ids and all(x in values for x in ids),"CLAIM_INVENTORY")
        for row in primary["claims"]:
            value=row["value"] if row["status"]=="OBSERVED_IN_ADMITTED_RECEIPT" else None
            b.require(b.canonical(value)==b.canonical(values[row["claim_id"]]),"SIGNED_VALUE_MISMATCH")
        execution=run_lean(ROOT,lean,raw,request,context,expected)
        # Preserve the exact v0.11/0.13 branch and claim projection. The extra
        # all-claim check is evidence, not authority to broaden the answer.
        return b.canonical({"schema":SCHEMA,"status":MATCH,"scope":"fresh_local_typed_projection_only",
            "primary_packet_sha256":b.sha(pair_inputs["primary_packet"]),
            "witness_packet_sha256":b.sha(pair_inputs["witness_packet"]),
            "diverse_result_sha256":b.sha(b.canonical(verified)),
            "anchor_tip":primary["anchor_tip"],"context_sha256":primary["context_sha256"],
            "answer_status":primary["answer_status"],"original_family_status":primary["original_family_status"],
            "claims":primary["claims"],"branches":primary["branches"],
            "selected_interpretation":None,"execution":execution,**BOUNDARY})
    except ERRORS as exc:
        return hold(str(exc) if type(exc) is ValueError else "LEAN_EGRESS_UNAVAILABLE")


def verified_display(packet,snapshot,lean,**pair_inputs):
    """Fresh execution before display. No assertion of past execution chronology."""
    expected=publication(snapshot,lean,**pair_inputs)
    if packet!=expected:
        return hold("PUBLICATION_MISMATCH"),2
    result=p.strict(expected)
    return expected,0 if result.get("status")==MATCH and result.get("answer_status")=="ACTIVE_VIEW_ALL_OBSERVED" else 2
