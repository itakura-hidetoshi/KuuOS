# PlanOS v0.94: Finite-Temperature Concentration Certificate Kernel v0.1

## 位置づけ

v0.93 はゼロ温度極限で最小作用候補集合に質量が集中する構造を記録した。

v0.94 は有限温度において、非最小作用候補へ残る確率質量を作用ギャップから上界評価し、最小作用支持への集中度を機械可読な証明書として出力する。

## 有限温度分布

候補作用を `A(c)`、最小作用を `A_min`、温度を `tau > 0` とする。

```text
p_tau(c) proportional to exp(-(A(c) - A_min) / tau)
```

最小作用候補集合を `M`、非最小候補集合を `N`、最小正作用ギャップを `Delta` とする。

```text
P_tau(N)
<=
(|N| / max(1, |M|)) * exp(-Delta / tau)
```

この上界と実測非最小質量がともに `epsilon` 以下である場合、`epsilon_concentration_certified = true` とする。

## 同率最小候補

最小作用候補が複数ある場合、全最小候補を `minimal_action_candidate_ids` に保持する。

集中証明書は単一候補選択を行わない。

## 境界

本kernelは確率集中を評価するだけであり、権限、現在周期、実行状態を変更しない。

```text
authority_invariance_preserved = true
history_read_only = true
future_only = true
active_now = false
execution_permission = false
```

## Fail-closed条件

以下を遮断する。

- source zero-temperature limitの欠落
- 非正または非有限の温度
- `0 < epsilon < 1` を満たさない値
- 空の候補作用集合
- 空候補ID
- 負または非有限の作用
- 無効な分配関数

## Lean定理

```text
finite_temperature_mass_is_normalized
finite_temperature_identifies_minimal_support
finite_temperature_nonminimal_mass_is_bounded
finite_temperature_epsilon_concentration_is_certified
finite_temperature_certificate_preserves_governance
finite_temperature_certificate_is_future_only_and_not_execution
exp_gap_bound_nonnegative
```
