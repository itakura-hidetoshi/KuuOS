# Dependent Origination Contextual Descent — Formal v1.1

## Purpose

v1.0 restored the parent notion of dependent origination to a contextual
state-valued functor with composable transport.  v1.1 develops the next
non-quantum layer: how several refined contexts can be locally compatible and
what, if anything, may be said globally.

The central distinction is

```text
local compatibility
!=
existence of one global state
```

while an invariant semantic readout can still descend uniquely.

## 1. Refinement direction

The parent transport is covariant, so contextual refinement is oriented as

```text
root -> chart -> common refinement.
```

`RefinementCover Context Index` contains

```text
rootContext
chart i
toChart i : rootContext -> chart i.
```

No topology, groupoid, invertibility, or site structure is built into this
definition.

## 2. Pairwise overlap system

`OverlapSystem C` supplies, for every pair `i j`, a common refinement

```text
meet i j
```

and arrows

```text
chart i -> meet i j
chart j -> meet i j.
```

The only contextual coherence law is equality of the two root paths:

```text
root -> chart i -> meet i j
=
root -> chart j -> meet i j.
```

This is not a claim that `meet i j` is a categorical pullback.  It is an
explicit common-refinement witness adequate for the parent transport law.

## 3. Local state families

A `LocalStateFamily D C` chooses

```text
state i : D(chart i)
```

for every chart.

It is `OverlapCompatible` when the two selected local states become equal after
transport to every common refinement:

```text
D(leftToMeet i j) (state i)
=
D(rightToMeet i j) (state j).
```

## 4. Global states automatically satisfy local compatibility

A root state

```text
x : D(rootContext)
```

induces the local family

```text
state i = D(toChart i) x.
```

By functorial composition and equality of the two root-to-meet paths, v1.1
proves

```text
ofGlobal_overlapCompatible.
```

Thus overlap compatibility is a necessary condition for ordinary root-state
gluing.

## 5. State descent is additional structure

`StateDescends D C s` means

```text
exists x : D(rootContext),
  forall i, D(toChart i) x = s.state i.
```

The framework does **not** assert that every compatible local family descends.
That stronger property is separately named

```text
HasStateDescent D C O.
```

Likewise, uniqueness is not automatic.  `CoverSeparatesGlobalStates D C` means
that two root states with identical images on every chart are equal.

The theorem

```text
existsUnique_globalState_of_descent_and_separation
```

states precisely:

```text
state descent + local separation
=> unique root-state gluing.
```

## 6. System maps preserve local structure

For a v1.0 transport-compatible system map

```text
eta : SystemHom D E,
```

local families map pointwise by `eta`.

v1.1 proves that such maps preserve

- overlap compatibility;
- existence of a root-state descent witness.

So local/descent structure is natural with respect to maps between
contextual dependent-origination systems.

## 7. Invariant semantic descent

The v0.1 parent already contains `InvariantReadout`:

```text
readout : D(X) -> Semantic
```

with value unchanged by every admissible contextual transport.

Suppose local states are overlap-compatible.  Transporting the state on chart
`i` and the state on chart `j` to `meet i j` yields the same state.  Invariance
of the readout on both paths therefore proves

```text
readout(chart i, state i)
=
readout(chart j, state j).
```

This is formalized as

```text
local_semantic_eq_of_overlapCompatible.
```

## 8. Global meaning without requiring global state descent

For a nonempty chart index, pairwise equality of local semantic values gives one
unique semantic value.  Therefore v1.1 proves

```text
semanticDescends_of_overlapCompatible :
  OverlapCompatible ... s -> SemanticDescends R C s.
```

Crucially, no `StateDescends` hypothesis appears.

The explicit boundary theorem

```text
semanticDescent_without_stateDescent
```

says that even if one assumes

```text
not (StateDescends D C s),
```

overlap compatibility still gives unique invariant semantic descent.

The claim is logical and structural:

```text
no global root-state witness
+ compatible local conditioned states
+ transport-invariant readout
=> unique global semantic value.
```

It does not manufacture an example of failed state descent, nor does it claim
that every semantic codomain is physically meaningful.

## 9. Relation to earlier groupoid Cech descent

The older

```text
GaugeInvariantDependentOriginationGroupoidCechDescentV0_1
```

is a reversible action-groupoid specialization.  Its chart transition arrows
and gauge cocycle remain valid downstream structures.

v1.1 does not import that groupoid as the parent definition.  Instead:

```text
general contextual refinement/descent
  +-- reversible gauge/Cech specialization
  +-- irreversible directed refinement
  +-- history/memory specialization
  +-- later quantum realization.
```

## 10. What is not claimed

v1.1 is deliberately weaker than a full sheaf theorem.

It does not assume or prove:

- a Grothendieck topology;
- categorical pullbacks for every chart pair;
- triple-overlap or higher simplicial descent data;
- effective descent for every compatible family;
- equivalence with a stack or infinity-sheaf;
- any quantum, Hamiltonian, or Yang--Mills theorem.

Those may be added as later specializations if needed.

## 11. Structural reading

The non-quantum spine is now

```text
context
-> conditioned state fiber
-> admissible relation / transport
-> refinement
-> common refinement / overlap
-> compatibility
-> optional state gluing
-> invariant semantic gluing.
```

The intended mathematical interpretation of the final step is:

```text
one does not need to postulate one context-free substance in order for
compatible conditioned presentations to support one invariant meaning.
```

This remains a mathematical structural interpretation of dependent origination,
not an assertion that category theory is identical with Buddhist doctrine.
