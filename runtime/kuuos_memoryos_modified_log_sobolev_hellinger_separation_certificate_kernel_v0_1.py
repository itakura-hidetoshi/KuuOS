from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from typing import Any, Mapping

from runtime.kuuos_memoryos_reversible_markov_semigroup_entropy_production_certificate_kernel_v0_1 import (
    REFERENCE_P,
    REFERENCE_Q,
    STATE_IDS,
    UNIFORM_STATIONARY,
)
from runtime.kuuos_memoryos_log_sobolev_hypercontractive_mixing_certificate_kernel_v0_1 import (
    SCHEMA_VERSION as SOURCE_MEMORYOS_V059_SCHEMA_VERSION,
    _normalize_source_memoryos_v058,
)

SCHEMA_VERSION = (
    "kuuos.memoryos.modified-log-sobolev-hellinger-separation-"
    "cutoff-certificate.v0.1"
)
DOEBLIN_STATIONARY_WEIGHT = Fraction(3, 16)
DOEBLIN_RESIDUAL_WEIGHT = Fraction(13, 16)
PROFILE_HORIZON = 10
MLSI_BLOCK_HORIZON = 11

REFERENCE_KERNEL = (
    (Fraction(3, 4), Fraction(1, 4), Fraction(0)),
    (Fraction(1, 4), Fraction(1, 2), Fraction(1, 4)),
    (Fraction(0), Fraction(1, 4), Fraction(3, 4)),
)
RESIDUAL_KERNEL = (
    (Fraction(9, 13), Fraction(4, 13), Fraction(0)),
    (Fraction(4, 13), Fraction(5, 13), Fraction(4, 13)),
    (Fraction(0), Fraction(4, 13), Fraction(9, 13)),
)


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


def _matrix_mul(
    a: tuple[tuple[Fraction, ...], ...],
    b: tuple[tuple[Fraction, ...], ...],
) -> tuple[tuple[Fraction, ...], ...]:
    return tuple(
        tuple(
            sum(a[i][k] * b[k][j] for k in range(len(b)))
            for j in range(len(b[0]))
        )
        for i in range(len(a))
    )


def _matrix_json(
    matrix: tuple[tuple[Fraction, ...], ...]
) -> list[list[dict[str, int]]]:
    return [[_q(x) for x in row] for row in matrix]


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


def _normalize_source_memoryos_v059(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError("source_memoryos_v059_certificate_invalid")
    source = dict(value)
    if source.get("accepted") is not True:
        raise ValueError("source_memoryos_v059_not_accepted")
    if source.get("schema_version") != SOURCE_MEMORYOS_V059_SCHEMA_VERSION:
        raise ValueError("source_memoryos_v059_schema_invalid")
    digest = source.get("certificate_digest")
    unsigned = dict(source)
    unsigned.pop("certificate_digest", None)
    if not isinstance(digest, str) or canonical_digest(unsigned) != digest:
        raise ValueError("source_memoryos_v059_certificate_digest_mismatch")
    raw = source.get("observables")
    if not isinstance(raw, Mapping):
        raise ValueError("source_memoryos_v059_observables_invalid")
    obs = dict(raw)
    _require_bool(
        obs,
        (
            "source_memoryos_v058_exact",
            "source_memoryos_v057_exact",
            "source_entropy_trajectory_digest_bound",
            "source_entropy_production_digest_bound",
            "source_semigroup_digest_bound",
            "logarithmic_entropy_bridge_exact",
            "log_sobolev_constant_four_exact",
            "all_reference_kl_chi_square_envelopes_exact",
            "one_step_l2_to_l4_hypercontractive",
            "two_step_l2_to_linf_hypercontractive",
            "reference_total_variation_trajectory_exact",
            "worst_case_total_variation_mixing_bound_exact",
            "all_mixing_thresholds_exact",
            "all_full_rank_transport_log_sobolev_mixing_commutes",
            "singular_atomic_log_sobolev_mixing_retained",
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
            "source_memoryos_v058_mutated",
            "source_memoryos_v057_mutated",
            "source_decisionos_v06_mutated",
            "persistent_world_state_mutated",
            "verification_result_claimed",
            "truth_authority_granted",
        ),
        "source_memoryos_v059",
    )
    expected_counts = {
        "log_sobolev_record_count": 1,
        "reference_kl_envelope_record_count": 10,
        "hypercontractive_schedule_record_count": 2,
        "reference_total_variation_record_count": 10,
        "worst_case_mixing_record_count": 9,
        "mixing_threshold_record_count": 3,
        "full_rank_transport_log_sobolev_mixing_record_count": 8,
        "singular_atomic_log_sobolev_mixing_record_count": 4,
        "rank_one_source_boundary_count": 3,
    }
    for field, expected in expected_counts.items():
        if obs.get(field) != expected:
            raise ValueError(f"source_memoryos_v059_{field}_mismatch")
    collections = (
        ("log_sobolev_mode_record", "log_sobolev_mode_digest"),
        ("reference_kl_envelope_records", "reference_kl_envelope_digest"),
        ("hypercontractive_schedule_records", "hypercontractive_schedule_digest"),
        ("reference_total_variation_records", "reference_total_variation_digest"),
        ("worst_case_mixing_records", "worst_case_mixing_digest"),
        ("mixing_threshold_records", "mixing_threshold_digest"),
        (
            "full_rank_transport_log_sobolev_mixing_records",
            "full_rank_transport_log_sobolev_mixing_digest",
        ),
        (
            "singular_atomic_log_sobolev_mixing_records",
            "singular_atomic_log_sobolev_mixing_digest",
        ),
    )
    digests: dict[str, str] = {}
    for field, digest_field in collections:
        item = obs.get(field)
        if item is None or canonical_digest(item) != obs.get(digest_field):
            raise ValueError(f"source_memoryos_v059_{digest_field}_mismatch")
        digests[digest_field] = obs[digest_field]
    candidate_ids = obs.get("retained_decision_candidate_ids")
    history_ids = obs.get("retained_history_ids")
    probe_ids = obs.get("retained_probe_ids")
    if candidate_ids != ["continue", "hold", "reobserve", "terminate_candidate"]:
        raise ValueError("source_memoryos_v059_candidate_order_mismatch")
    if (
        not isinstance(history_ids, list)
        or len(history_ids) != 2
        or len(set(history_ids)) != 2
    ):
        raise ValueError("source_memoryos_v059_history_support_invalid")
    if (
        not isinstance(probe_ids, list)
        or len(probe_ids) != 9
        or len(set(probe_ids)) != 9
    ):
        raise ValueError("source_memoryos_v059_probe_support_invalid")
    review_fields: dict[str, list[str]] = {}
    for field in (
        "source_relational_frontier_candidate_ids",
        "source_required_review_candidate_ids",
        "source_dissent_review_candidate_ids",
        "source_minority_protection_candidate_ids",
    ):
        items = obs.get(field)
        if not isinstance(items, list) or any(x not in candidate_ids for x in items):
            raise ValueError(f"source_memoryos_v059_{field}_invalid")
        review_fields[field] = list(items)
    return {
        "certificate_digest": digest,
        "source_memoryos_v058_certificate_digest": obs[
            "source_memoryos_v058_certificate_digest"
        ],
        "source_memoryos_v058_entropy_trajectory_digest": obs[
            "source_memoryos_v058_entropy_trajectory_digest"
        ],
        "source_memoryos_v058_entropy_production_digest": obs[
            "source_memoryos_v058_entropy_production_digest"
        ],
        "candidate_ids": list(candidate_ids),
        "history_ids": list(history_ids),
        "probe_ids": list(probe_ids),
        "full_rank_records": [
            dict(x)
            for x in obs["full_rank_transport_log_sobolev_mixing_records"]
        ],
        "singular_records": [
            dict(x)
            for x in obs["singular_atomic_log_sobolev_mixing_records"]
        ],
        "rank_one_source_boundary_count": obs["rank_one_source_boundary_count"],
        **digests,
        **review_fields,
    }


def _reference_masses(
    distribution_id: str, time: int
) -> dict[str, dict[str, int]]:
    u = Fraction(3, 20) * Fraction(3, 4) ** time
    early, late = Fraction(1, 3) - u, Fraction(1, 3) + u
    if distribution_id == "reference_q":
        early, late = late, early
    return {
        "early": _q(early),
        "middle": _q(Fraction(1, 3)),
        "late": _q(late),
    }


def _likelihoods(
    masses: Mapping[str, Mapping[str, int]],
) -> dict[str, dict[str, int]]:
    return {
        state: _q(_f(masses[state]) / _f(UNIFORM_STATIONARY[state]))
        for state in STATE_IDS
    }


def _derive_observables(
    source_v059: Mapping[str, Any], source_v058: Mapping[str, Any]
) -> dict[str, Any]:
    v059 = _normalize_source_memoryos_v059(source_v059)
    v058 = _normalize_source_memoryos_v058(source_v058)
    if v059["source_memoryos_v058_certificate_digest"] != v058[
        "certificate_digest"
    ]:
        raise ValueError("source_v059_v058_certificate_binding_mismatch")
    if v059["source_memoryos_v058_entropy_trajectory_digest"] != v058[
        "entropy_trajectory_digest"
    ]:
        raise ValueError("source_v059_v058_entropy_trajectory_binding_mismatch")
    if v059["source_memoryos_v058_entropy_production_digest"] != v058[
        "entropy_production_digest"
    ]:
        raise ValueError("source_v059_v058_entropy_production_binding_mismatch")
    if (
        v059["candidate_ids"] != v058["candidate_ids"]
        or v059["history_ids"] != v058["history_ids"]
        or v059["probe_ids"] != v058["probe_ids"]
    ):
        raise ValueError("source_v059_v058_support_binding_mismatch")

    two_step = _matrix_mul(REFERENCE_KERNEL, REFERENCE_KERNEL)
    pi_kernel = tuple(
        tuple(Fraction(1, 3) for _ in STATE_IDS) for _ in STATE_IDS
    )
    reconstructed = tuple(
        tuple(
            DOEBLIN_STATIONARY_WEIGHT * pi_kernel[i][j]
            + DOEBLIN_RESIDUAL_WEIGHT * RESIDUAL_KERNEL[i][j]
            for j in range(3)
        )
        for i in range(3)
    )
    decomposition_records = [
        {
            "source_state_id": STATE_IDS[i],
            "target_state_id": STATE_IDS[j],
            "two_step_kernel_entry": _q(two_step[i][j]),
            "stationary_component": _q(
                DOEBLIN_STATIONARY_WEIGHT * pi_kernel[i][j]
            ),
            "residual_component": _q(
                DOEBLIN_RESIDUAL_WEIGHT * RESIDUAL_KERNEL[i][j]
            ),
            "reconstructed_entry": _q(reconstructed[i][j]),
            "decomposition_exact": two_step[i][j] == reconstructed[i][j],
        }
        for i in range(3)
        for j in range(3)
    ]
    doeblin_record = {
        "reference_kernel": _matrix_json(REFERENCE_KERNEL),
        "two_step_kernel": _matrix_json(two_step),
        "stationary_projection_kernel": _matrix_json(pi_kernel),
        "residual_kernel": _matrix_json(RESIDUAL_KERNEL),
        "stationary_weight": _q(DOEBLIN_STATIONARY_WEIGHT),
        "residual_weight": _q(DOEBLIN_RESIDUAL_WEIGHT),
        "weights_sum_to_one": (
            DOEBLIN_STATIONARY_WEIGHT + DOEBLIN_RESIDUAL_WEIGHT == 1
        ),
        "residual_rows_stochastic": all(
            sum(row) == 1 for row in RESIDUAL_KERNEL
        ),
        "residual_columns_stochastic": all(
            sum(RESIDUAL_KERNEL[i][j] for i in range(3)) == 1
            for j in range(3)
        ),
        "residual_kernel_symmetric": all(
            RESIDUAL_KERNEL[i][j] == RESIDUAL_KERNEL[j][i]
            for i in range(3)
            for j in range(3)
        ),
        "all_decomposition_entries_exact": all(
            x["decomposition_exact"] for x in decomposition_records
        ),
        "formal_theorem": "two_step_modified_log_sobolev_entropy_decay",
    }

    block_records = [
        {
            "block": block,
            "physical_time": 2 * block,
            "modified_entropy_contraction_coefficient": _q(
                DOEBLIN_RESIDUAL_WEIGHT**block
            ),
            "worst_case_initial_kl_envelope": _q(2),
            "worst_case_kl_envelope": _q(
                2 * DOEBLIN_RESIDUAL_WEIGHT**block
            ),
            "coefficient_nonnegative": True,
        }
        for block in range(MLSI_BLOCK_HORIZON + 1)
    ]
    symbolic_kl_records: list[dict[str, Any]] = []
    hellinger_records: list[dict[str, Any]] = []
    separation_records: list[dict[str, Any]] = []
    for distribution_id in ("reference_p", "reference_q"):
        for block in range(MLSI_BLOCK_HORIZON + 1):
            masses = _reference_masses(distribution_id, 2 * block)
            likelihoods = _likelihoods(masses)
            symbolic_kl_records.append(
                {
                    "distribution_id": distribution_id,
                    "block": block,
                    "physical_time": 2 * block,
                    "mass_distribution": masses,
                    "likelihood_ratios": likelihoods,
                    "symbolic_terms": [
                        {
                            "state_id": state,
                            "mass_coefficient": masses[state],
                            "log_argument_likelihood_ratio": likelihoods[state],
                            "term_form": "mass * Real.log(likelihood_ratio)",
                        }
                        for state in STATE_IDS
                    ],
                    "modified_entropy_decay_coefficient": _q(
                        DOEBLIN_RESIDUAL_WEIGHT**block
                    ),
                    "modified_log_sobolev_decay_formally_bound": True,
                    "mass_normalized": (
                        sum(_f(x) for x in masses.values()) == 1
                    ),
                }
            )
        for time in range(PROFILE_HORIZON + 1):
            masses = _reference_masses(distribution_id, time)
            likelihoods = _likelihoods(masses)
            u = Fraction(9, 20) * Fraction(3, 4) ** time
            hellinger_records.append(
                {
                    "distribution_id": distribution_id,
                    "time": time,
                    "mass_distribution": masses,
                    "likelihood_ratios": likelihoods,
                    "hellinger_squared_expression": [
                        {
                            "state_id": state,
                            "term_form": (
                                "(Real.sqrt(likelihood_ratio) - 1)^2 / 6"
                            ),
                            "sqrt_argument": likelihoods[state],
                        }
                        for state in STATE_IDS
                    ],
                    "rational_hellinger_squared_envelope": _q(u * u / 3),
                    "all_sqrt_arguments_nonnegative": all(
                        _f(x) >= 0 for x in likelihoods.values()
                    ),
                    "hellinger_envelope_formally_bound": True,
                }
            )
            minimum = min(_f(x) for x in likelihoods.values())
            separation = 1 - minimum
            separation_records.append(
                {
                    "distribution_id": distribution_id,
                    "time": time,
                    "minimum_likelihood_ratio": _q(minimum),
                    "separation_to_uniform": _q(separation),
                    "expected_reference_separation": _q(u),
                    "separation_exact": separation == u,
                }
            )

    worst_sep_records = []
    identity = tuple(
        tuple(Fraction(int(i == j)) for j in range(3)) for i in range(3)
    )
    exact_power = identity
    for time in range(PROFILE_HORIZON + 1):
        if time > 0:
            exact_power = _matrix_mul(exact_power, REFERENCE_KERNEL)
        profile = (
            Fraction(3, 2) * Fraction(3, 4) ** time
            - Fraction(1, 2) * Fraction(1, 4) ** time
        )
        min_entry = min(x for row in exact_power for x in row)
        explicit = 1 - 3 * min_entry
        worst_sep_records.append(
            {
                "time": time,
                "spectral_profile": _q(profile),
                "minimum_kernel_entry": _q(min_entry),
                "explicit_worst_case_separation": _q(explicit),
                "profile_exact": explicit == profile,
            }
        )

    thresholds = [
        (
            "worst_case_separation_le_one_quarter",
            "worst_case_separation",
            Fraction(1, 4),
            7,
            Fraction(3, 2) * Fraction(3, 4) ** 7
            - Fraction(1, 2) * Fraction(1, 4) ** 7,
            Fraction(3, 2) * Fraction(3, 4) ** 6
            - Fraction(1, 2) * Fraction(1, 4) ** 6,
            7,
        ),
        (
            "worst_case_separation_le_one_eighth",
            "worst_case_separation",
            Fraction(1, 8),
            9,
            Fraction(3, 2) * Fraction(3, 4) ** 9
            - Fraction(1, 2) * Fraction(1, 4) ** 9,
            Fraction(3, 2) * Fraction(3, 4) ** 8
            - Fraction(1, 2) * Fraction(1, 4) ** 8,
            9,
        ),
        (
            "reference_separation_le_one_twentieth",
            "reference_separation",
            Fraction(1, 20),
            8,
            Fraction(9, 20) * Fraction(3, 4) ** 8,
            Fraction(9, 20) * Fraction(3, 4) ** 7,
            8,
        ),
        (
            "reference_hellinger_le_one_twentieth_envelope",
            "reference_hellinger",
            Fraction(1, 20) ** 2,
            6,
            (Fraction(9, 20) * Fraction(3, 4) ** 6) ** 2 / 3,
            (Fraction(9, 20) * Fraction(3, 4) ** 5) ** 2 / 3,
            6,
        ),
        (
            "worst_case_kl_le_one_quarter_block",
            "worst_case_kl",
            Fraction(1, 4),
            11,
            2 * Fraction(13, 16) ** 11,
            2 * Fraction(13, 16) ** 10,
            22,
        ),
    ]
    cutoff_records = [
        {
            "threshold_id": threshold_id,
            "profile_kind": kind,
            "epsilon_or_squared_epsilon": _q(epsilon),
            "certified_index": index,
            "certified_physical_time": physical_time,
            "certified_value": _q(value),
            "previous_value": _q(previous),
            "certified": value <= epsilon,
            "previous_value_not_sufficient": previous > epsilon,
        }
        for (
            threshold_id,
            kind,
            epsilon,
            index,
            value,
            previous,
            physical_time,
        ) in thresholds
    ]

    full_rank_records = [
        {
            "source_cross_numerator": x["source_cross_numerator"],
            "target_cross_numerator": x["target_cross_numerator"],
            "distribution_id": x["distribution_id"],
            "modified_log_sobolev_decay_transport_commutes": True,
            "hellinger_profile_transport_commutes": True,
            "separation_profile_transport_commutes": True,
        }
        for x in v059["full_rank_records"]
    ]
    singular_records = [
        {
            "source_cross_numerator": x["source_cross_numerator"],
            "target_cross_numerator": x["target_cross_numerator"],
            "distribution_id": x["distribution_id"],
            "singular_atomic_modified_entropy_ledger_retained": True,
            "singular_atomic_hellinger_ledger_retained": True,
            "singular_atomic_separation_ledger_retained": True,
            "two_dimensional_target_density_emitted": False,
        }
        for x in v059["singular_records"]
    ]

    observables = {
        "input_digest": canonical_digest(
            {
                "schema_version": SCHEMA_VERSION,
                "source_memoryos_v059_certificate_digest": v059[
                    "certificate_digest"
                ],
                "source_memoryos_v058_certificate_digest": v058[
                    "certificate_digest"
                ],
                "profile_horizon": PROFILE_HORIZON,
                "mlsi_block_horizon": MLSI_BLOCK_HORIZON,
            }
        ),
        "source_memoryos_v059_certificate_digest": v059["certificate_digest"],
        "source_memoryos_v059_log_sobolev_mode_digest": v059[
            "log_sobolev_mode_digest"
        ],
        "source_memoryos_v059_reference_kl_envelope_digest": v059[
            "reference_kl_envelope_digest"
        ],
        "source_memoryos_v059_hypercontractive_schedule_digest": v059[
            "hypercontractive_schedule_digest"
        ],
        "source_memoryos_v059_reference_total_variation_digest": v059[
            "reference_total_variation_digest"
        ],
        "source_memoryos_v059_worst_case_mixing_digest": v059[
            "worst_case_mixing_digest"
        ],
        "source_memoryos_v059_mixing_threshold_digest": v059[
            "mixing_threshold_digest"
        ],
        "source_memoryos_v059_full_rank_transport_digest": v059[
            "full_rank_transport_log_sobolev_mixing_digest"
        ],
        "source_memoryos_v059_singular_atomic_digest": v059[
            "singular_atomic_log_sobolev_mixing_digest"
        ],
        "source_memoryos_v058_certificate_digest": v058["certificate_digest"],
        "source_memoryos_v058_entropy_trajectory_digest": v058[
            "entropy_trajectory_digest"
        ],
        "source_memoryos_v058_entropy_production_digest": v058[
            "entropy_production_digest"
        ],
        "retained_decision_candidate_ids": v059["candidate_ids"],
        "retained_history_ids": v059["history_ids"],
        "retained_probe_ids": v059["probe_ids"],
        "two_step_doeblin_record": doeblin_record,
        "two_step_doeblin_digest": canonical_digest(doeblin_record),
        "two_step_decomposition_records": decomposition_records,
        "two_step_decomposition_digest": canonical_digest(
            decomposition_records
        ),
        "modified_entropy_block_records": block_records,
        "modified_entropy_block_digest": canonical_digest(block_records),
        "reference_symbolic_kl_block_records": symbolic_kl_records,
        "reference_symbolic_kl_block_digest": canonical_digest(
            symbolic_kl_records
        ),
        "reference_hellinger_profile_records": hellinger_records,
        "reference_hellinger_profile_digest": canonical_digest(
            hellinger_records
        ),
        "reference_separation_profile_records": separation_records,
        "reference_separation_profile_digest": canonical_digest(
            separation_records
        ),
        "worst_case_separation_profile_records": worst_sep_records,
        "worst_case_separation_profile_digest": canonical_digest(
            worst_sep_records
        ),
        "cutoff_threshold_records": cutoff_records,
        "cutoff_threshold_digest": canonical_digest(cutoff_records),
        "full_rank_transport_modified_entropy_profile_records": (
            full_rank_records
        ),
        "full_rank_transport_modified_entropy_profile_digest": (
            canonical_digest(full_rank_records)
        ),
        "singular_atomic_modified_entropy_profile_records": singular_records,
        "singular_atomic_modified_entropy_profile_digest": canonical_digest(
            singular_records
        ),
        "doeblin_stationary_weight": _q(DOEBLIN_STATIONARY_WEIGHT),
        "doeblin_residual_weight": _q(DOEBLIN_RESIDUAL_WEIGHT),
        "two_step_doeblin_record_count": 1,
        "two_step_decomposition_record_count": len(decomposition_records),
        "modified_entropy_block_record_count": len(block_records),
        "reference_symbolic_kl_block_record_count": len(symbolic_kl_records),
        "reference_hellinger_profile_record_count": len(hellinger_records),
        "reference_separation_profile_record_count": len(
            separation_records
        ),
        "worst_case_separation_profile_record_count": len(worst_sep_records),
        "cutoff_threshold_record_count": len(cutoff_records),
        "full_rank_transport_modified_entropy_profile_record_count": len(
            full_rank_records
        ),
        "singular_atomic_modified_entropy_profile_record_count": len(
            singular_records
        ),
        "rank_one_source_boundary_count": v059[
            "rank_one_source_boundary_count"
        ],
        "source_memoryos_v059_exact": True,
        "source_memoryos_v058_exact": True,
        "source_v059_v058_bindings_exact": True,
        "two_step_kernel_exact": two_step
        == (
            (Fraction(5, 8), Fraction(5, 16), Fraction(1, 16)),
            (Fraction(5, 16), Fraction(3, 8), Fraction(5, 16)),
            (Fraction(1, 16), Fraction(5, 16), Fraction(5, 8)),
        ),
        "two_step_doeblin_decomposition_exact": (
            doeblin_record["all_decomposition_entries_exact"]
            and doeblin_record["residual_rows_stochastic"]
            and doeblin_record["residual_columns_stochastic"]
        ),
        "residual_kernel_kl_data_processing_exact": True,
        "modified_log_sobolev_two_step_entropy_decay_exact": True,
        "iterated_modified_entropy_decay_exact": True,
        "all_reference_symbolic_kl_blocks_bound": all(
            x["modified_log_sobolev_decay_formally_bound"]
            and x["mass_normalized"]
            for x in symbolic_kl_records
        ),
        "all_reference_hellinger_profiles_exact": all(
            x["all_sqrt_arguments_nonnegative"]
            and x["hellinger_envelope_formally_bound"]
            for x in hellinger_records
        ),
        "all_reference_separation_profiles_exact": all(
            x["separation_exact"] for x in separation_records
        ),
        "all_worst_case_separation_profiles_exact": all(
            x["profile_exact"] for x in worst_sep_records
        ),
        "all_finite_cutoff_thresholds_exact": all(
            x["certified"] and x["previous_value_not_sufficient"]
            for x in cutoff_records
        ),
        "all_full_rank_transport_modified_entropy_profiles_commute": all(
            x["modified_log_sobolev_decay_transport_commutes"]
            and x["hellinger_profile_transport_commutes"]
            and x["separation_profile_transport_commutes"]
            for x in full_rank_records
        ),
        "singular_atomic_modified_entropy_profiles_retained": all(
            x["singular_atomic_modified_entropy_ledger_retained"]
            and x["singular_atomic_hellinger_ledger_retained"]
            and x["singular_atomic_separation_ledger_retained"]
            and not x["two_dimensional_target_density_emitted"]
            for x in singular_records
        ),
        "rank_one_source_two_dimensional_recovery_not_claimed": True,
        "all_decision_candidates_retained": True,
        "all_planos_histories_retained": True,
        "all_quotient_coordinate_probes_retained": True,
        "source_relational_frontier_candidate_ids": v059[
            "source_relational_frontier_candidate_ids"
        ],
        "source_required_review_candidate_ids": v059[
            "source_required_review_candidate_ids"
        ],
        "source_dissent_review_candidate_ids": v059[
            "source_dissent_review_candidate_ids"
        ],
        "source_minority_protection_candidate_ids": v059[
            "source_minority_protection_candidate_ids"
        ],
        "relational_frontier_preserved": True,
        "required_review_set_preserved": True,
        "dissent_visibility_preserved": True,
        "minority_visibility_preserved": True,
        "modified_log_sobolev_witness_advisory_only": True,
        "hellinger_profile_not_candidate_preference": True,
        "separation_cutoff_not_activation_schedule": True,
        "finite_cutoff_not_asymptotic_cutoff_claim": True,
        "singular_boundary_not_information_recovery": True,
        "candidate_ranking_performed": False,
        "candidate_pruning_performed": False,
        "candidate_selection_performed": False,
        "decision_commit_performed": False,
        "decision_receipt_issued": False,
        "plan_synthesis_performed": False,
        "activation_performed": False,
        "execution_permission": False,
        "source_memoryos_v059_mutated": False,
        "source_memoryos_v058_mutated": False,
        "source_decisionos_v06_mutated": False,
        "persistent_world_state_mutated": False,
        "verification_result_claimed": False,
        "truth_authority_granted": False,
        "future_only": True,
        "read_only": True,
    }
    return observables


def issue_modified_log_sobolev_hellinger_separation_certificate(
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    if not isinstance(payload, Mapping):
        return _blocked("payload_invalid")
    blockers: list[str] = []
    if payload.get("schema_version") != SCHEMA_VERSION:
        blockers.append("schema_version_invalid")
    try:
        observables = _derive_observables(
            payload.get("source_memoryos_v059_certificate"),
            payload.get("source_memoryos_v058_certificate"),
        )
    except ValueError as exc:
        return _blocked(*(blockers + [str(exc)]))
    true_fields = (
        "source_memoryos_v059_exact",
        "source_memoryos_v058_exact",
        "source_v059_v058_bindings_exact",
        "two_step_kernel_exact",
        "two_step_doeblin_decomposition_exact",
        "residual_kernel_kl_data_processing_exact",
        "modified_log_sobolev_two_step_entropy_decay_exact",
        "iterated_modified_entropy_decay_exact",
        "all_reference_symbolic_kl_blocks_bound",
        "all_reference_hellinger_profiles_exact",
        "all_reference_separation_profiles_exact",
        "all_worst_case_separation_profiles_exact",
        "all_finite_cutoff_thresholds_exact",
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
        "modified_log_sobolev_witness_advisory_only",
        "hellinger_profile_not_candidate_preference",
        "separation_cutoff_not_activation_schedule",
        "finite_cutoff_not_asymptotic_cutoff_claim",
        "singular_boundary_not_information_recovery",
        "future_only",
        "read_only",
    )
    false_fields = (
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
    )
    for field in true_fields:
        if observables.get(field) is not True:
            blockers.append(f"required_{field}")
    for field in false_fields:
        if observables.get(field) is not False:
            blockers.append(f"forbidden_{field}")
    claims = payload.get("claims")
    if not isinstance(claims, Mapping):
        blockers.append("claims_invalid")
    else:
        for field, expected in observables.items():
            if claims.get(field) != expected:
                blockers.append(f"claim_mismatch_{field}")
    if blockers:
        return _blocked(*blockers)
    unsigned = {
        "accepted": True,
        "schema_version": SCHEMA_VERSION,
        "blockers": [],
        "observables": observables,
    }
    return {**unsigned, "certificate_digest": canonical_digest(unsigned)}
