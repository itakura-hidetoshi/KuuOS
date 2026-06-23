# PlanOS Vacuum Expectation Learning Replan Intake v0.18

## 位置づけ

PlanOS v0.18 は、LearnOS v0.3のfuture-only learning receiptを、既存PlanOS replan kernelのsource bindingとpristine bindへ接続する。

この層はreplan intakeをcommitする。

この層はreplanを起動せず、candidateを選択せず、planを合成せず、executionを許可しない。

## 接続経路

```text
WORLD v0.51 pre-commit intake
→ ObserveOS v0.3 observation commit
→ VerifyOS v0.3 verification receipt
→ LearnOS v0.3 future-only delta
→ PlanOS v0.18 exact replan intake
→ existing PlanOS v0.2 ReplanSourceBinding
→ existing PlanOS v0.4 pristine closed-loop bind
→ separate history, Qi condition, generation, constraint and deliberation phases
```

## source binding

intakeは次を要求する。

```text
committed current plan = true
committed LearnOS state = true
learning delta bound = true
Middle Way report bound = true
verification evidence bound = true
future-only learning = true
learning inactive now = true
replan required by LearnOS = true
```

LearnOS receipt全体はintake digestの入力として保持される。

## pristine bind

```text
phase = bind
event index = 0
history required = true
```

PlanOS intake eventは一回だけappendされる。

```text
indexBefore.current = 0
indexAfter.current = 1
historyAfter.committedRecords = historyBefore.committedRecords + 1
```

## 所有権

```text
replan owner = PlanOS
candidate selection owner = DecisionOS
plan synthesis owner = PlanOS
execution owner = ActOS
```

LearnOSはreplanの必要性を記録する。

PlanOS v0.18はその債務をPlanOS intakeへ受け入れる。

## activation separation

```text
intake committed = true
bind committed = true
replan activated = false
plan activated = false
execution permitted = false
host licence granted = false
```

intake commitはreplan activationではない。

bind commitはplan synthesisではない。

## future-only境界

```text
future only = true
active now = false
current cycle unchanged = true
past plan unchanged = true
memory overwrite = false
```

## 非権限境界

```text
replan intake != truth authority
replan intake != causal authority
replan intake != final commitment
replan intake != self-modification
replan intake != execution permission
replan intake != host licence
replan intake != memory overwrite
replan intake != WORLD update
```

## Lean定理

```text
intake_requires_committed_future_only_learning
intake_binds_existing_replan_source
intake_enters_pristine_planos_bind
intake_event_index_appends_exactly_once
intake_history_appends_exactly_once
intake_preserves_planos_decisionos_actos_ownership
intake_commit_is_not_activation_plan_or_execution
intake_future_boundary_preserves_current_and_past
intake_bridge_grants_no_new_authority
intake_digest_is_exact
intake_candidate_value_remains_exact
```

## Honest classification

```text
an exact PlanOS-owned replan intake over a LearnOS v0.3 future-only receipt,
reusing the existing PlanOS source and closed-loop bind contracts,
with one append-only intake record and preserved OS ownership,
but without replan activation, candidate selection, plan synthesis,
execution permission, host licensing, memory overwrite or WORLD update
```
