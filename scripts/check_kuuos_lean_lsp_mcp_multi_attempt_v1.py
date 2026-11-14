#!/usr/bin/env python3
"""Live, bounded Lean-LSP MCP goal and tactic-trial proof of capability.

This is an MCP transport and semantic tool test, not a theorem certification.
Runs against a precompiled existing KuuOS file with the exact repository pins.
"""
from __future__ import annotations

import json
import os
import pathlib
from collections.abc import Mapping

from scripts.check_kuuos_lean_lsp_mcp_compatibility_v7_17 import (
    MCPClient,
    PROBE_FILE,
    PROTOCOL_VERSION,
    call_tool,
    extract_text,
    require_pins,
    sha,
    tool_map,
)

SERVER_COMMAND = [
    "uvx", "--from", "lean-lsp-mcp==0.30.0",
    "lean-lsp-mcp", "--transport", "stdio",
]
TRIAL_SNIPPETS = ["simp [transport]", "simp", "rfl"]
DISABLED_TOOLS = ",".join([
    "lean_run_code", "lean_build", "lean_profile_proof",
    "lean_minimal_hypotheses", "lean_leansearch", "lean_loogle",
    "lean_leanfinder", "lean_state_search", "lean_hammer_premise",
])


def _structured(response: Mapping) -> dict:
    value = response.get("result", {})
    if not isinstance(value, Mapping):
        return {}
    content = value.get("structuredContent", {})
    if isinstance(content, Mapping):
        return dict(content)
    return {}


def main() -> int:
    root = pathlib.Path.cwd().resolve()
    pins = require_pins(root)
    env = {
        "LEAN_PROJECT_PATH": str(root),
        "LEAN_LOG_LEVEL": "NONE",
        "LEAN_MCP_SCRATCH_SLOTS": "1",
        "LEAN_MCP_DISABLED_TOOLS": DISABLED_TOOLS,
    }
    client = MCPClient(SERVER_COMMAND, cwd=root, env=env, timeout_seconds=240)
    try:
        initialized = client.request("initialize", {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {},
            "clientInfo": {"name": "KuuOS Lean MCP Tactic Trial", "version": "1"},
        })
        client.notify("notifications/initialized")
        listed = client.request("tools/list")
        tools = tool_map(listed)
        required = {"lean_goal", "lean_multi_attempt", "lean_diagnostic_messages"}
        missing = sorted(required.difference(tools))
        if missing:
            raise RuntimeError("required_tools_missing:" + ",".join(missing))
        if "lean_run_code" in tools or "lean_build" in tools:
            raise RuntimeError("high_effect_tools_unexpectedly_enabled")

        # A real existing theorem whose line 38 is 'simp [transport]'.
        goal_response = call_tool(client, "lean_goal", {
            "file_path": PROBE_FILE, "line": 38,
        })
        trial_response = call_tool(client, "lean_multi_attempt", {
            "file_path": PROBE_FILE, "line": 38,
            "snippets": TRIAL_SNIPPETS,
        })

        goal_data = _structured(goal_response)
        trial_data = _structured(trial_response)
        goal_text = extract_text(goal_response)
        trial_text = extract_text(trial_response)
        if not (goal_data or goal_text.strip()):
            raise RuntimeError("lean_goal_empty_response")
        if not (trial_data or trial_text.strip()):
            raise RuntimeError("lean_multi_attempt_empty_response")

        raw_items = trial_data.get("items")
        if raw_items is not None and (
            not isinstance(raw_items, list) or len(raw_items) != len(TRIAL_SNIPPETS)
        ):
            raise RuntimeError("lean_multi_attempt_item_count_mismatch")

        receipt = {
            "version": "kuuos_lean_mcp_goal_trial_receipt_v1",
            "status": "KUUOS_LEAN_MCP_GOAL_AND_MULTI_ATTEMPT_CALLED",
            "host": "GitHub Actions local stdio; not ChatGPT tunnel",
            "checkout_source_sha": os.getenv("GITHUB_SHA") or None,
            "pins": pins,
            "test_file": PROBE_FILE,
            "test_line": 38,
            "attempt_snippets": TRIAL_SNIPPETS,
            "protocol_version": initialized.get("result", {}).get("protocolVersion"),
            "required_tools_present": True,
            "high_effect_tools_disabled": True,
            "goal_output_digest": sha(goal_response.get("result", {})),
            "trial_output_digest": sha(trial_response.get("result", {})),
            "trial_items_count": len(raw_items) if isinstance(raw_items, list) else None,
            "trial_structured_content_present": bool(trial_data),
            "mcp_tool_calls_succeeded": True,
            "validates_target_pr_3522": False,
            "validates_chatgpt_tunnel": False,
            "theorem_authority": False,
        }
        out = root / "kuuos_lean_mcp_goal_trial_receipt_v1.json"
        out.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(receipt, indent=2, sort_keys=True))
    finally:
        client.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
