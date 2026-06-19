from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

import runtime.kuuos_qi_world_cross_cycle_reentry_v1_4_new as _impl
from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_decision_os_wa_kernel_v0_3 import (
    build_replan_wa_activation_receipt,
)
from runtime.kuuos_plan_os_kernel_v0_1 import build_initial_plan_state
from runtime.kuuos_plan_os_store_v0_1 import PlanStore
from runtime.v01_plan_os_replan_bound_synthesis import (
    _candidate_steps,
    _complete_plan,
)

VERSION = _impl.VERSION
RECEIPT_VERSION = _impl.RECEIPT_VERSION
CYCLE_ID = _impl.CYCLE_ID
CROSS_CYCLE_NON_AUTHORITY = _impl.CROSS_CYCLE_NON_AUTHORITY
cross_cycle_receipt_digest = _impl.cross_cycle_receipt_digest


def _build_next_plan_from_learning(
    root: Path,
    wa: Mapping[str, Any],
    learning_delta_digest: str,
) -> dict[str, Any]:
    wa_activation = build_replan_wa_activation_receipt(
        state=wa,
        mission_cycle_phase="replan",
        mission_cycle_state_digest=sha("cross-cycle-wa-replan-state"),
        replan_receipt_digest=sha("cross-cycle-wa-replan-receipt"),
        next_plan_basis_digest=learning_delta_digest,
        now_ms=50_000,
    )
    store = PlanStore(root)
    state = store.initialize(
        build_initial_plan_state(
            plan_id="cross-cycle-plan-v14",
            source_wa_state=wa,
            replan_activation_receipt=wa_activation,
            plan_budget=2.0,
            maximum_step_risk=0.40,
            now_ms=60_000,
        )
    )
    state, _ = _complete_plan(store, state, _candidate_steps(), 10)
    return state


def validate_cross_cycle_reentry_receipt(
    receipt: Mapping[str, Any],
) -> list[str]:
    errors = list(_impl.validate_cross_cycle_reentry_receipt(receipt))
    try:
        previous = dict(receipt.get("previous_cycle_receipt", {}))
        next_artifacts = dict(receipt.get("next_cycle_artifacts", {}))
        learn = previous.get("native_artifacts", {}).get("LearnOS", {})
        plan = next_artifacts.get("PlanOS", {})
        if plan.get("next_plan_basis_digest") != learn.get(
            "learning_delta_digest"
        ):
            errors.append("cross_cycle_plan_learning_basis_mismatch")
    except (AttributeError, TypeError):
        errors.append("cross_cycle_plan_learning_basis_unreadable")
    return errors


def build_cross_cycle_reentry_receipt(root: Path) -> dict[str, Any]:
    previous = _impl.build_native_full_cycle_receipt(root / "previous-cycle")
    prior_errors = _impl.validate_native_full_cycle_receipt(previous)
    if prior_errors:
        raise ValueError("previous_cycle_invalid:" + ";".join(prior_errors))

    learn = previous["native_artifacts"]["LearnOS"]
    lineage_id = str(learn["lineage_id"])
    mission_contract_digest = str(learn["mission_contract_digest"])

    belief, belief_activation = _impl._build_next_belief(
        root / "next-belief",
        lineage_id=lineage_id,
        previous_receipt=previous,
    )
    decision = _impl._build_next_decision(
        root / "next-decision",
        lineage_id=lineage_id,
        mission_contract_digest=mission_contract_digest,
        previous_learn_state_digest=learn["learn_state_digest"],
        belief_activation=belief_activation,
    )
    plural = _impl._build_next_plural(
        root / "next-plural",
        lineage_id=lineage_id,
        decision=decision,
    )
    wa = _impl._build_next_wa(root / "next-wa", plural)
    plan = _build_next_plan_from_learning(
        root / "next-plan",
        wa,
        str(learn["learning_delta_digest"]),
    )

    next_artifacts = {
        "BeliefOS": belief,
        "BeliefActivation": belief_activation,
        "DecisionOS": decision,
        "DecisionOSPlural": plural,
        "DecisionOSWa": wa,
        "PlanOS": plan,
    }
    next_errors = _impl._validate_next_artifacts(next_artifacts)
    if next_errors:
        raise ValueError("next_cycle_invalid:" + ";".join(next_errors))

    qi_receipt = _impl._build_cross_cycle_qi_receipt(previous, next_artifacts)
    world = _impl._build_cross_cycle_world_projection(previous, next_artifacts)
    receipt = {
        "version": RECEIPT_VERSION,
        "cycle_id": CYCLE_ID,
        "previous_cycle_receipt": deepcopy(previous),
        "previous_cycle_receipt_digest": previous[
            "native_full_cycle_receipt_digest"
        ],
        "next_cycle_artifacts": deepcopy(next_artifacts),
        "cross_cycle_process_lineage_digest": _impl._expected_process_lineage_digest(
            previous, next_artifacts
        ),
        "cross_cycle_qi_receipt": qi_receipt,
        "cross_cycle_world_projection": world,
        "cross_cycle_world_projection_digest": world[
            "world_projection_digest"
        ],
        "previous_cycle_immutable": True,
        "next_act_not_started": True,
        "cross_cycle_non_authority": deepcopy(CROSS_CYCLE_NON_AUTHORITY),
        "cross_cycle_receipt_digest": "",
    }
    receipt["cross_cycle_receipt_digest"] = cross_cycle_receipt_digest(receipt)
    errors = validate_cross_cycle_reentry_receipt(receipt)
    if errors:
        raise ValueError("cross_cycle_receipt_invalid:" + ";".join(errors))
    return receipt
