# MemoryOS GitHub Chat Long-Term Writeback v0.2

## Purpose

This additive protocol closes the false operational gap in which a conversation reports that long-term memory could not be updated merely because GitHub tools were used in the same conversation.

GitHub operations and conversational long-term-memory writeback are separate phases. They may be executed sequentially in one conversation.

## Core Rule

```text
GitHub_tool_use_does_not_block_long_term_memory_writeback
```

The following statement is prohibited unless a real, independently identified capability error occurred:

```text
GitHub操作ツールとの併用制約により長期メモリへ保存できませんでした
```

A new conversation is not required merely because GitHub was searched, edited, committed, reviewed, merged, or checked in the current conversation.

## Two-Lane Model

```text
GitHub lane
  observe repository state
  -> edit or create repository surfaces
  -> obtain stable commit / PR / merge / workflow pointers
  -> verify resulting state

Memory writeback lane
  normalize durable handoff facts
  -> remove transient logs and redundant detail
  -> preserve repository, branch, PR, commit, merge and CI pointers
  -> append to conversational long-term memory
  -> return an explicit writeback receipt
```

The lanes are independent in authority but composable in execution order.

## Required Sequence

```text
perform_github_operations
  -> verify_github_result
  -> build_handoff_digest
  -> invoke_long_term_memory_writeback
  -> verify_writeback_result
  -> report_both_receipts
```

GitHub completion is not memory completion. Memory completion is not inferred from a GitHub commit.

## Save Triggers

Long-term-memory writeback is required when at least one of the following holds:

- the user explicitly says 保存して, 記憶して, 継承して, or equivalent;
- a PR, merge, release, formal proof frontier, CI closure, or canonical architectural decision changes future work;
- the assistant has already promised that the state will be retained across conversations;
- an established additive-only or tighten-only baseline receives a new successor state.

## Handoff Digest

A handoff digest should normally contain:

```yaml
repository: owner/name
branch: string | null
pr_number: integer | null
head_commit: string | null
merge_commit: string | null
workflow_runs:
  - name: string
    run_id: integer | null
    conclusion: success | failure | cancelled | pending | unknown
completed_spine:
  - string
open_frontier:
  - string
invariants:
  - string
release_mode: append-only | tighten-only | ordinary
recorded_at: ISO-8601 timestamp
```

Large source files, complete diffs, and full CI logs remain in GitHub. Long-term memory stores the durable semantic digest and stable pointers.

## Writeback Receipt

A successful result must be represented as:

```yaml
github_receipt:
  status: verified
  stable_pointer: string
memory_writeback_receipt:
  status: stored
  scope: long_term_memory
  mode: additive_only
```

The assistant must not claim `status: stored` unless a memory-write operation actually succeeded.

## Genuine Capability Failure

If the long-term-memory facility is genuinely unavailable, disabled, rejected, or returns an error:

1. Do not attribute the failure to GitHub coexistence.
2. Do not claim that storage succeeded.
3. Preserve the normalized handoff digest in the current response.
4. State the actual capability condition precisely.
5. Retry within the same conversation when the capability becomes available.

Permitted structured result:

```yaml
memory_writeback_receipt:
  status: capability_unavailable
  reason: exact observed condition
  handoff_digest_preserved_in_current_conversation: true
  github_tool_coexistence_was_not_the_cause: true
```

## Fixed Points

```text
GitHub_tool_use_does_not_block_long_term_memory_writeback
GitHub_and_memory_writeback_are_separate_sequential_phases
same_conversation_writeback_is_the_default
new_conversation_is_not_required_by_GitHub_use
no_false_saved_claim
no_false_coexistence_failure_claim
actual_memory_receipt_required
handoff_digest_is_additive_only
GitHub_stores_full_evidence
long_term_memory_stores_durable_semantic_handoff
existing_confirmed_baselines_are_not_overwritten
```

## Relationship to v0.1

This protocol extends `MEMORYOS_GITHUB_EXTERNAL_MEMORY_v0_1.md` without changing its authority boundary.

- v0.1: GitHub is an external pointer and evidence surface, not MemoryOS authority.
- v0.2: use of that GitHub surface does not prevent a separate conversational long-term-memory writeback in the same conversation.

## Validation

```bash
python3 scripts/validate_memoryos_github_chat_long_term_writeback_v0_2.py
```

Expected output:

```text
PASS: KuuOS MemoryOS GitHub chat long-term writeback v0.2 validates
```

## Version

Version: v0.2  
Date: 2026-06-21  
Author: Hidetoshi Itakura / 板倉英俊  
Release mode: append-only / tighten-only / overwrite-forbidden
