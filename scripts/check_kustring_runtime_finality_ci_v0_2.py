#!/usr/bin/env python3
"""Validate the KuString runtime finality CI execution topology.

The validator accepts either the legacy workflow, where the finality suite and
report builder are invoked directly, or the centralized scheduling topology,
where the workflow delegates to ``run_pr_entry_check_v0_4.py``. Centralized
scheduling must preserve the subsystem command set, generated finality report,
and authority boundary.
"""

from __future__ import annotations

import pathlib
from collections.abc import Sequence

ROOT = pathlib.Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "kustring_runtime_finality_v0_2.yml"
ENTRY_RUNNER = ROOT / "scripts" / "run_pr_entry_check_v0_4.py"
FINALITY_SUITE = ROOT / "scripts" / "run_kustring_runtime_finality_suite_v0_2.py"
REPORT_BUILDER = ROOT / "scripts" / "build_kustring_runtime_finality_report_v0_2.py"

COMMON_WORKFLOW_REQUIRED = [
    "KuString Runtime Finality v0.2",
    "workflow_dispatch",
    "actions/checkout@v4",
    "actions/setup-python@v5",
    "python-version: '3.12'",
    "actions/upload-artifact@v4",
]

LEGACY_WORKFLOW_REQUIRED = [
    "python3 scripts/run_kustring_runtime_finality_suite_v0_2.py",
    "python3 scripts/build_kustring_runtime_finality_report_v0_2.py",
    "kustring-runtime-finality-report-v0-2",
    "specs/kustring_runtime_finality_report_v0_2.generated.json",
]

CENTRAL_WORKFLOW_REQUIRED = [
    "python3 scripts/run_pr_entry_check_v0_4.py",
    "--check-id kustring-finality",
    "--output-root .out/checks",
    "name: kustring-finality-",
    "github.run_id",
    ".out/checks/kustring-finality",
    "if-no-files-found: error",
]

ENTRY_RUNNER_REQUIRED = [
    'if check_id == "kustring-finality":',
    "scripts/run_kustring_runtime_finality_suite_v0_2.py",
    "scripts/build_kustring_runtime_finality_report_v0_2.py",
    "specs/kustring_runtime_finality_report_v0_2.generated.json",
    "shutil.copy2",
    "central scheduling != validator weakening",
]

FINALITY_SUITE_REQUIRED = [
    "scripts/run_kustring_runtime_closure_suite_v0_2.py",
    "scripts/check_kustring_runtime_finality_v0_2.py",
    "scripts/check_kustring_runtime_finality_ci_v0_2.py",
    "scripts/check_kustring_runtime_workflow_paths_v0_2.py",
    "scripts/check_kustring_runtime_finality_report_v0_2.py",
    "scripts/check_kustring_runtime_chain_index_v0_2.py",
]

REPORT_BUILDER_REQUIRED = [
    "scripts/run_kustring_runtime_closure_suite_v0_2.py",
    "scripts/check_kustring_runtime_finality_v0_2.py",
    "scripts/check_kustring_runtime_finality_ci_v0_2.py",
    "scripts/check_kustring_runtime_chain_index_v0_2.py",
    "specs/kustring_runtime_finality_report_v0_2.generated.json",
    "generated_report_is_integrity_summary_only",
    "implementation_not_proof",
    "OUT.write_text",
]


def missing_tokens(text: str, required: Sequence[str]) -> list[str]:
    return [token for token in required if token not in text]


def check_file(
    path: pathlib.Path,
    label: str,
    required: Sequence[str],
    errors: list[str],
) -> None:
    if not path.is_file():
        errors.append(f"missing {label}: {path.relative_to(ROOT)}")
        return
    text = path.read_text(encoding="utf-8")
    for token in missing_tokens(text, required):
        errors.append(f"{label} missing: {token}")


def validate_workflow(errors: list[str]) -> None:
    if not WORKFLOW.is_file():
        errors.append("missing workflow")
        return

    text = WORKFLOW.read_text(encoding="utf-8")
    for token in missing_tokens(text, COMMON_WORKFLOW_REQUIRED):
        errors.append(f"workflow missing: {token}")

    legacy_missing = missing_tokens(text, LEGACY_WORKFLOW_REQUIRED)
    central_missing = missing_tokens(text, CENTRAL_WORKFLOW_REQUIRED)
    legacy_mode = not legacy_missing
    central_mode = not central_missing

    if legacy_mode and central_mode:
        errors.append("workflow topology ambiguous: both legacy and centralized modes detected")
        return

    if not legacy_mode and not central_mode:
        errors.append("workflow topology unsupported: expected legacy direct or centralized runner mode")
        for token in central_missing:
            errors.append(f"central workflow missing: {token}")
        for token in legacy_missing:
            errors.append(f"legacy workflow missing: {token}")
        return

    if central_mode:
        check_file(ENTRY_RUNNER, "central entry runner", ENTRY_RUNNER_REQUIRED, errors)

    check_file(FINALITY_SUITE, "finality suite", FINALITY_SUITE_REQUIRED, errors)
    check_file(REPORT_BUILDER, "finality report builder", REPORT_BUILDER_REQUIRED, errors)


def main() -> int:
    errors: list[str] = []
    validate_workflow(errors)
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: KuString runtime finality CI workflow checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
