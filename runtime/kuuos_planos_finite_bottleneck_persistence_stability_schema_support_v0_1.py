from __future__ import annotations

from typing import Any

from runtime.kuuos_planos_finite_filtration_persistent_homology_certificate_support_v0_1 import (
    canonical_digest,
)


def _nat(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _unique_text(value: Any, seen: set[str], invalid: str, duplicate: str):
    if not isinstance(value, str) or not value:
        return False, invalid
    if value in seen:
        return False, duplicate
    seen.add(value)
    return True, ""


def normalize_diagram_intervals(values: Any, side: str, maximum_coordinate: int):
    if not isinstance(values, list) or not values:
        return [f"diagram_{side}_intervals_empty"], []
    fields = {
        "interval_id",
        "dimension",
        "birth",
        "death",
        "birth_simplex_id",
        "death_simplex_id",
        "source_interval_digest",
    }
    blockers, out, ids, digests = [], [], set(), set()
    for index, item in enumerate(values):
        if not isinstance(item, dict) or set(item) != fields:
            blockers.append(f"diagram_{side}_interval_schema_invalid_{index}")
            continue
        interval_id = item["interval_id"]
        ok, reason = _unique_text(
            interval_id,
            ids,
            f"diagram_{side}_interval_id_invalid_{index}",
            f"duplicate_diagram_{side}_interval_id",
        )
        if not ok:
            blockers.append(reason)
            continue
        dimension, birth, death = item["dimension"], item["birth"], item["death"]
        if (
            not _nat(dimension)
            or dimension > 2
            or not _nat(birth)
            or birth > maximum_coordinate
            or (
                death is not None
                and (
                    not _nat(death)
                    or death > maximum_coordinate
                    or death <= birth
                )
            )
        ):
            blockers.append(f"diagram_{side}_interval_numeric_invalid_{interval_id}")
            continue
        birth_id, death_id = item["birth_simplex_id"], item["death_simplex_id"]
        if (
            not isinstance(birth_id, str)
            or not birth_id
            or not isinstance(death_id, str)
            or (death is None) != (death_id == "")
        ):
            blockers.append(f"diagram_{side}_simplex_binding_invalid_{interval_id}")
            continue
        digest = item["source_interval_digest"]
        ok, reason = _unique_text(
            digest,
            digests,
            f"diagram_{side}_source_interval_digest_missing_{interval_id}",
            f"duplicate_diagram_{side}_source_interval_digest",
        )
        if not ok:
            blockers.append(reason)
            continue
        out.append(dict(item))
    key = lambda item: (
        item["dimension"],
        item["birth"],
        item["death"] is None,
        item["death"] if item["death"] is not None else 10**18,
        item["interval_id"],
    )
    return blockers, sorted(out, key=key)


def normalize_perturbation_records(values: Any, maximum_coordinate: int):
    if not isinstance(values, list) or not values:
        return ["simplex_perturbation_records_empty"], []
    fields = {
        "simplex_id",
        "dimension",
        "filtration_a",
        "filtration_b",
        "source_simplex_digest_a",
        "source_simplex_digest_b",
    }
    blockers, out, ids, digests_a, digests_b = [], [], set(), set(), set()
    for index, item in enumerate(values):
        if not isinstance(item, dict) or set(item) != fields:
            blockers.append(f"simplex_perturbation_schema_invalid_{index}")
            continue
        simplex_id = item["simplex_id"]
        ok, reason = _unique_text(
            simplex_id,
            ids,
            f"simplex_perturbation_id_invalid_{index}",
            "duplicate_simplex_perturbation_id",
        )
        if not ok:
            blockers.append(reason)
            continue
        if (
            not _nat(item["dimension"])
            or item["dimension"] > 2
            or not _nat(item["filtration_a"])
            or item["filtration_a"] > maximum_coordinate
            or not _nat(item["filtration_b"])
            or item["filtration_b"] > maximum_coordinate
        ):
            blockers.append(f"simplex_perturbation_numeric_invalid_{simplex_id}")
            continue
        for side, seen in (("a", digests_a), ("b", digests_b)):
            digest = item[f"source_simplex_digest_{side}"]
            ok, reason = _unique_text(
                digest,
                seen,
                f"source_simplex_digest_{side}_missing_{simplex_id}",
                f"duplicate_source_simplex_digest_{side}",
            )
            if not ok:
                blockers.append(reason)
        out.append(dict(item))
    return blockers, sorted(out, key=lambda item: (item["dimension"], item["simplex_id"]))


def normalize_matching_claims(values: Any):
    if not isinstance(values, list) or not values:
        return ["claimed_optimal_matching_empty"], []
    fields = {
        "match_id",
        "dimension",
        "match_kind",
        "left_interval_id",
        "right_interval_id",
        "cost_twice",
    }
    allowed = {"point_to_point", "left_to_diagonal", "diagonal_to_right"}
    blockers, out, ids = [], [], set()
    for index, item in enumerate(values):
        if not isinstance(item, dict) or set(item) != fields:
            blockers.append(f"matching_claim_schema_invalid_{index}")
            continue
        match_id = item["match_id"]
        ok, reason = _unique_text(
            match_id,
            ids,
            f"matching_claim_id_invalid_{index}",
            "duplicate_matching_claim_id",
        )
        if not ok:
            blockers.append(reason)
            continue
        dimension, kind = item["dimension"], item["match_kind"]
        left, right, cost = (
            item["left_interval_id"],
            item["right_interval_id"],
            item["cost_twice"],
        )
        if not _nat(dimension) or dimension > 2 or kind not in allowed or not _nat(cost):
            blockers.append(f"matching_claim_numeric_or_kind_invalid_{match_id}")
            continue
        if not isinstance(left, str) or not isinstance(right, str):
            blockers.append(f"matching_claim_interval_ids_invalid_{match_id}")
            continue
        valid_binding = (
            (kind == "point_to_point" and bool(left) and bool(right))
            or (kind == "left_to_diagonal" and bool(left) and not right)
            or (kind == "diagonal_to_right" and not left and bool(right))
        )
        if not valid_binding:
            blockers.append(f"matching_claim_binding_invalid_{match_id}")
            continue
        out.append(dict(item))
    return blockers, sorted(out, key=lambda item: item["match_id"])


def compute_bottleneck_stability_input_digest(**payload):
    return canonical_digest(payload)
