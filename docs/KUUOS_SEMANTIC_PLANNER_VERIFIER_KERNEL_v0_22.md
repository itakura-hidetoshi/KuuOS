# KuuOS Semantic Planner / Independent Outcome Verifier v0.22

## Purpose

v0.22 closes the next cognition-plane gap above the persistent mission and observation-belief layers.

```text
mission contract v0.20
+ active goal portfolio
+ observation-belief state v0.21
+ available capabilities
+ finite resource envelope
→ semantic plan proposal
→ independent outcome verification
→ mission evidence adapter
```

The release does not authorize an external effect. It produces bounded proposals and evidence receipts that remain subordinate to lower ActOS, lease, connector, and host-execution gates.

## Semantic plan

Every plan is digest-bound to:

- mission, lineage, contract, and mission-state digests
- exact observation-belief-state digest and local chart
- active goal and goal-portfolio digests
- planner identity
- finite validity interval
- prerequisite claim digests
- available and required capability sets
- finite cycle and total-cost bounds
- subgoal and step dependency DAGs
- alternatives and expected observations
- prior plan and failure-verification digests during replanning

A step contains an objective, typed dependencies, required capabilities, cost bound, expected observations, success claims, and compensation references. Every step explicitly carries `effect_authority_granted = false`.

## Plan blockers

The planner preserves blockers rather than pretending that planning completed execution.

```text
unknown prerequisite      → blocked_unknown
contradicted prerequisite → blocked_contradiction
stale prerequisite        → blocked_stale
missing capability        → capability_gap
finite budget exceeded    → resource_blocked
```

A ready plan is still only a proposal.

## Exact-basis invalidation

A plan is bound to the exact belief-state digest used during planning. Any subsequent belief-state revision produces an invalidation receipt. The receipt separately records which prerequisite claim digests changed, while still invalidating the exact state basis when an unrelated observation changes the state.

```text
same exact belief digest → still_current
changed belief digest    → invalidated
```

This prevents silent reuse of a plan generated under a stale epistemic snapshot.

## Replanning

A successor plan requires:

- prior plan digest
- non-success verification receipt
- explicit replan reason
- strictly incremented plan revision

A `verified_success` receipt cannot be used as failure evidence for replanning.

## Independent outcome verification

The verifier must have an identity distinct from the planner. Verified success requires independent observations that:

- validate under the same mission and chart
- were not used as planning evidence
- were not emitted by the planner identity
- support every mission success criterion
- meet the contract minimum-confidence threshold

Possible outcomes are:

```text
verified_success
partial_success
inconclusive
contradicted
regression_detected
verification_requires_human
```

The central invariant is:

```text
execution success != mission success
```

Execution receipts may be attached, but they cannot independently create `verified_success`.

## Mission-evidence adapter

A valid verifier receipt can be converted into v0.20 `authorized_verification` mission evidence. The adapter does not itself transition mission lifecycle state; the mission renewal/termination kernel remains the owner of that decision.

## Persistence

The append-only store contains:

```text
initial.json
snapshot.json
planner-verifier-ledger.jsonl
```

It persists plans, verification receipts, and invalidation receipts. Replay is idempotent. Recovery reconstructs state from the immutable initial packet and ledger; snapshot mismatch fails closed, and repair is explicit.

## Formal boundary

The Lean module proves:

- execution success without independent mission evidence is not mission-success eligibility
- planner and verifier identity separation
- plan non-authority preservation
- the combined proposal, finite-resource, exact-binding, separation, contradiction-visibility, and non-authority boundary

## Validation

```bash
PYTHONPATH=. python scripts/check_semantic_planner_verifier_v0_22.py
PYTHONPATH=. python -m unittest -v tests.test_semantic_planner_verifier_v0_22
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KUOS.OpenHorizon.SemanticPlannerVerifierKernelV0_22
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true build KuuOSFormal
```

## Next dependency

```text
v0.23 Cognitive Memory Consolidation
+ Bounded Credit Assignment and Strategy Learning
```
