# MemoryOS v0.49 — candidate nullspace and dephasing rank stratification

## Purpose

MemoryOS v0.48 reconstructed the complete four-candidate Gram kernel through the exact two-history factorization

```text
G = C K C*
```

with

```text
C = [[ 1,  1],   continue
     [ 1, -1],   hold
     [ 1,  0],   reobserve
     [ 0,  1]]   terminate_candidate.
```

MemoryOS v0.49 identifies the exact candidate-coordinate nullspace induced by this factorization and separates it from an additional coherence-dependent null direction that exists only at full coherence.

## Structural nullspace

For candidate coefficients in order

```text
continue, hold, reobserve, terminate_candidate
```

the candidate-to-history map is

```text
u = continue + hold + reobserve
v = continue - hold + terminate_candidate.
```

The factor matrix has two exact structural null relations:

```text
n1 = (1,0,-1,-1)
   = continue - reobserve - terminate_candidate

n2 = (0,1,-1,1)
   = hold - reobserve + terminate_candidate.
```

Both lift to history coordinates `(0,0)`.

At every dephasing step, the runtime verifies for each structural relation:

```text
C* n = 0
n* G = 0
G n = 0
n* G n = 0.
```

These are exact integer-numerator equalities, not tolerance-based checks.

## Null-translation invariance

For arbitrary candidate coefficients `(c,h,r,t)` and arbitrary integers `alpha,beta`, define

```text
(c',h',r',t')
  = (c + alpha,
     h + beta,
     r - alpha - beta,
     t - alpha + beta).
```

This adds `alpha*n1 + beta*n2`.

The history coordinates are unchanged:

```text
u(c',h',r',t') = u(c,h,r,t)
v(c',h',r',t') = v(c,h,r,t).
```

Therefore the complete candidate Gram quadratic evidence is unchanged for every source cross term.

The Lean theorem proves this for arbitrary integer candidate coefficients, arbitrary integer null translations, and arbitrary integer coherence cross term.

## Coherence-dependent null direction

The antisymmetric history probe is

```text
q = (0,0,1,-1)
  = reobserve - terminate_candidate.
```

Unlike `n1` and `n2`, this vector does not lie in the structural kernel of `C*`; it lifts to history coordinates `(1,-1)`.

For source metric

```text
K(cross) = [[2,cross],[cross,2]],
```

its exact energy is

```text
q* G q = 4 - 2*cross.
```

Across the reference dephasing trajectory:

```text
cross:                   [2,1,0]
antisymmetric energy:    [0,2,4]
extra null active:       [true,false,false]
```

Thus the antisymmetric direction is null only at full coherence. Partial dephasing releases that null direction and restores a second effective history dimension.

## Symmetric control direction

The symmetric history probe is

```text
s = (0,0,1,1)
  = reobserve + terminate_candidate.
```

It lifts to `(1,1)` and has exact energy

```text
s* G s = 4 + 2*cross.
```

Its trajectory is

```text
[8,6,4],
```

so it remains strictly positive throughout the same three steps.

## Rank and nullity stratification

The recovered history metric determinant numerator is

```text
4 - cross^2.
```

The exact trajectory is

```text
history determinant: [0,3,4]
history rank:        [1,2,2]
candidate Gram rank: [1,2,2]
candidate nullity:   [3,2,2].
```

The two structural null vectors persist at every step.

At full coherence, the additional antisymmetric direction is linearly independent from those two structural vectors, giving a three-dimensional candidate nullspace.

After dephasing, the antisymmetric energy becomes positive and the candidate nullity returns to the two structural directions.

## Independence witness

The three vectors

```text
n1 = (1,0,-1,-1)
n2 = (0,1,-1,1)
q  = (0,0,1,-1)
```

have the nonzero coordinate minor

```text
[[ 1, 0, 0],
 [ 0, 1, 0],
 [-1,-1, 1]]
```

with determinant `1`.

The Lean package proves their linear independence directly.

## Source binding

The certificate binds both:

```text
MemoryOS v0.48 factorization reconstruction certificate
MemoryOS v0.45 complete candidate Gram certificate.
```

It requires exact agreement of:

```text
v0.45 certificate digest
v0.45 candidate-kernel digest
candidate order
history order
factor matrix
trajectory length
dephasing numerators
denominators
all candidate-kernel entries.
```

A re-signed v0.48 trajectory that no longer matches the independently supplied v0.45 source is rejected.

## Fail-closed rejection

The runtime rejects:

```text
source schema substitution
source certificate digest mismatch
v0.48-to-v0.45 certificate mismatch
v0.48-to-v0.45 kernel mismatch
candidate or history support mismatch
factor-matrix substitution
trajectory substitution
non-Hermitian candidate or history metric
incomplete candidate-pair or history-pair support
structural relation not lifted to zero
nonzero structural left or right kernel action
nonzero structural quadratic energy
negative or imaginary history determinant
unexpected rank or nullity trajectory
unexpected antisymmetric or symmetric probe energy
false preservation claim
false authority or mutation claim.
```

## DecisionOS preservation

The source DecisionOS relational surfaces remain unchanged:

```text
relational frontier: [reobserve]
required review:     [continue, hold, reobserve]
dissent review:      [continue]
minority protection: [hold].
```

A null direction is a relation among candidate coordinates. It does not make any candidate dispensable.

Rank recovery is a coherence statement. It is not candidate preference, ranking, or selection.

## Boundary

```text
null relation       != candidate deletion
zero energy         != candidate irrelevance
higher nullity      != pruning permission
rank recovery       != candidate preference
factor quotient     != DecisionOS decision
MemoryOS evidence   != execution authority
runtime validation  != verification result.
```

No ranking, pruning, selection, decision commit, decision receipt, plan synthesis, activation, execution, source mutation, WORLD mutation, verification authority, or truth authority is granted.

## Artifacts

```text
runtime/kuuos_memoryos_candidate_nullspace_dephasing_rank_stratification_certificate_kernel_v0_1.py
scripts/check_planos_memoryos_candidate_nullspace_dephasing_rank_stratification_certificate_kernel_v0_1.py
formal/KUOS/OpenHorizon/MemoryOSCandidateNullspaceDephasingRankStratificationV0_49.lean
formal/KuuOSMemoryOSV0_49.lean
manifests/kuuos_memoryos_candidate_nullspace_dephasing_rank_stratification_certificate_kernel_v0_1.json
runtime/kuuos_current_check.py
```
