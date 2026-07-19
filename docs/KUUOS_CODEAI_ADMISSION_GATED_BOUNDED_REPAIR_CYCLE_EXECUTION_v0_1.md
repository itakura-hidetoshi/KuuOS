# CodeAI Admission-Gated Bounded Repair Cycle Execution v0.1

## Status

This additive stage consumes one exact active, one-shot, non-reusable bounded repair-cycle execution input and performs one admitted repair cycle through the existing isolated CodeAI execution boundaries.

It is the execution successor of **CodeAI Repair Cycle Admission Consumption v0.1**. The predecessor issues authority and budgets; this stage consumes that authority once.

## Route

1. Verify the sealed admission-consumption receipt.
2. Verify the sealed active execution input.
3. Verify the updated admission-consumption registry receipt.
4. Verify a fresh execution request, deny-by-default policy, and replay registry.
5. Require exact cycle, actor, repository, commit, repair, regeneration, candidate-set, and verification-plan lineage.
6. Reject reused execution-input digests and reused cycle-execution nonces.
7. Require the execution registry frontier to advance monotonically.
8. Require the allowed stage set to be exactly:
   - candidate regeneration adapter,
   - candidate portfolio selection,
   - isolated candidate application,
   - autonomous verification execution.
9. Invoke the provider-neutral candidate adapter once within the admitted provider-call and output budgets.
10. Revalidate the returned repair and regeneration receipts and candidate-set digest.
11. Invoke the existing bounded repair-cycle orchestration, which performs least-change candidate selection, isolated patch application, and runner-neutral verification.
12. Record pass, failed, or budget-aborted outcome.
13. Record used and unused values for all five admitted budget dimensions.
14. Advance the execution registry by exactly one input digest and one nonce.
15. Issue one sealed execution receipt without Git, merge, deployment, or successor authority.

## Exact input state

The execution input must state all of the following:

- source admission was consumed;
- one cycle only;
- one-shot;
- active;
- non-reusable;
- unconsumed;
- bounded cycle execution authority granted;
- candidate generation, candidate selection, isolated application, and verification authority granted;
- automatic execution, network, secret, live repository, Git, merge, deployment, and general successor authority denied;
- no cycle action has already been performed.

Any disagreement blocks before provider or runner invocation.

## Replay registry

The execution registry contains parallel unique histories of:

- consumed execution-input digests;
- consumed cycle-execution nonce digests.

A successful cycle transition satisfies:

- `next revision = source revision + 1`;
- `next consumed count = source consumed count + 1`;
- `last executed cycle index` increases strictly;
- exactly one execution-input digest is appended;
- exactly one cycle-execution nonce is appended.

The registry receipt is evidence of a deterministic transition. It is not a claim of external atomic persistence.

## Five-dimensional budget

The stage refuses any outer policy that exceeds the sealed execution input. It also refuses any inner bounded-cycle policy that exceeds the outer admitted policy.

The dimensions are:

1. candidate count;
2. provider-call count;
3. verification command count;
4. timeout seconds;
5. combined provider and runner output bytes.

Provider output is accounted before verification. The maximum verification output budget plus provider output must fit inside the admitted output budget before the bounded cycle starts.

The receipt records maximum, used, and unused values. Unused budget is historical accounting only and is not reusable authority.

## Provider-neutral boundary

The provider adapter receives only sealed lineage, isolated repository digest, and bounded resource limits. It must return:

- provider and session identifiers;
- declared output bytes;
- generated candidate count;
- exact repair receipt;
- exact regeneration receipt;
- candidate portfolio;
- explicit declarations that no network, secret, live repository, or Git effect occurred.

The adapter output remains untrusted until all receipts, candidate digests, repository and commit lineage, counts, and effect declarations are validated.

## Existing execution components

After admission validation, this stage delegates to the existing **CodeAI Bounded Repair Cycle Orchestration v0.1**. That component performs:

- failed-candidate exclusion;
- least-change portfolio selection;
- isolated patch application;
- autonomous runner-neutral verification;
- pass, failure, or runtime-budget-abort evidence generation.

The input repository mapping is checked for immutability. Only the returned isolated snapshot may differ.

## Outcomes

### Passed

All declared verification checks completed and passed. This is verification evidence, not proof or merge authority.

### Failed

The cycle completed but one or more checks failed. Failure establishes neither that another repair is required nor that continuation is authorized.

### Budget-aborted

The bounded verification layer stopped because a runtime budget was reached. The cycle receipt records the abort without converting unused budget into authority.

## Fixed boundaries

- execution input consumption != correctness;
- admitted execution != successful repair;
- cycle pass != proof;
- cycle failure != required repair;
- provider output != trusted patch;
- candidate selection != correctness;
- isolated application != live repository mutation;
- verification evidence != merge authority;
- unused budget != reusable authority;
- one completed cycle != unrestricted continuation;
- execution receipt != Git authority;
- execution receipt != deployment authority;
- execution receipt != general successor-stage authority.

## Explicit non-authority

This stage does not mutate a live repository and does not create or change Git refs, branches, commits, pushes, pull requests, merges, deployments, network access, or secret access.

A next-cycle eligibility bit may be recorded from the existing bounded orchestration, but no next-cycle authority is granted.
