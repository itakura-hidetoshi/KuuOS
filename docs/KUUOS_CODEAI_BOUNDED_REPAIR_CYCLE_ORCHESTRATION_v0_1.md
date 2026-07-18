# KuuOS CodeAI Bounded Repair Cycle Orchestration v0.1

Status: additive bounded orchestration sibling

Version: v0.1

Predecessor: CodeAI Verification-Guided Candidate Repair and Regeneration v0.1

Downstream stages: Candidate Portfolio Selection, Isolated Candidate Application,
and Autonomous Verification Execution v0.1

## 1. Purpose

This surface closes one governed repair cycle after verification-guided candidate
regeneration. It consumes the exact repair and downstream regeneration receipts,
excludes the candidate that already produced the failed verification evidence,
re-ranks the remaining proposal-only portfolio, selects one least-change
independent-verification target, applies it only to an isolated in-memory snapshot,
and executes one sealed bounded verification plan.

```text
failed verification evidence
  -> Verification-Guided Candidate Repair and Regeneration
  -> repair portfolio and sealed lineage receipts
  -> exclude the already-failed candidate
  -> least-change bounded reselection
  -> isolated candidate application
  -> bounded verification execution
  -> sealed repair-cycle receipt
```

The profile performs exactly one numbered cycle per invocation. A failed cycle may
be marked eligible for another separately authorized cycle only when its index is
below the policy maximum. Eligibility never starts another cycle by itself.

## 2. Required lineage

Before selection or runner invocation, the kernel verifies exact correspondence
for:

- verification-guided repair receipt digest;
- downstream autonomous regeneration receipt digest;
- repair-to-regeneration receipt link;
- canonical repair-candidate-set digest;
- combined candidate count, IDs, and digests;
- read-only repository snapshot digest;
- repository full name and source commit SHA;
- sealed verification plan digest;
- cycle request digest and freshness;
- cycle policy digest;
- positive cycle index not exceeding the maximum cycle count.

Any mismatch blocks the cycle before downstream stage invocation.

## 3. Failed-candidate exclusion

The source repair receipt identifies the candidate whose verification failed or
was aborted by runtime budget. That exact candidate digest must remain present in
the combined repair lineage, but it is excluded from the reselection portfolio.
The remaining candidates are deterministically re-ranked without changing their
candidate, patch-artifact, or Candidate Patch receipt digests.

Exclusion means only that the same failed candidate is not immediately replayed by
this cycle. It does not prove any remaining candidate is better or correct.

## 4. Bounded reselection

The kernel projects the eligible repair candidates into a sealed proposal-only
portfolio and reuses Autonomous Candidate Portfolio Selection v0.1. Selection is
restricted by:

- maximum candidate count;
- maximum patch bytes;
- maximum changed paths;
- allowed and forbidden risk labels;
- unresolved-question policy;
- allowed and forbidden path prefixes;
- deterministic least-change admissible ordering.

The selection receipt designates one independent-verification target only. It
grants no correctness, execution, Git, merge, deployment, or successor authority.

## 5. Isolated application

The selected candidate is passed to Autonomous Isolated Candidate Application
v0.1 with exact selection, candidate, patch-artifact, repository, commit, and
snapshot correspondence. Source and result path counts, snapshot bytes, patch
bytes, changed paths, allowed operations, and exact path accounting remain
bounded.

Application occurs only against a value-level copy. The source repository mapping
is re-digested after the cycle and any mutation blocks receipt emission.

## 6. Bounded verification execution

The resulting isolated snapshot is passed to Autonomous Verification Execution
v0.1. The cycle policy bounds:

- allowed check IDs;
- executable prefixes;
- work-directory prefixes;
- environment keys;
- command count;
- per-check and total timeout;
- per-check and total output bytes;
- verification snapshot path count and size.

Network, secrets, live repository access, and Git operations are all required to
be disabled. Nonzero exits, timeouts, malformed runner results, forbidden effects,
output-budget violations, and runner exceptions remain failed evidence rather
than success.

## 7. Cycle outcome

The sealed receipt records one of:

- `repair_cycle_verification_passed`;
- `repair_cycle_verification_failed`;
- `repair_cycle_verification_aborted_by_budget`.

It also records:

- cycle index and maximum cycle count;
- whether the cycle limit has been reached;
- whether another cycle is merely eligible;
- selected candidate and patch-artifact digests;
- selection, application, execution, evidence-bundle, and independent-evidence
  receipt digests;
- resulting isolated repository snapshot digest.

`next_cycle_eligible` is descriptive state only. The receipt always records
`next_cycle_authority_granted = false` and
`successor_stage_authority_granted = false`.

## 8. Fixed semantics

```text
cycle orchestration != correctness
cycle pass != proof
cycle failure != required repair
failed-candidate exclusion != correctness judgement
repair candidate ranking != correctness
reselection != verification
isolated application != live repository mutation
verification evidence != merge authority
next-cycle eligibility != execution authority
cycle receipt != successor-stage authority
```

## 9. Non-effects

This stage performs none of the following:

- live repository patch application;
- repository mutation;
- Git ref change;
- branch, commit, push, pull-request, or merge effect;
- deployment;
- network use;
- secret access;
- automatic next-cycle execution;
- correctness or proof certification.

## 10. Implementation map

- runtime: `runtime/kuuos_codeai_bounded_repair_cycle_orchestration_v0_1.py`
- integration checker: `scripts/check_codeai_bounded_repair_cycle_orchestration_v0_1.py`
- unit tests: `tests/test_kuuos_codeai_bounded_repair_cycle_orchestration_v0_1.py`
- example: `examples/codeai_bounded_repair_cycle_orchestration_v0_1.json`
- manifest: `manifests/kuuos_codeai_bounded_repair_cycle_orchestration_v0_1.json`
- Lean kernel: `formal/KUOS/CodeAI/BoundedRepairCycleOrchestrationV0_1.lean`
- Lean root: `formal/KuuOSCodeAIBoundedRepairCycleOrchestrationV0_1.lean`
- workflow: `.github/workflows/codeai-bounded-repair-cycle-orchestration-v0-1.yml`
