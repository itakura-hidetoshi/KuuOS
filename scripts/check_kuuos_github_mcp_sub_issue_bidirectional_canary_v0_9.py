#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import tempfile
from typing import Any, Mapping

from runtime.kuuos_github_mcp_sub_issue_bidirectional_canary_v0_9 import (
    AUTHORITY_READY,
    CHILD_TITLE_PREFIX,
    CHILD_VERSION,
    CONFIRMATION,
    PLAN_VERSION,
    REQUEST_TITLE,
    REQUEST_VERSION,
    VERIFIED,
    build_github_mcp_sub_issue_bidirectional_canary,
)

BASE_SHA = "fb25c64fef34b6eeb38c97398c67465640b72261"
NONCE = "subissue-v09-check-001"
PARENT = 1901
CHILD = 1902
CHILD_ID = 91902
IMAGE = "ghcr.io/github/github-mcp-server@sha256:2b0c48b070f61e9d3969269ead600f62d00fb237b60ac849ef3d166ee7de9ad3"


def response(payload: Any, *, error: bool = False) -> dict[str, Any]:
    text = payload if isinstance(payload, str) else json.dumps(payload)
    return {
        "jsonrpc": "2.0",
        "id": 1,
        "result": {"isError": error, "content": [{"type": "text", "text": text}]},
    }


class MockTransport:
    def __init__(self) -> None:
        self.parent_children: list[dict[str, Any]] = []
        self.child: dict[str, Any] | None = None
        self.child_parent: dict[str, Any] | None = None

    def list_tools(self) -> dict[str, Any]:
        return {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "tools": [
                    {"name": "issue_write", "annotations": {"readOnlyHint": False}},
                    {"name": "issue_read", "annotations": {"readOnlyHint": True}},
                    {"name": "sub_issue_write", "annotations": {"readOnlyHint": False}},
                ]
            },
        }

    def call_tool(self, name: str, arguments: Mapping[str, Any]) -> dict[str, Any]:
        args = dict(arguments)
        if name == "issue_read" and args["method"] == "get":
            if args["issue_number"] == PARENT:
                return response(
                    {
                        "number": PARENT,
                        "title": REQUEST_TITLE,
                        "state": "open",
                        "body": json.dumps(
                            {
                                "version": REQUEST_VERSION,
                                "confirmation": CONFIRMATION,
                                "expected_main_sha": BASE_SHA,
                                "transaction_nonce": NONCE,
                                "server_image": IMAGE,
                            }
                        ),
                    }
                )
            return response(self.child)
        if name == "issue_read" and args["method"] == "get_sub_issues":
            return response(self.parent_children)
        if name == "issue_read" and args["method"] == "get_parent":
            return response({"parent": self.child_parent})
        if name == "issue_write" and args["method"] == "create":
            self.child = {
                "number": CHILD,
                "title": args["title"],
                "state": "open",
                "body": args["body"],
            }
            self.child_parent = None
            return response(
                {
                    "id": str(CHILD_ID),
                    "url": f"https://github.com/itakura-hidetoshi/KuuOS/issues/{CHILD}",
                }
            )
        if name == "sub_issue_write" and args["method"] == "add":
            assert self.child is not None
            self.parent_children = [
                {
                    "id": CHILD_ID,
                    "number": CHILD,
                    "title": self.child["title"],
                    "state": "open",
                }
            ]
            self.child_parent = {
                "number": PARENT,
                "title": REQUEST_TITLE,
                "state": "OPEN",
                "url": f"https://github.com/itakura-hidetoshi/KuuOS/issues/{PARENT}",
                "repository": "itakura-hidetoshi/KuuOS",
            }
            return response({"status": "added"})
        if name == "sub_issue_write" and args["method"] == "remove":
            self.parent_children = []
            self.child_parent = None
            return response({"status": "removed"})
        if name == "issue_write" and args["method"] == "update":
            assert self.child is not None
            self.child["state"] = "closed"
            return response(
                {
                    "id": str(CHILD_ID),
                    "url": f"https://github.com/itakura-hidetoshi/KuuOS/issues/{CHILD}",
                }
            )
        return response("unexpected", error=True)

    def close(self) -> None:
        pass


def plan() -> dict[str, Any]:
    return {
        "version": PLAN_VERSION,
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
        "parent_issue_number": PARENT,
        "request_issue_title": REQUEST_TITLE,
        "request_version_marker": REQUEST_VERSION,
        "child_title_prefix": CHILD_TITLE_PREFIX,
        "child_version_marker": CHILD_VERSION,
        "upward_read_method": "get_parent",
        "require_child_parent_preflight_absent": True,
        "require_child_parent_exact_when_attached": True,
        "require_child_parent_absent_after_remove": True,
        "server": {
            "kind": "official_github_mcp_server",
            "launcher": "docker",
            "image": IMAGE,
            "token_env": "GITHUB_PERSONAL_ACCESS_TOKEN",
            "toolsets": ["issues"],
            "tools": ["issue_write", "issue_read", "sub_issue_write"],
        },
    }


def authority() -> dict[str, Any]:
    return {
        "authority_status": AUTHORITY_READY,
        "plan_read_allowed": True,
        "tool_discovery_allowed": True,
        "external_action_allowed": True,
        "mcp_write_tool_call_allowed": True,
        "post_write_reobservation_allowed": True,
        "upward_parent_reobservation_allowed": True,
        "compensating_sub_issue_remove_allowed": True,
        "compensating_parent_reobservation_allowed": True,
        "compensating_child_close_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "github_mcp_sub_issue_bidirectional_canary_plan_v0_9.json").write_text(
            json.dumps(plan())
        )
        (
            root / "github_mcp_sub_issue_bidirectional_canary_authority_v0_9.json"
        ).write_text(json.dumps(authority()))
        transport = MockTransport()
        result = build_github_mcp_sub_issue_bidirectional_canary(
            runtime_context={
                "runtime_root": str(root),
                "github_mcp_sub_issue_bidirectional_canary_enabled": True,
                "apply_github_mcp_sub_issue_bidirectional_canary": True,
                "execute_external_actions": True,
                "confirmation": CONFIRMATION,
                "repository_full_name": "itakura-hidetoshi/KuuOS",
                "base_sha": BASE_SHA,
                "transaction_nonce": NONCE,
                "parent_issue_number": PARENT,
                "mode": "mock",
            },
            authority_packet=authority(),
            transport=transport,
        )
        assert result.status == VERIFIED, result.to_dict()
        assert result.child_parent_preflight_absent
        assert result.child_parent_added_verified
        assert result.child_parent_removed_verified
        assert result.binding_added_verified
        assert result.binding_removed_verified
        assert result.child_closed_verified
        assert not result.compensation_attempted
        assert transport.parent_children == []
        assert transport.child_parent is None
        assert transport.child and transport.child["state"] == "closed"
        print(json.dumps(result.to_dict(), ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
