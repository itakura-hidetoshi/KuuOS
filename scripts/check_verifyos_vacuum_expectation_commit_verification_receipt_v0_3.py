#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "kuuos_verifyos_vacuum_expectation_commit_verification_receipt_v0_3"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def main() -> int:
    formal_root = ROOT / "formal/KuuOSVerifyOSV0_3.lean"
    top_root = ROOT / "formal/KuuOSFormal.lean"
    formal = ROOT / "formal/KUOS/VerifyOS/VacuumExpectationCommitVerificationReceiptV0_3.lean"
    observe = ROOT / "formal/KUOS/ObserveOS/VacuumExpectationIntakeCommitReceiptV0_3.lean"
    docs = ROOT / "docs/KUUOS_VERIFYOS_VACUUM_EXPECTATION_COMMIT_VERIFICATION_RECEIPT_v0_3.md"
    manifest_path = ROOT / "manifests/kuuos_verifyos_vacuum_expectation_commit_verification_receipt_v0_3.json"
    workflow = ROOT / ".github/workflows/verifyos-vacuum-expectation-commit-verification-v0-3.yml"

    for path in (formal_root, top_root, formal, observe, docs, manifest_path, workflow):
        require(path.is_file(), f"missing file: {path}")

    import_token = "KUOS.VerifyOS.VacuumExpectationCommitVerificationReceiptV0_3"
    require_tokens(formal_root, (import_token,))
    require_tokens(top_root, (import_token,))
    require_tokens(
        formal,
        (
            "VacuumExpectationCommitVerificationBridge",
            "VacuumExpectationCommitVerificationReceipt",
            "verification_requires_explicit_observe_commit",
            "verification_receipt_digest_is_exact",
            "verification_index_appends_exactly_once",
            "verification_verdict_and_record_are_exact",
            "passed_receipt_discharges_verification_debt",
            "failed_receipt_requires_corrective_action",
            "indeterminate_receipt_preserves_verification_debt",
            "verification_never_becomes_truth_or_causality",
            "verification_bridge_grants_no_downstream_authority",
            "verified_candidate_value_remains_exact",
        ),
    )
    require_tokens(
        observe,
        (
            "observationRecordCommitted",
            "verifyOSHandoffRequired",
            "commit_preserves_verification_debt",
        ),
    )
    require_tokens(
        ROOT / "formal/KUOS/VerifyOS/EvidenceBoundVerificationV0_1.lean",
        (
            "CriterionBinding",
            "ChallengeRequirements",
            "CorroborationSurface",
            "AdjudicationBoundary",
            "VerificationDebtSemantics",
            "VerifyEventIndex",
        ),
    )
    require_tokens(
        docs,
        (
            "verification != truth",
            "verification != causal attribution",
            "verification receipt != automatic learning",
            "verification receipt != PlanOS activation",
        ),
    )
    require_tokens(
        ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py",
        ("check_verifyos_v03",),
    )

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest["version"] == VERSION, "manifest version mismatch")
    require(manifest["formal_module"] == str(formal.relative_to(ROOT)), "formal module mismatch")
    require(manifest["documentation"] == str(docs.relative_to(ROOT)), "documentation mismatch")
    require(manifest["workflow"] == str(workflow.relative_to(ROOT)), "workflow mismatch")

    boundaries = manifest["boundaries"]
    for field in (
        "source_observe_commit_required",
        "verification_receipt_required",
        "verification_index_append_once",
        "verifyos_owns_adjudication",
    ):
        require(boundaries[field] is True, f"required boundary missing: {field}")
    for field in (
        "verification_is_truth",
        "causal_authority_granted",
        "world_sidecar_owns_verification",
        "observeos_performs_verification",
        "bridge_runtime_performs_verification",
        "automatic_learning",
        "automatic_plan_activation",
        "automatic_execution",
        "automatic_memory_overwrite",
        "automatic_world_update",
    ):
        require(boundaries[field] is False, f"forbidden promotion: {field}")

    print("VerifyOS vacuum expectation commit verification receipt v0.3 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
