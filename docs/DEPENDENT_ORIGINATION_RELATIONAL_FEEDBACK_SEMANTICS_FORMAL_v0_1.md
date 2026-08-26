# Dependent Origination Relational Feedback Semantics — Formal v0.1

## Source boundary

This layer was extracted from a user-supplied external behavioral-surrogate test package dated 2026-08-25. The package explicitly stated that it was neither the official KuuOS implementation nor a measurement of hidden ChatGPT state.

KuuOS imports only the structural ideas that survive mathematical abstraction. The package's hard-coded scalar coefficients, thresholds, psychological interpretation, clinical interpretation, and `core_proxy` performance comparison are not imported.

## What was useful

The useful content is the separation of:

- body state;
- episodic memory;
- structural memory;
- relational state;
- a present-state readout (`I_now` in the surrogate);
- observation / evidence / unresolved difference;
- decision gate and action;
- feedback into the next encounter;
- preference for a reversible probe under high uncertainty.

This is naturally a history-sensitive closed loop rather than a new replacement for the KuuOS dependent-origination core.

## Correction of the surrogate semantics

In the supplied Python model, the stored `i_now` field is not read by `observe` or by the decision gate. The code recomputes the same scalar from other fields. Therefore `i_now` is a diagnostic readout there, not an independent causal state variable.

Formal v0.1 removes this ambiguity:

```text
context
  = body × episodic-memory × structural-memory × relation

currentSelf : context -> I_now
observe     : stimulus -> I_now -> observation
```

Thus the present state is derived from context and is explicitly on the causal path into observation.

The theorem

```text
response_changes_after_step_of_currentSelf_changes
```

states the exact sufficient condition for feedback to alter a later response to a fixed stimulus: feedback must alter the derived present state, and the observation map at that stimulus must separate the two present states.

## Closed-loop factorization

One encounter is represented as

```text
context
  -> currentSelf
  -> observation
  -> evidence
  -> unresolved difference
  -> gate
  -> selected action
  -> feedback(outcome)
  -> next context.
```

No numerical formula is fixed for any arrow.

The complete encounter update is lifted into the existing KuuOS finite-history carrier:

```text
toHistoryTransport :
  HistoryTransport (Stimulus × Outcome) Context.
```

Therefore trajectory composition is exact:

```text
T(left ++ right, x) = T(left, T(right, x)).
```

The future response after a split history inherits the same composition law.

## Coordinate-specific sensitivity

Formal v0.1 defines context relations for pairs differing only in:

- body;
- episodic memory;
- structural memory;
- relation.

`CurrentSelfSensitiveAlong R` is a witness that such a coordinate difference reaches the derived present state.

If the fixed-stimulus observation map is injective, then

```text
current-state sensitivity
  -> same-stimulus response sensitivity.
```

This is the abstract theorem-level content behind the surrogate's body-state, structural-memory, and relationship experiments. It does not assert that any particular human or AI system satisfies the sensitivity hypotheses.

## Reversible probe policy

The supplied Python model used a hand-selected numerical uncertainty threshold. KuuOS does not adopt that threshold.

Instead:

```text
HighUncertainty : Delta -> Prop
Probe           : Action -> Prop
Reversible      : Action -> Prop
```

are abstract predicates. A `ReversibleProbePolicy` certifies

```text
HighUncertainty(delta)
  -> Probe(selectedAction)
  -> Reversible(selectedAction).
```

This aligns with the existing DecisionOS Middle-Way / reversibility architecture without replacing its interval-valued deliberation kernel.

## Relation to existing KuuOS layers

This file is deliberately a leaf extension over the established history-sensitive transport infrastructure. It complements rather than replaces:

- `DependentOriginationMemoryLiftedHistoryTransportV0_7`;
- `DependentOriginationProcessTensorMemoryBridgeV0_8`;
- DecisionOS relational deliberation and reversibility gates;
- the later presentation-independent higher-categorical dependent-origination spine.

It is not inserted into the current numbered core-spine frontier because an independent Draft PR is already advancing that frontier. This keeps the change additive and avoids coupling a behavioral-semantics extraction to the ongoing scaled-anodyne/WFS construction.

## Scope boundary

Formal v0.1 makes no claim of:

- empirical human psychology;
- clinical efficacy or treatment guidance;
- hidden ChatGPT-state measurement;
- numerical calibration;
- equivalence with the official KuuOS runtime;
- quantum, Hamiltonian, spectral-gap, or Yang--Mills authority.

Its claim is only structural: a relational feedback loop with a derived present-state readout can be represented as an exact KuuOS finite-history process, and the conditions under which context changes become future same-stimulus response changes can be stated and proved explicitly.
