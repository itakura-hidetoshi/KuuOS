# Dependent Origination — Global Duskin / Local Mapping Comparison v1.23

## Scope

v1.23 begins the comparison between the two higher-categorical presentations already present in KuuOS:

- the **local 2-Yoneda presentation** with mapping quasicategories `N(B(X,Y))`;
- the **global Duskin presentation** with one scaled simplicial set `N_Duskin(B)`.

The goal here is deliberately the exact one-skeleton boundary.  We do **not** identify a full global mapping simplicial set with `N(B(X,Y))` yet.

## Native local side

For every pair of objects `X,Y`, Mathlib's nerve identifies

```text
mappingNerve(X,Y)_0 ≃ (X ⟶ Y).
```

KuuOS exposes this as `mappingNerveVertexEquiv`.

Thus a local mapping vertex is not merely analogous to a bicategorical 1-morphism: it is natively equivalent to one.

## Global side

A global Duskin 1-simplex is a normal lax functor

```text
[1] -> B.
```

v1.23 extracts:

- its source object;
- its target object;
- its principal arrow `0 -> 1`.

For specified objects `X,Y`, `GlobalDuskinEdgeOver B X Y` bundles a global 1-simplex together with endpoint identifications.  From it KuuOS constructs

```text
GlobalDuskinEdgeOver B X Y
  -> (X ⟶ Y)
  -> mappingNerve(X,Y)_0.
```

The final arrow is theorem-level and uses the native Mathlib nerve equivalence.

## Exact reverse boundary

The reverse direction is not silently inferred.  `GlobalDuskinEdgeRepresentability B X Y` explicitly asks for an inverse from local mapping vertices to fixed-endpoint global edges, with both inverse laws.

Once this data is supplied,

```text
GlobalDuskinEdgeOver B X Y ≃ mappingNerve(X,Y)_0.
```

A family of such witnesses for all `X,Y` is bundled as `GlobalDuskinLocalOneSkeletonComparison B`.

This separation matters: a normal-lax walking-arrow classification theorem should prove this representability, rather than having it hidden in the definition of dependent origination.

## Equivalence edges and completeness

A fixed-endpoint global edge is declared an equivalence edge only when its extracted 1-morphism is the forward arrow of a native Mathlib bicategorical adjoint equivalence

```text
q : X ≌ Y.
```

Under edge representability, every such `q` obtains a global representative.  Conversely, an `ObjectUnivalence B` witness sends the adjoint-equivalence witness of a global equivalence edge to an object path

```text
X = Y.
```

The resulting theorem verifies that applying the univalence equivalence back to this path recovers an adjoint equivalence whose forward morphism is exactly the arrow carried by the original global edge.

Hence v1.20 and v1.21/v1.22 are now connected at the object/equivalence-edge one-skeleton without collapsing equivalence into definitional equality.

## Proved boundary

```text
mappingNerve(X,Y)_0 ≃ (X ⟶ Y)

fixed-endpoint global Duskin edge
  -> (X ⟶ Y)
  -> mappingNerve(X,Y)_0

GlobalDuskinEdgeRepresentability(X,Y)
  -> global edge ≃ local mapping vertex

ObjectUnivalence B
  + global adjoint-equivalence edge
  -> object path
```

## Still open

The following remain intentionally unproved:

1. construction of the **full simplicial global mapping object** extracted from the global Duskin nerve;
2. equivalence of that mapping object with `mappingNerve X Y` in every degree;
3. compatibility with bicategorical horizontal composition;
4. compatibility with the global scaling and the v1.22 scaled-horn family;
5. a conditional equivalence between the full local complete-Segal and global scaled-Duskin presentations.

The next mathematically natural step is therefore to formalize a global mapping-object interface whose 0-simplices recover `GlobalDuskinEdgeOver`, then state and prove the strongest comparison available without assuming full scaled-anodyne fibrancy.
