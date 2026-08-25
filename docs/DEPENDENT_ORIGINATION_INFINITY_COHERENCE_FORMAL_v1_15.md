# Dependent Origination — Infinity-Coherence Interface v1.15

## Purpose

v1.15 adds an **all-dimensional coherence carrier** above the genuine bicategorical layer.

The design is intentionally conservative. The repository now has:

- ordinary contextual transport;
- explicit 2-cell coherence;
- a genuine Mathlib bicategory;
- higher multicategorical operation cells;
- and now cells in every natural-number dimension through a reflexive globular tower.

It does **not** yet claim a proved quasicategory, complete Segal space, or other complete model of an infinity category.

## Reflexive globular tower

`ReflexiveGlobularCoherenceTower` supplies

```text
Cell(0), Cell(1), Cell(2), ...
```

with source and target maps

```text
s_n,t_n : Cell(n+1) -> Cell(n)
```

and identity/degeneracy cells

```text
id_n : Cell(n) -> Cell(n+1).
```

The globularity equations are

```text
s s = s t
t s = t t.
```

Thus higher cells have coherent parallel boundaries in all dimensions.

## Bicategorical 2-truncation bridge

`InfinityCoherenceInterface` contains the existing `BicategoricalTransportSystem` and embeds:

```text
objects        -> Cell(0)
1-morphisms    -> Cell(1)
2-morphisms    -> Cell(2).
```

The source and target equations for these embeddings are explicit fields, so the first three levels of the tower recover the bicategorical boundaries.

The current state semantics remains set-truncated at dimension 2: a bicategorical 2-cell still gives equality of represented state transports.

## Higher dimensions

Every cell has an identity higher cell, giving a coherent tower to arbitrary finite dimension. Nontrivial higher cells may also be supplied by a concrete realization.

This is enough to provide a stable interface for future higher models without pretending that all infinity-categorical axioms have already been proved.

## Simplicial route

The pinned Mathlib revision contains native simplicial-object infrastructure. v1.15 exposes `SimplicialCoherenceCandidate`, a wrapper around a `Type`-valued simplicial object, as a future realization target.

A simplicial object alone is not a quasicategory. A future upgrade must add the relevant horn-filling or Segal/completeness conditions before the stronger name is used.

## Relationship with the other axes

The current architecture can now be read as

```text
Dependent Origination Core
  |
  +-- enriched relation texture
  +-- stack-effective local/global descent when supplied
  +-- bicategorical and all-dimensional coherence
  +-- higher-multicategory joint dependence
  +-- monoidal causal process theory
```

These axes are independent unless an explicit bridge theorem connects them.

## Boundary

v1.15 does not claim:

- quasicategory horn filling;
- Segal or complete-Segal conditions;
- infinity-stack descent;
- equivalence between globular and simplicial presentations;
- all higher cells are invertible;
- quantum or physical Yang--Mills authority.

Those remain explicit future obligations.
