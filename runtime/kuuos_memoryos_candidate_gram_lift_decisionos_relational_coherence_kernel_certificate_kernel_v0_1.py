from __future__ import annotations

from hashlib import sha256
import json
from typing import Any, Mapping

SCHEMA_VERSION = (
    "kuuos.memoryos.candidate-gram-lift-decisionos-relational-coherence-"
    "kernel-certificate.v0.1"
)
SOURCE_MEMORYOS_V043_SCHEMA_VERSION = (
    "kuuos.memoryos.observer-relative-temporal-window-coherence-cocycle-"
    "composition-certificate.v0.1"
)
SOURCE_MEMORYOS_V044_SCHEMA_VERSION = (
    "kuuos.memoryos.observer-relative-coherence-quadratic-evidence-"
    "decisionos-handoff-certificate.v0.1"
)
MAXIMUM_CANDIDATE_COUNT = 128
MAXIMUM_HISTORY_COUNT = 128
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


def _string_ids(value: Any, field: str, maximum: int) -> list[str]:
    if (
        not isinstance(value, list)
        or not value
        or len(value) > maximum
        or len(value) != len(set(value))
        or any(not isinstance(item, str) or not item for item in value)
    ):
        raise ValueError(field + "_invalid")
    return list(value)


def _integer(value: Any, field: str, *, nonnegative: bool = False) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(field + "_invalid")
    if abs(value) > MAXIMUM_ABSOLUTE_INTEGER:
        raise ValueError(field + "_out_of_bounds")
    if nonnegative and value < 0:
        raise ValueError(field + "_negative")
    return value


def _kernel_entry_map(
    raw_entries: Any,
    *,
    history_ids: list[str],
    prefix: str,
) -> dict[tuple[str, str], tuple[int, int]]:
    if not isinstance(raw_entries, list):
        raise ValueError(prefix + "_kernel_entries_invalid")
    expected = {(row, column) for row in history_ids for column in history_ids}
    result: dict[tuple[str, str], tuple[int, int]] = {}
    for raw in raw_entries:
        if not isinstance(raw, Mapping):
            raise ValueError(prefix + "_kernel_entry_invalid")
        item = dict(raw)
        row = item.get("row_history_id")
        column = item.get("column_history_id")
        if row not in history_ids or column not in history_ids:
            raise ValueError(prefix + "_kernel_pair_invalid")
        pair = row, column
        if pair in result:
            raise ValueError(prefix + "_kernel_pair_duplicate")
        result[pair] = (
            _integer(item.get("real_numerator"), prefix + "_kernel_real"),
            _integer(item.get("imag_numerator"), prefix + "_kernel_imag"),
        )
    if set(result) != expected:
        raise ValueError(prefix + "_kernel_pair_support_mismatch")
    for row in history_ids:
        for column in history_ids:
            left = result[(row, column)]
            right = result[(column, row)]
            if left[0] != right[0] or left[1] != -right[1]:
                raise ValueError(prefix + "_kernel_not_hermitian")
    return result


def _normalize_source_memoryos_v043(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError("source_memoryos_v043_certificate_invalid")
    source = dict(value)
    if source.get("accepted") is not True:
        raise ValueError("source_memoryos_v043_not_accepted")
    if source.get("schema_version") != SOURCE_MEMORYOS_V043_SCHEMA_VERSION:
        raise ValueError("source_memoryos_v043_schema_invalid")
    digest = source.get("certificate_digest")
    if not isinstance(digest, str) or not digest:
        raise ValueError("source_memoryos_v043_certificate_digest_missing")
    observables = source.get("observables")
    governance_claims = source.get("governance_claims")
    if not isinstance(observables, Mapping) or not isinstance(governance_claims, Mapping):
        raise ValueError("source_memoryos_v043_surface_invalid")
    observables = dict(observables)
    expected_digest = canonical_digest(
        {
            "schema_version": SOURCE_MEMORYOS_V043_SCHEMA_VERSION,
            "input_digest": observables.get("input_digest"),
            "observables": observables,
            "governance_claims": dict(governance_claims),
        }
    )
    if digest != expected_digest:
        raise ValueError("source_memoryos_v043_certificate_digest_mismatch")
    for field in (
        "observer_translation_compatible",
        "refinement_coarsening_consistent",
        "cocycle_direct_composition_consistent",
        "source_v042_trajectory_exact",
        "composition_associative",
        "all_composed_steps_hermitian",
        "all_composed_diagonals_preserved",
        "all_composed_steps_psd_by_diagonal_phase_congruence",
        "all_history_pair_support_retained",
    ):
        if observables.get(field) is not True:
            raise ValueError("source_memoryos_v043_required_" + field)
    for field in (
        "history_pruning_performed",
        "history_ranking_performed",
        "representative_history_selected",
        "plan_selection_performed",
        "decision_commit_performed",
        "activation_performed",
        "execution_permission",
        "persistent_world_state_mutated",
        "verification_result_claimed",
        "truth_authority_granted",
    ):
        if observables.get(field) is not False:
            raise ValueError("source_memoryos_v043_forbidden_" + field)
    history_ids = _string_ids(
        observables.get("retained_history_ids"),
        "source_memoryos_v043_history_ids",
        MAXIMUM_HISTORY_COUNT,
    )
    raw_trajectory = observables.get("refined_final_trajectory")
    if (
        not isinstance(raw_trajectory, list)
        or not raw_trajectory
        or len(raw_trajectory) > MAXIMUM_DEPHASING_STEP_COUNT
    ):
        raise ValueError("source_memoryos_v043_trajectory_invalid")
    trajectory: list[dict[str, Any]] = []
    for index, raw_step in enumerate(raw_trajectory):
        if not isinstance(raw_step, Mapping):
            raise ValueError("source_memoryos_v043_step_invalid")
        step = dict(raw_step)
        if step.get("kernel_hermitian") is not True:
            raise ValueError("source_memoryos_v043_step_not_hermitian")
        if step.get("positive_semidefinite_by_diagonal_phase_congruence") is not True:
            raise ValueError("source_memoryos_v043_step_psd_witness_missing")
        denominator = _integer(
            step.get("kernel_entry_denominator"),
            "source_memoryos_v043_denominator",
        )
        if denominator <= 0:
            raise ValueError("source_memoryos_v043_denominator_nonpositive")
        trajectory.append(
            {
                "step_index": index,
                "dephasing_numerator": _integer(
                    step.get("dephasing_numerator"),
                    "source_memoryos_v043_dephasing_numerator",
                    nonnegative=True,
                ),
                "kernel_entry_denominator": denominator,
                "entries": _kernel_entry_map(
                    step.get("kernel_entries"),
                    history_ids=history_ids,
                    prefix="source_memoryos_v043",
                ),
            }
        )
    return {
        "certificate_digest": digest,
        "observables": observables,
        "history_ids": history_ids,
        "trajectory": trajectory,
    }


def _normalize_source_memoryos_v044(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError("source_memoryos_v044_certificate_invalid")
    source = dict(value)
    if source.get("accepted") is not True:
        raise ValueError("source_memoryos_v044_not_accepted")
    if source.get("schema_version") != SOURCE_MEMORYOS_V044_SCHEMA_VERSION:
        raise ValueError("source_memoryos_v044_schema_invalid")
    digest = source.get("certificate_digest")
    if not isinstance(digest, str) or not digest:
        raise ValueError("source_memoryos_v044_certificate_digest_missing")
    unsigned = dict(source)
    unsigned.pop("certificate_digest", None)
    if canonical_digest(unsigned) != digest:
        raise ValueError("source_memoryos_v044_certificate_digest_mismatch")
    observables = source.get("observables")
    if not isinstance(observables, Mapping):
        raise ValueError("source_memoryos_v044_observables_invalid")
    observables = dict(observables)
    for field in (
        "all_quadratic_evidence_nonnegative_by_psd",
        "all_quadratic_evidence_real_by_hermitian_symmetry",
        "all_decision_candidates_retained",
        "decisionos_candidate_order_preserved",
        "relational_frontier_preserved",
        "required_review_set_preserved",
        "dissent_visibility_preserved",
        "minority_visibility_preserved",
        "coherence_evidence_used_as_advisory_only",
        "coherence_contrast_not_used_as_scalar_utility",
        "future_only",
        "read_only",
    ):
        if observables.get(field) is not True:
            raise ValueError("source_memoryos_v044_required_" + field)
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
        "source_decisionos_v06_mutated",
        "persistent_world_state_mutated",
        "verification_result_claimed",
        "truth_authority_granted",
    ):
        if observables.get(field) is not False:
            raise ValueError("source_memoryos_v044_forbidden_" + field)
    candidate_ids = _string_ids(
        observables.get("retained_decision_candidate_ids"),
        "source_memoryos_v044_candidate_ids",
        MAXIMUM_CANDIDATE_COUNT,
    )
    history_ids = _string_ids(
        observables.get("retained_history_ids"),
        "source_memoryos_v044_history_ids",
        MAXIMUM_HISTORY_COUNT,
    )
    raw_couplings = observables.get("candidate_history_couplings")
    if not isinstance(raw_couplings, list) or len(raw_couplings) != len(candidate_ids):
        raise ValueError("source_memoryos_v044_couplings_incomplete")
    coupling_map: dict[str, dict[str, int]] = {}
    for raw in raw_couplings:
        if not isinstance(raw, Mapping):
            raise ValueError("source_memoryos_v044_coupling_invalid")
        item = dict(raw)
        candidate_id = item.get("candidate_id")
        coefficients = item.get("history_coefficients")
        if candidate_id not in candidate_ids or candidate_id in coupling_map:
            raise ValueError("source_memoryos_v044_coupling_candidate_invalid")
        if not isinstance(coefficients, Mapping) or set(coefficients) != set(history_ids):
            raise ValueError("source_memoryos_v044_coupling_history_support_mismatch")
        normalized: dict[str, int] = {}
        for history_id in history_ids:
            normalized[history_id] = _integer(
                coefficients[history_id],
                "source_memoryos_v044_coupling_coefficient",
            )
        if not any(normalized.values()):
            raise ValueError("source_memoryos_v044_zero_coupling_forbidden")
        coupling_map[candidate_id] = normalized
    if set(coupling_map) != set(candidate_ids):
        raise ValueError("source_memoryos_v044_coupling_candidate_support_mismatch")
    raw_records = observables.get("candidate_quadratic_evidence_records")
    if not isinstance(raw_records, list) or len(raw_records) != len(candidate_ids):
        raise ValueError("source_memoryos_v044_evidence_records_incomplete")
    evidence_map: dict[str, list[dict[str, int]]] = {}
    for raw in raw_records:
        if not isinstance(raw, Mapping):
            raise ValueError("source_memoryos_v044_evidence_record_invalid")
        item = dict(raw)
        candidate_id = item.get("candidate_id")
        trajectory = item.get("quadratic_evidence_trajectory")
        if candidate_id not in candidate_ids or candidate_id in evidence_map:
            raise ValueError("source_memoryos_v044_evidence_candidate_invalid")
        if not isinstance(trajectory, list) or not trajectory:
            raise ValueError("source_memoryos_v044_evidence_trajectory_invalid")
        normalized_trajectory: list[dict[str, int]] = []
        for index, raw_step in enumerate(trajectory):
            if not isinstance(raw_step, Mapping):
                raise ValueError("source_memoryos_v044_evidence_step_invalid")
            step = dict(raw_step)
            if step.get("step_index") != index:
                raise ValueError("source_memoryos_v044_evidence_step_index_invalid")
            if step.get("nonnegative_psd_witness") is not True:
                raise ValueError("source_memoryos_v044_evidence_psd_witness_missing")
            if step.get("real_valued_hermitian_witness") is not True:
                raise ValueError("source_memoryos_v044_evidence_real_witness_missing")
            imag = _integer(
                step.get("evidence_imag_numerator"),
                "source_memoryos_v044_evidence_imag",
            )
            if imag != 0:
                raise ValueError("source_memoryos_v044_evidence_imag_nonzero")
            denominator = _integer(
                step.get("evidence_denominator"),
                "source_memoryos_v044_evidence_denominator",
            )
            if denominator <= 0:
                raise ValueError("source_memoryos_v044_evidence_denominator_nonpositive")
            normalized_trajectory.append(
                {
                    "step_index": index,
                    "dephasing_numerator": _integer(
                        step.get("dephasing_numerator"),
                        "source_memoryos_v044_evidence_dephasing_numerator",
                        nonnegative=True,
                    ),
                    "real_numerator": _integer(
                        step.get("evidence_real_numerator"),
                        "source_memoryos_v044_evidence_real",
                        nonnegative=True,
                    ),
                    "denominator": denominator,
                }
            )
        evidence_map[candidate_id] = normalized_trajectory
    if set(evidence_map) != set(candidate_ids):
        raise ValueError("source_memoryos_v044_evidence_candidate_support_mismatch")
    return {
        "certificate_digest": digest,
        "observables": observables,
        "candidate_ids": candidate_ids,
        "history_ids": history_ids,
        "coupling_map": coupling_map,
        "evidence_map": evidence_map,
    }


def _candidate_pair_entry(
    *,
    history_ids: list[str],
    history_entries: Mapping[tuple[str, str], tuple[int, int]],
    left_coefficients: Mapping[str, int],
    right_coefficients: Mapping[str, int],
) -> tuple[int, int]:
    real = 0
    imag = 0
    for row in history_ids:
        for column in history_ids:
            weight = left_coefficients[row] * right_coefficients[column]
            source_real, source_imag = history_entries[(row, column)]
            real += weight * source_real
            imag += weight * source_imag
    return real, imag


def issue_candidate_gram_lift_decisionos_relational_coherence_kernel_certificate(
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    if not isinstance(payload, Mapping):
        return _blocked("payload_invalid")
    blockers: list[str] = []
    if payload.get("schema_version") != SCHEMA_VERSION:
        blockers.append("schema_version_invalid")
    try:
        source_v043 = _normalize_source_memoryos_v043(
            payload.get("source_memoryos_v043_certificate")
        )
        source_v044 = _normalize_source_memoryos_v044(
            payload.get("source_memoryos_v044_certificate")
        )
    except ValueError as exc:
        return _blocked(*(blockers + [str(exc)]))

    v044_obs = source_v044["observables"]
    v043_obs = source_v043["observables"]
    if (
        v044_obs.get("source_memoryos_v043_certificate_digest")
        != source_v043["certificate_digest"]
    ):
        blockers.append("source_v044_v043_certificate_binding_mismatch")
    if (
        v044_obs.get("source_memoryos_v043_conditioned_kernel_digest")
        != v043_obs.get("refined_final_kernel_digest")
    ):
        blockers.append("source_v044_v043_kernel_binding_mismatch")
    if source_v044["history_ids"] != source_v043["history_ids"]:
        blockers.append("source_v044_v043_history_support_mismatch")
    if len(next(iter(source_v044["evidence_map"].values()))) != len(source_v043["trajectory"]):
        blockers.append("source_v044_v043_trajectory_length_mismatch")

    candidate_ids = source_v044["candidate_ids"]
    history_ids = source_v043["history_ids"]
    candidate_kernel_trajectory: list[dict[str, Any]] = []
    pair_support_complete = True
    all_hermitian = True
    all_diagonals_match = True
    all_psd_by_gram_lift = True

    for source_step in source_v043["trajectory"]:
        step_index = source_step["step_index"]
        entries: list[dict[str, Any]] = []
        entry_map: dict[tuple[str, str], tuple[int, int]] = {}
        for left_id in candidate_ids:
            for right_id in candidate_ids:
                real, imag = _candidate_pair_entry(
                    history_ids=history_ids,
                    history_entries=source_step["entries"],
                    left_coefficients=source_v044["coupling_map"][left_id],
                    right_coefficients=source_v044["coupling_map"][right_id],
                )
                entry_map[(left_id, right_id)] = real, imag
                entries.append(
                    {
                        "left_candidate_id": left_id,
                        "right_candidate_id": right_id,
                        "real_numerator": real,
                        "imag_numerator": imag,
                    }
                )
        expected_pair_count = len(candidate_ids) * len(candidate_ids)
        step_pair_support = len(entries) == expected_pair_count
        step_hermitian = all(
            entry_map[(left_id, right_id)][0]
            == entry_map[(right_id, left_id)][0]
            and entry_map[(left_id, right_id)][1]
            == -entry_map[(right_id, left_id)][1]
            for left_id in candidate_ids
            for right_id in candidate_ids
        )
        step_diagonals_match = True
        for candidate_id in candidate_ids:
            source_evidence = source_v044["evidence_map"][candidate_id][step_index]
            diagonal = entry_map[(candidate_id, candidate_id)]
            if (
                diagonal[0] != source_evidence["real_numerator"]
                or diagonal[1] != 0
                or source_step["kernel_entry_denominator"]
                != source_evidence["denominator"]
                or source_step["dephasing_numerator"]
                != source_evidence["dephasing_numerator"]
            ):
                step_diagonals_match = False
        pair_support_complete = pair_support_complete and step_pair_support
        all_hermitian = all_hermitian and step_hermitian
        all_diagonals_match = all_diagonals_match and step_diagonals_match
        candidate_kernel_trajectory.append(
            {
                "step_index": step_index,
                "dephasing_numerator": source_step["dephasing_numerator"],
                "kernel_entry_denominator": source_step["kernel_entry_denominator"],
                "candidate_kernel_entries": entries,
                "candidate_pair_support_complete": step_pair_support,
                "candidate_kernel_hermitian": step_hermitian,
                "candidate_kernel_positive_semidefinite_by_gram_lift": True,
                "candidate_kernel_diagonal_matches_v044_quadratic_evidence": step_diagonals_match,
            }
        )

    pair_records: list[dict[str, Any]] = []
    for left_index, left_id in enumerate(candidate_ids):
        for right_id in candidate_ids[left_index + 1 :]:
            trajectory: list[dict[str, Any]] = []
            for step in candidate_kernel_trajectory:
                item = next(
                    entry
                    for entry in step["candidate_kernel_entries"]
                    if entry["left_candidate_id"] == left_id
                    and entry["right_candidate_id"] == right_id
                )
                trajectory.append(
                    {
                        "step_index": step["step_index"],
                        "dephasing_numerator": step["dephasing_numerator"],
                        "real_numerator": item["real_numerator"],
                        "imag_numerator": item["imag_numerator"],
                        "denominator": step["kernel_entry_denominator"],
                    }
                )
            pair_records.append(
                {
                    "left_candidate_id": left_id,
                    "right_candidate_id": right_id,
                    "pair_coherence_trajectory": trajectory,
                    "full_coherence_real_numerator": trajectory[0]["real_numerator"],
                    "fully_dephased_real_numerator": trajectory[-1]["real_numerator"],
                    "pair_coherence_contrast_numerator": trajectory[0]["real_numerator"]
                    - trajectory[-1]["real_numerator"],
                    "pair_retained": True,
                }
            )

    input_digest = canonical_digest(
        {
            "schema_version": SCHEMA_VERSION,
            "source_memoryos_v043_certificate_digest": source_v043[
                "certificate_digest"
            ],
            "source_memoryos_v044_certificate_digest": source_v044[
                "certificate_digest"
            ],
            "candidate_ids": candidate_ids,
            "history_ids": history_ids,
            "candidate_history_couplings": v044_obs["candidate_history_couplings"],
        }
    )
    candidate_kernel_digest = canonical_digest(candidate_kernel_trajectory)
    observables = {
        "input_digest": input_digest,
        "source_memoryos_v043_certificate_digest": source_v043["certificate_digest"],
        "source_memoryos_v043_conditioned_kernel_digest": v043_obs[
            "refined_final_kernel_digest"
        ],
        "source_memoryos_v044_certificate_digest": source_v044["certificate_digest"],
        "source_memoryos_v044_quadratic_evidence_input_digest": v044_obs[
            "input_digest"
        ],
        "retained_history_ids": history_ids,
        "retained_decision_candidate_ids": candidate_ids,
        "candidate_history_couplings": v044_obs["candidate_history_couplings"],
        "candidate_gram_kernel_trajectory": candidate_kernel_trajectory,
        "candidate_pair_coherence_records": pair_records,
        "candidate_gram_kernel_digest": candidate_kernel_digest,
        "all_candidate_pair_support_retained": pair_support_complete,
        "all_candidate_kernels_hermitian": all_hermitian,
        "all_candidate_kernels_psd_by_gram_lift": all_psd_by_gram_lift,
        "all_candidate_diagonals_match_v044_quadratic_evidence": all_diagonals_match,
        "all_decision_candidates_retained": True,
        "all_planos_histories_retained": True,
        "source_relational_frontier_candidate_ids": v044_obs[
            "source_relational_frontier_candidate_ids"
        ],
        "source_required_review_candidate_ids": v044_obs[
            "source_required_review_candidate_ids"
        ],
        "source_dissent_review_candidate_ids": v044_obs[
            "source_dissent_review_candidate_ids"
        ],
        "source_minority_protection_candidate_ids": v044_obs[
            "source_minority_protection_candidate_ids"
        ],
        "relational_frontier_preserved": True,
        "required_review_set_preserved": True,
        "dissent_visibility_preserved": True,
        "minority_visibility_preserved": True,
        "candidate_pair_coherence_advisory_only": True,
        "candidate_gram_kernel_not_relational_order": True,
        "candidate_ranking_performed": False,
        "candidate_pruning_performed": False,
        "candidate_selection_performed": False,
        "decision_commit_performed": False,
        "decision_receipt_issued": False,
        "plan_synthesis_performed": False,
        "activation_performed": False,
        "execution_permission": False,
        "source_memoryos_v043_mutated": False,
        "source_memoryos_v044_mutated": False,
        "source_decisionos_v06_mutated": False,
        "persistent_world_state_mutated": False,
        "verification_result_claimed": False,
        "truth_authority_granted": False,
        "future_only": True,
        "read_only": True,
    }
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
    "SOURCE_MEMORYOS_V043_SCHEMA_VERSION",
    "SOURCE_MEMORYOS_V044_SCHEMA_VERSION",
    "canonical_digest",
    "issue_candidate_gram_lift_decisionos_relational_coherence_kernel_certificate",
]
