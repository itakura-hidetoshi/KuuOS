# PlanOS Jacobi Field and Geodesic Deviation Certificate Kernel v0.1

## Purpose

PlanOS v1.09 extends the v1.08 multi-chart curvature atlas from static curvature compatibility to bounded infinitesimal variation dynamics along retained candidate geodesics.

The kernel evaluates covariant acceleration, tidal acceleration, the Jacobi equation, and local conjugate-point candidates without selecting a plan or granting execution authority.

## Geodesic and Jacobi data

For each retained candidate, the certificate consumes:

- a velocity field `V`
- covariant acceleration `∇_V V`
- a nonzero Jacobi variation field `J`
- first and second covariant derivatives of `J`
- an endpoint Jacobi field
- the source candidate digest

The curvature action is fixed as

```text
(R(V,J)V)^i = R^i_jkl V^j J^k V^l
```

The Jacobi residual is

```text
JacobiResidual^i = (∇²_V J)^i + (R(V,J)V)^i
```

The kernel requires the residual to remain within an explicit bound.

## Tidal acceleration

The quantity `R(V,J)V` is retained as chart-local tidal acceleration.

It represents infinitesimal relative acceleration between nearby candidate geodesics.

It is not interpreted as candidate quality, ethical priority, or execution pressure.

## Local conjugate-point candidates

A retained variation is marked as a local conjugate-point candidate when:

- its initial variation norm is nonzero above a configured lower bound
- its endpoint variation norm is below the configured conjugate-point tolerance
- the Jacobi equation remains satisfied within the configured residual bound

This is finite-window local evidence only.

It does not establish a global conjugate point, geodesic incompleteness, optimality failure, or plan rejection.

## Runtime validation

The runtime independently verifies:

- metric and Riemann tensor schemas
- finite candidate vector fields
- unique candidate identifiers
- source and input digest integrity
- bounded covariant acceleration
- bounded tidal acceleration
- bounded Jacobi residual
- nonzero initial variation norm
- endpoint variation norm
- local conjugate-point candidate retention
- non-mutation and non-authority boundaries

The reference fixture uses a two-dimensional constant-curvature witness with `K = 0.2`.

For `V = e_x` and `J = e_y`, the fixture reconstructs nonzero tidal acceleration and balances it with the second covariant derivative so that the Jacobi residual vanishes.

## Formal package

The Mathlib layer defines curvature action, Jacobi residual, and variation norm squared.

It proves:

- zero curvature gives zero tidal acceleration
- zero curvature reduces the Jacobi residual to the second covariant derivative
- a second derivative equal to the negative tidal term solves the Jacobi equation
- zero endpoint variation has zero metric norm
- a zero Jacobi field has zero curvature action
- Jacobi and conjugate-point evidence grants no authority
- the certificate remains read-only, future-only, and inactive

## Fixed boundaries

```text
geodesic != selected plan
Jacobi field != alternate-plan authorization
tidal acceleration != urgency
conjugate-point candidate != plan rejection
local endpoint zero != global conjugate point
curvature evidence != ethical verdict
variation dynamics != execution
WORLD-conditioned geometry != WORLD mutation
```
