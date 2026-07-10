#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from scripts.check_planos_external_commit_authorization_grant_v0_45 import _ready_external_commit_request
from runtime.kuuos_planos_external_commit_authorization_grant_v0_45 import build_external_commit_authorization_grant
from runtime.kuuos_planos_external_commit_receipt_v0_46 import SOURCE_VERSION, VERSION, build_external_commit_receipt

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_VERSION = "kuuos_planos_external_commit_receipt_v0_46"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def _ready_external_commit_grant() -> dict:
    source = _ready_external_commit_request()
    return build_external_commit_authorization_grant(external_commit_request=source).to_dict()


def _exercise_runtime() -> None:
    source = _ready_external_commit_grant()
    require(source["version"] == SOURCE_VERSION, "source external commit grant version mismatch")
    require("external_commit_authorization_grant" in source, "source external commit grant missing")
    receipt = build_external_commit_receipt(external_commit_grant=source).to_dict()
    require(receipt["version"] == VERSION, "runtime version mismatch")
    require(receipt["status"] == "PLANOS_EXTERNAL_COMMIT_RECEIPT_READY", f"receipt status mismatch: {receipt.get('blockers')}")
    require(receipt["selected_candidate_id"] == "repair-route", "selected id mismatch")
    require(receipt["boundary"]["external_commit_receipt_only"] is True, "receipt-only boundary missing")
    require(receipt["boundary"]["external_commit_authorization_granted"] is True, "external commit authorization grant not preserved")
    require(receipt["boundary"]["external_commit_granted"] is True, "external commit not recorded")
    require(receipt["boundary"]["memory_overwrite_granted"] is False, "memory overwrite promoted")
    require(receipt["boundary"]["truth_authority_granted"] is False, "truth authority promoted")
    require(receipt["boundary"]["blocker_release_granted"] is False, "blocker release promoted")
    require(receipt["external_commit_receipt"]["external_commit_granted"] is True, "receipt record missing external commit")
    require(receipt["external_commit_receipt"]["memory_overwrite_ready"] is False, "receipt leaked memory readiness")

    promoted = dict(source)
    boundary = dict(promoted["boundary"])
    boundary["external_commit_granted"] = True
    promoted["boundary"] = boundary
    blocked = build_external_commit_receipt(external_commit_grant=promoted).to_dict()
    require(blocked["status"] == "PLANOS_EXTERNAL_COMMIT_RECEIPT_BLOCKED", "pre-committed source not blocked")
    require("source_boundary_external_commit_granted_promoted" in blocked["blockers"], "pre-commit blocker missing")

    memory_promoted = dict(source)
    boundary2 = dict(memory_promoted["boundary"])
    boundary2["memory_overwrite_granted"] = True
    memory_promoted["boundary"] = boundary2
    blocked_memory = build_external_commit_receipt(external_commit_grant=memory_promoted).to_dict()
    require(blocked_memory["status"] == "PLANOS_EXTERNAL_COMMIT_RECEIPT_BLOCKED", "memory-promoted source not blocked")
    require("source_boundary_memory_overwrite_granted_promoted" in blocked_memory["blockers"], "memory promotion blocker missing")

    mismatch = dict(source)
    record = dict(mismatch["external_commit_authorization_grant"])
    record["selected_candidate_digest"] = "wrong-digest"
    mismatch["external_commit_authorization_grant"] = record
    blocked_record = build_external_commit_receipt(external_commit_grant=mismatch).to_dict()
    require(blocked_record["status"] == "PLANOS_EXTERNAL_COMMIT_RECEIPT_BLOCKED", "record mismatch not blocked")
    require("selected_candidate_digest_external_commit_grant_mismatch" in blocked_record["blockers"], "record mismatch blocker missing")


def main() -> int:
    runtime = ROOT / "runtime/kuuos_planos_external_commit_receipt_v0_46.py"
    source_runtime = ROOT / "runtime/kuuos_planos_external_commit_authorization_grant_v0_45.py"
    formal = ROOT / "formal/KUOS/PlanOS/ExternalCommitReceiptV0_46.lean"
    source_formal = ROOT / "formal/KUOS/PlanOS/ExternalCommitAuthorizationGrantV0_45.lean"
    formal_root = ROOT / "formal/KuuOSPlanOSV0_46.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_EXTERNAL_COMMIT_RECEIPT_v0_46.md"
    manifest_path = ROOT / "manifests/kuuos_planos_external_commit_receipt_v0_46.json"

    for path in (runtime, source_runtime, formal, source_formal, formal_root, aggregate_root, docs, manifest_path):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(runtime, ("build_external_commit_receipt", "PLANOS_EXTERNAL_COMMIT_RECEIPT_READY", "PLANOS_EXTERNAL_COMMIT_RECEIPT_BLOCKED", "external_commit_receipt", "external_commit_receipt_only", "external_commit_authorization_granted", "external_commit_granted", "memory_overwrite_granted"))
    require_tokens(formal, ("ExternalCommitReceiptSurface", "ExternalCommitReceiptBoundary", "PlanOSExternalCommitReceiptBridge", "source_grant_authorizes_but_does_not_commit_memory_truth_or_blocker_release", "receipt_binds_candidate_and_preserves_execution_state", "receipt_records_external_commit_but_not_memory_truth_or_blocker_release", "boundary_preserves_external_commit_receipt_only", "history_appends_one_external_commit_receipt_record", "digest_is_exact"))
    require_tokens(source_formal, ("PlanOSExternalCommitAuthorizationGrantBridge", "grant_authorizes_external_commit_but_does_not_commit_memory_truth_or_blocker_release"))
    require_tokens(formal_root, ("KUOS.PlanOS.ExternalCommitReceiptV0_46",))
    require_tokens(aggregate_root, ("KUOS.PlanOS.ExternalCommitReceiptV0_46",))
    require_tokens(docs, ("PlanOS External Commit Receipt v0.46", "external commit receipt only = true", "external commit authorization granted = true", "external commit granted = true", "memory overwrite granted = false", "truth authority granted = false"))
    require_tokens(ROOT / "scripts/run_plan_os_full_checks.py", ("check_planos_external_commit_receipt_v0_46.py", "v0.1-v0.46"))
    require_tokens(ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py", ("check_planos_v046",))

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest["version"] == MANIFEST_VERSION, "manifest version mismatch")
    require(manifest["runtime"] == str(runtime.relative_to(ROOT)), "runtime mismatch")
    require(manifest["formal_module"] == str(formal.relative_to(ROOT)), "formal mismatch")
    require(manifest["documentation"] == str(docs.relative_to(ROOT)), "docs mismatch")
    require(manifest["source_version"] == SOURCE_VERSION, "source version mismatch")
    require(manifest["history_delta"] == 1, "history delta mismatch")
    for field, value in manifest["inputs"].items():
        require(value is True, f"input missing: {field}")
    for field, value in manifest["outputs"].items():
        require(value is True, f"output missing: {field}")
    for field, value in manifest["required"].items():
        require(value is True, f"required boundary missing: {field}")
    for field, value in manifest["closed"].items():
        require(value is False, f"closed boundary promoted: {field}")

    _exercise_runtime()
    print("PlanOS external commit receipt v0.46 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
