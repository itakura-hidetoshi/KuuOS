#!/usr/bin/env python3
"""CodeAI v1.97 candidate -> real Lean MCP -> direct pinned Lean precommit.

Isolated PR checkout only; restores original proof even on failure.
No Git writes, no paid model, no weakening, no hidden axioms, no main merge.
This receipt is NOT independent CI certification or merge authority.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import tempfile

from scripts.kuuos_v197_codeai_structural_candidates_v1 import (
    ROOT, REPO, TARGET, ORIGINAL_BLOB, variants,
)
from scripts.check_kuuos_lean_mcp_fullsource_v1 import (
    git_blob, sha256, imports_of, declarations_of,
)
from scripts.check_kuuos_lean_lsp_mcp_compatibility_v7_17 import (
    MCPClient, PROTOCOL_VERSION, require_pins, call_tool, tool_map,
)
from scripts.check_kuuos_lean_mcp_parent_pr3522_v155_v1 import structured
from scripts.kuuos_lean_mcp_repair_loop_v1 import (
    require_semantics, forbidden_code_constructs, DISABLED_MCP_TOOLS,
)

CANDIDATE = "round3-associator-simp-nat"
EXACT_CANDIDATE_BLOB = "2ee902a37f15d1c9d2068f053375482188a90ed4"
OUT = Path("/tmp/kuuos-v197-codeai-lean-mcp")


def main() -> int:
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text())
    if event.get("number") != 3522 or event.get("repository", {}).get("full_name") != REPO:
        raise RuntimeError("wrong PR event")
    source_head = event["pull_request"]["head"]["sha"]
    branch = event["pull_request"]["head"]["ref"]
    require_pins(ROOT)
    source_path = ROOT / TARGET
    original = source_path.read_bytes()
    if git_blob(original) != ORIGINAL_BLOB:
        raise RuntimeError("original v1.97 source blob drift")
    new_source = variants(original.decode("utf-8"))[CANDIDATE].encode("utf-8")
    if git_blob(new_source) != EXACT_CANDIDATE_BLOB:
        raise RuntimeError("CodeAI candidate != pinned directly compiled blob")
    old_decls = [(d["kind"], d["name_lexical"]) for d in
                 declarations_of(original.decode("utf-8"), TARGET)]
    new_decls = [(d["kind"], d["name_lexical"]) for d in
                 declarations_of(new_source.decode("utf-8"), TARGET)]
    if old_decls != new_decls or imports_of(original.decode()) != imports_of(new_source.decode()):
        raise RuntimeError("Lean imports/declaration names changed")
    if forbidden_code_constructs(new_source.decode("utf-8")):
        raise RuntimeError("candidate includes forbidden executable constructs")
    OUT.mkdir(parents=True, exist_ok=False)
    original_mode = stat.S_IMODE(source_path.stat().st_mode)
    receipt = {
        "schema": "kuuos-v197-codeai-mcp-direct-precommit-v1",
        "source_head": source_head, "branch": branch,
        "original_blob": ORIGINAL_BLOB, "candidate_blob": EXACT_CANDIDATE_BLOB,
        "source_restored": False, "mcp_complete": False,
        "mcp_diagnostic_errors": None, "direct_lean_success": False,
        "independent_ci_certified": False, "git_write_performed": False,
        "status": "NO_DATA",
    }
    client = None
    try:
        source_path.write_bytes(new_source)
        cmd = ["uvx","--from","lean-lsp-mcp==0.30.0",
               "lean-lsp-mcp","--transport","stdio"]
        env = {
            "LEAN_PROJECT_PATH": str(ROOT),
            "LEAN_LOG_LEVEL": "NONE",
            "LEAN_MCP_DISABLED_TOOLS": DISABLED_MCP_TOOLS,
            "LEAN_MCP_SCRATCH_SLOTS": "1",
        }
        client = MCPClient(cmd, cwd=ROOT, env=env, timeout_seconds=240)
        client.request("initialize", {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {},
            "clientInfo": {"name": "KuuOS v1.97 CodeAI exact MCP", "version": "1"},
        })
        client.notify("notifications/initialized")
        available = tool_map(client.request("tools/list"))
        required = {"lean_diagnostic_messages", "lean_goal", "lean_multi_attempt"}
        if not required.issubset(available):
            raise RuntimeError("MCP has missing required tools")
        if "lean_build" in available or "lean_run_code" in available:
            raise RuntimeError("MCP high-effect unsafe tools are enabled")
        result = call_tool(client, "lean_diagnostic_messages", {
            "file_path": TARGET, "timeout_s": 120,
        })
        observed = require_semantics(structured(result), new_source)
        receipt["mcp_complete"] = observed.success and not observed.partial
        receipt["mcp_diagnostic_errors"] = len(observed.errors)
        receipt["mcp_diagnostic_sha256"] = sha256(
            json.dumps(observed.diagnostics, sort_keys=True).encode("utf-8")
        )
        if observed.errors or not observed.success or observed.partial:
            raise RuntimeError("MCP diagnostics not completely green")
        # Record, but do not promote an optional tactic probe to proof authority.
        # The candidate is already syntactically complete (no open proof goal).
        for tool, params in (
            ("lean_goal", {"file_path": TARGET, "line": 54}),
            ("lean_multi_attempt", {"file_path": TARGET, "line": 54,
                                    "snippets": ["rfl", "simp"]}),
        ):
            try:
                response = call_tool(client, tool, params)
                receipt[tool + "_result_sha256"] = sha256(
                    json.dumps(response.get("result", {}), sort_keys=True).encode("utf-8")
                )
            except Exception as exc:
                receipt[tool + "_obstruction"] = type(exc).__name__ + ": " + str(exc)[:240]
        client.close()
        client = None
        with tempfile.TemporaryDirectory(prefix="kuuos-v197-mcp-direct-") as tmp:
            lean_out = Path(tmp) / "candidate.olean"
            run = subprocess.run([
                "lake","env","lean","-DwarningAsError=true",
                "-Dweak.sorryAsError=true","-o",str(lean_out),TARGET,
            ],cwd=ROOT, capture_output=True, text=True, timeout=300)
            log=run.stdout+"\n"+run.stderr
            (OUT/"direct_lean.log").write_text(log)
            receipt["direct_lean_exit"] = run.returncode
            receipt["direct_lean_log_sha256"] = sha256(log.encode("utf-8"))
            receipt["direct_lean_success"] = run.returncode == 0 and lean_out.is_file()
            if not receipt["direct_lean_success"]:
                raise RuntimeError("independent direct Lean failed on MCP candidate")
        receipt["status"] = "MCP_AND_DIRECT_LEAN_LOCAL_GREEN"
    except Exception as exc:
        receipt["status"] = "MCP_OR_DIRECT_LEAN_OBSTRUCTION"
        receipt["obstruction"] = type(exc).__name__ + ": " + str(exc)[:600]
    finally:
        if client is not None:
            try:
                client.close()
            except Exception as exc:
                receipt["client_close_obstruction"] = str(exc)[:240]
        source_path.write_bytes(original)
        source_path.chmod(original_mode)
        receipt["source_restored"] = (
            source_path.read_bytes() == original
            and stat.S_IMODE(source_path.stat().st_mode) == original_mode
        )
        (OUT/"receipt.json").write_text(
            json.dumps(receipt, sort_keys=True, indent=2, ensure_ascii=False)+"\n"
        )
        print("KUUOS_V197_CODEAI_LEAN_MCP_PRECOMMIT "+
              json.dumps(receipt, sort_keys=True, ensure_ascii=False))
    return 0 if receipt["status"]=="MCP_AND_DIRECT_LEAN_LOCAL_GREEN" and receipt["source_restored"] else 2


if __name__=="__main__":
    raise SystemExit(main())
