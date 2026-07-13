# PlanOS Multi-Chart Atlas Curvature Certificate Kernel v0.1

## Purpose

PlanOS v1.08 extends the v1.07 second-order metric-jet curvature layer from one local coordinate chart to a bounded finite atlas.

The kernel verifies that the same local PlanOS geometry is represented consistently across overlapping charts without turning chart choice, curvature, or holonomy into candidate-selection or execution authority.

## Inputs

The certificate consumes three or more chart snapshots.

Each chart retains:

- a stable `chart_id`
- an ordered coordinate schema
- the source PlanOS v1.07 curvature-certificate digest
- metric and inverse metric
- Christoffel symbols
- Riemann and Ricci tensors
- scalar curvature
- candidate two-plane, sectional-curvature, and infinitesimal-holonomy records
- a positive boundary margin and regularity radius

Each directed overlap transition retains:

- source and target chart identifiers
- Jacobian `J = ∂y / ∂x`
- inverse Jacobian `K = ∂x / ∂y`
- inverse-coordinate Hessian `∂²x / ∂y∂y`
- a positive overlap margin
- a stable source transition digest

## Coordinate transformation laws

For a contravariant vector,

```text
v'^a = J^a_i v^i
```

For the metric and inverse metric,

```text
g'_{ab} = K^i_a K^j_b g_{ij}
g'^{ab} = J^a_i J^b_j g^{ij}
```

For the affine connection,

```text
Γ'^a_bc
  = J^a_i K^j_b K^k_c Γ^i_jk
    + J^a_i ∂²x^i/(∂y^b∂y^c)
```

For Riemann and Ricci curvature,

```text
R'^a_bcd = J^a_i K^j_b K^k_c K^l_d R^i_jkl
Ric'_{bd} = K^j_b K^l_d Ric_{jl}
```

Scalar curvature is required to be chart invariant.

Candidate plane vectors and holonomy vectors transform contravariantly.

Sectional curvature is required to remain invariant, while the infinitesimal holonomy increment is required to transform equivariantly.

## Atlas cocycle

For transitions from chart `A` to `B`, `B` to `C`, and `A` to `C`, the kernel verifies

```text
J_AC = J_BC J_AB
K_AC = K_AB K_BC
```

At least one explicit three-chart cocycle witness is required.

The current kernel verifies the affine transition surface.

Transition Hessians are represented and checked for lower-index symmetry.

The normal fixture uses affine transitions, so the Hessian contribution vanishes while the full connection transformation law remains present.

## Boundary and singularity guards

Every chart must retain a positive boundary margin and regularity radius.

Every overlap must retain a positive overlap margin.

Every transition Jacobian must satisfy a configured lower bound on the absolute determinant.

The Jacobian, inverse Jacobian, and transition Hessian are separately bounded.

A singular or near-singular transition is rejected before geometric compatibility is certified.

## Runtime validation

The runtime independently verifies:

- at least three charts and consistent dimensions
- unique chart identifiers and transition pairs
- finite tensor schemas
- metric symmetry and positive definiteness
- exact inverse-metric identities
- Ricci symmetry and scalar contraction
- Jacobian and inverse-Jacobian identities
- transition-Hessian symmetry
- metric and inverse-metric transformation laws
- affine-connection transformation law
- Riemann and Ricci transformation laws
- scalar-curvature invariance
- candidate-plane identity retention
- sectional-curvature invariance
- infinitesimal-holonomy equivariance
- atlas Jacobian and inverse-Jacobian cocycles
- chart-boundary and overlap margins
- digest integrity and numeric bounds

The reference fixture contains three non-identical coordinate charts.

It retains scalar curvature `-0.2`, sectional curvature `0.1`, and nonzero infinitesimal holonomy in every chart.

All transformation and cocycle residuals are zero in the reference fixture.

## Formal package

The Mathlib layer defines:

- contravariant vector transformation
- Jacobian composition
- covariant metric transformation
- affine-connection transformation with inverse Hessian
- `(1,3)` Riemann transformation
- covariant Ricci transformation
- a two-dimensional determinant guard
- chart-local sectional values

It proves:

- functorial composition of vector and holonomy transformation
- identity-Jacobian action
- zero metric preservation
- zero connection preservation under zero transition Hessian
- zero Riemann and Ricci preservation
- sectional-value invariance from equal numerator and Gram determinant
- singularity of a zero first Jacobian row in dimension two
- regularity of the identity transition
- atlas non-authority and future-only boundaries

## Fixed boundaries

```text
chart choice != candidate selection
coordinate value != intrinsic value
connection coefficient != tensor component
sectional curvature != plan ranking
scalar curvature != global truth
holonomy != execution
atlas compatibility != activation authorization
WORLD-conditioned chart data != WORLD mutation
```

The certificate does not select a preferred chart.

It does not rank candidate plans.

It does not mutate any source PlanOS v1.07 curvature certificate or persistent WORLD state.

It is read-only, future-only, inactive now, and grants no execution permission.
