#!/usr/bin/env python3
from __future__ import annotations

import json

from runtime.kuuos_qi_process_tensor_local_real_yinyang_geometry_v2_4 import (
    STATUS_OK,
    build_local_real_yinyang_geometry_receipt,
    compose_conversion_parity,
    validate_local_real_yinyang_geometry_receipt,
)


def main() -> int:
    qi = {
        "cycle_id": "v2-4-check-cycle",
        "process_tensor_visible": True,
        "transition_continuity_visible": True,
        "memory_continuity_visible": True,
        "nonmarkov_memory_visible": True,
        "qi_process_tensor_receipt_digest": "v2-4-check-source-digest",
    }
    frames = [
        {
            "context_id": "clinical-local-context",
            "conjugation_involutive": True,
            "gauge_local": True,
            "absolute_global_polarity_claim": False,
        },
        {
            "context_id": "recovery-local-context",
            "conjugation_involutive": True,
            "gauge_local": True,
            "absolute_global_polarity_claim": False,
        },
    ]
    double_conversion = [
        {
            "source_context": "clinical-local-context",
            "target_context": "held-memory-context",
            "real_structure_compatible": False,
            "conversion_visible": True,
            "memory_link_visible": True,
            "holonomy_residue_visible": True,
        },
        {
            "source_context": "held-memory-context",
            "target_context": "recovery-local-context",
            "real_structure_compatible": False,
            "conversion_visible": True,
            "memory_link_visible": True,
            "holonomy_residue_visible": True,
        },
    ]

    baseline = build_local_real_yinyang_geometry_receipt(
        qi,
        frames,
        double_conversion,
        qi_intensity=4,
        qi_capacity=6,
        recoverability_gap_candidate=0.2,
    )
    assert validate_local_real_yinyang_geometry_receipt(qi, baseline) == []
    assert baseline["candidate_flow_admissible"] is True
    assert baseline["history_transport_surface"]["conversion_parity"] == "even"
    assert baseline["history_transport_surface"]["composed_polarity_action"] == "preserve"
    assert baseline["qi_split_surface"]["admitted_plus_held_equals_total"] is True
    assert baseline["recoverability_surface"]["recoverability_gap_candidate_visible"] is True

    saturation = build_local_real_yinyang_geometry_receipt(
        qi,
        frames,
        double_conversion,
        qi_intensity=9,
        qi_capacity=6,
        recoverability_gap_candidate=0.2,
    )
    assert saturation["admitted_qi_intensity"] == 6
    assert saturation["held_qi_residue"] == 3
    assert saturation["disposition"] == "YANG_SATURATION_SPLITS_ADMITTED_AND_HELD_QI"

    boundary_hold = build_local_real_yinyang_geometry_receipt(
        qi,
        frames,
        double_conversion,
        qi_intensity=4,
        qi_capacity=6,
        two_truths_gap=False,
    )
    assert boundary_hold["candidate_flow_admissible"] is False
    assert boundary_hold["admitted_qi_intensity"] == 0
    assert boundary_hold["held_qi_residue"] == 4

    odd_conversion = build_local_real_yinyang_geometry_receipt(
        qi,
        frames,
        double_conversion[:1],
        qi_intensity=4,
        qi_capacity=6,
    )
    assert odd_conversion["history_transport_surface"]["conversion_parity"] == "odd"
    assert odd_conversion["disposition"] == (
        "ODD_LOCAL_REAL_CONVERSION_REQUIRES_POLARITY_AWARE_READOUT"
    )
    assert compose_conversion_parity("convert", "convert") == "preserve"
    assert compose_conversion_parity("preserve", "convert") == "convert"

    absolute_frames = [dict(frame) for frame in frames]
    absolute_frames[0]["absolute_global_polarity_claim"] = True
    absolute_claim = build_local_real_yinyang_geometry_receipt(
        qi,
        absolute_frames,
        double_conversion,
        qi_intensity=4,
        qi_capacity=6,
    )
    assert absolute_claim["candidate_flow_admissible"] is False
    assert absolute_claim["disposition"] == (
        "FAIL_CLOSED_ON_GLOBAL_ABSOLUTE_POLARITY_CLAIM"
    )

    assert all(value is False for value in baseline["non_authority"].values())
    print(
        json.dumps(
            {
                "status": STATUS_OK,
                "baseline_digest": baseline["local_real_yinyang_receipt_digest"],
                "baseline_disposition": baseline["disposition"],
                "saturation_held_qi_residue": saturation["held_qi_residue"],
                "odd_conversion_parity": odd_conversion["history_transport_surface"][
                    "conversion_parity"
                ],
                "absolute_claim_disposition": absolute_claim["disposition"],
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
