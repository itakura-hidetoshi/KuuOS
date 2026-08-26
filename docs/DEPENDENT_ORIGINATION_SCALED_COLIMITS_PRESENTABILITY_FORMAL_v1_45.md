# Dependent Origination — Scaled Colimits and Presentability Formal v1.45

## Scope

This layer closes the internal categorical/presentability frontier left by v1.44 for the canonical KuuOS scaled horn-cylinder generator class

\[
T=\text{all canonical minimally-scaled horn-cylinder attachment inclusions}.
\]

The goal is to derive Mathlib's `MorphismProperty.HasSmallObjectArgument T` without retaining a separate KuuOS factorization or presentability certificate.

## Colimits in `ScaledSSet`

For a diagram \(D:J\to\mathbf{ScaledSSet}\), take the ordinary simplicial-set colimit

\[
L=\operatorname*{colim}_j U(D_j)
\]

and put on `L` the least scaling containing both degenerate 2-simplex families and every image of a thin 2-simplex from a diagram object:

\[
t\text{ thin}\iff t=\sigma_0x\;\lor\;t=\sigma_1x\;\lor\;\exists j,x,\;x\text{ thin in }D_j\land\iota_j(x)=t.
\]

Every colimit leg is scaled by construction. For any scaled cocone, the ordinary simplicial-set colimit map is scaled: degeneracies map to degeneracies and each generated thin simplex maps through a scaled cocone leg. Thus the explicit cocone is a colimit in `ScaledSSet`.

Consequently `ScaledSSet` has all small colimits and the forgetful functor

\[
U:\mathbf{ScaledSSet}\to\mathbf{SSet}
\]

preserves them.

## Minimal scaling and Hom

If `A_min` is `A` with minimal scaling, every simplicial map out of it is automatically scaled. Hence

\[
\boxed{\operatorname{Hom}_{\mathbf{ScaledSSet}}(A_{\min},X)\simeq\operatorname{Hom}_{\mathbf{SSet}}(A,U X).}
\]

v1.45 packages this naturally in `X` as a coyoneda natural isomorphism. Since `U` preserves filtered colimits, finite presentability of `A` transfers to `A_min`.

## Canonical generator sources

Each generator source is

\[
A_{n,i,\varepsilon}=(\Delta[n]\times\{\varepsilon\})\cup(\Lambda_i^n\times\Delta[1])\subset\Delta[n]\times\Delta[1]
\]

with minimal scaling. The ambient product is finite; Mathlib proves that subcomplexes of finite simplicial sets are finite and finite simplicial sets are finitely presentable. Therefore every canonical generator source is finitely presentable in `ScaledSSet`.

## Small-object argument at `aleph0`

The generator class is already small from its `MorphismProperty.ofHoms` presentation. The explicit colimits supply local smallness, pushouts, coproducts, and transfinite iteration colimits. Finite presentability of generator sources supplies the required source-Hom preservation on relative cell-complex colimits.

Hence

\[
\boxed{\operatorname{IsCardinalForSmallObjectArgument}(T,\aleph_0)}
\]

and

\[
\boxed{\operatorname{HasSmallObjectArgument}(T)}
\]

hold. Pinned Mathlib then supplies the functorial factorization and native weak factorization system

\[
\boxed{(T^{\perp\perp},T^\perp)}
\]

with cellular description

\[
\boxed{T^{\perp\perp}=\operatorname{Retr}\operatorname{TransfiniteComp}\operatorname{Pushout}\operatorname{Coproduct}(T).}
\]

## Mathematical boundary

This closes the internal canonical KuuOS small-object/WFS frontier. It does not identify this canonical generated class with an external or future Lurie scaled-anodyne implementation. That comparison remains a separate morphism-property theorem, e.g.

\[
T\le\mathcal A_{\mathrm{std}}\le T^{\perp\perp}
\]

or the stronger equality \(\mathcal A_{\mathrm{std}}=T^{\perp\perp}\). No ordinary/unscaled anodyne result is silently promoted to that external scaled comparison.
