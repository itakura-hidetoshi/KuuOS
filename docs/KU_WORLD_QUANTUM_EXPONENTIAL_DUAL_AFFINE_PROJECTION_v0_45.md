# WORLD Quantum Exponential Dual-Affine Projection v0.45

v0.45 extends the finite v0.44 Araki–Petz quantum-information-geometric sidecar with natural and expectation coordinates, a Fenchel–Young separation gap, quantum Bregman divergence, and exponential/mixture information projections.

```text
v0.44 Araki–Petz quantum information geometry
  → natural coordinate
  → expectation coordinate
  → log-partition shadow / dual-potential shadow
  → Fenchel–Young gap
  → quantum Bregman divergence
  → exponential projection
  → mixture projection
  → dual Pythagorean decomposition
  → Petz-recoverable projected coordinates
```

The exact WORLD state is not replaced by a quantum exponential family, a dual coordinate system, a Legendre transform, or an information projection.

## Dual coordinates

Each WORLD patch carries finite coordinate maps

```text
vartheta_i : Parameter → Tangent
eta_i      : Parameter → Tangent
```

representing natural and expectation coordinates. Both maps are injective inside the finite observational sidecar.

Gauge transport preserves both coordinate representations:

```text
T_ij(vartheta_i(theta)) = vartheta_j(T_ij(theta))
T_ij(eta_i(theta))      = eta_j(T_ij(theta)).
```

## Fenchel–Young separation

The finite potential shadows are

```text
psi_i(theta)
phi_i(eta).
```

The typed Fenchel–Young gap is

```text
F_i(theta, eta)
  = psi_i(theta) + phi_i(eta)
  - g_QF(theta; vartheta_i(theta), eta_i(eta)).
```

Lean verifies

```text
F_i(theta, eta) >= 0
F_i(theta, eta) = 0 iff theta = eta.
```

This is a finite supplied duality certificate. Genuine differentiability, strict convexity, and smooth Legendre duality remain external analytic receipts.

## Quantum Bregman divergence

v0.45 introduces

```text
D_QB,i(theta || eta)
```

with the finite typed identification

```text
D_QB,i(theta || eta) = D_i(theta || eta),
```

where `D_i` is the v0.43 information divergence. Lean therefore derives

```text
D_QB >= 0
D_QB(theta || eta) = 0 iff theta = eta
```

and gauge invariance directly from the already validated v0.43 divergence surface.

The genuine identification of Araki relative entropy with a noncommutative Bregman divergence remains external.

## Exponential and mixture projections

Each patch carries two parameter projections

```text
Pi_e : Parameter → Parameter
Pi_m : Parameter → Parameter.
```

Lean verifies idempotence:

```text
Pi_e(Pi_e(theta)) = Pi_e(theta)
Pi_m(Pi_m(theta)) = Pi_m(theta).
```

Their projection defects are

```text
L_e(theta) = D_QB(theta || Pi_e(theta))
L_m(theta) = D_QB(Pi_m(theta) || theta).
```

Lean derives

```text
L_e(theta) >= 0
L_e(theta) = 0 iff Pi_e(theta) = theta

L_m(theta) >= 0
L_m(theta) = 0 iff Pi_m(theta) = theta.
```

Zero projection defect means fixed-point recoverability inside the finite sidecar. It does not establish ontological WORLD identity.

## Dual Pythagorean laws

The finite exponential and mixture Pythagorean decompositions are

```text
D_QB(theta || eta)
  = D_QB(theta || Pi_e(theta))
  + D_QB(Pi_e(theta) || eta)
```

and

```text
D_QB(theta || eta)
  = D_QB(theta || Pi_m(eta))
  + D_QB(Pi_m(eta) || eta).
```

The projected natural and expectation coordinates are linked to the v0.44 Petz-recoverability predicate.

## Higher-gauge covariance

Natural coordinates, expectation coordinates, both potential shadows, the Fenchel–Young gap, quantum Bregman divergence, and both projections are transported covariantly across the WORLD patch atlas.

Coordinate equivalence does not collapse WORLD branches, and the higher-gauge 2-cell of v0.42–v0.43 remains intact.

## Lean-direct surface

Lean directly verifies:

- injectivity of natural and expectation coordinates;
- Fenchel–Young nonnegativity and zero separation;
- identification of quantum Bregman divergence with v0.43 divergence;
- divergence nonnegativity and parameter separation;
- idempotence of exponential and mixture projections;
- nonnegative projection defects;
- zero projection defect iff projection fixed point;
- exponential and mixture Pythagorean decompositions;
- Petz recoverability of projected coordinates;
- gauge invariance and covariance;
- analytic-receipt, runtime-boundary, and representation-boundary packages.

## External analytic receipts

The following remain external:

- genuine noncommutative exponential-family realization;
- smooth Legendre duality;
- strict convexity of quantum potentials;
- Araki-relative-entropy/Bregman identification;
- e-flat and m-flat autoparallel submanifolds;
- the full quantum information-projection theorem;
- equivalence with Petz sufficiency;
- infinite-dimensional dually flat geometry;
- continuum quantum exponential fields;
- higher-stack dual-affine geometry.

## Runtime boundary

Runtime validates only a hash-bound fail-closed receipt. It does not:

```text
construct a quantum exponential family
compute a physical log-partition function
execute a Legendre transform
execute an information projection
infer WORLD identity from projection
optimize a WORLD state
update WORLD
```

The fixed boundary is

```text
WORLD != quantum exponential family
WORLD != dual coordinates
WORLD != information projection
zero projection defect != ontological identity
candidate != authority
validation != truth
```

The v0.45 layer remains a read-only sidecar preserving noncommutativity, non-Markovian history, multi-WORLD noncollapse, and the two-truths gap.
