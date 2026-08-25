# Dependent Origination Homotopy-Class Strictification Formal v1.38

## Purpose

Version 1.37 proved that selected scaled Duskin horn filling modulo boundary
simplicial homotopy class is invariant under coherent normalized scaled
bicategorical model equivalence.  Version 1.38 isolates the exact additional
lifting property required to recover literal strict horn filling without using
fibrancy circularly.

## Two strictification levels

### Universal

`UniversalScaledHornHomotopyClassStrictification X sX` requires every scaled
horn problem in `(X,sX)` to admit strict replacement whenever it admits a
homotopy-class filler.

This is deliberately strong.  It implies:

- family-local strictification for every chosen admissible family;
- the v1.33 one-step `ScaledHornHomotopyRectification` property.

### Family-local

`ScaledHornFamilyHomotopyClassStrictification X sX F` only requires the same
replacement for horn problems selected by the family `F`.

This is the minimal strictification input needed for the existing
`HasScaledHornFillers X sX F` predicate.

## Exact equivalence inside one presentation

Under family-local strictification:

```text
HasScaledHornFillers X sX F
  <->
HasHomotopyClassScaledHornFillers X sX F.
```

The forward implication is unconditional and was already implicit in v1.37:
a strict filler has literal boundary equality and therefore class equality.
The reverse implication is exactly the local strictification property.

## Presentation-independent strict fibrancy

For models `B` and `C`, v1.37 supplies

```text
class-fibrant(B) <-> class-fibrant(C)
```

from normalization, coherent strong quasi-inverse data, full scaled Duskin
transport, and admissible-family preservation.

If each presentation additionally has family-local strictification, v1.38
proves

```text
strict-fibrant(B)
  <-> class-fibrant(B)
  <-> class-fibrant(C)
  <-> strict-fibrant(C).
```

The package is

`CoherentNormalizedScaledStrictifiableModelEquivalence`.

Its strict-fibrancy theorem is

`globalDuskinStrictFibrancy_iff`.

## Logical boundary

No theorem asserts

```text
arbitrary bicategory
  -> homotopy-class strictification.
```

Nor is strictification obtained from a global prism, from class-level
presentation invariance, or from the desired strict fibrancy itself.

The remaining independent problem is now sharply stated:

```text
chosen standard scaled-anodyne generator family
  + appropriate relative lifting / cylinder-extension theorem
  -> family-local homotopy-class strictification.
```

That theorem, once formalized for a concrete standard scaled presentation,
would discharge the final extra field needed for unconditional strict
presentation invariance in that presentation.
