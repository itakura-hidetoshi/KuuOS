#!/usr/bin/env python3
"""Strictly build changed Lean modules and their immediate dependent frontier."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys
import time
from collections.abc import Iterable, Mapping
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
FORMAL_ROOT = ROOT / "formal"
EXPECTED_LEAN_TOOLCHAIN = "leanprover/lean4:v4.31.0"
EXPECTED_MATHLIB_TAG = "v4.31.0"
EXPECTED_MATHLIB_REV = "fabf563a7c95a166b8d7b6efca11c8b4dc9d911f"
LAKE_INPUTS = frozenset({"lean-toolchain", "lakefile.toml", "lake-manifest.json"})
LOCAL_GENERATED_PREFIXES = (".lake/", "artifacts/")
STRICT_LAKE_ARGS = (
    "-KleanArgs=-DwarningAsError=true",
    "-KleanArgs=-DsorryAsError=true",
)


class ChangedLeanError(RuntimeError):
    """A fail-closed planning or validation error."""


def sha256_file(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_changed_paths(base: str, head: str, include_worktree: bool = True) -> list[str]:
    commands = [
        ["git", "diff", "--name-only", "--diff-filter=ACMR", f"{base}...{head}"],
    ]
    if include_worktree:
        commands.extend(
            [
                ["git", "diff", "--name-only", "--diff-filter=ACMR", head],
                ["git", "ls-files", "--others", "--exclude-standard"],
            ]
        )

    changed: set[str] = set()
    for command in commands:
        result = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if result.returncode:
            message = result.stderr.strip() or f"{' '.join(command)} exited {result.returncode}"
            raise ChangedLeanError(f"cannot resolve changed paths: {message}")
        changed.update(line.strip() for line in result.stdout.splitlines() if line.strip())
    return sorted(
        path for path in changed if not path.startswith(LOCAL_GENERATED_PREFIXES)
    )


def selection_changed_paths(path: pathlib.Path) -> list[str]:
    try:
        selection = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ChangedLeanError(f"cannot load CI selection {path}: {exc}") from exc
    paths = selection.get("changed_paths")
    if not isinstance(paths, list) or not all(isinstance(item, str) for item in paths):
        raise ChangedLeanError("CI selection changed_paths must be a list of strings")
    return sorted(set(paths))


def module_name(path: pathlib.Path) -> str:
    try:
        relative = path.relative_to(FORMAL_ROOT)
    except ValueError as exc:
        raise ChangedLeanError(f"Lean source is outside formal/: {path}") from exc
    if relative.suffix != ".lean":
        raise ChangedLeanError(f"Lean source does not end in .lean: {path}")
    return ".".join(relative.with_suffix("").parts)


def discover_modules() -> dict[str, pathlib.Path]:
    modules: dict[str, pathlib.Path] = {}
    for path in sorted(FORMAL_ROOT.rglob("*.lean")):
        name = module_name(path)
        if name in modules:
            raise ChangedLeanError(f"duplicate Lean module {name}: {modules[name]} and {path}")
        modules[name] = path
    return modules


def project_imports(path: pathlib.Path, known_modules: set[str]) -> set[str]:
    imports: set[str] = set()
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise ChangedLeanError(f"cannot read Lean source {path}: {exc}") from exc
    for line in lines:
        match = re.match(r"^\s*import\s+(.+?)\s*(?:--.*)?$", line)
        if not match:
            continue
        for candidate in match.group(1).split():
            if candidate in known_modules:
                imports.add(candidate)
    return imports


def import_graph(modules: Mapping[str, pathlib.Path]) -> dict[str, set[str]]:
    known_modules = set(modules)
    return {
        importer: project_imports(path, known_modules)
        for importer, path in modules.items()
    }


def reverse_import_graph(
    modules: Mapping[str, pathlib.Path],
    forward: Mapping[str, set[str]] | None = None,
) -> dict[str, set[str]]:
    forward = import_graph(modules) if forward is None else forward
    reverse = {name: set() for name in modules}
    for importer, imports in forward.items():
        for imported in imports:
            reverse[imported].add(importer)
    return reverse


def registered_roots() -> list[str]:
    try:
        lakefile = (ROOT / "lakefile.toml").read_text(encoding="utf-8")
    except OSError as exc:
        raise ChangedLeanError(f"cannot read lakefile.toml roots: {exc}") from exc
    match = re.search(r"roots\s*=\s*\[(.*?)\]", lakefile, flags=re.DOTALL)
    if match is None:
        raise ChangedLeanError("lakefile.toml does not declare Lean library roots")
    roots = re.findall(r'"([^"]+)"', match.group(1))
    if not roots:
        raise ChangedLeanError("lakefile.toml Lean library roots are empty")
    return roots


def registered_module_closure(
    modules: Mapping[str, pathlib.Path], forward: Mapping[str, set[str]]
) -> set[str]:
    closure: set[str] = set()
    pending = [root for root in registered_roots() if root in modules]
    while pending:
        module = pending.pop()
        if module in closure:
            continue
        closure.add(module)
        pending.extend(forward.get(module, set()) - closure)
    return closure


def is_broad_aggregate(module: str) -> bool:
    return module in {"KuuOSFormal", "KUOS"} or module.startswith("KuuOSFormalV")


def dependent_frontier(
    direct_targets: Iterable[str],
    reverse_graph: Mapping[str, set[str]],
    registered_modules: set[str],
    depth: int,
) -> tuple[list[str], list[str], list[str]]:
    direct = set(direct_targets)
    visited = set(direct)
    frontier = set(direct)
    dependents: set[str] = set()
    skipped_aggregates: set[str] = set()
    skipped_unregistered: set[str] = set()

    for _ in range(depth):
        next_frontier: set[str] = set()
        for target in sorted(frontier):
            for dependent in sorted(reverse_graph.get(target, set())):
                if dependent in visited:
                    continue
                visited.add(dependent)
                if dependent not in registered_modules:
                    skipped_unregistered.add(dependent)
                    continue
                if is_broad_aggregate(dependent):
                    skipped_aggregates.add(dependent)
                    continue
                dependents.add(dependent)
                next_frontier.add(dependent)
        frontier = next_frontier
        if not frontier:
            break
    return sorted(dependents), sorted(skipped_aggregates), sorted(skipped_unregistered)


def pin_evidence() -> dict[str, str]:
    try:
        toolchain = (ROOT / "lean-toolchain").read_text(encoding="utf-8").strip()
        lakefile = (ROOT / "lakefile.toml").read_text(encoding="utf-8")
        manifest = json.loads((ROOT / "lake-manifest.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ChangedLeanError(f"cannot read pinned Lean inputs: {exc}") from exc

    if toolchain != EXPECTED_LEAN_TOOLCHAIN:
        raise ChangedLeanError(
            f"Lean pin changed: expected {EXPECTED_LEAN_TOOLCHAIN}, found {toolchain or '<empty>'}"
        )
    mathlib_tag = re.search(
        r'\[\[require\]\]\s*\nname\s*=\s*"mathlib".*?\nrev\s*=\s*"([^"]+)"',
        lakefile,
        flags=re.DOTALL,
    )
    if mathlib_tag is None or mathlib_tag.group(1) != EXPECTED_MATHLIB_TAG:
        found = mathlib_tag.group(1) if mathlib_tag else "<missing>"
        raise ChangedLeanError(
            f"Mathlib tag changed: expected {EXPECTED_MATHLIB_TAG}, found {found}"
        )

    packages = manifest.get("packages")
    if not isinstance(packages, list):
        raise ChangedLeanError("lake-manifest.json packages must be a list")
    mathlib_packages = [item for item in packages if isinstance(item, dict) and item.get("name") == "mathlib"]
    if len(mathlib_packages) != 1:
        raise ChangedLeanError("lake-manifest.json must contain exactly one mathlib package")
    mathlib_rev = str(mathlib_packages[0].get("rev", ""))
    if mathlib_rev != EXPECTED_MATHLIB_REV:
        raise ChangedLeanError(
            f"Mathlib manifest pin changed: expected {EXPECTED_MATHLIB_REV}, found {mathlib_rev}"
        )
    return {
        "lean_toolchain": toolchain,
        "mathlib_tag": mathlib_tag.group(1),
        "mathlib_manifest_rev": mathlib_rev,
    }


def build_plan(changed_paths: list[str], dependent_depth: int) -> dict[str, Any]:
    pins = pin_evidence()
    lean_paths = sorted(
        path for path in changed_paths if path.startswith("formal/") and path.endswith(".lean")
    )
    lake_inputs = sorted(set(changed_paths) & LAKE_INPUTS)
    modules = discover_modules()
    path_to_module = {
        path.relative_to(ROOT).as_posix(): name for name, path in modules.items()
    }

    missing = sorted(path for path in lean_paths if path not in path_to_module)
    if missing:
        raise ChangedLeanError(f"changed Lean source is unavailable: {missing[0]}")
    direct_targets = sorted(path_to_module[path] for path in lean_paths)

    dependent_targets: list[str] = []
    skipped_aggregates: list[str] = []
    skipped_unregistered: list[str] = []
    full_reasons: list[str] = []
    if lake_inputs:
        full_reasons.append("pinned Lake input changed")
    if any(is_broad_aggregate(target) for target in direct_targets):
        full_reasons.append("broad aggregate root changed")

    if full_reasons:
        build_targets = ["KuuOSFormal"]
    elif direct_targets:
        forward = import_graph(modules)
        reverse = reverse_import_graph(modules, forward)
        registered = registered_module_closure(modules, forward)
        dependent_targets, skipped_aggregates, skipped_unregistered = dependent_frontier(
            direct_targets, reverse, registered, dependent_depth
        )
        build_targets = sorted(set(direct_targets) | set(dependent_targets))
    else:
        build_targets = []

    return {
        "schema_version": "0.1",
        "mode": "full-required" if full_reasons else "changed-target",
        "changed_paths": changed_paths,
        "changed_lean_files": lean_paths,
        "changed_lake_inputs": lake_inputs,
        "direct_targets": direct_targets,
        "dependent_targets": dependent_targets,
        "dependent_depth": dependent_depth,
        "skipped_broad_aggregate_dependents": skipped_aggregates,
        "skipped_unregistered_dependents": skipped_unregistered,
        "build_targets": build_targets,
        "full_reasons": full_reasons,
        "strict_lean_args": list(STRICT_LAKE_ARGS),
        "pins": pins,
        "status": "planned" if build_targets else "skipped",
        "authority_boundary": (
            "changed-target validation is local evidence; full KuuOSFormal remains the merge boundary"
        ),
    }


def runtime_version(command: str) -> str:
    try:
        result = subprocess.run(
            [command, "--version"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
    except OSError as exc:
        raise ChangedLeanError(f"cannot launch {command}: {exc}") from exc
    output = result.stdout.strip()
    if result.returncode:
        raise ChangedLeanError(f"{command} --version failed: {output}")
    return output


def write_receipt(path: pathlib.Path | None, receipt: Mapping[str, Any]) -> None:
    if path is None:
        return
    output = path if path.is_absolute() else ROOT / path
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--selection", type=pathlib.Path)
    source.add_argument("--base")
    parser.add_argument("--head", default="HEAD")
    parser.add_argument("--dependent-depth", type=int, default=1, choices=range(0, 4))
    parser.add_argument("--output", type=pathlib.Path)
    parser.add_argument("--plan-only", action="store_true")
    parser.add_argument("--committed-only", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    started = dt.datetime.now(dt.timezone.utc)
    start_clock = time.monotonic()
    try:
        changed_paths = (
            selection_changed_paths(args.selection)
            if args.selection is not None
            else git_changed_paths(args.base, args.head, include_worktree=not args.committed_only)
        )
        plan = build_plan(changed_paths, args.dependent_depth)
    except ChangedLeanError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    print(json.dumps(plan, ensure_ascii=False, indent=2))
    write_receipt(args.output, plan)
    if args.plan_only or not plan["build_targets"]:
        return 0

    try:
        lean_version = runtime_version("lean")
        lake_version = runtime_version("lake")
        if not re.search(r"\bversion 4\.31\.0\b", lean_version):
            raise ChangedLeanError(f"expected local Lean 4.31.0, found: {lean_version}")
    except ChangedLeanError as exc:
        plan.update(
            {
                "status": "failed",
                "error": str(exc),
                "duration_seconds": round(time.monotonic() - start_clock, 3),
            }
        )
        write_receipt(args.output, plan)
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    manifest_before = sha256_file(ROOT / "lake-manifest.json")
    command = ["lake", *STRICT_LAKE_ARGS, "build", *plan["build_targets"]]
    print(f">>> {' '.join(command)}", flush=True)
    env = os.environ.copy()
    env["LEAN_ABORT_ON_PANIC"] = "1"
    result = subprocess.run(command, cwd=ROOT, env=env, check=False)
    manifest_after = sha256_file(ROOT / "lake-manifest.json")
    manifest_unchanged = manifest_before == manifest_after
    return_code = result.returncode if manifest_unchanged else 1
    if not manifest_unchanged:
        print("ERROR: lake-manifest.json changed during changed-target validation", file=sys.stderr)

    plan.update(
        {
            "status": "passed" if return_code == 0 else "failed",
            "return_code": return_code,
            "command": command,
            "lean_version": lean_version,
            "lake_version": lake_version,
            "manifest_unchanged": manifest_unchanged,
            "started_at": started.isoformat(),
            "finished_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            "duration_seconds": round(time.monotonic() - start_clock, 3),
        }
    )
    write_receipt(args.output, plan)
    print(json.dumps(plan, ensure_ascii=False, indent=2))
    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
