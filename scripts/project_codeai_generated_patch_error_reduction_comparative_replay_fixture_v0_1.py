#!/usr/bin/env python3
from __future__ import annotations

from typing import Any

from runtime.kuuos_codeai_generated_patch_error_reduction_comparative_replay_evaluation_v0_1 import (
    EVIDENCE_DIGEST_FIELD,
    POLICY_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
)


def project_fixture(fixture: dict[str, Any]) -> dict[str, Any]:
    baseline = fixture["baseline"]
    successor = fixture["successor"]
    comparison_evidence = fixture["comparison_evidence"]
    comparison_receipt = fixture["comparison_receipt"]
    return {
        "schema_version": fixture["schema_version"],
        "profile_version": fixture["profile_version"],
        "baseline": {
            "dataset_id": baseline["dataset"]["dataset_id"],
            "dataset_digest": baseline["dataset"][
                "codeai_generated_patch_error_replay_dataset_digest"
            ],
            "evidence_digest": baseline["evidence"][
                "codeai_generated_patch_error_baseline_evidence_digest"
            ],
            "receipt_digest": baseline["receipt"][
                "codeai_generated_patch_error_baseline_receipt_digest"
            ],
            "metrics_digest": baseline["evidence"]["metrics_digest"],
            "total_case_count": baseline["evidence"]["metrics"]["total_case_count"],
            "verified_patch_count": baseline["evidence"]["metrics"][
                "verified_patch_count"
            ],
        },
        "successor": {
            "dataset_id": successor["dataset"]["dataset_id"],
            "dataset_digest": successor["dataset"][
                "codeai_generated_patch_error_replay_dataset_digest"
            ],
            "evidence_digest": successor["evidence"][
                "codeai_generated_patch_error_baseline_evidence_digest"
            ],
            "receipt_digest": successor["receipt"][
                "codeai_generated_patch_error_baseline_receipt_digest"
            ],
            "metrics_digest": successor["evidence"]["metrics_digest"],
            "total_case_count": successor["evidence"]["metrics"]["total_case_count"],
            "verified_patch_count": successor["evidence"]["metrics"][
                "verified_patch_count"
            ],
        },
        "comparison_request_digest": fixture["comparison_request"][
            REQUEST_DIGEST_FIELD
        ],
        "comparison_policy_digest": fixture["comparison_policy"][
            POLICY_DIGEST_FIELD
        ],
        "comparison_evidence_digest": comparison_evidence[EVIDENCE_DIGEST_FIELD],
        "comparison_receipt_digest": comparison_receipt[RECEIPT_DIGEST_FIELD],
        "codeai_disposition": comparison_receipt["codeai_disposition"],
        "error_reduction_confirmed": comparison_receipt[
            "error_reduction_confirmed"
        ],
        "comparison_metrics": comparison_evidence["comparison_metrics"],
    }
