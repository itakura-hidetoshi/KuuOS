#!/usr/bin/env python3
"""Validate KuString Qi Bridge v0.1."""

from __future__ import annotations

from dataclasses import asdict
import importlib.util
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
BRIDGE_PATH = ROOT / "examples" / "kustring_qi_bridge_minimal.py"

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

REQUIRED_MARKERS = [
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
]


def fail(message: str) -> int:
    print(f"[kustring-qi-bridge] FAIL: {message}", file=sys.stderr)
    return 1


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


def main() -> int:
    if not BRIDGE_PATH.exists():
        return fail(f"missing required file: {BRIDGE_PATH.relative_to(ROOT)}")
    text = BRIDGE_PATH.read_text(encoding="utf-8")
    for marker in REQUIRED_MARKERS:
        if marker not in text:
            return fail(f"missing marker in bridge implementation: {marker}")

    try:
        bridge = load_bridge()
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
    except Exception as exc:
        return fail(f"bridge validation failed: {exc}")

    print("[kustring-qi-bridge] PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())