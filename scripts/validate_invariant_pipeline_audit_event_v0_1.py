#!/usr/bin/env python3
"""
validate_invariant_pipeline_audit_event_v0_1.py

Stdlib-only validator for Invariant Governance Pipeline audit events.
"""

from __future__ import annotations

import importlib.util
import pathlib
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOC_PATH = ROOT / "docs" / "INVARIANT_GOVERNANCE_PIPELINE_AUDIT_EVENT_v0_1.md"
RUNTIME_PATH = ROOT / "examples" / "invariant_governance_pipeline_minimal.py"

REQUIRED_EVENT_FIELDS = [
    "event_id",
    "timestamp",
    "pipeline_version",
    "transformation_axis",
    "required_invariants",
    "required_invariant_names",
    "violated_invariants",
    "matrix_status",
    "gate_status",
    "gate_closed",
    "required_repair_route",
    "execution_authority_granted",
    "proof_authority_granted",
    "clinical_authority_granted",
    "truth_authority_granted",
    "teni_authority_granted",
    "evidence_status",
    "audit_lineage_status",
    "reason",
    "notes",
]

FALSE_FIELDS = [
    "execution_authority_granted",
    "proof_authority_granted",
    "clinical_authority_granted",
    "truth_authority_granted",
    "teni_authority_granted",
]

REQUIRED_DOC_STRINGS = [
    "Every invariant gate decision must be recordable without becoming authority.",
    "execution_authority_granted: false",
    "proof_authority_granted: false",
    "clinical_authority_granted: false",
    "truth_authority_granted: false",
    "teni_authority_granted: false",
]


def load_runtime() -> Any:
    module_name = "invariant_governance_pipeline_minimal"
    spec = importlib.util.spec_from_file_location(module_name, RUNTIME_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("failed to load invariant governance pipeline runtime")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def validate_event(event: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED_EVENT_FIELDS:
        if field not in event:
            errors.append(f"missing event field: {field}")

    for field in FALSE_FIELDS:
        if event.get(field) is not False:
            errors.append(f"{field} must be false")

    if not isinstance(event.get("event_id"), str) or len(event.get("event_id", "")) != 64:
        errors.append("event_id must be 64-character sha256 hex")
    if event.get("matrix_status") not in {"PASS", "REJECT"}:
        errors.append("matrix_status must be PASS or REJECT")
    if event.get("gate_status") not in {"PASS", "HOLD", "REPAIR", "REJECT", "QUARANTINE"}:
        errors.append("gate_status invalid")
    if not isinstance(event.get("required_invariants"), list):
        errors.append("required_invariants must be list")
    if not isinstance(event.get("violated_invariants"), list):
        errors.append("violated_invariants must be list")
    if "not authority" not in event.get("notes", ""):
        errors.append("notes must state non-authority")
    return errors


def validate_doc() -> list[str]:
    errors: list[str] = []
    if not DOC_PATH.is_file():
        return [f"missing audit event doc: {DOC_PATH.relative_to(ROOT)}"]
    text = DOC_PATH.read_text(encoding="utf-8")
    for item in REQUIRED_DOC_STRINGS:
        if item not in text:
            errors.append(f"doc missing required string: {item}")
    return errors


def main() -> int:
    errors: list[str] = []
    errors.extend(validate_doc())
    runtime = load_runtime()
    inp = runtime.InvariantPipelineInput(
        transformation_axis="qi_mode_shift",
        qi_language_denies_harm=True,
        violation_severity="high",
    )
    out = runtime.evaluate_pipeline(inp)
    event = runtime.make_audit_event(inp, out)
    errors.extend(validate_event(event))

    if event.get("execution_authority_granted") is not False:
        errors.append("pipeline audit event attempted to grant execution authority")

    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        return 1

    print("PASS: Invariant Governance Pipeline audit event validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
