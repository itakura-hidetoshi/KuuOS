# Dependent Origination — Biequivalence-Level Presentation Invariant v1.26

## Status

This layer extends the v1.25 presentation-independent invariant kernel from two
presentations of one bicategory to different bicategorical models connected by
Whitehead-style biequivalence data.

The parent dependent-origination definition is unchanged:

\[
D:\mathcal C\to \mathbf{Type}
\]

with composable transport.  The higher-categorical structures remain
specializations and completion layers rather than replacements for that parent
definition.

## 1. Why v1.25 was not yet fully presentation independent

Version 1.25 established the intrinsic carrier

\[
\mathcal I_B(X,Y)=\mathcal B(X,Y)
\]

and proved that the local mapping nerve and global scaled Duskin presentation
of the **same** bicategory recover the same one- and two-cell data.

That removes dependence on the choice

\[
N(\mathcal B(X,Y))
\quad\text{versus}\quad
N_{\mathrm{Duskin}}(\mathcal B).
\]

But a stronger question remains:

> What if the same higher structure is represented by a different,
> biequivalent bicategory?

The invariant should not depend on that choice either.

## 2. Whitehead-style model-equivalence data

The formal carrier is

```lean
BicategoricalModelEquivalence B C
```

with the following data.

### 2.1 Native pseudofunctor

\[
F:\mathcal B\to\mathcal C
\]

is a native Mathlib pseudofunctor.

### 2.2 Local equivalence on every hom-category

For every pair \(X,Y\in\mathcal B\),

\[
\mathcal B(X,Y)
\simeq
\mathcal C(FX,FY).
\]

Crucially, the forward functor of this equivalence is required to be exactly
the native hom-functor induced by \(F\):

\[
F_{X,Y}(f)=F(f),
\qquad
F_{X,Y}(\alpha)=F_2(\alpha).
\]

Thus the categorical equivalence is a certificate for the actual
pseudofunctorial action, not an unrelated equivalence witness.

### 2.3 Essential surjectivity on objects

Every \(Z\in\mathcal C\) is adjoint-equivalent to an image object:

\[
\forall Z\in\mathcal C,
\quad
\exists X\in\mathcal B,
\quad
FX\simeq Z.
\]

This is the expected Whitehead-style object condition for biequivalence.

## 3. The mapping invariant is now model independent

For every \(X,Y\in\mathcal B\), v1.26 provides

\[
\boxed{
\mathcal I_B(X,Y)
\simeq
\mathcal I_C(FX,FY)
}
\]

with

\[
\mathcal I_B(X,Y)=\mathcal B(X,Y),
\qquad
\mathcal I_C(FX,FY)=\mathcal C(FX,FY).
\]

The equivalence acts exactly by the pseudofunctor:

\[
f\mapsto F(f),
\qquad
\alpha\mapsto F_2(\alpha).
\]

Therefore the intrinsic mapping carrier is no longer tied to one concrete
bicategory model.

## 4. Local mapping vertices transport canonically

A source local vertex

\[
x\in N(\mathcal B(X,Y))_0
\]

is first decoded to its intrinsic one-cell

\[
f=\operatorname{inv}_1(x),
\]

then transported by \(F\), then re-encoded as a target local vertex:

\[
x
\longmapsto
f
\longmapsto
F(f)
\longmapsto
x'.
\]

The formal commuting theorem is

\[
\boxed{
\operatorname{inv}_1(x')
=
F(\operatorname{inv}_1(x)).
}
\]

This is exact equality, not merely existence of a comparison.

## 5. Local mapping edges transport canonically

For a local mapping edge \(e\), decode the intrinsic two-cell

\[
\alpha=\operatorname{inv}_2(e),
\]

transport it by the pseudofunctor,

\[
\alpha\mapsto F_2(\alpha),
\]

and use the native nerve edge constructor in the target hom-category.

The formal theorem is

\[
\boxed{
\operatorname{inv}_2(F_*e)
=
F_2(\operatorname{inv}_2(e)).
}
\]

Thus the one- and two-cell transport squares commute exactly.

## 6. Universal observable independence under model replacement

Let

\[
\Phi:\mathcal C(FX,FY)\to Z
\]

be any one-cell observable.  Evaluating via the categorical-equivalence
presentation or via direct pseudofunctorial transport gives the same result:

\[
\boxed{
\Phi(F_{X,Y}(f))
=
\Phi(F(f)).
}
\]

Likewise, for every two-cell observable,

\[
\boxed{
\Phi(F_{X,Y}(\alpha))
=
\Phi(F_2(\alpha)).
}
\]

The proposition-valued forms are proved as well.

This makes the invariant principle explicit:

\[
\boxed{
\text{presentation}
\to
\text{intrinsic carrier}
\to
\text{model transport}
\to
\text{observable}
}
\]

and the observable cannot distinguish the two encodings of the same transported
intrinsic datum.

## 7. Source global Duskin data can already cross models

A direct map

\[
N_{\mathrm{Duskin}}(\mathcal B)
\to
N_{\mathrm{Duskin}}(\mathcal C)
\]

is not required to transport the invariant.

For a source global Duskin edge, v1.26 uses

\[
\text{source global edge}
\to
\text{source local vertex}
\to
\text{source intrinsic one-cell}
\to
\text{target intrinsic one-cell}
\to
\text{target local vertex}.
\]

The result satisfies

\[
\boxed{
\operatorname{inv}_1(\text{target local vertex})
=
F(\operatorname{inv}_1(\text{source global edge})).
}
\]

Similarly, for a source global Duskin triangle comparison cell,

\[
\boxed{
\operatorname{inv}_2(\text{target local edge})
=
F_2(\operatorname{comparison}(\sigma)).
}
\]

Hence source global presentation data already transport across bicategorical
models through the intrinsic carrier.

## 8. Why direct global-to-global transport is deferred

The present global Duskin nerve uses strictly unitary normal-lax simplices.
A general pseudofunctor need not be strictly unitary.

Therefore composing a current Duskin simplex directly with an arbitrary
pseudofunctor does not automatically land in the exact same strictly-unitary
simplex type.

This is a presentation-normalization issue.

It does **not** obstruct the invariant, because the invariant is already defined
before choosing that normalized global presentation.

The remaining problem is to construct a coherent strictly-unitary
normalization and prove that its global transport recovers the same intrinsic
one- and two-cell maps established here.

## 9. Bundled theorem-level package

The structure

```lean
PresentationIndependentInvariantUnderModelEquivalence E
```

packages four consequences:

1. source and target intrinsic mapping carriers are categorically equivalent;
2. transported local vertices commute with intrinsic one-cell transport;
3. transported local edges commute with intrinsic two-cell transport;
4. every target object is covered up to intrinsic object equivalence.

Every `BicategoricalModelEquivalence` canonically supplies this package.

## 10. Mathematical boundary

### Proved in v1.26

\[
\boxed{
\begin{array}{c}
\text{different bicategorical models}\\
\text{related by local equivalences + object essential surjectivity}
\end{array}
\Longrightarrow
\text{same transported intrinsic 1/2-cell invariants}
}
\]

and source global Duskin data can be transported into the target local mapping
presentation through those invariants.

### Still open

The following are intentionally not claimed yet:

- a canonical direct global-Duskin-to-global-Duskin map for arbitrary
  pseudofunctors;
- strictly-unitary normalization of that transport;
- all-degree mapping simplicial equivalence across models;
- compatibility of normalized global transport with the scaled-horn family;
- a complete equivalence theorem for the full local/global `(∞,2)` models.

## 11. Conceptual consequence for dependent origination

The higher presentation is now increasingly secondary.

At the present formal frontier:

\[
\boxed{
\text{dependent-origination higher invariant}
=
\text{intrinsic bicategorical relation data up to model equivalence}
}
\]

rather than

\[
\text{a specific nerve, triangulation, stack presentation, or coordinate model}.
\]

The next normalization theorem should therefore be understood as a theorem
about **representing** the invariant globally, not as a redefinition of the
invariant itself.
