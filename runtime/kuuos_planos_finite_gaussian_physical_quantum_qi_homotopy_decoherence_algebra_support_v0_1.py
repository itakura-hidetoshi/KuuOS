from __future__ import annotations

from collections import defaultdict
from itertools import combinations


def gaussian_unit(phase_mod4: int) -> tuple[int, int]:
    units = ((1, 0), (0, 1), (-1, 0), (0, -1))
    return units[phase_mod4]


def gaussian_amplitude(weight: int, phase_mod4: int) -> tuple[int, int]:
    real, imag = gaussian_unit(phase_mod4)
    return weight * real, weight * imag


def gaussian_sum(values: list[tuple[int, int]]) -> tuple[int, int]:
    return sum(value[0] for value in values), sum(value[1] for value in values)


def gaussian_norm_squared(value: tuple[int, int]) -> int:
    return value[0] * value[0] + value[1] * value[1]


def compile_histories(
    states: list[dict],
    transitions: list[dict],
    histories: list[dict],
    qi_dimension: int,
):
    state_ids = {item["state_id"] for item in states}
    transition_by_id = {item["transition_id"]: item for item in transitions}
    blockers: list[str] = []
    output: list[dict] = []

    for history in histories:
        history_id = history["history_id"]
        transition_sequence: list[dict] = []
        for transition_id in history["transition_ids"]:
            transition = transition_by_id.get(transition_id)
            if transition is None:
                blockers.append(
                    f"history_transition_missing_{history_id}_{transition_id}"
                )
                continue
            transition_sequence.append(transition)
        if len(transition_sequence) != len(history["transition_ids"]):
            continue

        for transition in transition_sequence:
            if transition["from_state_id"] not in state_ids:
                blockers.append(
                    f"transition_from_state_missing_{transition['transition_id']}"
                )
            if transition["to_state_id"] not in state_ids:
                blockers.append(
                    f"transition_to_state_missing_{transition['transition_id']}"
                )

        adjacency_ok = True
        for left, right in zip(transition_sequence, transition_sequence[1:]):
            if left["to_state_id"] != right["from_state_id"]:
                blockers.append(
                    f"history_adjacency_invalid_{history_id}_"
                    f"{left['transition_id']}_{right['transition_id']}"
                )
                adjacency_ok = False
        if not adjacency_ok or not transition_sequence:
            continue

        state_sequence = [transition_sequence[0]["from_state_id"]]
        state_sequence.extend(item["to_state_id"] for item in transition_sequence)
        qi_flux_total = [
            sum(item["qi_flux_increment"][coordinate] for item in transition_sequence)
            for coordinate in range(qi_dimension)
        ]
        action_total = sum(item["action_increment"] for item in transition_sequence)
        amplitude = gaussian_amplitude(
            history["weight_numerator"], history["phase_mod4"]
        )
        output.append(
            {
                **history,
                "root_state_id": state_sequence[0],
                "terminal_state_id": state_sequence[-1],
                "state_sequence": state_sequence,
                "action_total": action_total,
                "qi_flux_total": qi_flux_total,
                "gaussian_amplitude_real": amplitude[0],
                "gaussian_amplitude_imag": amplitude[1],
                "contains_loop": len(set(state_sequence)) != len(state_sequence),
            }
        )
    return blockers, sorted(output, key=lambda item: item["history_id"])


def partition_function_polynomial(compiled_histories: list[dict]):
    coefficients: dict[int, int] = defaultdict(int)
    for history in compiled_histories:
        coefficients[history["action_total"]] += history["weight_numerator"]
    return [
        {
            "action_level": action,
            "weight_coefficient_numerator": coefficients[action],
        }
        for action in sorted(coefficients)
    ]


def _amplitude_of(histories: list[dict]) -> tuple[int, int]:
    return gaussian_sum(
        [
            (
                item["gaussian_amplitude_real"],
                item["gaussian_amplitude_imag"],
            )
            for item in histories
        ]
    )


def endpoint_gaussian_interference_profile(compiled_histories: list[dict]):
    grouped: dict[str, list[dict]] = defaultdict(list)
    for history in compiled_histories:
        grouped[history["terminal_state_id"]].append(history)
    output: list[dict] = []
    for endpoint in sorted(grouped):
        histories = grouped[endpoint]
        amplitude = _amplitude_of(histories)
        coherent = gaussian_norm_squared(amplitude)
        incoherent = sum(item["weight_numerator"] ** 2 for item in histories)
        output.append(
            {
                "terminal_state_id": endpoint,
                "history_ids": sorted(item["history_id"] for item in histories),
                "total_weight_numerator": sum(
                    item["weight_numerator"] for item in histories
                ),
                "gaussian_amplitude_real": amplitude[0],
                "gaussian_amplitude_imag": amplitude[1],
                "coherent_intensity_numerator_squared": coherent,
                "incoherent_intensity_numerator_squared": incoherent,
                "interference_delta_numerator_squared": coherent - incoherent,
                "phase_support_mod4": sorted(
                    {item["phase_mod4"] for item in histories}
                ),
            }
        )
    return output


def homotopy_class_amplitude_profile(compiled_histories: list[dict]):
    grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for history in compiled_histories:
        grouped[
            (history["terminal_state_id"], history["homotopy_class_id"])
        ].append(history)
    output: list[dict] = []
    for (endpoint, class_id), histories in sorted(grouped.items()):
        amplitude = _amplitude_of(histories)
        coherent = gaussian_norm_squared(amplitude)
        incoherent = sum(item["weight_numerator"] ** 2 for item in histories)
        output.append(
            {
                "terminal_state_id": endpoint,
                "homotopy_class_id": class_id,
                "coherence_block_ids": sorted(
                    {item["coherence_block_id"] for item in histories}
                ),
                "history_ids": sorted(item["history_id"] for item in histories),
                "total_weight_numerator": sum(
                    item["weight_numerator"] for item in histories
                ),
                "gaussian_amplitude_real": amplitude[0],
                "gaussian_amplitude_imag": amplitude[1],
                "coherent_intensity_numerator_squared": coherent,
                "incoherent_intensity_numerator_squared": incoherent,
                "within_class_interference_delta_numerator_squared": coherent
                - incoherent,
            }
        )
    return output


def decoherence_profile(compiled_histories: list[dict]):
    endpoints: dict[str, list[dict]] = defaultdict(list)
    for history in compiled_histories:
        endpoints[history["terminal_state_id"]].append(history)
    output: list[dict] = []
    for endpoint in sorted(endpoints):
        histories = endpoints[endpoint]
        blocks: dict[str, list[dict]] = defaultdict(list)
        for history in histories:
            blocks[history["coherence_block_id"]].append(history)
        pre_amplitude = _amplitude_of(histories)
        pre_intensity = gaussian_norm_squared(pre_amplitude)
        incoherent = sum(item["weight_numerator"] ** 2 for item in histories)
        block_rows: list[dict] = []
        post_intensity = 0
        for block_id in sorted(blocks):
            members = blocks[block_id]
            amplitude = _amplitude_of(members)
            intensity = gaussian_norm_squared(amplitude)
            post_intensity += intensity
            block_rows.append(
                {
                    "coherence_block_id": block_id,
                    "homotopy_class_ids": sorted(
                        {item["homotopy_class_id"] for item in members}
                    ),
                    "history_ids": sorted(item["history_id"] for item in members),
                    "gaussian_amplitude_real": amplitude[0],
                    "gaussian_amplitude_imag": amplitude[1],
                    "coherent_intensity_numerator_squared": intensity,
                }
            )
        retained_within = post_intensity - incoherent
        discarded_cross = pre_intensity - post_intensity
        output.append(
            {
                "terminal_state_id": endpoint,
                "pre_decoherence_amplitude_real": pre_amplitude[0],
                "pre_decoherence_amplitude_imag": pre_amplitude[1],
                "pre_decoherence_coherent_intensity_numerator_squared": pre_intensity,
                "post_decoherence_block_intensity_numerator_squared": post_intensity,
                "fully_incoherent_intensity_numerator_squared": incoherent,
                "retained_within_block_interference_numerator_squared": retained_within,
                "discarded_cross_block_interference_numerator_squared": discarded_cross,
                "intensity_decomposition_exact": (
                    pre_intensity == post_intensity + discarded_cross
                    and post_intensity == incoherent + retained_within
                ),
                "coherence_blocks": block_rows,
            }
        )
    return output


def depth_state_marginals(
    compiled_histories: list[dict],
    weight_denominator: int,
):
    maximum_depth = max(len(item["transition_ids"]) for item in compiled_histories)
    output: list[dict] = []
    for depth in range(maximum_depth + 1):
        weights: dict[str, int] = defaultdict(int)
        for history in compiled_histories:
            sequence = history["state_sequence"]
            state_id = sequence[min(depth, len(sequence) - 1)]
            weights[state_id] += history["weight_numerator"]
        output.append(
            {
                "depth": depth,
                "weight_denominator": weight_denominator,
                "support_count": len(weights),
                "state_weights": [
                    {
                        "state_id": state_id,
                        "weight_numerator": weights[state_id],
                    }
                    for state_id in sorted(weights)
                ],
            }
        )
    return output


def scenario_marginals(
    compiled_histories: list[dict],
    weight_denominator: int,
):
    grouped: dict[str, list[dict]] = defaultdict(list)
    for history in compiled_histories:
        grouped[history["scenario_id"]].append(history)
    return [
        {
            "scenario_id": scenario_id,
            "weight_numerator": sum(
                item["weight_numerator"] for item in grouped[scenario_id]
            ),
            "weight_denominator": weight_denominator,
            "history_ids": sorted(
                item["history_id"] for item in grouped[scenario_id]
            ),
        }
        for scenario_id in sorted(grouped)
    ]


def branch_and_reconvergence_points(compiled_histories: list[dict]):
    outgoing: dict[str, set[str]] = defaultdict(set)
    incoming: dict[str, set[str]] = defaultdict(set)
    for history in compiled_histories:
        sequence = history["state_sequence"]
        for source, target in zip(sequence, sequence[1:]):
            outgoing[source].add(target)
            incoming[target].add(source)
    branch_points = [
        {
            "state_id": state_id,
            "successor_state_ids": sorted(successors),
            "successor_count": len(successors),
        }
        for state_id, successors in sorted(outgoing.items())
        if len(successors) > 1
    ]
    reconvergence_points = [
        {
            "state_id": state_id,
            "predecessor_state_ids": sorted(predecessors),
            "predecessor_count": len(predecessors),
        }
        for state_id, predecessors in sorted(incoming.items())
        if len(predecessors) > 1
    ]
    return branch_points, reconvergence_points


def shared_prefix_length(left: list[str], right: list[str]) -> int:
    length = 0
    for left_state, right_state in zip(left, right):
        if left_state != right_state:
            break
        length += 1
    return length


def pairwise_shared_prefix_profile(compiled_histories: list[dict]):
    output: list[dict] = []
    for left, right in combinations(compiled_histories, 2):
        output.append(
            {
                "left_history_id": left["history_id"],
                "right_history_id": right["history_id"],
                "shared_state_prefix_length": shared_prefix_length(
                    left["state_sequence"], right["state_sequence"]
                ),
                "same_terminal_state": left["terminal_state_id"]
                == right["terminal_state_id"],
                "same_scenario": left["scenario_id"] == right["scenario_id"],
                "same_homotopy_class": left["homotopy_class_id"]
                == right["homotopy_class_id"],
                "same_coherence_block": left["coherence_block_id"]
                == right["coherence_block_id"],
            }
        )
    return output


def exact_gaussian_homotopy_decoherence_observables(
    compiled_histories: list[dict],
    weight_denominator: int,
):
    branch_points, reconvergence_points = branch_and_reconvergence_points(
        compiled_histories
    )
    return {
        "retained_history_ids": [item["history_id"] for item in compiled_histories],
        "history_count": len(compiled_histories),
        "distinct_state_sequence_count": len(
            {tuple(item["state_sequence"]) for item in compiled_histories}
        ),
        "partition_function_polynomial": partition_function_polynomial(
            compiled_histories
        ),
        "endpoint_gaussian_interference_profile": (
            endpoint_gaussian_interference_profile(compiled_histories)
        ),
        "homotopy_class_amplitude_profile": homotopy_class_amplitude_profile(
            compiled_histories
        ),
        "decoherence_profile": decoherence_profile(compiled_histories),
        "depth_state_marginals": depth_state_marginals(
            compiled_histories, weight_denominator
        ),
        "scenario_marginals": scenario_marginals(
            compiled_histories, weight_denominator
        ),
        "branch_points": branch_points,
        "reconvergence_points": reconvergence_points,
        "loop_history_ids": sorted(
            item["history_id"]
            for item in compiled_histories
            if item["contains_loop"]
        ),
        "pairwise_shared_prefix_profile": pairwise_shared_prefix_profile(
            compiled_histories
        ),
    }


__all__ = [
    "branch_and_reconvergence_points",
    "compile_histories",
    "decoherence_profile",
    "depth_state_marginals",
    "endpoint_gaussian_interference_profile",
    "exact_gaussian_homotopy_decoherence_observables",
    "gaussian_amplitude",
    "gaussian_norm_squared",
    "gaussian_sum",
    "gaussian_unit",
    "homotopy_class_amplitude_profile",
    "pairwise_shared_prefix_profile",
    "partition_function_polynomial",
    "scenario_marginals",
    "shared_prefix_length",
]
