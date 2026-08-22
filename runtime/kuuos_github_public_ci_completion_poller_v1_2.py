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
        raise RuntimeError(f"source_github_api_read_failed:{url}:{exc}") from exc
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
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as exc:
        raise RuntimeError(f"self_dispatch_failed:{exc}") from exc


def _load_state(path: pathlib.Path) -> int | None:
    if not path.is_file():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    if not isinstance(payload, dict):
        return None
    value = _i(payload.get("last_processed_run_id"), -1)
    return value if value >= 0 else None


def _save_state(path: pathlib.Path, run_id: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(
        json.dumps(
            {
                "version": VERSION,
                "last_processed_run_id": int(run_id),
                "source_repo": SOURCE_REPO,
                "source_workflow": SOURCE_WORKFLOW_NAME,
                "canonical_base": CANONICAL_BASE,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
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
    return {
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


def _workflow_runs_url(source_repo: str, workflow_file: str) -> str:
    encoded = urllib.parse.quote(workflow_file, safe="")
    return (
        f"https://api.github.com/repos/{source_repo}/actions/workflows/{encoded}/runs"
        "?event=pull_request&status=completed&per_page=50"
    )


def _jobs_url(source_repo: str, run_id: int) -> str:
    return f"https://api.github.com/repos/{source_repo}/actions/runs/{run_id}/jobs?filter=latest&per_page=100"


def poll_once(
    *,
    state_file: pathlib.Path,
    target_repo: str,
    dispatch_token: str,
    source_repo: str = SOURCE_REPO,
    workflow_file: str = SOURCE_WORKFLOW_FILE,
) -> PollSummary:
    runs_payload = _http_json(_workflow_runs_url(source_repo, workflow_file))
    raw_runs = runs_payload.get("workflow_runs")
    runs = [dict(run) for run in raw_runs if isinstance(run, Mapping)] if isinstance(raw_runs, list) else []
    runs.sort(key=lambda run: _i(run.get("id"), 0))
    previous = _load_state(state_file)
    if previous is None:
        latest = max((_i(run.get("id"), 0) for run in runs), default=0)
        _save_state(state_file, latest)
        return PollSummary(
            VERSION,
            "KUUOS_PUBLIC_CI_POLLER_BOOTSTRAP_PRIMED",
            source_repo,
            SOURCE_WORKFLOW_NAME,
            CANONICAL_BASE,
            0,
            latest,
            0,
            [],
            [],
            True,
            False,
            True,
        )

    last_processed = previous
    dispatched: list[int] = []
    ignored: list[int] = []
    examined = 0
    for run in runs:
        run_id = _i(run.get("id"), 0)
        if run_id <= previous:
            continue
        examined += 1
        classification, _ = classify_run(run, source_repo=source_repo)
        if classification == "ignored":
            ignored.append(run_id)
            last_processed = max(last_processed, run_id)
            continue
        jobs_payload = _http_json(_jobs_url(source_repo, run_id))
        ready, blockers, _ = validate_exact_job_and_step(jobs_payload)
        if not ready:
            raise RuntimeError(
                "source_exact_job_step_gate_blocked:"
                + str(run_id)
                + ":"
                + ",".join(blockers)
            )
        payload = make_dispatch_payload(run)
        _post_self_dispatch(target_repo, dispatch_token, payload)
        dispatched.append(run_id)
        last_processed = max(last_processed, run_id)

    _save_state(state_file, last_processed)
    return PollSummary(
        VERSION,
        "KUUOS_PUBLIC_CI_POLLER_READY",
        source_repo,
        SOURCE_WORKFLOW_NAME,
        CANONICAL_BASE,
        previous,
        last_processed,
        examined,
        dispatched,
        ignored,
        False,
        False,
        True,
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
    payload = make_dispatch_payload(failed_run)
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
    args = parser.parse_args()

    if args.self_check:
        _self_check()
        print("KUUOS_GITHUB_PUBLIC_CI_COMPLETION_POLLER_V1_2_SELF_CHECK_OK")
        return 0

    token = os.environ.get(args.dispatch_token_env, "")
    summary = poll_once(
        state_file=pathlib.Path(args.state_file),
        target_repo=args.target_repo,
        dispatch_token=token,
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
