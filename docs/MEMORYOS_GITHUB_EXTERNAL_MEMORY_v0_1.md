# MemoryOS GitHub External Memory v0.1

## 空OS MemoryOS GitHub 外部メモリー規約

This document defines how KuuOS MemoryOS may use GitHub as an external memory surface.

GitHub may store durable pointers, append-only ledgers, issues, pull requests, commits, tags, Actions logs, validation artifacts, release packets, and recall indexes.

GitHub must not become MemoryOS authority, truth authority, proof authority, clinical authority, Ten'i authority, or execution authority.

## 1. Purpose

MemoryOS already treats memory as append-only, evidence-bound, time-explicit, lineage-preserved, and non-destructive.

The GitHub external memory layer adds a public and reproducible external surface:

```text
MemoryOS internal trace
  -> GitHub pointer record
  -> commit / issue / PR / artifact / release reference
  -> hash-pinned recall index
  -> compile_context input candidate
  -> MemoryOS authority boundary preserved
```

The purpose is not to replace internal MemoryOS. The purpose is to let MemoryOS remember where external evidence, design decisions, validation results, and repair lineage are stored.

## 2. Core Rule

```text
GitHub_external_memory_is_pointer_and_evidence_surface_not_memory_authority
```

A GitHub record can be strong evidence that something was committed, reviewed, validated, discussed, or released at a specific repository state.

A GitHub record cannot by itself decide truth, proof completion, clinical validity, Ten'i, world-state update, or execution permission.

## 3. Memory Modes

GitHub can serve MemoryOS in five modes:

```text
pointer_memory
  stores repo, path, commit SHA, issue, PR, release, artifact, or workflow pointer

evidence_memory
  stores externally reviewable proof of existence, validation output, CI log, release packet, or audit receipt

semantic_digest_memory
  stores non-authoritative summaries that help recall but never replace source evidence

repair_lineage_memory
  stores issue -> PR -> review -> commit -> validator -> release lineage

conflict_visibility_memory
  stores contradictions, stale claims, supersession, tombstones, and unresolved premise debt
```

## 4. Canonical GitHub Surfaces

```text
commits
branches
issues
pull requests
review comments
GitHub Actions workflows
workflow logs
artifacts
release packets
tags
repository files
```

For MemoryOS, moving branch names are weak references. Commit SHAs, tag objects, artifact IDs, and content hashes are stronger references.

## 5. Memory Record Schema

A GitHub external memory record should include:

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
lineage:
  parent_memory_ids: list[string]
  supersedes: list[string]
  tombstones: list[string]
constraints:
  no_overwrite: true
  no_execution_authority: true
  no_truth_authority: true
  no_proof_authority: true
  no_clinical_authority: true
  no_teni_authority: true
```

## 6. Write Protocol

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

The recommended repository path is:

```text
memoryos/external/github/YYYY/MM/<memory_id>.yaml
```

Index files may be placed under:

```text
memoryos/external/github/indexes/
```

Indexes are recall aids, not authority.

## 7. Recall Protocol

When MemoryOS recalls GitHub memory:

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

A recalled digest must cite or point to the source record. A digest without source evidence remains advisory only.

## 8. Supersession and Tombstone

GitHub external memory must not silently overwrite.

Allowed:

```text
append superseding record
append tombstone record
append conflict record
append repair record
append stale-reference warning
```

Forbidden:

```text
silently editing old memory to hide conflict
using force-push as memory correction
deleting evidence to simulate forgetting
turning a summary into authority
using branch HEAD as if it were pinned evidence
```

## 9. Conflict Handling

If GitHub memory conflicts with internal MemoryOS or later repository evidence:

```text
conflict detected
  -> mark both records visible
  -> classify uncertainty
  -> open repair_lineage_memory if repair is needed
  -> do not collapse into one hidden summary
  -> do not update world belief directly
```

Conflict visibility is a feature, not a defect.

## 10. Security and Privacy Boundary

GitHub external memory must not store:

```text
credentials
secrets
private keys
raw clinical data
identifiable patient data
private operational tokens
unredacted internal-only research material
```

For public repositories, all GitHub external memory should be publishable, reproducible, and safe to audit.

## 11. Relationship to GPT GitHub Integration

GPT may help read, summarize, classify, and draft GitHub external memory records.

GPT must remain non-authoritative:

```text
GPT_summary_not_memory_authority
GPT_recall_not_truth_authority
GPT_issue_draft_not_memory_commit
GPT_PR_draft_not_memory_commit
GPT_CI_interpretation_not_memory_truth
```

## 12. Validation Command

```bash
make memoryos-github-external-memory-checks
```

or:

```bash
python3 scripts/validate_memoryos_github_external_memory_v0_1.py
```

Expected success:

```text
PASS: KuuOS MemoryOS GitHub external memory surface v0.1 validates
```

## 13. Non-Authority Fixed Points

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

## 14. Version

Version: v0.1
Date: 2026-05-13
Author: Hidetoshi Itakura / 板倉英俊
Release mode: append-only / tighten-only / overwrite-forbidden
