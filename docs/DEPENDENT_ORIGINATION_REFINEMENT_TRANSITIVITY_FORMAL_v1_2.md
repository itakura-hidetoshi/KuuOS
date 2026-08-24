# Dependent Origination Refinement Transitivity — Formal v1.2

## Purpose

v1.0 restored dependent origination to its contextual parent:

```text
context category -> state-valued functor -> composable transport.
```

v1.1 then added one local-to-global layer:

```text
root -> chart_i -> common refinement_(i,j),
```

separating state-level descent from invariant semantic descent.

v1.2 asks the next structural question: what happens when every local chart is
itself refined again?

The answer is compositional.  Refinement of refinement is not a new parent
notion.  It can be flattened to one contextual refinement, and descent behaves
transitively.

## 1. Second-stage contextual refinement

For a v1.1 cover `C`, v1.2 introduces

```text
RefinementOfCover C SubIndex
```

with data

```text
chart_i -> subchart_(i,j).
```

For each outer chart `i`, `localCover R i` is an ordinary v1.1 refinement cover
whose root is `chart_i`.

No topology, pullback universal property, groupoid, site, or invertibility is
assumed.

## 2. Flattening

The two stages

```text
root -> chart_i -> subchart_(i,j)
```

are flattened to one cover indexed by

```text
Sigma SubIndex.
```

The flattened root-to-subchart arrow is exactly

```text
C.toChart i >> R.chartToSubchart i j.
```

Functorial transport therefore proves

```text
D(chart_i -> subchart_(i,j)) (D(root -> chart_i) x)
=
D(root -> subchart_(i,j)) x.
```

This theorem is `twoStep_transport_eq_flatten_transport`.

## 3. Nested local families

`NestedLocalStateFamily D R` carries one state in every `subchart_(i,j)`.

It has two canonical views:

- `flatten`: one local family on the flattened cover;
- `ofTop`: refine a chosen top-level local family by transport.

A root state may therefore be transported in two conceptually different but
mathematically identical ways:

```text
root state
 -> top local family
 -> nested family
```

or directly

```text
root state
 -> flattened family.
```

The pointwise identity is formalized by
`nested_ofGlobal_flatten_state_eq`.

## 4. Exact transitivity of state descent

`LocallyDescendsTo D R u s` says that every nested state in `u` is obtained from
its parent state in the top-level family `s`.

`NestedStateDescends D C R u` means:

```text
there exists a top family s such that
  s descends from a root state,
and
  u descends locally from s.
```

The main theorem is

```text
nestedStateDescends_iff_flattenStateDescends
```

and states exactly

```text
NestedStateDescends D C R u
<->
StateDescends D R.flatten u.flatten.
```

Thus state descent is genuinely transitive under contextual refinement.  No
extra overlap or reversibility assumption is required for this equivalence; it
is a consequence of functorial composition.

## 5. Refinement does not manufacture a missing global state

A subtle issue is whether a sufficiently fine family could admit a root-state
witness even though the chosen top-level family does not.

This can happen if inner refinements forget distinctions between parent chart
states.  v1.2 therefore isolates the exact extra hypothesis:

```text
SubcoversSeparateChartStates D R.
```

It says that within every parent chart, agreement after all inner refinements
forces equality already at that parent chart.

Under this separation condition,

```text
not StateDescends D C s
```

plus local descent of `u` from `s` implies

```text
not StateDescends D R.flatten u.flatten.
```

This is theorem

```text
no_flattenStateDescent_of_no_topStateDescent.
```

Hence further contextual conditioning cannot create a hidden global carrier when
the finer observations still separate the states they refine.

## 6. Semantic refinement

For an invariant readout `Readout`, v1.2 defines

```text
SemanticRefinesTo Readout R u s
```

meaning that each subchart state has exactly the same invariant semantic value
as its parent chart state.

Local state descent automatically implies this semantic relation by transport
invariance:

```text
semanticRefinesTo_of_locallyDescendsTo.
```

## 7. Transitivity of semantic descent

Suppose the top family `s` already has one unique semantic value and every
subchart state refines the semantic value of its parent chart.

Then the flattened family has the same unique semantic value:

```text
semanticDescends_flatten_of_semanticRefinesTo.
```

No root-state witness is used.

Combining this with v1.1 gives

```text
top overlap compatibility
+
local descent to the top family
=>
semantic descent of the fully refined family.
```

The theorem is

```text
semanticDescends_flatten_of_top_overlapCompatible_and_localDescent.
```

## 8. Global meaning without global substance survives refinement

The strongest boundary theorem in this layer is

```text
semanticDescent_persists_without_flattenStateDescent.
```

Under:

- nonempty outer and flattened chart families;
- top-level overlap compatibility;
- no top-level root-state witness;
- local state descent into the nested family;
- local subcovers that separate their parent chart states;

it proves simultaneously

```text
not StateDescends D R.flatten u.flatten
```

and

```text
SemanticDescends Readout R.flatten u.flatten.
```

So the v1.1 distinction is stable under further refinement:

```text
no global state carrier
but
one global invariant meaning.
```

The point is structural, not metaphysical.  The formal statement is only that a
unique transport-invariant semantic value can be determined by coherent local
conditioned states even when no root-state witness exists in the chosen state
functor.

## 9. Parent hierarchy after v1.2

```text
Dependent origination parent
  = contextual state functor + composable transport

  -> contextual lens change / system maps
  -> reversible groupoid specialization when available
  -> history and memory specializations
  -> refinement cover
  -> overlap compatibility
  -> optional state descent
  -> invariant semantic descent
  -> refinement of refinement
  -> flattening
  -> state-descent transitivity
  -> semantic-descent transitivity.
```

Quantum/process-tensor and physical layers remain downstream realizations and do
not redefine this parent structure.

## 10. Scope boundary

This layer does not claim:

- a Grothendieck topology;
- sheaf descent on an arbitrary site;
- existence of pullbacks or fiber products;
- higher-categorical descent;
- groupoid-valued or stack-valued gluing;
- quantum or physical dynamics;
- any equivalence between category theory and Buddhist doctrine.

Those may be added as explicit specializations.  The present theorem is narrower:
composable contextual refinement supports exact transitivity of state descent and
independent transitivity of invariant semantic descent.
