# KuuOS v14.0 — Causal WorldModel OS

## 1. 世代転換

v14.0 は、v13 系の個別 runtime / bridge / receipt を追加する系列ではない。

新しい中心は、単一の因果 WORLD モデルを次の操作で直接扱う OS カーネルである。

```text
initialize
observe
intervene (do)
undo
counterfactual
inspect
```

WORLD モデルの内部状態は、ライセンスされたトランザクションによって実際に更新される。
これは候補生成だけでも dry-run だけでもない。

一方で、内部 WORLD モデルの変更と、外部世界への行為・事実認定・最終意思決定は分離される。

```text
internal WORLD-model mutation != external-world actuation
world-model state != truth authority
counterfactual projection != fact
causal estimate != execution permission
```

## 2. OS 構造

```text
┌─────────────────────────────────────────────────────────┐
│ KuuOS v14.0 Causal WorldModel OS                        │
├─────────────────────────────────────────────────────────┤
│ Command Surface                                         │
│ initialize / observe / intervene / undo / counterfactual│
├─────────────────────────────────────────────────────────┤
│ Transaction Kernel                                      │
│ license binding / replay protection / snapshot / audit  │
├─────────────────────────────────────────────────────────┤
│ Causal Model Core                                       │
│ typed variables / affine mechanisms / DAG / propagation │
├─────────────────────────────────────────────────────────┤
│ Non-Markov Memory Link                                  │
│ process tensor / memory kernel / history window         │
├─────────────────────────────────────────────────────────┤
│ Persistent WORLD State                                  │
│ revision / uncertainty / interventions / lineage digest │
└─────────────────────────────────────────────────────────┘
```

## 3. 因果モデル

v14.0 の最初の実装は、任意コードを構造方程式として実行しない。
構造機構は宣言的な `affine` 型に限定する。

```text
Y = bias + Σ(weight(parent) × parent) + noise
```

各変数は少なくとも次を持つ。

```json
{
  "value": 3.0,
  "uncertainty": 0.2,
  "status": "observed | derived | intervened | counterfactual_intervened",
  "unit": "...",
  "provenance": ["transaction-id"]
}
```

因果グラフは DAG でなければならない。循環、欠落親、未定義重み、負の noise は fail-closed で拒否する。

## 4. 観測と do 介入

### observe

観測値を WORLD モデルへ直接反映し、子孫変数を構造機構に従って再計算する。

### intervene

`do(X=x)` として介入値を固定し、介入対象を構造機構から切り離した上で子孫を再計算する。
介入は `active_interventions` に保持される。

両操作とも、更新直前の WORLD 状態をスナップショットとして保存する。

## 5. undo

`undo` は単なる取消候補ではない。
指定トランザクション直前のスナップショットを読み、WORLD モデル状態を実際に復元する。

復元後も revision は前進し、次の lineage を記録する。

```text
previous_world_model_digest
restored_from_transaction_id
last_command_digest
process_tensor_context_digest
history_digest
```

したがって、復元によって履歴が消去されることはない。

## 6. counterfactual

反実仮想は現在の WORLD 状態を複製した twin projection 上で `do` 介入を行う。

```text
persistent state: unchanged
projection: changed
result: variable deltas + projection digest
```

反実仮想結果は、将来の PlanOS / DecisionOS / ScientificMethodOS が利用できるが、それ自体は事実でも実行許可でもない。

## 7. 非マルコフ記憶

各コマンドは次の process-tensor context を必須とする。

```text
process_tensor_digest
memory_kernel_digest
history_window_digest
instrument_trace_digest
non_markov_context_digest
```

WORLD モデル更新は現在値だけではなく、履歴窓・記憶核・計測履歴に結び付けられる。

## 8. トランザクション境界

各コマンドは `command_digest` を持ち、ライセンスの `bound_command_digest` と一致しなければならない。

ライセンスは次を明示する。

```text
allowed_command_kinds
allowed_variables
protected_variables
direct_world_model_mutation_allowed
observation_update_allowed
intervention_allowed
undo_allowed
counterfactual_allowed
```

同一 `transaction_id` の再利用は拒否される。

## 9. 永続面

```text
kuuos_causal_world_model_state_v14_0.json
kuuos_causal_world_model_event_ledger_v14_0.jsonl
kuuos_causal_world_model_audit_v14_0.jsonl
kuuos_causal_world_model_snapshots_v14_0/
kuuos_causal_world_model_results_v14_0/
```

この構造により、状態、イベント、監査、復元点、反実仮想結果を一つの OS 内で追跡できる。

## 10. v14 系の次段

v14.0 を基盤として、以後は receipt の横展開ではなく、次の OS 機能を積み上げる。

```text
v14.1 ScientificMethodOS
  仮説 → 介入候補 → 観測設計 → 更新

v14.2 ActiveLearningOS
  不確実性を最も減らす観測・介入を選ぶ

v14.3 MultiAgentCausalOS
  複数エージェントの因果グラフと証拠を共有・比較する

v14.4 MultimodalCausalOS
  テキスト・画像・時系列・臨床情報を因果変数へ接続する

v14.5 DecisionOS Causal Action Boundary
  因果推定と外部行為の許可境界を接続する
```

v14 系の評価軸は「receipt が増えたか」ではなく、次である。

```text
WORLDモデルが実際に更新できるか
介入の結果が因果伝播するか
反実仮想が現在状態を壊さず計算できるか
undo が状態を本当に復元できるか
不確実性と履歴が失われないか
```
