#!/usr/bin/env python3
"""Read-only real Lean-LSP MCP probe AFTER source-sealed 14D direct Lean SUCCESS.

Run in a disposable GitHub Actions sandbox, never in canonical main.
The target is the actual 14D import smoke backed by the scratch split; this
is not a proof of the unchanged monolithic module or the public proof root.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from scripts.codeai_v061_f112_fourteen_full_source_split import (
    ROOT, OUT, SOURCE, SOURCE_BLOB, assert_source, blob,
)
from scripts.check_kuuos_lean_lsp_mcp_compatibility_v7_17 import (
    MCPClient, PROTOCOL_VERSION, call_tool, tool_map,
)
from scripts.check_kuuos_lean_mcp_parent_pr3522_v155_v1 import structured

DISABLED = ",".join((
    "lean_run_code", "lean_build", "lean_profile_proof",
    "lean_minimal_hypotheses", "lean_leansearch", "lean_loogle",
    "lean_leanfinder", "lean_state_search", "lean_hammer_premise",
))
TARGET = OUT / "OriginalImportSmoke.lean"
RECEIPT = OUT / "real-lean-mcp-receipt.json"
REQUIRED = {"lean_diagnostic_messages", "lean_file_outline", "lean_goal", "lean_multi_attempt"}


def main() -> int:
    source = assert_source()
    assert blob(SOURCE.read_bytes()) == SOURCE_BLOB
    before_sha = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    manifest = json.loads((OUT / "manifest.json").read_text())
    assert manifest["parent_original_git_blob"] == SOURCE_BLOB
    assert manifest["parent_original_sha256"] == before_sha
    five_stage = json.loads((OUT / "five-stage/manifest.json").read_text())
    assert five_stage["original_fourteen_source_blob"] == SOURCE_BLOB
    assert five_stage["original_fourteen_sha256"] == before_sha
    assert five_stage["original_theorem_declarations_and_bodies_unchanged"] is True
    assert five_stage["original_axiom_audits"] == 21
    assert TARGET.is_file() and "nativeK5PentagonatorFifteen_raw_ne" in TARGET.read_text()
    for name in ("generic_core", "fourteen_five_exchange", "fourteen_five_leftfirst",
                 "fourteen_five_rightfirst", "fourteen_five_theorems",
                 "original_module_import_shim"):
        assert (OUT / (name + "-exit.txt")).read_text().strip() == "0", name
    assert (OUT / "import-smoke-exit.txt").read_text().strip() == "0"

    data = {
        "schema": "kuuos.codeai.v061.f112.14d.real_mcp.v1",
        "source_sha256": before_sha,
        "original_blob": SOURCE_BLOB,
        "mcp_version": "0.30.0",
        "target": str(TARGET.relative_to(ROOT)),
        "status": "NO_DATA",
        "independent_lean_ci": False,
        "original_monolith_certified": False,
        "full_root_certified": False,
        "memory_promoted": False,
        "git_write_performed": False,
    }
    client = None
    try:
        client = MCPClient(
            ["uvx", "--from", "lean-lsp-mcp==0.30.0", "lean-lsp-mcp", "--transport", "stdio"],
            cwd=ROOT,
            env={
                "LEAN_PROJECT_PATH": str(ROOT),
                "LEAN_LOG_LEVEL": "NONE",
                "LEAN_MCP_DISABLED_TOOLS": DISABLED,
                "LEAN_MCP_SCRATCH_SLOTS": "1",
            },
            timeout_seconds=240,
        )
        initialized = client.request("initialize", {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {},
            "clientInfo": {"name": "KuuOS CodeAI F112 14D source-bound probe", "version": "0.61"},
        })
        client.notify("notifications/initialized")
        names = tool_map(client.request("tools/list"))
        assert REQUIRED.issubset(names), "NO_DATA: required Lean MCP tools missing"
        assert not ({"lean_run_code", "lean_build"} & set(names))
        data["mcp_protocol"] = initialized.get("result", {}).get("protocolVersion")
        data["tool_count"] = len(names)
        observation = call_tool(
            client, "lean_diagnostic_messages",
            {"file_path": data["target"], "timeout_s": 180},
        )
        diag = structured(observation)
        data["diagnostics_raw_sha256"] = hashlib.sha256(
            json.dumps(observation.get("result", {}), sort_keys=True, ensure_ascii=False).encode()
        ).hexdigest()
        data["semantic_success"] = diag.get("success")
        data["partial"] = diag.get("partial")
        data["failed_dependencies"] = diag.get("failed_dependencies")
        items = diag.get("items")
        data["diagnostics_count"] = len(items) if isinstance(items, list) else None
        data["error_count"] = (
            sum(i.get("severity") == "error" for i in items if isinstance(i, dict))
            if isinstance(items, list) else None
        )
        if not (
            diag.get("success") is True and diag.get("partial") is False
            and diag.get("timed_out") is not True
            and diag.get("failed_dependencies") == []
            and isinstance(items, list) and data["error_count"] == 0
        ):
            data["status"] = "HOLD_MCP_DIAGNOSTICS"
            return 1
        data["status"] = "LOCAL_SPLIT_IMPORT_MCP_SUCCESS_ONLY"
        return 0
    except Exception as exc:
        data["status"] = "MCP_EXECUTION_OBSTRUCTION"
        data["obstruction"] = f"{type(exc).__name__}: {str(exc)[:500]}"
        return 1
    finally:
        if client is not None:
            client.close()
        assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == before_sha
        RECEIPT.write_text(json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
        print("CODEAI_F112_14D_REAL_MCP_OBSERVATION", json.dumps(data, sort_keys=True))


if __name__ == "__main__":
    raise SystemExit(main())
