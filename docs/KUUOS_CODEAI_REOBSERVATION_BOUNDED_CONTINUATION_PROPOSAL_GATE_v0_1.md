# CodeAI Reobservation-Bounded Continuation Proposal Gate v0.1

## Purpose

This additive stage consumes the exact output of **CodeAI Environment Capsule and Livelock-Efficiency Gate v0.1** and evaluates one read-only continuation proposal against a newly sealed policy.

It emits one of two read-only dispositions:

- `bounded_continuation_proposal_admitted`;
- `bounded_continuation_proposal_held`.

Admission means only that one proposed observation or non-mutating verification action fits the exact predecessor lineage, the derived residual budget, and the mandatory reobservation contract. It does not execute the action, reserve or consume budget, dispatch a specialist, select a candidate, mutate a repository, grant Git authority, or claim correctness.

Malformed, tampered, stale, version-mismatched, or lineage-mismatched inputs are structurally blocked before a disposition is produced. Structurally valid inputs that fail predecessor, proposal, or budget predicates produce a hold.

## Exact predecessor and source binding

The reference specialization binds:

- repository: `itakura-hidetoshi/KuuOS`;
- current source commit: `2944084ee7d415993f35c2bb8551c4fe83ee443d`;
- predecessor profile: `CodeAI Environment Capsule and Livelock-Efficiency Gate v0.1`;
- predecessor manifest digest: `c24224d427dca0529e9a4aaee1e69da44c95800fc99f763e15500f53f7f0104d`;
- predecessor gate pack: `e0b8aeea1179a999317e1a0092940c3cb062644c366e0a1700219d35f98debb8`;
- predecessor receipt: `51e921bc13bd9a25ae7d7bae34e786e4c4e52d8377a29fe43e60b8b5100ef439`;
- selected specialist: `specialist-formal-001`;
- specialist kind: `formal`;
- selected subtask: `verify`;
- environment capsule: `60bec0429b6d113e1fffc3f4e7a98eaed0cc650ebf6a3ba884ba574342fb5be0`;
- progress trace: `9ea48de292b513393fa2ef91de33b93eb6c86e315304345f66b88362777f8755`;
- predecessor policy: `b68081d31c7ae11ddfee6737733630b2b69ed2fb894207a4ed93fed2a338cfc6`.

The current source commit and the predecessor stage's own historical source commit are not conflated. The former fixes the tree in which this downstream stage is defined; the latter remains sealed inside the exact predecessor manifest.

## Predecessor predicates

The predecessor must remain exactly verifiable and must report:

- `progress_efficiency_admitted`;
- continuation hint only;
- observable trace grounded;
- reproducible environment capsule;
- livelock free;
- efficiency within budget;
- exact environment;
- predecessor router verified;
- no hold reasons.

The predecessor must not report continuation authority, execution authority, repository mutation, Git authority, or correctness.

A predecessor admission is evidence about the measured prior trajectory. It is not inherited authority.

## Residual budget derivation

The gate does not accept self-reported residual totals. For every resource `r`, it derives:

```text
residual_before[r] = policy.maximum_total[r] - predecessor.measured_usage[r]
residual_if_executed[r] = residual_before[r] - proposal.requested[r]
```

`residual_if_executed` is hypothetical only. The gate records:

- `hypothetical_residual_only = true`;
- `budget_reserved = false`;
- `budget_consumed = false`;
- `action_executed = false`.

Resources are independently bounded for:

- steps;
- tool calls;
- model calls;
- token units;
- wall-clock time;
- failed actions.

A proposal is held if predecessor usage already exceeds a total ceiling, if the proposal exceeds a per-proposal ceiling, or if the proposal exceeds derived residual capacity.

## Exactly one reobservation-bounded proposal

A valid proposal binds one continuation round and exactly one action from:

- `observe_repository`;
- `inspect_artifact`;
- `run_read_only_check`;
- `run_formal_verification`.

The proposal must bind:

- the exact source and predecessor lineage;
- the pre-action state digest;
- the action target digest;
- an expected observation contract;
- an expected artifact contract;
- explicit incremental resource bounds;
- observable grounding;
- read-only behavior;
- a new checkpoint;
- mandatory reentry to the predecessor environment/livelock-efficiency gate.

The proposal is held for multiple actions, a mutating action, a disallowed action kind, self-report-only evidence, a missing observable return, a missing checkpoint, missing gate reentry, or a forbidden authority claim.

## Reference specialization

The sealed predecessor measured:

- 6 steps;
- 9 tool calls;
- 6 model calls;
- 46,000 token units;
- 1,380,000 ms wall-clock time;
- 0 failed actions.

The total policy ceilings are:

- 8 steps;
- 12 tool calls;
- 8 model calls;
- 60,000 token units;
- 1,800,000 ms wall-clock time;
- 0 failed actions.

The derived residual budget is therefore:

- 2 steps;
- 3 tool calls;
- 2 model calls;
- 14,000 token units;
- 420,000 ms wall-clock time;
- 0 failed actions.

The reference proposal requests one read-only formal-verification action:

- 1 step;
- 1 tool call;
- 1 model call;
- 7,000 token units;
- 180,000 ms;
- 0 failed actions.

It requires an observable artifact, a new checkpoint, and reentry to the predecessor gate. The resulting decision is `bounded_continuation_proposal_admitted`.

Reference gate pack digest:

- `dc1256d1bc81b419ae49685bda4d15b015d2729c1003a3f1a9dab94c1a07a215`.

Reference receipt digest:

- `ad8c048ca5af8241f07efc32fa30d4a219d4e1733ee01868ea16dd5b4081a260`.

## Research basis

The stage narrows current primary research into a deterministic repository contract without extending the papers' empirical claims.

1. **Teaching LLMs When to Stop Seeking and Start Acting** (ICLR 2026 submission, OpenReview `K9GAwws48i`) treats termination as a distinct decision rather than allowing unconstrained information seeking.
2. **EAT: Entropy After `</Think>` for reasoning model early exiting** (ICLR 2026 submission, OpenReview `hfEVqiJyF6`) motivates adaptive stopping instead of a uniform fixed compute budget.
3. **Look Before You Leap: Autonomous Exploration for LLM Agents** (arXiv:2605.16143) separates bounded exploration from later action and uses verifiable exploration checkpoints.
4. **ContractBench: Can LLM Agents Preserve Observation Contracts?** (arXiv:2605.17281) shows that temporal validity and byte-level integrity of observation artifacts are independent, regression-prone requirements.
5. **Capability Gates Are Not Authorization: Confused-Deputy Failures in LLM Agent Frameworks** (arXiv:2606.28679) distinguishes capability exposure from per-call authorization; this stage correspondingly refuses to convert a gate result into execution or Git authority.
6. **AgentRx: Diagnosing AI Agent Failures from Execution Trajectories** (ICML 2026 submission, OpenReview `VDQkzHwidO`) motivates trace-local, auditable constraint evidence instead of terminal self-report alone.

KuuOS makes a narrower claim: exact predecessor evidence plus derived residual capacity can admit a read-only proposal as a hint. It does not establish that the proposed action is correct, sufficient, safe in every external environment, or authorized to execute.

## Formal kernel

The Lean surface defines:

- `ActionKind`;
- `Binding`;
- `Budget`;
- `MeasuredUsage`;
- `ContinuationProposal`;
- `GateEvidence`;
- `PredecessorAdmitted`;
- `ProposalBounded`;
- `ResidualSufficient`;
- `ObservableReturn`;
- `BoundaryPreserved`;
- `GateAdmitted`.

Generic theorems extract exact binding, predecessor admission, proposal boundedness, residual sufficiency, observable return, and authority-boundary preservation.

Separate theorems prove that repository mismatch, a held predecessor, multiple actions, a mutating action, missing reobservation, token-budget excess, and self-report-only evidence forbid admission.

The reference proposal is admitted. Mutating, over-budget, missing-reobservation, and self-report-only variants are not admitted. No compound proposition is discharged with `native_decide`.

## Fixed boundaries

```text
continuation hint != continuation authority
proposal admission != action execution
hypothetical residual != budget reservation
budget fit != correctness proof
livelock-free measurement != task completion proof
efficiency pass != successful continuation proof
observable return requirement != observed return
new checkpoint requirement != checkpoint existence
gate reentry requirement != reentry execution
gate receipt != repository mutation authority
gate receipt != Git authority
self report != observable evidence
```
