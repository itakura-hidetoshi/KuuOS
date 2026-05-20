#!/usr/bin/env python3
"""Validate the Physical Quantum Qi dynamics kernel v0.1.

This validator checks that the validated Qi type licenses only the appropriate
motion terms, that evidence is required for the selected dynamics level, and that
all outputs remain observe-only with no authority expansion.
"""

from __future__ import annotations

from dataclasses import asdict
import importlib.util
import json
from pathlib import Path
import sys
from typing import Any, Dict, List, Mapping

ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = ROOT / "docs" / "PHYSICAL_QUANTUM_QI_DYNAMICS_KERNEL_v0_1.md"
SPEC_PATH = ROOT / "specs" / "physical_quantum_qi_dynamics_kernel_v0_1.json"
ADAPTER_PATH = ROOT / "examples" / "physical_quantum_qi_dynamics_kernel_minimal.py"
CASES_PATH = ROOT / "validation_cases" / "physical_quantum_qi_dynamics_kernel_cases_v0_1.json"

REQUIRED_FILES = [DOC_PATH, SPEC_PATH, ADAPTER_PATH, CASES_PATH]

REQUIRED_MARKERS = {
    "docs/PHYSICAL_QUANTUM_QI_DYNAMICS_KERNEL_v0_1.md": [
        "validated_type",
        "licensed_dynamics_terms",
        "dynamics license",
        "FullPathQi",
        "sk_fv_history_flow",
        "memory_kernel_backflow",
        "process-tensor-style motion terms",
        "direct_execution_allowed = false",
        "authority_expansion = false",
        "standalone_diagnosis_authority = false",
        "standalone_treatment_authorization = false",
        "medical_act_authorization = false",
        "medical_modality_neutral = true",
        "qi_denied_by_boundary = false",
        "east_asian_medical_reasoning_denied = false",
        "biomedicine_privileged_by_wording = false",
    ],
    "specs/physical_quantum_qi_dynamics_kernel_v0_1.json": [
        "physical_quantum_qi_dynamics_kernel_v0_1",
        "validated_type_licenses_dynamics_terms",
        "licensed_terms_by_type",
        "required_evidence_by_type",
        "FullPathQi",
        "sk_fv_history_flow",
        "memory_kernel_backflow",
        "path_measure_normalization_guard",
        "direct_execution_allowed",
        "authority_expansion",
        "standalone_diagnosis_authority",
        "standalone_treatment_authorization",
        "medical_act_authorization",
        "medical_modality_neutral_boundary",
        "qi_denied_by_boundary",
        "east_asian_medical_reasoning_denied",
        "biomedicine_privileged_by_wording",
    ],
    "examples/physical_quantum_qi_dynamics_kernel_minimal.py": [
        "class QiDynamicsInput",
        "class QiDynamicsDecision",
        "evaluate_physical_quantum_qi_dynamics",
        "LICENSED_TERMS_BY_TYPE",
        "REQUIRED_EVIDENCE_BY_TYPE",
        "QI_DYN_ACCEPT_EVIDENCE_BOUND_MOTION_CANDIDATE",
        "QI_DYN_HOLD_REQUIRED_EVIDENCE_MISSING",
        "QI_DYN_BLOCK_AUTHORITY_EXPANSION_ATTEMPT",
        "direct_execution_allowed=False",
        "standalone_diagnosis_authority: bool = False",
        "standalone_treatment_authorization: bool = False",
        "medical_act_authorization: bool = False",
        "medical_modality_neutral: bool = True",
        "qi_denied_by_boundary: bool = False",
        "east_asian_medical_reasoning_denied: bool = False",
        "biomedicine_privileged_by_wording: bool = False",
    ],
    "validation_cases/physical_quantum_qi_dynamics_kernel_cases_v0_1.json": [
        "full_path_qi_licenses_history_bearing_motion",
        "proto_qi_ignores_unlicensed_memory_kernel",
        "physical_qi_holds_when_required_evidence_missing",
        "authority_expansion_blocks_motion",
        "sk_fv_history_flow",
        "memory_kernel_backflow",
        "QI_DYN_HOLD_REQUIRED_EVIDENCE_MISSING",
        "QI_DYN_BLOCK_AUTHORITY_EXPANSION_ATTEMPT",
        "standalone_diagnosis_authority",
        "standalone_treatment_authorization",
        "medical_act_authorization",
        "medical_modality_neutral",
        "qi_denied_by_boundary",
        "east_asian_medical_reasoning_denied",
        "biomedicine_privileged_by_wording",
    ],
}

MEDICAL_MODALITY_NEUTRAL_EXPECTATIONS = {
    "standalone_diagnosis_authority": False,
    "standalone_treatment_authorization": False,
    "medical_act_authorization": False,
    "medical_modality_neutral": True,
    "qi_denied_by_boundary": False,
    "east_asian_medical_reasoning_denied": False,
    "biomedicine_privileged_by_wording": False,
    "professional_judgment_required": True,
    "patient_context_required": True,
}


def fail(message: str) -> int:
    print(f"[physical-quantum-qi-dynamics-kernel] FAIL: {message}", file=sys.stderr)
    return 1


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_adapter():
    spec = importlib.util.spec_from_file_location("physical_quantum_qi_dynamics_kernel_minimal", ADAPTER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load Physical Quantum Qi dynamics kernel")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def false_authority() -> Dict[str, bool]:
    return {
        "execution_authority": False,
        "belief_commit_authority": False,
        "memory_overwrite_authority": False,
        "world_root_rewrite_authority": False,
        "safety_override_authority": False,
    }


def validate_spec(spec: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if spec.get("schema_id") != "physical_quantum_qi_dynamics_kernel_v0_1":
        errors.append("schema_id must be physical_quantum_qi_dynamics_kernel_v0_1")
    if spec.get("update_policy") != "additive_only":
        errors.append("update_policy must be additive_only")
    if spec.get("overwrite_policy") != "forbidden":
        errors.append("overwrite_policy must be forbidden")
    authority = spec.get("authority", {})
    for key in [
        "execution_authority",
        "belief_commit_authority",
        "memory_overwrite_authority",
        "world_root_rewrite_authority",
        "safety_override_authority",
        "direct_execution_allowed",
        "authority_expansion",
        "standalone_diagnosis_authority",
        "standalone_treatment_authorization",
        "medical_act_authorization",
    ]:
        if authority.get(key) is not False:
            errors.append(f"authority.{key} must be false")
    neutral = spec.get("medical_modality_neutral_boundary", {})
    for key, expected in MEDICAL_MODALITY_NEUTRAL_EXPECTATIONS.items():
        if neutral.get(key) is not expected:
            errors.append(f"medical_modality_neutral_boundary.{key} must be {expected}")
    licensed = spec.get("licensed_terms_by_type", {})
    if "memory_kernel_backflow" in licensed.get("ProtoQi", []):
        errors.append("ProtoQi must not license memory_kernel_backflow")
    if "sk_fv_history_flow" not in licensed.get("FullPathQi", []):
        errors.append("FullPathQi must license sk_fv_history_flow")
    return errors


def _assert_expected(name: str, result: Mapping[str, Any], expected: Mapping[str, Any]) -> List[str]:
    errors: List[str] = []
    for key, expected_value in expected.items():
        if key == "active_term":
            if expected_value not in result.get("active_terms", ()):
                errors.append(f"case {name}: expected active term {expected_value}")
        elif key == "ignored_term":
            if expected_value not in result.get("ignored_terms", ()):
                errors.append(f"case {name}: expected ignored term {expected_value}")
        elif key == "reason_code":
            if expected_value not in result.get("reason_codes", ()):
                errors.append(f"case {name}: expected reason code {expected_value}")
        else:
            actual = result.get(key)
            if actual != expected_value:
                errors.append(f"case {name}: expected {key}={expected_value!r}, got {actual!r}")
    return errors


def validate_cases(adapter: Any, cases_doc: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    for case in cases_doc.get("cases", []):
        name = case.get("name", "<unnamed>")
        authority = false_authority()
        authority.update(case.get("authority_override", {}))
        decision = adapter.evaluate_physical_quantum_qi_dynamics(
            adapter.QiDynamicsInput(
                packet_id=name,
                validated_type=case.get("validated_type", ""),
                evidence_status=case.get("evidence_status", {}),
                numeric_terms=case.get("numeric_terms", {}),
                authority=authority,
                direct_execution_requested=case.get("direct_execution_requested", False),
                unresolved_blockers=tuple(case.get("unresolved_blockers", ())),
            )
        )
        result = asdict(decision)
        expected = case.get("expect", {})
        errors.extend(_assert_expected(name, result, expected))
        errors.extend(_assert_expected(name, result, MEDICAL_MODALITY_NEUTRAL_EXPECTATIONS))
        if result.get("direct_execution_allowed") is not False:
            errors.append(f"case {name}: direct_execution_allowed must remain false")
        if result.get("authority_expansion") is not False:
            errors.append(f"case {name}: authority_expansion must remain false")
    return errors


def validate_adapter_behavior(adapter: Any) -> List[str]:
    errors: List[str] = []
    full_evidence = {key: "pass" for key in adapter.REQUIRED_EVIDENCE_BY_TYPE["FullPathQi"]}
    decision = adapter.evaluate_physical_quantum_qi_dynamics(
        adapter.QiDynamicsInput(
            packet_id="validator-fullpath",
            validated_type="FullPathQi",
            evidence_status=full_evidence,
            numeric_terms={"sk_fv_history_flow": 1.0, "memory_kernel_backflow": 0.5},
            authority=false_authority(),
        )
    )
    result = asdict(decision)
    if decision.motion_status != "qi_motion_candidate_ready":
        errors.append("FullPathQi should produce qi_motion_candidate_ready with complete evidence")
    if "sk_fv_history_flow" not in decision.active_terms:
        errors.append("FullPathQi should activate sk_fv_history_flow")
    if decision.direct_execution_allowed is not False:
        errors.append("direct_execution_allowed must remain false")
    errors.extend(_assert_expected("validator-fullpath", result, MEDICAL_MODALITY_NEUTRAL_EXPECTATIONS))

    proto_evidence = {key: "pass" for key in adapter.REQUIRED_EVIDENCE_BY_TYPE["ProtoQi"]}
    proto = adapter.evaluate_physical_quantum_qi_dynamics(
        adapter.QiDynamicsInput(
            packet_id="validator-proto",
            validated_type="ProtoQi",
            evidence_status=proto_evidence,
            numeric_terms={"gauge_connection_tendency": 0.2, "memory_kernel_backflow": 99.0},
            authority=false_authority(),
        )
    )
    proto_result = asdict(proto)
    if "memory_kernel_backflow" not in proto.ignored_terms:
        errors.append("ProtoQi must ignore memory_kernel_backflow")
    errors.extend(_assert_expected("validator-proto", proto_result, MEDICAL_MODALITY_NEUTRAL_EXPECTATIONS))
    return errors


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
        spec = load_json(SPEC_PATH)
        cases = load_json(CASES_PATH)
        adapter = load_adapter()
        errors: List[str] = []
        errors.extend(validate_spec(spec))
        errors.extend(validate_adapter_behavior(adapter))
        errors.extend(validate_cases(adapter, cases))
    except Exception as exc:  # pragma: no cover - CLI validator
        return fail(f"validator exception: {exc}")

    if errors:
        for err in errors:
            print(f"[physical-quantum-qi-dynamics-kernel] ERROR: {err}", file=sys.stderr)
        return 1

    print("[physical-quantum-qi-dynamics-kernel] PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())