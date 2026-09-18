#!/usr/bin/env python3
from __future__ import annotations

import base64
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from scripts.chatgpt_ci_completion_push_v0_2 import resolve_pr_numbers


def receipt_path(
    *,
    pull_request: int,
    run_id: int,
    run_attempt: int,
    head_sha: str,
) -> str:
    return (
        f"ci-events/{pull_request}-{run_id}-{run_attempt}-"
        f"{head_sha[:12]}.json"
    )


def build_receipt(
    *,
    repository: str,
    pull_request: int,
    workflow: str,
    run_id: int,
    run_attempt: int,
    status: str,
    conclusion: str,
    head_sha: str,
    head_branch: str,
    run_url: str,
    updated_at: str,
) -> dict[str, Any]:
    return {
        "version": "chatgpt_ci_commit_wakeup_v0_1",
        "source_repository": repository,
        "source_pull_request": pull_request,
        "workflow": workflow,
        "run_id": run_id,
        "run_attempt": run_attempt,
        "status": status,
        "conclusion": conclusion,
        "head_sha": head_sha,
        "head_branch": head_branch,
        "run_url": run_url,
        "updated_at": updated_at,
        "event_is_wakeup_signal_only": True,
        "fresh_mcp_reobservation_required": True,
        "merge_authority_granted": False,
        "write_authority_granted": False,
    }


def should_skip_source(
    *,
    pull_request: int,
    head_branch: str,
    inbox_pull_request: int,
    inbox_branch: str,
) -> bool:
    return pull_request == inbox_pull_request or head_branch == inbox_branch


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


def exists(url: str, headers: dict[str, str]) -> bool:
    try:
        request_json(url, headers)
        return True
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return False
        raise


def main() -> int:
    repository = os.environ["REPOSITORY"]
    token = os.environ["GH_TOKEN"]
    run_id = int(os.environ["RUN_ID"])
    run_attempt = int(os.environ["RUN_ATTEMPT"])
    head_sha = os.environ["HEAD_SHA"]
    head_branch = os.environ["HEAD_BRANCH"]
    inbox_branch = os.environ["INBOX_BRANCH"]
    inbox_pull_request = int(os.environ["INBOX_PULL_REQUEST"])
    user_agent = os.environ.get(
        "USER_AGENT", "KuuOS-ChatGPT-CI-Commit-Wakeup-v0.1"
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
    if not event_pull_requests:
        associated = request_json(
            f"https://api.github.com/repos/{repository}/commits/{head_sha}/pulls?per_page=100",
            headers,
        )
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
            "CHATGPT_CI_COMMIT_WAKEUP_NO_PR "
            f"run_id={run_id} attempt={run_attempt} head_sha={head_sha}"
        )
        return 0

    for pr_number in pr_numbers:
        if should_skip_source(
            pull_request=pr_number,
            head_branch=head_branch,
            inbox_pull_request=inbox_pull_request,
            inbox_branch=inbox_branch,
        ):
            print(
                "CHATGPT_CI_COMMIT_WAKEUP_SELF_SKIP "
                f"pr={pr_number} run_id={run_id} attempt={run_attempt}"
            )
            continue

        packet = build_receipt(
            repository=repository,
            pull_request=pr_number,
            workflow=os.environ["WORKFLOW_NAME"],
            run_id=run_id,
            run_attempt=run_attempt,
            status=os.environ["RUN_STATUS"],
            conclusion=os.environ["RUN_CONCLUSION"],
            head_sha=head_sha,
            head_branch=head_branch,
            run_url=os.environ["RUN_URL"],
            updated_at=os.environ["UPDATED_AT"],
        )
        path = receipt_path(
            pull_request=pr_number,
            run_id=run_id,
            run_attempt=run_attempt,
            head_sha=head_sha,
        )
        encoded_path = urllib.parse.quote(path, safe="/")
        branch_query = urllib.parse.quote(inbox_branch, safe="")
        contents_url = (
            f"https://api.github.com/repos/{repository}/contents/"
            f"{encoded_path}?ref={branch_query}"
        )
        if exists(contents_url, headers):
            print(
                "CHATGPT_CI_COMMIT_WAKEUP_DEDUPLICATED "
                f"pr={pr_number} run_id={run_id} attempt={run_attempt} path={path}"
            )
            continue

        payload = json.dumps(
            {
                "message": (
                    "Record CI completion wake-up "
                    f"for PR {pr_number} run {run_id} attempt {run_attempt}"
                ),
                "content": base64.b64encode(
                    (json.dumps(packet, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
                    .encode("utf-8")
                ).decode("ascii"),
                "branch": inbox_branch,
            },
            ensure_ascii=False,
        ).encode("utf-8")
        created = request_json(
            f"https://api.github.com/repos/{repository}/contents/{encoded_path}",
            {**headers, "Content-Type": "application/json"},
            data=payload,
            method="PUT",
        )
        commit_sha = (
            ((created or {}).get("commit") or {}).get("sha")
            if isinstance(created, dict)
            else None
        )
        print(
            "CHATGPT_CI_COMMIT_WAKEUP_CREATED "
            f"pr={pr_number} run_id={run_id} attempt={run_attempt} "
            f"path={path} commit={commit_sha}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
