from __future__ import annotations

from hashlib import sha256
import json
from math import gcd
from typing import Any, Mapping

SCHEMA_VERSION = (
    "kuuos.memoryos.candidate-pair-cauchy-schwarz-relational-coherence-"
    "envelope-certificate.v0.1"
)
SOURCE_MEMORYOS_V045_SCHEMA_VERSION = (
    "kuuos.memoryos.candidate-gram-lift-decisionos-relational-coherence-"
    "kernel-certificate.v0.1"
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


def _candidate_entry_map(
    raw_entries: Any,
    *,
    candidate_ids: list[str],
    prefix: str,
) -> dict[tuple[str, str], tuple[int, int]]:
    if not isinstance(raw_entries, list):
        raise ValueError(prefix + "_entries_invalid")
    expected_pairs = {
        (left_id, right_id)
        for left_id in candidate_ids
        for right_id in candidate_ids
    }
    result: dict[tuple[str, str], tuple[int, int]] = {}
    for raw in raw_entries:
        if not isinstance(raw, Mapping):
            raise ValueError(prefix + "_entry_invalid")
        item = dict(raw)
        left_id = item.get("left_candidate_id")
        right_id = item.get("right_candidate_id")
        if left_id not in candidate_ids or right_id not in candidate_ids:
            raise ValueError(prefix + "_pair_invalid")
        pair = left_id, right_id
        if pair in result:
            raise ValueError(prefix + "_pair_duplicate")
        result[pair] = (
            _integer(item.get("real_numerator"), prefix + "_real"),
            _integer(item.get("imag_numerator"), prefix + "_imag"),
        )
    if set(result) != expected_pairs:
        raise ValueError(prefix + "_pair_support_mismatch")
    for left_id in candidate_ids:
        for right_id in candidate_ids:
            left = result[(left_id, right_id)]
            right = result[(right_id, left_id)]
            if left[0] != right[0] or left[1] != -right[1]:
                raise ValueError(prefix + "_not_hermitian")
    for candidate_id in candidate_ids:
        diagonal = result[(candidate_id, candidate_id)]
        if diagonal[1] != 0:
            raise ValueError(prefix + "_diagonal_imaginary")
        if diagonal[0] < 0:
            raise ValueError(prefix + "_diagonal_negative")
    return result


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
        raise ValueError("source_memoryos_v045_" + field + "_invalid")
    return list(value)


def _normalize_source_memoryos_v045(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError("source_memoryos_v045_certificate_invalid")
    source = dict(value)
    if source.get("accepted") is not True:
        raise ValueError("source_memoryos_v045_not_accepted")
    if source.get("schema_version") != SOURCE_MEMORYOS_V045_SCHEMA_VERSION:
        raise ValueError("source_memoryos_v045_schema_invalid")
    digest = source.get("certificate_digest")
    if not isinstance(digest, str) or not digest:
        raise ValueError("source_memoryos_v045_certificate_digest_missing")
    unsigned = dict(source)
    unsigned.pop("certificate_digest", None)
    if canonical_digest(unsigned) != digest:
        raise ValueError("source_memoryos_v045_certificate_digest_mismatch")
    observables = source.get("observables")
    if not isinstance(observables, Mapping):
        raise ValueError("source_memoryos_v045_observables_invalid")
    observables = dict(observables)
    for field in (
        "all_candidate_pair_support_retained",
        "all_candidate_kernels_hermitian",
        "all_candidate_kernels_psd_by_gram_lift",
        "all_candidate_diagonals_match_v044_quadratic_evidence",
        "all_decision_candidates_retained",
        "all_planos_histories_retained",
        "relational_frontier_preserved",
        "required_review_set_preserved",
        "dissent_visibility_preserved",
        "minority_visibility_preserved",
        "candidate_pair_coherence_advisory_only",
        "candidate_gram_kernel_not_relational_order",
        "future_only",
        "read_only",
    ):
        if observables.get(field) is not True:
            raise ValueError("source_memoryos_v045_required_" + field)
    for field in (
        "candidate_ranking_performed",
        "candidate_pruning_performed",
        "candidate_selection_performed",
        "decision_commit_performed",
        "decision_receipt_issued",
        "plan_synthesis_performed",
        "activation_performed",
        "execution_permission",
        "source_memoryos_v043_mutated",
        "source_memoryos_v044_mutated",
        "source_decisionos_v06_mutated",
        "persistent_world_state_mutated",
        "verification_result_claimed",
        "truth_authority_granted",
    ):
        if observables.get(field) is not False:
            raise ValueError("source_memoryos_v045_forbidden_" + field)

    candidate_ids = _string_ids(
        observables.get("retained_decision_candidate_ids"),
        "source_memoryos_v045_candidate_ids",
    )
    raw_trajectory = observables.get("candidate_gram_kernel_trajectory")
    if (
        not isinstance(raw_trajectory, list)
        or not raw_trajectory
        or len(raw_trajectory) > MAXIMUM_DEPHASING_STEP_COUNT
    ):
        raise ValueError("source_memoryos_v045_trajectory_invalid")
    kernel_digest = observables.get("candidate_gram_kernel_digest")
    if not isinstance(kernel_digest, str) or not kernel_digest:
        raise ValueError("source_memoryos_v045_kernel_digest_missing")
    if canonical_digest(raw_trajectory) != kernel_digest:
        raise ValueError("source_memoryos_v045_kernel_digest_mismatch")

    trajectory: list[dict[str, Any]] = []
    previous_dephasing_numerator: int | None = None
    for index, raw_step in enumerate(raw_trajectory):
        if not isinstance(raw_step, Mapping):
            raise ValueError("source_memoryos_v045_step_invalid")
        step = dict(raw_step)
        if step.get("step_index") != index:
            raise ValueError("source_memoryos_v045_step_index_invalid")
        for field in (
            "candidate_pair_support_complete",
            "candidate_kernel_hermitian",
            "candidate_kernel_positive_semidefinite_by_gram_lift",
            "candidate_kernel_diagonal_matches_v044_quadratic_evidence",
        ):
            if step.get(field) is not True:
                raise ValueError("source_memoryos_v045_step_required_" + field)
        denominator = _integer(
            step.get("kernel_entry_denominator"),
            "source_memoryos_v045_denominator",
        )
        if denominator <= 0:
            raise ValueError("source_memoryos_v045_denominator_nonpositive")
        dephasing_numerator = _integer(
            step.get("dephasing_numerator"),
            "source_memoryos_v045_dephasing_numerator",
            nonnegative=True,
        )
        if (
            previous_dephasing_numerator is not None
            and dephasing_numerator >= previous_dephasing_numerator
        ):
            raise ValueError("source_memoryos_v045_dephasing_not_strictly_decreasing")
        previous_dephasing_numerator = dephasing_numerator
        trajectory.append(
            {
                "step_index": index,
                "dephasing_numerator": dephasing_numerator,
                "kernel_entry_denominator": denominator,
                "entries": _candidate_entry_map(
                    step.get("candidate_kernel_entries"),
                    candidate_ids=candidate_ids,
                    prefix="source_memoryos_v045",
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
    source_v043_digest = observables.get("source_memoryos_v043_certificate_digest")
    source_v044_digest = observables.get("source_memoryos_v044_certificate_digest")
    if not isinstance(source_v043_digest, str) or not source_v043_digest:
        raise ValueError("source_memoryos_v045_v043_digest_missing")
    if not isinstance(source_v044_digest, str) or not source_v044_digest:
        raise ValueError("source_memoryos_v045_v044_digest_missing")
    return {
        "certificate_digest": digest,
        "observables": observables,
        "candidate_ids": candidate_ids,
        "trajectory": trajectory,
        "kernel_digest": kernel_digest,
        "source_memoryos_v043_certificate_digest": source_v043_digest,
        "source_memoryos_v044_certificate_digest": source_v044_digest,
        **review_fields,
    }


def _normalized_fraction(numerator: int, denominator: int) -> tuple[int, int]:
    common = gcd(numerator, denominator)
    return numerator // common, denominator // common


def issue_candidate_pair_cauchy_schwarz_relational_coherence_envelope_certificate(
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    if not isinstance(payload, Mapping):
        return _blocked("payload_invalid")
    blockers: list[str] = []
    if payload.get("schema_version") != SCHEMA_VERSION:
        blockers.append("schema_version_invalid")
    try:
        source = _normalize_source_memoryos_v045(
            payload.get("source_memoryos_v045_certificate")
        )
    except ValueError as exc:
        return _blocked(*(blockers + [str(exc)]))

    candidate_ids = source["candidate_ids"]
    envelope_trajectory: list[dict[str, Any]] = []
    all_pair_support = True
    all_cauchy_schwarz = True
    all_normalized_bounded = True
    all_zero_diagonal_pairs_zero = True
    all_diagonals_nonnegative = True

    for source_step in source["trajectory"]:
        entries = source_step["entries"]
        pair_records: list[dict[str, Any]] = []
        for left_id in candidate_ids:
            for right_id in candidate_ids:
                real_numerator, imag_numerator = entries[(left_id, right_id)]
                left_diagonal = entries[(left_id, left_id)][0]
                right_diagonal = entries[(right_id, right_id)][0]
                coherence_magnitude_square = (
                    real_numerator * real_numerator
                    + imag_numerator * imag_numerator
                )
                diagonal_product = left_diagonal * right_diagonal
                determinant_margin = diagonal_product - coherence_magnitude_square
                cauchy_schwarz_holds = determinant_margin >= 0
                zero_diagonal_pair = left_diagonal == 0 or right_diagonal == 0
                zero_diagonal_forces_zero = (
                    not zero_diagonal_pair or coherence_magnitude_square == 0
                )
                if zero_diagonal_pair:
                    normalized_numerator = 0
                    normalized_denominator = 1
                else:
                    normalized_numerator, normalized_denominator = _normalized_fraction(
                        coherence_magnitude_square,
                        diagonal_product,
                    )
                normalized_at_most_one = (
                    normalized_numerator <= normalized_denominator
                )
                pair_records.append(
                    {
                        "left_candidate_id": left_id,
                        "right_candidate_id": right_id,
                        "source_real_numerator": real_numerator,
                        "source_imag_numerator": imag_numerator,
                        "source_kernel_entry_denominator": source_step[
                            "kernel_entry_denominator"
                        ],
                        "left_diagonal_numerator": left_diagonal,
                        "right_diagonal_numerator": right_diagonal,
                        "coherence_magnitude_square_numerator": coherence_magnitude_square,
                        "coherence_magnitude_square_denominator": source_step[
                            "kernel_entry_denominator"
                        ]
                        ** 2,
                        "diagonal_product_numerator": diagonal_product,
                        "diagonal_product_denominator": source_step[
                            "kernel_entry_denominator"
                        ]
                        ** 2,
                        "determinant_margin_numerator": determinant_margin,
                        "determinant_margin_denominator": source_step[
                            "kernel_entry_denominator"
                        ]
                        ** 2,
                        "cauchy_schwarz_bound_holds": cauchy_schwarz_holds,
                        "zero_diagonal_pair": zero_diagonal_pair,
                        "zero_diagonal_forces_zero_coherence": zero_diagonal_forces_zero,
                        "normalized_coherence_square_numerator": normalized_numerator,
                        "normalized_coherence_square_denominator": normalized_denominator,
                        "normalized_coherence_square_at_most_one": normalized_at_most_one,
                        "pair_retained": True,
                    }
                )
                all_cauchy_schwarz = all_cauchy_schwarz and cauchy_schwarz_holds
                all_normalized_bounded = (
                    all_normalized_bounded and normalized_at_most_one
                )
                all_zero_diagonal_pairs_zero = (
                    all_zero_diagonal_pairs_zero and zero_diagonal_forces_zero
                )
                all_diagonals_nonnegative = (
                    all_diagonals_nonnegative
                    and left_diagonal >= 0
                    and right_diagonal >= 0
                )
        step_pair_support = len(pair_records) == len(candidate_ids) ** 2
        all_pair_support = all_pair_support and step_pair_support
        envelope_trajectory.append(
            {
                "step_index": source_step["step_index"],
                "dephasing_numerator": source_step["dephasing_numerator"],
                "source_kernel_entry_denominator": source_step[
                    "kernel_entry_denominator"
                ],
                "candidate_pair_envelopes": pair_records,
                "ordered_candidate_pair_support_complete": step_pair_support,
                "all_step_cauchy_schwarz_bounds_hold": all(
                    item["cauchy_schwarz_bound_holds"] for item in pair_records
                ),
                "all_step_normalized_coherence_squares_at_most_one": all(
                    item["normalized_coherence_square_at_most_one"]
                    for item in pair_records
                ),
                "all_step_zero_diagonal_pairs_have_zero_coherence": all(
                    item["zero_diagonal_forces_zero_coherence"]
                    for item in pair_records
                ),
            }
        )

    input_digest = canonical_digest(
        {
            "schema_version": SCHEMA_VERSION,
            "source_memoryos_v045_certificate_digest": source[
                "certificate_digest"
            ],
            "source_candidate_gram_kernel_digest": source["kernel_digest"],
            "candidate_ids": candidate_ids,
        }
    )
    envelope_digest = canonical_digest(envelope_trajectory)
    observables = {
        "input_digest": input_digest,
        "source_memoryos_v045_certificate_digest": source["certificate_digest"],
        "source_memoryos_v045_candidate_gram_kernel_digest": source[
            "kernel_digest"
        ],
        "source_memoryos_v043_certificate_digest": source[
            "source_memoryos_v043_certificate_digest"
        ],
        "source_memoryos_v044_certificate_digest": source[
            "source_memoryos_v044_certificate_digest"
        ],
        "retained_decision_candidate_ids": candidate_ids,
        "candidate_pair_cauchy_schwarz_envelope_trajectory": envelope_trajectory,
        "candidate_pair_cauchy_schwarz_envelope_digest": envelope_digest,
        "all_ordered_candidate_pair_support_retained": all_pair_support,
        "all_cauchy_schwarz_bounds_hold": all_cauchy_schwarz,
        "all_normalized_coherence_squares_bounded_by_one": all_normalized_bounded,
        "all_zero_diagonal_pairs_have_zero_coherence": all_zero_diagonal_pairs_zero,
        "all_candidate_diagonals_nonnegative": all_diagonals_nonnegative,
        "source_candidate_gram_kernel_exact": True,
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
        "normalized_coherence_advisory_only": True,
        "normalized_coherence_not_scalar_utility": True,
        "off_diagonal_sign_not_preference": True,
        "candidate_ranking_performed": False,
        "candidate_pruning_performed": False,
        "candidate_selection_performed": False,
        "decision_commit_performed": False,
        "decision_receipt_issued": False,
        "plan_synthesis_performed": False,
        "activation_performed": False,
        "execution_permission": False,
        "source_memoryos_v045_mutated": False,
        "source_decisionos_v06_mutated": False,
        "persistent_world_state_mutated": False,
        "verification_result_claimed": False,
        "truth_authority_granted": False,
        "future_only": True,
        "read_only": True,
    }
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
    "SOURCE_MEMORYOS_V045_SCHEMA_VERSION",
    "canonical_digest",
    "issue_candidate_pair_cauchy_schwarz_relational_coherence_envelope_certificate",
]
