# PlanOS中道的bounded synthesis intake kernel v0.1

## 位置づけ

このkernelはPlanOS v1.03のintake層である。

入力はVerifyOS v0.4が発行した中道的条件付き連続性certificateである。

このkernelは計画を合成しない。

このkernelはVerifyOS certificateの条件付き有効性状態を、PlanOSが受理できる明示的なintake dispositionへ変換する。

DecisionOSが保持する選択権はPlanOSへ移らない。

PlanOSは実行権、WORLD変更権、真理権限を取得しない。

## 目的

VerifyOS certificateが存在するだけでは、PlanOSが合成へ進んでよいとは限らない。

PlanOS v1.03は`conditional_validity_status`を再検証し、合成可能性と返却経路を分離する。

中心規則は次である。

```text
conditional_validity_status == valid
```

この条件を満たす場合だけ、bounded synthesis requestをintakeへ受理する。

それ以外の状態では計画合成を開始しない。

## 入力binding

intakeは次の識別子を外部の期待値と照合する。

- **VerifyOS certificate digest**：受け取るcertificateそのものの固定識別子。
- **DecisionOS handoff digest**：選択済み候補をPlanOSへ渡した上流handoffの識別子。
- **WORLD binding digest**：候補評価が参照したWORLD bindingの識別子。
- **WORLD state digest**：参照したWORLD model stateの識別子。
- **WORLD revision**：WORLD model stateの改訂番号。
- **WORLD lineage digest**：WORLD stateの継承系列を表す識別子。
- **selected candidate id**：DecisionOSが選択した候補の識別子。
- **plan intent digest**：選択候補に対応する計画意図の識別子。
- **synthesis constraint digest**：bounded synthesis制約の識別子。

いずれかが期待値と一致しない場合、intakeはfail-closedで停止する。

source certificateを改変して再digestした場合でも、期待されたVerifyOS certificate digestと一致しなければ拒否する。

## 状態経路

### valid

`valid`は`retain`遷移に対応する。

PlanOSは次のdispositionを発行する。

```text
bounded_synthesis_intake_ready
```

このdispositionはbounded synthesis requestの受理を意味する。

これは計画合成の完了、計画receiptの発行、実行許可を意味しない。

### suspended

`suspended`は`suspend`遷移に対応する。

PlanOSは次のdispositionを発行する。

```text
await_condition_change
```

この状態では合成要求を受理しない。

条件の再観察または明示的な条件変化を待つ。

### revision_required

`revision_required`は`request_revision`遷移に対応する。

PlanOSは次のdispositionを発行する。

```text
return_to_decisionos_revision
```

PlanOSは候補を独自に差し替えない。

DecisionOSが選択理由、候補、制約、WORLD bindingを再検討する。

### superseded

`superseded`は`supersede_with_lineage`遷移に対応する。

PlanOSは次のdispositionを発行する。

```text
successor_lineage_reverification_required
```

旧対象は削除されない。

後継対象はpredecessorとsource lineageを保持したうえでVerifyOSによる再検証を必要とする。

### completed

`completed`は`complete`遷移に対応する。

PlanOSは次のdispositionを発行する。

```text
close_without_synthesis
```

目的が完了しているため、新しい計画を合成しない。

完了は履歴消去を意味しない。

### terminated

`terminated`は`terminate`遷移に対応する。

PlanOSは次のdispositionを発行する。

```text
terminate_without_synthesis
```

停止条件または終了理由を保持したまま合成を終了する。

終了は対象が最初から存在しなかったことを意味しない。

## admission規則

状態を`q`とし、intake admissionを`A(q)`とする。

```text
A(valid) = true
A(suspended) = false
A(revision_required) = false
A(superseded) = false
A(completed) = false
A(terminated) = false
```

VerifyOSによる検証成功は、すべての状態を合成可能にする一般許可ではない。

## lineage保存

source transition specに含まれる次の情報を再検証する。

- **source conditions**。
- **current conditions**。
- **changed conditions**。
- **source lineage**。
- **resulting lineage**。
- **predecessor reference**。
- **source responsibility lineage**。
- **resulting responsibility lineage**。
- **dissent evidence**。
- **minority evidence**。

source lineageはresulting lineageの部分集合でなければならない。

predecessor referenceとsource object digestはresulting lineageに残らなければならない。

source responsibility lineageはresulting responsibility lineageの部分集合でなければならない。

PlanOS責任主体は既存責任lineageを置換せず、追加される。

```text
R_result = R_verify ∪ {R_planos_intake}
```

## 中道境界

PlanOSは`valid`を永続的真理へ変換しない。

`valid`は確認された条件のもとでのintake可否を示す。

WORLD model predictionは真理ではない。

`suspended`、`revision_required`、`superseded`、`completed`、`terminated`を削除状態として扱わない。

各状態は理由、条件、lineage、責任主体を持つ明示的な経路へ変換される。

旧候補、異論、少数側証拠は消去されない。

## 権限境界

certificateは次を固定する。

```text
selection_remains_decisionos_owned = true
selection_authority_granted_to_planos = false
plan_synthesis_performed = false
concrete_plan_issued = false
plan_receipt_issued = false
execution_authority_granted = false
execution_permission = false
persistent_world_state_unchanged = true
world_model_prediction_not_truth = true
world_mutation_not_granted = true
history_read_only = true
qi_grants_no_authority = true
future_only = true
active_now = false
```

`bounded_synthesis_request_admitted = true`であっても、PlanOSはこのkernel内で具体的計画を生成しない。

後続のbounded synthesis kernelは、このintake certificateを入力として別途計画を生成しなければならない。

## fail-closed条件

次の場合はcertificateを発行しない。

- source VerifyOS certificateが存在しない。
- source certificate digestが不正である。
- source certificate digestが期待値と一致しない。
- VerifyOS kernel、version、statusが一致しない。
- DecisionOS handoff、WORLD binding、WORLD state、revision、lineageが期待値と一致しない。
- selected candidateまたはplan intentが期待値と一致しない。
- synthesis constraintが期待値と一致しない。
- transition kindとconditional validity statusが対応しない。
- transition spec digestが一致しない。
- changed condition集合が対称差と一致しない。
- lineageが単調でない。
- predecessor referenceが消えている。
- responsibility lineageが単調でない。
- VerifyOS責任主体が消えている。
- source certificateが合成、実行、WORLD更新、履歴消去、権限拡張を昇格している。
- intake bundle digestが一致しない。

## Lean形式化

Lean moduleは`IntakeDisposition`、`dispositionForStatus`、`admittedForStatus`、intake certificateを定義する。

Lean theoremは六状態の経路、lineage保存、責任保存、異論保存、少数側証拠保存を示す。

Lean theoremはPlanOSへ選択権と実行権が付与されないことを示す。

Lean theoremはintakeが計画合成またはWORLD変更ではないことを示す。

## 検証接続

runtime checkerはVerifyOS v0.4の実certificate builderを利用して六状態の正常経路を検証する。

checkerはsource digest改変、期待binding不一致、lineage消去、責任消去、silent rewrite、合成権限昇格をfail-closedで検証する。

checkerは`run_evidence_cycle_os_full_checks.py`へ接続される。

Lean moduleは`KuuOSFormalV0_69.lean`から到達する。

canonical formal rootとintegrated current rootは変更しない。
