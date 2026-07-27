#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime import kuuos_github_mcp_sub_issue_chain_reobservation_v1_0_1 as _v101
from runtime import kuuos_github_mcp_sub_issue_chain_canary_v1_0 as _base

REOBSERVATION_VERSION = "kuuos_github_mcp_sub_issue_chain_reobservation_v1_0_2"
MAX_PARENT_READ_ATTEMPTS = 30
PARENT_READ_DELAY_SECONDS = 2.0


def build_github_mcp_sub_issue_chain_canary(
    *,
    runtime_context: Mapping[str, Any],
    authority_packet: Mapping[str, Any],
    transport: _base.MCPTransport | None = None,
    max_attempts: int = MAX_PARENT_READ_ATTEMPTS,
    delay_seconds: float = PARENT_READ_DELAY_SECONDS,
) -> _base.GitHubMCPSubIssueChainCanaryResult:
    """Run v1.0 with an exact, bounded 60-second nested-parent read window.

    The final exact parent and absence checks remain owned by the v1.0 runtime.
    Exhaustion still returns the final stale observation and fails closed.
    """
    return _v101.build_github_mcp_sub_issue_chain_canary(
        runtime_context=runtime_context,
        authority_packet=authority_packet,
        transport=transport,
        max_attempts=max_attempts,
        delay_seconds=delay_seconds,
    )


CONFIRMATION = _base.CONFIRMATION
VERIFIED = _base.VERIFIED
