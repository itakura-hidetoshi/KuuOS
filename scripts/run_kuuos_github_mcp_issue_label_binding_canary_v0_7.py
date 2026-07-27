#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys

from runtime.kuuos_github_mcp_issue_label_binding_canary_v0_7_2 import (
    CONFIRMATION,
    VERIFIED,
    build_github_mcp_issue_label_binding_canary,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the reversible KuuOS GitHub MCP Issue-Label binding canary v0.7.2."
    )
    parser.add_argument("runtime_root", type=pathlib.Path)
    parser.add_argument("--confirmation", required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--base-sha", required=True)
    parser.add_argument("--transaction-nonce", required=True)
    parser.add_argument("--request-issue-number", type=int, required=True)
    parser.add_argument("--resolved-image-digest", default="")
    parser.add_argument("--execute-external-actions", action="store_true")
    args = parser.parse_args()

    root = args.runtime_root.expanduser().resolve()
    authority_path = root / "github_mcp_issue_label_binding_canary_authority_v0_7.json"
    if not authority_path.is_file():
        print(json.dumps({"status": "authority_packet_missing"}, sort_keys=True))
        return 2
    authority = json.loads(authority_path.read_text(encoding="utf-8"))

    result = build_github_mcp_issue_label_binding_canary(
        runtime_context={
            "runtime_root": str(root),
            "github_mcp_issue_label_binding_canary_enabled": True,
            "apply_github_mcp_issue_label_binding_canary": True,
            "execute_external_actions": args.execute_external_actions,
            "confirmation": args.confirmation,
            "repository_full_name": args.repository,
            "base_sha": args.base_sha,
            "transaction_nonce": args.transaction_nonce,
            "request_issue_number": args.request_issue_number,
            "resolved_image_digest": args.resolved_image_digest,
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
