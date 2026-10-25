#!/usr/bin/env python3
"""Fail-closed Lean .olean route for strictly additive F112 public imports.

Only a PR that ADDS new original F112 source files and makes precisely
corresponding import-line additions to formal/KuuOSFormal.lean can use the
single-module :olean route. Pre-existing non-Lean CI-control edits are
allowed only with full repository governance and an exact audited diff.
Unknown sources, audit triggers and malformed imports fail closed to full.

This does NOT infer proof truth from git diffs or caches: Lake still strictly
elaborates the public root and every added theorem module on the exact HEAD.
All historical 107 public roots remain unchanged and are verified by the
main-push full-library build.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_AGGREGATE = "formal/KuuOSFormal.lean"
NEW_SOURCE = re.compile(r"formal/Kuu/F112/([A-Za-z][A-Za-z0-9_]*)\.lean\Z")
NEW_IMPORT = re.compile(r"import Kuu\.F112\.([A-Za-z][A-Za-z0-9_]*)\Z")
SHA = re.compile(r"[0-9a-f]{40}\Z")
# Only pre-existing non-Lean CI controls. Keep full governance selected.
APPROVED_CI_OVERLAY = frozenset({
    ".github/workflows/lean-formal-validation.yml",
    ".github/workflows/pr-governance-gate.yml",
    "scripts/build_audit_summary.py",
    "scripts/build_lean4.sh",
    "scripts/select_lean_import_only_route.py",
    "tests/test_ci_lean_cache_topology.py",
    "tests/test_ci_f112_additive_root_route.py",
})


def _git(cwd: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", *args], cwd=cwd, text=True,
            capture_output=True, check=False, timeout=20,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return result.stdout if result.returncode == 0 else None


def choose_lean_targets(
    selection: Mapping[str, Any], cwd: Path = ROOT
) -> tuple[list[str], str]:
    """Return executable targets and an auditable route reason.

    On EVERY uncertified scenario, return the selector's complete original
    target list unchanged. The source graph and exact PR diff are inspected
    rather than guessing from the name of a touched file.
    """
    original = selection.get("lean_targets")
    if not isinstance(original, list) or not original or not all(
        isinstance(x, str) and x for x in original
    ):
        return ["KuuOSFormal"], "fallback-invalid-target-list"

    def fallback(reason: str) -> tuple[list[str], str]:
        return list(original), "full-" + reason

    if selection.get("lean_required") is not True:
        return fallback("lean-not-selected")
    if selection.get("comparison_mode") != "full-pr":
        return fallback("comparison-not-full-pr")
    if selection.get("validated_lean_incremental"):
        return fallback("incremental-diff")
    if selection.get("unknown_paths"):
        return fallback("unknown-paths")
    unmapped = selection.get("unmapped_paths", [])
    if (not isinstance(unmapped, list)
            or any(not isinstance(path, str) or path not in APPROVED_CI_OVERLAY
                   for path in unmapped)):
        return fallback("unclassified-paths")

    base, head = selection.get("comparison_base"), selection.get("comparison_head")
    if not isinstance(base, str) or not isinstance(head, str):
        return fallback("missing-revision")
    if SHA.fullmatch(base) is None or SHA.fullmatch(head) is None:
        return fallback("nonexact-revision")

    changed = selection.get("changed_paths")
    if not isinstance(changed, list) or not changed or not all(
        isinstance(path, str) for path in changed
    ):
        return fallback("unknown-paths")
    if len(changed) != len(set(changed)) or PUBLIC_AGGREGATE not in changed:
        return fallback("aggregate-not-unique")

    overlay = sorted(path for path in changed if path in APPROVED_CI_OVERLAY)
    if overlay:
        triggers = selection.get("full_audit_trigger_paths")
        if selection.get("full_audit_required") is not True:
            return fallback("ci-overlay-without-full-audit")
        if (not isinstance(triggers, list) or not triggers
                or any(not isinstance(p, str) or p not in overlay for p in triggers)):
            return fallback("unapproved-audit-trigger")
    elif (selection.get("full_audit_required") is not False
          or selection.get("full_audit_trigger_paths")):
        return fallback("audit-required")

    new_files = sorted(
        p for p in changed
        if p != PUBLIC_AGGREGATE and p not in APPROVED_CI_OVERLAY
    )
    if not new_files or any(NEW_SOURCE.fullmatch(p) is None for p in new_files):
        return fallback("not-only-new-f112")
    expected_module_names = {NEW_SOURCE.fullmatch(p).group(1) for p in new_files}
    expected_old_targets = {"KuuOSFormal"} | {
        "+Kuu.F112." + name for name in expected_module_names
    }
    if len(original) != len(expected_old_targets) or set(original) != expected_old_targets:
        return fallback("selector-target-mismatch")
    if any(not (cwd / p).is_file() for p in new_files):
        return fallback("missing-new-module")

    # The original changed_paths selector filters some status categories.
    # This second independent diff includes EVERY status (notably deletes).
    names = _git(cwd, "diff", "--name-status", "--no-renames",
                 f"{base}...{head}", "--")
    if names is None:
        return fallback("name-status-unavailable")
    statuses: dict[str, str] = {}
    for line in names.splitlines():
        parts = line.split("\t")
        if len(parts) != 2 or parts[1] in statuses:
            return fallback("unexpected-status-format")
        statuses[parts[1]] = parts[0]
    if set(statuses) != set(changed):
        return fallback("diff-incomplete")
    if statuses.get(PUBLIC_AGGREGATE) != "M" or any(
        statuses.get(path) != "A" for path in new_files
    ) or any(statuses.get(path) != "M" for path in overlay):
        return fallback("not-additions-only")

    patch = _git(cwd, "diff", "--no-ext-diff", "--no-renames",
                 "--unified=0", f"{base}...{head}", "--", PUBLIC_AGGREGATE)
    if patch is None:
        return fallback("root-patch-unavailable")
    imports: list[str] = []
    for line in patch.splitlines():
        if line.startswith("+++") or line.startswith("---"):
            continue
        if line.startswith("-"):
            return fallback("root-deletions")
        if line.startswith("+"):
            match = NEW_IMPORT.fullmatch(line[1:])
            if match is None:
                return fallback("root-not-import-only")
            imports.append(match.group(1))
    if len(imports) != len(expected_module_names) or set(imports) != expected_module_names:
        return fallback("new-import-mismatch")

    # Lean v4.30 Lake module facet syntax is also exercised by Qi v3.1-v3.3.
    # Root .olean compilation checks the modified public import environment;
    # all NEW F112 modules are explicit targets, too.
    execution = ["+KuuOSFormal:olean"] + [
        "+Kuu.F112." + name + ":olean" for name in sorted(expected_module_names)
    ]
    return execution, ("verified-additive-f112-audited-ci-overlay-olean"
                       if overlay else "verified-additive-f112-root-olean")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--selection", type=Path, required=True)
    args = parser.parse_args()
    try:
        receipt = json.loads(args.selection.read_text(encoding="utf-8"))
        if not isinstance(receipt, dict):
            raise ValueError("selection receipt must be an object")
        targets, route = choose_lean_targets(receipt)
        receipt["lean_execution_targets"] = targets
        receipt["lean_execution_route"] = route
        args.selection.write_text(
            json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(json.dumps(
            {"lean_execution_targets": targets, "lean_execution_route": route},
            ensure_ascii=False,
        ))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        # A broken selector MUST NOT make the CI green without building.
        print(f"Lean route selection failed: {exc}", flush=True)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
