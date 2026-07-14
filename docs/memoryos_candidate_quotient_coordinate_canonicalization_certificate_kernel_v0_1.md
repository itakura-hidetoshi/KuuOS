# MemoryOS v0.50 — candidate quotient-coordinate canonicalization

## Purpose

MemoryOS v0.49 identified the exact two-dimensional structural nullspace of
the four-candidate Gram representation. MemoryOS v0.50 constructs the quotient
coordinates explicitly and proves that all Gram evidence descends to a unique
canonical chart representative.

The candidate support is not quotiented or pruned. Only redundant coefficient
representations are identified.

## Quotient coordinates

For candidate coefficients in order

```text
(continue, hold, reobserve, terminate_candidate) = (c,h,r,t)
```

define

```text
u = c + h + r
v = c - h + t.
```

These are exactly the two history coordinates induced by the v0.48 factor
matrix.

The canonical representative is

```text
canonical(c,h,r,t) = (0,0,u,v).
```

## Exact decomposition

The source vector differs from its canonical representative by

```text
c * (1,0,-1,-1) + h * (0,1,-1,1),
```

the two structural null vectors certified by MemoryOS v0.49.

Equivalently,

```text
r = u - c - h
t = v - c + h.
```

Thus every coefficient vector has a canonical representative in the chart
`continue = hold = 0`.

## Uniqueness

A vector already in that chart is uniquely determined by `(u,v)`. Two
candidate coefficient vectors have the same quotient coordinates exactly when
their difference is a combination of the two structural null relations.

Canonicalization is idempotent.

## Metric descent

For every source cross term, the complete four-candidate bilinear pairing
computed from all sixteen Gram entries equals the two-history pairing on
quotient coordinates.

Therefore both

```text
B(x,y) = B(canonical(x), canonical(y))
Q(x)   = Q(canonical(x))
```

hold exactly.

The Lean package proves these identities for arbitrary integer candidate
coefficients and arbitrary integer source cross term.

## Runtime fixture

The runtime retains nine bounded probe vectors:

```text
four candidate basis vectors
two structural null vectors
antisymmetric history probe
symmetric history probe
mixed probe (2,-1,3,4)
```

The mixed probe has quotient coordinates `(4,7)` and canonical representative
`(0,0,4,7)`.

At each of the three dephasing steps the runtime verifies:

```text
9 quadratic descent records
9 × 9 = 81 ordered bilinear-pair descent records
```

The quotient metric rank trajectory remains

```text
[1,2,2].
```

## Source binding

The certificate binds:

- the accepted MemoryOS v0.49 certificate and rank-stratification digest;
- the accepted MemoryOS v0.48 certificate and factorization digest;
- exact candidate and history support;
- exact step indices, dephasing numerators, and denominators;
- the fixed structural null basis;
- the fixed probe support.

A re-signed source with a modified structural basis, factor matrix, or rank
trajectory is rejected.

## DecisionOS preservation

The following DecisionOS v0.6 surfaces remain unchanged:

```text
relational frontier
required review
dissent review
minority protection
```

All four candidates and both PlanOS histories remain retained.

## Boundary

```text
canonical representative != selected candidate
quotient coordinate       != candidate ranking
nullspace quotient        != candidate pruning
coordinate uniqueness     != decision uniqueness
metric descent            != decision commit
runtime validation        != verification result
```

No candidate ranking, pruning, selection, decision commit, decision receipt,
plan synthesis, activation, execution, source mutation, WORLD mutation,
verification authority, or truth authority is granted.

## Artifacts

```text
runtime/kuuos_memoryos_candidate_quotient_coordinate_canonicalization_certificate_kernel_v0_1.py
scripts/check_planos_memoryos_candidate_quotient_coordinate_canonicalization_certificate_kernel_v0_1.py
formal/KUOS/OpenHorizon/MemoryOSCandidateQuotientCoordinateCanonicalizationV0_50.lean
formal/KuuOSMemoryOSV0_50.lean
manifests/kuuos_memoryos_candidate_quotient_coordinate_canonicalization_certificate_kernel_v0_1.json
runtime/kuuos_current_check.py
```
