# KuuOS CodeAI Autonomous Candidate Regeneration v0.1

Status: additive bounded-regeneration sibling

Version: v0.1

Predecessors: CodeAI Autonomous Structured Edit Synthesis v0.1 and CodeAI Autonomous Unified Diff Candidates v0.1

## 1. Purpose

This surface evolves autonomous change-candidate generation from a single bounded
provider pass into a bounded feedback-driven regeneration loop. It consumes an
existing governed candidate portfolio, exact source receipts, a read-only
repository snapshot, explicit feedback, and one or more provider-neutral adapters.
It then asks for semantically distinct alternatives until the target portfolio
size is reached or the sealed call and round budgets are exhausted.

```text
existing governed candidate portfolio
  + exact source generation receipt
  + read-only repository text snapshot
  + sealed regeneration request and policy
  + provider-neutral adapters
  -> bounded feedback/diversity rounds
  -> AI Provider Boundary evaluation
  -> deterministic unified-diff and Candidate Patch validation
  -> semantic patch deduplication
  -> lineage-bound diversified candidate portfolio
```

Regeneration remains proposal-only. More candidates are not selection,
verification, correctness, application, Git authority, or deployment authority.

## 2. Source portfolios

The source generation receipt may be either:

- an Autonomous Structured Edit Synthesis v0.1 receipt; or
- an earlier Autonomous Candidate Regeneration v0.1 receipt.

The supplied seed candidate objects must correspond exactly to the source receipt:
contiguous ranks, candidate identifiers, candidate digests, patch artifacts,
source observation receipt, repository, and source commit are checked before any
provider call. A regeneration receipt can therefore seed a later bounded
regeneration without losing lineage.

## 3. Regeneration request

The sealed request records:

- stable request and revision identifiers;
- original intent text;
- target unique candidate count;
- maximum requested rounds;
- feedback reasons;
- ordered diversity axes;
- requirement traces and test-plan identifiers;
- risk labels and unresolved questions;
- prior candidate and producer-session lineage;
- request creation epoch.

The target must exceed the seed portfolio size and remain within the policy's
maximum unique-candidate count.

## 4. Regeneration policy

The sealed policy bounds:

- allowed provider identifiers;
- allowed diversity axes;
- maximum rounds;
- maximum provider calls per round;
- maximum total provider calls;
- raw output, intent, repository snapshot, and feedback budgets;
- maximum existing and combined candidate counts;
- request and response freshness windows;
- allowed and forbidden repository path prefixes.

Provider adapters are sorted by adapter identifier. Diversity axes are traversed
in request order. This produces deterministic orchestration for fixed inputs and
adapter behavior.

## 5. Feedback loop

Every round receives:

- the original intent and read-only snapshot;
- the selected diversity axis;
- bounded accumulated feedback;
- summaries of all current candidates;
- the patch-artifact digests that must not be repeated;
- the same governed structured-edit output contract used by the initial
  synthesis surface.

Provider exceptions, boundary `HOLD`, `REPAIR`, `REJECT`, and `QUARANTINE`
routes, malformed outputs, downstream Candidate Patch rejection, and duplicate
candidate identities remain visible. Their reasons are fed into the next round as
candidate context only. Fedback is not treated as truth or authority.

## 6. Novelty and lineage

A candidate is accepted only when:

1. its provider output passes the AI Provider Boundary as `CANDIDATE` material;
2. its structured proposal produces a supported Autonomous Unified Diff candidate;
3. Candidate Patch v0.1 marks the candidate ready;
4. its candidate identifier is new;
5. its candidate digest is new; and
6. its patch-artifact digest is new.

Patch-artifact digest equality is the v0.1 semantic-duplicate criterion. It blocks
identical effective patches even when a provider changes proposal identifiers or
producer sessions. Every accepted candidate carries the accumulated prior
candidate digests and producer-session identifiers.

## 7. Output

The result contains:

- per-call regeneration attempt receipts;
- newly accepted candidates;
- a deterministically reranked combined portfolio;
- exact seed, regenerated, and combined identifiers and digests;
- round, call, target, and no-progress accounting;
- a sealed regeneration receipt.

The advisory rank remains the least-change ordering inherited from Autonomous
Unified Diff Candidates v0.1:

1. changed-path count;
2. patch byte size;
3. risk-label count;
4. candidate identifier.

Ranking is not selection.

## 8. Fail-closed conditions

The route blocks before provider invocation for malformed or stale requests,
invalid policies, unsupported source profiles, receipt digest mismatches, source
or candidate-policy correspondence failures, seed portfolio drift, path-scope
violations, disallowed providers or diversity axes, and exceeded static budgets.

During regeneration, an individual failed provider call or rejected proposal does
not erase an accepted sibling. If no novel candidate is accepted, the route emits
`candidate_regeneration_exhausted_without_novel_candidate` with the complete
attempt history.

## 9. Preserved boundaries

```text
feedback != truth
feedback != authority
regeneration != correction
novelty != correctness
semantic difference != requirement satisfaction
more candidates != selection
candidate ranking != candidate selection
regenerated candidate != verified patch
regenerated candidate != applied patch
provider call != repository mutation
regeneration receipt != verification or execution lease
```

The kernel performs no live filesystem write, patch application, Git object or ref
change, branch creation, commit, push, pull request, merge, deployment, or secret
access. It grants no selection, verification, execution, merge, deployment, or
secret authority.

## 10. Validation

The implementation includes:

- an actual initial synthesis – regeneration integration checker;
- 13 unit tests covering target completion, duplicate suppression, feedback
  carry-forward, provider exception isolation, source and seed tamper rejection,
  freshness, provider policy, total call bounds, lineage, deterministic ranking,
  no-effect invariants, and chained regeneration;
- a strict Lean formal root;
- a dedicated GitHub Actions workflow that also builds the full `KuuOSFormal`
  baseline.
