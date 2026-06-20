from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime import kuuos_qi_world_successor_licensed_cycle_materialization_v2_0 as _core

_ORIGINAL_BUILD_BLOCKER = _core.build_post_effect_blocker_certificate
_ORIGINAL_VALIDATE_BLOCKER = _core.validate_post_effect_blocker_certificate


def _v18_compatible_source(source: Mapping[str, Any]) -> dict[str, Any]:
    adapted = deepcopy(dict(source))
    adapted["licensed_act_handoff_receipt_digest"] = source[
        "successor_licensed_act_handoff_receipt_digest"
    ]
    return adapted


def _build_post_effect_blocker_certificate(**kwargs: Any) -> dict[str, Any]:
    adapted = dict(kwargs)
    adapted["source"] = _v18_compatible_source(kwargs["source"])
    return _ORIGINAL_BUILD_BLOCKER(**adapted)


def _validate_post_effect_blocker_certificate(**kwargs: Any) -> list[str]:
    adapted = dict(kwargs)
    adapted["source"] = _v18_compatible_source(kwargs["source"])
    return _ORIGINAL_VALIDATE_BLOCKER(**adapted)


_core.build_post_effect_blocker_certificate = _build_post_effect_blocker_certificate
_core.validate_post_effect_blocker_certificate = _validate_post_effect_blocker_certificate

CHAIN_NON_AUTHORITY = _core.CHAIN_NON_AUTHORITY
CHAIN_VERSION = _core.CHAIN_VERSION
CLOSURE_NON_AUTHORITY = _core.CLOSURE_NON_AUTHORITY
CLOSURE_VERSION = _core.CLOSURE_VERSION
CYCLE_NON_AUTHORITY = _core.CYCLE_NON_AUTHORITY
CYCLE_ID = _core.CYCLE_ID
CYCLE_RECEIPT_VERSION = _core.CYCLE_RECEIPT_VERSION
HANDOFF_VERSION = _core.HANDOFF_VERSION
MATERIALIZATION_NON_AUTHORITY = _core.MATERIALIZATION_NON_AUTHORITY
VERSION = _core.VERSION
build_digest_linked_multi_cycle_chain = _core.build_digest_linked_multi_cycle_chain
build_second_closed_cycle_receipt = _core.build_second_closed_cycle_receipt
build_successor_evidence_closure_receipt = _core.build_successor_evidence_closure_receipt
build_successor_licensed_act_handoff_receipt = _core.build_successor_licensed_act_handoff_receipt
multi_cycle_chain_digest = _core.multi_cycle_chain_digest
second_cycle_receipt_digest = _core.second_cycle_receipt_digest
successor_closure_digest = _core.successor_closure_digest
successor_handoff_digest = _core.successor_handoff_digest
validate_digest_linked_multi_cycle_chain = _core.validate_digest_linked_multi_cycle_chain
validate_second_closed_cycle_receipt = _core.validate_second_closed_cycle_receipt
validate_successor_evidence_closure_receipt = _core.validate_successor_evidence_closure_receipt
validate_successor_licensed_act_handoff_receipt = _core.validate_successor_licensed_act_handoff_receipt

__all__ = [
    "CHAIN_NON_AUTHORITY",
    "CHAIN_VERSION",
    "CLOSURE_NON_AUTHORITY",
    "CLOSURE_VERSION",
    "CYCLE_NON_AUTHORITY",
    "CYCLE_ID",
    "CYCLE_RECEIPT_VERSION",
    "HANDOFF_VERSION",
    "MATERIALIZATION_NON_AUTHORITY",
    "VERSION",
    "build_digest_linked_multi_cycle_chain",
    "build_second_closed_cycle_receipt",
    "build_successor_evidence_closure_receipt",
    "build_successor_licensed_act_handoff_receipt",
    "multi_cycle_chain_digest",
    "second_cycle_receipt_digest",
    "successor_closure_digest",
    "successor_handoff_digest",
    "validate_digest_linked_multi_cycle_chain",
    "validate_second_closed_cycle_receipt",
    "validate_successor_evidence_closure_receipt",
    "validate_successor_licensed_act_handoff_receipt",
]
