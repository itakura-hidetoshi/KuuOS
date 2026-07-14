# MemoryOS gauge connection, holonomy, and covariant consistency certificate kernel v0.1

## Frontier

This artifact advances MemoryOS from v0.70 correlation and collusion certificates to
MemoryOS v0.71 gauge-covariant memory consistency.

The previous proposal of a time-varying collusion graph is intentionally replaced.
The new bounded model uses:

1. local memory charts,
2. chart-dependent frames,
3. exact-rational gauge connections on chart overlaps,
4. gauge-invariant holonomy and curvature,
5. covariant consistency residuals,
6. a gauge-invariant confidence adjustment.

The implementation is a finite additive Abelian gauge theory over `ℚ`. It does not
claim a physical electromagnetic field, a continuum principal bundle, or a
non-Abelian gauge theory.

## Literature grounding

The construction binds the following primary sources:

- Javidnia, *A Gauge Theory of Superposition: Toward a Sheaf-Theoretic Atlas of
  Neural Representations* (`arXiv:2603.00824`, 2026). This motivates local semantic
  charts, gauge fixing, and holonomy as an obstruction to globally consistent
  representation.
- Rayat, Li, and Chern, *Gauge-Equivariant Graph Neural Networks for Lattice Gauge
  Theories* (`arXiv:2604.20797`, 2026). Only the principles of local gauge symmetry,
  covariant transport, and loop observables are used; MemoryOS v0.71 is not a graph
  neural network.
- Bruzzese, *A Gauge-Covariant Theoretical Framework for Non-Abelian Holonomy
  Estimation and Feed-Forward Correction in Time-Bin Photonic Qudits*
  (`arXiv:2605.26697`, 2026). This motivates frame-covariant discrete transport and
  holonomy estimation. The MemoryOS implementation remains Abelian and exact-rational.
- Huang et al., *Learning Chern Numbers of Topological Insulators with Gauge
  Equivariant Neural Networks* (`arXiv:2502.15376`, 2025). This motivates separating
  frame-dependent representations from gauge-invariant outputs.
- Magnot, *A mathematical bridge between discretized gauge theories in quantum
  physics and approximate reasoning in pairwise comparisons* (`arXiv:1710.11080`,
  2017). This provides a foundational precedent for using simplex holonomy to
  represent inconsistency in pairwise information.

These papers motivate the construction but do not prove the KuuOS Lean theorems.

## Local memory atlas

Three local memory charts are denoted `a`, `b`, and `c`. A local section is

```text
s = (s_a, s_b, s_c).
```

An exact-rational additive connection is

```text
A = (A_ab, A_bc, A_ca).
```

A local frame change is

```text
g = (g_a, g_b, g_c).
```

The gauge transformations are

```text
s_i'   = s_i + g_i
A_ij'  = A_ij + g_j - g_i.
```

The connection values are frame dependent. They are not interpreted as direct
truth scores.

## Holonomy and curvature

The triangular holonomy is

```text
H(A) = A_ab + A_bc + A_ca.
```

All gauge terms cancel around the closed loop, so

```text
H(A^g) = H(A).
```

The curvature energy is the exact rational quantity

```text
E(A) = H(A)^2.
```

It is nonnegative and gauge invariant. The connection is flat exactly when
`H(A) = 0`, equivalently `E(A) = 0`.

The canonical profiles are:

| profile | A_ab | A_bc | A_ca | holonomy |
|---|---:|---:|---:|---:|
| flat | `1/3` | `1/4` | `-7/12` | `0` |
| curved | `1/2` | `1/3` | `-1/4` | `7/12` |

At threshold `1/2`, the flat profile is not flagged and the curved profile is
flagged. The flag is advisory and gauge invariant.

## Covariant consistency

The overlap residual on `a -> b` is

```text
D_ab(A,s) = s_b - s_a - A_ab.
```

Analogous definitions are used for `b -> c` and `c -> a`. If section and
connection transform together, every residual is unchanged:

```text
D_ij(A^g, s^g) = D_ij(A,s).
```

Memory consistency is therefore evaluated independently of arbitrary local chart
coordinates.

## Gauge fixing

A constructive tree gauge is

```text
g_a = 0
g_b = -A_ab
g_c = -(A_ab + A_bc).
```

After this frame change:

```text
A_ab' = 0
A_bc' = 0
A_ca' = H(A).
```

Thus tree-edge potentials are gauge artifacts and the sole residual on the closing
overlap is the gauge-invariant holonomy.

## Path dependence

Transport from chart `a` to `c` can use either:

```text
indirect: A_ab + A_bc
direct:   -A_ca.
```

Their difference is exactly

```text
(A_ab + A_bc) - (-A_ca) = H(A).
```

Nonzero curvature is therefore recorded as path-dependent memory transport, not as
an arbitrary edge anomaly.

## Gauge-adjusted confidence

MemoryOS v0.70 supplies the component-capped confidence `3/4`. The bounded v0.71
penalty is

```text
P(A) = |H(A)| / 7.
```

For the canonical curved profile:

```text
P(A) = 1/12
C_gauge = 3/4 - 1/12 = 2/3.
```

Both the penalty and adjusted confidence are gauge invariant. The Lean package also
proves the adjusted value remains in `[0,1]` whenever the supplied base and penalty
satisfy the stated bounds.

This finite penalty is a MemoryOS certificate design choice. It is not asserted to
be a universal physical action, Bayesian posterior, or optimal statistical loss.

## Actual Lean package

`MemoryOSGaugeConnectionHolonomyV0_71.lean` proves:

- gauge invariance of triangular holonomy,
- gauge invariance and nonnegativity of curvature energy,
- equivalence of zero curvature energy and flatness,
- invariance of all three covariant overlap residuals,
- constructive tree gauge fixing,
- equality of path-transport discrepancy and holonomy,
- gauge invariance of curvature threshold flags,
- gauge invariance of the curvature penalty and adjusted confidence,
- unit-interval preservation under explicit hypotheses,
- exact canonical values `0`, `7/12`, `1/12`, and `2/3`.

## Runtime profile

The runtime derives and signs:

- 5 literature records,
- 3 local chart records,
- 3 connection-overlap records for each of 2 profiles,
- 2 holonomy and curvature records,
- 3 gauge-parameter records,
- 6 transformed-connection records,
- 6 covariant-residual records,
- 3 tree-gauge-fixing records,
- 2 path-transport records,
- 2 gauge-adjusted-confidence records,
- 8 full-rank transport records,
- 4 singular atomic transport records,
- 3 rank-one source boundaries.

All numeric fields are exact rational values. No floating-point phase, matrix
exponential, or transcendental holonomy approximation is emitted.

## Fail-closed boundary

The checker rejects:

- a modified v0.70 certificate or digest,
- changed connection coefficients,
- a changed holonomy or curvature value,
- a gauge transform that changes holonomy,
- non-covariant section residuals,
- false tree-gauge residuals,
- confidence adjustment using frame-dependent connection components,
- a non-Abelian claim,
- candidate ranking, activation, execution, or persistent WORLD mutation claims,
- unexpected claims.

## Authority boundary

MemoryOS v0.71 remains future-only, read-only, and advisory.

Gauge curvature is not truth authority. A curvature flag is not DecisionOS candidate
ranking. Gauge fixing does not delete source records or choose a privileged truth
frame. The layer does not synthesize plans, commit decisions, activate tools, execute
actions, or mutate persistent WORLD state.
