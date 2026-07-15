# MemoryOS v0.86 — Joint Sensor Product Refinement Certificate Kernel

## Scope

MemoryOS v0.86 extends the v0.85 group-valued sensor layer from one post-processing sensor to finite two-sensor products. The new layer treats a pair

\[
\sigma:G\to H,
\qquad
\tau:G\to I
\]

as the joint sensor

\[
\langle\sigma,\tau\rangle:G\to H\times I,
\qquad
g\mapsto(\sigma(g),\tau(g)).
\]

The construction is finite, exact, read-only, and advisory. It does not infer physical measurements, rank candidates, prune histories, select plans, mutate source certificates, or grant truth or execution authority.

## Formal kernel law

For the root-independent global evaluation

\[
E_i:\Gamma(F)^\times\to G,
\]

the joint evaluation is

\[
E_i^{\sigma,\tau}
=
\langle\sigma,\tau\rangle\circ E_i.
\]

Its invisible kernel is exactly the intersection of the component kernels:

\[
\boxed{
K_i^{\sigma,\tau}
=
K_i^\sigma\cap K_i^\tau
}
\]

where

\[
K_i^\sigma=\ker(\sigma\circ E_i),
\qquad
K_i^\tau=\ker(\tau\circ E_i).
\]

Therefore

\[
K_i^{\sigma,\tau}\le K_i^\sigma,
\qquad
K_i^{\sigma,\tau}\le K_i^\tau.
\]

A product sensor is at least as informative as either component separately.

## Root independence

The joint evaluation homomorphism, joint invisible kernel, and joint visible range are independent of the selected root chart:

\[
E_i^{\sigma,\tau}=E_j^{\sigma,\tau},
\]

\[
K_i^{\sigma,\tau}=K_j^{\sigma,\tau},
\]

\[
R_i^{\sigma,\tau}=R_j^{\sigma,\tau}.
\]

## Quotient projections

Since the joint kernel lies inside each component kernel, there are canonical quotient homomorphisms

\[
\Gamma(F)^\times/K_i^{\sigma,\tau}
\longrightarrow
\Gamma(F)^\times/K_i^\sigma,
\]

\[
\Gamma(F)^\times/K_i^{\sigma,\tau}
\longrightarrow
\Gamma(F)^\times/K_i^\tau.
\]

Both maps preserve representative classes:

\[
[s]_{K^{\sigma,\tau}}
\longmapsto
[s]_{K^\sigma},
\qquad
[s]_{K^{\sigma,\tau}}
\longmapsto
[s]_{K^\tau}.
\]

The first isomorphism theorem also gives

\[
\Gamma(F)^\times/K_i^{\sigma,\tau}
\simeq_{\mathrm{mul}}
\operatorname{range}(E_i^{\sigma,\tau}).
\]

## Joint faithfulness

The sensor pair is jointly injective exactly when simultaneous equality of both component outputs forces equality in the source group:

\[
\langle\sigma,\tau\rangle\text{ injective}
\iff
\forall x,y,
\sigma(x)=\sigma(y)
\land
\tau(x)=\tau(y)
\Rightarrow x=y.
\]

For a jointly injective pair,

\[
K_i^{\sigma,\tau}=K_i,
\]

and therefore

\[
\Gamma(F)^\times/K_i
\simeq_{\mathrm{mul}}
\Gamma(F)^\times/K_i^{\sigma,\tau}.
\]

If either component is injective, the pair is jointly injective.

## Wilson projection coherence

A class function on either component group can be pulled back along the corresponding product projection. The resulting joint Wilson observable equals the original component Wilson observable exactly:

\[
W_{\chi\circ\pi_H}^{\sigma,\tau}(s)
=
W_\chi^\sigma(s),
\]

\[
W_{\psi\circ\pi_I}^{\sigma,\tau}(s)
=
W_\psi^\tau(s).
\]

These observables remain root independent.

## Canonical finite sensor family

The exact runtime retains the v0.85 identity, parity, and terminal sensors and evaluates five product profiles:

| Joint sensor | Jointly injective | AB/BA separator |
|---|---:|---:|
| identity × parity | yes | preserved |
| identity × terminal | yes | preserved |
| parity × terminal | no | collapsed |
| parity × parity | no | collapsed |
| terminal × terminal | no | collapsed |

For the canonical mixed section, ordered AB lies in every component kernel. Ordered BA is visible to identity sensing but invisible to parity and terminal sensing. Since joint invisibility is intersection membership, pairing identity with any sensor preserves the separator, while combinations built only from parity and terminal sensors remain unable to recover it.

The collapse is recorded as finite sensor-resolution loss. It is not treated as source equality or truth.

## Exact runtime ledger

- literature records: 6
- joint sensor profiles: 5
- kernel-intersection records: 20
- root-independence records: 80
- quotient-projection records: 40
- jointly-injective quotient equivalences: 8
- Wilson-projection records: 40
- canonical joint visibility records: 20
- confidence-preservation records: 4
- memory-fusion records: 4
- full-rank transport records: 8
- singular atomic records: 4
- rank-one source boundaries: 3

## Confidence policy

The v0.85 adjusted confidence values are copied exactly:

\[
\frac13,
\qquad
\frac5{18},
\qquad
\frac{11}{54},
\qquad
\frac{11}{54}.
\]

The new joint-sensor penalty is

\[
0.
\]

Sensor-family resolution is diagnostic metadata only.

## Fail-closed source binding

The runtime reissues the accepted v0.85 certificate and verifies:

- source schema and acceptance,
- full certificate digest,
- required and forbidden Boolean claims,
- exact record counts,
- every source collection digest,
- candidate, history, and probe support,
- review, dissent, and minority sets,
- identity/parity/terminal profile semantics,
- canonical AB/BA visibility at all roots.

Claim mutation, collection mutation, unexpected claims, confidence mutation, or authority-boundary mutation blocks issuance.

## Authority boundary

MemoryOS v0.86 does not claim:

- a universal classification of sensor families,
- a universal information lattice,
- a continuum multi-sensor observation stack,
- physical measurement-fusion inference,
- candidate ranking, pruning, or selection,
- decision commit or receipt issuance,
- plan synthesis, activation, or execution,
- source or persistent WORLD mutation,
- verification authority or truth authority.
