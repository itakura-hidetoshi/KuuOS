from __future__ import annotations

import tempfile
from copy import deepcopy
from pathlib import Path

from runtime.kuuos_qi_world_licensed_effect_evidence_closure_v1_8 import (
    BLOCKER_ORDER,
    blocker_certificate_digest,
    build_licensed_effect_evidence_closure_receipt,
    closure_receipt_digest,
    validate_licensed_effect_evidence_closure_receipt,
)


def _retag(receipt: dict) -> dict:
    receipt["licensed_effect_evidence_closure_receipt_digest"] = ""
    receipt["licensed_effect_evidence_closure_receipt_digest"] = (
        closure_receipt_digest(receipt)
    )
    return receipt


def _retag_blocker(certificate: dict) -> dict:
    certificate["post_effect_blocker_certificate_digest"] = ""
    certificate["post_effect_blocker_certificate_digest"] = (
        blocker_certificate_digest(certificate)
    )
    return certificate


def _retag_world(world: dict) -> dict:
    from runtime.kuuos_belief_os_types_v0_1 import sha

    world["world_projection_digest"] = ""
    world["world_projection_digest"] = sha(
        {
            key: value
            for key, value in world.items()
            if key != "world_projection_digest"
        }
    )
    return world


def _require_error(receipt: dict, expected: str) -> None:
    errors = validate_licensed_effect_evidence_closure_receipt(_retag(receipt))
    if expected not in errors:
        raise AssertionError({"expected": expected, "errors": errors})


def run_licensed_effect_evidence_closure_scenarios() -> dict:
    with tempfile.TemporaryDirectory(
        prefix="kuuos-licensed-effect-evidence-closure-v18-"
    ) as temporary:
        receipt = build_licensed_effect_evidence_closure_receipt(Path(temporary))
        assert validate_licensed_effect_evidence_closure_receipt(receipt) == []

        source = receipt["source_licensed_handoff_receipt"]
        states = receipt["native_evidence_states"]
        act = states["ActOS"]
        observe = states["ObserveOS"]
        verify = states["VerifyOS"]
        learn = states["LearnOS"]
        next_plan = receipt["next_cycle_artifacts"]["PlanOS"]
        blocker = receipt["post_effect_blocker_certificate"]
        world = receipt["post_effect_world_projection"]

        assert observe["source_act_state_digest"] == act["act_state_digest"]
        assert verify["source_observe_state_digest"] == observe[
            "observe_state_digest"
        ]
        assert learn["source_verify_state_digest"] == verify[
            "verify_state_digest"
        ]
        assert next_plan["next_plan_basis_digest"] == learn[
            "learning_delta_digest"
        ]
        assert observe["observation_debt_discharged"] is True
        assert verify["verification_debt_discharged"] is True
        assert learn["future_only"] is True
        assert learn["active_now"] is False
        assert learn["memory_overwrite"] is False
        assert learn["past_records_unchanged"] is True
        assert receipt["replan_debt_discharged"] is True
        assert receipt["next_act_not_started"] is True
        assert blocker["all_required_blockers_active"] is True
        assert blocker["missing_blockers"] == []
        assert list(blocker["composed_blocker_vector"]) == list(BLOCKER_ORDER)
        assert all(blocker["composed_blocker_vector"].values())
        assert blocker["disposition"] == "BLOCKED_PENDING_NEXT_EXTERNAL_AUTHORITY"
        assert world["projection_read_only"] is True
        assert world["runtime_updates_world"] is False
        assert world["indra_transport_still_unrealized"] is True
        assert source["release_consumption_count"] == 1

        observe_substitution = deepcopy(receipt)
        observe_substitution["native_evidence_states"]["ObserveOS"][
            "source_act_state_digest"
        ] = "substituted-act-state-digest"
        _require_error(
            observe_substitution,
            "closure_observe_source_act_mismatch",
        )

        verify_substitution = deepcopy(receipt)
        verify_substitution["native_evidence_states"]["VerifyOS"][
            "source_observe_state_digest"
        ] = "substituted-observe-state-digest"
        _require_error(
            verify_substitution,
            "closure_verify_source_observe_mismatch",
        )

        learn_substitution = deepcopy(receipt)
        learn_substitution["native_evidence_states"]["LearnOS"][
            "source_verify_state_digest"
        ] = "substituted-verify-state-digest"
        _require_error(
            learn_substitution,
            "closure_learn_source_verify_mismatch",
        )

        plan_basis_substitution = deepcopy(receipt)
        plan_basis_substitution["next_cycle_artifacts"]["PlanOS"][
            "next_plan_basis_digest"
        ] = "substituted-learning-delta-digest"
        _require_error(
            plan_basis_substitution,
            "closure_next_plan_learning_basis_mismatch",
        )

        source_act_substitution = deepcopy(receipt)
        source_act_substitution["native_evidence_states"]["ActOS"][
            "act_state_digest"
        ] = "substituted-source-act-state"
        _require_error(
            source_act_substitution,
            "closure_source_act_state_substitution",
        )

        reopened_observation_debt = deepcopy(receipt)
        reopened_observation_debt["native_evidence_states"]["ObserveOS"][
            "observation_debt_discharged"
        ] = False
        _require_error(
            reopened_observation_debt,
            "closure_observation_debt_open",
        )

        reopened_verification_debt = deepcopy(receipt)
        reopened_verification_debt["native_evidence_states"]["VerifyOS"][
            "verification_debt_discharged"
        ] = False
        _require_error(
            reopened_verification_debt,
            "closure_verification_debt_open",
        )

        present_learning = deepcopy(receipt)
        present_learning["native_evidence_states"]["LearnOS"][
            "future_only"
        ] = False
        _require_error(present_learning, "closure_learning_not_future_only")

        world_update = deepcopy(receipt)
        changed_world = world_update["post_effect_world_projection"]
        changed_world["runtime_updates_world"] = True
        _retag_world(changed_world)
        world_update["post_effect_world_projection_digest"] = changed_world[
            "world_projection_digest"
        ]
        _require_error(world_update, "closure_world_update_claim")

        indra_realization = deepcopy(receipt)
        changed_world = indra_realization["post_effect_world_projection"]
        changed_world["indra_transport_still_unrealized"] = False
        _retag_world(changed_world)
        indra_realization["post_effect_world_projection_digest"] = changed_world[
            "world_projection_digest"
        ]
        _require_error(indra_realization, "closure_indra_transport_realized")

        blocker_loss = deepcopy(receipt)
        changed_blocker = blocker_loss["post_effect_blocker_certificate"]
        changed_blocker["component_vectors"]["world_projection_surface"][
            "world_identity_blocker"
        ] = False
        changed_blocker["composed_blocker_vector"][
            "world_identity_blocker"
        ] = False
        changed_blocker["active_blockers"].remove("world_identity_blocker")
        changed_blocker["missing_blockers"] = ["world_identity_blocker"]
        changed_blocker["all_required_blockers_active"] = False
        changed_blocker["disposition"] = "QUARANTINE_EVIDENCE_CLOSURE_INCOMPLETE"
        _retag_blocker(changed_blocker)
        blocker_loss["post_effect_blocker_certificate_digest"] = changed_blocker[
            "post_effect_blocker_certificate_digest"
        ]
        _require_error(
            blocker_loss,
            "closure_blocker_component_vectors_invalid",
        )

        next_act_started = deepcopy(receipt)
        next_act_started["next_act_not_started"] = False
        _require_error(
            next_act_started,
            "closure_next_act_not_started_invalid",
        )

        source_replay = deepcopy(receipt)
        source_replay["source_licensed_handoff_receipt"][
            "release_consumption_count"
        ] = 2
        _require_error(
            source_replay,
            "closure_source_release_not_single_use",
        )

        truth_escalation = deepcopy(receipt)
        truth_escalation["truth_promoted"] = True
        _require_error(truth_escalation, "closure_truth_promoted_invalid")

        return {
            "status": "KUUOS_QI_WORLD_LICENSED_EFFECT_EVIDENCE_CLOSURE_V1_8_OK",
            "source_licensed_handoff_receipt_digest": source[
                "licensed_act_handoff_receipt_digest"
            ],
            "act_state_digest": act["act_state_digest"],
            "observe_state_digest": observe["observe_state_digest"],
            "verify_state_digest": verify["verify_state_digest"],
            "learn_state_digest": learn["learn_state_digest"],
            "learning_delta_digest": learn["learning_delta_digest"],
            "next_plan_state_digest": next_plan["plan_state_digest"],
            "native_evidence_lineage_digest": receipt[
                "native_evidence_lineage_digest"
            ],
            "post_effect_blocker_certificate_digest": blocker[
                "post_effect_blocker_certificate_digest"
            ],
            "licensed_effect_evidence_closure_receipt_digest": receipt[
                "licensed_effect_evidence_closure_receipt_digest"
            ],
            "observation_debt_discharged": receipt[
                "observation_debt_discharged"
            ],
            "verification_debt_discharged": receipt[
                "verification_debt_discharged"
            ],
            "replan_debt_discharged": receipt["replan_debt_discharged"],
            "next_act_not_started": receipt["next_act_not_started"],
            "all_required_blockers_active": blocker[
                "all_required_blockers_active"
            ],
            "indra_transport_still_unrealized": receipt[
                "indra_transport_still_unrealized"
            ],
            "exact_world_updated": receipt["exact_world_updated"],
        }
