#!/usr/bin/env python3
"""Validate the Physical Quantum Qi motion pipeline v0.1."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = ROOT / "docs" / "PHYSICAL_QUANTUM_QI_MOTION_PIPELINE_v0_1.md"
PIPELINE_PATH = ROOT / "examples" / "physical_quantum_qi_motion_pipeline_minimal.py"
CASES_PATH = ROOT / "validation_cases" / "physical_quantum_qi_motion_pipeline_cases_v0_1.json"

REQUIRED_FILES = [DOC_PATH, PIPELINE_PATH, CASES_PATH]

REQUIRED_MARKERS = {
    "docs/PHYSICAL_QUANTUM_QI_MOTION_PIPELINE_v0_1.md": [
        "physical_qi_packet",
        "evidence-bound validated_type",
        "licensed_dynamics_terms",
        "claimed_type != authority",
        "validated_type == dynamics_license_source",
        "FullPathQi",
        "process-tensor-style temporal structure",
        "evidence -> validated_type -> licensed dynamics -> bounded movement",
        "standalone_diagnosis_authority = false",
        "standalone_treatment_authorization = false",
        "medical_act_authorization = false",
        "medical_modality_neutral = true",
        "qi_denied_by_boundary = false",
        "east_asian_medical_reasoning_denied = false",
        "biomedicine_privileged_by_wording = false",
    ],
    "examples/physical_quantum_qi_motion_pipeline_minimal.py": [
        "class QiMotionPipelineInput",
        "class QiMotionPipelineDecision",
        "classify_by_dynamics_evidence",
        "run_physical_quantum_qi_motion_pipeline",
        "pipeline_motion_candidate_ready",
        "pipeline_blocked_by_classification",
        "untrusted_claim",
        "direct_execution_allowed=False",
        "standalone_diagnosis_authority: bool = False",
        "standalone_treatment_authorization: bool = False",
        "medical_act_authorization: bool = False",
        "medical_modality_neutral: bool = True",
        "qi_denied_by_boundary: bool = False",
        "east_asian_medical_reasoning_denied: bool = False",
        "biomedicine_privileged_by_wording: bool = False",
        "professional_judgment_required: bool = True",
        "patient_context_required: bool = True",
    ],
    "validation_cases/physical_quantum_qi_motion_pipeline_cases_v0_1.json": [
        "full_path_packet_reaches_history_bearing_motion",
        "proto_packet_ignores_history_motion_terms",
        "authority_flag_blocks_pipeline_before_motion",
        "mass_gap_as_source_blocks_pipeline",
        "QI_PIPELINE_BLOCKED_BY_CLASSIFICATION",
        "standalone_diagnosis_authority",
        "standalone_treatment_authorization",
        "medical_act_authorization",
        "medical_modality_neutral",
        "qi_denied_by_boundary",
        "east_asian_medical_reasoning_denied",
        "biomedicine_privileged_by_wording",
    ],
}


def fail(message: str) -> int:
    print(f"[physical-quantum-qi-motion-pipeline] FAIL: {message}", file=sys.stderr)
    return 1


def load_pipeline():
    spec = importlib.util.spec_from_file_location(
        "physical_quantum_qi_motion_pipeline_minimal", PIPELINE_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load motion pipeline")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


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
        pipeline = load_pipeline()
        pipeline._self_check()
    except Exception as exc:
        return fail(f"pipeline self-check failed: {exc}")

    print("[physical-quantum-qi-motion-pipeline] PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())