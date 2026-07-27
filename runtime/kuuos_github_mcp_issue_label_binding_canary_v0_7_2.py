#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime import kuuos_github_mcp_issue_label_binding_canary_v0_7 as _base
from runtime.kuuos_github_mcp_issue_label_binding_canary_v0_7_1 import (
    AUTHORITY_READY,
    BLOCKED,
    COMPENSATED,
    CONFIRMATION,
    GitHubMCPIssueLabelBindingCanaryResult,
    PLAN_VERSION,
    VERIFIED,
)

LEGACY_LABEL_PREFIX = "kuuos-mcp-binding-canary-"
LABEL_PREFIX = "kuuos-mcp-bind-"
GITHUB_LABEL_NAME_MAX_LENGTH = 50

_base_validate_plan = _base._validate_plan


def _validate_plan(plan: Mapping[str, Any], blockers: list[str]) -> None:
    """Retain the v0.7 contract while enforcing GitHub's label-name bound."""
    normalized = dict(plan)
    prefix = str(plan.get("label_prefix", ""))
    if prefix == LABEL_PREFIX:
        normalized["label_prefix"] = LEGACY_LABEL_PREFIX
    _base_validate_plan(normalized, blockers)

    if prefix != LABEL_PREFIX:
        blockers.append("label_prefix_not_v0_7_2_bounded")
    nonce = str(plan.get("transaction_nonce", ""))
    if len(prefix + nonce) > GITHUB_LABEL_NAME_MAX_LENGTH:
        blockers.append("label_name_exceeds_github_limit")


# The base transaction resolves this helper through module globals at call time.
# Installing the bounded validator preserves the transaction and compensation logic.
_base._validate_plan = _validate_plan
build_github_mcp_issue_label_binding_canary = (
    _base.build_github_mcp_issue_label_binding_canary
)
