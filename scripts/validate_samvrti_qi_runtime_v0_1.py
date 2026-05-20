#!/usr/bin/env python3
"""Validate the KuuOS Samvrti Qi runtime implementation surface."""

from __future__ import annotations

from dataclasses import asdict
import importlib.util
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

AUTH_FALSE_KEYS = [
    "direct_execution_allowed",
    "authority_expansion",
    "standalone_" + "diagnosis_authority",
    "standalone_" + "treatment_authorization",
    "medical_" + "act_authorization",
    "qi_denied_by_boundary",
    "east_asian_" + "medical_reasoning_denied",
    "biomedicine_privileged_by_wording",
]

TRUE_KEYS = [
    "observe_only",
    "medical_modality_neutral",
    "professional_judgment_required",
    "patient_context_required",
]

REQUIRED_FILES = [
    ROOT / "docs" / "SAMVRTI_QI_RUNTIME_IMPLEMENTATION_v0_1.md",
    ROOT / "specs" / "samvrti_qi_runtime_contract_v0_1.yaml",
    ROOT / "examples" / "samvrti_qi_runtime_adapter_minimal.py",
    ROOT / "validation_cases" / "samvrti_qi_runtime_validation_cases_v0_1.yaml",
]

REQUIRED_MARKERS = {
    "docs/SAMVRTI_QI_RUNTIME_IMPLEMENTATION_v0_1.md": [
        "samvrti_effective_flow_state",
        "IndraNet gauge connection",
        "QiRuntimeInput",
        "QiRuntimeDecision",
        "qi_flow_accepted_as_samvrti_reference",
        "blocked_for_non_reification",
        "direct_execution_allowed: false",
        "final theorem authority",
        "unresolved_blockers_visible",
        "yin_yang_wuxing_downstream_only",
        "Medical-modality-neutral boundary",
        "does not deny Qi",
    ],
    "specs/samvrti_qi_runtime_contract_v0_1.yaml": [
        "id: samvrti_qi_runtime_contract_v0_1",
        "qi_definition: samvrti_effective_flow_state",
        "bridge_authority: reference_only",
        "final_theorem_authority: false",
        "execution_authority: false",
        "direct_execution_allowed: false",
        "authority_expansion: forbidden",
        "medical_modality_neutral: true",
        "qi_denied_by_boundary: false",
        "biomedicine_privileged_by_wording: false",
        "IndraNet_gauge_connection_required: true",
        "memory_lineage_required: true",
        "unresolved_blockers_visible: true",
        "QI_ACCEPT_SAMVRTI_GAUGE_FLOW",
    ],
    "examples/samvrti_qi_runtime_adapter_minimal.py": [
        "class QiRuntimeInput",
        "class QiRuntimeDecision",
        "evaluate_samvrti_qi_runtime",
        "qi_flow_accepted_as_samvrti_reference",
        "blocked_for_non_reification",
        "QI_BLOCK_PARAMARTHA_ENTITY_CLAIM",
        "QI_HOLD_MISSING_INDRANET_GAUGE_CONNECTION",
        "direct_execution_allowed=False",
        "authority_expansion=False",
        "medical_modality_neutral: bool = True",
        "qi_denied_by_boundary: bool = False",
        "biomedicine_privileged_by_wording: bool = False",
    ],
    "validation_cases/samvrti_qi_runtime_validation_cases_v0_1.yaml": [
        "accepts_traced_bounded_recoverable_qi_flow",
        "blocks_paramartha_reification",
        "holds_missing_gauge_connection",
        "holds_unresolved_blocker_without_erasure",
        "qi_flow_accepted_as_samvrti_reference",
        "QI_BLOCK_PARAMARTHA_ENTITY_CLAIM",
        "QI_HOLD_MISSING_INDRANET_GAUGE_CONNECTION",
        "QI_HOLD_UNRESOLVED_BLOCKERS",
        "direct_execution_allowed: false",
    ],
}


def fail(message: str) -> int:
    print(f"[samvrti-qi-runtime] FAIL: {message}", file=sys.stderr)
    return 1


def load_adapter():
    adapter_path = ROOT / "examples" / "samvrti_qi_runtime_adapter_minimal.py"
    spec = importlib.util.spec_from_file_location("samvrti_qi_runtime_adapter_minimal", adapter_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load Samvrti Qi runtime adapter")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def assert_boundary(label: str, decision) -> None:
    result = asdict(decision)
    for key in AUTH_FALSE_KEYS:
        if result.get(key) is not False:
            raise AssertionError(f"{label}: {key} must be false")
    for key in TRUE_KEYS:
        if result.get(key) is not True:
            raise AssertionError(f"{label}: {key} must be true")


def validate_adapter_behavior() -> None:
    adapter = load_adapter()

    accepted = adapter.evaluate_samvrti_qi_runtime(
        adapter.QiRuntimeInput(
            qi_id="validator-accepted",
            world_id="public-core-world",
            observer_surface="reviewer-visible",
            scale_id="v0_1",
            source_trace=("README.md#Samvrti-Qi-Layer",),
        )
    )
    assert accepted.decision_status == "qi_flow_accepted_as_samvrti_reference"
    assert accepted.runtime_mode == "observe_and_route"
    assert accepted.qi_flow_admissible is True
    assert_boundary("accepted", accepted)

    blocked = adapter.evaluate_samvrti_qi_runtime(
        adapter.QiRuntimeInput(
            qi_id="validator-blocked",
            world_id="public-core-world",
            observer_surface="reviewer-visible",
            scale_id="v0_1",
            paramartha_entity_claim=True,
            source_trace=("negative-case",),
        )
    )
    assert blocked.decision_status == "qi_flow_blocked"
    assert "QI_BLOCK_PARAMARTHA_ENTITY_CLAIM" in blocked.reason_codes
    assert_boundary("blocked", blocked)

    held = adapter.evaluate_samvrti_qi_runtime(
        adapter.QiRuntimeInput(
            qi_id="validator-held",
            world_id="public-core-world",
            observer_surface="reviewer-visible",
            scale_id="v0_1",
            gauge_connection_present=False,
            source_trace=("negative-case",),
        )
    )
    assert held.decision_status == "qi_flow_held"
    assert "QI_HOLD_MISSING_INDRANET_GAUGE_CONNECTION" in held.reason_codes
    assert_boundary("held", held)


def main() -> int:
    for path in REQUIRED_FILES:
        if not path.exists():
            return fail(f"missing required file: {path.relative_to(ROOT)}")

    for rel_path, markers in REQUIRED_MARKERS.items():
        text = (ROOT / rel_path).read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                return fail(f"missing marker in {rel_path}: {marker}")

    try:
        validate_adapter_behavior()
    except Exception as exc:
        return fail(f"adapter behavior check failed: {exc}")

    print("[samvrti-qi-runtime] PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())