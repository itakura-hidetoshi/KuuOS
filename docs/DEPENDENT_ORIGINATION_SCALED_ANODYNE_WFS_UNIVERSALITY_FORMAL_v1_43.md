# Dependent Origination — Scaled-Anodyne WFS Universality v1.43

This layer strengthens the v1.42 generator-closure result without identifying
KuuOS's canonical scaled-anodyne class with an external model structure.

Let

\[
T=\{\text{canonical minimally-scaled horn-cylinder attachment inclusions}\}.
\]

The v1.42 canonical left class is

\[
\mathcal A_{\mathrm{can}}=T^{\perp\perp}=T.\mathrm{rlp}.\mathrm{llp},
\]

and the canonical right class is

\[
\mathcal F_{\mathrm{can}}=T^\perp=T.\mathrm{rlp}.
\]

## Universal property

Define a morphism property `A` to be orthogonally saturated when

\[
A^{\perp\perp}=A.
\]

v1.43 proves:

\[
\boxed{
T\le A\ \wedge\ A^{\perp\perp}=A
\Longrightarrow
T^{\perp\perp}\le A.
}
\]

Hence `canonicalGeneratedScaledAnodyne` is the least orthogonally saturated
morphism property containing the canonical attachment generators.

For a v1.42 `ScaledAnodynePresentation` satisfying

\[
T\le A\le T^{\perp\perp},
\]

orthogonal saturation forces literal equality

\[
\boxed{A=T^{\perp\perp}}.
\]

Thus compatible presentations were already right-class equivalent in v1.42;
v1.43 shows that among orthogonally saturated presentations the canonical left
class itself is unique.

## Algebraic closure laws

Because the canonical left class is an `llp` class, pinned Mathlib supplies
stability under:

- retracts;
- cobase change;
- identity and composition.

Because the canonical right class is an `rlp` class, pinned Mathlib supplies
stability under:

- retracts;
- base change;
- identity and composition.

These are consequences, not extra KuuOS axioms.

## Weak factorization system frontier

The orthogonality relations are already exact:

\[
\mathcal A_{\mathrm{can}}={}^\perp\mathcal F_{\mathrm{can}},
\qquad
\mathcal F_{\mathrm{can}}=\mathcal A_{\mathrm{can}}^\perp.
\]

The sole remaining datum needed for Mathlib's native weak-factorization-system
structure is

\[
\boxed{
\operatorname{HasFactorization}
(\mathcal A_{\mathrm{can}},\mathcal F_{\mathrm{can}}).
}
\]

Under this input, Mathlib's retract argument yields

\[
\boxed{
\operatorname{IsWeakFactorizationSystem}
(\mathcal A_{\mathrm{can}},\mathcal F_{\mathrm{can}}).
}
\]

Accordingly, the next constructive frontier is a genuine factorization theorem,
most naturally via a small-object argument once the required colimits and
smallness properties of the scaled-simplicial-set category are established.

## Boundary

v1.43 does **not** claim:

- that the factorization theorem is already proved;
- that `ScaledSSet` already carries a full cofibrantly generated model structure;
- that the canonical KuuOS class is already equal to a Lurie/Mathlib standard
  scaled-anodyne class;
- that ordinary unscaled anodyne extensions can be silently promoted to the
  scaled setting.

The remaining gap is therefore sharply localized to factorization/small-object
machinery, rather than lifting or presentation invariance.
