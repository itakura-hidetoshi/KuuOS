from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import math
from typing import Any, Mapping

VERSION = "kuuos_qi_yinyang_wuxing_fibonacci_history_geometry_v2_5"
RECEIPT_VERSION = (
    "kuuos_qi_yinyang_wuxing_fibonacci_history_geometry_receipt_v2_5"
)
STATUS_OK = "KUUOS_QI_YINYANG_WUXING_FIBONACCI_HISTORY_GEOMETRY_V2_5_OK"

FIVE_PHASES = (
    {"index": 0, "key": "wood", "label_ja": "木"},
    {"index": 1, "key": "fire", "label_ja": "火"},
    {"index": 2, "key": "earth", "label_ja": "土"},
    {"index": 3, "key": "metal", "label_ja": "金"},
    {"index": 4, "key": "water", "label_ja": "水"},
)

NON_AUTHORITY = {
    "grants_execution_authority": False,
    "grants_truth_authority": False,
    "grants_final_commitment_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_clinical_authority": False,
    "grants_theorem_authority": False,
    "updates_exact_world": False,
    "claims_physical_anyon_realization": False,
    "claims_historical_identity_with_classical_wuxing": False,
    "uses_golden_ratio_as_clinical_threshold": False,
}


def _stable_digest(value: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(value))
    payload.pop("wuxing_fibonacci_receipt_digest", None)
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _nonnegative_int(value: Any, *, default: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        return default
    return value


def _phase_index(value: Any) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        return 0
    return value % 5


def golden_ratio() -> float:
    return (1.0 + math.sqrt(5.0)) / 2.0


def history_dimension(resolved: int, active: int) -> float:
    return float(resolved) + float(active) * golden_ratio()


def advance_history(resolved: int, active: int) -> tuple[int, int]:
    """Multiply the formal coefficient pair resolved + active*tau by tau."""
    return active, resolved + active


def advance_phase_history(
    *,
    initial_phase_index: int,
    resolved_channels: int,
    active_channels: int,
    steps: int,
) -> dict[str, Any]:
    phase = _phase_index(initial_phase_index)
    resolved = _nonnegative_int(resolved_channels)
    active = _nonnegative_int(active_channels)
    bounded_steps = _nonnegative_int(steps)
    trajectory: list[dict[str, Any]] = []

    for ordinal in range(bounded_steps + 1):
        phase_record = FIVE_PHASES[phase]
        trajectory.append(
            {
                "step": ordinal,
                "phase_index": phase,
                "phase_key": phase_record["key"],
                "phase_label_ja": phase_record["label_ja"],
                "resolved_channels": resolved,
                "active_channels": active,
                "history_dimension": history_dimension(resolved, active),
            }
        )
        if ordinal < bounded_steps:
            phase = (phase + 1) % 5
            resolved, active = advance_history(resolved, active)

    return {
        "initial_phase_index": _phase_index(initial_phase_index),
        "final_phase_index": phase,
        "steps": bounded_steps,
        "initial_resolved_channels": _nonnegative_int(resolved_channels),
        "initial_active_channels": _nonnegative_int(active_channels),
        "final_resolved_channels": resolved,
        "final_active_channels": active,
        "trajectory": trajectory,
    }


def _v2_4_dependency_visible(receipt: Mapping[str, Any]) -> bool:
    process = receipt.get("process_tensor_surface", {})
    local_real = receipt.get("local_real_structure_surface", {})
    recovery = receipt.get("recoverability_surface", {})
    non_authority = receipt.get("non_authority", {})
    return bool(
        receipt.get("version")
        == "kuuos_qi_process_tensor_local_real_yinyang_geometry_v2_4"
        and isinstance(process, Mapping)
        and process.get("process_support_visible") is True
        and isinstance(local_real, Mapping)
        and local_real.get("all_frames_involutive") is True
        and local_real.get("all_frames_gauge_local") is True
        and local_real.get("absolute_global_polarity_claim") is False
        and isinstance(recovery, Mapping)
        and recovery.get("protected_history_visible") is True
        and recovery.get("two_truths_gap") is True
        and isinstance(non_authority, Mapping)
        and non_authority
        and all(value is False for value in non_authority.values())
    )


def build_yinyang_wuxing_fibonacci_history_receipt(
    local_real_yinyang_receipt: Mapping[str, Any],
    *,
    initial_phase_index: int = 0,
    steps: int = 5,
    resolved_channels: int = 1,
    active_channels: int = 0,
    context_allows_projection: bool = True,
    preserve_two_truths_gap: bool = True,
    preserve_protected_history: bool = True,
) -> dict[str, Any]:
    """Build a deterministic non-authoritative Wuxing/Fibonacci history receipt.

    The five phases are a Z5 base coordinate. Fibonacci fusion is a separate
    history fibre. The receipt does not identify classical Wuxing with SU(2)_3,
    assert a physical anyon realization, or turn the golden ratio into a
    clinical threshold.
    """

    projection = advance_phase_history(
        initial_phase_index=initial_phase_index,
        resolved_channels=resolved_channels,
        active_channels=active_channels,
        steps=steps,
    )
    phi = golden_ratio()
    initial_dimension = history_dimension(
        projection["initial_resolved_channels"],
        projection["initial_active_channels"],
    )
    final_dimension = history_dimension(
        projection["final_resolved_channels"],
        projection["final_active_channels"],
    )
    expected_dimension = initial_dimension * (phi ** projection["steps"])
    dimension_error = abs(final_dimension - expected_dimension)

    dependency_visible = _v2_4_dependency_visible(local_real_yinyang_receipt)
    boundaries_ok = bool(preserve_two_truths_gap and preserve_protected_history)
    projection_admissible = bool(
        dependency_visible
        and boundaries_ok
        and context_allows_projection
    )
    phase_returned = (
        projection["final_phase_index"] == projection["initial_phase_index"]
    )
    history_returned = bool(
        projection["final_resolved_channels"]
        == projection["initial_resolved_channels"]
        and projection["final_active_channels"]
        == projection["initial_active_channels"]
    )
    canonical_unit_seed = bool(
        projection["initial_resolved_channels"] == 1
        and projection["initial_active_channels"] == 0
    )
    five_step_fusion_identity = bool(
        projection["steps"] == 5
        and canonical_unit_seed
        and projection["final_resolved_channels"] == 3
        and projection["final_active_channels"] == 5
    )

    if not dependency_visible:
        disposition = "YIN_HOLDS_ON_V2_4_LOCAL_REAL_DEPENDENCY_GAP"
    elif not boundaries_ok:
        disposition = "YIN_HOLDS_ON_TWO_TRUTHS_OR_PROTECTED_HISTORY_GAP"
    elif not context_allows_projection:
        disposition = "YIN_CONTEXT_HOLDS_WUXING_FIBONACCI_PROJECTION"
    elif phase_returned and not history_returned and five_step_fusion_identity:
        disposition = "FIVE_PHASE_BASE_RETURNS_WITH_FIBONACCI_HISTORY_ADVANCE"
    else:
        disposition = "WUXING_FIBONACCI_HISTORY_GEOMETRY_VISIBLE"

    receipt: dict[str, Any] = {
        "version": VERSION,
        "receipt_version": RECEIPT_VERSION,
        "source_local_real_yinyang_digest": local_real_yinyang_receipt.get(
            "local_real_yinyang_receipt_digest"
        ),
        "dependency_surface": {
            "v2_4_local_real_yinyang_dependency_visible": dependency_visible,
            "preserve_two_truths_gap": bool(preserve_two_truths_gap),
            "preserve_protected_history": bool(preserve_protected_history),
            "context_allows_projection": bool(context_allows_projection),
        },
        "five_phase_base_surface": {
            "carrier": "Z5",
            "canonical_phase_order": [dict(item) for item in FIVE_PHASES],
            "phase_transition": "j -> j + 1 mod 5",
            "phase_is_relational_coordinate_not_substance": True,
            "phase_returned": phase_returned,
            "phase_return_period": 5,
        },
        "yin_yang_orientation_surface": {
            "orientation_pair": ["q", "q_inverse"],
            "q_formula": "exp(i*pi/5)",
            "involution": "q <-> q_inverse",
            "trace_invariant_formula": "q + q_inverse = phi",
            "orientation_is_relation_not_fixed_essence": True,
            "trace_invariant_is_not_polarity_substance": True,
        },
        "fibonacci_history_fibre_surface": {
            "fusion_rule": "tau * tau = 1 + tau",
            "coefficient_step": "(resolved, active) -> (active, resolved + active)",
            "projection": projection,
            "canonical_five_step_identity": "tau^5 = 3 + 5*tau",
            "five_step_fusion_identity_visible": five_step_fusion_identity,
            "history_returned": history_returned,
            "history_is_path_multiplicity_not_qi_quantity": True,
        },
        "golden_ratio_growth_surface": {
            "golden_ratio": phi,
            "minimal_polynomial": "phi^2 - phi - 1 = 0",
            "initial_history_dimension": initial_dimension,
            "final_history_dimension": final_dimension,
            "expected_history_dimension": expected_dimension,
            "dimension_scaling_error": dimension_error,
            "dimension_scaling_verified": dimension_error < 1e-12,
            "entropy_rate_per_step": math.log(phi),
            "entropy_rate_for_projection": projection["steps"] * math.log(phi),
            "entropy_is_history_growth_not_thermodynamic_or_clinical_fact": True,
        },
        "categorical_surface": {
            "candidate_model": "Vec_Z5^alpha x Fib",
            "combined_generator": "X = s tensor tau",
            "five_step_closure": "X^5 = 1 tensor (3 + 5*tau)",
            "su2_3_even_subcategory_relation": "Fib is structurally modelled by the even sector of SU(2)_3",
            "classical_wuxing_not_identified_with_su2_3": True,
            "physical_anyon_realization_not_claimed": True,
            "pentagon_coherence_not_identified_with_five_phase_cycle": True,
        },
        "operational_surface": {
            "projection_admissible": projection_admissible,
            "same_phase_may_carry_distinct_history": True,
            "phase_only_projection_can_be_nonmarkovian": True,
            "history_lineage_must_not_be_erased_on_phase_return": True,
            "golden_ratio_is_not_a_clinical_threshold": True,
            "receipt_is_not_world_adoption": True,
        },
        "disposition": disposition,
        "projection_admissible": projection_admissible,
        "non_authority": deepcopy(NON_AUTHORITY),
        "wuxing_fibonacci_receipt_digest": "",
    }
    receipt["wuxing_fibonacci_receipt_digest"] = _stable_digest(receipt)
    return receipt


def validate_yinyang_wuxing_fibonacci_history_receipt(
    local_real_yinyang_receipt: Mapping[str, Any],
    receipt: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []

    def require(condition: bool, code: str) -> None:
        if not condition:
            errors.append(code)

    dependency = receipt.get("dependency_surface", {})
    fibre = receipt.get("fibonacci_history_fibre_surface", {})
    projection = fibre.get("projection", {}) if isinstance(fibre, Mapping) else {}

    try:
        expected = build_yinyang_wuxing_fibonacci_history_receipt(
            local_real_yinyang_receipt,
            initial_phase_index=_phase_index(
                projection.get("initial_phase_index")
                if isinstance(projection, Mapping)
                else 0
            ),
            steps=_nonnegative_int(
                projection.get("steps") if isinstance(projection, Mapping) else 0
            ),
            resolved_channels=_nonnegative_int(
                projection.get("initial_resolved_channels")
                if isinstance(projection, Mapping)
                else 0
            ),
            active_channels=_nonnegative_int(
                projection.get("initial_active_channels")
                if isinstance(projection, Mapping)
                else 0
            ),
            context_allows_projection=(
                dependency.get("context_allows_projection") is True
                if isinstance(dependency, Mapping)
                else False
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
        )
        require(receipt.get("version") == VERSION, "version_invalid")
        require(
            receipt.get("receipt_version") == RECEIPT_VERSION,
            "receipt_version_invalid",
        )
        require(
            receipt.get("wuxing_fibonacci_receipt_digest")
            == _stable_digest(receipt),
            "receipt_digest_invalid",
        )
        for key in (
            "source_local_real_yinyang_digest",
            "dependency_surface",
            "five_phase_base_surface",
            "yin_yang_orientation_surface",
            "fibonacci_history_fibre_surface",
            "golden_ratio_growth_surface",
            "categorical_surface",
            "operational_surface",
            "disposition",
            "projection_admissible",
            "non_authority",
        ):
            require(receipt.get(key) == expected.get(key), f"{key}_invalid")
        require(
            dict(receipt.get("non_authority", {})) == NON_AUTHORITY,
            "positive_authority_detected",
        )
    except Exception as exc:  # pragma: no cover
        errors.append(f"validation_exception:{type(exc).__name__}")
    return errors
