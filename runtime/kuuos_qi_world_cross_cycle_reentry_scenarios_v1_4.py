from __future__ import annotations

import tempfile
from copy import deepcopy
from pathlib import Path

from runtime.kuuos_belief_os_types_v0_1 import (
    activation_receipt_digest as belief_activation_digest,
    sha,
    state_digest as belief_state_digest,
)
from runtime.kuuos_decision_os_types_v0_1 import state_digest as decision_state_digest
from runtime.kuuos_plan_os_types_v0_1 import state_digest as plan_state_digest
from runtime.kuuos_qi_world_cross_cycle_reentry_v1_4 import (
    build_cross_cycle_reentry_receipt,
    cross_cycle_receipt_digest,
    validate_cross_cycle_reentry_receipt,
)


def _retag_receipt(receipt: dict) -> dict:
    receipt["cross_cycle_receipt_digest"] = ""
    receipt["cross_cycle_receipt_digest"] = cross_cycle_receipt_digest(receipt)
    return receipt


def _require_error(receipt: dict, expected: str) -> None:
    errors = validate_cross_cycle_reentry_receipt(_retag_receipt(receipt))
    if expected not in errors:
        raise AssertionError({"expected": expected, "errors": errors})


def run_cross_cycle_reentry_scenarios() -> dict:
    with tempfile.TemporaryDirectory(prefix="kuuos-cross-cycle-v14-") as temporary:
        receipt = build_cross_cycle_reentry_receipt(Path(temporary))
        assert validate_cross_cycle_reentry_receipt(receipt) == []

        previous = receipt["previous_cycle_receipt"]
        previous_artifacts = previous["native_artifacts"]
        next_artifacts = receipt["next_cycle_artifacts"]
        learn = previous_artifacts["LearnOS"]
        belief = next_artifacts["BeliefOS"]
        activation = next_artifacts["BeliefActivation"]
        decision = next_artifacts["DecisionOS"]
        plural = next_artifacts["DecisionOSPlural"]
        wa = next_artifacts["DecisionOSWa"]
        plan = next_artifacts["PlanOS"]

        assert belief["source_memory_digest"] == learn["learn_state_digest"]
        assert learn["learning_delta_digest"] in belief["evidence_digests"]
        assert activation["next_plan_basis_digest"] == learn["learning_delta_digest"]
        assert decision["source_belief_receipt_digest"] == activation[
            "belief_activation_receipt_digest"
        ]
        assert plural["source_decision_state_digest"] == decision[
            "decision_state_digest"
        ]
        assert wa["source_plural_state_digest"] == plural["plural_state_digest"]
        assert plan["source_wa_state_digest"] == wa["wa_state_digest"]
        assert receipt["previous_cycle_immutable"] is True
        assert receipt["next_act_not_started"] is True

        memory_substitution = deepcopy(receipt)
        mutated_belief = memory_substitution["next_cycle_artifacts"]["BeliefOS"]
        mutated_belief["source_memory_digest"] = sha("substituted-memory")
        mutated_belief["belief_state_digest"] = ""
        mutated_belief["belief_state_digest"] = belief_state_digest(mutated_belief)
        _require_error(
            memory_substitution,
            "cross_cycle_belief_memory_binding_mismatch",
        )

        basis_substitution = deepcopy(receipt)
        mutated_activation = basis_substitution["next_cycle_artifacts"][
            "BeliefActivation"
        ]
        mutated_activation["next_plan_basis_digest"] = sha("substituted-basis")
        mutated_activation["belief_activation_receipt_digest"] = ""
        mutated_activation["belief_activation_receipt_digest"] = belief_activation_digest(
            mutated_activation
        )
        _require_error(
            basis_substitution,
            "cross_cycle_learning_delta_basis_mismatch",
        )

        decision_substitution = deepcopy(receipt)
        mutated_decision = decision_substitution["next_cycle_artifacts"][
            "DecisionOS"
        ]
        mutated_decision["source_belief_receipt_digest"] = sha(
            "substituted-belief-receipt"
        )
        mutated_decision["decision_state_digest"] = ""
        mutated_decision["decision_state_digest"] = decision_state_digest(
            mutated_decision
        )
        _require_error(
            decision_substitution,
            "cross_cycle_decision_belief_mismatch",
        )

        plan_substitution = deepcopy(receipt)
        mutated_plan = plan_substitution["next_cycle_artifacts"]["PlanOS"]
        mutated_plan["source_wa_state_digest"] = sha("substituted-wa")
        mutated_plan["plan_state_digest"] = ""
        mutated_plan["plan_state_digest"] = plan_state_digest(mutated_plan)
        _require_error(plan_substitution, "cross_cycle_plan_wa_mismatch")

        lineage_substitution = deepcopy(receipt)
        mutated_lineage_belief = lineage_substitution["next_cycle_artifacts"][
            "BeliefOS"
        ]
        mutated_lineage_belief["lineage_id"] = "substituted-lineage"
        mutated_lineage_belief["belief_state_digest"] = ""
        mutated_lineage_belief["belief_state_digest"] = belief_state_digest(
            mutated_lineage_belief
        )
        _require_error(lineage_substitution, "cross_cycle_lineage_mismatch")

        qi_mutation = deepcopy(receipt)
        qi_mutation["cross_cycle_qi_receipt"]["nonmarkov_memory_visible"] = False
        _require_error(qi_mutation, "cross_cycle_qi_nonmarkov_not_visible")

        world_mutation = deepcopy(receipt)
        world = world_mutation["cross_cycle_world_projection"]
        world["runtime_updates_world"] = True
        world["world_projection_digest"] = ""
        world["world_projection_digest"] = sha(
            {key: value for key, value in world.items() if key != "world_projection_digest"}
        )
        world_mutation["cross_cycle_world_projection_digest"] = world[
            "world_projection_digest"
        ]
        _require_error(
            world_mutation,
            "cross_cycle_world_runtime_updates_world_invalid",
        )

        previous_mutation = deepcopy(receipt)
        previous_mutation["previous_cycle_immutable"] = False
        _require_error(
            previous_mutation,
            "cross_cycle_previous_cycle_not_immutable",
        )

        act_boundary_mutation = deepcopy(receipt)
        act_boundary_mutation["next_act_not_started"] = False
        _require_error(
            act_boundary_mutation,
            "cross_cycle_next_act_boundary_invalid",
        )

        return {
            "status": "KUUOS_QI_WORLD_CROSS_CYCLE_REENTRY_V1_4_OK",
            "previous_cycle_receipt_digest": receipt[
                "previous_cycle_receipt_digest"
            ],
            "previous_learn_state_digest": learn["learn_state_digest"],
            "previous_learning_delta_digest": learn["learning_delta_digest"],
            "next_belief_state_digest": belief["belief_state_digest"],
            "next_decision_state_digest": decision["decision_state_digest"],
            "next_wa_state_digest": wa["wa_state_digest"],
            "next_plan_state_digest": plan["plan_state_digest"],
            "cross_cycle_process_lineage_digest": receipt[
                "cross_cycle_process_lineage_digest"
            ],
            "cross_cycle_world_projection_digest": receipt[
                "cross_cycle_world_projection_digest"
            ],
            "next_artifact_count": len(next_artifacts),
            "next_act_not_started": receipt["next_act_not_started"],
            "cross_cycle_non_authority": receipt[
                "cross_cycle_non_authority"
            ],
        }
