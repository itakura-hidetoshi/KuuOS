#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import re
from typing import Any, Mapping

VERSION = "kuuos_runtime_root_bound_fact_observation_bundle_v7_34"
SOURCE_VERSION = "kuuos_runtime_root_bound_development_intake_v7_33"
INPUT_VERSION = "kuuos_root_bound_fact_observations_v7_34"

READY = "KUUOS_ROOT_BOUND_FACT_OBSERVATION_BUNDLE_READY"
PARTIAL = "KUUOS_ROOT_BOUND_FACT_OBSERVATION_BUNDLE_PARTIAL"
OBSTRUCTED = "KUUOS_ROOT_BOUND_FACT_OBSERVATION_BUNDLE_OBSTRUCTED"
NOT_APPLICABLE = "KUUOS_ROOT_BOUND_FACT_OBSERVATION_BUNDLE_NOT_APPLICABLE"

BUNDLE_COMPLETE = "root_bound_fact_bundle_complete"
MISSING_OBSERVATIONS = "root_bound_fact_bundle_missing_observations"
SEMANTIC_REOBSERVATION = "root_bound_fact_bundle_semantic_reobservation_required"
ROOT_REOBSERVATION = "root_bound_fact_bundle_root_reobservation_required"
BINDING_OBSTRUCTION = "root_bound_fact_bundle_binding_obstruction"

SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA64 = re.compile(r"^[0-9a-f]{64}$")

APPLICABLE_INTAKE_STATES = {
    "root_bound_task_intake_ready",
    "root_bound_task_intake_ready_local_reconciliation_required",
    "root_bound_task_intake_ready_future_mutation_authority_required",
    "root_bound_task_intake_route_degraded",
}

TARGET_AWARE_PLANES = {
    "working_bytes",
    "lean_semantics",
    "local_diff",
}
ROOT_HEAD_PLANES = {
    "remote_ci",
    "remote_repository",
    "local_revision",
    "local_diff",
    "working_bytes",
    "lean_semantics",
}


@dataclass(frozen=True)
class RootBoundFactObservationBundleResult:
    version: str
    status: str
    packet_id: str
    bundle_state: str
    task_id: str
    task_kind: str
    lineage_root_id: str
    lineage_root_main_sha: str
    selected_fact_planes: list[str]
    fresh_fact_planes: list[str]
    missing_fact_planes: list[str]
    stale_fact_planes: list[str]
    target_paths: list[str]
    lean_filesystem_coherent: bool | None
    task_candidate_retained: bool
    mutation_executed: bool
    write_authority_granted: bool
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


def _commit(
    value: Any,
    name: str,
    blockers: list[str],
    *,
    optional: bool = False,
) -> str:
    text = str(value or "").strip().lower()
    if optional and not text:
        return ""
    if SHA40.fullmatch(text) is None:
        blockers.append(name + "_invalid")
    return text


def _paths(value: Any, name: str, blockers: list[str]) -> list[str]:
    if not isinstance(value, list):
        blockers.append(name + "_not_list")
        return []
    result: list[str] = []
    for raw in value:
        path = str(raw).strip()
        if not path:
            blockers.append(name + "_empty_path")
            continue
        if path.startswith("/") or path.startswith("../") or "/../" in path:
            blockers.append(name + "_outside_repository:" + path)
            continue
        result.append(path)
    if len(result) != len(set(result)):
        blockers.append(name + "_duplicates")
    return sorted(set(result))


def build_root_bound_fact_observation_bundle(
    *,
    intake_packet: Mapping[str, Any],
    observations_packet: Mapping[str, Any],
) -> RootBoundFactObservationBundleResult:
    intake = _m(intake_packet)
    obs_packet = _m(observations_packet)
    blockers: list[str] = []
    warnings: list[str] = []

    intake_digest = _sha(intake)
    if intake.get("version") != SOURCE_VERSION:
        blockers.append("intake_packet_version_invalid")

    intake_state = str(intake.get("intake_state", ""))
    intake_applicable = bool(
        intake.get("status")
        in {
            "KUUOS_ROOT_BOUND_DEVELOPMENT_INTAKE_READY",
            "KUUOS_ROOT_BOUND_DEVELOPMENT_INTAKE_PARTIAL",
        }
        and intake_state in APPLICABLE_INTAKE_STATES
        and intake.get("write_authority_granted") is False
        and intake.get("merge_authority_granted") is False
    )

    task_id = str(intake.get("task_id", "")).strip()
    task_kind = str(intake.get("task_kind", "")).strip()
    root_id = str(intake.get("lineage_root_id", "")).strip()
    root_main = str(intake.get("lineage_root_main_sha", "")).strip().lower()
    target_paths = sorted(
        {str(path) for path in intake.get("target_paths", []) if str(path)}
    )
    selected_planes = sorted(
        {
            str(plane)
            for plane in intake.get("required_fact_planes", [])
            if str(plane)
        }
    )
    intake_evidence = _m(intake.get("evidence"))
    task_binding_digest = str(
        intake_evidence.get("task_binding_digest", "")
    ).strip()
    scope_digest = str(intake_evidence.get("scope_digest", "")).strip()

    if not intake_applicable:
        packet_id = "kuuos-root-bound-fact-bundle-" + _sha(
            {
                "intake_digest": intake_digest,
                "state": "not_applicable",
                "blockers": sorted(set(blockers)),
            }
        )[:16]
        return RootBoundFactObservationBundleResult(
            VERSION,
            OBSTRUCTED if blockers else NOT_APPLICABLE,
            packet_id,
            "intake_not_ready_for_fact_materialization",
            task_id,
            task_kind,
            root_id,
            root_main,
            selected_planes,
            [],
            selected_planes,
            [],
            target_paths,
            None,
            bool(task_id),
            False,
            False,
            "return_to_v7_33_root_bound_development_intake",
            {
                "source_intake_packet_digest": intake_digest,
                "source_authority_transferred": False,
            },
            sorted(set(blockers)),
            warnings,
        )

    if obs_packet.get("version") != INPUT_VERSION:
        blockers.append("observations_packet_version_invalid")

    if _digest(
        obs_packet.get("source_intake_packet_digest"),
        "source_intake_packet_digest",
        blockers,
    ) != intake_digest:
        blockers.append("source_intake_packet_digest_mismatch")

    if str(obs_packet.get("task_id", "")).strip() != task_id:
        blockers.append("task_id_mismatch")
    if str(obs_packet.get("lineage_root_id", "")).strip() != root_id:
        blockers.append("lineage_root_id_mismatch")
    if _commit(
        obs_packet.get("lineage_root_main_sha"),
        "lineage_root_main_sha",
        blockers,
    ) != root_main:
        blockers.append("lineage_root_main_sha_mismatch")
    if _digest(
        obs_packet.get("task_binding_digest"),
        "task_binding_digest",
        blockers,
    ) != task_binding_digest:
        blockers.append("task_binding_digest_mismatch")
    if _digest(
        obs_packet.get("scope_digest"),
        "scope_digest",
        blockers,
    ) != scope_digest:
        blockers.append("scope_digest_mismatch")

    fresh_main = _commit(
        obs_packet.get("fresh_current_main_head_sha"),
        "fresh_current_main_head_sha",
        blockers,
    )
    fresh_main_obs_digest = _digest(
        obs_packet.get("fresh_current_main_observation_digest"),
        "fresh_current_main_observation_digest",
        blockers,
    )
    root_stale = bool(fresh_main and root_main and fresh_main != root_main)

    raw_observations = obs_packet.get("observations", [])
    if not isinstance(raw_observations, list):
        blockers.append("observations_not_list")
        raw_observations = []

    normalized: list[dict[str, Any]] = []
    seen_keys: set[tuple[str, str]] = set()
    for index, raw in enumerate(raw_observations):
        if not isinstance(raw, Mapping):
            blockers.append(f"observation_{index}_not_object")
            continue
        plane = str(raw.get("fact_plane", "")).strip()
        provider = str(raw.get("provider_id", "")).strip()
        target_path = str(raw.get("target_path", "")).strip()
        if not plane:
            blockers.append(f"observation_{index}_fact_plane_missing")
        if plane not in selected_planes:
            blockers.append(f"observation_{index}_unselected_fact_plane:{plane}")
        if not provider:
            blockers.append(f"observation_{index}_provider_missing")

        if target_path:
            if target_path not in target_paths:
                blockers.append(
                    f"observation_{index}_target_outside_task_scope:{target_path}"
                )
        elif plane in TARGET_AWARE_PLANES and target_paths:
            blockers.append(f"observation_{index}_target_path_required")

        key = (plane, target_path)
        if key in seen_keys:
            blockers.append(
                f"duplicate_fact_observation:{plane}:{target_path or 'GLOBAL'}"
            )
        seen_keys.add(key)

        bound_root = _commit(
            raw.get("bound_root_main_sha"),
            f"observation_{index}_bound_root_main_sha",
            blockers,
        )
        if bound_root != root_main:
            blockers.append(f"observation_{index}_root_main_mismatch")

        obs_digest = _digest(
            raw.get("observation_digest"),
            f"observation_{index}_digest",
            blockers,
        )
        freshness_digest = _digest(
            raw.get("freshness_binding_digest"),
            f"observation_{index}_freshness_binding_digest",
            blockers,
        )
        fresh = raw.get("fresh") is True

        if raw.get("raw_payload_persisted") is not False:
            blockers.append(f"observation_{index}_raw_payload_boundary_invalid")
        if raw.get("source_authority_transferred") is not False:
            blockers.append(
                f"observation_{index}_source_authority_transfer_invalid"
            )

        content_digest = _digest(
            raw.get("content_digest"),
            f"observation_{index}_content_digest",
            blockers,
            optional=plane not in {"working_bytes"},
        )
        semantic_source_digest = _digest(
            raw.get("semantic_source_content_digest"),
            f"observation_{index}_semantic_source_digest",
            blockers,
            optional=plane not in {"lean_semantics"},
        )
        semantic_result_digest = _digest(
            raw.get("semantic_result_digest"),
            f"observation_{index}_semantic_result_digest",
            blockers,
            optional=plane not in {"lean_semantics"},
        )

        observed_head = _commit(
            raw.get("observed_head_sha"),
            f"observation_{index}_observed_head_sha",
            blockers,
            optional=plane not in ROOT_HEAD_PLANES,
        )
        if plane in ROOT_HEAD_PLANES and observed_head and observed_head != root_main:
            # Stale provider evidence is retained but not treated as a structural
            # contradiction if it is explicitly marked non-fresh.
            if fresh:
                blockers.append(f"observation_{index}_fresh_head_mismatch")

        normalized.append(
            {
                "fact_plane": plane,
                "provider_id": provider,
                "target_path": target_path,
                "bound_root_main_sha": bound_root,
                "observed_head_sha": observed_head,
                "fresh": fresh,
                "observation_digest": obs_digest,
                "freshness_binding_digest": freshness_digest,
                "content_digest": content_digest,
                "semantic_source_content_digest": semantic_source_digest,
                "semantic_result_digest": semantic_result_digest,
            }
        )

    fresh_planes: set[str] = set()
    stale_planes: set[str] = set()
    for item in normalized:
        plane = item["fact_plane"]
        if item["fresh"] and (
            plane not in ROOT_HEAD_PLANES
            or not item["observed_head_sha"]
            or item["observed_head_sha"] == root_main
        ):
            fresh_planes.add(plane)
        else:
            stale_planes.add(plane)

    # Target-aware planes require coverage of every task target when selected.
    for plane in TARGET_AWARE_PLANES.intersection(selected_planes):
        covered = {
            item["target_path"]
            for item in normalized
            if item["fact_plane"] == plane and item["fresh"]
        }
        if target_paths and set(target_paths).issubset(covered):
            fresh_planes.add(plane)
        elif target_paths:
            fresh_planes.discard(plane)
            stale_planes.add(plane)

    missing_planes = sorted(set(selected_planes).difference(fresh_planes))

    lean_filesystem_coherent: bool | None = None
    semantic_reobserve = False
    if "working_bytes" in selected_planes and "lean_semantics" in selected_planes:
        fs_by_path = {
            item["target_path"]: item["content_digest"]
            for item in normalized
            if item["fact_plane"] == "working_bytes"
            and item["fresh"]
            and item["target_path"]
            and item["content_digest"]
        }
        lean_by_path = {
            item["target_path"]: item["semantic_source_content_digest"]
            for item in normalized
            if item["fact_plane"] == "lean_semantics"
            and item["fresh"]
            and item["target_path"]
            and item["semantic_source_content_digest"]
        }
        comparable = sorted(set(fs_by_path).intersection(lean_by_path))
        if comparable:
            mismatched = [
                path
                for path in comparable
                if fs_by_path[path] != lean_by_path[path]
            ]
            lean_filesystem_coherent = not mismatched
            if mismatched:
                semantic_reobserve = True
                warnings.extend(
                    "lean_semantic_source_stale:" + path
                    for path in mismatched
                )
        elif target_paths:
            lean_filesystem_coherent = False
            semantic_reobserve = True

    if blockers:
        state = BINDING_OBSTRUCTION
        status = OBSTRUCTED
        next_route = "repair_fact_observation_binding"
    elif root_stale:
        state = ROOT_REOBSERVATION
        status = PARTIAL
        next_route = "return_to_v7_32_and_v7_33_on_fresh_main"
    elif semantic_reobserve:
        state = SEMANTIC_REOBSERVATION
        status = PARTIAL
        next_route = "reobserve_lean_semantics_on_current_filesystem_bytes"
    elif missing_planes:
        state = MISSING_OBSERVATIONS
        status = PARTIAL
        next_route = "collect_missing_root_bound_fact_observations"
    else:
        state = BUNDLE_COMPLETE
        status = READY
        next_route = "derive_task_specific_readiness_from_complete_fact_bundle"

    evidence = {
        "source_intake_packet_digest": intake_digest,
        "task_binding_digest": task_binding_digest,
        "scope_digest": scope_digest,
        "fresh_current_main_head_sha": fresh_main,
        "fresh_current_main_observation_digest": fresh_main_obs_digest,
        "root_stale_against_fresh_main": root_stale,
        "normalized_observations_digest": _sha(normalized),
        "selected_fact_planes": selected_planes,
        "fresh_fact_planes": sorted(fresh_planes),
        "missing_fact_planes": missing_planes,
        "stale_fact_planes": sorted(stale_planes),
        "lean_filesystem_coherent": lean_filesystem_coherent,
        "observation_bundle_executes_mutation": False,
        "observation_bundle_grants_write_authority": False,
        "observation_bundle_grants_merge_authority": False,
        "task_candidate_retained": True,
        "raw_provider_payloads_persisted": False,
        "source_authority_transferred": False,
    }

    packet_id = "kuuos-root-bound-fact-bundle-" + _sha(
        {
            "intake_digest": intake_digest,
            "state": state,
            "evidence": evidence,
            "blockers": sorted(set(blockers)),
            "warnings": sorted(set(warnings)),
        }
    )[:16]

    return RootBoundFactObservationBundleResult(
        VERSION,
        status,
        packet_id,
        state,
        task_id,
        task_kind,
        root_id,
        root_main,
        selected_planes,
        sorted(fresh_planes),
        missing_planes,
        sorted(stale_planes),
        target_paths,
        lean_filesystem_coherent,
        True,
        False,
        False,
        next_route,
        evidence,
        sorted(set(blockers)),
        sorted(set(warnings)),
    )
