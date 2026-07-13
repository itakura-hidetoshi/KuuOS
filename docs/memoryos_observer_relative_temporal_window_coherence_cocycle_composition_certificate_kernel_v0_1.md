# MemoryOS v0.43 — observer-relative temporal-window coherence cocycle composition certificate v0.1

## Purpose

MemoryOS v0.41 converts the complete observer-relative record ledger into exact candidate-specific history influence. MemoryOS v0.42 maps the resulting conditioned action numerator to a Gaussian unit phase and deforms every PlanOS v1.23 coherence kernel by diagonal phase congruence. MemoryOS v0.43 proves that this deformation is coherent under chronological temporal-window refinement and coarsening.

```text
MemoryOS v0.41 complete record-bound influence
  -> source-bound temporal segments
  -> candidate-specific segment phases in Z4
  -> chronological diagonal phase congruences
  -> refined / coarse / direct cocycle equality
  -> exact equality with accepted MemoryOS v0.42 trajectory
```

This layer remains read-only and future-only. It composes advisory coherence deformations; it does not rank, select, activate, execute, or mutate any history.

## Temporal segmentation

The reference MemoryOS v0.41 ledger is retained in source order:

```text
record-tail      observer-alpha  discarded-tail
record-window-a  observer-alpha  retained-window, lag weight 3
record-window-b  observer-beta   retained-window, lag weight 2
```

Each v0.43 temporal segment binds exactly one source record. The flattened segment record order must equal the complete v0.41 record order. Segment observer identity, sequence position, kind, and lag weight are recomputed from the source receipt rather than trusted from claims.

The alpha-to-beta boundary requires the source-bound translation:

```text
translation-alpha-beta
```

and requires its translation residue to remain visible. Same-observer transitions must not invent a translation.

## Exact segment components

The ordered component support remains:

```text
body
boundary
leak
observation
holonomy
recovery
rollback
lockin
residue
```

The source-bound weighted segment components are:

```text
tail-segment:
  holonomy = 1
  rollback = 1
  residue = 2

window-segment-a:
  body = 3
  observation = 6
  residue = 3

window-segment-b:
  boundary = 2
  leak = -2
  holonomy = 2
  residue = 4
```

Their sum exactly reproduces the v0.41 weighted-window plus discarded-tail decomposition.

## Candidate-specific temporal influence

For each PlanOS history `p`, each temporal segment `s` contributes

```text
I[p,s] = <g_p, weighted_components(s)>.
```

The reference values are:

```text
plan-history-a:
  base action numerator = 11
  segment influences = [9, 18, 16]
  segment phases mod 4 = [1, 2, 0]
  total influence = 43
  conditioned action numerator = 54
  conditioned phase = 2

plan-history-b:
  base action numerator = 20
  segment influences = [2, 3, 4]
  segment phases mod 4 = [2, 3, 0]
  total influence = 9
  conditioned action numerator = 29
  conditioned phase = 1
```

The checker independently recomputes the complete v0.41 candidate influence profile and requires exact equality with the accepted source receipt.

## Coherence cocycle

For a phase profile `u`, define

```text
Phi_u(K) = D_u K D_u*.
```

For chronological phase profiles `u` then `v`, v0.43 proves

```text
Phi_v(Phi_u(K)) = Phi_(v * u)(K).
```

Pointwise phase multiplication is associative, so three chronological temporal segments satisfy

```text
Phi_w(Phi_v(Phi_u(K)))
  = Phi_(w * (v * u))(K)
  = Phi_((w * v) * u)(K).
```

This is the exact cocycle/composition law used by the runtime and formal package.

## Refinement and coarsening

The refined route applies the following phase profiles in chronological order:

```text
base action
  -> tail-segment
  -> window-segment-a
  -> window-segment-b
```

The coarse route applies:

```text
base action
  -> complete tail
  -> combined retained window
```

The direct route applies the final conditioned phase from v0.41 in one step.

The accepted v0.42 route supplies the already conditioned PlanOS trajectory.

v0.43 requires exact equality:

```text
refined final trajectory
  = coarse final trajectory
  = direct conditioned trajectory
  = accepted MemoryOS v0.42 conditioned trajectory.
```

This equality is checked entrywise for every dephasing step and every ordered history pair.

## Reference kernel trajectory

At the fully coherent PlanOS step, the source off-diagonal entry is

```text
K[a,b] = -2i.
```

The refined chronological sequence is:

```text
source:            -2i
base action:       -2
complete tail:      2i
window segment a:   2
window segment b:   2
```

The final value equals the direct v0.42 conditioned entry.

`window-segment-b` is an explicit nonzero but phase-neutral witness:

```text
plan-history-a influence = 16 != 0, 16 mod 4 = 0
plan-history-b influence = 4  != 0,  4 mod 4 = 0
```

Thus phase neutrality in the bounded Z4 encoding does not imply erased history or zero source influence.

## Structural preservation

Every refined, coarse, and direct stage preserves:

```text
Hermitian symmetry
all diagonal entries
positive-semidefinite witness by repeated diagonal phase congruence
complete PlanOS history support
complete ordered history-pair support
kernel entry denominator
dephasing trajectory order
```

The composition changes phase relations only. It performs no amplitude reweighting and deletes no kernel entry.

## Source binding

The v0.43 certificate binds:

```text
accepted MemoryOS v0.41 certificate digest
MemoryOS v0.41 influence handoff digest
MemoryOS v0.40 record-ledger digest
MemoryOS v0.40 temporal-cycle digest
complete v0.41 record IDs, digests, observers, and translations
complete v0.41 candidate couplings and influence profile
accepted MemoryOS v0.42 certificate digest
MemoryOS v0.42 source and conditioned kernel digests
accepted PlanOS v1.23 input digest
PlanOS v1.23 complete partial-dephasing trajectory
```

Substitution of any bound source, history support, record order, observer, translation, or kernel digest is rejected.

## Fail-closed validation

The checker rejects at least:

```text
invalid source schema or non-accepted source
MemoryOS v0.41 / v0.42 / PlanOS digest substitution
v0.41 candidate influence arithmetic mismatch
record ID, digest, order, or observer substitution
segment record coverage or order mismatch
segment count differing from source record count
segment binding to more than one source record
incorrect discarded-tail or retained-window classification
incorrect lag weight
hidden source translation residue
missing observer-transition translation
invented same-observer translation
hidden observation/backaction
non-Hermitian source kernel
missing PSD or structural witness
source kernel digest mismatch
conditioned kernel digest mismatch
refinement/coarsening inconsistency
direct cocycle inconsistency
v0.42 trajectory inconsistency
history pruning or ranking
representative selection or plan selection
decision commit, activation, or execution
MemoryOS, PlanOS, or WORLD mutation
verification-result or truth-authority claim
```

## Mathlib theorem surface

```text
composePhase
phaseDeformMatrix_compose
composePhase_assoc
phaseDeformMatrix_three_compose
phaseDeformMatrix_refinement_coarsening
three_phase_composition_preserves_positiveSemidefinite
three_phase_composition_preserves_hermitian
three_phase_composition_preserves_diagonal
gaussianSequentialDeform
reference_temporal_segment_phases
reference_nonzero_phase_neutral_segment
reference_refined_sequence_equals_direct
reference_coarse_sequence_equals_direct
reference_refined_and_coarse_offdiagonal
cocycle_certificate_preserves_temporal_and_kernel_structure
cocycle_certificate_grants_no_authority
```

The general theorems are stated for arbitrary finite complex kernels. Exact Gaussian-integer reference values are proved separately.

## Fixed boundaries

```text
temporal segmentation != history replacement
window refinement != history pruning
window coarsening != information deletion
phase-neutral segment != zero historical influence
cocycle equality != causal truth
observer translation compatibility != observer equivalence
Hermitian/PSD preservation != empirical validity
kernel coherence != plan quality
history support preservation != plan selection
future-only advisory composition != decision commit
runtime validation != verification result
```

## Artifacts

```text
runtime/kuuos_memoryos_observer_relative_temporal_window_coherence_cocycle_composition_schema_support_v0_1.py
runtime/kuuos_memoryos_observer_relative_temporal_window_coherence_cocycle_composition_algebra_support_v0_1.py
runtime/kuuos_memoryos_observer_relative_temporal_window_coherence_cocycle_composition_certificate_support_v0_1.py
runtime/kuuos_memoryos_observer_relative_temporal_window_coherence_cocycle_composition_certificate_kernel_v0_1.py
scripts/check_planos_memoryos_observer_relative_temporal_window_coherence_cocycle_composition_certificate_kernel_v0_1.py
formal/KUOS/OpenHorizon/MemoryOSObserverRelativeTemporalWindowCoherenceCocycleCompositionV0_43.lean
formal/KuuOSMemoryOSV0_43.lean
manifests/kuuos_memoryos_observer_relative_temporal_window_coherence_cocycle_composition_certificate_kernel_v0_1.json
runtime/kuuos_current_check.py
```
