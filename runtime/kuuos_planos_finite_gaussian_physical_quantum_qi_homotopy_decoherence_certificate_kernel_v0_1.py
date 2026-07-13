from __future__ import annotations

from collections import defaultdict

from runtime.kuuos_planos_finite_gaussian_physical_quantum_qi_homotopy_decoherence_algebra_support_v0_1 import (
    compile_histories,
    exact_gaussian_homotopy_decoherence_observables,
)
from runtime.kuuos_planos_finite_gaussian_physical_quantum_qi_homotopy_decoherence_schema_support_v0_1 import (
    compute_gaussian_homotopy_decoherence_input_digest,
    normalize_claims,
    normalize_histories,
    normalize_states,
    normalize_transitions,
)


SCHEMA_VERSION = (
    "kuuos.planos.finite-gaussian-physical-quantum-qi-homotopy-"
    "decoherence-certificate.v0.1"
)

MAXIMUM_QI_DIMENSION = 8
MAXIMUM_STATE_COUNT = 64
MAXIMUM_TRANSITION_COUNT = 256
MAXIMUM_HISTORY_COUNT = 128
MAXIMUM_HISTORY_LENGTH = 32
MAXIMUM_ACTION_INCREMENT = 10_000
MAXIMUM_ABSOLUTE_QI_COORDINATE = 10_000
MAXIMUM_ABSOLUTE_QI_FLUX = 10_000


def _nonempty_text(value) -> bool:
    return isinstance(value, str) and bool(value)


def _positive_nat(value) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def _expected_claims(input_digest: str, observables: dict) -> dict:
    return {
        "input_digest": input_digest,
        **observables,
        "all_histories_retained": True,
        "z4_phase_surface_used": True,
        "gaussian_integer_arithmetic_exact": True,
        "homotopy_classes_retained": True,
        "coherence_blocks_retained": True,
        "decoherence_mask_applied_without_pruning": True,
        "argmin_performed": False,
        "representative_history_selected": False,
        "history_ranking_performed": False,
        "history_pruning_performed": False,
        "activation_performed": False,
        "execution_permission": False,
        "source_v121_certificate_mutated": False,
        "source_path_homotopy_certificate_mutated": False,
        "persistent_world_state_mutated": False,
    }


def issue_finite_gaussian_physical_quantum_qi_homotopy_decoherence_certificate(
    payload,
):
    top_fields = {
        "schema_version",
        "source_v121_certificate_digest",
        "source_path_homotopy_certificate_digest",
        "source_physical_quantum_qi_definition_digest",
        "weight_denominator",
        "qi_dimension",
        "states",
        "transitions",
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
        "source_v121_certificate_digest",
        "source_path_homotopy_certificate_digest",
        "source_physical_quantum_qi_definition_digest",
    ):
        if not _nonempty_text(payload[field]):
            blockers.append(field + "_missing")

    qi_dimension = payload["qi_dimension"]
    if not _positive_nat(qi_dimension) or qi_dimension > MAXIMUM_QI_DIMENSION:
        blockers.append("qi_dimension_invalid")
        qi_dimension = 1

    weight_denominator = payload["weight_denominator"]
    if not _positive_nat(weight_denominator):
        blockers.append("weight_denominator_invalid")
        weight_denominator = 1

    state_errors, states = normalize_states(
        payload["states"],
        qi_dimension=qi_dimension,
        maximum_state_count=MAXIMUM_STATE_COUNT,
        maximum_absolute_qi_coordinate=MAXIMUM_ABSOLUTE_QI_COORDINATE,
    )
    transition_errors, transitions = normalize_transitions(
        payload["transitions"],
        qi_dimension=qi_dimension,
        maximum_transition_count=MAXIMUM_TRANSITION_COUNT,
        maximum_action_increment=MAXIMUM_ACTION_INCREMENT,
        maximum_absolute_qi_flux=MAXIMUM_ABSOLUTE_QI_FLUX,
    )
    history_errors, histories = normalize_histories(
        payload["histories"],
        maximum_history_count=MAXIMUM_HISTORY_COUNT,
        maximum_history_length=MAXIMUM_HISTORY_LENGTH,
    )
    claim_errors, claims = normalize_claims(payload["claims"])
    blockers.extend(state_errors)
    blockers.extend(transition_errors)
    blockers.extend(history_errors)
    blockers.extend(claim_errors)

    if sum(item["weight_numerator"] for item in histories) != weight_denominator:
        blockers.append("history_weights_do_not_sum_to_denominator")

    state_by_id = {item["state_id"]: item for item in states}
    for transition in transitions:
        left = state_by_id.get(transition["from_state_id"])
        right = state_by_id.get(transition["to_state_id"])
        if left is None or right is None:
            continue
        expected_flux = [
            right_value - left_value
            for left_value, right_value in zip(
                left["qi_coordinate"], right["qi_coordinate"]
            )
        ]
        if transition["qi_flux_increment"] != expected_flux:
            blockers.append(
                "transition_qi_flux_mismatch_" + transition["transition_id"]
            )

    class_to_blocks: dict[str, set[str]] = defaultdict(set)
    block_to_classes: dict[str, set[str]] = defaultdict(set)
    for history in histories:
        class_to_blocks[history["homotopy_class_id"]].add(
            history["coherence_block_id"]
        )
        block_to_classes[history["coherence_block_id"]].add(
            history["homotopy_class_id"]
        )
    for class_id, blocks in sorted(class_to_blocks.items()):
        if len(blocks) != 1:
            blockers.append(
                "homotopy_class_spans_multiple_coherence_blocks_" + class_id
            )
    for block_id, classes in sorted(block_to_classes.items()):
        if len(classes) != 1:
            blockers.append("coherence_block_mixes_homotopy_classes_" + block_id)

    compile_errors, compiled_histories = compile_histories(
        states, transitions, histories, qi_dimension
    )
    blockers.extend(compile_errors)

    if compiled_histories:
        roots = {item["root_state_id"] for item in compiled_histories}
        if len(roots) != 1:
            blockers.append("history_family_must_share_one_initial_state")
    else:
        blockers.append("no_compiled_histories")

    input_digest = compute_gaussian_homotopy_decoherence_input_digest(
        source_v121_certificate_digest=payload["source_v121_certificate_digest"],
        source_path_homotopy_certificate_digest=payload[
            "source_path_homotopy_certificate_digest"
        ],
        source_physical_quantum_qi_definition_digest=payload[
            "source_physical_quantum_qi_definition_digest"
        ],
        weight_denominator=weight_denominator,
        qi_dimension=qi_dimension,
        states=states,
        transitions=transitions,
        histories=histories,
    )

    observables = (
        exact_gaussian_homotopy_decoherence_observables(
            compiled_histories, weight_denominator
        )
        if compiled_histories
        else {
            "retained_history_ids": [],
            "history_count": 0,
            "distinct_state_sequence_count": 0,
            "partition_function_polynomial": [],
            "endpoint_gaussian_interference_profile": [],
            "homotopy_class_amplitude_profile": [],
            "decoherence_profile": [],
            "depth_state_marginals": [],
            "scenario_marginals": [],
            "branch_points": [],
            "reconvergence_points": [],
            "loop_history_ids": [],
            "pairwise_shared_prefix_profile": [],
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
            "source_v121_certificate_digest": payload[
                "source_v121_certificate_digest"
            ],
            "source_path_homotopy_certificate_digest": payload[
                "source_path_homotopy_certificate_digest"
            ],
            "source_physical_quantum_qi_definition_digest": payload[
                "source_physical_quantum_qi_definition_digest"
            ],
        },
        "weight_denominator": weight_denominator,
        "qi_dimension": qi_dimension,
        "compiled_histories": compiled_histories,
        "observables": observables,
        "phase_surface": {
            "phase_group": "Z4",
            "amplitude_ring": "Gaussian integers Z[i]",
            "floating_point_used": False,
        },
        "decoherence": {
            "homotopy_partition_exact": not any(
                blocker.startswith("homotopy_class_spans_multiple_")
                or blocker.startswith("coherence_block_mixes_")
                for blocker in blockers
            ),
            "histories_removed": False,
            "amplitudes_reweighted": False,
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
            "source_v121_certificate_mutated": False,
            "source_path_homotopy_certificate_mutated": False,
            "persistent_world_state_mutated": False,
        },
    }


__all__ = [
    "SCHEMA_VERSION",
    "issue_finite_gaussian_physical_quantum_qi_homotopy_decoherence_certificate",
]
