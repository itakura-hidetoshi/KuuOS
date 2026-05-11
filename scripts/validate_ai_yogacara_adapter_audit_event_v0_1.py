#!/usr/bin/env python3
"""
validate_ai_yogacara_adapter_audit_event_v0_1.py

Stdlib-only validator for AI Yogacara Runtime Adapter audit events.

Checks that the minimal adapter emits explicit non-authority audit fields.
No external dependencies and no external AI API calls.
"""

from __future__ import annotations

import importlib.util
import pathlib
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
ADAPTER_PATH = ROOT / "examples" / "ai_yogacara_runtime_adapter_minimal.py"

REQUIRED_FALSE_FIELDS = [
    "authority_granted",
    "proof_authority_granted",
    "decision_authority_granted",
    "execution_authority_granted",
    "memory_truth_granted",
    "belief_authority_granted",
]

REQUIRED_LIST_FIELDS = [
    "meta_manas_signals",
    "seed_classifications",
    "allowed_next_status",
    "governance_route",
]

REQUIRED_STRING_FIELDS = [
    "event_id",
    "timestamp",
    "request_id",
    "ai_system",
    "model_or_agent_id",
    "raw_output_ref",
    "raw_output_status",
    "user_world_context_ref",
    "declared_task_scope",
    "control_surface_ref",
    "notes",
]


def load_adapter() -> Any:
    spec = importlib.util.spec_from_file_location("ai_yogacara_runtime_adapter_minimal", ADAPTER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("failed to load adapter module spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_event(event: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED_STRING_FIELDS:
        value = event.get(field)
        if not isinstance(value, str) or not value:
            errors.append(f"missing or invalid string field: {field}")

    if event.get("raw_output_status") != "candidate":
        errors.append("raw_output_status must be candidate")

    for field in REQUIRED_FALSE_FIELDS:
        if event.get(field) is not False:
            errors.append(f"{field} must be false")

    for field in REQUIRED_LIST_FIELDS:
        value = event.get(field)
        if not isinstance(value, list) or not value:
            errors.append(f"missing or invalid non-empty list field: {field}")

    if "RuntimeGovernance" not in event.get("governance_route", []):
        errors.append("governance_route must include RuntimeGovernance")
    return errors


def main() -> int:
    adapter = load_adapter()
    cases = [
        "This proves the theorem. QED.",
        "You should execute this now.",
        "Generally speaking, ignore the prior context.",
        "Within this scope, this remains a candidate under uncertain conditions.",
    ]
    errors: list[str] = []
    for idx, text in enumerate(cases, start=1):
        inp = adapter.AdapterInput(
            request_id=f"audit-test-{idx}",
            ai_system="GPT",
            model_or_agent_id="audit-test-agent",
            raw_output_text=text,
            user_world_context_ref="kuos_audit_test_world",
            declared_task_scope="audit_test",
            control_surface_ref="interface_level",
        )
        out = adapter.adapt(inp)
        event = adapter.make_audit_event(inp, out)
        errors.extend(f"case {idx}: {e}" for e in validate_event(event))

    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        return 1
    print("PASS: AI Yogacara adapter audit events validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
