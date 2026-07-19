# KuuOS CodeAI Repair Cycle Continuation Admission v0.1

## Status

Additive, fail-closed continuation-admission sibling for `CodeAI Bounded Repair Cycle Orchestration v0.1`.

## Purpose

This profile turns a prior cycle's non-authoritative `next_cycle_eligible` statement into a fresh, policy-bound, exactly-one-cycle admission token. It does not start the next cycle. It only proves that a new request, the prior sealed receipt, an accumulated budget ledger, and a deny-by-default continuation policy correspond exactly enough to reserve bounded resources for cycle `n + 1`.

## Inputs

1. A sealed `CodeAI Bounded Repair Cycle Orchestration v0.1` receipt.
2. A fresh sealed continuation request.
3. A sealed continuation policy.
4. A sealed cumulative budget ledger.

The source cycle must have:

- completed with verification failure or budget abort;
- `cycle_verification_passed = false`;
- `next_cycle_eligible = true`;
- `cycle_limit_reached = false`;
- no prior next-cycle, execution, live repository, Git, network, secret, merge, deployment, or general successor-stage authority.

## Exact correspondence

Admission is blocked unless all of the following match:

- source cycle receipt digest in the request, policy, and budget ledger;
- source selected-candidate digest in the request and policy;
- policy current cycle index and source cycle index;
- policy maximum cycle count and source maximum cycle count;
- ledger completed-cycle count and source cycle index;
- requested next cycle index and `source cycle index + 1`.

Skipping a cycle, replaying a different receipt, substituting another selected candidate, or using a stale request or ledger is fail-closed.

## Budget reservation

The continuation request reserves five independent resources for exactly one next cycle:

- candidate count;
- provider-call count;
- verification command count;
- timeout seconds;
- output bytes.

For each resource, the runtime verifies:

- accumulated consumption does not exceed the policy total;
- the requested reservation is at least the policy minimum;
- the requested reservation does not exceed the per-cycle maximum;
- accumulated consumption plus the reservation does not exceed the total.

The receipt records the reservation and remaining budget before and after reservation.

## Admission result

A successful receipt records:

- the exact current and admitted cycle indices;
- the source receipt and selected-candidate lineage;
- request, policy, and ledger digests;
- all five resource reservations;
- remaining budget before and after reservation;
- `exactly_one_next_cycle_admitted = true`;
- `continuation_admission_authority_granted = true`;
- `admission_scope = one_sealed_next_cycle`;
- `admission_reusable = false`;
- `admission_consumed = false`.

The admission token is intentionally future-only and inactive. A downstream stage must consume it once and must independently verify its digest, exact cycle index, reservation, freshness, and non-reuse state.

## Denied capabilities

The policy requires all of these to remain false:

- network access;
- secret access;
- live repository access;
- Git operations;
- automatic execution.

The receipt additionally records no candidate generation, selection, patch application, runner invocation, repository mutation, branch, commit, push, pull request, merge, deployment, or automatic next-cycle start.

## Fixed semantics

- continuation admission != cycle execution
- continuation admission != correctness
- source eligibility != continuation authority
- remaining budget != safe outcome
- exact cycle sequence != successful repair
- one-cycle admission != reusable capability
- reservation != resource consumption
- admission receipt != selection authority
- admission receipt != verification authority
- admission receipt != merge or deployment authority
- admission receipt != live repository or Git capability

## Fail-closed behavior

Malformed objects, missing or extra fields, digest mismatch, unsupported source disposition, cycle-limit exhaustion, non-successor index, lineage mismatch, stale request or ledger, inconsistent cycle counts, insufficient remaining budget, per-cycle budget excess, or forbidden capability requests return `blocked` with no admission receipt.
