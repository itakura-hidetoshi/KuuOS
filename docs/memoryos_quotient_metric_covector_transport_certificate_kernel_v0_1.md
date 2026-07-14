# MemoryOS quotient-metric covector transport certificate kernel v0.1

## Frontier

This package advances MemoryOS from v0.51 exact quotient-mode diagonalization to v0.52 exact covector transport between the three retained dephasing metrics.

The source quotient metric numerator remains

```text
K(c) = [[2,c],
        [c,2]]
```

for cross numerators `c = [2,1,0]`.

## Full-rank transport

For a source cross `c` and target cross `d`, define the integer transport numerator

```text
P(c -> d) = K(d) adj(K(c)).
```

The formal and runtime layers verify

```text
P(c -> d) K(c) = det(K(c)) K(d).
```

When `det(K(c)) != 0`, division by the source determinant gives an exact rational transport of metric covectors. The six transitions sourced at `c = 1` or `c = 0` are therefore full-rank transports.

Reference matrices are

```text
P(1 -> 0) = [[ 4,-2],
             [-2, 4]], denominator 3

P(0 -> 1) = [[4,2],
             [2,4]], denominator 4.
```

Their round trip scales by twelve before denominator cancellation.

## Composition

For arbitrary source, middle, and target cross terms, the integer transport numerators satisfy

```text
P(middle -> target) P(source -> middle)
  = det(K(middle)) P(source -> target).
```

The reference runtime checks all `3^3 = 27` ordered composition records.

## Rank-one boundary

At full coherence `c = 2`,

```text
det K(2) = 0
symmetric weight = 4
antisymmetric weight = 0.
```

No inverse and no complete transport are claimed from that source. The certificate retains only the exact symmetric-mode partial relation

```text
4 * target_symmetric_dual
  = (2 + target_cross) * source_symmetric_dual.
```

The missing antisymmetric coordinate is not reconstructed. Dephasing can reveal it only after the source metric becomes full rank.

## Probe coverage

All nine MemoryOS v0.50 probes are retained across all nine directed step transitions:

```text
9 transitions * 9 probes = 81 probe transport records.
```

The runtime also retains all four DecisionOS candidates, both PlanOS histories, relational-frontier review sets, dissent visibility, and minority visibility.

## Source binding

The runtime binds:

- the accepted MemoryOS v0.51 certificate and mode-diagonalization digest;
- the accepted MemoryOS v0.50 certificate and quotient-coordinate digest;
- exact candidate and history support;
- all nine quotient-coordinate probes;
- the determinant, rank, mode-weight, and inverse trajectories.

Re-signed substitutions of mode weights, quotient coordinates, transport claims, or authority claims are rejected.

## Boundary

A covector transport is an algebraic comparison witness, not a candidate preference, decision rule, or execution instruction. Rank-one partial transport is not information recovery.

The certificate performs no ranking, pruning, selection, decision commit, plan synthesis, activation, execution, source mutation, WORLD mutation, verification-result claim, or truth-authority grant. It remains future-only, read-only, and advisory.
