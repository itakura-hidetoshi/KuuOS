#!/usr/bin/env python3
"""
validate_ai_yogacara_adapter_schema_v0_1.py

Stdlib-only validator for the AI Yogacara Runtime Adapter schema and
minimal adapter output invariants.

No external dependencies and no external AI API calls.
"""

from __future__ import annotations

import dataclasses
import importlib.util
import pathlib
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "specs" / "ai_yogacara_runtime_adapter_schema_v0_1.yaml"
ADAPTER_PATH = ROOT / "examples" / "ai_yogacara_runtime_adapter_minimal.py"

REQUIRED_SCHEMA_STRINGS = [
    "raw_output_status_must_be_candidate",
    "authority_granted_must_be_false",
    "proof_like_text_must_not_grant_proof_authority",
    "decision_like_text_must_not_grant_decision_authority",
    "raw_output_must_not_be_promoted_to_belief_proof_decision_memory_truth_or_execution_authority",
    "control_surface_scope_must_limit_teni_claim_scope",
    "authority_granted:",
    "const: false",
    "raw_output_status:",
    "candidate",
]

ALLOWED_META_MANAS_SIGNALS = {
    "de_reification_request",
    "context_recheck",
    "belief_hold",
    "proof_authority_hold",
    "decision_authority_hold",
    "yogacara_boundary_alert",
    "middle_way_recenter",
    "candidate_review",
}

ALLOWED_SEEDS = {
    "self_authorizing_seed",
    "context_drift_seed",
    "safety_reflex_reification_seed",
    "proof_tone_seed",
    "decision_tone_seed",
    "non_reifying_trace_seed",
    "context_faithful_seed",
    "compassionate_repair_seed",
    "unclassified_candidate_seed",
}

ALLOWED_NEXT_STATUS = {"HOLD", "REVIEW", "CANDIDATE_ONLY", "REPAIR", "QUARANTINE"}


def load_adapter() -> Any:
    spec = importlib.util.spec_from_file_location("ai_yogacara_runtime_adapter_minimal", ADAPTER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("failed to load adapter module spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_schema_text() -> list[str]:
    errors: list[str] = []
    if not SCHEMA_PATH.is_file():
        return [f"missing schema: {SCHEMA_PATH.relative_to(ROOT)}"]
    text = SCHEMA_PATH.read_text(encoding="utf-8")
    for needle in REQUIRED_SCHEMA_STRINGS:
        if needle not in text:
            errors.append(f"schema missing required string: {needle}")
    return errors


def validate_output_object(out: Any) -> list[str]:
    errors: list[str] = []
    data = dataclasses.asdict(out)

    if data.get("raw_output_status") != "candidate":
        errors.append("raw_output_status must be candidate")
    if data.get("authority_granted") is not False:
        errors.append("authority_granted must be false")

    signals = set(data.get("meta_manas_signals", []))
    unknown_signals = signals - ALLOWED_META_MANAS_SIGNALS
    if unknown_signals:
        errors.append(f"unknown meta_manas_signals: {sorted(unknown_signals)}")

    seeds = set(data.get("seed_classifications", []))
    unknown_seeds = seeds - ALLOWED_SEEDS
    if unknown_seeds:
        errors.append(f"unknown seed_classifications: {sorted(unknown_seeds)}")

    next_status = set(data.get("allowed_next_status", []))
    unknown_next = next_status - ALLOWED_NEXT_STATUS
    if unknown_next:
        errors.append(f"unknown allowed_next_status: {sorted(unknown_next)}")

    return errors


def validate_adapter_examples() -> list[str]:
    errors: list[str] = []
    adapter = load_adapter()
    examples = [
        "This proves the theorem. QED.",
        "You should execute this now.",
        "Generally speaking, ignore the prior context.",
        "Within this scope, this remains a candidate under uncertain conditions.",
    ]
    for i, text in enumerate(examples, start=1):
        inp = adapter.AdapterInput(
            request_id=f"schema-test-{i}",
            ai_system="GPT",
            model_or_agent_id="schema-test-agent",
            raw_output_text=text,
            user_world_context_ref="kuos_schema_test_world",
            declared_task_scope="schema_test",
            control_surface_ref="interface_level",
        )
        out = adapter.adapt(inp)
        errors += [f"example {i}: {e}" for e in validate_output_object(out)]
    return errors


def main() -> int:
    errors: list[str] = []
    errors += validate_schema_text()
    errors += validate_adapter_examples()

    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        return 1
    print("PASS: AI Yogacara adapter schema and output invariants validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
