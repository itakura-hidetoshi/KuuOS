#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from runtime.kuuos_codeai_autonomous_structured_edit_synthesis_v0_1 import (
    BOUNDARY_CANDIDATE,
    BOUNDARY_REJECT,
    BOUNDARY_REPAIR,
    ProviderAdapter,
    STATUS_READY,
    build_codeai_autonomous_structured_edit_synthesis,
)

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "codeai_autonomous_structured_edit_synthesis_v0_1.json"
CANDIDATE_EXAMPLE = ROOT / "examples" / "codeai_candidate_patch_envelope_v0_1.json"


def main() -> int:
    data = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    candidate_data = json.loads(CANDIDATE_EXAMPLE.read_text(encoding="utf-8"))
    adapters = [
        ProviderAdapter(
            item["adapter_id"],
            item["provider_id"],
            item["model_id"],
            lambda _prompt, response=item["response"]: response,
        )
        for item in data["provider_adapters"]
    ]
    result = build_codeai_autonomous_structured_edit_synthesis(
        source_observation_receipt=candidate_data["source_observation_receipt"],
        repository_files=data["repository_files"],
        synthesis_request=data["synthesis_request"],
        provider_adapters=adapters,
        synthesis_policy=data["synthesis_policy"],
        candidate_policy=candidate_data["candidate_policy"],
    )
    assert result.status == STATUS_READY, result.issues
    assert len(result.attempts) == 3
    assert [attempt.boundary_status for attempt in result.attempts] == [
        BOUNDARY_REJECT,
        BOUNDARY_CANDIDATE,
        BOUNDARY_REPAIR,
    ]
    assert len(result.candidates) == 1
    assert result.receipt is not None
    assert result.receipt["provider_call_count"] == 3
    assert result.receipt["structured_proposal_count"] == 1
    assert result.receipt["generated_candidate_count"] == 1
    assert result.receipt["raw_provider_output_treated_as_authority"] is False
    assert result.receipt["candidate_selected"] is False
    assert result.receipt["repository_mutation_performed"] is False
    assert result.receipt["execution_authority_granted"] is False
    print("PASS: autonomous structured edit synthesis produced one governed diff candidate")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
