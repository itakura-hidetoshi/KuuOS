#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from scripts.check_planos_blocker_release_closeout_receipt_v0_59 import _ready_blocker_release_receipt
from runtime.kuuos_planos_blocker_release_closeout_receipt_v0_59 import (
    build_blocker_release_closeout_receipt,
)
from runtime.kuuos_planos_next_cycle_admission_request_v0_60 import (
    SOURCE_VERSION,
    VERSION,
    build_next_cycle_admission_request,
)

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_VERSION = VERSION


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def _ready_blocker_release_closeout() -> dict:
    source = _ready_blocker_release_receipt()
    return build_blocker_release_closeout_receipt(blocker_release_receipt=source).to_dict()


def _exercise_runtime() -> None:
    source = _ready_blocker_release_closeout()
    require(source["version"] == SOURCE_VERSION, "source version mismatch")
    receipt = build_next_cycle_admission_request(blocker_release_closeout=source).to_dict()
    require(receipt["version"] == VERSION, "runtime version mismatch")
    require(
        receipt["status"] == "PLANOS_NEXT_CYCLE_ADMISSION_REQUEST_READY",
        f"request blocked: {receipt.get('blockers')}",
    )
    require(receipt["selected_candidate_id"] == "repair-route", "selected id mismatch")
    boundary = receipt["boundary"]
    require(boundary["request_owned_by_plan_os"] is True, "request owner missing")
    require(
        boundary["source_blocker_release_closeout_preserved"] is True,
        "source closeout not preserved",
    )
    require(
        boundary["selected_candidate_bound_to_blocker_release_closeout"] is True,
        "selected candidate not bound to closeout",
    )
    require(boundary["memory_overwrite_preserved"] is True, "memory overwrite not preserved")
    require(boundary["memory_overwrite_closeout_preserved"] is True, "memory closeout not preserved")
    require(boundary["cycle_closed_preserved"] is True, "memory cycle closeout not preserved")
    require(boundary["truth_authority_preserved"] is True, "truth authority not preserved")
    require(
        boundary["truth_authority_cycle_closed_preserved"] is True,
        "truth authority cycle closeout not preserved",
    )
    require(
        boundary["blocker_release_authorization_request_preserved"] is True,
        "blocker release request not preserved",
    )
    require(
        boundary["blocker_release_authorization_grant_preserved"] is True,
        "blocker release grant not preserved",
    )
    require(boundary["blocker_release_preserved"] is True, "blocker release not preserved")
    require(
        boundary["blocker_release_cycle_closed_preserved"] is True,
        "blocker release closeout not preserved",
    )
    require(boundary["next_cycle_admission_request_only"] is True, "request-only boundary missing")
    require(boundary["next_cycle_admission_requested"] is True, "admission request missing")
    require(boundary["next_cycle_admission_granted"] is False, "admission granted early")
    require(boundary["next_cycle_started"] is False, "next cycle started early")

    record = receipt["next_cycle_admission_request"]
    require(record["memory_overwrite_preserved"] is True, "request lost memory overwrite")
    require(record["memory_overwrite_closeout_preserved"] is True, "request lost memory closeout")
    require(record["truth_authority_preserved"] is True, "request lost truth authority")
    require(record["truth_authority_cycle_closed_preserved"] is True, "request lost truth closeout")
    require(record["blocker_release_preserved"] is True, "request lost blocker release")
    require(
        record["blocker_release_cycle_closed_preserved"] is True,
        "request lost blocker release closeout",
    )
    require(record["next_cycle_admission_requested"] is True, "request record missing request")
    require(record["next_cycle_admission_granted"] is False, "request record granted admission")
    require(record["next_cycle_started"] is False, "request record started next cycle")

    pre_requested = dict(source)
    pre_requested_boundary = dict(pre_requested["boundary"])
    pre_requested_boundary["next_cycle_admission_requested"] = True
    pre_requested["boundary"] = pre_requested_boundary
    blocked_requested = build_next_cycle_admission_request(blocker_release_closeout=pre_requested).to_dict()
    require(
        blocked_requested["status"] == "PLANOS_NEXT_CYCLE_ADMISSION_REQUEST_BLOCKED",
        "pre-requested source not blocked",
    )
    require(
        "source_boundary_next_cycle_admission_requested_promoted" in blocked_requested["blockers"],
        "pre-request blocker missing",
    )

    ready_promoted = dict(source)
    source_record = dict(ready_promoted["blocker_release_closeout_receipt"])
    source_record["next_cycle_admission_ready"] = True
    ready_promoted["blocker_release_closeout_receipt"] = source_record
    blocked_ready = build_next_cycle_admission_request(blocker_release_closeout=ready_promoted).to_dict()
    require(
        blocked_ready["status"] == "PLANOS_NEXT_CYCLE_ADMISSION_REQUEST_BLOCKED",
        "pre-ready source record not blocked",
    )
    require(
        "source_record_next_cycle_admission_ready_promoted" in blocked_ready["blockers"],
        "pre-ready blocker missing",
    )

    mismatch = dict(source)
    mismatch_record = dict(mismatch["blocker_release_closeout_receipt"])
    mismatch_record["selected_candidate_digest"] = "wrong-digest"
    mismatch["blocker_release_closeout_receipt"] = mismatch_record
    blocked_mismatch = build_next_cycle_admission_request(blocker_release_closeout=mismatch).to_dict()
    require(
        blocked_mismatch["status"] == "PLANOS_NEXT_CYCLE_ADMISSION_REQUEST_BLOCKED",
        "mismatch not blocked",
    )
    require(
        "selected_candidate_digest_blocker_release_closeout_mismatch" in blocked_mismatch["blockers"],
        "digest mismatch blocker missing",
    )


def main() -> int:
    runtime = ROOT / "runtime/kuuos_planos_next_cycle_admission_request_v0_60.py"
    formal = ROOT / "formal/KUOS/PlanOS/NextCycleAdmissionRequestV0_60.lean"
    formal_root = ROOT / "formal/KuuOSPlanOSV0_60.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_NEXT_CYCLE_ADMISSION_REQUEST_v0_60.md"
    manifest_path = ROOT / "manifests/kuuos_planos_next_cycle_admission_request_v0_60.json"

    for path in (runtime, formal, formal_root, aggregate_root, docs, manifest_path):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(runtime, (
        "build_next_cycle_admission_request",
        "PLANOS_NEXT_CYCLE_ADMISSION_REQUEST_READY",
        "next_cycle_admission_request_only",
        "next_cycle_admission_requested",
        "next_cycle_admission_granted",
        "next_cycle_started",
    ))
    require_tokens(formal, (
        "NextCycleAdmissionRequestSurface",
        "NextCycleAdmissionRequestBoundary",
        "PlanOSNextCycleAdmissionRequestBridge",
        "source_closeout_closes_release_cycle_but_does_not_request_admission",
        "request_binds_candidate_and_preserves_closed_prior_cycle",
        "request_opens_admission_request_but_not_grant_or_start",
        "boundary_is_next_cycle_admission_request_only",
        "history_appends_one_next_cycle_admission_request",
        "digest_is_exact",
    ))
    require_tokens(formal_root, ("KUOS.PlanOS.NextCycleAdmissionRequestV0_60",))
    require_tokens(aggregate_root, ("KUOS.PlanOS.NextCycleAdmissionRequestV0_60",))
    require_tokens(docs, (
        "PlanOS Next-Cycle Admission Request v0.60",
        "next cycle admission request only = true",
        "next cycle admission requested = true",
        "next cycle admission granted = false",
        "next cycle started = false",
    ))
    require_tokens(ROOT / "scripts/run_plan_os_full_checks.py", (
        "check_planos_next_cycle_admission_request_v0_60.py",
        "v0.1-v0.60",
    ))
    require_tokens(ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py", ("check_planos_v060",))

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest["version"] == MANIFEST_VERSION, "manifest version mismatch")
    require(manifest["runtime"] == str(runtime.relative_to(ROOT)), "runtime mismatch")
    require(manifest["formal_module"] == str(formal.relative_to(ROOT)), "formal mismatch")
    require(manifest["documentation"] == str(docs.relative_to(ROOT)), "docs mismatch")
    require(manifest["source_version"] == SOURCE_VERSION, "source version mismatch")
    require(manifest["history_delta"] == 1, "history delta mismatch")
    for section in ("inputs", "outputs", "required"):
        for field, value in manifest[section].items():
            require(value is True, f"{section} field missing: {field}")
    for field, value in manifest["closed"].items():
        require(value is False, f"closed boundary promoted: {field}")

    _exercise_runtime()
    print("PlanOS next-cycle admission request v0.60 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
