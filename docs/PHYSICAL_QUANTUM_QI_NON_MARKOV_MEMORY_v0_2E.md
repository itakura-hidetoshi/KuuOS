# Physical Quantum Qi Non-Markov Memory v0.2E

Status: design-baseline-candidate  
Root: Physical Quantum Qi v0.2 deepening  
Policy: additive-only / overwrite-forbidden / non-authoritative / non-execution

## 1. Purpose

This document fixes Qi memory as a primary non-Markovian structure.

Qi is not determined by a current scalar state and is not semantically reducible
to a Markov process.  Qi is a history-bearing operator-valued flow whose current,
leak, transport, and recoverability depend on admissible past history, boundary
crossings, observation burden, holonomy, rollback, recovery, and unresolved
residue.

Canonical statement:

```text
Qi is fundamentally non-Markovian.
Markov reduction is forbidden as Qi semantics.
Finite-window access is allowed only as history-preserving projection.
```

## 2. Canonical Qi non-Markov current

The Qi current is not a function of the current state alone:

```text
J_Qi^mu(t) != J_Qi^mu(Qi(t))
```

The v0.2E canonical form is:

```text
J_Qi^mu(t)
=
J_bare^mu(t)
+ int_{tau <= t} K_Qi^{mu nu}(t,tau) X_nu(tau) d tau
+ int_{gamma <= t} H_Qi^{mu nu}(gamma,t) dU_gamma
+ R_Qi,mem^mu(t)
```

where:

```text
K_Qi(t,tau)      = Qi history kernel
X(tau)           = past state, leak, observation, boundary, repair, rollback data
H_Qi(gamma,t)    = IndraNet path-history / holonomy-history kernel
U_gamma          = gauge transport along path gamma
R_Qi,mem(t)      = compression, coarse-graining, unresolved memory residue
```

This means Qi flow carries:

```text
current state
boundary history
leak history
observation history
holonomy history
recovery history
rollback history
lock-in history
unresolved residue
```

## 3. Memory kernel decomposition

The Qi memory root is:

```text
M_Qi(t)
=
(
  K_body,
  K_boundary,
  K_leak,
  K_observation,
  K_holonomy,
  K_recovery,
  K_rollback,
  K_lockin,
  K_residue
)
```

Component meanings:

```text
K_body        internal body/system history
K_boundary    membrane and boundary-crossing history
K_leak        leak history
K_observation measurement and observation-burden history
K_holonomy    IndraNet gauge-transport twist history
K_recovery    repair and recovery history
K_rollback    rollback and failed-repair history
K_lockin      phase-lock and fixation history
K_residue     unresolved residue and tail debt
```

Two Qi states with the same apparent current value are not equivalent if their
memory kernels differ.

## 4. Forbidden Markov semantics

The following is forbidden as Qi semantics:

```text
Qi(t + dt) = F(Qi(t), u(t))
```

or any equivalent current-state-only replacement.

Forbidden claims:

```text
current-state-only Qi identity
current-state-only recoverability
current-state-only transport safety
Markov snapshot as FullPathQi
Markov chart as semantic substitute
memory compression as deletion
fresh valid path erasing holonomy history
repair success erasing rollback history
```

A Markov-like implementation may be used only as an external computational cache
if it is explicitly non-authoritative and cannot replace the non-Markov memory
root.

## 5. Finite-window projection is not Markov reduction

Finite-window access is allowed only as a history-preserving projection:

```text
Qi_Window(t; L)
=
Pi_L { Qi(tau), K_Qi(t,tau), residue(tau), tau in [t-L,t] }
```

Required fields for any finite-window projection:

```text
history_window_L
kernel_tail_bound
discarded_tail_residue
holonomy_tail_residue
boundary_leak_tail_residue
observation_tail_burden
recovery_tail_debt
rollback_tail_debt
lockin_tail_residue
```

The discarded tail must remain visible through tail residue.  A finite window is
therefore a partial observation of the non-Markov root, not a replacement of it.

## 6. Non-Markov recoverability

Recoverability is history-dependent:

```text
delta_rec(t)
=
C_recovery(t | M_Qi[0,t])
-
D_recovery(t | M_Qi[0,t])
```

Past leak, observation burden, lock-in, holonomy residue, failed repair, and
rollback history can change delta_rec even when the current apparent state is
unchanged.

Therefore:

```text
current-state-only recovery judgment is forbidden
positive local recovery does not erase past recovery debt
rollback history remains visible after repair
```

## 7. Non-Markov IndraNet transport

IndraNet transport is also history-bearing:

```text
U_Gamma[0,t]
=
P exp int_{Gamma[0,t]} A_mu dx^mu
```

Holonomy memory:

```text
W(C; history)
=
Tr P exp oint_{C[0,t]} A_mu dx^mu
```

A new valid path may reduce future residue but cannot erase prior holonomy
history.

Required transport memory visibility:

```text
scope_drift_history
holonomy_residue_history
component_transport_residue_history
path_order_history
boundary_crossing_history
```

## 8. Memory compression rule

Compression is allowed only as constrained projection:

```text
M_Qi(t) -> Pi_compress M_Qi(t)
```

Compression must not delete:

```text
unresolved conflict
boundary leak history
holonomy residue
scope drift
recovery failure
rollback history
observation burden
authority boundary
```

Compressed Qi memory cannot replace the source history.  It can only point to it
or preserve a bounded projection with visible residual debt.

## 9. Handoff rule

Qi non-Markov memory may support:

```text
PlanOS.transport_candidate
MemoryOS.recordable_history_candidate
ReflectionOS.residue_analysis_candidate
BeliefOS.observation_candidate
DecisionOS.safety_evaluable_candidate
```

It grants no:

```text
execution authority
commit authority
belief root commit authority
memory overwrite authority
world root rewrite authority
proof authority
ontology authority
truth authority
clinical authority
safety override authority
```

## 10. Locked invariants

```text
Qi memory is primary.
Qi is non-Markovian by definition.
Markov reduction is forbidden as Qi semantics.
Finite-window projection is allowed only as history-preserving projection.
Discarded history must leave visible tail residue.
Holonomy history cannot be erased.
Boundary leak history cannot be erased.
Observation burden cannot be erased.
Rollback history cannot be erased.
Recovery failure cannot be erased.
Current-state-only recovery judgment is forbidden.
Current-state-only transport judgment is forbidden.
Qi memory grants no execution authority.
Qi memory grants no truth authority.
Qi memory cannot overwrite source history.
Compressed Qi memory cannot replace source history.
```

## 11. One-sentence definition

```text
Qi is a non-Markovian operator-valued flow whose memory kernel preserves boundary
crossing, leak, observation burden, holonomy, recovery, rollback, lock-in, and
unresolved residue as primary state, not as secondary approximation.
```
