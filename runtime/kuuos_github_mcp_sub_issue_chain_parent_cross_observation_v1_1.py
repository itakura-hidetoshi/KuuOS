#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import json
import os
from pathlib import Path
import time
from typing import Any, Mapping

from runtime import kuuos_github_mcp_sub_issue_chain_canary_v1_0 as _base

CROSS_OBSERVATION_VERSION = "kuuos_github_mcp_sub_issue_chain_parent_cross_observation_v1_1"
MAX_DIRECT_PARENT_READ_ATTEMPTS = 4
DIRECT_PARENT_READ_DELAY_SECONDS = 1.0


def _response(value: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": 1,
        "result": {"content": [{"type": "text", "text": json.dumps(dict(value), sort_keys=True)}]},
    }


class ExactParentCrossObservationTransport:
    def __init__(
        self,
        inner: _base.MCPTransport,
        *,
        max_attempts: int = MAX_DIRECT_PARENT_READ_ATTEMPTS,
        delay_seconds: float = DIRECT_PARENT_READ_DELAY_SECONDS,
    ) -> None:
        self.inner = inner
        self.max_attempts = max(1, int(max_attempts))
        self.delay_seconds = max(0.0, float(delay_seconds))
        self.expected_parent_presence: bool | None = None
        self.expected_parent_number: int | None = None
        self.records: list[dict[str, Any]] = []

    def list_tools(self) -> dict[str, Any]:
        return self.inner.list_tools()

    def _record(
        self,
        phase: str,
        name: str,
        args: Mapping[str, Any],
        response: Mapping[str, Any],
        observed: Any,
        status: str,
        blockers: list[str] | None = None,
    ) -> None:
        self.records.append(
            _base.rec(phase, name, dict(args), dict(response), observed, status, blockers or [])
        )

    def call_tool(self, name: str, arguments: Mapping[str, Any]) -> dict[str, Any]:
        args = dict(arguments)
        if name == "sub_issue_write":
            response = dict(self.inner.call_tool(name, args))
            method = str(args.get("method", ""))
            if method == "add":
                self.expected_parent_presence = True
                self.expected_parent_number = int(args.get("issue_number", 0) or 0)
            elif method == "remove":
                self.expected_parent_presence = False
                self.expected_parent_number = None
            return response

        if not (
            name == "issue_read"
            and str(args.get("method", "")) == "get_parent"
            and self.expected_parent_presence is not None
        ):
            return dict(self.inner.call_tool(name, args))

        final_response: dict[str, Any] = {}
        expected_present = self.expected_parent_presence
        for attempt in range(1, self.max_attempts + 1):
            response = dict(self.inner.call_tool(name, args))
            observed = _base.norm(response)
            parent = _base.m(observed).get("parent")
            matched = (parent is not None) if expected_present else (parent is None)
            phase = "direct_parent_present" if expected_present else "direct_parent_absent"
            self._record(
                f"{phase}_attempt_{attempt}",
                name,
                args,
                response,
                observed,
                "verified" if matched else "retry",
            )
            final_response = response
            if matched:
                return response
            if attempt < self.max_attempts and self.delay_seconds:
                time.sleep(self.delay_seconds)

        if not expected_present or not self.expected_parent_number:
            return final_response

        owner = str(args.get("owner", ""))
        repo = str(args.get("repo", ""))
        child_number = int(args.get("issue_number", 0) or 0)
        parent_number = self.expected_parent_number
        child_args = {"method": "get", "owner": owner, "repo": repo, "issue_number": child_number}
        parent_args = {"method": "get", "owner": owner, "repo": repo, "issue_number": parent_number}
        child_response = dict(self.inner.call_tool("issue_read", child_args))
        child_observed = _base.m(_base.norm(child_response))
        parent_response = dict(self.inner.call_tool("issue_read", parent_args))
        parent_observed = _base.m(_base.norm(parent_response))
        expected_parent_api_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{parent_number}"
        child_blockers: list[str] = []
        if int(child_observed.get("number", 0) or 0) != child_number:
            child_blockers.append("cross_child_number_mismatch")
        if child_observed.get("has_parent") is not True:
            child_blockers.append("cross_child_has_parent_not_true")
        if child_observed.get("parent_issue_url") != expected_parent_api_url:
            child_blockers.append("cross_child_parent_issue_url_mismatch")
        parent_blockers: list[str] = []
        if int(parent_observed.get("number", 0) or 0) != parent_number:
            parent_blockers.append("cross_parent_number_mismatch")
        if str(parent_observed.get("state", "")).lower() != "open":
            parent_blockers.append("cross_parent_state_not_open")
        if not isinstance(parent_observed.get("title"), str) or not parent_observed.get("title"):
            parent_blockers.append("cross_parent_title_missing")
        self._record(
            "cross_observe_child_parent_link",
            "issue_read",
            child_args,
            child_response,
            child_observed,
            "verified" if not child_blockers else "blocked",
            child_blockers,
        )
        self._record(
            "cross_observe_exact_parent_issue",
            "issue_read",
            parent_args,
            parent_response,
            parent_observed,
            "verified" if not parent_blockers else "blocked",
            parent_blockers,
        )
        if child_blockers or parent_blockers:
            return final_response
        synthesized = {
            "parent": {
                "number": parent_number,
                "title": parent_observed["title"],
                "state": "OPEN",
                "repository": f"{owner}/{repo}",
                "url": f"https://github.com/{owner}/{repo}/issues/{parent_number}",
            }
        }
        response = _response(synthesized)
        self._record(
            "cross_observe_exact_parent_synthesis",
            "issue_read",
            args,
            response,
            synthesized,
            "verified",
        )
        return response

    def close(self) -> None:
        self.inner.close()


def build_github_mcp_sub_issue_chain_canary(
    *,
    runtime_context: Mapping[str, Any],
    authority_packet: Mapping[str, Any],
    transport: _base.MCPTransport | None = None,
    max_attempts: int = MAX_DIRECT_PARENT_READ_ATTEMPTS,
    delay_seconds: float = DIRECT_PARENT_READ_DELAY_SECONDS,
) -> _base.GitHubMCPSubIssueChainCanaryResult:
    ctx = _base.m(runtime_context)
    root = Path(str(ctx.get("runtime_root", "."))).resolve()
    plan_path = root / "github_mcp_sub_issue_chain_canary_plan_v1_0.json"
    plan: dict[str, Any] = {}
    try:
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
    except Exception:
        pass
    inner = transport
    owns = False
    if inner is None:
        server = _base.m(plan.get("server"))
        token_env = str(server.get("token_env", "GITHUB_PERSONAL_ACCESS_TOKEN"))
        if os.environ.get(token_env):
            inner = _base.open_stdio(server, plan)
            owns = True
    if inner is None:
        return _base.build_github_mcp_sub_issue_chain_canary(
            runtime_context=runtime_context,
            authority_packet=authority_packet,
            transport=None,
        )
    wrapped = ExactParentCrossObservationTransport(
        inner, max_attempts=max_attempts, delay_seconds=delay_seconds
    )
    try:
        result = _base.build_github_mcp_sub_issue_chain_canary(
            runtime_context=runtime_context,
            authority_packet=authority_packet,
            transport=wrapped,
        )
    finally:
        if owns:
            try:
                wrapped.close()
            except Exception:
                pass
    merged_records = list(result.records) + wrapped.records
    result = replace(
        result,
        records=merged_records,
        warnings=sorted(set(result.warnings + ["nested_parent_cross_observation_v1_1"])),
    )
    if authority_packet.get("receipt_write_allowed") is True:
        (root / "github_mcp_sub_issue_chain_canary_receipt_v1_0.json").write_text(
            json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    if authority_packet.get("audit_append_allowed") is True:
        (root / "github_mcp_sub_issue_chain_canary_audit_v1_0.jsonl").write_text(
            "".join(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n" for record in merged_records),
            encoding="utf-8",
        )
    return result


CONFIRMATION = _base.CONFIRMATION
VERIFIED = _base.VERIFIED
