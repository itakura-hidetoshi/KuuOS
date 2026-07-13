# PlanOS Finite Normal-Ball Cover and Bounded Hopf–Rinow Witness Certificate Kernel v0.1

## 位置づけ

PlanOS v1.12は、v1.11の局所injectivity-radius下界の内部で、二次局所指数モデル、normal-coordinate ball、基点からのradial geodesic witness、有限sample injectivity、chart-safe coveringを保持した。

PlanOS v1.13は、複数のv1.12 normal ballを有限被覆として束ね、ball overlapを通過する局所測地線extension chainを構成する。

その結果を、有限windowに限定した

```text
bounded Hopf–Rinow finite-window witness
```

として保持する。

これは古典的Hopf–Rinow定理の同値条件、測地線完備性、距離完備性、閉有界集合のコンパクト性、大域最短測地線の存在を主張しない。

## Finite normal-ball cover

各normal ballは次を保持する。

```text
ball_id
center
radius
source_injectivity_radius_lower_bound
chart_id
source_normal_ball_digest
```

各ballについて、

```text
0 < radius < source_injectivity_radius_lower_bound
```

を要求する。

したがって、v1.12で保持された局所injectivity下界の内部にある有限normal ballのみを利用する。

## Retained sample coverage

各有限sample pointは、明示されたnormal ballへ割り当てられる。

```text
sample_id
point
assigned_ball_id
source_sample_digest
```

runtimeは、

```text
distance(point, center_assigned) < radius_assigned
```

を再計算する。

これは保持された有限sample集合の被覆であり、対象空間全体の有限被覆ではない。

## Ball overlap witness

ballを切り替える場合、明示的なoverlap witnessを要求する。

```text
overlap_id
left_ball_id
right_ball_id
witness_point
source_overlap_digest
```

witness pointについて、

```text
radius_left - distance(center_left, witness) >= minimum_overlap_margin
radius_right - distance(center_right, witness) >= minimum_overlap_margin
```

を検証する。

隣接extension segmentが異なるballを使用する場合、そのjunction pointは対応するoverlap witnessと一致しなければならない。

## Local geodesic extension chain

各segmentは、

```text
segment_id
start_parameter
end_parameter
length
start_point
end_point
start_tangent
end_tangent
normal_ball_id
source_segment_digest
```

を保持する。

runtimeは、

```text
length = end_parameter - start_parameter
```

を再計算する。

さらに、segmentが割り当てられたnormal ball内に留まり、

```text
length <= maximum_segment_length_fraction * normal_ball_radius
```

を満たすことを要求する。

`maximum_segment_length_fraction` は、

```text
0 < fraction < 1
```

に限定する。

## Chain continuity

隣接segment間で、

```text
left.end_parameter = right.start_parameter
left.end_point = right.start_point
```

を検証する。

接ベクトルjumpは、明示された有限上限以下でなければならない。

異なるballへ切り替わるjunctionでは、対応するoverlap witnessが必要である。

## Finite-window extension

finite windowを、

```text
[finite_window_start, finite_window_end]
```

とする。

最初のsegmentはwindow開始点から始まり、最後のsegmentはwindow終端へ到達しなければならない。

また、

```text
sum(segment.length)
= finite_window_end - finite_window_start
```

を要求する。

これにより、保持されたsegment chainが有限window全体を覆うことを証明する。

## Bounded Hopf–Rinow finite-window witness

本kernelで保持するwitnessは、次の有限情報の組である。

```text
finite retained normal-ball cover
retained sample coverage
normal-ball overlap chain
local extension segment chain
positive finite parameter window
finite coordinate envelope
```

この組を、

```text
bounded_hopf_rinow_finite_window_witness = true
```

として保持する。

意味は、有限window上で局所normal geometryを貼り合わせ、保持されたpathを終端まで延長できた、ということである。

次の主張には昇格しない。

```text
classical Hopf–Rinow equivalence
global geodesic completeness
global metric completeness
global compactness
global existence of minimizing geodesics
```

## 基準fixture

二つのnormal ballを使用する。

```text
ball A:
  center = (0.0, 0.0)
  radius = 0.8
  injectivity lower bound = 1.5

ball B:
  center = (0.9, 0.0)
  radius = 0.8
  injectivity lower bound = 1.4
```

junction pointは、

```text
(0.6, 0.1)
```

であり、両ballに対して正のoverlap clearanceを持つ。

extension chainは、

```text
segment 0: [0.0, 0.7], ball A
segment 1: [0.7, 1.4], ball B
```

である。

したがって、

```text
finite window = [0.0, 1.4]
total extension length = 1.4
```

を再構成する。

## Digest binding

次をcanonical digestへ固定する。

```text
coordinate schema
normal-ball records
cover sample points
overlap records
geodesic extension segments
```

各recordは固有IDとsource digestを持つ。

重複ID、重複source digest、入力変更後のstale digestを拒否する。

## Fail-closed条件

次の場合はcertificateを生成しない。

```text
source v1.12 certificate digest欠落
source atlas digest欠落
input digest不一致
coordinate schema不正
normal ball空集合
normal ball radius非正
normal ball radiusがinjectivity下界以上
重複ball IDまたはdigest
sample空集合
sample assigned ball欠落
sampleがassigned ball外
重複sample IDまたはdigest
overlap ball欠落
overlap margin不足
重複overlap pair
segment空集合
segment parameter順序不正
segment length不一致
segmentがnormal ball外
segmentがball radiusに対して長すぎる
segment parameter gapまたはoverlap
junction position残差超過
junction tangent jump超過
ball切替時のoverlap witness欠落
junctionとoverlap witness不一致
finite window開始または終端不一致
segment length総和不一致
非有限component
```

## 固定境界

```text
finite retained cover != global finite cover
local extension chain != geodesic completeness
finite coordinate envelope != compactness theorem
bounded Hopf–Rinow witness != classical Hopf–Rinow theorem
normal-ball overlap != global chart equivalence
finite-window reachability != execution authorization
geometric extension != candidate selection
WORLD-conditioned geometry != WORLD mutation
```

source v1.12 certificate、source atlas certificate、persistent WORLD stateを変更しない。

候補identityを保持し、選択を行わない。

```text
source_exponential_map_certificate_not_mutated = true
source_atlas_certificate_not_mutated = true
persistent_world_state_unchanged = true
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

## Mathlib package

formal層は次を証明する。

```text
normal ball radiusからsource injectivity boundの正値性
normal ball縮小時の包含保存
明示assignmentからfinite indexed cover
local extension stepの正のparameter increment
local extension stepがnormal ball radius未満
二段extension chainのtelescoping length identity
二段extension chainがより後のparameterへ到達
二段extension chain total lengthの正値性
bounded finite-window witnessのwindow長正値性
cover・extension・coordinate boundのconjunction
finite cover・extension・Hopf–Rinow witnessの非権限性
local・finite・read-only・future-only境界
```

## 検証

```bash
PYTHONPATH=. python3 scripts/check_planos_finite_normal_ball_cover_hopf_rinow_witness_certificate_kernel_v0_1.py
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile planos
lake env lean formal/KuuOSPlanOSV1_13.lean
```
