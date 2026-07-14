# MemoryOS v0.56: exact f-divergence transport and data-processing contraction

MemoryOS v0.56 extends the v0.55 relative-entropy layer to an exact finite-support
`f`-divergence transport certificate and a deterministic data-processing
contraction witness.

## Source distributions

The retained quotient-coordinate probes carry

\[
P_i=\frac{i}{45},\qquad Q_i=\frac{10-i}{45},
\qquad i=1,\ldots,9.
\]

No probe, candidate, history, dissent record, or minority-protection record is
removed.

## Generic full-rank transport

For an arbitrary generator \(f\), define the density contribution

\[
I_f(p,q,V)=q\,f(p/q)\,V.
\]

On a full-rank quotient-metric transition,

\[
\rho(c\to d)=\frac{\det K(c)}{\det K(d)},\qquad
J(c\to d)=\frac{\det K(d)}{\det K(c)},\qquad
\rho J=1.
\]

Both densities receive the same factor \(\rho\), so the likelihood ratio is
unchanged. Therefore

\[
I_f(p\rho,q\rho,VJ)=I_f(p,q,V).
\]

The Lean layer proves this for an arbitrary real-valued generator and for a
finite support sum.

## Exact generator catalog

The executable certificate evaluates three rational generators:

\[
D_{\mathrm P}(P\|Q)=\sum_i\frac{(P_i-Q_i)^2}{Q_i},
\]

\[
D_{\mathrm N}(P\|Q)=\sum_i\frac{(P_i-Q_i)^2}{P_i},
\]

\[
D_{\triangle}(P,Q)=\sum_i\frac{(P_i-Q_i)^2}{P_i+Q_i}.
\]

All per-probe terms and all full-rank transported terms are exact rationals.

## Deterministic coarse-graining channel

The nine probes are mapped to three bins:

- early: probes 1–3
- middle: probes 4–6
- late: probes 7–9

The coarse masses are

\[
P^\sharp=\left(\frac{2}{15},\frac13,\frac{8}{15}\right),
\qquad
Q^\sharp=\left(\frac{8}{15},\frac13,\frac{2}{15}\right).
\]

Reference contractions are

\[
D_{\mathrm P}^{\rm fine}=\frac{2593}{1134},\qquad
D_{\mathrm P}^{\rm coarse}=\frac32,\qquad
\Delta_{\mathrm P}=\frac{446}{567},
\]

\[
D_{\mathrm N}^{\rm fine}=\frac{2593}{1134},\qquad
D_{\mathrm N}^{\rm coarse}=\frac32,\qquad
\Delta_{\mathrm N}=\frac{446}{567},
\]

\[
D_{\triangle}^{\rm fine}=\frac{8}{15},\qquad
D_{\triangle}^{\rm coarse}=\frac{12}{25},\qquad
\Delta_{\triangle}=\frac{4}{75}.
\]

## Pearson completed-square theorem

For two atoms, Lean proves

\[
\frac{(p_1-q_1)^2}{q_1}
+\frac{(p_2-q_2)^2}{q_2}
-\frac{((p_1+p_2)-(q_1+q_2))^2}{q_1+q_2}
=
\frac{\left(q_2(p_1-q_1)-q_1(p_2-q_2)\right)^2}
{q_1q_2(q_1+q_2)}.
\]

For positive \(q_1,q_2\), the right-hand side is nonnegative, yielding exact
data-processing contraction under pairwise merging. Six runtime merge
witnesses telescope to the total Pearson gap \(446/567\).

## Transport/channel commutation

For each of the four invertible full-rank transitions and each generator, the
certificate checks that:

- the fine divergence is transport invariant;
- the coarse divergence is transport invariant;
- the contraction gap is transport invariant;
- applying transport before or after coarse-graining gives the same ledger.

## Singular boundary

A full-rank-to-rank-one transition emits no two-dimensional target
`f`-divergence density. The exact atomic contributions are retained as singular
measure records. A rank-one source does not reconstruct lost two-dimensional
density, Jacobian, or antisymmetric information.

## Fail-closed binding

The runtime independently validates and binds the accepted v0.55 certificate,
its relative-entropy transport and cocycle digests, an independently supplied
accepted v0.54 certificate, and the v0.54 density-transport digest. Altered
source masses, transport factors, ledgers, contraction gaps, singular records,
or authority claims are rejected.

## Boundary

The certificate is future-only, read-only, and advisory. It grants no candidate
ranking, pruning, selection, decision commit, plan synthesis, activation,
execution, source mutation, WORLD mutation, verification claim, or truth
authority.
