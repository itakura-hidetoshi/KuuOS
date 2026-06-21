from __future__ import annotations

import json

from runtime.kuuos_endogenous_mission_observation_v0_31 import (
    build_mission_observation_report,
    make_world_evidence_packet,
)
from runtime.kuuos_open_ended_background_agency_v0_30 import make_initial_state


def main() -> int:
    state = make_initial_state(
        agency_id="v031-check",
        root_lineage_digest="a" * 64,
        created_at_ms=1_000,
    )
    packet = make_world_evidence_packet(
        packet_id="v031-check-packet",
        source_state_digest=state["body_digest"],
        world_fragment_digest="b" * 64,
        observed_at_ms=1_010,
        unresolved_items=[
            {
                "item_id": "anomaly-1",
                "question": "Which hypothesis explains the unresolved WORLD anomaly?",
                "severity": 3,
                "uncertainty": 4,
                "evidence_refs": ["observation:1"],
                "counterevidence_refs": ["observation:counter-1"],
            }
        ],
        observation_channels=[
            {
                "channel_id": "structured-observer",
                "modality": "structured-observation",
                "supports_items": ["anomaly-1"],
                "cost_class": "LOW",
                "risk_class": "LOW",
                "latency_class": "SHORT",
            },
            {
                "channel_id": "historical-retrieval",
                "modality": "memory-and-archive-retrieval",
                "supports_items": ["*"],
                "cost_class": "LOW",
                "risk_class": "LOW",
                "latency_class": "MEDIUM",
            },
        ],
    )
    report = build_mission_observation_report(state, packet, generated_at_ms=1_020)
    body = report["body"]
    assert body["route"] == "MISSION_PORTFOLIO_READY"
    assert len(body["mission_candidates"]) == 1
    assert len(body["observation_portfolio"]) == 2
    assert body["mission_candidates"][0]["mission_type"] == "DISAMBIGUATE"
    assert body["grants_plan_activation"] is False
    assert body["grants_actos_invocation"] is False
    print(json.dumps({
        "status": "ENDOGENOUS_MISSION_OBSERVATION_V0_31_OK",
        "report_digest": report["body_digest"],
        "route": body["route"],
        "mission_candidates": len(body["mission_candidates"]),
        "observation_candidates": len(body["observation_portfolio"]),
        "counterevidence_preserved": body["preserves_counterevidence"],
        "candidate_not_authority": body["mission_candidate_not_activation"],
    }, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
