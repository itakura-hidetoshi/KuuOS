#!/usr/bin/env python3
"""Minimal KuuOS MemoryOS GitHub external memory example."""

from __future__ import annotations

from dataclasses import dataclass, asdict
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
    summary: str
    authority: Literal["external_pointer_only"]
    uncertainty: Literal["low", "medium", "high"]
    no_overwrite: bool = True
    no_execution_authority: bool = True
    no_truth_authority: bool = True
    no_proof_authority: bool = True
    no_clinical_authority: bool = True
    no_teni_authority: bool = True


def stable_memory_id(repository: str, ref_type: str, ref: str) -> str:
    raw = f"{repository}|{ref_type}|{ref}"
    return "ghmem_" + sha256(raw.encode("utf-8")).hexdigest()[:24]


def create_pointer_record() -> GitHubExternalMemoryRecord:
    commit = "2213be4b8a772f7b998dc0d90fcf0c1290a600db"
    return GitHubExternalMemoryRecord(
        memory_id=stable_memory_id("itakura-hidetoshi/KuuOS", "commit", commit),
        memory_kind="evidence_memory",
        created_at=datetime.now(timezone.utc).isoformat(),
        source_system="github",
        repository="itakura-hidetoshi/KuuOS",
        ref_type="commit",
        ref=commit,
        commit_sha=commit,
        path=None,
        url=f"https://github.com/itakura-hidetoshi/KuuOS/commit/{commit}",
        summary="Pointer to a KuuOS commit used as external MemoryOS evidence.",
        authority="external_pointer_only",
        uncertainty="low",
    )


def validate_record(record: GitHubExternalMemoryRecord) -> list[str]:
    errors: list[str] = []
    if record.source_system != "github":
        errors.append("source_system must be github")
    if record.authority != "external_pointer_only":
        errors.append("authority must be external_pointer_only")
    if record.ref_type == "commit" and record.commit_sha != record.ref:
        errors.append("commit memory must pin commit_sha")
    if record.ref in {"HEAD", "main", "master"} and record.commit_sha is None:
        errors.append("moving ref requires pinned commit_sha")
    for field in (
        "no_overwrite",
        "no_execution_authority",
        "no_truth_authority",
        "no_proof_authority",
        "no_clinical_authority",
        "no_teni_authority",
    ):
        if getattr(record, field) is not True:
            errors.append(f"required constraint is false: {field}")
    return errors


def compile_context_candidate(record: GitHubExternalMemoryRecord) -> dict[str, object]:
    return {
        "memory_id": record.memory_id,
        "source": "github_external_memory",
        "repository": record.repository,
        "ref_type": record.ref_type,
        "ref": record.ref,
        "commit_sha": record.commit_sha,
        "summary": record.summary,
        "authority": record.authority,
        "uncertainty": record.uncertainty,
        "may_update_world_directly": False,
        "may_execute": False,
        "may_claim_truth": False,
    }


def main() -> None:
    record = create_pointer_record()
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
