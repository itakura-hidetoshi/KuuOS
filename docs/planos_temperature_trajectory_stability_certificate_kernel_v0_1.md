# PlanOS Temperature Trajectory Stability Certificate Kernel v0.1

## 位置づけ

本層は、PlanOS v0.97 が追記した温度軌跡を有限windowとして検証し、有界性、連続性、非振動性を証明書化する。

温度安定性の判定は、候補選択、周期開始、実行許可を発生させない。

履歴は検証入力として参照するだけであり、source trajectoryを書き換えない。

## 入力

```text
source_temperature_trajectory_receipt_digest
trajectory_window_digest
window_start_ordinal
window_end_ordinal
trajectory_records
minimum_temperature
effective_temperature_ceiling
maximum_up_step
maximum_down_step
stability_thresholds
```

`trajectory_window_digest` は、canonical JSONで表現した `trajectory_records` 配列のSHA-256 digestである。

source receipt digestはwindow末尾のv0.97 receipt digestへ直接束縛する。

## fail-closed検証

各recordの自己digestを再計算する。

cycle ordinalはwindow開始値から終了値まで重複なく連続しなければならない。

各recordの `prior_trajectory_digest` は直前recordのreceipt digestと一致しなければならない。

各recordの `previous_temperature` は直前recordの `bounded_temperature` と一致しなければならない。

`temperature_delta` は `bounded_temperature - previous_temperature` と一致しなければならない。

方向、disposition、温度差の符号は一致しなければならない。

全温度は有限かつ正であり、minimum temperature以上、effective concentration ceiling以下でなければならない。

上昇stepと下降stepは、それぞれ指定されたrate limitを超えてはならない。

record countはinclusive window lengthと一致しなければならない。

## 評価量

```text
total_variation = sum(abs(temperature_delta))
net_temperature_drift = final_bounded_temperature - initial_previous_temperature
reversal_density = reversal_count / max(1, record_count - 1)
mean_absolute_step = total_variation / record_count
oscillation_measure = max(record oscillation measure)
```

holdを挟む場合も、直前の非hold方向から反対方向へ移った時点を一回の反転として数える。

## disposition

```text
stable
damped
drifting
oscillatory
insufficient_evidence
```

record数が閾値未満なら `insufficient_evidence` とする。

反転密度または振動量が閾値を超える場合は `oscillatory` とする。

net driftが閾値を超える場合は `drifting` とする。

total variationとmean absolute stepが閾値内なら `stable` とする。

それ以外では、window後半の平均stepが前半以下なら `damped` とし、増大していれば `drifting` とする。

## 証明書

```text
source_trajectory_receipt_digest
trajectory_window_digest
window_start_ordinal
window_end_ordinal
record_count
hold_count
increase_count
decrease_count
reversal_count
total_variation
net_temperature_drift
maximum_observed_step
mean_absolute_step
oscillation_measure
rate_limit_preserved
temperature_bounds_preserved
concentration_ceiling_preserved
ordinal_continuity_preserved
digest_chain_preserved
stability_disposition
stability_certificate_digest
history_read_only
qi_grants_no_authority
future_only
active_now
execution_permission
```

## 不変条件

```text
history_read_only = true
qi_grants_no_authority = true
future_only = true
active_now = false
execution_permission = false
```

## Lean定理

```text
temperature_total_variation_is_nonnegative
bounded_steps_bound_total_variation
reversal_count_is_bounded_by_transition_count
trajectory_ordinals_are_contiguous
trajectory_digest_chain_is_preserved
stable_trajectory_preserves_temperature_bounds
stable_trajectory_preserves_concentration_ceiling
temperature_stability_grants_no_authority
temperature_stability_history_is_read_only
temperature_stability_is_future_only_and_not_execution
```
