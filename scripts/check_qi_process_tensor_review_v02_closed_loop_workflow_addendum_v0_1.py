#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifests" / "qi_process_tensor_review_v02_closed_loop_workflow_addendum_v0_1.json"
WORKFLOW = ROOT / ".github" / "workflows" / "qi-process-tensor-review.yml"
PR_ENTRY_RUNNER = ROOT / "scripts" / "run_pr_entry_check_v0_4.py"
CLOSED_LOOP_SUITE = "run_qi_v02_memoryos_replay_loop_closure_checks.py"
ADDENDUM_CHECK = "check_qi_process_tensor_review_v02_closed_loop_workflow_addendum_v0_1.py"


def load(path: pathlib.Path) -> dict:
    if not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def validate_workflow_link(errors: list[str]) -> None:
    if not WORKFLOW.is_file():
        errors.append("workflow_missing")
        return

    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    if CLOSED_LOOP_SUITE in workflow_text:
        return

    delegated = (
        "run_pr_entry_check_v0_4.py" in workflow_text
        and "--check-id qi-process-review" in workflow_text
    )
    if not delegated:
        errors.append("workflow_missing_closed_loop_step")
        return

    if not PR_ENTRY_RUNNER.is_file():
        errors.append("pr_entry_runner_missing")
        return

    runner_text = PR_ENTRY_RUNNER.read_text(encoding="utf-8")
    if CLOSED_LOOP_SUITE not in runner_text:
        errors.append("pr_entry_runner_missing_closed_loop_suite")
    if ADDENDUM_CHECK not in runner_text:
        errors.append("pr_entry_runner_missing_addendum_check")


def main() -> int:
    errors: list[str] = []
    m = load(MANIFEST)
    if not m:
        errors.append("manifest_missing")
    expected = {
        "manifest_version": "qi_process_tensor_review_v02_closed_loop_workflow_addendum_v0_1",
        "addendum_status": "QI_PROCESS_TENSOR_REVIEW_V02_CLOSED_LOOP_WORKFLOW_ADDENDUM_READY",
        "extends_manifest": "manifests/qi_process_tensor_review_bundle_manifest_v0_1.json",
        "authority": "workflow_ci_only",
        "scheduler_update_scope": "replay_hint_only",
    }
    for key, value in expected.items():
        if m.get(key) != value:
            errors.append(f"{key}_mismatch")
    for key in ["additive_only", "does_not_replace_v0_1_manifest", "closed_loop_workflow_step_required", "scheduler_state_mutation_performed"]:
        if m.get(key) is not True:
            errors.append(f"{key}_not_true")
    for key in ["probe_execution_performed", "memory_write_performed", "world_update_performed", "control_packet_mutation_performed", "grants_probe_execution_authority", "grants_world_update_authority", "grants_control_packet_authority", "grants_memory_overwrite_authority"]:
        if m.get(key) is not False:
            errors.append(f"{key}_not_false")
    suite = m.get("closed_loop_suite")
    if suite != "scripts/run_qi_v02_memoryos_replay_loop_closure_checks.py":
        errors.append("closed_loop_suite_mismatch")
    if not (ROOT / suite).is_file():
        errors.append("closed_loop_suite_missing")

    validate_workflow_link(errors)

    for group in ["script_files", "workflow_files", "docs_files"]:
        files = m.get(group, [])
        if not isinstance(files, list) or not files:
            errors.append(f"{group}_missing")
            continue
        for item in files:
            if not (ROOT / item).is_file():
                errors.append(f"missing_file:{item}")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi process tensor review v0.2 closed-loop workflow addendum check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
