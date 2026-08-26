# Dependent Origination — Scaled Small-Object Argument Formal v1.44

## Scope

This layer connects the canonical KuuOS scaled horn-cylinder attachment
generators to the native Mathlib small-object argument.

The canonical generator property is

\[
T=\text{all minimally-scaled horn-cylinder attachment inclusions}.
\]

Earlier layers established

\[
\mathcal A_{\mathrm{can}}=T^{\perp\perp},
\qquad
\mathcal F_{\mathrm{can}}=T^\perp,
\]

and proved all orthogonality and closure laws.  The only remaining datum in
v1.43 was factorization through these classes.

## Mathlib small-object theorem

Pinned Mathlib defines

`MorphismProperty.HasSmallObjectArgument I`.

Under this typeclass it supplies a functorial factorization

\[
I^{\perp\perp}\; ;\; I^\perp
\]

and identifies the left class with

\[
\operatorname{Retr}
\operatorname{TransfiniteComp}
\operatorname{Pushout}
\operatorname{Coproduct}(I).
\]

For the canonical KuuOS generators this gives exactly the v1.43 missing
factorization.

## Generator smallness

The generator property is defined by `MorphismProperty.ofHoms` from the
explicit type `ScaledHornAttachmentGeneratorIndex`.

Therefore its Mathlib `MorphismProperty.IsSmall` instance is obtained directly
from `isSmall_ofHoms`; generator-smallness is no longer part of the frontier.

## Exact remaining cardinal data

For a regular cardinal `κ`, v1.44 packages precisely the remaining fields of
Mathlib `IsCardinalForSmallObjectArgument` as

`CanonicalScaledSmallObjectCardinalData κ`:

1. `LocallySmall ScaledSSet`;
2. `HasPushouts ScaledSSet`;
3. `HasCoproducts ScaledSSet` in the chosen universe;
4. `HasIterationOfShape κ.ord.ToType ScaledSSet`;
5. preservation of the relevant relative-cell-complex colimits by
   `Hom(A,-)` for generator sources `A`.

From these data, v1.44 constructs

`IsCardinalForSmallObjectArgument T κ`

and then

`HasSmallObjectArgument T`.

## Consequences

The resulting theorem chain is

\[
\boxed{
\begin{aligned}
&\text{CanonicalScaledSmallObjectCardinalData}(\kappa)\\
&\Longrightarrow \text{HasSmallObjectArgument}(T)\\
&\Longrightarrow \text{HasFactorization}(T^{\perp\perp},T^\perp)\\
&\Longrightarrow \text{IsWeakFactorizationSystem}(T^{\perp\perp},T^\perp).
\end{aligned}}
\]

The left class also receives the explicit cellular description

\[
\boxed{
T^{\perp\perp}
=
\operatorname{Retr}
\operatorname{TransfiniteComp}
\operatorname{Pushout}
\operatorname{Coproduct}(T).
}
\]

## Mathematical boundary

This file does **not** claim that the required colimits or presentability
properties of `ScaledSSet` are already available.

The new frontier is exact and constructive:

\[
\boxed{
\text{build the needed colimits in ScaledSSet and prove generator-source
presentability / Hom-colimit preservation.}
}
\]

The ordinary simplicial-set implementation in pinned Mathlib provides the
blueprint: its horn generators use `aleph0`, finite presentability of the horn
sources, and the existing simplicial-set colimit infrastructure.  The scaled
case must establish the corresponding facts for the explicit KuuOS
`ScaledSSet` category rather than silently importing the unscaled theorem.
