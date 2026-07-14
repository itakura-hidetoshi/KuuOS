# MemoryOS v0.54 — Quotient metric density transport and Radon–Nikodym cocycle

MemoryOS v0.54 extends the v0.53 quotient-transport Jacobian witness with an exact density/measure transport layer. It remains future-only, read-only, and advisory. It does not rank, prune, select, commit, activate, execute, mutate WORLD state, claim verification, or grant truth authority.

## Source bindings

The certificate fail-closes over:

- the accepted MemoryOS v0.53 certificate digest;
- the v0.53 quotient-transport Jacobian digest;
- the v0.53 mode-composition digest;
- an independently supplied accepted MemoryOS v0.52 certificate;
- the v0.52 quotient-metric covector transport digest and composition digest;
- all four DecisionOS candidate IDs, both PlanOS history IDs, all nine quotient-coordinate probes, and the relational review, dissent, and minority-protection sets.

## Exact density transport

For

\[
K(c)=\begin{pmatrix}2&c\\c&2\end{pmatrix},\qquad
\det K(c)=4-c^2=(2+c)(2-c),
\]

v0.53 established the normalized full-rank Jacobian

\[
J(c\to d)=\frac{\det K(d)}{\det K(c)}.
\]

On an invertible full-rank transition, v0.54 defines the Radon–Nikodym density multiplier

\[
\rho(c\to d)=J(c\to d)^{-1}
             =\frac{\det K(c)}{\det K(d)}.
\]

The modewise density factors are the reciprocals of the mode transport multipliers:

\[
\rho_s(c\to d)=\frac{2+c}{2+d},\qquad
\rho_a(c\to d)=\frac{2-c}{2-d},
\]

and satisfy

\[
\rho_s(c\to d)\rho_a(c\to d)=\rho(c\to d),\qquad
\rho(c\to d)J(c\to d)=1.
\]

Reference values are:

- `1 -> 0`: symmetric density factor `3/2`, antisymmetric density factor `1/2`, total density factor `3/4`;
- `0 -> 1`: symmetric density factor `2/3`, antisymmetric density factor `2`, total density factor `4/3`;
- both nontrivial full-rank round trips have total density factor `1`.

## Finite-support pushforward and pullback

Each of the nine retained quotient-coordinate probes receives a fixed exact rational source mass weight. For every invertible full-rank transition, the runtime emits:

- the source mass and source density;
- the target coordinate-cell volume factor `J`;
- the target pushforward density `source_density * rho`;
- an exact pushforward mass witness;
- an exact pullback witness recovering the source density.

Thus the discrete support is preserved and the density change compensates exactly for the coordinate-volume change.

## Radon–Nikodym cocycle

For full-rank `source`, `middle`, and `target` metrics,

\[
\rho(s\to m)\rho(m\to t)=\rho(s\to t).
\]

All 27 ordered triples are retained. Exactly eight triples are fully invertible and carry an active density cocycle. The two nontrivial round-trip paths preserve density exactly.

## Singular measure boundary

For target cross `2`,

\[
\det K(2)=0,\qquad J(c\to2)=0
\]

for full-rank source `c`. v0.54 therefore does not emit a two-dimensional density multiplier. It retains each probe mass as a singular pushforward support witness and marks the transition as a full-rank-to-rank-one singular measure boundary.

When the source cross is `2`, no two-dimensional source density exists. Only the previously certified partial symmetric transport remains visible; no recovery of lost antisymmetric information or two-dimensional density is claimed.

## Runtime counts

- directed transitions: 9
- invertible full-rank density transitions: 4
- probe density transport records: 36
- full-rank to rank-one singular transitions: 2
- singular probe pushforward records: 18
- rank-one source boundaries: 3
- ordered cocycle records: 27
- active full-rank cocycles: 8
- nontrivial density-preserving round trips: 2

## Fail-closed rejection

The checker rejects source certificate substitution, digest mismatch, Jacobian or mode-composition tampering, v0.52 transport tampering, density multiplier changes, probe mass/density witness changes, cocycle changes, false two-dimensional density at a singular boundary, false information recovery, candidate ranking or selection, decision commit, plan synthesis, activation, execution, source or WORLD mutation, verification claims, and truth authority.
