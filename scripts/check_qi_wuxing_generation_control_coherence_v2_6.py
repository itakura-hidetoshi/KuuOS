#!/usr/bin/env python3
from __future__ import annotations

import json

from runtime.kuuos_qi_yinyang_wuxing_fibonacci_history_geometry_v2_5 import (
    build_yinyang_wuxing_fibonacci_history_receipt,
)
from runtime.kuuos_qi_wuxing_generation_control_coherence_v2_6 import (
    STATUS_OK,
    build_wuxing_generation_control_coherence_receipt,
    validate_wuxing_generation_control_coherence_receipt,
)


def _v2_4_dependency_receipt() -> dict:
    return {
        "version": "kuuos_qi_process_tensor_local_real_yinyang_geometry_v2_4",
        "local_real_yinyang_receipt_digest": "v2-6-check-source-digest",
        "process_tensor_surface": {"process_support_visible": True},
        "local_real_structure_surface": {
            "all_frames_involutive": True,
            "all_frames_gauge_local": True,
            "absolute_global_polarity_claim": False,
        },
        "recoverability_surface": {
            "protected_history_visible": True,
            "two_truths_gap": True,
        },
        "non_authority": {
            "grants_execution_authority": False,
            "grants_truth_authority": False,
        },
    }


def _v2_5_receipt() -> dict:
    return build_yinyang_wuxing_fibonacci_history_receipt(
        _v2_4_dependency_receipt(),
        initial_phase_index=0,
        steps=5,
        resolved_channels=1,
        active_channels=0,
    )


def main() -> int:
    predecessor = _v2_5_receipt()

    balanced = build_wuxing_generation_control_coherence_receipt(
        predecessor,
        nominal_control_strength=1.0,
        actual_control_strength=1.0,
    )
    assert validate_wuxing_generation_control_coherence_receipt(
        predecessor, balanced
    ) == []
    assert balanced["strength_surface"]["classification"] == "balanced"
    assert balanced["strength_surface"]["overacting_control"] is False
    assert balanced["phase_history_separation_surface"]["phase_endpoint_agrees"] is True
    assert balanced["phase_history_separation_surface"]["history_endpoint_differs"] is True
    assert balanced["inverse_direction_surface"]["phase_returns"] is True
    assert balanced["inverse_direction_surface"]["history_advances_twice"] is True
    assert balanced["coherence_surface"]["composition_verified"] is True
    assert balanced["coherence_surface"]["center_is_coherence_not_earth_substance"] is True

    overacting = build_wuxing_generation_control_coherence_receipt(
        predecessor,
        nominal_control_strength=1.0,
        actual_control_strength=1.5,
    )
    assert overacting["strength_surface"]["classification"] == "over"
    assert overacting["strength_surface"]["overacting_control"] is True

    under = build_wuxing_generation_control_coherence_receipt(
        predecessor,
        nominal_control_strength=1.0,
        actual_control_strength=0.5,
    )
    assert under["strength_surface"]["classification"] == "under"
    assert under["strength_surface"]["overacting_control"] is False

    held = build_wuxing_generation_control_coherence_receipt(
        predecessor,
        preserve_protected_history=False,
    )
    assert held["projection_admissible"] is False
    assert held["disposition"] == "YIN_HOLDS_ON_TWO_TRUTHS_OR_PROTECTED_HISTORY_GAP"

    assert all(value is False for value in balanced["non_authority"].values())

    print(
        json.dumps(
            {
                "status": STATUS_OK,
                "balanced_digest": balanced[
                    "generation_control_coherence_receipt_digest"
                ],
                "balanced_disposition": balanced["disposition"],
                "phase_endpoint_agrees_history_differs": True,
                "control_insult_phase_returns_history_persists": True,
                "composition_coherence_verified": True,
                "overacting_is_excess_control": True,
                "center_is_coherence_not_earth_substance": True,
                "non_authority_preserved": True,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
