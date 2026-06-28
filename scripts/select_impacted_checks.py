#!/usr/bin/env python3
"""Fail-closed impact selector for KuuOS CI checks."""

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
REGISTRY_FRAGMENT_DIRNAME = "check_registry.d"


def _load_json(path: pathlib.Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot load check registry {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"check registry {path} must contain an object")
    return data


def _extend_unique(target: list[Any], values: Any, field: str, path: pathlib.Path) -> None:
    if values is None:
        return
    if not isinstance(values, list):
        raise ValueError(f"{field} in {path} must be a list")
    for value in values:
        if value not in target:
            target.append(value)


def load_registry(path: pathlib.Path) -> dict[str, Any]:
    data = _load_json(path)
    if data.get("schema_version") not in {"0.1", "0.2"}:
        raise ValueError("unsupported or missing registry schema_version")
    if not isinstance(data.get("checks"), dict) or not data["checks"]:
        raise ValueError("registry checks must be a non-empty object")

    data.setdefault("known_paths", [])
    data.setdefault("full_audit_paths", [])
    data.setdefault("policy", {})
    data["policy"].setdefault("boundaries", [])
    fragments: list[str] = []
    fragment_dir = path.parent / REGISTRY_FRAGMENT_DIRNAME
    if fragment_dir.is_dir():
        for fragment_path in sorted(fragment_dir.glob("*.json")):
            fragment = _load_json(fragment_path)
            if fragment.get("schema_version") not in {"0.2"}:
                raise ValueError(f"unsupported fragment schema_version in {fragment_path}")
            _extend_unique(data["known_paths"], fragment.get("known_paths"), "known_paths", fragment_path)
            _extend_unique(
                data["full_audit_paths"],
                fragment.get("full_audit_paths"),
                "full_audit_paths",
                fragment_path,
            )
            fragment_policy = fragment.get("policy", {})
            if fragment_policy and not isinstance(fragment_policy, dict):
                raise ValueError(f"policy in {fragment_path} must be an object")
            _extend_unique(
                data["policy"]["boundaries"],
                fragment_policy.get("boundaries") if fragment_policy else None,
                "policy.boundaries",
                fragment_path,
            )
            fragment_checks = fragment.get("checks", {})
            if not isinstance(fragment_checks, dict) or not fragment_checks:
                raise ValueError(f"checks in {fragment_path} must be a non-empty object")
            duplicates = sorted(set(data["checks"]) & set(fragment_checks))
            if duplicates:
                raise ValueError(
                    f"duplicate registry check {duplicates[0]!r} in {fragment_path}"
                )
            data["checks"].update(fragment_checks)
            fragments.append(str(fragment_path.relative_to(ROOT)))
    data["registry_fragments"] = fragments
    return data


def git_changed_paths(base: str, head: str) -> tuple[list[str], str | None]:
    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=ACMR", f"{base}...{head}"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode:
        return [], result.stderr.strip() or f"git diff exited {result.returncode}"
    return sorted({line.strip() for line in result.stdout.splitlines() if line.strip()}), None


def matches(path: str, patterns: Iterable[str]) -> bool:
    return any(fnmatch.fnmatchcase(path, pattern) for pattern in patterns)


def dependency_closure(
    selected: set[str], checks: Mapping[str, Mapping[str, Any]]
) -> set[str]:
    result = set(selected)
    pending = list(selected)
    while pending:
        check_id = pending.pop()
        dependencies = checks[check_id].get("depends_on", [])
        if not isinstance(dependencies, list):
            raise ValueError(f"depends_on must be a list for {check_id}")
        for dependency in dependencies:
            if dependency not in checks:
                raise ValueError(f"unknown dependency {dependency!r} for {check_id}")
            if dependency not in result:
                result.add(dependency)
                pending.append(dependency)
    return result


def apply_supersedence(
    selected: set[str],
    checks: Mapping[str, Mapping[str, Any]],
    full_audit: bool,
) -> set[str]:
    result = set(selected)
    relations = ("supersedes",) if full_audit else ("supersedes", "pr_supersedes")
    for check_id in sorted(selected):
        for relation in relations:
            targets = checks[check_id].get(relation, [])
            if not isinstance(targets, list):
                raise ValueError(f"{relation} must be a list for {check_id}")
            for target in targets:
                if target not in checks:
                    raise ValueError(f"unknown {relation} target {target!r} for {check_id}")
                result.discard(target)
    return result


def expand_check(check_id: str, check: Mapping[str, Any]) -> list[dict[str, Any]]:
    runner = str(check.get("runner", "python"))
    common = {
        "group": check.get("group", ""),
        "tier": check.get("tier", ""),
        "timeout_minutes": int(check.get("timeout_minutes", 30)),
    }
    if runner != "python-sharded":
        return [{
            "id": check_id,
            "name": check.get("name", check_id),
            "runner": runner,
            "command": check.get("command", ""),
            **common,
        }]

    count = check.get("shard_count")
    template = check.get("command")
    if not isinstance(count, int) or count <= 0:
        raise ValueError(f"positive shard_count required for {check_id}")
    if not isinstance(template, str) or "{index}" not in template or "{count}" not in template:
        raise ValueError(f"sharded command template invalid for {check_id}")
    width = max(2, len(str(count - 1)))
    return [{
        "id": f"{check_id}-{index:0{width}d}",
        "name": f"{check.get('name', check_id)} shard {index + 1}/{count}",
        "runner": "python",
        "command": template.format(index=index, count=count),
        "parent_id": check_id,
        "shard_index": index,
        "shard_count": count,
        **common,
    } for index in range(count)]


def select(
    registry: Mapping[str, Any], changed_paths: list[str], diff_error: str | None
) -> dict[str, Any]:
    checks: Mapping[str, Mapping[str, Any]] = registry["checks"]
    patterns: dict[str, list[str]] = {}
    for check_id, check in checks.items():
        value = check.get("paths", [])
        if not isinstance(value, list):
            raise ValueError(f"paths must be a list for {check_id}")
        patterns[check_id] = value

    known = registry.get("known_paths", [])
    control = registry.get("full_audit_paths", [])
    unknown_paths = [path for path in changed_paths if not matches(path, known)]
    trigger_paths = [
        path for path in changed_paths
        if path.startswith(".github/workflows/") or matches(path, control)
    ]
    unmapped_paths = [
        path for path in changed_paths
        if not any(matches(path, values) for values in patterns.values())
    ]
    full_audit = bool(diff_error or unknown_paths or trigger_paths or unmapped_paths)
    reasons = []
    if diff_error:
        reasons.append(f"change diff unavailable: {diff_error}")
    if unknown_paths:
        reasons.append("unclassified paths require fail-closed full audit")
    if unmapped_paths:
        reasons.append("known but unmapped paths require fail-closed full audit")
    if trigger_paths:
        reasons.append("audit-control surface changed")

    direct = {
        check_id for check_id, values in patterns.items()
        if any(matches(path, values) for path in changed_paths)
    }
    direct.add("workflow-integrity")
    selected = (
        {check_id for check_id, check in checks.items() if check.get("full_audit_member")}
        if full_audit else set(direct)
    )
    selected = dependency_closure(selected, checks)
    selected = apply_supersedence(selected, checks, full_audit)

    expanded = [
        item
        for check_id in sorted(selected, key=lambda value: (str(checks[value].get("group", "")), value))
        for item in expand_check(check_id, checks[check_id])
    ]
    python_matrix = [
        {"id": item["id"], "name": item["name"], "command": item["command"]}
        for item in expanded if item["runner"] == "python"
    ]
    unsupported = [item["runner"] for item in expanded if item["runner"] not in {"python", "lean"}]
    if unsupported:
        raise ValueError(f"unsupported expanded runner {unsupported[0]!r}")

    return {
        "schema_version": "0.2",
        "changed_paths": changed_paths,
        "direct_checks": sorted(direct),
        "selected_checks": expanded,
        "python_matrix": python_matrix,
        "lean_required": any(item["runner"] == "lean" for item in expanded),
        "full_audit_required": full_audit,
        "unknown_paths": unknown_paths,
        "unmapped_paths": unmapped_paths,
        "full_audit_trigger_paths": trigger_paths,
        "reasons": reasons,
        "registry_fragments": registry.get("registry_fragments", []),
        "boundaries": registry.get("policy", {}).get("boundaries", []),
    }


def write_github_output(path: pathlib.Path, selection: Mapping[str, Any]) -> None:
    values = {
        "python_matrix": json.dumps(selection["python_matrix"], separators=(",", ":")),
        "python_count": len(selection["python_matrix"]),
        "lean_required": str(bool(selection["lean_required"])).lower(),
        "full_audit_required": str(bool(selection["full_audit_required"])).lower(),
    }
    with path.open("a", encoding="utf-8") as handle:
        for key, value in values.items():
            handle.write(f"{key}={value}\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--registry", type=pathlib.Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    parser.add_argument("--github-output", type=pathlib.Path)
    args = parser.parse_args()
    try:
        registry = load_registry(args.registry)
        changed_paths, diff_error = git_changed_paths(args.base, args.head)
        selection = select(registry, changed_paths, diff_error)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(selection, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.github_output:
        write_github_output(args.github_output, selection)
    print(json.dumps(selection, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
