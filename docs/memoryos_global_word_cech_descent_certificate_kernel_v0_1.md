# MemoryOS v0.82 — global word sections and non-Abelian Čech descent

## Scope

MemoryOS v0.82 advances the normalized four-root pair-groupoid of v0.81 from pairwise word transport to exact descent of complete local word families.

The finite model remains the four-route `S3` atlas inherited from v0.78–v0.81. It does not claim a continuum sheaf, stack, principal bundle, universal non-Abelian cohomology classification, physical gauge field, or truth authority.

## Local word families

Let

\[
F_i = F(Y_1^{(i)},Y_2^{(i)},Y_3^{(i)},D_i)
\]

be the normalized free group at route root \(i\). The v0.81 transport is

\[
T_{i\leftarrow j}:F_j\longrightarrow F_i
\]

with

\[
T_{i\leftarrow i}=\operatorname{id},
\qquad
T_{i\leftarrow j}T_{j\leftarrow k}=T_{i\leftarrow k},
\qquad
T_{i\leftarrow j}^{-1}=T_{j\leftarrow i}.
\]

A local word family is a four-tuple

\[
w=(w_0,w_1,w_2,w_3),\qquad w_i\in F_i.
\]

It is descent-compatible when

\[
\boxed{T_{i\leftarrow j}(w_j)=w_i}
\]

for every ordered pair \((i,j)\).

## Non-Abelian Čech mismatch

The exact ordered overlap mismatch is

\[
M_{ij}(w)=w_i^{-1}T_{i\leftarrow j}(w_j).
\]

Compatibility is equivalent to

\[
M_{ij}(w)=1
\]

for all ordered overlaps.

The Lean kernel proves the exact non-Abelian cocycle law

\[
\boxed{
M_{ij}(w)\;T_{i\leftarrow j}(M_{jk}(w))=M_{ik}(w)
}
\]

and the transported inverse law

\[
\boxed{
M_{ij}(w)\;T_{i\leftarrow j}(M_{ji}(w))=1.
}
\]

These statements hold for arbitrary local families, including incompatible or deliberately perturbed families.

## Reconstruction of global sections

Given one anchor root \(a\) and one word \(u\in F_a\), define

\[
\operatorname{Rec}_a(u)_i=T_{i\leftarrow a}(u).
\]

The formal kernel proves:

1. `Rec_a(u)` is compatible;
2. its anchor component is exactly \(u\);
3. every compatible family is reconstructed from any one of its components:

\[
\boxed{
\operatorname{Rec}_a(w_a)=w.
}
\]

Thus the four local presentations form one exact global descent section without privileging a permanent root chart.

## Evaluation and Wilson descent

For a compatible section \(w\), the exact group evaluation is root independent:

\[
\boxed{
\operatorname{ev}_i(w_i)=\operatorname{ev}_j(w_j).
}
\]

For every class function \(\chi\), the Wilson observable also descends:

\[
\boxed{
\chi(\operatorname{ev}_i(w_i))
=
\chi(\operatorname{ev}_j(w_j)).
}
\]

The global section therefore has one finite exact group value and one class-function value, although each local word presentation differs.

## Single-chart perturbation localization

Starting from a compatible family, v0.82 right-multiplies only the route-2 component by the defect generator:

\[
w'_2=w_2D_2,
\qquad
w'_i=w_i\quad(i\ne2).
\]

The exact mismatch support is localized to the six directed off-diagonal overlaps incident to route 2:

\[
(i,2),\;(2,i),\qquad i\in\{0,1,3\}.
\]

All overlaps avoiding route 2 remain identity, while all six incident directed overlaps are nontrivial. The full non-Abelian cocycle law remains exact for the perturbed family.

This is a diagnostic localization statement only. It does not rank, prune, select, delete, or verify any candidate.

## Canonical global separator

The v0.81 route-0 normalized mixed word

\[
u=Y_3^{(0)}D_0
\]

is promoted to the global section

\[
w_i=T_{i\leftarrow0}(u).
\]

For all four roots:

- ordered AB evaluates to identity with permutation trace `3`;
- ordered BA evaluates to `(021)` with permutation trace `0`.

Hence

\[
\boxed{
W_{\mathrm{perm}}(w^{AB})=3\ne0=W_{\mathrm{perm}}(w^{BA})
}
\]

is a root-independent global-section separator.

## Exact runtime ledger

The certificate contains:

- 6 inherited literature records;
- 4 finite route-object records;
- 4 global-section component records;
- 16 pairwise compatibility records;
- 16 canonical mismatch records;
- 64 canonical non-Abelian cocycle records;
- 16 mismatch inverse records;
- 16 anchor reconstruction records;
- 4 one-chart-perturbed component records;
- 16 perturbed mismatch records;
- 64 perturbed cocycle records;
- 8 exact global-section evaluation records;
- 2 global Wilson descent records;
- 4 source-confidence preservation records;
- 4 memory-fusion records;
- 8 full-rank transport records;
- 4 singular atomic records;
- 3 rank-one source boundaries.

All free words are deterministic signed-generator lists with exact free reduction. All finite group values are exact permutation triples. All confidence values are exact rationals.

## Source binding and fail-closed behavior

The runtime regenerates the accepted v0.81 certificate and validates:

- source schema and certificate digest;
- all required true and forbidden false claims;
- source collection counts and collection digests;
- retained candidates, histories, probes, review sets, dissent, and minority visibility;
- normalized transition substitution support;
- canonical separator values and traces.

The v0.82 checker rejects edits to mismatch, cocycle, inverse, reconstruction, perturbation-support, global evaluation, confidence, authority-boundary, or source-certificate data.

## Confidence policy

No new confidence penalty is introduced:

\[
C_{v0.82}=C_{v0.81}.
\]

The retained exact values are:

- flat: \(1/3\);
- single-support: \(5/18\);
- ordered AB: \(11/54\);
- ordered BA: \(11/54\).

## Authority boundary

MemoryOS v0.82 remains:

- future-only;
- read-only;
- advisory;
- non-ranking;
- non-pruning;
- non-selecting;
- non-committing;
- non-activating;
- non-executing;
- non-mutating;
- non-verifying;
- non-truth-authoritative.
