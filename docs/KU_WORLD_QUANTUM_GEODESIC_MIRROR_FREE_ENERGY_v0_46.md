# WORLD Quantum Geodesic, Mirror Descent, and Variational Free Energy v0.46

v0.46 extends the v0.45 dual-affine projection layer with finite exponential and mixture geodesic witnesses, quantum-geodesic action, variational free-energy decomposition, and Bregman mirror-descent certificates.

```text
v0.45 dual-affine projection
  → exponential / mixture geodesics
  → quantum-geodesic action
  → complexity + inaccuracy decomposition
  → variational free energy
  → surprisal-shadow bound
  → mirror-descent step
  → Bregman descent certificate
  → projected mirror defect
  → higher-gauge covariance
```

The exact WORLD state is not replaced by a geodesic path, a free-energy scalar, or an optimization trajectory.

## Geodesic witnesses

Each patch carries finite paths

```text
gamma_e(theta, eta; t)
gamma_m(theta, eta; t)
```

with endpoints at `t = 0` and `t = 1`. The finite quantum-geodesic action satisfies

```text
A_Q(theta, eta) >= 0
A_Q(theta, eta) = 0 iff theta = eta.
```

Smooth geodesic existence and identification with the BKM Levi-Civita geometry remain external analytic receipts.

## Variational free energy

The finite decomposition is

```text
F_var(theta) = complexity(theta) + inaccuracy(theta),
```

with both terms nonnegative. Lean therefore derives `F_var(theta) >= 0`.

A supplied surprisal shadow obeys

```text
surprisal_shadow <= F_var(theta).
```

This is a finite observational bound. It is not physical evidence, truth authority, or a WORLD-state identity.

## Bregman mirror descent

For step size `h >= 0`, the mirror step `M_h(theta)` carries the certificate

```text
F_var(M_h(theta))
  + D_QB(M_h(theta) || theta)
  <= F_var(theta).
```

Lean derives

```text
F_var(M_h(theta)) <= F_var(theta)
F_var(theta) - F_var(M_h(theta)) >= 0.
```

The projected step is

```text
Pi_e(M_h(theta)),
```

and its Bregman defect is nonnegative, with zero iff the mirror step is already fixed by the exponential projection.

A descent witness is not execution authority. Low free energy is not truth, safety, permission, commitment, or ontological identity.

## Geodesic convexity

Finite exponential and mixture geodesic convexity certificates are retained:

```text
F_var(gamma(theta, eta; t))
  <= (1 - t) F_var(theta) + t F_var(eta),
  0 <= t <= 1.
```

Genuine convexity from smooth quantum geometry remains external.

## Higher-gauge covariance

Geodesics, action, free-energy components, gradients, mirror steps, and dissipation transport covariantly across the WORLD patch atlas. Gauge-coordinate equivalence does not collapse WORLD branches or erase higher-gauge holonomy.

## Lean-direct surface

Lean directly verifies:

- exponential and mixture geodesic endpoints;
- quantum-geodesic action nonnegativity and separation;
- variational free-energy nonnegativity;
- the surprisal-shadow bound;
- zero-step mirror identity;
- mirror-step free-energy nonincrease;
- nonnegative mirror dissipation;
- the Bregman descent certificate;
- nonnegative projected mirror defect;
- zero projected defect iff projection fixed point;
- finite e/m geodesic convexity certificates;
- gauge invariance and covariance;
- analytic-receipt, runtime-boundary, and representation-boundary packages.

## External analytic receipts

The following remain external:

- smooth quantum geodesic realization;
- BKM Levi-Civita geodesic identification;
- Legendre mirror-map construction;
- convergence and rates of mirror descent;
- the genuine variational free-energy principle;
- physical evidence-bound identification;
- active-inference interpretation;
- quantum gradient-flow realization;
- continuum mirror flow;
- higher-gauge variational flow.

## Runtime boundary

Runtime validates only a hash-bound, fail-closed receipt. It does not:

```text
construct a physical quantum geodesic
compute physical free energy
execute mirror descent
infer truth from low free energy
grant execution from a descent witness
optimize a WORLD state
update WORLD
```

The fixed boundary is

```text
WORLD != geodesic path
low free energy != truth authority
descent witness != execution authority
evidence bound != physical evidence
geodesic action != WORLD history identity
candidate != authority
validation != truth
```

The v0.46 layer remains a read-only sidecar preserving noncommutativity, non-Markovian history, multi-WORLD noncollapse, and the two-truths gap.
