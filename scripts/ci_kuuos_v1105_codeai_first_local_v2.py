#!/usr/bin/env python3
"""v1.105 CodeAI: exact-source, local, sequential direct Lean trials.

Preserve all 39 public declaration names, fixed original source, imported
independently certified v1.104, mathlib pin. Stop at first full local
direct Lean+39 axioms+real lean-lsp-mcp GREEN; no independent CI on RED.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
import sys
from scripts import kuuos_sandbox_lean_cycle_v1 as cycle

ROOT = Path(__file__).resolve().parents[1]
BRANCH = "research/v1105-codeai-local-v2-20261124"
ORIGINAL = ROOT / "formal/KUOS/DependentOriginationDoubleDeloopingTypeCOuterHornCocycleCompletionV1_105.lean"
V104 = ROOT / "formal/KUOS/DependentOriginationDoubleDeloopingTypeADimensionFourFamilyRLPV1_104.lean"
V103 = ROOT / "formal/KUOS/DependentOriginationDoubleDeloopingTypeAHighDimensionalFillersV1_103.lean"
OUT = Path("/tmp/kuuos-v1105-local-v2-trials")
GREEN = Path("/tmp/kuuos-v1105-local-v2-green")
NAMESPACE = "KUOS.DependentOriginationDoubleDeloopingTypeCOuterHornCocycleCompletionV1_105"
PROBE = ROOT / "formal/KUOS/DependentOriginationDoubleDeloopingTypeCOuterHornCocycleCompletionProbeV1_105.lean"
PINS = {
    ORIGINAL: "fb4d15a3467df69b8d2ba14276c2f4da6a1670d5",
    V104: "5c911aaeb9a21baff57f6af8c8655309af47d027",
    V103: "dbec61c9798481709f2deda0028e84b7515f209e",
}
CANDIDATES = [
    ("A-revert", "0100e19fed0f3504ce0fbe153e705f0b0c04387f"),
    ("B-normnum", "a4867a2fe1c83c7f684eab12a0b0c3b25d5a5ff5")
]
STANDARD = {"propext", "Classical.choice", "Quot.sound"}

def require(test, msg):
    if not test:
        raise cycle.Hold(msg)

def check_fixed():
    require(os.environ.get("GITHUB_ACTIONS") == "true" and
            os.environ.get("GITHUB_REF_NAME") == BRANCH,
            "WRONG_RUNTIME_OR_BRANCH")
    for path,blob in PINS.items():
        require(path.exists() and path.is_file() and not path.is_symlink() and
                cycle.git_blob(path.read_bytes()) == blob,
                "SOURCE_BLOB_MISMATCH " + str(path))
    require(cycle.git_blob((ROOT / "scripts/kuuos_sandbox_lean_cycle_v1.py").read_bytes()) ==
            "5383253dbe9cda9cab90a410c2fd66ee6b9d6f41",
            "CODEAI_ENGINE_BLOB_MISMATCH")
    return cycle.require_pins(ROOT)

def normalized_signature(s):
    for before, after in [
        ("SSet.{0}", "SSet"),
        ("standardTypeCSourceCarrier.{0}", "standardTypeCSourceCarrier"),
        ("standardTypeCEdgeToHorn.{0}", "standardTypeCEdgeToHorn"),
        ("standardTypeCEdgeCollapseToPoint.{0}", "standardTypeCEdgeCollapseToPoint"),
        ("SSet.horn.face.{0}", "SSet.horn.face"),
        ("natTypeAFour_face1_val.{0}", "natTypeAFour_face1_val"),
        ("natTypeAFour_face2_val.{0}", "natTypeAFour_face2_val"),
        ("natTypeAFour_face3_val.{0}", "natTypeAFour_face3_val"),
        ("natTypeAFour_face4_val.{0}", "natTypeAFour_face4_val"),
        ("(by simp) (Fin.le_last _)", "(by omega) (by omega)"),
        ("(by decide +revert)", "(by decide)"),
        ("(by norm_num)", "(by decide)"),
    ]:
        s = s.replace(before, after)
    return s

def local_declarations(source):
    """Read all 39 source declarations, including inline-where structure fields.

    The reusable CodeAI cycle parser assumes newline-before-where for structures.
    v1.105's real structure has an inline 'where', so audit its complete fields
    as a single protected signature. This makes the contract stricter, not weaker.
    """
    stripped = cycle.without_comments_strings(source)
    found = list(cycle.DECL.finditer(stripped))
    result = {}
    for index, match in enumerate(found):
        if match.group(1) == "private":
            continue
        name, kind = match.group(3), match.group(2)
        require(name not in result, "DUPLICATE_PUBLIC_DECLARATION " + name)
        end = found[index + 1].start() if index + 1 < len(found) else len(stripped)
        block = stripped[match.start():end]
        if kind in {"structure", "class"}:
            require("where" in block, "STRUCTURE_WITHOUT_FIELDS " + name)
            statement = block  # include EVERY original field in integrity comparison
        else:
            terminators = [x for x in (block.find(":="), block.find("\nwhere"))
                           if x >= 0]
            require(bool(terminators), "UNKNOWN_DECLARATION_BOUNDARY " + name)
            statement = block[:min(terminators)]
        result[name] = " ".join(statement.split())
    return result

def contract(original, code):
    left, right = local_declarations(original), local_declarations(code)
    require(len(left) == 39 and list(left) == list(right),
            "PUBLIC_39_NAME_ORDER_MISMATCH")
    reasons = {}
    for name in left:
        if left[name] == right[name]:
            continue
        require(normalized_signature(right[name]) == left[name],
                "NON_UNIVERSE_OR_PROOF_TERM_SIGNATURE_CHANGE " + name)
        reasons[name] = (
            "Exact original declaration and all structure fields retained up to "
            "explicit native universe and alternative closed Fin proof terms"
        )
    require(not cycle.TRUST_BYPASS.search(cycle.without_comments_strings(code)),
            "TRUST_ESCAPE_IN_CANDIDATE")
    require(cycle.imports(original) ==
            ["KUOS.DependentOriginationDoubleDeloopingTypeADimensionFourFamilyRLPV1_104"],
            "ORIGINAL_IMPORT_UNEXPECTED")
    require(cycle.imports(code) == cycle.imports(original), "IMPORT_CHANGED")
    return {
        "public_declarations": list(left),
        "signature_changes": reasons,
        "import_additions": {},
        "declaration_statement_text_unchanged": not bool(reasons),
        "inline_where_structure_fields_exact": True,
        "reconstructed_original_signature_compatible": True,
    }

def real_lean_mcp(candidate, name):
    from scripts.check_kuuos_lean_lsp_mcp_compatibility_v7_17 import (
        MCPClient, PROTOCOL_VERSION, call_tool, tool_map
    )
    from scripts.check_kuuos_lean_mcp_parent_pr3522_v155_v1 import structured
    from scripts.kuuos_lean_mcp_repair_loop_v1 import require_semantics
    disabled = ",".join([
        "lean_run_code", "lean_build", "lean_profile_proof",
        "lean_minimal_hypotheses", "lean_leansearch", "lean_loogle",
        "lean_leanfinder", "lean_state_search", "lean_hammer_premise"
    ])
    require(not PROBE.exists(), "MCP_PROBE_EXISTS")
    with PROBE.open("xb") as f:
        f.write(candidate)
    receipt = {
        "status": "MCP_NO_DATA", "candidate_blob": cycle.git_blob(candidate),
        "selected_candidate": name, "version": "lean-lsp-mcp==0.30.0",
        "independent_ci_success": False
    }
    client = None
    try:
        client = MCPClient(
            ["uvx","--from","lean-lsp-mcp==0.30.0","lean-lsp-mcp","--transport","stdio"],
            cwd=ROOT, timeout_seconds=240, env={
                "LEAN_PROJECT_PATH": str(ROOT), "LEAN_LOG_LEVEL": "NONE",
                "LEAN_MCP_SCRATCH_SLOTS": "1", "LEAN_MCP_DISABLED_TOOLS": disabled
            })
        init = client.request("initialize",{
            "protocolVersion": PROTOCOL_VERSION, "capabilities": {},
            "clientInfo": {"name":"KuuOS v1.105 CodeAI local","version":"1"}})
        client.notify("notifications/initialized")
        tools = tool_map(client.request("tools/list"))
        require("lean_diagnostic_messages" in tools and "lean_goal" in tools,
                "MCP_TYPED_TOOLS_MISSING")
        require("lean_build" not in tools and "lean_run_code" not in tools,
                "MCP_EFFECT_ESCAPE")
        response = call_tool(client,"lean_diagnostic_messages",{
            "file_path": str(PROBE.relative_to(ROOT)), "timeout_s": 120})
        diag = require_semantics(structured(response),candidate)
        receipt.update({
            "status": "MCP_TYPED_LOCAL_GREEN" if diag.success and not diag.errors
                and not diag.partial and not diag.failed_dependencies else "MCP_TYPED_RED",
            "protocol": init.get("result",{}).get("protocolVersion"),
            "success": diag.success,
            "errors": len(diag.errors),
            "partial": diag.partial,
            "failed_dependencies": diag.failed_dependencies,
            "diagnostics": diag.diagnostics[:20]
        })
    finally:
        if client is not None:
            client.close()
        if PROBE.exists():
            require(PROBE.read_bytes() == candidate,"MCP_PROBE_CHANGED")
            PROBE.unlink()
        (OUT / "real-mcp-receipt.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2,sort_keys=True)+"\n")
    return receipt

def main():
    pins=check_fixed()
    require(not OUT.exists() and not GREEN.exists(), "APPEND_ONLY_OUTPUT_OVERLAP")
    OUT.mkdir()
    original=ORIGINAL.read_text()
    records=[]
    selected=None
    for idx,(name,blob) in enumerate(CANDIDATES,1):
        path=ROOT / "research/codeai/v1105/r1" / (name + ".lean")
        require(path.is_file() and not path.is_symlink() and
                cycle.git_blob(path.read_bytes()) == blob,
                "CANDIDATE_BLOB_MISMATCH " + name)
        data=path.read_bytes()
        ct=contract(original,data.decode("utf8"))
        out=OUT / ("attempt-%02d-"%idx+name)
        out.mkdir()
        rec={
            "candidate":name,"candidate_blob":blob,"original_blob":PINS[ORIGINAL],
            "predecessor_blob":PINS[V104],"source_head":os.environ.get("GITHUB_SHA"),
            "contract":ct,"state":"NOT_TESTED","independent_ci_started":False,
            "formal_PR_3555_mutated":False
        }
        direct=cycle.run_lean(ROOT,path,out/"direct",seconds=850)
        rec["direct"]=direct
        if not direct["direct_success"]:
            rec["state"]="DIRECT_RED" if not direct["timed_out"] else "NO_DATA_TIMEOUT"
        else:
            auditfile=out/"audit.lean"
            auditfile.write_text(data.decode()+"\n"+"\n".join(
                "#print axioms "+NAMESPACE+"."+n for n in ct["public_declarations"])+"\n")
            audit=cycle.run_lean(ROOT,auditfile,out/"axiom_audit",seconds=850)
            rec["audit"]=audit
            if audit["direct_success"]:
                try:
                    axioms=cycle.audit_axioms(
                        (out/"axiom_audit"/"stdout.log").read_text(),
                        ct["public_declarations"],NAMESPACE)
                    require(axioms["checked"]==39 and
                            not set(axioms["allowed"])-STANDARD and
                            not axioms["sorryAx"],"AXIOM_REQUIREMENTS_NOT_MET")
                    rec["axioms"]=axioms
                    rec["state"]="LOCAL_DIRECT_AND_39_AXIOMS_GREEN"
                except cycle.Hold as e:
                    rec["state"]="AXIOM_OBSTRUCTION"
                    rec["obstruction"]=str(e)
            else:
                rec["state"]="AXIOM_AUDIT_RED"
        (out/"receipt.json").write_text(json.dumps(rec,ensure_ascii=False,indent=2,sort_keys=True)+"\n")
        records.append(rec)
        print("KUUOS_V1105_LOCAL_ATTEMPT",json.dumps({
            "candidate":name,"blob":blob,"status":rec["state"],
            "errors":direct["error_count"],"exit_code":direct["exit_code"],
            "independent_CI_started":False
        }),flush=True)
        if rec["state"]=="LOCAL_DIRECT_AND_39_AXIOMS_GREEN":
            selected=(name,data,rec)
            break
    state="NO_LOCAL_GREEN"
    mcp=None
    if selected:
        name,data,rec=selected
        mcp=real_lean_mcp(data,name)
        if mcp["status"]=="MCP_TYPED_LOCAL_GREEN":
            GREEN.mkdir()
            (GREEN/"selected.lean").write_bytes(data)
            (GREEN/"selected.json").write_text(json.dumps({
                "name":name,"blob":cycle.git_blob(data),
                "original_blob":PINS[ORIGINAL],"v104_blob":PINS[V104],
                "source_head":os.environ.get("GITHUB_SHA"),
                "public_names":39,"axioms":rec["axioms"],
                "real_mcp":mcp["status"],"independent_ci_started":False,
                "formal_pr_modified":False
            },ensure_ascii=False,sort_keys=True,indent=2)+"\n")
            state="LOCAL_LEAN_39_AXIOMS_AND_REAL_MCP_GREEN"
        else:
            state="REAL_LEAN_MCP_OBSTRUCTION"
    (OUT/"summary.json").write_text(json.dumps({
        "status":state,"pins":pins,"original_blob":PINS[ORIGINAL],
        "v104_blob":PINS[V104],"trials":records,
        "mcp":mcp,"independent_ci_started":False,
        "formal_pr_modified":False
    },ensure_ascii=False,sort_keys=True,indent=2)+"\n")
    for p,blob in PINS.items():
        require(cycle.git_blob(p.read_bytes())==blob,"PINNED_SOURCE_MODIFIED")
    print("KUUOS_V1105_LOCAL_FINAL",json.dumps({"state":state,
         "trials":len(records),"independent_ci_started":False}),flush=True)
    return 0 if state=="LOCAL_LEAN_39_AXIOMS_AND_REAL_MCP_GREEN" else 1

if __name__=="__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        OUT.mkdir(exist_ok=True,parents=True)
        (OUT/"obstruction.txt").write_text(type(e).__name__+": "+str(e)+"\n")
        print("KUUOS_V1105_LOCAL_HOLD",type(e).__name__,str(e),file=sys.stderr)
        raise SystemExit(2)
