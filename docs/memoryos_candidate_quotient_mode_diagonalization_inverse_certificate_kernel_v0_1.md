# MemoryOS candidate quotient-mode diagonalization and inverse certificate kernel v0.1

## Frontier

This package advances the MemoryOS frontier from v0.50 quotient-coordinate canonicalization to v0.51 exact mode diagonalization and inverse witnesses.

The source candidate coefficient vector remains ordered as

```text
continue, hold, reobserve, terminate_candidate
```

MemoryOS v0.50 maps it to the two quotient coordinates

```text
u = continue + hold + reobserve
v = continue - hold + terminate_candidate.
```

MemoryOS v0.51 does not remove any candidate or PlanOS history. It changes only the algebraic basis used to expose the quotient metric.

## Symmetric and antisymmetric modes

Define

```text
s = u + v
a = u - v.
```

For source cross numerator `c`, the quotient metric numerator is

```text
K(c) = [[2,c],
        [c,2]].
```

The two fixed mode vectors are

```text
symmetric:     (1, 1)
antisymmetric: (1,-1).
```

Their exact eigenweights are

```text
lambda_s = 2 + c
lambda_a = 2 - c.
```

For arbitrary quotient vectors `x` and `y`, the complete bilinear pairing satisfies

```text
2 B_c(x,y)
  = (2+c) s_x s_y
  + (2-c) a_x a_y.
```

The same identity with `x = y` diagonalizes every quadratic evidence value.

## Reference trajectory

The source dephasing cross numerators are

```text
[2,1,0].
```

Therefore the exact mode-weight trajectory is

```text
symmetric weights:     [4,3,2]
antisymmetric weights: [0,1,2].
```

The determinant factors as

```text
det K(c) = (2+c)(2-c) = 4-c^2,
```

which gives

```text
determinants: [0,3,4]
ranks:        [1,2,2].
```

At full coherence, the antisymmetric weight is zero and the quotient pairing is exactly rank one:

```text
B_2(x,y) = 2 s_x s_y.
```

Dephasing releases the antisymmetric mode without changing the retained candidate or history support.

## Integer adjugate inverse witness

The integer adjugate is

```text
adj K(c) = [[ 2,-c],
            [-c, 2]].
```

The formal and runtime layers verify both identities

```text
K(c) adj K(c) = (4-c^2) I
adj K(c) K(c) = (4-c^2) I.
```

At `c = 2`, the determinant is zero and no inverse is claimed. At `c = 1` and `c = 0`, the determinant is respectively three and four, so the adjugate supplies an exact rational inverse witness after division by that determinant.

## Probe coverage

All nine MemoryOS v0.50 probes are retained:

```text
four candidate basis vectors
two structural-null probes
antisymmetric history probe
symmetric history probe
mixed candidate probe
```

The mixed probe has v0.50 quotient coordinates `(4,7)` and v0.51 mode coordinates

```text
s = 11
a = -3.
```

For each of three source steps, the checker validates:

```text
9 probe quadratic mode records
81 ordered probe-pair bilinear mode records
```

This yields 27 quadratic and 243 ordered bilinear records across the trajectory.

## Source binding

The runtime binds:

- the accepted MemoryOS v0.50 certificate digest;
- the v0.50 quotient-coordinate digest;
- the accepted MemoryOS v0.48 factorization certificate digest;
- the v0.48 factorization trajectory digest;
- exact candidate and history support;
- all v0.50 canonical coordinates and descent records;
- the exact v0.48 two-history metric at every step.

Re-signed substitutions of coordinates, descent values, factor rows, mode trajectories, or authority claims are rejected.

## Boundary

The symmetric mode is not consensus. The antisymmetric mode is not dissent classification. Rank one is not candidate agreement, and an inverse metric witness is not a decision rule.

The certificate performs no:

- candidate ranking, pruning, or selection;
- decision commit or decision receipt issuance;
- plan synthesis or activation;
- execution authorization;
- source certificate mutation;
- DecisionOS or persistent WORLD mutation;
- verification-result or truth-authority claim.

The package remains future-only, read-only, and advisory.
