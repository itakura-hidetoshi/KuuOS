from __future__ import annotations

import hashlib
import hmac
import json

import pytest

from kuuos_mcp_bridge.github_event_ingress import (
    GitHubIngressError, compile_signed_github_wakeup, verify_github_signature,
)
from kuuos_mcp_bridge.github_event_contract import CI_EVENT, PR_EVENT, MGAP_REPO

SECRET = "k" * 40
ID = "a20f3142-0b52-4ea4-a93b-3412cf17f010"


def signed(payload, *, event_type="workflow_run"):
    raw = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()
    signature = "sha256=" + hmac.new(SECRET.encode(), raw, hashlib.sha256).hexdigest()
    return (event_type, raw, signature, SECRET, ID)


def ci():
    return {
        "action": "completed", "repository": {"full_name": MGAP_REPO},
        "workflow_run": {
            "name": "PR Lean Fast Check", "event": "pull_request",
            "status": "completed", "conclusion": "failure",
            "id": 44726446342, "run_attempt": 1, "head_sha": "b" * 40,
        },
    }


def pr():
    return {
        "action": "synchronize", "repository": {"full_name": MGAP_REPO},
        "pull_request": {
            "number": 6883,
            "head": {"repo": {"full_name": MGAP_REPO}, "sha": "b" * 40},
            "base": {"ref": "formal/real-hilbert-uniform-coercive-strong-limit"},
        },
    }


def test_ci_completion_is_signed_wakeup_not_ci_certificate():
    got = compile_signed_github_wakeup(*signed(ci()))
    assert got.packet["name"] == CI_EVENT
    assert got.repository == MGAP_REPO
    receipt = got.public_receipt()
    assert receipt["github_transport_signature_verified"] is True
    assert receipt["signal_is_success_evidence"] is False
    assert receipt["merge_authority_granted"] is False
    assert receipt["run_id"] == 44726446342


def test_pr_update_uses_distinct_event_identity():
    got = compile_signed_github_wakeup(*signed(pr(), event_type="pull_request"))
    assert got.packet["name"] == PR_EVENT
    assert got.public_receipt()["pr_number"] == 6883
    assert got.event_id.startswith("evt_")


def test_signed_replay_keeps_exact_event_id():
    one = compile_signed_github_wakeup(*signed(ci()))
    two = compile_signed_github_wakeup(*signed(ci()))
    assert one.event_id == two.event_id


def test_modified_body_or_signature_rejected_before_parsing():
    event_type, raw, signature, secret, did = signed(ci())
    with pytest.raises(GitHubIngressError, match="github_signature_mismatch"):
        compile_signed_github_wakeup(event_type, raw + b" ", signature, secret, did)
    with pytest.raises(GitHubIngressError, match="github_signature_mismatch"):
        compile_signed_github_wakeup(event_type, raw, "sha256=" + "0" * 64, secret, did)


def test_missing_secret_or_wrong_signature_format_rejected():
    _, raw, signature, _, _ = signed(ci())
    with pytest.raises(GitHubIngressError, match="github_ingress_secret_not_configured"):
        verify_github_signature(raw, signature, "short")
    with pytest.raises(GitHubIngressError, match="github_signature_format_invalid"):
        verify_github_signature(raw, "sha1=" + "0" * 40, SECRET)


def test_unsigned_event_types_not_admitted():
    value = signed(ci(), event_type="push")
    with pytest.raises(GitHubIngressError, match="github_event_type_not_allowlisted"):
        compile_signed_github_wakeup(*value)


def test_pending_ci_not_promoted():
    x = ci()
    x["workflow_run"]["status"] = "in_progress"
    with pytest.raises(GitHubIngressError, match="github_payload_scope_invalid"):
        compile_signed_github_wakeup(*signed(x))


def test_fork_pr_and_wrong_base_not_admitted():
    x = pr()
    x["pull_request"]["head"]["repo"]["full_name"] = "fork/repo"
    with pytest.raises(GitHubIngressError, match="github_payload_scope_invalid"):
        compile_signed_github_wakeup(*signed(x, event_type="pull_request"))
    x = pr()
    x["pull_request"]["base"]["ref"] = "main"
    with pytest.raises(GitHubIngressError, match="github_payload_scope_invalid"):
        compile_signed_github_wakeup(*signed(x, event_type="pull_request"))


def test_invalid_delivery_id_blocks_even_valid_signature():
    value = signed(ci())
    with pytest.raises(GitHubIngressError, match="github_delivery_id_invalid"):
        compile_signed_github_wakeup(*value[:4], "x")


def test_payload_limit_and_json_structure_fail_closed():
    with pytest.raises(GitHubIngressError, match="github_payload_size_invalid"):
        verify_github_signature(b"x" * 300000, "sha256=" + "0" * 64, SECRET)
    value = signed(["unexpected"])
    with pytest.raises(GitHubIngressError, match="github_payload_not_object"):
        compile_signed_github_wakeup(*value)


def test_unknown_repo_and_event_scope_fail_closed():
    x = ci()
    x["repository"]["full_name"] = "someone/other"
    with pytest.raises(GitHubIngressError, match="github_payload_scope_invalid"):
        compile_signed_github_wakeup(*signed(x))
