# Dependent Origination Memory-Lifted History — formal v0.7

## Canonical base

This layer is additive over:

```text
main@9a501974d79fd83177abae861a955fe48b0cd0d1
```

It extends the v0.1–v0.6 dependent-origination transport spine without weakening or replacing any earlier theorem.

## Purpose

The v0.6 layer identified finite dependent-origination history with a free-monoid action / one-object functor:

```text
List Event
→ free history category
→ state-valued functor
```

The next question is how a history-sensitive or non-Markov observable dynamics can coexist with this strict functorial composition law.

The answer formalized here is to distinguish:

```text
full state = visible state × explicit memory
```

from the visible projection alone.

On the full state, finite history is strictly compositional. After memory is projected away, visible evolution depends on the updated memory created by the earlier history.

This is a state-space Markovization bridge. It is not a claim that every process tensor is equivalent to the finite-memory carrier used here.

## Core structure

```lean
structure MemoryLiftedStep
    (Event : Type u) (Visible : Type v) (Memory : Type w) where
  visibleUpdate : Event → Visible → Memory → Visible
  memoryUpdate : Event → Visible → Memory → Memory
```

One event therefore acts on the enlarged state by

```text
(event, (x,m))
↦
(visibleUpdate event x m,
 memoryUpdate event x m).
```

The v0.6 generator theorem then produces the finite-history transport automatically:

```text
MemoryLiftedStep.extendedStep
→ HistoryTransport.ofSingleEventTransport
→ HistoryTransport Event (Visible × Memory)
→ FreeHistoryCategory Event ⥤ Type
```

Thus the enlarged system inherits the same functorial dependent-origination semantics as the generic categorical spine.

## Exact enlarged-state composition

For finite histories `left` and `right`,

```text
H(left ++ right, state)
=
H(left, H(right, state)).
```

This is strict functoriality on the full visible-plus-memory carrier.

No invertibility or total-time factorization is assumed.

## Visible projection

Define

```text
visibleEval m word x
memoryEval  m word x
```

as the first and second projections of the enlarged-state history result starting from `(x,m)`.

Then the visible projection satisfies the exact identity

```text
visibleEval m (left ++ right) x
=
visibleEval (memoryEval m right x)
  left
  (visibleEval m right x).
```

Likewise the memory projection satisfies

```text
memoryEval m (left ++ right) x
=
memoryEval (memoryEval m right x)
  left
  (visibleEval m right x).
```

This is the precise non-Markov boundary in the present state-space model:

- the enlarged state is strictly compositional;
- the visible state alone is not closed under composition with the original fixed memory;
- the memory produced by the previous history is part of the condition for the next visible update.

In KuuOS language, the visible state does not possess an autonomous substance-like evolution law independent of its retained relational conditions.

## Additive coarse summary and genuine visible history sensitivity

When `Event = Time` with `[AddMonoid Time]`, define genuine visible history sensitivity at initial memory `m₀` by the existence of finite histories `left`, `right` with

```text
left.sum = right.sum
```

but

```text
visibleEval m₀ left x ≠ visibleEval m₀ right x
```

for some visible state `x`.

This is a direct observable obstruction to collapsing history into total elapsed time.

The formal theorem proves:

```text
GenuinelyVisibleHistorySensitive S m₀
→
GenuinelyHistorySensitive S.toHistoryTransport
```

and consequently

```text
GenuinelyVisibleHistorySensitive S m₀
→
¬ Nonempty (TotalTimeFactorization S.toHistoryTransport).
```

Equivalently, if a total-time factorization certificate exists on the enlarged state, then equal-total-time histories must agree after every fixed-memory visible projection and after every visible readout.

## Relation to the v0.4 transfer semigroup

The v0.4 transfer-word model satisfies

```text
Eval(word, x) = T_(word.sum) x.
```

Therefore it lies on the total-time-factorized branch.

The present v0.7 layer does not modify that theorem. It clarifies its place in the larger hierarchy:

```text
functorial dependent origination
  ↓
free finite history
  ↓
memory-lifted full-state history
  ├─ total-time factorized branch
  │    ↓
  │  additive semigroup
  │    ↓
  │  linear transfer / vacuum / gap / readout decay
  │
  └─ visible history-sensitive branch
       ↓
     no total-time factorization certificate
```

## Relation to existing KuuOS non-Markov memory connection

The existing module

```text
KUOS.WORLD.KuuOSNonMarkovMemoryConnectionV0_72
```

contains a `HistoricalConnection` with a read-only history module and a linear memory kernel

```text
memoryKernel : H →ₗ[A] M.
```

Its `apply` operation combines a directional connection term with the memory-kernel contribution and proves a pathwise Leibniz law.

That existing structure is an analytic connection layer. It does **not** by itself specify a discrete or continuous evolution update for the history carrier.

Therefore v0.7 deliberately does not reinterpret `HistoricalConnection.apply` as a time step. A future explicit bridge from that WORLD layer into `MemoryLiftedStep` must provide, rather than assume:

1. the event/time parameter;
2. the visible evolution update;
3. the memory evolution/update;
4. any compatibility theorem identifying those updates with the analytic historical connection.

This prevents a connection/derivation object from being silently promoted into a dynamical semigroup.

## Relation to process tensors

The memory-lifted state-space construction is a useful realization of history dependence, but it is not the definition of an arbitrary process tensor.

A general higher-order process tensor may require:

- explicit intervention slots;
- varying input/output systems;
- causal multilinear or completely-positive structure;
- richer categories than the free one-object history category;
- memory carriers that are not presented as an ordinary product state.

Accordingly, a future process-tensor bridge must state those additional structures explicitly.

## Buddhist / KuuOS interpretation

The formal content supports the same non-reification boundary used throughout the dependent-origination spine:

- **空**: the visible state is not assigned an autonomous, context-free evolution essence;
- **縁起**: the next visible presentation depends on the retained memory/context produced by prior relations;
- **中道**: the formalism neither reifies hidden memory as ultimate substance nor erases the causal relevance of relational history;
- **世俗的構造**: the enlarged state and its functorial transport are explicit conventional mathematical carriers used for prediction and composition.

This remains a structural interpretation. The category, memory carrier, transfer operators, and gap parameters are not promoted to ultimate metaphysical entities.

## Physical authority boundary

This layer does not construct or assert:

- a Yang–Mills Hamiltonian;
- a Yang–Mills process tensor;
- a physical vacuum-orthogonal Hilbert sector;
- a spectral measure;
- a physical mass gap;
- a theorem identifying a KuuOS memory carrier with a gauge-theory environment.

`itakura-hidetoshi/4d-mass-gap` remains authoritative for its own physical proof obligations. KuuOS imports only the structural proof pattern where an explicit bridge is supplied.
