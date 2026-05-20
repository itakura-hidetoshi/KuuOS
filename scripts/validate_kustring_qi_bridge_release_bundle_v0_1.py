#!/usr/bin/env python3
"""Validate KuString Qi Bridge release bundle v0.1."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "specs" / "kustring_qi_bridge_release_bundle_manifest_v0_1.json"
PACKET_PATH = ROOT / "specs" / "kustring_qi_bridge_release_packet_v0_1.json"
RUNNER_PATH = ROOT / "scripts" / "run_qi_motion_chain_checks_v0_1.py"
VALIDATOR_PATH = ROOT / "scripts" / "validate_kustring_qi_bridge_v0_1.py"

FALSE_INVARIANTS = [
    "direct_execution_allowed",
    "authority_expansion",
    "standalone_" + "diagnosis_authority",
    "standalone_" + "treatment_authorization",
    "medical_" + "act_authorization",
    "qi_denied_by_boundary",
    "east_asian_" + "medical_reasoning_denied",
    "biomedicine_privileged_by_wording",
]
TRUE_INVARIANTS = [
    "samvrti_to_physical_bridge_explicit",
    "string_brane_gauge_current_history_projection_required",
    "samvrti_qi_not_equal_physical_qi_by_assertion",
    "bridge_output_is_evidence_projection_only",
    "physical_classifier_remains_responsible_for_validated_type",
    "observe_only",
    "medical_modality_neutral",
    "professional_judgment_required",
    "patient_context_required",
]


def fail(message: str) -> int:
    print(f"[kustring-qi-bridge-release] FAIL: {message}", file=sys.stderr)
    return 1


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def check_required_files(manifest: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    for rel_path in manifest.get("required_files", []):
        if not (ROOT / rel_path).exists():
            errors.append(f"missing required file: {rel_path}")
    for rel_path in manifest.get("required_runner_inclusion", []):
        if not (ROOT / rel_path).exists():
            errors.append(f"missing required runner: {rel_path}")
    return errors


def check_manifest(manifest: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if manifest.get("manifest_id") != "kustring_qi_bridge_release_bundle_manifest_v0_1":
        errors.append("manifest_id mismatch")
    if manifest.get("update_policy") != "additive_only":
        errors.append("update_policy must be additive_only")
    if manifest.get("overwrite_policy") != "forbidden":
        errors.append("overwrite_policy must be forbidden")
    invariants = manifest.get("release_invariants", {})
    for key in TRUE_INVARIANTS:
        if invariants.get(key) is not True:
            errors.append(f"release_invariants.{key} must be true")
    for key in FALSE_INVARIANTS:
        if invariants.get(key) is not False:
            errors.append(f"release_invariants.{key} must be false")
    position = manifest.get("expected_chain_position", {})
    if position.get("after") != "samvrti-validator":
        errors.append("expected_chain_position.after must be samvrti-validator")
    if position.get("before") != "samvrti-to-physical-motion-builder":
        errors.append("expected_chain_position.before must be samvrti-to-physical-motion-builder")
    return errors


def check_packet(packet: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if packet.get("packet_id") != "kustring_qi_bridge_release_packet_v0_1":
        errors.append("packet_id mismatch")
    if packet.get("status") != "release_candidate":
        errors.append("release packet status must be release_candidate")
    claims = packet.get("release_claims", {})
    for key, value in claims.items():
        if value is not True:
            errors.append(f"release_claims.{key} must be true")
    authority = packet.get("authority_claims", {})
    for key, value in authority.items():
        if value is not False:
            errors.append(f"authority_claims.{key} must be false")
    return errors


def check_runner_inclusion() -> List[str]:
    text = RUNNER_PATH.read_text(encoding="utf-8")
    required = [
        "kustring-qi-bridge",
        "examples/kustring_qi_bridge_minimal.py",
        "kustring-qi-bridge-validator",
        "scripts/validate_kustring_qi_bridge_v0_1.py",
        "samvrti-to-physical-motion-builder",
    ]
    return [f"runner missing marker: {marker}" for marker in required if marker not in text]


def check_chain_order() -> List[str]:
    text = RUNNER_PATH.read_text(encoding="utf-8")
    ordered = [
        "samvrti-validator",
        "kustring-qi-bridge",
        "kustring-qi-bridge-validator",
        "samvrti-to-physical-motion-builder",
    ]
    positions = {marker: text.find(marker) for marker in ordered}
    errors = [f"runner missing ordered marker: {m}" for m, idx in positions.items() if idx < 0]
    if errors:
        return errors
    if not (positions["samvrti-validator"] < positions["kustring-qi-bridge"] < positions["kustring-qi-bridge-validator"] < positions["samvrti-to-physical-motion-builder"]):
        errors.append("runner order must be samvrti-validator -> kustring bridge -> bridge validator -> evidence builder")
    return errors


def main() -> int:
    if not MANIFEST_PATH.exists():
        return fail("missing release bundle manifest")
    if not PACKET_PATH.exists():
        return fail("missing release packet")

    manifest = load_json(MANIFEST_PATH)
    packet = load_json(PACKET_PATH)

    errors: List[str] = []
    errors.extend(check_required_files(manifest))
    errors.extend(check_manifest(manifest))
    errors.extend(check_packet(packet))
    errors.extend(check_runner_inclusion())
    errors.extend(check_chain_order())

    if errors:
        for err in errors:
            print(f"[kustring-qi-bridge-release] ERROR: {err}", file=sys.stderr)
        return 1

    result = subprocess.run([sys.executable, str(VALIDATOR_PATH)], cwd=str(ROOT), check=False)
    if result.returncode != 0:
        return fail("bridge validator failed")

    print("[kustring-qi-bridge-release] PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())