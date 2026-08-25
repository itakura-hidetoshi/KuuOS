# Dependent Origination — Enriched Context v1.13

## Purpose

v1.13 adds an **enrichment axis** to the restored non-quantum dependent-origination parent.

The parent still has ordinary contextual transport

```text
f : X -> Y
```

with functorial state action.  The enriched layer additionally equips the context type with Mathlib's native `V`-enriched category structure, so the relation space itself is a `V`-object

```text
X ⟶[V] Y.
```

This answers a question ordinary category structure cannot express: not merely whether a contextual relation exists, but what additional structure the relation space carries.

## Native Mathlib carrier

The implementation uses

```lean
Mathlib.CategoryTheory.Enriched.Basic
CategoryTheory.EnrichedCategory
```

directly.  It does not introduce a KuuOS-specific substitute for enriched categories.

For a monoidal category `V`, Mathlib supplies:

```text
Hom  : X,Y |-> X ⟶[V] Y
id   : I_V -> X ⟶[V] X
comp : (X ⟶[V] Y) ⊗ (Y ⟶[V] Z) -> X ⟶[V] Z
```

with enriched identity and associativity laws.

## KuuOS bridge

`EnrichedDependentOriginationSystem` contains the old parent `FunctorialTransportSystem` together with

```text
liftHom : (X -> Y) -> (I_V -> X ⟶[V] Y).
```

It requires ordinary identity and ordinary composition to be represented by native enriched identity and composition.

Thus the old transport path remains authoritative for state evolution while the enriched hom object records relation texture.

## Interpretation

Different choices of `V` can encode different kinds of structure on relations, for example:

- order/intensity;
- metric or cost;
- additive/linear structure;
- probability-like or resource-like structure;
- other monoidal relation semantics.

The parent does not choose one of these universally.

## Ordinary category as a specialization

Mathlib proves that `Type`-enriched categories recover ordinary categories.  v1.13 exposes the canonical `Type` enrichment as `ordinaryTypeEnrichment`.

Therefore the enrichment axis is additive rather than a replacement:

```text
ordinary contextual category
  -> canonical Type-enrichment

or

ordinary contextual category
  + richer V-enrichment.
```

## Boundary

v1.13 does not claim that enrichment implies:

- effective descent;
- stack structure;
- causal order;
- no-signalling;
- bicategorical or infinity-categorical higher coherence;
- quantum or physical Yang--Mills authority.

Those are distinct structural axes.
