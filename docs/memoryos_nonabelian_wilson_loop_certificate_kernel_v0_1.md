# MemoryOS v0.72 — Non-Abelian Wilson-Loop Certificate Kernel

## Purpose

MemoryOS v0.72 replaces any proposed time-varying collusion-graph frontier with a finite non-Abelian gauge layer.

The layer represents local memory charts by finite frames, chart transitions by noncommuting link variables, multi-chart transport by ordered products, and global fusion consistency by conjugacy-class observables such as Wilson characters.

It remains future-only, read-only, and advisory.

## Literature grounding

The certificate binds the following primary-source directions:

1. `arXiv:2605.26697` — matrix-valued discrete transport, path ordering, and gauge-covariant non-Abelian holonomy estimation.
2. `arXiv:2602.02436` — gauge-equivariant learning of Wilson-loop observables while preserving gauge invariance.
3. `arXiv:2501.16955` — gauge-covariant attention and invariant contractions in lattice-gauge learning.
4. `arXiv:2603.00824` — local semantic charts, constructive gauge fixing, and holonomy as a global obstruction.
5. `arXiv:2604.12416` — non-Abelian gauge-equivariant machine learning in four-dimensional SU(3) lattice-gauge settings.

The MemoryOS implementation does not claim to reproduce the physical models of those papers. It imports only bounded mathematical principles: local frame covariance, path ordering, conjugacy-class invariance, Wilson observables, and constructive gauge fixing.

## Finite gauge group

The exact runtime group is

\[
S_3=\operatorname{Perm}(\{0,1,2\}).
\]

Permutations are stored as exact integer triples. The runtime also stores their exact `3 × 3` permutation matrices.

The canonical generators are

\[
s_{01}=(01),\qquad s_{12}=(12).
\]

They do not commute:

\[
s_{01}s_{12}\ne s_{12}s_{01}.
\]

No floating-point matrix arithmetic is used.

## Non-Abelian connection

For three charts `a`, `b`, and `c`, a connection is

\[
U=(U_{ab},U_{bc},U_{ca})\in S_3^3.
\]

A local frame choice is

\[
g=(g_a,g_b,g_c)\in S_3^3.
\]

The link transformation is

\[
U'_{ij}=g_i^{-1}U_{ij}g_j.
\]

Unlike the Abelian v0.71 layer, multiplication order is semantically significant.

## Path-ordered transport

Transport along `a → b → c` is

\[
T_{abc}=U_{ab}U_{bc}.
\]

The reversed product is

\[
T_{cba}=U_{bc}U_{ab}.
\]

For the canonical non-Abelian profile,

\[
U_{ab}=s_{01},\qquad U_{bc}=s_{12},\qquad U_{ca}=e,
\]

and therefore

\[
T_{abc}=(012),\qquad T_{cba}=(021).
\]

The commutator is nontrivial.

## Holonomy covariance

The ordered Wilson-loop holonomy is

\[
H(U)=U_{ab}U_{bc}U_{ca}.
\]

Lean proves

\[
H(U^g)=g_a^{-1}H(U)g_a.
\]

The holonomy representative is therefore not generally gauge invariant. It is gauge covariant and its conjugacy class is gauge invariant.

The canonical non-Abelian profile has

\[
H(U)=(012),
\]

while the selected local frame change produces

\[
H(U^g)=(021).
\]

These representatives differ but belong to the same conjugacy class and both have order three.

## Wilson class functions

A class function is an observable `χ` satisfying

\[
\chi(g^{-1}hg)=\chi(h).
\]

The Wilson observable is

\[
W_\chi(U)=\chi(H(U)).
\]

Lean proves

\[
W_\chi(U^g)=W_\chi(U)
\]

for every class function.

The runtime uses the trace of the three-dimensional permutation representation:

\[
\chi_{\mathrm{perm}}(h)=\#\{i:h(i)=i\}.
\]

It exhaustively verifies conjugacy invariance for all `6 × 6` pairs of `S3` elements and frame changes.

Canonical values:

- identity holonomy: trace `3`, normalized character `1`;
- three-cycle holonomy: trace `0`, normalized character `0`.

## Constructive non-Abelian tree gauge

The tree gauge is

\[
g_a=e,\qquad
 g_b=U_{ab}^{-1},\qquad
 g_c=(U_{ab}U_{bc})^{-1}.
\]

Lean proves

\[
U'_{ab}=e,\qquad U'_{bc}=e,\qquad U'_{ca}=H(U).
\]

Thus the tree links are removed without changing or deleting source records. The only residual link is the ordered holonomy.

## Multi-chart memory fusion

Fusion uses the frame-independent signature

\[
\mathcal F(U)=
(\operatorname{ConjClass}(H(U)),\chi_{\mathrm{perm}}(H(U)),\operatorname{ord}(H(U))).
\]

Canonical signatures:

- flat profile: `([1,1,1], 3, 1)`;
- non-Abelian profile: `([3], 0, 3)`.

A nontrivial signature emits an advisory review flag. It does not rank, prune, or select candidates.

## Gauge-adjusted confidence

The inherited v0.71 confidence is

\[
C_0=\frac23.
\]

The bounded Wilson-deficit penalty is

\[
P_W(U)=\frac{3-\chi_{\mathrm{perm}}(H(U))}{18}.
\]

The adjusted confidence is

\[
C_W(U)=C_0-P_W(U).
\]

Canonical values:

- flat profile: `P_W=0`, `C_W=2/3`;
- non-Abelian profile: `P_W=1/6`, `C_W=1/2`.

The penalty depends only on a conjugacy-class observable. No local link component is used as truth.

This penalty is a finite MemoryOS certificate convention. It is not a Bayesian posterior, a physical action, or a universal statistical optimum.

## Exact runtime ledgers

- literature records: `5`
- local memory charts: `3`
- non-Abelian gauge frames: `3`
- link records: `6`
- transformed link records: `6`
- path-ordered transport records: `4`
- commutator records: `2`
- holonomy records: `2`
- conjugacy-class records: `2`
- Wilson-character records: `2`
- non-Abelian tree-gauge records: `6`
- multi-chart fusion records: `2`
- gauge-adjusted confidence records: `2`
- full-rank transport records: `8`
- singular atomic records: `4`
- rank-one source boundaries: `3`

## Fail-closed checks

The checker rejects:

- v0.71 source-certificate or collection-digest tampering;
- modified path ordering;
- false transformed holonomy;
- false Wilson trace;
- modified confidence adjustment;
- local-link truth claims;
- physical SU(3) or continuum-bundle claims;
- candidate selection or execution authority;
- unexpected claims.

## Authority boundary

The layer does not:

- rank, prune, or select candidates;
- synthesize plans;
- commit decisions or issue decision receipts;
- activate tools or execute actions;
- delete source records during gauge fixing;
- mutate DecisionOS or persistent WORLD state;
- claim verification authority or truth authority.

## Formal root

`formal/KuuOSMemoryOSV0_72.lean`

## Runtime root

`runtime/kuuos_memoryos_nonabelian_wilson_loop_certificate_kernel_v0_1.py`

## Checker

`scripts/check_planos_memoryos_nonabelian_wilson_loop_certificate_kernel_v0_1.py`
