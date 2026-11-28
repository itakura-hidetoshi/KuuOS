#!/usr/bin/env python3
"""Exact-source core Lean probe, actual MCP audit, and independent direct replay."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import check_kuuos_lean_lsp_mcp_compatibility_v7_17 as mcp

SOURCE = ROOT / "scripts/lean_probes/verifyos_method_sound_coverage_v0_14.lean"
BLOB = "b11ce505cb5f0d13fc812474299e5b0b96a50b87"
BASE = "5c282fd5a34573f326d74a2b6e933fc616f09f96"
NS = "KUOS.VerifyOS.MethodSoundCoverageV0_14."
PIN = "leanprover/lean4:v4.30.0-rc2"
MATHLIB = "5450b53e5ddc75d46418fabb605edbf36bd0beb6"
AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
DECLARATIONS = (
    "Supported", "Honors", "Forced", "Covers", "Agrees", "Functional",
    "support_sound", "support_honors", "forced_iff_supported",
    "missing_support_has_two_models", "agreement_and_cover_give_support",
    "full_answer_forced_iff_cover", "conflicting_support_no_functional_model",
    "unavailable_reports_no_support", "support_mono_admission",
    "honors_restrict_scope", "commonErrorReports",
    "distinct_methods_can_agree_wrong", "exampleScope", "exampleTruth",
    "scoped_soundness_does_not_transport",
)
THEOREMS = (
    "support_sound", "support_honors", "forced_iff_supported",
    "missing_support_has_two_models", "agreement_and_cover_give_support",
    "full_answer_forced_iff_cover", "conflicting_support_no_functional_model",
    "unavailable_reports_no_support", "support_mono_admission",
    "honors_restrict_scope", "distinct_methods_can_agree_wrong",
    "scoped_soundness_does_not_transport",
)


def need(condition, reason):
    if not condition:
        raise RuntimeError(reason)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\x00" + raw).hexdigest()


def canonical(obj):
    return (json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":")) + "\n").encode()


def save(path, obj):
    path.write_bytes(canonical(obj))


def load(path):
    return json.loads(path.read_bytes())


def exact_source():
    raw = SOURCE.read_bytes()
    need(blob(raw) == BLOB, "SOURCE_BLOB_MISMATCH")
    text = raw.decode("utf-8")
    need(re.findall(r"(?m)^(?:def|theorem) (\w+)", text) == list(DECLARATIONS), "DECLARATION_INVENTORY")
    need(re.findall(r"(?m)^theorem (\w+)", text) == list(THEOREMS), "THEOREM_INVENTORY")
    need(re.findall(r"(?m)^#print axioms (\w+)$", text) == list(DECLARATIONS), "AXIOM_INVENTORY")
    need(not re.search(r"\b(?:sorry|admit|axiom|unsafe|native_decide)\b", "\n".join(
        line for line in text.splitlines() if not line.startswith("#print axioms")
    )), "FORBIDDEN_PROOF_TOKEN")
    need((ROOT/"lean-toolchain").read_text().strip() == PIN, "TOOLCHAIN_PIN")
    need([x["rev"] for x in load(ROOT/"lake-manifest.json")["packages"] if x["name"]=="mathlib"] == [MATHLIB], "MATHLIB_PIN")
    return raw


def normalize(values):
    need(isinstance(values, list) and all(isinstance(x, str) for x in values), "AXIOM_VALUE_TYPE")
    # Only the known display aliases, not arbitrary names/universe suffixes.
    aliases = {"Classical.choice.{u}":"Classical.choice", "Quot.sound.{u}":"Quot.sound"}
    out = [aliases.get(x, x) for x in values]
    need(len(set(out)) == len(out) and set(out) <= AXIOMS, "AXIOM_NOT_ALLOWED:" + repr(values))
    return sorted(out)


def direct(out):
    raw = exact_source()
    out.mkdir(parents=True, exist_ok=False)
    project = out / "project"
    project.mkdir()
    (project/"lean-toolchain").write_text(PIN+"\n")
    (project/"lakefile.toml").write_text('name = "VerifyOSProbe"\nversion = "0.1.0"\ndefaultTargets = ["MethodSoundCoverage"]\n[[lean_lib]]\nname = "MethodSoundCoverage"\n')
    source = project/"MethodSoundCoverage.lean"
    source.write_bytes(raw)
    version = subprocess.run(["lean", "--version"], check=True, capture_output=True, text=True).stdout.strip()
    need("version 4.30.0-rc2" in version, "ACTUAL_LEAN_VERSION")
    start = time.monotonic()
    proc = subprocess.run(["lean", "-DwarningAsError=true", "-Dweak.sorryAsError=true", "-o",
                           str(project/"MethodSoundCoverage.olean"), str(source)],
                          cwd=project, capture_output=True, text=True, timeout=120, check=False)
    elapsed = time.monotonic()-start
    log = proc.stdout + "\n" + proc.stderr
    (out/"lean.log").write_text(log)
    print(log, flush=True)
    print("VERIFYOS_DIRECT_EXIT", proc.returncode, "seconds", elapsed, flush=True)
    need(proc.returncode==0 and (project/"MethodSoundCoverage.olean").is_file(), "DIRECT_LEAN_FAILED")
    need(not re.search(r"\b(?:warning:|error:|sorryAx)\b", log), "DIRECT_DIAGNOSTIC")
    pattern = r"'("+re.escape(NS)+r"\w+)' (?:does not depend on any axioms|depends on axioms: \[([^\]]*)\])"
    reports = re.findall(pattern, log)
    need(len(reports)==len(DECLARATIONS) and {x[0] for x in reports}=={NS+x for x in DECLARATIONS}, "DIRECT_AXIOM_INVENTORY")
    audits = {name:normalize([x.strip() for x in values.split(",") if x.strip()]) for name,values in reports}
    need(source.read_bytes()==raw and exact_source()==raw, "SOURCE_DRIFT")
    receipt = {"schema":"kuuos.verifyos.method-sound-coverage.v0.14.direct",
        "canonical_parent":BASE, "checkout_sha":os.environ.get("GITHUB_SHA"),
        "source_blob":BLOB, "source_sha256":sha(raw), "lean_version":version,
        "lean_pin":PIN,"mathlib_manifest_pin":MATHLIB,"mathlib_imported":False,
        "exit_code":proc.returncode,"axioms":audits,"declaration_count":len(audits),
        "theorem_count":len(THEOREMS),"proof_authority":False,"runtime_bridge_proved":False}
    save(out/"direct.json",receipt)
    print("VERIFYOS_V014_DIRECT",json.dumps(receipt,sort_keys=True),flush=True)
    return receipt


def structured(response):
    value = response["result"]
    need(value.get("isError") is False, "MCP_ERROR")
    obj = value.get("structuredContent")
    if not isinstance(obj,dict):
        obj = json.loads(mcp.extract_text(response))
    need(isinstance(obj,dict), "MCP_STRUCTURED_RESULT")
    return obj


def mcp_audit(out):
    prior = load(out/"direct.json")
    raw = exact_source()
    project = out/"project"
    source = project/"MethodSoundCoverage.lean"
    need(prior["source_blob"]==BLOB and prior["source_sha256"]==sha(raw)
         and source.read_bytes()==raw and prior["exit_code"]==0, "MCP_SOURCE_BINDING")
    cmd = ["uvx","--from","lean-lsp-mcp=="+mcp.EXPECTED_SERVER_VERSION,
           "lean-lsp-mcp","--transport","stdio"]
    version = mcp.server_version(cmd[:-2],project)
    client = mcp.MCPClient(cmd,cwd=project,env={"LEAN_PROJECT_PATH":str(project),
        "LEAN_LOG_LEVEL":"NONE","LEAN_MCP_DISABLED_TOOLS":mcp.DISABLED_DURING_PROBE,
        "LEAN_MCP_SCRATCH_SLOTS":"1"},timeout_seconds=240)
    rows = {}
    try:
        client.request("initialize",{"protocolVersion":mcp.PROTOCOL_VERSION,
            "capabilities":{},"clientInfo":{"name":"VerifyOS method sound coverage","version":"0.14"}})
        client.notify("notifications/initialized")
        need({"lean_diagnostic_messages","lean_verify"} <= set(mcp.tool_map(client.request("tools/list"))),"MCP_TOOLS")
        diag_raw = mcp.call_tool(client,"lean_diagnostic_messages",{"file_path":source.name,"timeout_s":180})
        save(out/"mcp-diagnostics.json",diag_raw)
        diag = structured(diag_raw)
        need(diag.get("success") is True and diag.get("partial") is False and diag.get("timed_out") is False
             and diag.get("failed_dependencies")==[] and isinstance(diag.get("items"),list)
             and not any(x.get("severity") in ("warning","error") for x in diag["items"]), "MCP_DIAGNOSTIC_FAILURE")
        for j,name in enumerate(THEOREMS):
            full=NS+name
            reply=mcp.call_tool(client,"lean_verify",{"file_path":source.name,"theorem_name":full,"scan_source":False})
            save(out/f"mcp-verify-{j}.json",reply)
            value=structured(reply)
            axioms=normalize(value.get("axioms"))
            need(value.get("warnings")==[] and axioms==prior["axioms"][full], "MCP_AXIOM_MISMATCH:"+full)
            rows[full]=axioms
            print("VERIFYOS_V014_MCP_AUDIT",full,json.dumps(axioms),flush=True)
    finally:
        client.close()
    need(source.read_bytes()==raw and exact_source()==raw, "MCP_SOURCE_DRIFT")
    receipt={"schema":"kuuos.verifyos.method-sound-coverage.v0.14.mcp",
        "direct_sha256":sha(canonical(prior)),"source_blob":BLOB,
        "source_sha256":sha(raw),"mcp_version":version,"theorems":rows,"status":"REAL_LEAN_MCP_CHECKED"}
    save(out/"mcp.json",receipt)
    print("VERIFYOS_V014_MCP",json.dumps(receipt,sort_keys=True),flush=True)


def independent(out, first):
    actual=direct(out)
    original=load(first/"direct.json")
    need(actual==original, "INDEPENDENT_DIRECT_RECEIPT_MISMATCH")
    need((first/"project/MethodSoundCoverage.lean").read_bytes()==exact_source(), "INDEPENDENT_SOURCE_MISMATCH")
    mp=load(first/"mcp.json")
    need(mp["status"]=="REAL_LEAN_MCP_CHECKED" and mp["source_blob"]==BLOB
         and mp["source_sha256"]==actual["source_sha256"] and mp["direct_sha256"]==sha(canonical(original))
         and mp["theorems"]=={NS+n:actual["axioms"][NS+n] for n in THEOREMS}, "INDEPENDENT_MCP_RECEIPT_MISMATCH")
    diag=structured(load(first/"mcp-diagnostics.json"))
    need(diag["success"] is True and diag["partial"] is False and diag["timed_out"] is False
         and diag["failed_dependencies"]==[] and not any(x.get("severity") in ("warning","error") for x in diag["items"]), "INDEPENDENT_MCP_DIAGNOSTICS")
    for j,name in enumerate(THEOREMS):
        row=structured(load(first/f"mcp-verify-{j}.json"))
        need(row["warnings"]==[] and normalize(row["axioms"])==actual["axioms"][NS+name], "INDEPENDENT_MCP_ROW")
    receipt={"status":"INDEPENDENT_DIRECT_AND_MCP_EVIDENCE_MATCHED",
        "direct_sha256":sha(canonical(actual)),"mcp_sha256":sha(canonical(mp)),
        "source_blob":BLOB,"source_sha256":actual["source_sha256"],
        "declarations":len(DECLARATIONS),"theorems":len(THEOREMS),"mcp_theorems":len(mp["theorems"]),
        "proof_authority":False,"runtime_bridge_proved":False}
    save(out/"independent.json",receipt)
    print("VERIFYOS_V014_INDEPENDENT",json.dumps(receipt,sort_keys=True),flush=True)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--phase",choices=("direct","mcp","independent"),required=True)
    ap.add_argument("--out",type=Path,required=True)
    ap.add_argument("--first",type=Path)
    args=ap.parse_args()
    if args.phase=="direct": direct(args.out)
    elif args.phase=="mcp": mcp_audit(args.out)
    else:
        need(args.first is not None,"SANDBOX_RECEIPT_REQUIRED")
        independent(args.out,args.first)


if __name__=="__main__":
    main()
