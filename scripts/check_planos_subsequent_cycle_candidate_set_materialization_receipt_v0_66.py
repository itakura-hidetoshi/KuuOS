#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from scripts.check_planos_subsequent_cycle_candidate_generation_start_receipt_v0_65 import (
    _ready_subsequent_cycle_replan_request,
)
from runtime.kuuos_planos_subsequent_cycle_candidate_generation_start_receipt_v0_65 import (
    build_subsequent_cycle_candidate_generation_start_receipt,
)
from runtime.kuuos_planos_subsequent_cycle_candidate_set_materialization_receipt_v0_66 import (
    MAX_CANDIDATES,
    SOURCE_VERSION,
    VERSION,
    build_subsequent_cycle_candidate_set_materialization_receipt,
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


def _ready_candidate_generation_start_receipt() -> dict:
    source = _ready_subsequent_cycle_replan_request()
    return build_subsequent_cycle_candidate_generation_start_receipt(
        subsequent_cycle_replan_request=source
    ).to_dict()


def _candidate_specs() -> list[dict[str, str]]:
    return [
        {
            "candidate_id": "repair-route::continuity",
            "objective": "preserve the verified repair route with bounded continuity",
            "constraint_digest": "constraint-continuity-v1",
        },
        {
            "candidate_id": "repair-route::refinement",
            "objective": "refine the repair route under the closed authority chain",
            "constraint_digest": "constraint-refinement-v1",
        },
        {
            "candidate_id": "repair-route::recovery",
            "objective": "retain a rollback-safe recovery alternative",
            "constraint_digest": "constraint-recovery-v1",
        },
    ]


def _exercise_runtime() -> None:
    source = _ready_candidate_generation_start_receipt()
    require(source["version"] == SOURCE_VERSION, "source version mismatch")
    specs = _candidate_specs()
    receipt = build_subsequent_cycle_candidate_set_materialization_receipt(
        candidate_generation_start_receipt=source,
        candidate_specs=specs,
    ).to_dict()
    require(receipt["version"] == VERSION, "runtime version mismatch")
    require(
        receipt["status"]
        == "PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_SET_MATERIALIZATION_RECEIPT_READY",
        f"candidate-set materialization blocked: {receipt.get('blockers')}",
    )
    require(receipt["candidate_count"] == len(specs), "candidate count mismatch")
    require(receipt["candidate_set_digest"], "candidate-set digest missing")
    require(len(receipt["candidate_set"]) == len(specs), "candidate set length mismatch")

    candidate_ids = [candidate["candidate_id"] for candidate in receipt["candidate_set"]]
    candidate_digests = [candidate["candidate_digest"] for candidate in receipt["candidate_set"]]
    require(len(candidate_ids) == len(set(candidate_ids)), "candidate ids not unique")
    require(len(candidate_digests) == len(set(candidate_digests)), "candidate digests not unique")
    for ordinal, candidate in enumerate(receipt["candidate_set"]):
        require(candidate["ordinal"] == ordinal, "candidate ordinal mismatch")
        require(candidate["parent_candidate_id"] == "repair-route", "parent candidate id mismatch")
        require(candidate["parent_candidate_digest"] == source["selected_candidate_digest"], "parent digest mismatch")
        require(candidate["candidate_digest"], "candidate digest missing")

    boundary = receipt["boundary"]
    require(boundary["receipt_owned_by_plan_os"] is True, "receipt owner missing")
    require(boundary["source_candidate_generation_start_receipt_preserved"] is True, "source start not preserved")
    require(boundary["selected_candidate_provenance_bound_to_generation_start"] is True, "provenance not bound")
    require(boundary["memory_overwrite_preserved"] is True, "memory overwrite not preserved")
    require(boundary["truth_authority_preserved"] is True, "truth authority not preserved")
    require(boundary["blocker_release_preserved"] is True, "blocker release not preserved")
    require(boundary["next_cycle_cycle_closed"] is True, "prior cycle closeout not preserved")
    require(boundary["subsequent_cycle_replan_requested"] is True, "replan request not preserved")
    require(boundary["subsequent_cycle_candidate_generation_started"] is True, "generation start not preserved")
    require(
        boundary["subsequent_cycle_candidate_set_materialization_receipt_only"] is True,
        "materialization-only boundary missing",
    )
    require(boundary["subsequent_cycle_candidate_set_materialized"] is True, "candidate set not materialized")
    require(boundary["subsequent_cycle_candidate_set_nonempty"] is True, "nonempty boundary missing")
    require(boundary["subsequent_cycle_candidate_ids_unique"] is True, "unique-id boundary missing")
    require(boundary["subsequent_cycle_candidate_selected"] is False, "candidate selected early")
    require(boundary["subsequent_cycle_admission_requested"] is False, "admission requested early")

    record = receipt["subsequent_cycle_candidate_set_materialization_receipt"]
    require(record["candidate_count"] == len(specs), "record candidate count mismatch")
    require(record["candidate_set_digest"] == receipt["candidate_set_digest"], "record set digest mismatch")
    require(record["subsequent_cycle_candidate_set_materialized"] is True, "record did not materialize set")
    require(record["subsequent_cycle_candidate_selected"] is False, "record selected candidate")
    require(record["subsequent_cycle_admission_requested"] is False, "record requested admission")
    require(record["source_subsequent_cycle_replan_request_digest"], "replan digest missing")
    require(record["source_blocker_release_authorization_request_digest"], "authority chain missing")

    empty = build_subsequent_cycle_candidate_set_materialization_receipt(
        candidate_generation_start_receipt=source,
        candidate_specs=[],
    ).to_dict()
    require(empty["status"].endswith("BLOCKED"), "empty candidate set not blocked")
    require("candidate_specs_empty" in empty["blockers"], "empty candidate blocker missing")

    duplicate_specs = _candidate_specs()
    duplicate_specs[1] = dict(duplicate_specs[1])
    duplicate_specs[1]["candidate_id"] = duplicate_specs[0]["candidate_id"]
    duplicate = build_subsequent_cycle_candidate_set_materialization_receipt(
        candidate_generation_start_receipt=source,
        candidate_specs=duplicate_specs,
    ).to_dict()
    require(duplicate["status"].endswith("BLOCKED"), "duplicate ids not blocked")
    require("candidate_ids_not_unique" in duplicate["blockers"], "duplicate-id blocker missing")

    oversized_specs = [
        {
            "candidate_id": f"candidate-{index}",
            "objective": f"bounded objective {index}",
            "constraint_digest": f"constraint-{index}",
        }
        for index in range(MAX_CANDIDATES + 1)
    ]
    oversized = build_subsequent_cycle_candidate_set_materialization_receipt(
        candidate_generation_start_receipt=source,
        candidate_specs=oversized_specs,
    ).to_dict()
    require(oversized["status"].endswith("BLOCKED"), "oversized candidate set not blocked")
    require(
        "candidate_specs_exceed_bounded_limit" in oversized["blockers"],
        "bounded-limit blocker missing",
    )

    pre_materialized = dict(source)
    pre_boundary = dict(pre_materialized["boundary"])
    pre_boundary["subsequent_cycle_candidate_set_materialized"] = True
    pre_materialized["boundary"] = pre_boundary
    blocked_boundary = build_subsequent_cycle_candidate_set_materialization_receipt(
        candidate_generation_start_receipt=pre_materialized,
        candidate_specs=specs,
    ).to_dict()
    require(blocked_boundary["status"].endswith("BLOCKED"), "pre-materialized boundary not blocked")
    require(
        "source_boundary_subsequent_cycle_candidate_set_materialized_promoted"
        in blocked_boundary["blockers"],
        "pre-materialized boundary blocker missing",
    )

    mismatch = dict(source)
    mismatch_record = dict(mismatch["subsequent_cycle_candidate_generation_start_receipt"])
    mismatch_record["selected_candidate_digest"] = "wrong-digest"
    mismatch["subsequent_cycle_candidate_generation_start_receipt"] = mismatch_record
    blocked_mismatch = build_subsequent_cycle_candidate_set_materialization_receipt(
        candidate_generation_start_receipt=mismatch,
        candidate_specs=specs,
    ).to_dict()
    require(blocked_mismatch["status"].endswith("BLOCKED"), "provenance mismatch not blocked")
    require(
        "selected_candidate_digest_generation_start_mismatch" in blocked_mismatch["blockers"],
        "provenance mismatch blocker missing",
    )


def main() -> int:
    runtime = ROOT / "runtime/kuuos_planos_subsequent_cycle_candidate_set_materialization_receipt_v0_66.py"
    formal = ROOT / "formal/KUOS/PlanOS/SubsequentCycleCandidateSetMaterializationReceiptV0_66.lean"
    formal_root = ROOT / "formal/KuuOSPlanOSV0_66.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_SET_MATERIALIZATION_RECEIPT_v0_66.md"
    manifest_path = ROOT / "manifests/kuuos_planos_subsequent_cycle_candidate_set_materialization_receipt_v0_66.json"

    for path in (runtime, formal, formal_root, aggregate_root, docs, manifest_path):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(runtime, (
        "build_subsequent_cycle_candidate_set_materialization_receipt",
        "PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_SET_MATERIALIZATION_RECEIPT_READY",
        "MaterializedCandidate",
        "candidate_set_digest",
        "candidate_ids_not_unique",
        "candidate_specs_exceed_bounded_limit",
    ))
    require_tokens(formal, (
        "SubsequentCycleCandidateSetMaterializationReceiptSurface",
        "SubsequentCycleCandidateSetMaterializationReceiptBoundary",
        "PlanOSSubsequentCycleCandidateSetMaterializationReceiptBridge",
        "source_start_records_generation_without_materialized_set",
        "candidate_set_is_nonempty_exact_and_digest_bound",
        "receipt_materializes_candidate_set_without_selection_or_admission",
        "boundary_is_candidate_set_materialization_receipt_only",
        "history_appends_one_candidate_set_materialization_receipt",
        "digest_is_exact",
    ))
    require_tokens(formal_root, ("KUOS.PlanOS.SubsequentCycleCandidateSetMaterializationReceiptV0_66",))
    require_tokens(aggregate_root, ("KUOS.PlanOS.SubsequentCycleCandidateSetMaterializationReceiptV0_66",))
    require_tokens(docs, (
        "PlanOS Subsequent-Cycle Candidate-Set Materialization Receipt v0.66",
        "candidate count equals candidate input count",
        "subsequent-cycle candidate selected = false",
        "subsequent-cycle admission requested = false",
    ))
    require_tokens(ROOT / "scripts/run_plan_os_full_checks.py", (
        "check_planos_subsequent_cycle_candidate_set_materialization_receipt_v0_66.py",
        "v0.1-v0.66",
    ))
    require_tokens(ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py", ("check_planos_v066",))

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest["version"] == MANIFEST_VERSION, "manifest version mismatch")
    require(manifest["runtime"] == str(runtime.relative_to(ROOT)), "runtime mismatch")
    require(manifest["formal_module"] == str(formal.relative_to(ROOT)), "formal mismatch")
    require(manifest["documentation"] == str(docs.relative_to(ROOT)), "docs mismatch")
    require(manifest["source_version"] == SOURCE_VERSION, "source version mismatch")
    require(manifest["bounded_candidate_limit"] == MAX_CANDIDATES, "bounded limit mismatch")
    require(manifest["history_delta"] == 1, "history delta mismatch")
    for section in ("inputs", "outputs", "required"):
        for field, value in manifest[section].items():
            require(value is True, f"{section} field missing: {field}")
    for field, value in manifest["closed"].items():
        require(value is False, f"closed boundary promoted: {field}")

    _exercise_runtime()
    print("PlanOS subsequent-cycle candidate-set materialization receipt v0.66 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
