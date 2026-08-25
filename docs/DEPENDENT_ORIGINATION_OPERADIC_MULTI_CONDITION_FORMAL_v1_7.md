# Dependent Origination Operadic Multi-Condition Axis — Formal v1.7

## Purpose

The original dependent-origination parent is unary: a context morphism transports one conditioned state into another. That is appropriate for composable contextual change, but it does not by itself express the distinct situation in which several conditioned inputs jointly participate in one resulting state.

v1.7 adds this second axis explicitly.

```text
unary relation:
X -> Y

multi-condition operation:
(X₁, X₂, ..., Xₙ) -> Y
```

The old unary transport remains authoritative. Multi-input operations are extra structure, not an interpretation silently extracted from ordinary category composition.

## Positive-arity colored signature

`MultiConditionSignature` assigns a type of primitive operations to a list-like finite family of input colors and one output color. The Lean encoding uses `Fin (n + 1)`, so every primitive has at least one input.

This is deliberate: a nullary constant is not treated as primitive dependent origination in this layer.

## Algebra

`MultiConditionAlgebra` interprets each primitive operation as an actual many-input map on a family of carriers:

```text
op : (X₁, ..., Xₙ) -> Y
states xᵢ : Carrier Xᵢ
-------------------------
act op x : Carrier Y
```

## Free operadic tree syntax

`MultiConditionExpr` has two constructors:

```text
atom
compose
```

A `compose` node takes one primitive multi-condition operation together with one child expression for each input. Child outputs must match parent input colors by construction.

Therefore nesting `compose` nodes is typed tree grafting. This is the free planar operadic syntax used by the current KuuOS layer.

It is not yet a symmetric-operad quotient: no permutation action or permutation coherence is claimed here.

## Embedding ordinary contextual transport

`OperadicDependentOriginationExtension D` contains:

- a multi-condition signature;
- an algebra on the existing context-indexed state carriers;
- an explicit unary operation for every old context morphism;
- a proof that this unary operation acts exactly as `D.transport`.

Thus:

```text
ordinary contextual transport
=
arity-one sector of the operadic extension
```

not a competing semantics.

The theorem `eval_unaryExpr` proves the exact equality after evaluation.

## Genuine multi-condition structure

`HasGenuineMultiCondition` records existence of a primitive with actual arity at least two. This property is separate from the mandatory unary embedding.

Hence an operadic extension may conservatively reproduce only unary transport, or may add genuinely joint conditioning when the domain supplies it.

## Shared semantic preservation

`SharedSemanticReadout` expresses a natural compatibility law for invariant meaning:

```text
all inputs read as value s
+
primitive operation is semantic-compatible
-------------------------------------------
output reads as value s
```

`AllAtomsAt` lifts the condition to every atomic leaf of a recursively nested tree.

The theorem

```text
eval_preserves_shared_semantics
```

proves that arbitrarily nested operadic grafting preserves the shared invariant semantic value.

This gives a multi-condition analogue of the earlier local/global semantic descent principle:

```text
many conditioned carriers
may jointly compose
without requiring one underlying substance carrier,
while one invariant meaning may remain stable.
```

## Relation to bicategorical v1.6

The two axes answer different questions.

```text
bicategorical axis:
How are different dependent paths related coherently?

operadic axis:
How do several dependent conditions jointly produce one output?
```

They are intentionally kept separate. A later layer may combine them into a higher-operadic, monoidal, or process-theoretic structure only after the required coherence is explicit.

## Boundaries

v1.7 does not yet claim:

- symmetric group actions on inputs;
- a symmetric colored operad quotient;
- higher operads;
- a monoidal process theory;
- sheaf or stack structure;
- enriched-category structure;
- infinity-category structure;
- causal/no-signalling completeness;
- quantum or physical theorem authority in the parent dependent-origination core.

The parent interpretation remains a mathematical structural model of composable and jointly conditioned establishment, not an assertion that a specific categorical formalism is identical to Buddhist doctrine.
