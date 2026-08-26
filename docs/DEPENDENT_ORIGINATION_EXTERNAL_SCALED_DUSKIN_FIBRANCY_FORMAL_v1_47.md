# Dependent Origination — External Scaled-Duskin Fibrancy Formal v1.47

## Scope

Version 1.46 proves that an arbitrary external scaled-anodyne generator family
`E` determines the same generated left class, right lifting class, weak
factorization system, and fibrant objects as the canonical KuuOS horn-cylinder
generators `T`, provided

\[
T\le E^{\perp\perp},
\qquad
E\le T^{\perp\perp}.
\]

Version 1.47 returns that external comparison to the global Duskin model-
equivalence spine.

## Separate source and target presentations

A bicategorical equivalence

\[
B \simeq C
\]

may involve different universe levels.  Therefore v1.47 does not require a
single external generator family to inhabit an artificial common universe.
Instead it packages

- an external presentation `P_B` for the global Duskin scaled object of `B`;
- an external presentation `P_C` for the global Duskin scaled object of `C`.

Each presentation contains its own generator family and a v1.46
`ScaledAnodyneGeneratorComparison` certificate.

The two generator lists need not be equal.

## External fibrancy

For an external presentation `P` on `B`, define

\[
\operatorname{ExternalFibrant}_P(N_D(B))
:\Longleftrightarrow
E_P^\perp\bigl(N_D(B)\to *\bigr).
\]

By v1.46,

\[
E_P^\perp=T^\perp,
\]

hence

\[
\boxed{
\operatorname{ExternalFibrant}_P(N_D(B))
\iff
\operatorname{AttachmentFibrant}(N_D(B)).
}
\]

The same statement holds independently for `C`.

## Return to the global model-equivalence carrier

The new structure

`CoherentNormalizedScaledExternalDuskinModelEquivalence`

contains

1. the already established coherent normalized homotopy-class model
   equivalence;
2. source external fibrancy with respect to `P_B`;
3. target external fibrancy with respect to `P_C`.

Using the external/canonical fibrancy equivalences, v1.47 constructs the
existing v1.42

`CoherentNormalizedScaledAttachmentFibrantModelEquivalence`.

Therefore all established strictification and terminal-RLP machinery is reused
without duplication.

## Main theorem

The final theorem is

\[
\boxed{
\operatorname{HasScaledHornFillers}
  (N_D(B),H_B)
\iff
\operatorname{HasScaledHornFillers}
  (N_D(C),H_C).
}
\]

The source and target may be certified by different external scaled-anodyne
presentations.

## Mathematical boundary

This layer does not invent or identify a Lurie scaled-anodyne generator family.
The remaining genuinely external task is now exact:

for every proposed standard generator family `E`, prove

\[
\boxed{
T\le E^{\perp\perp}
\quad\text{and}\quad
E\le T^{\perp\perp}.
}
\]

Once those two inclusions are available, v1.46 and v1.47 automatically provide

- generated left-class equality;
- right-class equality;
- weak-factorization-system transport;
- external fibrancy = canonical attachment fibrancy;
- terminal RLP for every chosen scaled horn family;
- strict global scaled-Duskin fibrancy invariance across coherent normalized
  bicategorical model equivalence.
