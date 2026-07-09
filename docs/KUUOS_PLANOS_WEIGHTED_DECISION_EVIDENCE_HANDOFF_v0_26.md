# PlanOS Weighted Decision Evidence Handoff v0.26

## 位置づけ

PlanOS v0.26は、PlanOS v0.25のpath integral candidate weighting receiptを、DecisionOSが読むためのevidence handoffへ変換する。

この層は候補を選択しない。

この層はDecisionOSのdecision receiptを発行しない。

この層はActOSを呼び出さない。

この層はactivation authorizationを与えない。

## 接続経路

```text
PlanOS v0.25 candidate weighting receipt
→ weighted DecisionOS evidence items
→ review candidate ids
→ probe candidate ids
→ barrier candidate ids
→ DecisionOS-readable evidence handoff
```

## handoffの意味

v0.26 handoffは、v0.25のadvisory scoreをDecisionOS向けの証拠項目に変換する。

```text
candidate_weight_receipt
→ advisory_score_digest
→ recommended_replan_route
→ probe_required
→ barrier_required
→ eligible_for_decisionos_review
```

`eligible_for_decisionos_review` は選択ではない。

DecisionOSが別のselection gateで判断するための入力である。

## barrierとprobe

```text
barrier candidate
→ not selectable here
→ blocked from PlanOS handoff selection
→ may require reobserve or repair before DecisionOS review
```

```text
probe candidate
→ review required
→ evidence preserved
→ not auto-selected
```

## boundary

```text
handoff owned by PlanOS = true
selection owned by DecisionOS = true
candidate weights advisory only = true
decision evidence only = true
selected candidate committed = false
decision made = false
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
runtime/kuuos_planos_weighted_decision_evidence_handoff_v0_26.py
```

The runtime builds:

```text
PLANOS_WEIGHTED_DECISION_EVIDENCE_HANDOFF_READY
```

or:

```text
PLANOS_WEIGHTED_DECISION_EVIDENCE_HANDOFF_BLOCKED
```

## Lean定理

```text
source_weighting_remains_advisory
handoff_is_decision_evidence_only
handoff_grants_no_decision_activation_execution_or_truth
boundary_blocks_selection_and_commit_here
history_appends_one_handoff_record
digest_is_exact
```

## Honest classification

```text
an additive PlanOS-owned evidence handoff over the v0.25 path-integral candidate
weighting receipt, converting advisory scores into DecisionOS-readable evidence
items while granting no candidate selection, decision receipt, activation,
ActOS invocation, execution, external commit, memory overwrite, truth authority
or blocker release authority
```
