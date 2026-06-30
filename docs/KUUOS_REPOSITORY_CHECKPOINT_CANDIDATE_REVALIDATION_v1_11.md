# KuuOS Repository Checkpoint Candidate Revalidation v1.11

## Purpose

v1.11 closes the explicit trust boundary documented by v1.10.

A candidate is not accepted merely because its own digest is internally consistent. The receipt replays the complete v1.09 candidate derivation against the v1.06 review record, v1.07 route, v1.08 namespace decision, stability evidence, observations, policies, and original evaluation times.

## Outcomes

- `CHECKPOINT_CANDIDATE_REVALIDATION_VALID`: the complete v1.09 replay passes, repository binding is exact, and the candidate remains fresh.
- `CHECKPOINT_CANDIDATE_REVALIDATION_REJECTED` with `CANDIDATE_STALE`: replay passes but the candidate exceeded the configured age bound.
- `CHECKPOINT_CANDIDATE_REVALIDATION_REJECTED` with `INVALID_EVIDENCE`: replay, policy, or binding validation fails.

## Forgery resistance

A caller can alter a candidate and recompute its candidate digest. Such a candidate may be self-consistent but is not derivationally valid.

v1.11 reconstructs the expected candidate from the full upstream evidence chain. A self-resigned candidate that differs from that reconstruction is rejected.

## Safety boundary

The receipt is read-only validation evidence.

It never grants repository-change authority, executes a transition, invokes Git, or mutates a reference.

Receipt validity does not imply that the candidate is ready for a CAS transition. A valid receipt can also attest that a clean or creation-route case correctly produced no candidate.

## Formal claims

The Lean model proves that:

- a valid receipt requires complete replay, exact binding, and freshness;
- a valid receipt is nonexecuting and grants no authority;
- a stale rejection can preserve successful replay without granting authority;
- identical inputs derive identical receipts.
