#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import hashlib
import re

from runtime.kuuos_repository_atomic_application_types_v0_92 import (
    RepositoryAtomicApplicationReceipt,
)
from runtime.kuuos_repository_commit_candidate_types_v0_93 import (
    CANDIDATE_CERTIFIED,
    GIT_OBJECT_FORMAT_SHA1 as CANDIDATE_OBJECT_FORMAT_SHA1,
    RepositoryCommitCandidateCertificate,
    RepositoryCommitCandidatePolicy,
    RepositoryParentTreeInventory,
)
from runtime.kuuos_repository_commit_candidate_v0_93 import (
    git_object_oid,
    repository_commit_candidate_certificate_issues,
)
from runtime.kuuos_repository_object_materialization_authorization_types_v0_94 import (
    AUTHORIZATION_GRANTED,
    AUTHORIZATION_REJECTED,
    GIT_OBJECT_FORMAT_SHA1,
    OBJECT_KINDS,
    RepositoryCandidateObject,
    RepositoryObjectDatabaseEntry,
    RepositoryObjectDatabaseObservation,
    RepositoryObjectMaterializationAuthorizationCertificate,
    RepositoryObjectMaterializationAuthorizationPolicy,
    RepositoryObjectMaterializationNonceStatusReceipt,
    RepositoryObjectMaterializationPlanItem,
    RepositoryObjectMaterializationScope,
    repository_object_database_observation_digest,
    repository_object_materialization_authorization_certificate_digest,
    repository_object_materialization_authorization_policy_digest,
    repository_object_materialization_nonce_status_receipt_digest,
    repository_object_materialization_scope_digest,
)
from runtime.kuuos_repository_structure_types_v0_79 import RepositorySnapshot

_HEX40 = re.compile(r"^[0-9a-f]{40}$")
_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_KIND_ORDER = {"blob": 0, "tree": 1, "commit": 2}


def _canonical_strings(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(values)))


def _payload_digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _commit_payload(certificate: RepositoryCommitCandidateCertificate) -> bytes:
    author = certificate.author
    committer = certificate.committer
    text = (
        f"tree {certificate.root_tree_oid}\n"
        f"parent {certificate.parent_commit_sha}\n"
        f"author {author.name} <{author.email}> {author.timestamp} {author.timezone}\n"
        f"committer {committer.name} <{committer.email}> "
        f"{committer.timestamp} {committer.timezone}\n"
        "\n"
        f"{certificate.message}"
    )
    return text.encode("utf-8")


def build_repository_object_materialization_authorization_policy(
    policy_id: str,
    *,
    allowed_repository_ids: tuple[str, ...],
    authorized_nonce_authority_ids: tuple[str, ...],
    max_authorization_lifetime_seconds: int,
    max_observation_age_seconds: int,
    max_nonce_status_age_seconds: int,
    max_new_object_count: int,
    max_new_payload_bytes: int,
) -> RepositoryObjectMaterializationAuthorizationPolicy:
    policy = RepositoryObjectMaterializationAuthorizationPolicy(
        policy_id=policy_id,
        allowed_repository_ids=_canonical_strings(allowed_repository_ids),
        authorized_nonce_authority_ids=_canonical_strings(
            authorized_nonce_authority_ids
        ),
        allowed_object_kinds=OBJECT_KINDS,
        max_authorization_lifetime_seconds=max_authorization_lifetime_seconds,
        max_observation_age_seconds=max_observation_age_seconds,
        max_nonce_status_age_seconds=max_nonce_status_age_seconds,
        max_new_object_count=max_new_object_count,
        max_new_payload_bytes=max_new_payload_bytes,
        require_object_database_source=True,
        require_working_tree_ignored=True,
        require_reference_nonmutation=True,
        policy_digest="",
    )
    policy = replace(
        policy,
        policy_digest=(
            repository_object_materialization_authorization_policy_digest(policy)
        ),
    )
    issues = repository_object_materialization_authorization_policy_issues(policy)
    if issues:
        raise ValueError(f"object_materialization_policy_invalid:{issues[0]}")
    return policy


def repository_object_materialization_authorization_policy_issues(
    policy: RepositoryObjectMaterializationAuthorizationPolicy,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not policy.policy_id:
        issues.append("object_materialization_policy_id_missing")
    for values, name in (
        (policy.allowed_repository_ids, "allowed_repository_ids"),
        (policy.authorized_nonce_authority_ids, "authorized_nonce_authority_ids"),
        (policy.allowed_object_kinds, "allowed_object_kinds"),
    ):
        if values != _canonical_strings(values):
            issues.append(f"object_materialization_{name}_not_canonical")
        if not values or any(not value for value in values):
            issues.append(f"object_materialization_{name}_invalid")
    if policy.allowed_object_kinds != OBJECT_KINDS:
        issues.append("object_materialization_object_kinds_invalid")
    bounds = (
        policy.max_authorization_lifetime_seconds,
        policy.max_observation_age_seconds,
        policy.max_nonce_status_age_seconds,
        policy.max_new_object_count,
        policy.max_new_payload_bytes,
    )
    if any(value <= 0 for value in bounds):
        issues.append("object_materialization_policy_bound_invalid")
    if not policy.require_object_database_source:
        issues.append("object_materialization_object_database_source_not_required")
    if not policy.require_working_tree_ignored:
        issues.append("object_materialization_working_tree_ignore_not_required")
    if not policy.require_reference_nonmutation:
        issues.append("object_materialization_reference_nonmutation_not_required")
    if policy.policy_digest != (
        repository_object_materialization_authorization_policy_digest(policy)
    ):
        issues.append("object_materialization_policy_digest_mismatch")
    return tuple(issues)


def _candidate_object_order_key(candidate: RepositoryCandidateObject) -> tuple:
    if candidate.kind == "tree":
        tree_origins = tuple(
            origin.removeprefix("tree:") for origin in candidate.origins
        )
        depth = max(
            0 if directory == "/" else directory.count("/") + 1
            for directory in tree_origins
        )
        return (_KIND_ORDER[candidate.kind], -depth, candidate.origins, candidate.oid)
    return (_KIND_ORDER[candidate.kind], 0, candidate.origins, candidate.oid)


def derive_repository_candidate_objects(
    certificate: RepositoryCommitCandidateCertificate,
    application_receipt: RepositoryAtomicApplicationReceipt,
    snapshot: RepositorySnapshot,
    parent_tree_inventory: RepositoryParentTreeInventory,
    candidate_policy: RepositoryCommitCandidatePolicy,
) -> tuple[RepositoryCandidateObject, ...]:
    issues = repository_commit_candidate_certificate_issues(
        certificate,
        application_receipt,
        snapshot,
        parent_tree_inventory,
        candidate_policy,
    )
    if issues:
        raise ValueError(f"commit_candidate_certificate_invalid:{issues[0]}")
    if certificate.status != CANDIDATE_CERTIFIED:
        raise ValueError("commit_candidate_not_certified")

    text_by_path = snapshot.texts
    raw: list[RepositoryCandidateObject] = []
    for blob in certificate.blob_candidates:
        if blob.path not in text_by_path:
            raise ValueError("materialization_blob_text_missing")
        payload = text_by_path[blob.path].encode("utf-8")
        candidate = RepositoryCandidateObject(
            kind="blob",
            oid=git_object_oid("blob", payload),
            payload_size=len(payload),
            payload_digest=_payload_digest(payload),
            origins=(f"blob:{blob.path}",),
        )
        if candidate.oid != blob.git_blob_oid or candidate.payload_size != blob.utf8_size:
            raise ValueError("materialization_blob_candidate_mismatch")
        raw.append(candidate)

    for tree in certificate.tree_candidates:
        if not (
            len(tree.entry_names)
            == len(tree.entry_modes)
            == len(tree.entry_oids)
        ):
            raise ValueError("materialization_tree_entry_arity_mismatch")
        payload = b"".join(
            f"{mode} {name}\0".encode("utf-8") + bytes.fromhex(oid)
            for name, mode, oid in zip(
                tree.entry_names,
                tree.entry_modes,
                tree.entry_oids,
                strict=True,
            )
        )
        directory = tree.directory if tree.directory else "/"
        candidate = RepositoryCandidateObject(
            kind="tree",
            oid=git_object_oid("tree", payload),
            payload_size=len(payload),
            payload_digest=_payload_digest(payload),
            origins=(f"tree:{directory}",),
        )
        if candidate.oid != tree.git_tree_oid:
            raise ValueError("materialization_tree_candidate_mismatch")
        raw.append(candidate)

    commit_payload = _commit_payload(certificate)
    commit_candidate = RepositoryCandidateObject(
        kind="commit",
        oid=git_object_oid("commit", commit_payload),
        payload_size=len(commit_payload),
        payload_digest=_payload_digest(commit_payload),
        origins=("commit:candidate",),
    )
    if (
        commit_candidate.oid != certificate.candidate_commit_oid
        or commit_candidate.payload_digest != certificate.commit_payload_digest
    ):
        raise ValueError("materialization_commit_candidate_mismatch")
    raw.append(commit_candidate)

    deduplicated: dict[str, RepositoryCandidateObject] = {}
    for candidate in raw:
        previous = deduplicated.get(candidate.oid)
        if previous is None:
            deduplicated[candidate.oid] = candidate
            continue
        if (
            previous.kind != candidate.kind
            or previous.payload_size != candidate.payload_size
            or previous.payload_digest != candidate.payload_digest
        ):
            raise ValueError("materialization_candidate_oid_collision")
        deduplicated[candidate.oid] = replace(
            previous,
            origins=_canonical_strings(previous.origins + candidate.origins),
        )

    result = tuple(sorted(deduplicated.values(), key=_candidate_object_order_key))
    if not result or result[-1].kind != "commit":
        raise ValueError("materialization_commit_object_missing")
    return result


def build_repository_object_database_observation(
    observation_id: str,
    *,
    repository_id: str,
    git_dir_fingerprint: str,
    object_format: str,
    source_commit_sha: str,
    queried_oids: tuple[str, ...],
    existing_objects: tuple[RepositoryObjectDatabaseEntry, ...],
    object_database_read: bool,
    working_tree_read: bool,
    observed_at_epoch_seconds: int,
) -> RepositoryObjectDatabaseObservation:
    observation = RepositoryObjectDatabaseObservation(
        observation_id=observation_id,
        repository_id=repository_id,
        git_dir_fingerprint=git_dir_fingerprint,
        object_format=object_format,
        source_commit_sha=source_commit_sha,
        queried_oids=_canonical_strings(queried_oids),
        existing_objects=tuple(
            sorted(existing_objects, key=lambda entry: (entry.oid, entry.kind))
        ),
        object_database_read=object_database_read,
        working_tree_read=working_tree_read,
        observed_at_epoch_seconds=observed_at_epoch_seconds,
        receipt_digest="",
    )
    observation = replace(
        observation,
        receipt_digest=repository_object_database_observation_digest(observation),
    )
    issues = repository_object_database_observation_issues(observation)
    if issues:
        raise ValueError(f"object_database_observation_invalid:{issues[0]}")
    return observation


def repository_object_database_observation_issues(
    observation: RepositoryObjectDatabaseObservation,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not observation.observation_id or not observation.repository_id:
        issues.append("object_database_observation_identity_missing")
    if not _HEX64.fullmatch(observation.git_dir_fingerprint):
        issues.append("object_database_git_dir_fingerprint_invalid")
    if not observation.object_format:
        issues.append("object_database_object_format_missing")
    if not _HEX40.fullmatch(observation.source_commit_sha):
        issues.append("object_database_source_commit_invalid")
    if observation.queried_oids != _canonical_strings(observation.queried_oids):
        issues.append("object_database_queried_oids_not_canonical")
    if any(not _HEX40.fullmatch(oid) for oid in observation.queried_oids):
        issues.append("object_database_queried_oid_invalid")
    entries = observation.existing_objects
    if entries != tuple(sorted(entries, key=lambda entry: (entry.oid, entry.kind))):
        issues.append("object_database_existing_objects_not_canonical")
    if len({entry.oid for entry in entries}) != len(entries):
        issues.append("object_database_existing_oid_duplicate")
    for entry in entries:
        if entry.kind not in OBJECT_KINDS:
            issues.append("object_database_existing_kind_invalid")
            break
        if not _HEX40.fullmatch(entry.oid):
            issues.append("object_database_existing_oid_invalid")
            break
        if entry.payload_size < 0 or not _HEX64.fullmatch(entry.payload_digest):
            issues.append("object_database_existing_payload_invalid")
            break
        if entry.oid not in observation.queried_oids:
            issues.append("object_database_unqueried_existing_object")
            break
    if observation.observed_at_epoch_seconds < 0:
        issues.append("object_database_observed_at_negative")
    if observation.receipt_digest != repository_object_database_observation_digest(
        observation
    ):
        issues.append("object_database_observation_digest_mismatch")
    return tuple(issues)


def build_repository_object_materialization_scope(
    scope_id: str,
    certificate: RepositoryCommitCandidateCertificate,
    policy: RepositoryObjectMaterializationAuthorizationPolicy,
    observation: RepositoryObjectDatabaseObservation,
    *,
    authorization_nonce: str,
    issued_at_epoch_seconds: int,
    expires_at_epoch_seconds: int,
) -> RepositoryObjectMaterializationScope:
    scope = RepositoryObjectMaterializationScope(
        scope_id=scope_id,
        candidate_certificate_digest=certificate.certificate_digest,
        authorization_policy_digest=policy.policy_digest,
        object_database_observation_digest=observation.receipt_digest,
        repository_id=observation.repository_id,
        git_dir_fingerprint=observation.git_dir_fingerprint,
        parent_commit_sha=certificate.parent_commit_sha,
        candidate_commit_oid=certificate.candidate_commit_oid,
        authorization_nonce=authorization_nonce,
        issued_at_epoch_seconds=issued_at_epoch_seconds,
        expires_at_epoch_seconds=expires_at_epoch_seconds,
        scope_digest="",
    )
    scope = replace(
        scope,
        scope_digest=repository_object_materialization_scope_digest(scope),
    )
    issues = repository_object_materialization_scope_issues(scope)
    if issues:
        raise ValueError(f"object_materialization_scope_invalid:{issues[0]}")
    return scope


def repository_object_materialization_scope_issues(
    scope: RepositoryObjectMaterializationScope,
) -> tuple[str, ...]:
    issues: list[str] = []
    required = (
        scope.scope_id,
        scope.candidate_certificate_digest,
        scope.authorization_policy_digest,
        scope.object_database_observation_digest,
        scope.repository_id,
        scope.authorization_nonce,
    )
    if any(not value for value in required):
        issues.append("object_materialization_scope_required_field_missing")
    for digest in (
        scope.candidate_certificate_digest,
        scope.authorization_policy_digest,
        scope.object_database_observation_digest,
        scope.git_dir_fingerprint,
    ):
        if not _HEX64.fullmatch(digest):
            issues.append("object_materialization_scope_digest_invalid")
            break
    if not _HEX40.fullmatch(scope.parent_commit_sha):
        issues.append("object_materialization_scope_parent_invalid")
    if not _HEX40.fullmatch(scope.candidate_commit_oid):
        issues.append("object_materialization_scope_candidate_oid_invalid")
    if scope.issued_at_epoch_seconds < 0:
        issues.append("object_materialization_scope_issued_at_negative")
    if scope.expires_at_epoch_seconds <= scope.issued_at_epoch_seconds:
        issues.append("object_materialization_scope_expiry_invalid")
    if scope.scope_digest != repository_object_materialization_scope_digest(scope):
        issues.append("object_materialization_scope_digest_mismatch")
    return tuple(issues)


def build_repository_object_materialization_nonce_status_receipt(
    status_id: str,
    scope: RepositoryObjectMaterializationScope,
    *,
    authority_id: str,
    checked_at_epoch_seconds: int,
    registry_snapshot_digest: str,
    consumed: bool,
    revoked: bool,
) -> RepositoryObjectMaterializationNonceStatusReceipt:
    receipt = RepositoryObjectMaterializationNonceStatusReceipt(
        status_id=status_id,
        authorization_nonce=scope.authorization_nonce,
        authorization_scope_digest=scope.scope_digest,
        authority_id=authority_id,
        checked_at_epoch_seconds=checked_at_epoch_seconds,
        registry_snapshot_digest=registry_snapshot_digest,
        consumed=consumed,
        revoked=revoked,
        receipt_digest="",
    )
    receipt = replace(
        receipt,
        receipt_digest=(
            repository_object_materialization_nonce_status_receipt_digest(receipt)
        ),
    )
    issues = repository_object_materialization_nonce_status_receipt_issues(receipt)
    if issues:
        raise ValueError(f"object_materialization_nonce_status_invalid:{issues[0]}")
    return receipt


def repository_object_materialization_nonce_status_receipt_issues(
    receipt: RepositoryObjectMaterializationNonceStatusReceipt,
) -> tuple[str, ...]:
    issues: list[str] = []
    required = (
        receipt.status_id,
        receipt.authorization_nonce,
        receipt.authorization_scope_digest,
        receipt.authority_id,
        receipt.registry_snapshot_digest,
    )
    if any(not value for value in required):
        issues.append("object_materialization_nonce_required_field_missing")
    if not _HEX64.fullmatch(receipt.authorization_scope_digest):
        issues.append("object_materialization_nonce_scope_digest_invalid")
    if not _HEX64.fullmatch(receipt.registry_snapshot_digest):
        issues.append("object_materialization_nonce_registry_digest_invalid")
    if receipt.checked_at_epoch_seconds < 0:
        issues.append("object_materialization_nonce_checked_at_negative")
    if receipt.receipt_digest != (
        repository_object_materialization_nonce_status_receipt_digest(receipt)
    ):
        issues.append("object_materialization_nonce_receipt_digest_mismatch")
    return tuple(issues)


def _materialization_plan(
    candidate_objects: tuple[RepositoryCandidateObject, ...],
    observation: RepositoryObjectDatabaseObservation,
) -> tuple[
    tuple[RepositoryObjectMaterializationPlanItem, ...],
    bool,
    int,
    int,
    int,
]:
    existing_by_oid = {entry.oid: entry for entry in observation.existing_objects}
    plan: list[RepositoryObjectMaterializationPlanItem] = []
    collision_free = True
    write_order = 0
    reused_count = 0
    new_count = 0
    new_bytes = 0
    for candidate in candidate_objects:
        existing = existing_by_oid.get(candidate.oid)
        exact = bool(
            existing is not None
            and existing.kind == candidate.kind
            and existing.payload_size == candidate.payload_size
            and existing.payload_digest == candidate.payload_digest
        )
        if existing is not None and not exact:
            collision_free = False
        write_required = existing is None
        item_order = write_order if write_required else -1
        if write_required:
            write_order += 1
            new_count += 1
            new_bytes += candidate.payload_size
        elif exact:
            reused_count += 1
        plan.append(
            RepositoryObjectMaterializationPlanItem(
                kind=candidate.kind,
                oid=candidate.oid,
                payload_size=candidate.payload_size,
                payload_digest=candidate.payload_digest,
                origins=candidate.origins,
                already_present_exact=exact,
                write_required=write_required,
                write_order=item_order,
            )
        )
    return tuple(plan), collision_free, reused_count, new_count, new_bytes


def _construct_authorization_certificate(
    authorization_id: str,
    candidate_certificate: RepositoryCommitCandidateCertificate,
    candidate_objects: tuple[RepositoryCandidateObject, ...],
    policy: RepositoryObjectMaterializationAuthorizationPolicy,
    scope: RepositoryObjectMaterializationScope,
    observation: RepositoryObjectDatabaseObservation,
    nonce_status: RepositoryObjectMaterializationNonceStatusReceipt,
    *,
    evaluated_at_epoch_seconds: int,
) -> RepositoryObjectMaterializationAuthorizationCertificate:
    plan, collision_free, reused_count, new_count, new_bytes = (
        _materialization_plan(candidate_objects, observation)
    )
    existing_by_oid = {entry.oid: entry for entry in observation.existing_objects}
    parent_entry = existing_by_oid.get(candidate_certificate.parent_commit_sha)
    expected_queries = _canonical_strings(
        tuple(item.oid for item in candidate_objects)
        + (candidate_certificate.parent_commit_sha,)
    )

    candidate_binding_exact = (
        scope.candidate_certificate_digest == candidate_certificate.certificate_digest
        and scope.parent_commit_sha == candidate_certificate.parent_commit_sha
        and scope.candidate_commit_oid == candidate_certificate.candidate_commit_oid
    )
    policy_binding_exact = scope.authorization_policy_digest == policy.policy_digest
    observation_binding_exact = (
        scope.object_database_observation_digest == observation.receipt_digest
    )
    repository_allowed = observation.repository_id in policy.allowed_repository_ids
    repository_identity_exact = (
        scope.repository_id == observation.repository_id
        and scope.git_dir_fingerprint == observation.git_dir_fingerprint
    )
    object_format_exact = (
        observation.object_format == GIT_OBJECT_FORMAT_SHA1
        and candidate_certificate.git_object_format == CANDIDATE_OBJECT_FORMAT_SHA1
    )
    source_parent_present = bool(
        observation.source_commit_sha == candidate_certificate.parent_commit_sha
        and parent_entry is not None
        and parent_entry.kind == "commit"
    )
    queried_object_set_exact = observation.queried_oids == expected_queries
    object_kinds_allowed = all(
        item.kind in policy.allowed_object_kinds for item in candidate_objects
    )
    object_count_within_policy = new_count <= policy.max_new_object_count
    payload_bytes_within_policy = new_bytes <= policy.max_new_payload_bytes
    observation_age = evaluated_at_epoch_seconds - observation.observed_at_epoch_seconds
    observation_fresh = 0 <= observation_age <= policy.max_observation_age_seconds
    object_database_source = (
        observation.object_database_read and policy.require_object_database_source
    )
    working_tree_ignored = (
        not observation.working_tree_read and policy.require_working_tree_ignored
    )
    nonce_scope_bound = (
        nonce_status.authorization_nonce == scope.authorization_nonce
        and nonce_status.authorization_scope_digest == scope.scope_digest
    )
    nonce_authority_authorized = (
        nonce_status.authority_id in policy.authorized_nonce_authority_ids
    )
    nonce_age = evaluated_at_epoch_seconds - nonce_status.checked_at_epoch_seconds
    nonce_status_fresh = 0 <= nonce_age <= policy.max_nonce_status_age_seconds
    authorization_lifetime_within_policy = (
        scope.expires_at_epoch_seconds - scope.issued_at_epoch_seconds
        <= policy.max_authorization_lifetime_seconds
    )
    authorization_not_expired = (
        scope.issued_at_epoch_seconds
        <= evaluated_at_epoch_seconds
        <= scope.expires_at_epoch_seconds
    )
    no_future_evidence = all(
        value <= evaluated_at_epoch_seconds
        for value in (
            scope.issued_at_epoch_seconds,
            observation.observed_at_epoch_seconds,
            nonce_status.checked_at_epoch_seconds,
        )
    )
    reference_nonmutation_required = policy.require_reference_nonmutation
    existing_objects_reused_exactly = all(
        (not item.already_present_exact and item.write_required)
        or (item.already_present_exact and not item.write_required)
        for item in plan
    )

    grant_inputs = (
        candidate_binding_exact,
        policy_binding_exact,
        observation_binding_exact,
        repository_allowed,
        repository_identity_exact,
        object_format_exact,
        source_parent_present,
        queried_object_set_exact,
        collision_free,
        existing_objects_reused_exactly,
        object_kinds_allowed,
        object_count_within_policy,
        payload_bytes_within_policy,
        observation_fresh,
        object_database_source,
        working_tree_ignored,
        nonce_authority_authorized,
        nonce_scope_bound,
        nonce_status_fresh,
        not nonce_status.consumed,
        not nonce_status.revoked,
        authorization_lifetime_within_policy,
        authorization_not_expired,
        no_future_evidence,
        reference_nonmutation_required,
    )
    granted = all(grant_inputs)
    certificate = RepositoryObjectMaterializationAuthorizationCertificate(
        authorization_id=authorization_id,
        status=AUTHORIZATION_GRANTED if granted else AUTHORIZATION_REJECTED,
        candidate_certificate_digest=candidate_certificate.certificate_digest,
        authorization_policy_digest=policy.policy_digest,
        materialization_scope_digest=scope.scope_digest,
        object_database_observation_digest=observation.receipt_digest,
        nonce_status_receipt_digest=nonce_status.receipt_digest,
        repository_id=observation.repository_id,
        git_dir_fingerprint=observation.git_dir_fingerprint,
        parent_commit_sha=candidate_certificate.parent_commit_sha,
        candidate_commit_oid=candidate_certificate.candidate_commit_oid,
        plan_items=plan,
        unique_candidate_object_count=len(candidate_objects),
        reused_existing_object_count=reused_count,
        new_object_count=new_count,
        new_payload_bytes=new_bytes,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
        candidate_certificate_valid=True,
        candidate_binding_exact=candidate_binding_exact,
        policy_binding_exact=policy_binding_exact,
        scope_binding_exact=(
            candidate_binding_exact
            and policy_binding_exact
            and observation_binding_exact
        ),
        observation_binding_exact=observation_binding_exact,
        repository_allowed=repository_allowed,
        repository_identity_exact=repository_identity_exact,
        object_format_exact=object_format_exact,
        source_parent_present=source_parent_present,
        queried_object_set_exact=queried_object_set_exact,
        candidate_object_payloads_exact=True,
        existing_objects_collision_free=collision_free,
        existing_objects_reused_exactly=existing_objects_reused_exactly,
        object_order_deterministic=True,
        object_kinds_allowed=object_kinds_allowed,
        object_count_within_policy=object_count_within_policy,
        payload_bytes_within_policy=payload_bytes_within_policy,
        observation_fresh=observation_fresh,
        object_database_source=object_database_source,
        working_tree_ignored=working_tree_ignored,
        nonce_authority_authorized=nonce_authority_authorized,
        nonce_scope_bound=nonce_scope_bound,
        nonce_status_fresh=nonce_status_fresh,
        nonce_unused=not nonce_status.consumed,
        nonce_not_revoked=not nonce_status.revoked,
        authorization_lifetime_within_policy=authorization_lifetime_within_policy,
        authorization_not_expired=authorization_not_expired,
        no_future_evidence=no_future_evidence,
        reference_nonmutation_required=reference_nonmutation_required,
        materialization_authorization_granted=granted,
        single_use_materialization_eligible=granted,
        object_database_write_authority_granted=granted,
        commit_object_materialization_authority_granted=(
            granted and any(item.kind == "commit" for item in plan)
        ),
        object_database_write_performed=False,
        commit_object_written=False,
        index_write_performed=False,
        working_tree_write_performed=False,
        reference_mutation_authority_granted=False,
        reference_mutated=False,
        signing_performed=False,
        certificate_digest="",
    )
    return replace(
        certificate,
        certificate_digest=(
            repository_object_materialization_authorization_certificate_digest(
                certificate
            )
        ),
    )


def authorize_repository_object_materialization(
    authorization_id: str,
    candidate_certificate: RepositoryCommitCandidateCertificate,
    application_receipt: RepositoryAtomicApplicationReceipt,
    snapshot: RepositorySnapshot,
    parent_tree_inventory: RepositoryParentTreeInventory,
    candidate_policy: RepositoryCommitCandidatePolicy,
    policy: RepositoryObjectMaterializationAuthorizationPolicy,
    scope: RepositoryObjectMaterializationScope,
    observation: RepositoryObjectDatabaseObservation,
    nonce_status: RepositoryObjectMaterializationNonceStatusReceipt,
    *,
    evaluated_at_epoch_seconds: int,
) -> RepositoryObjectMaterializationAuthorizationCertificate:
    if not authorization_id:
        raise ValueError("object_materialization_authorization_id_missing")
    if evaluated_at_epoch_seconds < 0:
        raise ValueError("object_materialization_evaluated_at_negative")
    for issues, prefix in (
        (
            repository_object_materialization_authorization_policy_issues(policy),
            "object_materialization_policy_invalid",
        ),
        (
            repository_object_materialization_scope_issues(scope),
            "object_materialization_scope_invalid",
        ),
        (
            repository_object_database_observation_issues(observation),
            "object_database_observation_invalid",
        ),
        (
            repository_object_materialization_nonce_status_receipt_issues(
                nonce_status
            ),
            "object_materialization_nonce_status_invalid",
        ),
    ):
        if issues:
            raise ValueError(f"{prefix}:{issues[0]}")

    candidate_objects = derive_repository_candidate_objects(
        candidate_certificate,
        application_receipt,
        snapshot,
        parent_tree_inventory,
        candidate_policy,
    )
    certificate = _construct_authorization_certificate(
        authorization_id,
        candidate_certificate,
        candidate_objects,
        policy,
        scope,
        observation,
        nonce_status,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
    )
    issues = repository_object_materialization_authorization_certificate_issues(
        certificate,
        candidate_certificate,
        application_receipt,
        snapshot,
        parent_tree_inventory,
        candidate_policy,
        policy,
        scope,
        observation,
        nonce_status,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
    )
    if issues:
        raise ValueError(f"object_materialization_certificate_invalid:{issues[0]}")
    return certificate


def repository_object_materialization_authorization_certificate_issues(
    certificate: RepositoryObjectMaterializationAuthorizationCertificate,
    candidate_certificate: RepositoryCommitCandidateCertificate,
    application_receipt: RepositoryAtomicApplicationReceipt,
    snapshot: RepositorySnapshot,
    parent_tree_inventory: RepositoryParentTreeInventory,
    candidate_policy: RepositoryCommitCandidatePolicy,
    policy: RepositoryObjectMaterializationAuthorizationPolicy,
    scope: RepositoryObjectMaterializationScope,
    observation: RepositoryObjectDatabaseObservation,
    nonce_status: RepositoryObjectMaterializationNonceStatusReceipt,
    *,
    evaluated_at_epoch_seconds: int,
) -> tuple[str, ...]:
    issues: list[str] = []
    try:
        candidate_objects = derive_repository_candidate_objects(
            candidate_certificate,
            application_receipt,
            snapshot,
            parent_tree_inventory,
            candidate_policy,
        )
        expected = _construct_authorization_certificate(
            certificate.authorization_id,
            candidate_certificate,
            candidate_objects,
            policy,
            scope,
            observation,
            nonce_status,
            evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
        )
    except ValueError as error:
        issues.append(str(error))
        return tuple(issues)

    if certificate.to_dict() != expected.to_dict():
        issues.append("object_materialization_recomputation_mismatch")
    if certificate.status not in (AUTHORIZATION_GRANTED, AUTHORIZATION_REJECTED):
        issues.append("object_materialization_status_invalid")
    if certificate.object_database_write_performed:
        issues.append("unexpected_object_database_write")
    if certificate.commit_object_written:
        issues.append("unexpected_commit_object_write")
    if certificate.index_write_performed:
        issues.append("unexpected_index_write")
    if certificate.working_tree_write_performed:
        issues.append("unexpected_working_tree_write")
    if certificate.reference_mutation_authority_granted:
        issues.append("unexpected_reference_mutation_authority")
    if certificate.reference_mutated:
        issues.append("unexpected_reference_mutation")
    if certificate.signing_performed:
        issues.append("unexpected_signing")
    if certificate.certificate_digest != (
        repository_object_materialization_authorization_certificate_digest(
            certificate
        )
    ):
        issues.append("object_materialization_certificate_digest_mismatch")
    return tuple(issues)
