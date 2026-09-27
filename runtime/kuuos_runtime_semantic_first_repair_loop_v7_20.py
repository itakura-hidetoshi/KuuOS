#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import re
import time
from typing import Any, Mapping

from runtime.kuuos_codeai_candidate_patch_envelope_v0_1 import (
    RECEIPT_DIGEST_FIELD as CANDIDATE_RECEIPT_DIGEST_FIELD,
    DISPOSITION_SUPPORTED as CANDIDATE_DISPOSITION_SUPPORTED,
    canonical_digest as candidate_canonical_digest,
)
from runtime.kuuos_codeai_candidate_static_admissibility_preflight_schema_v0_1 import (
    RECEIPT_DIGEST_FIELD as PREFLIGHT_RECEIPT_DIGEST_FIELD,
    DISPOSITION_ADMISSIBLE,
    DISPOSITION_REPAIRABLE,
    DISPOSITION_HOLD,
    DISPOSITION_REJECTED,
    MODE_PREFLIGHT_ONLY,
    canonical_digest as preflight_canonical_digest,
)

VERSION = "kuuos_runtime_semantic_first_repair_loop_v7_20"
PLAN_VERSION = "kuuos_semantic_first_repair_loop_plan_v7_20"
OBSERVATION_VERSION = "kuuos_semantic_first_repair_observation_v7_20"
FEDERATION_VERSION = "kuuos_runtime_development_mcp_federation_v7_19"

READY = "KUUOS_SEMANTIC_FIRST_REPAIR_LOOP_READY"
PARTIAL = "KUUOS_SEMANTIC_FIRST_REPAIR_LOOP_PARTIAL"
OBSTRUCTED = "KUUOS_SEMANTIC_FIRST_REPAIR_LOOP_OBSTRUCTED"
BLOCKED = "KUUOS_SEMANTIC_FIRST_REPAIR_LOOP_BLOCKED"

NO_REPAIR_NEEDED = "no_semantic_repair_needed"
WORKSPACE_REPAIR_REQUIRED = "workspace_binding_repair_required"
LEAN_REOBSERVE = "lean_semantic_reobservation_required"
CANDIDATE_GENERATION_READY = "repair_candidate_generation_ready"
CANDIDATE_STALE = "repair_candidate_stale_for_current_bytes"
CANDIDATE_PREFLIGHT_READY = "candidate_static_preflight_ready"
CANDIDATE_REPAIR_FEEDBACK = "candidate_repair_feedback_ready"
CANDIDATE_HOLD = "candidate_hold_preserved"
CANDIDATE_REJECTED = "candidate_rejected_preserved"
SHADOW_REOBSERVE = "candidate_shadow_semantic_reobservation_required"
CANDIDATE_REGRESSION = "candidate_semantic_regression"
CANDIDATE_NO_IMPROVEMENT = "candidate_no_semantic_improvement"
LOCAL_APPLICATION_CANDIDATE = "local_application_candidate"
GIT_DIFF_REVIEW_READY = "git_diff_review_ready"
REMOTE_RECONCILIATION_REQUIRED = "remote_revision_reconciliation_required"
REMOTE_SUBMISSION_CANDIDATE = "remote_submission_candidate"
LOCAL_GIT_ADMISSION_REQUIRED = "local_git_admission_required"
LINEAGE_OBSTRUCTION = "repair_lineage_obstruction"

SHA64 = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True)
class SemanticFirstRepairLoopResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    route: str
    target_path: str
    current_error_count: int | None
    candidate_error_count: int | None
    semantic_improvement: bool | None
    local_semantic_work_allowed: bool
    local_application_authority_granted: bool
    remote_mutation_authority_granted: bool
    output_path: str
    receipt_path: str
    audit_path: str
    output_written: bool
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sha(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


def _root(value: Any, blockers: list[str]) -> pathlib.Path:
    if not value:
        blockers.append("runtime_root_missing")
        return pathlib.Path(".").resolve()
    root = pathlib.Path(str(value)).expanduser().resolve()
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")
    return root


def _read_json(path: pathlib.Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def _write_json(path: pathlib.Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(
        json.dumps(dict(value), ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    os.replace(tmp, path)


def _append_jsonl(path: pathlib.Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(value), ensure_ascii=False, sort_keys=True) + "\n")


def _digest(
    value: Any,
    field: str,
    blockers: list[str],
    *,
    optional: bool = False,
) -> str:
    text = str(value or "").strip()
    if optional and not text:
        return ""
    if not SHA64.fullmatch(text):
        blockers.append(field + "_invalid")
    return text


def _nat(value: Any, field: str, blockers: list[str]) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        blockers.append(field + "_invalid")
        return None
    return value


def _validate_plan(plan: Mapping[str, Any], blockers: list[str]) -> None:
    if plan.get("version") != PLAN_VERSION:
        blockers.append("plan_version_invalid")
    required_false = (
        "semantic_improvement_grants_local_write_authority",
        "semantic_improvement_grants_remote_write_authority",
        "stale_diagnostic_may_apply_patch",
        "candidate_receipt_is_current_byte_binding",
        "static_preflight_is_correctness_proof",
        "candidate_rejection_erases_local_worktree",
        "remote_revision_mismatch_blocks_local_repair",
        "source_authority_transferred",
    )
    for key in required_false:
        if plan.get(key) is not False:
            blockers.append(key + "_must_be_false")
    required_true = (
        "candidate_patch_bound_to_before_digest",
        "lean_observation_bound_to_source_digest",
        "candidate_result_requires_fresh_shadow_semantics",
        "remote_submission_requires_git_diff_review",
        "remote_submission_requires_revision_alignment",
        "remote_submission_requires_separate_authority_after_this_layer",
        "dirty_worktree_may_continue_semantic_repair",
    )
    for key in required_true:
        if plan.get(key) is not True:
            blockers.append(key + "_must_be_true")


def _receipt_digest_ok(
    receipt: Mapping[str, Any],
    field: str,
    digest_fn,
) -> bool:
    return receipt.get(field) == digest_fn(
        {k: v for k, v in receipt.items() if k != field}
    )


def _validate_candidate_receipt(
    value: Any,
    issues: list[str],
) -> Mapping[str, Any] | None:
    if value in (None, {}):
        return None
    receipt = _m(value)
    if not receipt:
        issues.append("candidate_receipt_not_object")
        return None
    if not _receipt_digest_ok(
        receipt,
        CANDIDATE_RECEIPT_DIGEST_FIELD,
        candidate_canonical_digest,
    ):
        issues.append("candidate_receipt_digest_mismatch")
    if receipt.get("candidate_patch_ready") is not True:
        issues.append("candidate_patch_not_ready")
    if receipt.get("codeai_disposition") != CANDIDATE_DISPOSITION_SUPPORTED:
        issues.append("candidate_patch_disposition_invalid")
    if receipt.get("operating_mode") != "proposal_only":
        issues.append("candidate_patch_mode_invalid")
    if receipt.get("route_receipt_recorded") is not True:
        issues.append("candidate_patch_route_not_recorded")
    for field in (
        "execution_lease_issued",
        "repository_mutation_performed",
        "git_ref_changed",
        "branch_created",
        "commit_created",
        "push_performed",
        "pull_request_created",
        "merge_performed",
        "deployment_performed",
        "secret_access_performed",
        "selection_authority_granted",
        "execution_authority_granted",
        "merge_authority_granted",
        "deployment_authority_granted",
        "secret_access_authority_granted",
    ):
        if receipt.get(field) is not False:
            issues.append("candidate_receipt_required_false:" + field)
    return receipt


def _validate_preflight_receipt(
    value: Any,
    issues: list[str],
) -> Mapping[str, Any] | None:
    if value in (None, {}):
        return None
    receipt = _m(value)
    if not receipt:
        issues.append("preflight_receipt_not_object")
        return None
    if not _receipt_digest_ok(
        receipt,
        PREFLIGHT_RECEIPT_DIGEST_FIELD,
        preflight_canonical_digest,
    ):
        issues.append("preflight_receipt_digest_mismatch")
    if receipt.get("operating_mode") != MODE_PREFLIGHT_ONLY:
        issues.append("preflight_mode_invalid")
    if receipt.get("route_receipt_recorded") is not True:
        issues.append("preflight_route_not_recorded")
    if receipt.get("codeai_disposition") not in {
        DISPOSITION_ADMISSIBLE,
        DISPOSITION_REPAIRABLE,
        DISPOSITION_HOLD,
        DISPOSITION_REJECTED,
    }:
        issues.append("preflight_disposition_invalid")
    for field in (
        "repository_mutation_performed",
        "git_effect_performed",
        "candidate_selected",
        "candidate_selection_authority_granted",
        "execution_authority_granted",
        "merge_authority_granted",
        "deployment_authority_granted",
        "static_preflight_treated_as_correctness_proof",
    ):
        if receipt.get(field) is not False:
            issues.append("preflight_receipt_required_false:" + field)
    return receipt


def _semantic_record(
    value: Any,
    prefix: str,
    blockers: list[str],
    *,
    optional: bool = False,
) -> dict[str, Any] | None:
    if optional and value in (None, {}):
        return None
    record = _m(value)
    if not record:
        blockers.append(prefix + "_not_object")
        return None
    source_digest = _digest(
        record.get("source_content_digest"),
        prefix + "_source_content_digest",
        blockers,
    )
    diagnostics_digest = _digest(
        record.get("diagnostics_digest"),
        prefix + "_diagnostics_digest",
        blockers,
    )
    error_count = _nat(
        record.get("error_count"),
        prefix + "_error_count",
        blockers,
    )
    warning_count = _nat(
        record.get("warning_count"),
        prefix + "_warning_count",
        blockers,
    )
    goal_digest = _digest(
        record.get("goal_digest"),
        prefix + "_goal_digest",
        blockers,
        optional=True,
    )
    observation_digest = _digest(
        record.get("semantic_observation_digest"),
        prefix + "_semantic_observation_digest",
        blockers,
    )
    return {
        "source_content_digest": source_digest,
        "diagnostics_digest": diagnostics_digest,
        "error_count": error_count,
        "warning_count": warning_count,
        "goal_digest": goal_digest,
        "semantic_observation_digest": observation_digest,
    }


def _federation_workspace(
    federation: Mapping[str, Any],
    blockers: list[str],
) -> Mapping[str, Any]:
    if federation.get("version") != FEDERATION_VERSION:
        blockers.append("federation_version_invalid")
    workspace = _m(federation.get("workspace"))
    if not workspace:
        blockers.append("federation_workspace_missing")
        return {}
    return workspace


def _classify(
    *,
    federation: Mapping[str, Any],
    observation: Mapping[str, Any],
    blockers: list[str],
) -> dict[str, Any]:
    if observation.get("version") != OBSERVATION_VERSION:
        blockers.append("repair_observation_version_invalid")

    workspace = _federation_workspace(federation, blockers)
    target_path = str(observation.get("target_path", "")).strip()
    if not target_path:
        blockers.append("target_path_missing")
    if target_path and str(workspace.get("target_path", "")) != target_path:
        blockers.append("federation_target_path_mismatch")

    current_digest = _digest(
        observation.get("current_content_digest"),
        "current_content_digest",
        blockers,
    )
    if current_digest and str(workspace.get("filesystem_content_digest", "")) != current_digest:
        blockers.append("current_content_federation_digest_mismatch")

    current_semantics = _semantic_record(
        observation.get("current_semantics"),
        "current_semantics",
        blockers,
    )

    local_semantic_allowed = workspace.get("local_semantic_work_allowed") is True
    remote_aligned = workspace.get("remote_local_aligned") is True

    route = WORKSPACE_REPAIR_REQUIRED
    status = PARTIAL
    candidate_error_count: int | None = None
    improvement: bool | None = None
    lineage_issues: list[str] = []
    reasons: list[str] = []

    if not local_semantic_allowed:
        route = WORKSPACE_REPAIR_REQUIRED
        reasons.append("federation_disallows_local_semantic_work")
    elif current_semantics is None:
        route = LEAN_REOBSERVE
        reasons.append("current_semantics_missing")
    elif current_semantics["source_content_digest"] != current_digest:
        route = LEAN_REOBSERVE
        reasons.append("current_lean_observation_stale_for_filesystem_bytes")
    else:
        current_errors = current_semantics["error_count"]
        candidate = _m(observation.get("candidate"))
        if not candidate:
            if current_errors == 0:
                if workspace.get("worktree_clean") is True:
                    route = NO_REPAIR_NEEDED
                else:
                    route = GIT_DIFF_REVIEW_READY
                status = READY
            else:
                route = CANDIDATE_GENERATION_READY
                status = READY
        else:
            before_digest = _digest(
                candidate.get("before_content_digest"),
                "candidate_before_content_digest",
                blockers,
            )
            result_digest = _digest(
                candidate.get("result_content_digest"),
                "candidate_result_content_digest",
                blockers,
                optional=True,
            )
            before_errors = _nat(
                candidate.get("before_error_count"),
                "candidate_before_error_count",
                blockers,
            )
            candidate_receipt = _validate_candidate_receipt(
                candidate.get("candidate_patch_receipt"),
                lineage_issues,
            )
            preflight_receipt = _validate_preflight_receipt(
                candidate.get("static_preflight_receipt"),
                lineage_issues,
            )

            if candidate_receipt is None:
                route = CANDIDATE_GENERATION_READY
                status = READY
                reasons.append("candidate_receipt_absent")
            elif current_digest not in {before_digest, result_digest}:
                route = CANDIDATE_STALE
                status = PARTIAL
                reasons.append("workspace_bytes_are_neither_candidate_source_nor_result")
            elif lineage_issues:
                route = LINEAGE_OBSTRUCTION
                status = OBSTRUCTED
            elif preflight_receipt is None:
                route = CANDIDATE_PREFLIGHT_READY
                status = READY
            else:
                disposition = preflight_receipt.get("codeai_disposition")
                if disposition == DISPOSITION_REPAIRABLE:
                    route = CANDIDATE_REPAIR_FEEDBACK
                    status = READY
                elif disposition == DISPOSITION_HOLD:
                    route = CANDIDATE_HOLD
                    status = READY
                elif disposition == DISPOSITION_REJECTED:
                    route = CANDIDATE_REJECTED
                    status = READY
                else:
                    shadow = _semantic_record(
                        candidate.get("shadow_semantics"),
                        "candidate_shadow_semantics",
                        blockers,
                        optional=True,
                    )
                    if not result_digest or shadow is None:
                        route = SHADOW_REOBSERVE
                        status = PARTIAL
                        reasons.append("candidate_result_semantic_observation_missing")
                    elif shadow["source_content_digest"] != result_digest:
                        route = SHADOW_REOBSERVE
                        status = PARTIAL
                        reasons.append("candidate_shadow_semantics_stale")
                    else:
                        candidate_error_count = shadow["error_count"]
                        if before_errors is None or candidate_error_count is None:
                            route = SHADOW_REOBSERVE
                            status = PARTIAL
                        else:
                            improvement = candidate_error_count < before_errors
                            if candidate_error_count > before_errors:
                                route = CANDIDATE_REGRESSION
                                status = READY
                            elif candidate_error_count == before_errors and before_errors > 0:
                                route = CANDIDATE_NO_IMPROVEMENT
                                status = READY
                            elif current_digest == before_digest:
                                route = LOCAL_APPLICATION_CANDIDATE
                                status = READY
                            elif current_digest == result_digest:
                                # The result has been applied by another authorized/local layer.
                                if current_semantics["source_content_digest"] != result_digest:
                                    route = LEAN_REOBSERVE
                                    status = PARTIAL
                                elif (
                                    current_semantics["error_count"] is not None
                                    and candidate_error_count is not None
                                    and current_semantics["error_count"] > candidate_error_count
                                ):
                                    route = LEAN_REOBSERVE
                                    status = PARTIAL
                                    reasons.append("post_application_semantics_worse_than_shadow")
                                elif candidate.get("git_diff_reviewed") is not True:
                                    route = GIT_DIFF_REVIEW_READY
                                    status = READY
                                else:
                                    _digest(
                                        candidate.get("git_diff_digest"),
                                        "candidate_git_diff_digest",
                                        blockers,
                                    )
                                    if not remote_aligned:
                                        route = REMOTE_RECONCILIATION_REQUIRED
                                        status = PARTIAL
                                    elif workspace.get(
                                        "remote_mutation_eligible_before_authority_check"
                                    ) is not True:
                                        route = LOCAL_GIT_ADMISSION_REQUIRED
                                        status = PARTIAL
                                    else:
                                        route = REMOTE_SUBMISSION_CANDIDATE
                                        status = READY
                            else:
                                route = CANDIDATE_STALE
                                status = PARTIAL
                                reasons.append("workspace_bytes_are_neither_candidate_source_nor_result")

    if blockers:
        return {
            "route": LINEAGE_OBSTRUCTION,
            "status": BLOCKED,
            "target_path": target_path,
            "current_error_count": (
                current_semantics["error_count"]
                if current_semantics is not None
                else None
            ),
            "candidate_error_count": candidate_error_count,
            "semantic_improvement": improvement,
            "local_semantic_work_allowed": local_semantic_allowed,
            "lineage_issues": sorted(set(lineage_issues)),
            "reasons": sorted(set(reasons)),
        }

    return {
        "route": route,
        "status": status,
        "target_path": target_path,
        "current_error_count": (
            current_semantics["error_count"]
            if current_semantics is not None
            else None
        ),
        "candidate_error_count": candidate_error_count,
        "semantic_improvement": improvement,
        "local_semantic_work_allowed": local_semantic_allowed,
        "lineage_issues": sorted(set(lineage_issues)),
        "reasons": sorted(set(reasons)),
        "remote_local_aligned": remote_aligned,
        "current_content_digest": current_digest,
        "current_semantic_observation_digest": (
            current_semantics["semantic_observation_digest"]
            if current_semantics is not None
            else ""
        ),
    }


def build_semantic_first_repair_loop(
    *,
    runtime_context: Mapping[str, Any],
    authority_packet: Mapping[str, Any],
) -> SemanticFirstRepairLoopResult:
    ctx = _m(runtime_context)
    authority_packet = _m(authority_packet)
    blockers: list[str] = []
    warnings: list[str] = []

    root = _root(ctx.get("runtime_root"), blockers)
    plan_path = root / "semantic_first_repair_loop_plan_v7_20.json"
    federation_path = root / "development_mcp_federation_packet_v7_19.json"
    observation_path = root / "semantic_first_repair_observation_v7_20.json"
    output_path = root / "semantic_first_repair_loop_packet_v7_20.json"
    receipt_path = root / "semantic_first_repair_loop_receipt_v7_20.json"
    audit_path = root / "semantic_first_repair_loop_audit_v7_20.jsonl"

    if ctx.get("semantic_first_repair_loop_enabled") is not True:
        blockers.append("semantic_first_repair_loop_enabled_not_true")
    if ctx.get("apply_semantic_first_repair_loop") is not True:
        blockers.append("apply_semantic_first_repair_loop_not_true")
    if (
        authority_packet.get("authority_status")
        != "KUUOS_SEMANTIC_FIRST_REPAIR_LOOP_AUTHORITY_READY"
    ):
        blockers.append("semantic_first_repair_loop_authority_not_ready")

    for field in (
        "plan_read_allowed",
        "federation_packet_read_allowed",
        "repair_observation_read_allowed",
        "output_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if authority_packet.get(field) is not True:
            blockers.append(field.replace("_allowed", "_not_allowed"))

    plan = _read_json(plan_path)
    federation = _read_json(federation_path)
    observation = _read_json(observation_path)

    if not plan:
        blockers.append("semantic_first_repair_plan_missing_or_invalid")
    else:
        _validate_plan(plan, blockers)
    if not federation:
        blockers.append("development_mcp_federation_packet_missing_or_invalid")
    if not observation:
        blockers.append("semantic_first_repair_observation_missing_or_invalid")

    classified: dict[str, Any] = {}
    if not blockers:
        classified = _classify(
            federation=federation,
            observation=observation,
            blockers=blockers,
        )

    if blockers:
        status = BLOCKED
        route = LINEAGE_OBSTRUCTION
    else:
        status = classified["status"]
        route = classified["route"]

    output: dict[str, Any] = {}
    output_written = False
    if not blockers:
        output = {
            "version": VERSION,
            "status": status,
            "route": route,
            "repair_state": classified,
            "semantic_first_boundary": {
                "dirty_worktree_may_continue_semantic_repair": True,
                "lean_observation_bound_to_source_digest": True,
                "stale_diagnostic_may_apply_patch": False,
                "candidate_patch_bound_to_before_digest": True,
                "candidate_receipt_is_current_byte_binding": False,
                "candidate_result_requires_fresh_shadow_semantics": True,
                "semantic_improvement_grants_local_write_authority": False,
                "semantic_improvement_grants_remote_write_authority": False,
                "static_preflight_is_correctness_proof": False,
                "candidate_rejection_erases_local_worktree": False,
                "remote_revision_mismatch_blocks_local_repair": False,
                "remote_submission_requires_git_diff_review": True,
                "remote_submission_requires_revision_alignment": True,
                "remote_submission_requires_separate_authority_after_this_layer": True,
                "source_authority_transferred": False,
            },
            "reused_codeai_contracts": {
                "candidate_patch_envelope": "runtime/kuuos_codeai_candidate_patch_envelope_v0_1.py",
                "typed_structured_edit_ir": "runtime/kuuos_codeai_typed_structured_edit_ir_v0_1.py",
                "static_admissibility_preflight": "runtime/kuuos_codeai_candidate_static_admissibility_preflight_v0_1.py",
                "verification_guided_repair": "runtime/kuuos_codeai_verification_guided_candidate_repair_regeneration_v0_1.py",
                "bounded_repair_cycle": "runtime/kuuos_codeai_bounded_repair_cycle_orchestration_v0_1.py",
            },
            "epoch": int(time.time()),
        }
        _write_json(output_path, output)
        output_written = True

    packet_id = "kuuos-semantic-first-repair-loop-" + _sha(
        {
            "plan": plan,
            "federation": federation,
            "observation": observation,
            "output": output,
            "blockers": sorted(set(blockers)),
        }
    )[:16]

    receipt = {
        "version": VERSION,
        "status": status,
        "packet_id": packet_id,
        "route": route,
        "target_path": str(classified.get("target_path", "")),
        "semantic_improvement": classified.get("semantic_improvement"),
        "output_written": output_written,
        "output_digest": _sha(output),
        "local_application_authority_granted": False,
        "remote_mutation_authority_granted": False,
        "semantic_improvement_grants_write_authority": False,
        "source_authority_transferred": False,
        "blockers": sorted(set(blockers)),
        "warnings": warnings,
        "epoch": int(time.time()),
    }

    if authority_packet.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if authority_packet.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return SemanticFirstRepairLoopResult(
        VERSION,
        status,
        packet_id,
        str(root),
        route,
        str(classified.get("target_path", "")),
        classified.get("current_error_count"),
        classified.get("candidate_error_count"),
        classified.get("semantic_improvement"),
        bool(classified.get("local_semantic_work_allowed", False)),
        False,
        False,
        str(output_path),
        str(receipt_path),
        str(audit_path),
        output_written,
        sorted(set(blockers)),
        warnings,
    )
