#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
POLICY = ROOT / "manifests" / "kuuos_validator_tiering_policy_v0_1.json"

REQUIRED_TIERS = [
    "T0_hot_path_guard",
    "T1_local_artifact_validator",
    "T2_changed_path_ci_validator",
    "T3_runtime_full_check",
    "T4_governance_full_check",
    "T5_release_freeze_finality_check",
]

FORBIDDEN_HOT_PATH_WORK = {
    "runtime_full_check",
    "all_governance_validation",
    "manifest_tree_scan",
    "network_io",
    "repository_wide_search",
    "recursive_validator_chain",
}

REQUIRED_GLOBAL_INVARIANTS = {
    "hot_path_must_not_run_full_validator",
    "full_check_must_not_be_required_per_tick",
    "governance_validation_must_not_be_required_per_tick",
    "release_finality_validation_must_not_be_required_per_tick",
    "runtime_receipts_remain_non_authoritative",
    "validators_may_block_admission_but_do_not_grant_execution_authority",
}

REQUIRED_QI_OUTPUTS = {
    "daemon_qi_process_tensor_tick_scheduler_v0_1.json",
    "daemon_qi_process_tensor_closed_loop_receipt_v0_1.json",
    "daemon_result_v0_1.json",
}


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def main() -> int:
    errors: list[str] = []
    if not POLICY.exists():
        print("ERROR: missing validator tiering policy")
        return 1

    data = json.loads(POLICY.read_text(encoding="utf-8"))
    if data.get("policy_version") != "kuuos_validator_tiering_policy_v0_1":
        errors.append("bad policy_version")
    if data.get("policy_status") != "active_non_authoritative_runtime_cost_boundary":
        errors.append("bad policy_status")

    tiers = _as_list(data.get("tiers"))
    tier_by_id = {tier.get("tier_id"): tier for tier in tiers if isinstance(tier, dict)}
    for tier_id in REQUIRED_TIERS:
        if tier_id not in tier_by_id:
            errors.append(f"missing tier: {tier_id}")

    hot = tier_by_id.get("T0_hot_path_guard", {})
    hot_forbidden = set(_as_list(hot.get("forbidden_work")))
    missing_hot_forbidden = FORBIDDEN_HOT_PATH_WORK - hot_forbidden
    for item in sorted(missing_hot_forbidden):
        errors.append(f"hot path does not forbid: {item}")
    if hot.get("cost_boundary") != "constant_or_artifact_local":
        errors.append("hot path must be constant_or_artifact_local")
    if hot.get("may_open_execution_authority") is not False:
        errors.append("hot path may_open_execution_authority must be false")

    for tier_id, tier in tier_by_id.items():
        if tier.get("may_open_execution_authority") is not False:
            errors.append(f"tier may open execution authority: {tier_id}")

    invariants = set(_as_list(data.get("global_invariants")))
    for item in sorted(REQUIRED_GLOBAL_INVARIANTS - invariants):
        errors.append(f"missing invariant: {item}")

    mapping = data.get("qi_process_tensor_runtime_mapping")
    if not isinstance(mapping, dict):
        errors.append("missing qi_process_tensor_runtime_mapping")
        mapping = {}
    for output in REQUIRED_QI_OUTPUTS:
        entry = mapping.get(output)
        if not isinstance(entry, dict):
            errors.append(f"missing qi mapping: {output}")
            continue
        if entry.get("runtime_emit_tier") != "T0_hot_path_guard":
            errors.append(f"bad runtime_emit_tier for {output}")
        if entry.get("ci_coverage_tier") not in {"T3_runtime_full_check", "T4_governance_full_check"}:
            errors.append(f"bad ci_coverage_tier for {output}")

    for flag in data.get("authority_flags_must_remain_false", []):
        if not isinstance(flag, str) or not flag.startswith("grants_"):
            errors.append(f"bad authority flag: {flag}")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: KuuOS validator tiering policy v0.1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
