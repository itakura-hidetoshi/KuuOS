#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

from runtime.kuuos_codeai_candidate_patch_envelope_v0_1 import canonical_digest, seal
from runtime.kuuos_codeai_autonomous_unified_diff_candidates_v0_1 import (
    RECEIPT_DIGEST_FIELD as UNIFIED_DIFF_RECEIPT_DIGEST_FIELD,
    STATUS_READY as UNIFIED_DIFF_STATUS_READY,
    build_codeai_autonomous_unified_diff_candidates,
)
from runtime.kuuos_codeai_autonomous_candidate_portfolio_selection_v0_1 import (
    POLICY_DIGEST_FIELD as SELECTION_POLICY_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD as SELECTION_REQUEST_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as SELECTION_RECEIPT_DIGEST_FIELD,
    STATUS_READY as SELECTION_STATUS_READY,
    build_codeai_autonomous_candidate_portfolio_selection,
)
from runtime.kuuos_codeai_autonomous_isolated_candidate_application_v0_1 import (
    POLICY_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    STATUS_READY,
    build_codeai_autonomous_isolated_candidate_application,
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
    application_data = json.loads(
        (ROOT / "examples" / "codeai_autonomous_isolated_candidate_application_v0_1.json").read_text(
            encoding="utf-8"
        )
    )

    repository_files = proposal_data["repository_files"]
    repository_before = deepcopy(repository_files)
    upstream = build_codeai_autonomous_unified_diff_candidates(
        source_observation_receipt=candidate_data["source_observation_receipt"],
        repository_files=repository_files,
        proposals=proposal_data["proposals"],
        candidate_policy=candidate_data["candidate_policy"],
    )
    assert upstream.status == UNIFIED_DIFF_STATUS_READY, upstream.issues
    assert upstream.receipt is not None
    portfolio_digest = upstream.receipt[UNIFIED_DIFF_RECEIPT_DIGEST_FIELD]

    selection_request = dict(selection_data["selection_request"])
    selection_request["source_portfolio_receipt_digest"] = portfolio_digest
    selection_request = seal(selection_request, SELECTION_REQUEST_DIGEST_FIELD)
    selection_policy = dict(selection_data["selection_policy"])
    selection_policy["expected_source_portfolio_receipt_digest"] = portfolio_digest
    selection_policy = seal(selection_policy, SELECTION_POLICY_DIGEST_FIELD)
    selection = build_codeai_autonomous_candidate_portfolio_selection(
        source_portfolio_receipt=upstream.receipt,
        candidates=upstream.candidates,
        selection_request=selection_request,
        selection_policy=selection_policy,
    )
    assert selection.status == SELECTION_STATUS_READY, selection.issues
    assert selection.receipt is not None
    assert selection.selected_candidate is not None

    selected = selection.selected_candidate
    candidate = selected.patch_candidate
    source_snapshot_digest = canonical_digest(repository_files)
    request = dict(application_data["application_request"])
    request["source_selection_receipt_digest"] = selection.receipt[
        SELECTION_RECEIPT_DIGEST_FIELD
    ]
    request["selected_candidate_digest"] = candidate["codeai_candidate_patch_digest"]
    request["source_repository_snapshot_digest"] = source_snapshot_digest
    request = seal(request, REQUEST_DIGEST_FIELD)
    policy = dict(application_data["application_policy"])
    policy["expected_source_selection_receipt_digest"] = selection.receipt[
        SELECTION_RECEIPT_DIGEST_FIELD
    ]
    policy["expected_selected_candidate_digest"] = candidate[
        "codeai_candidate_patch_digest"
    ]
    policy["expected_patch_artifact_digest"] = candidate["patch_artifact_digest"]
    policy["expected_repository_full_name"] = candidate["repository_full_name"]
    policy["expected_source_commit_sha"] = candidate["source_commit_sha"]
    policy["expected_source_repository_snapshot_digest"] = source_snapshot_digest
    policy = seal(policy, POLICY_DIGEST_FIELD)

    result = build_codeai_autonomous_isolated_candidate_application(
        source_selection_receipt=selection.receipt,
        selected_candidate=selected,
        repository_files=repository_files,
        application_request=request,
        application_policy=policy,
    )
    assert result.status == STATUS_READY, result.issues
    assert result.resulting_repository_files is not None
    assert result.receipt is not None
    assert repository_files == repository_before
    assert result.resulting_repository_files != repository_files
    assert result.receipt["isolated_patch_applied"] is True
    assert result.receipt["isolated_snapshot_materialized"] is True
    assert result.receipt["verification_workspace_ready"] is True
    assert result.receipt["live_repository_patch_applied"] is False
    assert result.receipt["repository_mutation_performed"] is False
    assert result.receipt["git_ref_changed"] is False
    assert result.receipt["verification_executed"] is False
    print("PASS: selected candidate materialized into an isolated verification snapshot")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
