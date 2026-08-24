# Dependent Origination Free-History Functor — Formal v0.6

## Purpose

This note fixes the categorical meaning of finite history in the KuuOS dependent-origination transport spine.

The parent principle remains:

> dependent origination is compositional transport before object-substance.

The v0.5 layer made ordered finite histories primary.  v0.6 now identifies the exact algebraic/categorical structure carried by that definition.

## 1. Free histories

For an event type `Event`, finite histories are words

```text
List Event.
```

With empty word `[]` and concatenation `++`, `List Event` is the free monoid on `Event`.

Mathlib turns any monoid `M` into a one-object category `CategoryTheory.SingleObj M`.  Therefore KuuOS uses

```text
FreeHistoryCategory Event := SingleObj (List Event).
```

A history word is now a morphism of this category.

## 2. Why the composition orientation matches KuuOS

Mathlib's `SingleObj` uses reversed multiplication for categorical composition:

```text
f ≫ g = g * f.
```

For the list monoid, multiplication is concatenation.  Hence

```text
f ≫ g = g ++ f.
```

KuuOS v0.5 uses

```text
eval (left ++ right) x = eval left (eval right x).
```

Therefore the Mathlib categorical composition law gives exactly the intended temporal/relational convention: the right history acts first, then the left history.

## 3. History transport is a functor

Every

```text
H : HistoryTransport Event State
```

canonically determines

```text
H.toFreeHistoryFunctor :
  SingleObj (List Event) ⥤ Type
```

with

```text
obj _      = State
map word   = H.eval word.
```

The two fields already present in `HistoryTransport`,

```text
eval [] x = x

eval (left ++ right) x = eval left (eval right x),
```

are exactly the identity and composition laws required by the functor.

Thus the v0.1 categorical spine and the v0.5 history spine are not parallel analogies.  They are the same compositional structure at two abstraction levels.

## 4. Generator theorem

Define the one-event action

```text
singleEventTransport H event := H.eval [event].
```

Then every finite history satisfies

```text
H.eval word x
  = word.foldr (fun event acc => H.singleEventTransport event acc) x.
```

Consequently, a `HistoryTransport` is completely determined by its single-event maps.

Conversely, every arbitrary family

```text
step : Event → State → State
```

generates a compositional history transport by `foldr`.

So, at this layer,

```text
HistoryTransport Event State
```

is precisely a free-monoid action of finite event words on `State`.

## 5. What "history-sensitive" means here

The v0.5 predicate can distinguish two words that have the same coarse summary, for example equal total elapsed time, but different denotation.

This is genuine sensitivity to ordered event history relative to that coarse summary.

However, the strict append law also means all history dependence is mediated through the chosen state carrier and its event actions.  In particular, this layer should not be identified automatically with an arbitrary higher-order process tensor.

A non-Markov model can fit this interface when `State` is an enriched memory-bearing carrier and the event maps update that carrier.  A process tensor that takes interventions as higher-order inputs may instead require a richer event type, richer carrier, or richer source category.

That distinction is intentional.

## 6. Markov / semigroup specialization

The v0.4 positive-time transfer word is already a special case of `HistoryTransport`.

The v0.5 `TotalTimeFactorization` theorem then says its free-history functor factors semantically through the coarse summary

```text
word ↦ word.sum.
```

Hence:

```text
free ordered history
  → optional coarse summary
  → additive semigroup
  → linear transfer
  → vacuum subtraction
  → exponential gap/readout decay.
```

The coarse summary is additional structure.  It is not part of the definition of dependent origination.

## 7. Relation to existing KuuOS process-tensor modules

Existing KuuOS modules already expose history-bearing process carriers, non-Markov memory visibility, and protected-history receipts.

v0.6 does not promote those modules into the new formal transport structure automatically.  A future bridge must explicitly exhibit the event/carrier/category data and prove the required composition laws.

This avoids converting architectural vocabulary into theorem authority.

## 8. Philosophical reading

The formal picture is now:

```text
objects are not primary substances;
relations compose;
finite relational histories are morphisms;
state appearances are transported functorially along those morphisms.
```

For gauge transport, reversible arrows give the groupoid branch.
For finite ordered history, free words give the free-category/monoid branch.
For Euclidean positive time, an additional quotient/factorization may collapse histories to total time.

The common structural content is compositional dependence, not a privileged representative.

## 9. Physical authority boundary

This file and its Lean companion are KuuOS structural mathematics only.

They do **not** construct or assert:

- a Yang–Mills Hamiltonian,
- a spectral measure,
- a physical vacuum-orthogonal Hilbert sector,
- a Yang–Mills process tensor,
- or a physical mass gap.

Those obligations remain with the authoritative physical proof development in `itakura-hidetoshi/4d-mass-gap`.
