# Dependent Origination — Choi / Complete Positivity Equivalence v0.10

This layer closes the finite-dimensional positivity gap left explicit in v0.9.

## Statement

For a complex-linear map

\[
\Phi : M_n(\mathbb C) \to M_m(\mathbb C),
\]

with v0.9 Choi matrix

\[
J_\Phi[(i,a),(j,b)] = \Phi(E_{ij})_{ab},
\]

v0.10 proves

\[
\boxed{
J_\Phi \succeq 0
\iff
\Phi \text{ is represented by Mathlib's } CompletelyPositiveMap
}.
\]

The theorem is `choi_posSemidef_iff_mathlibCompletelyPositive`.

## Mathlib side

The repository is pinned to Mathlib revision

`5450b53e5ddc75d46418fabb605edbf36bd0beb6`.

At that revision, `CompletelyPositiveMap` requires positivity preservation of
all finite `CStarMatrix` amplifications.

v0.10 proves exactly those obligations rather than introducing a parallel CP
predicate.

## Block flattening

A `k × k` block matrix with `d × d` complex blocks is flattened to the scalar
matrix indexed by `Fin k × Fin d`:

\[
\operatorname{flat}(M)_{(p,a),(q,b)} = M_{pq}[a,b].
\]

The file proves that flattening preserves multiplication and involution.  It
then proves both positivity-transfer directions from C-star square
factorizations, rather than assuming that the two order implementations are
definitionally identical.

## CP implies Choi positivity

Define the Choi probe by

\[
\Omega_{ij}=E_{ij}.
\]

Its flattening is the rank-one Gram matrix of the diagonal Bell vector, hence is
positive.  Complete positivity applied at amplification size `n` gives

\[
(id_n \otimes \Phi)(\Omega) \ge 0.
\]

The flattened image is entrywise exactly `J_Φ`, proving `J_Φ \succeq 0`.

## Choi positivity implies complete positivity

From `J_Φ \succeq 0`, the matrix C-star square-factorization gives

\[
J_\Phi = B^* B.
\]

For each row index `r` of `B`, define a Kraus matrix

\[
(K_r)_{ai}=\overline{B_{r,(i,a)}}.
\]

The v0.9 Choi reconstruction formula then yields

\[
\Phi(X)=\sum_r K_r X K_r^*.
\]

At arbitrary amplification size `k`, the proof defines `I_k \otimes K_r`
without an arithmetic reindexing and establishes the exact scalar-block formula

\[
\operatorname{flat}((id_k\otimes\Phi)(M))
=
\sum_r
(I_k\otimes K_r)\operatorname{flat}(M)(I_k\otimes K_r)^*.
\]

Every summand is positive semidefinite when `M` is positive, and finite sums
remain positive.  The result is transferred back to `CStarMatrix`, satisfying
Mathlib's complete-positivity field for every `k`.

## Channel certificate

v0.10 also supplies a channel surface

`MathlibCPChannelCertificate n m`

consisting of a Mathlib CP map plus the already-proved v0.9 trace-preservation
condition.  Conversions to and from `ChoiChannelCertificate` preserve the
underlying linear map exactly.

## Scope

This is the finite-dimensional Choi theorem for the matrix algebras used by the
KuuOS process-tensor layer.  It does not claim an infinite-dimensional Choi
representation and does not promote any KuuOS process tensor to a physical
Yang–Mills process without an explicit physical bridge.
