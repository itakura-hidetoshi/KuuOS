# PlanOS Hysteresis Constraint DecisionOS Handoff v0.20

## 位置づけ

PlanOS v0.20 は、PlanOS v0.19の生成候補をHysteresisGateとConstraintBoundaryへ通し、適格候補集合としてDecisionOSへ渡す。

この層が進める位相は次だけである。

```text
generate
→ constrain
→ deliberate handoff
```

DecisionOSによる選択、PlanOSによるplan synthesis、activation、ActOS executionは行わない。

## 候補適格性

各候補は次を束縛する。

```text
candidate identity
HysteresisGate
ConstraintBoundary
included in admissible set
```

適格集合に含まれる候補は、mission invariant、authority boundary、Qi transition readiness、hysteresis passを満たす。

非免除の切替候補は、次の必要marginを満たさなければならない。

```text
base switch threshold
+ Qi hysteresis
+ oscillation penalty
+ recovery protection penalty
≤ switch benefit
```

## hold代替

holdは必須の適格代替として保持する。

```text
hold candidate = hold
switch exempt = true
included in admissible set = true
forwarded to DecisionOS = true
```

primary候補が制約を通過しない場合でも、適格候補集合は空にならない。

## DecisionOS handoff

handoffは次を保持する。

```text
generated candidate set bound
admissible candidate set bound
candidate identities preserved
hold alternative preserved
retained alternatives preserved
dissent visible
minority preserved
DecisionOS owns selection
```

handoff時点では次はfalseである。

```text
DecisionSelectionBoundary supplied
selection performed
plan synthesis performed
silent substitution detected
```

handoff commitはcandidate selectionではない。

## event lineage

```text
generation index < constrain index < handoff index
```

replan historyにはconstrainとhandoffの2 recordだけを追加する。

## 所有権

```text
constraint evaluation owner = PlanOS
candidate selection owner = DecisionOS
plan synthesis owner = PlanOS
execution owner = ActOS
```

## 非権限境界

```text
constraint pass != candidate selection
DecisionOS handoff != DecisionOS selection receipt
handoff != plan synthesis
handoff != replan activation
handoff != plan activation
handoff != execution permission
handoff != host licence
handoff != memory overwrite
handoff != WORLD update
```

## Lean定理

```text
follows_constraint_deliberation_prefix
hold_is_admissible_and_forwarded
included_primary_requires_hysteresis_margin
handoff_preserves_admissible_set
handoff_is_not_selection_or_synthesis
events_append_strictly
history_appends_two_records
preserves_identity_dissent_and_minority
bridge_grants_no_new_authority
digest_is_exact
```

## Honest classification

```text
an exact PlanOS-owned hysteresis and constraint filter over the v0.19 candidate set,
with a nonempty admissible set and source-preserving DecisionOS handoff,
but without DecisionOS selection, plan synthesis, activation, execution,
host licensing, memory overwrite or WORLD update
```
