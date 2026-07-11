# PlanOS Temperature Trajectory Receipt Kernel v0.1

## 位置づけ

本層は、PlanOS v0.96 が生成した有界な Qi temperature 更新を、非マルコフ温度軌跡へ一件だけ追記する receipt として固定する。

温度更新は実行権限ではない。

本層は、過去履歴を書き換えず、次周期用の温度変化、方向、disposition、振動量、反転回数を記録する。

## 記録対象

```text
source_rate_limit_receipt_digest
prior_trajectory_digest
cycle_ordinal
previous_temperature
target_temperature
bounded_temperature
temperature_delta
direction
disposition
reversal_count
oscillation_measure
trajectory_append_count
temperature_trajectory_receipt_digest
```

`trajectory_append_count` は常に1である。

## 方向整合性

```text
hold_deadband
→ bounded_temperature = previous_temperature

increase_rate_limited
→ bounded_temperature >= previous_temperature

decrease_rate_limited
→ bounded_temperature <= previous_temperature
```

方向と disposition が一致しない場合は fail-closed とする。

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
trajectory_append_is_singleton
temperature_trajectory_grants_no_authority
temperature_trajectory_history_is_read_only
temperature_trajectory_is_future_only_and_not_execution
temperature_delta_identity
```
