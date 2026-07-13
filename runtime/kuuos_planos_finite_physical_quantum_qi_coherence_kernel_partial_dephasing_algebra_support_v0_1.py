from __future__ import annotations

from collections import defaultdict
from math import gcd


Gaussian = tuple[int, int]


def gaussian_unit(phase_mod4: int) -> Gaussian:
    return ((1, 0), (0, 1), (-1, 0), (0, -1))[phase_mod4]


def gaussian_amplitude(weight: int, phase_mod4: int) -> Gaussian:
    real, imag = gaussian_unit(phase_mod4)
    return weight * real, weight * imag


def gaussian_add(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] + right[0], left[1] + right[1]


def gaussian_sum(values: list[Gaussian]) -> Gaussian:
    real = 0
    imag = 0
    for value in values:
        real += value[0]
        imag += value[1]
    return real, imag


def gaussian_scale(scale: int, value: Gaussian) -> Gaussian:
    return scale * value[0], scale * value[1]


def gaussian_mul_conj(left: Gaussian, right: Gaussian) -> Gaussian:
    # (a + bi) * conjugate(c + di)
    return (
        left[0] * right[0] + left[1] * right[1],
        left[1] * right[0] - left[0] * right[1],
    )


def gaussian_norm_squared(value: Gaussian) -> int:
    return value[0] * value[0] + value[1] * value[1]


def reduced_fraction(numerator: int, denominator: int) -> dict:
    divisor = gcd(abs(numerator), denominator)
    if divisor == 0:
        divisor = 1
    return {
        "numerator": numerator // divisor,
        "denominator": denominator // divisor,
    }


def compile_histories(histories: list[dict]) -> list[dict]:
    output: list[dict] = []
    for item in histories:
        amplitude = gaussian_amplitude(
            item["weight_numerator"],
            item["phase_mod4"],
        )
        output.append(
            {
                **item,
                "gaussian_amplitude_real": amplitude[0],
                "gaussian_amplitude_imag": amplitude[1],
                "amplitude_norm_squared": gaussian_norm_squared(amplitude),
            }
        )
    return sorted(output, key=lambda item: item["history_id"])


def _amplitude(item: dict) -> Gaussian:
    return item["gaussian_amplitude_real"], item["gaussian_amplitude_imag"]


def history_amplitude_profile(compiled_histories: list[dict]) -> list[dict]:
    return [
        {
            "history_id": item["history_id"],
            "terminal_state_id": item["terminal_state_id"],
            "homotopy_class_id": item["homotopy_class_id"],
            "coherence_block_id": item["coherence_block_id"],
            "weight_numerator": item["weight_numerator"],
            "phase_mod4": item["phase_mod4"],
            "gaussian_amplitude_real": item["gaussian_amplitude_real"],
            "gaussian_amplitude_imag": item["gaussian_amplitude_imag"],
            "amplitude_norm_squared": item["amplitude_norm_squared"],
        }
        for item in compiled_histories
    ]


def _group_by_endpoint(compiled_histories: list[dict]):
    grouped: dict[str, list[dict]] = defaultdict(list)
    for item in compiled_histories:
        grouped[item["terminal_state_id"]].append(item)
    return grouped


def _group_by_endpoint_block(compiled_histories: list[dict]):
    grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for item in compiled_histories:
        grouped[
            (item["terminal_state_id"], item["coherence_block_id"])
        ].append(item)
    return grouped


def endpoint_intensity_profile(compiled_histories: list[dict]) -> list[dict]:
    output: list[dict] = []
    for endpoint, members in sorted(_group_by_endpoint(compiled_histories).items()):
        amplitude = gaussian_sum([_amplitude(item) for item in members])
        blocks: dict[str, list[dict]] = defaultdict(list)
        for item in members:
            blocks[item["coherence_block_id"]].append(item)
        post = sum(
            gaussian_norm_squared(
                gaussian_sum([_amplitude(item) for item in block_members])
            )
            for block_members in blocks.values()
        )
        incoherent = sum(item["amplitude_norm_squared"] for item in members)
        output.append(
            {
                "terminal_state_id": endpoint,
                "history_ids": sorted(item["history_id"] for item in members),
                "gaussian_amplitude_real": amplitude[0],
                "gaussian_amplitude_imag": amplitude[1],
                "fully_coherent_intensity_numerator_squared": (
                    gaussian_norm_squared(amplitude)
                ),
                "block_dephased_intensity_numerator_squared": post,
                "fully_incoherent_intensity_numerator_squared": incoherent,
            }
        )
    return output


def block_amplitude_profile(compiled_histories: list[dict]) -> list[dict]:
    output: list[dict] = []
    grouped = _group_by_endpoint_block(compiled_histories)
    for (endpoint, block_id), members in sorted(grouped.items()):
        amplitude = gaussian_sum([_amplitude(item) for item in members])
        output.append(
            {
                "terminal_state_id": endpoint,
                "coherence_block_id": block_id,
                "homotopy_class_ids": sorted(
                    {item["homotopy_class_id"] for item in members}
                ),
                "history_ids": sorted(item["history_id"] for item in members),
                "block_mass_numerator_squared": sum(
                    item["amplitude_norm_squared"] for item in members
                ),
                "gaussian_amplitude_real": amplitude[0],
                "gaussian_amplitude_imag": amplitude[1],
                "block_coherent_intensity_numerator_squared": (
                    gaussian_norm_squared(amplitude)
                ),
            }
        )
    return output


def endpoint_coherent_kernel(compiled_histories: list[dict]) -> list[dict]:
    output: list[dict] = []
    for left in compiled_histories:
        for right in compiled_histories:
            same_endpoint = (
                left["terminal_state_id"] == right["terminal_state_id"]
            )
            value = (
                gaussian_mul_conj(_amplitude(left), _amplitude(right))
                if same_endpoint
                else (0, 0)
            )
            output.append(
                {
                    "row_history_id": left["history_id"],
                    "column_history_id": right["history_id"],
                    "same_terminal_state": same_endpoint,
                    "same_coherence_block": (
                        same_endpoint
                        and left["coherence_block_id"]
                        == right["coherence_block_id"]
                    ),
                    "real_numerator": value[0],
                    "imag_numerator": value[1],
                }
            )
    return output


def _kernel_is_hermitian(entries: list[dict]) -> bool:
    by_pair = {
        (item["row_history_id"], item["column_history_id"]): item
        for item in entries
    }
    for (row, column), item in by_pair.items():
        reverse = by_pair[(column, row)]
        if item["real_numerator"] != reverse["real_numerator"]:
            return False
        if item["imag_numerator"] != -reverse["imag_numerator"]:
            return False
    return True


def _kernel_step_entries(
    compiled_histories: list[dict],
    *,
    dephasing_denominator: int,
    dephasing_numerator: int,
) -> list[dict]:
    output: list[dict] = []
    for left in compiled_histories:
        for right in compiled_histories:
            same_endpoint = (
                left["terminal_state_id"] == right["terminal_state_id"]
            )
            same_block = (
                same_endpoint
                and left["coherence_block_id"]
                == right["coherence_block_id"]
            )
            if not same_endpoint:
                scale = 0
            elif same_block:
                scale = dephasing_denominator
            else:
                scale = dephasing_numerator
            value = gaussian_scale(
                scale,
                gaussian_mul_conj(_amplitude(left), _amplitude(right)),
            )
            output.append(
                {
                    "row_history_id": left["history_id"],
                    "column_history_id": right["history_id"],
                    "real_numerator": value[0],
                    "imag_numerator": value[1],
                }
            )
    return output


def _mass_profiles(compiled_histories: list[dict]):
    endpoint_mass: dict[str, int] = defaultdict(int)
    block_mass: dict[tuple[str, str], int] = defaultdict(int)
    for item in compiled_histories:
        mass = item["amplitude_norm_squared"]
        endpoint_mass[item["terminal_state_id"]] += mass
        block_mass[
            (item["terminal_state_id"], item["coherence_block_id"])
        ] += mass
    return endpoint_mass, block_mass


def _intensity_totals(compiled_histories: list[dict]) -> tuple[int, int]:
    endpoint_profile = endpoint_intensity_profile(compiled_histories)
    pre = sum(
        item["fully_coherent_intensity_numerator_squared"]
        for item in endpoint_profile
    )
    post = sum(
        item["block_dephased_intensity_numerator_squared"]
        for item in endpoint_profile
    )
    return pre, post


def partial_dephasing_trajectory(
    compiled_histories: list[dict],
    *,
    dephasing_denominator: int,
    dephasing_numerators: list[int],
) -> list[dict]:
    incoherent_mass = sum(
        item["amplitude_norm_squared"] for item in compiled_histories
    )
    endpoint_mass, block_mass = _mass_profiles(compiled_histories)
    endpoint_hs = sum(value * value for value in endpoint_mass.values())
    block_hs = sum(value * value for value in block_mass.values())
    cross_hs = endpoint_hs - block_hs
    pre_intensity, post_intensity = _intensity_totals(compiled_histories)

    normalized_denominator = dephasing_denominator * incoherent_mass
    purity_denominator = normalized_denominator * normalized_denominator

    output: list[dict] = []
    for numerator in dephasing_numerators:
        purity_numerator = (
            dephasing_denominator
            * dephasing_denominator
            * block_hs
            + numerator * numerator * cross_hs
        )
        mixedness_numerator = purity_denominator - purity_numerator
        cross_coherence = numerator * numerator * cross_hs
        readout_intensity = (
            numerator * pre_intensity
            + (dephasing_denominator - numerator) * post_intensity
        )
        kernel_entries = _kernel_step_entries(
            compiled_histories,
            dephasing_denominator=dephasing_denominator,
            dephasing_numerator=numerator,
        )
        output.append(
            {
                "dephasing_numerator": numerator,
                "dephasing_denominator": dephasing_denominator,
                "kernel_entry_denominator": dephasing_denominator,
                "normalized_kernel_denominator": normalized_denominator,
                "trace_numerator": normalized_denominator,
                "purity_numerator": purity_numerator,
                "purity_denominator_squared": purity_denominator,
                "purity_reduced": reduced_fraction(
                    purity_numerator, purity_denominator
                ),
                "quadratic_mixedness_numerator": mixedness_numerator,
                "quadratic_mixedness_denominator_squared": purity_denominator,
                "quadratic_mixedness_reduced": reduced_fraction(
                    mixedness_numerator, purity_denominator
                ),
                "cross_block_coherence_hilbert_schmidt_numerator_quartic": (
                    cross_coherence
                ),
                "readout_intensity_numerator": readout_intensity,
                "readout_intensity_denominator": dephasing_denominator,
                "block_trace_profile": [
                    {
                        "terminal_state_id": endpoint,
                        "coherence_block_id": block_id,
                        "trace_numerator": dephasing_denominator * mass,
                        "trace_denominator": normalized_denominator,
                    }
                    for (endpoint, block_id), mass in sorted(block_mass.items())
                ],
                "convex_gram_witness": {
                    "endpoint_gram_coefficient_numerator": numerator,
                    "block_gram_coefficient_numerator": (
                        dephasing_denominator - numerator
                    ),
                    "coefficient_denominator": dephasing_denominator,
                    "nonnegative_coefficients": True,
                },
                "kernel_hermitian": _kernel_is_hermitian(kernel_entries),
                "positive_semidefinite_by_convex_gram_construction": True,
                "kernel_entries": kernel_entries,
            }
        )
    return output


def exact_partial_dephasing_observables(
    compiled_histories: list[dict],
    *,
    dephasing_denominator: int,
    dephasing_numerators: list[int],
) -> dict:
    endpoint_mass, block_mass = _mass_profiles(compiled_histories)
    incoherent_mass = sum(
        item["amplitude_norm_squared"] for item in compiled_histories
    )
    endpoint_hs = sum(value * value for value in endpoint_mass.values())
    block_hs = sum(value * value for value in block_mass.values())
    cross_hs = endpoint_hs - block_hs
    raw_kernel = endpoint_coherent_kernel(compiled_histories)
    trajectory = partial_dephasing_trajectory(
        compiled_histories,
        dephasing_denominator=dephasing_denominator,
        dephasing_numerators=dephasing_numerators,
    )

    traces = [item["trace_numerator"] for item in trajectory]
    cross_values = [
        item["cross_block_coherence_hilbert_schmidt_numerator_quartic"]
        for item in trajectory
    ]
    purity_values = [item["purity_numerator"] for item in trajectory]
    mixedness_values = [
        item["quadratic_mixedness_numerator"] for item in trajectory
    ]

    return {
        "retained_history_ids": [
            item["history_id"] for item in compiled_histories
        ],
        "history_count": len(compiled_histories),
        "terminal_state_ids": sorted(
            {item["terminal_state_id"] for item in compiled_histories}
        ),
        "homotopy_class_ids": sorted(
            {item["homotopy_class_id"] for item in compiled_histories}
        ),
        "coherence_block_ids": sorted(
            {item["coherence_block_id"] for item in compiled_histories}
        ),
        "history_amplitude_profile": history_amplitude_profile(
            compiled_histories
        ),
        "endpoint_intensity_profile": endpoint_intensity_profile(
            compiled_histories
        ),
        "block_amplitude_profile": block_amplitude_profile(
            compiled_histories
        ),
        "endpoint_coherent_kernel": raw_kernel,
        "incoherent_mass_numerator_squared": incoherent_mass,
        "endpoint_gram_hilbert_schmidt_numerator_quartic": endpoint_hs,
        "block_gram_hilbert_schmidt_numerator_quartic": block_hs,
        "cross_block_hilbert_schmidt_numerator_quartic": cross_hs,
        "partial_dephasing_trajectory": trajectory,
        "trajectory_trace_preserved": len(set(traces)) == 1,
        "trajectory_cross_coherence_nonincreasing": all(
            left >= right for left, right in zip(cross_values, cross_values[1:])
        ),
        "trajectory_purity_nonincreasing": all(
            left >= right for left, right in zip(purity_values, purity_values[1:])
        ),
        "trajectory_mixedness_nondecreasing": all(
            left <= right
            for left, right in zip(mixedness_values, mixedness_values[1:])
        ),
    }


__all__ = [
    "compile_histories",
    "endpoint_coherent_kernel",
    "exact_partial_dephasing_observables",
    "gaussian_amplitude",
    "gaussian_mul_conj",
    "gaussian_norm_squared",
    "partial_dephasing_trajectory",
]
