#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib

from runtime.kuuos_github_mcp_server_bridge_v0_1 import build_github_mcp_server_bridge


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the bounded KuuOS bridge to GitHub's official MCP Server."
    )
    parser.add_argument("runtime_root", help="Directory containing the plan and authority JSON files.")
    parser.add_argument(
        "--execute-external-actions",
        action="store_true",
        help="Enable the runtime half of the write gate. The plan, authority, and operation gates must also pass.",
    )
    args = parser.parse_args()
    root = pathlib.Path(args.runtime_root).expanduser().resolve()
    authority_path = root / "github_mcp_server_bridge_authority.json"
    try:
        authority = json.loads(authority_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "authority_read_failed", "error": str(exc)}, indent=2))
        return 2
    result = build_github_mcp_server_bridge(
        runtime_context={
            "runtime_root": str(root),
            "github_mcp_server_bridge_enabled": True,
            "apply_github_mcp_server_bridge": True,
            "execute_external_actions": bool(args.execute_external_actions),
        },
        authority_packet=authority,
    )
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.status in {
        "KUUOS_GITHUB_MCP_BRIDGE_APPLIED",
        "KUUOS_GITHUB_MCP_BRIDGE_IDLE",
    } else 1


if __name__ == "__main__":
    raise SystemExit(main())
