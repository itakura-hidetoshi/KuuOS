# WORLD Quantum Log-Sobolev, Contractivity, and Exponential Mixing v0.48

v0.48 extends the v0.47 finite gradient-flow layer with a supplied finite log-Sobolev certificate, one-step contraction factors, iterated gradient-flow shadows, and finite exponential mixing bounds.

```text
v0.47 gradient flow / JKO / entropy production
  → finite log-Sobolev certificate
  → relative entropy to equilibrium
  → one-step contraction
  → iterated gradient-flow shadow
  → geometric relative-entropy decay
  → Lyapunov decay
  → mixing-distance bound
  → higher-gauge covariance
```

The exact WORLD state is not replaced by a quantum Markov semigroup, a mixing trajectory, or an equilibrium distribution.

## Finite log-Sobolev certificate

Each patch carries a nonnegative finite rate `lambda_i` and the supplied inequality

```text
2 lambda_i D_QB(theta || theta_*) <= Sigma(theta),
```

where `Sigma` is the v0.47 entropy-production shadow and `theta_*` is its equilibrium witness.

This is a finite typed certificate. A genuine quantum log-Sobolev inequality for a primitive quantum Markov semigroup remains an external analytic receipt.

## Relative entropy to equilibrium

The finite equilibrium-relative entropy is

```text
H_*(theta) = D_QB(theta || theta_*).
```

Lean derives

```text
H_*(theta) >= 0
H_*(theta) = 0 iff theta = theta_*.
```

## One-step contraction

Each patch carries a contraction factor

```text
0 <= rho_i <= 1
```

and supplied one-step certificates

```text
H_*(G_h(theta)) <= rho_i H_*(theta)
L(G_h(theta))   <= rho_i L(theta)
```

for nonnegative step size `h`.

## Iterated finite flow

The finite iterate is defined recursively:

```text
G_h^0(theta)     = theta
G_h^(n+1)(theta) = G_h(G_h^n(theta)).
```

Lean proves by induction

```text
H_*(G_h^n(theta)) <= rho_i^n H_*(theta)
L(G_h^n(theta))   <= rho_i^n L(theta).
```

This is finite geometric decay. It is not a claim of continuous-time exponential convergence.

## Mixing distance

Each patch carries a nonnegative mixing-distance shadow satisfying

```text
d_mix(theta) <= H_*(theta)
d_mix(theta) = 0 iff theta = theta_*.
```

Lean therefore derives

```text
d_mix(G_h^n(theta)) <= rho_i^n H_*(theta).
```

The mixing-distance shadow is not physical total variation, trace distance, or an ontological distance between WORLD branches.

## Higher-gauge covariance

The log-Sobolev rate, contraction factor, relative entropy to equilibrium, and mixing distance are preserved across patch transport. Gauge-coordinate equivalence does not collapse WORLD branches or erase higher-gauge holonomy.

## Lean-direct surface

Lean directly verifies:

- nonnegativity of equilibrium-relative entropy;
- zero relative entropy iff the parameter equals the equilibrium witness;
- the finite log-Sobolev certificate;
- recursive finite gradient-flow iteration;
- geometric contraction of equilibrium-relative entropy;
- geometric contraction of the Lyapunov gap;
- finite exponential mixing-distance bounds;
- zero mixing distance iff equilibrium;
- gauge invariance of equilibrium-relative entropy and mixing distance;
- analytic-receipt, runtime-boundary, and representation-boundary packages.

## External analytic receipts

The following remain external:

- genuine quantum log-Sobolev inequality;
- equivalence with hypercontractivity;
- comparison with a spectral gap;
- primitive quantum Markov semigroup realization;
- complete log-Sobolev inequalities;
- continuous-time exponential mixing;
- physical Pinsker or trace-distance identification;
- continuum quantum mixing;
- higher-gauge mixing flow.

## Runtime boundary

Runtime validates only a hash-bound fail-closed receipt. It does not:

```text
compute a physical log-Sobolev constant
execute a quantum Markov semigroup
declare physical mixing
infer ergodicity from a finite certificate
collapse WORLD branches at equilibrium
optimize a WORLD state
update WORLD
```

The fixed boundary is

```text
WORLD != Markov semigroup
finite contraction != physical mixing
equilibrium != WORLD collapse
mixing-distance shadow != ontological distance
log-Sobolev certificate != truth authority
candidate != authority
validation != truth
```

The v0.48 layer remains a read-only sidecar preserving noncommutativity, non-Markovian history, multi-WORLD noncollapse, and the two-truths gap.
