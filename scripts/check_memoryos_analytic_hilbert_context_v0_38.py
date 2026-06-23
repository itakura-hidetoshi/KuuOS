#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from runtime.kuuos_memoryos_analytic_hilbert_context_v0_38 import (
    ANALYTIC_PACKET_VERSION,
    ANALYTIC_SURFACES,
    BOUNDARY,
    CAPSULE_ROUTES,
    CAPSULE_VERSION,
    NON_AUTHORITY,
    RETRIEVAL_ROUTES,
    RETRIEVAL_VERSION,
    VERSION,
    WORLD_BRIDGE_ID,
)

ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    require(
        VERSION == "kuuos_memoryos_analytic_hilbert_context_v0_38",
        "version mismatch",
    )
    require(
        ANALYTIC_PACKET_VERSION
        == "world_kuu_vacuum_os_hilbert_analytic_packet_v0_49",
        "analytic packet version mismatch",
    )
    require(
        CAPSULE_VERSION == "memoryos_analytic_hilbert_context_capsule_v0_38",
        "capsule version mismatch",
    )
    require(
        RETRIEVAL_VERSION == "memoryos_analytic_hilbert_context_retrieval_v0_38",
        "retrieval version mismatch",
    )
    require(
        WORLD_BRIDGE_ID == "KUOS.WORLD.KuuVacuumOSHilbertCompletionBridgeV0_49",
        "WORLD bridge id mismatch",
    )
    require(
        ANALYTIC_SURFACES
        == (
            "os_reflection_form",
            "os_hilbert_vacuum",
            "vacuum_state",
            "gauge_invariance",
            "modular_time",
            "physical_time",
            "hamiltonian_vacuum",
        ),
        "analytic surfaces mismatch",
    )
    for route in (
        "QUARANTINE_MEMORY_SOURCE",
        "REOBSERVE_ANALYTIC_EVIDENCE",
        "PRESERVE_RESIDUE_WITH_ANALYTIC_CONTEXT",
        "READY_FOR_READ_ONLY_ANALYTIC_RETRIEVAL",
    ):
        require(route in CAPSULE_ROUTES, f"capsule route missing: {route}")
    for route in (
        "QUARANTINE_ANALYTIC_RETRIEVAL",
        "RETURN_ANALYTIC_CONTEXT_WITH_ACTIVE_SHIELD",
        "REOBSERVE_ANALYTIC_EVIDENCE",
        "RETURN_ANALYTIC_CONTEXT_WITH_RESIDUE",
        "RETURN_READ_ONLY_HILBERT_CONTEXT",
    ):
        require(route in RETRIEVAL_ROUTES, f"retrieval route missing: {route}")
    for field, value in NON_AUTHORITY.items():
        require(value is False, f"authority boundary lost: {field}")
    for field, value in BOUNDARY.items():
        require(value is True, f"boundary lost: {field}")

    manifest_path = ROOT / "manifests/kuuos_memoryos_analytic_hilbert_context_v0_38.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest["version"] == VERSION, "manifest version mismatch")
    require(
        manifest["memory_predecessor"]
        == "kuuos_memoryos_predictive_shielded_memory_v0_37",
        "memory predecessor mismatch",
    )
    require(
        manifest["world_predecessor"] == WORLD_BRIDGE_ID,
        "WORLD predecessor mismatch",
    )
    for key in (
        "runtime_kernel",
        "unit_test",
        "validation_script",
        "documentation",
        "formal_module",
        "formal_root",
        "workflow",
        "central_runtime_check",
        "source_runtime",
        "source_world_formal",
    ):
        relative = manifest[key]
        require((ROOT / relative).is_file(), f"manifest file missing: {relative}")
    require(
        set(manifest["analytic_surfaces"]) == set(ANALYTIC_SURFACES),
        "manifest analytic surfaces mismatch",
    )
    require(
        set(manifest["capsule_routes"]) == CAPSULE_ROUTES,
        "manifest capsule routes mismatch",
    )
    require(
        set(manifest["retrieval_routes"]) == RETRIEVAL_ROUTES,
        "manifest retrieval routes mismatch",
    )
    false_boundaries = (
        "runtime_constructs_os_completion",
        "vacuum_state_is_truth_authority",
        "analytic_vacuum_is_unique_vacuum_claim",
        "analytic_vacuum_is_metaphysical_kuu",
        "analytic_vacuum_is_exact_world",
        "modular_time_is_physical_time",
        "runtime_executes_physical_time",
        "runtime_executes_hamiltonian",
        "memory_overwrite_allowed",
        "world_update_allowed",
        "retrieval_grants_plan_activation",
        "retrieval_grants_actos_invocation",
        "retrieval_grants_truth",
    )
    for field in false_boundaries:
        require(
            manifest["boundaries"][field] is False,
            f"manifest boundary promoted: {field}",
        )

    runtime = (
        ROOT / "runtime/kuuos_memoryos_analytic_hilbert_context_v0_38.py"
    ).read_text(encoding="utf-8")
    for phrase in (
        "world_kuu_vacuum_os_hilbert_analytic_packet_v0_49",
        "analytic_source_world_fragment_mismatch",
        "analytic_packet_{field}_forbidden",
        "REOBSERVE_ANALYTIC_EVIDENCE",
        "RETURN_ANALYTIC_CONTEXT_WITH_ACTIVE_SHIELD",
        "RETURN_READ_ONLY_HILBERT_CONTEXT",
        "modular_time_distinct_from_physical_time",
        "physical_time_execution_performed",
        "hamiltonian_execution_performed",
    ):
        require(phrase in runtime, f"runtime boundary missing: {phrase}")

    tests = (
        ROOT / "tests/test_memoryos_analytic_hilbert_context_v0_38.py"
    ).read_text(encoding="utf-8")
    for phrase in (
        "test_complete_packet_builds_read_only_analytic_capsule",
        "test_incomplete_analytic_evidence_routes_to_reobserve",
        "test_truth_and_unique_vacuum_promotion_are_rejected",
        "test_runtime_os_completion_and_time_execution_are_rejected",
        "test_same_sequence_source_substitution_is_rejected",
        "test_blocked_capability_returns_active_shield_context",
        "test_capsule_tampering_is_detected",
    ):
        require(phrase in tests, f"regression test missing: {phrase}")

    documentation = (
        ROOT / "docs/KUUOS_MEMORYOS_ANALYTIC_HILBERT_CONTEXT_v0_38.md"
    ).read_text(encoding="utf-8")
    for phrase in (
        "本層は OS Hilbert completion を構成しない",
        "解析的真空を唯一真空、正確な WORLD、形而上学的な空と同一視しない",
        "モジュラー時間と物理時間は別々の digest として保持する",
        "MemoryOS は blocker を discharge しない",
        "analytic vacuum ≠ metaphysical Kū",
        "CI success ≠ truth",
    ):
        require(phrase in documentation, f"documentation boundary missing: {phrase}")

    source_memory = (
        ROOT / "runtime/kuuos_memoryos_predictive_shielded_memory_v0_37.py"
    ).read_text(encoding="utf-8")
    for phrase in (
        "contradiction_residue_preserved",
        "blocker_shield_precedes_capability_return",
        "world_imagination_candidate_not_truth",
        "append_only_capsule_lineage",
    ):
        require(phrase in source_memory, f"v0.37 boundary missing: {phrase}")

    source_world = (
        ROOT / "formal/KUOS/WORLD/KuuVacuumOSHilbertCompletionBridgeV0_49.lean"
    ).read_text(encoding="utf-8")
    for phrase in (
        "noRuntimeOSCompletionConstruction",
        "noRuntimeHamiltonianExecution",
        "noRuntimePhysicalTimeExecution",
        "noRuntimeUniqueVacuumDeclaration",
        "modularTimeNotPhysicalTime",
        "vacuumStateNotTruthAuthority",
        "vacuumDoesNotCollapseWorlds",
        "nonMarkovianHistoryPreserved",
        "twoTruthsGapPreserved",
    ):
        require(phrase in source_world, f"v0.49 boundary missing: {phrase}")

    formal = (
        ROOT / "formal/KUOS/OpenHorizon/MemoryOSAnalyticHilbertContextKernelV0_38.lean"
    ).read_text(encoding="utf-8")
    for phrase in (
        "analytic_context_cannot_promote_vacuum_or_world",
        "memoryos_analytic_hilbert_context_boundary",
        "analytic.noRuntimeOSCompletionConstruction",
        "analytic.modularTimeNotPhysicalTimeProof",
        "analytic.vacuumStateNotTruthAuthorityProof",
    ):
        require(phrase in formal, f"formal boundary missing: {phrase}")

    formal_root = (ROOT / "formal/KUOS.lean").read_text(encoding="utf-8")
    require(
        "import KUOS.OpenHorizon.MemoryOSAnalyticHilbertContextKernelV0_38"
        in formal_root,
        "formal root import missing",
    )
    central = (ROOT / "scripts/run_kuuos_runtime_full_check_v0_48.py").read_text(
        encoding="utf-8"
    )
    require("check_memoryos_v038" in central, "central runtime registration missing")

    print("MemoryOS analytic Hilbert context v0.38 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
