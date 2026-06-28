#!/usr/bin/env python3
"""Select the smallest fail-closed KuuOS CI audit set for a change.

The registry is JSON encoded inside a YAML-compatible file so the selector remains
stdlib-only. Selection reduces repeated execution; it does not weaken any KuuOS
authority, truth, proof, or release boundary.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import pathlib
import subprocess
import sys
from collections.abc import Iterable, Mapping
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "ci" / "check_registry.yaml"


def load_registry(path: pathlib.Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot load check registry {path}: {exc}") from exc
    if data.get("schema_version") != "0.1":
        raise ValueError("unsupported or missing registry schema_version")
    checks = data.get("checks")
    if not isinstance(checks, dict) or not checks:
        raise ValueError("registry checks must be a non-empty object")
    return data


def git_changed_paths(base: str, head: str) -> tuple[list[str], str | None]:
    command = ["git", "diff", "--name-only", "--diff-filter=ACMR", f"{base}...{head}"]
    completed = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or f"git diff exited {completed.returncode}"
        return [], detail
    paths = sorted({line.strip() for line in completed.stdout.splitlines() if line.strip()})
    return paths, None


def matches(path: str, patterns: Iterable[str]) -> bool:
    return any(fnmatch.fnmatchcase(path, pattern) for pattern in patterns)


def dependency_closure(selected: set[str], checks: Mapping[str, Mapping[str, Any]]) -> set[str]:
    closure = set(selected)
    pending = list(selected)
    while pending:
        check_id = pending.pop()
        check = checks.get(check_id)
        if check is None:
            raise ValueError(f"unknown check in dependency graph: {check_id}")
        dependencies = check.get("depends_on", [])
        if not isinstance(dependencies, list):
            raise ValueError(f"depends_on must be a list for {check_id}")
        for dependency in dependencies:
            if dependency not in checks:
                raise ValueError(f"unknown dependency {dependency!r} for {check_id}")
            if dependency not in closure:
                closure.add(dependency)
                pending.append(dependency)
    return closure


def apply_supersedence(
    selected: set[str],
    checks: Mapping[str, Mapping[str, Any]],
    *,
    full_audit_required: bool,
) -> set[str]:
    result = set(selected)
    for check_id in sorted(selected):
        relations = ["supersedes"]
        if not full_audit_required:
            relations.append("pr_supersedes")
        for relation in relations:
            supersedes = checks[check_id].get(relation, [])
            if not isinstance(supersedes, list):
                raise ValueError(f"{relation} must be a list for {check_id}")
            for superseded in supersedes:
                if superseded not in checks:
                    raise ValueError(
                        f"unknown {relation} target {superseded!r} for {check_id}"
                    )
                result.discard(superseded)
    return result


def select(registry: Mapping[str, Any], changed_paths: list[str], diff_error: str | None) -> dict[str, Any]:
    checks: Mapping[str, Mapping[str, Any]] = registry["checks"]
    reasons: list[str] = []

    check_patterns: dict[str, list[str]] = {}
    for check_id, check in checks.items():
        patterns = check.get("paths", [])
        if not isinstance(patterns, list):
            raise ValueError(f"paths must be a list for {check_id}")
        check_patterns[check_id] = patterns

    unknown_paths = [
        path for path in changed_paths if not matches(path, registry.get("known_paths", []))
    ]
    trigger_paths = [
        path for path in changed_paths if matches(path, registry.get("full_audit_paths", []))
    ]
    unmapped_paths = [
        path
        for path in changed_paths
        if not any(matches(path, patterns) for patterns in check_patterns.values())
    ]

    full_audit_required = bool(diff_error or unknown_paths or trigger_paths or unmapped_paths)
    if diff_error:
        reasons.append(f"change diff unavailable: {diff_error}")
    if unknown_paths:
        reasons.append("unclassified paths require fail-closed full audit")
    if unmapped_paths:
        reasons.append("known but unmapped paths require fail-closed full audit")
    if trigger_paths:
        reasons.append("audit-control surface changed")

    direct: set[str] = set()
    for check_id, patterns in check_patterns.items():
        if any(matches(path, patterns) for path in changed_paths):
            direct.add(check_id)

    # This small structural invariant is always retained on pull requests.
    direct.add("workflow-integrity")

    if full_audit_required:
        selected = {
            check_id
            for check_id, check in checks.items()
            if bool(check.get("full_audit_member", False))
        }
    else:
        selected = set(direct)

    selected = dependency_closure(selected, checks)
    selected = apply_supersedence(
        selected,
        checks,
        full_audit_required=full_audit_required,
    )

    ordered_ids = sorted(selected, key=lambda item: (str(checks[item].get("group", "")), item))
    python_matrix: list[dict[str, Any]] = []
    lean_required = False
    selected_checks: list[dict[str, Any]] = []

    for check_id in ordered_ids:
        check = checks[check_id]
        runner = str(check.get("runner", "python"))
        selected_checks.append(
            {
                "id": check_id,
                "name": check.get("name", check_id),
                "runner": runner,
                "group": check.get("group", ""),
                "tier": check.get("tier", ""),
                "command": check.get("command", ""),
                "timeout_minutes": int(check.get("timeout_minutes", 30)),
            }
        )
        if runner == "lean":
            lean_required = True
        elif runner == "python":
            python_matrix.append(
                {
                    "id": check_id,
                    "name": check.get("name", check_id),
                    "command": check.get("command", ""),
                }
            )
        else:
            raise ValueError(f"unsupported runner {runner!r} for {check_id}")

    return {
        "schema_version": "0.1",
        "changed_paths": changed_paths,
        "direct_checks": sorted(direct),
        "selected_checks": selected_checks,
        "python_matrix": python_matrix,
        "lean_required": lean_required,
        "full_audit_required": full_audit_required,
        "unknown_paths": unknown_paths,
        "unmapped_paths": unmapped_paths,
        "full_audit_trigger_paths": trigger_paths,
        "reasons": reasons,
        "boundaries": registry.get("policy", {}).get("boundaries", []),
    }


def write_github_output(path: pathlib.Path, selection: Mapping[str, Any]) -> None:
    python_matrix = json.dumps(selection["python_matrix"], separators=(",", ":"))
    lines = [
        f"python_matrix={python_matrix}",
        f"python_count={len(selection['python_matrix'])}",
        f"lean_required={str(bool(selection['lean_required'])).lower()}",
        f"full_audit_required={str(bool(selection['full_audit_required'])).lower()}",
    ]
    with path.open("a", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--registry", type=pathlib.Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    parser.add_argument("--github-output", type=pathlib.Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        registry = load_registry(args.registry)
        changed_paths, diff_error = git_changed_paths(args.base, args.head)
        selection = select(registry, changed_paths, diff_error)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(selection, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    if args.github_output is not None:
        write_github_output(args.github_output, selection)

    print(json.dumps(selection, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
