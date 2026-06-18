# KuuOS DecisionOS Wa Relational Harmony Kernel v0.2

DecisionOS v0.2 restores the fixed KuuOS definition of 和 and places it above the committed DecisionOS v0.1 deliberation receipt.

> 和とは、異なる個がインドラネットワークとして互いに包摂・響き合い、絶えず対話・創発・調整を続けるなかで現れる動的・生成的な調和である。

The kernel does not reinterpret 和 as obedience, unanimity, social smoothness, majority preference, or a single scalar winner. Command-like enforcement, static conformity, exclusion, oppression, minority erasure, and false stability contradict 和.

```text
v0.20 Mission Contract
  + BeliefOS v0.3
  + DecisionOS v0.1 committed decision basis
        ↓
DecisionOS v0.2 Wa relational harmony evaluation
        ↓
ENDORSE / REOBSERVE / REPAIR / ESCALATE / HOLD / REJECT / QUARANTINE
        ↓
future-only Replan basis
```

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

和 includes a permanent self-critical vigilance field. The alert dimensions are:

```text
coercive_conformity
exclusion
oppression
hierarchy_concentration
minority_erasure
false_stability
complacency_in_safe_conditions
```

The last term carries the operational lesson of 徒然草第150段: failure often occurs in apparently safe, familiar, or easy conditions. A smooth surface therefore never disables inspection.

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

The weakest-link term prevents a high average from hiding failed inclusion, dialogue, non-hierarchy, or feedback.

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

Thus increased coercion, exclusion, oppression, hierarchy, minority erasure, false stability, or complacency can only reduce the conservative Wa score.

## 4. Why Wa is not a weighted average alone

A weighted mean permits compensation: strong efficiency or apparent agreement could hide complete failure of dialogue or minority inclusion. DecisionOS v0.2 therefore combines:

- weighted relational support;
- weakest-dimension sensitivity;
- independent false-harmony vigilance;
- explicit dissent consideration;
- explicit minority preservation;
- retained alternatives from DecisionOS v0.1.

和 is a relational constraint and review surface, not a universal value sovereign.

## 5. False harmony classification

```text
confirmed false harmony
  if alert_lower reaches the confirmed threshold
  or minority preservation is explicitly false

suspected false harmony
  if alert_upper reaches the suspicion threshold
  or dissent was not considered

no false-harmony warning
  only when the conservative alert upper bound remains below suspicion
```

Confirmed false harmony routes to `ESCALATE`. Suspected false harmony routes to `REOBSERVE`. The kernel never silently relabels coercion as harmony.

## 6. Wa gate

A selected or recommended option may be endorsed only when:

```text
Wa_lower >= minimum_wa_floor
weakest_lower >= minimum_dimension_floor
alert_upper < suspected_false_harmony_threshold
dissent_considered = true
minority_preserved = true
source option identity is unchanged
```

If another retained alternative has a better Wa interval, v0.2 records that evidence but does not silently substitute it for the v0.1 selection. A changed selection requires return to deliberation through Replan.

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

Phase skipping, stale source state, digest mismatch, event-index regression, time regression, replay mutation, and authority escalation are rejected.

## 8. Source binding

Genesis binds exact digests for:

```text
source DecisionOS v0.1 state
committed decision
source decision basis
mission contract
mission state
belief receipt
source route
source selected option
source recommended options
source admissible options
source retained alternatives
```

v0.2 cannot rewrite the v0.1 option set or replace the selected option.

## 9. Plurality and dissent

Every source-admissible option must receive a Wa profile. The kernel preserves:

- all admissible option IDs;
- retained alternative IDs;
- dissent evidence digests;
- minority stakeholder digests;
- dialogue receipt digests;
- Indra-network receipt digests;
- complete Wa and alert intervals.

Absence of dissent is not interpreted automatically as agreement.

## 10. Commit and Replan boundary

Commit requires:

```text
future_only = true
memory_overwrite = false
wa_not_truth = true
wa_not_execution = true
wa_not_moral_veto = true
activation_boundary = mission_replan_only
```

`ENDORSE` means that the source decision basis passes the Wa gate. It is not an execution license, clinical order, institutional approval, legal authorization, or theorem authority.

## 11. Durable storage

```text
wa-genesis.json
wa-ledger.jsonl
wa-snapshot.json
.wa-decision-os.lock
```

The ledger is append-only authority and the snapshot is a reconstructible cache. Recovery verifies event order, state chains, commit chains, source bindings, and replay identity before snapshot repair.

## 12. Formal surface

The Lean surface proves:

- typed strict Wa phase order;
- strict event-index growth;
- weighted support and weakest-link mixture remain in `[0,1]`;
- conservative Wa interval remains ordered and bounded;
- increasing alert cannot increase conservative Wa;
- full alert collapses Wa to zero;
- bottleneck sensitivity exposes a zero weakest dimension;
- confirmed false harmony cannot be endorsed;
- minority erasure cannot be endorsed;
- endorsement preserves the source option identity;
- retained alternatives remain bounded by the source option field;
- Wa grants no truth, execution, moral-veto, clinical, or host-license authority;
- activation remains future-only and Replan-bound.

## 13. Public boundary

DecisionOS v0.2 is a structural, auditable harmony evaluator. It does not declare universal harmony, erase conflict, compel consensus, or authorize action.
