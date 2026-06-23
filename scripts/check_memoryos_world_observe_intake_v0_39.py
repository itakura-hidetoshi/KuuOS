#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from runtime.kuuos_memoryos_world_observe_intake_v0_39 import (
    BOUNDARY,
    CAPSULE_ROUTES,
    CAPSULE_VERSION,
    INTAKE_ROUTES,
    INTAKE_VERSION,
    NON_AUTHORITY,
    VERSION,
    WORLD_CANDIDATE_VERSION,
)

ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def main() -> int:
    require(VERSION == "kuuos_memoryos_world_observe_intake_v0_39", "version mismatch")
    require(
        WORLD_CANDIDATE_VERSION
        == "world_vacuum_expectation_observation_candidate_packet_v0_50",
        "WORLD candidate version mismatch",
    )
    require(
        CAPSULE_VERSION == "memoryos_world_observe_intake_capsule_v0_39",
        "capsule version mismatch",
    )
    require(
        INTAKE_VERSION == "memoryos_world_observe_intake_envelope_v0_39",
        "intake version mismatch",
    )
    for value in NON_AUTHORITY.values():
        require(value is False, "non-authority promoted")
    for value in BOUNDARY.values():
        require(value is True, "boundary lost")
    for route in (
        "QUARANTINE_ANALYTIC_SOURCE",
        "REOBSERVE_ANALYTIC_SOURCE",
        "HOLD_INCOMPLETE_WORLD_CANDIDATE",
        "PRESERVE_RESIDUE_FOR_OBSERVE_OWNER",
        "READY_FOR_OBSERVE_OWNER_REVIEW",
    ):
        require(route in CAPSULE_ROUTES, f"capsule route missing: {route}")
    for route in (
        "QUARANTINE_OBSERVE_INTAKE",
        "REOBSERVE_BEFORE_OBSERVE_INTAKE",
        "HOLD_WORLD_CANDIDATE_INCOMPLETE",
        "RETURN_CANDIDATE_WITH_ACTIVE_SHIELD",
        "RETURN_CANDIDATE_WITH_RESIDUE_TO_OBSERVE_OWNER",
        "RETURN_READ_ONLY_CANDIDATE_TO_OBSERVE_OWNER",
    ):
        require(route in INTAKE_ROUTES, f"intake route missing: {route}")

    manifest_path = ROOT / "manifests/kuuos_memoryos_world_observe_intake_v0_39.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest["version"] == VERSION, "manifest version mismatch")
    require(
        manifest["memory_predecessor"]
        == "kuuos_memoryos_analytic_hilbert_context_v0_38",
        "memory predecessor mismatch",
    )
    require(
        manifest["world_predecessor"]
        == "KUOS.WORLD.VacuumExpectationObservationCandidateBridgeV0_50",
        "WORLD predecessor mismatch",
    )
    require(
        manifest["observe_boundary"]
        == "KUOS.ObserveOS.ReplanLineageObservationEnvelopeV0_2",
        "ObserveOS boundary mismatch",
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
    ):
        require((ROOT / manifest[key]).is_file(), f"manifest file missing: {key}")
    require(set(manifest["capsule_routes"]) == CAPSULE_ROUTES, "capsule routes mismatch")
    require(set(manifest["intake_routes"]) == INTAKE_ROUTES, "intake routes mismatch")
    for field in (
        "world_candidate_is_raw_evidence",
        "world_candidate_is_observation_record",
        "world_candidate_is_verification_result",
        "world_candidate_has_act_effect_lineage",
        "automatic_observe_activation",
        "automatic_observe_commit",
        "retrieval_grants_plan_activation",
        "retrieval_grants_actos_authority",
        "memory_may_discharge_blocker",
        "world_update_allowed",
        "memory_overwrite_allowed",
    ):
        require(manifest["boundaries"][field] is False, f"boundary promoted: {field}")
    for field in (
        "observeos_owner_review_required",
        "raw_evidence_still_required",
        "observation_not_verification",
        "verification_required",
        "append_only_lineage",
    ):
        require(manifest["boundaries"][field] is True, f"boundary missing: {field}")

    runtime = ROOT / "runtime/kuuos_memoryos_world_observe_intake_v0_39.py"
    require_tokens(
        runtime,
        (
            "world_candidate_source_world_mismatch",
            "world_candidate_observation_record_claim_forbidden",
            "act_effect_observation_route_impersonated",
            "raw_evidence_required",
            "RETURN_CANDIDATE_WITH_ACTIVE_SHIELD",
            "RETURN_READ_ONLY_CANDIDATE_TO_OBSERVE_OWNER",
        ),
    )
    tests = ROOT / "tests/test_memoryos_world_observe_intake_v0_39.py"
    require_tokens(
        tests,
        (
            "test_complete_candidate_routes_to_observe_owner_review",
            "test_observation_and_authority_impersonation_are_rejected",
            "test_same_candidate_identity_substitution_is_rejected",
            "test_blocked_capability_returns_active_shield",
            "test_read_only_owner_intake_creates_no_observation_record",
        ),
    )
    documentation = ROOT / "docs/KUUOS_MEMORYOS_WORLD_OBSERVE_INTAKE_v0_39.md"
    require_tokens(
        documentation,
        (
            "WORLD candidate != raw evidence",
            "WORLD candidate != ObserveOS observation record",
            "ObserveOS owner review != ObserveOS activation",
            "observation != verification",
        ),
    )
    formal = ROOT / "formal/KUOS/OpenHorizon/MemoryOSWorldObserveIntakeKernelV0_39.lean"
    require_tokens(
        formal,
        (
            "MemoryOSWorldObserveIntakeV039",
            "world_candidate_cannot_become_observation_record",
            "memoryos_world_observe_intake_boundary",
            "k.worldObservation.vacuumExpectationNotFactProof",
            "k.observeBoundary.verificationForbidden",
        ),
    )
    require_tokens(
        ROOT / "formal/KUOS.lean",
        ("KUOS.OpenHorizon.MemoryOSWorldObserveIntakeKernelV0_39",),
    )
    require_tokens(
        ROOT / "formal/KUOS/ObserveOS/ReplanLineageObservationEnvelopeV0_2.lean",
        (
            "observation_requires_recorded_source_effect",
            "observation_does_not_discharge_verification",
            "observe_lineage_envelope_grants_no_new_authority",
        ),
    )
    require_tokens(
        ROOT / "formal/KUOS/WORLD/VacuumExpectationObservationCandidateBridgeV0_50.lean",
        (
            "vacuumExpectationNotFact",
            "candidateNotPlanActivation",
            "candidateNotActAuthority",
        ),
    )
    require_tokens(
        ROOT / "scripts/run_kuuos_runtime_full_check_v0_50.py",
        ("check_memoryos_v039",),
    )
    print("MemoryOS WORLD ObserveOS intake v0.39 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
