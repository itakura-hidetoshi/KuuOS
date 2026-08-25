# Dependent Origination Globular / Nerve Comparison — Formal v1.17

## Status

This layer corrects a tempting but false universal statement.

The v1.15 carrier

```text
ReflexiveGlobularCoherenceTower
```

contains arbitrary cell types in every natural-number dimension, together with
source, target and reflexive identity operations satisfying globularity.

The v1.16 carrier

```text
dependentNerve D = N(D.state.Elements)
```

is a simplicial set obtained from the category of context-state elements.
These are different structures.  The parent axioms do not imply an equivalence
between an arbitrary v1.15 tower and `N(∫D)`.

## Necessary comparison data

v1.17 introduces

```text
LevelwiseNerveCompatible T D
```

with fields

```text
T.Cell n ≃ (dependentNerve D).obj (op ⦋n⦌)
```

for every `n`.

This is deliberately only a necessary carrier-level comparison.  A genuine
globular/simplicial equivalence would additionally have to relate globular
source/target/identity data to all simplicial face and degeneracy operators.
That extra realization is not inferred from v1.15.

## Concrete obstruction

The file defines

```text
unitTower
```

with exactly one cell in every dimension.

It also defines

```text
twoStateSystem
```

consisting of one discrete context carrying two states.  Its category of
elements therefore has two distinct context-state objects, and its dependent
nerve has two distinct zero-simplices.

The theorem

```text
unitTower_not_levelwise_compatible
```

proves that the one-cell tower cannot even be levelwise equivalent at dimension
zero to that dependent nerve.

The existential theorem

```text
no_universal_globular_nerve_comparison
```

therefore establishes a formal obstruction to any theorem of the form

```text
forall T D, T ≃ N(∫D).
```

## Mathematical meaning

The corrected hierarchy is

```text
v1.15 arbitrary globular coherence
  + no realization data
  -> no automatic simplicial comparison

v1.15 chosen tower
  + explicit comparison / realization data
  -> possible comparison with v1.16 dependent nerve.
```

This is a strengthening of claim discipline, not a weakening of the higher
architecture.  The v1.15 tower remains useful as an all-dimensional coherence
interface, and v1.16 remains a genuine quasicategory realization of the
one-categorical dependent-origination parent.  They simply solve different
modeling problems until a bridge is actually supplied.

## Non-claims

v1.17 does not claim:

- every globular tower is simplicial;
- every globular tower is a quasicategory;
- every globular tower is equivalent to `N(∫D)`;
- the v1.15 tower and v1.16 nerve have the same higher cells;
- a globular/simplicial comparison can be obtained from cardinality alone.

The comparison must be constructed, not assumed.
