# WORLD Kū Vacuum Central Reference State Bridge v0.50

v0.50 promotes the completed-Hilbert-space vacuum introduced in v0.49 from an isolated analytic layer to the common reference state of the WORLD mathematical sidecar.

The unifying path is:

```text
OS reflection positivity
  -> completed Hilbert-space vacuum Ω_Kū
  -> vacuum state ω_Kū
  -> vacuum correlation functions
  -> modular reference state
  -> relative entropy against comparison states
  -> Petz recovery preserving the vacuum reference
  -> excitation vectors π(a)Ω_Kū
```

The word central means a common organizing reference.

It does not mean that the vacuum vector, the vacuum state, or the represented observables belong to the algebraic center.

## Common reference state

The v0.49 vacuum is reused without replacement:

```text
Ω_Kū = Ω_v0.49
ω_Kū(a) = <Ω_Kū, π(a)Ω_Kū>.
```

The v0.33 modular reference state is identified with the same functional:

```text
referenceState(a) = ω_Kū(a).
```

This equality is the principal typed connection of v0.50.

It makes the earlier modular, relative-entropy, and recovery bridges read from one shared reference state rather than from unrelated state symbols.

## Reflection positivity

The positive-time OS form remains the entry point:

```text
Re (F, F)_OS >= 0.
```

After quotienting null directions and completing, the constant-observable class becomes Ω_Kū.

Thus reflection positivity supplies the Hilbert carrier and the reference vector used by all later layers.

The quotient and completion existence theorem remains an analytic receipt inherited from v0.49.

## Vacuum correlations

The one-point function is

```text
ω_Kū(a).
```

The two-point function is

```text
C_Kū(a,b) = ω_Kū(ab)
           = <Ω_Kū, π(ab)Ω_Kū>.
```

These correlations use the same vector state as modular theory and recovery.

Runtime does not numerically evaluate the correlation functions.

## Modular theory

The v0.32 modular flow and v0.33 reference state are anchored at ω_Kū.

```text
ω_Kū(σ_t(a)) = ω_Kū(a).
```

The cyclic and separating role of Ω_Kū continues to support the Tomita and modular structures.

Modular time remains distinct from physical time.

## Relative entropy

The local and global Araki relative entropies from v0.34 are interpreted as comparison-state quantities relative to ω_Kū.

The existing Lean-direct consequences remain available:

```text
0 <= S_region
S_region <= S_global
region inclusion implies data processing
```

The analytic Araki formula, relative modular logarithm, lower semicontinuity, and full normal-UCP theorem remain external receipts.

Relative entropy is not an ontological distance between WORLD states and is not a truth score.

## Petz recovery

The v0.35 recovered channel preserves the same vacuum reference:

```text
ω_Kū(R_Petz(Φ(a))) = ω_Kū(a).
```

The recovered channel remains unital and idempotent on its declared range.

Recovery means recovery of declared state statistics under the supplied channel structure.

It does not mean WORLD overwrite, memory restoration, causal reversal, or automatic correction of an agent state.

## Excitation states

Every represented observable generates an excitation vector

```text
|a>_Kū = π(a)Ω_Kū.
```

The identity observable produces the vacuum:

```text
|1>_Kū = Ω_Kū.
```

The vacuum expectation of an observable is the overlap

```text
<Ω_Kū, |a>_Kū> = ω_Kū(a).
```

The excitation sector is therefore organized around the same state used by reflection positivity, modular theory, relative entropy, and recovery.

An excitation vector is not a truth claim, execution instruction, or unique physical particle state unless additional physical hypotheses are supplied.

## Lean-direct surface

Lean directly verifies:

- unit norm and nonvanishing of the central vacuum;
- equality with the existing cyclic and separating standard-form vector;
- access to OS reflection positivity;
- equality of the vacuum functional and modular reference state;
- vector-state formulas for one-point and two-point vacuum correlations;
- excitation-vector construction and the identity excitation;
- modular stationarity of the vacuum state;
- nonnegativity, global boundedness, and regional data processing for vacuum-relative entropy aliases;
- exact preservation of the vacuum reference by the recovered channel;
- unitality and idempotence of the recovered channel;
- analytic-receipt, runtime-boundary, and representation-boundary packages.

## Fixed boundary

```text
central reference != algebraic center
vacuum state != truth authority
excitation state != truth authority
relative entropy != ontological distance
Petz recovery != WORLD overwrite
modular time != physical time
WORLD != vacuum
Kū != zero vector
validation != truth
candidate != authority
```

The v0.50 bridge is read-only.

It does not compute correlation functions, compute relative entropy, construct a Petz map, build actual excitation vectors at runtime, execute modular flow, update WORLD, or assert external physical realization.
