# MemoryOS v0.60 — modified log-Sobolev entropy decay, Hellinger/separation profiles, and finite cutoff thresholds

## Scope

MemoryOS v0.60 extends the reversible three-state Markov semigroup of v0.58 and the logarithmic Sobolev/mixing package of v0.59. It proves an actual logarithmic entropy contraction from an exact two-step Doeblin decomposition, then records finite Hellinger, separation, and KL-envelope profiles.

The layer is future-only, read-only, and advisory. It does not rank, prune, or select candidates; commit decisions; synthesize plans; activate or execute actions; mutate source or WORLD state; claim verification; or grant truth authority.

## Exact two-step Doeblin decomposition

For

\[
K=\begin{pmatrix}
3/4&1/4&0\\
1/4&1/2&1/4\\
0&1/4&3/4
\end{pmatrix},
\]

v0.60 computes

\[
K^2=\begin{pmatrix}
5/8&5/16&1/16\\
5/16&3/8&5/16\\
1/16&5/16&5/8
\end{pmatrix}.
\]

Let `Pi` be the stationary projection kernel with every row equal to `(1/3,1/3,1/3)`. Then

\[
K^2=\frac3{16}\Pi+\frac{13}{16}R,
\]

where

\[
R=\begin{pmatrix}
9/13&4/13&0\\
4/13&5/13&4/13\\
0&4/13&9/13
\end{pmatrix}.
\]

The runtime checks all nine entries and proves that `R` is row-stochastic, column-stochastic, and symmetric.

## Actual modified logarithmic entropy contraction

The Lean package calls Mathlib's `InformationTheory.convexOn_klFun`. It proves finite Jensen data processing for the residual kernel `R` and separately proves that mixing a nonnegative likelihood ratio with the stationary value `1` contracts `klFun` by the residual weight.

Combining both steps gives

\[
D(pK^2\Vert\pi)\le \frac{13}{16}D(p\Vert\pi).
\]

For `m` two-step blocks,

\[
D(pK^{2m}\Vert\pi)\le
\left(\frac{13}{16}\right)^mD(p\Vert\pi).
\]

This is a valid finite modified-entropy contraction. v0.60 does not claim that `13/16` is a globally optimal or convention-independent modified log-Sobolev coefficient.

## Hellinger profile

For uniform likelihood ratios `r0,r1,r2`, define

\[
H^2=\frac{(\sqrt{r_0}-1)^2+(\sqrt{r_1}-1)^2+(\sqrt{r_2}-1)^2}{6}.
\]

Lean proves

\[
H^2\le \frac12\chi^2.
\]

Under likelihood normalization it also proves the affinity identity

\[
H^2=1-\frac{\sqrt{r_0}+\sqrt{r_1}+\sqrt{r_2}}3.
\]

For the reference slow-mode likelihood vector `(1-u,1,1+u)`,

\[
H^2\le \frac{u^2}{3},
\qquad
u_n=\frac9{20}\left(\frac34\right)^n.
\]

The runtime retains symbolic `Real.sqrt` expressions rather than replacing them with floating-point approximations.

## Separation profiles

For likelihood ratios, separation from stationarity is

\[
1-\min(r_0,r_1,r_2).
\]

For the reference distributions,

\[
\operatorname{sep}_{ref}(n)=
\frac9{20}\left(\frac34\right)^n.
\]

For the worst initial state, exact kernel powers give

\[
\operatorname{sep}_{worst}(n)=
\frac32\left(\frac34\right)^n-
\frac12\left(\frac14\right)^n.
\]

The runtime checks the spectral formula against the minimum entry of every exact kernel power for times `0` through `10`.

## Finite threshold witnesses

Each certificate includes both the first certified index and the immediately preceding insufficient value.

| profile | threshold | certified | previous insufficient |
|---|---:|---:|---:|
| worst-case separation | `1/4` | `n=7` | `n=6` |
| worst-case separation | `1/8` | `n=9` | `n=8` |
| reference separation | `1/20` | `n=8` | `n=7` |
| reference Hellinger, rational envelope | `1/20` | `n=6` | `n=5` |
| worst-case KL envelope | `1/4` | block `11`, physical time `22` | block `10` |

These are finite exact threshold witnesses. They are not an assertion of an asymptotic cutoff phenomenon.

## Source binding and failure closure

The runtime independently validates and binds:

- the accepted MemoryOS v0.59 certificate;
- all v0.59 log-Sobolev, KL-envelope, hypercontractive, TV, mixing, transport, and singular digests;
- an independently supplied accepted MemoryOS v0.58 certificate;
- the v0.58 entropy-trajectory and entropy-production digests;
- all DecisionOS candidate identifiers;
- both PlanOS history identifiers;
- all nine quotient-coordinate probe identifiers;
- relational-frontier, required-review, dissent, and minority-protection sets.

Altered source records, false Doeblin weights, changed finite thresholds, source substitution, and forbidden authority claims are rejected fail-closed.

## Runtime counts

- two-step Doeblin records: 1
- two-step decomposition records: 9
- modified entropy block records: 12
- symbolic reference KL block records: 24
- reference Hellinger profile records: 22
- reference separation profile records: 22
- worst-case separation profile records: 11
- cutoff threshold records: 5
- full-rank transport profile records: 8
- singular atomic profile records: 4
- rank-one source boundaries: 3

## Transport and singular boundaries

Across four full-rank quotient-metric transitions and both reference distributions, modified entropy, Hellinger, and separation profiles commute with the retained mass-level transport, producing eight records.

Across two full-rank-to-rank-one transitions and both reference distributions, all three ledgers remain singular atomic evidence, producing four records. No two-dimensional target density or lost antisymmetric information is reconstructed.

## Files

- `formal/KUOS/OpenHorizon/MemoryOSModifiedLogSobolevHellingerSeparationV0_60.lean`
- `formal/KuuOSMemoryOSV0_60.lean`
- `runtime/kuuos_memoryos_modified_log_sobolev_hellinger_separation_certificate_kernel_v0_1.py`
- `scripts/check_planos_memoryos_modified_log_sobolev_hellinger_separation_certificate_kernel_v0_1.py`
- `manifests/kuuos_memoryos_modified_log_sobolev_hellinger_separation_certificate_kernel_v0_1.json`
- `runtime/kuuos_current_check.py`
