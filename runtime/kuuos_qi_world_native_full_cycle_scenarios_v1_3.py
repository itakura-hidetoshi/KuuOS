from __future__ import annotations

import tempfile
from copy import deepcopy
from pathlib import Path

from runtime.kuuos_act_os_types_v0_1 import state_digest as act_state_digest
from runtime.kuuos_belief_os_gerbe_types_v0_3 import receipt_digest as belief_receipt_digest
from runtime.kuuos_decision_os_plural_types_v0_2 import state_digest as plural_state_digest
from runtime.kuuos_decision_os_types_v0_1 import state_digest as decision_state_digest
from runtime.kuuos_decision_os_wa_types_v0_3 import wa_state_digest
from runtime.kuuos_learn_os_types_v0_1 import state_digest as learn_state_digest
from runtime.kuuos_observe_os_types_v0_1 import state_digest as observe_state_digest
from runtime.kuuos_plan_os_types_v0_1 import plan_state_digest
from runtime.kuuos_qi_world_native_full_cycle_v1_3 import (
    build_native_full_cycle_receipt,
    full_cycle_receipt_digest,
    validate_native_full_cycle_receipt,
)
from runtime.kuuos_qi_world_os_interface_types_v1_0 import interface_receipt_digest
from runtime.kuuos_verify_os_types_v0_1 import state_digest as verify_state_digest


def _retag_artifact(state: dict, field: str, digest_fn) -> None:
    state[field] = ""
    state[field] = digest_fn(state)


def _retag_interface(interface: dict) -> None:
    interface["qi_world_os_interface_receipt_digest"] = ""
    interface["qi_world_os_interface_receipt_digest"] = interface_receipt_digest(interface)


def _retag_receipt(receipt: dict) -> dict:
    receipt["native_full_cycle_receipt_digest"] = ""
    receipt["native_full_cycle_receipt_digest"] = full_cycle_receipt_digest(receipt)
    return receipt


def _require_error(receipt: dict, expected: str) -> None:
    errors = validate_native_full_cycle_receipt(_retag_receipt(receipt))
    if expected not in errors:
        raise AssertionError({"expected": expected, "errors": errors})


def run_native_full_cycle_scenarios() -> dict:
    with tempfile.TemporaryDirectory(prefix="kuuos-native-full-v13-") as temporary:
        receipt = build_native_full_cycle_receipt(Path(temporary))
        assert validate_native_full_cycle_receipt(receipt) == []
        artifacts = receipt["native_artifacts"]
        interface = receipt["qi_world_os_interface_receipt"]

        belief = artifacts["BeliefOSReceipt"]
        decision = artifacts["DecisionOS"]
        plural = artifacts["DecisionOSPlural"]
        wa = artifacts["DecisionOSWa"]
        plan = artifacts["PlanOS"]
        act = artifacts["ActOS"]
        observe = artifacts["ObserveOS"]
        verify = artifacts["VerifyOS"]
        learn = artifacts["LearnOS"]

        assert decision["source_belief_receipt_digest"] == belief[
            "belief_gerbe_receipt_digest"
        ]
        assert plural["source_decision_state_digest"] == decision[
            "decision_state_digest"
        ]
        assert wa["source_plural_state_digest"] == plural["plural_state_digest"]
        assert plan["source_wa_state_digest"] == wa["wa_state_digest"]
        assert act["source_plan_state_digest"] == plan["plan_state_digest"]
        assert observe["source_act_state_digest"] == act["act_state_digest"]
        assert verify["source_observe_state_digest"] == observe[
            "observe_state_digest"
        ]
        assert learn["source_verify_state_digest"] == verify[
            "verify_state_digest"
        ]
        assert interface["os_packets"]["BeliefOS"]["native_artifact"] is True
        assert interface["os_packets"]["DecisionOS"]["native_artifact"] is True
        assert interface["os_packets"]["PlanOS"]["native_artifact"] is True

        belief_substitution = deepcopy(receipt)
        substituted_belief = belief_substitution["native_artifacts"][
            "BeliefOSReceipt"
        ]
        substituted_belief["counterevidence_digests"] = list(
            substituted_belief.get("counterevidence_digests", [])
        ) + ["substituted-counterevidence"]
        substituted_belief["belief_gerbe_receipt_digest"] = ""
        substituted_belief["belief_gerbe_receipt_digest"] = belief_receipt_digest(
            substituted_belief
        )
        _require_error(
            belief_substitution,
            "native_full_cycle_decision_belief_mismatch",
        )

        decision_substitution = deepcopy(receipt)
        decision_substitution["native_artifacts"]["DecisionOS"][
            "source_belief_receipt_digest"
        ] = "substituted-belief-receipt"
        _retag_artifact(
            decision_substitution["native_artifacts"]["DecisionOS"],
            "decision_state_digest",
            decision_state_digest,
        )
        _require_error(
            decision_substitution,
            "native_full_cycle_decision_belief_mismatch",
        )

        plural_substitution = deepcopy(receipt)
        plural_substitution["native_artifacts"]["DecisionOSPlural"][
            "source_decision_state_digest"
        ] = "substituted-decision-state"
        _retag_artifact(
            plural_substitution["native_artifacts"]["DecisionOSPlural"],
            "plural_state_digest",
            plural_state_digest,
        )
        _require_error(
            plural_substitution,
            "native_full_cycle_plural_decision_mismatch",
        )

        wa_substitution = deepcopy(receipt)
        wa_substitution["native_artifacts"]["DecisionOSWa"][
            "source_plural_state_digest"
        ] = "substituted-plural-state"
        _retag_artifact(
            wa_substitution["native_artifacts"]["DecisionOSWa"],
            "wa_state_digest",
            wa_state_digest,
        )
        _require_error(wa_substitution, "native_full_cycle_wa_plural_mismatch")

        plan_substitution = deepcopy(receipt)
        plan_substitution["native_artifacts"]["PlanOS"][
            "source_wa_state_digest"
        ] = "substituted-wa-state"
        _retag_artifact(
            plan_substitution["native_artifacts"]["PlanOS"],
            "plan_state_digest",
            plan_state_digest,
        )
        _require_error(plan_substitution, "native_full_cycle_plan_wa_mismatch")

        act_substitution = deepcopy(receipt)
        act_substitution["native_artifacts"]["ActOS"][
            "source_plan_state_digest"
        ] = "substituted-plan-state"
        _retag_artifact(
            act_substitution["native_artifacts"]["ActOS"],
            "act_state_digest",
            act_state_digest,
        )
        _require_error(act_substitution, "native_full_cycle_act_plan_mismatch")

        observe_substitution = deepcopy(receipt)
        observe_substitution["native_artifacts"]["ObserveOS"][
            "source_act_state_digest"
        ] = "substituted-act-state"
        _retag_artifact(
            observe_substitution["native_artifacts"]["ObserveOS"],
            "observe_state_digest",
            observe_state_digest,
        )
        _require_error(observe_substitution, "native_full_cycle_observe_act_mismatch")

        verify_substitution = deepcopy(receipt)
        verify_substitution["native_artifacts"]["VerifyOS"][
            "source_observe_state_digest"
        ] = "substituted-observe-state"
        _retag_artifact(
            verify_substitution["native_artifacts"]["VerifyOS"],
            "verify_state_digest",
            verify_state_digest,
        )
        _require_error(verify_substitution, "native_full_cycle_verify_observe_mismatch")

        learn_substitution = deepcopy(receipt)
        learn_substitution["native_artifacts"]["LearnOS"][
            "source_verify_state_digest"
        ] = "substituted-verify-state"
        _retag_artifact(
            learn_substitution["native_artifacts"]["LearnOS"],
            "learn_state_digest",
            learn_state_digest,
        )
        _require_error(learn_substitution, "native_full_cycle_learn_verify_mismatch")

        authority_removed = deepcopy(receipt)
        authority_removed["qi_world_os_interface_receipt"]["os_packets"]["ActOS"][
            "external_authority_receipt_digest"
        ] = ""
        _retag_interface(authority_removed["qi_world_os_interface_receipt"])
        errors = validate_native_full_cycle_receipt(_retag_receipt(authority_removed))
        if not any("act_external_authority_receipt_digest_required" in error for error in errors):
            raise AssertionError(errors)

        return {
            "status": "KUUOS_QI_WORLD_NATIVE_FULL_CYCLE_V1_3_OK",
            "lineage_id": decision["lineage_id"],
            "mission_contract_digest": decision["mission_contract_digest"],
            "artifact_count": len(artifacts),
            "interface_packet_count": len(interface["os_packets"]),
            "process_lineage_digest": receipt["process_lineage_digest"],
            "world_projection_digest": receipt["world_projection_digest"],
            "belief_receipt_digest": belief["belief_gerbe_receipt_digest"],
            "decision_state_digest": decision["decision_state_digest"],
            "wa_state_digest": wa["wa_state_digest"],
            "plan_state_digest": plan["plan_state_digest"],
            "act_state_digest": act["act_state_digest"],
            "learn_state_digest": learn["learn_state_digest"],
            "full_cycle_non_authority": receipt["full_cycle_non_authority"],
        }
