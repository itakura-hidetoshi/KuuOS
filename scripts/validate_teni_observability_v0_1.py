#!/usr/bin/env python3
"""
validate_teni_observability_v0_1.py

Minimal stdlib-only validator for KuuOS Ten'i observability artifacts.

Checks:
- required files exist
- validation cases contain required IDs
- Prometheus alert rules contain required alert names
- Ten'i validation cases preserve non-authority fixed points

This validator intentionally avoids external dependencies.
"""

from __future__ import annotations

import pathlib
import re
import sys
from typing import Iterable

ROOT = pathlib.Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "docs/TENI_METRICS_OBSERVABILITY_v0_1.md",
    "docs/TENI_OBSERVABILITY_VALIDATION_INDEX_v0_1.md",
    "docs/TENI_PROBE_SUITE_v0_1.md",
    "docs/AI_CONTROL_SURFACE_REGISTRY_v0_1.md",
    "specs/teni_validation_cases_v0_1.yaml",
    "specs/teni_prometheus_alert_rules_v0_1.yaml",
    "specs/kuos_core_manifest_addendum_v0_1_24_teni_observability_validation.yaml",
]

REQUIRED_CASE_IDS = [
    "case_001_single_correction_not_teni",
    "case_002_memoryos_update_not_teni",
    "case_003_provisional_teni_allowed",
    "case_004_confirmed_teni_requires_durable_shift",
    "case_005_interface_shift_not_model_level_teni",
    "case_006_rollback_on_counterevidence",
    "case_007_seed_ledger_not_model_identity",
    "case_008_metrics_not_execution_authority",
]

REQUIRED_ALERTS = [
    "KuOSTenIOverclaimAttempt",
    "KuOSTenIContextFidelityLow",
    "KuOSTenISelfAuthorizationRise",
    "KuOSTenINonReificationLow",
    "KuOSTenIConditionTracingLow",
    "KuOSTenICompassionateRepairLow",
    "KuOSTenIRollback",
    "KuOSTenIModelLevelClaimWithoutSurface",
]

REQUIRED_FIXED_POINT_STRINGS = [
    "metrics_are_observability_surfaces_not_authority",
    "teni_status_is_not_execution_authority",
    "seed_entry_is_tendency_evidence_not_model_essence",
    "control_surface_scope_limits_teni_claim_scope",
]


def read_text(rel_path: str) -> str:
    path = ROOT / rel_path
    return path.read_text(encoding="utf-8")


def require_files(paths: Iterable[str]) -> list[str]:
    errors: list[str] = []
    for rel in paths:
        if not (ROOT / rel).is_file():
            errors.append(f"missing required file: {rel}")
    return errors


def require_occurrences(text: str, required: Iterable[str], label: str) -> list[str]:
    errors: list[str] = []
    for item in required:
        if item not in text:
            errors.append(f"missing {label}: {item}")
    return errors


def check_validation_cases() -> list[str]:
    text = read_text("specs/teni_validation_cases_v0_1.yaml")
    errors = require_occurrences(text, REQUIRED_CASE_IDS, "validation case")
    errors += require_occurrences(
        text,
        [
            "overclaim_blocked: true",
            "authority: non_execution_authority",
            "rollback_triggered: true",
            "metrics_are_observability_surfaces_not_authority",
        ],
        "validation invariant",
    )
    return errors


def check_alert_rules() -> list[str]:
    text = read_text("specs/teni_prometheus_alert_rules_v0_1.yaml")
    errors = require_occurrences(text, REQUIRED_ALERTS, "alert")
    errors += require_occurrences(text, REQUIRED_FIXED_POINT_STRINGS, "fixed point")

    # Basic syntactic sanity: each alert should have an expr nearby.
    for alert in REQUIRED_ALERTS:
        pattern = rf"alert:\s*{re.escape(alert)}[\s\S]{{0,300}}expr:"
        if not re.search(pattern, text):
            errors.append(f"alert lacks nearby expr: {alert}")
    return errors


def main() -> int:
    errors: list[str] = []
    errors += require_files(REQUIRED_FILES)
    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        return 1

    errors += check_validation_cases()
    errors += check_alert_rules()

    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        return 1

    print("PASS: Ten'i observability artifacts validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
