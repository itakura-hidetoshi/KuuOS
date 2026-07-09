# PlanOS DecisionOS Selection Receipt Intake v0.29

## 位置づけ

PlanOS v0.29は、PlanOS v0.28のDecisionOS selection requestに対して、DecisionOSが返したselection receiptをPlanOS側で受け取るintakeである。

この層は選択結果を受領し、要求候補集合との対応を検証する。

この層はPlanOS synthesisを行わない。

この層はselected candidateをcommitしない。

この層はActOSを呼び出さない。

## 接続経路

```text
PlanOS v0.28 DecisionOS selection request
+ DecisionOS admissible candidate selection receipt
→ PlanOS DecisionOS selection receipt intake
→ selected candidate bound to request
→ intake record
```

## 検証境界

v0.29は、DecisionOS selection receiptの `selected_candidate_id` がv0.28の `requested_candidate_ids` に含まれることを要求する。

また、selected candidate digestがrequest itemのcandidate digestと矛盾しないことを要求する。

```text
selected candidate
→ requested candidate set membership
→ candidate digest match
→ intake record
```

## まだ実行しないもの

```text
selected candidate committed here = false
plan synthesis granted = false
activation authorization granted = false
ActOS invoked = false
execution granted = false
truth authority granted = false
memory overwrite granted = false
blocker release granted = false
external commit granted = false
```

## boundary

```text
intake owned by PlanOS = true
selection receipt owned by DecisionOS = true
selection receipt intake only = true
selected candidate bound to request = true
selected candidate committed here = false
plan synthesis granted = false
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
runtime/kuuos_planos_decisionos_selection_receipt_intake_v0_29.py
```

The runtime builds:

```text
PLANOS_DECISIONOS_SELECTION_RECEIPT_INTAKE_READY
```

or:

```text
PLANOS_DECISIONOS_SELECTION_RECEIPT_INTAKE_BLOCKED
```

## Lean定理

```text
source_request_remains_selection_request_only
intake_binds_decisionos_selection_to_request
intake_grants_no_commit_synthesis_activation_execution_or_truth
boundary_blocks_plan_synthesis_commit_memory_and_blocker_release
history_appends_one_selection_receipt_intake_record
digest_is_exact
```

## Honest classification

```text
an additive PlanOS-owned intake over a DecisionOS selection receipt, binding a
selected candidate back to the v0.28 selection request while granting no PlanOS
synthesis, selected candidate commit, activation, ActOS invocation, execution,
external commit, memory overwrite, truth authority, or blocker release authority
```
