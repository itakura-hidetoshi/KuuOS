# Dependent Origination — Scaled Horn Cylinder Extension v1.39

## Purpose

Version 1.38 isolated the local condition needed to recover literal strict
scaled-horn fibrancy from the presentation-independent homotopy-class horn
invariant.  Version 1.39 replaces that bare strictification interface by a
geometric sufficient condition.

The key observation is that Mathlib's `RelativeMorphism.HomotopyClass` is a
`Quot` by one-step relative simplicial homotopies.  Equality of two quotient
classes yields, by `Quot.eqvGen_exact`, the equivalence closure of the
one-step relation.

Thus a homotopy-class filler can be made strict whenever a scaled simplex can
be transported in both endpoint directions across every one-step horn
homotopy.

## Boundary realization

For a relative horn map `f : Λ[n,i] -> X`, a
`ScaledHornBoundaryRealization` is a scaled simplex

```text
q : Δ[n] -> X
```

with literal boundary equation

```text
f = Λ[n,i].ι ; q.
```

Intermediate representatives in a homotopy-class zigzag are not required to
preserve the horn scaling; the simplex itself remains scaled throughout.

## Forward and backward cylinder extension

For a one-step relative homotopy

```text
H : f ~ g
```

a forward cylinder starts with a scaled realization of `f` at endpoint zero:

```text
Δ[n] × Δ[1] -> X
```

whose restriction to `Λ[n,i] × Δ[1]` is `H`, and whose endpoint-one simplex is
scaled.  This produces a literal scaled realization of `g`.

The backward cylinder fixes a scaled realization of `g` at endpoint one and
requires a scaled endpoint zero, producing a literal realization of `f`.

Both directions are necessary because `Quot` equality uses the equivalence
closure of one-step homotopy.  Formal symmetry in `Relation.EqvGen` must not be
confused with an actual reverse simplicial homotopy.

## EqvGen strictification

The proof proceeds simultaneously in both directions over

```text
Relation.EqvGen HornHomotopyStep f g.
```

- `rel`: use the forward/backward cylinder extensions;
- `refl`: identity transport;
- `symm`: swap the two induction hypotheses;
- `trans`: compose transports.

Consequently

```text
ScaledHornProblemCylinderExtension
  -> homotopy-class filler
  -> strict scaled filler.
```

Family-local cylinder extension therefore implies the v1.38
`ScaledHornFamilyHomotopyClassStrictification` interface, and universal
cylinder extension implies universal strictification.

## Presentation-independent strict fibrancy

Combining v1.37 and v1.39 gives

```text
coherent normalized scaled model equivalence
  -> presentation-independent homotopy-class horn fibrancy

family-local two-sided cylinder extension on B and C
  -> local homotopy-class strictification on B and C
  -> strict_B <-> class_B <-> class_C <-> strict_C.
```

The resulting package is

```text
CoherentNormalizedScaledCylinderExtendableModelEquivalence.
```

## Ordinary anodyne anchor

The pinned Mathlib revision proves

```text
SSet.anodyneExtensions Λ[n,i].ι
```

for every ordinary horn inclusion with `n > 0`.  Hence every underlying inner
horn in the KuuOS presentation is an ordinary anodyne extension.

This is not yet the desired scaled theorem.  The same pinned Mathlib source
explicitly lists inner variants of anodyne extensions as TODO and does not
provide a scaled-anodyne model structure.

Therefore v1.39 does **not** claim

```text
ordinary anodyne = inner anodyne = scaled anodyne.
```

## Remaining exact theorem

The remaining independent target is

```text
concrete standard scaled-anodyne generator presentation
  + relative scaled cylinder / endpoint lifting
  -> ScaledHornFamilyCylinderExtension.
```

Once this is proved for the selected global Duskin scaling, the v1.38 bare
strictification fields disappear automatically through v1.39.
