# PlanOS Selected Candidate Next-Cycle Synthesis v0.21

## 位置づけ

PlanOS v0.21 は、DecisionOS v0.4の選択receiptをPlanOSへ戻し、選択候補に対応する次周期plan basisを合成してcommitする。

選択はDecisionOSが所有し、合成はPlanOSが所有する。

この層はplanを現在周期でactivationせず、executionを許可しない。

## 接続経路

```text
PlanOS v0.20 admissible set handoff
→ DecisionOS v0.4 admissible selection
→ exact selected-candidate binding
→ history, Qi, learning and mission binding
→ NextCycleSynthesis
→ ReplanCommitBoundary
→ next-plan phase required
```

## source binding

```text
source selection performed = true
selected candidate identity exact = true
selected candidate bound = true
decision receipt bound = true
history bound = true
Qi condition bound = true
learning delta bound = true
mission contract bound = true
```

PlanOSはDecisionOSの選択候補を別候補へ置換しない。

## next-cycle synthesis

```text
activeFromCycle = currentCycle + 1
futureOnly = true
activeNow = false
currentCycleUnchanged = true
pastPlanUnchanged = true
```

合成basisは現在周期では有効にならない。

## commit boundary

```text
synthesis committed = true
next plan basis committed = true
next plan phase required = true
active now = false
memory overwrite = false
host licence granted = false
```

basis commitはplan activationではない。

next-plan phase requirementはActOS execution permissionではない。

## event lineage

```text
DecisionOS handoff index
< synthesis index
< commit index
```

PlanOS historyにはsynthesisとcommitの2 recordを追加する。

## 所有権

```text
candidate selection owner = DecisionOS
plan synthesis owner = PlanOS
execution owner = ActOS
```

## 非権限境界

```text
plan synthesis != truth authority
plan synthesis != causal authority
basis commit != plan activation
basis commit != final commitment authority
basis commit != execution permission
basis commit != host licence
basis commit != memory overwrite
basis commit != WORLD update
```

## Lean定理

```text
synthesis_requires_exact_decision_selection
synthesis_binds_history_qi_learning_and_mission
synthesis_starts_exactly_next_cycle
synthesis_is_future_only_and_inactive
synthesis_commit_requires_next_plan_phase
synthesis_commit_does_not_activate_execute_or_license
synthesis_events_append_strictly
synthesis_history_appends_two_records
synthesis_bridge_preserves_ownership
synthesis_bridge_grants_no_downstream_authority
synthesis_digest_is_exact
```

## Honest classification

```text
an exact PlanOS-owned next-cycle synthesis receipt over a DecisionOS v0.4 selection,
with immutable selected identity, bound history, Qi, learning and mission context,
and a committed future-only next-plan basis,
but without present activation, execution permission, host licensing,
memory overwrite or WORLD update
```
