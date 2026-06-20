from __future__ import annotations

import tempfile
from copy import deepcopy
from pathlib import Path

from runtime.kuuos_qi_world_concrete_third_licensed_cycle_materialization_public_v2_2 import (
    binding_digest,
    build_concrete_three_cycle_bundle,
    build_third_cycle_binding_receipt,
    bundle_digest,
    closure_digest,
    handoff_digest,
    receipt_digest,
    requirement_digest,
    validate_concrete_three_cycle_bundle,
    validate_third_closed_cycle_receipt,
    validate_third_cycle_authority_requirement,
    validate_third_cycle_binding_receipt,
    validate_third_licensed_act_handoff_receipt,
    validate_third_native_evidence_closure_receipt,
)
from runtime.kuuos_qi_world_licensed_multi_cycle_chain_induction_v2_1 import (
    extension_witness_digest,
    validate_closed_cycle_extension_witness,
)


def _expect(errors: list[str], expected: str) -> None:
    if expected not in errors:
        raise AssertionError({"expected": expected, "errors": errors})


def _retag_requirement(value: dict) -> dict:
    value["third_cycle_authority_requirement_digest"] = ""
    value["third_cycle_authority_requirement_digest"] = requirement_digest(value)
    return value


def _retag_handoff(value: dict) -> dict:
    value["third_licensed_act_handoff_receipt_digest"] = ""
    value["third_licensed_act_handoff_receipt_digest"] = handoff_digest(value)
    return value


def _retag_closure(value: dict) -> dict:
    value["third_native_evidence_closure_receipt_digest"] = ""
    value["third_native_evidence_closure_receipt_digest"] = closure_digest(value)
    return value


def _retag_receipt(value: dict) -> dict:
    value["licensed_cycle_receipt_digest"] = ""
    value["licensed_cycle_receipt_digest"] = receipt_digest(value)
    return value


def _retag_bundle(value: dict) -> dict:
    value["concrete_three_cycle_bundle_digest"] = ""
    value["concrete_three_cycle_bundle_digest"] = bundle_digest(value)
    return value


def _retag_binding(value: dict) -> dict:
    value["third_cycle_binding_receipt_digest"] = ""
    value["third_cycle_binding_receipt_digest"] = binding_digest(value)
    return value


def run_concrete_third_licensed_cycle_materialization_scenarios() -> dict:
    with tempfile.TemporaryDirectory(prefix="kuuos-third-cycle-v22-") as temporary:
        bundle = build_concrete_three_cycle_bundle(Path(temporary))
        assert validate_concrete_three_cycle_bundle(bundle) == []

        base = bundle["source_two_cycle_chain"]
        third = bundle["third_cycle_receipt"]
        closure = third["source_third_closure_receipt"]
        handoff = third["source_third_handoff_receipt"]
        requirement = handoff["third_cycle_authority_requirement"]
        witness = bundle["materialized_extension_witness"]
        chain = bundle["three_cycle_chain"]
        states = closure["native_evidence_states"]
        authority = handoff["external_authority_packet"]
        binding = build_third_cycle_binding_receipt(base, third)

        assert validate_third_cycle_binding_receipt(binding) == []
        assert binding["materialized_extension_witness"] == witness
        assert binding["third_cycle_receipt_digest"] == third[
            "licensed_cycle_receipt_digest"
        ]
        assert handoff["target_act_state"]["effect_recorded"] is True
        assert states["ObserveOS"]["source_act_state_digest"] == states["ActOS"][
            "act_state_digest"
        ]
        assert states["VerifyOS"]["source_observe_state_digest"] == states[
            "ObserveOS"
        ]["observe_state_digest"]
        assert states["LearnOS"]["source_verify_state_digest"] == states[
            "VerifyOS"
        ]["verify_state_digest"]
        assert closure["next_cycle_artifacts"]["PlanOS"][
            "next_plan_basis_digest"
        ] == states["LearnOS"]["learning_delta_digest"]
        assert third["cycle_ordinal"] == 3
        assert third["predecessor_cycle_receipt_digest"] == base["cycle_nodes"][1][
            "closed_cycle_receipt_digest"
        ]
        assert authority["external_authority_packet_digest"] not in base[
            "authority_packet_digests"
        ]
        assert authority["human_approval_receipt_digest"] not in base[
            "human_approval_receipt_digests"
        ]
        assert authority["host_license_digest"] not in base["host_license_digests"]
        assert witness["source_materialization_receipt_digest"] == handoff[
            "third_licensed_act_handoff_receipt_digest"
        ]
        assert witness["source_native_closure_receipt_digest"] == closure[
            "third_native_evidence_closure_receipt_digest"
        ]
        assert chain["cycle_count"] == 3
        assert chain["cycle_ordinals"] == [1, 2, 3]
        assert chain["cycle_nodes"][:2] == base["cycle_nodes"]
        assert chain["next_act_started"] is False

        wrong_target = deepcopy(requirement)
        wrong_target["target_cycle_ordinal"] = 4
        _expect(
            validate_third_cycle_authority_requirement(
                _retag_requirement(wrong_target), base_chain=base
            ),
            "requirement_target_ordinal_invalid",
        )

        consumed_source = deepcopy(handoff)
        consumed_source["source_receipt_consumed"] = True
        _expect(
            validate_third_licensed_act_handoff_receipt(
                _retag_handoff(consumed_source)
            ),
            "handoff_source_receipt_consumed_invalid",
        )

        inherited_authority = deepcopy(handoff)
        inherited_authority["predecessor_authority_inherited"] = True
        _expect(
            validate_third_licensed_act_handoff_receipt(
                _retag_handoff(inherited_authority)
            ),
            "handoff_predecessor_authority_inherited_invalid",
        )

        closure_activation = deepcopy(closure)
        closure_activation["next_act_not_started"] = False
        _expect(
            validate_third_native_evidence_closure_receipt(
                _retag_closure(closure_activation)
            ),
            "closure_next_act_not_started_invalid",
        )

        world_mutation = deepcopy(closure)
        world_mutation["post_effect_world_projection"]["runtime_updates_world"] = True
        world_mutation["post_effect_world_projection"]["world_projection_digest"] = ""
        _expect(
            validate_third_native_evidence_closure_receipt(
                _retag_closure(world_mutation)
            ),
            "closure_world_digest_invalid",
        )

        replay = deepcopy(third)
        replay["receipt_consumption_count"] = 1
        _expect(
            validate_third_closed_cycle_receipt(_retag_receipt(replay)),
            "receipt_consumption_forbidden",
        )

        renewable = deepcopy(third)
        renewable["consumed_authority_renewable"] = True
        _expect(
            validate_third_closed_cycle_receipt(_retag_receipt(renewable)),
            "receipt_consumed_authority_renewable_invalid",
        )

        reused_witness = deepcopy(witness)
        reused_witness["fresh_external_authority_packet_digest"] = base[
            "authority_packet_digests"
        ][0]
        reused_witness["extension_witness_digest"] = ""
        reused_witness["extension_witness_digest"] = extension_witness_digest(
            reused_witness
        )
        _expect(
            validate_closed_cycle_extension_witness(
                reused_witness, source_chain=base
            ),
            "witness_authority_reuse",
        )

        closure_binding_tamper = deepcopy(binding)
        closure_binding_tamper["source_native_closure_receipt_digest"] = "0" * 64
        _expect(
            validate_third_cycle_binding_receipt(
                _retag_binding(closure_binding_tamper)
            ),
            "binding_native_closure_digest_mismatch",
        )

        authority_binding_tamper = deepcopy(binding)
        authority_binding_tamper["fresh_external_authority_packet_digest"] = (
            base["authority_packet_digests"][0]
        )
        _expect(
            validate_third_cycle_binding_receipt(
                _retag_binding(authority_binding_tamper)
            ),
            "binding_authority_digest_mismatch",
        )

        binding_escalation = deepcopy(binding)
        binding_escalation["non_authority"][
            "binding_is_execution_capability"
        ] = True
        _expect(
            validate_third_cycle_binding_receipt(
                _retag_binding(binding_escalation)
            ),
            "binding_non_authority_invalid",
        )

        bundle_escalation = deepcopy(bundle)
        bundle_escalation["non_authority"]["bundle_is_execution_capability"] = True
        _expect(
            validate_concrete_three_cycle_bundle(
                _retag_bundle(bundle_escalation)
            ),
            "bundle_non_authority_invalid",
        )

        return {
            "status": "KUUOS_QI_WORLD_CONCRETE_THIRD_LICENSED_CYCLE_MATERIALIZATION_V2_2_OK",
            "base_chain_digest": base["inductive_chain_digest"],
            "third_handoff_receipt_digest": handoff[
                "third_licensed_act_handoff_receipt_digest"
            ],
            "third_closure_receipt_digest": closure[
                "third_native_evidence_closure_receipt_digest"
            ],
            "third_cycle_receipt_digest": third[
                "licensed_cycle_receipt_digest"
            ],
            "third_cycle_binding_receipt_digest": binding[
                "third_cycle_binding_receipt_digest"
            ],
            "materialized_extension_witness_digest": witness[
                "extension_witness_digest"
            ],
            "three_cycle_chain_digest": chain["inductive_chain_digest"],
            "bundle_digest": bundle["concrete_three_cycle_bundle_digest"],
            "cycle_count": chain["cycle_count"],
            "third_act_effect_recorded": bundle[
                "third_act_effect_recorded"
            ],
            "third_native_closure_completed": bundle[
                "third_native_closure_completed"
            ],
            "v2_1_induction_witness_realized": bundle[
                "v2_1_induction_witness_realized"
            ],
            "all_cycles_closed": bundle["all_cycles_closed"],
            "all_blockers_active": bundle["all_blockers_active"],
            "next_act_started": bundle["next_act_started"],
        }
