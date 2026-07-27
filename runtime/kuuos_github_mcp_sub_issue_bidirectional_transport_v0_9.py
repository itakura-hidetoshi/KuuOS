#!/usr/bin/env python3
from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Mapping

from runtime import kuuos_github_mcp_sub_issue_binding_canary_v0_8 as _base
from runtime.kuuos_github_mcp_sub_issue_bidirectional_contract_v0_9 import (
    AUTHORITY_READY,
    BLOCKED,
    CHILD_TITLE_PREFIX,
    CHILD_VERSION,
    COMPENSATED,
    CONFIRMATION,
    PLAN_VERSION,
    REQUEST_TITLE,
    REQUEST_VERSION,
    VERIFIED,
    parent_absent_blockers,
    parent_exact_blockers,
)


def error_response(message: str) -> dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": 1,
        "result": {
            "isError": True,
            "content": [{"type": "text", "text": message}],
        },
    }


class BidirectionalTransport:
    def __init__(
        self,
        inner: _base.MCPTransport,
        *,
        repository_full_name: str,
        parent_issue_number: int,
    ) -> None:
        self.inner = inner
        self.repository_full_name = repository_full_name
        self.parent_issue_number = parent_issue_number
        self.owner, self.repo = repository_full_name.split("/", 1)
        self.child_issue_number = 0
        self.stage = "initial"
        self.child_parent_preflight_absent = False
        self.child_parent_added_verified = False
        self.child_parent_removed_verified = False
        self.compensation_child_parent_removed = False
        self.extra_records: dict[str, dict[str, Any]] = {}
        self.extra_blockers: list[str] = []

    def list_tools(self) -> dict[str, Any]:
        return self.inner.list_tools()

    def close(self) -> None:
        self.inner.close()

    def _parent_args(self) -> dict[str, Any]:
        return {
            "method": "get_parent",
            "owner": self.owner,
            "repo": self.repo,
            "issue_number": self.child_issue_number,
        }

    def _check_parent(
        self,
        *,
        phase: str,
        expect_parent: bool,
        status_ok: str,
    ) -> bool:
        arguments = self._parent_args()
        try:
            response = self.inner.call_tool("issue_read", arguments)
        except Exception as exc:
            response = {"error": f"{type(exc).__name__}:{exc}"}
            observed: Any = {}
            local = [f"{phase}_tool_exception"]
        else:
            local: list[str] = []
            observed = {}
            if _base._tool_returned_error(response):
                local.append(f"{phase}_tool_returned_error")
            else:
                observed = _base._normalize_tool_payload(response)
                if expect_parent:
                    local += parent_exact_blockers(
                        observed,
                        parent_issue_number=self.parent_issue_number,
                        parent_title=REQUEST_TITLE,
                        repository_full_name=self.repository_full_name,
                    )
                else:
                    local += parent_absent_blockers(observed)
        self.extra_records[phase] = _base._record(
            phase=phase,
            tool="issue_read",
            arguments=arguments,
            response=response,
            observed=observed,
            status=status_ok if not local else "blocked",
            blockers=local,
        )
        self.extra_blockers.extend(local)
        return not local

    def call_tool(self, name: str, arguments: Mapping[str, Any]) -> dict[str, Any]:
        args = dict(arguments)
        response = self.inner.call_tool(name, args)

        if (
            name == "issue_write"
            and args.get("method") == "create"
            and not _base._tool_returned_error(response)
        ):
            observed = _base._normalize_tool_payload(response)
            _, child_number, _ = _base._extract_created_child(observed)
            self.child_issue_number = child_number
            self.stage = "child_created"
            return response

        if (
            name == "issue_read"
            and args.get("method") == "get"
            and int(args.get("issue_number", 0) or 0) == self.child_issue_number
            and self.child_issue_number > 0
            and self.stage == "child_created"
            and not _base._tool_returned_error(response)
        ):
            ok = self._check_parent(
                phase="verify_child_parent_preflight_absent",
                expect_parent=False,
                status_ok="verified_absent",
            )
            self.child_parent_preflight_absent = ok
            self.stage = (
                "child_parent_preflight_checked"
                if ok
                else "preflight_check_failed"
            )
            return (
                response
                if ok
                else error_response("bidirectional_child_parent_preflight_failed")
            )

        if name == "sub_issue_write" and args.get("method") == "add":
            if not _base._tool_returned_error(response):
                self.stage = "added"
            return response

        if (
            name == "issue_read"
            and args.get("method") == "get_sub_issues"
            and self.stage == "added"
            and not _base._tool_returned_error(response)
        ):
            ok = self._check_parent(
                phase="verify_child_parent_added",
                expect_parent=True,
                status_ok="verified",
            )
            self.child_parent_added_verified = ok
            self.stage = "added_checked" if ok else "added_check_failed"
            return (
                response
                if ok
                else error_response("bidirectional_child_parent_add_check_failed")
            )

        if name == "sub_issue_write" and args.get("method") == "remove":
            self.stage = (
                "removed"
                if self.stage == "added_checked"
                else "compensation_removed"
            )
            return response

        if (
            name == "issue_read"
            and args.get("method") == "get_sub_issues"
            and self.stage == "removed"
            and not _base._tool_returned_error(response)
        ):
            ok = self._check_parent(
                phase="verify_child_parent_removed",
                expect_parent=False,
                status_ok="verified_absent",
            )
            self.child_parent_removed_verified = ok
            self.stage = "removed_checked" if ok else "removed_check_failed"
            return (
                response
                if ok
                else error_response("bidirectional_child_parent_remove_check_failed")
            )

        if (
            name == "issue_read"
            and args.get("method") == "get_sub_issues"
            and self.stage == "compensation_removed"
            and not _base._tool_returned_error(response)
        ):
            ok = self._check_parent(
                phase="verify_compensation_child_parent_removed",
                expect_parent=False,
                status_ok="verified_absent",
            )
            self.compensation_child_parent_removed = ok
            self.stage = (
                "compensation_checked"
                if ok
                else "compensation_check_failed"
            )
            return (
                response
                if ok
                else error_response("bidirectional_compensation_parent_check_failed")
            )

        return response


PATCHED_CONSTANTS = {
    "PLAN_VERSION": PLAN_VERSION,
    "REQUEST_VERSION": REQUEST_VERSION,
    "CHILD_VERSION": CHILD_VERSION,
    "AUTHORITY_READY": AUTHORITY_READY,
    "CONFIRMATION": CONFIRMATION,
    "VERIFIED": VERIFIED,
    "COMPENSATED": COMPENSATED,
    "BLOCKED": BLOCKED,
    "REQUEST_TITLE": REQUEST_TITLE,
    "CHILD_TITLE_PREFIX": CHILD_TITLE_PREFIX,
}


@contextmanager
def patched_base_constants():
    previous = {name: getattr(_base, name) for name in PATCHED_CONSTANTS}
    for name, value in PATCHED_CONSTANTS.items():
        setattr(_base, name, value)
    try:
        yield
    finally:
        for name, value in previous.items():
            setattr(_base, name, value)


def merge_records(
    records: list[dict[str, Any]],
    extras: Mapping[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    after = {
        "verify_child_created": "verify_child_parent_preflight_absent",
        "verify_sub_issue_binding_added": "verify_child_parent_added",
        "verify_sub_issue_binding_removed": "verify_child_parent_removed",
        "verify_compensation_binding_removed":
            "verify_compensation_child_parent_removed",
    }
    merged: list[dict[str, Any]] = []
    inserted: set[str] = set()
    for record in records:
        merged.append(dict(record))
        phase = after.get(str(record.get("phase", "")))
        if phase and phase in extras:
            merged.append(dict(extras[phase]))
            inserted.add(phase)
    for phase, record in extras.items():
        if phase not in inserted:
            merged.append(dict(record))
    return merged
