# PlanOS Conjugate Event Sequence and Injectivity Radius Certificate Kernel v0.1

## 位置づけ

PlanOS v1.10は、endpoint-fixedな有限変分基底上で第二変分とindex formを再構成し、有限基底Morse indexとnullityを保持した。

PlanOS v1.11は、その有限windowを区分測地線segmentへ分解し、共役点候補のイベント列とMorse index jumpを照合する。

さらに、共役点候補またはcut-locus候補が現れる前のevent-free範囲を、局所injectivity-radius下界として保持する。

この層は局所的な有限証拠を扱う。

大域的Morse index theorem、真のcut locus、完全なinjectivity radius、候補棄却、実行判断は主張しない。

## 区分測地線

有限windowを、

```text
[s_0,s_1], [s_1,s_2], ..., [s_{m-1},s_m]
```

へ分割する。

各segmentは次を保持する。

```text
segment_id
start_parameter
end_parameter
length
start_point
end_point
start_tangent
end_tangent
source_segment_digest
```

runtimeは、

```text
length = end_parameter - start_parameter
```

を再計算する。

隣接segmentについて、

```text
end_parameter_left = start_parameter_right
end_point_left = start_point_right
```

を検証する。

接ベクトルは完全一致を必須とせず、明示されたjunction tangent jump上限以内であることを要求する。

## 共役点イベント列

各共役点候補は、

```text
event_id
parameter
multiplicity
morse_index_before
morse_index_after
nullity_at_event
source_event_digest
```

を保持する。

イベントparameterは有限window内で狭義単調増加しなければならない。

Morse index jumpは、

```text
morse_index_after
= morse_index_before + multiplicity
```

を満たす。

イベント列は前後のindexを連鎖させる。

```text
next.morse_index_before
= previous.morse_index_after
```

局所多重度候補とnullityは、

```text
nullity_at_event = multiplicity
```

として照合する。

最後のindexはv1.10由来の期待値と一致しなければならない。

## 有限windowの加法関係

初期indexを `index_0`、イベント多重度を `m_k` とすると、

```text
index_final = index_0 + sum_k m_k
```

である。

これは有限window上のイベント列整合性であり、大域Morse index theoremの完全証明ではない。

## Cut-locus候補

cut-locus候補は二種類に限定する。

```text
conjugate
multiple_geodesic
```

`conjugate`原因の場合は、同じparameterの共役イベントIDへ結合する。

```text
cut.parameter = event.parameter
```

`multiple_geodesic`原因の場合は、

```text
competing_geodesic_count >= 2
```

を要求する。

cut-locus候補は局所的な候補証拠であり、真の大域cut locusとは同一視しない。

## 局所injectivity-radius下界

window開始parameterを `s_0`、保持する半径下界を `r` とする。

```text
r > 0
```

かつ、

```text
s_0 + r
<= earliest_conjugate_event_parameter
```

```text
s_0 + r
<= earliest_cut_locus_candidate_parameter
```

を要求する。

したがって、保持された有限候補集合に関して、`s_0+r`までobstruction-freeである。

certificateはこれを、

```text
local_injectivity_radius_lower_bound
```

として保持する。

これは局所・有限window・有限候補に限定された下界であり、大域injectivity radiusの完全値ではない。

## 基準fixture

基準windowは、

```text
[0.0, 3.0]
```

である。

二つのsegmentを使用する。

```text
segment-0: [0.0, 1.5]
segment-1: [1.5, 3.0]
```

共役イベントは、

```text
parameter = 2.0
multiplicity = 1
morse_index_before = 0
morse_index_after = 1
nullity_at_event = 1
```

である。

cut候補は、

```text
2.0: conjugate
2.5: multiple_geodesic
```

である。

局所injectivity-radius下界は、

```text
1.5
```

とする。

最初のobstruction候補は `2.0`であるため、この下界より手前に保持されたobstructionは存在しない。

## Digest binding

次をcanonical digestへ固定する。

```text
coordinate schema
piecewise geodesic segments
conjugate event sequence
cut-locus candidates
```

各segment、event、cut候補は固有IDとsource digestを持つ。

重複IDまたは重複source digestは拒否する。

## Fail-closed条件

次の場合はcertificateを生成しない。

```text
source Morse-index certificate digest欠落
input digest不一致
coordinate schema不正
空または重複したsegment
segment parameter順序不正
segment length不一致
segment gapまたはoverlap
junction position残差超過
junction tangent jump超過
空でないwindowを覆わないsegment列
重複した共役イベント
イベントparameter非単調
イベントがwindow外
非正のmultiplicity
Morse index chain不一致
index jumpとmultiplicity不一致
nullityとmultiplicity不一致
最終index不一致
cut cause不正
conjugate cutとイベントの不一致
multiple-geodesic count不足
cut候補がwindow外
injectivity下界以前のobstruction
非有限component
```

## 固定境界

```text
conjugate event != automatic plan rejection
Morse index jump != candidate ranking
cut-locus candidate != proven global cut locus
injectivity-radius lower bound != guaranteed execution region
piecewise geodesic != selected plan
multiple geodesics != ambiguity verdict
local obstruction != ethical verdict
geometric certificate != activation authorization
WORLD-conditioned geometry != WORLD mutation
```

本層はsource v1.10 certificateとpersistent WORLD stateを変更しない。

```text
source_morse_index_certificate_not_mutated = true
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
PYTHONPATH=. python3 scripts/check_planos_conjugate_event_sequence_injectivity_radius_certificate_kernel_v0_1.py
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile planos
lake env lean formal/KuuOSPlanOSV1_11.lean
```
