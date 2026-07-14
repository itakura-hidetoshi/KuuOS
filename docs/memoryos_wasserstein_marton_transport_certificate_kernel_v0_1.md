# MemoryOS v0.62 — finite path Wasserstein transport, Pearson information, and Marton coupling

## Scope

MemoryOS v0.62 extends the three-state reversible Markov semigroup carried by MemoryOS v0.58–v0.61. It adds an exact finite path-metric transport package:

- the three-point \(W_1\) formula on `early — middle — late`;
- explicit one-step coupling witnesses for every unordered pair of kernel rows;
- Dobrushin \(W_1\) contraction coefficient \(3/4\);
- coarse Ricci curvature \(1/4\);
- a sharp Pearson transport-information inequality;
- exact finite Marton state-pair and influence profiles;
- full-rank transport commutation and singular-measure retention.

The package is future-only, read-only, and advisory. It does not rank, prune, or select candidates; commit decisions; synthesize plans; activate or execute actions; mutate source or WORLD state; claim verification; or grant truth authority.

## Three-point path Wasserstein formula

On the ordered path with distances

\[
d(\mathrm{early},\mathrm{middle})=1,\qquad
d(\mathrm{middle},\mathrm{late})=1,\qquad
d(\mathrm{early},\mathrm{late})=2,
\]

the finite line formula is

\[
W_1(p,q)=|p_0-q_0|+|(p_0+p_1)-(q_0+q_1)|.
\]

For probability-mode coordinates \((a,b)\), where the centered masses are

\[
(a+b,\,-2b,\,-a+b),
\]

this becomes

\[
W_1(a,b)=|a+b|+|a-b|.
\]

Lean proves the associated quadratic transport-information inequality

\[
W_1(a,b)^2\le \frac23\chi^2(a,b),\qquad
\chi^2(a,b)=6a^2+18b^2.
\]

The constant \(2/3\) is sharp on the slow antisymmetric mode \(b=0\).

This is a Pearson-information transport inequality. v0.62 does not rename it as a KL \(T_1\) theorem.

## Exact one-step coupling witnesses

For

\[
K=
\begin{pmatrix}
3/4&1/4&0\\
1/4&1/2&1/4\\
0&1/4&3/4
\end{pmatrix},
\]

the runtime emits an explicit nonnegative coupling matrix for each unordered pair of rows, verifies both marginals, and computes its path cost.

The resulting exact row distances are

\[
W_1(K_{\mathrm{early}},K_{\mathrm{middle}})=\frac34,
\]

\[
W_1(K_{\mathrm{middle}},K_{\mathrm{late}})=\frac34,
\]

\[
W_1(K_{\mathrm{early}},K_{\mathrm{late}})=\frac32.
\]

Thus

\[
W_1(K_i,K_j)=\frac34\,d(i,j)
\]

for all state pairs. The Dobrushin transport coefficient is \(3/4\), and the corresponding finite coarse Ricci curvature is

\[
1-\frac34=\frac14.
\]

## Mode and semigroup contraction

The slow and fast modes evolve as

\[
a\mapsto \frac34 a,\qquad b\mapsto \frac14 b.
\]

Lean proves directly from the absolute-value formula that

\[
W_1\!\left(\frac34a,\frac14b\right)\le \frac34 W_1(a,b).
\]

Iteration gives

\[
W_1(K^n p,K^n q)\le\left(\frac34\right)^n W_1(p,q).
\]

The slow mode saturates the coefficient.

## Reference profiles

For each of the two reference distributions,

\[
W_1(P_n,\pi)=W_1(Q_n,\pi)=\frac3{10}\left(\frac34\right)^n.
\]

The Pearson information profile from v0.61 is

\[
\chi^2_n=\frac{27}{200}\left(\frac9{16}\right)^n.
\]

Hence every reference record satisfies the exact equality

\[
W_1(P_n,\pi)^2=\frac23\chi^2_n.
\]

The pairwise reference distance is

\[
W_1(P_n,Q_n)=\frac35\left(\frac34\right)^n.
\]

## Marton coupling profiles

For each unordered state pair, v0.62 records the exact finite profile

\[
W_1(K^n(i,\cdot),K^n(j,\cdot))=
\left(\frac34\right)^n d(i,j),\qquad 0\le n\le10.
\]

Lean also proves an abstract reusable theorem: if a coupling transport ledger satisfies

\[
T_{n+1}\le\frac34T_n,
\]

then

\[
T_n\le\left(\frac34\right)^nT_0.
\]

Any mismatch probability or 1-Lipschitz observable expectation gap bounded by that transport ledger inherits the same geometric bound. This is the precise finite Marton coupling statement made by v0.62; it is not presented as a general path-space Gaussian concentration theorem.

The finite influence recursion is

\[
I_0=0,\qquad I_{n+1}=1+\frac34I_n,
\]

with closed form

\[
I_n=4\left(1-\left(\frac34\right)^n\right)<4.
\]

The runtime also records the exact finite variance proxy \(\sum_{k=1}^n I_k^2\) for horizons zero through ten.

## Exact threshold witnesses

Each threshold record retains the immediately preceding insufficient value.

| profile | threshold | first certified time |
|---|---:|---:|
| reference to stationarity | \(1/10\) | 4 |
| reference to stationarity | \(1/20\) | 7 |
| reference pair | \(1/10\) | 7 |
| reference pair | \(1/20\) | 9 |
| adjacent-state Marton profile | \(1/4\) | 5 |
| endpoint-state Marton profile | \(1/4\) | 8 |

## Source binding and fail-closed behavior

The runtime independently validates and binds:

- the accepted MemoryOS v0.61 certificate;
- the v0.61 integrated-curvature mode digest;
- the functional-inequality hierarchy digest;
- the reference hierarchy digest;
- the finite concentration profile and threshold digests;
- all full-rank and singular transport records;
- all DecisionOS candidate identifiers;
- both PlanOS history identifiers;
- all nine quotient-coordinate probes;
- relational-frontier, required-review, dissent, and minority-protection sets.

Altered source curvature records, false Dobrushin claims, changed threshold times, source substitution, unexpected claims, and forbidden authority claims are rejected fail-closed.

## Runtime counts

- kernel-row coupling records: 3
- Pearson transport-information mode records: 2
- reference-to-stationarity Wasserstein records: 22
- reference-pair Wasserstein records: 11
- Marton state-pair records: 33
- Marton influence records: 11
- Wasserstein threshold records: 6
- full-rank transport records: 8
- singular atomic transport records: 4
- rank-one source boundaries: 3

## Transport and singular boundaries

Across four full-rank quotient-metric transitions and both reference distributions, the Pearson transport inequality, Wasserstein contraction, and Marton profile commute with retained mass-level evidence, producing eight records.

Across two full-rank-to-rank-one transitions and both reference distributions, Wasserstein and Marton evidence remains a singular atomic ledger, producing four records. No two-dimensional target density or lost antisymmetric information is reconstructed.

## Files

- `formal/KUOS/OpenHorizon/MemoryOSWassersteinMartonTransportV0_62.lean`
- `formal/KuuOSMemoryOSV0_62.lean`
- `runtime/kuuos_memoryos_wasserstein_marton_transport_certificate_kernel_v0_1.py`
- `scripts/check_planos_memoryos_wasserstein_marton_transport_certificate_kernel_v0_1.py`
- `manifests/kuuos_memoryos_wasserstein_marton_transport_certificate_kernel_v0_1.json`
- `runtime/kuuos_current_check.py`
