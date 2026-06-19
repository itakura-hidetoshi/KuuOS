from __future__ import annotations

import tempfile
from copy import deepcopy
from pathlib import Path

from runtime.kuuos_act_os_types_v0_1 import state_digest as act_state_digest
from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_decision_os_plural_types_v0_2 import state_digest as plural_state_digest
from runtime.kuuos_decision_os_types_v0_1 import state_digest as decision_state_digest
from runtime.kuuos_decision_os_wa_types_v0_3 import wa_state_digest
from runtime.kuuos_learn_os_types_v0_1 import state_digest as learn_state_digest
from runtime.kuuos_plan_os_types_v0_1 import plan_state_digest
from runtime.kuuos_qi_world_native_full_cycle_v1_3 import (
    build_native_full_cycle_receipt,
    full_cycle_receipt_digest,
    validate_native_full_cycle_receipt,
)
from runtime.kuuos_qi_world_os_interface_types_v1_0 import interface_receipt_digest


def _retag_state(state: dict, field: str, digest_fn) -> None:
    state[field] = ""
    state[field] = digest_fn(state)


def _retag_interface(interface: dict) -> None:
    interface["qi_world_os_interface_receipt_digest"] = ""
    interface["qi_world_os_interface_receipt_digest"] = interface_receipt_digest(
        interface
    )


def _retag_receipt(receipt: dict) -> dict:
    receipt["full_cycle_receipt_digest"] = ""
    receipt["full_cycle_receipt_digest"] = full_cycle_receipt_digest(receipt)
    return receipt


def _require_error(receipt: dict, expected: str) -> None:
    errors = validate_native_full_cycle_receipt(_retag_receipt(receipt))
    if expected not in errors:
        raise AssertionError({"expected": expected, "errors": errors})


def run_native_full_cycle_scenarios() -> dict:
    with tempfile.TemporaryDirectory(prefix="kuuos-native-full-cycle-v13-") as temporary:
        receipt = build_native_full_cycle_receipt(Path(temporary))
        assert validate_native_full_cycle_receipt(receipt) == []
        artifacts = receipt["native_artifacts"]
        interface = receipt["qi_world_os_interface_receipt"]

        assert artifacts["DecisionOS"]["source_belief_receipt_digest"] == artifacts[
            "BeliefOS"
        ]["belief_gerbe_receipt_digest"]
        assert artifacts["DecisionOSPlural"]["source_decision_state_digest"] == artifacts[
            "DecisionOS"
        ]["decision_state_digest"]
        assert artifacts["DecisionOSWa"]["source_plural_state_digest"] == artifacts[
            "DecisionOSPlural"
        ]["plural_state_digest"]
        assert artifacts["PlanOS"]["source_wa_state_digest"] == artifacts[
            "DecisionOSWa"
        ]["wa_state_digest"]
        assert artifacts["ActOS"]["source_plan_state_digest"] == artifacts[
            "PlanOS"
        ]["plan_state_digest"]
        assert artifacts["ObserveOS"]["source_act_state_digest"] == artifacts[
            "ActOS"
        ]["act_state_digest"]
        assert artifacts["VerifyOS"]["source_observe_state_digest"] == artifacts[
            "ObserveOS"
        ]["observe_state_digest"]
        assert artifacts["LearnOS"]["source_verify_state_digest"] == artifacts[
            "VerifyOS"
        ]["verify_state_digest"]
        assert all(
            packet.get("native_artifact") is True
            for name, packet in interface["os_packets"].items()
            if name != "Governance"
        )

        decision_substitution = deepcopy(receipt)
        decision_substitution["native_artifacts"]["DecisionOS"][
            "source_belief_receipt_digest"
        ] = sha("substituted-belief-receipt")
        _retag_state(
            decision_substitution["native_artifacts"]["DecisionOS"],
            "decision_state_digest",
            decision_state_digest,
        )
        _require_error(
            decision_substitution,
            "upstream:native_decision_source_belief_mismatch",
        )

        plural_substitution = deepcopy(receipt)
        plural_substitution["native_artifacts"]["DecisionOSPlural"][
            "source_decision_state_digest"
        ] = sha("substituted-decision-state")
        _retag_state(
            plural_substitution["native_artifacts"]["DecisionOSPlural"],
            "plural_state_digest",
            plural_state_digest,
        )
        _require_error(
            plural_substitution,
            "upstream:native_plural_source_decision_mismatch",
        )

        wa_substitution = deepcopy(receipt)
        wa_substitution["native_artifacts"]["DecisionOSWa"][
            "source_plural_state_digest"
        ] = sha("substituted-plural-state")
        _retag_state(
            wa_substitution["native_artifacts"]["DecisionOSWa"],
            "wa_state_digest",
            wa_state_digest,
        )
        _require_error(
            wa_substitution,
            "upstream:native_wa_source_plural_mismatch",
        )

        plan_substitution = deepcopy(receipt)
        plan_substitution["native_artifacts"]["PlanOS"][
            "source_wa_state_digest"
        ] = sha("substituted-wa-state")
        _retag_state(
            plan_substitution["native_artifacts"]["PlanOS"],
            "plan_state_digest",
            plan_state_digest,
        )
        _require_error(
            plan_substitution,
            "upstream:native_plan_source_wa_mismatch",
        )

        act_substitution = deepcopy(receipt)
        act_substitution["native_artifacts"]["ActOS"][
            "source_plan_state_digest"
        ] = sha("substituted-plan-state")
        _retag_state(
            act_substitution["native_artifacts"]["ActOS"],
            "act_state_digest",
            act_state_digest,
        )
        _require_error(
            act_substitution,
            "native_full_cycle_act_source_plan_mismatch",
        )

        past_mutation = deepcopy(receipt)
        past_mutation["native_artifacts"]["LearnOS"][
            "past_records_unchanged"
        ] = False
        _retag_state(
            past_mutation["native_artifacts"]["LearnOS"],
            "learn_state_digest",
            learn_state_digest,
        )
        errors = validate_native_full_cycle_receipt(_retag_receipt(past_mutation))
        if not any("learn_past_record_mutation_forbidden" in error for error in errors):
            raise AssertionError(errors)

        authority_removed = deepcopy(receipt)
        authority_removed["qi_world_os_interface_receipt"]["os_packets"]["ActOS"][
            "external_authority_receipt_digest"
        ] = ""
        _retag_interface(authority_removed["qi_world_os_interface_receipt"])
        errors = validate_native_full_cycle_receipt(_retag_receipt(authority_removed))
        if not any("act_external_authority_receipt_digest_required" in error for error in errors):
            raise AssertionError(errors)

        world_mutation = deepcopy(receipt)
        world_mutation["qi_world_os_interface_receipt"]["world_projection"][
            "runtime_updates_world"
        ] = True
        _retag_interface(world_mutation["qi_world_os_interface_receipt"])
        _require_error(
            world_mutation,
            "interface:world_projection_runtime_updates_world_invalid",
        )

        return {
            "status": "KUUOS_QI_WORLD_NATIVE_FULL_CYCLE_V1_3_OK",
            "cycle_id": receipt["cycle_id"],
            "lineage_id": receipt["lineage_id"],
            "native_artifact_count": len(artifacts),
            "os_packet_count": len(interface["os_packets"]),
            "process_lineage_digest": receipt["process_lineage_digest"],
            "world_projection_digest": receipt["world_projection_digest"],
            "full_cycle_non_authority": receipt["full_cycle_non_authority"],
        }
