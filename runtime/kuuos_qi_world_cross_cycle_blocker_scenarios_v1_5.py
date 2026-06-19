from __future__ import annotations

import tempfile
from copy import deepcopy
from pathlib import Path

from runtime.kuuos_qi_world_cross_cycle_blocker_v1_5 import (
    BLOCKER_ORDER,
    blocker_certificate_digest,
    blocker_identity,
    blocker_meet,
    blocker_receipt_digest,
    blocker_weaker_or_equal,
    build_cross_cycle_blocker_certificate,
    build_cross_cycle_blocker_receipt,
    validate_cross_cycle_blocker_receipt,
)
from runtime.kuuos_qi_world_cross_cycle_reentry_v1_4 import (
    cross_cycle_receipt_digest,
)


def _retag(receipt: dict) -> dict:
    receipt["cross_cycle_blocker_receipt_digest"] = ""
    receipt["cross_cycle_blocker_receipt_digest"] = blocker_receipt_digest(
        receipt
    )
    return receipt


def _retag_certificate(certificate: dict) -> dict:
    certificate["blocker_certificate_digest"] = ""
    certificate["blocker_certificate_digest"] = blocker_certificate_digest(
        certificate
    )
    return certificate


def _require_error(receipt: dict, expected: str) -> None:
    errors = validate_cross_cycle_blocker_receipt(_retag(receipt))
    if expected not in errors:
        raise AssertionError({"expected": expected, "errors": errors})


def run_cross_cycle_blocker_scenarios() -> dict:
    with tempfile.TemporaryDirectory(
        prefix="kuuos-cross-cycle-blocker-v15-"
    ) as temporary:
        receipt = build_cross_cycle_blocker_receipt(Path(temporary))
        assert validate_cross_cycle_blocker_receipt(receipt) == []

        certificate = receipt["blocker_certificate"]
        components = certificate["component_vectors"]
        vectors = list(components.values())
        identity = blocker_identity()
        left = vectors[0]
        right = vectors[1]
        third = vectors[2]

        assert blocker_meet(left, identity) == left
        assert blocker_meet(identity, left) == left
        assert blocker_meet(left, right) == blocker_meet(right, left)
        assert blocker_meet(blocker_meet(left, right), third) == blocker_meet(
            left, blocker_meet(right, third)
        )
        assert blocker_meet(left, left) == left
        assert blocker_weaker_or_equal(blocker_meet(left, right), left)
        assert blocker_weaker_or_equal(blocker_meet(left, right), right)

        composed = certificate["composed_blocker_vector"]
        assert list(composed) == list(BLOCKER_ORDER)
        assert all(composed.values())
        assert certificate["all_required_blockers_active"] is True
        assert certificate["missing_blockers"] == []
        assert certificate["fail_closed_on_boundary_loss"] is True
        assert certificate["candidate_weighting_not_truth"] is True
        assert certificate["barrier_potential_can_only_block_or_probe"] is True
        assert receipt["unlicensed_transition_blocked"] is True
        assert receipt["next_act_started"] is False
        assert receipt["exact_world_updated"] is False
        assert receipt["previous_cycle_overwritten"] is False
        assert receipt["recursive_self_invocation_started"] is False

        forged_component = deepcopy(receipt)
        forged_certificate = forged_component["blocker_certificate"]
        forged_certificate["component_vectors"]["world_projection_surface"][
            "world_identity_blocker"
        ] = False
        _retag_certificate(forged_certificate)
        _require_error(forged_component, "blocker_component_vectors_invalid")

        forged_composition = deepcopy(receipt)
        forged_certificate = forged_composition["blocker_certificate"]
        forged_certificate["composed_blocker_vector"][
            "same_cycle_self_loop_blocker"
        ] = False
        forged_certificate["active_blockers"].remove(
            "same_cycle_self_loop_blocker"
        )
        forged_certificate["missing_blockers"] = [
            "same_cycle_self_loop_blocker"
        ]
        forged_certificate["all_required_blockers_active"] = False
        _retag_certificate(forged_certificate)
        _require_error(forged_composition, "blocker_composed_vector_invalid")

        execution_boundary_loss = deepcopy(receipt)
        source = execution_boundary_loss["source_cross_cycle_receipt"]
        source["cross_cycle_non_authority"]["bridge_grants_execution"] = True
        source["cross_cycle_receipt_digest"] = ""
        source["cross_cycle_receipt_digest"] = cross_cycle_receipt_digest(source)
        execution_boundary_loss["source_cross_cycle_receipt_digest"] = source[
            "cross_cycle_receipt_digest"
        ]
        execution_boundary_loss["blocker_certificate"] = (
            build_cross_cycle_blocker_certificate(source)
        )
        execution_boundary_loss["all_required_blockers_active"] = False
        execution_boundary_loss["unlicensed_transition_blocked"] = False
        _require_error(
            execution_boundary_loss,
            "blocker_execution_authority_blocker_inactive",
        )

        world_boundary_loss = deepcopy(receipt)
        source = world_boundary_loss["source_cross_cycle_receipt"]
        world = source["cross_cycle_world_projection"]
        world["runtime_updates_world"] = True
        world["world_projection_digest"] = ""
        from runtime.kuuos_belief_os_types_v0_1 import sha

        world["world_projection_digest"] = sha(
            {
                key: value
                for key, value in world.items()
                if key != "world_projection_digest"
            }
        )
        source["cross_cycle_world_projection_digest"] = world[
            "world_projection_digest"
        ]
        source["cross_cycle_receipt_digest"] = ""
        source["cross_cycle_receipt_digest"] = cross_cycle_receipt_digest(source)
        world_boundary_loss["source_cross_cycle_receipt_digest"] = source[
            "cross_cycle_receipt_digest"
        ]
        world_boundary_loss["blocker_certificate"] = (
            build_cross_cycle_blocker_certificate(source)
        )
        world_boundary_loss["all_required_blockers_active"] = False
        world_boundary_loss["unlicensed_transition_blocked"] = False
        _require_error(
            world_boundary_loss,
            "blocker_world_identity_blocker_inactive",
        )

        present_activation = deepcopy(receipt)
        present_activation["next_act_started"] = True
        _require_error(present_activation, "blocker_next_act_started_invalid")

        authority_forgery = deepcopy(receipt)
        authority_forgery["non_authority"]["blocker_issues_authority"] = True
        _require_error(authority_forgery, "blocker_receipt_non_authority_invalid")

        return {
            "status": "KUUOS_QI_WORLD_CROSS_CYCLE_BLOCKER_V1_5_OK",
            "source_cross_cycle_receipt_digest": receipt[
                "source_cross_cycle_receipt_digest"
            ],
            "blocker_certificate_digest": certificate[
                "blocker_certificate_digest"
            ],
            "cross_cycle_blocker_receipt_digest": receipt[
                "cross_cycle_blocker_receipt_digest"
            ],
            "blocker_count": len(BLOCKER_ORDER),
            "active_blockers": certificate["active_blockers"],
            "missing_blockers": certificate["missing_blockers"],
            "disposition": certificate["disposition"],
            "unlicensed_transition_blocked": receipt[
                "unlicensed_transition_blocked"
            ],
            "fail_closed_on_boundary_loss": certificate[
                "fail_closed_on_boundary_loss"
            ],
            "non_authority": receipt["non_authority"],
        }
