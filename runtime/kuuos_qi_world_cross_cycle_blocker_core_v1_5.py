from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping, Sequence

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_qi_world_cross_cycle_reentry_v1_4 import (
    build_cross_cycle_reentry_receipt,
    validate_cross_cycle_reentry_receipt,
)

VERSION = "kuuos_qi_world_cross_cycle_blocker_theory_v1_5"
CERTIFICATE_VERSION = "kuuos_qi_world_cross_cycle_blocker_certificate_v1_5"
CYCLE_ID = "qi-world-cross-cycle-blocker-v15"

BLOCKER_ORDER = (
    "present_activation_blocker",
    "execution_authority_blocker",
    "memory_overwrite_blocker",
    "world_identity_blocker",
    "truth_authority_blocker",
    "same_cycle_self_loop_blocker",
    "multi_world_collapse_blocker",
)

BLOCKED_CAPABILITY_BY_BLOCKER = {
    "present_activation_blocker": "present_cycle_act_start",
    "execution_authority_blocker": "unlicensed_execution_authority",
    "memory_overwrite_blocker": "previous_cycle_or_history_overwrite",
    "world_identity_blocker": "exact_world_identity_mutation",
    "truth_authority_blocker": "projection_to_truth_authority_escalation",
    "same_cycle_self_loop_blocker": "same_cycle_recursive_self_invocation",
    "multi_world_collapse_blocker": "candidate_world_collapse_to_single_fact",
}

BLOCKER_NON_AUTHORITY = {
    "blocker_grants_execution": False,
    "blocker_grants_truth": False,
    "blocker_issues_authority": False,
    "blocker_starts_act": False,
    "blocker_updates_exact_world": False,
    "blocker_overwrites_previous_cycle": False,
    "blocker_commits_plan": False,
}


def _canonical_digest(value: Mapping[str, Any], field: str) -> str:
    packet = deepcopy(dict(value))
    packet.pop(field, None)
    return sha(packet)


def blocker_certificate_digest(value: Mapping[str, Any]) -> str:
    return _canonical_digest(value, "blocker_certificate_digest")


def blocker_receipt_digest(value: Mapping[str, Any]) -> str:
    return _canonical_digest(value, "cross_cycle_blocker_receipt_digest")


def blocker_identity() -> dict[str, bool]:
    return {name: True for name in BLOCKER_ORDER}


def normalize_blocker_vector(value: Mapping[str, Any]) -> dict[str, bool]:
    return {name: value.get(name) is True for name in BLOCKER_ORDER}


def blocker_meet(
    left: Mapping[str, Any], right: Mapping[str, Any]
) -> dict[str, bool]:
    a = normalize_blocker_vector(left)
    b = normalize_blocker_vector(right)
    return {name: bool(a[name] and b[name]) for name in BLOCKER_ORDER}


def meet_blocker_vectors(
    vectors: Sequence[Mapping[str, Any]],
) -> dict[str, bool]:
    result = blocker_identity()
    for vector in vectors:
        result = blocker_meet(result, vector)
    return result


def blocker_weaker_or_equal(
    left: Mapping[str, Any], right: Mapping[str, Any]
) -> bool:
    """Pointwise Boolean order: False <= True.

    `left <= right` means every blocker active in `left` is also active in
    `right`. The meet is therefore a lower bound of both inputs.
    """

    a = normalize_blocker_vector(left)
    b = normalize_blocker_vector(right)
    return all((not a[name]) or b[name] for name in BLOCKER_ORDER)


def _component_vector(**updates: bool) -> dict[str, bool]:
    vector = blocker_identity()
    for key, value in updates.items():
        if key not in vector:
            raise KeyError(f"unknown_blocker:{key}")
        vector[key] = bool(value)
    return vector


def _derive_component_vectors(
    receipt: Mapping[str, Any],
) -> dict[str, dict[str, bool]]:
    previous = dict(receipt.get("previous_cycle_receipt", {}))
    previous_artifacts = dict(previous.get("native_artifacts", {}))
    learn = dict(previous_artifacts.get("LearnOS", {}))
    next_artifacts = dict(receipt.get("next_cycle_artifacts", {}))
    belief = dict(next_artifacts.get("BeliefOS", {}))
    plan = dict(next_artifacts.get("PlanOS", {}))
    qi = dict(receipt.get("cross_cycle_qi_receipt", {}))
    qi_state = dict(qi.get("enriched_state", {}))
    qi_history = qi_state.get("process_history", [])
    if not isinstance(qi_history, list):
        qi_history = []
    world = dict(receipt.get("cross_cycle_world_projection", {}))
    non_authority = dict(receipt.get("cross_cycle_non_authority", {}))

    expected_next_inventory = {
        "BeliefOS",
        "BeliefActivation",
        "DecisionOS",
        "DecisionOSPlural",
        "DecisionOSWa",
        "PlanOS",
    }

    receipt_vector = _component_vector(
        present_activation_blocker=receipt.get("next_act_not_started") is True,
        memory_overwrite_blocker=receipt.get("previous_cycle_immutable") is True,
        same_cycle_self_loop_blocker=(
            receipt.get("next_act_not_started") is True
            and "ActOS" not in next_artifacts
            and set(next_artifacts) == expected_next_inventory
        ),
    )

    plan_vector = _component_vector(
        present_activation_blocker=(
            plan.get("current_phase") == "commit"
            and receipt.get("next_act_not_started") is True
        ),
        execution_authority_blocker=(
            non_authority.get("bridge_grants_execution") is False
            and non_authority.get("bridge_starts_act") is False
            and non_authority.get("bridge_issues_authority") is False
        ),
        same_cycle_self_loop_blocker=(
            plan.get("current_phase") == "commit" and "ActOS" not in next_artifacts
        ),
    )

    qi_vector = _component_vector(
        execution_authority_blocker=(
            qi.get("grants_execution_authority") is False
            and qi.get("grants_final_commitment_authority") is False
        ),
        memory_overwrite_blocker=(
            qi.get("grants_memory_overwrite_authority") is False
            and qi_state.get("memory_overwrite_blocker") is True
            and receipt.get("previous_cycle_immutable") is True
        ),
        truth_authority_blocker=qi.get("grants_truth_authority") is False,
        same_cycle_self_loop_blocker=(
            qi.get("process_tensor_visible") is True
            and qi.get("memory_continuity_visible") is True
            and len(qi_history) >= 2
        ),
        multi_world_collapse_blocker=(
            qi_state.get("noncollapse_guard") is True
            and qi_state.get("two_truths_gap") is True
            and qi_state.get("candidate_only") is True
            and qi_state.get("nonfinal_marker") is True
        ),
    )

    world_vector = _component_vector(
        world_identity_blocker=(
            world.get("projection_read_only") is True
            and world.get("exact_world_identified") is False
            and world.get("runtime_updates_world") is False
            and non_authority.get("bridge_updates_exact_world") is False
        ),
        truth_authority_blocker=(
            world.get("candidate_only") is True
            and world.get("nonfinal_marker") is True
            and world.get("two_truths_gap") is True
            and non_authority.get("bridge_grants_truth") is False
        ),
        multi_world_collapse_blocker=(
            world.get("multi_world_noncollapse") is True
            and world.get("two_truths_gap") is True
            and world.get("exact_world_identified") is False
        ),
    )

    lineage_vector = _component_vector(
        memory_overwrite_blocker=(
            learn.get("past_records_unchanged") is True
            and belief.get("memory_overwrite") is False
            and non_authority.get("bridge_overwrites_previous_cycle") is False
        ),
        same_cycle_self_loop_blocker=(
            learn.get("active_now") is False
            and learn.get("future_only") is True
            and receipt.get("next_act_not_started") is True
        ),
    )

    authority_vector = _component_vector(
        execution_authority_blocker=(
            non_authority.get("bridge_grants_execution") is False
            and non_authority.get("bridge_issues_authority") is False
            and non_authority.get("bridge_starts_act") is False
        ),
        memory_overwrite_blocker=(
            non_authority.get("bridge_overwrites_previous_cycle") is False
        ),
        world_identity_blocker=(
            non_authority.get("bridge_updates_exact_world") is False
        ),
        truth_authority_blocker=(
            non_authority.get("bridge_grants_truth") is False
        ),
    )

    return {
        "receipt_surface": receipt_vector,
        "plan_surface": plan_vector,
        "qi_process_surface": qi_vector,
        "world_projection_surface": world_vector,
        "lineage_surface": lineage_vector,
        "authority_surface": authority_vector,
    }


def build_cross_cycle_blocker_certificate(
    receipt: Mapping[str, Any],
) -> dict[str, Any]:
    components = _derive_component_vectors(receipt)
    composed = meet_blocker_vectors(list(components.values()))
    active = [name for name in BLOCKER_ORDER if composed[name]]
    missing = [name for name in BLOCKER_ORDER if not composed[name]]
    all_active = not missing
    certificate = {
        "version": CERTIFICATE_VERSION,
        "cycle_id": CYCLE_ID,
        "source_cross_cycle_receipt_digest": receipt.get(
            "cross_cycle_receipt_digest"
        ),
        "blocker_order": list(BLOCKER_ORDER),
        "component_vectors": deepcopy(components),
        "composed_blocker_vector": composed,
        "active_blockers": active,
        "missing_blockers": missing,
        "all_required_blockers_active": all_active,
        "blocked_capabilities": [
            BLOCKED_CAPABILITY_BY_BLOCKER[name] for name in active
        ],
        "disposition": (
            "BLOCKED_UNLICENSED_CROSS_CYCLE_TRANSITION"
            if all_active
            else "QUARANTINE_BLOCKER_EVIDENCE_INCOMPLETE"
        ),
        "bounded_to_cross_cycle_transition": True,
        "contextual_not_root_sovereignty": True,
        "repairable_by_new_evidence": True,
        "fail_closed_on_boundary_loss": True,
        "candidate_weighting_not_truth": True,
        "barrier_potential_can_only_block_or_probe": True,
        "non_authority": deepcopy(BLOCKER_NON_AUTHORITY),
        "blocker_certificate_digest": "",
    }
    certificate["blocker_certificate_digest"] = blocker_certificate_digest(
        certificate
    )
    return certificate


def validate_cross_cycle_blocker_certificate(
    source_receipt: Mapping[str, Any], certificate: Mapping[str, Any]
) -> list[str]:
    errors: list[str] = []

    def require(condition: bool, code: str) -> None:
        if not condition:
            errors.append(code)

    try:
        require(
            certificate.get("version") == CERTIFICATE_VERSION,
            "blocker_certificate_version_invalid",
        )
        require(
            certificate.get("blocker_certificate_digest")
            == blocker_certificate_digest(certificate),
            "blocker_certificate_digest_invalid",
        )
        require(
            certificate.get("source_cross_cycle_receipt_digest")
            == source_receipt.get("cross_cycle_receipt_digest"),
            "blocker_source_receipt_digest_mismatch",
        )
        require(
            certificate.get("blocker_order") == list(BLOCKER_ORDER),
            "blocker_order_invalid",
        )
        expected = build_cross_cycle_blocker_certificate(source_receipt)
        require(
            dict(certificate.get("component_vectors", {}))
            == expected["component_vectors"],
            "blocker_component_vectors_invalid",
        )
        require(
            dict(certificate.get("composed_blocker_vector", {}))
            == expected["composed_blocker_vector"],
            "blocker_composed_vector_invalid",
        )
        require(
            list(certificate.get("active_blockers", []))
            == expected["active_blockers"],
            "blocker_active_inventory_invalid",
        )
        require(
            list(certificate.get("missing_blockers", []))
            == expected["missing_blockers"],
            "blocker_missing_inventory_invalid",
        )
        require(
            certificate.get("all_required_blockers_active")
            is expected["all_required_blockers_active"],
            "blocker_all_active_flag_invalid",
        )
        require(
            list(certificate.get("blocked_capabilities", []))
            == expected["blocked_capabilities"],
            "blocker_capability_inventory_invalid",
        )
        require(
            certificate.get("disposition") == expected["disposition"],
            "blocker_disposition_invalid",
        )
        for name in BLOCKER_ORDER:
            require(
                expected["composed_blocker_vector"][name] is True,
                f"blocker_{name}_inactive",
            )
        for key, expected_value in {
            "bounded_to_cross_cycle_transition": True,
            "contextual_not_root_sovereignty": True,
            "repairable_by_new_evidence": True,
            "fail_closed_on_boundary_loss": True,
            "candidate_weighting_not_truth": True,
            "barrier_potential_can_only_block_or_probe": True,
        }.items():
            require(
                certificate.get(key) is expected_value,
                f"blocker_{key}_invalid",
            )
        require(
            dict(certificate.get("non_authority", {}))
            == BLOCKER_NON_AUTHORITY,
            "blocker_non_authority_invalid",
        )
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_cross_cycle_blocker_receipt(root: Path) -> dict[str, Any]:
    source = build_cross_cycle_reentry_receipt(root / "cross-cycle-v14")
    source_errors = validate_cross_cycle_reentry_receipt(source)
    if source_errors:
        raise ValueError("source_cross_cycle_invalid:" + ";".join(source_errors))
    certificate = build_cross_cycle_blocker_certificate(source)
    receipt = {
        "version": VERSION,
        "cycle_id": CYCLE_ID,
        "source_cross_cycle_receipt": deepcopy(source),
        "source_cross_cycle_receipt_digest": source[
            "cross_cycle_receipt_digest"
        ],
        "blocker_certificate": certificate,
        "all_required_blockers_active": certificate[
            "all_required_blockers_active"
        ],
        "unlicensed_transition_blocked": certificate[
            "all_required_blockers_active"
        ],
        "next_act_started": False,
        "exact_world_updated": False,
        "previous_cycle_overwritten": False,
        "recursive_self_invocation_started": False,
        "non_authority": deepcopy(BLOCKER_NON_AUTHORITY),
        "cross_cycle_blocker_receipt_digest": "",
    }
    receipt["cross_cycle_blocker_receipt_digest"] = blocker_receipt_digest(
        receipt
    )
    errors = validate_cross_cycle_blocker_receipt(receipt)
    if errors:
        raise ValueError("cross_cycle_blocker_invalid:" + ";".join(errors))
    return receipt


def validate_cross_cycle_blocker_receipt(
    receipt: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []

    def require(condition: bool, code: str) -> None:
        if not condition:
            errors.append(code)

    try:
        require(receipt.get("version") == VERSION, "blocker_receipt_version_invalid")
        require(
            receipt.get("cross_cycle_blocker_receipt_digest")
            == blocker_receipt_digest(receipt),
            "blocker_receipt_digest_invalid",
        )
        source = dict(receipt.get("source_cross_cycle_receipt", {}))
        errors.extend(
            "blocker_source_" + error
            for error in validate_cross_cycle_reentry_receipt(source)
        )
        require(
            receipt.get("source_cross_cycle_receipt_digest")
            == source.get("cross_cycle_receipt_digest"),
            "blocker_source_digest_mismatch",
        )
        certificate = dict(receipt.get("blocker_certificate", {}))
        errors.extend(validate_cross_cycle_blocker_certificate(source, certificate))
        require(
            receipt.get("all_required_blockers_active") is True,
            "blocker_receipt_all_active_missing",
        )
        require(
            receipt.get("unlicensed_transition_blocked") is True,
            "blocker_unlicensed_transition_not_blocked",
        )
        for key, expected in {
            "next_act_started": False,
            "exact_world_updated": False,
            "previous_cycle_overwritten": False,
            "recursive_self_invocation_started": False,
        }.items():
            require(receipt.get(key) is expected, f"blocker_{key}_invalid")
        require(
            dict(receipt.get("non_authority", {})) == BLOCKER_NON_AUTHORITY,
            "blocker_receipt_non_authority_invalid",
        )
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors
