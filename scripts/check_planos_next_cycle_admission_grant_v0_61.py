#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from scripts.check_planos_next_cycle_admission_request_v0_60 import _ready_blocker_release_closeout
from runtime.kuuos_planos_next_cycle_admission_request_v0_60 import build_next_cycle_admission_request
from runtime.kuuos_planos_next_cycle_admission_grant_v0_61 import (
    SOURCE_VERSION,
    VERSION,
    build_next_cycle_admission_grant,
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


def _ready_next_cycle_admission_request() -> dict:
    source = _ready_blocker_release_closeout()
    return build_next_cycle_admission_request(blocker_release_closeout=source).to_dict()


def _exercise_runtime() -> None:
    source = _ready_next_cycle_admission_request()
    require(source["version"] == SOURCE_VERSION, "source version mismatch")
    receipt = build_next_cycle_admission_grant(next_cycle_admission_request=source).to_dict()
    require(receipt["version"] == VERSION, "runtime version mismatch")
    require(
        receipt["status"] == "PLANOS_NEXT_CYCLE_ADMISSION_GRANT_READY",
        f"grant blocked: {receipt.get('blockers')}",
    )
    require(receipt["selected_candidate_id"] == "repair-route", "selected id mismatch")
    boundary = receipt["boundary"]
    require(boundary["grant_owned_by_plan_os"] is True, "grant owner missing")
    require(
        boundary["source_next_cycle_admission_request_preserved"] is True,
        "source request not preserved",
    )
    require(
        boundary["selected_candidate_bound_to_next_cycle_admission_request"] is True,
        "selected candidate not bound to request",
    )
    require(boundary["memory_overwrite_preserved"] is True, "memory overwrite not preserved")
    require(boundary["memory_overwrite_closeout_preserved"] is True, "memory closeout not preserved")
    require(boundary["cycle_closed_preserved"] is True, "memory cycle closeout not preserved")
    require(boundary["truth_authority_preserved"] is True, "truth authority not preserved")
    require(
        boundary["truth_authority_cycle_closed_preserved"] is True,
        "truth authority cycle closeout not preserved",
    )
    require(boundary["blocker_release_preserved"] is True, "blocker release not preserved")
    require(
        boundary["blocker_release_cycle_closed_preserved"] is True,
        "blocker release closeout not preserved",
    )
    require(
        boundary["next_cycle_admission_request_preserved"] is True,
        "admission request not preserved",
    )
    require(boundary["next_cycle_admission_grant_only"] is True, "grant-only boundary missing")
    require(boundary["next_cycle_admission_requested"] is True, "admission request missing")
    require(boundary["next_cycle_admission_granted"] is True, "admission grant missing")
    require(boundary["next_cycle_started"] is False, "next cycle started early")

    record = receipt["next_cycle_admission_grant"]
    require(record["memory_overwrite_preserved"] is True, "grant lost memory overwrite")
    require(record["memory_overwrite_closeout_preserved"] is True, "grant lost memory closeout")
    require(record["truth_authority_preserved"] is True, "grant lost truth authority")
    require(record["truth_authority_cycle_closed_preserved"] is True, "grant lost truth closeout")
    require(record["blocker_release_preserved"] is True, "grant lost blocker release")
    require(
        record["blocker_release_cycle_closed_preserved"] is True,
        "grant lost blocker release closeout",
    )
    require(record["next_cycle_admission_requested"] is True, "grant lost admission request")
    require(record["next_cycle_admission_granted"] is True, "grant record did not grant admission")
    require(record["next_cycle_started"] is False, "grant record started next cycle")

    pre_granted = dict(source)
    pre_granted_boundary = dict(pre_granted["boundary"])
    pre_granted_boundary["next_cycle_admission_granted"] = True
    pre_granted["boundary"] = pre_granted_boundary
    blocked_granted = build_next_cycle_admission_grant(next_cycle_admission_request=pre_granted).to_dict()
    require(
        blocked_granted["status"] == "PLANOS_NEXT_CYCLE_ADMISSION_GRANT_BLOCKED",
        "pre-granted source not blocked",
    )
    require(
        "source_boundary_next_cycle_admission_granted_promoted" in blocked_granted["blockers"],
        "pre-grant boundary blocker missing",
    )

    record_granted = dict(source)
    granted_record = dict(record_granted["next_cycle_admission_request"])
    granted_record["next_cycle_admission_granted"] = True
    record_granted["next_cycle_admission_request"] = granted_record
    blocked_record_grant = build_next_cycle_admission_grant(
        next_cycle_admission_request=record_granted
    ).to_dict()
    require(
        blocked_record_grant["status"] == "PLANOS_NEXT_CYCLE_ADMISSION_GRANT_BLOCKED",
        "pre-granted source record not blocked",
    )
    require(
        "source_record_next_cycle_admission_granted_promoted" in blocked_record_grant["blockers"],
        "pre-grant record blocker missing",
    )

    record_started = dict(source)
    started_record = dict(record_started["next_cycle_admission_request"])
    started_record["next_cycle_started"] = True
    record_started["next_cycle_admission_request"] = started_record
    blocked_started = build_next_cycle_admission_grant(next_cycle_admission_request=record_started).to_dict()
    require(
        blocked_started["status"] == "PLANOS_NEXT_CYCLE_ADMISSION_GRANT_BLOCKED",
        "pre-started source record not blocked",
    )
    require(
        "source_record_next_cycle_started_promoted" in blocked_started["blockers"],
        "pre-start record blocker missing",
    )

    mismatch = dict(source)
    mismatch_record = dict(mismatch["next_cycle_admission_request"])
    mismatch_record["selected_candidate_digest"] = "wrong-digest"
    mismatch["next_cycle_admission_request"] = mismatch_record
    blocked_mismatch = build_next_cycle_admission_grant(next_cycle_admission_request=mismatch).to_dict()
    require(
        blocked_mismatch["status"] == "PLANOS_NEXT_CYCLE_ADMISSION_GRANT_BLOCKED",
        "mismatch not blocked",
    )
    require(
        "selected_candidate_digest_next_cycle_admission_request_mismatch" in blocked_mismatch["blockers"],
        "digest mismatch blocker missing",
    )


def main() -> int:
    runtime = ROOT / "runtime/kuuos_planos_next_cycle_admission_grant_v0_61.py"
    formal = ROOT / "formal/KUOS/PlanOS/NextCycleAdmissionGrantV0_61.lean"
    formal_root = ROOT / "formal/KuuOSPlanOSV0_61.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_NEXT_CYCLE_ADMISSION_GRANT_v0_61.md"
    manifest_path = ROOT / "manifests/kuuos_planos_next_cycle_admission_grant_v0_61.json"

    for path in (runtime, formal, formal_root, aggregate_root, docs, manifest_path):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(runtime, (
        "build_next_cycle_admission_grant",
        "PLANOS_NEXT_CYCLE_ADMISSION_GRANT_READY",
        "next_cycle_admission_grant_only",
        "next_cycle_admission_requested",
        "next_cycle_admission_granted",
        "next_cycle_started",
    ))
    require_tokens(formal, (
        "NextCycleAdmissionGrantSurface",
        "NextCycleAdmissionGrantBoundary",
        "PlanOSNextCycleAdmissionGrantBridge",
        "source_request_requests_admission_but_does_not_grant_or_start",
        "grant_binds_candidate_and_preserves_closed_prior_cycle",
        "grant_authorizes_admission_without_starting_next_cycle",
        "boundary_is_next_cycle_admission_grant_only",
        "history_appends_one_next_cycle_admission_grant",
        "digest_is_exact",
    ))
    require_tokens(formal_root, ("KUOS.PlanOS.NextCycleAdmissionGrantV0_61",))
    require_tokens(aggregate_root, ("KUOS.PlanOS.NextCycleAdmissionGrantV0_61",))
    require_tokens(docs, (
        "PlanOS Next-Cycle Admission Grant v0.61",
        "next cycle admission grant only = true",
        "next cycle admission requested = true",
        "next cycle admission granted = true",
        "next cycle started = false",
    ))
    require_tokens(ROOT / "scripts/run_plan_os_full_checks.py", (
        "check_planos_next_cycle_admission_grant_v0_61.py",
        "v0.1-v0.61",
    ))
    require_tokens(ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py", ("check_planos_v061",))

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
    print("PlanOS next-cycle admission grant v0.61 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
