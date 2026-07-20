from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_codeai_evidence_bearing_candidate_portfolio_schema_v0_1 import (
    CLASSIFICATIONS,
    DISPOSITION_ADMISSIBLE,
    DISPOSITION_HOLD,
    DISPOSITION_REJECTED,
    DISPOSITION_REPAIRABLE,
    PREFLIGHT_RECEIPT_DIGEST_FIELD,
    PREFLIGHT_REPORT_DIGEST_FIELD,
    classification_flags,
    route_for,
)


def report_receipt_correspondence_issues(
    report: Mapping[str, Any],
    receipt: Mapping[str, Any],
) -> list[str]:
    issues: list[str] = []
    pairs = (
        ("static_admissibility_report_digest", report[PREFLIGHT_REPORT_DIGEST_FIELD]),
        ("typed_edit_ir_digest", report["typed_edit_ir_digest"]),
        ("typed_edit_ir_receipt_digest", report["typed_edit_ir_receipt_digest"]),
        ("repository_full_name", report["repository_full_name"]),
        ("source_commit_sha", report["source_commit_sha"]),
        ("source_repository_snapshot_digest", report["source_repository_snapshot_digest"]),
        ("result_repository_snapshot_digest", report["result_repository_snapshot_digest"]),
        ("operation_count", report["operation_count"]),
        ("changed_paths", report["changed_paths"]),
        ("finding_counts", report["finding_counts"]),
        ("codeai_disposition", report["codeai_disposition"]),
    )
    for field, expected in pairs:
        if receipt.get(field) != expected:
            issues.append("preflight_report_receipt_mismatch:" + field)
    for field, expected in classification_flags(report["codeai_disposition"]).items():
        if receipt.get(field) is not expected:
            issues.append("preflight_report_receipt_mismatch:" + field)
    return issues


def normalize_candidate(
    *,
    candidate_id: str,
    candidate_sequence: int,
    report: Mapping[str, Any],
    receipt: Mapping[str, Any],
) -> dict[str, Any]:
    classification = report["codeai_disposition"]
    return {
        "candidate_id": candidate_id,
        "candidate_sequence": candidate_sequence,
        "classification": classification,
        "evidence_route": route_for(classification),
        "typed_edit_ir_digest": report["typed_edit_ir_digest"],
        "typed_edit_ir_receipt_digest": report["typed_edit_ir_receipt_digest"],
        "static_admissibility_report_digest": report[PREFLIGHT_REPORT_DIGEST_FIELD],
        "preflight_receipt_digest": receipt[PREFLIGHT_RECEIPT_DIGEST_FIELD],
        "repository_full_name": report["repository_full_name"],
        "source_commit_sha": report["source_commit_sha"],
        "source_repository_snapshot_digest": report["source_repository_snapshot_digest"],
        "result_repository_snapshot_digest": report["result_repository_snapshot_digest"],
        "operation_count": report["operation_count"],
        "changed_paths": list(report["changed_paths"]),
        "finding_counts": dict(report["finding_counts"]),
        "findings": [dict(finding) for finding in report["findings"]],
        "exact_lineage_verified": True,
        "classification_preserved": True,
        "finding_evidence_preserved": True,
        "preflight_route_receipt_preserved": True,
        "rank_assigned": False,
        "candidate_selected": False,
        "verification_runner_invoked": False,
        "repair_executed": False,
        "execution_authority_granted": False,
        "git_authority_granted": False,
    }


def summarize(candidates: list[Mapping[str, Any]]) -> tuple[dict[str, int], int, int]:
    counts = {classification: 0 for classification in CLASSIFICATIONS}
    total_findings = 0
    changed_paths: set[str] = set()
    for candidate in candidates:
        counts[candidate["classification"]] += 1
        total_findings += len(candidate["findings"])
        changed_paths.update(candidate["changed_paths"])
    return counts, total_findings, len(changed_paths)


def route_counts_named(counts: Mapping[str, int]) -> dict[str, int]:
    return {
        "admissible": counts[DISPOSITION_ADMISSIBLE],
        "repairable": counts[DISPOSITION_REPAIRABLE],
        "hold": counts[DISPOSITION_HOLD],
        "rejected": counts[DISPOSITION_REJECTED],
    }
