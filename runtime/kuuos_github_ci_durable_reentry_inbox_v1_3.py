#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
from typing import Any, Mapping

VERSION = "kuuos_github_ci_durable_reentry_inbox_v1_3"
READY = "KUUOS_GITHUB_CI_DURABLE_REENTRY_INBOX_READY"
BLOCKED = "KUUOS_GITHUB_CI_DURABLE_REENTRY_INBOX_BLOCKED"
ACK_READY = "KUUOS_GITHUB_CI_DURABLE_REENTRY_ACK_READY"
ACK_BLOCKED = "KUUOS_GITHUB_CI_DURABLE_REENTRY_ACK_BLOCKED"
PENDING_TITLE_PREFIX = "[KuuOS CI Reentry Pending]"
SOURCE_REPOSITORY = "itakura-hidetoshi/4d-mass-gap"
SOURCE_WORKFLOW = "PR Lean Fast Check"
SOURCE_JOB = "Changed Lean fast check"
SOURCE_STEP = "Run changed Lean fast check"
CANONICAL_BASE = "formal/real-hilbert-uniform-coercive-strong-limit"
DESTINATION_REPOSITORY = "itakura-hidetoshi/KuuOS"
SENDER_VERSION = "mgap4d_kuuos_ci_completion_sender_v0_1"
V11_VERIFIED = "KUUOS_GITHUB_CI_COMPLETION_REENTRY_VERIFIED"

_SHA40 = re.compile(r"^[0-9a-f]{40}$")
_TERMINAL_CONCLUSIONS = {
    "success",
    "failure",
    "cancelled",
    "timed_out",
    "neutral",
    "skipped",
    "stale",
    "action_required",
    "startup_failure",
}


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _i(value: Any, default: int = 0) -> int:
    if isinstance(value, bool):
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _digest(value: Any) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _names(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if isinstance(item, str) and item]


def _write(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _identity(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "repository": str(payload.get("repository", "")),
        "run_id": _i(payload.get("run_id"), 0),
        "workflow_name": str(payload.get("workflow_name", "")),
        "head_sha": str(payload.get("head_sha", "")).lower(),
    }


def _identity_key(identity: Mapping[str, Any]) -> str:
    return _digest(
        {
            "repository": str(identity.get("repository", "")),
            "run_id": _i(identity.get("run_id"), 0),
            "workflow_name": str(identity.get("workflow_name", "")),
            "head_sha": str(identity.get("head_sha", "")).lower(),
        }
    )


def compile_inbox(raw_event: Mapping[str, Any]) -> dict[str, Any]:
    payload = _m(raw_event.get("client_payload"))
    blockers: list[str] = []

    if str(raw_event.get("action", "")) not in {"", "completed"}:
        blockers.append("repository_dispatch_action_invalid")
    if str(payload.get("version", "")) != SENDER_VERSION:
        blockers.append("sender_version_mismatch")
    if str(payload.get("repository", "")) != SOURCE_REPOSITORY:
        blockers.append("source_repository_mismatch")
    if str(payload.get("workflow_name", "")) != SOURCE_WORKFLOW:
        blockers.append("source_workflow_mismatch")
    if str(payload.get("run_event", "")) != "pull_request":
        blockers.append("source_run_event_not_pull_request")
    if str(payload.get("status", "")) != "completed":
        blockers.append("source_workflow_not_completed")
    if payload.get("conclusion") not in _TERMINAL_CONCLUSIONS:
        blockers.append("source_workflow_conclusion_not_terminal")
    if _i(payload.get("run_id"), 0) <= 0:
        blockers.append("run_id_invalid")
    head_sha = str(payload.get("head_sha", "")).lower()
    if _SHA40.fullmatch(head_sha) is None:
        blockers.append("head_sha_invalid")
    if _i(payload.get("pr_number"), 0) <= 0:
        blockers.append("pull_request_number_invalid")
    if str(payload.get("pr_base_branch", "")) != CANONICAL_BASE:
        blockers.append("canonical_base_mismatch")
    if str(payload.get("destination_repository", "")) != DESTINATION_REPOSITORY:
        blockers.append("destination_repository_mismatch")
    if _names(payload.get("required_job_names")) != [SOURCE_JOB]:
        blockers.append("required_job_binding_mismatch")
    if _names(payload.get("required_step_names")) != [SOURCE_STEP]:
        blockers.append("required_step_binding_mismatch")
    if payload.get("source_job_conclusion") not in _TERMINAL_CONCLUSIONS:
        blockers.append("source_job_conclusion_not_terminal")
    if payload.get("source_step_conclusion") not in _TERMINAL_CONCLUSIONS:
        blockers.append("source_step_conclusion_not_terminal")
    if payload.get("event_is_wakeup_signal_only") is not True:
        blockers.append("event_signal_boundary_missing")
    if payload.get("fresh_mcp_reobservation_required") is not True:
        blockers.append("fresh_mcp_reobservation_boundary_missing")

    identity = _identity(payload)
    issue_key = _identity_key(identity)
    record = {
        "version": VERSION,
        "status": "pending" if not blockers else "blocked",
        "issue_key": issue_key,
        "identity": identity,
        "source": {
            "head_branch": str(payload.get("head_branch", "")),
            "conclusion": payload.get("conclusion"),
            "pr_number": _i(payload.get("pr_number"), 0),
            "pr_base_branch": str(payload.get("pr_base_branch", "")),
            "required_job_names": _names(payload.get("required_job_names")),
            "required_step_names": _names(payload.get("required_step_names")),
            "source_job_conclusion": payload.get("source_job_conclusion"),
            "source_step_conclusion": payload.get("source_step_conclusion"),
            "source_event_digest": str(payload.get("source_event_digest", "")),
            "source_jobs_digest": str(payload.get("source_jobs_digest", "")),
        },
        "mcp_reobserve_request": {
            "observation_kind": "workflow_run_jobs",
            "repo_full_name": identity["repository"],
            "run_id": identity["run_id"],
            "expected_workflow_name": identity["workflow_name"],
            "expected_head_sha": identity["head_sha"],
            "required_job_names": [SOURCE_JOB],
            "required_step_names": [SOURCE_STEP],
            "fresh_mcp_reobservation_required": True,
        },
        "boundary": {
            "durable_issue_is_wakeup_signal_only": True,
            "durable_issue_is_not_ci_success_evidence": True,
            "fresh_mcp_reobservation_required_before_ack": True,
            "ack_does_not_grant_merge_authority": True,
            "ack_does_not_grant_write_authority": True,
        },
        "source_dispatch_digest": _digest(raw_event),
        "blockers": sorted(set(blockers)),
    }
    record["record_digest"] = _digest(record)

    issue_spec: dict[str, Any] = {}
    if not blockers:
        issue_spec = {
            "issue_key": issue_key,
            "title": f"{PENDING_TITLE_PREFIX} {issue_key}",
            "body": json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True),
            "dedupe_query": f'repo:{DESTINATION_REPOSITORY} is:issue in:title "{issue_key}"',
        }

    return {
        "version": VERSION,
        "status": READY if not blockers else BLOCKED,
        "persist_allowed": not blockers,
        "record": record,
        "issue_spec": issue_spec,
        "blockers": sorted(set(blockers)),
    }


def parse_inbox_body(body: str) -> dict[str, Any]:
    try:
        value = json.loads(body)
    except (TypeError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def compile_ack(
    inbox_record: Mapping[str, Any],
    verification: Mapping[str, Any],
) -> dict[str, Any]:
    record = _m(inbox_record)
    identity = _m(record.get("identity"))
    blockers: list[str] = []

    if record.get("version") != VERSION:
        blockers.append("inbox_version_mismatch")
    if record.get("status") != "pending":
        blockers.append("inbox_not_pending")
    expected_key = _identity_key(identity)
    if str(record.get("issue_key", "")) != expected_key:
        blockers.append("inbox_identity_key_mismatch")
    if verification.get("status") != V11_VERIFIED:
        blockers.append("fresh_mcp_verification_not_verified")
    if verification.get("fresh_mcp_reobservation") is not True:
        blockers.append("fresh_mcp_reobservation_missing")
    if verification.get("route") not in {"verified_success", "verified_non_success"}:
        blockers.append("verification_route_not_terminal")
    if verification.get("merge_authority_granted") is not False:
        blockers.append("verification_merge_authority_boundary_broken")
    if verification.get("write_authority_granted") is not False:
        blockers.append("verification_write_authority_boundary_broken")

    checks = {
        "repository": str(verification.get("repository", "")) == str(identity.get("repository", "")),
        "run_id": _i(verification.get("run_id"), 0) == _i(identity.get("run_id"), 0),
        "workflow_name": str(verification.get("workflow_name", "")) == str(identity.get("workflow_name", "")),
        "head_sha": str(verification.get("head_sha", "")).lower() == str(identity.get("head_sha", "")).lower(),
    }
    for field, agrees in checks.items():
        if not agrees:
            blockers.append(f"verification_{field}_mismatch")

    ack = {
        "version": VERSION,
        "status": "acknowledged" if not blockers else "blocked",
        "issue_key": str(record.get("issue_key", "")),
        "identity": dict(identity),
        "verification_route": verification.get("route"),
        "event_conclusion": verification.get("event_conclusion"),
        "fresh_mcp_reobservation": verification.get("fresh_mcp_reobservation") is True,
        "merge_authority_granted": False,
        "write_authority_granted": False,
        "verification_evidence_digest": str(verification.get("evidence_digest", "")),
        "verification_digest": _digest(verification),
        "blockers": sorted(set(blockers)),
    }
    ack["ack_digest"] = _digest(ack)

    return {
        "version": VERSION,
        "status": ACK_READY if not blockers else ACK_BLOCKED,
        "close_issue_allowed": not blockers,
        "ack": ack,
        "comment": json.dumps(ack, ensure_ascii=False, indent=2, sort_keys=True),
        "blockers": sorted(set(blockers)),
    }


def _fixture_payload(*, conclusion: str = "success") -> dict[str, Any]:
    sha = "a" * 40
    return {
        "version": SENDER_VERSION,
        "repository": SOURCE_REPOSITORY,
        "run_id": 123,
        "workflow_name": SOURCE_WORKFLOW,
        "head_sha": sha,
        "head_branch": "formal/example",
        "status": "completed",
        "conclusion": conclusion,
        "run_event": "pull_request",
        "pr_number": 2093,
        "pr_base_branch": CANONICAL_BASE,
        "required_job_names": [SOURCE_JOB],
        "required_step_names": [SOURCE_STEP],
        "source_job_conclusion": conclusion,
        "source_step_conclusion": conclusion,
        "destination_repository": DESTINATION_REPOSITORY,
        "source_event_digest": "event-digest",
        "source_jobs_digest": "jobs-digest",
        "event_is_wakeup_signal_only": True,
        "fresh_mcp_reobservation_required": True,
    }


def _fixture_event(*, conclusion: str = "success") -> dict[str, Any]:
    return {"action": "completed", "client_payload": _fixture_payload(conclusion=conclusion)}


def _fixture_verification(record: Mapping[str, Any], *, route: str = "verified_success") -> dict[str, Any]:
    identity = _m(record.get("identity"))
    return {
        "version": "kuuos_github_ci_completion_reentry_v1_1",
        "status": V11_VERIFIED,
        "route": route,
        "repository": identity.get("repository"),
        "run_id": identity.get("run_id"),
        "head_sha": identity.get("head_sha"),
        "workflow_name": identity.get("workflow_name"),
        "event_conclusion": "success" if route == "verified_success" else "failure",
        "fresh_mcp_reobservation": True,
        "merge_authority_granted": False,
        "write_authority_granted": False,
        "blockers": [],
        "evidence_digest": "fresh-evidence",
    }


def self_check() -> None:
    ready = compile_inbox(_fixture_event())
    assert ready["status"] == READY
    assert ready["persist_allowed"] is True
    assert ready["record"]["status"] == "pending"
    assert ready["issue_spec"]["title"].startswith(PENDING_TITLE_PREFIX)
    parsed = parse_inbox_body(ready["issue_spec"]["body"])
    assert parsed["issue_key"] == ready["record"]["issue_key"]
    assert parsed["boundary"]["durable_issue_is_not_ci_success_evidence"] is True

    failed = compile_inbox(_fixture_event(conclusion="failure"))
    assert failed["status"] == READY
    assert failed["record"]["source"]["conclusion"] == "failure"

    wrong_base_event = _fixture_event()
    wrong_base_event["client_payload"]["pr_base_branch"] = "main"
    wrong_base = compile_inbox(wrong_base_event)
    assert wrong_base["persist_allowed"] is False
    assert "canonical_base_mismatch" in wrong_base["blockers"]

    no_fresh_event = _fixture_event()
    no_fresh_event["client_payload"]["fresh_mcp_reobservation_required"] = False
    no_fresh = compile_inbox(no_fresh_event)
    assert no_fresh["persist_allowed"] is False
    assert "fresh_mcp_reobservation_boundary_missing" in no_fresh["blockers"]

    record = ready["record"]
    verified = _fixture_verification(record)
    ack = compile_ack(record, verified)
    assert ack["status"] == ACK_READY
    assert ack["close_issue_allowed"] is True
    assert ack["ack"]["fresh_mcp_reobservation"] is True
    assert ack["ack"]["merge_authority_granted"] is False

    unverified = dict(verified)
    unverified["status"] = "KUUOS_GITHUB_CI_COMPLETION_REENTRY_VERIFY_BLOCKED"
    blocked_ack = compile_ack(record, unverified)
    assert blocked_ack["close_issue_allowed"] is False
    assert "fresh_mcp_verification_not_verified" in blocked_ack["blockers"]

    wrong_head = dict(verified)
    wrong_head["head_sha"] = "b" * 40
    mismatched_ack = compile_ack(record, wrong_head)
    assert mismatched_ack["close_issue_allowed"] is False
    assert "verification_head_sha_mismatch" in mismatched_ack["blockers"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-check", action="store_true")
    parser.add_argument("--event")
    parser.add_argument("--output-dir", default=".kuuos/github-ci-durable-reentry-inbox-v1-3")
    parser.add_argument("--ack-record")
    parser.add_argument("--verification")
    args = parser.parse_args()

    if args.self_check:
        self_check()
        print("KUUOS_GITHUB_CI_DURABLE_REENTRY_INBOX_V1_3_SELF_CHECK_OK")
        return 0

    out = pathlib.Path(args.output_dir)
    if args.ack_record or args.verification:
        if not args.ack_record or not args.verification:
            parser.error("--ack-record and --verification must be supplied together")
        record = json.loads(pathlib.Path(args.ack_record).read_text(encoding="utf-8"))
        verification = json.loads(pathlib.Path(args.verification).read_text(encoding="utf-8"))
        if not isinstance(record, Mapping) or not isinstance(verification, Mapping):
            raise SystemExit("ack inputs must be JSON objects")
        result = compile_ack(record, verification)
        _write(out / "ci_reentry_ack_spec.json", result)
        print(result["status"])
        return 0 if result["close_issue_allowed"] else 2

    if not args.event:
        parser.error("--event is required unless --self-check or ack mode is used")
    raw = json.loads(pathlib.Path(args.event).read_text(encoding="utf-8"))
    if not isinstance(raw, Mapping):
        raise SystemExit("event payload must be a JSON object")
    result = compile_inbox(raw)
    _write(out / "ci_reentry_inbox_result.json", result)
    if result["persist_allowed"]:
        _write(out / "ci_reentry_inbox_record.json", result["record"])
        _write(out / "ci_reentry_issue_spec.json", result["issue_spec"])
    print(result["status"])
    return 0 if result["persist_allowed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
