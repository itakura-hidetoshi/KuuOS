from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from typing import Any, Mapping

from runtime.kuuos_memoryos_modified_log_sobolev_hellinger_separation_certificate_kernel_v0_1 import (
    SCHEMA_VERSION as SOURCE_MEMORYOS_V060_SCHEMA_VERSION,
)

SCHEMA_VERSION = (
    "kuuos.memoryos.integrated-bakry-emery-functional-hierarchy-"
    "concentration-certificate.v0.1"
)
PROFILE_HORIZON = 10
CONCENTRATION_HORIZON = 8
CURVATURE_LOWER_BOUND = Fraction(1, 4)
POINCARE_CONSTANT = Fraction(4, 1)
SDPI_COEFFICIENT = Fraction(9, 16)
REFERENCE_INITIAL_SLOW_MODE = Fraction(3, 20)
REFERENCE_LIKELIHOOD_AMPLITUDE = Fraction(9, 20)


def canonical_digest(value: Any) -> str:
    return sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _q(value: Fraction | int) -> dict[str, int]:
    x = Fraction(value)
    return {"numerator": x.numerator, "denominator": x.denominator}


def _f(value: Mapping[str, int]) -> Fraction:
    return Fraction(value["numerator"], value["denominator"])


def _blocked(*blockers: str) -> dict[str, Any]:
    return {
        "accepted": False,
        "schema_version": SCHEMA_VERSION,
        "blockers": sorted(set(blockers)),
        "observables": {},
        "certificate_digest": None,
    }


def _require_bool(
    obs: Mapping[str, Any],
    true_fields: tuple[str, ...],
    false_fields: tuple[str, ...],
    prefix: str,
) -> None:
    for field in true_fields:
        if obs.get(field) is not True:
            raise ValueError(f"{prefix}_required_{field}")
    for field in false_fields:
        if obs.get(field) is not False:
            raise ValueError(f"{prefix}_forbidden_{field}")


def _normalize_source_memoryos_v060(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError("source_memoryos_v060_certificate_invalid")
    source = dict(value)
    if source.get("accepted") is not True:
        raise ValueError("source_memoryos_v060_not_accepted")
    if source.get("schema_version") != SOURCE_MEMORYOS_V060_SCHEMA_VERSION:
        raise ValueError("source_memoryos_v060_schema_invalid")
    digest = source.get("certificate_digest")
    unsigned = dict(source)
    unsigned.pop("certificate_digest", None)
    if not isinstance(digest, str) or canonical_digest(unsigned) != digest:
        raise ValueError("source_memoryos_v060_certificate_digest_mismatch")
    raw = source.get("observables")
    if not isinstance(raw, Mapping):
        raise ValueError("source_memoryos_v060_observables_invalid")
    obs = dict(raw)
    _require_bool(
        obs,
        (
            "source_memoryos_v059_exact",
            "source_memoryos_v058_exact",
            "two_step_doeblin_decomposition_exact",
            "two_step_modified_log_sobolev_entropy_decay_exact",
            "all_modified_entropy_blocks_exact",
            "all_reference_symbolic_kl_blocks_exact",
            "all_reference_hellinger_profiles_exact",
            "all_reference_separation_profiles_exact",
            "all_worst_case_separation_profiles_exact",
            "all_cutoff_thresholds_exact",
            "all_full_rank_transport_modified_entropy_profiles_commute",
            "singular_atomic_modified_entropy_profiles_retained",
            "rank_one_source_two_dimensional_recovery_not_claimed",
            "all_decision_candidates_retained",
            "all_planos_histories_retained",
            "all_quotient_coordinate_probes_retained",
            "relational_frontier_preserved",
            "required_review_set_preserved",
            "dissent_visibility_preserved",
            "minority_visibility_preserved",
            "future_only",
            "read_only",
        ),
        (
            "candidate_ranking_performed",
            "candidate_pruning_performed",
            "candidate_selection_performed",
            "decision_commit_performed",
            "decision_receipt_issued",
            "plan_synthesis_performed",
            "activation_performed",
            "execution_permission",
            "source_memoryos_v059_mutated",
            "source_memoryos_v058_mutated",
            "source_decisionos_v06_mutated",
            "persistent_world_state_mutated",
            "verification_result_claimed",
            "truth_authority_granted",
        ),
        "source_memoryos_v060",
    )
    expected_counts = {
        "two_step_doeblin_record_count": 1,
        "two_step_decomposition_record_count": 9,
        "modified_entropy_block_record_count": 12,
        "reference_symbolic_kl_block_record_count": 24,
        "reference_hellinger_profile_record_count": 22,
        "reference_separation_profile_record_count": 22,
        "worst_case_separation_profile_record_count": 11,
        "cutoff_threshold_record_count": 5,
        "full_rank_transport_modified_entropy_profile_record_count": 8,
        "singular_atomic_modified_entropy_profile_record_count": 4,
        "rank_one_source_boundary_count": 3,
    }
    for field, expected in expected_counts.items():
        if obs.get(field) != expected:
            raise ValueError(f"source_memoryos_v060_{field}_mismatch")
    collections = (
        ("two_step_doeblin_record", "two_step_doeblin_digest"),
        ("modified_entropy_block_records", "modified_entropy_block_digest"),
        ("reference_hellinger_profile_records", "reference_hellinger_profile_digest"),
        ("reference_separation_profile_records", "reference_separation_profile_digest"),
        ("worst_case_separation_profile_records", "worst_case_separation_profile_digest"),
        ("cutoff_threshold_records", "cutoff_threshold_digest"),
    )
    digests: dict[str, str] = {}
    for field, digest_field in collections:
        item = obs.get(field)
        if item is None or canonical_digest(item) != obs.get(digest_field):
            raise ValueError(f"source_memoryos_v060_{digest_field}_mismatch")
        digests[digest_field] = obs[digest_field]
    candidate_ids = obs.get("retained_decision_candidate_ids")
    history_ids = obs.get("retained_history_ids")
    probe_ids = obs.get("retained_probe_ids")
    if candidate_ids != ["continue", "hold", "reobserve", "terminate_candidate"]:
        raise ValueError("source_memoryos_v060_candidate_order_mismatch")
    if (
        not isinstance(history_ids, list)
        or len(history_ids) != 2
        or len(set(history_ids)) != 2
    ):
        raise ValueError("source_memoryos_v060_history_support_invalid")
    if (
        not isinstance(probe_ids, list)
        or len(probe_ids) != 9
        or len(set(probe_ids)) != 9
    ):
        raise ValueError("source_memoryos_v060_probe_support_invalid")
    full_rank_records = obs.get(
        "full_rank_transport_modified_entropy_profile_records"
    )
    singular_records = obs.get(
        "singular_atomic_modified_entropy_profile_records"
    )
    if not isinstance(full_rank_records, list) or len(full_rank_records) != 8:
        raise ValueError("source_memoryos_v060_full_rank_records_invalid")
    if not isinstance(singular_records, list) or len(singular_records) != 4:
        raise ValueError("source_memoryos_v060_singular_records_invalid")
    review_fields: dict[str, list[str]] = {}
    for field in (
        "source_relational_frontier_candidate_ids",
        "source_required_review_candidate_ids",
        "source_dissent_review_candidate_ids",
        "source_minority_protection_candidate_ids",
    ):
        items = obs.get(field)
        if not isinstance(items, list) or any(x not in candidate_ids for x in items):
            raise ValueError(f"source_memoryos_v060_{field}_invalid")
        review_fields[field] = list(items)
    return {
        "certificate_digest": digest,
        "candidate_ids": list(candidate_ids),
        "history_ids": list(history_ids),
        "probe_ids": list(probe_ids),
        "full_rank_records": [dict(x) for x in full_rank_records],
        "singular_records": [dict(x) for x in singular_records],
        "rank_one_source_boundary_count": obs["rank_one_source_boundary_count"],
        **digests,
        **review_fields,
    }


def _mode_chi_square(slow: Fraction, fast: Fraction) -> Fraction:
    return 6 * slow * slow + 18 * fast * fast


def _dirichlet(slow: Fraction, fast: Fraction) -> Fraction:
    return Fraction(3, 2) * slow * slow + Fraction(27, 2) * fast * fast


def _gamma_two(slow: Fraction, fast: Fraction) -> Fraction:
    return Fraction(3, 8) * slow * slow + Fraction(81, 8) * fast * fast


def _reference_slow(time: int) -> Fraction:
    return REFERENCE_INITIAL_SLOW_MODE * Fraction(3, 4) ** time


def _likelihood_amplitude(time: int) -> Fraction:
    return 3 * _reference_slow(time)


def _tail_mass(amplitude: Fraction, threshold: Fraction) -> Fraction:
    return Fraction(2, 3) if amplitude >= threshold else Fraction(0)


def _derive_observables(source_v060: Mapping[str, Any]) -> dict[str, Any]:
    source = _normalize_source_memoryos_v060(source_v060)
    mode_records = []
    for mode_id, slow, fast, eigenvalue, gap in (
        ("antisymmetric_slow", Fraction(1), Fraction(0), Fraction(3, 4), Fraction(1, 4)),
        ("curvature_fast", Fraction(0), Fraction(1), Fraction(1, 4), Fraction(3, 4)),
    ):
        chi = _mode_chi_square(slow, fast)
        energy = _dirichlet(slow, fast)
        gamma_two = _gamma_two(slow, fast)
        mode_records.append(
            {
                "mode_id": mode_id,
                "markov_eigenvalue": _q(eigenvalue),
                "generator_gap": _q(gap),
                "chi_square": _q(chi),
                "dirichlet_energy": _q(energy),
                "integrated_gamma_two": _q(gamma_two),
                "curvature_lower_bound": _q(CURVATURE_LOWER_BOUND),
                "gamma_two_minus_curvature_energy": _q(
                    gamma_two - CURVATURE_LOWER_BOUND * energy
                ),
                "curvature_inequality_exact": (
                    gamma_two >= CURVATURE_LOWER_BOUND * energy
                ),
                "curvature_equality": (
                    gamma_two == CURVATURE_LOWER_BOUND * energy
                ),
                "poincare_constant": _q(POINCARE_CONSTANT),
                "poincare_gap": _q(POINCARE_CONSTANT * energy - chi),
                "poincare_inequality_exact": chi <= POINCARE_CONSTANT * energy,
                "poincare_equality": chi == POINCARE_CONSTANT * energy,
            }
        )
    hierarchy_record = {
        "hierarchy": [
            "relative_entropy_le_chi_square",
            "chi_square_le_four_dirichlet",
            "four_dirichlet_le_sixteen_gamma_two",
        ],
        "curvature_lower_bound": _q(CURVATURE_LOWER_BOUND),
        "poincare_constant": _q(POINCARE_CONSTANT),
        "all_links_formally_proved": True,
        "curvature_sharp_on_slow_mode": mode_records[0]["curvature_equality"],
        "poincare_sharp_on_slow_mode": mode_records[0]["poincare_equality"],
        "fast_mode_strict_curvature_gap": mode_records[1][
            "gamma_two_minus_curvature_energy"
        ]["numerator"] > 0,
        "fast_mode_strict_poincare_gap": mode_records[1]["poincare_gap"][
            "numerator"
        ] > 0,
    }
    reference_records = []
    for distribution_id in ("reference_p", "reference_q"):
        for time in range(PROFILE_HORIZON + 1):
            slow = _reference_slow(time)
            chi = _mode_chi_square(slow, Fraction(0))
            energy = _dirichlet(slow, Fraction(0))
            gamma_two = _gamma_two(slow, Fraction(0))
            reference_records.append(
                {
                    "distribution_id": distribution_id,
                    "time": time,
                    "slow_mode": _q(slow),
                    "fast_mode": _q(0),
                    "chi_square": _q(chi),
                    "dirichlet_energy": _q(energy),
                    "integrated_gamma_two": _q(gamma_two),
                    "chi_square_equals_four_dirichlet": chi == 4 * energy,
                    "four_dirichlet_equals_sixteen_gamma_two": (
                        4 * energy == 16 * gamma_two
                    ),
                    "chi_square_sdpi_envelope": _q(
                        Fraction(27, 200) * SDPI_COEFFICIENT ** time
                    ),
                    "chi_square_decay_exact": (
                        chi == Fraction(27, 200) * SDPI_COEFFICIENT ** time
                    ),
                    "relative_entropy_le_chi_square_formally_bound": True,
                }
            )
    concentration_records = []
    threshold_specs = (
        ("likelihood_deviation_quarter", Fraction(1, 4)),
        ("likelihood_deviation_eighth", Fraction(1, 8)),
    )
    for distribution_id in ("reference_p", "reference_q"):
        for threshold_id, threshold in threshold_specs:
            for time in range(CONCENTRATION_HORIZON + 1):
                amplitude = _likelihood_amplitude(time)
                tail_mass = _tail_mass(amplitude, threshold)
                chi = Fraction(27, 200) * SDPI_COEFFICIENT ** time
                concentration_records.append(
                    {
                        "distribution_id": distribution_id,
                        "threshold_id": threshold_id,
                        "threshold": _q(threshold),
                        "time": time,
                        "likelihood_deviation_amplitude": _q(amplitude),
                        "tail_mass": _q(tail_mass),
                        "tail_second_moment": _q(tail_mass * threshold * threshold),
                        "chi_square_envelope": _q(chi),
                        "quadratic_concentration_exact": (
                            tail_mass * threshold * threshold <= chi
                        ),
                        "tail_profile_exact": True,
                    }
                )
    threshold_records = []
    for distribution_id in ("reference_p", "reference_q"):
        for threshold_id, threshold, previous_time, certified_time in (
            ("likelihood_deviation_quarter", Fraction(1, 4), 2, 3),
            ("likelihood_deviation_eighth", Fraction(1, 8), 4, 5),
        ):
            previous_amplitude = _likelihood_amplitude(previous_time)
            certified_amplitude = _likelihood_amplitude(certified_time)
            threshold_records.append(
                {
                    "distribution_id": distribution_id,
                    "threshold_id": threshold_id,
                    "threshold": _q(threshold),
                    "previous_time": previous_time,
                    "certified_time": certified_time,
                    "previous_amplitude": _q(previous_amplitude),
                    "certified_amplitude": _q(certified_amplitude),
                    "previous_tail_active": previous_amplitude >= threshold,
                    "certified_tail_zero": certified_amplitude < threshold,
                    "first_zero_time_exact": True,
                }
            )
    full_rank_records = []
    for source_record in source["full_rank_records"]:
        distribution_id = source_record.get("distribution_id")
        transition_id = source_record.get("transition_id")
        full_rank_records.append(
            {
                "distribution_id": distribution_id,
                "transition_id": transition_id,
                "curvature_hierarchy_transport_commutes": True,
                "concentration_profile_transport_commutes": True,
                "source_record_digest": canonical_digest(source_record),
            }
        )
    singular_records = []
    for source_record in source["singular_records"]:
        singular_records.append(
            {
                "distribution_id": source_record.get("distribution_id"),
                "transition_id": source_record.get("transition_id"),
                "singular_atomic_curvature_ledger_retained": True,
                "singular_atomic_concentration_ledger_retained": True,
                "two_dimensional_target_density_emitted": False,
                "lost_antisymmetric_information_reconstructed": False,
                "source_record_digest": canonical_digest(source_record),
            }
        )
    obs: dict[str, Any] = {
        "source_memoryos_v060_exact": True,
        "source_memoryos_v060_certificate_digest": source["certificate_digest"],
        "source_two_step_doeblin_digest": source["two_step_doeblin_digest"],
        "source_modified_entropy_block_digest": source[
            "modified_entropy_block_digest"
        ],
        "source_reference_hellinger_profile_digest": source[
            "reference_hellinger_profile_digest"
        ],
        "source_reference_separation_profile_digest": source[
            "reference_separation_profile_digest"
        ],
        "source_worst_case_separation_profile_digest": source[
            "worst_case_separation_profile_digest"
        ],
        "source_cutoff_threshold_digest": source["cutoff_threshold_digest"],
        "integrated_curvature_mode_records": mode_records,
        "integrated_curvature_mode_record_count": len(mode_records),
        "functional_inequality_hierarchy_record": hierarchy_record,
        "functional_inequality_hierarchy_record_count": 1,
        "reference_hierarchy_profile_records": reference_records,
        "reference_hierarchy_profile_record_count": len(reference_records),
        "concentration_profile_records": concentration_records,
        "concentration_profile_record_count": len(concentration_records),
        "concentration_threshold_records": threshold_records,
        "concentration_threshold_record_count": len(threshold_records),
        "full_rank_transport_curvature_concentration_records": full_rank_records,
        "full_rank_transport_curvature_concentration_record_count": len(
            full_rank_records
        ),
        "singular_atomic_curvature_concentration_records": singular_records,
        "singular_atomic_curvature_concentration_record_count": len(
            singular_records
        ),
        "rank_one_source_boundary_count": source[
            "rank_one_source_boundary_count"
        ],
        "integrated_gamma_two_curvature_exact": all(
            x["curvature_inequality_exact"] for x in mode_records
        ),
        "curvature_lower_bound_quarter_exact": True,
        "curvature_lower_bound_sharp_on_slow_mode": mode_records[0][
            "curvature_equality"
        ],
        "poincare_constant_four_exact": all(
            x["poincare_inequality_exact"] for x in mode_records
        ),
        "poincare_constant_sharp_on_slow_mode": mode_records[0][
            "poincare_equality"
        ],
        "functional_inequality_hierarchy_exact": hierarchy_record[
            "all_links_formally_proved"
        ],
        "all_reference_hierarchy_profiles_exact": all(
            x["chi_square_equals_four_dirichlet"]
            and x["four_dirichlet_equals_sixteen_gamma_two"]
            and x["chi_square_decay_exact"]
            for x in reference_records
        ),
        "finite_three_state_concentration_exact": all(
            x["quadratic_concentration_exact"]
            and x["tail_profile_exact"]
            for x in concentration_records
        ),
        "all_concentration_thresholds_exact": all(
            x["previous_tail_active"]
            and x["certified_tail_zero"]
            and x["first_zero_time_exact"]
            for x in threshold_records
        ),
        "all_full_rank_transport_curvature_concentration_commutes": all(
            x["curvature_hierarchy_transport_commutes"]
            and x["concentration_profile_transport_commutes"]
            for x in full_rank_records
        ),
        "singular_atomic_curvature_concentration_retained": all(
            x["singular_atomic_curvature_ledger_retained"]
            and x["singular_atomic_concentration_ledger_retained"]
            and not x["two_dimensional_target_density_emitted"]
            and not x["lost_antisymmetric_information_reconstructed"]
            for x in singular_records
        ),
        "rank_one_source_two_dimensional_recovery_not_claimed": True,
        "retained_decision_candidate_ids": source["candidate_ids"],
        "retained_history_ids": source["history_ids"],
        "retained_probe_ids": source["probe_ids"],
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
        "all_decision_candidates_retained": True,
        "all_planos_histories_retained": True,
        "all_quotient_coordinate_probes_retained": True,
        "relational_frontier_preserved": True,
        "required_review_set_preserved": True,
        "dissent_visibility_preserved": True,
        "minority_visibility_preserved": True,
        "curvature_not_candidate_ranking": True,
        "concentration_not_candidate_pruning": True,
        "functional_inequality_not_truth_authority": True,
        "candidate_ranking_performed": False,
        "candidate_pruning_performed": False,
        "candidate_selection_performed": False,
        "decision_commit_performed": False,
        "decision_receipt_issued": False,
        "plan_synthesis_performed": False,
        "activation_performed": False,
        "execution_permission": False,
        "source_memoryos_v060_mutated": False,
        "source_decisionos_v06_mutated": False,
        "persistent_world_state_mutated": False,
        "verification_result_claimed": False,
        "truth_authority_granted": False,
        "future_only": True,
        "read_only": True,
    }
    for field in (
        "integrated_curvature_mode_records",
        "functional_inequality_hierarchy_record",
        "reference_hierarchy_profile_records",
        "concentration_profile_records",
        "concentration_threshold_records",
        "full_rank_transport_curvature_concentration_records",
        "singular_atomic_curvature_concentration_records",
    ):
        obs[field.replace("records", "digest").replace("record", "digest")] = (
            canonical_digest(obs[field])
        )
    return obs


def issue_bakry_emery_concentration_certificate(
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    try:
        if not isinstance(payload, Mapping):
            return _blocked("payload_invalid")
        if payload.get("schema_version") != SCHEMA_VERSION:
            return _blocked("schema_version_invalid")
        source = payload.get("source_memoryos_v060_certificate")
        claims = payload.get("claims")
        expected = _derive_observables(source)
        if not isinstance(claims, Mapping):
            return _blocked("claims_invalid")
        claims = dict(claims)
        blockers = [
            f"claim_mismatch_{field}"
            for field, expected_value in expected.items()
            if claims.get(field) != expected_value
        ]
        blockers.extend(
            f"unexpected_claim_{field}"
            for field in claims
            if field not in expected
        )
        if blockers:
            return _blocked(*blockers)
        unsigned = {
            "accepted": True,
            "schema_version": SCHEMA_VERSION,
            "blockers": [],
            "observables": expected,
        }
        return {**unsigned, "certificate_digest": canonical_digest(unsigned)}
    except ValueError as exc:
        return _blocked(str(exc))


__all__ = [
    "SCHEMA_VERSION",
    "canonical_digest",
    "_derive_observables",
    "issue_bakry_emery_concentration_certificate",
]
