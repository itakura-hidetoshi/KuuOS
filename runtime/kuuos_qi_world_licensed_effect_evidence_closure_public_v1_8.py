from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime import kuuos_qi_world_licensed_effect_evidence_closure_v1_8 as _core

_ORIGINAL_BUILD_BLOCKER = _core.build_post_effect_blocker_certificate
_ORIGINAL_VALIDATE_CLOSURE = _core.validate_licensed_effect_evidence_closure_receipt


def _learning_delta(learn: Mapping[str, Any]) -> dict[str, Any]:
    value = learn.get("learning_delta", {})
    return dict(value) if isinstance(value, Mapping) else {}


def build_post_effect_blocker_certificate(
    *,
    source: Mapping[str, Any],
    states: Mapping[str, Mapping[str, Any]],
    next_artifacts: Mapping[str, Mapping[str, Any]],
    world: Mapping[str, Any],
) -> dict[str, Any]:
    certificate = _ORIGINAL_BUILD_BLOCKER(
        source=source,
        states=states,
        next_artifacts=next_artifacts,
        world=world,
    )
    learn = dict(states["LearnOS"])
    delta = _learning_delta(learn)
    components = deepcopy(dict(certificate["component_vectors"]))

    evidence = dict(components["native_evidence_surface"])
    evidence["memory_overwrite_blocker"] = bool(
        delta.get("future_only") is True
        and delta.get("memory_overwrite") is False
        and delta.get("past_record_mutation") is False
        and learn.get("past_records_unchanged") is True
    )
    evidence["same_cycle_self_loop_blocker"] = bool(
        delta.get("active_now") is False
        and delta.get("activation_requires_replan") is True
        and learn.get("active_now") is False
        and learn.get("current_cycle_unchanged") is True
    )
    components["native_evidence_surface"] = evidence

    debt = dict(components["debt_closure_surface"])
    debt["present_activation_blocker"] = bool(
        states["ObserveOS"].get("observation_debt_discharged") is True
        and states["VerifyOS"].get("verification_debt_discharged") is True
        and learn.get("learning_debt_discharged") is True
        and learn.get("replan_required") is True
        and delta.get("activation_requires_replan") is True
    )
    components["debt_closure_surface"] = debt

    composed = _core.meet_blocker_vectors(list(components.values()))
    active = [name for name in _core.BLOCKER_ORDER if composed[name]]
    missing = [name for name in _core.BLOCKER_ORDER if not composed[name]]
    certificate["component_vectors"] = components
    certificate["composed_blocker_vector"] = composed
    certificate["active_blockers"] = active
    certificate["missing_blockers"] = missing
    certificate["all_required_blockers_active"] = not missing
    certificate["disposition"] = (
        "BLOCKED_PENDING_NEXT_EXTERNAL_AUTHORITY"
        if not missing
        else "QUARANTINE_EVIDENCE_CLOSURE_INCOMPLETE"
    )
    certificate["post_effect_blocker_certificate_digest"] = ""
    certificate["post_effect_blocker_certificate_digest"] = (
        _core.blocker_certificate_digest(certificate)
    )
    return certificate


def validate_licensed_effect_evidence_closure_receipt(
    receipt: Mapping[str, Any],
) -> list[str]:
    errors = [
        error
        for error in _ORIGINAL_VALIDATE_CLOSURE(receipt)
        if error
        not in {
            "closure_learning_not_future_only",
            "closure_learning_memory_overwrite",
        }
    ]

    def require(condition: bool, code: str) -> None:
        if not condition:
            errors.append(code)

    try:
        states = dict(receipt.get("native_evidence_states", {}))
        learn = dict(states.get("LearnOS", {}))
        delta = _learning_delta(learn)
        require(delta.get("future_only") is True, "closure_learning_delta_not_future_only")
        require(
            delta.get("memory_overwrite") is False,
            "closure_learning_delta_memory_overwrite",
        )
        require(delta.get("active_now") is False, "closure_learning_delta_active_now")
        require(
            delta.get("activation_requires_replan") is True,
            "closure_learning_delta_replan_boundary_missing",
        )
        require(
            delta.get("current_cycle_mutation") is False,
            "closure_learning_delta_current_cycle_mutation",
        )
        require(
            delta.get("past_record_mutation") is False,
            "closure_learning_delta_past_mutation",
        )
        require(learn.get("active_now") is False, "closure_learning_present_activation")
        require(
            learn.get("learning_debt_discharged") is True,
            "closure_learning_debt_open",
        )
        require(learn.get("replan_required") is True, "closure_replan_debt_missing")
        require(
            learn.get("current_cycle_unchanged") is True,
            "closure_learning_current_cycle_changed",
        )
        require(
            learn.get("past_records_unchanged") is True,
            "closure_learning_past_changed",
        )
    except (AttributeError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


_core.build_post_effect_blocker_certificate = build_post_effect_blocker_certificate
_core.validate_licensed_effect_evidence_closure_receipt = (
    validate_licensed_effect_evidence_closure_receipt
)

VERSION = _core.VERSION
RECEIPT_VERSION = _core.RECEIPT_VERSION
BLOCKER_VERSION = _core.BLOCKER_VERSION
CYCLE_ID = _core.CYCLE_ID
CLOSURE_NON_AUTHORITY = _core.CLOSURE_NON_AUTHORITY
BLOCKER_ORDER = _core.BLOCKER_ORDER
closure_receipt_digest = _core.closure_receipt_digest
blocker_certificate_digest = _core.blocker_certificate_digest
validate_post_effect_blocker_certificate = _core.validate_post_effect_blocker_certificate
build_licensed_effect_evidence_closure_receipt = (
    _core.build_licensed_effect_evidence_closure_receipt
)
