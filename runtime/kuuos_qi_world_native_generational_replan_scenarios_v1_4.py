from __future__ import annotations

import tempfile
from copy import deepcopy
from pathlib import Path

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_plan_os_replan_types_v0_2 import replan_state_digest
from runtime.kuuos_qi_world_native_generational_replan_v1_4 import (
    _digest,
    build_native_generational_replan_receipt,
    receipt_digest,
    validate_native_generational_replan_receipt,
)


def _retag(receipt: dict) -> dict:
    receipt["native_generational_replan_receipt_digest"] = ""
    receipt["native_generational_replan_receipt_digest"] = receipt_digest(receipt)
    return receipt


def _require_error(receipt: dict, expected: str) -> None:
    errors = validate_native_generational_replan_receipt(_retag(receipt))
    if expected not in errors:
        raise AssertionError({"expected": expected, "errors": errors})


def run_native_generational_replan_scenarios() -> dict:
    with tempfile.TemporaryDirectory(
        prefix="kuuos-qi-world-native-generational-v14-"
    ) as temporary:
        receipt = build_native_generational_replan_receipt(Path(temporary))
        assert validate_native_generational_replan_receipt(receipt) == []
        artifacts = receipt["native_replan_artifacts"]
        replan = artifacts["PlanOSReplan"]
        decision = artifacts["DecisionOS"]
        plural = artifacts["DecisionOSPlural"]
        wa = artifacts["DecisionOSWa"]
        source = receipt["source_native_full_cycle_receipt"]
        source_artifacts = source["native_artifacts"]

        assert replan["source_plan_state_digest"] == source_artifacts["PlanOS"][
            "plan_state_digest"
        ]
        assert replan["source_learn_state_digest"] == source_artifacts["LearnOS"][
            "learn_state_digest"
        ]
        assert decision["source_belief_receipt_digest"] == source_artifacts[
            "BeliefOSReceipt"
        ]["belief_gerbe_receipt_digest"]
        assert plural["source_decision_state_digest"] == decision[
            "decision_state_digest"
        ]
        assert wa["source_plural_state_digest"] == plural["plural_state_digest"]
        assert replan["decision_receipt"]["decision_os_state_digest"] == decision[
            "decision_state_digest"
        ]
        assert replan["decision_receipt"]["wa_relational_harmony_digest"] == wa[
            "wa_state_digest"
        ]
        assert replan["selected_candidate_id"] == decision["selected_option_id"]
        assert receipt["target_generation"] == receipt["source_generation"] + 1
        assert replan["active_now"] is False
        assert replan["host_license_granted"] is False

        learn_substitution = deepcopy(receipt)
        changed_replan = learn_substitution["native_replan_artifacts"][
            "PlanOSReplan"
        ]
        changed_replan["source_learn_state_digest"] = sha(
            "substituted-learn-state"
        )
        changed_replan["replan_state_digest"] = ""
        changed_replan["replan_state_digest"] = replan_state_digest(changed_replan)
        _require_error(learn_substitution, "v14_source_learn_mismatch")

        history_substitution = deepcopy(receipt)
        extended = history_substitution["extended_qi_process_receipt"]
        history = extended["enriched_state"]["process_history"]
        history[0]["target_state_digest"] = sha("substituted-history-target")
        history_substitution["extended_qi_process_receipt_digest"] = sha(extended)
        _require_error(history_substitution, "v14_qi_history_prefix_mutated")

        mutable_world = deepcopy(receipt)
        world = mutable_world["next_world_projection"]
        world["runtime_updates_world"] = True
        world["world_projection_digest"] = ""
        world["world_projection_digest"] = _digest(world, "world_projection_digest")
        mutable_world["next_world_projection_digest"] = world[
            "world_projection_digest"
        ]
        _require_error(
            mutable_world,
            "v14_world_runtime_updates_world_invalid",
        )

        present_activation = deepcopy(receipt)
        changed_replan = present_activation["native_replan_artifacts"][
            "PlanOSReplan"
        ]
        changed_replan["active_now"] = True
        changed_replan["replan_state_digest"] = ""
        changed_replan["replan_state_digest"] = replan_state_digest(changed_replan)
        _require_error(present_activation, "v14_present_activation_forbidden")

        return {
            "status": "KUUOS_QI_WORLD_NATIVE_GENERATIONAL_REPLAN_V1_4_OK",
            "source_generation": receipt["source_generation"],
            "target_generation": receipt["target_generation"],
            "source_full_cycle_receipt_digest": receipt[
                "source_native_full_cycle_receipt_digest"
            ],
            "source_qi_process_receipt_digest": receipt[
                "source_qi_process_receipt_digest"
            ],
            "extended_qi_process_receipt_digest": receipt[
                "extended_qi_process_receipt_digest"
            ],
            "source_world_projection_digest": receipt[
                "source_world_projection_digest"
            ],
            "next_world_projection_digest": receipt[
                "next_world_projection_digest"
            ],
            "native_decision_state_digest": decision["decision_state_digest"],
            "native_wa_state_digest": wa["wa_state_digest"],
            "native_replan_state_digest": replan["replan_state_digest"],
            "next_plan_basis_digest": replan["next_plan_basis_digest"],
            "selected_candidate_id": replan["selected_candidate_id"],
            "future_only": receipt["future_only"],
            "active_now": receipt["active_now"],
            "non_authority": receipt["non_authority"],
        }
