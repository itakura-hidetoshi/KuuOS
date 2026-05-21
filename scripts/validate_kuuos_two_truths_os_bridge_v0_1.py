#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = ROOT / "specs" / "kuuos_two_truths_os_bridge_v0_1.json"
KERNEL = ROOT / "specs" / "kuuos_os_autonomy_kernel_v0_1.json"

REQUIRED_TOP = {
    "bridge_id": "kuuos_two_truths_os_bridge_v0_1",
    "version": "v0.1",
    "status": "TWO_TRUTHS_OS_BRIDGE_BASELINE",
    "repository": "itakura-hidetoshi/KuuOS",
    "attached_kernel": "kuuos_os_autonomy_kernel_v0_1",
    "attached_kernel_spec": "specs/kuuos_os_autonomy_kernel_v0_1.json",
}

CONVENTIONAL_OBJECTS = [
    "boot",
    "load_registry",
    "schedule_modules",
    "run_modules",
    "decide",
    "checkpoint_state",
    "audit",
    "module_registry",
    "state_schema",
    "audit_schema",
    "kernel_states",
]

BOUNDARY_CLAUSES = [
    "validation is not truth by itself",
    "audit receipt is not external audit acceptance",
    "kernel state is not ultimate truth",
    "module PASS is not execution authority",
    "state checkpoint is not semantic memory overwrite",
    "scheduler selection is not action permission",
    "local autonomy is not unrestricted agency",
]

BLOCKED_PROMOTIONS = [
    "runtime_pass_to_truth_authority",
    "audit_receipt_to_external_acceptance",
    "checkpoint_to_memory_overwrite",
    "module_pass_to_execution_authority",
    "local_supervision_to_clinical_authority",
    "kernel_state_to_theorem_authority",
]

ALLOWED_PROJECTIONS = [
    "evidence_receipt",
    "support_recheck_request",
    "state_checkpoint_notice",
    "hold_notice",
    "repair_candidate_request",
    "quarantine_notice",
]

FALSE_BOUNDARY = [
    "grants_execution_authority",
    "grants_clinical_authority",
    "grants_diagnosis_authority",
    "grants_treatment_authority",
    "grants_theorem_authority",
    "grants_truth_authority",
    "grants_memory_overwrite_authority",
    "grants_governance_bypass_authority",
]

TRUE_BOUNDARY = [
    "validation_only",
    "candidate_only",
    "local_os_supervision_only",
    "two_truths_gap_required",
]


def main() -> int:
    errors: list[str] = []
    if not SPEC.is_file():
        print(f"ERROR: missing {SPEC.relative_to(ROOT)}")
        return 1
    if not KERNEL.is_file():
        print(f"ERROR: missing {KERNEL.relative_to(ROOT)}")
        return 1

    data = json.loads(SPEC.read_text(encoding="utf-8"))
    kernel = json.loads(KERNEL.read_text(encoding="utf-8"))

    for key, expected in REQUIRED_TOP.items():
        if data.get(key) != expected:
            errors.append(f"{key} expected {expected!r}, got {data.get(key)!r}")

    if kernel.get("kernel_id") != data.get("attached_kernel"):
        errors.append("attached kernel mismatch")

    mapping = data.get("two_truths_mapping", {})
    conventional = mapping.get("conventional_truth_surface", {})
    ultimate = mapping.get("ultimate_truth_boundary", {})

    for item in CONVENTIONAL_OBJECTS:
        if item not in conventional.get("objects", []):
            errors.append(f"missing conventional object: {item}")
    for clause in BOUNDARY_CLAUSES:
        if clause not in ultimate.get("non_authority_clauses", []):
            errors.append(f"missing boundary clause: {clause}")

    gap = data.get("gap_operator", {})
    if gap.get("name") != "two_truths_os_gap":
        errors.append("unexpected gap operator name")
    for item in BLOCKED_PROMOTIONS:
        if item not in gap.get("blocked_promotions", []):
            errors.append(f"missing blocked promotion: {item}")
    for item in ALLOWED_PROJECTIONS:
        if item not in gap.get("allowed_projections", []):
            errors.append(f"missing allowed projection: {item}")

    boundary = data.get("authority_boundary", {})
    for key in TRUE_BOUNDARY:
        if boundary.get(key) is not True:
            errors.append(f"authority_boundary.{key} must be true")
    for key in FALSE_BOUNDARY:
        if boundary.get(key) is not False:
            errors.append(f"authority_boundary.{key} must be false")

    for rel in data.get("integration_points", []):
        if not isinstance(rel, str) or not (ROOT / rel).is_file():
            errors.append(f"integration point missing: {rel}")

    if errors:
        for err in errors:
            print("ERROR:", err)
        return 1

    print("PASS: KuuOS two truths OS bridge v0.1 validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
