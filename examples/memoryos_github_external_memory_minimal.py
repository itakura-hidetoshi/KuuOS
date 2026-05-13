#!/usr/bin/env python3
"""Minimal KuuOS MemoryOS GitHub external memory example.

This example is stdlib-only. It does not call the GitHub API.
It shows how MemoryOS should normalize a GitHub pointer as external memory
without granting truth, proof, clinical, Ten'i, world-update, or execution authority.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from hashlib import sha256
from typing import Literal

MemoryKind = Literal[
    "pointer_memory",
    "evidence_memory",
    "semantic_digest_memory",
    "repair_lineage_memory",
    "conflict_visibility_memory",
]

RefType = Literal[
    "commit",
    "file",
    "issue",
    "pull_request",
    "review_comment",
    "workflow_run",
    "artifact",
    "release",
    "tag",
]

Uncertainty = Literal["low", "medium", "high"]


@dataclass(frozen=True)
class ExternalMemoryConstraints:
    no_overwrite: bool = True
    no_execution_authority: bool = True
    no_truth_authority: bool = True
    no_proof_authority: bool = True
    no_clinical_authority: bool = True
    no_teni_authority: bool = True


@dataclass(frozen=True)
class ExternalMemoryLineage:
    parent_memory_ids: tuple[str, ...] = ()
    supersedes: tuple[str, ...] = ()
    tombstones: tuple[str, ...] = ()


@dataclass(frozen=True)
class GitHubExternalMemoryRecord:
    memory_id: str
    memory_kind: MemoryKind
    created_at: str
    source_system: Literal["github"]
    repository: str
    ref_type: RefType
    ref: str
    commit_sha: str | None
    path: str | None
    url: str | None
    content_sha256: str | None
    summary: str
    authority: Literal["external_pointer_only"]
    uncertainty: Uncertainty
    lineage: ExternalMemoryLineage = field(default_factory=ExternalMemoryLineage)
    constraints: ExternalMemoryConstraints = field(default_factory=ExternalMemoryConstraints)


def stable_memory_id(repository: str, ref_type: str, ref: str, path: str | None = None) -> str:
    raw = "|".join([repository, ref_type, ref, path or ""])
    return "ghmem_" + sha256(raw.encode("utf-8")).hexdigest()[:24]


def content_hash(text: str) -> str:
    return sha256(text.encode("utf-8")).hexdigest()


def create_pointer_record(
    *,
    repository: str,
    ref_type: RefType,
    ref: str,
    summary: str,
    commit_sha: str | None = None,
    path: str | None = None,
    url: str | None = None,
    content: str | None = None,
    memory_kind: MemoryKind = "pointer_memory",
    uncertainty: Uncertainty = "low",
) -> GitHubExternalMemoryRecord:
    return GitHubExternalMemoryRecord(
        memory_id=stable_memory_id(repository, ref_type, ref, path),
        memory_kind=memory_kind,
        created_at=datetime.now(timezone.utc).isoformat(),
        source_system="github",
        repository=repository,
        ref_type=ref_type,
        ref=ref,
        commit_sha=commit_sha,
        path=path,
        url=url,
        content_sha256=content_hash(content) if content is not None else None,
        summary=summary,
        authority="external_pointer_only",
        uncertainty=uncertainty,
    )


def validate_record(record: GitHubExternalMemoryRecord) -> list[str]:
    errors: list[str] = []

    if record.source_system != "github":
        errors.append("source_system must be github")
    if record.authority != "external_pointer_only":
        errors.append("authority must be external_pointer_only")
    if record.ref_type == "file" and not record.path:
        errors.append("file records require path")
    if record.ref_type == "commit" and not record.commit_sha:
        errors.append("commit records require commit_sha")
    if record.ref in {"main", "master", "HEAD"} and record.commit_sha is None:
        errors.append("moving branch or HEAD requires a pinned commit_sha")

    constraints = record.constraints
    required_true = {
        "no_overwrite": constraints.no_overwrite,
        "no_execution_authority": constraints.no_execution_authority,
        "no_truth_authority": constraints.no_truth_authority,
        "no_proof_authority": constraints.no_proof_authority,
        "no_clinical_authority": constraints.no_clinical_authority,
        "no_teni_authority": constraints.no_teni_authority,
    }
    for name, value in required_true.items():
        if value is not True:
            errors.append(f"constraint must remain true: {name}")

    if record.memory_kind == "semantic_digest_memory" and not record.content_sha256:
        errors.append("semantic digest memory should include content_sha256 or source evidence hash")

    return errors


def compile_context_candidate(record: GitHubExternalMemoryRecord) -> dict[str, object]:
    """Expose a non-authoritative recall candidate to MemoryOS compile_context."""
    return {
        "memory_id": record.memory_id,
        "source": "github_external_memory",
        "repository": record.repository,
        "ref_type": record.ref_type,
        "ref": record.ref,
        "commit_sha": record.commit_sha,
        "path": record.path,
        "summary": record.summary,
        "authority": record.authority,
        "uncertainty": record.uncertainty,
        "may_update_world_directly": False,
        "may_execute": False,
        "may_claim_truth": False,
    }


def main() -> None:
    record = create_pointer_record(
        repository="itakura-hidetoshi/KuuOS",
        ref_type="commit",
        ref="ef0115d5fcfc6b1bea6aa395f15da34be94c5eb7",
        commit_sha="ef0115d5fcfc6b1bea6aa395f15da34be94c5eb7",
        url="https://github.com/itakura-hidetoshi/KuuOS/commit/ef0115d5fcfc6b1bea6aa395f15da34be94c5eb7",
        summary="Pointer to a KuuOS commit used as external MemoryOS evidence.",
        memory_kind="evidence_memory",
    )
    errors = validate_record(record)
    if errors:
        raise SystemExit("FAIL: " + "; ".join(errors))

    candidate = compile_context_candidate(record)
    assert candidate["may_execute"] is False
    assert candidate["may_claim_truth"] is False
    assert candidate["may_update_world_directly"] is False

    print("PASS: MemoryOS GitHub external memory minimal example")
    print(asdict(record))


if __name__ == "__main__":
    main()
