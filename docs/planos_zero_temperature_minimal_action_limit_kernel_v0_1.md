# PlanOS Zero-Temperature Minimal-Action Limit Kernel v0.1

## 位置づけ

本層は、v0.92のKL正則化更新に対する低温極限を有限候補集合上で具体化する。

温度が正の場合、候補分布は最小作用候補の近傍にも正の質量を保持する。

温度がゼロへ近づく極限では、質量は許容候補のうち最小作用を持つ候補集合へ集中する。

## 離散極限

候補作用を `A(c)` とする。

正温度分布は次で定義する。

```text
p_tau(c) proportional to exp(-(A(c)-A_min)/tau)
```

ゼロ温度極限は次で定義する。

```text
p_0(c) = 0                         if A(c) > A_min
p_0(c) = 1 / number_of_minimizers  if A(c) = A_min
```

最小作用候補が複数存在する場合、kernelは恣意的な単一選択を行わず、最小作用支持上に質量を保持する。

## 境界

本層は次を保存する。

```text
admissible_support_preserved = true
minimal_action_support_identified = true
authority_invariance_preserved = true
history_read_only = true
future_only = true
active_now = false
execution_permission = false
```

ゼロ温度極限は探索幅を閉じるが、権限を増加させず、現在周期を変更せず、実行許可を生成しない。

## Fail-closed条件

次を遮断する。

```text
source update missing
nonpositive temperature
empty candidate action field
negative or nonfinite action
empty minimal-action support
selection outside minimal-action support
invalid partition function
```

## Lean定理

```text
zero_temperature_limit_selects_minimal_action_admissible_paths
zero_temperature_minimizers_carry_unit_mass
zero_temperature_limit_preserves_governance
zero_temperature_limit_is_future_only_and_not_execution
```
