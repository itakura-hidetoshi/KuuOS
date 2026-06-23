#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from runtime.kuuos_memoryos_predictive_shielded_memory_v0_37 import (
    BOUNDARY,
    CAPSULE_ROUTES,
    CAPSULE_VERSION,
    MEMORY_TYPES,
    NON_AUTHORITY,
    RETRIEVAL_ROUTES,
    RETRIEVAL_VERSION,
    VERSION,
)

ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    require(
        VERSION == "kuuos_memoryos_predictive_shielded_memory_v0_37",
        "version mismatch",
    )
    require(
        CAPSULE_VERSION == "memoryos_predictive_shielded_capsule_v0_37",
        "capsule version mismatch",
    )
    require(
        RETRIEVAL_VERSION == "memoryos_predictive_shielded_retrieval_v0_37",
        "retrieval version mismatch",
    )
    require(
        MEMORY_TYPES == ("working", "episodic", "semantic", "procedural"),
        "memory hierarchy mismatch",
    )
    for route in (
        "QUARANTINE_SOURCE_BLOCKER_EVIDENCE",
        "REOBSERVE_PREDICTIVE_STATE",
        "REVIEW_CONTRADICTION_RESIDUE",
        "PRESERVE_RESIDUE_WITH_CONTEXT",
        "READY_FOR_SHIELDED_RETRIEVAL",
    ):
        require(route in CAPSULE_ROUTES, f"capsule route missing: {route}")
    for route in (
        "QUARANTINE_RETRIEVAL",
        "RETURN_CONTEXT_WITH_ACTIVE_SHIELD",
        "REOBSERVE_BEFORE_RETRIEVAL",
        "REVIEW_BEFORE_RETRIEVAL",
        "RETURN_CONTEXT_WITH_RESIDUE",
        "RETURN_PREDICTIVE_CONTEXT_CANDIDATE",
    ):
        require(route in RETRIEVAL_ROUTES, f"retrieval route missing: {route}")

    for field, value in NON_AUTHORITY.items():
        require(value is False, f"authority boundary lost: {field}")
    for field in (
        "memory_hierarchy_separated",
        "episodic_source_immutable",
        "semantic_consolidation_candidate_only",
        "procedural_memory_not_execution",
        "observable_predictive_state_candidate_only",
        "contradiction_residue_preserved",
        "blocker_shield_precedes_capability_return",
        "safe_read_only_fallback_available",
        "world_imagination_candidate_not_truth",
        "world_imagination_cannot_commit",
        "append_only_capsule_lineage",
        "source_v035_boundary_preserved",
    ):
        require(BOUNDARY[field] is True, f"boundary lost: {field}")

    manifest_path = (
        ROOT / "manifests/kuuos_memoryos_predictive_shielded_memory_v0_37.json"
    )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest["version"] == VERSION, "manifest version mismatch")
    require(
        manifest["predecessor"]
        == "kuuos_memoryos_qi_world_blocker_integration_v0_35",
        "predecessor mismatch",
    )
    for key in (
        "runtime_kernel",
        "unit_test",
        "validation_script",
        "documentation",
        "research_basis",
        "formal_module",
        "formal_root",
        "workflow",
        "central_runtime_check",
    ):
        relative = manifest[key]
        require((ROOT / relative).is_file(), f"manifest file missing: {relative}")
    source_ids = {item["id"] for item in manifest["research_sources"]}
    for source_id in (
        "arXiv:1512.00589",
        "arXiv:1906.10437",
        "arXiv:2207.05738",
        "arXiv:2309.02427",
        "arXiv:2310.08560",
        "arXiv:2505.22101",
        "arXiv:1708.08611",
        "arXiv:2102.12981",
        "arXiv:2301.04104",
    ):
        require(source_id in source_ids, f"research source missing: {source_id}")
    boundaries = manifest["boundaries"]
    for field in (
        "automatic_consolidation_performed",
        "semantic_candidate_is_truth",
        "procedural_candidate_grants_execution",
        "predictive_state_is_latent_truth",
        "memory_can_discharge_blocker",
        "safe_fallback_is_task_success",
        "world_imagination_is_sourced_world",
        "world_imagination_can_commit",
        "memory_overwrite_allowed",
        "retrieval_grants_plan_activation",
        "retrieval_grants_actos_invocation",
        "retrieval_grants_truth",
    ):
        require(boundaries[field] is False, f"manifest authority promoted: {field}")

    runtime = (
        ROOT / "runtime/kuuos_memoryos_predictive_shielded_memory_v0_37.py"
    ).read_text(encoding="utf-8")
    for phrase in (
        "OBSERVABLE_PREDICTIVE_STATE_CANDIDATE",
        "SEMANTIC_CONSOLIDATION_CANDIDATE",
        "PROCEDURAL_REUSE_CANDIDATE",
        "memory_records_append_only_violation",
        "RETURN_CONTEXT_WITH_ACTIVE_SHIELD",
        "READ_ONLY_CONTEXT_OR_REOBSERVE",
        "world_candidate_replaces_sourced_world_forbidden",
    ):
        require(phrase in runtime, f"runtime boundary missing: {phrase}")

    tests = (
        ROOT / "tests/test_memoryos_predictive_shielded_memory_v0_37.py"
    ).read_text(encoding="utf-8")
    for phrase in (
        "test_memory_hierarchy_is_separated_without_authority_promotion",
        "test_semantic_truth_promotion_is_rejected",
        "test_procedural_execution_promotion_is_rejected",
        "test_append_only_record_removal_is_rejected",
        "test_blocked_capability_returns_active_shield_context",
        "test_capsule_tampering_is_detected",
    ):
        require(phrase in tests, f"regression test missing: {phrase}")

    documentation = (
        ROOT / "docs/KUUOS_MEMORYOS_PREDICTIVE_SHIELDED_MEMORY_v0_37.md"
    ).read_text(encoding="utf-8")
    for phrase in (
        "Semantic record は fact ではない",
        "Procedural record は execution authority ではない",
        "WORLD imagination は sourced WORLD を更新しない",
        "READ_ONLY_CONTEXT_OR_REOBSERVE",
        "retrieval != ActOS invocation",
    ):
        require(phrase in documentation, f"documentation boundary missing: {phrase}")

    research = (
        ROOT / "docs/research/MEMORYOS_QI_BLOCKER_AI_THEORY_RESEARCH_v0_37.md"
    ).read_text(encoding="utf-8")
    for phrase in (
        "Cognitive Architectures for Language Agents",
        "Safe Reinforcement Learning via Shielding",
        "The Black-Box Simplex Architecture",
        "Mastering Diverse Domains through World Models",
        "predictive state candidate != hidden-state truth",
    ):
        require(phrase in research, f"research mapping missing: {phrase}")

    formal = (
        ROOT
        / "formal/KUOS/OpenHorizon/MemoryOSPredictiveShieldedMemoryKernelV0_37.lean"
    ).read_text(encoding="utf-8")
    require(
        "memoryos_predictive_shielded_memory_boundary" in formal,
        "formal boundary theorem missing",
    )
    require(
        "consolidation_cannot_promote_truth_or_execution" in formal,
        "formal consolidation theorem missing",
    )

    formal_root = (ROOT / "formal/KUOS.lean").read_text(encoding="utf-8")
    require(
        "import KUOS.OpenHorizon.MemoryOSPredictiveShieldedMemoryKernelV0_37"
        in formal_root,
        "formal root import missing",
    )
    central = (ROOT / "scripts/run_kuuos_runtime_full_check_v0_48.py").read_text(
        encoding="utf-8"
    )
    require("check_memoryos_v037" in central, "central runtime registration missing")

    print("MemoryOS predictive shielded memory v0.37 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
