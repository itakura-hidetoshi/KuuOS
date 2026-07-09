# PlanOS DecisionOS Review Intake v0.27

## 位置づけ

PlanOS v0.27は、PlanOS v0.26のweighted DecisionOS evidence handoffを、DecisionOSがレビュー可能な選択前入力へ変換する。

この層は候補を選択しない。

この層はDecisionOS decision receiptを発行しない。

この層はPlanOS synthesisを行わない。

この層はActOSを呼び出さない。

## 接続経路

```text
PlanOS v0.26 weighted DecisionOS evidence handoff
→ DecisionOS review intake
→ review candidate ids
→ probe candidate ids
→ excluded barrier candidate ids
→ decision review items
```

## 役割

v0.27は、DecisionOSに渡せる候補レビュー入力を整える。

```text
decision evidence item
→ review reason digest
→ DecisionOS review required
→ selectable here = false
```

`selectable here = false` は、この層で候補を決めないことを意味する。

DecisionOS selectionは別gateで行う。

## silent substitution防止

v0.27は、source handoffの `review_candidate_ids` と実際に生成されたreview item idsを照合する。

一致しない場合は次で停止する。

```text
review_candidate_ids_silent_substitution_detected
```

## barrierとprobe

```text
barrier candidate
→ excluded barrier candidate ids
→ not review-selectable here
```

```text
probe candidate
→ probe flag preserved
→ DecisionOS review required
→ not auto-selected
```

## boundary

```text
intake owned by PlanOS = true
review owned by DecisionOS = true
decision review input only = true
silent substitution forbidden = true
barrier candidate review blocked here = true
probe candidate review flag required = true
candidate selection authority granted = false
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
runtime/kuuos_planos_decision_review_intake_v0_27.py
```

The runtime builds:

```text
PLANOS_DECISION_REVIEW_INTAKE_READY
```

or:

```text
PLANOS_DECISION_REVIEW_INTAKE_BLOCKED
```

## Lean定理

```text
source_handoff_remains_evidence_only
intake_is_review_input_only
intake_grants_no_selection_decision_activation_execution_or_truth
boundary_blocks_execution_commit_memory_and_blocker_release
history_appends_one_review_intake_record
digest_is_exact
```

## Honest classification

```text
an additive PlanOS-owned DecisionOS review-intake layer over the v0.26 weighted
evidence handoff, converting evidence items into DecisionOS-reviewable input
while forbidding silent substitution and excluding barrier candidates here, and
while granting no candidate selection, decision receipt, activation,
ActOS invocation, execution, external commit, memory overwrite, truth authority
or blocker release authority
```
