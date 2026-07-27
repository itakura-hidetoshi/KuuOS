#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import json
import os
from pathlib import Path
import time
from typing import Any, Mapping

from runtime import kuuos_github_mcp_sub_issue_chain_canary_v1_0 as _base

REOBSERVATION_VERSION = "kuuos_github_mcp_sub_issue_chain_reobservation_v1_0_1"
MAX_PARENT_READ_ATTEMPTS = 4
PARENT_READ_DELAY_SECONDS = 1.0


class BoundedParentReobservationTransport:
    def __init__(
        self,
        inner: _base.MCPTransport,
        *,
        max_attempts: int = MAX_PARENT_READ_ATTEMPTS,
        delay_seconds: float = PARENT_READ_DELAY_SECONDS,
    ) -> None:
        self.inner = inner
        self.max_attempts = max(1, int(max_attempts))
        self.delay_seconds = max(0.0, float(delay_seconds))
        self.expected_parent_presence: bool | None = None
        self.records: list[dict[str, Any]] = []

    def list_tools(self) -> dict[str, Any]:
        return self.inner.list_tools()

    def call_tool(
        self,
        name: str,
        arguments: Mapping[str, Any],
    ) -> dict[str, Any]:
        args = dict(arguments)
        if name == "sub_issue_write":
            response = self.inner.call_tool(name, args)
            method = str(args.get("method", ""))
            if method == "add":
                self.expected_parent_presence = True
            elif method == "remove":
                self.expected_parent_presence = False
            return response

        if not (
            name == "issue_read"
            and str(args.get("method", "")) == "get_parent"
            and self.expected_parent_presence is not None
        ):
            return self.inner.call_tool(name, args)

        final_response: dict[str, Any] = {}
        expected_present = self.expected_parent_presence
        for attempt in range(1, self.max_attempts + 1):
            response = dict(self.inner.call_tool(name, args))
            observed = _base.norm(response)
            parent = _base.m(observed).get("parent")
            matched = (parent is not None) if expected_present else (parent is None)
            phase = (
                "bounded_parent_present_reobservation"
                if expected_present
                else "bounded_parent_absent_reobservation"
            )
            self.records.append(
                _base.rec(
                    f"{phase}_attempt_{attempt}",
                    name,
                    args,
                    response,
                    observed,
                    "verified" if matched else "retry",
                    [],
                )
            )
            final_response = response
            if matched:
                return response
            if attempt < self.max_attempts and self.delay_seconds:
                time.sleep(self.delay_seconds)
        return final_response

    def close(self) -> None:
        self.inner.close()


def build_github_mcp_sub_issue_chain_canary(
    *,
    runtime_context: Mapping[str, Any],
    authority_packet: Mapping[str, Any],
    transport: _base.MCPTransport | None = None,
    max_attempts: int = MAX_PARENT_READ_ATTEMPTS,
    delay_seconds: float = PARENT_READ_DELAY_SECONDS,
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

    wrapped = BoundedParentReobservationTransport(
        inner,
        max_attempts=max_attempts,
        delay_seconds=delay_seconds,
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
    merged_warnings = sorted(
        set(result.warnings + [f"parent_reobservation_policy:{max_attempts}_attempts"])
    )
    result = replace(
        result,
        records=merged_records,
        warnings=merged_warnings,
    )

    if authority_packet.get("receipt_write_allowed") is True:
        receipt = root / "github_mcp_sub_issue_chain_canary_receipt_v1_0.json"
        receipt.write_text(
            json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True)
            + "\n",
            encoding="utf-8",
        )
    if authority_packet.get("audit_append_allowed") is True:
        audit = root / "github_mcp_sub_issue_chain_canary_audit_v1_0.jsonl"
        audit.write_text(
            "".join(
                json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n"
                for record in merged_records
            ),
            encoding="utf-8",
        )
    return result


CONFIRMATION = _base.CONFIRMATION
VERIFIED = _base.VERIFIED
