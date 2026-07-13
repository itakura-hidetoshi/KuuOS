# PlanOS Finite p-Wasserstein Persistence Transport Certificate Kernel v0.1

## 位置づけ

PlanOS v1.18は、2つの有限persistence diagramについて、対角点を許すbottleneck matchingと有限摂動安定性witnessを保持した。

PlanOS v1.19は、同じ有限diagram対を有限 `p`-Wasserstein transportへ拡張する。

各matching edgeのcostを `c_e` とすると、

```text
sum_e c_e^p
```

を最小化し、総輸送cost、cost moment、tail count、bottleneckとの有限関係をcertificate化する。

この層は有限diagram・有限dimension・有界な `p` に限定される。

一般のpersistence stability theorem、無限diagram transport、候補ranking、activationまたはexecution権限は主張しない。

## Exact doubled-cost encoding

v1.18と同じく、距離は数学的値の2倍を整数で保持する。

有限interval間では、

```text
cost_twice
= 2 * max(
    abs(birth_left - birth_right),
    abs(death_left - death_right)
  )
```

無限interval間では、

```text
cost_twice
= 2 * abs(birth_left - birth_right)
```

有限intervalと対角線のcostは、

```text
cost_twice
= death - birth
```

である。

無限intervalは対角線へ送れない。

## p-Wasserstein objective

`p_exponent` は正の整数であり、runtimeでは明示された上限以下に制限する。

総輸送powerは、

```text
transport_power_sum_twice_units
= sum_e cost_twice(e)^p
```

である。

数学的なp-Wasserstein距離 `W_p` との関係は、

```text
transport_power_sum_twice_units
= (2 * W_p)^p
```

である。

matchingはhomology dimension `0`, `1`, `2` ごとに有限dynamic programmingで求める。

目的関数は総power sumである。

同値な解では、

```text
smaller maximum edge cost
point-to-point before diagonal
lexicographic interval identifiers
```

の順で決定する。

## Integer root bracket

総power sumが完全 `p` 乗でない場合、無理根を浮動小数点へ丸めない。

代わりに、

```text
floor_twice^p <= transport_power_sum_twice_units
transport_power_sum_twice_units <= ceil_twice^p
```

を満たす整数root bracketを保持する。

完全 `p` 乗の場合に限り、

```text
wasserstein_distance_rational
= root_twice / 2
```

を出力する。

## Moment profile

matching costについて、order `1` から `p` まで、

```text
moment(order)
= sum_e cost_twice(e)^order
```

を再計算する。

`order = p` のmomentは総輸送powerと一致する。

## Tail profile

各正のthreshold `T` について、

```text
count_at_or_above(T)
= number of e with cost_twice(e) >= T
```

を再計算する。

さらに、

```text
count_at_or_above(T) * T^p
<= transport_power_sum_twice_units
```

をexact integerで検証する。

これは有限matching上のMarkov型tail lower boundである。

## Bottleneck–Wasserstein finite bounds

v1.18のbottleneck距離を独立再計算する。

有限matching cardinalityを `N` とすると、

```text
bottleneck_twice^p
<= transport_power_sum_twice_units
```

および、

```text
transport_power_sum_twice_units
<= N * bottleneck_twice^p
```

を検証する。

また、v1.18の有限摂動witness

```text
bottleneck_twice <= 2 * filtration_sup_norm
```

から、

```text
transport_power_sum_twice_units
<= N * (2 * filtration_sup_norm)^p
```

を確認する。

これは保持された有限instanceのcardinality付き上界であり、一般のp-Wasserstein stability theoremではない。

## 基準fixture

Diagram A:

```text
H0 [0,2)
H0 [0,infinity)
H1 [2,6)
```

Diagram B:

```text
H0 [1,3)
H0 [1,infinity)
H1 [3,7)
H1 [4,6)
```

`p = 2` の最適輸送は、3本のpoint-to-point matchingと1本のdiagonal-to-right matchingで構成される。

全edgeの `cost_twice` は2である。

したがって、

```text
transport_power_sum_twice_units = 4 * 2^2 = 16
2 * W_2 = 4
W_2 = 2
```

moment profileは、

```text
order 1: 8
order 2: 16
```

である。

tail profileは、

```text
threshold 1: count 4, lower bound 4
threshold 2: count 4, lower bound 16
threshold 3: count 0, lower bound 0
```

である。

`p = 3` では、

```text
transport_power_sum_twice_units = 32
3^3 < 32 < 4^3
```

となるため、root bracket `[3,4]` を保持し、小数近似は出力しない。

## Digest binding

次をcanonical digestへ固定する。

```text
diagram A intervals
diagram B intervals
simplex perturbation records
p exponent
tail thresholds
claimed optimal transport matching
claimed transport power sum
claimed integer root bracket
claimed bottleneck distance
claimed filtration sup norm
claimed moment profile
claimed tail profile
```

source v1.17 persistent-homology certificate digestsとsource v1.18 bottleneck certificate digestも保持する。

## Fail-closed条件

次の場合はcertificateを生成しない。

```text
source digest欠落
input digest不一致
p <= 0
p upper bound超過
interval schema不正
simplex endpoint binding不一致
無限intervalのpartner欠落
無限intervalの対角matching
matching claim改変
cost power改変
transport power sum改変
integer root bracket改変
bottleneck claim改変
filtration sup norm改変
moment profile改変
tail profile改変
tail threshold非単調または非正
bottleneck lower bound違反
finite-cardinality upper bound違反
finite perturbation budget違反
tail power bound違反
record count上限超過
```

## 固定境界

```text
finite diagram pair != all persistence diagrams
finite p range != arbitrary p
power-sum witness != complete transport theory
integer root bracket != decimal approximation
observed finite bound != general stability theorem
large moment != candidate utility
heavy tail != automatic rejection
small Wasserstein distance != activation authorization
diagonal matching != deletion authority
transport plan != executable plan
WORLD-conditioned topology != WORLD mutation
```

source certificateとpersistent WORLD stateは変更しない。

```text
source_persistent_homology_certificate_a_not_mutated = true
source_persistent_homology_certificate_b_not_mutated = true
source_bottleneck_stability_certificate_not_mutated = true
persistent_world_state_unchanged = true
```

候補identityを保持し、選択を行わない。

```text
candidate_identity_retained = true
decision_selection_performed = false
```

read-onlyかつfuture-onlyである。

```text
history_read_only = true
future_only = true
active_now = false
execution_permission = false
```

## 検証

```bash
PYTHONPATH=. python3 scripts/check_planos_finite_p_wasserstein_persistence_transport_certificate_kernel_v0_1.py
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile planos
lake env lean formal/KuuOSPlanOSV1_19.lean
```
