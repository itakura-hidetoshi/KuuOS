#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import tempfile
from typing import Any, Mapping

from runtime.kuuos_github_mcp_label_canary_v0_6 import (
    AUTHORITY_READY,
    CONFIRMATION,
    VERIFIED,
    build_github_mcp_label_canary,
)

BASE_SHA = "45ace8b96a3e57a5f01910837ee14083fb784170"
NONCE = "label-v06-check-001"
IMAGE = "ghcr.io/github/github-mcp-server@sha256:2b0c48b070f61e9d3969269ead600f62d00fb237b60ac849ef3d166ee7de9ad3"


def _response(payload: Any, *, error: bool = False) -> dict[str, Any]:
    text = payload if isinstance(payload, str) else json.dumps(payload)
    return {
        "jsonrpc": "2.0",
        "id": 1,
        "result": {
            "isError": error,
            "content": [{"type": "text", "text": text}],
        },
    }


class LabelCanaryMockTransport:
    def __init__(self) -> None:
        self.label: dict[str, Any] | None = None
        self.calls: list[dict[str, Any]] = []

    def list_tools(self) -> dict[str, Any]:
        return {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "tools": [
                    {
                        "name": "label_write",
                        "inputSchema": {"type": "object"},
                        "annotations": {
                            "readOnlyHint": False,
                            "destructiveHint": True,
                        },
                    },
                    {
                        "name": "get_label",
                        "inputSchema": {"type": "object"},
                        "annotations": {"readOnlyHint": True},
                    },
                ]
            },
        }

    def call_tool(self, name: str, arguments: Mapping[str, Any]) -> dict[str, Any]:
        args = dict(arguments)
        self.calls.append({"name": name, "arguments": args})
        if name == "get_label":
            if self.label is None:
                return _response(
                    f"label '{args['name']}' not found in {args['owner']}/{args['repo']}",
                    error=True,
                )
            return _response(self.label)
        if name == "label_write" and args.get("method") == "create":
            self.label = {
                "name": args["name"],
                "color": args["color"],
                "description": args["description"],
            }
            return _response(f"label '{args['name']}' created successfully")
        if name == "label_write" and args.get("method") == "delete":
            self.label = None
            return _response(f"label '{args['name']}' deleted successfully")
        return _response("unexpected tool", error=True)

    def close(self) -> None:
        return None


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        plan = {
            "version": "kuuos_github_mcp_label_canary_plan_v0_6",
            "mode": "mock",
            "repository_full_name": "itakura-hidetoshi/KuuOS",
            "base_branch": "main",
            "base_sha": BASE_SHA,
            "write_capable": True,
            "read_only": False,
            "lockdown_mode": True,
            "execute_external_actions": True,
            "confirmation": CONFIRMATION,
            "label_nonce": NONCE,
            "label_prefix": "kuuos-mcp-canary-",
            "label_color": "5319e7",
            "description_marker": "KUUOS_GITHUB_MCP_LABEL_CANARY v0.6",
            "server": {
                "kind": "official_github_mcp_server",
                "launcher": "docker",
                "image": IMAGE,
                "token_env": "GITHUB_PERSONAL_ACCESS_TOKEN",
                "toolsets": ["labels"],
                "tools": ["label_write", "get_label"],
            },
        }
        authority = {
            "authority_status": AUTHORITY_READY,
            "plan_read_allowed": True,
            "tool_discovery_allowed": True,
            "external_action_allowed": True,
            "mcp_write_tool_call_allowed": True,
            "post_write_reobservation_allowed": True,
            "compensating_delete_allowed": True,
            "receipt_write_allowed": True,
            "audit_append_allowed": True,
        }
        (root / "github_mcp_label_canary_plan_v0_6.json").write_text(
            json.dumps(plan), encoding="utf-8"
        )
        (root / "github_mcp_label_canary_authority_v0_6.json").write_text(
            json.dumps(authority), encoding="utf-8"
        )
        transport = LabelCanaryMockTransport()
        result = build_github_mcp_label_canary(
            runtime_context={
                "runtime_root": str(root),
                "github_mcp_label_canary_enabled": True,
                "apply_github_mcp_label_canary": True,
                "execute_external_actions": True,
                "confirmation": CONFIRMATION,
                "repository_full_name": "itakura-hidetoshi/KuuOS",
                "base_sha": BASE_SHA,
                "label_nonce": NONCE,
                "mode": "mock",
            },
            authority_packet=authority,
            transport=transport,
        )
        assert result.status == VERIFIED, result.to_dict()
        assert result.preflight_absent is True
        assert result.created_verified is True
        assert result.deleted_verified is True
        assert result.compensation_attempted is False
        assert transport.label is None
        assert [call["name"] for call in transport.calls] == [
            "get_label",
            "label_write",
            "get_label",
            "label_write",
            "get_label",
        ]
        receipt = json.loads(
            (root / "github_mcp_label_canary_receipt_v0_6.json").read_text()
        )
        assert receipt["status"] == VERIFIED
        print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
