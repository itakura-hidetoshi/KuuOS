# Dependent Origination — Scaled Terminal RLP Formalization v1.41

## Result

Version 1.41 lowers the strict scaled-fibrancy frontier from the bespoke
attachment-extension interface of v1.40 to a genuine categorical right
lifting property.

The category used here has:

- objects: simplicial sets equipped with an explicit `ScaledSimplicialSet`;
- morphisms: simplicial maps satisfying `IsScaledMap`.

The construction is designed so that the native Mathlib diagonal lift already
contains the scaled endpoint information required by v1.40.

## Minimal attachment scaling

For a simplicial set `X`, `minimalScaling X` declares a 2-simplex thin exactly
when it lies in one of the two degeneracy families

`X.σ 0 x` or `X.σ 1 x`.

Every simplicial map out of this minimal scaling is scaled, by simplicial
naturality of the degeneracies and the requirement that every scaling contains
both degenerate families.

Therefore the canonical attachment map

`(Δ[n] × {ε}) ∪ (Λ[n,i] × Δ[1]) -> X`

is automatically a morphism of scaled simplicial sets when the attachment is
given minimal scaling.

## Cylinder scaling

The cylinder `Δ[n] × Δ[1]` is scaled by projection to the simplex factor:

`thin(t) :<-> simplexScaling.thin(t.1)`.

Both endpoint inclusions

`Δ[n] -> Δ[n] × Δ[1]`

are scaled for this structure.

Hence any scaled morphism from the cylinder to a target has scaled endpoint
restrictions automatically.

## Native terminal RLP

The scaled point is `Δ[0]` with maximal scaling.  It is terminal in the scaled
category.  For a morphism `i : A -> B`, the ordinary Mathlib proposition

`HasLiftingProperty i (X -> point)`

is proved equivalent to extension of every scaled map `A -> X` across `i`.

Applying this to the minimally-scaled horn-cylinder attachment inclusion gives
a globally scaled cylinder extension.  Restriction along the opposite endpoint
then gives the endpoint-scaled condition of v1.40 without any extra
stability axiom.

## Strict-fibrancy spine

The resulting route is

```text
HasLiftingProperty
  canonical scaled attachment inclusion
  (target -> scaled point)
    |
    v
globally scaled cylinder extension
    |
    v
v1.40 attachment lifting
    |
    v
v1.39 two-sided cylinder extension
    |
    v
homotopy-class strictification
    |
    v
strict scaled horn fibrancy.
```

Combined with the previously proved coherent normalized model-equivalence
transport of homotopy-class horn fibrancy, this gives presentation-independent
strict scaled-Duskin fibrancy whenever the selected horn families satisfy the
terminal RLP on both presentations.

## Exact remaining boundary

No ordinary or unscaled anodyne theorem is promoted to a scaled statement.
The remaining independent theorem is now precisely:

> for the chosen standard scaled-anodyne horn family, prove that each canonical
> minimally-scaled horn-cylinder attachment inclusion has the left lifting
> property against the terminal map of the global scaled-Duskin nerve.

Equivalently, the global scaled-Duskin nerve's terminal map must have the right
lifting property against those canonical scaled attachment inclusions.
