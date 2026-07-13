from __future__ import annotations

from hashlib import sha256
import json
from typing import Any, Mapping

SCHEMA_VERSION = (
    "kuuos.memoryos.observer-relative-coherence-quadratic-evidence-"
    "decisionos-handoff-certificate.v0.1"
)
SOURCE_MEMORYOS_V043_SCHEMA_VERSION = (
    "kuuos.memoryos.observer-relative-temporal-window-coherence-cocycle-"
    "composition-certificate.v0.1"
)
SOURCE_DECISIONOS_VERSION = "v0.6"
SOURCE_DECISIONOS_STATUS = "DECISIONOS_WORLD_CONDITIONED_RELATIONAL_DELIBERATION_READY"
MAX_ABS_COEFFICIENT = 64


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


def _entry_map(step: Mapping[str, Any]) -> dict[tuple[str, str], tuple[int, int]]:
    result: dict[tuple[str, str], tuple[int, int]] = {}
    for item in step.get("kernel_entries", []):
        if not isinstance(item, Mapping):
            raise ValueError("source_memoryos_v043_kernel_entry_invalid")
        row = item.get("row_history_id")
        column = item.get("column_history_id")
        real = item.get("real_numerator")
        imag = item.get("imag_numerator")
        if not isinstance(row, str) or not row or not isinstance(column, str) or not column:
            raise ValueError("source_memoryos_v043_kernel_pair_invalid")
        if not isinstance(real, int) or isinstance(real, bool):
            raise ValueError("source_memoryos_v043_kernel_real_invalid")
        if not isinstance(imag, int) or isinstance(imag, bool):
            raise ValueError("source_memoryos_v043_kernel_imag_invalid")
        pair = row, column
        if pair in result:
            raise ValueError("source_memoryos_v043_kernel_pair_duplicate")
        result[pair] = real, imag
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
    if not isinstance(observables, Mapping):
        raise ValueError("source_memoryos_v043_observables_invalid")
    observables = dict(observables)
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
    history_ids = observables.get("retained_history_ids")
    if (
        not isinstance(history_ids, list)
        or not history_ids
        or len(history_ids) != len(set(history_ids))
        or any(not isinstance(item, str) or not item for item in history_ids)
    ):
        raise ValueError("source_memoryos_v043_history_ids_invalid")
    trajectory = observables.get("refined_final_trajectory")
    if not isinstance(trajectory, list) or not trajectory:
        raise ValueError("source_memoryos_v043_trajectory_invalid")
    normalized_steps: list[dict[str, Any]] = []
    expected_pairs = {(row, column) for row in history_ids for column in history_ids}
    for index, raw_step in enumerate(trajectory):
        if not isinstance(raw_step, Mapping):
            raise ValueError("source_memoryos_v043_step_invalid")
        step = dict(raw_step)
        if step.get("kernel_hermitian") is not True:
            raise ValueError("source_memoryos_v043_step_not_hermitian")
        if step.get("positive_semidefinite_by_diagonal_phase_congruence") is not True:
            raise ValueError("source_memoryos_v043_step_psd_witness_missing")
        denominator = step.get("kernel_entry_denominator")
        numerator = step.get("dephasing_numerator")
        if not isinstance(denominator, int) or isinstance(denominator, bool) or denominator <= 0:
            raise ValueError("source_memoryos_v043_denominator_invalid")
        if not isinstance(numerator, int) or isinstance(numerator, bool) or numerator < 0:
            raise ValueError("source_memoryos_v043_dephasing_numerator_invalid")
        entries = _entry_map(step)
        if set(entries) != expected_pairs:
            raise ValueError("source_memoryos_v043_history_pair_support_mismatch")
        for row in history_ids:
            for column in history_ids:
                left = entries[(row, column)]
                right = entries[(column, row)]
                if left[0] != right[0] or left[1] != -right[1]:
                    raise ValueError("source_memoryos_v043_hermitian_entry_mismatch")
        normalized_steps.append(
            {
                "step_index": index,
                "dephasing_numerator": numerator,
                "kernel_entry_denominator": denominator,
                "entries": entries,
            }
        )
    return {
        "certificate_digest": digest,
        "observables": observables,
        "history_ids": list(history_ids),
        "trajectory": normalized_steps,
    }


def _normalize_source_decisionos_v06(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError("source_decisionos_v06_receipt_invalid")
    source = dict(value)
    if source.get("decisionos_version") != SOURCE_DECISIONOS_VERSION:
        raise ValueError("source_decisionos_v06_version_invalid")
    if source.get("status") != SOURCE_DECISIONOS_STATUS:
        raise ValueError("source_decisionos_v06_not_ready")
    digest = source.get("decisionos_relational_deliberation_receipt_digest")
    if not isinstance(digest, str) or not digest:
        raise ValueError("source_decisionos_v06_digest_missing")
    unsigned = dict(source)
    unsigned.pop("decisionos_relational_deliberation_receipt_digest", None)
    if canonical_digest(unsigned) != digest:
        raise ValueError("source_decisionos_v06_digest_mismatch")
    candidate_ids = source.get("all_candidate_ids")
    if (
        not isinstance(candidate_ids, list)
        or not candidate_ids
        or len(candidate_ids) != len(set(candidate_ids))
        or any(not isinstance(item, str) or not item for item in candidate_ids)
    ):
        raise ValueError("source_decisionos_v06_candidate_ids_invalid")
    records = source.get("candidate_deliberation_records")
    if not isinstance(records, list) or len(records) != len(candidate_ids):
        raise ValueError("source_decisionos_v06_records_incomplete")
    record_map: dict[str, dict[str, Any]] = {}
    for raw in records:
        if not isinstance(raw, Mapping):
            raise ValueError("source_decisionos_v06_record_invalid")
        item = dict(raw)
        candidate_id = item.get("candidate_id")
        if candidate_id not in candidate_ids or candidate_id in record_map:
            raise ValueError("source_decisionos_v06_record_candidate_invalid")
        record_map[candidate_id] = item
    if set(record_map) != set(candidate_ids):
        raise ValueError("source_decisionos_v06_record_support_mismatch")
    for field in (
        "all_candidates_considered",
        "candidate_identity_preserved",
        "retained_alternatives_preserved",
        "dissent_visibility_preserved",
        "minority_visibility_preserved",
        "decisionos_owns_selection",
        "persistent_world_state_unchanged",
        "history_read_only",
        "future_only",
    ):
        if source.get(field) is not True:
            raise ValueError("source_decisionos_v06_required_" + field)
    for field in (
        "selection_authority_granted_by_deliberation",
        "decision_selection_performed",
        "decision_receipt_issued",
        "plan_synthesis_performed",
        "active_now",
        "execution_permission",
    ):
        if source.get(field) is not False:
            raise ValueError("source_decisionos_v06_forbidden_" + field)
    if source.get("selected_candidate_id") != "":
        raise ValueError("source_decisionos_v06_selected_candidate_forbidden")
    return {
        "receipt": source,
        "receipt_digest": digest,
        "candidate_ids": list(candidate_ids),
        "record_map": record_map,
    }


def _normalize_couplings(
    value: Any,
    *,
    candidate_ids: list[str],
    history_ids: list[str],
) -> list[dict[str, Any]]:
    if not isinstance(value, list) or len(value) != len(candidate_ids):
        raise ValueError("candidate_history_couplings_incomplete")
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for raw in value:
        if not isinstance(raw, Mapping):
            raise ValueError("candidate_history_coupling_invalid")
        item = dict(raw)
        if set(item) != {"candidate_id", "history_coefficients"}:
            raise ValueError("candidate_history_coupling_schema_invalid")
        candidate_id = item.get("candidate_id")
        coefficients = item.get("history_coefficients")
        if candidate_id not in candidate_ids or candidate_id in seen:
            raise ValueError("candidate_history_coupling_candidate_invalid")
        if not isinstance(coefficients, Mapping) or set(coefficients) != set(history_ids):
            raise ValueError("candidate_history_coefficient_support_mismatch")
        normalized: dict[str, int] = {}
        for history_id in history_ids:
            coefficient = coefficients[history_id]
            if (
                not isinstance(coefficient, int)
                or isinstance(coefficient, bool)
                or abs(coefficient) > MAX_ABS_COEFFICIENT
            ):
                raise ValueError("candidate_history_coefficient_invalid")
            normalized[history_id] = coefficient
        if not any(normalized.values()):
            raise ValueError("candidate_history_coupling_zero_vector_forbidden")
        seen.add(candidate_id)
        result.append(
            {
                "candidate_id": candidate_id,
                "history_coefficients": normalized,
            }
        )
    if seen != set(candidate_ids):
        raise ValueError("candidate_history_coupling_candidate_support_mismatch")
    return sorted(result, key=lambda item: item["candidate_id"])


def _quadratic_evidence(
    *,
    step: Mapping[str, Any],
    history_ids: list[str],
    coefficients: Mapping[str, int],
) -> tuple[int, int]:
    real = 0
    imag = 0
    entries = step["entries"]
    for row in history_ids:
        for column in history_ids:
            weight = coefficients[row] * coefficients[column]
            value = entries[(row, column)]
            real += weight * value[0]
            imag += weight * value[1]
    return real, imag


def issue_observer_relative_coherence_quadratic_evidence_decisionos_handoff_certificate(
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    if not isinstance(payload, Mapping):
        return _blocked("payload_invalid")
    blockers: list[str] = []
    if payload.get("schema_version") != SCHEMA_VERSION:
        blockers.append("schema_version_invalid")
    try:
        memory = _normalize_source_memoryos_v043(
            payload.get("source_memoryos_v043_certificate")
        )
        decision = _normalize_source_decisionos_v06(
            payload.get("source_decisionos_v06_receipt")
        )
        couplings = _normalize_couplings(
            payload.get("candidate_history_couplings"),
            candidate_ids=decision["candidate_ids"],
            history_ids=memory["history_ids"],
        )
    except ValueError as exc:
        blockers.append(str(exc))
        return _blocked(*blockers)

    evidence_records: list[dict[str, Any]] = []
    all_nonnegative = True
    all_imaginary_zero = True
    for coupling in couplings:
        candidate_id = coupling["candidate_id"]
        coefficients = coupling["history_coefficients"]
        trajectory: list[dict[str, Any]] = []
        for step in memory["trajectory"]:
            real, imag = _quadratic_evidence(
                step=step,
                history_ids=memory["history_ids"],
                coefficients=coefficients,
            )
            all_nonnegative = all_nonnegative and real >= 0
            all_imaginary_zero = all_imaginary_zero and imag == 0
            trajectory.append(
                {
                    "step_index": step["step_index"],
                    "dephasing_numerator": step["dephasing_numerator"],
                    "evidence_real_numerator": real,
                    "evidence_imag_numerator": imag,
                    "evidence_denominator": step["kernel_entry_denominator"],
                    "nonnegative_psd_witness": real >= 0,
                    "real_valued_hermitian_witness": imag == 0,
                }
            )
        source_record = decision["record_map"][candidate_id]
        evidence_records.append(
            {
                "candidate_id": candidate_id,
                "source_deliberation_classification": source_record[
                    "deliberation_classification"
                ],
                "source_relationally_reviewable": bool(
                    source_record["relationally_reviewable"]
                ),
                "source_required_review": candidate_id
                in decision["receipt"]["required_review_candidate_ids"],
                "history_coefficients": coefficients,
                "quadratic_evidence_trajectory": trajectory,
                "full_coherence_evidence_numerator": trajectory[0][
                    "evidence_real_numerator"
                ],
                "fully_dephased_evidence_numerator": trajectory[-1][
                    "evidence_real_numerator"
                ],
                "coherence_contrast_numerator": trajectory[0][
                    "evidence_real_numerator"
                ]
                - trajectory[-1]["evidence_real_numerator"],
                "candidate_retained": True,
            }
        )

    source = decision["receipt"]
    candidate_ids = decision["candidate_ids"]
    evidence_map = {item["candidate_id"]: item for item in evidence_records}
    positive_contrast = sorted(
        candidate_id
        for candidate_id in candidate_ids
        if evidence_map[candidate_id]["coherence_contrast_numerator"] > 0
    )
    zero_contrast = sorted(
        candidate_id
        for candidate_id in candidate_ids
        if evidence_map[candidate_id]["coherence_contrast_numerator"] == 0
    )
    negative_contrast = sorted(
        candidate_id
        for candidate_id in candidate_ids
        if evidence_map[candidate_id]["coherence_contrast_numerator"] < 0
    )
    input_digest = canonical_digest(
        {
            "schema_version": SCHEMA_VERSION,
            "source_memoryos_v043_certificate_digest": memory["certificate_digest"],
            "source_decisionos_v06_receipt_digest": decision["receipt_digest"],
            "candidate_history_couplings": couplings,
        }
    )
    observables = {
        "input_digest": input_digest,
        "source_memoryos_v043_certificate_digest": memory["certificate_digest"],
        "source_memoryos_v043_cocycle_digest": memory["observables"][
            "temporal_window_cocycle_composition_digest"
        ],
        "source_memoryos_v043_conditioned_kernel_digest": memory["observables"][
            "refined_final_kernel_digest"
        ],
        "source_decisionos_v06_receipt_digest": decision["receipt_digest"],
        "retained_history_ids": memory["history_ids"],
        "retained_decision_candidate_ids": candidate_ids,
        "candidate_history_couplings": couplings,
        "candidate_quadratic_evidence_records": evidence_records,
        "positive_coherence_contrast_candidate_ids": positive_contrast,
        "zero_coherence_contrast_candidate_ids": zero_contrast,
        "negative_coherence_contrast_candidate_ids": negative_contrast,
        "all_quadratic_evidence_nonnegative_by_psd": all_nonnegative,
        "all_quadratic_evidence_real_by_hermitian_symmetry": all_imaginary_zero,
        "all_decision_candidates_retained": set(evidence_map) == set(candidate_ids),
        "decisionos_candidate_order_preserved": [
            item["candidate_id"] for item in evidence_records
        ]
        == sorted(candidate_ids),
        "source_relational_frontier_candidate_ids": source[
            "relational_frontier_candidate_ids"
        ],
        "source_required_review_candidate_ids": source[
            "required_review_candidate_ids"
        ],
        "source_dissent_review_candidate_ids": source[
            "dissent_review_candidate_ids"
        ],
        "source_minority_protection_candidate_ids": source[
            "minority_protection_candidate_ids"
        ],
        "relational_frontier_preserved": source[
            "relational_frontier_candidate_ids"
        ]
        == decision["receipt"]["relational_frontier_candidate_ids"],
        "required_review_set_preserved": source["required_review_candidate_ids"]
        == decision["receipt"]["required_review_candidate_ids"],
        "dissent_visibility_preserved": source["dissent_review_candidate_ids"]
        == decision["receipt"]["dissent_review_candidate_ids"],
        "minority_visibility_preserved": source[
            "minority_protection_candidate_ids"
        ]
        == decision["receipt"]["minority_protection_candidate_ids"],
        "coherence_evidence_used_as_advisory_only": True,
        "coherence_contrast_not_used_as_scalar_utility": True,
        "candidate_ranking_performed": False,
        "candidate_pruning_performed": False,
        "candidate_selection_performed": False,
        "decision_commit_performed": False,
        "decision_receipt_issued": False,
        "plan_synthesis_performed": False,
        "activation_performed": False,
        "execution_permission": False,
        "source_memoryos_v043_mutated": False,
        "source_decisionos_v06_mutated": False,
        "persistent_world_state_mutated": False,
        "verification_result_claimed": False,
        "truth_authority_granted": False,
        "future_only": True,
        "read_only": True,
    }
    required_true = (
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
    )
    for field in required_true:
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
    "canonical_digest",
    "issue_observer_relative_coherence_quadratic_evidence_decisionos_handoff_certificate",
]
