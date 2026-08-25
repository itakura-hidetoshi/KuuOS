# Dependent Origination Bicategorical Coherence — Formal v1.6

## Purpose

v1.5 introduced explicit two-cells between parallel dependent-origination paths, but intentionally did not claim a full bicategory. v1.6 moves the higher-categorical carrier to Mathlib's native `CategoryTheory.Bicategory` at the repository-pinned Mathlib revision.

The source now carries genuine bicategorical structure:

- categories of 1-morphisms and 2-morphisms;
- associator 2-isomorphisms;
- left and right unitors;
- left and right whiskering;
- whiskering exchange;
- pentagon coherence;
- triangle coherence.

## Dependent-origination reading

```text
objects       = contexts
1-morphisms   = admissible contextual transports
2-morphisms   = explicit relations between transport paths
associator    = coherent reassociation of dependent paths
unitors       = coherent insertion/removal of identity context change
pentagon      = consistency of fourfold reassociation
triangle      = compatibility of associator with units
```

The critical change from v1.5 is that these are no longer an informal package attached to an ordinary category. They are supplied by a genuine bicategory instance.

## State realization

`BicategoricalTransportSystem` keeps the present state semantics intentionally set-truncated:

```text
η : f ==> g
----------------
transport f = transport g
```

This does not remove `η` from the source. It says only that the current `Type`-valued state carrier forgets the higher distinction when producing state maps.

Theorems include:

- `transport_eq_of_twoCell`;
- `transport_associator`;
- `transport_leftUnitor`;
- `transport_rightUnitor`;
- `horizontalComp_exchange`;
- `source_pentagon`;
- `source_triangle`.

## Strict one-category bridge

Mathlib's `LocallyDiscrete C` promotes any ordinary category to a strict bicategory whose 2-morphisms are equalities. Therefore every existing `FunctorialTransportSystem C` embeds through

```text
FunctorialTransportSystem.toLocallyDiscreteBicategorical
```

without changing its state transport semantics.

This gives an additive hierarchy:

```text
one-category transport
-> locally discrete bicategory
-> explicit v1.5 two-cell carrier
-> native bicategory
```

The v1.5 carrier is not silently declared bicategorical. A nontrivial v1.5 carrier needs the full coherence structure before it belongs to the v1.6 layer.

## Philosophical scope

The mathematical interpretation is:

```text
different dependent paths need not be identical;
their reassociations and comparisons can themselves be structured relations.
```

This is compatible with the KuuOS reading of dependent origination as composable contextual establishment before object-substance specialization. It is not a claim that bicategory theory and Buddhist dependent origination are identical doctrines.

## Boundaries

v1.6 does not yet add:

- unbounded higher morphisms;
- infinity-category structure;
- sheaf/stack descent;
- operadic multi-input conditioning;
- symmetric monoidal process theory;
- enriched hom objects;
- causal/no-signalling structure;
- quantum or physical theorem authority to the parent core.

The operadic multi-condition axis is introduced separately in v1.7 so that higher coherence and multi-input conditioning remain distinguishable structural dimensions.
