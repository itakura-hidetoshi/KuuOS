# MemoryOS v0.44 — observer-relative coherence quadratic evidence DecisionOS handoff certificate v0.1

## Purpose

MemoryOS v0.43 proves that observer-relative temporal-window refinement, coarsening, direct conditioning, and the accepted MemoryOS v0.42 coherence trajectory are exactly equal. MemoryOS v0.44 turns that preserved PSD coherence kernel into exact candidate-specific quadratic evidence for the existing DecisionOS v0.6 relational deliberation field.

```text
MemoryOS v0.43 conditioned PlanOS coherence trajectory
  -> source-bound candidate/history coupling vectors
  -> exact quadratic forms c* K c
  -> candidate-specific coherence evidence trajectories
  -> read-only advisory handoff to DecisionOS v0.6
```

The layer retains every PlanOS history and every DecisionOS candidate. It does not convert coherence evidence into a scalar utility, ranking, pruning, selection, decision receipt, plan synthesis, activation, or execution.

## Exact quadratic evidence

For a retained DecisionOS candidate `d`, a source-bound real integer coupling vector `c_d`, and a MemoryOS-conditioned Hermitian PSD kernel `K_n`, v0.44 computes

```text
E_d(n) = c_d* K_n c_d.
```

Because `K_n` is PSD, every exact numerator is nonnegative. Because `K_n` is Hermitian and the reference coupling vectors are real, the imaginary numerator cancels exactly.

The common kernel-entry denominator is retained at every dephasing step.

## Reference coupling field

The retained MemoryOS history support is

```text
plan-history-a
plan-history-b
```

The complete DecisionOS v0.6 candidate field is coupled as follows:

```text
continue:            [ 1,  1]
hold:                [ 1, -1]
reobserve:           [ 1,  0]
terminate_candidate: [ 0,  1]
```

No coupling vector is zero. Every vector is bound to the complete retained history support.

## Exact evidence trajectories

For the accepted MemoryOS v0.43 final trajectory, the real kernel numerators are

```text
n = 2: [[2,2],[2,2]]
n = 1: [[2,1],[1,2]]
n = 0: [[2,0],[0,2]]
```

The exact candidate evidence numerators are therefore

```text
continue:            [8,6,4]
hold:                [0,2,4]
reobserve:           [2,2,2]
terminate_candidate: [2,2,2]
```

The full-coherence minus fully-dephased contrasts are

```text
continue:             4
hold:                -4
reobserve:            0
terminate_candidate:  0
```

Positive, zero, and negative contrasts coexist. This is an explicit witness that coherence contrast is not a monotone candidate utility and must not be used as a scalar selection shortcut.

## DecisionOS preservation

The source DecisionOS v0.6 relational deliberation receipt remains unchanged:

```text
relational frontier:        [reobserve]
required review candidates: [continue, hold, reobserve]
dissent review candidates:  [continue]
minority protection:        [hold]
retained nonadmissible:      [terminate_candidate]
```

v0.44 attaches exact coherence evidence to all four candidates while preserving those classifications and review obligations exactly.

In particular:

- `continue` retains its dissent-review requirement even though its coherence contrast is positive;
- `hold` retains minority protection even though its contrast is negative;
- `reobserve` remains the relational frontier even though its contrast is zero;
- `terminate_candidate` remains retained and nonadmissible rather than being deleted.

Thus coherence evidence cannot override relational, dissent, minority, admissibility, or review governance.

## Source binding

The certificate binds:

```text
accepted MemoryOS v0.43 certificate digest
MemoryOS v0.43 temporal-window cocycle digest
MemoryOS v0.43 conditioned-kernel digest
accepted DecisionOS v0.6 relational-deliberation receipt digest
complete retained PlanOS history support
complete retained DecisionOS candidate support
exact candidate/history coupling vectors
```

The runtime rejects source substitution, digest substitution, incomplete history support, missing candidates, duplicate candidates, invalid or oversized coefficients, zero coupling vectors, incomplete kernel-pair support, non-Hermitian entries, missing PSD witnesses, and false governance claims.

## Mathlib theorem surface

```text
quadraticEvidence2
coherenceQuadraticEvidence_nonnegative
conditionedCoherenceQuadraticEvidence_nonnegative
reference_continue_quadratic_evidence
reference_hold_quadratic_evidence
reference_reobserve_quadratic_evidence
reference_terminate_quadratic_evidence
reference_coherence_contrasts_are_plural
coherence_evidence_handoff_preserves_support_and_review
coherence_evidence_handoff_grants_no_authority
```

The general nonnegativity theorems are stated for arbitrary finite complex kernels satisfying the existing MemoryOS v0.42 PSD predicate. The four reference trajectories are proved separately in exact integer arithmetic.

## Fail-closed boundaries

```text
quadratic coherence evidence != empirical probability
coherence contrast != scalar utility
positive contrast != selection preference
negative contrast != rejection authority
zero contrast != irrelevance
PSD nonnegativity != plan quality
Hermitian realness != causal truth
candidate/history coupling != candidate identity
MemoryOS evidence handoff != DecisionOS selection
review-set preservation != decision commit
runtime validation != verification result
```

## Artifacts

```text
runtime/kuuos_memoryos_observer_relative_coherence_quadratic_evidence_decisionos_handoff_certificate_kernel_v0_1.py
scripts/check_planos_memoryos_observer_relative_coherence_quadratic_evidence_decisionos_handoff_certificate_kernel_v0_1.py
formal/KUOS/OpenHorizon/MemoryOSObserverRelativeCoherenceQuadraticEvidenceDecisionOSHandoffV0_44.lean
formal/KuuOSMemoryOSV0_44.lean
manifests/kuuos_memoryos_observer_relative_coherence_quadratic_evidence_decisionos_handoff_certificate_kernel_v0_1.json
runtime/kuuos_current_check.py
```
