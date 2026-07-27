#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import tempfile
from typing import Any, Mapping

from runtime.kuuos_github_mcp_issue_label_binding_canary_v0_7_2 import (
    AUTHORITY_READY,
    CONFIRMATION,
    LABEL_PREFIX,
    VERIFIED,
    build_github_mcp_issue_label_binding_canary,
)

BASE_SHA = "1cb3c4cceba77588403de9b8c1374bb93f1c9a0e"
NONCE = "binding-v07-check-001"
ISSUE_NUMBER = 1701
TITLE = "[KuuOS MCP Issue Label Binding Canary v0.7]"
VERSION = "kuuos_github_mcp_issue_label_binding_canary_request_v0_7"
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


class BindingCanaryMockTransport:
    def __init__(self) -> None:
        self.label: dict[str, Any] | None = None
        self.issue_labels: list[str] = []
        self.calls: list[dict[str, Any]] = []
        self.issue = {
            "number": ISSUE_NUMBER,
            "title": TITLE,
            "body": json.dumps(
                {
                    "version": VERSION,
                    "confirmation": CONFIRMATION,
                    "expected_main_sha": BASE_SHA,
                    "transaction_nonce": NONCE,
                    "server_image": IMAGE,
                }
            ),
            "state": "open",
        }

    def list_tools(self) -> dict[str, Any]:
        return {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "tools": [
                    {"name": "issue_write", "inputSchema": {"type": "object"}, "annotations": {"readOnlyHint": False}},
                    {"name": "issue_read", "inputSchema": {"type": "object"}, "annotations": {"readOnlyHint": True}},
                    {"name": "label_write", "inputSchema": {"type": "object"}, "annotations": {"readOnlyHint": False}},
                    {"name": "get_label", "inputSchema": {"type": "object"}, "annotations": {"readOnlyHint": True}},
                ]
            },
        }

    def call_tool(self, name: str, arguments: Mapping[str, Any]) -> dict[str, Any]:
        args = dict(arguments)
        self.calls.append({"name": name, "arguments": args})
        if name == "issue_read" and args.get("method") == "get":
            return _response(self.issue)
        if name == "issue_read" and args.get("method") == "get_labels":
            labels = [dict(self.label) for item in self.issue_labels if self.label and item == self.label["name"]]
            return _response({"labels": labels, "totalCount": len(labels)})
        if name == "get_label":
            if self.label is None:
                return _response(f"label '{args['name']}' not found", error=True)
            return _response(self.label)
        if name == "label_write" and args.get("method") == "create":
            self.label = {"name": args["name"], "color": args["color"], "description": args["description"]}
            return _response(f"label '{args['name']}' created successfully")
        if name == "issue_write" and args.get("method") == "update" and "labels" in args:
            self.issue_labels = list(args["labels"])
            return _response({"id": str(ISSUE_NUMBER), "url": f"https://github.com/itakura-hidetoshi/KuuOS/issues/{ISSUE_NUMBER}"})
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
            "version": "kuuos_github_mcp_issue_label_binding_canary_plan_v0_7",
            "mode": "mock",
            "repository_full_name": "itakura-hidetoshi/KuuOS",
            "base_branch": "main",
            "base_sha": BASE_SHA,
            "write_capable": True,
            "read_only": False,
            "lockdown_mode": True,
            "execute_external_actions": True,
            "confirmation": CONFIRMATION,
            "transaction_nonce": NONCE,
            "request_issue_number": ISSUE_NUMBER,
            "request_issue_title": TITLE,
            "request_version_marker": VERSION,
            "label_prefix": LABEL_PREFIX,
            "label_color": "0e8a16",
            "label_description_marker": "KUUOS_GITHUB_MCP_ISSUE_LABEL_BINDING_CANARY v0.7",
            "server": {
                "kind": "official_github_mcp_server",
                "launcher": "docker",
                "image": IMAGE,
                "token_env": "GITHUB_PERSONAL_ACCESS_TOKEN",
                "toolsets": ["issues", "labels"],
                "tools": ["issue_write", "issue_read", "label_write", "get_label"],
            },
        }
        authority = {
            "authority_status": AUTHORITY_READY,
            "plan_read_allowed": True,
            "tool_discovery_allowed": True,
            "external_action_allowed": True,
            "mcp_write_tool_call_allowed": True,
            "post_write_reobservation_allowed": True,
            "compensating_issue_detach_allowed": True,
            "compensating_label_delete_allowed": True,
            "receipt_write_allowed": True,
            "audit_append_allowed": True,
        }
        (root / "github_mcp_issue_label_binding_canary_plan_v0_7.json").write_text(json.dumps(plan))
        (root / "github_mcp_issue_label_binding_canary_authority_v0_7.json").write_text(json.dumps(authority))
        transport = BindingCanaryMockTransport()
        result = build_github_mcp_issue_label_binding_canary(
            runtime_context={
                "runtime_root": str(root),
                "github_mcp_issue_label_binding_canary_enabled": True,
                "apply_github_mcp_issue_label_binding_canary": True,
                "execute_external_actions": True,
                "confirmation": CONFIRMATION,
                "repository_full_name": "itakura-hidetoshi/KuuOS",
                "base_sha": BASE_SHA,
                "transaction_nonce": NONCE,
                "request_issue_number": ISSUE_NUMBER,
                "mode": "mock",
            },
            authority_packet=authority,
            transport=transport,
        )
        assert result.status == VERIFIED, result.to_dict()
        assert result.label_name == f"{LABEL_PREFIX}{NONCE}"
        assert len(result.label_name) <= 50
        assert result.issue_identity_verified is True
        assert result.issue_labels_preflight_empty is True
        assert result.label_preflight_absent is True
        assert result.label_created_verified is True
        assert result.label_attached_verified is True
        assert result.label_detached_verified is True
        assert result.label_deleted_verified is True
        assert result.compensation_attempted is False
        assert transport.issue_labels == []
        assert transport.label is None
        receipt = json.loads((root / "github_mcp_issue_label_binding_canary_receipt_v0_7.json").read_text())
        assert receipt["status"] == VERIFIED
        print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
