#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import re
from typing import Any, Mapping

VERSION = "kuuos_runtime_github_remote_candidate_materialization_v7_29"
SOURCE_VERSION = "kuuos_runtime_git_admission_post_commit_coherence_v7_28"
OBSERVATION_VERSION = "kuuos_github_remote_candidate_materialization_observation_v7_29"

READY = "KUUOS_GITHUB_REMOTE_CANDIDATE_MATERIALIZATION_READY"
PARTIAL = "KUUOS_GITHUB_REMOTE_CANDIDATE_MATERIALIZATION_PARTIAL"
OBSTRUCTED = "KUUOS_GITHUB_REMOTE_CANDIDATE_MATERIALIZATION_OBSTRUCTED"
NOT_APPLICABLE = "KUUOS_GITHUB_REMOTE_CANDIDATE_MATERIALIZATION_NOT_APPLICABLE"

AUTHORITY_REQUIRED = "remote_materialization_github_authority_required"
MATERIALIZATION_REQUIRED = "remote_object_materialization_receipt_required"
MATERIALIZATION_OBSTRUCTION = "remote_object_materialization_obstruction"
BRANCH_PUBLICATION_REQUIRED = "remote_candidate_branch_publication_required"
BRANCH_RESELECTION_REQUIRED = "remote_candidate_branch_reselection_required"
PUBLISHED_BASE_RECONCILIATION = "remote_candidate_published_base_reconciliation_required"
PUBLISHED_CI_REOBSERVATION = "remote_candidate_published_ci_reobservation_required"
ALREADY_PUBLISHED_CI_REOBSERVATION = "remote_candidate_already_published_ci_reobservation_required"

SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA64 = re.compile(r"^[0-9a-f]{64}$")
BRANCH = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]*$")


@dataclass(frozen=True)
class GitHubRemoteCandidateMaterializationResult:
    version: str
    status: str
    packet_id: str
    repository_full_name: str
    base_branch: str
    candidate_branch: str
    materialization_state: str
    candidate_retained: bool
    remote_objects_equivalent: bool
    git_commit_identity_equal: bool
    remote_candidate_published: bool
    remote_base_aligned: bool
    ci_reobservation_required: bool
    merge_candidate: bool
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
    text = str(value or "").strip()
    if optional and not text:
        return ""
    if SHA40.fullmatch(text) is None:
        blockers.append(name + "_invalid")
    return text


def _bool(value: Any, name: str, blockers: list[str]) -> bool:
    if not isinstance(value, bool):
        blockers.append(name + "_must_be_bool")
        return False
    return value


def _branch(value: Any, name: str, blockers: list[str]) -> str:
    text = str(value or "").strip()
    if (
        not text
        or BRANCH.fullmatch(text) is None
        or ".." in text
        or "@{" in text
        or "//" in text
        or text.endswith(("/", "."))
        or text.startswith(".")
        or text.endswith(".lock")
    ):
        blockers.append(name + "_invalid")
    return text


def _entries(value: Any, blockers: list[str]) -> list[dict[str, Any]]:
    if not isinstance(value, list) or not value:
        blockers.append("materialized_entries_missing")
        return []
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, raw in enumerate(value):
        if not isinstance(raw, Mapping):
            blockers.append(f"materialized_entry_{index}_not_object")
            continue
        path = str(raw.get("path", "")).strip()
        if not path or path in seen:
            blockers.append(f"materialized_entry_{index}_path_invalid")
            continue
        seen.add(path)
        mode = str(raw.get("mode", "")).strip()
        kind = str(raw.get("type", "")).strip()
        if mode not in {"100644", "100755", "120000"}:
            blockers.append(f"materialized_entry_{index}_mode_invalid")
        if kind != "blob":
            blockers.append(f"materialized_entry_{index}_type_invalid")
        local_digest = _digest(
            raw.get("local_content_digest"),
            f"materialized_entry_{index}_local_content_digest",
            blockers,
        )
        remote_digest = _digest(
            raw.get("remote_content_digest"),
            f"materialized_entry_{index}_remote_content_digest",
            blockers,
        )
        blob_sha = _commit(
            raw.get("remote_blob_sha"),
            f"materialized_entry_{index}_remote_blob_sha",
            blockers,
        )
        result.append(
            {
                "path": path,
                "mode": mode,
                "type": kind,
                "local_content_digest": local_digest,
                "remote_content_digest": remote_digest,
                "remote_blob_sha": blob_sha,
            }
        )
    return result


def build_github_remote_candidate_materialization(
    *,
    post_commit_packet: Mapping[str, Any],
    observation: Mapping[str, Any],
) -> GitHubRemoteCandidateMaterializationResult:
    source = _m(post_commit_packet)
    obs = _m(observation)
    blockers: list[str] = []
    warnings: list[str] = []

    if source.get("version") != SOURCE_VERSION:
        blockers.append("post_commit_packet_version_invalid")
    if obs.get("version") != OBSERVATION_VERSION:
        blockers.append("observation_version_invalid")

    source_digest = _sha(source)
    if _digest(
        obs.get("source_post_commit_packet_digest"),
        "source_post_commit_packet_digest",
        blockers,
    ) != source_digest:
        blockers.append("source_post_commit_packet_digest_mismatch")

    repository = str(obs.get("repository_full_name", "")).strip()
    if repository != "itakura-hidetoshi/KuuOS":
        blockers.append("repository_full_name_invalid")

    base_branch = _branch(obs.get("base_branch"), "base_branch", blockers)
    candidate_branch = _branch(obs.get("candidate_branch"), "candidate_branch", blockers)
    if candidate_branch == base_branch:
        blockers.append("candidate_branch_must_differ_from_base_branch")

    source_ready = bool(
        source.get("remote_publish_ready") is True
        and source.get("admission_state") == "remote_publish_candidate_ready"
    )
    source_evidence = _m(source.get("evidence"))
    local_commit_sha = _commit(
        source_evidence.get("commit_sha"),
        "source_local_commit_sha",
        blockers,
        optional=not source_ready,
    )
    local_parent_sha = _commit(
        source_evidence.get("commit_parent_sha"),
        "source_local_parent_sha",
        blockers,
        optional=not source_ready,
    )
    local_tree_digest = _digest(
        source_evidence.get("commit_tree_digest"),
        "source_local_tree_digest",
        blockers,
        optional=not source_ready,
    )
    local_admission_receipt = _digest(
        source_evidence.get("git_admission_receipt_digest"),
        "source_git_admission_receipt_digest",
        blockers,
        optional=not source_ready,
    )
    source_paths_digest = _digest(
        source_evidence.get("committed_changed_paths_digest"),
        "source_committed_changed_paths_digest",
        blockers,
        optional=not source_ready,
    )

    if not source_ready:
        packet_id = "kuuos-github-remote-materialization-" + _sha(
            {
                "source_digest": source_digest,
                "state": "not_applicable",
                "blockers": sorted(set(blockers)),
            }
        )[:16]
        return GitHubRemoteCandidateMaterializationResult(
            VERSION,
            OBSTRUCTED if blockers else NOT_APPLICABLE,
            packet_id,
            repository,
            base_branch,
            candidate_branch,
            "post_commit_packet_not_remote_publish_ready",
            bool(source.get("candidate_retained", True)),
            False,
            False,
            False,
            False,
            False,
            False,
            "return_to_v7_28_post_commit_coherence",
            {
                "source_post_commit_packet_digest": source_digest,
                "source_authority_transferred": False,
            },
            sorted(set(blockers)),
            warnings,
        )

    github_authority = _bool(
        obs.get("github_write_authority_ready"),
        "github_write_authority_ready",
        blockers,
    )
    external_action_allowed = _bool(
        obs.get("external_action_allowed"),
        "external_action_allowed",
        blockers,
    )
    materialization_attempted = _bool(
        obs.get("materialization_attempted"),
        "materialization_attempted",
        blockers,
    )
    branch_publication_attempted = _bool(
        obs.get("branch_publication_attempted"),
        "branch_publication_attempted",
        blockers,
    )

    remote_base_before = _commit(
        obs.get("remote_base_before_sha"),
        "remote_base_before_sha",
        blockers,
    )
    remote_base_tree_sha = _commit(
        obs.get("remote_base_tree_sha"),
        "remote_base_tree_sha",
        blockers,
    )
    remote_base_observation_digest = _digest(
        obs.get("remote_base_observation_digest"),
        "remote_base_observation_digest",
        blockers,
    )

    if remote_base_before != local_parent_sha:
        blockers.append("remote_base_before_does_not_match_local_commit_parent")

    entries: list[dict[str, Any]] = []
    materialization_receipt_digest = ""
    remote_tree_sha = ""
    remote_tree_digest = ""
    local_message_digest = ""
    remote_message_digest = ""
    remote_commit_sha = ""
    remote_commit_parent_sha = ""
    remote_object_observation_digest = ""

    if materialization_attempted:
        materialization_receipt_digest = _digest(
            obs.get("remote_object_materialization_receipt_digest"),
            "remote_object_materialization_receipt_digest",
            blockers,
        )
        entries = _entries(obs.get("materialized_entries"), blockers)
        if _sha([entry["path"] for entry in entries]) != source_paths_digest:
            blockers.append("materialized_changed_paths_digest_mismatch")
        for entry in entries:
            if entry["local_content_digest"] != entry["remote_content_digest"]:
                blockers.append("materialized_blob_content_digest_mismatch:" + entry["path"])

        remote_tree_sha = _commit(
            obs.get("remote_tree_sha"),
            "remote_tree_sha",
            blockers,
        )
        remote_tree_digest = _digest(
            obs.get("remote_tree_content_digest"),
            "remote_tree_content_digest",
            blockers,
        )
        if remote_tree_digest != local_tree_digest:
            blockers.append("remote_tree_content_digest_mismatch")

        local_message_digest = _digest(
            obs.get("local_commit_message_digest"),
            "local_commit_message_digest",
            blockers,
        )
        remote_message_digest = _digest(
            obs.get("remote_commit_message_digest"),
            "remote_commit_message_digest",
            blockers,
        )
        if local_message_digest != remote_message_digest:
            blockers.append("remote_commit_message_digest_mismatch")

        remote_commit_sha = _commit(
            obs.get("remote_commit_sha"),
            "remote_commit_sha",
            blockers,
        )
        remote_commit_parent_sha = _commit(
            obs.get("remote_commit_parent_sha"),
            "remote_commit_parent_sha",
            blockers,
        )
        if remote_commit_parent_sha != local_parent_sha:
            blockers.append("remote_commit_parent_mismatch")

        remote_object_observation_digest = _digest(
            obs.get("remote_object_observation_digest"),
            "remote_object_observation_digest",
            blockers,
        )

    git_commit_identity_equal = bool(
        materialization_attempted
        and remote_commit_sha
        and remote_commit_sha == local_commit_sha
    )

    remote_objects_equivalent = bool(
        materialization_attempted
        and not blockers
        and entries
        and remote_tree_digest == local_tree_digest
        and remote_message_digest == local_message_digest
        and remote_commit_parent_sha == local_parent_sha
        and materialization_receipt_digest
        and remote_object_observation_digest
    )

    branch_absent_before = _bool(
        obs.get("candidate_branch_absent_before"),
        "candidate_branch_absent_before",
        blockers,
    )
    preexisting_head = _commit(
        obs.get("candidate_branch_preexisting_head_sha"),
        "candidate_branch_preexisting_head_sha",
        blockers,
        optional=branch_absent_before,
    )
    branch_created = _bool(
        obs.get("candidate_branch_created"),
        "candidate_branch_created",
        blockers,
    )
    post_branch_head = _commit(
        obs.get("post_publish_candidate_branch_head_sha"),
        "post_publish_candidate_branch_head_sha",
        blockers,
        optional=not (branch_created or not branch_absent_before),
    )
    post_publish_observation_digest = _digest(
        obs.get("post_publish_remote_observation_digest"),
        "post_publish_remote_observation_digest",
        blockers,
        optional=not (branch_created or not branch_absent_before),
    )
    remote_base_after = _commit(
        obs.get("remote_base_after_sha"),
        "remote_base_after_sha",
        blockers,
        optional=not (branch_created or not branch_absent_before),
    )

    published = bool(
        remote_objects_equivalent
        and remote_commit_sha
        and post_branch_head == remote_commit_sha
        and post_publish_observation_digest
        and (
            (branch_absent_before and branch_publication_attempted and branch_created)
            or (
                not branch_absent_before
                and preexisting_head == remote_commit_sha
                and not branch_created
            )
        )
    )
    base_aligned = bool(
        published
        and remote_base_after
        and remote_base_after == local_parent_sha
    )

    partial_remote_objects_may_exist = bool(
        materialization_attempted and not remote_objects_equivalent
    )

    if not github_authority or not external_action_allowed:
        state = AUTHORITY_REQUIRED
        status = PARTIAL if not blockers else OBSTRUCTED
        next_route = "retain_local_publish_candidate_and_acquire_github_write_authority"
    elif not materialization_attempted:
        state = MATERIALIZATION_REQUIRED
        status = PARTIAL if not blockers else OBSTRUCTED
        next_route = "materialize_remote_git_objects_from_verified_local_candidate"
    elif blockers:
        state = MATERIALIZATION_OBSTRUCTION
        status = OBSTRUCTED
        next_route = "inspect_partial_remote_objects_and_reestablish_materialization_binding"
    elif not remote_objects_equivalent:
        state = MATERIALIZATION_OBSTRUCTION
        status = OBSTRUCTED
        next_route = "reestablish_remote_object_equivalence"
    elif branch_absent_before and not branch_publication_attempted:
        state = BRANCH_PUBLICATION_REQUIRED
        status = PARTIAL
        next_route = "create_remote_candidate_branch_from_materialized_commit"
    elif not branch_absent_before and preexisting_head != remote_commit_sha:
        state = BRANCH_RESELECTION_REQUIRED
        status = PARTIAL
        next_route = "retain_materialized_commit_and_select_fresh_candidate_branch"
    elif not published:
        state = MATERIALIZATION_OBSTRUCTION
        status = OBSTRUCTED
        next_route = "reobserve_remote_candidate_branch_and_materialized_commit"
    elif not base_aligned:
        state = PUBLISHED_BASE_RECONCILIATION
        status = PARTIAL
        next_route = "retain_published_candidate_and_reconcile_updated_base"
    elif branch_absent_before:
        state = PUBLISHED_CI_REOBSERVATION
        status = READY
        next_route = "fresh_remote_exact_head_and_ci_reobservation"
    else:
        state = ALREADY_PUBLISHED_CI_REOBSERVATION
        status = READY
        next_route = "fresh_remote_exact_head_and_ci_reobservation"

    merge_candidate = False
    ci_reobservation_required = published
    commit_presentation_relation = (
        "exact_git_commit_identity"
        if git_commit_identity_equal
        else (
            "content_parent_message_equivalent_distinct_git_commit_identity"
            if remote_objects_equivalent
            else "remote_commit_equivalence_unresolved"
        )
    )

    if remote_objects_equivalent and not git_commit_identity_equal:
        warnings.append(
            "remote_commit_sha_differs_from_local_commit_sha_due_to_commit_metadata_surface"
        )
    if partial_remote_objects_may_exist:
        warnings.append(
            "unreachable_remote_git_objects_may_exist_even_when_ref_publication_did_not_complete"
        )

    evidence = {
        "source_post_commit_packet_digest": source_digest,
        "source_git_admission_receipt_digest": local_admission_receipt,
        "local_commit_sha": local_commit_sha,
        "local_commit_parent_sha": local_parent_sha,
        "local_commit_tree_digest": local_tree_digest,
        "remote_base_before_sha": remote_base_before,
        "remote_base_tree_sha": remote_base_tree_sha,
        "remote_base_observation_digest": remote_base_observation_digest,
        "remote_object_materialization_receipt_digest": materialization_receipt_digest,
        "materialized_entries_digest": _sha(entries),
        "remote_tree_sha": remote_tree_sha,
        "remote_tree_content_digest": remote_tree_digest,
        "local_commit_message_digest": local_message_digest,
        "remote_commit_message_digest": remote_message_digest,
        "remote_commit_sha": remote_commit_sha,
        "remote_commit_parent_sha": remote_commit_parent_sha,
        "remote_object_observation_digest": remote_object_observation_digest,
        "candidate_branch_absent_before": branch_absent_before,
        "candidate_branch_preexisting_head_sha": preexisting_head,
        "candidate_branch_created": branch_created,
        "post_publish_candidate_branch_head_sha": post_branch_head,
        "post_publish_remote_observation_digest": post_publish_observation_digest,
        "remote_base_after_sha": remote_base_after,
        "commit_presentation_relation": commit_presentation_relation,
        "git_commit_identity_equal": git_commit_identity_equal,
        "remote_objects_equivalent": remote_objects_equivalent,
        "partial_remote_objects_may_exist": partial_remote_objects_may_exist,
        "remote_branch_creation_is_base_branch_mutation": False,
        "remote_publish_receipt_is_merge_authority": False,
        "remote_publish_receipt_is_ci_success": False,
        "raw_source_bytes_persisted": False,
        "source_authority_transferred": False,
    }

    packet_id = "kuuos-github-remote-materialization-" + _sha(
        {
            "source_digest": source_digest,
            "repository": repository,
            "base_branch": base_branch,
            "candidate_branch": candidate_branch,
            "state": state,
            "evidence": evidence,
            "blockers": sorted(set(blockers)),
            "warnings": sorted(set(warnings)),
        }
    )[:16]

    return GitHubRemoteCandidateMaterializationResult(
        VERSION,
        status,
        packet_id,
        repository,
        base_branch,
        candidate_branch,
        state,
        True,
        remote_objects_equivalent,
        git_commit_identity_equal,
        published,
        base_aligned,
        ci_reobservation_required,
        merge_candidate,
        next_route,
        evidence,
        sorted(set(blockers)),
        sorted(set(warnings)),
    )
