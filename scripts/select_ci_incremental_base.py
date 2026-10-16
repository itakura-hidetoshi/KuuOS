#!/usr/bin/env python3
"""Optionally reuse completed non-Lean checks; uncertainty keeps full PR checks.

The mandatory exact base/head verification stays in ensure_ci_comparison.py.
This helper only reads Git and Actions history. It prints either one verified
ancestor SHA or nothing, never a replacement for a missing mandatory commit.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time

WORKFLOW = '.github/workflows/pr-governance-gate.yml'
IGNORED_JOBS = {
    'Select impacted audit checks', 'Strict Lean formal validation',
    'Governance gate and audit summary', 'Publish MCP Lean completion receipt',
    'Publish MCP CI completion receipt',
}


def full_sha(value: object) -> bool:
    return isinstance(value, str) and re.fullmatch(r'[0-9a-f]{40}', value) is not None and value != '0' * 40


def run_command(argv: list[str], deadline: float) -> subprocess.CompletedProcess[str]:
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise TimeoutError('optional history budget exhausted')
    return subprocess.run(argv, check=False, text=True, capture_output=True,
                          timeout=min(15.0, remaining))


def api_json(endpoint: str, fields: list[str], deadline: float, *, pages: bool = False):
    argv = ['gh', 'api', '-X', 'GET', endpoint]
    for field in fields:
        argv.extend(['-f', field])
    if pages:
        argv.extend(['--paginate', '--slurp'])
    result = run_command(argv, deadline)
    result.check_returncode()
    return json.loads(result.stdout)


def lean_additions_or_edits(candidate: str, head: str, deadline: float) -> bool:
    present = run_command(['git', 'cat-file', '-e', candidate + '^{commit}'], deadline)
    if present.returncode:
        return False
    ancestor = run_command(['git', 'merge-base', '--is-ancestor', candidate, head], deadline)
    if ancestor.returncode:
        return False
    # Disable rename detection and include deletions: a removed Python file must
    # not disappear merely because only its new *.lean destination was counted.
    diff = run_command(['git', 'diff', '--name-status', '--no-renames', '-z',
                        candidate, head, '--'], deadline)
    diff.check_returncode()
    parts = diff.stdout.split('\0')
    if not parts or parts[-1] != '':
        return False
    parts.pop()
    return bool(parts) and len(parts) % 2 == 0 and all(
        status in {'A', 'M'} and re.fullmatch(r'formal/[^\x00\r\n]+\.lean', path)
        for status, path in zip(parts[::2], parts[1::2])
    )


def completed_nonlean_checks(pages: object, run_id: int, attempt: int, sha: str) -> bool:
    if not isinstance(pages, list) or not pages:
        return False
    total = pages[0].get('total_count') if isinstance(pages[0], dict) else None
    if type(total) is not int or total <= 0:
        return False
    jobs = []
    for page in pages:
        if not isinstance(page, dict) or page.get('total_count') != total:
            return False
        batch = page.get('jobs')
        if not isinstance(batch, list) or not batch or not all(isinstance(j, dict) for j in batch):
            return False
        jobs.extend(batch)
    if len(jobs) != total:
        return False
    ids = [job.get('id') for job in jobs]
    if not all(type(i) is int and i > 0 for i in ids) or len(set(ids)) != len(ids):
        return False
    if any(job.get('run_id') != run_id or job.get('run_attempt') != attempt
           or job.get('head_sha') != sha or job.get('status') != 'completed'
           or not isinstance(job.get('name'), str) for job in jobs):
        return False
    selection = [job for job in jobs if job['name'] == 'Select impacted audit checks']
    if len(selection) != 1 or selection[0].get('conclusion') != 'success':
        return False
    nonlean = [job for job in jobs if job['name'] not in IGNORED_JOBS]
    return (bool(nonlean)
            and any(job.get('conclusion') == 'success' for job in nonlean)
            and all(job.get('conclusion') in {'success', 'skipped'} for job in nonlean))


def select_base(args: argparse.Namespace) -> str | None:
    deadline = time.monotonic() + 45.0
    try:
        payload = api_json(f'repos/{args.repository}/actions/workflows/pr-governance-gate.yml/runs',
                           ['event=pull_request', 'branch=' + args.branch, 'per_page=10'], deadline)
        runs = payload.get('workflow_runs') if isinstance(payload, dict) else None
        if not isinstance(runs, list):
            raise ValueError('invalid workflow history response')
        for run in runs[:10]:
            if not isinstance(run, dict):
                continue
            run_id, attempt, sha = run.get('id'), run.get('run_attempt'), run.get('head_sha')
            if (type(run_id) is not int or run_id <= 0 or run_id == args.current_run_id
                    or type(attempt) is not int or attempt <= 0 or not full_sha(sha)
                    or run.get('status') != 'completed' or run.get('event') != 'pull_request'
                    or run.get('head_branch') != args.branch or run.get('path') != WORKFLOW):
                continue
            head_repo, prs = run.get('head_repository'), run.get('pull_requests')
            if not isinstance(head_repo, dict) or head_repo.get('full_name') != args.repository:
                continue
            if not isinstance(prs, list) or not any(
                isinstance(pr, dict) and isinstance(pr.get('base'), dict)
                and pr['base'].get('sha') == args.base for pr in prs
            ):
                continue
            if not lean_additions_or_edits(sha, args.head, deadline):
                continue
            # Pin the attempt so a concurrent rerun cannot mix two job snapshots.
            endpoint = f'repos/{args.repository}/actions/runs/{run_id}/attempts/{attempt}/jobs'
            pages = api_json(endpoint, ['per_page=100'], deadline, pages=True)
            if completed_nonlean_checks(pages, run_id, attempt, sha):
                return sha
    except (OSError, ValueError, subprocess.SubprocessError, TimeoutError) as exc:
        # An unavailable optimization is not a failed proof, nor evidence to skip
        # checks. Do not log API stderr, which may contain credentials or bodies.
        print(f'Incremental history unavailable ({type(exc).__name__}); retaining full-pr checks.',
              file=sys.stderr)
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', required=True)
    parser.add_argument('--head', required=True)
    parser.add_argument('--branch', required=True)
    parser.add_argument('--repository', required=True)
    parser.add_argument('--current-run-id', type=int, required=True)
    args = parser.parse_args()
    if not full_sha(args.base) or not full_sha(args.head):
        parser.error('base and head must be nonzero full commit SHAs')
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', args.repository):
        parser.error('repository must be owner/name')
    if args.current_run_id <= 0 or not args.branch or any(c in args.branch for c in '\r\n\0'):
        parser.error('invalid workflow run or branch')
    candidate = select_base(args)
    if candidate is not None:
        print(candidate)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
