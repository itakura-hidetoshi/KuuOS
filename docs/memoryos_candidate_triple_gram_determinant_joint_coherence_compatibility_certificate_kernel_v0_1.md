# MemoryOS v0.47 — candidate-triple Gram determinant joint-coherence compatibility

## Purpose

MemoryOS v0.46 certifies every retained candidate pair through the exact Cauchy–Schwarz envelope

```text
|G[i,j]|² <= G[i,i] G[j,j].
```

Those pairwise inequalities are necessary but are not sufficient for three candidate relations to arise from one common positive-semidefinite Gram kernel.

MemoryOS v0.47 adds the missing joint condition. For every ordered candidate triple `(i,j,k)` and every dephasing step, it computes the exact Hermitian `3 × 3` principal minor

```text
det G[i,j,k]
  = Gii Gjj Gkk
    + 2 Re(Gij Gjk Gki)
    - Gii |Gjk|²
    - Gjj |Gki|²
    - Gkk |Gij|².
```

The certificate requires that every such determinant be nonnegative.

For the current two-history candidate Gram lift, the candidate kernel has rank at most two. Therefore every `3 × 3` candidate principal minor is not merely nonnegative but exactly zero.

## Why pairwise bounds are insufficient

Take a real symmetric candidate relation with unit diagonals and signed pair entries

```text
G12 = 1
G23 = 1
G31 = -1.
```

Each pair individually satisfies

```text
|Gij|² = 1 <= 1 · 1.
```

However,

```text
det [[1, 1,-1],
     [1, 1, 1],
     [-1,1, 1]]
  = -4.
```

Thus the three pairwise envelopes are not jointly realizable as a positive-semidefinite Gram relation.

MemoryOS v0.47 rejects exactly this kind of hidden triple inconsistency.

## Actual theorem

The source history kernel is

```text
K(c) = [[2,c],
        [c,2]].
```

For any three candidate coupling vectors

```text
x = (a,b)
y = (p,q)
z = (r,s),
```

define the candidate Gram entries through the v0.45 bilinear lift.

The formal package proves, for arbitrary real `c,a,b,p,q,r,s`,

```text
det Gram_K(c)(x,y,z) = 0.
```

This is an actual polynomial identity, not a finite fixture enumeration. It expresses that three vectors lifted from a two-dimensional history space are linearly dependent at the Gram level.

The same exact identity is also proved over integer arithmetic for the runtime numerator surface.

## Complete ordered-triple support

Candidate order:

```text
continue
hold
reobserve
terminate_candidate
```

For every dephasing step, the runtime retains

```text
4³ = 64 ordered candidate triples.
```

Of these,

```text
4 · 3 · 2 = 24
```

have three distinct candidate ids. The remaining 40 contain a repeated candidate id and are retained as degenerate ordered triples rather than deleted.

Each triple record binds:

```text
first, second, and third candidate ids
whether all three ids are distinct
all three diagonal numerators
all three oriented complex pair numerators
cyclic product Gij Gjk Gki
real and imaginary cyclic-product numerators
twice the cyclic real contribution
diagonal cubic term
three magnitude-square subtraction terms
exact 3 × 3 determinant numerator and denominator
principal-minor nonnegativity witness
rank-two determinant-zero witness
joint pair-envelope compatibility witness
```

## Exact reference trajectories

For

```text
continue → reobserve → terminate_candidate
```

the cyclic-product real numerators are

```text
[32, 9, 0].
```

The twice-cyclic contributions are

```text
[64, 18, 0].
```

The diagonal cubic terms are

```text
[32, 24, 16].
```

After subtracting the three exact pair-magnitude terms, the determinant trajectory is

```text
[0, 0, 0].
```

For the sign-sensitive triple

```text
hold → reobserve → terminate_candidate
```

the cyclic-product real numerators remain visibly signed:

```text
[0, -1, 0].
```

The determinant trajectory is still

```text
[0, 0, 0].
```

The negative cyclic product is preserved as relational information. It is not interpreted as collective rejection, preference, utility, or consensus.

## Source binding

The v0.47 runtime recomputes and binds:

```text
accepted MemoryOS v0.46 certificate digest
v0.46 candidate-pair envelope digest
v0.45 certificate digest
v0.45 candidate Gram kernel digest
v0.43 and v0.44 source certificate digests
complete candidate order
complete dephasing trajectory
all ordered pair entries used by every triple
```

It independently revalidates each v0.46 pair record, including:

```text
Hermitian symmetry
real nonnegative diagonals
Cauchy–Schwarz margin
zero-diagonal coherence extinction
reduced normalized coherence square
complete ordered-pair support
```

## Fail-closed rejection

The runtime rejects:

```text
source schema substitution
source certificate digest mismatch
source pair-envelope digest mismatch
incomplete or duplicate pair support
non-Hermitian source pairs
inconsistent diagonal binding
incorrect magnitude, margin, or normalized fraction arithmetic
nondecreasing dephasing sequence
negative candidate-triple principal minor
nonzero rank-two triple determinant
incomplete ordered-triple support
false preservation claims
promoted decision or execution authority
```

The checker includes two separate higher-order tampering cases:

1. a pairwise-valid mutation that makes a triple determinant negative;
2. a pairwise-valid mutation that keeps the triple determinant positive but nonzero, violating the exact rank-two source relation.

## DecisionOS preservation

The DecisionOS v0.6 relational surfaces remain unchanged:

```text
relational frontier: [reobserve]
required review:     [continue, hold, reobserve]
dissent review:      [continue]
minority protection: [hold]
```

No triple relation may remove or override any candidate in these sets.

## Boundary

```text
joint compatibility != candidate consensus
rank-two saturation != agreement
cyclic product       != group preference
negative cycle       != collective rejection
zero determinant     != duplicate candidates
principal minor      != scalar utility
triple support       != coalition formation
MemoryOS witness     != DecisionOS decision
runtime validation   != verification result
```

No candidate ranking, pruning, selection, decision commit, decision receipt, plan synthesis, activation, execution, source mutation, WORLD mutation, verification authority, or truth authority is granted.

## Artifacts

```text
runtime/kuuos_memoryos_candidate_triple_gram_determinant_joint_coherence_compatibility_certificate_kernel_v0_1.py
scripts/check_planos_memoryos_candidate_triple_gram_determinant_joint_coherence_compatibility_certificate_kernel_v0_1.py
formal/KUOS/OpenHorizon/MemoryOSCandidateTripleGramDeterminantJointCoherenceCompatibilityV0_47.lean
formal/KuuOSMemoryOSV0_47.lean
manifests/kuuos_memoryos_candidate_triple_gram_determinant_joint_coherence_compatibility_certificate_kernel_v0_1.json
runtime/kuuos_current_check.py
```
