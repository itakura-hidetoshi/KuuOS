from __future__ import annotations

import base64
import json

import pytest
from kuuos_mcp_bridge.github_event_contract import (
    CI_EVENT, PR_EVENT, CI_GATES_EVENT, CI_GATES_WORKFLOW,
    KUUOS_REPO, MGAP_REPO, EventContractError,
    compile_ci_completed, compile_pr_head_updated, decode_signing_secret,
    event_catalog, matches_filters, standard_webhook_signature,
    validate_delivery_url, validate_filters,
)


def ci_signal(repo=MGAP_REPO, **changes):
    workflow = "PR Lean Fast Check" if repo == MGAP_REPO else "Lean Formal Validation"
    event = "pull_request" if repo == MGAP_REPO else "push"
    data = {
        "action": "completed", "repository": {"full_name": repo},
        "workflow_run": {
            "id": 44669485294, "run_attempt": 1, "name": workflow,
            "event": event, "status": "completed", "conclusion": "failure",
            "head_sha": "a" * 40,
        },
    }
    data["workflow_run"].update(changes)
    return data


def pr_signal(repo=MGAP_REPO, **changes):
    base = "formal/real-hilbert-uniform-coercive-strong-limit" if repo == MGAP_REPO else "main"
    x = {
        "action": "synchronize", "repository": {"full_name": repo},
        "number": 6883,
        "pull_request": {
            "number": 6883, "head": {"sha": "b" * 40, "repo": {"full_name": repo}},
            "base": {"ref": base},
        },
    }
    x["pull_request"].update(changes)
    return x


def test_completion_packet_is_non_authoritative():
    e = compile_ci_completed(ci_signal())
    assert e["name"] == CI_EVENT
    assert e["eventId"].startswith("evt_")
    assert e["data"]["required_step_names"] == ["Run changed Lean fast check"]
    assert e["data"]["signal_is_success_evidence"] is False
    assert e["data"]["fresh_mcp_reobservation_required"] is True
    assert e["data"]["merge_authority_granted"] is False
    assert e["data"]["write_authority_granted"] is False


def test_completion_event_id_stable_on_replay_and_distinguishes_attempts():
    old = compile_ci_completed(ci_signal())
    same = compile_ci_completed(ci_signal())
    newer = compile_ci_completed(ci_signal(run_attempt=2))
    assert old["eventId"] == same["eventId"]
    assert newer["eventId"] != old["eventId"]


@pytest.mark.parametrize("payload,reason", [
    (ci_signal(status="in_progress"), "workflow_not_completed"),
    (ci_signal(conclusion=None), "conclusion_not_terminal"),
    (ci_signal(head_sha="not-a-hash"), "head_sha_invalid"),
    (ci_signal(name="Unexpected Workflow"), "workflow_not_allowlisted"),
    (ci_signal(event="push"), "mgap_run_event_not_pull_request"),
    (ci_signal(run_attempt=True), "run_attempt_invalid"),
    (ci_signal(run_attempt=0), "run_attempt_invalid"),
    (ci_signal(repo="itakura-hidetoshi/unknown"), "repository_not_allowlisted"),
])
def test_fail_closed_ci(payload, reason):
    with pytest.raises(EventContractError, match=reason):
        compile_ci_completed(payload)


def test_kuuos_workflow_is_separate_from_mgap():
    packet = compile_ci_completed(ci_signal(repo=KUUOS_REPO))
    assert packet["data"]["repository"] == KUUOS_REPO
    assert packet["data"]["required_step_names"] == []


def test_pr_packet_is_hint_not_verified_source():
    e = compile_pr_head_updated(pr_signal())
    assert e["name"] == PR_EVENT
    assert e["data"]["canonical_base"] == "formal/real-hilbert-uniform-coercive-strong-limit"
    assert e["data"]["fresh_mcp_reobservation_required"] is True
    assert e["data"]["merge_authority_granted"] is False


def test_pr_wrong_base_or_fork_rejected():
    bad_base = pr_signal(base={"ref": "main"})
    with pytest.raises(EventContractError, match="canonical_base_mismatch"):
        compile_pr_head_updated(bad_base)
    bad_fork = pr_signal(head={"sha": "b"*40, "repo": {"full_name": "someone/fork"}})
    with pytest.raises(EventContractError, match="fork_head_not_admitted"):
        compile_pr_head_updated(bad_fork)


def test_pr_non_head_change_not_emitted():
    x = pr_signal()
    x["action"] = "labeled"
    with pytest.raises(EventContractError, match="pr_action_not_head_update"):
        compile_pr_head_updated(x)


def test_filter_requires_explicit_repo_and_valid_workflow():
    assert validate_filters(CI_EVENT, {"repository": MGAP_REPO, "workflow_name": "PR Lean Fast Check"})["repository"] == MGAP_REPO
    with pytest.raises(EventContractError, match="repository_not_allowlisted"):
        validate_filters(CI_EVENT, {})
    with pytest.raises(EventContractError, match="unknown_filter"):
        validate_filters(CI_EVENT, {"repository": MGAP_REPO, "arbitrary": True})
    with pytest.raises(EventContractError, match="pr_event_disallows_workflow_filter"):
        validate_filters(PR_EVENT, {"repository": MGAP_REPO, "workflow_name": "PR Lean Fast Check"})
    with pytest.raises(EventContractError, match="ci_event_disallows_pr_filter"):
        validate_filters(CI_EVENT, {"repository": MGAP_REPO, "pr_number": 6883})
    with pytest.raises(EventContractError, match="pr_number_invalid"):
        validate_filters(PR_EVENT, {"repository": MGAP_REPO, "pr_number": True})


def test_pr_filter_does_not_match_unresolved_ci_pr():
    wakeup = compile_ci_completed(ci_signal())
    assert matches_filters(wakeup, {"repository": MGAP_REPO}) is True
    assert matches_filters(wakeup, {"repository": MGAP_REPO, "pr_number": 6883}) is False


def test_ci_source_filter_cannot_match_other_repo():
    event = compile_ci_completed(ci_signal())
    assert not matches_filters(event, {"repository": KUUOS_REPO})
    assert matches_filters(event, {"repository": MGAP_REPO, "workflow_name": "PR Lean Fast Check"})


def test_event_catalog_strict_and_no_merging_claim():
    catalog = event_catalog()
    assert [e["name"] for e in catalog["events"]] == [
        CI_EVENT, CI_GATES_EVENT, PR_EVENT
    ]
    assert all(e["delivery"] == ["webhook"] for e in catalog["events"])
    assert all(e["inputSchema"]["required"] == ["repository"] for e in catalog["events"])
    assert all(e["inputSchema"]["additionalProperties"] is False for e in catalog["events"])
    assert all(e["payloadSchema"]["properties"]["signal_is_success_evidence"]["const"] is False for e in catalog["events"])


def test_callback_preflight_rejects_local_or_ip_literals():
    assert validate_delivery_url("https://callback.example.org/ci") == "https://callback.example.org/ci"
    for url in ("http://callback.example.org", "https://localhost", "https://127.0.0.1", "https://[::1]", "https://foo.local", "https://foo", "https://user:pass@example.org", "https://example.org:8080/hi", "https://example.org/x#fragment"):
        with pytest.raises(EventContractError):
            validate_delivery_url(url)


def test_signing_secret_and_signature():
    secret = "whsec_" + base64.b64encode(b"a" * 32).decode("ascii")
    assert decode_signing_secret(secret) == b"a" * 32
    sig = standard_webhook_signature("evt_1234", 1788000000, b'{"ok":true}', secret)
    assert sig.startswith("v1,")
    assert sig == standard_webhook_signature("evt_1234", 1788000000, b'{"ok":true}', secret)
    assert sig != standard_webhook_signature("evt_1234", 1788000001, b'{"ok":true}', secret)
    for bad in ("whsec_bad", "none", "whsec_" + base64.b64encode(b"a"*8).decode("ascii")):
        with pytest.raises(EventContractError):
            decode_signing_secret(bad)


def test_payload_json_serialization():
    assert json.loads(json.dumps(compile_ci_completed(ci_signal())))
    assert json.loads(json.dumps(event_catalog()))


def test_ci_gate_source_event_is_separate_from_terminal_ci_completion():
    catalog = event_catalog()
    gated = next(v for v in catalog["events"] if v["name"] == CI_GATES_EVENT)
    assert gated["inputSchema"]["properties"]["repository"]["enum"] == [KUUOS_REPO]
    assert gated["inputSchema"]["properties"]["workflow_name"]["enum"] == [
        CI_GATES_WORKFLOW
    ]
    assert gated["payloadSchema"]["properties"]["ci_terminal_conclusion_verified"]["const"] is False
    assert validate_filters(CI_GATES_EVENT, {
        "repository": KUUOS_REPO, "workflow_name": CI_GATES_WORKFLOW
    })["workflow_name"] == CI_GATES_WORKFLOW
    with pytest.raises(EventContractError, match="repository_not_allowlisted"):
        validate_filters(CI_GATES_EVENT, {"repository": MGAP_REPO})
    with pytest.raises(EventContractError, match="workflow_not_allowlisted"):
        validate_filters(CI_GATES_EVENT, {
            "repository": KUUOS_REPO, "workflow_name": "Lean Formal Validation"
        })
    with pytest.raises(EventContractError, match="pr_filter"):
        validate_filters(CI_GATES_EVENT, {"repository": KUUOS_REPO, "pr_number": 1})
