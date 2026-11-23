#!/usr/bin/env python3
"""v1.104 CodeAI append-only local trials: actual Lean -> 21 axioms -> real typed Lean MCP.
Never run independent CI, change the original PR, or promote an unverified candidate.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
import sys
from scripts import kuuos_sandbox_lean_cycle_v1 as cycle

ROOT = Path(__file__).resolve().parents[1]
BRANCH = "research/v1104-codeai-r3-multitrial-20261124"
ORIGINAL = ROOT / "formal/KUOS/DependentOriginationDoubleDeloopingTypeADimensionFourFamilyRLPV1_104.lean"
V103 = ROOT / "formal/KUOS/DependentOriginationDoubleDeloopingTypeAHighDimensionalFillersV1_103.lean"
V102 = ROOT / "formal/KUOS/DependentOriginationDoubleDeloopingTypeALowDimensionalFillersV1_102.lean"
OUT = Path("/tmp/kuuos-v1104-r3-serial-local-evidence")
GREEN = Path("/tmp/kuuos-v1104-r3-selected-only")
PROBE = ROOT / "formal/KUOS/DependentOriginationDoubleDeloopingTypeADimensionFourFamilyRLPSandboxProbeV1_104.lean"
NAMESPACE = "KUOS.DependentOriginationDoubleDeloopingTypeADimensionFourFamilyRLPV1_104"
PINS = {
    ORIGINAL: "dc75c6d91c317bc8d350c7c45d4268dce38bf06c",
    V103: "dbec61c9798481709f2deda0028e84b7515f209e",
    V102: "f8b492b210e5525990aa587fa2eb5c8648a5ff19",
}
CANDIDATES = [
    ("A-revert", "5c911aaeb9a21baff57f6af8c8655309af47d027"),
    ("B-normnum", "1e54ff4a2a8cf20ed352e08f974f458292cab09d"),
    ("C-simp", "e2bc9de0fe06fe39c75292866c98f57ae8cdf002"),
]
STANDARD_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}

def require(ok, reason):
    if not ok:
        raise cycle.Hold(reason)

def ensure_sources():
    require(os.environ.get("GITHUB_ACTIONS") == "true", "WRONG_RUNTIME")
    require(os.environ.get("GITHUB_REF_NAME") == BRANCH, "WRONG_BRANCH")
    for path, sha in PINS.items():
        require(path.is_file() and not path.is_symlink() and cycle.git_blob(path.read_bytes()) == sha,
                "SOURCE_MISMATCH: " + str(path))
    require(cycle.git_blob((ROOT / "scripts/kuuos_sandbox_lean_cycle_v1.py").read_bytes())
            == "5383253dbe9cda9cab90a410c2fd66ee6b9d6f41", "CYCLE_ENGINE_MISMATCH")
    return cycle.require_pins(ROOT)

def contract(original: str, candidate: str):
    old = cycle.declarations(original)
    new = cycle.declarations(candidate)
    require(len(old) == 21 and list(old) == list(new) and
            list(old)[-1] == "natDoubleDelooping_standardTypeA_rlp",
            "21_DECLARATION_OBSTRUCTION")
    reasons = {}
    for name in old:
        if old[name] == new[name]:
            continue
        if name == "natTypeAHornLabel_tetrahedron_of_hornSimplex":
            expected = old[name].replace("(Λ[g.n, g.i] : SSet)", "(Λ[g.n, g.i] : SSet.{0})")
            reason = "Explicit Type0 simplicial-set carrier; original was not elaborated"
        elif name == "natTypeAFourCocycle_distinguished_zero":
            expected = old[name].replace(
                "(natTypeAFourCocycle i h0 h4 f).TypeADistinguishedZero i",
                "KUOS.DependentOriginationDoubleDeloopingTypeACocycleLiftingV1_101."
                "NatNormalizedDuskinCocycle.TypeADistinguishedZero "
                "(natTypeAFourCocycle i h0 h4 f) i")
            reason = "Correct existing v1.101 named predicate, not a fabricated projected method"
        else:
            raise cycle.Hold("UNADMITTED_SIGNATURE: " + name)
        require(expected == new[name], "UNADMITTED_CHANGE: " + name)
        reasons[name] = reason
    require(set(reasons) == {
        "natTypeAHornLabel_tetrahedron_of_hornSimplex",
        "natTypeAFourCocycle_distinguished_zero"
    }, "MISSING_REQUIRED_INTERFACE_REPAIRS")
    out = cycle.source_contract(original, candidate, reasons, {})
    require(cycle.imports(candidate) == [
        "KUOS.DependentOriginationDoubleDeloopingTypeAHighDimensionalFillersV1_103"
    ], "IMPORT_OBSTRUCTION")
    return out

def real_lean_mcp(candidate: bytes, attempt: str):
    from scripts.check_kuuos_lean_lsp_mcp_compatibility_v7_17 import (
        MCPClient, PROTOCOL_VERSION, call_tool, tool_map)
    from scripts.check_kuuos_lean_mcp_parent_pr3522_v155_v1 import structured
    from scripts.kuuos_lean_mcp_repair_loop_v1 import require_semantics
    disabled = ",".join([
        "lean_run_code", "lean_build", "lean_profile_proof",
        "lean_minimal_hypotheses", "lean_leansearch", "lean_loogle",
        "lean_leanfinder", "lean_state_search", "lean_hammer_premise",
    ])
    require(not PROBE.exists(), "MCP_PROBE_ALREADY_EXISTS")
    receipt = {
        "status": "MCP_NO_DATA", "candidate_blob": cycle.git_blob(candidate),
        "attempt": attempt, "version": "lean-lsp-mcp==0.30.0",
        "independent_ci_success": False, "authority": "LOCAL_ONLY"
    }
    client = None
    with PROBE.open("xb") as f:
        f.write(candidate)
    try:
        client = MCPClient(
            ["uvx", "--from", "lean-lsp-mcp==0.30.0", "lean-lsp-mcp", "--transport", "stdio"],
            cwd=ROOT,
            env={
                "LEAN_PROJECT_PATH": str(ROOT), "LEAN_LOG_LEVEL": "NONE",
                "LEAN_MCP_SCRATCH_SLOTS": "1", "LEAN_MCP_DISABLED_TOOLS": disabled,
            }, timeout_seconds=240,
        )
        init = client.request("initialize", {
            "protocolVersion": PROTOCOL_VERSION, "capabilities": {},
            "clientInfo": {"name": "KuuOS v1.104 R3 local typed verification",
                           "version": "1"},
        })
        client.notify("notifications/initialized")
        tools = tool_map(client.request("tools/list"))
        require("lean_diagnostic_messages" in tools and "lean_goal" in tools,
                "MCP_SEMANTIC_TOOLS_MISSING")
        require("lean_build" not in tools and "lean_run_code" not in tools,
                "MCP_HIGH_EFFECT_TOOLS_EXPOSED")
        response = call_tool(
            client, "lean_diagnostic_messages",
            {"file_path": str(PROBE.relative_to(ROOT)), "timeout_s": 120})
        diag = require_semantics(structured(response), candidate)
        receipt.update({
            "status": "MCP_TYPED_LOCAL_GREEN" if
                diag.success and not diag.errors and not diag.partial
                and not diag.failed_dependencies else "MCP_TYPED_RED",
            "protocol": init.get("result", {}).get("protocolVersion"),
            "diagnostics_success": diag.success,
            "partial": diag.partial,
            "failed_dependencies": diag.failed_dependencies,
            "error_count": len(diag.errors),
            "diagnostics": diag.diagnostics[:25],
        })
    finally:
        if client is not None:
            client.close()
        if PROBE.exists():
            require(PROBE.read_bytes() == candidate, "MCP_PROBE_MODIFIED")
            PROBE.unlink()
        (OUT / "real-lean-mcp-receipt.json").write_text(
            json.dumps(receipt, sort_keys=True, indent=2, ensure_ascii=False) + "\n")
    return receipt

def main():
    pins = ensure_sources()
    require(not OUT.exists() and not GREEN.exists(), "APPEND_ONLY_OUTPUT_REUSE")
    OUT.mkdir(parents=True)
    original = ORIGINAL.read_text()
    trials = []
    selected = None
    for index, (name, expected_blob) in enumerate(CANDIDATES, 1):
        path = ROOT / "research/codeai/v1104/r3" / (name + ".lean")
        require(path.is_file() and not path.is_symlink()
                and cycle.git_blob(path.read_bytes()) == expected_blob,
                "CANDIDATE_BLOB_MISMATCH " + name)
        code = path.read_text()
        scope = contract(original, code)
        d = OUT / ("attempt-%02d-%s" % (index, name))
        d.mkdir()
        record = {
            "candidate": name, "blob": expected_blob,
            "source_sha": os.environ.get("GITHUB_SHA"),
            "original_blob": PINS[ORIGINAL], "dependency_blob": PINS[V103],
            "source_contract": scope, "status": "UNVERIFIED",
            "independent_ci_started": False, "PR_3555_modified": False,
        }
        compiled = cycle.run_lean(ROOT, path, d / "direct", seconds=850)
        record["direct"] = compiled
        if not compiled["direct_success"]:
            record["status"] = "DIRECT_RED" if not compiled["timed_out"] else "NO_DATA_TIMEOUT"
        else:
            audit_file = d / "axioms.lean"
            report = code + "\n" + "\n".join(
                "#print axioms " + NAMESPACE + "." + x
                for x in scope["public_declarations"]) + "\n"
            audit_file.write_text(report)
            ax_run = cycle.run_lean(ROOT, audit_file, d / "axioms", seconds=850)
            record["audit_direct"] = ax_run
            if not ax_run["direct_success"]:
                record["status"] = "AXIOM_AUDIT_RED"
            else:
                try:
                    axioms = cycle.audit_axioms(
                        (d / "axioms/stdout.log").read_text(),
                        scope["public_declarations"], NAMESPACE)
                    require(axioms["checked"] == 21 and
                            not set(axioms["allowed"]) - STANDARD_AXIOMS
                            and not axioms["sorryAx"],
                            "AXIOM_INVARIANT_FAILURE")
                    record["axioms"] = axioms
                    record["status"] = "LOCAL_DIRECT_AND_21_AXIOMS_GREEN"
                except cycle.Hold as exc:
                    record["status"] = "AXIOM_OBSTRUCTION"
                    record["obstruction"] = str(exc)
        (d / "receipt.json").write_text(json.dumps(
            record, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
        trials.append(record)
        print("KUUOS_V1104_R3_TRIAL_RECEIPT", json.dumps({
            "candidate": name, "blob": expected_blob,
            "status": record["status"],
            "error_count": compiled["error_count"],
            "exit_code": compiled["exit_code"],
            "independent_ci": False,
        }, sort_keys=True), flush=True)
        if record["status"] == "LOCAL_DIRECT_AND_21_AXIOMS_GREEN":
            selected = (name, path, record)
            break
    result = {
        "schema": "kuuos-v1104-r3-serial-candidate-local-receipt-v1",
        "source_sha": os.environ.get("GITHUB_SHA"), "original_blob": PINS[ORIGINAL],
        "v103_blob": PINS[V103], "v102_blob": PINS[V102],
        "pin": pins, "trials": trials, "selected": None,
        "independent_ci_started": False, "PR_3555_modified": False,
        "merge_authorized": False, "authority": "LOCAL_ONLY",
        "status": "NO_LOCAL_GREEN"
    }
    if selected is not None:
        name, path, record = selected
        candidate = path.read_bytes()
        mcp = real_lean_mcp(candidate, name)
        result["real_lean_mcp"] = mcp
        if mcp["status"] == "MCP_TYPED_LOCAL_GREEN":
            GREEN.mkdir()
            (GREEN / "selected.lean").write_bytes(candidate)
            result["selected"] = name
            result["status"] = "LOCAL_LEAN_21_AXIOMS_AND_REAL_MCP_GREEN"
            (GREEN / "selected-source.json").write_text(json.dumps({
                "candidate": name,
                "git_blob": cycle.git_blob(candidate),
                "source_sha": os.environ.get("GITHUB_SHA"),
                "original_blob": PINS[ORIGINAL],
                "v103_blob": PINS[V103],
                "v102_blob": PINS[V102],
                "public_decl_count": 21,
                "local_direct_lean": True,
                "local_axiom_21": True,
                "real_lean_mcp": True,
                "independent_ci_started": False,
                "PR_3555_modified": False,
            }, sort_keys=True, indent=2) + "\n")
        else:
            result["status"] = "REAL_LEAN_MCP_OBSTRUCTION"
    (OUT / "summary.json").write_text(json.dumps(
        result, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    for path, sha in PINS.items():
        require(cycle.git_blob(path.read_bytes()) == sha,
                "SOURCE_MODIFIED_AFTER_TEST")
    for name, sha in CANDIDATES:
        path = ROOT / "research/codeai/v1104/r3" / (name + ".lean")
        require(cycle.git_blob(path.read_bytes()) == sha,
                "CANDIDATE_MUTATED_AFTER_TEST")
    print("KUUOS_V1104_R3_FINAL",json.dumps({
        "status": result["status"], "selected": result["selected"],
        "trials": len(trials), "independent_ci": False
    }), flush=True)
    return 0 if result["status"] == "LOCAL_LEAN_21_AXIOMS_AND_REAL_MCP_GREEN" else 1

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / "obstruction.txt").write_text(type(exc).__name__ + ": " + str(exc) + "\n")
        print("KUUOS_V1104_R3_HOLD", type(exc).__name__, str(exc), file=sys.stderr)
        raise SystemExit(2)
