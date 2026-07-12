# PlanOS Second-Order Metric Jet Curvature Certificate Kernel v0.1

## 位置づけ

PlanOS v1.05は、有限Plan座標上に内在的な非対角正定値計量を導入した。

```text
G_QHC = D_QH + B^T B
```

PlanOS v1.06は、この計量を局所状態依存の一次jetへ昇格し、Levi-Civita接続を再構成した。

```text
G = G(theta, Q, H, W)
g_ij
partial_k g_ij
Gamma^i_jk
```

PlanOS v1.07は二次metric jetを導入し、接続の局所変化と曲率を第一級certificateとして保持する。

```text
partial_a partial_b g_ij
partial_a Gamma^i_jk
R^i_jkl
Ric_jl
R
```

ここで、`H`と`W`はread-onlyであり、persistent WORLD stateは変更されない。

## 二次metric jet

入力は次である。

```text
g_ij
(g^-1)^ij
partial_a g_ij
partial_a partial_b g_ij
```

二次jetは、metric添字と微分添字の双方で整合性を要求する。

```text
partial_a partial_b g_ij
= partial_a partial_b g_ji

partial_a partial_b g_ij
= partial_b partial_a g_ij
```

runtimeは全成分を有限値として検証し、明示された絶対上界を超えるjetを拒否する。

## 逆計量の微分

逆計量の一次微分を、

```text
partial_a g^{il}
= - g^{ip} (partial_a g_pq) g^{ql}
```

として再構成する。

次の左右両側の微分恒等式を数値的に検証する。

```text
partial_a(g^-1 g) = 0
partial_a(g g^-1) = 0
```

## Christoffel記号の微分

第一種Christoffel記号はv1.06と同じ規約を使う。

```text
Gamma_ijk
= 1/2(
    partial_j g_ik
  + partial_k g_ij
  - partial_i g_jk
  )
```

その微分は、

```text
partial_a Gamma_ijk
= 1/2(
    partial_a partial_j g_ik
  + partial_a partial_k g_ij
  - partial_a partial_i g_jk
  )
```

である。

第一添字を上げた接続の微分は積の微分から得る。

```text
partial_a Gamma^i_jk
= (partial_a g^{il}) Gamma_ljk
  + g^{il} partial_a Gamma_ljk
```

## Riemann曲率

repositoryの添字規約は、

```text
R^i_jkl
= partial_k Gamma^i_lj
  - partial_l Gamma^i_kj
  + Gamma^i_km Gamma^m_lj
  - Gamma^i_lm Gamma^m_kj
```

である。

この規約では、最後の二添字について、

```text
R^i_jkl = -R^i_jlk
```

が成立する。

torsion-free接続と、その微分の下二添字対称性から、第一Bianchi恒等式を検証する。

```text
R^i_jkl
+ R^i_klj
+ R^i_ljk
= 0
```

第一添字を計量で下げ、

```text
R_ijkl = g_im R^m_jkl
```

とする。

runtimeはLevi-Civita曲率に固有のpair symmetryも検証する。

```text
R_ijkl = -R_jikl
R_ijkl = -R_ijlk
R_ijkl = R_klij
```

## Ricci曲率とscalar curvature

Ricci曲率は、

```text
Ric_jl = R^i_jil
```

である。

Levi-Civita接続由来のRicci曲率について、

```text
Ric_jl = Ric_lj
```

を検証する。

scalar curvatureは、

```text
Scal = g^{jl} Ric_jl
```

として再計算する。

## Sectional curvature

候補ごとに、二本の独立な接ベクトル`u`と`v`を保持する。

二平面のGram行列式は、

```text
Delta(u,v)
= g(u,u) g(v,v) - g(u,v)^2
```

である。

```text
Delta(u,v) > 0
```

を要求し、退化した二平面は拒否する。

repository規約におけるsectional curvatureは、

```text
K(u,v)
= R_ijkl u^i v^j v^k u^l
  / Delta(u,v)
```

である。

candidate ID、source candidate digest、二平面、Gram行列式、分子、sectional curvatureを保持する。

## 微小holonomy

同じ`u`,`v`を微小矩形loopの有向辺として用いる。

接ベクトル`w`に対する第一非自明holonomy項を、

```text
Delta_hol w^i
= R^i_jkl w^j u^k v^l
```

として保持する。

これは有限loopの完全なparallel transportではなく、局所曲率が生成する微小loop作用である。

```text
infinitesimal holonomy != execution
```

runtimeは各loop edge成分とholonomy increment成分の絶対上界を検証する。

## digest binding

次をcanonical digestへ固定する。

```text
source PlanOS v1.06 Levi-Civita certificate
Plan coordinate schema
state context
source first-order metric jet
second-order metric jet
candidate plane bundle
```

second-order metric jet digestは、

```text
source_metric_jet_digest
metric_second_derivatives
```

を束縛する。

candidate plane bundleは、

```text
candidate_id
plane_u
plane_v
holonomy_vector
source_candidate_digest
```

を束縛する。

重複candidate ID、重複source candidate digest、stale digestは拒否する。

## fail-closed条件

次の場合はcertificateを生成しない。

```text
source certificate digest欠落
state context digest欠落
Plan coordinate schema digest不一致
二次元未満のchart
metric schema不一致
metric非対称
metric非正定値
inverse metric不一致
first metric derivative非対称
second metric derivativeのmetric添字非対称
mixed partial非対称
second-order metric jet欠落
second-order metric jet digest不一致
candidate plane bundle digest不一致
空または重複したcandidate plane field
非有限成分
二次jet上界超過
inverse metric derivative恒等式不一致
connection derivative上界超過
Riemann反対称性不一致
第一Bianchi恒等式不一致
lower Riemann pair symmetry不一致
非自明曲率欠落
Riemann上界超過
Ricci非対称
Ricci上界超過
scalar curvature上界超過
退化二平面
sectional curvature上界超過
loop edge上界超過
holonomy increment上界超過
```

## 固定境界

```text
curvature != candidate selection
sectional curvature != plan ranking
Ricci curvature != ethical verdict
scalar curvature != global truth
holonomy != execution
singularity signal != command
WORLD-conditioned second jet != WORLD mutation
```

本層はcandidate plane fieldを保持し、選択を行わない。

```text
candidate_plane_field_retained = true
decision_selection_performed = false
```

本層はread-onlyかつfuture-onlyである。

```text
history_read_only = true
persistent_world_state_unchanged = true
future_only = true
active_now = false
execution_permission = false
```

接続と曲率から、選択権限・実行権限・WORLD mutation権限は生成されない。

## Mathlib package

formal layerは次を証明する。

```text
R^i_jkl = -R^i_jlk
```

torsion-free接続とその微分対称性の下で、

```text
R^i_jkl + R^i_klj + R^i_ljk = 0
```

また、零接続かつ零接続微分なら、

```text
Riemann = 0
Ricci = 0
scalar curvature = 0
sectional numerator = 0
infinitesimal holonomy = 0
```

を証明する。

## 検証

```bash
PYTHONPATH=. python3 scripts/check_planos_second_order_metric_jet_curvature_certificate_kernel_v0_1.py
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile planos
lake env lean formal/KuuOSPlanOSV1_07.lean
```
