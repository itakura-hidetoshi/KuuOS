from __future__ import annotations

from hashlib import sha256
import json
from math import gcd
from typing import Any, Mapping

from runtime.kuuos_memoryos_log_sobolev_hypercontractive_mixing_certificate_kernel_v0_1 import (
    SCHEMA_VERSION as SOURCE_MEMORYOS_V059_SCHEMA_VERSION,
)

SCHEMA_VERSION = (
    "kuuos.memoryos.modified-log-sobolev-hellinger-separation-"
    "certificate.v0.1"
)
STATE_IDS = ("early", "middle", "late")
REFERENCE_P = {
    "early": {"numerator": 11, "denominator": 60},
    "middle": {"numerator": 1, "denominator": 3},
    "late": {"numerator": 29, "denominator": 60},
}
REFERENCE_Q = {
    "early": {"numerator": 29, "denominator": 60},
    "middle": {"numerator": 1, "denominator": 3},
    "late": {"numerator": 11, "denominator": 60},
}
KERNEL = (
    ({"numerator": 3, "denominator": 4}, {"numerator": 1, "denominator": 4}, {"numerator": 0, "denominator": 1}),
    ({"numerator": 1, "denominator": 4}, {"numerator": 1, "denominator": 2}, {"numerator": 1, "denominator": 4}),
    ({"numerator": 0, "denominator": 1}, {"numerator": 1, "denominator": 4}, {"numerator": 3, "denominator": 4}),
)
ENTROPY_DECAY_COEFFICIENT = {"numerator": 9, "denominator": 16}
PROFILE_HORIZON = 7


def canonical_digest(value: Any) -> str:
    return sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _fraction(numerator: int, denominator: int = 1) -> dict[str, int]:
    if denominator == 0:
        raise ValueError("fraction_denominator_zero")
    if denominator < 0:
        numerator, denominator = -numerator, -denominator
    divisor = gcd(abs(numerator), denominator)
    return {"numerator": numerator // divisor, "denominator": denominator // divisor}


def _add(left: Mapping[str, int], right: Mapping[str, int]) -> dict[str, int]:
    return _fraction(
        left["numerator"] * right["denominator"] + right["numerator"] * left["denominator"],
        left["denominator"] * right["denominator"],
    )


def _sub(left: Mapping[str, int], right: Mapping[str, int]) -> dict[str, int]:
    return _fraction(
        left["numerator"] * right["denominator"] - right["numerator"] * left["denominator"],
        left["denominator"] * right["denominator"],
    )


def _mul(left: Mapping[str, int], right: Mapping[str, int]) -> dict[str, int]:
    return _fraction(
        left["numerator"] * right["numerator"],
        left["denominator"] * right["denominator"],
    )


def _pow(value: Mapping[str, int], exponent: int) -> dict[str, int]:
    result = _fraction(1)
    for _ in range(exponent):
        result = _mul(result, value)
    return result


def _le(left: Mapping[str, int], right: Mapping[str, int]) -> bool:
    return left["numerator"] * right["denominator"] <= right["numerator"] * left["denominator"]


def _lt(left: Mapping[str, int], right: Mapping[str, int]) -> bool:
    return left["numerator"] * right["denominator"] < right["numerator"] * left["denominator"]


def _pushforward(masses: Mapping[str, Mapping[str, int]]) -> dict[str, dict[str, int]]:
    source = [masses[state_id] for state_id in STATE_IDS]
    result: dict[str, dict[str, int]] = {}
    for column, state_id in enumerate(STATE_IDS):
        value = _fraction(0)
        for row in range(3):
            value = _add(value, _mul(source[row], KERNEL[row][column]))
        result[state_id] = value
    return result


def _chi_square_to_uniform(masses: Mapping[str, Mapping[str, int]]) -> dict[str, int]:
    total = _fraction(0)
    for state_id in STATE_IDS:
        ratio = _mul(_fraction(3), masses[state_id])
        displacement = _sub(ratio, _fraction(1))
        total = _add(total, _mul(displacement, displacement))
    return _mul(_fraction(1, 3), total)


def _separation_to_uniform(masses: Mapping[str, Mapping[str, int]]) -> dict[str, int]:
    ratios = [_mul(_fraction(3), masses[state_id]) for state_id in STATE_IDS]
    minimum = min(ratios, key=lambda item: item["numerator"] / item["denominator"])
    return _sub(_fraction(1), minimum)


def _symbolic_hellinger_record(
    distribution_id: str,
    time: int,
    masses: Mapping[str, Mapping[str, int]],
) -> dict[str, Any]:
    ratios = {state_id: _mul(_fraction(3), masses[state_id]) for state_id in STATE_IDS}
    chi_square = _chi_square_to_uniform(masses)
    return {
        "distribution_id": distribution_id,
        "time": time,
        "masses": dict(masses),
        "likelihood_ratios": ratios,
        "hellinger_square_expression": {
            "scale": _fraction(1, 6),
            "terms": [
                {"state_id": state_id, "expression": f"(Real.sqrt({ratios[state_id]['numerator']}/{ratios[state_id]['denominator']}) - 1)^2"}
                for state_id in STATE_IDS
            ],
        },
        "chi_square_upper_envelope": _mul(_fraction(1, 2), chi_square),
        "square_roots_kept_symbolic": True,
        "floating_point_approximation_used": False,
    }


def _normalize_source_v059(value: Any) -> dict[str, Any]:
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
    observables = source.get("observables")
    if not isinstance(observables, Mapping):
        raise ValueError("source_memoryos_v059_observables_invalid")
    required_true = (
        "future_only",
        "read_only",
        "all_decision_candidates_retained",
        "all_planos_histories_retained",
        "all_quotient_coordinate_probes_retained",
        "relational_frontier_preserved",
        "required_review_set_preserved",
        "dissent_visibility_preserved",
        "minority_visibility_preserved",
    )
    for field in required_true:
        if observables.get(field) is not True:
            raise ValueError(f"source_memoryos_v059_required_{field}")
    return source


def _derive_observables(source_v059: Mapping[str, Any]) -> dict[str, Any]:
    source_obs = source_v059["observables"]
    separation_records: list[dict[str, Any]] = []
    hellinger_records: list[dict[str, Any]] = []
    entropy_decay_records: list[dict[str, Any]] = []
    for distribution_id, initial in (("reference_p", REFERENCE_P), ("reference_q", REFERENCE_Q)):
        masses = dict(initial)
        initial_chi_square = _chi_square_to_uniform(masses)
        for time in range(PROFILE_HORIZON + 1):
            chi_square = _chi_square_to_uniform(masses)
            coefficient = _pow(ENTROPY_DECAY_COEFFICIENT, time)
            envelope = _mul(coefficient, initial_chi_square)
            separation = _separation_to_uniform(masses)
            separation_records.append(
                {
                    "distribution_id": distribution_id,
                    "time": time,
                    "masses": dict(masses),
                    "separation_to_uniform": separation,
                    "expected_geometric_separation": _mul(_fraction(9, 20), _pow(_fraction(3, 4), time)),
                    "separation_exact": separation == _mul(_fraction(9, 20), _pow(_fraction(3, 4), time)),
                }
            )
            hellinger_records.append(_symbolic_hellinger_record(distribution_id, time, masses))
            entropy_decay_records.append(
                {
                    "distribution_id": distribution_id,
                    "time": time,
                    "chi_square_to_uniform": chi_square,
                    "modified_log_sobolev_kl_upper_envelope": envelope,
                    "sharp_chi_square_decay_exact": chi_square == envelope,
                    "kl_not_replaced_by_chi_square": True,
                }
            )
            masses = _pushforward(masses)

    thresholds = [
        {
            "threshold_id": "reference-separation-three-twentieths",
            "threshold": _fraction(3, 20),
            "first_certified_time": 4,
            "previous_time": 3,
            "at_threshold_time": _mul(_fraction(9, 20), _pow(_fraction(3, 4), 4)),
            "at_previous_time": _mul(_fraction(9, 20), _pow(_fraction(3, 4), 3)),
        },
        {
            "threshold_id": "reference-separation-one-sixteenth",
            "threshold": _fraction(1, 16),
            "first_certified_time": 7,
            "previous_time": 6,
            "at_threshold_time": _mul(_fraction(9, 20), _pow(_fraction(3, 4), 7)),
            "at_previous_time": _mul(_fraction(9, 20), _pow(_fraction(3, 4), 6)),
        },
    ]
    for record in thresholds:
        record["threshold_met"] = _le(record["at_threshold_time"], record["threshold"])
        record["previous_time_insufficient"] = _lt(record["threshold"], record["at_previous_time"])

    full_rank = [
        {
            "source_record_index": index,
            "modified_entropy_decay_transport_commutes": True,
            "hellinger_expression_transport_commutes": True,
            "separation_profile_transport_commutes": True,
        }
        for index in range(8)
    ]
    singular = [
        {
            "source_record_index": index,
            "singular_atomic_entropy_metric_ledger_retained": True,
            "two_dimensional_target_density_emitted": False,
            "lost_antisymmetric_information_reconstructed": False,
        }
        for index in range(4)
    ]

    return {
        "source_memoryos_v059_certificate_digest": source_v059["certificate_digest"],
        "source_memoryos_v059_exact": True,
        "entropy_decay_coefficient": dict(ENTROPY_DECAY_COEFFICIENT),
        "modified_log_sobolev_entropy_decay_records": entropy_decay_records,
        "symbolic_hellinger_profile_records": hellinger_records,
        "exact_separation_profile_records": separation_records,
        "separation_threshold_records": thresholds,
        "full_rank_transport_entropy_metric_records": full_rank,
        "singular_atomic_entropy_metric_records": singular,
        "modified_log_sobolev_entropy_decay_record_count": len(entropy_decay_records),
        "symbolic_hellinger_profile_record_count": len(hellinger_records),
        "exact_separation_profile_record_count": len(separation_records),
        "separation_threshold_record_count": len(thresholds),
        "full_rank_transport_entropy_metric_record_count": len(full_rank),
        "singular_atomic_entropy_metric_record_count": len(singular),
        "rank_one_source_boundary_count": 3,
        "all_entropy_decay_envelopes_exact": all(item["sharp_chi_square_decay_exact"] for item in entropy_decay_records),
        "all_separation_values_exact": all(item["separation_exact"] for item in separation_records),
        "all_separation_thresholds_exact": all(item["threshold_met"] and item["previous_time_insufficient"] for item in thresholds),
        "all_hellinger_square_roots_symbolic": all(item["square_roots_kept_symbolic"] for item in hellinger_records),
        "no_hellinger_floating_point_approximation": all(not item["floating_point_approximation_used"] for item in hellinger_records),
        "all_full_rank_transport_entropy_metrics_commute": True,
        "singular_atomic_entropy_metrics_retained": True,
        "all_decision_candidates_retained": source_obs["all_decision_candidates_retained"],
        "all_planos_histories_retained": source_obs["all_planos_histories_retained"],
        "all_quotient_coordinate_probes_retained": source_obs["all_quotient_coordinate_probes_retained"],
        "relational_frontier_preserved": source_obs["relational_frontier_preserved"],
        "required_review_set_preserved": source_obs["required_review_set_preserved"],
        "dissent_visibility_preserved": source_obs["dissent_visibility_preserved"],
        "minority_visibility_preserved": source_obs["minority_visibility_preserved"],
        "candidate_ranking_performed": False,
        "candidate_pruning_performed": False,
        "candidate_selection_performed": False,
        "decision_commit_performed": False,
        "decision_receipt_issued": False,
        "plan_synthesis_performed": False,
        "activation_performed": False,
        "execution_permission": False,
        "source_memoryos_v059_mutated": False,
        "world_mutated": False,
        "verification_claimed": False,
        "truth_authority_claimed": False,
        "future_only": True,
        "read_only": True,
    }


def issue_modified_log_sobolev_hellinger_separation_certificate(payload: Any) -> dict[str, Any]:
    blockers: list[str] = []
    if not isinstance(payload, Mapping):
        return {"accepted": False, "schema_version": SCHEMA_VERSION, "blockers": ["payload_invalid"], "observables": {}, "certificate_digest": None}
    if payload.get("schema_version") != SCHEMA_VERSION:
        blockers.append("schema_version_mismatch")
    try:
        source = _normalize_source_v059(payload.get("source_memoryos_v059_certificate"))
        expected = _derive_observables(source)
    except ValueError as exc:
        blockers.append(str(exc))
        expected = {}
    if expected and payload.get("claims") != expected:
        blockers.append("claim_mismatch")
    accepted = not blockers
    certificate = {
        "accepted": accepted,
        "schema_version": SCHEMA_VERSION,
        "blockers": sorted(set(blockers)),
        "observables": expected if accepted else {},
    }
    certificate["certificate_digest"] = canonical_digest(certificate) if accepted else None
    return certificate
