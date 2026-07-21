#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from runtime.kuuos_codeai_temporal_holdout_replay_corpus_v0_1 import (
    CORPUS_DIGEST_FIELD,
    DISPOSITION_SEALED,
    EVIDENCE_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD,
    STATUS_READY,
    build_codeai_temporal_holdout_replay_corpus,
    seal,
)
from scripts.build_codeai_temporal_holdout_replay_corpus_fixture_v0_1 import (
    build_fixture,
)
from scripts.project_codeai_temporal_holdout_replay_corpus_fixture_v0_1 import (
    project_fixture,
)

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    fixture = build_fixture()
    result = build_codeai_temporal_holdout_replay_corpus(
        corpus=fixture["corpus"],
        request=fixture["request"],
        policy=fixture["policy"],
    )
    if result.status != STATUS_READY or result.evidence is None or result.receipt is None:
        raise SystemExit("temporal holdout corpus blocked: " + ",".join(result.issues))
    if result.receipt["codeai_disposition"] != DISPOSITION_SEALED:
        raise SystemExit("temporal holdout corpus disposition mismatch")
    if result.evidence[EVIDENCE_DIGEST_FIELD] != seal(
        result.evidence, EVIDENCE_DIGEST_FIELD
    )[EVIDENCE_DIGEST_FIELD]:
        raise SystemExit("temporal holdout evidence seal is not deterministic")
    if result.receipt[RECEIPT_DIGEST_FIELD] != seal(
        result.receipt, RECEIPT_DIGEST_FIELD
    )[RECEIPT_DIGEST_FIELD]:
        raise SystemExit("temporal holdout receipt seal is not deterministic")
    if fixture["corpus"][CORPUS_DIGEST_FIELD] != seal(
        fixture["corpus"], CORPUS_DIGEST_FIELD
    )[CORPUS_DIGEST_FIELD]:
        raise SystemExit("temporal holdout corpus seal is not deterministic")
    committed = json.loads(
        (ROOT / "examples/codeai_temporal_holdout_replay_corpus_v0_1.json").read_text(
            encoding="utf-8"
        )
    )
    projected = project_fixture(fixture)
    if committed != projected:
        raise SystemExit("committed temporal holdout projection is stale")
    for field in (
        "temporal_order_verified",
        "holdout_hidden_from_candidate_generation",
        "holdout_excluded_from_threshold_tuning",
        "holdout_excluded_from_memory_training",
        "holdout_excluded_from_prompt_selection",
        "holdout_excluded_from_model_selection",
    ):
        if result.evidence[field] is not True:
            raise SystemExit("temporal holdout guarantee missing: " + field)
    for field in (
        "historical_code_reexecuted",
        "provider_invoked",
        "verification_runner_invoked",
        "repository_mutation_performed",
        "git_effect_performed",
        "network_accessed",
        "secret_material_read",
        "selection_authority_granted",
        "successor_stage_authority_granted",
        "representativeness_claimed",
        "randomness_claimed",
        "unbiasedness_claimed",
        "correctness_proof_claimed",
    ):
        if result.evidence[field] is not False:
            raise SystemExit("temporal holdout boundary violated: " + field)
    print(
        json.dumps(
            {
                "status": result.status,
                "codeai_disposition": result.receipt["codeai_disposition"],
                "corpus_digest": fixture["corpus"][CORPUS_DIGEST_FIELD],
                "development_case_count": result.evidence["development_case_count"],
                "holdout_case_count": result.evidence["holdout_case_count"],
                "cross_split_case_id_overlap_count": result.evidence[
                    "cross_split_case_id_overlap_count"
                ],
                "cross_split_issue_digest_overlap_count": result.evidence[
                    "cross_split_issue_digest_overlap_count"
                ],
                "cross_split_replay_case_digest_overlap_count": result.evidence[
                    "cross_split_replay_case_digest_overlap_count"
                ],
                "evidence_digest": result.evidence[EVIDENCE_DIGEST_FIELD],
                "receipt_digest": result.receipt[RECEIPT_DIGEST_FIELD],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
