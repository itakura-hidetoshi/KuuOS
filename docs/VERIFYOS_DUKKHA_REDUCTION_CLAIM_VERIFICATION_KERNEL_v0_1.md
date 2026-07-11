# VerifyOS苦低減claim検証kernel v0.1

## 位置づけ

このkernelはVerifyOS v0.6の検証層である。

入力はVerifyOS v0.5が構造とWORLD条件を検証した有限plan certificateと、PlanOSおよびWORLDモデルが提示する苦低減assessmentである。

このkernelは苦を最小化しない。

このkernelは、計画が苦の持続的閉ループを弱めるというclaimを検証する。

候補選択、計画改訂、materialization、実行は行わない。

## 苦のベクトル

苦を単一効用へ縮約しない。

次の六次元を保持する。

```text
misfit
update_lag
attachment_rigidity
relational_curvature
structural_constraint
uncertainty_burden
```

各次元はbefore interval、after interval、delta intervalを持つ。

intervalは点推定より強い確実性を表すものではない。

予測不確実性を残したまま、確実な悪化、確実な非悪化、不確定を区別する。

## 情報幾何学的意味

`misfit`は現実分布と予測モデルの乖離を表す。

`update_lag`は必要なモデル移動と実際のモデル移動の差を表す。

`attachment_rigidity`は自己方向の過剰精度と再記述不能性を表す。

`relational_curvature`は関係的曲率、ねじれ、ホロノミーを表す。

`structural_constraint`は身体、制度、モデル族の有限性に由来する構造的な苦を表す。

`uncertainty_burden`は不確実性と、その負担配置を表す。

構造的な苦を執着由来の苦として偽装しない。

執着由来の苦を不可避な構造として固定しない。

## Delta interval

各次元について次を要求する。

```text
Delta.lower = after.lower - before.upper
Delta.upper = after.upper - before.lower
```

これにより、都合のよいdeltaだけを別に提出できない。

回避可能な次元は次である。

```text
misfit
update_lag
attachment_rigidity
relational_curvature
uncertainty_burden
```

`structural_constraint`は別に保持する。

## 苦の閉ループ

苦の絶対量だけでなく、持続的なfeedback gainを検証する。

```text
loop_gain_before_interval
loop_gain_after_interval
```

支持判定には、after intervalがbefore intervalより確実に低く、after upper boundが収縮境界を下回ることを要求する。

一時的に誤差を隠す計画と、苦を再生産する閉ループを弱める計画を区別する。

## 修正可能性

次を比較する。

```text
revision_capacity_before_interval
revision_capacity_after_interval
```

支持判定には、計画後の再記述可能性が確実に保持または増加することを要求する。

苦の低下を理由に、モデル族を狭めたり、自己モデルを固定したりしない。

## 偽の苦低減を拒否する条件

次を明示的に検証する。

```text
observation_integrity_preserved
adverse_evidence_retained
precision_collapse_not_used
model_family_narrowing_not_used
uncertainty_disclosed
structural_suffering_acknowledged
agency_preserved
dissent_preserved
minority_preserved
future_burden_assessed
causal_model_not_truth
single_scalar_utility_forbidden
```

不都合な観測を削除して距離を小さく見せることを認めない。

精度を全面的に低下させて誤差を小さく見せることを認めない。

反証可能なモデル族を排除して内部的一貫性だけを高めることを認めない。

因果モデルの予測を真理として扱わない。

## 非転嫁

protected groupとfuture subjectごとに六次元のdelta intervalを保持する。

支持判定には、すべてのupper boundが0以下であることを要求する。

したがって、全体平均を改善しながら少数側または未来へ苦を移転する計画は支持されない。

確実な悪化がある場合は反証となる。

悪化可能性を排除できない場合は不確定となる。

## 三値判定

### Supported

次を満たす場合である。

- 観測、異論、主体性、不確実性を保持する。
- 回避可能な全次元が確実に非悪化である。
- 少なくとも一つの回避可能な次元が確実に改善する。
- feedback gainが確実に低下して収縮境界を下回る。
- revision capacityが確実に保持または増加する。
- protected groupとfuture subjectへ苦を転嫁しない。

```text
dukkha_reduction_supported_for_materialization_intake
```

この場合だけmaterialization intake候補となる。

### Indeterminate

確実な悪化は示されないが、区間が重なり、苦低減を支持できない場合である。

```text
additional_evidence_required
```

追加観測またはholdへ進む。

### Contradicted

確実な悪化、feedback増幅、revision capacityの確実な低下、観測完全性の破壊、苦の転嫁がある場合である。

```text
return_to_planos_revision
```

PlanOS改訂へ返す。

## 構造破損

schema、digest、source binding、interval arithmetic、evidence lineageが不正な場合はcertificateを発行しない。

これはclaimの反証ではなく、検証可能な入力が成立していない状態である。

## VerifyOSの責務境界

VerifyOSは苦を最小化するOSではない。

VerifyOSは苦低減claimの妥当性と非転嫁性を検証する。

```text
selection_remains_decisionos_owned = true
selection_authority_granted_to_verifyos = false
plan_revision_authority_granted_to_verifyos = false
dukkha_minimization_authority_granted_to_verifyos = false
plan_activated = false
materialization_performed = false
execution_authority_granted = false
execution_permission = false
active_now = false
```

## 接続

```text
DecisionOS justified selection
→ PlanOS bounded synthesis
→ VerifyOS bounded plan verification
→ VerifyOS dukkha reduction claim verification
```

次段は、支持されたplanだけをActOSのmaterialization intakeへ渡す層である。
