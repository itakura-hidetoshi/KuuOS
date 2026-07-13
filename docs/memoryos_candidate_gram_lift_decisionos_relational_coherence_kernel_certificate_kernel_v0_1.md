# MemoryOS v0.45 — candidate Gram lift to DecisionOS relational coherence kernel

## Purpose

MemoryOS v0.44 produces exact candidate-specific quadratic coherence evidence. MemoryOS v0.45 lifts the accepted MemoryOS v0.43 history-space PSD kernel through the complete v0.44 candidate/history coupling field:

```text
history-space kernel K
candidate/history coupling field C
  -> candidate-space kernel G = C K C*
  -> complete DecisionOS candidate-pair coherence field
```

Every PlanOS history, every DecisionOS candidate, and every ordered candidate pair is retained.

## Exact reference candidate kernels

Candidate order:

```text
continue
hold
reobserve
terminate_candidate
```

At dephasing numerators `2, 1, 0`, the exact real numerator matrices are:

```text
n = 2
[[8,0,4,4],
 [0,0,0,0],
 [4,0,2,2],
 [4,0,2,2]]

n = 1
[[6,0,3,3],
 [0,2,1,-1],
 [3,1,2,1],
 [3,-1,1,2]]

n = 0
[[4,0,2,2],
 [0,4,2,-2],
 [2,2,2,0],
 [2,-2,0,2]]
```

The diagonal trajectories are exactly the accepted v0.44 quadratic evidence:

```text
continue:            [8,6,4]
hold:                [0,2,4]
reobserve:           [2,2,2]
terminate_candidate: [2,2,2]
```

Representative pair trajectories include:

```text
continue–hold:                [0,0,0]
continue–reobserve:           [4,3,2]
hold–reobserve:               [0,1,2]
hold–terminate_candidate:     [0,-1,-2]
reobserve–terminate_candidate:[2,1,0]
```

Negative off-diagonal coherence is allowed while every diagonal remains nonnegative. Therefore the candidate Gram kernel is not a candidate order, scalar utility, or selection rule.

## Theorem surface

```text
liftCandidateVector
candidateGramLift
candidateGramLift_diagonal_eq_quadraticForm
candidateGramLift_quadraticForm
candidateGramLift_preserves_positiveSemidefinite
candidateGramLift_diagonal_nonnegative
candidateGramEntry2
reference_continue_candidate_gram_row
reference_hold_candidate_gram_row
reference_reobserve_terminate_pair
candidate_gram_lift_preserves_support_and_review
candidate_gram_lift_grants_no_authority
```

The central identity is

```text
Q_(C K C*)(x) = Q_K(C* x)
```

in the row-vector convention used by the runtime. Hence a PSD history kernel induces a PSD candidate kernel. Its diagonal is definitionally the v0.44 quadratic evidence.

## Source binding

The certificate binds:

```text
accepted MemoryOS v0.43 certificate digest
accepted MemoryOS v0.44 certificate digest
v0.43 conditioned history-kernel digest
v0.44 quadratic-evidence input digest
complete retained history support
complete retained DecisionOS candidate support
exact candidate/history coupling field
```

The runtime rejects source substitution, digest mismatch, incomplete history or candidate support, duplicate pairs, non-Hermitian source kernels, missing PSD witnesses, diagonal disagreement with v0.44, and false governance claims.

## DecisionOS preservation

The following source fields remain unchanged:

```text
relational frontier:        [reobserve]
required review:            [continue, hold, reobserve]
dissent review:             [continue]
minority protection:        [hold]
```

Pairwise coherence does not override admissibility, review, dissent, minority protection, or relational deliberation.

## Boundary

```text
candidate Gram kernel != relational order
pairwise coherence != scalar utility
off-diagonal sign != preference
PSD != plan quality
candidate-pair field != selection
MemoryOS lift != DecisionOS decision
runtime validation != verification result
```

No candidate ranking, pruning, selection, decision commit, receipt issuance, plan synthesis, activation, execution, source mutation, WORLD mutation, verification authority, or truth authority is granted.

## Artifacts

```text
runtime/kuuos_memoryos_candidate_gram_lift_decisionos_relational_coherence_kernel_certificate_kernel_v0_1.py
scripts/check_planos_memoryos_candidate_gram_lift_decisionos_relational_coherence_kernel_certificate_kernel_v0_1.py
formal/KUOS/OpenHorizon/MemoryOSCandidateGramLiftDecisionOSRelationalCoherenceKernelV0_45.lean
formal/KuuOSMemoryOSV0_45.lean
manifests/kuuos_memoryos_candidate_gram_lift_decisionos_relational_coherence_kernel_certificate_kernel_v0_1.json
runtime/kuuos_current_check.py
```
