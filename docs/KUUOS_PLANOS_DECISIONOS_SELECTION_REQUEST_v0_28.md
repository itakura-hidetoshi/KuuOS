# PlanOS DecisionOS Selection Request v0.28

## 位置づけ

PlanOS v0.28は、PlanOS v0.27のDecisionOS review intakeを、DecisionOS selection gateへ渡すためのselection requestへ変換する。

この層は候補を選択しない。

この層はDecisionOS decision receiptを発行しない。

この層はPlanOS synthesisを行わない。

この層はActOSを呼び出さない。

## 接続経路

```text
PlanOS v0.27 DecisionOS review intake
→ DecisionOS selection request
→ requested candidate ids
→ probe candidate ids
→ excluded barrier candidate ids
→ selection request items
```

## requestの意味

v0.28は、review intakeで確認された候補をDecisionOSに選択してよい候補として依頼する。

ただし、依頼は選択ではない。

```text
decision review item
→ selection request digest
→ requested candidate id
→ selectable by this layer = false
```

DecisionOS selectionは別gateで実行される。

## probeとbarrier

```text
probe candidate
→ marked for DecisionOS review
→ not selected here
```

```text
barrier candidate
→ excluded barrier candidate ids
→ not requested as selectable here
```

## boundary

```text
request owned by PlanOS = true
selection owned by DecisionOS = true
selection request only = true
review intake preserved = true
probe candidates marked not selected = true
barrier candidates excluded = true
candidate selection authority granted = false
selected candidate committed = false
decision made = false
decision receipt issued = false
activation authorization granted = false
ActOS invoked = false
execution granted = false
truth authority granted = false
memory overwrite granted = false
blocker release granted = false
external commit granted = false
```

## runtime artifact

```text
runtime/kuuos_planos_decisionos_selection_request_v0_28.py
```

The runtime builds:

```text
PLANOS_DECISIONOS_SELECTION_REQUEST_READY
```

or:

```text
PLANOS_DECISIONOS_SELECTION_REQUEST_BLOCKED
```

## Lean定理

```text
source_intake_remains_review_input_only
request_is_selection_request_only
request_grants_no_selection_decision_activation_execution_or_truth
boundary_blocks_commit_memory_and_blocker_release
history_appends_one_selection_request_record
digest_is_exact
```

## Honest classification

```text
an additive PlanOS-owned selection-request layer over the v0.27 DecisionOS review
intake, preserving review input and asking DecisionOS to run a later selection gate
while granting no selection, decision receipt, activation, ActOS invocation,
execution, external commit, memory overwrite, truth authority, or blocker release
authority
```
