from __future__ import annotations

from copy import deepcopy
from typing import Any

from runtime.kuuos_qi_world_cross_cycle_blocker_core_v1_5 import BLOCKER_ORDER
from runtime.kuuos_qi_world_yinyang_process_blocker_complementarity_v2_3 import (
    STATUS_OK,
    build_yinyang_process_blocker_receipt,
    relational_polarity,
    validate_yinyang_process_blocker_receipt,
)


def _qi() -> dict[str, Any]:
    return {
        "cycle_id": "qi-world-yinyang-v23",
        "process_tensor_visible": True,
        "transition_continuity_visible": True,
        "memory_continuity_visible": True,
        "qi_process_tensor_receipt_digest": "qi-digest-v23",
    }


def _blockers() -> dict[str, Any]:
    return {
        "cycle_id": "qi-world-yinyang-v23",
        "composed_blocker_vector": {name: True for name in BLOCKER_ORDER},
        "all_required_blockers_active": True,
        "blocker_certificate_digest": "blocker-digest-v15",
    }


def run_yinyang_process_blocker_scenarios() -> dict[str, Any]:
    balanced = build_yinyang_process_blocker_receipt(
        _qi(), _blockers(), qi_intensity=2, qi_capacity=3
    )
    assert not validate_yinyang_process_blocker_receipt(_qi(), _blockers(), balanced)
    assert balanced["candidate_flow_admissible"] is True
    assert balanced["effective_qi_intensity"] == 2

    saturated = build_yinyang_process_blocker_receipt(
        _qi(), _blockers(), qi_intensity=4, qi_capacity=3
    )
    assert saturated["candidate_flow_admissible"] is False
    assert saturated["effective_qi_intensity"] == 0
    assert saturated["coupling"]["saturation_generates_yin_containment"] is True

    lost = _blockers()
    lost["composed_blocker_vector"] = deepcopy(lost["composed_blocker_vector"])
    lost["composed_blocker_vector"]["truth_authority_blocker"] = False
    lost["all_required_blockers_active"] = False
    boundary_loss = build_yinyang_process_blocker_receipt(
        _qi(), lost, qi_intensity=1, qi_capacity=3
    )
    assert boundary_loss["candidate_flow_admissible"] is False
    assert boundary_loss["disposition"] == "YIN_FAIL_CLOSED_ON_BOUNDARY_LOSS"

    assert relational_polarity("contain") == "yin"
    assert relational_polarity("propagate") == "yang"

    return {
        "status": STATUS_OK,
        "balanced_disposition": balanced["disposition"],
        "saturated_disposition": saturated["disposition"],
        "boundary_loss_disposition": boundary_loss["disposition"],
        "polarity_is_relational": True,
        "non_authority_preserved": all(
            value is False for value in balanced["non_authority"].values()
        ),
    }
