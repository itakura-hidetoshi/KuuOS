# PlanOS Adaptive Qi Temperature Calibration Kernel v0.1

## 位置づけ

本層は、v0.94の有限温度集中証明書を入力として、次周期に用いるQi temperatureを有界に校正する。

Qi temperatureは探索幅を調整するが、権限境界を変更しない。

## 集中上限

最小作用候補数をm、非最小候補数をn、最小正作用ギャップをΔ、許容非最小質量をεとする。

指数上界

```text
(n / m) * exp(-Δ / τ) <= ε
```

を満たす温度上限を計算する。

```text
τ <= Δ / log(n / (m ε))
```

集中証明を必須とする場合、校正温度はこの上限を越えない。

## Qi適応

activation、stagnation、transition readinessは探索側の信号として扱う。

recovery、coherence、hysteresis、history oscillationは安定化側の信号として扱う。

両者からraw temperatureを構成し、明示的な最小温度、最大温度、集中温度上限の範囲へ射影する。

## Fail-closed境界

次を遮断する。

- source concentration certificateの欠落
- 非正または非有限の温度
- 最小温度と最大温度の逆転
- 不正なtarget epsilon
- 不正な作用ギャップまたは支持数
- 負または非有限のQi・履歴信号
- 要求された集中条件を満たす温度が存在しない状態

## 不変条件

```text
concentration_bound_preserved = true
qi_grants_no_authority = true
history_read_only = true
future_only = true
active_now = false
execution_permission = false
```

PlanOSは温度を校正するが、現在周期を活性化せず、実行権限を生成しない。
