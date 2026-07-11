# PlanOS Qi-Conditioned Information Metric Certificate Kernel v0.1

## 位置づけ

本層は、PlanOS v0.91で定義した情報幾何目的構造のうち、Qi process tensorと非マルコフ履歴による計画計量の変形をruntime artifactとして固定する。

PlanOS v0.91からv0.98までは、経路作用、経路分布、変分更新、Qi temperature、温度軌跡安定性を接続した。

本層は、その上流にある次の写像を実装する。

```text
(Q, H, evidence)
→ Qi-conditioned information metric
→ nonnegative transition action
```

Qiは候補を選択しない。

Qiは実行権限を生成しない。

Qiと履歴は、計画変化方向の距離と切替抵抗だけを条件づける。

## 基底計量

有限座標集合を `I` とする。

基底計量は対角重みとして表す。

```text
G = diag(g_i)
```

各基底重みは次を満たす。

```text
0 < minimum_metric_weight
minimum_metric_weight <= g_i <= maximum_metric_weight
```

座標schemaと基底重みは、それぞれdigestで直接束縛する。

## Qi process tensor

次の成分を一つのQi process tensorとして束縛する。

```text
activation
stagnation
tension
recovery
coherence
coupling
transition_readiness
hysteresis
```

各成分は有限であり、閉区間 `[0, 1]` に属する。

全成分はdigestに含まれる。

v0.99で計量変形へ直接使用する成分は、recovery、stagnation、hysteresisである。

history oscillation measureは、source historyを書き換えない独立入力として使用する。

## 座標方向

各計画座標を次のいずれかへ分類する。

```text
neutral
switch
reroute
```

`switch`方向には、回復保護、Qi hysteresis、履歴振動抵抗を加える。

`reroute`方向には、明示的な観測または履歴証拠が存在する場合だけ、停滞解除discountを適用する。

`neutral`方向には本層の変形を適用しない。

## 計量変形

`switch`方向の未射影重みを次で定義する。

```text
raw_switch_weight
=
base_weight
+ recovery_coefficient * recovery
+ hysteresis_coefficient * hysteresis
+ oscillation_coefficient * history_oscillation_measure
```

`reroute`方向の未射影重みを次で定義する。

```text
raw_reroute_weight
=
base_weight
- stagnation_coefficient * stagnation * evidence_gate
```

`evidence_gate`は、reroute evidenceが存在する場合に1となり、それ以外では0となる。

最終重みは上下限へ射影する。

```text
conditioned_weight
=
min(
  maximum_metric_weight,
  max(minimum_metric_weight, raw_weight)
)
```

この射影により、停滞解除後も計量floorを下回らない。

## 遷移作用

座標変化を `delta_theta_i` とする。

本層の対角計量による遷移作用を次で定義する。

```text
transition_action
=
1/2 * sum_i(
  conditioned_weight_i * delta_theta_i^2
)
```

すべてのconditioned weightが非負であるため、transition actionは非負となる。

この作用は、v0.91のPlan path actionにおけるtransition actionへ接続できる。

## 証明書

証明書は少なくとも次を保持する。

```text
source_objective_kernel_digest
parameter_coordinate_schema_digest
base_metric_digest
qi_process_tensor_digest
history_condition_digest
reroute_evidence_digest
reroute_evidence_present
transition_direction_map
conditioned_metric_weights
recovery_switch_surcharge
hysteresis_switch_surcharge
oscillation_switch_surcharge
evidence_gated_reroute_discount
minimum_conditioned_weight
maximum_conditioned_weight
metric_nonnegativity_preserved
metric_floor_preserved
metric_ceiling_preserved
evidence_gate_preserved
recovery_protection_preserved
hysteresis_resistance_preserved
oscillation_resistance_preserved
conditioned_metric_digest
metric_certificate_digest
history_read_only
qi_grants_no_authority
future_only
active_now
execution_permission
```

## fail-closed条件

次の場合は証明書を生成しない。

```text
source digestの欠落
空の計量座標集合
座標schema digestの不一致
base metric digestの不一致
重複座標
非有限または非正の基底重み
metric floorまたはceiling違反
負の変形係数
範囲外のQi成分
transition direction mapの座標不一致
未知のtransition direction
reroute evidence digestの欠落
```

runtimeは証拠が存在しない場合、reroute discountを必ずゼロにする。

runtimeはswitch方向のconditioned weightを基底重みより低下させない。

## 不変条件

```text
metric_nonnegativity_preserved = true
metric_floor_preserved = true
metric_ceiling_preserved = true
evidence_gate_preserved = true
recovery_protection_preserved = true
hysteresis_resistance_preserved = true
oscillation_resistance_preserved = true
history_read_only = true
qi_grants_no_authority = true
future_only = true
active_now = false
execution_permission = false
```

Qi-conditioned metricはfuture-only planning metadataである。

計量変形は現在周期を活性化しない。

計量変形はDecisionOSの候補選択を代行しない。

計量変形はActOSの実行権限を生成しない。

## Lean定理

```text
base_metric_coordinate_is_positive
conditioned_metric_coordinate_is_nonnegative
qi_conditioned_quadratic_form_is_nonnegative
recovery_never_reduces_switch_metric
oscillation_never_reduces_switch_metric
reroute_discount_requires_evidence
reroute_discount_preserves_metric_floor
qi_metric_preserves_nonnegativity
qi_metric_grants_no_authority
qi_metric_history_is_read_only
qi_metric_is_future_only_and_not_execution
```

## 接続

本層により、Information-Geometric Qi Objective Kernel系列は次の上流接続を持つ。

```text
Qi process tensor
+ non-Markov history
+ reroute evidence
→ conditioned information metric
→ transition action
→ Plan path action
→ path distribution
```
