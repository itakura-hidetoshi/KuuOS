#!/usr/bin/env python3
"""Validate the Samvrti Qi to Physical Motion evidence builder v0.1."""

from __future__ import annotations

from dataclasses import asdict
import importlib.util
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = ROOT / "docs" / "SAMVRTI_QI_TO_PHYSICAL_MOTION_EVIDENCE_BUILDER_v0_1.md"
BUILDER_PATH = ROOT / "examples" / "samvrti_qi_to_physical_motion_evidence_builder_minimal.py"
CASES_PATH = ROOT / "validation_cases" / "samvrti_qi_to_physical_motion_evidence_builder_cases_v0_1.json"

REQUIRED_FILES = [DOC_PATH, BUILDER_PATH, CASES_PATH]

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

REQUIRED_MARKERS = {
    "docs/SAMVRTI_QI_TO_PHYSICAL_MOTION_EVIDENCE_BUILDER_v0_1.md": [
        "conservative evidence builder",
        "qi_flow_accepted_as_samvrti_reference != FullPathQi",
        "physical_qi_packet_candidate",
        "licensed motion terms",
        "observed conventional flow",
        "direct_execution_allowed",
    ],
    "examples/samvrti_qi_to_physical_motion_evidence_builder_minimal.py": [
        "class QiEvidenceBuilderInput",
        "class QiEvidenceBuilderDecision",
        "build_conservative_evidence",
        "KuStringQiBridge",
        "_bridge_from_builder_input",
        "bridge_packet_routed_to_motion_pipeline".replace("bridge_", "builder_"),
        "builder_not_opened_by_samvrti",
        "builder_blocked_by_kustring_bridge",
        "bridge_projected_level_hint",
        "untrusted_samvrti_projection",
        "direct_execution_allowed",
        "medical_modality_neutral",
    ],
    "validation_cases/samvrti_qi_to_physical_motion_evidence_builder_cases_v0_1.json": [
        "full_path_evidence_reaches_full_path_motion",
        "structural_only_reaches_proto_not_history_motion",
        "samvrti_direct_execution_request_blocks_builder",
        "FullPathQi",
        "ProtoQi",
    ],
}


def fail(message: str) -> int:
    print(f"[samvrti-qi-to-physical-motion-evidence-builder] FAIL: {message}", file=sys.stderr)
    return 1


def load_builder():
    spec = importlib.util.spec_from_file_location(
        "samvrti_qi_to_physical_motion_evidence_builder_minimal", BUILDER_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load evidence builder")
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
    for path in REQUIRED_FILES:
        if not path.exists():
            return fail(f"missing required file: {path.relative_to(ROOT)}")

    for rel_path, markers in REQUIRED_MARKERS.items():
        text = (ROOT / rel_path).read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                return fail(f"missing marker in {rel_path}: {marker}")

    try:
        builder = load_builder()
        builder._self_check()

        full = builder.run_samvrti_to_physical_motion_builder(
            builder.QiEvidenceBuilderInput(
                qi_id="validator-fullpath-builder",
                world_id="public-core-world",
                observer_surface="reviewer-visible",
                scale_id="v0_1",
                source_trace=("validator",),
                structural_support_present=True,
                transport_evidence_present=True,
                current_evidence_present=True,
                ward_evidence_present=True,
                open_system_evidence_present=True,
                full_path_evidence_present=True,
                numeric_terms={"sk_fv_history_flow": 1.0, "memory_kernel_backflow": 0.5},
            )
        )
        assert full.bridge_status == "bridge_evidence_projected"
        assert full.bridge_projected_level_hint == "FullPathQi"
        assert full.packet_validated_type == "FullPathQi"
        assert_boundary("full", full)

        blocked = builder.run_samvrti_to_physical_motion_builder(
            builder.QiEvidenceBuilderInput(
                qi_id="validator-blocked-builder",
                world_id="public-core-world",
                observer_surface="reviewer-visible",
                scale_id="v0_1",
                source_trace=("validator",),
                numeric_terms={"sk_fv_history_flow": 1.0},
                direct_execution_requested=True,
            )
        )
        assert blocked.builder_status == "builder_not_opened_by_samvrti"
        assert blocked.bridge_status == "bridge_blocked"
        assert_boundary("blocked", blocked)
    except Exception as exc:
        return fail(f"builder self-check failed: {exc}")

    print("[samvrti-qi-to-physical-motion-evidence-builder] PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())