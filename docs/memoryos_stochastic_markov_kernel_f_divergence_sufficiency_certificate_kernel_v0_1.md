# MemoryOS v0.57 — stochastic Markov-kernel f-divergence data processing and sufficiency

## Scope

MemoryOS v0.57 extends the exact finite-support `f`-divergence layer from deterministic coarse-graining to a rational stochastic Markov kernel. It also introduces an explicit sufficient stochastic channel with a recovery kernel, so strict contraction and equality can be represented in one fail-closed certificate.

The layer is future-only, read-only, and advisory. It does not rank, prune, select, commit, activate, execute, mutate WORLD state, or claim truth authority.

## Source distributions

The retained nine-probe distributions remain

\[
P_i=\frac{i}{45},\qquad Q_i=\frac{10-i}{45},\qquad i=1,\ldots,9.
\]

The three exact generators remain:

- Pearson chi-square: \((P-Q)^2/Q\)
- Neyman chi-square: \((P-Q)^2/P\)
- triangular discrimination: \((P-Q)^2/(P+Q)\)

## Stochastic Markov kernel

The v0.56 deterministic bins `early`, `middle`, and `late` are followed by the rational stochastic matrix

\[
M=
\begin{pmatrix}
3/4&1/4&0\\
1/4&1/2&1/4\\
0&1/4&3/4
\end{pmatrix}.
\]

Every row sums exactly to one. Every source probe remains represented through its deterministic-bin row; no probe is pruned.

The pushed-forward distributions are

\[
P'=(11/60,1/3,29/60),\qquad
Q'=(29/60,1/3,11/60).
\]

## Exact stochastic data processing

The exact reference values are:

| Generator | Fine | Deterministic coarse | Stochastic output | Fine-to-stochastic gap | Coarse-to-stochastic gap |
|---|---:|---:|---:|---:|---:|
| Pearson | 2593/1134 | 3/2 | 216/319 | 582223/361746 | 525/638 |
| Neyman | 2593/1134 | 3/2 | 216/319 | 582223/361746 | 525/638 |
| Triangular | 8/15 | 12/25 | 27/100 | 79/300 | 21/100 |

For all three generators,

\[
D_f(P'M,Q'M)<D_f(P^\sharp,Q^\sharp)<D_f(P,Q).
\]

The strict contraction proves that this reference stochastic kernel is not sufficient for the retained pair \((P,Q)\), assuming the ordinary data-processing inequality for any proposed recovery.

## Equality and sufficiency channel

A second stochastic channel maps every probe `i` to two tagged states:

\[
i\longmapsto (i,L)\text{ with probability }1/3,
\qquad
i\longmapsto(i,R)\text{ with probability }2/3.
\]

The tagged supports are disjoint across source probes. The recovery kernel maps both `(i,L)` and `(i,R)` deterministically back to `i`.

For an arbitrary generator `f`,

\[
q\alpha f\!\left(\frac{p\alpha}{q\alpha}\right)
+q(1-\alpha)f\!\left(\frac{p(1-\alpha)}{q(1-\alpha)}\right)
=qf(p/q),
\]

when the denominators are nonzero. Hence the tagged split preserves every source contribution exactly, and the recovery kernel reconstructs both `P` and `Q` exactly. This is an explicit finite sufficient statistic witness.

## Formal layer

Lean proves:

- finite summation of cellwise Jensen/data-processing witnesses;
- equality from forward data processing plus an exact recovery;
- impossibility of sufficiency under strict contraction;
- exact split contribution equality for an arbitrary real-valued generator;
- finite-support split equality;
- exact `1/3`–`2/3` split and mass recovery;
- exact rational stochastic output masses;
- exact Pearson, Neyman, and triangular stochastic contraction values;
- commutation of full-rank metric transport with the sufficient split equality.

## Transport and singular boundaries

For each of the four full-rank quotient-metric transports and each generator, the stochastic divergence and sufficient split divergence remain invariant after density scaling by the Radon–Nikodym multiplier and cell-volume scaling by the reciprocal Jacobian.

For the two full-rank-to-rank-one collapses, the stochastic output ledger is retained as a singular atomic measure. No two-dimensional target density is emitted. For the three rank-one source boundaries, no lost two-dimensional density or antisymmetric information is reconstructed.

## Runtime counts

- stochastic Markov rows: 9
- stochastic kernel entries: 27
- stochastic outputs: 3
- stochastic data-processing records: 3
- tagged split entries: 18
- tagged split outputs: 18
- recovery entries: 18
- sufficient probe-generator records: 27
- sufficient generator equality records: 3
- full-rank transport/Markov/sufficiency records: 12
- singular stochastic `f`-divergence records: 6
- rank-one source boundaries: 3

## Fail-closed bindings

The certificate independently validates and binds:

- accepted MemoryOS v0.56 certificate;
- v0.56 `f`-divergence transport digest;
- v0.56 data-processing digest;
- v0.56 `f`-divergence cocycle digest;
- independently supplied accepted MemoryOS v0.55 certificate;
- v0.55 relative-entropy transport and cocycle digests;
- all four DecisionOS candidate IDs;
- both PlanOS history IDs;
- all nine quotient-coordinate probes;
- relational-frontier, required-review, dissent, and minority-protection sets.

It rejects altered source certificates, generator totals, kernels, output masses, recovery rows, equality claims, singular records, and forbidden authority promotion.
