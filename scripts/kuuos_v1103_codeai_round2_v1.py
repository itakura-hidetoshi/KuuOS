#!/usr/bin/env python3
"""v1.103 CodeAI round-2 candidate portfolio, pinned direct Lean, real Lean MCP.
Candidates are proposal-only until independent exact-source CI succeeds.
All proof mutations are temporary, on an isolated Actions checkout.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
import stat
import subprocess
import tempfile
from scripts import kuuos_v1103_codeai_structural_candidates_v1 as base
from scripts.check_kuuos_lean_mcp_fullsource_v1 import git_blob, sha256, imports_of, declarations_of
from scripts.check_kuuos_lean_lsp_mcp_compatibility_v7_17 import (
    MCPClient, PROTOCOL_VERSION, require_pins, call_tool, tool_map)
from scripts.check_kuuos_lean_mcp_parent_pr3522_v155_v1 import structured
from scripts.kuuos_lean_mcp_repair_loop_v1 import (
    require_semantics, forbidden_code_constructs, DISABLED_MCP_TOOLS)

ROUND1 = base.variants
OLD183 = "            congr <;> exact Subsingleton.elim _ _"
OLD198 = ("          apply congrArg duskinComparison\n"
          "          rw [← hsource]\n"
          "          exact hnat.symm")
RW = ("          rw [← hsource]\n"
      "          exact congrArg duskinComparison hnat.symm")
CALC = ("          calc\n"
        "            _ = duskinComparison\n"
        "              (f.map.app (op ⦋2⦌)\n"
        "                ((Λ[g.n, g.i] : SSet).map alpha.op x)) := by\n"
        "                  exact congrArg duskinComparison hnat.symm\n"
        "            _ = _ := by\n"
        "                  exact congrArg\n"
        "                    (fun y => duskinComparison\n"
        "                      (f.map.app (op ⦋2⦌) y)) hsource")
HPHQ = ("            have hp : p = natOrdinalEdge p.as.le :=\n"
        "              Subsingleton.elim _ _\n"
        "            have hq : q = natOrdinalEdge q.as.le :=\n"
        "              Subsingleton.elim _ _\n"
        "            rw [hp, hq]")
OUT = Path("/tmp/kuuos-v1103-codeai-type-probes")
MOUT = Path("/tmp/kuuos-v1103-codeai-round2-mcp")


def variants(source: str) -> dict[str, str]:
    qualified = ROUND1(source)["round1-qualified-names-parser"]
    proposals = {}
    for arrow, fragment in (("original", OLD183), ("congr", "            congr"),
                            ("explicit-arrow", HPHQ)):
        s = qualified if fragment == OLD183 else base.replace_once(
            qualified, OLD183, fragment, "v1.103 arrow subsingleton step")
        for naturality, fix in (("rw", RW), ("calc", CALC)):
            proposals["round2-"+arrow+"-"+naturality] = base.replace_once(
                s, OLD198, fix, "v1.103 naturality congrArg step")
    return proposals


def verify_mcp() -> int:
    portfolio = json.loads((OUT/"portfolio_receipt.json").read_text())
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text())
    head = event["pull_request"]["head"]["sha"]
    assert portfolio["head"] == head
    assert portfolio["original_blob"] == base.ORIGINAL_BLOB
    successes = [r for r in portfolio["candidates"]
                 if r["status"] == "SUCCESS" and r["exit_code"] == 0
                 and r["olean_exists"]]
    MOUT.mkdir(parents=True, exist_ok=False)
    record = {"source_head":head,"original_blob":base.ORIGINAL_BLOB,
              "strict_direct_green":[r["variant"] for r in successes],
              "selected":None,"mcp_success":False,"mcp_errors":None,
              "second_direct_green":False,"source_restored":False,
              "git_mutation":False,"independent_ci_certified":False,
              "status":"NO_DIRECT_LEAN_GREEN"}
    src = base.ROOT/base.TARGET
    old = src.read_bytes()
    mode = stat.S_IMODE(src.stat().st_mode)
    client = None
    try:
        assert git_blob(old) == base.ORIGINAL_BLOB
        require_pins(base.ROOT)
        if not successes:
            return 0
        choice = successes[0]
        record["selected"] = choice["variant"]
        candidate = variants(old.decode("utf-8"))[choice["variant"]].encode("utf-8")
        assert git_blob(candidate) == choice["candidate_blob"]
        assert sha256(candidate) == choice["candidate_sha256"]
        assert imports_of(old.decode()) == imports_of(candidate.decode())
        signature = lambda s: [(d["kind"],d["name_lexical"])
            for d in declarations_of(s,base.MODULE)]
        assert signature(old.decode()) == signature(candidate.decode())
        assert not forbidden_code_constructs(candidate.decode())
        src.write_bytes(candidate)
        client = MCPClient(["uvx","--from","lean-lsp-mcp==0.30.0",
                            "lean-lsp-mcp","--transport","stdio"],
                           cwd=base.ROOT,
                           env={"LEAN_PROJECT_PATH":str(base.ROOT),
                                "LEAN_LOG_LEVEL":"NONE",
                                "LEAN_MCP_DISABLED_TOOLS":DISABLED_MCP_TOOLS,
                                "LEAN_MCP_SCRATCH_SLOTS":"1"},
                           timeout_seconds=240)
        client.request("initialize", {
            "protocolVersion":PROTOCOL_VERSION,"capabilities":{},
            "clientInfo":{"name":"KuuOS v1.103 round2","version":"1"}})
        client.notify("notifications/initialized")
        available=tool_map(client.request("tools/list"))
        assert {"lean_diagnostic_messages","lean_goal","lean_multi_attempt"}.issubset(available)
        assert "lean_build" not in available and "lean_run_code" not in available
        raw=call_tool(client,"lean_diagnostic_messages",{
            "file_path":base.TARGET,"timeout_s":120})
        obs=require_semantics(structured(raw),candidate)
        record["mcp_success"]=obs.success and not obs.partial
        record["mcp_errors"]=len(obs.errors)
        record["mcp_diagnostic_sha256"]=sha256(json.dumps(
            obs.diagnostics,sort_keys=True).encode())
        if obs.errors or not obs.success or obs.partial:
            raise RuntimeError("actual Lean MCP diagnostics blocked candidate")
        for line in (183,198):
            for tool,args in (
                ("lean_goal",{"file_path":base.TARGET,"line":line}),
                ("lean_multi_attempt",{"file_path":base.TARGET,"line":line,
                                       "snippets":["rfl","simp","exact Subsingleton.elim _ _"]}),
            ):
                try:
                    result=call_tool(client,tool,args)
                    record[tool+"_"+str(line)]=sha256(json.dumps(
                        result.get("result",{}),sort_keys=True).encode())
                except Exception as exc:
                    record[tool+"_"+str(line)+"_obstruction"]=str(exc)[:250]
        client.close()
        client=None
        with tempfile.TemporaryDirectory(prefix="v1103-round2-mcp-") as d:
            olean=Path(d)/"candidate.olean"
            done=subprocess.run(
                ["lake","env","lean","-DwarningAsError=true",
                 "-Dweak.sorryAsError=true","-o",str(olean),base.TARGET],
                cwd=base.ROOT,capture_output=True,text=True,timeout=300)
            log=done.stdout+"\n"+done.stderr
            (MOUT/"second_direct_lean.log").write_text(log)
            record["second_direct_exit"]=done.returncode
            record["second_direct_log_sha256"]=sha256(log.encode())
            if done.returncode or not olean.is_file() or "sorryAx" in log:
                raise RuntimeError("second direct fixed Lean failed")
        (MOUT/"candidate.lean").write_bytes(candidate)
        record["second_direct_green"]=True
        record["status"]="LOCAL_MCP_AND_SECOND_DIRECT_GREEN_CI_NOT_CERTIFIED"
    except Exception as exc:
        record["status"]="MCP_OR_DIRECT_OBSTRUCTION"
        record["obstruction"]=type(exc).__name__+": "+str(exc)[:700]
    finally:
        if client:
            try: client.close()
            except Exception as exc: record["mcp_close_obstruction"]=str(exc)[:250]
        src.write_bytes(old)
        src.chmod(mode)
        record["source_restored"]=(src.read_bytes()==old and
                                    stat.S_IMODE(src.stat().st_mode)==mode)
        (MOUT/"receipt.json").write_text(json.dumps(
            record,sort_keys=True,ensure_ascii=False,indent=2)+"\n")
        print("KUUOS_V1103_ROUND2_MCP_RECEIPT "+json.dumps(
            record,sort_keys=True,ensure_ascii=False))
    return 0 if record["source_restored"] else 2


def main() -> int:
    base.variants=variants
    status=base.main()
    if status: return status
    for p in sorted(OUT.glob("*.log")):
        print("KUUOS_V1103_ROUND2_FULL_LOG_BEGIN "+p.name)
        print(p.read_text(errors="replace")[-9000:])
        print("KUUOS_V1103_ROUND2_FULL_LOG_END "+p.name)
    return verify_mcp()


if __name__=="__main__":
    raise SystemExit(main())
