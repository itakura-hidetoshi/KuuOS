# MemoryOS v0.87 — Finite Sensor Family Refinement Certificate Kernel

## Scope

MemoryOS v0.87 extends the v0.86 two-sensor product to an arbitrary finite family of group-valued sensors

\[
\sigma_i:G\to H_i,
\qquad i\in I,
\]

with finite index set \(I\). The family sensor is the pointwise product

\[
\Sigma_I:G\to\prod_{i\in I}H_i,
\qquad
\Sigma_I(g)=(\sigma_i(g))_{i\in I}.
\]

The layer is finite, exact, read-only, and advisory. It does not rank or prune candidates, select decisions, mutate source certificates, infer physical measurements, or grant truth or execution authority.

## Finite family evaluation

For the root-independent global evaluation

\[
E_r:\Gamma(F)^\times\to G,
\]

the family evaluation is

\[
E_r^I=\Sigma_I\circ E_r.
\]

Its invisible kernel is

\[
K_r^I=\ker(E_r^I).
\]

## Kernel as a finite infimum

The central theorem is

\[
\boxed{
K_r^I=\bigcap_{i\in I}K_r^{\sigma_i}
}
\]

or, in the subgroup lattice,

\[
\boxed{
K_r^I=\bigwedge_{i\in I}K_r^{\sigma_i}.
}
\]

Consequently, for every component \(i\),

\[
K_r^I\le K_r^{\sigma_i}.
\]

The family is at least as informative as every component sensor.

For the empty family,

\[
\boxed{K_r^\varnothing=\top,}
\]

so every section is invisible.

## Root independence

The family evaluation, family kernel, and family range do not depend on the selected root chart:

\[
E_r^I=E_s^I,
\qquad
K_r^I=K_s^I,
\qquad
R_r^I=R_s^I.
\]

## Component quotient projections

Kernel inclusion gives a canonical homomorphism from the family quotient to every component quotient:

\[
\Gamma(F)^\times/K_r^I
\longrightarrow
\Gamma(F)^\times/K_r^{\sigma_i},
\]

\[
[s]_{K^I}\longmapsto[s]_{K^{\sigma_i}}.
\]

The first isomorphism theorem gives

\[
\Gamma(F)^\times/K_r^I
\simeq_{\mathrm{mul}}
\operatorname{range}(E_r^I).
\]

## Separating families

A finite family is jointly separating exactly when

\[
\forall x,y\in G,
\bigl(\forall i,\ \sigma_i(x)=\sigma_i(y)\bigr)
\Rightarrow x=y.
\]

Equivalently, \(\Sigma_I\) is injective. If one component sensor is injective, the complete family is injective. For a separating family,

\[
K_r^I=K_r,
\]

and

\[
\Gamma(F)^\times/K_r
\simeq_{\mathrm{mul}}
\Gamma(F)^\times/K_r^I.
\]

## Subfamily restriction and redundancy

For a reindexing map \(f:J\to I\), restriction to the reindexed family can only enlarge the invisible kernel:

\[
K_r^I\le K_r^{f^\ast I}.
\]

If \(f\) is surjective, then no component sensor has been lost and

\[
\boxed{K_r^I=K_r^{f^\ast I}.}
\]

This includes duplicate coordinates: repeating an existing sensor does not change the exact family kernel.

## Wilson projection coherence

For a class function \(\chi_i:H_i\to R\), pullback through the product projection gives

\[
\boxed{
W_{\chi_i\circ\pi_i}^{I}(s)=W_{\chi_i}^{\sigma_i}(s).
}
\]

The equality is exact and remains root independent.

## Canonical finite profiles

The runtime enumerates the exact \(S_3\) signatures of eight finite families:

| Family | Kernel order in \(S_3\) | Separating | AB/BA separator |
|---|---:|---:|---:|
| empty | 6 | no | collapsed |
| identity | 1 | yes | preserved |
| parity | 3 | no | collapsed |
| terminal | 6 | no | collapsed |
| identity + parity | 1 | yes | preserved |
| parity + terminal | 3 | no | collapsed |
| identity + parity + terminal | 1 | yes | preserved |
| parity + parity | 3 | no | collapsed |

The duplicated parity family has the same kernel as the parity singleton. Families containing identity sensing preserve the canonical ordered-AB/BA separator at every root. Nonseparating families record sensor-resolution loss rather than source equality or truth.

## Exact subfamily relations

The runtime records eight finite restrictions at every root. Exact kernel equality is retained for:

- identity + parity + terminal → identity + parity,
- identity + parity → identity,
- parity + terminal → parity,
- parity + parity → parity.

Strict information loss occurs for:

- identity + parity + terminal → parity + terminal,
- identity + parity → parity,
- parity → empty,
- identity → empty.

## Runtime ledger

- literature records: 6
- finite family profiles: 8
- family-kernel records: 32
- root-independence records: 128
- component quotient projections: 48
- separating-family quotient equivalences: 12
- Wilson component projections: 48
- canonical family visibility records: 32
- subfamily refinement records: 32
- confidence-preservation records: 4
- memory-fusion records: 4
- full-rank transport records: 8
- singular atomic records: 4
- rank-one source boundaries: 3

## Confidence policy

The v0.86 adjusted confidence values are preserved exactly:

\[
\frac13,
\qquad
\frac5{18},
\qquad
\frac{11}{54},
\qquad
\frac{11}{54}.
\]

The new finite-family penalty is zero. Family size, redundancy, and separator resolution are diagnostic metadata only.

## Fail-closed source binding

The runtime reissues the accepted v0.86 certificate and verifies:

- acceptance and schema,
- the complete certificate digest,
- all required and forbidden Boolean claims,
- exact source record counts,
- every source collection digest,
- candidate, history, and probe retention,
- review, dissent, and minority sets,
- canonical joint-profile order and injectivity,
- canonical AB/BA visibility at all four roots.

Mutation of source data, family claims, confidence, authority boundaries, or unexpected claims blocks issuance.

## Authority boundary

MemoryOS v0.87 does not claim:

- a universal classification of sensor families,
- a universal information lattice,
- an infinite-family limit,
- a continuum observation stack,
- physical measurement-fusion inference,
- candidate ranking, pruning, or selection,
- decision commit or receipt issuance,
- plan synthesis, activation, or execution,
- source or persistent WORLD mutation,
- verification authority or truth authority.
