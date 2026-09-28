#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import re
from typing import Any, Mapping

VERSION = "kuuos_runtime_root_bound_analysis_repair_readiness_v7_35"
INTAKE_VERSION = "kuuos_runtime_root_bound_development_intake_v7_33"
BUNDLE_VERSION = "kuuos_runtime_root_bound_fact_observation_bundle_v7_34"

READY = "KUUOS_ROOT_BOUND_ANALYSIS_REPAIR_READINESS_READY"
PARTIAL = "KUUOS_ROOT_BOUND_ANALYSIS_REPAIR_READINESS_PARTIAL"
OBSTRUCTED = "KUUOS_ROOT_BOUND_ANALYSIS_REPAIR_READINESS_OBSTRUCTED"
NOT_APPLICABLE = "KUUOS_ROOT_BOUND_ANALYSIS_REPAIR_READINESS_NOT_APPLICABLE"

ANALYSIS_READY = "root_bound_task_analysis_ready"
REPAIR_READY_AUTHORITY_PENDING = "root_bound_task_repair_ready_authority_pending"
EFFECT_READY_AUTHORITY_PENDING = "root_bound_task_effect_ready_authority_pending"
TASK_RECLASSIFICATION_REQUIRED = "root_bound_task_reclassification_required"
FACT_REOBSERVATION_REQUIRED = "root_bound_task_fact_reobservation_required"
BINDING_OBSTRUCTION = "root_bound_task_readiness_binding_obstruction"

SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA64 = re.compile(r"^[0-9a-f]{64}$")

COMPLETE_BUNDLE_STATE = "root_bound_fact_bundle_complete"

EFFECT_CONTRACTS: dict[str, tuple[str, str, str]] = {
    "lean_ci_repair": (
        "workspace_source_edit",
        "workspace_write_authority",
        "prepare_bounded_local_repair_then_request_fresh_workspace_authority",
    ),
    "local_worktree_review": (
        "workspace_git_or_file_mutation",
        "workspace_write_authority",
        "request_fresh_workspace_authority_for_bound_local_effect",
    ),
    "remote_repository_observation": (
        "github_remote_mutation",
        "github_write_authority",
        "request_fresh_github_authority_for_bound_remote_effect",
    ),
    "browser_functional_validation": (
        "browser_session_effect",
        "browser_effect_authority",
        "request_fresh_browser_effect_authority_for_bound_task",
    ),
    "browser_debugging": (
        "browser_session_effect",
        "browser_effect_authority",
        "request_fresh_browser_effect_authority_for_bound_task",
    ),
    "deployment_debugging": (
        "deployment_provider_effect",
        "deployment_provider_write_authority",
        "request_fresh_provider_authority_for_bound_deployment_effect",
    ),
    "database_debugging": (
        "database_provider_effect",
        "database_provider_write_authority",
        "request_fresh_provider_authority_for_bound_database_effect",
    ),
    "multi_mcp_orchestration": (
        "mcp_orchestration_effect",
        "mcp_orchestration_authority",
        "request_fresh_orchestration_authority_for_bound_task",
    ),
}

ANALYSIS_ONLY_TASKS = {
    "external_library_docs",
    "mcp_spec_research",
}


@dataclass(frozen=True)
class RootBoundAnalysisRepairReadinessResult:
    version: str
    status: str
    packet_id: str
    readiness_state: str
    task_id: str
    task_kind: str
    lineage_root_id: str
    lineage_root_main_sha: str
    target_paths: list[str]
    analysis_ready: bool
    repair_planning_ready: bool
    effect_requested: bool
    effect_required: bool
    effect_class: str
    fresh_authority_required: bool
    requested_authority_class: str
    task_candidate_retained: bool
    mutation_executed: bool
    write_authority_granted: bool
    merge_authority_granted: bool
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


def _digest(value: Any, name: str, blockers: list[str], *, optional: bool = False) -> str:
    text = str(value or "").strip()
    if optional and not text:
        return ""
    if SHA64.fullmatch(text) is None:
        blockers.append(name + "_invalid")
    return text


def _commit(value: Any, name: str, blockers: list[str], *, optional: bool = False) -> str:
    text = str(value or "").strip().lower()
    if optional and not text:
        return ""
    if SHA40.fullmatch(text) is None:
        blockers.append(name + "_invalid")
    return text


def _string_list(value: Any, name: str, blockers: list[str]) -> list[str]:
    if not isinstance(value, list):
        blockers.append(name + "_not_list")
        return []
    result = [str(item).strip() for item in value if str(item).strip()]
    if len(result) != len(set(result)):
        blockers.append(name + "_duplicates")
    return sorted(set(result))


def _not_applicable(
    *,
    intake: Mapping[str, Any],
    bundle: Mapping[str, Any],
    blockers: list[str],
    warnings: list[str],
) -> RootBoundAnalysisRepairReadinessResult:
    task_id = str(bundle.get("task_id") or intake.get("task_id") or "")
    task_kind = str(bundle.get("task_kind") or intake.get("task_kind") or "")
    root_id = str(bundle.get("lineage_root_id") or intake.get("lineage_root_id") or "")
    root_main = str(
        bundle.get("lineage_root_main_sha")
        or intake.get("lineage_root_main_sha")
        or ""
    )
    targets = sorted(
        {
            str(path)
            for path in (bundle.get("target_paths") or intake.get("target_paths") or [])
            if str(path)
        }
    )
    packet_id = "kuuos-root-bound-readiness-" + _sha(
        {
            "intake": _sha(intake),
            "bundle": _sha(bundle),
            "state": "not_applicable",
            "blockers": sorted(set(blockers)),
        }
    )[:16]
    return RootBoundAnalysisRepairReadinessResult(
        VERSION,
        OBSTRUCTED if blockers else NOT_APPLICABLE,
        packet_id,
        BINDING_OBSTRUCTION if blockers else "root_bound_task_not_applicable",
        task_id,
        task_kind,
        root_id,
        root_main,
        targets,
        False,
        False,
        False,
        False,
        "",
        False,
        "",
        bool(task_id),
        False,
        False,
        False,
        "return_to_v7_34_root_bound_fact_observation_bundle",
        {
            "source_intake_packet_digest": _sha(intake),
            "source_fact_bundle_packet_digest": _sha(bundle),
            "source_authority_transferred": False,
        },
        sorted(set(blockers)),
        sorted(set(warnings)),
    )


def build_root_bound_analysis_repair_readiness(
    *,
    intake_packet: Mapping[str, Any],
    fact_bundle_packet: Mapping[str, Any],
) -> RootBoundAnalysisRepairReadinessResult:
    intake = _m(intake_packet)
    bundle = _m(fact_bundle_packet)
    blockers: list[str] = []
    warnings: list[str] = []

    intake_digest = _sha(intake)
    bundle_digest = _sha(bundle)

    if intake.get("version") != INTAKE_VERSION:
        blockers.append("intake_packet_version_invalid")
    if bundle.get("version") != BUNDLE_VERSION:
        blockers.append("fact_bundle_packet_version_invalid")

    if blockers:
        return _not_applicable(
            intake=intake,
            bundle=bundle,
            blockers=blockers,
            warnings=warnings,
        )

    intake_evidence = _m(intake.get("evidence"))
    bundle_evidence = _m(bundle.get("evidence"))

    source_intake_digest = _digest(
        bundle_evidence.get("source_intake_packet_digest"),
        "source_intake_packet_digest",
        blockers,
    )
    if source_intake_digest != intake_digest:
        blockers.append("fact_bundle_source_intake_digest_mismatch")

    task_id = str(bundle.get("task_id", "")).strip()
    task_kind = str(bundle.get("task_kind", "")).strip()
    root_id = str(bundle.get("lineage_root_id", "")).strip()
    root_main = _commit(
        bundle.get("lineage_root_main_sha"),
        "bundle_lineage_root_main_sha",
        blockers,
    )
    target_paths = _string_list(bundle.get("target_paths", []), "bundle_target_paths", blockers)
    selected_planes = _string_list(
        bundle.get("selected_fact_planes", []),
        "bundle_selected_fact_planes",
        blockers,
    )
    fresh_planes = _string_list(
        bundle.get("fresh_fact_planes", []),
        "bundle_fresh_fact_planes",
        blockers,
    )
    missing_planes = _string_list(
        bundle.get("missing_fact_planes", []),
        "bundle_missing_fact_planes",
        blockers,
    )

    intake_task_id = str(intake.get("task_id", "")).strip()
    intake_task_kind = str(intake.get("task_kind", "")).strip()
    intake_root_id = str(intake.get("lineage_root_id", "")).strip()
    intake_root_main = _commit(
        intake.get("lineage_root_main_sha"),
        "intake_lineage_root_main_sha",
        blockers,
    )
    intake_targets = _string_list(intake.get("target_paths", []), "intake_target_paths", blockers)
    intake_planes = _string_list(
        intake.get("required_fact_planes", []),
        "intake_required_fact_planes",
        blockers,
    )

    if task_id != intake_task_id:
        blockers.append("task_id_mismatch")
    if task_kind != intake_task_kind:
        blockers.append("task_kind_mismatch")
    if root_id != intake_root_id:
        blockers.append("lineage_root_id_mismatch")
    if root_main != intake_root_main:
        blockers.append("lineage_root_main_sha_mismatch")
    if target_paths != intake_targets:
        blockers.append("target_paths_mismatch")
    if selected_planes != intake_planes:
        blockers.append("selected_fact_planes_mismatch")

    intake_binding_digest = _digest(
        intake_evidence.get("task_binding_digest"),
        "intake_task_binding_digest",
        blockers,
    )
    bundle_binding_digest = _digest(
        bundle_evidence.get("task_binding_digest"),
        "bundle_task_binding_digest",
        blockers,
    )
    if intake_binding_digest != bundle_binding_digest:
        blockers.append("task_binding_digest_mismatch")

    intake_scope_digest = _digest(
        intake_evidence.get("scope_digest"),
        "intake_scope_digest",
        blockers,
    )
    bundle_scope_digest = _digest(
        bundle_evidence.get("scope_digest"),
        "bundle_scope_digest",
        blockers,
    )
    if intake_scope_digest != bundle_scope_digest:
        blockers.append("scope_digest_mismatch")

    if bundle.get("mutation_executed") is not False:
        blockers.append("fact_bundle_mutation_boundary_invalid")
    if bundle.get("write_authority_granted") is not False:
        blockers.append("fact_bundle_write_authority_boundary_invalid")
    if bundle_evidence.get("observation_bundle_grants_merge_authority") is not False:
        blockers.append("fact_bundle_merge_authority_boundary_invalid")
    if bundle_evidence.get("source_authority_transferred") is not False:
        blockers.append("fact_bundle_source_authority_boundary_invalid")
    if intake.get("write_authority_granted") is not False:
        blockers.append("intake_write_authority_boundary_invalid")
    if intake.get("merge_authority_granted") is not False:
        blockers.append("intake_merge_authority_boundary_invalid")

    mutation_requested = intake.get("mutation_requested")
    if not isinstance(mutation_requested, bool):
        blockers.append("mutation_requested_must_be_bool")
        mutation_requested = False

    bundle_complete = bool(
        bundle.get("status") == "KUUOS_ROOT_BOUND_FACT_OBSERVATION_BUNDLE_READY"
        and bundle.get("bundle_state") == COMPLETE_BUNDLE_STATE
        and not missing_planes
        and set(selected_planes).issubset(set(fresh_planes))
        and bundle.get("task_candidate_retained") is True
    )

    if {
        "working_bytes",
        "lean_semantics",
    }.issubset(set(selected_planes)):
        if bundle.get("lean_filesystem_coherent") is not True:
            bundle_complete = False
            warnings.append("lean_filesystem_semantics_require_reobservation")

    if blockers:
        state = BINDING_OBSTRUCTION
        status = OBSTRUCTED
        analysis_ready = False
        repair_ready = False
        effect_required = False
        effect_class = ""
        authority_required = False
        authority_class = ""
        next_route = "repair_v7_33_v7_34_task_or_fact_binding"
    elif not bundle_complete:
        state = FACT_REOBSERVATION_REQUIRED
        status = PARTIAL
        analysis_ready = False
        repair_ready = False
        effect_required = False
        effect_class = ""
        authority_required = False
        authority_class = ""
        next_route = str(
            bundle.get("next_route")
            or "return_to_v7_34_and_complete_root_bound_fact_bundle"
        )
    elif mutation_requested and task_kind in ANALYSIS_ONLY_TASKS:
        state = TASK_RECLASSIFICATION_REQUIRED
        status = PARTIAL
        analysis_ready = True
        repair_ready = False
        effect_required = False
        effect_class = ""
        authority_required = False
        authority_class = ""
        next_route = "retain_analysis_and_reclassify_task_before_requesting_any_mutation_authority"
        warnings.append("mutation_intent_present_on_analysis_only_task_kind")
    elif not mutation_requested:
        state = ANALYSIS_READY
        status = READY
        analysis_ready = True
        repair_ready = task_kind == "lean_ci_repair"
        effect_required = False
        effect_class = ""
        authority_required = False
        authority_class = ""
        next_route = (
            "derive_bounded_local_repair_plan_without_mutation"
            if task_kind == "lean_ci_repair"
            else "perform_task_specific_analysis_without_effect_authority"
        )
    else:
        contract = EFFECT_CONTRACTS.get(task_kind)
        if contract is None:
            state = TASK_RECLASSIFICATION_REQUIRED
            status = PARTIAL
            analysis_ready = True
            repair_ready = False
            effect_required = False
            effect_class = ""
            authority_required = False
            authority_class = ""
            next_route = "retain_task_and_reclassify_effect_surface_before_authority_request"
            warnings.append("effect_surface_not_defined_for_task_kind")
        else:
            effect_class, authority_class, next_route = contract
            state = (
                REPAIR_READY_AUTHORITY_PENDING
                if task_kind == "lean_ci_repair"
                else EFFECT_READY_AUTHORITY_PENDING
            )
            status = READY
            analysis_ready = True
            repair_ready = task_kind in {"lean_ci_repair", "local_worktree_review"}
            effect_required = True
            authority_required = True

    evidence = {
        "source_intake_packet_digest": intake_digest,
        "source_fact_bundle_packet_digest": bundle_digest,
        "task_binding_digest": intake_binding_digest,
        "scope_digest": intake_scope_digest,
        "normalized_fact_observations_digest": str(
            bundle_evidence.get("normalized_observations_digest", "")
        ),
        "selected_fact_planes": selected_planes,
        "fresh_fact_planes": fresh_planes,
        "missing_fact_planes": missing_planes,
        "fact_bundle_complete": bundle_complete,
        "mutation_requested": mutation_requested,
        "effect_requirement_derived_from_task_kind_and_mutation_intent": True,
        "authority_requested_only_if_effect_required": bool(
            authority_required and effect_required
        ),
        "readiness_executes_mutation": False,
        "readiness_grants_write_authority": False,
        "readiness_grants_merge_authority": False,
        "fact_bundle_is_write_authority": False,
        "analysis_readiness_is_write_authority": False,
        "repair_readiness_is_write_authority": False,
        "source_authority_transferred": False,
    }

    packet_id = "kuuos-root-bound-readiness-" + _sha(
        {
            "intake_digest": intake_digest,
            "bundle_digest": bundle_digest,
            "state": state,
            "effect_class": effect_class,
            "authority_class": authority_class,
            "evidence": evidence,
            "blockers": sorted(set(blockers)),
            "warnings": sorted(set(warnings)),
        }
    )[:16]

    return RootBoundAnalysisRepairReadinessResult(
        VERSION,
        status,
        packet_id,
        state,
        task_id,
        task_kind,
        root_id,
        root_main,
        target_paths,
        analysis_ready,
        repair_ready,
        mutation_requested,
        effect_required,
        effect_class,
        authority_required,
        authority_class,
        True,
        False,
        False,
        False,
        next_route,
        evidence,
        sorted(set(blockers)),
        sorted(set(warnings)),
    )
