# MemoryOS v0.46 — candidate-pair Cauchy–Schwarz relational coherence envelope

## Purpose

MemoryOS v0.45 lifts the MemoryOS-conditioned PlanOS history kernel into a complete DecisionOS candidate Gram kernel.

MemoryOS v0.46 converts every retained candidate-pair entry into an exact bounded coherence envelope without ranking, pruning, or selecting candidates.

For each candidate pair `i, j` and each dephasing step, the runtime emits the exact witness

```text
|G[i,j]|^2 <= G[i,i] G[j,j]
```

as the nonnegative principal-minor margin

```text
G[i,i] G[j,j] - |G[i,j]|^2.
```

When both diagonals are positive, the exact reduced rational value

```text
normalized coherence square = |G[i,j]|^2 / (G[i,i] G[j,j])
```

is emitted in `[0,1]`.

When either diagonal is zero, the Cauchy–Schwarz bound forces the incident coherence entry to be zero. The runtime uses the canonical degenerate representation `0/1` and records the zero-diagonal witness explicitly.

## Actual theorem

For the two-history source kernel

```text
K(c) = [[2,c],[c,2]]
```

and candidate coupling vectors `x = (a,b)`, `y = (p,q)`, define

```text
B_c(x,y) = x K(c) y^T
E_c(x)   = B_c(x,x).
```

The formal package proves the exact identity

```text
E_c(x) E_c(y) - B_c(x,y)^2
  = (4 - c^2) (a q - b p)^2.
```

Therefore, whenever

```text
-2 <= c <= 2,
```

both factors on the right are nonnegative and

```text
B_c(x,y)^2 <= E_c(x) E_c(y).
```

It also proves that `E_c(x) = 0` forces `B_c(x,y) = 0` for every `y`.

This is the algebraic reason the v0.46 normalized envelope is bounded and why zero-energy candidate directions cannot carry hidden coherence.

## Exact reference envelope

Candidate order:

```text
continue
hold
reobserve
terminate_candidate
```

Dephasing numerators:

```text
2, 1, 0
```

Exact normalized coherence-square trajectories for distinct pairs are:

```text
continue–hold:                 [0,   0,   0]
continue–reobserve:            [1, 3/4, 1/2]
continue–terminate_candidate:  [1, 3/4, 1/2]
hold–reobserve:                [0, 1/4, 1/2]
hold–terminate_candidate:      [0, 1/4, 1/2]
reobserve–terminate_candidate: [1, 1/4,   0]
```

The corresponding determinant-margin numerator trajectories are:

```text
continue–hold:                 [0, 12, 16]
continue–reobserve:            [0,  3,  4]
continue–terminate_candidate:  [0,  3,  4]
hold–reobserve:                [0,  3,  4]
hold–terminate_candidate:      [0,  3,  4]
reobserve–terminate_candidate: [0,  3,  4]
```

The `hold–terminate_candidate` raw coherence remains

```text
[0, -1, -2].
```

Its normalized square is `[0, 1/4, 1/2]`. The negative sign remains visible but is not interpreted as negative preference, rejection, or lower utility.

## Complete support

For every step, all 16 ordered candidate pairs are retained.

Each record binds:

```text
left candidate id
right candidate id
raw real and imaginary numerators
source kernel denominator
left and right diagonal numerators
coherence magnitude square
candidate-diagonal product
principal-minor determinant margin
Cauchy–Schwarz witness
zero-diagonal witness
reduced normalized-coherence-square fraction
```

No representative pair or preferred candidate is selected.

## Source binding

The certificate recomputes and binds:

```text
accepted MemoryOS v0.45 certificate digest
MemoryOS v0.45 candidate Gram kernel digest
MemoryOS v0.43 source certificate digest
MemoryOS v0.44 source certificate digest
complete DecisionOS candidate order
complete dephasing trajectory
all ordered candidate-pair entries
```

It rejects:

```text
source substitution
certificate digest mismatch
candidate Gram digest mismatch
incomplete or duplicate candidate-pair support
non-Hermitian source entries
imaginary or negative diagonals
nondecreasing dephasing sequence
negative principal-minor margin
normalized coherence square above one
nonzero coherence incident to a zero diagonal
false governance claims
```

## DecisionOS preservation

The following DecisionOS v0.6 relational sets remain unchanged:

```text
relational frontier:  [reobserve]
required review:      [continue, hold, reobserve]
dissent review:       [continue]
minority protection:  [hold]
```

Normalized coherence is advisory relational evidence only. It does not override review, dissent, minority protection, admissibility, or DecisionOS ownership of any future selection operation.

## Boundary

```text
normalized coherence != scalar utility
coherence magnitude    != candidate quality
off-diagonal sign      != preference
Cauchy–Schwarz margin  != recommendation
unit normalized value  != identity of candidates
zero coherence         != rejection
MemoryOS envelope      != DecisionOS decision
runtime validation     != verification result
```

No candidate ranking, pruning, selection, decision commit, receipt issuance, plan synthesis, activation, execution, source mutation, WORLD mutation, verification authority, or truth authority is granted.

## Artifacts

```text
runtime/kuuos_memoryos_candidate_pair_cauchy_schwarz_relational_coherence_envelope_certificate_kernel_v0_1.py
scripts/check_planos_memoryos_candidate_pair_cauchy_schwarz_relational_coherence_envelope_certificate_kernel_v0_1.py
formal/KUOS/OpenHorizon/MemoryOSCandidatePairCauchySchwarzRelationalCoherenceEnvelopeV0_46.lean
formal/KuuOSMemoryOSV0_46.lean
manifests/kuuos_memoryos_candidate_pair_cauchy_schwarz_relational_coherence_envelope_certificate_kernel_v0_1.json
runtime/kuuos_current_check.py
```
