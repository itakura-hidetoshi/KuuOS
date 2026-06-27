from __future__ import annotations

from runtime.kuuos_capabilityos_qi_world_kernel_v0_60 import (
    GUARD_ORDER,
    build_capability_candidate,
    build_capability_definition,
    build_capability_path_candidate,
    validate_capability_candidate,
    validate_capability_path_candidate,
)


def fixture_definition() -> dict:
    return build_capability_definition(
        capability_id="reason-over-world",
        revision=0,
        provider_id="provider-a",
        skill_digest="skill-digest",
        task_type="world-reasoning",
        input_schema_digest="input-schema",
        output_schema_digest="output-schema",
        world_preconditions=["source-visible"],
        required_tools=["python"],
        verifier_capability="independent-verifier",
        known_failure_modes=["distribution-shift"],
        max_cost=20,
        max_steps=20,
        max_duration_ms=10_000,
    )


def fixture_qi(*, ready: bool = True) -> dict:
    return {
        "cycle_id": "cycle-1",
        "process_tensor_visible": ready,
        "transition_continuity_visible": ready,
        "memory_continuity_visible": ready,
        "nonmarkov_memory_visible": True,
        "qi_process_tensor_receipt_digest": "qi-digest",
    }


def fixture_yin_yang(
    *, intensity: int = 3, capacity: int = 5, boundary: bool = True
) -> dict:
    return {
        "yin_yang_receipt_digest": "yin-yang-digest",
        "yin_surface": {
            "boundary_visible": boundary,
            "all_required_blockers_active": boundary,
            "blocker_vector": {name: boundary for name in GUARD_ORDER},
        },
        "yang_surface": {"qi_intensity": intensity, "qi_capacity": capacity},
    }


def fixture_world(*, plural: bool = False, applicable: bool = True) -> dict:
    candidates = [
        {
            "world_candidate_id": "w1",
            "world_fragment_digest": "wf1",
            "supported_predicates": ["source-visible"] if applicable else [],
            "contradicted_predicates": [],
            "predicted_outcome_digest": "outcome-a",
            "uncertainty": 0.2,
            "admissible": True,
        }
    ]
    if plural:
        candidates.append(
            {
                "world_candidate_id": "w2",
                "world_fragment_digest": "wf2",
                "supported_predicates": ["source-visible"],
                "contradicted_predicates": [],
                "predicted_outcome_digest": "outcome-b",
                "uncertainty": 0.4,
                "admissible": True,
            }
        )
    return {
        "world_store_id": "world-store",
        "root_lineage_digest": "root-lineage",
        "world_generation": 3,
        "sourced_world_fragment_digest": "sourced-world",
        "world_candidates": candidates,
    }


def fixture_candidate(**overrides) -> dict:
    kwargs = {
        "definition": fixture_definition(),
        "mission_id": "mission",
        "lineage_id": "lineage",
        "cycle_id": "cycle-1",
        "chart_id": "chart",
        "qi_receipt": fixture_qi(),
        "yin_yang_receipt": fixture_yin_yang(),
        "world_context": fixture_world(),
        "memory_context": {
            "contradiction_status": "NONE",
            "memory_capsule_digest": "memory",
        },
        "available_tools": ["python"],
        "available_verifiers": ["independent-verifier"],
        "requested_cost": 5,
        "requested_steps": 5,
        "requested_duration_ms": 1000,
        "validity_not_before_ms": 1,
        "validity_expires_at_ms": 100,
    }
    kwargs.update(overrides)
    return build_capability_candidate(**kwargs)


def run_capabilityos_qi_world_scenarios() -> dict:
    definition = fixture_definition()
    ready = fixture_candidate()
    plural = fixture_candidate(world_context=fixture_world(plural=True))
    saturated = fixture_candidate(
        yin_yang_receipt=fixture_yin_yang(intensity=8, capacity=5)
    )
    held = fixture_candidate(available_verifiers=[])
    guard_loss = fixture_candidate(
        yin_yang_receipt=fixture_yin_yang(boundary=False)
    )
    process_gap = fixture_candidate(qi_receipt=fixture_qi(ready=False))
    world_gap = fixture_candidate(world_context=fixture_world(applicable=False))

    for packet in (ready, plural, saturated, held, guard_loss, process_gap, world_gap):
        errors = validate_capability_candidate(definition=definition, candidate=packet)
        if errors:
            raise AssertionError("candidate_invalid:" + ";".join(errors))

    path = build_capability_path_candidate(
        path_id="ready-plus-held", candidates=[ready, held]
    )
    path_errors = validate_capability_path_candidate(path)
    if path_errors:
        raise AssertionError("path_invalid:" + ";".join(path_errors))

    return {
        "ready_route": ready["disposition"],
        "plural_route": plural["disposition"],
        "saturation_route": saturated["disposition"],
        "verifier_route": held["disposition"],
        "guard_route": guard_loss["disposition"],
        "process_route": process_gap["disposition"],
        "world_route": world_gap["disposition"],
        "path_ready": path["path_ready_for_planos_candidate"],
        "path_support": path["effective_path_support"],
        "world_plurality_preserved": plural["world_context"][
            "world_plurality_visible"
        ],
        "authority_extended": any(ready["non_authority"].values()),
    }
