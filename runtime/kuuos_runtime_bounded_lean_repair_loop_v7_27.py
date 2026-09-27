#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import re
from typing import Any, Mapping

VERSION = "kuuos_runtime_bounded_lean_repair_loop_v7_27"
READINESS_VERSION = "kuuos_runtime_ci_repair_readiness_v7_26"
OBSERVATION_VERSION = "kuuos_bounded_lean_repair_observation_v7_27"

READY = "KUUOS_BOUNDED_LEAN_REPAIR_LOOP_READY"
PARTIAL = "KUUOS_BOUNDED_LEAN_REPAIR_LOOP_PARTIAL"
OBSTRUCTED = "KUUOS_BOUNDED_LEAN_REPAIR_LOOP_OBSTRUCTED"
NOT_APPLICABLE = "KUUOS_BOUNDED_LEAN_REPAIR_LOOP_NOT_APPLICABLE"
BLOCKED = "KUUOS_BOUNDED_LEAN_REPAIR_LOOP_BLOCKED"

SEMANTIC_REOBSERVATION = "post_edit_semantic_reobservation_required"
LEAN_ERRORS_REMAIN = "post_edit_lean_errors_remain"
BUDGET_REACHED = "bounded_repair_budget_reached"
DIFF_REOBSERVATION = "git_diff_reobservation_required"
NO_EFFECTIVE_EDIT = "no_effective_edit_observed"
GIT_ADMISSION_READY = "repair_locally_verified_git_admission_ready"
LINEAGE_OBSTRUCTION = "cross_surface_repair_obstruction"

SHA64 = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True)
class BoundedLeanRepairLoopResult:
    version: str
    status: str
    packet_id: str
    target_path: str
    iteration_index: int
    max_iterations: int
    repair_state: str
    candidate_retained: bool
    full_file_audit_bound: bool
    edit_effect_observed: bool
    lean_semantic_fresh: bool
    lean_error_count: int
    git_diff_fresh: bool
    local_repair_verified: bool
    git_admission_ready: bool
    remote_publish_ready: bool
    next_route: str
    evidence: dict[str, Any]
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


def _digest(
    value: Any,
    name: str,
    blockers: list[str],
    *,
    optional: bool = False,
) -> str:
    text = str(value or "").strip()
    if optional and not text:
        return ""
    if SHA64.fullmatch(text) is None:
        blockers.append(name + "_invalid")
    return text


def _positive_int(
    value: Any,
    name: str,
    blockers: list[str],
    *,
    maximum: int | None = None,
) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        blockers.append(name + "_invalid")
        return 1
    if maximum is not None and value > maximum:
        blockers.append(name + "_above_runtime_bound")
    return value


def _nonnegative_int(value: Any, name: str, blockers: list[str]) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        blockers.append(name + "_invalid")
        return 0
    return value


def _paths(value: Any, blockers: list[str]) -> list[str]:
    if not isinstance(value, list):
        blockers.append("git_changed_paths_not_list")
        return []
    out: list[str] = []
    for raw in value:
        path = str(raw).strip()
        if not path:
            blockers.append("git_changed_path_empty")
            continue
        if path not in out:
            out.append(path)
    return out


def build_bounded_lean_repair_loop(
    *,
    readiness_packet: Mapping[str, Any],
    repair_observation: Mapping[str, Any],
) -> BoundedLeanRepairLoopResult:
    readiness = _m(readiness_packet)
    observation = _m(repair_observation)
    blockers: list[str] = []
    warnings: list[str] = []

    if readiness.get("version") != READINESS_VERSION:
        blockers.append("readiness_version_invalid")
    if observation.get("version") != OBSERVATION_VERSION:
        blockers.append("repair_observation_version_invalid")

    target_path = str(readiness.get("target_path", "")).strip()
    observed_target = str(observation.get("target_path", "")).strip()

    if target_path and not target_path.endswith(".lean"):
        blockers.append("readiness_target_not_lean")
    if observed_target != target_path:
        blockers.append("repair_target_path_mismatch")

    iteration_index = _positive_int(
        observation.get("iteration_index"),
        "iteration_index",
        blockers,
        maximum=12,
    )
    max_iterations = _positive_int(
        observation.get("max_iterations"),
        "max_iterations",
        blockers,
        maximum=12,
    )
    if iteration_index > max_iterations:
        blockers.append("iteration_exceeds_max_iterations")

    full_file_audit_digest = _digest(
        observation.get("full_file_audit_digest"),
        "full_file_audit_digest",
        blockers,
    )
    edit_receipt_digest = _digest(
        observation.get("edit_receipt_digest"),
        "edit_receipt_digest",
        blockers,
        optional=observation.get("edit_applied") is not True,
    )
    pre_edit_digest = _digest(
        observation.get("pre_edit_content_digest"),
        "pre_edit_content_digest",
        blockers,
    )
    post_edit_digest = _digest(
        observation.get("post_edit_content_digest"),
        "post_edit_content_digest",
        blockers,
    )
    filesystem_observation_digest = _digest(
        observation.get("filesystem_observation_digest"),
        "filesystem_observation_digest",
        blockers,
    )
    lean_source_digest = _digest(
        observation.get("lean_source_content_digest"),
        "lean_source_content_digest",
        blockers,
    )
    lean_diagnostics_digest = _digest(
        observation.get("lean_diagnostics_digest"),
        "lean_diagnostics_digest",
        blockers,
    )
    git_diff_digest = _digest(
        observation.get("git_diff_digest"),
        "git_diff_digest",
        blockers,
    )
    git_target_post_digest = _digest(
        observation.get("git_diff_target_post_content_digest"),
        "git_diff_target_post_content_digest",
        blockers,
    )
    lean_error_count = _nonnegative_int(
        observation.get("lean_error_count"),
        "lean_error_count",
        blockers,
    )
    changed_paths = _paths(observation.get("git_changed_paths"), blockers)

    if readiness.get("full_target_file_audit_required") is not True:
        blockers.append("readiness_full_file_audit_boundary_missing")
    if readiness.get("evidence", {}).get("repair_scope") != "entire_target_file":
        blockers.append("readiness_repair_scope_not_entire_file")

    if readiness.get("local_repair_ready") is not True:
        if blockers:
            status = BLOCKED
        else:
            status = NOT_APPLICABLE
        packet_id = "kuuos-bounded-lean-repair-loop-" + _sha(
            {
                "readiness_packet_id": readiness.get("packet_id"),
                "target_path": target_path,
                "iteration_index": iteration_index,
                "blockers": sorted(set(blockers)),
            }
        )[:16]
        return BoundedLeanRepairLoopResult(
            VERSION,
            status,
            packet_id,
            target_path,
            iteration_index,
            max_iterations,
            "repair_not_locally_ready",
            bool(readiness.get("repair_candidate_retained")),
            bool(full_file_audit_digest),
            False,
            False,
            lean_error_count,
            False,
            False,
            False,
            False,
            "return_to_ci_repair_readiness",
            {},
            sorted(set(blockers)),
            warnings,
        )

    readiness_evidence = _m(readiness.get("evidence"))
    readiness_fs_digest = _digest(
        readiness_evidence.get("filesystem_content_digest"),
        "readiness_filesystem_content_digest",
        blockers,
    )

    if pre_edit_digest != readiness_fs_digest:
        blockers.append("edit_preimage_does_not_match_repair_ready_bytes")

    edit_applied = observation.get("edit_applied") is True
    edit_effect_observed = bool(
        edit_applied and post_edit_digest and post_edit_digest != pre_edit_digest
    )

    if observation.get("full_file_audit_completed") is not True:
        blockers.append("full_file_audit_not_completed")

    lean_semantic_fresh = bool(
        observation.get("lean_observation_after_edit") is True
        and post_edit_digest
        and lean_source_digest
        and post_edit_digest == lean_source_digest
    )

    git_diff_fresh = bool(
        observation.get("git_diff_observed_after_edit") is True
        and git_diff_digest
        and target_path in changed_paths
        and git_target_post_digest == post_edit_digest
    )

    if blockers:
        repair_state = LINEAGE_OBSTRUCTION
        status = OBSTRUCTED
        next_route = "reestablish_repair_readiness_from_current_bytes"
        local_repair_verified = False
        git_admission_ready = False
    elif not edit_effect_observed:
        repair_state = NO_EFFECTIVE_EDIT
        status = PARTIAL
        next_route = "retain_candidate_and_observe_or_apply_a_real_edit"
        local_repair_verified = False
        git_admission_ready = False
        warnings.append("repair_iteration_did_not_change_target_bytes")
    elif not lean_semantic_fresh:
        repair_state = SEMANTIC_REOBSERVATION
        status = PARTIAL
        next_route = "reobserve_lean_semantics_on_post_edit_bytes"
        local_repair_verified = False
        git_admission_ready = False
    elif lean_error_count > 0:
        local_repair_verified = False
        git_admission_ready = False
        if iteration_index >= max_iterations:
            repair_state = BUDGET_REACHED
            status = PARTIAL
            next_route = "retain_candidate_and_request_explicit_continuation_or_replan"
            warnings.append("repair_iteration_budget_reached_without_semantic_success")
        else:
            repair_state = LEAN_ERRORS_REMAIN
            status = PARTIAL
            next_route = "continue_bounded_repair_from_current_post_edit_bytes"
    elif not git_diff_fresh:
        repair_state = DIFF_REOBSERVATION
        status = PARTIAL
        next_route = "reobserve_git_diff_for_semantically_verified_bytes"
        local_repair_verified = True
        git_admission_ready = False
    else:
        repair_state = GIT_ADMISSION_READY
        status = READY
        next_route = "prepare_git_admission_then_post_commit_reobservation"
        local_repair_verified = True
        git_admission_ready = True

    supporting_paths = [path for path in changed_paths if path != target_path]
    if supporting_paths:
        warnings.append("supporting_file_changes_present_review_before_git_admission")

    evidence = {
        "repair_scope": "entire_target_file",
        "full_file_audit_digest": full_file_audit_digest,
        "edit_receipt_digest": edit_receipt_digest,
        "pre_edit_content_digest": pre_edit_digest,
        "post_edit_content_digest": post_edit_digest,
        "filesystem_observation_digest": filesystem_observation_digest,
        "lean_source_content_digest": lean_source_digest,
        "lean_diagnostics_digest": lean_diagnostics_digest,
        "git_diff_digest": git_diff_digest,
        "git_diff_target_post_content_digest": git_target_post_digest,
        "git_changed_paths_digest": _sha(changed_paths),
        "supporting_changed_path_count": len(supporting_paths),
        "full_target_file_audit_required": True,
        "ci_error_line_is_locator_not_scope": True,
        "raw_source_bytes_persisted": False,
        "raw_git_diff_persisted": False,
        "repair_budget_is_semantic_truth": False,
        "budget_exhaustion_is_rejection": False,
        "source_authority_transferred": False,
    }

    packet_id = "kuuos-bounded-lean-repair-loop-" + _sha(
        {
            "readiness_packet_id": readiness.get("packet_id"),
            "target_path": target_path,
            "iteration_index": iteration_index,
            "max_iterations": max_iterations,
            "repair_state": repair_state,
            "evidence": evidence,
            "blockers": sorted(set(blockers)),
            "warnings": sorted(set(warnings)),
        }
    )[:16]

    return BoundedLeanRepairLoopResult(
        VERSION,
        status,
        packet_id,
        target_path,
        iteration_index,
        max_iterations,
        repair_state,
        True,
        bool(full_file_audit_digest),
        edit_effect_observed,
        lean_semantic_fresh,
        lean_error_count,
        git_diff_fresh,
        local_repair_verified,
        git_admission_ready,
        False,
        next_route,
        evidence,
        sorted(set(blockers)),
        sorted(set(warnings)),
    )
