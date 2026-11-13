#!/usr/bin/env python3
"""Create a fail-closed *live GitHub PR HEAD* manifest for KuuOS full-source Lean repair.

Only GitHub read APIs; no git/gh CLI, source edits, proof generation, or PR writes.
The local full-source scanner independently verifies every downloaded Git blob.
A CI log can be attached only when its completed job is bound to the same HEAD.
"""
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
from collections.abc import Callable, Mapping
from typing import Any

REPO = "itakura-hidetoshi/KuuOS"
ROOT_URL = "https://api.github.com/repos/" + REPO
HEX40 = re.compile(r"^[0-9a-f]{40}$")
MAX_FILES = 500
MAX_LEAN = 150
MAX_LOG_BYTES = 10_000_000


class SnapshotObstruction(RuntimeError):
    pass


def sha40(value: Any) -> bool:
    return isinstance(value, str) and HEX40.fullmatch(value) is not None


def checked_pr(snapshot: Mapping, pr_number: int) -> tuple[str, str]:
    if snapshot.get("number") != pr_number or snapshot.get("state") != "open":
        raise SnapshotObstruction("PR identity or open status mismatch")
    head, base = snapshot.get("head"), snapshot.get("base")
    if not isinstance(head, Mapping) or not isinstance(base, Mapping):
        raise SnapshotObstruction("missing PR head/base")
    h, b = head.get("sha"), base.get("sha")
    if not sha40(h) or not sha40(b):
        raise SnapshotObstruction("missing exact PR source HEAD or base SHA")
    repo = head.get("repo")
    if not isinstance(repo, Mapping) or repo.get("full_name") != REPO:
        raise SnapshotObstruction("source repo mismatch")
    return h, b


def live_plan(pr_number: int, get_json: Callable[[str], Any]) -> tuple[dict, dict]:
    first = get_json("/pulls/" + str(pr_number))
    head, base = checked_pr(first, pr_number)
    all_files: list[dict] = []
    for page in range(1, 7):
        found = get_json(f"/pulls/{pr_number}/files?per_page=100&page={page}")
        if not isinstance(found, list):
            raise SnapshotObstruction("PR files API returned non-list")
        if not found:
            break
        all_files.extend(found)
        if len(all_files) > MAX_FILES:
            raise SnapshotObstruction("PR file list exceeds fixed audit budget")
        if len(found) < 100:
            break
    else:
        raise SnapshotObstruction("PR file pagination exhaustion")
    if len(all_files) != first.get("changed_files"):
        raise SnapshotObstruction("PR changed_files count differs from complete paginated listing")
    filenames = [x.get("filename") for x in all_files if isinstance(x, Mapping)]
    if len(filenames) != len(set(filenames)) or any(not isinstance(x, str) for x in filenames):
        raise SnapshotObstruction("duplicate/invalid PR file names")
    lean_files = sorted(
        (x for x in all_files
         if x.get("filename", "").startswith("formal/")
         and x["filename"].endswith(".lean")),
        key=lambda x: x["filename"],
    )
    if not lean_files or len(lean_files) > MAX_LEAN:
        raise SnapshotObstruction("no changed Lean source or target limit exceeded")
    targets = []
    for item in lean_files:
        path = item["filename"]
        if item.get("status") not in ("added", "modified") or not sha40(item.get("sha")):
            raise SnapshotObstruction("unsupported Lean change status or missing blob: " + path)
        if ".." in pathlib.PurePosixPath(path).parts:
            raise SnapshotObstruction("unsafe source path")
        targets.append({"path": path, "git_blob_sha": item["sha"]})
    last = get_json("/pulls/" + str(pr_number))
    second_head, second_base = checked_pr(last, pr_number)
    if (head, base) != (second_head, second_base):
        raise SnapshotObstruction("PR head/base moved while collecting exact blob manifest")
    plan = {
        "schema_version": "kuuos-lean-fullsource-v1",
        "source_head": head, "scope": "all-changed",
        "changed_lean_files": [x["path"] for x in targets],
        "targets": targets, "api_probes": [],
    }
    metadata = {
        "status": "EXACT_GITHUB_PR_FILE_MANIFEST_OBSERVED",
        "repo": REPO, "pr_number": pr_number,
        "source_head": head, "source_base": base,
        "pr_files_total": len(all_files), "changed_lean_count": len(targets),
        "head_rechecked_after_manifest": True,
        "blob_content_verified_locally": False,
        "full_import_closure_verified": False,
        "ci_run": None, "ci_log_status": "NO_DATA",
        "proof_certified": False, "github_write_performed": False,
    }
    return plan, metadata


def attach_ci_log(meta: dict, get_json: Callable[[str], Any],
                  get_log: Callable[[int], str]) -> str | None:
    """Bound a compiler log to a *completed exact-HEAD* workflow/job."""
    sha = meta["source_head"]
    listing = get_json(f"/actions/runs?head_sha={sha}&event=pull_request&per_page=100")
    if not isinstance(listing, Mapping) or not isinstance(listing.get("workflow_runs"), list):
        raise SnapshotObstruction("workflow runs API response unavailable")
    candidates = sorted(
        (x for x in listing["workflow_runs"] if
         x.get("name") == "KuuOS PR Governance Gate" and
         x.get("head_sha") == sha),
        key=lambda x: (x.get("created_at") or "", x.get("run_attempt", 0)),
        reverse=True,
    )
    if not candidates:
        meta["ci_log_status"] = "NO_DATA_NO_EXACT_HEAD_GOVERNANCE_RUN"
        return None
    run = candidates[0]
    if not isinstance(run.get("id"), int) or run.get("status") != "completed":
        meta["ci_log_status"] = "NO_DATA_LATEST_EXACT_HEAD_RUN_NOT_COMPLETED"
        return None
    jobs = get_json(f"/actions/runs/{run['id']}/jobs?per_page=100")
    if not isinstance(jobs, Mapping) or not isinstance(jobs.get("jobs"), list):
        raise SnapshotObstruction("jobs response missing")
    matches = [x for x in jobs["jobs"] if x.get("name") == "Strict Lean formal validation"]
    if len(matches) != 1:
        meta["ci_log_status"] = "NO_DATA_STRICT_LEAN_JOB_MISSING_OR_AMBIGUOUS"
        return None
    job = matches[0]
    if not isinstance(job.get("id"), int) or job.get("status") != "completed":
        meta["ci_log_status"] = "NO_DATA_STRICT_LEAN_JOB_INCOMPLETE"
        return None
    meta["ci_run"] = {
        "run_id": run["id"], "job_id": job["id"],
        "run_conclusion": run.get("conclusion"),
        "strict_job_conclusion": job.get("conclusion"),
        "source_head": sha, "run_attempt": run.get("run_attempt"),
    }
    log = get_log(job["id"])
    if not isinstance(log, str) or not log.strip() or len(log.encode()) > MAX_LOG_BYTES:
        raise SnapshotObstruction("job log missing or over max byte budget")
    meta["ci_log_status"] = "EXACT_HEAD_COMPLETED_STRICT_LEAN_LOG_CAPTURED_NOT_PROOF_CERTIFIED"
    return log


def github_json(path: str, token: str) -> Any:
    if not path.startswith("/") or "//" in path:
        raise SnapshotObstruction("invalid GitHub API path")
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = "Bearer " + token
    req = urllib.request.Request(ROOT_URL + path, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=35) as response:
            return json.load(response)
    except (urllib.error.URLError, json.JSONDecodeError) as exc:
        raise SnapshotObstruction("GitHub metadata request failed: " + type(exc).__name__) from exc


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def github_job_log(job_id: int, token: str) -> str:
    # Do not leak the API token to a secondary log-storage redirect host.
    req = urllib.request.Request(
        ROOT_URL + f"/actions/jobs/{job_id}/logs",
        headers={"Authorization": "Bearer " + token,
                 "Accept": "application/vnd.github+json"},
    )
    redirect_url = None
    try:
        with urllib.request.build_opener(NoRedirect()).open(req, timeout=35) as response:
            body = response.read(MAX_LOG_BYTES + 1)
    except urllib.error.HTTPError as exc:
        if exc.code not in (302, 303, 307, 308):
            raise SnapshotObstruction("GitHub logs API refused request") from exc
        redirect_url = exc.headers.get("Location")
    if redirect_url:
        parsed = urllib.parse.urlparse(redirect_url)
        host = (parsed.hostname or "").lower()
        if parsed.scheme != "https" or not (
            host.endswith(".actions.githubusercontent.com")
            or host == "pipelines.actions.githubusercontent.com"
            or host.endswith(".blob.core.windows.net")
        ):
            raise SnapshotObstruction("untrusted logs download redirect")
        # Signed, temporary URL: intentionally no Authorization header.
        with urllib.request.urlopen(redirect_url, timeout=60) as response:
            body = response.read(MAX_LOG_BYTES + 1)
    if len(body) > MAX_LOG_BYTES:
        raise SnapshotObstruction("GitHub log exceeded exact read byte limit")
    try:
        return body.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SnapshotObstruction("GitHub log is not UTF-8") from exc


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--pr", type=int, default=3522)
    p.add_argument("--output-dir", required=True, type=pathlib.Path)
    p.add_argument("--github-output", type=pathlib.Path)
    p.add_argument("--include-ci-log", action="store_true")
    p.add_argument("--verify-head")
    opts = p.parse_args()
    token = os.environ.get("GITHUB_TOKEN", "")
    try:
        if opts.verify_head is not None:
            actual, _ = checked_pr(github_json("/pulls/" + str(opts.pr), token), opts.pr)
            if actual != opts.verify_head:
                raise SnapshotObstruction("HEAD_DRIFT_OBSTRUCTION: expected " + opts.verify_head +
                                          " observed " + actual)
            print("KUUOS_CURRENT_PR_HEAD_RECHECK_MATCH " + actual)
            return 0
        output = opts.output_dir.resolve()
        if output.exists() and any(output.iterdir()):
            raise SnapshotObstruction("output already contains data; do not overwrite")
        plan, meta = live_plan(opts.pr, lambda path: github_json(path, token))
        log = (attach_ci_log(meta, lambda path: github_json(path, token),
                             lambda job_id: github_job_log(job_id, token))
               if opts.include_ci_log else None)
        output.mkdir(parents=True, exist_ok=True)
        (output / "plan.json").write_text(json.dumps(plan, indent=2) + "\n")
        if log is not None:
            (output / "source_bound_ci.log").write_text(log)
        (output / "live_head_receipt.json").write_text(json.dumps(meta, indent=2) + "\n")
        if opts.github_output:
            with opts.github_output.open("a") as fd:
                fd.write(f"source_head={meta['source_head']}\n")
                fd.write(f"changed_lean_count={meta['changed_lean_count']}\n")
                fd.write(f"ci_log_available={'true' if log is not None else 'false'}\n")
        print(json.dumps({
            "status": meta["status"], "source_head": meta["source_head"],
            "targets": meta["changed_lean_count"], "ci_log_status": meta["ci_log_status"],
            "proof_certified": False,
        }))
        return 0
    except (SnapshotObstruction, OSError, ValueError) as exc:
        print("KUUOS_LIVE_HEAD_OBSTRUCTION: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
