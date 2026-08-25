# Dependent Origination Quasicategory Nerve — Formal v1.16

## Status

This layer gives the non-quantum dependent-origination parent a concrete
simplicial-set realization for which strict Segal, inner horn filling, and the
native Mathlib `Quasicategory` predicate are actually proved.

It is additive over v1.15. No earlier theorem or assumption is weakened.

## Starting point

The parent core is

```text
D.state : Context ⥤ Type
```

with transport

```text
D.transport f x = D.state.map f x.
```

Instead of taking only the nerve of the context category, v1.16 uses Mathlib's
category of elements

```text
D.state.Elements.
```

An object is a pair

```text
(X, x)
```

with `x : D.state.obj X`. A morphism

```text
(X, x) -> (Y, y)
```

is a context morphism `f : X -> Y` satisfying

```text
D.state.map f x = y.
```

Thus the category itself already records the defining dependent-origination
condition that an admissible contextual relation transports the conditioned
state to the target state.

## Dependent-origination nerve

Define

```text
N_D := CategoryTheory.nerve D.state.Elements.
```

The `n`-simplices of `N_D` are composable strings of morphisms in the category
of elements, hence composable strings of context-state transports.

## Strict Segal theorem

Repository-pinned Mathlib proves that the nerve of every category is strict
Segal. v1.16 specializes

```text
CategoryTheory.Nerve.strictSegal D.state.Elements
```

to obtain

```text
dependentNerveStrictSegal D :
  SSet.StrictSegal (dependentNerve D).
```

The explicit theorem

```text
dependentNerve_segal D n
```

states

```text
Function.Bijective ((dependentNerve D).spine n).
```

So an `n`-simplex is uniquely determined by its composable length-`n` spine.
This is stronger than merely asserting the existence of composition.

## Strict Segal implies quasicategory

Pinned Mathlib proves

```text
SSet.StrictSegal.quasicategory :
  StrictSegal X -> Quasicategory X.
```

Its proof constructs the required inner-horn fillers from the Segal spine.
Applying it to `dependentNerveStrictSegal D` yields

```text
dependentNerve_quasicategory D :
  SSet.Quasicategory (dependentNerve D).
```

This is the native Mathlib quasicategory class, not a KuuOS-local surrogate.

## Inner horn filling

For every inner horn

```text
0 < i < n
```

and every simplicial map

```text
σ₀ : Λ[n,i] -> N_D,
```

v1.16 proves

```text
∃ σ : Δ[n] -> N_D,
  σ₀ = Λ[n,i].ι ≫ σ.
```

The Lean theorem is

```text
dependentNerve_innerHornFilling.
```

It is obtained from the proved quasicategory structure using the native theorem

```text
SSet.Quasicategory.hornFilling.
```

## Mathematical reading

The proved chain is

```text
context-dependent states
  -> category of context-state elements
  -> composable simplicial nerve
  -> unique Segal composition
  -> coherent inner-horn extension
  -> quasicategory.
```

In dependent-origination language, partially specified compatible compositions
of context-state transports admit coherent simplicial completion.

## Relation to v1.15

v1.15 introduced an independent all-dimensional reflexive globular coherence
tower and explicitly did not claim horn filling or quasicategory structure.

v1.16 closes those obligations for the specific canonical realization

```text
N(D.state.Elements).
```

It does **not** yet prove that the arbitrary v1.15 globular tower is equivalent
to this nerve.

Therefore the valid statement is

```text
category-of-elements nerve of the parent transport
  = proved strict-Segal quasicategory,
```

not

```text
every all-dimensional coherence tower
  = quasicategory.
```

## Scope boundary

This layer does not assert:

- equivalence between the v1.15 globular tower and `N_D`;
- a nontrivial `(∞,2)` realization of the v1.6 bicategory;
- complete Segal space structure;
- higher-stack descent;
- that arbitrary operadic or causal extensions are automatically encoded by
  the one-categorical category-of-elements nerve;
- quantum or physical Yang--Mills authority in the parent core.

Those are separate stronger comparison or enrichment problems.
