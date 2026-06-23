# PlanOS World Host-Effect Replan Intake v0.24

## 位置づけ

PlanOS v0.24は、LearnOS v0.4のimmutable future-only learning receiptを、既存PlanOS replan契約のpristine bindへ接続する。

この層はreplan activation、candidate generation、DecisionOS selection、plan synthesis、execution、WORLD disposition解決を行わない。

## 接続経路

```text
ObserveOS v0.4 qualifying observation receipt
→ VerifyOS v0.4 verification receipt
→ LearnOS v0.4 future-only learning receipt
→ PlanOS v0.24 exact replan intake
→ existing ReplanSourceBinding
→ existing ClosedLoopBindState
```

## 入力条件

```text
learning receipt committed = true
learning recorded = true
replan required = true
future only = true
active now = false
current-cycle mutation = false
past-record mutation = false
current plan committed = true
```

## 既存replan sourceへの結合

```text
committed current plan = true
committed LearnOS state = true
same mission contract = true
learning delta bound = true
middle-way report bound = true
verification evidence bound = true
future-only learning = true
learning inactive now = true
replan required by LearnOS = true
```

`learningInactiveNow`は「非活動状態が成立している」という正のBoolであり、`delta.activeNow = false`と独立に保持する。

## pristine bind

```text
phase is bind = true
event index = 0
history required = true
```

intakeはPlanOS replan stateをbind phaseへ置くだけで、次のhistory、Qi conditioning、candidate generationへ自動遷移しない。

## WORLD disposition candidate保持

```text
source disposition preserved = true
governance review preserved = true
WORLD commit separate = true
fresh commit authorization required = true
fresh commit authorization supplied = false
atomic commit ready = false
replan intake resolves WORLD disposition = false
automatic WORLD adoption = false
automatic WORLD rejection = false
automatic WORLD commit = false
automatic rollback = false
```

PlanOS intakeはWORLD disposition candidateを採用または棄却しない。

## 所有権

```text
replan owner = PlanOS
candidate selection owner = DecisionOS
plan synthesis owner = PlanOS
execution owner = ActOS
learning owner = LearnOS
WORLD disposition owner = WORLD
```

## activation分離

```text
intake committed = true
bind committed = true
replan activated = false
plan activated = false
execution permitted = false
host license granted = false
candidate generation = false
candidate selection = false
plan synthesis = false
WORLD disposition resolution = false
```

## receiptとledger

```text
receipt committed = true
receipt immutable = true
append only = true
exact replay idempotent = true
conflicting replay accepted = false

PlanOS index before = 0
PlanOS index after = 1
PlanOS history append = 1 record
```

## 非権限境界

```text
replan intake != replan activation
replan intake != candidate generation
replan intake != DecisionOS selection
replan intake != plan synthesis
replan intake != execution permission
replan intake != host license
replan intake != WORLD disposition resolution
replan intake != WORLD update
replan intake != memory overwrite
```

## Lean定理

```text
intake_requires_committed_future_only_learning
intake_binds_existing_replan_source
intake_enters_pristine_planos_bind
intake_preserves_future_boundary
intake_preserves_world_disposition_candidate
intake_preserves_planos_decisionos_actos_ownership
intake_commit_is_not_activation_generation_selection_or_execution
intake_receipt_is_immutable_append_only_and_replay_safe
intake_event_index_appends_exactly_once
intake_history_appends_one_record
intake_grants_no_downstream_authority
intake_digest_is_exact
```
