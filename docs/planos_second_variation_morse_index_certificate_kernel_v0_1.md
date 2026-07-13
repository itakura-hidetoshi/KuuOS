# PlanOS Second Variation and Morse Index Certificate Kernel v0.1

## 位置づけ

PlanOS v1.09は、候補測地線に沿うJacobi場と測地線偏差を有限window内で検証した。

PlanOS v1.10は、endpoint-fixedな有限変分基底上でエネルギー汎関数の第二変分をindex formとして再構成し、有限基底Morse indexとnullityを計算する。

この層は候補測地線の局所的な変分幾何を記述する。

候補選択、候補棄却、倫理判定、実行許可は行わない。

## Index form

候補測地線の接ベクトルを `T`、endpoint-fixedな変分場を `X,Y` とする。

有限quadrature近似では、

```text
I(X,Y)
= sum_s w_s (
    <D_T X, D_T Y>
    - <R(T,X)T, Y>
  )
```

を使用する。

ここで、

- `w_s`は正のquadrature weight
- `D_T X`は測地線方向の共変微分
- `R(T,X)T`は曲率によるtidal term

である。

runtimeは各基底対についてindex matrixを再計算する。

```text
I_ab = I(X_a, X_b)
```

## Endpoint-fixed変分

各変分基底は初期点と終点の両方で零であることを要求する。

```text
||X_a(0)|| <= epsilon_endpoint
||X_a(T)|| <= epsilon_endpoint
```

endpoint条件を満たさない変分はcertificateへ取り込まれない。

## 対称性

Levi-Civita計量とRiemann曲率のpair symmetryに対応して、index formは対称でなければならない。

```text
I_ab = I_ba
```

runtimeはindex matrixの最大対称性残差を再計算し、明示上限を超えた場合はfail closedする。

## スペクトル分解

対称index matrixに対し、Jacobi回転法で有限次元固有値分解を行う。

固有値は次の三領域へ分類する。

```text
lambda < -epsilon_zero  -> negative
|lambda| <= epsilon_zero -> null
lambda > epsilon_zero   -> positive
```

出力は、

```text
finite_basis_morse_index
finite_basis_nullity
finite_basis_positive_dimension
```

である。

Morse indexは負固有値の本数、nullityは零固有値候補の本数として保持する。

各固有方向について、元の変分基底に対する係数を保持する。

## Jacobi場との関係

Jacobi方程式を満たし、endpoint条件に整合する変分方向では、微分エネルギーと曲率エネルギーが釣り合う。

```text
<D_T X, D_T X>
= <R(T,X)T, X>
```

このときindex integrandは零となる。

したがってnullityは共役点多重度候補と関係する。

ただし、現在のcertificateが保持するのは有限基底・有限window・有限quadrature上の候補であり、大域Morse index theoremそのものではない。

## 基準fixture

基準fixtureは三次元Euclidean metricを使用する。

接ベクトルは、

```text
T = e_x
```

とする。

曲率成分として、

```text
R^y_{x y x} = 0.2
```

を保持する。

三つの変分基底を用いる。

```text
X_negative = e_y, D_T X_negative = 0
X_null     = e_x, D_T X_null = 0
X_positive = e_z, D_T X_positive = e_z
```

index matrixは、

```text
diag(-0.2, 0.0, 1.0)
```

となる。

したがって、

```text
finite_basis_morse_index = 1
finite_basis_nullity = 1
finite_basis_positive_dimension = 1
```

である。

## 数値整合性

runtimeは次を検証する。

```text
trace(I) = sum_a lambda_a
||I||_F^2 = sum_a lambda_a^2
```

さらにJacobi eigensolverの残存非対角成分を明示上限に対して検証する。

## Fail-closed条件

次の場合はcertificateを生成しない。

```text
source Jacobi certificate digest欠落
input digest不一致
metric非対称または非正定値
Riemann tensor schema不一致
空または重複した変分基底
変分source digest欠落または重複
endpoint非零
空または重複したquadrature sample
非正のquadrature weight
零または過小な接ベクトル
sample内のbasis data不一致
非有限component
index form対称性違反
index entry上界違反
固有値上界違反
spectral invariant残差超過
```

## 固定境界

```text
negative second variation != automatic plan rejection
Morse index != candidate ranking
nullity != proven global conjugate multiplicity
conjugate multiplicity candidate != urgency
index form != ethical verdict
spectral direction != activation authorization
curvature evidence != execution
WORLD-conditioned geometry != WORLD mutation
```

本層はsource Jacobi certificateとpersistent WORLD stateを変更しない。

```text
source_jacobi_certificate_not_mutated = true
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
PYTHONPATH=. python3 scripts/check_planos_second_variation_morse_index_certificate_kernel_v0_1.py
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile planos
lake env lean formal/KuuOSPlanOSV1_10.lean
```
