#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import tempfile
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_github_actions_bounded_live_log_observer_v7_0 import (
    AUTHORITY_READY,
    BLOCKED,
    TERMINAL,
    build_qi_github_actions_bounded_live_log_observer,
)

BASE_SHA = "d580238d4c659a2e809162056dfb4da6fb0898c3"
IMAGE = "ghcr.io/github/github-mcp-server@sha256:" + ("a" * 64)


class MockTransport:
    def __init__(self, *, mismatch: bool = False) -> None:
        self.mismatch = mismatch
        self.run_calls = 0
        self.log_calls = 0
        self.calls: list[dict[str, Any]] = []

    def list_tools(self) -> dict[str, Any]:
        return {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "tools": [
                    {"name": "actions_get", "annotations": {"readOnlyHint": True}},
                    {"name": "actions_list", "annotations": {"readOnlyHint": True}},
                    {"name": "get_job_logs", "annotations": {"readOnlyHint": True}},
                ]
            },
        }

    @staticmethod
    def _response(payload: Any) -> dict[str, Any]:
        text = payload if isinstance(payload, str) else json.dumps(payload)
        return {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "isError": False,
                "content": [{"type": "text", "text": text}],
            },
        }

    def call_tool(self, name: str, arguments: Mapping[str, Any]) -> dict[str, Any]:
        args = dict(arguments)
        self.calls.append({"name": name, "arguments": args})
        if name == "actions_get":
            self.run_calls += 1
            status = "in_progress" if self.run_calls == 1 else "completed"
            return self._response(
                {
                    "id": 9001,
                    "head_sha": ("0" * 40) if self.mismatch else BASE_SHA,
                    "status": status,
                    "conclusion": None if status != "completed" else "success",
                }
            )
        if name == "actions_list":
            status = "in_progress" if self.run_calls == 1 else "completed"
            return self._response(
                {
                    "jobs": [
                        {
                            "id": 9101,
                            "name": "strict",
                            "status": status,
                            "conclusion": None if status != "completed" else "success",
                        }
                    ]
                }
            )
        if name == "get_job_logs":
            self.log_calls += 1
            if "tail_lines" not in args:
                return self._response("alpha\nbeta\ngamma\n")
            if self.log_calls == 1:
                return self._response("alpha\n")
            return self._response("alpha\nbeta\n")
        raise RuntimeError(f"unexpected_tool:{name}")

    def close(self) -> None:
        return None


def authority() -> dict[str, Any]:
    return {
        "authority_status": AUTHORITY_READY,
        "plan_read_allowed": True,
        "tool_discovery_allowed": True,
        "external_read_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def plan() -> dict[str, Any]:
    return {
        "version": "qi_github_actions_bounded_live_log_observer_plan_v7_0",
        "mode": "mock",
        "repository_full_name": "itakura-hidetoshi/KuuOS",
        "expected_head_sha": BASE_SHA,
        "run_id": 9001,
        "job_id": 0,
        "tail_lines": 500,
        "poll_attempts": 3,
        "poll_interval_seconds": 0,
        "terminal_full_log": True,
        "persist_delta_excerpt_chars": 2000,
        "read_only": True,
        "lockdown_mode": True,
        "server": {
            "kind": "official_github_mcp_server",
            "launcher": "docker",
            "image": IMAGE,
            "token_env": "GITHUB_PERSONAL_ACCESS_TOKEN",
            "toolsets": ["actions"],
            "tools": ["actions_get", "actions_list", "get_job_logs"],
        },
    }


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "runtime_root": str(root),
        "repository_full_name": "itakura-hidetoshi/KuuOS",
        "expected_head_sha": BASE_SHA,
        "qi_github_actions_bounded_live_log_observer_enabled": True,
        "apply_github_actions_bounded_live_log_observer": True,
        "execute_external_observations": True,
        "mode": "mock",
    }


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        (root / "qi_github_actions_bounded_live_log_plan_v7_0.json").write_text(
            json.dumps(plan()), encoding="utf-8"
        )
        transport = MockTransport()
        result = build_qi_github_actions_bounded_live_log_observer(
            runtime_context=ctx(root),
            authority_packet=authority(),
            transport=transport,
        )
        assert result.status == TERMINAL, result.to_dict()
        assert result.terminal_observed is True
        assert result.poll_count == 2
        assert result.selected_job_id == 9101
        assert result.run_conclusion == "success"
        assert result.latest_delta_excerpt == "beta\n"
        assert result.latest_log_digest
        assert result.final_log_digest
        assert result.blockers == []
        assert [c["name"] for c in transport.calls] == [
            "actions_get",
            "actions_list",
            "get_job_logs",
            "actions_get",
            "actions_list",
            "get_job_logs",
            "get_job_logs",
        ]
        receipt = json.loads(
            (root / "qi_github_actions_bounded_live_log_receipt_v7_0.json").read_text()
        )
        assert receipt["raw_logs_persisted"] is False
        assert "alpha" not in json.dumps(receipt)
        assert receipt["latest_delta_excerpt"] == "beta\n"

    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        (root / "qi_github_actions_bounded_live_log_plan_v7_0.json").write_text(
            json.dumps(plan()), encoding="utf-8"
        )
        transport = MockTransport(mismatch=True)
        result = build_qi_github_actions_bounded_live_log_observer(
            runtime_context=ctx(root),
            authority_packet=authority(),
            transport=transport,
        )
        assert result.status == BLOCKED, result.to_dict()
        assert "observed_run_head_sha_mismatch" in result.blockers
        assert [c["name"] for c in transport.calls] == ["actions_get"]

    print("PASS: KuuOS Qi GitHub Actions bounded live-log observer v7.0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
