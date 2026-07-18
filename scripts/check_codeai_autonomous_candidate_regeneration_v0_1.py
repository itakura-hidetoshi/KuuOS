#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
from pathlib import Path

from runtime.kuuos_codeai_autonomous_structured_edit_synthesis_v0_1 import (
    ProviderAdapter,
    STATUS_READY as SYNTHESIS_READY,
    build_codeai_autonomous_structured_edit_synthesis,
)
from runtime.kuuos_codeai_autonomous_candidate_regeneration_v0_1 import (
    STATUS_READY,
    build_codeai_autonomous_candidate_regeneration,
)

ROOT = Path(__file__).resolve().parents[1]
STRUCTURED_EXAMPLE = ROOT / "examples" / "codeai_autonomous_structured_edit_synthesis_v0_1.json"
CANDIDATE_EXAMPLE = ROOT / "examples" / "codeai_candidate_patch_envelope_v0_1.json"
REGEN_EXAMPLE = ROOT / "examples" / "codeai_autonomous_candidate_regeneration_v0_1.json"


def main() -> int:
    structured = json.loads(STRUCTURED_EXAMPLE.read_text(encoding="utf-8"))
    candidate = json.loads(CANDIDATE_EXAMPLE.read_text(encoding="utf-8"))
    regen = json.loads(REGEN_EXAMPLE.read_text(encoding="utf-8"))

    seed_item = structured["provider_adapters"][0]
    seed_adapter = ProviderAdapter(
        seed_item["adapter_id"],
        seed_item["provider_id"],
        seed_item["model_id"],
        lambda _prompt, response=seed_item["response"]: copy.deepcopy(response),
    )
    seed = build_codeai_autonomous_structured_edit_synthesis(
        source_observation_receipt=candidate["source_observation_receipt"],
        repository_files=structured["repository_files"],
        synthesis_request=structured["synthesis_request"],
        provider_adapters=[seed_adapter],
        synthesis_policy=structured["synthesis_policy"],
        candidate_policy=candidate["candidate_policy"],
    )
    assert seed.status == SYNTHESIS_READY, seed.issues
    assert seed.receipt is not None
    assert len(seed.candidates) == 1

    adapters = []
    for item in regen["provider_adapters"]:
        queue = [copy.deepcopy(response) for response in item["responses"]]
        adapters.append(ProviderAdapter(
            item["adapter_id"], item["provider_id"], item["model_id"],
            lambda _prompt, responses=queue: responses.pop(0),
        ))

    result = build_codeai_autonomous_candidate_regeneration(
        source_generation_receipt=seed.receipt,
        source_observation_receipt=candidate["source_observation_receipt"],
        repository_files=regen["repository_files"],
        seed_candidates=seed.candidates,
        regeneration_request=regen["regeneration_request"],
        provider_adapters=adapters,
        regeneration_policy=regen["regeneration_policy"],
        candidate_policy=candidate["candidate_policy"],
    )
    assert result.status == STATUS_READY, result.issues
    assert len(result.regenerated_candidates) == 2
    assert len(result.combined_candidates) == 3
    assert [item.rank for item in result.combined_candidates] == [1, 2, 3]
    assert result.receipt is not None
    assert result.receipt["target_reached"] is True
    assert result.receipt["semantic_patch_deduplication_performed"] is True
    assert result.receipt["candidate_selected"] is False
    assert result.receipt["repository_mutation_performed"] is False
    assert result.receipt["git_ref_changed"] is False
    assert result.receipt["verification_authority_granted"] is False
    print("PASS: autonomous candidate regeneration produced two novel lineage-bound candidates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
