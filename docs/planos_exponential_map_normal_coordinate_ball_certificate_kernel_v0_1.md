# PlanOS Exponential Map and Normal Coordinate Ball Certificate Kernel v0.1

## 位置づけ

PlanOS v1.11は、有限window内の共役点イベント列、Morse index jump、cut-locus候補、局所injectivity-radius下界を保持した。

PlanOS v1.12は、その下界より厳密に小さい半径内で、基点 `p` における指数写像の有限二次局所モデル、normal-coordinate ball、基点からのradial geodesic一意性、有限sample injectivity、chart-safe被覆をcertificate化する。

本層は局所・有限sampleモデルである。

大域指数写像、strong convexity、任意の二終点間の一意測地線、完全なnormal neighborhoodは主張しない。

## 二次局所指数モデル

基点を `p`、接ベクトルを `v`、基点上のChristoffel記号を `Gamma` とする。

runtimeは次の二次局所モデルを再計算する。

```text
exp_p(v)^i
= p^i + v^i - 1/2 Gamma^i_jk v^j v^k
```

radial parameter `t` に沿う有限局所モデルは、

```text
gamma_v(t)^i
= p^i + t v^i - 1/2 t^2 Gamma^i_jk v^j v^k
```

である。

各candidateは、

```text
candidate_id
tangent_vector
expected_endpoint
expected_midpoint
assigned_chart_id
source_candidate_digest
```

を保持する。

runtimeは `t=1` のendpointと `t=1/2` のmidpointを独立再計算し、明示されたresidual上限以内であることを要求する。

## Normal-coordinate ball

v1.11由来の局所injectivity-radius下界を `r_inj`、v1.12で採用するnormal-coordinate ball半径を `r_normal` とする。

```text
0 < r_normal < r_inj
```

を必須条件とする。

各candidate tangentについて、基点metric `g` による有限座標normを計算する。

```text
||v||_g^2 = v^i g_ij v^j
```

```text
0 < ||v||_g < r_normal
```

を要求する。

この範囲では、v1.11の保持されたobstruction-free下界に基づき、基点からcandidate endpointへ向かうradial geodesicの局所一意性witnessを保持する。

これは基点からのradial一意性であり、ball内の任意の二点間の一意測地線またはstrong convexityではない。

## 有限sample injectivity

複数の保持candidateについて、再計算されたendpoint間の距離を調べる。

```text
separation(exp_p(v_a), exp_p(v_b))
>= minimum_distinct_endpoint_separation
```

を要求する。

したがって、保持された有限sample集合上で指数写像がinjectiveであることをcertificate化できる。

これは連続な接球全体に対する指数写像injectivityの完全証明ではない。

## Chart-safe geodesic-ball covering

v1.08 atlas lineageからchart digestを受け取り、各chartについて次を保持する。

```text
chart_id
center
safe_radius
coordinate_lower_bounds
coordinate_upper_bounds
source_chart_digest
```

各candidateの再計算endpointとmidpointが、割り当てchartのcoordinate bounds内にあり、chart centerからsafe radius以内にあることを検証する。

```text
endpoint in chart bounds
midpoint in chart bounds
endpoint distance to chart center <= safe_radius
midpoint distance to chart center <= safe_radius
```

atlas transition lawそのものはv1.08のauthorityを越えて再定義しない。

```text
atlas_transition_authority_not_extended = true
```

## 基準fixture

二次元座標 `x,y`、Euclidean metric、非零の有限Christoffel成分を使う。

```text
Gamma^x_yy = 0.1
Gamma^y_xy = Gamma^y_yx = 0.05
```

candidate A:

```text
v = (0.5, 0.2)
exp_p(v) = (0.498, 0.195)
gamma_v(1/2) = (0.2495, 0.09875)
```

candidate B:

```text
v = (-0.3, 0.4)
exp_p(v) = (-0.308, 0.406)
gamma_v(1/2) = (-0.152, 0.2015)
```

```text
r_inj = 1.5
r_normal = 0.8
```

両candidateはnormal ball内にあり、primary chartで安全に被覆され、endpointは有限sample separation下界を満たす。

## Digest binding

次をcanonical digestへ固定する。

```text
coordinate schema
base point
metric matrix
Christoffel symbols
chart records
radial geodesic candidates
```

sourceとして、

```text
v1.11 injectivity-radius certificate digest
v1.08 atlas certificate digest
```

を保持する。

## Fail-closed条件

次の場合はcertificateを生成しない。

```text
source digest欠落
local model input digest不一致
coordinate schema不正
base point schema不正
metric非対称
metric非正定値
Christoffel schema不正または非有限
chart空集合
chart IDまたはsource digest重複
chart bounds順序不正
chart centerがbounds外
candidate空集合
candidate IDまたはsource digest重複
零またはnull tangent
candidate tangentがnormal ball外
normal ball半径がinjectivity下界以上
endpoint residual超過
midpoint residual超過
assigned chart欠落
endpointまたはmidpointがchart bounds外
endpointまたはmidpointがchart safe radius外
有限sample endpoint separation不足
非有限component
```

## Mathlib層

Leanでは次を固定する。

```text
zero tangent -> exp model returns base point
zero connection -> exp model is base + tangent
radial parameter 0 -> base point
radial parameter 1 -> second-order exp model
strict normal-ball bound -> positive injectivity bound
smaller positive ball preserves injectivity-bound inclusion
finite-sample injectivity -> equal endpoints imply equal tangents
explicit chart witness -> chart coverage
local exponential evidence grants no authority
```

## 固定境界

```text
local exponential model != global exponential map
normal ball witness != strong convexity
radial uniqueness from basepoint != arbitrary endpoint-pair uniqueness
finite sample injectivity != continuum injectivity theorem
chart-safe covering != atlas mutation
geometric locality != candidate selection
normal coordinates != activation authorization
WORLD-conditioned geometry != WORLD mutation
```

本層はsource certificateを変更しない。

```text
source_injectivity_certificate_not_mutated = true
source_atlas_certificate_not_mutated = true
persistent_world_state_unchanged = true
```

candidate identityを保持し、選択を行わない。

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
PYTHONPATH=. python3 scripts/check_planos_exponential_map_normal_coordinate_ball_certificate_kernel_v0_1.py
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile planos
lake env lean formal/KuuOSPlanOSV1_12.lean
```
