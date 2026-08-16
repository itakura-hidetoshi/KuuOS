from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import math
from typing import Any, Mapping

from runtime.kuuos_qi_yinyang_wuxing_fibonacci_history_geometry_v2_5 import (
    VERSION as V2_5_VERSION,
    advance_history,
)

VERSION = "kuuos_qi_wuxing_generation_control_coherence_v2_6"
RECEIPT_VERSION = "kuuos_qi_wuxing_generation_control_coherence_receipt_v2_6"
STATUS_OK = "KUUOS_QI_WUXING_GENERATION_CONTROL_COHERENCE_V2_6_OK"

RELATIONS: dict[str, dict[str, int]] = {
    "generation": {"phase_delta": 1, "history_events": 1},
    "control": {"phase_delta": 2, "history_events": 1},
    "insult": {"phase_delta": -2, "history_events": 1},
    "mother": {"phase_delta": -1, "history_events": 1},
    "child": {"phase_delta": 1, "history_events": 1},
}

NON_AUTHORITY = {
    "grants_execution_authority": False,
    "grants_truth_authority": False,
    "grants_final_commitment_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_clinical_authority": False,
    "grants_theorem_authority": False,
    "updates_exact_world": False,
    "claims_strength_is_qi_quantity": False,
    "claims_nominal_strength_is_clinical_threshold": False,
    "claims_overacting_is_clinical_diagnosis": False,
    "claims_center_is_earth_substance": False,
    "claims_classical_wuxing_is_physical_gauge_theory": False,
    "claims_physical_anyon_realization": False,
}


def _stable_digest(value: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(value))
    payload.pop("generation_control_coherence_receipt_digest", None)
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _phase(value: Any) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        return 0
    return value % 5


def _history_pair(resolved: Any, active: Any) -> tuple[int, int]:
    if isinstance(resolved, bool) or not isinstance(resolved, int) or resolved < 0:
        resolved = 0
    if isinstance(active, bool) or not isinstance(active, int) or active < 0:
        active = 0
    return resolved, active


def _strength(value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return 0.0
    numeric = float(value)
    if not math.isfinite(numeric) or numeric < 0.0:
        return 0.0
    return numeric


def advance_history_n(resolved: int, active: int, steps: int) -> tuple[int, int]:
    resolved, active = _history_pair(resolved, active)
    bounded_steps = steps if isinstance(steps, int) and not isinstance(steps, bool) and steps >= 0 else 0
    for _ in range(bounded_steps):
        resolved, active = advance_history(resolved, active)
    return resolved, active


def relation_shift(relation: str) -> dict[str, int]:
    if relation not in RELATIONS:
        raise ValueError(f"unknown Wuxing relation: {relation}")
    return dict(RELATIONS[relation])


def compose_shifts(first: Mapping[str, int], second: Mapping[str, int]) -> dict[str, int]:
    return {
        "phase_delta": int(first["phase_delta"]) + int(second["phase_delta"]),
        "history_events": int(first["history_events"]) + int(second["history_events"]),
    }


def apply_shift(
    *,
    phase_index: int,
    resolved_channels: int,
    active_channels: int,
    shift: Mapping[str, int],
) -> dict[str, int]:
    phase_index = _phase(phase_index)
    resolved_channels, active_channels = _history_pair(resolved_channels, active_channels)
    history_events = int(shift["history_events"])
    if history_events < 0:
        raise ValueError("history_events must be nonnegative")
    resolved_channels, active_channels = advance_history_n(
        resolved_channels,
        active_channels,
        history_events,
    )
    return {
        "phase_index": (phase_index + int(shift["phase_delta"])) % 5,
        "resolved_channels": resolved_channels,
        "active_channels": active_channels,
    }


def apply_relation(
    relation: str,
    *,
    phase_index: int,
    resolved_channels: int,
    active_channels: int,
) -> dict[str, int]:
    return apply_shift(
        phase_index=phase_index,
        resolved_channels=resolved_channels,
        active_channels=active_channels,
        shift=relation_shift(relation),
    )


def classify_strength(nominal: Any, actual: Any) -> str:
    nominal_value = _strength(nominal)
    actual_value = _strength(actual)
    if actual_value < nominal_value:
        return "under"
    if actual_value == nominal_value:
        return "balanced"
    return "over"


def is_overacting_control(relation: str, *, nominal: Any, actual: Any) -> bool:
    return bool(relation == "control" and classify_strength(nominal, actual) == "over")


def _v2_5_dependency_visible(receipt: Mapping[str, Any]) -> bool:
    base = receipt.get("five_phase_base_surface", {})
    history = receipt.get("fibonacci_history_fibre_surface", {})
    operational = receipt.get("operational_surface", {})
    non_authority = receipt.get("non_authority", {})
    return bool(
        receipt.get("version") == V2_5_VERSION
        and isinstance(base, Mapping)
        and base.get("carrier") == "Z5"
        and base.get("phase_is_relational_coordinate_not_substance") is True
        and isinstance(history, Mapping)
        and history.get("history_is_path_multiplicity_not_qi_quantity") is True
        and isinstance(operational, Mapping)
        and operational.get("history_lineage_must_not_be_erased_on_phase_return") is True
        and isinstance(non_authority, Mapping)
        and non_authority
        and all(value is False for value in non_authority.values())
    )


def _coherence_sample() -> dict[str, Any]:
    initial = {
        "phase_index": 4,
        "resolved_channels": 1,
        "active_channels": 0,
    }
    first = relation_shift("control")
    second = relation_shift("insult")
    composed = compose_shifts(first, second)
    direct = apply_shift(**initial, shift=composed)
    after_first = apply_shift(**initial, shift=first)
    sequential = apply_shift(**after_first, shift=second)
    return {
        "initial": initial,
        "first": first,
        "second": second,
        "composed": composed,
        "direct": direct,
        "sequential": sequential,
        "verified": direct == sequential,
    }


def build_wuxing_generation_control_coherence_receipt(
    v2_5_receipt: Mapping[str, Any],
    *,
    nominal_control_strength: Any = 1.0,
    actual_control_strength: Any = 1.0,
    preserve_two_truths_gap: bool = True,
    preserve_protected_history: bool = True,
    context_allows_projection: bool = True,
) -> dict[str, Any]:
    dependency_visible = _v2_5_dependency_visible(v2_5_receipt)
    nominal = _strength(nominal_control_strength)
    actual = _strength(actual_control_strength)
    strength_class = classify_strength(nominal, actual)

    generation_once = apply_relation(
        "generation",
        phase_index=0,
        resolved_channels=1,
        active_channels=0,
    )
    generation_twice = apply_relation(
        "generation",
        phase_index=generation_once["phase_index"],
        resolved_channels=generation_once["resolved_channels"],
        active_channels=generation_once["active_channels"],
    )
    control_once = apply_relation(
        "control",
        phase_index=0,
        resolved_channels=1,
        active_channels=0,
    )
    insult_after_control = apply_relation(
        "insult",
        phase_index=control_once["phase_index"],
        resolved_channels=control_once["resolved_channels"],
        active_channels=control_once["active_channels"],
    )
    coherence = _coherence_sample()

    phase_endpoint_agrees = control_once["phase_index"] == generation_twice["phase_index"]
    history_endpoint_differs = (
        control_once["resolved_channels"], control_once["active_channels"]
    ) != (
        generation_twice["resolved_channels"], generation_twice["active_channels"]
    )
    control_insult_phase_returns = insult_after_control["phase_index"] == 0
    control_insult_history_preserved = (
        insult_after_control["resolved_channels"],
        insult_after_control["active_channels"],
    ) == (1, 1)

    boundaries_ok = bool(preserve_two_truths_gap and preserve_protected_history)
    projection_admissible = bool(
        dependency_visible and boundaries_ok and context_allows_projection
    )

    if not dependency_visible:
        disposition = "YIN_HOLDS_ON_V2_5_DEPENDENCY_GAP"
    elif not boundaries_ok:
        disposition = "YIN_HOLDS_ON_TWO_TRUTHS_OR_PROTECTED_HISTORY_GAP"
    elif not context_allows_projection:
        disposition = "YIN_CONTEXT_HOLDS_GENERATION_CONTROL_PROJECTION"
    elif not coherence["verified"]:
        disposition = "YIN_HOLDS_ON_COMPOSITION_COHERENCE_GAP"
    else:
        disposition = "WUXING_GENERATION_CONTROL_COHERENCE_VISIBLE"

    receipt: dict[str, Any] = {
        "version": VERSION,
        "receipt_version": RECEIPT_VERSION,
        "source_v2_5_digest": v2_5_receipt.get("wuxing_fibonacci_receipt_digest"),
        "dependency_surface": {
            "v2_5_dependency_visible": dependency_visible,
            "preserve_two_truths_gap": bool(preserve_two_truths_gap),
            "preserve_protected_history": bool(preserve_protected_history),
            "context_allows_projection": bool(context_allows_projection),
        },
        "relation_surface": {
            "carrier": "Z5",
            "relations": deepcopy(RELATIONS),
            "generation_formula": "p -> p + 1 mod 5",
            "control_formula": "p -> p + 2 mod 5",
            "insult_formula": "p -> p - 2 mod 5",
            "mother_formula": "p -> p - 1 mod 5",
            "child_formula": "p -> p + 1 mod 5",
            "overacting_is_not_a_distinct_direction": True,
            "insult_is_not_negative_strength": True,
        },
        "strength_surface": {
            "carrier": "nonnegative real",
            "nominal_control_strength": nominal,
            "actual_control_strength": actual,
            "classification": strength_class,
            "under_formula": "actual < nominal",
            "balanced_formula": "actual = nominal",
            "over_formula": "nominal < actual",
            "overacting_control": is_overacting_control(
                "control", nominal=nominal, actual=actual
            ),
            "strength_is_classification_not_validated_dynamics": True,
            "nominal_is_not_clinical_threshold": True,
        },
        "phase_history_separation_surface": {
            "control_once": control_once,
            "generation_twice": generation_twice,
            "phase_endpoint_agrees": phase_endpoint_agrees,
            "history_endpoint_differs": history_endpoint_differs,
            "control_is_one_history_event": True,
            "two_generations_are_two_history_events": True,
            "same_phase_endpoint_is_not_same_process": True,
        },
        "inverse_direction_surface": {
            "control_then_insult": insult_after_control,
            "phase_returns": control_insult_phase_returns,
            "history_advances_twice": control_insult_history_preserved,
            "phase_inverse_does_not_erase_history": True,
        },
        "coherence_surface": {
            "law": "A_(sigma+tau)(x) = A_tau(A_sigma(x))",
            "sample": coherence,
            "composition_verified": coherence["verified"],
            "center_is_coherence_not_earth_substance": True,
            "earth_remains_phase_index_two": True,
        },
        "operational_surface": {
            "projection_admissible": projection_admissible,
            "receipt_is_not_world_adoption": True,
            "formal_compilation_is_not_external_theorem_acceptance": True,
            "validation_is_not_truth": True,
            "selection_is_not_execution": True,
        },
        "disposition": disposition,
        "projection_admissible": projection_admissible,
        "non_authority": deepcopy(NON_AUTHORITY),
        "generation_control_coherence_receipt_digest": "",
    }
    receipt["generation_control_coherence_receipt_digest"] = _stable_digest(receipt)
    return receipt


def validate_wuxing_generation_control_coherence_receipt(
    v2_5_receipt: Mapping[str, Any],
    receipt: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []

    def require(condition: bool, code: str) -> None:
        if not condition:
            errors.append(code)

    dependency = receipt.get("dependency_surface", {})
    strength = receipt.get("strength_surface", {})

    try:
        expected = build_wuxing_generation_control_coherence_receipt(
            v2_5_receipt,
            nominal_control_strength=(
                strength.get("nominal_control_strength", 0.0)
                if isinstance(strength, Mapping)
                else 0.0
            ),
            actual_control_strength=(
                strength.get("actual_control_strength", 0.0)
                if isinstance(strength, Mapping)
                else 0.0
            ),
            preserve_two_truths_gap=(
                dependency.get("preserve_two_truths_gap") is True
                if isinstance(dependency, Mapping)
                else False
            ),
            preserve_protected_history=(
                dependency.get("preserve_protected_history") is True
                if isinstance(dependency, Mapping)
                else False
            ),
            context_allows_projection=(
                dependency.get("context_allows_projection") is True
                if isinstance(dependency, Mapping)
                else False
            ),
        )
        require(receipt.get("version") == VERSION, "version_invalid")
        require(receipt.get("receipt_version") == RECEIPT_VERSION, "receipt_version_invalid")
        require(
            receipt.get("generation_control_coherence_receipt_digest") == _stable_digest(receipt),
            "receipt_digest_invalid",
        )
        for key in (
            "source_v2_5_digest",
            "dependency_surface",
            "relation_surface",
            "strength_surface",
            "phase_history_separation_surface",
            "inverse_direction_surface",
            "coherence_surface",
            "operational_surface",
            "disposition",
            "projection_admissible",
            "non_authority",
        ):
            require(receipt.get(key) == expected.get(key), f"{key}_invalid")
        require(dict(receipt.get("non_authority", {})) == NON_AUTHORITY, "positive_authority_detected")
    except Exception as exc:  # pragma: no cover
        errors.append(f"validation_exception:{type(exc).__name__}")

    return errors
