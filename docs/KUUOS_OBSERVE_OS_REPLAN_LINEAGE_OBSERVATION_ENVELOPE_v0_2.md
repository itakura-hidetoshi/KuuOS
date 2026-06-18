# KuuOS ObserveOS Replan-Lineage Observation Envelope v0.2

ObserveOS v0.2 preserves the complete PlanOS replan lineage and ActOS v0.2 completion lineage when a recorded effect crosses into ObserveOS v0.1.

```text
ActOS v0.2 handoff and completion receipts
  + committed ActOS v0.1 effect state
  + exact Observe phase and cycle
  -> ObserveOS v0.2 lineage handoff
  -> ObserveOS v0.1 scope / collect / trace / assess / compare / commit
  -> ObserveOS v0.2 lineage completion receipt
```

## Boundary

The handoff accepts only a committed `EFFECT_RECORDED` Act state with both observation and verification debt preserved. The ActOS handoff and completion receipts must be canonical and must bind the same Act state, selected step, host receipt, host invocation, and upstream replan lineage.

Activation is accepted only in the Observe phase at the exact Act cycle. A different phase, different cycle, substituted Act completion, changed Qi digest, changed selected candidate, changed selected step, or changed observation target is rejected.

## Preserved lineage

The envelope retains:

- ActOS lineage handoff and completion receipts;
- PlanOS next-cycle compiler receipt;
- replan phase receipt;
- Qi condition packet;
- DecisionOS receipt;
- selected replan candidate and selected plan step;
- committed Act state and host effect receipts;
- expected observation and verification criterion digests.

Qi remains process context. It does not determine observation truth or verification outcome.

## ObserveOS v0.1 reuse

No second observation kernel is introduced. ObserveOS v0.2 delegates evidence scoping, collection, provenance tracing, quality assessment, directional comparison, and observation commit to ObserveOS v0.1.

The v0.1 phase chain remains:

```text
BIND -> SCOPE -> COLLECT -> TRACE -> ASSESS -> COMPARE -> COMMIT
```

## Observation and verification

An observation record is not a verification result. Every completion receipt keeps:

```text
observation_not_verification = true
verification_required = true
```

Matched and divergent observations may discharge the observation debt. Inconclusive and conflicted observations retain observation debt and request reobservation. All routes preserve verification debt.

## Single-use lineage

A process-local lineage store records two stages:

```text
HANDOFF_ISSUED
OBSERVATION_COMMITTED
```

Exact receipt replay is idempotent. A conflicting handoff for the same Act completion and observation target is rejected, and one handoff may commit at most one observation completion.

## Formal surface

The Lean surface proves:

- exact Observe-cycle and phase gating;
- upstream ActOS, PlanOS, replan, Qi, DecisionOS, candidate, and step lineage preservation;
- source-effect and observation-target binding;
- observation/verification separation;
- verification-debt preservation for every route;
- Qi non-authority;
- source identity preservation;
- single-use completion;
- recovery-count equality;
- no new truth, verification, effect, or overwrite authority.

## Public boundary

ObserveOS v0.2 is a lineage and evidence-boundary adapter. It does not replace VerifyOS, infer causality, complete the plan automatically, or rewrite prior memory.
