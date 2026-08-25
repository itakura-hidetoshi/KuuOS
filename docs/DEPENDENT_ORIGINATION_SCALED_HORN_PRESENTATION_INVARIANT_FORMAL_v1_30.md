# Dependent Origination — Scaled Horn Presentation Invariant v1.30

## Goal

Version 1.29 proved forward transport of scaled horn problems and fillers along a scaled map. That does **not** imply target fibrancy, because arbitrary target horns need not lie in the image.

Version 1.30 adds exactly the missing abstraction: a bidirectional equivalence of admissible horn presentations.

## Core object

`ScaledHornPresentationEquivalence HX HY` contains:

- forward and backward maps on horn-extension problems;
- preservation of admissibility in both directions;
- forward and backward filler transport;
- filler-existence equivalences for forward-after-backward and backward-after-forward.

This is intentionally weaker than an isomorphism of the ambient scaled simplicial sets.

## Main theorem

The central theorem is

```text
HasScaledHornFillers HX ↔ HasScaledHornFillers HY
```

for every `ScaledHornPresentationEquivalence HX HY`.

Thus scaled horn fibrancy is a presentation-independent invariant once the admissible horn presentations are equivalent.

## Conceptual meaning

The higher categorical realization can change presentation while preserving the same intrinsic filler property:

```text
presentation A
   ↓
intrinsic admissible horn/filler content
   ↑
presentation B
```

The invariant is therefore no longer tied to one chosen global scaled Duskin carrier.

## Boundary

This version does not yet prove that an arbitrary bicategorical model equivalence automatically induces a `ScaledHornPresentationEquivalence`.

The next mathematical task is to construct that bridge from normalized bicategorical model-equivalence data and then compare complete global `(∞,2)` presentations.
