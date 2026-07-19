#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import subprocess
from typing import Callable, Mapping, Sequence

from runtime.kuuos_codeai_autonomous_git_effect_execution_v0_1 import (
    GitEffectInvocation,
    PHASE_CREATE_PR,
    PHASE_LOCAL_COMMIT,
    PHASE_MARK_PR_READY,
    PHASE_MERGE,
    PHASE_PUSH,
)


@dataclass(frozen=True)
class CommandOutcome:
    returncode: int
    stdout: str
    stderr: str


CommandRunner = Callable[[Sequence[str], Path, Mapping[str, str], str | None, int], CommandOutcome]


def subprocess_runner(
    command: Sequence[str],
    cwd: Path,
    environment: Mapping[str, str],
    stdin: str | None,
    timeout_seconds: int,
) -> CommandOutcome:
    completed = subprocess.run(
        list(command),
        cwd=cwd,
        env=dict(environment),
        input=stdin,
        text=True,
        capture_output=True,
        timeout=timeout_seconds,
        check=False,
    )
    return CommandOutcome(completed.returncode, completed.stdout, completed.stderr)


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _empty_result(phase: str, *, adapter_id: str, adapter_session_id: str, epoch: int) -> dict:
    return {
        "adapter_id": adapter_id,
        "adapter_session_id": adapter_session_id,
        "effect_phase": phase,
        "status": "failed",
        "exit_code": 1,
        "command_count": 0,
        "stdout": "",
        "stderr": "",
        "completed_epoch": epoch,
        "local_commit_created": False,
        "local_commit_sha": "",
        "local_commit_parent_sha": "",
        "branch_pushed": False,
        "pushed_head_sha": "",
        "pull_request_created": False,
        "pull_request_number": 0,
        "pull_request_url_digest": "",
        "pull_request_draft": False,
        "pr_head_sha": "",
        "pr_base_branch": "",
        "pull_request_marked_ready": False,
        "merge_performed": False,
        "merged_head_sha": "",
        "merge_commit_sha": "",
        "force_push_performed": False,
        "remote_branch_deleted": False,
        "admin_merge_bypass_used": False,
        "deployment_performed": False,
        "secret_material_read": False,
        "token_material_emitted": False,
        "opaque_token_used": False,
        "exception_type": "",
    }


def _json(stdout: str) -> dict:
    value = json.loads(stdout)
    if not isinstance(value, dict):
        raise ValueError("expected JSON object from gh")
    return value


def build_subprocess_git_effect_adapter(
    *,
    workdir: str | Path,
    git_bin: str = "git",
    gh_bin: str = "gh",
    environment: Mapping[str, str] | None = None,
    runner: CommandRunner = subprocess_runner,
    adapter_id: str = "kuuos-codeai-git-subprocess-adapter-v0-1",
    adapter_session_id: str = "git-effect-adapter-session",
    completed_epoch: int = 0,
):
    root = Path(workdir).resolve()
    base_environment = {**os.environ, **dict(environment or {})}
    base_environment.update(
        {
            "GIT_TERMINAL_PROMPT": "0",
            "GH_PROMPT_DISABLED": "1",
            "GH_PAGER": "cat",
            "NO_COLOR": "1",
        }
    )

    def adapter(invocation: GitEffectInvocation) -> dict:
        result = _empty_result(
            invocation.effect_phase,
            adapter_id=adapter_id,
            adapter_session_id=adapter_session_id,
            epoch=completed_epoch,
        )
        outputs: list[str] = []
        errors: list[str] = []
        command_count = 0

        def run(command: Sequence[str], stdin: str | None = None) -> CommandOutcome:
            nonlocal command_count
            if command_count >= invocation.maximum_command_count:
                raise RuntimeError("command budget exhausted")
            command_count += 1
            outcome = runner(
                command,
                root,
                base_environment,
                stdin,
                invocation.maximum_timeout_seconds,
            )
            outputs.append(outcome.stdout)
            errors.append(outcome.stderr)
            total = sum(len(item.encode("utf-8")) for item in outputs + errors)
            if total > invocation.maximum_output_bytes:
                raise RuntimeError("output budget exhausted")
            if outcome.returncode != 0:
                raise RuntimeError(
                    f"command failed ({outcome.returncode}): {' '.join(command)}"
                )
            return outcome

        try:
            phase = invocation.effect_phase
            if phase == PHASE_LOCAL_COMMIT:
                before = run((git_bin, "rev-parse", "HEAD")).stdout.strip()
                if before != invocation.source_commit_sha:
                    raise RuntimeError("local HEAD does not match source commit")
                run((git_bin, "commit", "--no-gpg-sign", "-m", invocation.commit_message))
                after = run((git_bin, "rev-parse", "HEAD")).stdout.strip()
                parent = run((git_bin, "rev-parse", "HEAD^")).stdout.strip()
                result.update(
                    status="completed",
                    exit_code=0,
                    local_commit_created=True,
                    local_commit_sha=after,
                    local_commit_parent_sha=parent,
                )
            elif phase == PHASE_PUSH:
                head = run((git_bin, "rev-parse", "HEAD")).stdout.strip()
                if head != invocation.expected_head_sha:
                    raise RuntimeError("local HEAD does not match pinned push head")
                run(
                    (
                        git_bin,
                        "push",
                        "--porcelain",
                        invocation.remote_name,
                        f"HEAD:refs/heads/{invocation.head_branch}",
                    )
                )
                result.update(
                    status="completed",
                    exit_code=0,
                    branch_pushed=True,
                    pushed_head_sha=head,
                )
            elif phase == PHASE_CREATE_PR:
                if not invocation.opaque_token_use_allowed:
                    raise RuntimeError("opaque GitHub token use is not authorized")
                create = run(
                    (
                        gh_bin,
                        "pr",
                        "create",
                        "--repo",
                        invocation.repository_full_name,
                        "--base",
                        invocation.base_branch,
                        "--head",
                        invocation.head_branch,
                        "--title",
                        invocation.pull_request_title,
                        "--body-file",
                        "-",
                        "--draft",
                    ),
                    stdin=invocation.pull_request_body,
                )
                view = _json(
                    run(
                        (
                            gh_bin,
                            "pr",
                            "view",
                            invocation.head_branch,
                            "--repo",
                            invocation.repository_full_name,
                            "--json",
                            "number,url,isDraft,headRefOid,baseRefName",
                        )
                    ).stdout
                )
                url = str(view["url"])
                result.update(
                    status="completed",
                    exit_code=0,
                    pull_request_created=True,
                    pull_request_number=int(view["number"]),
                    pull_request_url_digest=_sha256_text(url),
                    pull_request_draft=bool(view["isDraft"]),
                    pr_head_sha=str(view["headRefOid"]),
                    pr_base_branch=str(view["baseRefName"]),
                    opaque_token_used=True,
                )
                if create.stdout.strip() and create.stdout.strip() != url:
                    errors.append("created PR URL differed from observed PR URL\n")
            elif phase == PHASE_MARK_PR_READY:
                if not invocation.opaque_token_use_allowed:
                    raise RuntimeError("opaque GitHub token use is not authorized")
                run(
                    (
                        gh_bin,
                        "pr",
                        "ready",
                        str(invocation.pull_request_number),
                        "--repo",
                        invocation.repository_full_name,
                    )
                )
                view = _json(
                    run(
                        (
                            gh_bin,
                            "pr",
                            "view",
                            str(invocation.pull_request_number),
                            "--repo",
                            invocation.repository_full_name,
                            "--json",
                            "number,isDraft,headRefOid,baseRefName",
                        )
                    ).stdout
                )
                result.update(
                    status="completed",
                    exit_code=0,
                    pull_request_number=int(view["number"]),
                    pull_request_draft=bool(view["isDraft"]),
                    pr_head_sha=str(view["headRefOid"]),
                    pr_base_branch=str(view["baseRefName"]),
                    pull_request_marked_ready=not bool(view["isDraft"]),
                    opaque_token_used=True,
                )
            elif phase == PHASE_MERGE:
                if not invocation.opaque_token_use_allowed:
                    raise RuntimeError("opaque GitHub token use is not authorized")
                method_flag = {
                    "merge": "--merge",
                    "squash": "--squash",
                    "rebase": "--rebase",
                }.get(invocation.merge_method)
                if method_flag is None:
                    raise RuntimeError("unsupported merge method")
                run(
                    (
                        gh_bin,
                        "pr",
                        "merge",
                        str(invocation.pull_request_number),
                        "--repo",
                        invocation.repository_full_name,
                        method_flag,
                        "--match-head-commit",
                        invocation.expected_head_sha,
                    )
                )
                view = _json(
                    run(
                        (
                            gh_bin,
                            "pr",
                            "view",
                            str(invocation.pull_request_number),
                            "--repo",
                            invocation.repository_full_name,
                            "--json",
                            "number,headRefOid,mergedAt,mergeCommit",
                        )
                    ).stdout
                )
                merge_commit = view.get("mergeCommit") or {}
                if not isinstance(merge_commit, dict):
                    raise RuntimeError("missing merge commit object")
                result.update(
                    status="completed",
                    exit_code=0,
                    pull_request_number=int(view["number"]),
                    merge_performed=bool(view.get("mergedAt")),
                    merged_head_sha=str(view["headRefOid"]),
                    merge_commit_sha=str(merge_commit.get("oid", "")),
                    opaque_token_used=True,
                )
            else:
                raise RuntimeError("unsupported effect phase")
        except BaseException as exc:
            result.update(
                status="failed",
                exit_code=1,
                exception_type=type(exc).__name__,
            )
            errors.append(str(exc) + "\n")

        result["command_count"] = command_count
        result["stdout"] = "".join(outputs)[: invocation.maximum_output_bytes]
        remaining = max(
            0,
            invocation.maximum_output_bytes - len(result["stdout"].encode("utf-8")),
        )
        encoded_error = "".join(errors).encode("utf-8")[:remaining]
        result["stderr"] = encoded_error.decode("utf-8", errors="ignore")
        return result

    return adapter


__all__ = [
    "CommandOutcome",
    "CommandRunner",
    "subprocess_runner",
    "build_subprocess_git_effect_adapter",
]
