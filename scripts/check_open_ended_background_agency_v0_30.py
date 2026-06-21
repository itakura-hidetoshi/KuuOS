from __future__ import annotations

import json

from runtime.kuuos_open_ended_background_agency_v0_30 import (
    apply_request,
    make_initial_state,
    make_request,
    validate_state,
)


def main() -> int:
    state = make_initial_state(
        agency_id="open-ended-background-agent-example",
        root_lineage_digest="b" * 64,
        created_at_ms=1_000,
    )
    proposal = make_request(
        request_id="proposal-world-model-1",
        source_state_digest=state["body_digest"],
        action="PROPOSE_EXPANSION",
        payload={
            "candidate_id": "world-model-fragment-1",
            "dimension": "world_model_expansion",
            "description": "Preserve and investigate an unresolved world-model possibility",
            "evidence_refs": ["observation:unresolved-1"],
            "requested_capabilities": ["active-observation-candidate"],
        },
        requested_at_ms=1_010,
    )
    transition = apply_request(state, proposal, applied_at_ms=1_020)
    result_state = transition["body"]["result_state"]
    body = validate_state(result_state)
    assert all(value == "OPEN" for value in body["constitutional_horizons"].values())
    assert body["candidate_expansions"][0]["status"] == "CANDIDATE"
    assert body["candidate_expansions"][0]["grants_execution_authority"] is False
    assert "max_total_cycles" not in body
    print(json.dumps({
        "status": "OPEN_ENDED_BACKGROUND_AGENCY_V0_30_OK",
        "state_digest": result_state["body_digest"],
        "candidate_id": body["candidate_expansions"][0]["candidate_id"],
        "open_horizons": sorted(body["constitutional_horizons"]),
        "candidate_not_authority": True,
        "local_control_not_constitutional_closure": True,
    }, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
