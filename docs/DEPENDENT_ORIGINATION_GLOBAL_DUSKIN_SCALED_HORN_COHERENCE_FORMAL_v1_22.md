# Dependent Origination — Global Duskin Scaled-Horn Coherence v1.22

## Status

This note documents the v1.22 formal boundary extending the v1.21 global scaled Duskin nerve.

The parent definition of dependent origination remains contextual composable transport.  The global scaled Duskin nerve is a higher-coherence specialization and global simplicial realization of a bicategorical layer; it is not the parent definition itself.

## What v1.22 adds

v1.21 already constructs

\[
B\longmapsto N_{\mathrm{Duskin}}(B)
\]

with

\[
N_{\mathrm{Duskin}}(B)_n
=
\operatorname{NormalLax}([n],B)
\]

and a global scaling in which a 2-simplex is thin when its normal-lax comparison 2-cell is invertible, together with all degenerate 2-simplices.

v1.22 now separates two logically different layers.

### 1. Coherence forced by every normal-lax simplex

For each Duskin 3-simplex \(\sigma:[3]\to B\), the normal-lax associativity law gives the tetrahedral equation

\[
(\sigma_{01,12}\triangleright \sigma_{23})
\circ \sigma_{02,23}
\circ \sigma(\alpha_{01,12,23})
=
\alpha_{\sigma_{01},\sigma_{12},\sigma_{23}}
\circ
(\sigma_{01}\triangleleft \sigma_{12,23})
\circ
\sigma_{01,13}.
\]

This is the 3-dimensional coherence relating the four triangular faces of the Duskin tetrahedron.

For every Duskin 1-simplex, the normality laws also expose explicit left- and right-unit coherence equations.  Hence the global simplicial carrier does not merely store triangles: its 3-simplices already encode bicategorical associativity coherence.

The resulting theorem-level certificate is

`GlobalDuskinLowDimensionalCoherence B`.

Every Mathlib bicategory has this certificate automatically.

### 2. Scaled-horn fibrancy as genuinely additional structure

A bicategory by itself does **not** automatically justify the statement that its global scaled Duskin nerve satisfies whichever scaled-anodyne presentation one intends to use for an \((\infty,2)\)-model.

v1.22 therefore introduces an explicit interface:

- `IsScaledMap`
- `ScaledHornExtensionProblem`
- `ScaledHornFiller`
- `ScaledHornFamily`
- `HasScaledHornFillers`

A `ScaledHornExtensionProblem` contains

1. a horn scaling,
2. a simplex scaling,
3. proof that the horn inclusion is scaled,
4. a horn map into the target,
5. proof that the horn map is scaled.

A `ScaledHornFamily` then specifies which such horn problems are admissible generators.  This is where a standard scaled-anodyne generating family can be installed later without changing the parent definition or silently strengthening arbitrary bicategories.

## Conditional completeness bridge

The file defines

`GlobalCompleteDuskinCertificate B F`

for an explicit admissible horn family `F`.  It records

- scaled horn fillers for `F`, and
- `ObjectUnivalence B`.

From the second field, v1.22 proves the one-way implication

\[
\text{GlobalCompleteDuskinCertificate}(B,F)
\Longrightarrow
\text{CompleteSegalInfinityTwoCategory}(B).
\]

This bridge deliberately uses the already formalized v1.20 object-univalence / Rezk-completeness analogue.

It does **not** claim that the local 2-Yoneda presentation and global scaled Duskin presentation are already equivalent.

## Exact boundary after v1.22

Proved:

\[
\text{bicategory}
\to
\text{global scaled Duskin nerve}
\to
\text{thin invertible composition triangles}
\to
\text{associativity tetrahedra + unit coherence}.
\]

Formalized as explicit additional certificates, but not assumed automatically:

\[
\text{chosen scaled-horn generators}
+
\text{scaled horn fillers}
+
\text{object univalence}.
\]

Still not claimed:

1. a specific standard scaled-anodyne generator family has been identified with the repository-native `ScaledHornFamily` interface;
2. the global Duskin mapping objects have been constructed and identified with `N(B(X,Y))`;
3. the v1.20 local complete-Segal presentation and the v1.21/v1.22 global scaled Duskin presentation are equivalent without those comparison data.

## Next frontier

The next mathematically natural unit is

\[
\boxed{
\text{standard scaled-anodyne generators}
\to
\text{global mapping-object extraction}
\to
N(B(X,Y))\text{ comparison}
\to
\text{conditional local/global model equivalence}
}
\]

with every extra fibrancy, completeness, and comparison hypothesis kept explicit.
