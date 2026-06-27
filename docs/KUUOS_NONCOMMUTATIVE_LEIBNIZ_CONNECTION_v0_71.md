# KuuOS Noncommutative Leibniz Connection v0.71

## 目的

v0.71は、v0.70の有限次元加群束模型を、非可換文脈代数とLeibniz接続へ拡張します。

空OS状態はグラフ上のノード集合ではなく、非可換代数 `A` 上の左加群 `M` として扱います。

接続は、各微分方向についてLeibniz則を満たします。

```text
nabla_i(a m) = delta_i(a) m + a nabla_i(m)
```

## 非可換文脈代数

runtimeでは、文脈代数を有限行列代数として具体化します。

```text
A = M_n(R)
```

一般に、`ab = ba` は成立しません。

微分方向は内部微分として表します。

```text
delta_i(a) = H_i a - a H_i
```

`H_i`同士は可換とします。

これにより、基底代数は非可換のまま、採用する微分方向は可換になります。

## 自由左加群

局所切断は、`n x r`行列として表します。

```text
M = A^r
```

左の文脈代数作用は行列左積です。

```text
a . m = a m
```

fiber endomorphismは右積として作用します。

```text
m . B_i = m B_i
```

## Leibniz接続

接続方向は次で定義します。

```text
nabla_i(m) = H_i m + m B_i
```

このとき、

```text
nabla_i(a m)
  = H_i a m + a m B_i
  = (H_i a - a H_i)m + a(H_i m + m B_i)
  = delta_i(a)m + a nabla_i(m)
```

となり、Leibniz則が成立します。

## 接続差

二つの接続が同じ微分計算に属するとき、差は

```text
(nabla'_i - nabla_i)(m) = m alpha_i
```

です。

右作用は左の文脈代数作用と可換するため、

```text
(nabla'_i - nabla_i)(a m)
  = a (nabla'_i - nabla_i)(m)
```

となります。

したがって、接続空間は加群線形1-formをモデル空間とするアフィン空間になります。

## 曲率

二方向の曲率作用を、

```text
F_ij = nabla_j nabla_i - nabla_i nabla_j
```

とします。

基底微分方向が可換するとき、

```text
F_ij(m) = m(B_i B_j - B_j B_i)
```

となります。

したがって曲率は左 `A`-線形です。

これは、曲率がfiber endomorphismとして表現できることを意味します。

## ゲージ変換

fiber基底変換を `g` とすると、

```text
m^g = m g^{-1}
B_i^g = g B_i g^{-1}
```

です。

このとき、

```text
nabla_i^g(m^g) = (nabla_i m)^g
```

が成立します。

許容ゲージ変換は、v0.70と同じく次を保存します。

- protected部分
- observe部分
- verify部分
- memory部分
- ethics部分
- authority filtration

## v0.70との接続

v0.70の`ModuleConnection`は、v0.71ではLeibniz接続のfiber potential `B_i`として再利用します。

v0.70の変形条件も維持します。

```text
[alpha_i, P_j] = 0
alpha_i | M_protected = 0
alpha_i(F^p M) subset F^p M
```

v0.71は、これらの条件に次を追加します。

- 文脈代数が非可換である具体的witness
- 微分のLeibniz則
- 接続のLeibniz則
- 接続差の左 `A`-線形性
- 曲率の左 `A`-線形性
- 接続作用のゲージ共変性

## rollback

rollbackはv0.70の三層検証を継承します。

- 代数的復元
- 構造的復元
- canonical digest復元

接続差が加群線形であるため、

```text
(nabla + alpha) - alpha = nabla
```

は非可換基底上でも成立します。

## 外部receipt

次は加群要素に含めません。

- digest
- review decision
- validity epoch
- production permission
- execution status

これらは、接続と変形を外側から束縛するimmutable receiptとして保持します。

## 権限継承

v0.71は、v0.69で確定した次の意味論を変更しません。

```text
APPROVE_EVIDENCE grants production application authority
```

v0.71のcandidate検証がlive effectを行わないことと、承認後のproduction適用権は矛盾しません。

前者は候補構成関数の作用境界であり、後者は承認receiptが与える適用権です。

## 実装

```text
runtime/kuuos_noncommutative_differential_calculus_v0_71.py
runtime/kuuos_leibniz_module_connection_v0_71.py
runtime/kuuos_leibniz_candidate_validation_v0_71.py
scripts/check_kuuos_noncommutative_leibniz_v071.py
formal/KUOS/WORLD/KuuOSNoncommutativeLeibnizConnectionV0_71.lean
formal/KuuOSFormalV0_71.lean
```

## Lean定理

- `connection_satisfies_leibniz`
- `difference_of_leibniz_connections_is_module_linear`
- `add_module_linear_deformation_preserves_leibniz`
- `connectionCommutator_smul`
- `commuting_derivations_make_curvature_module_linear`
- `gauge_transform_preserves_module_linearity`
- `rollback_linear_deformation_recovers_connection`

## 境界

v0.71は有限行列代数による局所模型です。

次を主張しません。

- 任意の非可換微分計算をすでに実装したこと
- 無限次元加群束をruntimeで完成したこと
- 有限fixtureが全contextを覆うこと
- 曲率減少がtruth増加を意味すること

## 次段階

自然な次段階は、MemoryOSの履歴依存性を接続へ組み込むことです。

```text
nabla_t(m)
  = nabla_t^(0)(m)
  + integral K(t, tau)m(tau) d tau
```

runtimeでは有限履歴核として開始し、確定済みMemoryOS capsuleをread-only sourceとして扱います。
