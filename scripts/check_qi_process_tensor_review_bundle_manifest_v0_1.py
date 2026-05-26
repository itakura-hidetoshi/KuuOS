#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifests" / "qi_process_tensor_review_bundle_manifest_v0_1.json"

REQUIRED_BOUNDARIES = {
    "proposal_artifact_only",
    "index_only",
    "summary_only",
    "suite_only",
    "workflow_ci_only",
    "release_only",
    "finality_only",
    "additive_only_future",
    "overwrite_forbidden",
    "no_probe_execution_authority",
    "no_next_tick_execution_authority",
    "no_control_packet_authority_from_review_artifacts",
    "no_memory_overwrite_authority",
}

FILE_GROUPS = [
    "runtime_files",
    "script_files",
    "test_files",
    "packet_files",
    "docs_files",
    "workflow_files",
    "example_files",
]


def load_json(path: pathlib.Path) -> dict:
    if not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def main() -> int:
    errors: list[str] = []
    manifest = load_json(MANIFEST)
    if not manifest:
        errors.append("manifest_missing_or_invalid")
    if manifest.get("manifest_version") != "qi_process_tensor_review_bundle_manifest_v0_1":
        errors.append("manifest_version_mismatch")
    if manifest.get("bundle_status") != "QI_PROCESS_TENSOR_REVIEW_BUNDLE_MANIFEST_READY":
        errors.append("bundle_status_mismatch")
    if manifest.get("bundle_scope") != "qi-process-tensor-review-only":
        errors.append("bundle_scope_mismatch")
    if manifest.get("authority") != "none":
        errors.append("authority_not_none")
    if manifest.get("review_only") is not True:
        errors.append("review_only_not_true")
    if manifest.get("read_only") is not True:
        errors.append("read_only_not_true")
    for key in [
        "grants_execution_authority",
        "grants_probe_execution_authority",
        "grants_next_tick_execution_authority",
        "grants_control_packet_authority",
        "grants_memory_overwrite_authority",
    ]:
        if manifest.get(key) is not False:
            errors.append(f"{key}_not_false")

    boundaries = set(manifest.get("required_boundaries", []))
    missing_boundaries = sorted(REQUIRED_BOUNDARIES - boundaries)
    if missing_boundaries:
        errors.append("missing_boundaries:" + ",".join(missing_boundaries))

    seen: set[str] = set()
    for group in FILE_GROUPS:
        files = manifest.get(group)
        if not isinstance(files, list) or not files:
            errors.append(f"{group}_missing_or_empty")
            continue
        for item in files:
            if not isinstance(item, str) or not item:
                errors.append(f"{group}_contains_invalid_path")
                continue
            if item in seen:
                errors.append(f"duplicate_file:{item}")
            seen.add(item)
            if not (ROOT / item).is_file():
                errors.append(f"missing_file:{item}")

    if not any(path.endswith("run_qi_process_tensor_review_checks_v0_1.py") for path in manifest.get("script_files", [])):
        errors.append("suite_runner_not_listed")
    if not any(path.endswith("check_qi_process_tensor_review_finality_packets_v0_1.py") for path in manifest.get("script_files", [])):
        errors.append("finality_packet_checker_not_listed")
    if not any(path.endswith("qi_process_tensor_review_release_packet_v0_1.json") for path in manifest.get("packet_files", [])):
        errors.append("release_packet_not_listed")
    if not any(path.endswith("qi_process_tensor_review_finality_packet_v0_1.json") for path in manifest.get("packet_files", [])):
        errors.append("finality_packet_not_listed")
    if not any(path.endswith("qi-process-tensor-review.yml") for path in manifest.get("workflow_files", [])):
        errors.append("github_actions_workflow_not_listed")
    if not any(path.endswith("qi_persistent_supervisor_operator_runbook_v0_1.md") for path in manifest.get("docs_files", [])):
        errors.append("runbook_not_listed")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi process tensor review bundle manifest check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
