"""GitHub signature/authenticity intake for future KuuOS MCP Events publication.

This module does not register an HTTP route, publish an event, or send webhooks.
It validates an exact raw GitHub webhook body with a configured secret and
produces a non-authoritative wake-up packet. A durable outbox and independent
GitHub MCP re-observation are required before Dots delivery and certification.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import re
from dataclasses import dataclass
from typing import Any, Mapping

from .github_event_contract import (
    EventContractError, compile_ci_completed, compile_pr_head_updated,
)

MAX_GITHUB_EVENT_BODY = 262_144
_SIGNATURE = re.compile(r"^sha256=[a-f0-9]{64}$")
_DELIVERY_ID = re.compile(r"^[A-Za-z0-9-]{16,96}$")


class GitHubIngressError(ValueError):
    """Sanitized intake failure category; no raw body or secret in exceptions."""


@dataclass(frozen=True)
class VerifiedGitHubWakeup:
    delivery_id: str
    source_kind: str
    event_id: str
    repository: str
    head_sha: str
    packet: dict[str, Any]

    def public_receipt(self) -> dict[str, Any]:
        data = self.packet["data"]
        return {
            "event_id": self.event_id,
            "delivery_id": self.delivery_id,
            "source_event": self.source_kind,
            "repository": self.repository,
            "head_sha": self.head_sha,
            "run_id": data.get("run_id"),
            "pr_number": data.get("pr_number"),
            "github_transport_signature_verified": True,
            "signal_is_success_evidence": False,
            "fresh_mcp_reobservation_required": True,
            "merge_authority_granted": False,
            "write_authority_granted": False,
        }


def verify_github_signature(body: bytes, signature: str, secret: str) -> None:
    """Verify HMAC-SHA256 over the EXACT received GitHub body bytes."""
    if not isinstance(body, bytes) or not 1 <= len(body) <= MAX_GITHUB_EVENT_BODY:
        raise GitHubIngressError("github_payload_size_invalid")
    if not isinstance(signature, str) or _SIGNATURE.fullmatch(signature) is None:
        raise GitHubIngressError("github_signature_format_invalid")
    if not isinstance(secret, str) or len(secret.encode("utf-8")) < 32:
        raise GitHubIngressError("github_ingress_secret_not_configured")
    expected = "sha256=" + hmac.new(
        secret.encode("utf-8"), body, hashlib.sha256
    ).hexdigest()
    if not hmac.compare_digest(expected, signature):
        raise GitHubIngressError("github_signature_mismatch")


def compile_signed_github_wakeup(
    event_type: str,
    raw_body: bytes,
    signature: str,
    secret: str,
    delivery_id: str,
) -> VerifiedGitHubWakeup:
    """Compile only approved, signed GitHub events without claiming CI truth."""
    verify_github_signature(raw_body, signature, secret)
    if not isinstance(delivery_id, str) or _DELIVERY_ID.fullmatch(delivery_id) is None:
        raise GitHubIngressError("github_delivery_id_invalid")
    if event_type not in ("workflow_run", "pull_request"):
        raise GitHubIngressError("github_event_type_not_allowlisted")
    try:
        event_data = json.loads(raw_body)
    except (ValueError, UnicodeError) as exc:
        raise GitHubIngressError("github_payload_json_invalid") from exc
    if not isinstance(event_data, dict):
        raise GitHubIngressError("github_payload_not_object")
    try:
        if event_type == "workflow_run":
            packet = compile_ci_completed(event_data)
        else:
            packet = compile_pr_head_updated(event_data)
    except (EventContractError, TypeError, ValueError) as exc:
        raise GitHubIngressError("github_payload_scope_invalid") from exc
    payload = packet.get("data")
    if not isinstance(payload, Mapping) or payload.get("fresh_mcp_reobservation_required") is not True:
        raise GitHubIngressError("wakeup_contract_invalid")
    if payload.get("signal_is_success_evidence") is not False:
        raise GitHubIngressError("wakeup_truth_boundary_invalid")
    return VerifiedGitHubWakeup(
        delivery_id=delivery_id,
        source_kind=event_type,
        event_id=packet["eventId"],
        repository=payload["repository"],
        head_sha=payload["head_sha"],
        packet=packet,
    )
