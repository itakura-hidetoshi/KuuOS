# PlanOS Native Coupled Information Metric Certificate Kernel v0.1

## 位置づけ

PlanOS v0.99は、有限Plan座標上のQi・履歴条件付き対角計量を構成した。

```text
G_QH = diag(g_i)
```

PlanOS v1.00は、WORLD counterfactual projectionから候補別のpullback計量を構成した。

```text
G_pullback = J^T G_W J
```

v1.00のpullback行列は一般に非対角だが、PlanOS自身の内在的計量は対角のままであった。

PlanOS v1.05は、計画変数間の内在的結合を第一級の計量成分として導入する。

```text
G_QHC = D_QH + B^T B
```

ここで、`D_QH`はv0.99由来の正の対角計量、`B`はprovenance-boundな有限coupling factorである。

## Gram型非対角計量

各Plan座標を `theta_i`、coupling factorを `B_ri` とする。

```text
(G_QHC)_ij = d_i delta_ij + sum_r B_ri B_rj
```

したがって、`i != j`について、

```text
(G_QHC)_ij = sum_r B_ri B_rj
```

が計画変数間の結合を表す。

任意の有限ベクトル `v` に対して、

```text
v^T G_QHC v
= sum_i d_i v_i^2 + sum_r (sum_i B_ri v_i)^2
```

である。

`d_i > 0`であるため、非零 `v` に対してこの値は正であり、`G_QHC`は対称正定値となる。

## 有界性

入力は正の下界と有限上界を持つ。

```text
0 < lambda_floor <= min_i d_i
max_i d_i + ||B||_F^2 <= lambda_ceiling
```

これにより、

```text
lambda_floor ||v||^2
<= v^T G_QHC v
<= lambda_ceiling ||v||^2
```

を安全な有限次元上界として扱える。

runtimeは固有値の数値近似へ依存せず、対角下界とFrobenius上界を再計算する。

## 候補作用

各候補のPlan差分を `delta theta` とする。

```text
A_QHC(delta theta)
= 1/2 delta theta^T G_QHC delta theta
= A_diagonal + A_gram
```

```text
A_diagonal
= 1/2 sum_i d_i (delta theta_i)^2
```

```text
A_gram
= 1/2 sum_r (sum_i B_ri delta theta_i)^2
```

`A_gram`は平方和であり、負にならない。

## 相乗作用とトレードオフ

full matrix actionは、対角成分とpairwise interactionへ分解される。

```text
A_QHC
= 1/2 sum_i G_ii (delta theta_i)^2
  + sum_{i<j} G_ij delta theta_i delta theta_j
```

pairwise contributionを、

```text
I_ij = G_ij delta theta_i delta theta_j
```

とする。

分類は `G_ij` の符号だけではなく、候補の変位方向を含む `I_ij` の符号で行う。

```text
I_ij < 0  -> synergy
I_ij = 0  -> neutral
I_ij > 0  -> tradeoff
```

したがって、同じmetric entryでも、候補経路の方向が変われば相乗・競合の意味は変わり得る。

certificateは各候補について次を保持する。

```text
coordinate_i
coordinate_j
metric_entry
delta_i
delta_j
interaction_contribution
interaction_disposition
```

## WORLD pullbackとの合成

PlanOS v1.00のWORLD pullbackを加えると、

```text
G_QHCW
= D_QH + B^T B + lambda_W J^T G_W J
```

となる。

```text
lambda_W >= 0
G_W >= 0
```

であるため、WORLD pullback項は半正定値であり、`D_QH + B^T B`の正定値性を失わせない。

v1.05はv1.00 source certificate digestを保持するが、persistent WORLD stateを変更しない。

## 対角計量との互換性

```text
B = 0
```

とすれば、

```text
G_QHC = D_QH
```

となる。

したがってv0.99の対角計量はv1.05の特殊例として保持される。

ただしv1.05 certificateの正常系では、少なくとも一つの非零非対角成分を要求する。対角のみのfactorは、非対角coupling導入を偽装するため拒否される。

## digest binding

次をcanonical digestへ固定する。

```text
Plan coordinate schema
base diagonal metric
coupling factor rows
candidate delta bundle
source v0.99 metric certificate
source v1.00 WORLD-conditioned metric certificate
```

coupling factorは、factor ID、全座標係数、provenance digestを保持する。

候補はcandidate ID、全座標差分、source candidate digestを保持する。

重複ID、重複provenance、重複source candidate digestは拒否する。

## fail-closed条件

次の場合はcertificateを生成しない。

```text
source certificate digest欠落
Plan coordinate schema digest不一致
base metric digest不一致
coupling factor digest不一致
candidate delta bundle digest不一致
空または重複したPlan座標
非有限または非正のbase weight
空または重複したcoupling factor
coupling provenance欠落または重複
coupling coordinate不一致
全ゼロcoupling
非対角成分を生成しないcoupling
空または重複したcandidate field
candidate delta coordinate不一致
source candidate digest欠落または重複
非有限candidate delta
非正のmetric floor
metric ceilingがfloor未満
再計算上界がmetric ceilingを超える
matrix action identity不一致
pairwise decomposition identity不一致
負のGram coupling action
```

## 固定境界

```text
coupled metric != candidate selection
metric action != DecisionOS verdict
synergy classification != execution recommendation
WORLD pullback composition != WORLD mutation
Qi conditioning != authority grant
```

本層は候補を保持し、候補選択を行わない。

```text
candidate_field_retained = true
decision_selection_performed = false
```

本層はread-onlyかつfuture-onlyである。

```text
history_read_only = true
source_metric_not_mutated = true
future_only = true
active_now = false
execution_permission = false
```

Qi、WORLD projection、metric certificateから、選択権限、実行権限、WORLD mutation権限は生成されない。

## 検証

```bash
PYTHONPATH=. python3 scripts/check_planos_native_coupled_information_metric_certificate_kernel_v0_1.py
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile planos
lake env lean formal/KuuOSPlanOSV1_05.lean
```
