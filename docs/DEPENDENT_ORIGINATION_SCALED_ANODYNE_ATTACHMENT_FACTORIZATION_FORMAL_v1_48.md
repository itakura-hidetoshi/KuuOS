# Dependent Origination — Scaled-Anodyne Attachment Factorization Formal v1.48

## Scope

Version 1.46 reduced comparison with any external scaled-anodyne presentation
`E` to two closure inclusions

\[
T\le E^{\perp\perp},
\qquad
E\le T^{\perp\perp},
\]

where `T` is the canonical KuuOS family of horn-cylinder attachment
inclusions.

Version 1.48 refines the first inclusion geometrically.

## The scaling mismatch

A canonical KuuOS generator has underlying map

\[
A=(\Delta[n]\times\{\varepsilon\})\cup
(\Lambda_i^n\times\Delta[1])
\hookrightarrow
\Delta[n]\times\Delta[1].
\]

Its source in `T` has **minimal scaling**, while the cylinder has the scaling
pulled back from the chosen simplex scaling on `Δ[n]`.

Therefore this map is generally stronger than the source one obtains by simply
restricting the cylinder scaling to the attachment.

## Induced attachment scaling

Let `A_induced` denote the same underlying attachment equipped with the scaling
pulled back along its inclusion into the cylinder.

Then the canonical generator factors literally as

\[
\boxed{
A_{\min}
\xrightarrow{m_{\mathrm{scale}}}
A_{\mathrm{induced}}
\xrightarrow{j_{\mathrm{induced}}}
\Delta[n]\times\Delta[1].
}
\]

The first map is the identity on the underlying simplicial set and only enriches
the source scaling.  The second map is scaled by construction.

Lean definitions:

- `pullbackScaling`;
- `inducedHornCylinderAttachmentScaling`;
- `inducedScaledHornCylinderAttachment`;
- `minimalToInducedHornCylinderAttachment`;
- `inducedScaledHornCylinderAttachmentInclusion`;
- `scaledHornCylinderAttachmentInclusion_factorization`.

## Generator families

The factorization is promoted to two morphism properties:

- `scaledHornAttachmentScalingEnrichments`;
- `inducedScaledHornAttachmentGenerators`.

For each original generator `g`, Lean proves

```text
scaledHornAttachmentScalingEnrichment g ≫
  inducedScaledHornAttachmentGeneratorHom g
=
scaledHornAttachmentGeneratorHom g.
```

## Refined external-comparison criterion

For an external generator family `E`, define the factor comparison condition
by

\[
\begin{aligned}
&\text{scaling enrichments}\le E^{\perp\perp},\\
&\text{induced attachments}\le E^{\perp\perp}.
\end{aligned}
\]

Because `E.rlp.llp` is closed under composition, these two inclusions imply

\[
\boxed{T\le E^{\perp\perp}.}
\]

Adding the reverse comparison

\[
E\le T^{\perp\perp}
\]

recovers the complete v1.46 certificate and therefore

\[
E^{\perp\perp}=T^{\perp\perp},
\qquad
E^\perp=T^\perp.
\]

## Relation to the standard scaled-anodyne generators

The standard scaled-anodyne generating family used in the literature contains
three types.  Type (A) consists of inner horn inclusions with the consecutive
triangle `Δ^{\{i-1,i,i+1\}}` declared thin.  The literature also proves
stability of scaled-anodyne maps under pushout-product with cofibrations.

This makes the **induced attachment** factor the natural target of the
standard type-(A) pushout-product comparison.

However, the KuuOS canonical source uses minimal scaling.  Consequently the
map

\[
m_{\mathrm{scale}}:A_{\min}\to A_{\mathrm{induced}}
\]

is a separate comparison obligation.  It must not be silently absorbed into
the type-(A) argument.

This is the main mathematical correction of v1.48: it identifies exactly where
the canonical strictification generator is stronger than the obvious standard
pushout-product geometry.

## New frontier

The standard-comparison problem is now split into three concrete pieces:

\[
\boxed{
\begin{aligned}
&\text{(I) induced type-(A)-style attachments}
   \le E_{\mathrm{std}}^{\perp\perp},\\
&\text{(II) source scaling enrichments}
   \le E_{\mathrm{std}}^{\perp\perp},\\
&\text{(III) }E_{\mathrm{std}}\le T^{\perp\perp}.
\end{aligned}}
\]

Once these are established, v1.46 and v1.47 immediately supply equality of the
weak factorization systems, equality of fibrant objects, and the external
presentation version of strict global Duskin fibrancy invariance.
