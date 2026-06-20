from __future__ import annotations

import tempfile
from copy import deepcopy
from pathlib import Path

from runtime.kuuos_qi_world_licensed_effect_evidence_closure_public_v1_8 import (
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


def _require_error(receipt: dict, expected: str) -> None:
    errors = validate_licensed_effect_evidence_closure_receipt(_retag(receipt))
    if expected not in errors:
        raise AssertionError({"expected": expected, "errors": errors})


def run_licensed_effect_evidence_closure_scenarios() -> dict:
    with tempfile.TemporaryDirectory(
        prefix="kuuos-licensed-effect-evidence-closure-v18-public-"
    ) as temporary:
        receipt = build_licensed_effect_evidence_closure_receipt(Path(temporary))
        assert validate_licensed_effect_evidence_closure_receipt(receipt) == []

        source = receipt["source_licensed_handoff_receipt"]
        states = receipt["native_evidence_states"]
        act = states["ActOS"]
        observe = states["ObserveOS"]
        verify = states["VerifyOS"]
        learn = states["LearnOS"]
        delta = learn["learning_delta"]
        plan = receipt["next_cycle_artifacts"]["PlanOS"]
        blocker = receipt["post_effect_blocker_certificate"]
        world = receipt["post_effect_world_projection"]

        assert observe["source_act_state_digest"] == act["act_state_digest"]
        assert verify["source_observe_state_digest"] == observe[
            "observe_state_digest"
        ]
        assert learn["source_verify_state_digest"] == verify[
            "verify_state_digest"
        ]
        assert plan["next_plan_basis_digest"] == learn["learning_delta_digest"]
        assert delta["future_only"] is True
        assert delta["memory_overwrite"] is False
        assert delta["active_now"] is False
        assert delta["activation_requires_replan"] is True
        assert learn["learning_debt_discharged"] is True
        assert learn["replan_required"] is True
        assert learn["past_records_unchanged"] is True
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
        _require_error(observe_substitution, "closure_observe_source_act_mismatch")

        verify_substitution = deepcopy(receipt)
        verify_substitution["native_evidence_states"]["VerifyOS"][
            "source_observe_state_digest"
        ] = "substituted-observe-state-digest"
        _require_error(verify_substitution, "closure_verify_source_observe_mismatch")

        learn_substitution = deepcopy(receipt)
        learn_substitution["native_evidence_states"]["LearnOS"][
            "source_verify_state_digest"
        ] = "substituted-verify-state-digest"
        _require_error(learn_substitution, "closure_learn_source_verify_mismatch")

        future_only_loss = deepcopy(receipt)
        changed_delta = future_only_loss["native_evidence_states"]["LearnOS"][
            "learning_delta"
        ]
        changed_delta["future_only"] = False
        _require_error(
            future_only_loss,
            "closure_learning_delta_not_future_only",
        )

        overwrite_forgery = deepcopy(receipt)
        changed_delta = overwrite_forgery["native_evidence_states"]["LearnOS"][
            "learning_delta"
        ]
        changed_delta["memory_overwrite"] = True
        _require_error(
            overwrite_forgery,
            "closure_learning_delta_memory_overwrite",
        )

        plan_basis_substitution = deepcopy(receipt)
        plan_basis_substitution["next_cycle_artifacts"]["PlanOS"][
            "next_plan_basis_digest"
        ] = "substituted-learning-delta-digest"
        _require_error(
            plan_basis_substitution,
            "closure_next_plan_learning_basis_mismatch",
        )

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
        _require_error(blocker_loss, "closure_blocker_component_vectors_invalid")

        next_act_started = deepcopy(receipt)
        next_act_started["next_act_not_started"] = False
        _require_error(next_act_started, "closure_next_act_not_started_invalid")

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
            "next_plan_state_digest": plan["plan_state_digest"],
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
