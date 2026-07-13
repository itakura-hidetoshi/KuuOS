from __future__ import annotations

from collections import defaultdict

from runtime.kuuos_planos_finite_physical_quantum_qi_coherence_kernel_partial_dephasing_algebra_support_v0_1 import (
    compile_histories,
    exact_partial_dephasing_observables,
)
from runtime.kuuos_planos_finite_physical_quantum_qi_coherence_kernel_partial_dephasing_schema_support_v0_1 import (
    compute_partial_dephasing_input_digest,
    normalize_claims,
    normalize_dephasing_numerators,
    normalize_histories,
)


SCHEMA_VERSION = (
    "kuuos.planos.finite-physical-quantum-qi-coherence-kernel-"
    "partial-dephasing-certificate.v0.1"
)

MAXIMUM_HISTORY_COUNT = 128
MAXIMUM_WEIGHT_NUMERATOR = 100_000
MAXIMUM_DEPHASING_DENOMINATOR = 10_000
MAXIMUM_DEPHASING_STEP_COUNT = 64


def _nonempty_text(value) -> bool:
    return isinstance(value, str) and bool(value)


def _positive_nat(value) -> bool:
    return (
        isinstance(value, int)
        and not isinstance(value, bool)
        and value > 0
    )


def _expected_claims(input_digest: str, observables: dict) -> dict:
    return {
        "input_digest": input_digest,
        **observables,
        "all_histories_retained": True,
        "homotopy_partition_exact": True,
        "exact_rational_partial_dephasing": True,
        "convex_gram_witness_used": True,
        "argmin_performed": False,
        "representative_history_selected": False,
        "history_ranking_performed": False,
        "history_pruning_performed": False,
        "activation_performed": False,
        "execution_permission": False,
        "source_v122_certificate_mutated": False,
        "persistent_world_state_mutated": False,
    }


def _partition_blockers(histories: list[dict]) -> list[str]:
    blockers: list[str] = []
    class_to_blocks: dict[str, set[str]] = defaultdict(set)
    block_to_classes: dict[str, set[str]] = defaultdict(set)
    for history in histories:
        class_to_blocks[history["homotopy_class_id"]].add(
            history["coherence_block_id"]
        )
        block_to_classes[history["coherence_block_id"]].add(
            history["homotopy_class_id"]
        )
    for class_id, block_ids in sorted(class_to_blocks.items()):
        if len(block_ids) != 1:
            blockers.append(
                "homotopy_class_spans_multiple_coherence_blocks_" + class_id
            )
    for block_id, class_ids in sorted(block_to_classes.items()):
        if len(class_ids) != 1:
            blockers.append(
                "coherence_block_mixes_homotopy_classes_" + block_id
            )
    if len(class_to_blocks) != len(block_to_classes):
        blockers.append("homotopy_coherence_block_cardinality_mismatch")
    return blockers


def issue_finite_physical_quantum_qi_coherence_kernel_partial_dephasing_certificate(
    payload,
):
    top_fields = {
        "schema_version",
        "source_v122_certificate_digest",
        "source_physical_quantum_qi_definition_digest",
        "weight_denominator",
        "dephasing_denominator",
        "dephasing_numerators",
        "histories",
        "claims",
    }
    blockers: list[str] = []

    if not isinstance(payload, dict) or set(payload) != top_fields:
        return {
            "schema_version": SCHEMA_VERSION,
            "accepted": False,
            "blockers": ["top_level_schema_invalid"],
        }

    if payload["schema_version"] != SCHEMA_VERSION:
        blockers.append("schema_version_mismatch")

    for field in (
        "source_v122_certificate_digest",
        "source_physical_quantum_qi_definition_digest",
    ):
        if not _nonempty_text(payload[field]):
            blockers.append(field + "_missing")

    weight_denominator = payload["weight_denominator"]
    if not _positive_nat(weight_denominator):
        blockers.append("weight_denominator_invalid")
        weight_denominator = 1

    dephasing_denominator = payload["dephasing_denominator"]
    if (
        not _positive_nat(dephasing_denominator)
        or dephasing_denominator > MAXIMUM_DEPHASING_DENOMINATOR
    ):
        blockers.append("dephasing_denominator_invalid")
        dephasing_denominator = 1

    history_errors, histories = normalize_histories(
        payload["histories"],
        maximum_history_count=MAXIMUM_HISTORY_COUNT,
        maximum_weight_numerator=MAXIMUM_WEIGHT_NUMERATOR,
    )
    dephasing_errors, dephasing_numerators = normalize_dephasing_numerators(
        payload["dephasing_numerators"],
        denominator=dephasing_denominator,
        maximum_step_count=MAXIMUM_DEPHASING_STEP_COUNT,
    )
    claim_errors, claims = normalize_claims(payload["claims"])
    blockers.extend(history_errors)
    blockers.extend(dephasing_errors)
    blockers.extend(claim_errors)

    if (
        sum(item["weight_numerator"] for item in histories)
        != weight_denominator
    ):
        blockers.append("history_weights_do_not_sum_to_denominator")

    blockers.extend(_partition_blockers(histories))

    compiled_histories = compile_histories(histories)
    input_digest = compute_partial_dephasing_input_digest(
        source_v122_certificate_digest=payload[
            "source_v122_certificate_digest"
        ],
        source_physical_quantum_qi_definition_digest=payload[
            "source_physical_quantum_qi_definition_digest"
        ],
        weight_denominator=weight_denominator,
        dephasing_denominator=dephasing_denominator,
        dephasing_numerators=dephasing_numerators,
        histories=histories,
    )

    observables = (
        exact_partial_dephasing_observables(
            compiled_histories,
            dephasing_denominator=dephasing_denominator,
            dephasing_numerators=dephasing_numerators,
        )
        if compiled_histories and dephasing_numerators
        else {
            "retained_history_ids": [],
            "history_count": 0,
            "terminal_state_ids": [],
            "homotopy_class_ids": [],
            "coherence_block_ids": [],
            "history_amplitude_profile": [],
            "endpoint_intensity_profile": [],
            "block_amplitude_profile": [],
            "endpoint_coherent_kernel": [],
            "incoherent_mass_numerator_squared": 0,
            "endpoint_gram_hilbert_schmidt_numerator_quartic": 0,
            "block_gram_hilbert_schmidt_numerator_quartic": 0,
            "cross_block_hilbert_schmidt_numerator_quartic": 0,
            "partial_dephasing_trajectory": [],
            "trajectory_trace_preserved": False,
            "trajectory_cross_coherence_nonincreasing": False,
            "trajectory_purity_nonincreasing": False,
            "trajectory_mixedness_nondecreasing": False,
        }
    )
    expected_claims = _expected_claims(input_digest, observables)

    if claims:
        for field, expected in expected_claims.items():
            if claims.get(field) != expected:
                blockers.append("claim_mismatch_" + field)

    return {
        "schema_version": SCHEMA_VERSION,
        "accepted": not blockers,
        "blockers": sorted(set(blockers)),
        "input_digest": input_digest,
        "source_bindings": {
            "source_v122_certificate_digest": payload[
                "source_v122_certificate_digest"
            ],
            "source_physical_quantum_qi_definition_digest": payload[
                "source_physical_quantum_qi_definition_digest"
            ],
        },
        "weight_denominator": weight_denominator,
        "dephasing_denominator": dephasing_denominator,
        "dephasing_numerators": dephasing_numerators,
        "compiled_histories": compiled_histories,
        "observables": observables,
        "partial_dephasing": {
            "homotopy_partition_exact": not _partition_blockers(histories),
            "exact_rational_partial_dephasing": True,
            "convex_gram_witness_used": True,
            "kernel_entries_are_empirical_probabilities": False,
            "dephasing_parameter_is_physical_time": False,
        },
        "noncollapse": {
            "all_histories_retained": True,
            "argmin_performed": False,
            "representative_history_selected": False,
            "history_ranking_performed": False,
            "history_pruning_performed": False,
            "activation_performed": False,
            "execution_permission": False,
        },
        "immutability": {
            "source_v122_certificate_mutated": False,
            "persistent_world_state_mutated": False,
        },
    }


__all__ = [
    "SCHEMA_VERSION",
    "issue_finite_physical_quantum_qi_coherence_kernel_partial_dephasing_certificate",
]
