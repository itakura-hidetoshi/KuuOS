#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
PACKET = ROOT / "manifests" / "cbf_membrane_gap_kernel_established_packet_v1_0.json"

REQUIRED_FILES = [
    "manifests/cbf_membrane_gap_kernel_contract_v1_0.json",
    "docs/CBF_MEMBRANE_GAP_KERNEL_v1_0.md",
    "scripts/validate_cbf_membrane_gap_kernel_contract_v1_0.py",
    "scripts/check_cbf_membrane_gap_validation_cases_v1_0.py",
    "tests/test_cbf_membrane_gap_kernel_contract_v1_0.py",
    "tests/test_cbf_membrane_gap_validation_cases_v1_0.py",
    "manifests/cbf_membrane_gap_kernel_validation_cases_v1_0.json",
    ".github/workflows/kuuos_runtime_full_check.yml",
    "formal/KUOS/CBFMembrane/Defs.lean",
    "formal/KUOS/CBFMembrane/Soundness.lean",
]

REQUIRED_CORE_INVARIANTS = {
    "membrane_license_only",
    "hard_and_grave_margins_cannot_be_offset",
    "belief_pass_is_not_true_state_proof",
    "local_pass_is_not_global_pass",
    "cptp_pass_is_not_membrane_pass",
    "expectation_pass_is_not_strong_spectral_pass",
    "negative_spectral_mass_blocks_strong_pass",
    "domain_unclear_blocks_strong_pass",
}

REQUIRED_UPDATE_FLAGS = {
    "additive_only",
    "tighten_only_default",
    "same_root_required",
    "overwrite_forbidden",
}


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _path_exists(repo_path: str) -> bool:
    return (ROOT / repo_path).exists()


def main() -> int:
    errors: list[str] = []
    if not PACKET.exists():
        print("ERROR: missing CBF established packet")
        return 1

    data = json.loads(PACKET.read_text(encoding="utf-8"))

    if data.get("packet_version") != "cbf_membrane_gap_kernel_established_packet_v1_0":
        errors.append("bad packet_version")
    if data.get("packet_status") != "established_baseline":
        errors.append("bad packet_status")

    scalar_paths = [
        data.get("root_contract"),
        data.get("documentation"),
        data.get("validator"),
        data.get("validation_case_checker"),
        data.get("validation_cases"),
        data.get("workflow"),
    ]
    list_paths = []
    list_paths.extend(_as_list(data.get("tests")))
    list_paths.extend(_as_list(data.get("lean_surface")))
    list_paths.extend(_as_list(data.get("registered_in")))

    packet_paths = {p for p in scalar_paths + list_paths if isinstance(p, str)}
    for path in REQUIRED_FILES:
        if path not in packet_paths:
            errors.append(f"packet does not register required file: {path}")
        elif not _path_exists(path):
            errors.append(f"registered file missing on disk: {path}")

    registered_in = set(_as_list(data.get("registered_in")))
    for path in [
        "manifests/kuuos_runtime_manifest_v0_1.json",
        "manifests/kuuos_validator_tiering_policy_v0_1.json",
        "scripts/run_kuuos_runtime_full_check_v0_1.py",
    ]:
        if path not in registered_in:
            errors.append(f"missing registration target: {path}")

    invariants = set(_as_list(data.get("core_invariants")))
    for invariant in sorted(REQUIRED_CORE_INVARIANTS - invariants):
        errors.append(f"missing core invariant: {invariant}")

    statement = data.get("baseline_statement", "")
    if "CBF pass is not truth" not in statement:
        errors.append("baseline statement must preserve non-truth pass")
    if "not execution" not in statement:
        errors.append("baseline statement must preserve non-execution pass")
    if "not falsity" not in statement:
        errors.append("baseline statement must preserve fail-not-falsity")

    runtime = data.get("runtime_binding")
    if not isinstance(runtime, dict):
        errors.append("missing runtime_binding")
        runtime = {}
    if runtime.get("hot_path") != "bounded_local_receipt_only":
        errors.append("runtime hot_path must be bounded_local_receipt_only")
    if runtime.get("runtime_authority_expansion") is not False:
        errors.append("runtime_authority_expansion must be false")

    update_policy = data.get("update_policy")
    if not isinstance(update_policy, dict):
        errors.append("missing update_policy")
        update_policy = {}
    for key in REQUIRED_UPDATE_FLAGS:
        if update_policy.get(key) is not True:
            errors.append(f"update_policy must set {key}=true")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1

    print("PASS: CBF membrane gap established packet v1.0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
