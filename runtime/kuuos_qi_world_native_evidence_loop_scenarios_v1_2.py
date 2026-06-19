from __future__ import annotations

import tempfile
from copy import deepcopy
from pathlib import Path

from runtime.kuuos_act_os_types_v0_1 import state_digest as act_state_digest
from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_learn_os_types_v0_1 import state_digest as learn_state_digest
from runtime.kuuos_observe_os_types_v0_1 import state_digest as observe_state_digest
from runtime.kuuos_qi_world_native_evidence_loop_v1_2 import (
    build_native_evidence_loop_receipt,
    native_loop_receipt_digest,
    validate_native_evidence_loop_receipt,
)
from runtime.kuuos_qi_world_os_interface_types_v1_0 import (
    interface_receipt_digest,
)
from runtime.kuuos_verify_os_types_v0_1 import state_digest as verify_state_digest


def _retag_native_state(state: dict, field: str, digest_fn) -> None:
    state[field] = ""
    state[field] = digest_fn(state)


def _retag_interface(interface: dict) -> None:
    interface["qi_world_os_interface_receipt_digest"] = ""
    interface["qi_world_os_interface_receipt_digest"] = interface_receipt_digest(
        interface
    )


def _retag_receipt(receipt: dict) -> dict:
    receipt["native_loop_receipt_digest"] = ""
    receipt["native_loop_receipt_digest"] = native_loop_receipt_digest(receipt)
    return receipt


def _require_error(receipt: dict, expected: str) -> None:
    errors = validate_native_evidence_loop_receipt(_retag_receipt(receipt))
    if expected not in errors:
        raise AssertionError({"expected": expected, "errors": errors})


def run_native_evidence_loop_scenarios() -> dict:
    with tempfile.TemporaryDirectory(prefix="kuuos-qi-world-native-v12-") as temporary:
        receipt = build_native_evidence_loop_receipt(Path(temporary))
        assert validate_native_evidence_loop_receipt(receipt) == []
        states = receipt["native_states"]
        interface = receipt["qi_world_os_interface_receipt"]

        assert states["ObserveOS"]["source_act_state_digest"] == states["ActOS"][
            "act_state_digest"
        ]
        assert states["VerifyOS"]["source_observe_state_digest"] == states[
            "ObserveOS"
        ]["observe_state_digest"]
        assert states["LearnOS"]["source_verify_state_digest"] == states[
            "VerifyOS"
        ]["verify_state_digest"]
        assert states["LearnOS"]["source_act_state_digest"] == states["ActOS"][
            "act_state_digest"
        ]
        assert interface["os_packets"]["ObserveOS"]["output_digest"] == states[
            "ObserveOS"
        ]["evidence_packet_digest"]
        assert interface["os_packets"]["VerifyOS"]["output_digest"] == states[
            "VerifyOS"
        ]["verification_evidence_digest"]
        assert interface["os_packets"]["LearnOS"]["output_digest"] == states[
            "LearnOS"
        ]["learning_delta_digest"]

        effect_removed = deepcopy(receipt)
        effect_removed["native_states"]["ActOS"]["effect_recorded"] = False
        _retag_native_state(
            effect_removed["native_states"]["ActOS"],
            "act_state_digest",
            act_state_digest,
        )
        _require_error(effect_removed, "native_loop_act_effect_missing")

        observe_substitution = deepcopy(receipt)
        observe_substitution["native_states"]["ObserveOS"][
            "source_act_state_digest"
        ] = sha("substituted-act-state")
        _retag_native_state(
            observe_substitution["native_states"]["ObserveOS"],
            "observe_state_digest",
            observe_state_digest,
        )
        _require_error(
            observe_substitution,
            "native_loop_observe_source_act_mismatch",
        )

        verify_substitution = deepcopy(receipt)
        verify_substitution["native_states"]["VerifyOS"][
            "source_observe_state_digest"
        ] = sha("substituted-observe-state")
        _retag_native_state(
            verify_substitution["native_states"]["VerifyOS"],
            "verify_state_digest",
            verify_state_digest,
        )
        _require_error(
            verify_substitution,
            "native_loop_verify_source_observe_mismatch",
        )

        learn_substitution = deepcopy(receipt)
        learn_substitution["native_states"]["LearnOS"][
            "source_verify_state_digest"
        ] = sha("substituted-verify-state")
        _retag_native_state(
            learn_substitution["native_states"]["LearnOS"],
            "learn_state_digest",
            learn_state_digest,
        )
        _require_error(
            learn_substitution,
            "native_loop_learn_source_verify_mismatch",
        )

        past_mutation = deepcopy(receipt)
        past_mutation["native_states"]["LearnOS"][
            "past_records_unchanged"
        ] = False
        _retag_native_state(
            past_mutation["native_states"]["LearnOS"],
            "learn_state_digest",
            learn_state_digest,
        )
        errors = validate_native_evidence_loop_receipt(
            _retag_receipt(past_mutation)
        )
        if not any("learn_past_record_mutation_forbidden" in error for error in errors):
            raise AssertionError(errors)

        authority_removed = deepcopy(receipt)
        authority_removed["qi_world_os_interface_receipt"]["os_packets"][
            "ActOS"
        ]["external_authority_receipt_digest"] = ""
        _retag_interface(authority_removed["qi_world_os_interface_receipt"])
        errors = validate_native_evidence_loop_receipt(
            _retag_receipt(authority_removed)
        )
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
            "status": "KUUOS_QI_WORLD_NATIVE_EVIDENCE_LOOP_V1_2_OK",
            "lineage_id": states["ActOS"]["lineage_id"],
            "process_lineage_digest": receipt["process_lineage_digest"],
            "world_projection_digest": receipt["world_projection_digest"],
            "native_state_count": len(states),
            "interface_packet_count": len(interface["os_packets"]),
            "act_state_digest": states["ActOS"]["act_state_digest"],
            "observe_state_digest": states["ObserveOS"]["observe_state_digest"],
            "verify_state_digest": states["VerifyOS"]["verify_state_digest"],
            "learn_state_digest": states["LearnOS"]["learn_state_digest"],
            "native_non_authority": receipt["native_non_authority"],
        }
