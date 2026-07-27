#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib

from runtime.kuuos_github_mcp_live_write_verification_v0_3 import (
    build_github_mcp_live_write_verification,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Execute an authority-gated GitHub MCP write transaction and verify its "
            "observable GitHub effect through a read-only MCP tool."
        )
    )
    parser.add_argument(
        "runtime_root",
        help="Directory containing the v0.3 plan and authority JSON files.",
    )
    parser.add_argument(
        "--execute-external-actions",
        action="store_true",
        help=(
            "Enable the runtime write gate. The plan, authority, repository, base SHA, "
            "operation approval, and post-write verification gates must also pass."
        ),
    )
    args = parser.parse_args()
    root = pathlib.Path(args.runtime_root).expanduser().resolve()
    authority_path = root / "github_mcp_live_write_verification_authority_v0_3.json"
    try:
        authority = json.loads(authority_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "authority_read_failed", "error": str(exc)}, indent=2))
        return 2

    result = build_github_mcp_live_write_verification(
        runtime_context={
            "runtime_root": str(root),
            "github_mcp_live_write_verification_enabled": True,
            "apply_github_mcp_live_write_verification": True,
            "execute_external_actions": bool(args.execute_external_actions),
        },
        authority_packet=authority,
    )
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.status in {
        "KUUOS_GITHUB_MCP_LIVE_WRITE_VERIFIED",
        "KUUOS_GITHUB_MCP_LIVE_WRITE_VERIFICATION_IDLE",
    } else 1


if __name__ == "__main__":
    raise SystemExit(main())
