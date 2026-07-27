#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys

from runtime.kuuos_github_mcp_workflow_dispatch_v0_5 import (
    CONFIRMATION,
    VERIFIED,
    build_github_mcp_workflow_dispatch,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the authority-gated KuuOS GitHub MCP workflow dispatch v0.5."
    )
    parser.add_argument("runtime_root", type=pathlib.Path)
    parser.add_argument("--confirmation", required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--base-sha", required=True)
    parser.add_argument("--poll-attempts", type=int, default=8)
    parser.add_argument("--poll-interval-seconds", type=float, default=2.0)
    parser.add_argument("--execute-external-actions", action="store_true")
    args = parser.parse_args()

    root = args.runtime_root.expanduser().resolve()
    authority_path = root / "github_mcp_workflow_dispatch_authority_v0_5.json"
    if not authority_path.is_file():
        print(json.dumps({"status": "authority_packet_missing"}, sort_keys=True))
        return 2
    authority = json.loads(authority_path.read_text(encoding="utf-8"))

    result = build_github_mcp_workflow_dispatch(
        runtime_context={
            "runtime_root": str(root),
            "github_mcp_workflow_dispatch_enabled": True,
            "apply_github_mcp_workflow_dispatch": True,
            "execute_external_actions": args.execute_external_actions,
            "confirmation": args.confirmation,
            "repository_full_name": args.repository,
            "base_sha": args.base_sha,
            "poll_attempts": args.poll_attempts,
            "poll_interval_seconds": args.poll_interval_seconds,
            "mode": "stdio" if os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN") else "mock",
        },
        authority_packet=authority,
    )
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    if args.confirmation != CONFIRMATION:
        return 2
    return 0 if result.status == VERIFIED else 1


if __name__ == "__main__":
    sys.exit(main())
