#!/usr/bin/env python3
"""Materialize exact CI comparison commits without relying on tracking aliases.

Only the runner's local object database is updated. No branch is pushed, no
checkout is changed, and a failed fetch never falls back to another commit.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys


def git(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(['git', *arguments], text=True, capture_output=True,
                          check=False, timeout=180)


def ensure_commit(sha: str) -> None:
    if not re.fullmatch(r'[0-9a-f]{40}', sha) or sha == '0' * 40:
        raise ValueError('comparison requires a nonzero full commit SHA')
    available = git('cat-file', '-e', sha + '^{commit}')
    if available.returncode:
        fetched = git('fetch', '--no-tags', '--no-recurse-submodules', 'origin', sha)
        if fetched.returncode:
            raise ValueError(f'comparison commit {sha} unavailable: {fetched.stderr.strip()}')
    # Checking the requested object, not FETCH_HEAD, also rejects tree/blob IDs.
    verified = git('rev-parse', '--verify', sha + '^{commit}')
    if verified.returncode or verified.stdout.strip() != sha:
        raise ValueError(f'comparison object is not the requested commit: {sha}')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', required=True)
    parser.add_argument('--head', required=True)
    args = parser.parse_args()
    try:
        # Validate both names before any fetch can occur.
        for sha in (args.base, args.head):
            if not re.fullmatch(r'[0-9a-f]{40}', sha) or sha == '0' * 40:
                raise ValueError('comparison requires nonzero full commit SHAs')
        ensure_commit(args.base)
        ensure_commit(args.head)
        ancestor = git('merge-base', args.base, args.head)
        if ancestor.returncode or not ancestor.stdout.strip():
            raise ValueError('comparison commits have no available merge base')
        print(f'Comparison commits verified: {args.base}...{args.head}')
        return 0
    except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
        print(f'CI comparison: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
