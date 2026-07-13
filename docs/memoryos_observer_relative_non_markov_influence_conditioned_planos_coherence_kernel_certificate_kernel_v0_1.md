# MemoryOS v0.42 — observer-relative non-Markov influence-conditioned PlanOS coherence kernel certificate v0.1

## Purpose

MemoryOS v0.41 returns an exact candidate-specific history influence to every retained PlanOS v1.23 history. MemoryOS v0.42 connects that influence to the actual PlanOS partial-dephasing coherence kernel without ranking, pruning, selecting, activating, or executing any history.

```text
MemoryOS v0.41 complete observer-relative influence handoff
  -> exact action numerator modulo four
  -> candidate-specific Gaussian unit phase
  -> diagonal phase congruence of every PlanOS v1.23 kernel step
  -> future-only advisory memory-conditioned coherence kernel
```

The deformation is algebraic and read-only. It does not reinterpret the influence functional as causal truth or the mod-four phase as physical time.

## Exact deformation

For each retained history `p`, let

```text
m_p = S_p^memory mod 4
u_p = i^(m_p) in {1, i, -1, -i}.
```

For a PlanOS v1.23 partial-dephasing kernel step `K(n)`, define

```text
K_memory(n)[p,q] = u_p K(n)[p,q] conjugate(u_q).
```

Equivalently,

```text
K_memory(n) = D_memory K(n) D_memory*.
```

A window-only counterfactual is computed from

```text
m_p^window = S_p^window mod 4.
```

Both kernels preserve every history and every ordered history pair. No amplitude magnitude is changed and no entry is deleted.

## Structural theorem

For a finite complex kernel `K`, phase vector `u`, and test vector `x`,

```text
x* (D K D*) x
  = (D* x)* K (D* x).
```

Therefore a positive-semidefinite source kernel remains positive semidefinite after diagonal phase congruence. Hermitian symmetry is preserved. Because every `u_p` has unit norm, every diagonal entry is unchanged.

The Lean package proves these statements for arbitrary finite index types and also proves exact Gaussian-integer reference values.

## Reference witness

The v0.41 fixture gives:

```text
plan-history-a:
  conditioned action numerator = 54
  window-only action numerator = 45
  full phase = 2
  window-only phase = 1

plan-history-b:
  conditioned action numerator = 29
  window-only action numerator = 27
  full phase = 1
  window-only phase = 3
```

The PlanOS v1.23 source fixture has two histories in distinct coherence blocks and dephasing denominator two. At the fully coherent step, the source off-diagonal entry is

```text
K[a,b] = -2i.
```

The complete non-Markov memory deformation gives

```text
u_a = -1
u_b = i
K_memory[a,b] = 2.
```

The suffix-window-only deformation gives

```text
u_a^window = i
u_b^window = -i
K_window[a,b] = 2i.
```

Thus the visible discarded tail changes the actual coherence kernel:

```text
2 != 2i.
```

At dephasing numerators two and one, both ordered off-diagonal entries change. At numerator zero, cross-block coherence is already zero, so no false tail effect is claimed there.

Reference result:

```text
tail-sensitive kernel entries = 4
tail-sensitive dephasing numerators = [2, 1]
```

## Exact invariants

Every conditioned step verifies:

```text
Hermitian symmetry = preserved
diagonal normalization = preserved
positive-semidefinite witness = preserved by diagonal congruence
history count = preserved
ordered history-pair support = preserved
kernel denominator = preserved
dephasing trajectory support = preserved
```

The deformation changes phase relationships only. It does not perform amplitude reweighting.

## Source binding

The v0.42 kernel binds:

```text
accepted MemoryOS v0.41 certificate digest
MemoryOS v0.41 influence-handoff digest
MemoryOS v0.41 complete candidate influence profile
accepted PlanOS v1.23 input digest
PlanOS v1.23 retained history order
PlanOS v1.23 exact partial-dephasing trajectory
PlanOS v1.23 Hermitian and convex-Gram PSD witnesses
```

The MemoryOS receipt and PlanOS kernel receipt must contain the same PlanOS v1.23 input digest and the same ordered history support.

## Fail-closed validation

The checker rejects:

```text
invalid source schema or acceptance
MemoryOS/PlanOS input-digest substitution
history support or order mismatch
candidate influence identity failure
conditioned/window/tail action arithmetic mismatch
mixed action denominators
missing or duplicate kernel pairs
kernel history outside the retained support
non-Hermitian source entries
non-real diagonal entries
invalid dephasing denominator or trajectory order
missing source convex-Gram PSD witness
incorrect memory phase or conditioned entry claim
hidden tail effect
history pruning or ranking
representative selection or plan selection
decision commit, activation, or execution
source mutation or persistent WORLD mutation
verification or truth-authority claim
```

## Mathlib theorem surface

```text
gaussianMul
gaussianConj
gaussianUnit
gaussianPhaseDeform
phaseDeformMatrix
quadraticForm
IsHermitianKernel
IsPositiveSemidefiniteKernel
phaseDeform_quadraticForm
phaseDeform_preserves_positiveSemidefinite
phaseDeform_preserves_hermitian
phaseDeform_preserves_diagonal
reference_memory_action_phases
reference_full_memory_offdiagonal
reference_window_only_offdiagonal
reference_tail_changes_coherence_kernel
reference_diagonal_preserved
coherence_handoff_preserves_kernel_structure
coherence_handoff_grants_no_authority
```

## Fixed boundaries

```text
memory-conditioned phase != physical time
mod-four encoding != complete physical phase dynamics
influence functional != causal truth
kernel deformation != candidate ranking
phase change != amplitude reweighting
Hermitian preservation != empirical validity
PSD witness != plan quality
nonzero off-diagonal entry != activation preference
tail-sensitive coherence != plan selection
all histories retained != all histories activated
future-only advisory kernel != decision commit
runtime validation != verification result
```

## Artifacts

```text
runtime/kuuos_memoryos_observer_relative_non_markov_influence_conditioned_planos_coherence_kernel_schema_support_v0_1.py
runtime/kuuos_memoryos_observer_relative_non_markov_influence_conditioned_planos_coherence_kernel_algebra_support_v0_1.py
runtime/kuuos_memoryos_observer_relative_non_markov_influence_conditioned_planos_coherence_kernel_certificate_support_v0_1.py
runtime/kuuos_memoryos_observer_relative_non_markov_influence_conditioned_planos_coherence_kernel_certificate_kernel_v0_1.py
scripts/check_memoryos_observer_relative_non_markov_influence_conditioned_planos_coherence_kernel_certificate_kernel_v0_1.py
formal/KUOS/OpenHorizon/MemoryOSObserverRelativeNonMarkovInfluenceConditionedPlanOSCoherenceKernelV0_42.lean
formal/KuuOSMemoryOSV0_42.lean
manifests/kuuos_memoryos_observer_relative_non_markov_influence_conditioned_planos_coherence_kernel_certificate_kernel_v0_1.json
runtime/kuuos_current_check.py
```
