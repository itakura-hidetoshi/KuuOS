# KuuOS BeliefOS Relational Conditional Kernel v0.1

BeliefOS v0.1 stores belief as a conditional, local, revisable relation rather than as truth, essence, or execution authority.

```text
belief != truth
confidence != certainty
persistence != essence
verification != final authority
qi readout != intervention license
belief commit != mission activation
```

## Root structure

BeliefOS is downstream of the KuuOS fourfold core.

```text
Emptiness
  -> no belief has independent self-nature or self-authority
Dependent Origination
  -> every belief carries conditions, evidence, observer, context, lineage, and history
Two Truths
  -> conventional usability remains separate from ultimate non-reification
Middle Way
  -> neither absolutize a belief nor erase operational responsibility
Qi process tensor
  -> condition belief on non-Markov flow history without treating Qi as substance or authority
```

## Strict phase order

```text
PROPOSE
  -> CONTEXTUALIZE
  -> TRACE
  -> WEIGH
  -> CHALLENGE
  -> QI_CONDITION
  -> TWO_TRUTHS_CHECK
  -> MIDDLE_WAY_GATE
  -> COMMIT
```

The next revision may reopen only through `COMMIT -> PROPOSE`. Phase skipping, stale state digests, event-index regression, timestamp regression, and authority escalation fail closed.

## Conditional belief field

A belief record contains:

- claim and hypothesis-space digests;
- context chart, observer, role, scale, temporal scope, task scope, and WORLD model;
- evidence, observations, verification receipts, and causal support;
- counterevidence, contradictions, alternatives, and unresolved residuals;
- a credal interval `[lower_probability, upper_probability]`;
- epistemic, aleatory, contextual, temporal, model, observer, and process-history uncertainty;
- Qi process-tensor and history-window digests;
- Two Truths and Middle Way boundaries;
- append-only event history and predecessor/current state digests.

Belief is represented by an interval rather than requiring a single precise probability. The interval width preserves visible ignorance and model plurality.

## Counterevidence preservation

The challenge phase appends counterevidence and alternatives. It does not silently delete prior challenges. A later implementation may resolve a challenge only through an explicit resolution receipt; absence from a new observation is not deletion authority.

## Qi process tensor boundary

Qi belongs to the conventional operating surface. It may condition:

- contextual priors;
- likelihood interpretation;
- temporal transition constraints;
- anomaly signals;
- recovery trajectories;
- context transport.

It may not become:

- standalone truth evidence;
- automatic fact promotion;
- direct execution permission;
- proof substitute;
- standalone clinical certainty;
- unrestricted causal explanation.

The runtime requires both a process-tensor digest and a history-window digest so that the update remains explicitly non-Markov and lineage-bound.

## Two Truths boundary

The state records both:

```text
samvrti_operationally_usable
paramartha_non_reified = true
two_truths_separated = true
```

Conventional usability does not imply absolute truth. Emptiness does not erase responsible operation.

## Middle Way gate

The gate records risks of:

- reification;
- nihilistic erasure;
- premature closure;
- abandonment of responsibility.

It routes the belief to one of:

```text
CANDIDATE | OBSERVE | HOLD | REPAIR | REJECT | QUARANTINE | RETIRED
```

A high reification or nihilistic-erasure risk cannot be promoted directly as `CANDIDATE`.

## Persistent store

```text
belief-genesis.json
belief-ledger.jsonl
belief-snapshot.json
.belief-os.lock
```

`belief-ledger.jsonl` is the append-only authority. `belief-snapshot.json` is a derived cache. Every commit binds the predecessor commit digest, predecessor belief-state digest, event, and result belief-state digest. A malformed ledger, broken digest chain, or snapshot mismatch fails closed. The snapshot may be repaired only from the verified ledger.

## v0.21 Mission Cycle bridge

A BeliefOS commit is future-only:

```text
future_only = true
memory_overwrite = false
activation_boundary = mission_replan_only
```

A committed belief does not become active for the next mission plan by itself. Activation requires:

- the v0.21 mission phase to be `replan`;
- a mission-cycle state digest;
- a Replan receipt digest;
- a `next_plan_basis_digest`.

```text
Observe / Verify / Learn
  -> BeliefOS conditional update
  -> BeliefOS COMMIT
  -> pending_replan_activation
  -> v0.21 Replan receipt
  -> next Plan belief basis
```

BeliefOS neither changes v0.21 phase order nor grants lower execution authority.

## Formal surface

The Lean surface proves:

- the typed phase order and strict event-index increase;
- nonnegative credal width;
- belief commit does not grant truth or execution authority;
- Qi conditioning does not grant authority;
- Two Truths separation and non-reification;
- Middle Way promotion avoids both collapse modes;
- counterevidence count is append-only;
- learning is future-only and non-overwriting;
- Replan is required for activation;
- ledger recovery and snapshot commit counts agree.

## Public boundary

This kernel is a structural and governance implementation. It does not grant theorem, truth, clinical, institutional, treatment, medical-act, shell, network, tool, or unrestricted execution authority.
