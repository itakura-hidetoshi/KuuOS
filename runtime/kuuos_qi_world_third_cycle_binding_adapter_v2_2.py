from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime import kuuos_qi_world_concrete_third_licensed_cycle_materialization_v2_2 as _core
from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_qi_world_licensed_multi_cycle_chain_induction_v2_1 import (
    validate_closed_cycle_extension_witness,
    validate_inductive_licensed_cycle_chain,
)

VERSION = "kuuos_qi_world_third_cycle_binding_adapter_v2_2"
BINDING_NON_AUTHORITY = {
    "binding_is_execution_capability": False,
    "binding_issues_authority": False,
    "binding_starts_next_act": False,
    "binding_updates_exact_world": False,
    "binding_overwrites_history": False,
    "binding_promotes_truth": False,
}


def _digest_without(value: Mapping[str, Any], field: str) -> str:
    packet = deepcopy(dict(value))
    packet.pop(field, None)
    return sha(packet)


def binding_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "third_cycle_binding_receipt_digest")


def build_third_cycle_binding_receipt(
    base_chain: Mapping[str, Any],
    third_receipt: Mapping[str, Any],
) -> dict[str, Any]:
    source_errors = validate_inductive_licensed_cycle_chain(base_chain)
    source_errors += _core.validate_third_closed_cycle_receipt(third_receipt)
    if source_errors:
        raise ValueError("binding_source_invalid:" + ";".join(source_errors))

    witness = _core.build_materialized_third_cycle_extension_witness(
        base_chain, third_receipt
    )
    handoff = dict(third_receipt["source_third_handoff_receipt"])
    closure = dict(third_receipt["source_third_closure_receipt"])
    authority = dict(handoff["external_authority_packet"])

    binding = {
        "version": VERSION,
        "source_two_cycle_chain": deepcopy(dict(base_chain)),
        "source_two_cycle_chain_digest": base_chain["inductive_chain_digest"],
        "source_cycle_count": base_chain["cycle_count"],
        "target_cycle_ordinal": third_receipt["cycle_ordinal"],
        "predecessor_cycle_receipt_digest": third_receipt[
            "predecessor_cycle_receipt_digest"
        ],
        "third_cycle_receipt": deepcopy(dict(third_receipt)),
        "third_cycle_receipt_digest": third_receipt[
            "licensed_cycle_receipt_digest"
        ],
        "source_materialization_receipt_digest": handoff[
            "third_licensed_act_handoff_receipt_digest"
        ],
        "source_native_closure_receipt_digest": closure[
            "third_native_evidence_closure_receipt_digest"
        ],
        "source_blocker_certificate_digest": closure[
            "post_effect_blocker_certificate_digest"
        ],
        "source_world_projection_digest": closure[
            "post_effect_world_projection_digest"
        ],
        "fresh_external_authority_packet_digest": authority[
            "external_authority_packet_digest"
        ],
        "new_human_approval_receipt_digest": authority[
            "human_approval_receipt_digest"
        ],
        "new_host_license_digest": authority["host_license_digest"],
        "materialized_extension_witness": deepcopy(witness),
        "materialized_extension_witness_digest": witness[
            "extension_witness_digest"
        ],
        "immediate_successor_exact": True,
        "predecessor_binding_exact": True,
        "materialization_binding_exact": True,
        "native_closure_binding_exact": True,
        "blocker_binding_exact": True,
        "world_projection_binding_exact": True,
        "authority_binding_exact": True,
        "closed_receipt_binding_exact": True,
        "source_prefix_read_only": True,
        "binding_receipt_immutable": True,
        "binding_receipt_append_only": True,
        "next_act_started": False,
        "non_authority": deepcopy(BINDING_NON_AUTHORITY),
        "third_cycle_binding_receipt_digest": "",
    }
    binding["third_cycle_binding_receipt_digest"] = binding_digest(binding)
    errors = validate_third_cycle_binding_receipt(binding)
    if errors:
        raise ValueError("third_cycle_binding_invalid:" + ";".join(errors))
    return binding


def validate_third_cycle_binding_receipt(
    binding: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []

    def req(ok: bool, code: str) -> None:
        if not ok:
            errors.append(code)

    try:
        req(binding.get("version") == VERSION, "binding_version_invalid")
        req(
            binding.get("third_cycle_binding_receipt_digest")
            == binding_digest(binding),
            "binding_digest_invalid",
        )

        base = dict(binding.get("source_two_cycle_chain", {}))
        errors += [
            "binding_base_" + error
            for error in validate_inductive_licensed_cycle_chain(base)
        ]
        third = dict(binding.get("third_cycle_receipt", {}))
        errors += [
            "binding_third_" + error
            for error in _core.validate_third_closed_cycle_receipt(third)
        ]
        witness = dict(binding.get("materialized_extension_witness", {}))
        errors += [
            "binding_witness_" + error
            for error in validate_closed_cycle_extension_witness(
                witness, source_chain=base
            )
        ]

        expected_witness = _core.build_materialized_third_cycle_extension_witness(
            base, third
        )
        req(witness == expected_witness, "binding_witness_substitution")

        handoff = dict(third.get("source_third_handoff_receipt", {}))
        closure = dict(third.get("source_third_closure_receipt", {}))
        authority = dict(handoff.get("external_authority_packet", {}))

        req(base.get("cycle_count") == 2, "binding_source_cycle_count_invalid")
        req(binding.get("source_cycle_count") == 2, "binding_cycle_count_invalid")
        req(binding.get("target_cycle_ordinal") == 3, "binding_target_ordinal_invalid")
        req(
            binding.get("target_cycle_ordinal") == base.get("cycle_count", 0) + 1,
            "binding_not_immediate_successor",
        )
        req(
            binding.get("source_two_cycle_chain_digest")
            == base.get("inductive_chain_digest"),
            "binding_source_chain_digest_mismatch",
        )
        req(
            binding.get("predecessor_cycle_receipt_digest")
            == third.get("predecessor_cycle_receipt_digest")
            == witness.get("predecessor_cycle_receipt_digest"),
            "binding_predecessor_digest_mismatch",
        )
        req(
            binding.get("third_cycle_receipt_digest")
            == third.get("licensed_cycle_receipt_digest")
            == witness.get("closed_cycle_receipt_digest"),
            "binding_closed_receipt_digest_mismatch",
        )
        req(
            binding.get("source_materialization_receipt_digest")
            == handoff.get("third_licensed_act_handoff_receipt_digest")
            == witness.get("source_materialization_receipt_digest"),
            "binding_materialization_digest_mismatch",
        )
        req(
            binding.get("source_native_closure_receipt_digest")
            == closure.get("third_native_evidence_closure_receipt_digest")
            == witness.get("source_native_closure_receipt_digest"),
            "binding_native_closure_digest_mismatch",
        )
        req(
            binding.get("source_blocker_certificate_digest")
            == closure.get("post_effect_blocker_certificate_digest")
            == witness.get("source_blocker_certificate_digest"),
            "binding_blocker_digest_mismatch",
        )
        req(
            binding.get("source_world_projection_digest")
            == closure.get("post_effect_world_projection_digest")
            == witness.get("source_world_projection_digest"),
            "binding_world_projection_digest_mismatch",
        )
        req(
            binding.get("fresh_external_authority_packet_digest")
            == authority.get("external_authority_packet_digest")
            == witness.get("fresh_external_authority_packet_digest"),
            "binding_authority_digest_mismatch",
        )
        req(
            binding.get("new_human_approval_receipt_digest")
            == authority.get("human_approval_receipt_digest")
            == witness.get("new_human_approval_receipt_digest"),
            "binding_approval_digest_mismatch",
        )
        req(
            binding.get("new_host_license_digest")
            == authority.get("host_license_digest")
            == witness.get("new_host_license_digest"),
            "binding_host_license_digest_mismatch",
        )
        req(
            binding.get("materialized_extension_witness_digest")
            == witness.get("extension_witness_digest"),
            "binding_witness_digest_mismatch",
        )

        expected = {
            "immediate_successor_exact": True,
            "predecessor_binding_exact": True,
            "materialization_binding_exact": True,
            "native_closure_binding_exact": True,
            "blocker_binding_exact": True,
            "world_projection_binding_exact": True,
            "authority_binding_exact": True,
            "closed_receipt_binding_exact": True,
            "source_prefix_read_only": True,
            "binding_receipt_immutable": True,
            "binding_receipt_append_only": True,
            "next_act_started": False,
        }
        for field, value in expected.items():
            req(binding.get(field) == value, f"binding_{field}_invalid")
        req(
            dict(binding.get("non_authority", {})) == BINDING_NON_AUTHORITY,
            "binding_non_authority_invalid",
        )
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_bound_materialized_extension_witness(
    base_chain: Mapping[str, Any],
    third_receipt: Mapping[str, Any],
) -> dict[str, Any]:
    binding = build_third_cycle_binding_receipt(base_chain, third_receipt)
    return deepcopy(dict(binding["materialized_extension_witness"]))


__all__ = [
    "BINDING_NON_AUTHORITY",
    "VERSION",
    "binding_digest",
    "build_bound_materialized_extension_witness",
    "build_third_cycle_binding_receipt",
    "validate_third_cycle_binding_receipt",
]
