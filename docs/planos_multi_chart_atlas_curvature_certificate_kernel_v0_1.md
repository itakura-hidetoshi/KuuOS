# PlanOS v1.08 Multi-Chart Atlas Curvature Certificate

PlanOS v1.08 extends the local second-order geometry of v1.07 from one coordinate chart to a finite read-only atlas.

## Inputs

Each chart retains:

- a unique chart identifier
- a Jacobian from the fixed reference chart
- the metric and inverse metric represented in that chart
- the Riemann tensor represented in that chart

The atlas digest binds the complete ordered chart set.

## Coordinate laws

For a Jacobian `J = dx/dy`, the metric transforms as

```text
g' = J^T g J
```

and the inverse metric transforms as

```text
g'^(-1) = J^(-1) g^(-1) J^(-T).
```

The `(1,3)` Riemann tensor transforms tensorially:

```text
R'^a_bcd
= (J^(-1))^a_i J^j_b J^k_c J^l_d R^i_jkl.
```

Ricci is recomputed by contraction in every chart and scalar curvature is independently contracted with the transformed inverse metric.

## Atlas consistency

For every pair of charts, the runtime reconstructs both directed transition matrices from the fixed reference Jacobians and verifies their product is the identity. This is the bounded finite-atlas cocycle condition used by this kernel.

## Fail-closed boundary

The kernel blocks:

- fewer than two charts
- missing or duplicate chart identifiers
- malformed or nonfinite matrices and curvature tensors
- singular transition Jacobians
- inverse Jacobian identity failure
- atlas digest mismatch
- metric or inverse-metric transformation mismatch
- Riemann transformation mismatch
- scalar curvature non-invariance
- Jacobian or curvature bound violation

A singular Jacobian is retained only as a detected chart boundary. It is never promoted into a valid transition.

## Formal surface

The Mathlib package defines metric, inverse-metric, Riemann, and Ricci coordinate transformations. It proves identity-chart invariance and preservation of zero curvature under arbitrary coordinate transformations.

## Fixed boundaries

```text
atlas != candidate selection
chart transition != WORLD mutation
coordinate singularity != physical singularity
scalar invariance != global truth
curvature != execution authority
```

The source v1.07 curvature certificate is not mutated. History and WORLD state remain read-only. The certificate is future-only, inactive now, and carries no execution permission.
