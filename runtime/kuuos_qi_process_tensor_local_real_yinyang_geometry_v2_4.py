from __future__ import annotations

from copy import deepcopy
from numbers import Real
from typing import Any, Mapping, Sequence

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_qi_process_tensor_local_real_yinyang_geometry_v2_4"
RECEIPT_VERSION = "kuuos_qi_process_tensor_local_real_yinyang_geometry_receipt_v2_4"
STATUS_OK = "KUUOS_QI_PROCESS_TENSOR_LOCAL_REAL_YINYANG_GEOMETRY_V2_4_OK"

NON_AUTHORITY = {
    "grants_execution_authority": False,
    "grants_truth_authority": False,
    "grants_final_commitment_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_clinical_authority": False,
    "grants_theorem_authority": False,
    "updates_exact_world": False,
    "constructs_tomita_operator": False,
    "executes_modular_operator": False,
}


def _receipt_digest(value: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(value))
    payload.pop("local_real_yinyang_receipt_digest", None)
    return sha(payload)


def _nonnegative_int(value: Any, *, default: int = 0) -> int:
    if isinstance(value, bool):
        return default
    if isinstance(value, int) and value >= 0:
        return value
    return default


def _positive_real(value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        return 0.0
    candidate = float(value)
    return candidate if candidate > 0.0 else 0.0


def _mapping_records(value: Sequence[Mapping[str, Any]] | Any) -> list[dict[str, Any]]:
    if isinstance(value, (str, bytes, bytearray)) or not isinstance(value, Sequence):
        return []
    return [dict(item) for item in value if isinstance(item, Mapping)]


def _normalize_frame_records(value: Sequence[Mapping[str, Any]] | Any) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for item in _mapping_records(value):
        records.append(
            {
                "context_id": str(item.get("context_id", "unknown-context")),
                "conjugation_involutive": item.get("conjugation_involutive") is True,
                "gauge_local": item.get("gauge_local") is True,
                "absolute_global_polarity_claim": item.get("absolute_global_polarity_claim") is True,
            }
        )
    return records


def _normalize_transport_records(value: Sequence[Mapping[str, Any]] | Any) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for item in _mapping_records(value):
        records.append(
            {
                "source_context": str(item.get("source_context", "unknown-source")),
                "target_context": str(item.get("target_context", "unknown-target")),
                "real_structure_compatible": item.get("real_structure_compatible") is True,
                "conversion_visible": item.get("conversion_visible") is True,
                "memory_link_visible": item.get("memory_link_visible") is True,
                "holonomy_residue_visible": item.get("holonomy_residue_visible") is True,
            }
        )
    return records


def compose_conversion_parity(first: str, second: str) -> str:
    """Compose preserve/convert parity without treating polarity as substance."""
    valid = {"preserve", "convert"}
    if first not in valid or second not in valid:
        return "undetermined"
    return "convert" if (first == "convert") ^ (second == "convert") else "preserve"


def build_local_real_yinyang_geometry_receipt(
    qi_receipt: Mapping[str, Any],
    frame_records: Sequence[Mapping[str, Any]],
    transport_records: Sequence[Mapping[str, Any]],
    *,
    qi_intensity: int,
    qi_capacity: int,
    recoverability_gap_candidate: float = 0.0,
    protected_history_visible: bool = True,
    two_truths_gap: bool = True,
    context_allows_candidate_flow: bool = True,
) -> dict[str, Any]:
    """Build a bounded evidence receipt for local-real Yin-Yang Process Tensor geometry.

    The receipt never constructs analytic Tomita/KMS objects, never identifies the
    WORLD with a Hilbert carrier, and never grants mutation or theorem authority.
    """

    frames = _normalize_frame_records(frame_records)
    transports = _normalize_transport_records(transport_records)
    intensity = _nonnegative_int(qi_intensity)
    capacity = _nonnegative_int(qi_capacity)
    recovery_gap = _positive_real(recoverability_gap_candidate)

    process_tensor_visible = qi_receipt.get("process_tensor_visible") is True
    transition_visible = qi_receipt.get("transition_continuity_visible") is True
    memory_visible = qi_receipt.get("memory_continuity_visible") is True
    process_support_visible = process_tensor_visible and transition_visible and memory_visible

    local_frames_visible = bool(frames)
    all_frames_involutive = local_frames_visible and all(
        item["conjugation_involutive"] for item in frames
    )
    all_frames_gauge_local = local_frames_visible and all(item["gauge_local"] for item in frames)
    absolute_global_polarity_claim = any(
        item["absolute_global_polarity_claim"] for item in frames
    )

    compatible_transport_count = sum(
        1 for item in transports if item["real_structure_compatible"]
    )
    conversion_count = sum(1 for item in transports if item["conversion_visible"])
    memory_link_count = sum(1 for item in transports if item["memory_link_visible"])
    holonomy_residue_count = sum(
        1 for item in transports if item["holonomy_residue_visible"]
    )
    conversion_parity = "odd" if conversion_count % 2 else "even"
    composed_polarity_action = "convert" if conversion_parity == "odd" else "preserve"

    explicit_nonmarkov = qi_receipt.get("nonmarkov_memory_visible") is True
    nonmarkov_memory_visible = explicit_nonmarkov or memory_link_count > 0
    holonomy_residue_visible = holonomy_residue_count > 0

    boundary_ok = bool(
        protected_history_visible
        and two_truths_gap
        and not absolute_global_polarity_claim
    )
    frame_ok = bool(
        local_frames_visible and all_frames_involutive and all_frames_gauge_local
    )
    candidate_flow_admissible = bool(
        process_support_visible
        and frame_ok
        and boundary_ok
        and context_allows_candidate_flow
    )

    admitted_intensity = min(intensity, capacity) if candidate_flow_admissible else 0
    held_residue = intensity - admitted_intensity
    saturation_detected = intensity > capacity
    return_channel_capacity = max(capacity - admitted_intensity, 0)
    recoverability_gap_visible = bool(
        recovery_gap > 0.0
        and protected_history_visible
        and nonmarkov_memory_visible
        and frame_ok
    )

    if absolute_global_polarity_claim:
        disposition = "FAIL_CLOSED_ON_GLOBAL_ABSOLUTE_POLARITY_CLAIM"
    elif not process_support_visible:
        disposition = "YIN_HOLDS_INCOMPLETE_PROCESS_TENSOR_EVIDENCE"
    elif not frame_ok:
        disposition = "YIN_HOLDS_INVALID_OR_MISSING_LOCAL_REAL_FRAME"
    elif not protected_history_visible:
        disposition = "YIN_HOLDS_ON_PROTECTED_HISTORY_LOSS"
    elif not two_truths_gap:
        disposition = "FAIL_CLOSED_ON_TWO_TRUTHS_GAP_LOSS"
    elif not context_allows_candidate_flow:
        disposition = "YIN_CONTEXT_HOLDS_CANDIDATE_FLOW"
    elif saturation_detected:
        disposition = "YANG_SATURATION_SPLITS_ADMITTED_AND_HELD_QI"
    elif conversion_parity == "odd":
        disposition = "ODD_LOCAL_REAL_CONVERSION_REQUIRES_POLARITY_AWARE_READOUT"
    else:
        disposition = "LOCAL_REAL_YINYANG_PROCESS_TENSOR_GEOMETRY_VISIBLE"

    receipt: dict[str, Any] = {
        "version": VERSION,
        "receipt_version": RECEIPT_VERSION,
        "source_cycle_id": qi_receipt.get("cycle_id"),
        "source_process_tensor_digest": qi_receipt.get("qi_process_tensor_receipt_digest")
        or qi_receipt.get("cross_cycle_qi_receipt_digest"),
        "process_tensor_surface": {
            "process_tensor_visible": process_tensor_visible,
            "transition_continuity_visible": transition_visible,
            "memory_continuity_visible": memory_visible,
            "nonmarkov_memory_visible": nonmarkov_memory_visible,
            "process_support_visible": process_support_visible,
        },
        "local_real_structure_surface": {
            "frame_count": len(frames),
            "frames": frames,
            "local_frames_visible": local_frames_visible,
            "all_frames_involutive": all_frames_involutive,
            "all_frames_gauge_local": all_frames_gauge_local,
            "absolute_global_polarity_claim": absolute_global_polarity_claim,
            "polarity_is_local_relational_not_intrinsic": True,
        },
        "history_transport_surface": {
            "transport_count": len(transports),
            "transports": transports,
            "compatible_transport_count": compatible_transport_count,
            "conversion_count": conversion_count,
            "conversion_parity": conversion_parity,
            "composed_polarity_action": composed_polarity_action,
            "memory_link_count": memory_link_count,
            "holonomy_residue_count": holonomy_residue_count,
            "holonomy_residue_visible": holonomy_residue_visible,
            "double_conversion_can_restore_readout_polarity": True,
            "history_residue_is_not_erased_by_even_parity": True,
        },
        "qi_split_surface": {
            "qi_intensity": intensity,
            "qi_capacity": capacity,
            "admitted_qi_intensity": admitted_intensity,
            "held_qi_residue": held_residue,
            "return_channel_capacity": return_channel_capacity,
            "saturation_detected": saturation_detected,
            "held_residue_preserved_without_erasure": True,
            "admitted_plus_held_equals_total": admitted_intensity + held_residue == intensity,
        },
        "recoverability_surface": {
            "recoverability_gap_candidate": recovery_gap,
            "recoverability_gap_candidate_visible": recoverability_gap_visible,
            "protected_history_visible": bool(protected_history_visible),
            "two_truths_gap": bool(two_truths_gap),
            "recoverability_gap_is_not_physical_mass_theorem": True,
            "protected_history_not_targeted_for_decay": True,
        },
        "coupling": {
            "context_allows_candidate_flow": bool(context_allows_candidate_flow),
            "candidate_flow_admissible": candidate_flow_admissible,
            "observation_holding_split_distinct_from_yinyang_frame": True,
            "modular_conjugation_not_identified_with_fixed_yin": True,
            "modular_flow_not_identified_with_qi_substance": True,
            "process_conversion_component_not_claimed_as_standalone_process_tensor": True,
        },
        "disposition": disposition,
        "candidate_flow_admissible": candidate_flow_admissible,
        "admitted_qi_intensity": admitted_intensity,
        "held_qi_residue": held_residue,
        "non_authority": deepcopy(NON_AUTHORITY),
        "local_real_yinyang_receipt_digest": "",
    }
    receipt["local_real_yinyang_receipt_digest"] = _receipt_digest(receipt)
    return receipt


def validate_local_real_yinyang_geometry_receipt(
    qi_receipt: Mapping[str, Any],
    receipt: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []

    def require(condition: bool, code: str) -> None:
        if not condition:
            errors.append(code)

    frames_surface = receipt.get("local_real_structure_surface", {})
    history_surface = receipt.get("history_transport_surface", {})
    split_surface = receipt.get("qi_split_surface", {})
    recovery_surface = receipt.get("recoverability_surface", {})
    coupling = receipt.get("coupling", {})

    try:
        frames = frames_surface.get("frames", []) if isinstance(frames_surface, Mapping) else []
        transports = history_surface.get("transports", []) if isinstance(history_surface, Mapping) else []
        expected = build_local_real_yinyang_geometry_receipt(
            qi_receipt,
            frames,
            transports,
            qi_intensity=_nonnegative_int(
                split_surface.get("qi_intensity") if isinstance(split_surface, Mapping) else None
            ),
            qi_capacity=_nonnegative_int(
                split_surface.get("qi_capacity") if isinstance(split_surface, Mapping) else None
            ),
            recoverability_gap_candidate=(
                recovery_surface.get("recoverability_gap_candidate", 0.0)
                if isinstance(recovery_surface, Mapping)
                else 0.0
            ),
            protected_history_visible=(
                recovery_surface.get("protected_history_visible") is True
                if isinstance(recovery_surface, Mapping)
                else False
            ),
            two_truths_gap=(
                recovery_surface.get("two_truths_gap") is True
                if isinstance(recovery_surface, Mapping)
                else False
            ),
            context_allows_candidate_flow=(
                coupling.get("context_allows_candidate_flow") is True
                if isinstance(coupling, Mapping)
                else False
            ),
        )
        require(receipt.get("version") == VERSION, "version_invalid")
        require(receipt.get("receipt_version") == RECEIPT_VERSION, "receipt_version_invalid")
        require(
            receipt.get("local_real_yinyang_receipt_digest") == _receipt_digest(receipt),
            "receipt_digest_invalid",
        )
        for key in (
            "source_cycle_id",
            "source_process_tensor_digest",
            "process_tensor_surface",
            "local_real_structure_surface",
            "history_transport_surface",
            "qi_split_surface",
            "recoverability_surface",
            "coupling",
            "disposition",
            "candidate_flow_admissible",
            "admitted_qi_intensity",
            "held_qi_residue",
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
