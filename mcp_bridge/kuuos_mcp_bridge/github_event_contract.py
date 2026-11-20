"""Fail-closed GitHub wake-up event contract for a future KuuOS MCP Events adapter.

The module deliberately does not advertise MCP Events, hold callback secrets,
create subscriptions, access GitHub, or grant any authorization. It converts
untrusted GitHub signal data into bounded records which require independent
GitHub MCP re-observation before being used for research or CI certification.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import ipaddress
import json
import re
from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlsplit

KUUOS_REPO = "itakura-hidetoshi/KuuOS"
MGAP_REPO = "itakura-hidetoshi/4d-mass-gap"
REPOSITORIES = (KUUOS_REPO, MGAP_REPO)
CI_EVENT = "kuuos.github.ci_completed"
PR_EVENT = "kuuos.github.pr_head_updated"
EVENTS = (CI_EVENT, PR_EVENT)
MGAP_WORKFLOW = "PR Lean Fast Check"
KUUOS_WORKFLOWS = (
    "KuuOS Runtime Full Check",
    "Lean Formal Validation",
    "All Governance Validation",
    "Core Governance Validation",
    "KuuOS PR Governance Gate",
)
TERMINAL = frozenset({
    "success", "failure", "cancelled", "timed_out", "neutral", "skipped",
    "stale", "action_required", "startup_failure",
})
_SHA40 = re.compile(r"^[0-9a-f]{40}$")


class EventContractError(ValueError):
    """The input may not be delivered or promoted into certification."""


def _record(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sha40(value: Any, *, name: str = "head_sha") -> str:
    if not isinstance(value, str) or not _SHA40.fullmatch(value):
        raise EventContractError(f"{name}_invalid")
    return value


def _repository(value: Any) -> str:
    if not isinstance(value, str) or value not in REPOSITORIES:
        raise EventContractError("repository_not_allowlisted")
    return value


def _positive_int(value: Any, name: str) -> int:
    if type(value) is not int or value <= 0:
        raise EventContractError(f"{name}_invalid")
    return value


def _canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _wakeup(event_name: str, identity: Mapping[str, Any], data: Mapping[str, Any]) -> dict[str, Any]:
    digest = hashlib.sha256(_canonical({"name": event_name, "identity": identity})).hexdigest()
    return {
        "eventId": "evt_" + digest,
        "name": event_name,
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "data": dict(data),
        "cursor": None,
    }


def compile_ci_completed(signal: Mapping[str, Any]) -> dict[str, Any]:
    """Compile GitHub's workflow_run envelope, without treating conclusion as CI proof."""
    if not isinstance(signal, Mapping):
        raise EventContractError("signal_not_mapping")
    run = _record(signal.get("workflow_run"))
    repo = _repository(_record(signal.get("repository")).get("full_name"))
    if signal.get("action") != "completed" or run.get("status") != "completed":
        raise EventContractError("workflow_not_completed")
    name = run.get("name")
    allowed = (MGAP_WORKFLOW,) if repo == MGAP_REPO else KUUOS_WORKFLOWS
    if name not in allowed:
        raise EventContractError("workflow_not_allowlisted")
    conclusion = run.get("conclusion")
    if not isinstance(conclusion, str) or conclusion not in TERMINAL:
        raise EventContractError("conclusion_not_terminal")
    rid = _positive_int(run.get("id"), "run_id")
    attempt = _positive_int(run.get("run_attempt", 1), "run_attempt")
    head = _sha40(run.get("head_sha"))
    event = run.get("event")
    if repo == MGAP_REPO and event != "pull_request":
        raise EventContractError("mgap_run_event_not_pull_request")
    if repo == KUUOS_REPO and event not in ("push", "pull_request", "workflow_dispatch"):
        raise EventContractError("kuuos_run_event_not_allowed")
    required_jobs = ["Changed Lean fast check"] if repo == MGAP_REPO else []
    required_steps = ["Run changed Lean fast check"] if repo == MGAP_REPO else []
    data = {
        "repository": repo, "workflow_name": name, "run_id": rid,
        "run_attempt": attempt, "head_sha": head,
        "status": "completed", "conclusion": conclusion,
        "required_job_names": required_jobs,
        "required_step_names": required_steps,
        "signal_is_success_evidence": False,
        "fresh_mcp_reobservation_required": True,
        "merge_authority_granted": False,
        "write_authority_granted": False,
    }
    return _wakeup(
        CI_EVENT,
        {"repository": repo, "run_id": rid, "run_attempt": attempt, "head_sha": head},
        data,
    )


def compile_pr_head_updated(signal: Mapping[str, Any]) -> dict[str, Any]:
    """Compile only a PR opening or synchronize event as a fresh-observation hint."""
    if not isinstance(signal, Mapping):
        raise EventContractError("signal_not_mapping")
    if signal.get("action") not in ("opened", "synchronize"):
        raise EventContractError("pr_action_not_head_update")
    repo = _repository(_record(signal.get("repository")).get("full_name"))
    pr = _record(signal.get("pull_request"))
    number = _positive_int(pr.get("number", signal.get("number")), "pr_number")
    head = _record(pr.get("head"))
    if _record(head.get("repo")).get("full_name") != repo:
        raise EventContractError("fork_head_not_admitted")
    head_sha = _sha40(head.get("sha"))
    base = _record(pr.get("base"))
    base_name = base.get("ref")
    expected_base = (
        "formal/real-hilbert-uniform-coercive-strong-limit"
        if repo == MGAP_REPO else "main"
    )
    if base_name != expected_base:
        raise EventContractError("canonical_base_mismatch")
    data = {
        "repository": repo, "pr_number": number, "head_sha": head_sha,
        "canonical_base": expected_base, "action": signal["action"],
        "signal_is_success_evidence": False,
        "fresh_mcp_reobservation_required": True,
        "merge_authority_granted": False,
        "write_authority_granted": False,
    }
    return _wakeup(
        PR_EVENT,
        {"repository": repo, "pr_number": number, "head_sha": head_sha,
         "action": signal["action"]},
        data,
    )


def validate_filters(event_name: str, arguments: Mapping[str, Any]) -> dict[str, Any]:
    """Validate source-side filters before any future MCP subscription or dispatch."""
    if event_name not in EVENTS or not isinstance(arguments, Mapping):
        raise EventContractError("event_or_arguments_invalid")
    if event_name == PR_EVENT and "workflow_name" in arguments:
        raise EventContractError("pr_event_disallows_workflow_filter")
    if event_name == CI_EVENT and "pr_number" in arguments:
        raise EventContractError("ci_event_disallows_pr_filter")
    allowed_fields = ({"repository", "workflow_name"} if event_name == CI_EVENT
                      else {"repository", "pr_number"})
    if set(arguments) - allowed_fields:
        raise EventContractError("unknown_filter")
    repo = _repository(arguments.get("repository"))
    filters: dict[str, Any] = {"repository": repo}
    if "pr_number" in arguments:
        filters["pr_number"] = _positive_int(arguments["pr_number"], "pr_number")
    if "workflow_name" in arguments:
        if event_name != CI_EVENT:
            raise EventContractError("pr_event_disallows_workflow_filter")
        allowed = (MGAP_WORKFLOW,) if repo == MGAP_REPO else KUUOS_WORKFLOWS
        if arguments["workflow_name"] not in allowed:
            raise EventContractError("workflow_not_allowlisted")
        filters["workflow_name"] = arguments["workflow_name"]
    return filters


def matches_filters(event: Mapping[str, Any], arguments: Mapping[str, Any]) -> bool:
    """A missing PR identity never matches a PR-specific subscription."""
    if not isinstance(event, Mapping):
        return False
    name, data = event.get("name"), _record(event.get("data"))
    try:
        expected = validate_filters(name, arguments)
    except EventContractError:
        return False
    if data.get("repository") != expected["repository"]:
        return False
    if "pr_number" in expected and data.get("pr_number") != expected["pr_number"]:
        return False
    if "workflow_name" in expected and data.get("workflow_name") != expected["workflow_name"]:
        return False
    return True


def event_catalog() -> dict[str, Any]:
    """An events/list proposal; it is not registered with an MCP server yet."""
    base_filters = {
        "type": "object",
        "properties": {
            "repository": {"type": "string", "enum": list(REPOSITORIES)},
            "pr_number": {"type": "integer", "minimum": 1},
        },
        "required": ["repository"], "additionalProperties": False,
    }
    ci_filters = json.loads(json.dumps(base_filters))
    del ci_filters["properties"]["pr_number"]
    ci_filters["properties"]["workflow_name"] = {"type": "string"}
    data_properties = {
        "repository": {"type": "string"},
        "head_sha": {"type": "string", "pattern": "^[0-9a-f]{40}$"},
        "fresh_mcp_reobservation_required": {"const": True},
        "signal_is_success_evidence": {"const": False},
    }
    return {
        "events": [
            {
                "name": CI_EVENT,
                "description": (
                    "GitHub Actions run completed; wake-up only. Re-fetch exact "
                    "workflow, job, Lean step and source HEAD via GitHub MCP."
                ),
                "delivery": ["webhook"],
                "inputSchema": ci_filters,
                "payloadSchema": {
                    "type": "object", "properties": {**data_properties,
                        "run_id": {"type": "integer"},
                        "run_attempt": {"type": "integer"},
                        "workflow_name": {"type": "string"},
                        "conclusion": {"type": "string"},
                    },
                    "required": ["repository", "head_sha", "run_id", "run_attempt",
                                 "workflow_name", "conclusion",
                                 "fresh_mcp_reobservation_required", "signal_is_success_evidence"],
                },
            },
            {
                "name": PR_EVENT,
                "description": (
                    "PR was opened or its head changed. Wake-up only; re-fetch "
                    "the current PR HEAD, changed sources and CI via GitHub MCP."
                ),
                "delivery": ["webhook"],
                "inputSchema": base_filters,
                "payloadSchema": {
                    "type": "object", "properties": {**data_properties,
                        "pr_number": {"type": "integer"},
                        "canonical_base": {"type": "string"},
                        "action": {"type": "string"},
                    },
                    "required": ["repository", "pr_number", "head_sha",
                                 "canonical_base", "action",
                                 "fresh_mcp_reobservation_required", "signal_is_success_evidence"],
                },
            },
        ],
    }


def validate_delivery_url(raw: str) -> str:
    """Only preliminary syntax validation; DNS/IP and challenge checks still required.

    Never make an outbound HTTP request on the strength of this function alone.
    """
    if not isinstance(raw, str) or len(raw) > 2048:
        raise EventContractError("callback_url_invalid")
    try:
        parts = urlsplit(raw)
        hostname = parts.hostname
        if parts.scheme != "https" or not hostname or parts.username or parts.password:
            raise EventContractError("callback_url_not_allowed")
        if parts.fragment or parts.port not in (None, 443) or parts.path.startswith("//"):
            raise EventContractError("callback_url_not_allowed")
        if hostname.lower() in {"localhost", "localhost.localdomain"} or hostname.endswith(".local"):
            raise EventContractError("callback_host_local")
        try:
            ipaddress.ip_address(hostname)
        except ValueError:
            pass
        else:
            raise EventContractError("callback_ip_literal_not_allowed")
        if "." not in hostname or hostname.endswith("."):
            raise EventContractError("callback_hostname_invalid")
    except (TypeError, ValueError) as exc:
        if isinstance(exc, EventContractError):
            raise
        raise EventContractError("callback_url_invalid") from exc
    return raw


def decode_signing_secret(value: str) -> bytes:
    """Decode the whsec_ key without logging or storing it in receipts."""
    if not isinstance(value, str) or not value.startswith("whsec_"):
        raise EventContractError("signing_secret_prefix_invalid")
    try:
        raw = base64.b64decode(value[6:], validate=True)
    except (ValueError, base64.binascii.Error) as exc:
        raise EventContractError("signing_secret_encoding_invalid") from exc
    if not 24 <= len(raw) <= 64:
        raise EventContractError("signing_secret_length_invalid")
    return raw


def standard_webhook_signature(event_id: str, timestamp: int, body: bytes, signing_secret: str) -> str:
    """Build the Standard Webhooks signature; no network requests are made."""
    # Application events and signed one-use verification challenges have
    # distinct protocol IDs. Restrict both without conflating them.
    if not isinstance(event_id, str) or not event_id.startswith(("evt_", "msg_verification_")):
        raise EventContractError("event_id_invalid")
    if type(timestamp) is not int or timestamp < 0 or not isinstance(body, bytes):
        raise EventContractError("webhook_input_invalid")
    key = decode_signing_secret(signing_secret)
    signed = event_id.encode("utf-8") + b"." + str(timestamp).encode("ascii") + b"." + body
    mac = hmac.new(key, signed, hashlib.sha256).digest()
    return "v1," + base64.b64encode(mac).decode("ascii")
