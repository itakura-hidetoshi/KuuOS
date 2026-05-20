#!/usr/bin/env python3
"""Validate the Samvrti Qi to Physical Motion evidence builder v0.1."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = ROOT / "docs" / "SAMVRTI_QI_TO_PHYSICAL_MOTION_EVIDENCE_BUILDER_v0_1.md"
BUILDER_PATH = ROOT / "examples" / "samvrti_qi_to_physical_motion_evidence_builder_minimal.py"
CASES_PATH = ROOT / "validation_cases" / "samvrti_qi_to_physical_motion_evidence_builder_cases_v0_1.json"

REQUIRED_FILES = [DOC_PATH, BUILDER_PATH, CASES_PATH]

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
        "run_samvrti_to_physical_motion_builder",
        "builder_packet_routed_to_motion_pipeline",
        "builder_not_opened_by_samvrti",
        "untrusted_samvrti_projection",
        "direct_execution_allowed=False",
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
    except Exception as exc:
        return fail(f"builder self-check failed: {exc}")

    print("[samvrti-qi-to-physical-motion-evidence-builder] PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
