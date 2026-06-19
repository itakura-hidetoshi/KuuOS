from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from runtime import kuuos_qi_world_native_generational_replan_core_v1_4 as _core
from runtime.kuuos_decision_os_wa_kernel_v0_3 import build_initial_wa_state
from runtime.kuuos_decision_os_wa_store_v0_3 import WaDecisionStore
from runtime.v03_decision_os_wa_relational_harmony import (
    WA_THRESHOLDS,
    WA_WEIGHTS,
    _complete_wa_cycle,
    _profile,
)


def _build_v14_wa(root: Path, plural: Mapping[str, Any]) -> dict[str, Any]:
    profiles = [
        _profile(
            plural,
            "strengthen-evidence",
            positive_lower=0.84,
            positive_upper=0.94,
        ),
        _profile(
            plural,
            "continue-current",
            positive_lower=0.62,
            positive_upper=0.74,
            alert_lower=0.08,
            alert_upper=0.16,
        ),
        _profile(
            plural,
            "hold-safe",
            positive_lower=0.58,
            positive_upper=0.70,
            alert_lower=0.04,
            alert_upper=0.10,
        ),
    ]
    store = WaDecisionStore(root)
    state = store.initialize(
        build_initial_wa_state(
            wa_id="native-generational-replan-wa",
            source_plural_state=plural,
            weights=WA_WEIGHTS,
            thresholds=WA_THRESHOLDS,
            now_ms=30_000,
        )
    )
    state, _ = _complete_wa_cycle(
        store,
        state,
        profiles=profiles,
        requested_route="ENDORSE",
        tick_base=20,
    )
    return state


_core._build_wa = _build_v14_wa

VERSION = _core.VERSION
RECEIPT_VERSION = _core.RECEIPT_VERSION
CYCLE_ID = _core.CYCLE_ID
NON_AUTHORITY = _core.NON_AUTHORITY
_digest = _core._digest
receipt_digest = _core.receipt_digest
build_native_generational_replan_receipt = (
    _core.build_native_generational_replan_receipt
)
validate_native_generational_replan_receipt = (
    _core.validate_native_generational_replan_receipt
)
