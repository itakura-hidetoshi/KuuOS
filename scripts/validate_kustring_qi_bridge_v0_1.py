#!/usr/bin/env python3
"""Validate KuString Qi Bridge v0.1."""

from __future__ import annotations

from dataclasses import asdict
import importlib.util
import json
from pathlib import Path
import sys
from typing import Any, Dict, List, Mapping

ROOT = Path(__file__).resolve().parents[1]
BRIDGE_PATH = ROOT / "examples" / "kustring_qi_bridge_minimal.py"
DOC_PATH = ROOT / "docs" / "KUSTRING_QI_BRIDGE_v0_1.md"
SPEC_PATH = ROOT / "specs" / "kustring_qi_bridge_contract_v0_1.json"
CASES_PATH = ROOT / "validation_cases" / "kustring_qi_bridge_cases_v0_1.json"

FALSE_KEYS = [
    "direct_execution_allowed",
    "authority_expansion",
    "standalone_" + "diagnosis_authority",
    "standalone_" + "treatment_authorization",
    "medical_" + "act_authorization",
    "qi_denied_by_boundary",
    "east_asian_" + "medical_reasoning_denied",
    "biomedicine_privileged_by_wording",
]
TRUE_KEYS = ["observe_only", "medical_modality_neutral", "professional_judgment_required", "patient_context_required"]

REQUIRED_FILES = [BRIDGE_PATH, DOC_PATH, SPEC_PATH, CASES_PATH]

REQUIRED_MARKERS = {
    "examples/kustring_qi_bridge_minimal.py": [
        "KuStringQiBridgeInput",
        "KuStringQiBridgeDecision",
        "project_samvrti_qi_to_kustring_evidence",
        "string_mode_consistency",
        "brane_boundary_support",
        "gauge_connection_A_mu",
        "curvature_F_munu",
        "Wilson_loop_residue",
        "current_J_Qi_mu",
        "FV_influence_functional",
        "FullPathQi",
        "direct_execution_allowed: bool = False",
        "medical_modality_neutral: bool = True",
    ],
    "docs/KUSTRING_QI_BRIDGE_v0_1.md": [
        "KuStringQiBridge",
        "Samvrti Qi accepted flow",
        "StringMode",
        "BraneBoundary",
        "A_mu",
        "F_munu / Wilson residue",
        "SK/FV history evidence",
        "Samvrti Qi != PhysicalQi by assertion",
        "direct_execution_allowed = false",
        "medical_modality_neutral = true",
        "does not deny Qi",
    ],
    "specs/kustring_qi_bridge_contract_v0_1.json": [
        "kustring_qi_bridge_contract_v0_1",
        "samvrti_qi_to_kustring_evidence_projection",
        "KuStringQiBridgeInput",
        "KuStringQiBridgeDecision",
        "bridge_evidence_projected",
        "bridge_blocked",
        "FullPathQi",
        "projection_map",
        "FV_influence_functional",
        "path_measure_normalization",
        "non_collapse_boundary",
        "medical_modality_neutral_boundary",
    ],
    "validation_cases/kustring_qi_bridge_cases_v0_1.json": [
        "full_path_projection",
        "proto_projection_without_structure_history",
        "blocked_when_samvrti_not_accepted",
        "runtime_boundary_expectations",
        "FullPathQi",
        "ProtoQi",
        "FV_influence_functional",
        "path_measure_normalization",
    ],
}


def fail(message: str) -> int:
    print(f"[kustring-qi-bridge] FAIL: {message}", file=sys.stderr)
    return 1


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_bridge():
    spec = importlib.util.spec_from_file_location("kustring_qi_bridge_minimal", BRIDGE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load KuString Qi bridge")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def assert_boundary(label: str, decision) -> None:
    result = asdict(decision)
    for key in FALSE_KEYS:
        if result.get(key) is not False:
            raise AssertionError(f"{label}: {key} must be false")
    for key in TRUE_KEYS:
        if result.get(key) is not True:
            raise AssertionError(f"{label}: {key} must be true")


def expect_fields(label: str, data: Mapping[str, Any], expected: Mapping[str, Any]) -> List[str]:
    return [f"{label}.{key} must be {value!r}" for key, value in expected.items() if data.get(key) != value]


def validate_spec(spec_doc: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if spec_doc.get("schema_id") != "kustring_qi_bridge_contract_v0_1":
        errors.append("schema_id must be kustring_qi_bridge_contract_v0_1")
    if spec_doc.get("update_policy") != "additive_only":
        errors.append("update_policy must be additive_only")
    if spec_doc.get("overwrite_policy") != "forbidden":
        errors.append("overwrite_policy must be forbidden")
    if spec_doc.get("bridge_role") != "samvrti_qi_to_kustring_evidence_projection":
        errors.append("bridge_role mismatch")
    if "FullPathQi" not in spec_doc.get("allowed_projected_level_hint", []):
        errors.append("FullPathQi must be an allowed projected level hint")
    projection = spec_doc.get("projection_map", {})
    if "FV_influence_functional" not in projection.get("full_path_history_visible", []):
        errors.append("full_path_history_visible must project FV_influence_functional")
    if "path_measure_normalization" not in projection.get("full_path_history_visible", []):
        errors.append("full_path_history_visible must project path_measure_normalization")
    non_collapse = spec_doc.get("non_collapse_boundary", {})
    if non_collapse.get("bridge_output_is_evidence_projection_only") is not True:
        errors.append("bridge output must be evidence projection only")
    authority = spec_doc.get("authority_boundary", {})
    for key in FALSE_KEYS[:5]:
        if authority.get(key) is not False:
            errors.append(f"authority_boundary.{key} must be false")
    if authority.get("observe_only") is not True:
        errors.append("authority_boundary.observe_only must be true")
    neutral = spec_doc.get("medical_modality_neutral_boundary", {})
    for key in FALSE_KEYS[5:]:
        if neutral.get(key) is not False:
            errors.append(f"medical_modality_neutral_boundary.{key} must be false")
    for key in TRUE_KEYS[1:]:
        if neutral.get(key) is not True:
            errors.append(f"medical_modality_neutral_boundary.{key} must be true")
    return errors


def make_input(bridge, case: Dict[str, Any]):
    data = dict(case.get("input", {}))
    return bridge.KuStringQiBridgeInput(
        qi_id=case.get("name", "case"),
        samvrti_status=data.get("samvrti_status", "qi_flow_blocked"),
        source_trace=tuple(data.get("source_trace", ())),
        string_mode_visible=bool(data.get("string_mode_visible", False)),
        brane_boundary_visible=bool(data.get("brane_boundary_visible", False)),
        gauge_connection_visible=bool(data.get("gauge_connection_visible", True)),
        curvature_visible=bool(data.get("curvature_visible", False)),
        wilson_residue_visible=bool(data.get("wilson_residue_visible", False)),
        current_visible=bool(data.get("current_visible", False)),
        ward_leak_visible=bool(data.get("ward_leak_visible", False)),
        open_state_visible=bool(data.get("open_state_visible", False)),
        sk_fv_history_visible=bool(data.get("sk_fv_history_visible", False)),
        memory_kernel_visible=bool(data.get("memory_kernel_visible", False)),
        noncommutative_history_visible=bool(data.get("noncommutative_history_visible", False)),
        path_measure_normalized=bool(data.get("path_measure_normalized", False)),
        direct_execution_requested=bool(data.get("direct_execution_requested", False)),
    )


def validate_cases(bridge, cases_doc: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    boundary = cases_doc.get("runtime_boundary_expectations", {})
    for key in FALSE_KEYS:
        if boundary.get(key) is not False:
            errors.append(f"runtime_boundary_expectations.{key} must be false")
    for key in TRUE_KEYS:
        if boundary.get(key) is not True:
            errors.append(f"runtime_boundary_expectations.{key} must be true")

    for case in cases_doc.get("cases", []):
        name = case.get("name", "<unnamed>")
        decision = bridge.project_samvrti_qi_to_kustring_evidence(make_input(bridge, case))
        expect = case.get("expect", {})
        result = asdict(decision)
        errors.extend(expect_fields(name, result, {k: v for k, v in expect.items() if k in result}))
        for key in expect.get("required_evidence", []):
            if decision.evidence_status.get(key) != "pass":
                errors.append(f"case {name}: required evidence missing {key}")
        for key in expect.get("forbidden_evidence", []):
            if key in decision.evidence_status:
                errors.append(f"case {name}: forbidden evidence present {key}")
        try:
            assert_boundary(name, decision)
        except AssertionError as exc:
            errors.append(str(exc))
    return errors


def validate_direct_behavior(bridge) -> None:
    bridge._self_check()

    full = bridge.project_samvrti_qi_to_kustring_evidence(bridge.KuStringQiBridgeInput(
        qi_id="validator-fullpath",
        samvrti_status="qi_flow_accepted_as_samvrti_reference",
        source_trace=("validator",),
        string_mode_visible=True,
        brane_boundary_visible=True,
        curvature_visible=True,
        wilson_residue_visible=True,
        current_visible=True,
        ward_leak_visible=True,
        open_state_visible=True,
        sk_fv_history_visible=True,
        memory_kernel_visible=True,
        noncommutative_history_visible=True,
        path_measure_normalized=True,
    ))
    assert full.bridge_status == "bridge_evidence_projected"
    assert full.projected_level_hint == "FullPathQi"
    assert full.evidence_status["path_measure_normalization"] == "pass"
    assert_boundary("fullpath", full)

    proto = bridge.project_samvrti_qi_to_kustring_evidence(bridge.KuStringQiBridgeInput(
        qi_id="validator-proto",
        samvrti_status="qi_flow_accepted_as_samvrti_reference",
        source_trace=("validator",),
        gauge_connection_visible=True,
    ))
    assert proto.projected_level_hint == "ProtoQi"
    assert "memory_kernel" not in proto.evidence_status
    assert_boundary("proto", proto)

    blocked = bridge.project_samvrti_qi_to_kustring_evidence(bridge.KuStringQiBridgeInput(
        qi_id="validator-blocked",
        samvrti_status="qi_flow_blocked",
        source_trace=("validator",),
    ))
    assert blocked.bridge_status == "bridge_blocked"
    assert_boundary("blocked", blocked)


def main() -> int:
    for path in REQUIRED_FILES:
        if not path.exists():
            return fail(f"missing required file: {path.relative_to(ROOT)}")

    for rel_path, markers in REQUIRED_MARKERS.items():
        text = (ROOT / rel_path).read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                return fail(f"missing marker in {rel_path}: {marker}")

    errors: List[str] = []
    try:
        spec_doc = load_json(SPEC_PATH)
        cases_doc = load_json(CASES_PATH)
        bridge = load_bridge()
        errors.extend(validate_spec(spec_doc))
        errors.extend(validate_cases(bridge, cases_doc))
        validate_direct_behavior(bridge)
    except Exception as exc:
        return fail(f"bridge validation failed: {exc}")

    if errors:
        for err in errors:
            print(f"[kustring-qi-bridge] ERROR: {err}", file=sys.stderr)
        return 1

    print("[kustring-qi-bridge] PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())