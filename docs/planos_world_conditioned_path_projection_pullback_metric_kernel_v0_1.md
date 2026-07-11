# PlanOS WORLD-Conditioned Path Projection Pullback Metric Kernel v0.1

## 位置づけ

本層は、PlanOS v0.99で構成したQiおよび非マルコフ履歴条件付き計量を、KuuOSのWORLDモデルへ接続する。

v0.99は次の写像を実装した。

```text
(Q, H, evidence)
→ G_QH
→ Plan transition action
```

本層は、局所WORLD patch、IndraNet、holonomy、transport residue、v14.0因果WORLD状態、反実仮想projectionを束縛し、次を追加する。

```text
Plan candidate
→ counterfactual WORLD projection
→ WORLD delta
→ pullback metric J^T G_W J
→ combined Plan-WORLD transition action
```

PlanOSはpersistent WORLD stateを変更しない。

PlanOSはWORLD予測を事実または真理へ昇格しない。

PlanOSはWORLD projectionから権限または実行許可を取得しない。

## WORLDモデルの二層

本層は次の二層を区別したまま束縛する。

```text
Indra-Qi Mandala WORLD substrate
  local WORLD patch
  gauge connection
  Qi relational flow
  holonomy
  transport residue
  process-tensor memory

KuuOS v14.0 Causal WorldModel projection
  causal graph
  typed causal variables
  uncertainty state
  active interventions
  counterfactual twin projection
```

因果DAGはMandala全体ではない。

因果変数は、局所WORLD patchと観測作用素から射影された慣習的表現である。

## WORLD binding

WORLD入力は次を一つのbinding digestへ固定する。

```text
world_model_kind
world_model_state_digest
world_model_revision
world_lineage_digest
world_patch_id
world_patch_projection_digest
observation_operator_digest
causal_graph_digest
causal_variable_schema_digest
causal_state_digest
uncertainty_state_digest
active_interventions_digest
process_tensor_context_digest
history_window_digest
holonomy_context_digest
transport_residue_digest
```

`world_binding_digest` が再計算値と一致しない場合はfail-closedとする。

holonomyとtransport residueは省略または消去できない。

## Plan計量とWORLD計量

v0.99のconditioned Plan metricを対角計量として受け取る。

```text
G_QH = diag(g_i)
```

各Plan座標重みは有限かつ正でなければならない。

WORLD側は有限座標集合上の対角計量を持つ。

```text
G_W = diag(w_a)
```

各WORLD重みは有限かつ非負である。

全重みがゼロのWORLD計量は拒否する。

Plan座標schema、conditioned metric、WORLD座標schema、WORLD metricはdigestで固定する。

## 候補counterfactual projection

各候補は次を保持する。

```text
candidate_id
parameter_delta
world_jacobian
projected_world_delta
persistent_world_state_digest_before
persistent_world_state_digest_after
projection_not_fact
world_prediction_not_truth
world_mutation_requested
candidate_world_projection_digest
```

候補projectionはread-only twin projectionである。

```text
persistent_world_state_digest_before
= world_model_state_digest

persistent_world_state_digest_after
= world_model_state_digest

projection_not_fact = true
world_prediction_not_truth = true
world_mutation_requested = false
```

## WORLD projection

Plan座標差分を `delta theta_i`、候補ごとの局所Jacobianを `J_ai` とする。

WORLD差分は次でなければならない。

```text
delta x_a = sum_i J_ai * delta theta_i
```

runtimeは、宣言されたWORLD差分とJacobianから再計算した差分の一致を検証する。

不一致はprojection lineageの破損として拒否する。

## Pullback metric

WORLD計量をPlan空間へ引き戻す。

```text
G_pullback = J^T G_W J
```

```text
(G_pullback)_ij
= sum_a w_a * J_ai * J_aj
```

WORLD transition actionは次となる。

```text
K_WORLD
= 1/2 * delta theta^T G_pullback delta theta
= 1/2 * sum_a w_a * (delta x_a)^2
```

WORLD重みが非負であるため、`K_WORLD` は非負である。

## Combined metric

v0.99のQi条件付き計量とWORLD pullbackを次で結合する。

```text
G_QHW
= G_QH + lambda_W * G_pullback
```

```text
lambda_W >= 0
```

候補ごとのcombined transition actionは次となる。

```text
K_combined
= K_Plan + lambda_W * K_WORLD
```

runtimeは、作用の和とcombined matrixによる二次形式が一致することを検証する。

## 候補保持

本層は全候補を独立にprojectionする。

候補選択は行わない。

```text
candidate_field_retained = true
decision_selection_performed = false
```

DecisionOSだけが候補選択を担う。

WORLD作用が最小であることは、自動選択、事実認定、実行許可を意味しない。

## fail-closed条件

次の場合は証明書を生成しない。

```text
source v0.99 certificate digestの欠落
WORLD binding digestの不一致
未知のWORLD model kind
負のWORLD revision
WORLD stateまたはlineage digestの欠落
WORLD patchまたはobservation projectionの欠落
causal graph、state、uncertainty、intervention digestの欠落
process tensorまたはhistory window digestの欠落
holonomyまたはtransport residue digestの欠落
Plan座標schemaまたはmetric digestの不一致
WORLD座標schemaまたはmetric digestの不一致
負または非有限のmetric weight
全ゼロWORLD計量
負のpullback weight
空の候補場
重複candidate ID
重複projection digest
候補projection digestの不一致
Plan座標またはWORLD座標の不一致
Jacobian次元の不一致
非有限deltaまたはJacobian
Jacobian projectionとWORLD deltaの不一致
persistent WORLD stateの変更
projectionのfact扱い
WORLD predictionのtruth扱い
WORLD mutation要求
combined action identityの不一致
```

## 不変条件

```text
world_pullback_metric_nonnegative = true
combined_qi_world_metric_nonnegative = true
plan_coordinate_dimension_preserved = true
source_world_state_digest_preserved = true
persistent_world_state_unchanged = true
counterfactual_projection_not_fact = true
world_model_prediction_not_truth = true
world_mutation_not_granted = true
holonomy_context_preserved = true
transport_residue_visible = true
candidate_field_retained = true
decision_selection_performed = false
history_read_only = true
qi_grants_no_authority = true
future_only = true
active_now = false
execution_permission = false
```

## Lean形式化

```text
plan_metric_quadratic_form_is_nonnegative
world_pullback_metric_is_nonnegative
combined_qi_world_metric_is_nonnegative
world_projection_preserves_plan_coordinate_dimension
counterfactual_projection_preserves_persistent_world
counterfactual_projection_is_not_fact
world_prediction_grants_no_authority
holonomy_context_is_preserved
transport_residue_is_not_erased
world_conditioned_plan_update_is_future_only
```

## OS責務分離

```text
WORLD Model
  possible WORLD transitions and counterfactual projections

PlanOS
  path projection, pullback geometry, candidate action construction

DecisionOS
  candidate selection with Wa and dissent evidence

ActOS
  execution feasibility and bounded authorization

LearnOS
  post-observation differences for the next cycle
```

PlanOS commitはWORLD mutationではない。

PlanOS commitはDecisionOS selectionではない。

PlanOS commitはActOS execution permissionではない。

## 接続

```text
WORLD state and counterfactual model
+ Qi process tensor
+ non-Markov history
+ Plan candidate field
→ WORLD-conditioned pullback geometry
→ combined transition action
→ Plan path action
→ future path distribution
```

PlanOSは、WORLDモデルが表現する世界可能性を読み取り、persistent WORLDを変更せずに、その世界可能性の幾何を計画空間へ引き戻す。
