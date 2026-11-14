#!/usr/bin/env python3
"""Exact-source read-only Lean MCP diagnostic probe for KuuOS PR #3522 v1.55."""
import argparse
import hashlib
import json
import os
import pathlib
from collections.abc import Mapping
from scripts.check_kuuos_lean_lsp_mcp_compatibility_v7_17 import (
    MCPClient, PROTOCOL_VERSION, call_tool, extract_text, require_pins, sha, tool_map,
)

PARENT_HEAD = "182940799808225c466e23a474e97f71add20318"
TARGET_FILE = "formal/KUOS/DependentOriginationStandardTypeAScaledLeibnizPushoutV1_55.lean"
TARGET_BLOB_SHA = "12acfd38ff346c3b27e27fe652c401b9175140b4"
DISABLED = ",".join([
    "lean_run_code", "lean_build", "lean_profile_proof", "lean_minimal_hypotheses",
    "lean_leansearch", "lean_loogle", "lean_leanfinder", "lean_state_search",
    "lean_hammer_premise",
])


def structured(response):
    """Recover a typed observation from MCP structuredContent or text JSON.

    Missing tool data is NO_DATA rather than diagnostic success.
    """
    v = response.get("result", {})
    if not isinstance(v, Mapping):
        return {}
    data = v.get("structuredContent", {})
    if isinstance(data, Mapping) and data:
        payload = data.get("result", data)
        if isinstance(payload, Mapping):
            return dict(payload)
    for part in v.get("content", []):
        if not isinstance(part, Mapping) or part.get("type") != "text":
            continue
        try:
            candidate = json.loads(part.get("text", ""))
        except (TypeError, ValueError):
            continue
        if isinstance(candidate, Mapping) and candidate:
            payload = candidate.get("result", candidate)
            if isinstance(payload, Mapping):
                return dict(payload)
    return {}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-root", required=True)
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()
    root = pathlib.Path(args.target_root).resolve(strict=True)
    pins = require_pins(root)
    source = (root / TARGET_FILE).read_bytes()
    blob = hashlib.sha1(f"blob {len(source)}\0".encode() + source).hexdigest()
    if blob != TARGET_BLOB_SHA:
        raise RuntimeError(f"source blob mismatch {blob} != {TARGET_BLOB_SHA}")
    if b"V1_54" not in source.splitlines()[0] or len(source.splitlines()) < 600:
        raise RuntimeError("v1.55 full file/import identity mismatch")
    receipt = {
        "status": "NO_DATA", "source_head": PARENT_HEAD,
        "target": TARGET_FILE, "source_blob": blob,
        "source_sha256": hashlib.sha256(source).hexdigest(),
        "source_line_count": len(source.splitlines()),
        "pins": pins, "import_build_exit": os.getenv("KUUOS_IMPORT_BUILD_EXIT"),
        "direct_v155_build_exit": os.getenv("KUUOS_V155_BUILD_EXIT"),
        "mcp_tools_called": False, "diagnostics_partial": None,
        "goal_status": "NO_DATA", "attempt_status": "NO_DATA",
        "certifies_parent_theorem": False, "certifies_chatgpt_tunnel": False,
        "no_source_edits": True,
    }
    try:
        env = {"LEAN_PROJECT_PATH": str(root), "LEAN_LOG_LEVEL": "NONE",
               "LEAN_MCP_DISABLED_TOOLS": DISABLED, "LEAN_MCP_SCRATCH_SLOTS": "1"}
        cmd = ["uvx", "--from", "lean-lsp-mcp==0.30.0",
               "lean-lsp-mcp", "--transport", "stdio"]
        client = MCPClient(cmd, cwd=root, env=env, timeout_seconds=240)
        try:
            initialized = client.request("initialize", {
                "protocolVersion": PROTOCOL_VERSION, "capabilities": {},
                "clientInfo": {"name": "KuuOS PR3522 V1.55", "version": "1"},
            })
            client.notify("notifications/initialized")
            tools = tool_map(client.request("tools/list"))
            need = {"lean_diagnostic_messages", "lean_goal", "lean_multi_attempt"}
            if not need.issubset(tools):
                raise RuntimeError(f"Lean tools missing: {need - set(tools)}")
            if "lean_run_code" in tools or "lean_build" in tools:
                raise RuntimeError("high effect tool unexpected")
            receipt["mcp_tools_called"] = True
            receipt["mcp_protocol"] = initialized.get("result", {}).get("protocolVersion")
            response = call_tool(client, "lean_diagnostic_messages", {
                "file_path": TARGET_FILE, "timeout_s": 120,
            })
            diag = structured(response)
            receipt["diagnostics_digest"] = sha(response.get("result", {}))
            receipt["diagnostics_partial"] = diag.get("partial")
            receipt["diagnostics_success"] = diag.get("success")
            receipt["diagnostics_model_keys"] = sorted(diag.keys())
            receipt["diagnostics_text_preview"] = extract_text(response)[:1800]
            receipt["failed_dependencies"] = diag.get("failed_dependencies")
            items = diag.get("items", [])
            if isinstance(items, list):
                receipt["diagnostics_count"] = len(items)
                receipt["diagnostics_first_20"] = [
                    {k: x.get(k) for k in ("severity", "message", "line", "column")}
                    for x in items[:20] if isinstance(x, Mapping)
                ]
            if not (diag or extract_text(response)):
                raise RuntimeError("diagnostics response empty")
            if not isinstance(diag.get("success"), bool):
                receipt["status"] = "DIAGNOSTICS_NO_TYPED_SUCCESS"
                raise RuntimeError("Lean MCP diagnostics returned no typed success value")
            if not isinstance(diag.get("partial"), bool):
                receipt["diagnostics_partial"] = "NO_DATA"
                raise RuntimeError("Lean MCP diagnostics returned no typed partial flag")
            if not isinstance(diag.get("success"), bool):
                receipt["status"] = "DIAGNOSTICS_NO_TYPED_SUCCESS"
            elif diag.get("partial") is True:
                receipt["status"] = "SEMANTIC_ELABORATION_PARTIAL"
            elif diag.get("failed_dependencies"):
                receipt["status"] = "IMPORT_DEPENDENCY_OBSTRUCTION"
            elif diag.get("success") is False:
                receipt["status"] = "SEMANTIC_DIAGNOSTICS_WITH_ERRORS"
            else:
                receipt["status"] = "SEMANTIC_DIAGNOSTICS_OBSERVED"
            if diag.get("partial") is False and not diag.get("failed_dependencies") and isinstance(diag.get("success"), bool):
                goal = call_tool(client, "lean_goal", {
                    "file_path": TARGET_FILE, "line": 269, "timeout_s": 90,
                })
                gm = structured(goal)
                receipt["goal_status"] = gm.get("status") or "NO_STATUS_FIELD"
                receipt["goal_keys"] = sorted(gm.keys())
                receipt["goal_digest"] = sha(goal.get("result", {}))
                attempts = call_tool(client, "lean_multi_attempt", {
                    "file_path": TARGET_FILE, "line": 269,
                    "snippets": ["exact hcomponent", "simpa using hcomponent", "assumption"],
                })
                am = structured(attempts)
                receipt["attempt_digest"] = sha(attempts.get("result", {}))
                receipt["attempt_count"] = len(am["items"]) if isinstance(am.get("items"), list) else None
                receipt["attempt_keys"] = sorted(am.keys())
                if receipt["attempt_count"] != 3:
                    receipt["attempt_status"] = "NO_DATA"
                    raise RuntimeError("Lean MCP did not return three structured tactic results")
                receipt["attempt_status"] = "responses_observed"
                receipt["attempt_summaries"] = [
                    {"snippet": x.get("snippet"), "proof_status": x.get("proof_status"),
                     "timed_out": x.get("timed_out"),
                     "errors": sum(1 for d in x.get("diagnostics", [])
                                   if d.get("severity") == "error")}
                    for x in am.get("items", []) if isinstance(x, Mapping)
                ]
        finally:
            client.close()
    except Exception as exc:
        receipt["probe_exception"] = f"{type(exc).__name__}: {str(exc)[:900]}"
        raise
    finally:
        pathlib.Path(args.receipt).write_text(
            json.dumps(receipt, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
        )
        print(json.dumps(receipt, indent=2, sort_keys=True, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
