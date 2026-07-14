# MemoryOS v0.58 — reversible Markov semigroup, entropy production, and sharp SDPI

## Scope

MemoryOS v0.58 extends the exact rational stochastic channel introduced in v0.57 into a finite reversible discrete-time Markov semigroup. The layer is future-only, read-only, and advisory. It does not rank, prune, select, commit, synthesize, activate, execute, mutate source state, mutate WORLD state, claim verification, or grant truth authority.

## Source bindings

The certificate independently validates and binds:

- the accepted MemoryOS v0.57 stochastic-kernel and sufficiency certificate;
- the v0.57 stochastic-kernel digest;
- the v0.57 stochastic data-processing digest;
- the v0.57 tagged-split and recovery-kernel digests;
- an independently supplied accepted MemoryOS v0.56 certificate;
- the v0.56 transport, data-processing, and cocycle digests;
- all retained DecisionOS candidate identifiers;
- both PlanOS history identifiers;
- all nine quotient-coordinate probe identifiers;
- relational-frontier, required-review, dissent, and minority-protection sets.

Source substitution, changed exact masses, altered kernels, changed semigroup powers, false detailed balance, false entropy values, false SDPI coefficients, false density recovery, and forbidden authority claims are rejected fail-closed.

## Reversible three-state kernel

The state order is `early`, `middle`, `late`. The v0.57 kernel is

\[
K=
\begin{pmatrix}
3/4&1/4&0\\
1/4&1/2&1/4\\
0&1/4&3/4
\end{pmatrix}.
\]

Every row and every column sums to one. The matrix is symmetric, so the uniform distribution

\[
\pi=(1/3,1/3,1/3)
\]

is stationary and satisfies detailed balance

\[
\pi_iK_{ij}=\pi_jK_{ji}
\]

for all nine ordered state pairs.

## Exact semigroup

The runtime derives `K^0` through `K^4` using exact rational matrix multiplication. It records nine bounded semigroup compositions for `m,n ∈ {0,1,2}` and verifies

\[
K^mK^n=K^{m+n}.
\]

Reference powers include

\[
K^2=
\begin{pmatrix}
5/8&5/16&1/16\\
5/16&3/8&5/16\\
1/16&5/16&5/8
\end{pmatrix}
\]

and

\[
K^3=
\begin{pmatrix}
35/64&21/64&1/8\\
21/64&11/32&21/64\\
1/8&21/64&35/64
\end{pmatrix}.
\]

## Eigenmodes and spectral gap

The exact eigenmodes are:

- stationary mode `(1,1,1)` with eigenvalue `1`;
- antisymmetric slow mode `(1,0,-1)` with eigenvalue `3/4`;
- curvature fast mode `(1,-2,1)` with eigenvalue `1/4`.

Therefore the subdominant eigenvalue is `3/4`, the spectral gap is

\[
1-3/4=1/4,
\]

and the sharp chi-square strong data-processing coefficient is

\[
\eta=(3/4)^2=9/16.
\]

## Chi-square entropy and entropy production

For centered mode coordinates `(a,b)`, define

\[
\chi^2(a,b)=6a^2+18b^2.
\]

One Markov step maps

\[
(a,b)\mapsto(3a/4,b/4).
\]

Hence

\[
\chi^2_{t+1}=\frac{27}{8}a_t^2+\frac98 b_t^2
\]

and the exact entropy production is

\[
\chi^2_t-\chi^2_{t+1}
 =\frac{21}{8}a_t^2+\frac{135}{8}b_t^2\ge0.
\]

The Lean package proves the generic one-step inequality

\[
\chi^2_{t+1}\le\frac9{16}\chi^2_t,
\]

its sharpness on the slow mode, the exact mode semigroup, and the iterated bound

\[
\chi^2_n\le(9/16)^n\chi^2_0.
\]

## Reference trajectories

The v0.57 output distributions are

\[
P_0=(11/60,1/3,29/60),\qquad
Q_0=(29/60,1/3,11/60).
\]

Both are pure antisymmetric slow-mode perturbations of `π`. Their exact chi-square entropy trajectory is therefore sharp at every time:

| time | entropy | SDPI relation |
|---:|---:|---:|
| 0 | `27/200` | initial |
| 1 | `243/3200` | `(9/16) E₀` |
| 2 | `2187/51200` | `(9/16)² E₀` |
| 3 | `19683/819200` | `(9/16)³ E₀` |
| 4 | `177147/13107200` | `(9/16)⁴ E₀` |

The corresponding entropy-production increments are

- `189/3200`;
- `1701/51200`;
- `15309/819200`;
- `137781/13107200`.

## Transport and singular boundaries

For each of the four full-rank quotient-metric transitions and each reference distribution, the mass-level Markov semigroup entropy ledger is unchanged by Radon–Nikodym coordinate transport. This produces eight exact transport/semigroup commutation records.

For the two full-rank-to-rank-one transitions and both reference distributions, the five-time entropy ledger is retained as singular atomic evidence. No two-dimensional target density is emitted. Rank-one source states do not reconstruct lost density or antisymmetric information.

## Runtime counts

- Markov states: 3
- kernel entries: 9
- kernel-power records: 5
- semigroup-composition records: 9
- detailed-balance records: 9
- eigenmode records: 3
- distribution trajectories: 2
- entropy timepoints: 10
- entropy-production records: 8
- full-rank transport/semigroup records: 8
- singular atomic entropy records: 4
- rank-one source boundaries: 3

## Files

- `formal/KUOS/OpenHorizon/MemoryOSReversibleMarkovSemigroupEntropyProductionV0_58.lean`
- `formal/KuuOSMemoryOSV0_58.lean`
- `runtime/kuuos_memoryos_reversible_markov_semigroup_entropy_production_certificate_kernel_v0_1.py`
- `scripts/check_planos_memoryos_reversible_markov_semigroup_entropy_production_certificate_kernel_v0_1.py`
- `manifests/kuuos_memoryos_reversible_markov_semigroup_entropy_production_certificate_kernel_v0_1.json`
- `runtime/kuuos_current_check.py`
