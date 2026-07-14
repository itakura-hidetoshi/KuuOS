# MemoryOS v0.55 — Relative entropy transport and singular Lebesgue decomposition

MemoryOS v0.55 extends the exact quotient-metric density transport of v0.54 with an executable relative-entropy layer and an explicit singular/absolutely-continuous measure decomposition.

## Reference probability pair

The nine retained quotient-coordinate probes carry two non-collapsed finite-support probability measures:

\[
P_i=\frac{i}{45},
\qquad
Q_i=\frac{10-i}{45},
\qquad i=1,\ldots,9.
\]

Both have total mass one and positive support on every probe. Their exact likelihood ratios range from

\[
\frac{P_1}{Q_1}=\frac19
\]

through the central ratio \(P_5/Q_5=1\), to

\[
\frac{P_9}{Q_9}=9.
\]

The runtime does not approximate logarithms. It retains each KL contribution as an exact symbolic pair

\[
\left(P_i,\frac{P_i}{Q_i}\right)
\]

representing \(P_i\log(P_i/Q_i)\). Reverse-KL terms retain the corresponding pair \((Q_i,Q_i/P_i)\).

## Full-rank transport

For an invertible quotient-metric transition \(c\to d\), v0.54 provides

\[
\rho(c\to d)=\frac{\det K(c)}{\det K(d)},
\qquad
J(c\to d)=\frac{\det K(d)}{\det K(c)},
\qquad
\rho J=1.
\]

Both densities are multiplied by the same \(\rho\), while coordinate-cell volume is multiplied by \(J\). Therefore

\[
\frac{P_i\rho}{Q_i\rho}=\frac{P_i}{Q_i},
\]

and

\[
(P_i\rho)\log\!\left(\frac{P_i\rho}{Q_i\rho}\right)J
=
P_i\log\!\left(\frac{P_i}{Q_i}\right).
\]

Thus forward KL, reverse KL, every probe contribution, and the complete finite-support symbolic ledger are invariant under all four invertible full-rank transitions.

The Lean layer proves the corresponding theorem with `Real.log`, not merely the symbolic runtime representation.

## Relative-entropy cocycle

All eight full-rank three-step paths inherit the Radon–Nikodym cocycle from v0.54. The relative-entropy ledger is invariant on each leg and therefore invariant under composition. The two nontrivial round trips preserve both forward and reverse relative entropy exactly.

## Singular Lebesgue decomposition

For a full-rank-to-rank-one transition, the two-dimensional target Jacobian is zero and no two-dimensional density is emitted. For every probe and for both measures,

\[
P_i=P_i^{ac}+P_i^s=0+P_i,
\]

\[
Q_i=Q_i^{ac}+Q_i^s=0+Q_i.
\]

The complete mass is retained in the singular component. Since the atomic \(P_i\) and \(Q_i\) masses remain visible, the exact symbolic relative-entropy ledger is retained at the singular-measure level, while no two-dimensional density representation is claimed.

For a rank-one source, v0.55 does not reconstruct a lost two-dimensional density, Jacobian, or antisymmetric component.

## Runtime certificate counts

- directed transitions: 9
- full-rank relative-entropy transitions: 4
- full-rank probe relative-entropy records: 36
- singular Lebesgue-decomposition transitions: 2
- singular probe decomposition records: 18
- singular atomic relative-entropy records: 18
- rank-one source boundaries: 3
- relative-entropy cocycle records: 27
- active full-rank entropy cocycles: 8
- nontrivial entropy-preserving round trips: 2

## Fail-closed source binding

The certificate independently validates and binds:

- accepted MemoryOS v0.54 certificate
- v0.54 density-transport digest
- v0.54 Radon–Nikodym cocycle digest
- independently supplied accepted MemoryOS v0.53 certificate
- v0.53 Jacobian digest
- v0.53 mode-composition digest
- all four DecisionOS candidate IDs
- both PlanOS history IDs
- all nine quotient-coordinate probe IDs
- relational-frontier, required-review, dissent, and minority-protection sets

It rejects source substitution, digest mismatch, altered density multipliers, altered Jacobians, modified singular records, changed symbolic KL terms, false two-dimensional recovery claims, and all forbidden authority promotions.

## Boundary

This layer is future-only, read-only, and advisory. It does not perform candidate ranking, pruning, selection, decision commit, decision receipt issuance, plan synthesis, activation, execution, source mutation, WORLD mutation, verification-result claims, or truth-authority assignment.
