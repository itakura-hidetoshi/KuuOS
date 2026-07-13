# MemoryOS v0.48 — two-history candidate Gram factorization reconstruction

## Purpose

MemoryOS v0.47 established joint three-candidate compatibility by showing that every `3 × 3` candidate principal minor is exactly zero. That proves rank at most two indirectly through determinants.

MemoryOS v0.48 replaces the determinant-only observation with an explicit factorization witness for the complete four-candidate kernel.

The fixed candidate-to-history factor matrix is

```text
C = [[ 1,  1],   continue
     [ 1, -1],   hold
     [ 1,  0],   reobserve
     [ 0,  1]]   terminate_candidate
```

For every partial-dephasing step, the full candidate kernel is reconstructed as

```text
G = C K C*
```

from the recovered two-history metric block `K`.

## Recovered history metric

The two coordinate anchors are the source-defined coupling rows

```text
reobserve           = [1,0]
terminate_candidate = [0,1].
```

Their `2 × 2` candidate principal block is therefore the complete history metric:

```text
K00 = G[reobserve,reobserve]
K01 = G[reobserve,terminate_candidate]
K10 = G[terminate_candidate,reobserve]
K11 = G[terminate_candidate,terminate_candidate].
```

Across the reference dephasing trajectory, the exact numerator matrices are

```text
full coherence:     [[2,2],[2,2]]
partial dephasing:  [[2,1],[1,2]]
full dephasing:     [[2,0],[0,2]].
```

The common rational denominator remains source-bound.

## Complete reconstruction

For candidate coordinates `x=(a,b)` and `y=(p,q)`, v0.48 reconstructs

```text
G[x,y]
  = a K00 p
  + a K01 q
  + b K10 p
  + b K11 q.
```

All `4 × 4 = 16` ordered candidate entries are checked independently at each of the three dephasing steps.

The runtime emits the source entry, reconstructed entry, both factor rows, and an exact equality witness for every ordered candidate pair.

## Row and column relations

The factor matrix gives exact relations, not approximations:

```text
continue = reobserve + terminate_candidate
hold     = reobserve - terminate_candidate.
```

Consequently, for every candidate `j`,

```text
G[continue,j] = G[reobserve,j] + G[terminate_candidate,j]
G[hold,j]     = G[reobserve,j] - G[terminate_candidate,j].
```

The corresponding column relations are also checked exactly.

These identities retain the negative partial-dephasing relation in the `hold` row rather than suppressing it.

## Rank witness

The complete candidate kernel factors through a two-dimensional history space. Therefore

```text
rank G <= 2.
```

The runtime validates this through the explicit factorization and additionally computes the exact complex Leibniz determinant of the complete `4 × 4` numerator matrix. The determinant trajectory is

```text
[0,0,0].
```

The Lean package proves the same determinant identity for arbitrary integer source cross term, not only for the three reference values.

## Binding to v0.47

The v0.48 certificate accepts both:

```text
MemoryOS v0.47 joint triple certificate
MemoryOS v0.45 complete candidate Gram certificate.
```

It requires the v0.45 certificate digest and candidate-kernel digest recorded by v0.47 to match the supplied v0.45 source exactly.

Every one of the `64` ordered v0.47 triple records at each step is rebound to the same candidate entries reconstructed from the explicit factorization. Thus the pair, triple, and full-kernel surfaces share one common algebraic witness.

## Fail-closed rejection

The runtime rejects:

```text
source schema substitution
source certificate digest mismatch
v0.47-to-v0.45 digest or kernel mismatch
candidate or history support mismatch
non-two-dimensional history factor space
non-reference candidate factor rows
incomplete or duplicate candidate-pair support
non-Hermitian candidate kernels
imaginary or negative diagonal entries
nondecreasing dephasing sequence
candidate entry not reproduced by C K C*
row or column factor relation failure
nonzero complete 4 × 4 determinant
v0.47 triple record not bound to the reconstructed kernel
false preservation or authority claims
```

The checker includes independent tampering cases for coupling substitution, factorization-breaking kernel mutation, and a re-signed v0.47 triple record that remains internally determinant-zero but no longer matches the source kernel.

## DecisionOS preservation

The DecisionOS v0.6 relational surfaces remain unchanged:

```text
relational frontier: [reobserve]
required review:     [continue, hold, reobserve]
dissent review:      [continue]
minority protection: [hold]
```

The coordinate anchors are algebraic history basis rows. They are not preferred candidates, selected candidates, representatives, or a relational order.

## Boundary

```text
factor row             != candidate priority
history anchor         != representative selection
rank-two factorization != candidate consensus
row dependence         != candidate redundancy
zero determinant       != permission to prune
kernel reconstruction  != decision commit
MemoryOS witness       != DecisionOS decision
runtime validation     != verification result
```

No candidate ranking, pruning, selection, decision commit, decision receipt, plan synthesis, activation, execution, source mutation, WORLD mutation, verification authority, or truth authority is granted.

## Artifacts

```text
runtime/kuuos_memoryos_two_history_candidate_gram_factorization_reconstruction_certificate_kernel_v0_1.py
scripts/check_planos_memoryos_two_history_candidate_gram_factorization_reconstruction_certificate_kernel_v0_1.py
formal/KUOS/OpenHorizon/MemoryOSTwoHistoryCandidateGramFactorizationReconstructionV0_48.lean
formal/KuuOSMemoryOSV0_48.lean
manifests/kuuos_memoryos_two_history_candidate_gram_factorization_reconstruction_certificate_kernel_v0_1.json
runtime/kuuos_current_check.py
```
