#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass
from typing import Any, Mapping

VERSION = "kuuos_github_public_ci_completion_poller_v1_2"
SOURCE_REPO = "itakura-hidetoshi/4d-mass-gap"
SOURCE_WORKFLOW_FILE = "pr-lean-fast-check.yml"
SOURCE_WORKFLOW_NAME = "PR Lean Fast Check"
CANONICAL_BASE = "formal/real-hilbert-uniform-coercive-strong-limit"
REQUIRED_JOB = "Changed Lean fast check"
REQUIRED_STEP = "Run changed Lean fast check"
DISPATCH_EVENT_TYPE = "kuuos_ci_completion_v1_1"
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


@dataclass(frozen=True)
class PollSummary:
    version: str
    status: str
    source_repo: str
    source_workflow: str
    canonical_base: str
    previous_run_id: int
    final_run_id: int
    examined_new_runs: int
    dispatched_run_ids: list[int]
    ignored_run_ids: list[int]
    bootstrap_primed: bool
    quarantined_run_ids: list[int]
    pending_run_ids: list[int]
    wakeup_is_success_evidence: bool
    fresh_mcp_reobservation_required: bool


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _i(value: Any, default: int = 0) -> int:
    if isinstance(value, bool):
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _names(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def _http_json(url: str) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "KuuOS-public-ci-poller-v1.2",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as exc:
        raise RuntimeError(f"source_github_api_read_failed:{type(exc).__name__}") from None
    if not isinstance(payload, dict):
        raise RuntimeError(f"source_github_api_payload_not_object:{url}")
    return payload


def _post_self_dispatch(target_repo: str, token: str, payload: Mapping[str, Any]) -> None:
    if not target_repo or "/" not in target_repo:
        raise RuntimeError("target_repo_invalid")
    if not token:
        raise RuntimeError("self_dispatch_token_missing")
    url = f"https://api.github.com/repos/{target_repo}/dispatches"
    body = json.dumps(
        {"event_type": DISPATCH_EVENT_TYPE, "client_payload": dict(payload)},
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    if len(payload) > 10:
        raise RuntimeError("self_dispatch_payload_too_many_properties")
    if len(body) >= 65536:
        raise RuntimeError("self_dispatch_payload_too_large")
    request = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "KuuOS-public-ci-poller-v1.2",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            if response.status not in {200, 201, 202, 204}:
                raise RuntimeError(f"self_dispatch_unexpected_status:{response.status}")
    except urllib.error.HTTPError as exc:
        request_id = str(exc.headers.get("X-GitHub-Request-Id", "")) if exc.headers else ""
        request_id = re.sub(r"[^a-zA-Z0-9:-]", "", request_id)[:100]
        raise RuntimeError(f"self_dispatch_failed:http_{exc.code}:request_id={request_id}") from None
    except (urllib.error.URLError, TimeoutError) as exc:
        raise RuntimeError(f"self_dispatch_failed:{type(exc).__name__}") from None


def _validate_state(payload: Any) -> int:
    if not isinstance(payload, Mapping):
        raise RuntimeError("state_invalid:expected_object")
    expected = {"version": VERSION, "source_repo": SOURCE_REPO,
                "source_workflow": SOURCE_WORKFLOW_NAME, "canonical_base": CANONICAL_BASE}
    if any(payload.get(key) != value for key, value in expected.items()):
        raise RuntimeError("state_identity_mismatch")
    value = payload.get("last_processed_run_id")
    if type(value) is not int or value < 0:
        raise RuntimeError("state_invalid:cursor")
    return value


def _load_state(path: pathlib.Path) -> int:
    if not path.is_file():
        raise RuntimeError("state_missing:explicit_reviewed_checkpoint_required")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        raise RuntimeError("state_invalid:unreadable_checkpoint") from None
    return _validate_state(payload)


def _state_payload(run_id: int, outcome: Mapping[str, Any] | None = None) -> dict[str, Any]:
    payload = {"version": VERSION, "last_processed_run_id": run_id,
               "source_repo": SOURCE_REPO, "source_workflow": SOURCE_WORKFLOW_NAME,
               "canonical_base": CANONICAL_BASE}
    if outcome is not None:
        payload["last_outcome"] = dict(outcome)
    _validate_state(payload)
    return payload


def _save_state(path: pathlib.Path, run_id: int, outcome: Mapping[str, Any] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(_state_payload(run_id, outcome), ensure_ascii=False,
                              indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def _run_base_ref(run: Mapping[str, Any]) -> str:
    pulls = run.get("pull_requests")
    if not isinstance(pulls, list):
        return ""
    for raw in pulls:
        pull = _m(raw)
        base = _m(pull.get("base"))
        ref = str(base.get("ref", ""))
        if ref:
            return ref
    return ""


def _same_repository_head(run: Mapping[str, Any], source_repo: str) -> bool:
    head_repo = _m(run.get("head_repository"))
    full_name = str(head_repo.get("full_name", ""))
    if full_name:
        return full_name == source_repo
    pulls = run.get("pull_requests")
    if not isinstance(pulls, list):
        return False
    for raw in pulls:
        head = _m(_m(raw).get("head"))
        repo = _m(head.get("repo"))
        candidate = str(repo.get("full_name", ""))
        if candidate:
            return candidate == source_repo
    return False


def classify_run(
    run: Mapping[str, Any],
    *,
    source_repo: str = SOURCE_REPO,
    workflow_name: str = SOURCE_WORKFLOW_NAME,
    canonical_base: str = CANONICAL_BASE,
) -> tuple[str, list[str]]:
    reasons: list[str] = []
    if str(run.get("name", "")) != workflow_name:
        reasons.append("workflow_name_mismatch")
    if str(run.get("event", "")) != "pull_request":
        reasons.append("run_event_not_pull_request")
    if str(run.get("status", "")) != "completed":
        reasons.append("workflow_not_completed")
    if run.get("conclusion") not in _TERMINAL_CONCLUSIONS:
        reasons.append("workflow_conclusion_not_terminal")
    if _SHA40.fullmatch(str(run.get("head_sha", "")).lower()) is None:
        reasons.append("head_sha_invalid")
    if _run_base_ref(run) != canonical_base:
        reasons.append("canonical_base_mismatch")
    if not _same_repository_head(run, source_repo):
        reasons.append("head_repository_not_source_repository")
    if reasons:
        return "ignored", reasons
    return "candidate", []


def validate_exact_job_and_step(
    jobs_payload: Mapping[str, Any],
    *,
    required_job: str = REQUIRED_JOB,
    required_step: str = REQUIRED_STEP,
) -> tuple[bool, list[str], dict[str, Any]]:
    blockers: list[str] = []
    raw_jobs = jobs_payload.get("jobs")
    jobs = [dict(job) for job in raw_jobs if isinstance(job, Mapping)] if isinstance(raw_jobs, list) else []
    matches = [job for job in jobs if str(job.get("name", "")) == required_job]
    if len(matches) != 1:
        blockers.append(f"required_job_cardinality:{len(matches)}")
        return False, blockers, {}
    job = matches[0]
    if str(job.get("status", "")) != "completed":
        blockers.append("required_job_not_completed")
    if job.get("conclusion") not in _TERMINAL_CONCLUSIONS:
        blockers.append("required_job_conclusion_not_terminal")
    raw_steps = job.get("steps")
    steps = [dict(step) for step in raw_steps if isinstance(step, Mapping)] if isinstance(raw_steps, list) else []
    step_matches = [step for step in steps if str(step.get("name", "")) == required_step]
    if len(step_matches) != 1:
        blockers.append(f"required_step_cardinality:{len(step_matches)}")
        return False, blockers, {"job": job}
    step = step_matches[0]
    if str(step.get("status", "")) != "completed":
        blockers.append("required_step_not_completed")
    if step.get("conclusion") not in _TERMINAL_CONCLUSIONS:
        blockers.append("required_step_conclusion_not_terminal")
    return not blockers, blockers, {"job": job, "step": step}


def make_dispatch_payload(run: Mapping[str, Any]) -> dict[str, Any]:
    pulls = run.get("pull_requests")
    pr_number = 0
    if isinstance(pulls, list) and pulls:
        pr_number = _i(_m(pulls[0]).get("number"), 0)
    completion = {
        "repository": SOURCE_REPO,
        "run_id": _i(run.get("id"), 0),
        "workflow_name": SOURCE_WORKFLOW_NAME,
        "head_sha": str(run.get("head_sha", "")).lower(),
        "head_branch": str(run.get("head_branch", "")),
        "status": str(run.get("status", "")),
        "conclusion": run.get("conclusion"),
        "run_event": str(run.get("event", "")),
        "required_job_names": [REQUIRED_JOB],
        "required_step_names": [REQUIRED_STEP],
        "source_pr_number": pr_number,
        "source_base_ref": CANONICAL_BASE,
        "wakeup_is_success_evidence": False,
        "fresh_mcp_reobservation_required": True,
        "source_transport": "public_github_rest_poll_then_kuuos_self_dispatch",
    }
    return {"schema_version": 2, "completion": completion}


def _workflow_runs_url(source_repo: str, workflow_file: str) -> str:
    encoded = urllib.parse.quote(workflow_file, safe="")
    return (
        f"https://api.github.com/repos/{source_repo}/actions/workflows/{encoded}/runs"
        "?event=pull_request&per_page=100"
    )


def _jobs_url(source_repo: str, run_id: int, attempt: int) -> str:
    return f"https://api.github.com/repos/{source_repo}/actions/runs/{run_id}/attempts/{attempt}/jobs?per_page=100"


def _run_window(source_repo: str, workflow_file: str, previous: int) -> list[dict[str, Any]]:
    """Read through the cursor before processing; never silently truncate backlog."""
    runs: dict[int, dict[str, Any]] = {}
    expected_total: int | None = None
    for page in range(1, 11):
        payload = _http_json(_workflow_runs_url(source_repo, workflow_file) + f"&page={page}")
        raw = payload.get("workflow_runs")
        total = payload.get("total_count")
        if not isinstance(raw, list) or type(total) is not int or total < 0:
            raise RuntimeError("source_runs_response_invalid")
        if expected_total is not None and total != expected_total:
            raise RuntimeError("source_runs_count_changed")
        expected_total = total
        if len(raw) > 100 or len(raw) > total:
            raise RuntimeError("source_runs_response_invalid")
        for run in raw:
            if not isinstance(run, Mapping) or type(run.get("id")) is not int or run["id"] <= 0:
                raise RuntimeError("source_runs_response_invalid")
            runs[run["id"]] = dict(run)
        if any(run_id <= previous for run_id in runs) or len(runs) >= total:
            return sorted(runs.values(), key=lambda run: run["id"])
        if len(raw) < 100:
            raise RuntimeError("source_runs_response_incomplete")
    raise RuntimeError("source_run_window_exceeded:checkpoint_not_advanced")


def _complete_jobs(source_repo: str, run: Mapping[str, Any]) -> dict[str, Any]:
    run_id = run["id"]
    attempt = run.get("run_attempt")
    if type(attempt) is not int or attempt <= 0:
        raise RuntimeError("source_run_attempt_invalid")
    jobs: list[Mapping[str, Any]] = []
    job_ids: set[int] = set()
    total: int | None = None
    for page in range(1, 11):
        payload = _http_json(_jobs_url(source_repo, run_id, attempt) + f"&page={page}")
        raw = payload.get("jobs")
        count = payload.get("total_count")
        if (not isinstance(raw, list) or type(count) is not int or count < 0
                or any(not isinstance(job, Mapping) for job in raw)
                or (total is not None and count != total)):
            raise RuntimeError("source_jobs_response_incomplete")
        total = count
        for job in raw:
            job_id = job.get("id")
            if type(job_id) is not int or job_id <= 0:
                raise RuntimeError("source_job_id_invalid")
            if job_id in job_ids:
                raise RuntimeError("source_jobs_duplicate_id")
            job_ids.add(job_id)
            if (job.get("run_id") != run_id
                    or str(job.get("head_sha", "")).lower() != str(run.get("head_sha", "")).lower()
                    or ("run_attempt" in job and job["run_attempt"] != attempt)):
                raise RuntimeError("source_job_identity_mismatch")
        jobs.extend(raw)
        if len(jobs) == total:
            return {"total_count": total, "jobs": jobs}
        if len(raw) < 100 or len(jobs) > total:
            raise RuntimeError("source_jobs_response_incomplete")
    raise RuntimeError("source_jobs_response_incomplete")


def poll_once(
    *,
    state_file: pathlib.Path,
    target_repo: str,
    dispatch_token: str,
    source_repo: str = SOURCE_REPO,
    workflow_file: str = SOURCE_WORKFLOW_FILE,
    state_store: Any = None,
) -> PollSummary:
    if source_repo != SOURCE_REPO or workflow_file != SOURCE_WORKFLOW_FILE:
        raise RuntimeError("source_identity_override_not_supported")
    previous = _validate_state(state_store.load()) if state_store is not None else _load_state(state_file)
    runs = _run_window(source_repo, workflow_file, previous)
    last_processed = previous
    dispatched: list[int] = []
    ignored: list[int] = []
    quarantined: list[int] = []
    pending: list[int] = []
    examined = 0

    def checkpoint(run_id: int, disposition: str, reason: str = "") -> None:
        outcome = {"run_id": run_id, "disposition": disposition, "reason": reason}
        if state_store is not None:
            state_store.save(_state_payload(run_id, outcome))
        _save_state(state_file, run_id, outcome)

    for run in runs:
        run_id = run["id"]
        if run_id <= previous:
            continue
        examined += 1
        # A lower-ID run can complete later. Do not cross it with a scalar cursor.
        if run.get("status") != "completed":
            pending.append(run_id)
            break
        classification, reasons = classify_run(run, source_repo=source_repo)
        if classification == "ignored":
            checkpoint(run_id, "ignored", ",".join(reasons))
            ignored.append(run_id)
            last_processed = run_id
            continue
        jobs_payload = _complete_jobs(source_repo, run)
        ready, blockers, _ = validate_exact_job_and_step(jobs_payload)
        # Only a complete, terminal cancelled observation may be quarantined.
        # It is never sent as a successful/verified required-check completion.
        if not ready and run.get("conclusion") == "cancelled" and blockers == ["required_job_cardinality:0"]:
            if any(job.get("status") != "completed" or job.get("conclusion") not in _TERMINAL_CONCLUSIONS
                   for job in jobs_payload["jobs"]):
                raise RuntimeError("cancelled_jobs_not_terminal")
            checkpoint(run_id, "quarantined", "cancelled_without_required_job")
            quarantined.append(run_id)
            last_processed = run_id
            continue
        if not ready:
            raise RuntimeError("source_exact_job_step_gate_blocked:" + str(run_id) + ":" + ",".join(blockers))
        _post_self_dispatch(target_repo, dispatch_token, make_dispatch_payload(run))
        # A failed POST never advances state. A failed checkpoint stops this poll;
        # a retry can duplicate only the in-flight notification (at-least-once).
        checkpoint(run_id, "dispatched")
        dispatched.append(run_id)
        last_processed = run_id

    return PollSummary(
        version=VERSION,
        status="KUUOS_PUBLIC_CI_POLLER_WAITING" if pending else "KUUOS_PUBLIC_CI_POLLER_READY",
        source_repo=source_repo, source_workflow=SOURCE_WORKFLOW_NAME,
        canonical_base=CANONICAL_BASE, previous_run_id=previous,
        final_run_id=last_processed, examined_new_runs=examined,
        dispatched_run_ids=dispatched, ignored_run_ids=ignored,
        bootstrap_primed=False, quarantined_run_ids=quarantined,
        pending_run_ids=pending, wakeup_is_success_evidence=False,
        fresh_mcp_reobservation_required=True,
    )


def _self_check() -> None:
    sha = "a" * 40
    good_run = {
        "id": 100,
        "name": SOURCE_WORKFLOW_NAME,
        "event": "pull_request",
        "status": "completed",
        "conclusion": "success",
        "head_sha": sha,
        "head_branch": "formal/test",
        "head_repository": {"full_name": SOURCE_REPO},
        "pull_requests": [
            {
                "number": 2018,
                "base": {"ref": CANONICAL_BASE},
                "head": {"sha": sha, "repo": {"full_name": SOURCE_REPO}},
            }
        ],
    }
    classification, blockers = classify_run(good_run)
    assert classification == "candidate" and blockers == []
    good_jobs = {
        "jobs": [
            {
                "name": REQUIRED_JOB,
                "status": "completed",
                "conclusion": "success",
                "steps": [
                    {"name": REQUIRED_STEP, "status": "completed", "conclusion": "success"}
                ],
            }
        ]
    }
    ready, blockers, evidence = validate_exact_job_and_step(good_jobs)
    assert ready and blockers == [] and evidence["step"]["conclusion"] == "success"
    skipped_jobs = {
        "jobs": [
            {
                "name": REQUIRED_JOB,
                "status": "completed",
                "conclusion": "success",
                "steps": [
                    {"name": REQUIRED_STEP, "status": "completed", "conclusion": "skipped"}
                ],
            }
        ]
    }
    ready, blockers, _ = validate_exact_job_and_step(skipped_jobs)
    assert ready and blockers == []
    wrong_base = dict(good_run)
    wrong_base["pull_requests"] = [
        {"number": 1, "base": {"ref": "main"}, "head": {"repo": {"full_name": SOURCE_REPO}}}
    ]
    classification, reasons = classify_run(wrong_base)
    assert classification == "ignored" and "canonical_base_mismatch" in reasons
    forked = dict(good_run)
    forked["head_repository"] = {"full_name": "someone/fork"}
    classification, reasons = classify_run(forked)
    assert classification == "ignored" and "head_repository_not_source_repository" in reasons
    missing_step = {
        "jobs": [
            {
                "name": REQUIRED_JOB,
                "status": "completed",
                "conclusion": "success",
                "steps": [],
            }
        ]
    }
    ready, blockers, _ = validate_exact_job_and_step(missing_step)
    assert not ready and "required_step_cardinality:0" in blockers
    failed_run = dict(good_run)
    failed_run["conclusion"] = "failure"
    classification, blockers = classify_run(failed_run)
    assert classification == "candidate" and blockers == []
    payload = make_dispatch_payload(failed_run)["completion"]
    assert payload["wakeup_is_success_evidence"] is False
    assert payload["fresh_mcp_reobservation_required"] is True
    assert payload["required_step_names"] == [REQUIRED_STEP]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-check", action="store_true")
    parser.add_argument(
        "--state-file",
        default=".kuuos/state/kuuos_mgap_ci_completion_poller_v1_2.json",
    )
    parser.add_argument("--target-repo", default=os.environ.get("GITHUB_REPOSITORY", ""))
    parser.add_argument("--dispatch-token-env", default="GITHUB_TOKEN")
    parser.add_argument("--summary-file")
    parser.add_argument("--durable-state", action="store_true")
    args = parser.parse_args()

    if args.self_check:
        _self_check()
        print("KUUOS_GITHUB_PUBLIC_CI_COMPLETION_POLLER_V1_2_SELF_CHECK_OK")
        return 0

    token = os.environ.get(args.dispatch_token_env, "")
    state_store = None
    if args.durable_state:
        if args.target_repo != os.environ.get("GITHUB_REPOSITORY"):
            raise RuntimeError("durable_state_target_must_be_current_repository")
        if __package__:
            from .kuuos_ci_poller_state import GitHubStateStore
        else:
            from kuuos_ci_poller_state import GitHubStateStore
        state_store = GitHubStateStore(args.target_repo, token)
    summary = poll_once(
        state_file=pathlib.Path(args.state_file),
        target_repo=args.target_repo,
        dispatch_token=token,
        state_store=state_store,
    )
    payload = asdict(summary)
    rendered = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)
    print(rendered)
    if args.summary_file:
        path = pathlib.Path(args.summary_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
