# MemoryOS v0.66 — continuous log-MGF convexity certificate kernel v0.1

## Scope

MemoryOS v0.66 extends the accepted finite-grid Legendre–Fenchel package from v0.65 with an actual differentiable three-state log-MGF layer.

The package is deliberately finite-state and exact at the algebraic boundary. It does not infer a general large-deviation principle from finite-state differentiability.

## Three-state partition functions

For a three-state observable

\[
f=(f_E,f_M,f_L),
\]

v0.66 defines

\[
Z_f(t)=e^{tf_E}+e^{tf_M}+e^{tf_L},
\]

\[
Z_f'(t)=f_Ee^{tf_E}+f_Me^{tf_M}+f_Le^{tf_L},
\]

and

\[
Z_f''(t)=f_E^2e^{tf_E}+f_M^2e^{tf_M}+f_L^2e^{tf_L}.
\]

The stationary MGF remains

\[
M_f(t)=Z_f(t)/3,
\]

and the log-MGF is

\[
\Lambda_f(t)=\log M_f(t).
\]

## Actual derivative package

The Lean package proves the derivatives of `partitionSum`, `partitionFirstMoment`, `stationaryMGF`, and `stationaryLogMGF` with `HasDerivAt`.

The tilted mean is

\[
\mu_f(t)=\frac{Z_f'(t)}{Z_f(t)},
\]

and Lean proves

\[
\Lambda_f'(t)=\mu_f(t).
\]

The tilted curvature is

\[
\kappa_f(t)=
\frac{Z_f''(t)Z_f(t)-Z_f'(t)^2}{Z_f(t)^2}.
\]

Lean also proves

\[
\mu_f'(t)=\kappa_f(t).
\]

## Pairwise-square curvature identity

The curvature numerator is rewritten exactly as

\[
Z_f''Z_f-(Z_f')^2
=
 e^{t(f_E+f_M)}(f_E-f_M)^2
+e^{t(f_E+f_L)}(f_E-f_L)^2
+e^{t(f_M+f_L)}(f_M-f_L)^2.
\]

Every term is nonnegative. Therefore

\[
\kappa_f(t)\ge 0
\]

for every real tilt.

This nonnegative second-derivative witness is passed to the actual Mathlib theorem

`convexOn_of_hasDerivWithinAt2_nonneg`

to prove that the stationary log-MGF is convex on the whole real line.

## Continuous Legendre stationarity

The v0.65 objective is retained:

\[
J_f(t,a)=ta-\Lambda_f(t).
\]

Lean proves

\[
J_f'(t,a)=a-\mu_f(t).
\]

Any global continuous optimizer, when supplied as an optimizer witness, is a local maximum. Fermat's theorem then gives the stationary equation

\[
\mu_f(t_*)=a.
\]

The package does not assert that such a global optimizer exists for every observable and threshold.

## Comparison with the finite grid

If a global continuous optimizer exists, its objective dominates the accepted v0.65 finite-grid rate. Consequently its exponential envelope is no larger than the finite-grid optimized envelope.

For the bounded interval `[0,4]`, v0.66 additionally proves that tilt `4` is an actual interval optimizer whenever the full support lies below the threshold. The four accepted tail-extinction profiles therefore retain the same boundary optimizer as v0.65.

## Runtime ledger

The exact-rational runtime records:

- 22 derivative and curvature profile records,
- 44 continuous stationarity input records,
- 44 finite-grid comparison records,
- 4 bounded-interval boundary optimizer records,
- 22 Marton continuous-optimizer input records,
- 8 full-rank transport records,
- 4 singular atomic records,
- 3 rank-one source-boundary records.

The runtime does not numerically evaluate `exp`, `log`, a transcendental optimizer, or a root of the stationary equation. It records rational support values, rational thresholds, symbolic partition terms, symbolic derivative equations, and formal theorem bindings.

## Source binding

The certificate validates and binds the accepted MemoryOS v0.65 certificate, including:

- finite tilt grid digest,
- finite Legendre-rate profile digest,
- explicit extinction optimizer digest,
- Marton optimizer input digest,
- full-rank and singular transport digests,
- retained DecisionOS candidate IDs,
- retained PlanOS history IDs,
- retained quotient-coordinate probe IDs,
- relational frontier and review visibility sets.

Any source substitution, digest change, profile support change, false optimizer claim, unexpected claim, or authority escalation is rejected fail-closed.

## Mathematical boundary

MemoryOS v0.66 proves finite three-state differentiability and convexity. It does not claim:

- existence of an unbounded nonnegative-tilt optimizer for every threshold,
- a closed-form transcendental optimizer,
- a Cramér theorem,
- a Gärtner–Ellis theorem,
- an asymptotic large-deviation principle,
- a path-space Gaussian theorem,
- recovery of a lost rank-one coordinate.

## Authority boundary

MemoryOS v0.66 is future-only, read-only, and advisory.

It does not rank, prune, or select candidates; commit decisions; issue decision receipts; synthesize plans; activate or execute actions; mutate the source certificate, DecisionOS, or persistent WORLD state; claim verification truth; or grant truth authority.
