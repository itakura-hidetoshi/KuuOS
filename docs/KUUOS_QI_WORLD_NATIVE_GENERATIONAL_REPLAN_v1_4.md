# KuuOS Qi–WORLD Native Generational Replan v1.4

## Purpose

v1.3 closed one native Belief-to-Learn cycle. v1.4 closes the next bounded
inter-generation edge without creating a replacement kernel:

```text
native LearnOS future-only delta
→ PlanOS-owned native replan
→ Qi-conditioned non-Markov candidate field
→ native DecisionOS
→ native plural deliberation
→ native Wa review
→ committed next-PLAN basis
→ extended Qi lineage
→ read-only next WORLD projection
```

The next plan basis is not active execution. It becomes usable only in the
next cycle and still requires the ordinary PlanOS, Governance, ActOS, and
external-host-authority boundaries.

## Reused native kernels

v1.4 directly reuses:

- the v1.3 native Belief-to-Learn receipt;
- PlanOS v0.2 Qi-conditioned non-Markov replan;
- DecisionOS v0.1 relational deliberation;
- DecisionOS v0.2 plural deliberation;
- DecisionOS v0.3 Wa review;
- the existing Qi Process Tensor evaluator;
- the read-only WORLD projection boundary.

No `ReplanOS` is introduced. Replan ownership remains with PlanOS.

## Source bindings

```text
PlanOSReplan.source_plan_state_digest
  = source v1.3 PlanOS.plan_state_digest

PlanOSReplan.source_learn_state_digest
  = source v1.3 LearnOS.learn_state_digest

PlanOSReplan.source_learning_delta_digest
  = source v1.3 LearnOS.learning_delta_digest
```

The committed LearnOS delta remains future-only and inactive. It creates a
replan obligation, not an automatic belief or plan mutation.

## Qi Process Tensor role

The v1.3 Qi history is reused as an immutable prefix. PlanOS constructs a
native non-Markov history packet containing the actual ActOS, ObserveOS,
VerifyOS, and LearnOS digests.

The Qi condition packet binds the source process tensor, process history,
path dependence, intervention history, recovery, coherence, coupling,
transition readiness, observation debt, hysteresis, and memory horizon.

Qi is context only:

```text
qi_grants_truth_authority = false
qi_grants_causal_authority = false
qi_grants_execution_authority = false
qi_activates_plan = false
```

After the next plan basis is committed, one new
`GENERATIONAL_REPLAN_BASIS_COMMITTED` record is appended to the Qi history.
The complete v1.3 history remains byte-for-byte the prefix of the extended
history.

## WORLD role

WORLD supplies the horizontal candidate-state projection against which the
next-generation candidates are interpreted. The next projection binds the
source WORLD digest, the extended Qi receipt, the learning delta, native
Decision/plural/Wa states, and the committed next plan basis.

It remains:

```text
projection_read_only = true
candidate_only = true
nonfinal_marker = true
exact_world_identified = false
runtime_updates_world = false
multi_world_noncollapse = true
two_truths_gap = true
future_model_candidate_only = true
```

The projection describes a future modeling candidate. It does not alter the
exact WORLD.

## Native deliberation

The replan candidate field contains:

```text
strengthen-evidence
continue-current
hold-safe
```

DecisionOS selects from exactly that field. Plural deliberation and Wa review
preserve the selected identity and retained alternatives. PlanOS accepts the
selection only when:

```text
PlanOS decision_receipt.decision_os_state_digest
  = native DecisionOS.decision_state_digest

PlanOS decision_receipt.wa_relational_harmony_digest
  = native DecisionOSWa.wa_state_digest

PlanOS selected_candidate_id
  = DecisionOS selected_option_id
```

## Generation boundary

```text
target_generation = source_generation + 1
future_only = true
active_now = false
current_cycle_unchanged = true
past_history_unchanged = true
host_license_granted = false
next_plan_not_execution = true
external_authority_required_for_future_act = true
```

Closing the cycle therefore does not create a self-executing loop.

## Rejected substitutions

The v1.4 validator rejects source Plan/Learn/learning-delta substitution,
Decision/plural/Wa detachment, selected identity substitution, Qi history
prefix mutation, next-basis mismatch across Qi and WORLD, mutable or exact
WORLD claims, present activation, host-license synthesis, generation-order
errors, and adapter truth/execution/authority/history-overwrite claims.

## Boundary

```text
Learn delta ≠ present activation
Qi context ≠ execution authority
WORLD projection ≠ exact WORLD
Decision selection ≠ execution
next PLAN basis ≠ execution permission
Governance admission ≠ external host authority
adapter ≠ authority issuer
```
