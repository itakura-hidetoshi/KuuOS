from __future__ import annotations

from hashlib import sha256
import json
from math import gcd
from typing import Any, Mapping

from runtime.kuuos_memoryos_quotient_metric_density_transport_radon_nikodym_cocycle_certificate_kernel_v0_1 import (
    SCHEMA_VERSION as SOURCE_MEMORYOS_V054_SCHEMA_VERSION,
    SOURCE_MEMORYOS_V053_SCHEMA_VERSION,
    EXPECTED_CROSSES,
    _normalize_source_memoryos_v053,
)

SCHEMA_VERSION = (
    "kuuos.memoryos.relative-entropy-transport-lebesgue-decomposition-"
    "certificate.v0.1"
)


def canonical_digest(value: Any) -> str:
    return sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


def _blocked(*blockers: str) -> dict[str, Any]:
    return {
        "accepted": False,
        "schema_version": SCHEMA_VERSION,
        "blockers": sorted(set(blockers)),
        "observables": {},
        "certificate_digest": None,
    }


def _determinant(cross: int) -> int:
    return 4 - cross * cross


def _fraction(numerator: int, denominator: int) -> dict[str, int]:
    if denominator == 0:
        raise ValueError("fraction_denominator_zero")
    if denominator < 0:
        numerator, denominator = -numerator, -denominator
    divisor = gcd(abs(numerator), denominator)
    return {
        "numerator": numerator // divisor,
        "denominator": denominator // divisor,
    }


def _fraction_product(
    left: Mapping[str, int], right: Mapping[str, int]
) -> dict[str, int]:
    return _fraction(
        left["numerator"] * right["numerator"],
        left["denominator"] * right["denominator"],
    )


def _fraction_quotient(
    numerator: Mapping[str, int], denominator: Mapping[str, int]
) -> dict[str, int]:
    if denominator["numerator"] == 0:
        raise ValueError("fraction_quotient_denominator_zero")
    return _fraction(
        numerator["numerator"] * denominator["denominator"],
        numerator["denominator"] * denominator["numerator"],
    )


def _fraction_sum(values: list[Mapping[str, int]]) -> dict[str, int]:
    total = {"numerator": 0, "denominator": 1}
    for value in values:
        total = _fraction(
            total["numerator"] * value["denominator"]
            + value["numerator"] * total["denominator"],
            total["denominator"] * value["denominator"],
        )
    return total


def _require_boolean_fields(
    observables: Mapping[str, Any],
    required_true: tuple[str, ...],
    required_false: tuple[str, ...],
    source_name: str,
) -> None:
    for field in required_true:
        if observables.get(field) is not True:
            raise ValueError(f"{source_name}_required_{field}")
    for field in required_false:
        if observables.get(field) is not False:
            raise ValueError(f"{source_name}_forbidden_{field}")


def _normalize_source_memoryos_v054(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError("source_memoryos_v054_certificate_invalid")
    source = dict(value)
    if source.get("accepted") is not True:
        raise ValueError("source_memoryos_v054_not_accepted")
    if source.get("schema_version") != SOURCE_MEMORYOS_V054_SCHEMA_VERSION:
        raise ValueError("source_memoryos_v054_schema_invalid")
    digest = source.get("certificate_digest")
    if not isinstance(digest, str) or not digest:
        raise ValueError("source_memoryos_v054_certificate_digest_missing")
    unsigned = dict(source)
    unsigned.pop("certificate_digest", None)
    if canonical_digest(unsigned) != digest:
        raise ValueError("source_memoryos_v054_certificate_digest_mismatch")

    observables = source.get("observables")
    if not isinstance(observables, Mapping):
        raise ValueError("source_memoryos_v054_observables_invalid")
    observables = dict(observables)
    _require_boolean_fields(
        observables,
        (
            "source_memoryos_v053_exact",
            "source_memoryos_v052_exact",
            "source_jacobian_digest_bound",
            "source_mode_composition_digest_bound",
            "source_memoryos_v052_transport_digest_bound",
            "all_full_rank_density_multipliers_exact",
            "all_mode_density_products_exact",
            "all_finite_support_pushforward_pullback_witnesses_exact",
            "all_active_radon_nikodym_cocycles_exact",
            "full_rank_round_trip_density_preserved",
            "full_rank_to_rank_one_is_singular_measure_boundary",
            "rank_one_source_two_dimensional_density_not_recovered",
            "all_decision_candidates_retained",
            "all_planos_histories_retained",
            "all_quotient_coordinate_probes_retained",
            "relational_frontier_preserved",
            "required_review_set_preserved",
            "dissent_visibility_preserved",
            "minority_visibility_preserved",
            "density_witness_advisory_only",
            "density_transport_not_candidate_preference",
            "singular_boundary_not_information_recovery",
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
            "source_memoryos_v053_mutated",
            "source_memoryos_v052_mutated",
            "source_decisionos_v06_mutated",
            "persistent_world_state_mutated",
            "verification_result_claimed",
            "truth_authority_granted",
        ),
        "source_memoryos_v054",
    )

    expected_counts = {
        "transition_count": 9,
        "density_active_transition_count": 4,
        "probe_density_transport_record_count": 36,
        "singular_measure_collapse_transition_count": 2,
        "singular_probe_pushforward_record_count": 18,
        "rank_one_source_boundary_count": 3,
        "density_cocycle_record_count": 27,
        "active_density_cocycle_count": 8,
        "nontrivial_round_trip_density_path_count": 2,
    }
    for field, expected in expected_counts.items():
        if observables.get(field) != expected:
            raise ValueError(f"source_memoryos_v054_{field}_mismatch")

    candidate_ids = observables.get("retained_decision_candidate_ids")
    if candidate_ids != [
        "continue",
        "hold",
        "reobserve",
        "terminate_candidate",
    ]:
        raise ValueError("source_memoryos_v054_candidate_order_mismatch")
    history_ids = observables.get("retained_history_ids")
    if (
        not isinstance(history_ids, list)
        or len(history_ids) != 2
        or len(set(history_ids)) != 2
    ):
        raise ValueError("source_memoryos_v054_history_support_invalid")
    probe_ids = observables.get("retained_probe_ids")
    if (
        not isinstance(probe_ids, list)
        or len(probe_ids) != 9
        or len(set(probe_ids)) != 9
        or any(not isinstance(probe_id, str) for probe_id in probe_ids)
    ):
        raise ValueError("source_memoryos_v054_probe_support_invalid")

    transitions = observables.get("quotient_metric_density_transport_trajectory")
    transition_digest = observables.get(
        "quotient_metric_density_transport_digest"
    )
    if not isinstance(transitions, list) or len(transitions) != 9:
        raise ValueError("source_memoryos_v054_transition_trajectory_invalid")
    if canonical_digest(transitions) != transition_digest:
        raise ValueError("source_memoryos_v054_density_transport_digest_mismatch")

    expected_pairs = {
        (source_cross, target_cross)
        for source_cross in EXPECTED_CROSSES
        for target_cross in EXPECTED_CROSSES
    }
    transition_map: dict[tuple[int, int], dict[str, Any]] = {}
    for item in transitions:
        if not isinstance(item, Mapping):
            raise ValueError("source_memoryos_v054_transition_invalid")
        record = dict(item)
        pair = (
            record.get("source_cross_numerator"),
            record.get("target_cross_numerator"),
        )
        if pair not in expected_pairs or pair in transition_map:
            raise ValueError("source_memoryos_v054_transition_support_invalid")
        source_cross, target_cross = pair
        source_det = _determinant(source_cross)
        target_det = _determinant(target_cross)
        active = source_det != 0 and target_det != 0
        singular = source_det != 0 and target_det == 0
        rank_one_source = source_det == 0
        expected_density = (
            _fraction(source_det, target_det) if active else None
        )
        expected_jacobian = (
            _fraction(target_det, source_det) if source_det != 0 else None
        )
        expected_fields = {
            "source_metric_determinant": source_det,
            "target_metric_determinant": target_det,
            "density_transport_active": active,
            "full_rank_to_rank_one_singular_measure_boundary": singular,
            "rank_one_source_boundary": rank_one_source,
            "radon_nikodym_density_multiplier": expected_density,
            "source_normalized_jacobian": expected_jacobian,
        }
        for field, expected in expected_fields.items():
            if record.get(field) != expected:
                raise ValueError(
                    f"source_memoryos_v054_{field}_mismatch"
                )
        density_records = record.get("probe_density_transport_records")
        singular_records = record.get("singular_probe_pushforward_records")
        if active:
            if (
                not isinstance(density_records, list)
                or len(density_records) != 9
                or singular_records != []
            ):
                raise ValueError(
                    "source_memoryos_v054_active_probe_records_invalid"
                )
            record_probe_ids = [
                density_record.get("probe_id")
                for density_record in density_records
            ]
            if record_probe_ids != probe_ids:
                raise ValueError(
                    "source_memoryos_v054_active_probe_order_mismatch"
                )
            if not all(
                density_record.get("pushforward_mass_preserved") is True
                and density_record.get(
                    "pullback_density_recovers_source"
                ) is True
                and density_record.get("probe_retained") is True
                for density_record in density_records
            ):
                raise ValueError(
                    "source_memoryos_v054_active_probe_witness_mismatch"
                )
        elif singular:
            if (
                density_records != []
                or not isinstance(singular_records, list)
                or len(singular_records) != 9
            ):
                raise ValueError(
                    "source_memoryos_v054_singular_probe_records_invalid"
                )
            record_probe_ids = [
                singular_record.get("probe_id")
                for singular_record in singular_records
            ]
            if record_probe_ids != probe_ids:
                raise ValueError(
                    "source_memoryos_v054_singular_probe_order_mismatch"
                )
            if not all(
                singular_record.get(
                    "support_retained_as_singular_measure"
                ) is True
                and singular_record.get(
                    "two_dimensional_target_density_emitted"
                ) is False
                and singular_record.get("probe_retained") is True
                for singular_record in singular_records
            ):
                raise ValueError(
                    "source_memoryos_v054_singular_probe_witness_mismatch"
                )
        else:
            if density_records != [] or singular_records != []:
                raise ValueError(
                    "source_memoryos_v054_rank_one_probe_records_invalid"
                )
        transition_map[pair] = record
    if set(transition_map) != expected_pairs:
        raise ValueError("source_memoryos_v054_transition_support_incomplete")

    cocycles = observables.get("radon_nikodym_cocycle_records")
    cocycle_digest = observables.get("radon_nikodym_cocycle_digest")
    if not isinstance(cocycles, list) or len(cocycles) != 27:
        raise ValueError("source_memoryos_v054_cocycle_records_invalid")
    if canonical_digest(cocycles) != cocycle_digest:
        raise ValueError("source_memoryos_v054_cocycle_digest_mismatch")
    cocycle_map: dict[tuple[int, int, int], dict[str, Any]] = {}
    for item in cocycles:
        if not isinstance(item, Mapping):
            raise ValueError("source_memoryos_v054_cocycle_invalid")
        record = dict(item)
        triple = (
            record.get("source_cross_numerator"),
            record.get("middle_cross_numerator"),
            record.get("target_cross_numerator"),
        )
        if (
            any(cross not in EXPECTED_CROSSES for cross in triple)
            or triple in cocycle_map
        ):
            raise ValueError("source_memoryos_v054_cocycle_support_invalid")
        source_cross, middle_cross, target_cross = triple
        active = all(
            _determinant(cross) != 0
            for cross in (source_cross, middle_cross, target_cross)
        )
        if record.get("density_cocycle_active") is not active:
            raise ValueError(
                "source_memoryos_v054_cocycle_active_flag_mismatch"
            )
        if record.get("radon_nikodym_cocycle_exact") is not active:
            raise ValueError(
                "source_memoryos_v054_cocycle_exactness_mismatch"
            )
        cocycle_map[triple] = record
    if len(cocycle_map) != 27:
        raise ValueError("source_memoryos_v054_cocycle_support_incomplete")

    digest_fields = {
        "source_memoryos_v053_certificate_digest": "v053_certificate",
        "source_memoryos_v053_jacobian_digest": "v053_jacobian",
        "source_memoryos_v053_mode_composition_digest": "v053_mode_composition",
        "source_memoryos_v052_certificate_digest": "v052_certificate",
        "source_memoryos_v052_transport_digest": "v052_transport",
    }
    digests: dict[str, str] = {}
    for field, short_name in digest_fields.items():
        value = observables.get(field)
        if not isinstance(value, str) or not value:
            raise ValueError(
                f"source_memoryos_v054_{short_name}_digest_missing"
            )
        digests[field] = value

    review_fields: dict[str, list[str]] = {}
    for field in (
        "source_relational_frontier_candidate_ids",
        "source_required_review_candidate_ids",
        "source_dissent_review_candidate_ids",
        "source_minority_protection_candidate_ids",
    ):
        items = observables.get(field)
        if (
            not isinstance(items, list)
            or len(items) != len(set(items))
            or any(item not in candidate_ids for item in items)
        ):
            raise ValueError(f"source_memoryos_v054_{field}_invalid")
        review_fields[field] = list(items)

    return {
        "certificate_digest": digest,
        "density_transport_digest": transition_digest,
        "density_cocycle_digest": cocycle_digest,
        "candidate_ids": list(candidate_ids),
        "history_ids": list(history_ids),
        "probe_ids": list(probe_ids),
        "transitions": transition_map,
        "cocycles": cocycle_map,
        **digests,
        **review_fields,
    }


def _derive_observables(
    source_memoryos_v054_certificate: Mapping[str, Any],
    source_memoryos_v053_certificate: Mapping[str, Any],
) -> dict[str, Any]:
    v054 = _normalize_source_memoryos_v054(
        source_memoryos_v054_certificate
    )
    v053 = _normalize_source_memoryos_v053(
        source_memoryos_v053_certificate
    )
    bindings = (
        v054["source_memoryos_v053_certificate_digest"]
        == v053["certificate_digest"],
        v054["source_memoryos_v053_jacobian_digest"]
        == v053["jacobian_digest"],
        v054["source_memoryos_v053_mode_composition_digest"]
        == v053["mode_composition_digest"],
        v054["candidate_ids"] == v053["candidate_ids"],
        v054["history_ids"] == v053["history_ids"],
        v054["probe_ids"] == v053["probe_ids"],
    )
    binding_errors = (
        "source_v054_v053_certificate_binding_mismatch",
        "source_v054_v053_jacobian_binding_mismatch",
        "source_v054_v053_mode_composition_binding_mismatch",
        "source_v054_v053_candidate_support_mismatch",
        "source_v054_v053_history_support_mismatch",
        "source_v054_v053_probe_support_mismatch",
    )
    for exact, error in zip(bindings, binding_errors, strict=True):
        if not exact:
            raise ValueError(error)

    p_masses = {
        probe_id: _fraction(ordinal, 45)
        for ordinal, probe_id in enumerate(v054["probe_ids"], start=1)
    }
    q_masses = {
        probe_id: _fraction(10 - ordinal, 45)
        for ordinal, probe_id in enumerate(v054["probe_ids"], start=1)
    }
    if _fraction_sum(list(p_masses.values())) != {
        "numerator": 1,
        "denominator": 1,
    }:
        raise ValueError("reference_p_mass_not_normalized")
    if _fraction_sum(list(q_masses.values())) != {
        "numerator": 1,
        "denominator": 1,
    }:
        raise ValueError("reference_q_mass_not_normalized")

    transitions: list[dict[str, Any]] = []
    for source_cross in EXPECTED_CROSSES:
        for target_cross in EXPECTED_CROSSES:
            source_record = v054["transitions"][
                source_cross, target_cross
            ]
            active = source_record["density_transport_active"]
            singular = source_record[
                "full_rank_to_rank_one_singular_measure_boundary"
            ]
            rank_one_source = source_record["rank_one_source_boundary"]
            rho = source_record["radon_nikodym_density_multiplier"]
            jacobian = source_record["source_normalized_jacobian"]
            full_rank_records: list[dict[str, Any]] = []
            singular_records: list[dict[str, Any]] = []

            for probe_id in v054["probe_ids"]:
                p_mass = p_masses[probe_id]
                q_mass = q_masses[probe_id]
                likelihood_ratio = _fraction_quotient(p_mass, q_mass)
                reverse_likelihood_ratio = _fraction_quotient(
                    q_mass, p_mass
                )
                p_symbolic_term = {
                    "coefficient": p_mass,
                    "log_argument_ratio": likelihood_ratio,
                }
                q_symbolic_term = {
                    "coefficient": q_mass,
                    "log_argument_ratio": reverse_likelihood_ratio,
                }
                if active:
                    p_target_density = _fraction_product(p_mass, rho)
                    q_target_density = _fraction_product(q_mass, rho)
                    p_pushforward_mass = _fraction_product(
                        p_target_density, jacobian
                    )
                    q_pushforward_mass = _fraction_product(
                        q_target_density, jacobian
                    )
                    target_ratio = _fraction_quotient(
                        p_target_density, q_target_density
                    )
                    reverse_target_ratio = _fraction_quotient(
                        q_target_density, p_target_density
                    )
                    target_p_symbolic_term = {
                        "coefficient": p_pushforward_mass,
                        "log_argument_ratio": target_ratio,
                    }
                    target_q_symbolic_term = {
                        "coefficient": q_pushforward_mass,
                        "log_argument_ratio": reverse_target_ratio,
                    }
                    full_rank_records.append(
                        {
                            "probe_id": probe_id,
                            "p_source_mass": p_mass,
                            "q_source_mass": q_mass,
                            "source_likelihood_ratio": likelihood_ratio,
                            "target_likelihood_ratio": target_ratio,
                            "source_reverse_likelihood_ratio": reverse_likelihood_ratio,
                            "target_reverse_likelihood_ratio": reverse_target_ratio,
                            "p_target_density": p_target_density,
                            "q_target_density": q_target_density,
                            "target_coordinate_cell_volume": jacobian,
                            "p_pushforward_mass": p_pushforward_mass,
                            "q_pushforward_mass": q_pushforward_mass,
                            "source_relative_entropy_symbolic_term": p_symbolic_term,
                            "target_relative_entropy_symbolic_term": target_p_symbolic_term,
                            "source_reverse_relative_entropy_symbolic_term": q_symbolic_term,
                            "target_reverse_relative_entropy_symbolic_term": target_q_symbolic_term,
                            "likelihood_ratio_invariant": target_ratio == likelihood_ratio,
                            "reverse_likelihood_ratio_invariant": reverse_target_ratio == reverse_likelihood_ratio,
                            "p_mass_preserved": p_pushforward_mass == p_mass,
                            "q_mass_preserved": q_pushforward_mass == q_mass,
                            "relative_entropy_term_invariant": target_p_symbolic_term == p_symbolic_term,
                            "reverse_relative_entropy_term_invariant": target_q_symbolic_term == q_symbolic_term,
                            "probe_retained": True,
                        }
                    )
                elif singular:
                    singular_records.append(
                        {
                            "probe_id": probe_id,
                            "p_source_mass": p_mass,
                            "q_source_mass": q_mass,
                            "p_absolutely_continuous_mass": {"numerator": 0, "denominator": 1},
                            "q_absolutely_continuous_mass": {"numerator": 0, "denominator": 1},
                            "p_singular_mass": p_mass,
                            "q_singular_mass": q_mass,
                            "p_lebesgue_decomposition_exact": p_mass == _fraction_sum([{"numerator": 0, "denominator": 1}, p_mass]),
                            "q_lebesgue_decomposition_exact": q_mass == _fraction_sum([{"numerator": 0, "denominator": 1}, q_mass]),
                            "singular_likelihood_ratio": likelihood_ratio,
                            "singular_reverse_likelihood_ratio": reverse_likelihood_ratio,
                            "source_relative_entropy_symbolic_term": p_symbolic_term,
                            "singular_relative_entropy_symbolic_term": p_symbolic_term,
                            "source_reverse_relative_entropy_symbolic_term": q_symbolic_term,
                            "singular_reverse_relative_entropy_symbolic_term": q_symbolic_term,
                            "singular_atomic_relative_entropy_retained": True,
                            "two_dimensional_relative_entropy_density_emitted": False,
                            "probe_retained": True,
                        }
                    )

            source_forward_ledger = [
                {
                    "coefficient": p_masses[probe_id],
                    "log_argument_ratio": _fraction_quotient(
                        p_masses[probe_id], q_masses[probe_id]
                    ),
                }
                for probe_id in v054["probe_ids"]
            ]
            source_reverse_ledger = [
                {
                    "coefficient": q_masses[probe_id],
                    "log_argument_ratio": _fraction_quotient(
                        q_masses[probe_id], p_masses[probe_id]
                    ),
                }
                for probe_id in v054["probe_ids"]
            ]
            if active:
                target_forward_ledger = [
                    record["target_relative_entropy_symbolic_term"]
                    for record in full_rank_records
                ]
                target_reverse_ledger = [
                    record["target_reverse_relative_entropy_symbolic_term"]
                    for record in full_rank_records
                ]
            elif singular:
                target_forward_ledger = [
                    record["singular_relative_entropy_symbolic_term"]
                    for record in singular_records
                ]
                target_reverse_ledger = [
                    record["singular_reverse_relative_entropy_symbolic_term"]
                    for record in singular_records
                ]
            else:
                target_forward_ledger = []
                target_reverse_ledger = []

            transitions.append(
                {
                    "source_cross_numerator": source_cross,
                    "target_cross_numerator": target_cross,
                    "full_rank_relative_entropy_transport_active": active,
                    "singular_lebesgue_decomposition_active": singular,
                    "rank_one_source_boundary": rank_one_source,
                    "source_radon_nikodym_density_multiplier": rho,
                    "source_normalized_jacobian": jacobian,
                    "p_reference_mass_total": _fraction_sum(list(p_masses.values())),
                    "q_reference_mass_total": _fraction_sum(list(q_masses.values())),
                    "source_relative_entropy_symbolic_ledger": source_forward_ledger,
                    "target_relative_entropy_symbolic_ledger": target_forward_ledger,
                    "source_reverse_relative_entropy_symbolic_ledger": source_reverse_ledger,
                    "target_reverse_relative_entropy_symbolic_ledger": target_reverse_ledger,
                    "full_rank_probe_relative_entropy_records": full_rank_records,
                    "singular_probe_lebesgue_decomposition_records": singular_records,
                    "full_rank_relative_entropy_ledger_invariant": (
                        active
                        and target_forward_ledger == source_forward_ledger
                        and target_reverse_ledger == source_reverse_ledger
                        and all(
                            record["likelihood_ratio_invariant"]
                            and record["reverse_likelihood_ratio_invariant"]
                            and record["p_mass_preserved"]
                            and record["q_mass_preserved"]
                            and record["relative_entropy_term_invariant"]
                            and record["reverse_relative_entropy_term_invariant"]
                            for record in full_rank_records
                        )
                    ),
                    "singular_lebesgue_decomposition_exact": (
                        singular
                        and target_forward_ledger == source_forward_ledger
                        and target_reverse_ledger == source_reverse_ledger
                        and all(
                            record["p_lebesgue_decomposition_exact"]
                            and record["q_lebesgue_decomposition_exact"]
                            and record["singular_atomic_relative_entropy_retained"]
                            and not record["two_dimensional_relative_entropy_density_emitted"]
                            for record in singular_records
                        )
                    ),
                    "rank_one_source_two_dimensional_kl_recovery_claimed": False,
                    "source_memoryos_v054_density_transport_bound": (
                        source_record["source_metric_determinant"] == _determinant(source_cross)
                        and source_record["target_metric_determinant"] == _determinant(target_cross)
                    ),
                }
            )

    compositions: list[dict[str, Any]] = []
    transition_map = {
        (item["source_cross_numerator"], item["target_cross_numerator"]): item
        for item in transitions
    }
    for source_cross in EXPECTED_CROSSES:
        for middle_cross in EXPECTED_CROSSES:
            for target_cross in EXPECTED_CROSSES:
                source_cocycle = v054["cocycles"][source_cross, middle_cross, target_cross]
                active = source_cocycle["density_cocycle_active"]
                source_middle = transition_map[source_cross, middle_cross]
                middle_target = transition_map[middle_cross, target_cross]
                source_target = transition_map[source_cross, target_cross]
                entropy_cocycle_exact = (
                    active
                    and source_middle["full_rank_relative_entropy_ledger_invariant"]
                    and middle_target["full_rank_relative_entropy_ledger_invariant"]
                    and source_target["full_rank_relative_entropy_ledger_invariant"]
                    and source_middle["source_relative_entropy_symbolic_ledger"]
                    == middle_target["source_relative_entropy_symbolic_ledger"]
                    == source_target["source_relative_entropy_symbolic_ledger"]
                )
                compositions.append(
                    {
                        "source_cross_numerator": source_cross,
                        "middle_cross_numerator": middle_cross,
                        "target_cross_numerator": target_cross,
                        "relative_entropy_cocycle_active": active,
                        "relative_entropy_cocycle_exact": entropy_cocycle_exact,
                        "reverse_relative_entropy_cocycle_exact": entropy_cocycle_exact,
                        "nontrivial_round_trip_relative_entropy_preserved": (
                            entropy_cocycle_exact
                            and source_cross == target_cross
                            and source_cross != middle_cross
                        ),
                        "source_memoryos_v054_density_cocycle_bound": (
                            source_cocycle["radon_nikodym_cocycle_exact"] is active
                        ),
                    }
                )

    active_transitions = [
        item for item in transitions
        if item["full_rank_relative_entropy_transport_active"]
    ]
    singular_transitions = [
        item for item in transitions
        if item["singular_lebesgue_decomposition_active"]
    ]
    active_cocycles = [
        item for item in compositions
        if item["relative_entropy_cocycle_active"]
    ]
    first_probe_id = v054["probe_ids"][0]
    middle_probe_id = v054["probe_ids"][4]
    last_probe_id = v054["probe_ids"][-1]

    return {
        "input_digest": canonical_digest(
            {
                "schema_version": SCHEMA_VERSION,
                "source_memoryos_v054_certificate_digest": v054["certificate_digest"],
                "source_memoryos_v054_density_transport_digest": v054["density_transport_digest"],
                "source_memoryos_v054_density_cocycle_digest": v054["density_cocycle_digest"],
                "source_memoryos_v053_certificate_digest": v053["certificate_digest"],
                "source_memoryos_v053_jacobian_digest": v053["jacobian_digest"],
                "candidate_ids": v054["candidate_ids"],
                "history_ids": v054["history_ids"],
                "probe_ids": v054["probe_ids"],
            }
        ),
        "source_memoryos_v054_certificate_digest": v054["certificate_digest"],
        "source_memoryos_v054_density_transport_digest": v054["density_transport_digest"],
        "source_memoryos_v054_density_cocycle_digest": v054["density_cocycle_digest"],
        "source_memoryos_v053_certificate_digest": v053["certificate_digest"],
        "source_memoryos_v053_jacobian_digest": v053["jacobian_digest"],
        "source_memoryos_v053_mode_composition_digest": v053["mode_composition_digest"],
        "retained_history_ids": v054["history_ids"],
        "retained_decision_candidate_ids": v054["candidate_ids"],
        "retained_probe_ids": v054["probe_ids"],
        "reference_p_probe_masses": p_masses,
        "reference_q_probe_masses": q_masses,
        "reference_p_mass_total": _fraction_sum(list(p_masses.values())),
        "reference_q_mass_total": _fraction_sum(list(q_masses.values())),
        "reference_first_probe_likelihood_ratio": _fraction_quotient(p_masses[first_probe_id], q_masses[first_probe_id]),
        "reference_middle_probe_likelihood_ratio": _fraction_quotient(p_masses[middle_probe_id], q_masses[middle_probe_id]),
        "reference_last_probe_likelihood_ratio": _fraction_quotient(p_masses[last_probe_id], q_masses[last_probe_id]),
        "relative_entropy_transport_trajectory": transitions,
        "relative_entropy_transport_digest": canonical_digest(transitions),
        "relative_entropy_cocycle_records": compositions,
        "relative_entropy_cocycle_digest": canonical_digest(compositions),
        "transition_count": len(transitions),
        "full_rank_relative_entropy_transition_count": len(active_transitions),
        "full_rank_probe_relative_entropy_record_count": sum(
            len(item["full_rank_probe_relative_entropy_records"])
            for item in transitions
        ),
        "singular_lebesgue_decomposition_transition_count": len(singular_transitions),
        "singular_probe_lebesgue_decomposition_record_count": sum(
            len(item["singular_probe_lebesgue_decomposition_records"])
            for item in transitions
        ),
        "singular_atomic_relative_entropy_record_count": sum(
            len(item["singular_probe_lebesgue_decomposition_records"])
            for item in transitions
        ),
        "rank_one_source_boundary_count": sum(
            item["rank_one_source_boundary"] for item in transitions
        ),
        "relative_entropy_cocycle_record_count": len(compositions),
        "active_relative_entropy_cocycle_count": len(active_cocycles),
        "nontrivial_round_trip_relative_entropy_path_count": sum(
            item["nontrivial_round_trip_relative_entropy_preserved"]
            for item in compositions
        ),
        "source_memoryos_v054_exact": True,
        "source_memoryos_v053_exact": True,
        "source_density_transport_digest_bound": True,
        "source_density_cocycle_digest_bound": True,
        "source_jacobian_digest_bound": True,
        "reference_probability_masses_exact": (
            _fraction_sum(list(p_masses.values())) == {"numerator": 1, "denominator": 1}
            and _fraction_sum(list(q_masses.values())) == {"numerator": 1, "denominator": 1}
        ),
        "all_reference_likelihood_ratios_exact": all(
            _fraction_product(
                _fraction_quotient(p_masses[probe_id], q_masses[probe_id]),
                q_masses[probe_id],
            ) == p_masses[probe_id]
            for probe_id in v054["probe_ids"]
        ),
        "all_full_rank_relative_entropy_terms_invariant": all(
            item["full_rank_relative_entropy_ledger_invariant"]
            and item["source_memoryos_v054_density_transport_bound"]
            for item in active_transitions
        ),
        "all_reverse_relative_entropy_terms_invariant": all(
            item["full_rank_relative_entropy_ledger_invariant"]
            for item in active_transitions
        ),
        "all_relative_entropy_cocycles_exact": all(
            item["relative_entropy_cocycle_exact"]
            and item["reverse_relative_entropy_cocycle_exact"]
            and item["source_memoryos_v054_density_cocycle_bound"]
            for item in active_cocycles
        ),
        "full_rank_round_trip_relative_entropy_preserved": (
            sum(
                item["nontrivial_round_trip_relative_entropy_preserved"]
                for item in compositions
            ) == 2
        ),
        "all_singular_lebesgue_decompositions_exact": all(
            item["singular_lebesgue_decomposition_exact"]
            for item in singular_transitions
        ),
        "singular_atomic_relative_entropy_retained": all(
            record["singular_atomic_relative_entropy_retained"]
            for item in singular_transitions
            for record in item["singular_probe_lebesgue_decomposition_records"]
        ),
        "rank_one_source_two_dimensional_kl_not_recovered": all(
            not item["rank_one_source_two_dimensional_kl_recovery_claimed"]
            and item["target_relative_entropy_symbolic_ledger"] == []
            for item in transitions
            if item["rank_one_source_boundary"]
        ),
        "all_decision_candidates_retained": True,
        "all_planos_histories_retained": True,
        "all_quotient_coordinate_probes_retained": True,
        "source_relational_frontier_candidate_ids": v054["source_relational_frontier_candidate_ids"],
        "source_required_review_candidate_ids": v054["source_required_review_candidate_ids"],
        "source_dissent_review_candidate_ids": v054["source_dissent_review_candidate_ids"],
        "source_minority_protection_candidate_ids": v054["source_minority_protection_candidate_ids"],
        "relational_frontier_preserved": True,
        "required_review_set_preserved": True,
        "dissent_visibility_preserved": True,
        "minority_visibility_preserved": True,
        "relative_entropy_witness_advisory_only": True,
        "relative_entropy_not_candidate_preference": True,
        "singular_decomposition_not_information_recovery": True,
        "candidate_ranking_performed": False,
        "candidate_pruning_performed": False,
        "candidate_selection_performed": False,
        "decision_commit_performed": False,
        "decision_receipt_issued": False,
        "plan_synthesis_performed": False,
        "activation_performed": False,
        "execution_permission": False,
        "source_memoryos_v054_mutated": False,
        "source_memoryos_v053_mutated": False,
        "source_decisionos_v06_mutated": False,
        "persistent_world_state_mutated": False,
        "verification_result_claimed": False,
        "truth_authority_granted": False,
        "future_only": True,
        "read_only": True,
    }


def issue_relative_entropy_transport_lebesgue_decomposition_certificate(
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    if not isinstance(payload, Mapping):
        return _blocked("payload_invalid")
    blockers: list[str] = []
    if payload.get("schema_version") != SCHEMA_VERSION:
        blockers.append("schema_version_invalid")
    try:
        observables = _derive_observables(
            payload.get("source_memoryos_v054_certificate"),
            payload.get("source_memoryos_v053_certificate"),
        )
    except ValueError as exc:
        return _blocked(*(blockers + [str(exc)]))

    required_true = (
        "source_memoryos_v054_exact",
        "source_memoryos_v053_exact",
        "source_density_transport_digest_bound",
        "source_density_cocycle_digest_bound",
        "source_jacobian_digest_bound",
        "reference_probability_masses_exact",
        "all_reference_likelihood_ratios_exact",
        "all_full_rank_relative_entropy_terms_invariant",
        "all_reverse_relative_entropy_terms_invariant",
        "all_relative_entropy_cocycles_exact",
        "full_rank_round_trip_relative_entropy_preserved",
        "all_singular_lebesgue_decompositions_exact",
        "singular_atomic_relative_entropy_retained",
        "rank_one_source_two_dimensional_kl_not_recovered",
        "all_decision_candidates_retained",
        "all_planos_histories_retained",
        "all_quotient_coordinate_probes_retained",
        "relational_frontier_preserved",
        "required_review_set_preserved",
        "dissent_visibility_preserved",
        "minority_visibility_preserved",
        "relative_entropy_witness_advisory_only",
        "relative_entropy_not_candidate_preference",
        "singular_decomposition_not_information_recovery",
        "future_only",
        "read_only",
    )
    required_false = (
        "candidate_ranking_performed",
        "candidate_pruning_performed",
        "candidate_selection_performed",
        "decision_commit_performed",
        "decision_receipt_issued",
        "plan_synthesis_performed",
        "activation_performed",
        "execution_permission",
        "source_memoryos_v054_mutated",
        "source_memoryos_v053_mutated",
        "source_decisionos_v06_mutated",
        "persistent_world_state_mutated",
        "verification_result_claimed",
        "truth_authority_granted",
    )
    for field in required_true:
        if observables.get(field) is not True:
            blockers.append("observable_required_" + field)
    for field in required_false:
        if observables.get(field) is not False:
            blockers.append("observable_forbidden_" + field)

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
    "SOURCE_MEMORYOS_V054_SCHEMA_VERSION",
    "SOURCE_MEMORYOS_V053_SCHEMA_VERSION",
    "EXPECTED_CROSSES",
    "canonical_digest",
    "_derive_observables",
    "_normalize_source_memoryos_v054",
    "issue_relative_entropy_transport_lebesgue_decomposition_certificate",
]
