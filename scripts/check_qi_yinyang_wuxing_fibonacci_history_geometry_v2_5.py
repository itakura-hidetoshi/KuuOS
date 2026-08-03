#!/usr/bin/env python3
from __future__ import annotations

import json

from runtime.kuuos_qi_yinyang_wuxing_fibonacci_history_geometry_v2_5 import (
    STATUS_OK,
    build_yinyang_wuxing_fibonacci_history_receipt,
    validate_yinyang_wuxing_fibonacci_history_receipt,
)


def _dependency_receipt() -> dict:
    return {
        "version": "kuuos_qi_process_tensor_local_real_yinyang_geometry_v2_4",
        "local_real_yinyang_receipt_digest": "v2-5-check-source-digest",
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


def main() -> int:
    dependency = _dependency_receipt()
    baseline = build_yinyang_wuxing_fibonacci_history_receipt(
        dependency,
        initial_phase_index=0,
        steps=5,
        resolved_channels=1,
        active_channels=0,
    )
    assert validate_yinyang_wuxing_fibonacci_history_receipt(
        dependency, baseline
    ) == []
    projection = baseline["fibonacci_history_fibre_surface"]["projection"]
    assert projection["final_phase_index"] == 0
    assert projection["final_resolved_channels"] == 3
    assert projection["final_active_channels"] == 5
    assert baseline["five_phase_base_surface"]["phase_returned"] is True
    assert baseline["fibonacci_history_fibre_surface"]["history_returned"] is False
    assert baseline["golden_ratio_growth_surface"]["dimension_scaling_verified"] is True

    ten_step = build_yinyang_wuxing_fibonacci_history_receipt(
        dependency,
        initial_phase_index=3,
        steps=10,
        resolved_channels=1,
        active_channels=0,
    )
    ten_projection = ten_step["fibonacci_history_fibre_surface"]["projection"]
    assert ten_projection["final_phase_index"] == 3
    assert (
        ten_projection["final_resolved_channels"],
        ten_projection["final_active_channels"],
    ) == (34, 55)

    held = build_yinyang_wuxing_fibonacci_history_receipt(
        dependency,
        preserve_two_truths_gap=False,
    )
    assert held["projection_admissible"] is False
    assert held["disposition"] == (
        "YIN_HOLDS_ON_TWO_TRUTHS_OR_PROTECTED_HISTORY_GAP"
    )

    assert all(value is False for value in baseline["non_authority"].values())
    print(
        json.dumps(
            {
                "status": STATUS_OK,
                "baseline_digest": baseline["wuxing_fibonacci_receipt_digest"],
                "baseline_disposition": baseline["disposition"],
                "five_step_coefficients": [
                    projection["final_resolved_channels"],
                    projection["final_active_channels"],
                ],
                "ten_step_coefficients": [
                    ten_projection["final_resolved_channels"],
                    ten_projection["final_active_channels"],
                ],
                "phase_returns_history_advances": True,
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
