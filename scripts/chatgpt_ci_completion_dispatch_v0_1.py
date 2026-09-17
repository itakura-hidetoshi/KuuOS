#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import time
import urllib.request
from dataclasses import dataclass
from typing import Any, Callable, Mapping, Protocol

EVENT_TYPE = "chatgpt_ci_completion_dispatch_v0_1"
PRODUCER = "repository_dispatch_v0_1"
PACKET_VERSION = "chatgpt_ci_completion_push_v0_3"
_SHA40 = re.compile(r"^[0-9a-f]{40}$")
WORKFLOWS = {
    "itakura-hidetoshi/KuuOS": "KuuOS PR Governance Gate",
    "itakura-hidetoshi/4d-mass-gap": "PR Lean Fast Check",
}
DEFAULT_DELAYS = (0.0, 1.0, 2.0, 4.0, 8.0, 16.0, 30.0)


@dataclass(frozen=True)
class DispatchIdentity:
    repository: str
    pull_request: int
    run_id: int
    run_attempt: int
    head_sha: str
    head_branch: str
    workflow: str


class GitHubApiLike(Protocol):
    def get_workflow_run(self, repository: str, run_id: int) -> dict[str, Any]: ...
    def get_pull_request(self, repository: str, pr_number: int) -> dict[str, Any]: ...
    def list_issue_comments(self, repository: str, pr_number: int) -> list[dict[str, Any]]: ...
    def create_issue_comment(self, repository: str, pr_number: int, body: str) -> dict[str, Any]: ...


def _positive_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return None
    return parsed if parsed > 0 else None


def validate_dispatch_payload(
    event: Mapping[str, Any], repository: str
) -> DispatchIdentity | None:
    if event.get("action") != EVENT_TYPE:
        return None
    raw = event.get("client_payload")
    if not isinstance(raw, Mapping):
        return None
    expected_workflow = WORKFLOWS.get(repository)
    if expected_workflow is None:
        return None
    if raw.get("repository") != repository or raw.get("workflow") != expected_workflow:
        return None
    pull_request = _positive_int(raw.get("pull_request"))
    run_id = _positive_int(raw.get("run_id"))
    run_attempt = _positive_int(raw.get("run_attempt"))
    head_sha = str(raw.get("head_sha", "")).lower()
    head_branch = str(raw.get("head_branch", ""))
    if pull_request is None or run_id is None or run_attempt is None:
        return None
    if _SHA40.fullmatch(head_sha) is None or not head_branch:
        return None
    return DispatchIdentity(
        repository=repository,
        pull_request=pull_request,
        run_id=run_id,
        run_attempt=run_attempt,
        head_sha=head_sha,
        head_branch=head_branch,
        workflow=expected_workflow,
    )


def _run_identity_matches(identity: DispatchIdentity, run: Mapping[str, Any]) -> bool:
    return (
        _positive_int(run.get("id")) == identity.run_id
        and _positive_int(run.get("run_attempt")) == identity.run_attempt
        and str(run.get("name", "")) == identity.workflow
        and str(run.get("event", "")) == "pull_request"
        and str(run.get("head_sha", "")).lower() == identity.head_sha
    )


def verify_run(identity: DispatchIdentity, run: Mapping[str, Any]) -> bool:
    return (
        _run_identity_matches(identity, run)
        and str(run.get("status", "")) == "completed"
        and run.get("conclusion") is not None
    )


def producer_marker(identity: DispatchIdentity) -> str:
    return (
        "<!-- CHATGPT_CI_COMPLETION_PUSH_V0_1 "
        f"producer={PRODUCER} run_id={identity.run_id} "
        f"attempt={identity.run_attempt} pr={identity.pull_request} -->"
    )


def build_comment(
    identity: DispatchIdentity,
    run: Mapping[str, Any],
    *,
    polling_used: bool,
) -> str:
    packet = {
        "version": PACKET_VERSION,
        "repository": identity.repository,
        "pull_request": identity.pull_request,
        "workflow": identity.workflow,
        "run_id": identity.run_id,
        "run_attempt": identity.run_attempt,
        "status": run.get("status"),
        "conclusion": run.get("conclusion"),
        "head_sha": identity.head_sha,
        "head_branch": identity.head_branch,
        "run_url": run.get("html_url"),
        "updated_at": run.get("updated_at"),
        "producer": PRODUCER,
        "event_is_wakeup_signal_only": True,
        "fresh_mcp_reobservation_required": True,
        "polling_used": bool(polling_used),
    }
    return (
        producer_marker(identity)
        + "\n\nChatGPT CI completion secondary wake-up signal. "
        "This comment is not CI truth and grants no merge/write authority.\n\n"
        "Fresh-reobserve this exact run through GitHub MCP before governed action.\n\n"
        "```json\n"
        + json.dumps(packet, ensure_ascii=False, indent=2, sort_keys=True)
        + "\n```\n"
    )


def _pr_head_matches(identity: DispatchIdentity, pr: Mapping[str, Any]) -> bool:
    head = pr.get("head")
    if not isinstance(head, Mapping):
        return False
    repo = head.get("repo")
    if not isinstance(repo, Mapping):
        return False
    return (
        _positive_int(pr.get("number")) == identity.pull_request
        and str(head.get("sha", "")).lower() == identity.head_sha
        and str(repo.get("full_name", "")) == identity.repository
    )


def process_event(
    event: Mapping[str, Any],
    github: GitHubApiLike,
    *,
    repository: str,
    sleep_fn: Callable[[float], None] = time.sleep,
    delays: tuple[float, ...] = DEFAULT_DELAYS,
) -> dict[str, Any]:
    identity = validate_dispatch_payload(event, repository)
    if identity is None:
        return {"outcome": "ignored"}
    if not delays:
        delays = (0.0,)

    terminal: Mapping[str, Any] | None = None
    reads = 0
    for delay in delays:
        if delay > 0:
            sleep_fn(delay)
        observed = github.get_workflow_run(identity.repository, identity.run_id)
        reads += 1
        if not _run_identity_matches(identity, observed):
            return {
                "outcome": "identity_mismatch",
                "run_id": identity.run_id,
                "run_attempt": identity.run_attempt,
                "head_sha": identity.head_sha,
            }
        if str(observed.get("status", "")) == "completed":
            if observed.get("conclusion") is None:
                return {"outcome": "terminal_conclusion_missing"}
            terminal = observed
            break

    polling_used = reads > 1
    if terminal is None:
        return {
            "outcome": "nonterminal_exhausted",
            "run_id": identity.run_id,
            "run_attempt": identity.run_attempt,
            "head_sha": identity.head_sha,
            "polling_used": polling_used,
        }

    pr = github.get_pull_request(identity.repository, identity.pull_request)
    if not _pr_head_matches(identity, pr):
        return {
            "outcome": "stale_pr_head",
            "run_id": identity.run_id,
            "run_attempt": identity.run_attempt,
            "head_sha": identity.head_sha,
            "polling_used": polling_used,
        }

    marker = producer_marker(identity)
    comments = github.list_issue_comments(identity.repository, identity.pull_request)
    for item in comments:
        if isinstance(item, Mapping) and marker in str(item.get("body", "")):
            return {
                "outcome": "deduplicated",
                "run_id": identity.run_id,
                "run_attempt": identity.run_attempt,
                "head_sha": identity.head_sha,
                "polling_used": polling_used,
            }

    body = build_comment(identity, terminal, polling_used=polling_used)
    created = github.create_issue_comment(
        identity.repository, identity.pull_request, body
    )
    return {
        "outcome": "comment_created",
        "run_id": identity.run_id,
        "run_attempt": identity.run_attempt,
        "head_sha": identity.head_sha,
        "polling_used": polling_used,
        "comment_id": created.get("id"),
    }


class GitHubApi:
    def __init__(self, token: str):
        self.headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "ChatGPT-CI-Completion-Dispatch-v0.1",
        }

    def _request(
        self,
        url: str,
        *,
        data: bytes | None = None,
        method: str = "GET",
    ) -> Any:
        headers = dict(self.headers)
        if data is not None:
            headers["Content-Type"] = "application/json"
        request = urllib.request.Request(
            url, data=data, headers=headers, method=method
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            if response.status == 204:
                return None
            return json.load(response)

    def get_workflow_run(self, repository: str, run_id: int) -> dict[str, Any]:
        result = self._request(
            f"https://api.github.com/repos/{repository}/actions/runs/{run_id}"
        )
        return result if isinstance(result, dict) else {}

    def get_pull_request(
        self, repository: str, pr_number: int
    ) -> dict[str, Any]:
        result = self._request(
            f"https://api.github.com/repos/{repository}/pulls/{pr_number}"
        )
        return result if isinstance(result, dict) else {}

    def list_issue_comments(
        self, repository: str, pr_number: int
    ) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        page = 1
        while True:
            result = self._request(
                f"https://api.github.com/repos/{repository}/issues/{pr_number}/comments"
                f"?per_page=100&page={page}"
            )
            if not isinstance(result, list):
                break
            out.extend(item for item in result if isinstance(item, dict))
            if len(result) < 100:
                break
            page += 1
        return out

    def create_issue_comment(
        self, repository: str, pr_number: int, body: str
    ) -> dict[str, Any]:
        data = json.dumps({"body": body}, ensure_ascii=False).encode("utf-8")
        result = self._request(
            f"https://api.github.com/repos/{repository}/issues/{pr_number}/comments",
            data=data,
            method="POST",
        )
        return result if isinstance(result, dict) else {}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--event", required=True)
    parser.add_argument(
        "--repository", default=os.environ.get("GITHUB_REPOSITORY", "")
    )
    args = parser.parse_args()

    token = os.environ.get("GH_TOKEN", "")
    if not token:
        raise SystemExit("GH_TOKEN is required")
    with open(args.event, "r", encoding="utf-8") as handle:
        event = json.load(handle)
    if not isinstance(event, Mapping):
        raise SystemExit("event must be a JSON object")

    result = process_event(
        event,
        GitHubApi(token),
        repository=args.repository,
    )
    print(
        "CHATGPT_CI_COMPLETION_DISPATCH_RESULT "
        + json.dumps(result, sort_keys=True)
    )
    return 0 if result.get("outcome") in {
        "ignored",
        "deduplicated",
        "comment_created",
        "stale_pr_head",
    } else 2


if __name__ == "__main__":
    raise SystemExit(main())
