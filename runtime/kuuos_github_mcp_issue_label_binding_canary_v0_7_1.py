#!/usr/bin/env python3
from __future__ import annotations

import html
import json
from typing import Any

from runtime import kuuos_github_mcp_issue_label_binding_canary_v0_7 as _base

PLAN_VERSION = _base.PLAN_VERSION
AUTHORITY_READY = _base.AUTHORITY_READY
CONFIRMATION = _base.CONFIRMATION
VERIFIED = _base.VERIFIED
COMPENSATED = _base.COMPENSATED
BLOCKED = _base.BLOCKED
GitHubMCPIssueLabelBindingCanaryResult = _base.GitHubMCPIssueLabelBindingCanaryResult


def _decode_observed_issue_body_once(value: Any) -> str:
    """Undo the single HTML-entity layer emitted by official issue_read."""
    return html.unescape(str(value))


def _issue_identity_blockers(
    *,
    observed: Any,
    issue_number: int,
    expected_title: str,
    expected_version: str,
    expected_confirmation: str,
    expected_base_sha: str,
    expected_nonce: str,
) -> list[str]:
    local: list[str] = []
    issue = _base._mapping(observed)
    if int(issue.get("number", 0) or 0) != issue_number:
        local.append("observed_issue_number_mismatch")
    if str(issue.get("title", "")) != expected_title:
        local.append("observed_issue_title_mismatch")
    if str(issue.get("state", "")).lower() != "open":
        local.append("observed_issue_state_not_open")

    body_text = _decode_observed_issue_body_once(issue.get("body", ""))
    try:
        body = json.loads(body_text)
    except json.JSONDecodeError:
        local.append("observed_issue_body_not_strict_json")
        return local
    if not isinstance(body, dict):
        local.append("observed_issue_body_not_object")
        return local

    expected_fields = {
        "version": expected_version,
        "confirmation": expected_confirmation,
        "expected_main_sha": expected_base_sha,
        "transaction_nonce": expected_nonce,
        "server_image": body.get("server_image"),
    }
    if set(body) != set(expected_fields):
        local.append("observed_issue_body_fields_invalid")
    for key, expected in expected_fields.items():
        if key == "server_image":
            if not _base._is_pinned_official_image(body.get(key, "")):
                local.append("observed_issue_server_image_not_pinned")
        elif body.get(key) != expected:
            local.append(f"observed_issue_{key}_mismatch")
    return local


# The base transaction resolves this helper through its module globals at call time.
# Installing the audited compatibility validator therefore leaves the transaction,
# receipt, compensation, and formal authority surfaces unchanged.
_base._issue_identity_blockers = _issue_identity_blockers
build_github_mcp_issue_label_binding_canary = (
    _base.build_github_mcp_issue_label_binding_canary
)
