# Dependent Origination: Scaled Horn Attachment Lifting v1.40

Version 1.40 moves the strictification frontier one geometric level below the two-sided cylinder-extension interface of v1.39.

## Canonical attachment

For an inner horn `Λ[n,i] ⊂ Δ[n]` and endpoint `ε ∈ {0,1}`, define

```text
Aε(n,i) = (Δ[n] × {ε}) ∪ (Λ[n,i] × Δ[1])
         ⊂ Δ[n] × Δ[1].
```

This is represented by Mathlib `Subcomplex.unionProd`.  Its endpoint piece and horn-cylinder piece form an actual pushout via `Subcomplex.unionProd.isPushout`.

Given a literal scaled boundary realization `q : Δ[n] -> X` and a relative horn homotopy `H`, the endpoint map and `H.h` agree on their intersection.  Therefore `IsPushout.desc` produces the canonical attachment map

```text
Aε(n,i) -> X.
```

No choice of an arbitrary attachment map is added.

## Attachment lifting

The new primitive geometric condition asks that the canonical attachment map extend across

```text
Aε(n,i) -> Δ[n] × Δ[1]
```

and that the opposite endpoint of the extension remains scaled.

Two directions are used:

```text
ε = 0 : forward attachment lifting
ε = 1 : backward attachment lifting.
```

The asymmetry of a single simplicial homotopy is therefore handled without assuming that a homotopy is reversible.

## Derived spine

The formal implication is

```text
ScaledHornProblemAttachmentLifting
  -> ScaledHornProblemCylinderExtension        (v1.39)
  -> homotopy-class strictification            (v1.39)
  -> strict fibrancy = homotopy-class fibrancy (v1.38).
```

At family level:

```text
ScaledHornFamilyAttachmentLifting
  -> ScaledHornFamilyCylinderExtension
  -> ScaledHornFamilyHomotopyClassStrictification.
```

Combined with the v1.37 presentation-independent homotopy-class invariant, a coherent normalized scaled bicategorical model equivalence carrying attachment lifting on both presentations yields presentation-independent strict global scaled-Duskin fibrancy.

## Mathematical boundary

This layer does **not** assert that the attachment inclusion is already a scaled-anodyne extension in pinned Mathlib.  The pinned revision has ordinary horn anodyne extensions but no completed inner/scaled anodyne model structure suitable for that identification.

The remaining theorem is now concrete:

```text
for the chosen global scaled-Duskin presentation,
prove the canonical union-product horn-cylinder attachment maps
have the required two-sided extension property with scaled opposite endpoint.
```

That theorem can be attacked either by a direct combinatorial scaled extension construction or by first formalizing the appropriate scaled-anodyne/pushout-product class and proving these attachment inclusions belong to it.
