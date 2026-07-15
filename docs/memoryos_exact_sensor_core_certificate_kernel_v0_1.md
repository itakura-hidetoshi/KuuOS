# MemoryOS v0.88 — Exact Sensor Core and Redundancy Certificate Kernel

## Scope

MemoryOS v0.88 advances the v0.87 finite sensor-family layer from kernel refinement to exact finite support reduction. For a finite homogeneous sensor family

\[
\sigma_i:G\to H,
\qquad i\in I,
\]

and a retained support \(S\subseteq I\), define

\[
K_r^S=\bigcap_{i\in S}K_r^{\sigma_i}.
\]

The new layer certifies one-coordinate redundancy, duplicate and dominated-sensor removal, irredundancy witnesses, and canonical minimum-cardinality cores for the finite canonical \(S_3\) profiles.

The construction remains finite, exact, read-only, and advisory. It does not use core size to rank or prune candidates, mutate source certificates, infer physical measurement sufficiency, or grant truth or execution authority.

## Finite support kernel

For a finite support \(S\),

\[
K_r^S=\bigwedge_{i\in S}K_r^{\sigma_i}.
\]

Membership is exact:

\[
s\in K_r^S
\iff
\forall i\in S,\ s\in K_r^{\sigma_i}.
\]

The empty support satisfies

\[
\boxed{K_r^\varnothing=\top.}
\]

If \(S\subseteq T\), then

\[
\boxed{K_r^T\le K_r^S.}
\]

Thus erasing a sensor can only enlarge the invisible kernel.

## One-step redundancy

A sensor \(i\in S\) is redundant exactly when

\[
K_r^S=K_r^{S\setminus\{i\}}.
\]

If the remaining support already implies invisibility to sensor \(i\),

\[
K_r^{S\setminus\{i\}}\le K_r^{\sigma_i},
\]

then erasing \(i\) preserves the exact kernel.

Duplicate sensors are a special case. If \(i\ne j\) and \(\sigma_i=\sigma_j\), then

\[
\boxed{K_r^S=K_r^{S\setminus\{j\}}.}
\]

## Irredundancy witnesses

A support is one-step irredundant when every retained coordinate is necessary:

\[
\forall i\in S,
\quad
K_r^S\ne K_r^{S\setminus\{i\}}.
\]

The formal witness criterion is constructive. For each \(i\in S\), it suffices to provide a section that is invisible to every sensor after erasing \(i\), but remains visible to \(\sigma_i\).

## Exact sensor core

A core \(C\subseteq S\) is exact when:

1. \(C\subseteq S\),
2. \(K_r^C=K_r^S\),
3. \(C\) is one-step irredundant.

Exact-core equality composes through intermediate supports. If \(C\) is an exact core of \(M\), and \(M\) preserves the kernel of \(S\), then \(C\) is an exact core of \(S\).

Equal kernels preserve the exact observable quotient and representative classes. The runtime records this equivalence at all four roots.

## Canonical finite exhaustive search

The runtime exhaustively enumerates every index subset of each canonical v0.87 family. It computes all kernel-preserving subfamilies, determines the minimum cardinality, and selects the lexicographically first minimum support as the canonical core.

This is a finite exact search over the listed profiles only. It does not assert uniqueness of minimum cores in general. The duplicated parity family has two distinct minimum cores, each selecting one of the duplicate coordinates.

## Canonical exact cores

| Source family | Source size | Canonical core | Core size | Kernel order |
|---|---:|---|---:|---:|
| empty | 0 | empty | 0 | 6 |
| identity | 1 | identity | 1 | 1 |
| parity | 1 | parity | 1 | 3 |
| terminal | 1 | empty | 0 | 6 |
| identity + parity | 2 | identity | 1 | 1 |
| parity + terminal | 2 | parity | 1 | 3 |
| identity + parity + terminal | 3 | identity | 1 | 1 |
| parity + parity | 2 | first parity | 1 | 3 |

The identity sensor dominates parity and terminal sensing whenever present. Parity dominates terminal sensing. A terminal singleton is equivalent to the empty support. Repeated parity coordinates are exactly redundant.

## Exact runtime ledger

- literature records: 6
- exact-core profiles: 8
- rootwise exact-core records: 32
- one-step redundancy records: 48
- canonical removal records: 24
- irredundancy witness records: 24
- equal-kernel quotient-equivalence records: 32
- exhaustive minimality records: 8
- confidence-preservation records: 4
- memory-fusion records: 4
- full-rank transport records: 8
- singular atomic records: 4
- rank-one source boundaries: 3

## Confidence policy

The v0.87 adjusted confidence values are preserved exactly:

\[
\frac13,
\qquad
\frac5{18},
\qquad
\frac{11}{54},
\qquad
\frac{11}{54}.
\]

The new exact-core penalty is zero. Core cardinality and redundancy are diagnostic metadata only.

## Fail-closed source binding

The runtime reissues and validates the accepted v0.87 certificate, including:

- acceptance, schema, and complete certificate digest,
- required and forbidden Boolean claims,
- every exact source record count,
- every source collection digest,
- canonical family order and sensor coordinates,
- candidate, history, and probe retention,
- review, dissent, and minority sets,
- source confidence values.

Mutation of the source certificate, exact-core records, confidence, authority boundaries, or unexpected claims blocks issuance.

## Authority boundary

MemoryOS v0.88 does not claim:

- uniqueness of minimum sensor cores in general,
- a universal classification of sensor families,
- a universal information lattice,
- an infinite-family limit,
- a continuum observation stack,
- physical measurement sufficiency,
- candidate ranking, pruning, or selection,
- decision commit or receipt issuance,
- plan synthesis, activation, or execution,
- source or persistent WORLD mutation,
- verification authority or truth authority.
