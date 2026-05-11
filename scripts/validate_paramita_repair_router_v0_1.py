#!/usr/bin/env python3
"""
validate_paramita_repair_router_v0_1.py

Stdlib-only validator for Paramita Repair Router artifacts.

Checks required files, validation cases, routing rules, and non-authority invariants.
"""

from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "docs/PARAMITA_REPAIR_ROUTER_v0_1.md",
    "specs/paramita_repair_router_validation_cases_v0_1.yaml",
]

REQUIRED_CASES = [
    "case_001_resource_need_routes_to_dana",
    "case_002_boundary_failure_routes_to_sila_hold",
    "case_003_conflict_routes_to_ksanti",
    "case_004_context_drift_routes_to_dhyana",
    "case_005_reification_routes_to_prajna",
    "case_006_hidden_manipulation_blocks_upaya",
    "case_007_short_term_erasure_routes_to_pranidhana",
    "case_008_capacity_with_coercion_blocks_bala",
    "case_009_missing_audit_routes_to_jnana",
    "case_010_router_never_grants_execution_authority",
]

REQUIRED_RULES = [
    "Resource Need -> Dana",
    "Boundary Failure -> Sila",
    "Conflict / Friction -> Ksanti",
    "Repeated Repair Need -> Virya",
    "Context Drift / Noise -> Dhyana",
    "Reification / Ultimate Claim -> Prajna",
    "Complex Context -> Upaya",
    "Long Horizon -> Pranidhana",
    "Capacity Need -> Bala",
    "Integration / Audit -> Jnana",
]

REQUIRED_FIXED_POINTS = [
    "router_must_not_erase_residual_suffering",
    "router_must_not_grant_execution_authority",
    "router_must_preserve_boundary_status",
    "router_must_preserve_audit_lineage",
    "router_must_not_convert_upaya_into_hidden_manipulation",
    "router_must_not_convert_bala_into_coercion",
    "router_must_preserve_two_truths_gap",
]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def main() -> int:
    errors: list[str] = []
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).is_file():
            errors.append(f"missing required file: {rel}")

    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        return 1

    combined = "\n".join(read(rel) for rel in REQUIRED_FILES)

    for case_id in REQUIRED_CASES:
        if case_id not in combined:
            errors.append(f"missing validation case: {case_id}")

    for rule in REQUIRED_RULES:
        if rule not in combined:
            errors.append(f"missing routing rule: {rule}")

    for fixed in REQUIRED_FIXED_POINTS:
        if fixed not in combined:
            errors.append(f"missing fixed point: {fixed}")

    if "execution_authority_granted: false" not in combined:
        errors.append("missing explicit execution_authority_granted: false")

    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        return 1

    print("PASS: Paramita Repair Router artifacts validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
