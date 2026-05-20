#!/usr/bin/env python3
"""Check KuString Qi Bridge chain index and baseline packet v0.1."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
CHAIN_INDEX_PATH = ROOT / "specs" / "kustring_qi_bridge_chain_index_v0_1.json"
BASELINE_PATH = ROOT / "specs" / "kustring_qi_bridge_baseline_packet_v0_1.json"
FINALITY_CHECKER_PATH = ROOT / "scripts" / "check_kustring_qi_bridge_finality_packet_v0_1.py"
RUNNER_PATH = ROOT / "scripts" / "run_qi_motion_chain_checks_v0_1.py"

TRUE_INVARIANTS = [
    "samvrti_to_physical_bridge_explicit",
    "kustring_projection_required",
    "string_brane_gauge_current_history_projection_required",
    "samvrti_qi_not_collapsed_into_physical_qi",
    "physical_classifier_remains_type_authority",
    "bridge_output_is_evidence_projection_only",
    "observe_only",
    "medical_modality_neutral",
    "professional_judgment_required",
    "patient_context_required",
]

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

TRUE_BASELINE_CLAIMS = [
    "chain_index_present",
    "all_chain_files_present",
    "finality_checker_present",
    "finality_checker_pass_required",
    "release_bundle_validator_pass_required",
    "runner_chain_position_checked",
    "append_only_lineage_preserved",
    "same_root_required",
    "samvrti_to_physical_bridge_explicit",
    "kustring_projection_required",
    "samvrti_qi_not_collapsed_into_physical_qi",
    "physical_classifier_remains_type_authority",
    "bridge_output_is_evidence_projection_only",
    "medical_modality_neutral_boundary_preserved",
]


def fail(message: str) -> int:
    print(f"[kustring-qi-bridge-chain] FAIL: {message}", file=sys.stderr)
    return 1


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def check_chain_index(chain: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if chain.get("chain_index_id") != "kustring_qi_bridge_chain_index_v0_1":
        errors.append("chain_index_id mismatch")
    if chain.get("update_policy") != "additive_only":
        errors.append("update_policy must be additive_only")
    if chain.get("overwrite_policy") != "forbidden":
        errors.append("overwrite_policy must be forbidden")
    if chain.get("same_root_required") is not True:
        errors.append("same_root_required must be true")

    entries = chain.get("chain_order", [])
    if len(entries) < 10:
        errors.append("chain_order must include at least 10 entries")
    for idx, entry in enumerate(entries):
        rel_path = entry.get("path")
        if not rel_path:
            errors.append(f"chain_order[{idx}].path missing")
            continue
        if not (ROOT / rel_path).exists():
            errors.append(f"chain_order[{idx}] missing file: {rel_path}")

    invariants = chain.get("baseline_invariants", {})
    for key in TRUE_INVARIANTS:
        if invariants.get(key) is not True:
            errors.append(f"baseline_invariants.{key} must be true")
    for key in FALSE_INVARIANTS:
        if invariants.get(key) is not False:
            errors.append(f"baseline_invariants.{key} must be false")
    return errors


def check_baseline_packet(packet: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if packet.get("packet_id") != "kustring_qi_bridge_baseline_packet_v0_1":
        errors.append("baseline packet_id mismatch")
    if packet.get("status") != "baseline_established_candidate":
        errors.append("baseline status must be baseline_established_candidate")
    claims = packet.get("baseline_claims", {})
    for key in TRUE_BASELINE_CLAIMS:
        if claims.get(key) is not True:
            errors.append(f"baseline_claims.{key} must be true")
    forbidden = packet.get("forbidden_baseline_claims", {})
    if not forbidden:
        errors.append("forbidden_baseline_claims must be nonempty")
    for key, value in forbidden.items():
        if value is not False:
            errors.append(f"forbidden_baseline_claims.{key} must be false")
    if "chain_index_valid" not in packet.get("baseline_rule", ""):
        errors.append("baseline_rule must require chain_index_valid")
    return errors


def check_runner_mentions_chain() -> List[str]:
    text = RUNNER_PATH.read_text(encoding="utf-8")
    required = [
        "kustring-qi-bridge-chain-index",
        "scripts/check_kustring_qi_bridge_chain_index_v0_1.py",
    ]
    return [f"runner missing chain marker: {m}" for m in required if m not in text]


def main() -> int:
    if not CHAIN_INDEX_PATH.exists():
        return fail("missing chain index")
    if not BASELINE_PATH.exists():
        return fail("missing baseline packet")

    chain = load_json(CHAIN_INDEX_PATH)
    baseline = load_json(BASELINE_PATH)

    errors: List[str] = []
    errors.extend(check_chain_index(chain))
    errors.extend(check_baseline_packet(baseline))
    errors.extend(check_runner_mentions_chain())

    if errors:
        for err in errors:
            print(f"[kustring-qi-bridge-chain] ERROR: {err}", file=sys.stderr)
        return 1

    result = subprocess.run([sys.executable, str(FINALITY_CHECKER_PATH)], cwd=str(ROOT), check=False)
    if result.returncode != 0:
        return fail("finality checker failed")

    print("[kustring-qi-bridge-chain] PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())