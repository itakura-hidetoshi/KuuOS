from __future__ import annotations

from hashlib import sha256
import json
from math import gcd
from typing import Any, Mapping

SCHEMA_VERSION = (
    "kuuos.memoryos.candidate-triple-gram-determinant-joint-coherence-"
    "compatibility-certificate.v0.1"
)
SOURCE_MEMORYOS_V046_SCHEMA_VERSION = (
    "kuuos.memoryos.candidate-pair-cauchy-schwarz-relational-coherence-"
    "envelope-certificate.v0.1"
)
MAXIMUM_CANDIDATE_COUNT = 128
MAXIMUM_DEPHASING_STEP_COUNT = 64
MAXIMUM_ABSOLUTE_INTEGER = 10_000_000


def canonical_digest(value: Any) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


def _blocked(*blockers: str) -> dict[str, Any]:
    return {
        "accepted": False,
        "schema_version": SCHEMA_VERSION,
        "blockers": sorted(set(blockers)),
        "observables": {},
        "certificate_digest": None,
    }


def _integer(value: Any, field: str, *, nonnegative: bool = False) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(field + "_invalid")
    if abs(value) > MAXIMUM_ABSOLUTE_INTEGER:
        raise ValueError(field + "_out_of_bounds")
    if nonnegative and value < 0:
        raise ValueError(field + "_negative")
    return value


def _string_ids(value: Any, field: str) -> list[str]:
    if (
        not isinstance(value, list)
        or not value
        or len(value) > MAXIMUM_CANDIDATE_COUNT
        or len(value) != len(set(value))
        or any(not isinstance(item, str) or not item for item in value)
    ):
        raise ValueError(field + "_invalid")
    return list(value)


def _review_ids(
    observables: Mapping[str, Any],
    field: str,
    candidate_ids: list[str],
) -> list[str]:
    value = observables.get(field)
    if (
        not isinstance(value, list)
        or len(value) != len(set(value))
        or any(item not in candidate_ids for item in value)
    ):
        raise ValueError("source_memoryos_v046_" + field + "_invalid")
    return list(value)


def _normalized_fraction(numerator: int, denominator: int) -> tuple[int, int]:
    common = gcd(numerator, denominator)
    return numerator // common, denominator // common


def _complex_mul(
    left: tuple[int, int],
    right: tuple[int, int],
) -> tuple[int, int]:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def _complex_abs_square(value: tuple[int, int]) -> int:
    return value[0] * value[0] + value[1] * value[1]


def _pair_record_map(
    raw_records: Any,
    *,
    candidate_ids: list[str],
    denominator: int,
    prefix: str,
) -> dict[tuple[str, str], dict[str, Any]]:
    if not isinstance(raw_records, list):
        raise ValueError(prefix + "_pair_records_invalid")
    expected_pairs = {
        (left_id, right_id)
        for left_id in candidate_ids
        for right_id in candidate_ids
    }
    result: dict[tuple[str, str], dict[str, Any]] = {}
    for raw in raw_records:
        if not isinstance(raw, Mapping):
            raise ValueError(prefix + "_pair_record_invalid")
        item = dict(raw)
        left_id = item.get("left_candidate_id")
        right_id = item.get("right_candidate_id")
        if left_id not in candidate_ids or right_id not in candidate_ids:
            raise ValueError(prefix + "_pair_invalid")
        pair = left_id, right_id
        if pair in result:
            raise ValueError(prefix + "_pair_duplicate")
        if item.get("pair_retained") is not True:
            raise ValueError(prefix + "_pair_not_retained")
        if item.get("source_kernel_entry_denominator") != denominator:
            raise ValueError(prefix + "_pair_denominator_mismatch")
        real_numerator = _integer(item.get("source_real_numerator"), prefix + "_real")
        imag_numerator = _integer(item.get("source_imag_numerator"), prefix + "_imag")
        left_diagonal = _integer(
            item.get("left_diagonal_numerator"),
            prefix + "_left_diagonal",
            nonnegative=True,
        )
        right_diagonal = _integer(
            item.get("right_diagonal_numerator"),
            prefix + "_right_diagonal",
            nonnegative=True,
        )
        magnitude_square = _complex_abs_square((real_numerator, imag_numerator))
        diagonal_product = left_diagonal * right_diagonal
        determinant_margin = diagonal_product - magnitude_square
        zero_diagonal_pair = left_diagonal == 0 or right_diagonal == 0
        if zero_diagonal_pair:
            normalized_numerator, normalized_denominator = 0, 1
        else:
            normalized_numerator, normalized_denominator = _normalized_fraction(
                magnitude_square,
                diagonal_product,
            )
        expected = {
            "coherence_magnitude_square_numerator": magnitude_square,
            "coherence_magnitude_square_denominator": denominator**2,
            "diagonal_product_numerator": diagonal_product,
            "diagonal_product_denominator": denominator**2,
            "determinant_margin_numerator": determinant_margin,
            "determinant_margin_denominator": denominator**2,
            "cauchy_schwarz_bound_holds": determinant_margin >= 0,
            "zero_diagonal_pair": zero_diagonal_pair,
            "zero_diagonal_forces_zero_coherence": (
                not zero_diagonal_pair or magnitude_square == 0
            ),
            "normalized_coherence_square_numerator": normalized_numerator,
            "normalized_coherence_square_denominator": normalized_denominator,
            "normalized_coherence_square_at_most_one": (
                normalized_numerator <= normalized_denominator
            ),
        }
        for field, expected_value in expected.items():
            if item.get(field) != expected_value:
                raise ValueError(prefix + "_pair_" + field + "_mismatch")
        result[pair] = {
            "real_numerator": real_numerator,
            "imag_numerator": imag_numerator,
            "left_diagonal_numerator": left_diagonal,
            "right_diagonal_numerator": right_diagonal,
        }
    if set(result) != expected_pairs:
        raise ValueError(prefix + "_pair_support_mismatch")
    for left_id in candidate_ids:
        diagonal = result[(left_id, left_id)]
        if diagonal["imag_numerator"] != 0:
            raise ValueError(prefix + "_diagonal_imaginary")
        if diagonal["real_numerator"] != diagonal["left_diagonal_numerator"]:
            raise ValueError(prefix + "_diagonal_left_mismatch")
        if diagonal["real_numerator"] != diagonal["right_diagonal_numerator"]:
            raise ValueError(prefix + "_diagonal_right_mismatch")
        for right_id in candidate_ids:
            forward = result[(left_id, right_id)]
            reverse = result[(right_id, left_id)]
            if (
                forward["real_numerator"] != reverse["real_numerator"]
                or forward["imag_numerator"] != -reverse["imag_numerator"]
            ):
                raise ValueError(prefix + "_not_hermitian")
            if (
                forward["left_diagonal_numerator"]
                != result[(left_id, left_id)]["real_numerator"]
                or forward["right_diagonal_numerator"]
                != result[(right_id, right_id)]["real_numerator"]
            ):
                raise ValueError(prefix + "_pair_diagonal_binding_mismatch")
    return result


def _normalize_source_memoryos_v046(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError("source_memoryos_v046_certificate_invalid")
    source = dict(value)
    if source.get("accepted") is not True:
        raise ValueError("source_memoryos_v046_not_accepted")
    if source.get("schema_version") != SOURCE_MEMORYOS_V046_SCHEMA_VERSION:
        raise ValueError("source_memoryos_v046_schema_invalid")
    digest = source.get("certificate_digest")
    if not isinstance(digest, str) or not digest:
        raise ValueError("source_memoryos_v046_certificate_digest_missing")
    unsigned = dict(source)
    unsigned.pop("certificate_digest", None)
    if canonical_digest(unsigned) != digest:
        raise ValueError("source_memoryos_v046_certificate_digest_mismatch")
    observables = source.get("observables")
    if not isinstance(observables, Mapping):
        raise ValueError("source_memoryos_v046_observables_invalid")
    observables = dict(observables)
    for field in (
        "all_ordered_candidate_pair_support_retained",
        "all_cauchy_schwarz_bounds_hold",
        "all_normalized_coherence_squares_bounded_by_one",
        "all_zero_diagonal_pairs_have_zero_coherence",
        "all_candidate_diagonals_nonnegative",
        "source_candidate_gram_kernel_exact",
        "relational_frontier_preserved",
        "required_review_set_preserved",
        "dissent_visibility_preserved",
        "minority_visibility_preserved",
        "normalized_coherence_advisory_only",
        "normalized_coherence_not_scalar_utility",
        "off_diagonal_sign_not_preference",
        "future_only",
        "read_only",
    ):
        if observables.get(field) is not True:
            raise ValueError("source_memoryos_v046_required_" + field)
    for field in (
        "candidate_ranking_performed",
        "candidate_pruning_performed",
        "candidate_selection_performed",
        "decision_commit_performed",
        "decision_receipt_issued",
        "plan_synthesis_performed",
        "activation_performed",
        "execution_permission",
        "source_memoryos_v045_mutated",
        "source_decisionos_v06_mutated",
        "persistent_world_state_mutated",
        "verification_result_claimed",
        "truth_authority_granted",
    ):
        if observables.get(field) is not False:
            raise ValueError("source_memoryos_v046_forbidden_" + field)

    candidate_ids = _string_ids(
        observables.get("retained_decision_candidate_ids"),
        "source_memoryos_v046_candidate_ids",
    )
    raw_trajectory = observables.get(
        "candidate_pair_cauchy_schwarz_envelope_trajectory"
    )
    if (
        not isinstance(raw_trajectory, list)
        or not raw_trajectory
        or len(raw_trajectory) > MAXIMUM_DEPHASING_STEP_COUNT
    ):
        raise ValueError("source_memoryos_v046_trajectory_invalid")
    envelope_digest = observables.get(
        "candidate_pair_cauchy_schwarz_envelope_digest"
    )
    if not isinstance(envelope_digest, str) or not envelope_digest:
        raise ValueError("source_memoryos_v046_envelope_digest_missing")
    if canonical_digest(raw_trajectory) != envelope_digest:
        raise ValueError("source_memoryos_v046_envelope_digest_mismatch")

    trajectory: list[dict[str, Any]] = []
    previous_dephasing_numerator: int | None = None
    for index, raw_step in enumerate(raw_trajectory):
        if not isinstance(raw_step, Mapping):
            raise ValueError("source_memoryos_v046_step_invalid")
        step = dict(raw_step)
        if step.get("step_index") != index:
            raise ValueError("source_memoryos_v046_step_index_invalid")
        for field in (
            "ordered_candidate_pair_support_complete",
            "all_step_cauchy_schwarz_bounds_hold",
            "all_step_normalized_coherence_squares_at_most_one",
            "all_step_zero_diagonal_pairs_have_zero_coherence",
        ):
            if step.get(field) is not True:
                raise ValueError("source_memoryos_v046_step_required_" + field)
        denominator = _integer(
            step.get("source_kernel_entry_denominator"),
            "source_memoryos_v046_denominator",
        )
        if denominator <= 0:
            raise ValueError("source_memoryos_v046_denominator_nonpositive")
        dephasing_numerator = _integer(
            step.get("dephasing_numerator"),
            "source_memoryos_v046_dephasing_numerator",
            nonnegative=True,
        )
        if (
            previous_dephasing_numerator is not None
            and dephasing_numerator >= previous_dephasing_numerator
        ):
            raise ValueError(
                "source_memoryos_v046_dephasing_not_strictly_decreasing"
            )
        previous_dephasing_numerator = dephasing_numerator
        trajectory.append(
            {
                "step_index": index,
                "dephasing_numerator": dephasing_numerator,
                "kernel_entry_denominator": denominator,
                "entries": _pair_record_map(
                    step.get("candidate_pair_envelopes"),
                    candidate_ids=candidate_ids,
                    denominator=denominator,
                    prefix="source_memoryos_v046",
                ),
            }
        )

    review_fields = {
        field: _review_ids(observables, field, candidate_ids)
        for field in (
            "source_relational_frontier_candidate_ids",
            "source_required_review_candidate_ids",
            "source_dissent_review_candidate_ids",
            "source_minority_protection_candidate_ids",
        )
    }
    source_v045_digest = observables.get(
        "source_memoryos_v045_certificate_digest"
    )
    source_gram_digest = observables.get(
        "source_memoryos_v045_candidate_gram_kernel_digest"
    )
    source_v043_digest = observables.get(
        "source_memoryos_v043_certificate_digest"
    )
    source_v044_digest = observables.get(
        "source_memoryos_v044_certificate_digest"
    )
    for field, field_value in (
        ("v045_digest", source_v045_digest),
        ("gram_digest", source_gram_digest),
        ("v043_digest", source_v043_digest),
        ("v044_digest", source_v044_digest),
    ):
        if not isinstance(field_value, str) or not field_value:
            raise ValueError("source_memoryos_v046_" + field + "_missing")
    return {
        "certificate_digest": digest,
        "observables": observables,
        "candidate_ids": candidate_ids,
        "trajectory": trajectory,
        "envelope_digest": envelope_digest,
        "source_memoryos_v045_certificate_digest": source_v045_digest,
        "source_memoryos_v045_candidate_gram_kernel_digest": source_gram_digest,
        "source_memoryos_v043_certificate_digest": source_v043_digest,
        "source_memoryos_v044_certificate_digest": source_v044_digest,
        **review_fields,
    }


def issue_candidate_triple_gram_determinant_joint_coherence_compatibility_certificate(
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    if not isinstance(payload, Mapping):
        return _blocked("payload_invalid")
    blockers: list[str] = []
    if payload.get("schema_version") != SCHEMA_VERSION:
        blockers.append("schema_version_invalid")
    try:
        source = _normalize_source_memoryos_v046(
            payload.get("source_memoryos_v046_certificate")
        )
    except ValueError as exc:
        return _blocked(*(blockers + [str(exc)]))

    candidate_ids = source["candidate_ids"]
    triple_trajectory: list[dict[str, Any]] = []
    all_triple_support = True
    all_principal_minors_nonnegative = True
    all_determinants_zero = True
    all_repeated_triples_degenerate = True
    all_distinct_triples_rank_two_saturated = True

    for source_step in source["trajectory"]:
        entries = source_step["entries"]
        denominator = source_step["kernel_entry_denominator"]
        triple_records: list[dict[str, Any]] = []
        for first_id in candidate_ids:
            for second_id in candidate_ids:
                for third_id in candidate_ids:
                    first_diagonal = entries[(first_id, first_id)][
                        "real_numerator"
                    ]
                    second_diagonal = entries[(second_id, second_id)][
                        "real_numerator"
                    ]
                    third_diagonal = entries[(third_id, third_id)][
                        "real_numerator"
                    ]
                    first_second = (
                        entries[(first_id, second_id)]["real_numerator"],
                        entries[(first_id, second_id)]["imag_numerator"],
                    )
                    second_third = (
                        entries[(second_id, third_id)]["real_numerator"],
                        entries[(second_id, third_id)]["imag_numerator"],
                    )
                    third_first = (
                        entries[(third_id, first_id)]["real_numerator"],
                        entries[(third_id, first_id)]["imag_numerator"],
                    )
                    cyclic_product = _complex_mul(
                        _complex_mul(first_second, second_third),
                        third_first,
                    )
                    diagonal_cubic = (
                        first_diagonal * second_diagonal * third_diagonal
                    )
                    first_subtraction = (
                        first_diagonal * _complex_abs_square(second_third)
                    )
                    second_subtraction = (
                        second_diagonal * _complex_abs_square(third_first)
                    )
                    third_subtraction = (
                        third_diagonal * _complex_abs_square(first_second)
                    )
                    determinant_numerator = (
                        diagonal_cubic
                        + 2 * cyclic_product[0]
                        - first_subtraction
                        - second_subtraction
                        - third_subtraction
                    )
                    candidate_ids_distinct = (
                        len({first_id, second_id, third_id}) == 3
                    )
                    principal_minor_nonnegative = determinant_numerator >= 0
                    rank_two_determinant_zero = determinant_numerator == 0
                    triple_records.append(
                        {
                            "first_candidate_id": first_id,
                            "second_candidate_id": second_id,
                            "third_candidate_id": third_id,
                            "candidate_ids_distinct": candidate_ids_distinct,
                            "first_diagonal_numerator": first_diagonal,
                            "second_diagonal_numerator": second_diagonal,
                            "third_diagonal_numerator": third_diagonal,
                            "first_second_real_numerator": first_second[0],
                            "first_second_imag_numerator": first_second[1],
                            "second_third_real_numerator": second_third[0],
                            "second_third_imag_numerator": second_third[1],
                            "third_first_real_numerator": third_first[0],
                            "third_first_imag_numerator": third_first[1],
                            "cyclic_product_real_numerator": cyclic_product[0],
                            "cyclic_product_imag_numerator": cyclic_product[1],
                            "twice_cyclic_product_real_numerator": (
                                2 * cyclic_product[0]
                            ),
                            "diagonal_cubic_numerator": diagonal_cubic,
                            "first_diagonal_times_second_third_magnitude_square_numerator": (
                                first_subtraction
                            ),
                            "second_diagonal_times_third_first_magnitude_square_numerator": (
                                second_subtraction
                            ),
                            "third_diagonal_times_first_second_magnitude_square_numerator": (
                                third_subtraction
                            ),
                            "candidate_triple_gram_determinant_numerator": (
                                determinant_numerator
                            ),
                            "candidate_triple_gram_determinant_denominator": (
                                denominator**3
                            ),
                            "candidate_triple_principal_minor_nonnegative": (
                                principal_minor_nonnegative
                            ),
                            "candidate_triple_rank_two_determinant_zero": (
                                rank_two_determinant_zero
                            ),
                            "pairwise_envelopes_jointly_compatible": (
                                principal_minor_nonnegative
                            ),
                            "triple_retained": True,
                        }
                    )
                    all_principal_minors_nonnegative = (
                        all_principal_minors_nonnegative
                        and principal_minor_nonnegative
                    )
                    all_determinants_zero = (
                        all_determinants_zero and rank_two_determinant_zero
                    )
                    if candidate_ids_distinct:
                        all_distinct_triples_rank_two_saturated = (
                            all_distinct_triples_rank_two_saturated
                            and rank_two_determinant_zero
                        )
                    else:
                        all_repeated_triples_degenerate = (
                            all_repeated_triples_degenerate
                            and rank_two_determinant_zero
                        )
        step_support = len(triple_records) == len(candidate_ids) ** 3
        all_triple_support = all_triple_support and step_support
        triple_trajectory.append(
            {
                "step_index": source_step["step_index"],
                "dephasing_numerator": source_step["dephasing_numerator"],
                "source_kernel_entry_denominator": denominator,
                "candidate_triple_gram_determinant_records": triple_records,
                "ordered_candidate_triple_support_complete": step_support,
                "all_step_candidate_triple_principal_minors_nonnegative": all(
                    item["candidate_triple_principal_minor_nonnegative"]
                    for item in triple_records
                ),
                "all_step_candidate_triple_determinants_zero": all(
                    item["candidate_triple_rank_two_determinant_zero"]
                    for item in triple_records
                ),
                "all_step_pairwise_envelopes_jointly_compatible": all(
                    item["pairwise_envelopes_jointly_compatible"]
                    for item in triple_records
                ),
            }
        )

    input_digest = canonical_digest(
        {
            "schema_version": SCHEMA_VERSION,
            "source_memoryos_v046_certificate_digest": source[
                "certificate_digest"
            ],
            "source_candidate_pair_envelope_digest": source[
                "envelope_digest"
            ],
            "candidate_ids": candidate_ids,
        }
    )
    triple_digest = canonical_digest(triple_trajectory)
    observables = {
        "input_digest": input_digest,
        "source_memoryos_v046_certificate_digest": source[
            "certificate_digest"
        ],
        "source_memoryos_v046_candidate_pair_envelope_digest": source[
            "envelope_digest"
        ],
        "source_memoryos_v045_certificate_digest": source[
            "source_memoryos_v045_certificate_digest"
        ],
        "source_memoryos_v045_candidate_gram_kernel_digest": source[
            "source_memoryos_v045_candidate_gram_kernel_digest"
        ],
        "source_memoryos_v043_certificate_digest": source[
            "source_memoryos_v043_certificate_digest"
        ],
        "source_memoryos_v044_certificate_digest": source[
            "source_memoryos_v044_certificate_digest"
        ],
        "retained_decision_candidate_ids": candidate_ids,
        "candidate_triple_gram_determinant_trajectory": triple_trajectory,
        "candidate_triple_gram_determinant_digest": triple_digest,
        "ordered_candidate_triple_count_per_step": len(candidate_ids) ** 3,
        "distinct_ordered_candidate_triple_count_per_step": (
            len(candidate_ids)
            * max(len(candidate_ids) - 1, 0)
            * max(len(candidate_ids) - 2, 0)
        ),
        "all_ordered_candidate_triple_support_retained": all_triple_support,
        "all_candidate_triple_principal_minors_nonnegative": (
            all_principal_minors_nonnegative
        ),
        "all_candidate_triple_determinants_zero": all_determinants_zero,
        "all_pairwise_envelopes_jointly_compatible": (
            all_principal_minors_nonnegative
        ),
        "candidate_gram_rank_at_most_two_witness": all_determinants_zero,
        "all_repeated_candidate_triples_degenerate": (
            all_repeated_triples_degenerate
        ),
        "all_distinct_candidate_triples_rank_two_saturated": (
            all_distinct_triples_rank_two_saturated
        ),
        "source_candidate_pair_envelope_exact": True,
        "source_relational_frontier_candidate_ids": source[
            "source_relational_frontier_candidate_ids"
        ],
        "source_required_review_candidate_ids": source[
            "source_required_review_candidate_ids"
        ],
        "source_dissent_review_candidate_ids": source[
            "source_dissent_review_candidate_ids"
        ],
        "source_minority_protection_candidate_ids": source[
            "source_minority_protection_candidate_ids"
        ],
        "relational_frontier_preserved": True,
        "required_review_set_preserved": True,
        "dissent_visibility_preserved": True,
        "minority_visibility_preserved": True,
        "joint_coherence_compatibility_advisory_only": True,
        "triple_cyclic_product_not_group_preference": True,
        "rank_two_saturation_not_candidate_consensus": True,
        "candidate_ranking_performed": False,
        "candidate_pruning_performed": False,
        "candidate_selection_performed": False,
        "decision_commit_performed": False,
        "decision_receipt_issued": False,
        "plan_synthesis_performed": False,
        "activation_performed": False,
        "execution_permission": False,
        "source_memoryos_v046_mutated": False,
        "source_decisionos_v06_mutated": False,
        "persistent_world_state_mutated": False,
        "verification_result_claimed": False,
        "truth_authority_granted": False,
        "future_only": True,
        "read_only": True,
    }
    for field in (
        "all_ordered_candidate_triple_support_retained",
        "all_candidate_triple_principal_minors_nonnegative",
        "all_candidate_triple_determinants_zero",
        "all_pairwise_envelopes_jointly_compatible",
        "candidate_gram_rank_at_most_two_witness",
        "all_repeated_candidate_triples_degenerate",
        "all_distinct_candidate_triples_rank_two_saturated",
        "source_candidate_pair_envelope_exact",
        "relational_frontier_preserved",
        "required_review_set_preserved",
        "dissent_visibility_preserved",
        "minority_visibility_preserved",
        "joint_coherence_compatibility_advisory_only",
        "triple_cyclic_product_not_group_preference",
        "rank_two_saturation_not_candidate_consensus",
        "future_only",
        "read_only",
    ):
        if observables[field] is not True:
            blockers.append("observable_required_" + field)

    claims = payload.get("claims")
    if not isinstance(claims, Mapping):
        blockers.append("claims_invalid")
    else:
        for field, expected in observables.items():
            if claims.get(field) != expected:
                blockers.append("claim_mismatch_" + field)
        extra = sorted(set(claims) - set(observables))
        if extra:
            blockers.append("claim_extra_field_" + extra[0])
    if blockers:
        return _blocked(*blockers)
    certificate = {
        "accepted": True,
        "schema_version": SCHEMA_VERSION,
        "blockers": [],
        "observables": observables,
    }
    certificate["certificate_digest"] = canonical_digest(certificate)
    return certificate


__all__ = [
    "SCHEMA_VERSION",
    "SOURCE_MEMORYOS_V046_SCHEMA_VERSION",
    "canonical_digest",
    "issue_candidate_triple_gram_determinant_joint_coherence_compatibility_certificate",
]
