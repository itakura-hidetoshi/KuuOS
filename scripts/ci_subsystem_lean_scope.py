#!/usr/bin/env python3
"""Fail-closed focused Lean scope for dedicated Gauge/Modular workflows.

The canonical exact-head PR Governance check owns the full public-root Lean
build. A dedicated subsystem still checks its runtime on every triggering PR,
and runs strict targeted Lean only if a subsystem source/workflow changes,
if its diff cannot be proved, or if the run is manually requested.

Kept separate from ci_codeai_lean_scope.py so a performance repair does not
start all 49 CodeAI workflows that depend on that shared selector.
"""
from __future__ import annotations

import argparse
import fnmatch
import pathlib
import subprocess

from scripts.ci_codeai_lean_scope import (
    GLOBAL_LEAN_INPUTS,
    changed_paths,
    workflow_pr_paths,
)


def needs_subsystem_lean(
    changed: list[str], patterns: list[str], delegated_paths: list[str]
) -> bool:
    """Return False only when every changed path has central CI authority.

    The dedicated subsystem always reruns Lean when its own source, tests,
    manifest, workflow or an unclassified input changes. Empty or unknown
    inputs are conservatively treated as needing full scoped Lean.
    """
    if not changed or not patterns:
        return True
    delegated = GLOBAL_LEAN_INPUTS | frozenset(delegated_paths)
    owned = [pattern for pattern in patterns if pattern not in delegated]
    if not owned:
        return True
    return any(
        fnmatch.fnmatchcase(path, pattern)
        for path in changed
        for pattern in owned
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workflow", type=pathlib.Path, required=True)
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", default="HEAD")
    parser.add_argument("--github-output", type=pathlib.Path, required=True)
    parser.add_argument("--delegated-path", action="append", default=[])
    args = parser.parse_args()

    try:
        patterns = workflow_pr_paths(args.workflow.read_text(encoding="utf-8"))
        changed = changed_paths(args.base, args.head)
        needed = needs_subsystem_lean(changed, patterns, args.delegated_path)
        detail = f"changed={len(changed)}, owned={len(patterns)}"
    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        needed = True
        detail = f"fail closed ({type(exc).__name__}): {exc}"

    with args.github_output.open("a", encoding="utf-8") as out:
        out.write(f"needed={'true' if needed else 'false'}\n")
    print(f"Subsystem strict Lean required: {needed} ({detail})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
