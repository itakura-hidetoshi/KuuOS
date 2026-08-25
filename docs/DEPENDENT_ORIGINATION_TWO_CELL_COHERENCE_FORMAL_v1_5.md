# Dependent Origination Two-Cell Coherence — Formal v1.5

## Purpose

v1.4 allowed arbitrary filtered indexing categories, but eventual path coherence
was still expressed by strict equality:

```text
f >> h = g >> h
```

and the rooted refinement cocone also used strict equality:

```text
toChart i >> chart.map f = toChart j.
```

v1.5 is the first higher-categorical lift of the parent dependent-origination
spine.  It replaces those source-level equalities by explicit typed two-cells.

## Core reading

```text
objects       = contexts
1-morphisms   = admissible context/refinement transports
2-cells       = explicit relations between parallel transport paths
```

This is closer to the intended dependent-origination reading than erasing path
differences by equality.  Distinct paths may remain distinct while a higher
coherence witness relates them.

## Minimal two-cell carrier

`Refinement2CellStructure C` contains:

- a type `cell f g` of two-cells between parallel arrows;
- identity two-cells;
- vertical composition;
- left whiskering;
- right whiskering.

Two-cells are data rather than propositions, so multiple witnesses are not
collapsed by definition.

This is intentionally **not yet a full bicategory**.  The complete unit,
associativity, interchange, and higher coherence-law package is not claimed in
v1.5.

## Strict v1.4 as a specialization

`equality2CellStructure` regards an equality `f = g` as a degenerate two-cell.
Consequently:

```text
FilteredIndexing.toTwoFiltered
FilteredRefinementDiagram.toTwoDimensional
```

embed the v1.4 structures into v1.5 without weakening any earlier theorem.

Thus the hierarchy is additive:

```text
strict equality coherence
    -> equality two-cells
    -> general typed two-cells
```

not a replacement of the v1.4 strict layer.

## Set-truncated realization

The current parent state transport is still a functor into `Type`:

```text
D : Context -> Type.
```

A higher source does not automatically make this target higher-categorical.
`SetTruncatedTwoRealization D H` therefore explicitly requires:

```text
alpha : cell f g
----------------
D.transport f = D.transport g
```

This says that the present state semantics intentionally forgets the higher
path distinction.  The source two-cell is retained, but the `Type`-valued
realization is a set-truncation of it.

A later higher target may replace this equality by an explicit equivalence or
higher morphism.  v1.5 does not claim that stronger realization.

## Two-dimensional refinement diagram

`TwoDimensionalRefinementDiagram` contains:

```text
rootContext
chart : J -> Context
indexCellMap
root-to-chart arrows
rootCoherence as a context two-cell
```

The former strict equation

```text
toChart i >> chart.map f = toChart j
```

is replaced by

```text
toChart i >> chart.map f  ==>  toChart j.
```

After choosing a set-truncated realization, theorem
`root_transport_coherent` recovers the ordinary state-level equality required
for a root-generated coherent family.

## Two-filtered indexing

`TwoFilteredIndexing` keeps the common-future object condition and replaces
strict eventual coequalization by:

```text
for f,g : i -> j,
there exist h : j -> k and alpha : (f >> h) ==> (g >> h).
```

The theorem `eventual_parallel_transport_agreement` proves that these paths
act equally after set-truncated realization, without asserting that the source
paths themselves are equal.

## Semantic descent

A coherent state family still has unique invariant meaning on a two-filtered
diagram:

```text
twoFilteredSemanticDescends_of_coherent
```

The semantic theorem needs only the common-future object part of filteredness;
the two-cell layer preserves stronger path information rather than being needed
to manufacture semantic equality.

This distinction is deliberate:

```text
unique invariant meaning
!=
source path equality
```

and now also:

```text
set-truncated path agreement
!=
absence of higher path structure.
```

## Relation to the larger roadmap

v1.5 addresses the `higher category` axis first.

The other proposed axes remain independent future extensions:

- sheaf / stack: local-to-global gluing with stronger descent conditions;
- operad / multicategory: multiple conditions jointly producing one context;
- process theory: monoidal parallel composition;
- enriched category: structured hom objects / strengths / costs / metrics;
- infinity-category: unbounded coherent higher morphisms;
- causal structure: orientation, interventions, independence, and no-signalling constraints.

They should not be folded into one opaque master definition.

## Scope boundary

v1.5 does **not** claim:

- a full strict 2-category;
- a bicategory;
- an infinity-category;
- a Grothendieck topology;
- a sheaf, stack, or higher stack;
- an operad or multicategory;
- a symmetric monoidal process theory;
- enriched-category structure;
- causal completeness;
- a categorical colimit or Mathlib final-functor theorem;
- quantum/process-tensor authority in the parent core;
- Hamiltonian, mass-gap, or physical Yang--Mills theorem authority.

The parent interpretation remains:

```text
dependent origination
= context-dependent establishment
+ composable transport
+ explicitly retained coherence between transport paths.
```
