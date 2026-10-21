#!/usr/bin/env python3
"""Fail-closed scope decision for CodeAI Lean checks triggered by global Lake files."""
from __future__ import annotations

import argparse
import fnmatch
import pathlib
import re
import subprocess

GLOBAL_LEAN_INPUTS = frozenset({
    "lean-toolchain", "lake-manifest.json", "lakefile.toml"
})


def workflow_pr_paths(source: str) -> list[str]:
    """Extract the declarative pull_request.paths block without a YAML dependency."""
    inside_event = False
    inside_paths = False
    patterns: list[str] = []
    for line in source.splitlines():
        if line == "  pull_request:":
            inside_event = True
            inside_paths = False
            continue
        if inside_event and re.match(r"^  [A-Za-z_][A-Za-z0-9_-]*:", line):
            break
        if inside_event and line == "    paths:":
            inside_paths = True
            continue
        if inside_paths:
            match = re.match(r"^      - ['\"]?([^'\"\n]+)['\"]?$", line)
            if match:
                patterns.append(match.group(1))
            elif line and not line.startswith("      "):
                break
    return patterns


def needs_targeted_lean(changed: list[str], patterns: list[str]) -> bool:
    """A path already checked by PR Governance alone does not activate CodeAI Lean."""
    if not changed or not patterns:
        return True  # fail-closed on missing data
    relevant = [pattern for pattern in patterns if pattern not in GLOBAL_LEAN_INPUTS]
    if not relevant:
        return True  # fail-closed if a workflow has no own scope
    return any(fnmatch.fnmatchcase(path, pattern) for path in changed for pattern in relevant)


def changed_paths(base: str, head: str) -> list[str]:
    # HEAD is GitHub's checked-out PR merge commit, containing all PR changes.
    # Base can be shallow; fetch just that commit if it isn't locally present.
    available = subprocess.run(
        ["git", "cat-file", "-e", f"{base}^{{commit}}"],
        capture_output=True, check=False,
    )
    if available.returncode != 0:
        subprocess.run(
            ["git", "fetch", "--no-tags", "--depth=1", "origin", base],
            check=True, capture_output=True, text=True,
        )
    output = subprocess.run(
        ["git", "diff", "--name-only", base, head, "--"],
        check=True, capture_output=True, text=True,
    ).stdout
    return [line for line in output.splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workflow", type=pathlib.Path, required=True)
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", default="HEAD")
    parser.add_argument("--github-output", type=pathlib.Path, required=True)
    args = parser.parse_args()

    # When the diff cannot be proved, do the full targeted Lean check instead.
    try:
        source = args.workflow.read_text(encoding="utf-8")
        patterns = workflow_pr_paths(source)
        changed = changed_paths(args.base, args.head)
        needed = needs_targeted_lean(changed, patterns)
        detail = f"changed={len(changed)}, scoped_paths={len(patterns)}"
    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        needed = True
        detail = f"fail-closed: {type(exc).__name__}: {exc}"

    with args.github_output.open("a", encoding="utf-8") as out:
        out.write(f"needed={'true' if needed else 'false'}\n")
    print(f"CodeAI strict Lean required: {needed} ({detail})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
