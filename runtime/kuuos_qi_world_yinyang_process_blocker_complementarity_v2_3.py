from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_qi_world_cross_cycle_blocker_core_v1_5 import (
    BLOCKER_ORDER,
    blocker_meet,
    normalize_blocker_vector,
)

VERSION = "kuuos_qi_world_yinyang_process_blocker_complementarity_v2_3"
RECEIPT_VERSION = "kuuos_qi_world_yinyang_process_blocker_receipt_v2_3"
STATUS_OK = "KUUOS_QI_WORLD_YINYANG_PROCESS_BLOCKER_COMPLEMENTARITY_V2_3_OK"

NON_AUTHORITY = {
    "grants_execution_authority": False,
    "grants_truth_authority": False,
    "grants_final_commitment_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_clinical_authority": False,
    "grants_theorem_authority": False,
    "updates_exact_world": False,
}


def _receipt_digest(value: Mapping[str, Any]) -> str:
    payload = deepcopy(dict(value))
    payload.pop("yin_yang_receipt_digest", None)
    return sha(payload)


def _nonnegative_int(value: Any, *, default: int = 0) -> int:
    if isinstance(value, bool):
        return default
    if isinstance(value, int) and value >= 0:
        return value
    return default


def relational_polarity(relation: str) -> str:
    """Return polarity for a relation, never an intrinsic object label."""
    normalized = relation.strip().lower()
    if normalized in {"contain", "constrain", "preserve_boundary", "hold"}:
        return "yin"
    if normalized in {"generate", "propagate", "accumulate", "express"}:
        return "yang"
    return "undetermined"


def build_yinyang_process_blocker_receipt(
    qi_receipt: Mapping[str, Any],
    blocker_certificate: Mapping[str, Any],
    *,
    qi_intensity: int,
    qi_capacity: int,
    context_allows_candidate_flow: bool = True,
) -> dict[str, Any]:
    """Couple Qi process support with blocker boundaries without granting authority.

    The boson/fermion language is retained only as a structural analogy. This
    function makes no particle-identity claim and proves no theorem of physics.
    """

    intensity = _nonnegative_int(qi_intensity)
    capacity = _nonnegative_int(qi_capacity)
    process_visible = qi_receipt.get("process_tensor_visible") is True
    transition_visible = qi_receipt.get("transition_continuity_visible") is True
    memory_visible = qi_receipt.get("memory_continuity_visible") is True
    yang_process_visible = process_visible and transition_visible and memory_visible

    raw_vector = blocker_certificate.get("composed_blocker_vector", {})
    vector = normalize_blocker_vector(raw_vector if isinstance(raw_vector, Mapping) else {})
    all_blockers_active = all(vector.values())
    certificate_all_active = blocker_certificate.get("all_required_blockers_active") is True
    yin_boundary_visible = all_blockers_active and certificate_all_active
    yin_occupancy_idempotent = blocker_meet(vector, vector) == vector

    within_capacity = intensity <= capacity
    saturation = intensity > capacity
    candidate_flow_admissible = bool(
        yang_process_visible
        and yin_boundary_visible
        and within_capacity
        and context_allows_candidate_flow
    )
    effective_intensity = intensity if candidate_flow_admissible else 0

    if not yang_process_visible:
        disposition = "YIN_HOLDS_INCOMPLETE_QI_PROCESS_EVIDENCE"
    elif not yin_boundary_visible:
        disposition = "YIN_FAIL_CLOSED_ON_BOUNDARY_LOSS"
    elif saturation:
        disposition = "YANG_SATURATION_GENERATES_YIN_CONTAINMENT"
    elif not context_allows_candidate_flow:
        disposition = "YIN_CONTEXT_HOLDS_YANG"
    else:
        disposition = "YIN_CONTAINS_AND_SHAPES_YANG_CANDIDATE_FLOW"

    receipt: dict[str, Any] = {
        "version": VERSION,
        "receipt_version": RECEIPT_VERSION,
        "source_qi_cycle_id": qi_receipt.get("cycle_id"),
        "source_blocker_cycle_id": blocker_certificate.get("cycle_id"),
        "source_qi_digest": qi_receipt.get("qi_process_tensor_receipt_digest")
        or qi_receipt.get("cross_cycle_qi_receipt_digest"),
        "source_blocker_digest": blocker_certificate.get("blocker_certificate_digest"),
        "yin_surface": {
            "boundary_visible": yin_boundary_visible,
            "blocker_vector": vector,
            "all_required_blockers_active": all_blockers_active,
            "occupancy_boolean": True,
            "occupancy_idempotent": yin_occupancy_idempotent,
            "contains_without_erasing": True,
            "preserves_identity_and_history": True,
        },
        "yang_surface": {
            "process_visible": yang_process_visible,
            "qi_intensity": intensity,
            "qi_capacity": capacity,
            "within_capacity": within_capacity,
            "accumulation_uses_natural_occupancy": True,
            "effective_intensity": effective_intensity,
            "candidate_flow_admissible": candidate_flow_admissible,
        },
        "coupling": {
            "context_allows_candidate_flow": bool(context_allows_candidate_flow),
            "saturation_detected": saturation,
            "saturation_generates_yin_containment": saturation,
            "boundary_loss_generates_fail_closed_yin": not yin_boundary_visible,
            "yin_without_yang_is_stasis_risk": True,
            "yang_without_yin_is_overflow_risk": True,
            "mutual_regulation_required": True,
            "polarity_is_relational_not_intrinsic": True,
            "same_surface_can_change_polarity_by_relation": (
                relational_polarity("contain") == "yin"
                and relational_polarity("propagate") == "yang"
            ),
        },
        "physics_boundary": {
            "boson_fermion_language_is_structural_analogy": True,
            "claims_physical_particle_identity": False,
            "claims_physics_theorem": False,
            "qi_is_not_reified_as_quantum_particle": True,
            "blocker_is_not_reified_as_fermion": True,
        },
        "disposition": disposition,
        "candidate_flow_admissible": candidate_flow_admissible,
        "effective_qi_intensity": effective_intensity,
        "non_authority": deepcopy(NON_AUTHORITY),
        "yin_yang_receipt_digest": "",
    }
    receipt["yin_yang_receipt_digest"] = _receipt_digest(receipt)
    return receipt


def validate_yinyang_process_blocker_receipt(
    qi_receipt: Mapping[str, Any],
    blocker_certificate: Mapping[str, Any],
    receipt: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []

    def require(condition: bool, code: str) -> None:
        if not condition:
            errors.append(code)

    yang = receipt.get("yang_surface", {})
    coupling = receipt.get("coupling", {})
    try:
        expected = build_yinyang_process_blocker_receipt(
            qi_receipt,
            blocker_certificate,
            qi_intensity=_nonnegative_int(
                yang.get("qi_intensity") if isinstance(yang, Mapping) else None
            ),
            qi_capacity=_nonnegative_int(
                yang.get("qi_capacity") if isinstance(yang, Mapping) else None
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
            receipt.get("yin_yang_receipt_digest") == _receipt_digest(receipt),
            "receipt_digest_invalid",
        )
        for key in (
            "source_qi_cycle_id",
            "source_blocker_cycle_id",
            "source_qi_digest",
            "source_blocker_digest",
            "yin_surface",
            "yang_surface",
            "coupling",
            "physics_boundary",
            "disposition",
            "candidate_flow_admissible",
            "effective_qi_intensity",
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
