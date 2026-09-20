#!/usr/bin/env python3
import json
import os
import urllib.request
from typing import Any


def resolve_pr_numbers(
    event_pull_requests: list[dict[str, Any]],
    associated_pull_requests: list[dict[str, Any]],
    head_sha: str,
    repository: str,
) -> list[int]:
    direct = {
        int(item["number"])
        for item in event_pull_requests
        if isinstance(item, dict)
        and isinstance(item.get("number"), int)
        and int(item["number"]) > 0
    }
    if direct:
        return sorted(direct)

    fallback: set[int] = set()
    for item in associated_pull_requests:
        if not isinstance(item, dict):
            continue
        number = item.get("number")
        head = item.get("head") or {}
        head_repo = head.get("repo") or {}
        if not isinstance(number, int) or number <= 0:
            continue
        if head.get("sha") != head_sha:
            continue
        if head_repo.get("full_name") != repository:
            continue
        fallback.add(number)
    return sorted(fallback)


def request_json(
    url: str,
    headers: dict[str, str],
    *,
    data: bytes | None = None,
    method: str = "GET",
) -> Any:
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def main() -> int:
    repository = os.environ["REPOSITORY"]
    run_id = os.environ["RUN_ID"]
    run_attempt = os.environ["RUN_ATTEMPT"]
    head_sha = os.environ["HEAD_SHA"]
    token = os.environ["GH_TOKEN"]
    user_agent = os.environ.get(
        "USER_AGENT", "ChatGPT-CI-Completion-Push-v0.2"
    )

    event_pull_requests = json.loads(
        os.environ.get("EVENT_PULL_REQUESTS_JSON", "[]")
    )
    if not isinstance(event_pull_requests, list):
        event_pull_requests = []

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": user_agent,
    }

    associated_pull_requests: list[dict[str, Any]] = []
    resolution_source = "workflow_run.pull_requests"
    if not event_pull_requests:
        resolution_source = "commit_association"
        associated_url = (
            f"https://api.github.com/repos/{repository}/commits/{head_sha}/pulls?per_page=100"
        )
        associated = request_json(associated_url, headers)
        if isinstance(associated, list):
            associated_pull_requests = associated

    pr_numbers = resolve_pr_numbers(
        event_pull_requests,
        associated_pull_requests,
        head_sha=head_sha,
        repository=repository,
    )
    if not pr_numbers:
        print(
            "CHATGPT_CI_COMPLETION_PUSH_NO_PR "
            f"run_id={run_id} attempt={run_attempt} head_sha={head_sha} "
            f"source={resolution_source}"
        )
        return 0

    for pr_number in pr_numbers:
        marker = (
            "<!-- CHATGPT_CI_COMPLETION_PUSH_V0_1 "
            f"run_id={run_id} attempt={run_attempt} pr={pr_number} -->"
        )
        packet = {
            "version": "chatgpt_ci_completion_push_v0_2",
            "repository": repository,
            "pull_request": pr_number,
            "workflow": os.environ["WORKFLOW_NAME"],
            "run_id": int(run_id),
            "run_attempt": int(run_attempt),
            "status": os.environ["RUN_STATUS"],
            "conclusion": os.environ["RUN_CONCLUSION"],
            "head_sha": head_sha,
            "head_branch": os.environ["HEAD_BRANCH"],
            "run_url": os.environ["RUN_URL"],
            "updated_at": os.environ["UPDATED_AT"],
            "pr_resolution_source": resolution_source,
            "event_is_wakeup_signal_only": True,
            "fresh_mcp_reobservation_required": True,
            "polling_required": False,
        }
        body = (
            f"{marker}\n\n"
            "ChatGPT CI completion wake-up signal. This comment is not CI truth and grants no merge/write authority.\n\n"
            "After webhook activation, fresh-reobserve this exact workflow run once through GitHub MCP, verify the exact head SHA and terminal job/step result, then continue. Do not poll the run waiting for completion.\n\n"
            "```json\n"
            + json.dumps(packet, ensure_ascii=False, indent=2, sort_keys=True)
            + "\n```\n"
        )

        comments_url = (
            f"https://api.github.com/repos/{repository}/issues/{pr_number}/comments"
        )
        found = False
        page = 1
        while True:
            comments = request_json(
                f"{comments_url}?per_page=100&page={page}", headers
            )
            if not isinstance(comments, list):
                break
            if any(
                marker in (item.get("body") or "")
                for item in comments
                if isinstance(item, dict)
            ):
                found = True
                break
            if len(comments) < 100:
                break
            page += 1

        if found:
            print(
                "CHATGPT_CI_COMPLETION_PUSH_DEDUPLICATED "
                f"pr={pr_number} run_id={run_id} attempt={run_attempt} "
                f"source={resolution_source}"
            )
            continue

        payload = json.dumps({"body": body}, ensure_ascii=False).encode("utf-8")
        created = request_json(
            comments_url,
            {**headers, "Content-Type": "application/json"},
            data=payload,
            method="POST",
        )
        created_id = created.get("id") if isinstance(created, dict) else None
        print(
            "CHATGPT_CI_COMPLETION_PUSH_CREATED "
            f"pr={pr_number} comment={created_id} run_id={run_id} "
            f"attempt={run_attempt} conclusion={packet['conclusion']} "
            f"source={resolution_source}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
