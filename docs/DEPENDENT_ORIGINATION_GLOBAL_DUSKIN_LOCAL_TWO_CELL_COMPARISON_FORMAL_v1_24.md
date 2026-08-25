# Dependent Origination — Global Duskin / Local Two-Cell Comparison v1.24

## Position in the spine

v1.23 established the first local/global comparison layer at the one-skeleton:
for fixed objects `X,Y`, global Duskin edges extract bicategorical 1-morphisms
and therefore vertices of the local mapping nerve `N(B(X,Y))`.

v1.24 advances one dimension:

```text
global Duskin 2-simplex
  -> normal-lax comparison 2-cell
  -> local mapping-nerve 1-simplex
  -> exact recovery of the 2-cell
  -> thinness/invertibility comparison.
```

This is still a specialization layer of the parent contextual-composable
transport definition; it does not redefine dependent origination itself.

## Local mapping edges are bicategorical 2-morphisms

For parallel 1-morphisms

```text
f,g : X -> Y
```

the local mapping nerve has vertices represented by `f` and `g`.  The type
`MappingNerveEdge X Y f g` is the edge space between those two vertices.

A bicategorical 2-morphism

```text
alpha : f ==> g
```

is sent by Mathlib's native `CategoryTheory.nerve.edgeMk` to such an edge.
Mathlib's native `CategoryTheory.nerve.homEquiv` recovers exactly `alpha`.
Moreover, `edgeMk_surjective` shows that every fixed-endpoint local mapping
edge comes from a bicategorical 2-morphism.

Thus the local mapping nerve has the expected dimensional interpretation:

```text
mappingNerve(X,Y)_0 = 1-morphisms X -> Y
mappingNerve(X,Y)_1 = 2-morphisms between them.
```

## Global Duskin triangles

For a global Duskin 2-simplex `sigma`, define its three vertices and the two
parallel arrows from its initial to terminal vertex:

```text
composite = sigma(0->1) >> sigma(1->2)
long      = sigma(0->2).
```

The normal-lax structure supplies the canonical comparison cell

```text
sigma.mapComp : composite ==> long.
```

v1.24 sends this cell to a local mapping-nerve edge

```text
duskinComparisonMappingEdge sigma.
```

The theorem `duskinComparisonMappingEdge_hom` proves that applying native
`nerve.homEquiv` recovers the original normal-lax comparison cell exactly.

So this is not a heuristic association between two presentations.  At the
2-cell level the comparison is a typed theorem.

## Scaling compatibility in dimension two

The v1.21 global scaling declares a Duskin 2-simplex thin when either:

1. its comparison cell is invertible; or
2. it is simplicially degenerate.

v1.24 proves that invertibility of the local mapping 2-morphism is equivalent
to invertibility of the original Duskin comparison cell.

Therefore every local-invertible comparison edge gives a globally thin Duskin
triangle.  For a nondegenerate Duskin triangle the result is exact:

```text
global thinness
  <-> invertibility of the corresponding local mapping 2-morphism.
```

This is the first direct compatibility theorem between the global scaling and
the local mapping-category structure.

## What is automatic now

For every bicategory `B`:

```text
Duskin 2-simplex
  -> local mapping edge
```

is canonical, and the local edge remembers exactly the global comparison
2-cell.  The structure

```text
GlobalDuskinLocalTwoCellForwardComparison B
```

packages this theorem-level forward bridge together with nondegenerate
thinness detection.

No additional fibrancy, completeness, or univalence assumption is needed for
this forward direction.

## What remains explicit

v1.24 does **not** claim that an arbitrary local mapping edge already has a
canonical globally fixed-endpoint Duskin-triangle representative with all
required object/edge identifications.

It also does not yet construct a single global mapping simplicial object in all
degrees.  The remaining frontier is therefore:

```text
one-skeleton representability                  -- v1.23 conditional
+ automatic comparison-cell bridge             -- v1.24 proved
-> fixed-endpoint triangle representability
-> higher-dimensional global mapping object
-> simplicial comparison with N(B(X,Y))
-> composition/scaling/horn compatibility
-> conditional local/global model equivalence.
```

In particular, the target statement

```text
Map_{N_Duskin(B)}(X,Y) ~= N(B(X,Y))
```

is still not asserted until the left-hand mapping simplicial object and its
comparison maps have been constructed explicitly.

## Conceptual interpretation

The local and global `(infinity,2)` presentations are now connected through
two adjacent dimensions:

```text
global 1-simplex -> local mapping vertex

global 2-simplex comparison cell -> local mapping edge.
```

This sharpens the meaning of the global Duskin nerve inside KuuOS:

```text
global scaled Duskin nerve
=
global simplicial realization of bicategorical contextual transport,
whose low-dimensional cells recover the same 1- and 2-morphism data used by
the local 2-Yoneda mapping nerves.
```

The equality of the full models remains a later conditional theorem rather
than an assumption.
