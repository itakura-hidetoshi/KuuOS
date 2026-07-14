# MemoryOS v0.61 — integrated Bakry–Émery curvature, functional inequalities, and concentration

## Scope

MemoryOS v0.61 extends the reversible three-state Markov semigroup and the v0.60 modified-entropy/Hellinger/separation package with an actual integrated Bakry–Émery curvature calculation, a formally connected functional-inequality hierarchy, and finite exact concentration profiles.

The layer is future-only, read-only, and advisory. It does not rank, prune, or select candidates; commit decisions; synthesize plans; activate or execute actions; mutate source or WORLD state; claim verification; or grant truth authority.

## Generator modes

For the reversible kernel

\[
K=\begin{pmatrix}
3/4&1/4&0\\
1/4&1/2&1/4\\
0&1/4&3/4
\end{pmatrix},
\]

the nonstationary eigenvalues are \(3/4\) and \(1/4\). For \(A=I-K\), the corresponding generator gaps are

\[
\lambda_{\rm slow}=1/4,\qquad
\lambda_{\rm fast}=3/4.
\]

In slow/fast probability-mode coordinates \((a,b)\), v0.61 uses

\[
\chi^2(a,b)=6a^2+18b^2,
\]

\[
\mathcal E(a,b)=\frac32a^2+\frac{27}{2}b^2,
\]

and defines the integrated carré-du-champ iteration

\[
\Gamma_2^{\rm int}(a,b)
=\langle Af,Af\rangle_\pi
=\frac38a^2+\frac{81}{8}b^2.
\]

This is explicitly an integrated finite-state Bakry–Émery statement; no unsupported pointwise curvature claim is made.

## Curvature lower bound

Lean proves

\[
\Gamma_2^{\rm int}(a,b)\ge
\frac14\mathcal E(a,b),
\]

with exact gap

\[
\Gamma_2^{\rm int}
-\frac14\mathcal E
=\frac{27}{4}b^2.
\]

The curvature lower bound \(1/4\) is sharp on the slow eigenspace \(b=0\).

## Functional-inequality hierarchy

The v0.59 logarithmic theorem and the new curvature calculation are connected into

\[
D_{\rm KL}
\le \chi^2
\le 4\mathcal E
\le 16\Gamma_2^{\rm int}.
\]

The Poincaré inequality has exact gap

\[
4\mathcal E-\chi^2=36b^2,
\]

and is also sharp on the slow eigenspace. For the reference \(P,Q\) trajectories, every timepoint is pure slow mode, so

\[
\chi^2=4\mathcal E=16\Gamma_2^{\rm int}
\]

holds exactly.

## Finite three-state concentration

For a threshold \(t\ge0\), v0.61 defines an exact indicator for each of the three likelihood deviations and the uniform tail mass

\[
\operatorname{Tail}_t(x,y,z)
=\frac{1_{\{|x|\ge t\}}+
1_{\{|y|\ge t\}}+
1_{\{|z|\ge t\}}}{3}.
\]

Lean proves the finite Chebyshev inequality

\[
\operatorname{Tail}_t(x,y,z)t^2
\le\frac{x^2+y^2+z^2}{3}.
\]

For the Markov mode sequence it then proves

\[
\operatorname{Tail}_t(K^n f)t^2
\le
\left(\frac9{16}\right)^n\chi^2(f).
\]

This is an actual tail-indicator theorem, not merely a variance label.

## Exact reference thresholds

The reference likelihood-deviation amplitude is

\[
u_n=\frac9{20}\left(\frac34\right)^n.
\]

For both reference distributions:

- threshold \(1/4\): tail mass is \(2/3\) through \(n=2\) and exactly \(0\) from \(n=3\);
- threshold \(1/8\): tail mass is \(2/3\) through \(n=4\) and exactly \(0\) from \(n=5\).

The runtime checks every profile time from \(0\) through \(8\), including the exact tail mass, the quadratic tail bound, and the sharp \(\chi^2\) decay envelope.

## Runtime counts

- integrated curvature mode records: 2
- functional-inequality hierarchy records: 1
- reference hierarchy profile records: 22
- concentration profile records: 36
- concentration threshold records: 4
- full-rank transport curvature/concentration records: 8
- singular atomic curvature/concentration records: 4
- rank-one source boundaries: 3

## Source binding

The runtime validates and binds the accepted MemoryOS v0.60 certificate, its Doeblin, modified-entropy, Hellinger, separation, and finite-threshold digests, all retained DecisionOS candidates, both PlanOS histories, all quotient-coordinate probes, and the review/dissent/minority sets.

Altered source profiles, false curvature coefficients, changed threshold times, source substitution, and forbidden authority claims are rejected fail-closed.

## Transport and singular boundaries

Across full-rank quotient-metric transitions, the integrated curvature ledger, functional hierarchy, and concentration profile commute with retained mass-level transport.

Across full-rank-to-rank-one transitions, these ledgers remain singular atomic evidence. No two-dimensional target density or lost antisymmetric information is reconstructed.

## Files

- `formal/KUOS/OpenHorizon/MemoryOSBakryEmeryConcentrationV0_61.lean`
- `formal/KuuOSMemoryOSV0_61.lean`
- `runtime/kuuos_memoryos_bakry_emery_concentration_certificate_kernel_v0_1.py`
- `scripts/check_planos_memoryos_bakry_emery_concentration_certificate_kernel_v0_1.py`
- `manifests/kuuos_memoryos_bakry_emery_concentration_certificate_kernel_v0_1.json`
- `runtime/kuuos_current_check.py`
