# MemoryOS quotient-transport Jacobian and volume stratification v0.1

## Frontier

This package advances MemoryOS from v0.52 exact quotient-metric covector transport to v0.53 exact mode multipliers, Jacobians, and rank-stratified volume behavior.

The retained dephasing cross numerators remain

```text
[2,1,0]
```

with quotient metrics

```text
K(c) = [[2,c],
        [c,2]].
```

No DecisionOS candidate or PlanOS history is removed.

## Raw transport modes

MemoryOS v0.52 defines

```text
P(c -> d) = K(d) adj(K(c)).
```

The fixed symmetric and antisymmetric mode vectors are eigenvectors of this transport numerator. Their exact eigenvalues are

```text
mu_s(c -> d) = (2+d)(2-c)
mu_a(c -> d) = (2-d)(2+c).
```

The complete transport determinant factors as

```text
det P(c -> d) = det K(c) det K(d).
```

## Full-rank normalized transport

When `det K(c) != 0`, division by the source determinant gives exact rational mode multipliers

```text
symmetric:     (2+d)/(2+c)
antisymmetric: (2-d)/(2-c).
```

Their product is the exact Jacobian

```text
J(c -> d) = det K(d) / det K(c).
```

For the two full-rank source metrics:

```text
1 -> 0:
  symmetric multiplier     2/3
  antisymmetric multiplier 2
  Jacobian                 4/3

0 -> 1:
  symmetric multiplier     3/2
  antisymmetric multiplier 1/2
  Jacobian                 3/4
```

The round-trip Jacobian is exactly one.

## Stratification

The nine directed transitions divide into:

```text
6 normalized source-active transitions
4 invertible full-rank-to-full-rank transitions
2 full-rank-to-rank-one volume collapses
3 rank-one source boundaries
```

A full-rank source may map to the rank-one target with Jacobian zero. That is a genuine volume collapse, not an inverse.

At source cross `2`, the determinant is zero. No two-dimensional normalized Jacobian is issued. The symmetric dual retains the exact partial relation from v0.52, while the antisymmetric source dual is zero and cannot determine a later nonzero antisymmetric dual.

## Composition

Raw mode eigenvalues satisfy the determinant-scaled cocycle

```text
mu_mode(m -> t) mu_mode(s -> m)
  = det K(m) mu_mode(s -> t).
```

On paths whose source and middle metrics are full rank, the normalized mode multipliers compose exactly. All 27 ordered source-middle-target triples are retained; 12 have active normalized composition and 8 remain entirely within the invertible full-rank stratum.

## Runtime coverage

The certificate binds:

- accepted MemoryOS v0.52 certificate and both transport digests;
- accepted MemoryOS v0.51 certificate and mode digest;
- all four DecisionOS candidate ids;
- both PlanOS history ids;
- all nine quotient-coordinate probes;
- all v0.52 transition and composition witnesses.

It emits:

```text
9 transition records
81 probe-mode transport records
27 mode-composition records
```

Re-signed substitutions of transport matrices, mode weights, source digests, boundary claims, or authority claims are rejected.

## Boundary

Jacobian and volume distortion are algebraic comparison witnesses. They are not candidate utility, preference, consensus, selection, decision authority, activation, execution, verification, or truth authority.

The package remains future-only, read-only, and advisory.
