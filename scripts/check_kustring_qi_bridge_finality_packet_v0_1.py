#!/usr/bin/env python3
"""Check KuString Qi Bridge finality packet v0.1."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
FINALITY_PATH = ROOT / "specs" / "kustring_qi_bridge_finality_packet_v0_1.json"
RELEASE_VALIDATOR_PATH = ROOT / "scripts" / "validate_kustring_qi_bridge_release_bundle_v0_1.py"
RUNNER_PATH = ROOT / "scripts" / "run_qi_motion_chain_checks_v0_1.py"

TRUE_CLAIMS = [
    "release_bundle_validator_present",
    "release_bundle_validator_pass_required",
    "bridge_validator_pass_required",
    "runner_finality_check_required",
    "append_only_lineage_preserved",
    "same_root_required",
    "samvrti_to_physical_bridge_explicit",
    "string_brane_gauge_current_history_projection_required",
    "samvrti_qi_not_collapsed_into_physical_qi",
    "physical_classifier_remains_type_authority",
    "bridge_output_is_evidence_projection_only",
    "neutral_medical_modality_boundary_preserved",
]

REQUIRED_REFERENCES = [
    "specs/kustring_qi_bridge_release_packet_v0_1.json",
    "specs/kustring_qi_bridge_release_bundle_manifest_v0_1.json",
    "specs/kustring_qi_bridge_contract_v0_1.json",
    "validation_cases/kustring_qi_bridge_cases_v0_1.json",
    "examples/kustring_qi_bridge_minimal.py",
    "scripts/validate_kustring_qi_bridge_v0_1.py",
    "scripts/validate_kustring_qi_bridge_release_bundle_v0_1.py",
    "scripts/run_qi_motion_chain_checks_v0_1.py",
]


def fail(message: str) -> int:
    print(f"[kustring-qi-bridge-finality] FAIL: {message}", file=sys.stderr)
    return 1


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def check_packet(packet: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if packet.get("packet_id") != "kustring_qi_bridge_finality_packet_v0_1":
        errors.append("packet_id mismatch")
    if packet.get("status") != "finality_candidate":
        errors.append("status must be finality_candidate")
    claims = packet.get("finality_claims", {})
    for key in TRUE_CLAIMS:
        if claims.get(key) is not True:
            errors.append(f"finality_claims.{key} must be true")
    forbidden = packet.get("forbidden_claims", {})
    if not forbidden:
        errors.append("forbidden_claims must be nonempty")
    for key, value in forbidden.items():
        if value is not False:
            errors.append(f"forbidden_claims.{key} must be false")
    if "release_bundle_validator_passes" not in packet.get("finality_rule", ""):
        errors.append("finality_rule must require release_bundle_validator_passes")
    return errors


def check_references(packet: Dict[str, Any]) -> List[str]:
    text = json.dumps(packet, sort_keys=True)
    errors: List[str] = []
    for rel_path in REQUIRED_REFERENCES:
        if rel_path not in text:
            errors.append(f"finality packet missing reference: {rel_path}")
        if not (ROOT / rel_path).exists():
            errors.append(f"referenced file missing: {rel_path}")
    return errors


def check_runner_mentions_finality() -> List[str]:
    text = RUNNER_PATH.read_text(encoding="utf-8")
    required = [
        "kustring-qi-bridge-finality",
        "scripts/check_kustring_qi_bridge_finality_packet_v0_1.py",
    ]
    return [f"runner missing finality marker: {m}" for m in required if m not in text]


def main() -> int:
    if not FINALITY_PATH.exists():
        return fail("missing finality packet")
    packet = load_json(FINALITY_PATH)

    errors: List[str] = []
    errors.extend(check_packet(packet))
    errors.extend(check_references(packet))
    errors.extend(check_runner_mentions_finality())

    if errors:
        for err in errors:
            print(f"[kustring-qi-bridge-finality] ERROR: {err}", file=sys.stderr)
        return 1

    result = subprocess.run([sys.executable, str(RELEASE_VALIDATOR_PATH)], cwd=str(ROOT), check=False)
    if result.returncode != 0:
        return fail("release bundle validator failed")

    print("[kustring-qi-bridge-finality] PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())