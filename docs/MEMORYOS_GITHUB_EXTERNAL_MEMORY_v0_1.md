# MemoryOS GitHub External Memory v0.1

## 空OS MemoryOS GitHub 外部メモリー規約

This document defines GitHub as an external MemoryOS surface.

GitHub may store durable pointers, commits, issues, pull requests, workflow runs, artifacts, release references, validation outputs, and repair lineage records.

GitHub is not MemoryOS authority.

## Core Rule

```text
GitHub_external_memory_is_pointer_and_evidence_surface_not_memory_authority
```

A GitHub record can show that a repository event, validation event, review event, or release-surface event occurred at a specific external state.

A GitHub record cannot by itself decide truth, proof completion, clinical validity, Ten'i, world-state update, MemoryOS overwrite, or execution permission.

## Memory Modes

```text
pointer_memory
  repo, path, commit SHA, issue, PR, release, artifact, workflow pointer

evidence_memory
  externally reviewable validation output, CI log, release packet, audit receipt

semantic_digest_memory
  non-authoritative summary for recall; never source evidence

repair_lineage_memory
  issue -> PR -> review -> commit -> validator -> release lineage

conflict_visibility_memory
  contradiction, stale reference, supersession, tombstone, unresolved premise debt
```

## Record Schema

```yaml
memory_id: string
memory_kind: pointer_memory | evidence_memory | semantic_digest_memory | repair_lineage_memory | conflict_visibility_memory
created_at: ISO-8601 timestamp
source_system: github
repository: owner/name
ref_type: commit | file | issue | pull_request | review_comment | workflow_run | artifact | release | tag
ref: string
commit_sha: string | null
path: string | null
url: string | null
content_sha256: string | null
summary: string
authority: external_pointer_only
uncertainty: low | medium | high
constraints:
  no_overwrite: true
  no_execution_authority: true
  no_truth_authority: true
  no_proof_authority: true
  no_clinical_authority: true
  no_teni_authority: true
```

## Write Protocol

```text
observe_github_surface
  -> extract_stable_pointer
  -> classify_memory_kind
  -> normalize_external_memory_record
  -> compute_content_hash_when_available
  -> append_record_under_memoryos/external/github
  -> validate_record
  -> expose_as_compile_context_candidate
```

Recommended path:

```text
memoryos/external/github/YYYY/MM/<memory_id>.yaml
```

Indexes may be stored under:

```text
memoryos/external/github/indexes/
```

Indexes are recall aids, not authority.

## Recall Protocol

```text
input question
  -> search recall index
  -> retrieve stable GitHub pointers
  -> prefer commit SHA over branch name
  -> fetch source evidence when needed
  -> compare current surface with pinned surface
  -> expose conflicts and stale references
  -> compile_context with uncertainty visible
```

## Non-Authority Fixed Points

```text
GitHub_external_memory_is_pointer_and_evidence_surface_not_memory_authority
GitHub_commit_is_evidence_not_truth
GitHub_issue_is_discussion_not_memory_authority
GitHub_PR_is_proposal_not_memory_authority
GitHub_CI_pass_is_validation_signal_not_truth
GitHub_branch_HEAD_is_not_stable_memory
GitHub_release_is_public_surface_not_proof_completion
semantic_digest_is_not_source_evidence
MemoryOS_compile_context_must_expose_uncertainty
MemoryOS_no_silent_overwrite
MemoryOS_lineage_preserved
MemoryOS_conflict_visible
MemoryOS_append_only_external_pointer
no_execution_authority
no_clinical_authority
no_teni_authority
no_world_update_authority
```

## Validation

```bash
make memoryos-github-external-memory-checks
```

Expected output:

```text
PASS: KuuOS MemoryOS GitHub external memory surface v0.1 validates
```

## Version

Version: v0.1
Date: 2026-05-14
Author: Hidetoshi Itakura / 板倉英俊
Release mode: append-only / tighten-only / overwrite-forbidden
