# PlanOS Path Integral Candidate Weighting v0.25

## 位置づけ

PlanOS v0.25は、PlanOS v0.24のPhysical Quantum Qi Path Integral reroute gateを、候補ごとのadvisory weighting receiptへ実体化する。

この層は候補を選択しない。

この層は候補を実行しない。

この層はActOSを呼び出さない。

PlanOS v0.25は、`reinforce_path_weight`、`open_probe_potential`、`add_barrier_potential`を、候補ごとのscore、probe要求、barrier要求、replan recommendationへ変換する。

## 接続経路

```text
PlanOS v0.24 Physical Quantum Qi Path Integral reroute gate
→ path integral candidate weighting surface
→ Qi process tensor bonus
→ blocker penalty
→ advisory candidate weight receipts
→ retained / probe / barrier candidate id surfaces
→ replan recommendation only
```

## 重み付け規則

```text
reinforce_path_weight = positive path delta
open_probe_potential = weak positive path delta + probe required
add_barrier_potential = negative path delta + barrier required
```

Qi process tensor continuity is treated as evidence bonus.

Blocker missing-evidence surface is treated as penalty and route conversion.

## receipt境界

```text
candidate weighting advisory only = true
selection authority granted = false
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
runtime/kuuos_planos_path_integral_candidate_weighting_v0_25.py
```

The runtime builds:

```text
PLANOS_PATH_INTEGRAL_CANDIDATE_WEIGHTING_READY
```

or:

```text
PLANOS_PATH_INTEGRAL_CANDIDATE_WEIGHTING_BLOCKED
```

The receipt contains:

```text
source_gate_digest
path_integral_digest
qi_process_tensor_digest
blocker_digest
dominant_reentry_mode
candidate_weight_receipts
retained_candidate_ids
probe_candidate_ids
barrier_candidate_ids
boundary
receipt_digest
```

## Lean定理

```text
uses_v024_path_integral_evidence
path_integral_weighting_is_advisory
reroute_modes_are_visible
receipt_is_replan_recommendation_only
receipt_grants_no_selection_activation_execution_or_commit
history_appends_one_weighting_record
digest_is_exact
```

## Honest classification

```text
an additive PlanOS-owned candidate-weighting materialization over the v0.24
Physical Quantum Qi Path Integral reroute surface, producing advisory candidate
scores and replan recommendations only, while granting no selection,
activation, ActOS invocation, execution, external commit, memory overwrite,
truth authority or blocker release authority
```
