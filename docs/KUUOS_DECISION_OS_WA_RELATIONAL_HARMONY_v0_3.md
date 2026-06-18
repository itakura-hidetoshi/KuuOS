# KuuOS DecisionOS Wa Relational Harmony Kernel v0.3

DecisionOS v0.3 restores the fixed KuuOS definition of 和 and places it above the committed plural deliberation and appeal receipt of DecisionOS v0.2.

> 和とは、異なる個がインドラネットワークとして互いに包摂・響き合い、絶えず対話・創発・調整を続けるなかで現れる動的・生成的な調和である。

The kernel does not reinterpret 和 as obedience, unanimity, social smoothness, majority preference, or a single scalar winner. Command-like enforcement, static conformity, exclusion, oppression, minority erasure, and false stability contradict 和.

```text
v0.20 Mission Contract
  + BeliefOS v0.3
  + DecisionOS v0.1 relational deliberation
  + DecisionOS v0.2 plural harmony / veto / appeal
        ↓
DecisionOS v0.3 Wa relational harmony evaluation
        ↓
ENDORSE / REOBSERVE / REPAIR / ESCALATE / HOLD / REJECT / QUARANTINE
        ↓
future-only Replan basis
```

The pre-existing daemon Wa v0.1 remains a local runtime-posture function using Qi scope, emptiness, over-density, and nihilism risk. v0.3 does not replace it; v0.3 is the upper relational-ethical review gate.

## 1. Fixed Wa dimensions

The positive relational field has seven interval-valued dimensions:

```text
inclusion
dialogue
mutual_reflection
emergence
dynamic_adaptation
non_hierarchy
recursive_feedback
```

Each dimension is a context-local interval `[lower, upper]` in `[0,1]`. No dimension is truth authority and no point estimate is required.

## 2. Vigilance field

和 includes a permanent self-critical vigilance field:

```text
coercive_conformity
exclusion
oppression
hierarchy_concentration
minority_erasure
false_stability
complacency_in_safe_conditions
```

The final term carries the operational lesson of 徒然草第150段: failure can arise in apparently safe, familiar, or easy conditions. A smooth surface never disables inspection.

## 3. Wa function

For option `a`, let the positive dimension intervals be `[l_i(a), u_i(a)]`, with nonnegative weights `w_i` summing to one.

```text
weighted_lower(a) = Σ w_i l_i(a)
weighted_upper(a) = Σ w_i u_i(a)
weakest_lower(a) = min_i l_i(a)
weakest_upper(a) = min_i u_i(a)
```

With bottleneck sensitivity `β ∈ [0,1]`:

```text
relational_lower(a)
  = (1 - β) weighted_lower(a) + β weakest_lower(a)

relational_upper(a)
  = (1 - β) weighted_upper(a) + β weakest_upper(a)
```

For alert intervals `[p_j^L(a), p_j^U(a)]`:

```text
alert_lower(a) = max_j p_j^L(a)
alert_upper(a) = max_j p_j^U(a)
```

The conservative Wa interval is:

```text
Wa_lower(a) = relational_lower(a) × (1 - alert_upper(a))
Wa_upper(a) = relational_upper(a) × (1 - alert_lower(a))
```

A high average therefore cannot hide failed inclusion, dialogue, non-hierarchy, feedback, or minority preservation.

## 4. Binding to DecisionOS v0.2

Genesis binds exact digests for:

```text
source plural state
committed plural decision
plural decision basis
underlying v0.1 decision basis
mission contract
source option field
stakeholder registry
stakeholder-local utility records
veto records
aggregate records
appeal history
source plural route
source selected option
retained alternatives
```

DecisionOS v0.3 cannot rewrite v0.1, v0.2, stakeholder utilities, validated vetoes, or appeal history.

## 5. False harmony classification

```text
confirmed false harmony
  if alert_lower reaches the confirmed threshold
  or minority preservation is explicitly false

suspected false harmony
  if alert_upper reaches the suspicion threshold
  or dissent was not considered
```

Confirmed false harmony routes to `ESCALATE`. Suspected false harmony routes to `REOBSERVE`. Coercion is never relabelled as harmony.

## 6. Source-route bridge

```text
CONSENSUS_CANDIDATE
  -> evaluate the exact selected option through the Wa gate

NEGOTIATE or APPEAL
  -> REOBSERVE

HANDOVER
  -> ESCALATE

HOLD
  -> HOLD

REJECT
  -> REJECT

QUARANTINE
  -> QUARANTINE
```

A consensus candidate may be endorsed only when:

```text
Wa_lower >= minimum_wa_floor
weakest_lower >= minimum_dimension_floor
alert_upper < suspected_false_harmony_threshold
dissent_considered = true
minority_preserved = true
source selected-option identity is unchanged
```

Another option's better Wa interval is evidence for future Replan, not permission for silent substitution.

## 7. Strict phase order

```text
BIND
  ↓
PROFILE
  ↓
EVALUATE
  ↓
FALSE_HARMONY_CHECK
  ↓
PLURALITY_CHECK
  ↓
GATE
  ↓
COMMIT
```

Phase skipping, stale state, digest mismatch, event-index regression, time regression, replay mutation, and authority escalation are rejected.

## 8. Plurality and dissent

Every source option must receive a Wa profile. The kernel preserves:

- all source option IDs;
- retained alternative IDs;
- stakeholder registry and local utility digests;
- validated and unvalidated veto evidence;
- appeal history;
- dissent evidence digests;
- minority stakeholder digests;
- dialogue receipt digests;
- Indra-network receipt digests;
- complete Wa and alert intervals.

Absence of dissent is not interpreted automatically as agreement.

## 9. Commit and Replan boundary

Commit requires:

```text
future_only = true
memory_overwrite = false
wa_not_truth = true
wa_not_execution = true
wa_not_moral_veto = true
activation_boundary = mission_replan_only
```

`ENDORSE` means that the exact v0.2 consensus candidate passes the Wa gate. It is not an execution license, clinical order, institutional approval, legal authorization, or theorem authority.

## 10. Durable storage

```text
wa-v03-genesis.json
wa-v03-ledger.jsonl
wa-v03-snapshot.json
.decision-os-wa-v03.lock
```

The ledger is append-only authority and the snapshot is a reconstructible cache. Recovery verifies event order, state chains, commit chains, source bindings, and replay identity before snapshot repair.

## 11. Formal surface

The Lean surface proves:

- typed strict Wa phase order;
- strict event-index growth;
- weighted support and weakest-link mixture remain in `[0,1]`;
- the conservative Wa interval remains ordered and bounded;
- increasing alert cannot increase conservative Wa;
- full alert collapses Wa to zero;
- bottleneck sensitivity exposes the weakest dimension;
- confirmed false harmony cannot be endorsed;
- minority erasure cannot be endorsed;
- endorsement preserves the exact v0.2 selected-option identity;
- retained alternatives remain bounded by the source option field;
- silent substitution is forbidden;
- Wa grants no truth, execution, moral-veto, clinical, or host-license authority;
- activation remains future-only and Replan-bound.

## 12. Public boundary

DecisionOS v0.3 is a structural, auditable harmony evaluator. It does not declare universal harmony, erase conflict, compel consensus, replace a selected option, or authorize action.
