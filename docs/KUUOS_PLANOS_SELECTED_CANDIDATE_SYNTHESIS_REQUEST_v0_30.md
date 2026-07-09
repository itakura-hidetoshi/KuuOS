# PlanOS Selected Candidate Synthesis Request v0.30

## 位置づけ

PlanOS v0.30は、v0.29で受け取ったDecisionOS selection receipt intakeから、selected candidateをPlanOS synthesisへ渡すためのrequestを作る。

この層はsynthesis requestだけを作る。

この層はmaterializationを行わない。

この層はactivation authorizationを与えない。

この層はActOSを呼び出さない。

## 接続経路

```text
PlanOS v0.29 DecisionOS selection receipt intake
→ selected candidate synthesis request
→ selected candidate bound to intake
→ synthesis request digest
```

## requestの意味

v0.30は、selected candidateをPlanOS synthesisの入力候補として包む。

ただし、包むことは合成ではない。

```text
selected candidate
→ synthesis request
→ materialization granted = false
→ execution granted = false
```

## boundary

```text
request owned by PlanOS = true
source selection receipt intake preserved = true
selected candidate bound to intake = true
synthesis request only = true
materialization granted = false
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
runtime/kuuos_planos_selected_candidate_synthesis_request_v0_30.py
```

The runtime builds:

```text
PLANOS_SELECTED_CANDIDATE_SYNTHESIS_REQUEST_READY
```

or:

```text
PLANOS_SELECTED_CANDIDATE_SYNTHESIS_REQUEST_BLOCKED
```

## Lean定理

```text
source_intake_remains_receipt_intake_only
request_binds_selected_candidate_to_intake
request_grants_no_materialization_activation_execution_or_truth
boundary_blocks_materialization_commit_memory_and_blocker_release
history_appends_one_synthesis_request_record
digest_is_exact
```

## Honest classification

```text
an additive PlanOS-owned synthesis-request layer over the v0.29 DecisionOS
selection receipt intake, binding the selected candidate to the intake record
while granting no materialization, activation, ActOS invocation, execution,
external commit, memory overwrite, truth authority, or blocker release authority
```
