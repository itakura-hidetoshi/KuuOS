#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from runtime.kuuos_codeai_candidate_patch_envelope_v0_1 import seal
from runtime.kuuos_codeai_autonomous_unified_diff_candidates_v0_1 import (
    RECEIPT_DIGEST_FIELD as UNIFIED_DIFF_RECEIPT_DIGEST_FIELD,
    STATUS_READY as UNIFIED_DIFF_STATUS_READY,
    build_codeai_autonomous_unified_diff_candidates,
)
from runtime.kuuos_codeai_autonomous_candidate_portfolio_selection_v0_1 import (
    POLICY_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    STATUS_READY,
    build_codeai_autonomous_candidate_portfolio_selection,
)

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    proposal_data = json.loads(
        (ROOT / "examples" / "codeai_autonomous_unified_diff_candidates_v0_1.json").read_text(
            encoding="utf-8"
        )
    )
    candidate_data = json.loads(
        (ROOT / "examples" / "codeai_candidate_patch_envelope_v0_1.json").read_text(
            encoding="utf-8"
        )
    )
    selection_data = json.loads(
        (ROOT / "examples" / "codeai_autonomous_candidate_portfolio_selection_v0_1.json").read_text(
            encoding="utf-8"
        )
    )
    upstream = build_codeai_autonomous_unified_diff_candidates(
        source_observation_receipt=candidate_data["source_observation_receipt"],
        repository_files=proposal_data["repository_files"],
        proposals=proposal_data["proposals"],
        candidate_policy=candidate_data["candidate_policy"],
    )
    assert upstream.status == UNIFIED_DIFF_STATUS_READY, upstream.issues
    assert upstream.receipt is not None
    source_digest = upstream.receipt[UNIFIED_DIFF_RECEIPT_DIGEST_FIELD]
    request = dict(selection_data["selection_request"])
    request["source_portfolio_receipt_digest"] = source_digest
    request = seal(request, REQUEST_DIGEST_FIELD)
    policy = dict(selection_data["selection_policy"])
    policy["expected_source_portfolio_receipt_digest"] = source_digest
    policy = seal(policy, POLICY_DIGEST_FIELD)
    result = build_codeai_autonomous_candidate_portfolio_selection(
        source_portfolio_receipt=upstream.receipt,
        candidates=upstream.candidates,
        selection_request=request,
        selection_policy=policy,
    )
    assert result.status == STATUS_READY, result.issues
    assert result.selected_candidate is not None
    assert result.selected_candidate.upstream_rank == 1
    assert result.receipt is not None
    assert result.receipt["candidate_selected"] is True
    assert result.receipt["selected_for_independent_verification"] is True
    assert result.receipt["verification_lease_issued"] is False
    assert result.receipt["execution_lease_issued"] is False
    assert result.receipt["repository_mutation_performed"] is False
    assert result.receipt["selected_candidate_treated_as_correct"] is False
    print("PASS: autonomous candidate portfolio selection chose one verification target")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
