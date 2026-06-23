# PlanOS Activation Admission ActOS Handoff v0.23

## 位置づけ

PlanOS v0.23は、PlanOS v0.22のcompiler materialization receiptを入力として、次周期のactivation admissionを評価し、ActOSへhandoffする。

この層はPlanOSによるadmission判定だけを所有する。

activation authorizationとexecutionはActOSが所有する。

v0.23はplanをactivateせず、ActOSを呼び出さず、lease使用を予約しない。

## 接続経路

```text
PlanOS v0.22 materialization receipt
→ non-hold executable material gate
→ exact next-cycle freshness
→ adaptive epoch and capability epoch binding
→ cycle authorization binding
→ fresh human approval binding
→ fresh host licence binding
→ capability, lease, session and action-intent binding
→ operation, resource and effect-ceiling concordance
→ PlanOS activation admission receipt
→ ActOS handoff receipt
```

## hold境界

v0.22のhold候補は実行可能step数が0である。

そのためv0.23 admissionは次を要求する。

```text
selected candidate != hold
executable material present = true
```

holdはactivation admissionへ昇格しない。

## 次周期とepoch

```text
target cycle = current cycle + 1
adaptive epoch = target cycle
capability epoch = adaptive epoch
```

materialization、human approval、host licence、lease、session、action intentはすべてfreshでなければならない。

古いauthority materialは次周期へ継承しない。

## generation authority binding

```text
cycle authorization bound = true
human approval bound = true
host licence bound = true
capability bound = true
lease bound = true
session bound = true
action intent bound = true
```

さらに次の一致を要求する。

```text
owner exact
lineage exact
capability identity exact
adapter kind exact
capability epoch exact
operation allowed
resource allowed
effect within capability ceiling
effect within lease ceiling
```

## action intent

Action intentはDecisionOS selection receiptと別の契約である。

```text
action intent distinct from decision = true
staged only = true
```

選択候補そのものをexecution intentとして扱わない。

外部commitを含むeffectはadmission対象にならない。

## admission境界

```text
source materialization bound = true
freshness accepted = true
authority material accepted = true
admitted = true
activated = false
ActOS invoked = false
executed = false
lease use reserved = false
```

admittedはactivatedを意味しない。

## ActOS handoff

```text
materialization receipt bound = true
admission receipt bound = true
selected identity preserved = true
target cycle preserved = true
authority material preserved = true
handoff committed = true
activation owner = ActOS
execution owner = ActOS
```

handoffではactivation authorizationを供給しない。

ActOSは別のauthorization gateでfreshness、scope、lease、session、intentを再検証する。

## event lineage

```text
v0.22 materialization receipt index
< v0.23 admission index
< v0.23 ActOS handoff index
```

adapter historyにはadmissionとhandoffの2 recordを追加する。

## 所有権

```text
activation admission owner = PlanOS
activation authorization owner = ActOS
execution owner = ActOS
```

## 非権限境界

```text
admission != activation authorization
admission != plan activation
handoff != ActOS invocation
handoff != execution permission
handoff != lease-use reservation
handoff != external commit
handoff != truth authority
handoff != clinical authority
handoff != legal authority
handoff != memory overwrite
```

## Lean定理

```text
requires_materialized_non_hold_candidate
requires_exact_next_cycle_and_fresh_epoch
requires_fresh_generation_material
requires_complete_authority_binding
requires_exact_scope_and_effect_concordance
intent_is_distinct_and_staged_only
admission_does_not_activate_invoke_or_execute
handoff_preserves_material_identity_cycle_and_authority
handoff_is_not_activation_authorization_or_execution
events_append_strictly
history_appends_two_records
bridge_preserves_ownership
bridge_grants_no_activation_execution_or_commit
digest_is_exact
```

## Honest classification

```text
an exact PlanOS-owned activation-admission and ActOS-handoff receipt over a
non-hold v0.22 materialization, with fresh next-cycle approval, licence,
capability, lease, session and distinct action-intent bindings, while keeping
activation authorization, lease-use reservation, ActOS invocation and execution
outside this layer
```
