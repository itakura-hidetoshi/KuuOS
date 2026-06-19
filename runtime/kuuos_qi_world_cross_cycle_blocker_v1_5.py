from __future__ import annotations

from typing import Any, Mapping

from runtime import kuuos_qi_world_cross_cycle_blocker_core_v1_5 as _core

_ORIGINAL_DERIVE_COMPONENT_VECTORS = _core._derive_component_vectors


def _derive_component_vectors(
    receipt: Mapping[str, Any],
) -> dict[str, dict[str, bool]]:
    components = _ORIGINAL_DERIVE_COMPONENT_VECTORS(receipt)
    next_artifacts = dict(receipt.get("next_cycle_artifacts", {}))
    activation = dict(next_artifacts.get("BeliefActivation", {}))
    previous = dict(receipt.get("previous_cycle_receipt", {}))
    learn = dict(
        dict(previous.get("native_artifacts", {})).get("LearnOS", {})
    )
    non_authority = dict(receipt.get("cross_cycle_non_authority", {}))
    components["lineage_surface"]["memory_overwrite_blocker"] = bool(
        learn.get("past_records_unchanged") is True
        and activation.get("memory_overwrite") is False
        and non_authority.get("bridge_overwrites_previous_cycle") is False
    )
    components["lineage_surface"]["same_cycle_self_loop_blocker"] = bool(
        learn.get("active_now") is False
        and learn.get("current_cycle_unchanged") is True
        and receipt.get("next_act_not_started") is True
    )
    return components


_core._derive_component_vectors = _derive_component_vectors

VERSION = _core.VERSION
CERTIFICATE_VERSION = _core.CERTIFICATE_VERSION
CYCLE_ID = _core.CYCLE_ID
BLOCKER_ORDER = _core.BLOCKER_ORDER
BLOCKED_CAPABILITY_BY_BLOCKER = _core.BLOCKED_CAPABILITY_BY_BLOCKER
BLOCKER_NON_AUTHORITY = _core.BLOCKER_NON_AUTHORITY
blocker_certificate_digest = _core.blocker_certificate_digest
blocker_receipt_digest = _core.blocker_receipt_digest
blocker_identity = _core.blocker_identity
normalize_blocker_vector = _core.normalize_blocker_vector
blocker_meet = _core.blocker_meet
meet_blocker_vectors = _core.meet_blocker_vectors
blocker_weaker_or_equal = _core.blocker_weaker_or_equal
build_cross_cycle_blocker_certificate = (
    _core.build_cross_cycle_blocker_certificate
)
validate_cross_cycle_blocker_certificate = (
    _core.validate_cross_cycle_blocker_certificate
)
build_cross_cycle_blocker_receipt = _core.build_cross_cycle_blocker_receipt
validate_cross_cycle_blocker_receipt = (
    _core.validate_cross_cycle_blocker_receipt
)
