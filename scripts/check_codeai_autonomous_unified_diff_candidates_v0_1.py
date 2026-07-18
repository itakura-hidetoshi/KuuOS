#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import runtime.kuuos_codeai_autonomous_unified_diff_candidates_v0_1 as m

ROOT = Path(__file__).resolve().parents[1]
BASE_EXAMPLE = ROOT / "examples" / "codeai_candidate_patch_envelope_v0_1.json"
EXAMPLE = ROOT / "examples" / "codeai_autonomous_unified_diff_candidates_v0_1.json"


def load_inputs() -> dict:
    base = json.loads(BASE_EXAMPLE.read_text(encoding="utf-8"))
    example = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    return {
        "source_observation_receipt": base["source_observation_receipt"],
        "candidate_policy": base["candidate_policy"],
        "repository_files": example["repository_files"],
        "proposals": example["proposals"],
    }


def main() -> None:
    result = m.build_codeai_autonomous_unified_diff_candidates(**load_inputs())
    assert result.status == m.STATUS_READY, result.issues
    assert len(result.candidates) == 2
    assert result.candidates[0].rank == 1
    assert result.candidates[0].proposal_id.endswith("001")
    assert result.receipt is not None
    assert result.receipt["candidate_selected"] is False
    assert result.receipt["patch_applied"] is False
    assert result.receipt["repository_mutation_performed"] is False
    assert result.receipt["unified_diff_candidates_generated_by_kernel"] is True
    for candidate in result.candidates:
        assert candidate.patch_artifact.startswith("diff --git a/")
        assert candidate.patch_artifact.endswith("\n")
        assert candidate.candidate_receipt["candidate_patch_ready"] is True
    print(
        json.dumps(
            {
                "status": result.status,
                "candidate_count": len(result.candidates),
                "candidate_ids": [item.proposal_id for item in result.candidates],
                "receipt_digest": result.receipt[m.RECEIPT_DIGEST_FIELD],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
