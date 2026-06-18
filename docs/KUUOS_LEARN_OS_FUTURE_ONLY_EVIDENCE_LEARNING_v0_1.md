# KuuOS LearnOS Future-Only Evidence Learning v0.1

LearnOS v0.1 converts a committed VerifyOS record into an auditable, future-only learning delta candidate. It does not rewrite past belief, memory, action, observation, verification, plan, or mission records. It does not activate the candidate. Activation requires a later Replan phase under the persistent mission contract.

```text
committed VerifyOS record
  + verification evidence lineage
  + criterion / challenge / corroboration / adjudication receipts
  + preserved counterevidence
  + uncertainty and residuals
  + Qi process-history digest
  + target-scope declaration
        ↓
LearnOS v0.1
        ↓
LEARNING_REINFORCEMENT_CANDIDATE
LEARNING_REPAIR_CANDIDATE
LEARNING_REOBSERVATION_CANDIDATE
LEARNING_HOLD
        ↓
Replan required before activation
```

## 1. Boundary

```text
learning != truth promotion
learning != memory overwrite
learning != direct belief mutation
learning != direct plan mutation
learning != direct criterion mutation
learning != causal proof
learning != self-modification authority
learning delta != active policy
commit != activation
```

LearnOS records what may be changed in a future cycle and why. It never changes the present or past operational state.

## 2. Strict phases

```text
BIND
  ↓
ABSTRACT
  ↓
CHALLENGE
  ↓
DELTA
  ↓
MIDDLE_WAY_GATE
  ↓
COMMIT
```

Phase skipping, stale-state application, source substitution, evidence substitution, counterevidence deletion, unsupported generalization, scope widening, present-cycle activation, memory overwrite, and authority escalation are rejected.

## 3. Source binding

LearnOS accepts only a committed VerifyOS state satisfying:

```text
current_phase = commit
route != PENDING
verification_recorded = true
learning_required = true
verification_evidence_digest canonical
adjudication receipt canonical
```

It binds the exact:

- VerifyOS state digest;
- source ObserveOS and ActOS state digests;
- verification evidence digest;
- inherited criterion digest;
- criterion, challenge, corroboration, and adjudication receipt digests;
- mission contract digest;
- verdict and debt semantics.

## 4. Evidence abstraction

ABSTRACT creates an evidence abstraction packet without discarding lineage:

```text
supported_pattern_digests
failed_pattern_digests
unresolved_pattern_digests
counterevidence_digests
uncertainty_digest
residual_digest
scope_digest
qi_process_history_digest
abstraction_method_digest
```

All pattern lists are declarative summaries. Original evidence remains authoritative for audit. A summary cannot replace or delete its source evidence.

## 5. Challenge preservation

CHALLENGE requires:

```text
alternative_explanation_digests
anti_overgeneralization_test_digests
distribution_shift_risk_digest
observer_bias_risk_digest
negative_transfer_risk_digest
counterevidence_preserved = true
challenge_complete = true
```

At least one anti-overgeneralization test is required. LearnOS must retain counterevidence and unresolved residuals even for a passed verification.

## 6. Learning delta

The learning delta declares only a future candidate:

```text
learning_delta_id
source_verify_state_digest
source_verification_evidence_digest
learning_kind
  = reinforcement | repair | reobservation | hold
target_scope
  = belief_candidate | plan_assumption | verification_criterion
    | observation_policy | execution_guard | no_change
before_digest
after_candidate_digest
change_rationale_digest
uncertainty_digest
counterevidence_digest
qi_process_history_digest
applicability_condition_digest
reversal_condition_digest
expiration_condition_digest
future_only = true
memory_overwrite = false
active_now = false
activation_requires_replan = true
```

The delta is rejected when it widens beyond its declared source scope, attempts to remove an invariant, or claims current activation.

## 7. Verdict-sensitive routing

### VerifyOS PASSED

May produce:

```text
LEARNING_REINFORCEMENT_CANDIDATE
```

A passed verification supports a bounded reinforcement candidate only. It cannot establish absolute truth or erase counterevidence.

### VerifyOS FAILED

May produce:

```text
LEARNING_REPAIR_CANDIDATE
```

A failed verification must preserve the failed basis and declare corrective scope. It cannot automatically rollback or rewrite the plan.

### VerifyOS INDETERMINATE

May produce:

```text
LEARNING_REOBSERVATION_CANDIDATE
```

An indeterminate verification may only propose additional observation or hold. It cannot reinforce or repair as though the evidence were conclusive.

### HOLD

Any source route may produce:

```text
LEARNING_HOLD
```

when scope, evidence, challenge, or governance conditions remain insufficient.

## 8. Emptiness, dependent origination, two truths, and Middle Way

### Emptiness

A learning delta is not a self-existing fact or active rule. It is a dependent candidate bound to evidence, context, observer, time, method, and history.

### Dependent origination

Every delta preserves:

- source verification and evidence lineage;
- criterion and challenge lineage;
- observer and scope conditions;
- uncertainty and counterevidence;
- action / observation / verification history;
- Qi process-history digest;
- mission and authority boundaries.

### Two truths

```text
samvrti surface:
  candidate is operationally usable for future Replan deliberation

paramartha boundary:
  candidate is not absolute truth, essence, or autonomous authority
```

### Middle Way

The gate rejects both:

- reification: treating a passed result as permanent truth or universal policy;
- nihilistic erasure: discarding failed, conflicting, or indeterminate evidence as useless.

Allowed routes are reinforcement candidate, repair candidate, reobservation candidate, or hold.

## 9. Qi process-history role

Qi is a conventional process-history context, not truth evidence or causal authority. LearnOS may use a Qi process-history digest to preserve temporal activation, stagnation, tension, recovery, coherence, coupling, and transition context.

Qi may condition:

- applicability boundaries;
- temporal transition expectations;
- anomaly and recovery patterns;
- observation-policy proposals;
- future hypothesis prioritization.

Qi may not:

- promote a claim to truth;
- grant execution or clinical authority;
- substitute for verification evidence;
- justify unrestricted causal attribution;
- activate the learning delta.

## 10. Middle Way gate

The gate records bounded risks:

```text
reification_risk
nihilistic_erasure_risk
overgeneralization_risk
negative_transfer_risk
premature_activation_risk
scope_drift_risk
```

A candidate is admissible only when all risks are within declared thresholds, counterevidence is preserved, source-route compatibility holds, and no authority is granted.

## 11. Mission Cycle adapter

LearnOS emits a Learn-phase receipt for the fixed v0.21 cycle:

```text
Mission → Plan → Act → Observe → Verify → Learn → Replan
```

The receipt contains:

```text
mission_cycle_phase = learn
learning_delta_digest
learning_route
future_only = true
memory_overwrite = false
active_now = false
replan_required = true
next_plan_basis_candidate_digest
```

Only the subsequent Replan phase may decide whether to include the candidate in the next plan basis. Replan itself does not grant execution authority.

## 12. Debt semantics

All committed LearnOS routes satisfy:

```text
learning_recorded = true
learning_debt_discharged = true
replan_required = true
current_cycle_unchanged = true
past_records_unchanged = true
```

Route-specific debt:

```text
REINFORCEMENT_CANDIDATE:
  corrective_action_required = false
  reobservation_required = false

REPAIR_CANDIDATE:
  corrective_action_required = true
  reobservation_required = false

REOBSERVATION_CANDIDATE:
  corrective_action_required = false
  reobservation_required = true

HOLD:
  corrective_action_required = false
  reobservation_required may remain true
```

## 13. Persistence

```text
learn-genesis.json
learn-ledger.jsonl
learn-snapshot.json
.learn-os.lock
```

The ledger is append-only authority. The snapshot is derived and repairable. The store provides exclusive writer locking, digest chains, fsync, atomic snapshot replacement, exact event replay idempotence, restart reconstruction, corruption detection, and ledger-derived snapshot repair.

## 14. Formal surface

The Lean surface proves:

- strict phase progression and event-index growth;
- exact committed VerifyOS binding;
- source evidence and counterevidence preservation;
- anti-overgeneralization challenge requirement;
- verdict-sensitive route compatibility;
- all deltas are future-only, inactive now, and require Replan;
- no past record or memory overwrite;
- Qi history grants no truth, causal, execution, or clinical authority;
- learning commit does not activate a candidate;
- append-only recovery count equals committed LearnOS record count.

## 15. Public boundary

LearnOS v0.1 is a future-candidate learning kernel. It is not an online self-modification engine, autonomous policy updater, scientific truth engine, clinical learning system, legal decision system, or direct execution controller.
