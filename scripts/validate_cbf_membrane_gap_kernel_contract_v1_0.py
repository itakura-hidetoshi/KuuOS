#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "manifests" / "cbf_membrane_gap_kernel_contract_v1_0.json"

REQUIRED_INVARIANTS = {
    "cbf_pass_is_not_truth_pass",
    "cbf_pass_is_not_execute",
    "cbf_fail_is_not_falsity",
    "cbf_license_is_membrane_license_only",
    "hard_and_grave_membranes_cannot_be_offset_by_score_average_usefulness_or_soft_slack",
    "negative_margin_cannot_be_averaged_away",
    "negative_spectral_mass_cannot_be_masked_by_positive_expectation",
    "belief_pass_is_not_true_state_proof",
    "missing_barrier_evidence_is_not_pass_evidence",
    "safe_is_not_equivalent_to_recoverable",
    "local_pass_is_not_global_pass",
    "cptp_pass_is_not_membrane_pass",
    "expectation_pass_is_not_strong_spectral_pass",
    "domain_unclear_blocks_strong_pass",
}

REQUIRED_RELEASE_STRENGTHS = {
    "NO_LICENSE",
    "LOCAL_MEMBRANE_LICENSE",
    "BELIEF_MEMBRANE_LICENSE",
    "PROJECTED_MEMBRANE_LICENSE",
    "GLOBAL_GLUED_MEMBRANE_LICENSE",
    "ROBUST_SPECTRAL_MEMBRANE_LICENSE",
}

REQUIRED_DECISIONS = {
    "PASS_NOMINAL",
    "PASS_PROJECTED",
    "PASS_WITH_RESIDUE",
    "PASS_BUT_THIN",
    "PASS_WITH_UNCERTAINTY",
    "LOCAL_PASS_GLOBAL_HOLD",
    "REOBSERVE_REQUIRED",
    "REDECOMPOSE_REQUIRED",
    "RECOVERY_MODE_REQUIRED",
    "HOLD_MEMBRANE_THIN",
    "HOLD_DOMAIN_UNCLEAR",
    "BLOCK_MEMBRANE_BREACH",
    "BLOCK_NEGATIVE_SPECTRAL_MASS",
    "BLOCK_AUTHORITY_BOUNDARY",
    "HANDOVER_REQUIRED",
}

REQUIRED_RECEIPT_SECTIONS = {
    "state_carrier",
    "action_candidate",
    "membrane_stack",
    "gap_bundle",
    "uncertainty",
    "projection",
    "gluing",
    "spectral",
    "learning_calibration",
    "release_strength",
    "decision",
    "reason_codes",
    "authority",
    "same_root",
    "append_only",
}

FORBIDDEN_AUTHORITY_TRUE = {
    "cbf_truth_authority",
    "cbf_execute_authority",
    "cbf_final_commitment_authority",
    "cbf_memory_overwrite_authority",
    "cbf_theorem_authority",
    "cbf_clinical_authority",
}


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _as_set(value: Any) -> set[str]:
    return {item for item in _as_list(value) if isinstance(item, str)}


def main() -> int:
    errors: list[str] = []

    if not CONTRACT.exists():
        print("ERROR: missing CBF membrane gap kernel contract")
        return 1

    data = json.loads(CONTRACT.read_text(encoding="utf-8"))

    if data.get("contract_version") != "cbf_membrane_gap_kernel_contract_v1_0":
        errors.append("bad contract_version")
    if data.get("contract_status") != "active_non_authoritative_membrane_license_kernel":
        errors.append("bad contract_status")

    boundary = data.get("authority_boundary")
    if not isinstance(boundary, dict):
        errors.append("missing authority_boundary")
        boundary = {}

    for key in sorted(FORBIDDEN_AUTHORITY_TRUE):
        if boundary.get(key) is not False:
            errors.append(f"authority boundary must be false: {key}")
    if boundary.get("membrane_license_only") is not True:
        errors.append("membrane_license_only must be true")

    invariants = _as_set(data.get("fixed_invariants"))
    for item in sorted(REQUIRED_INVARIANTS - invariants):
        errors.append(f"missing invariant: {item}")

    tiers = data.get("membrane_tiers")
    if not isinstance(tiers, list):
        errors.append("membrane_tiers must be a list")
        tiers = []
    tier_by_name = {tier.get("tier"): tier for tier in tiers if isinstance(tier, dict)}
    for tier_name in ["grave", "hard", "soft"]:
        if tier_name not in tier_by_name:
            errors.append(f"missing membrane tier: {tier_name}")

    for tier_name in ["grave", "hard"]:
        tier = tier_by_name.get(tier_name, {})
        if tier.get("slack_allowed") is not False:
            errors.append(f"{tier_name} slack_allowed must be false")
        if tier.get("average_offset_allowed") is not False:
            errors.append(f"{tier_name} average_offset_allowed must be false")
        if tier.get("score_offset_allowed") is not False:
            errors.append(f"{tier_name} score_offset_allowed must be false")

    soft = tier_by_name.get("soft", {})
    if soft and soft.get("slack_allowed") is not True:
        errors.append("soft slack_allowed must be true")
    if soft and soft.get("residue_required") is not True:
        errors.append("soft residue_required must be true")

    release_strengths = _as_set(data.get("release_strengths"))
    for item in sorted(REQUIRED_RELEASE_STRENGTHS - release_strengths):
        errors.append(f"missing release strength: {item}")

    decisions = _as_set(data.get("decision_enum"))
    for item in sorted(REQUIRED_DECISIONS - decisions):
        errors.append(f"missing decision: {item}")

    sections = _as_set(data.get("required_receipt_sections"))
    for item in sorted(REQUIRED_RECEIPT_SECTIONS - sections):
        errors.append(f"missing receipt section: {item}")

    forbidden_claims = _as_set(data.get("forbidden_receipt_claims"))
    for claim in [
        "grants_execution_authority",
        "grants_truth_authority",
        "proves_global_safety_from_local_pass_only",
        "proves_strong_spectral_safety_from_expectation_only",
    ]:
        if claim not in forbidden_claims:
            errors.append(f"missing forbidden receipt claim: {claim}")

    tiering = data.get("runtime_tiering")
    if not isinstance(tiering, dict):
        errors.append("missing runtime_tiering")
        tiering = {}
    if tiering.get("runtime_emit_tier") != "T0_hot_path_guard":
        errors.append("CBF runtime emit tier must be T0_hot_path_guard")
    if tiering.get("may_open_execution_authority") is not False:
        errors.append("CBF may_open_execution_authority must be false")

    update_policy = data.get("update_policy")
    if not isinstance(update_policy, dict):
        errors.append("missing update_policy")
        update_policy = {}
    for key in ["additive_only", "tighten_only_default", "same_root_required", "overwrite_forbidden"]:
        if update_policy.get(key) is not True:
            errors.append(f"update_policy must set {key}=true")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1

    print("PASS: CBF membrane gap kernel contract v1.0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
