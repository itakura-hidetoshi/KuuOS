# PlanOS WORLD-Conditioned Objective Distribution Update Kernel v0.1

## 位置づけ

本層は、PlanOS v1.00が生成したWORLD条件付きcombined transition actionを、次周期の候補分布へ反映する。

v1.00は次を実装した。

```text
(Q, H, W)
→ G_QH + lambda_W J^T G_W J
→ combined transition action
```

v1.01は、その作用をPlanOS v0.92のKL正則化更新則へ戻す。

```text
WORLD-conditioned action bundle
+ prior candidate distribution
→ next candidate distribution
```

本層は候補を選択しない。

候補選択はDecisionOSの責務として残す。

## 入力

```text
source_world_conditioned_metric_certificate_digest
source_world_binding_digest
source_world_model_state_digest
source_world_model_revision
source_world_lineage_digest
world_conditioned_action_bundle_digest
candidate_world_projection_digests
plan_transition_action_map
world_transition_action_map
combined_transition_action_map
prior_distribution_digest
prior_distribution
admissible_candidate_ids
beta
entropy_weight
hold_floor
```

WORLD state、revision、lineageは読み取り専用のsource bindingとして保持する。

## Action bundle

候補ごとに次の作用を保持する。

```text
K_Plan(c)
K_WORLD(c)
K_QHW(c)
```

```text
K_QHW(c)
= K_Plan(c) + lambda_W K_WORLD(c)
```

v1.01はv1.00で計算されたaction mapを再計算しない。

代わりに、candidate projection digestと三つのaction mapを単一のaction bundle digestへ束縛する。

候補集合またはdigestが一致しない場合はfail-closedとする。

## 更新則

候補を `c`、事前分布を `p_t(c)`、WORLD条件付きcombined actionを `A_QHW(c)` とする。

```text
F[p]
= KL(p || p_t)
+ beta E_p[A_QHW]
- eta H(p)
```

有限候補集合での更新は次となる。

```text
p_next(c)
proportional to
p_t(c)^(1 / (1 + eta))
* exp(
    -beta * A_QHW(c) / (1 + eta)
  )
```

runtimeでは最小作用を減算した等価な指数表現を用い、数値的underflowを抑制する。

## 許容候補

`admissible_candidate_ids` に含まれる候補だけを正規化対象とする。

許容候補は正のprior supportを持たなければならない。

不許容候補は候補場から削除しない。

```text
candidate_field_retained = true
nonadmissible_candidates_zero_mass = true
```

候補場保持と確率質量付与を分離する。

## hold preservation

holdが許容候補である場合、次を保持する。

```text
P_next(hold) >= hold_floor
```

hold floorを満たすための再配分は、他の許容候補の相対比を保った非負rescalingで行う。

holdが不許容である場合、hold floorは適用しない。

## DecisionOS境界

本層は分布だけを生成する。

```text
decision_selection_performed = false
selected_candidate_id = ""
```

最大質量候補または最小作用候補を、自動的に選択候補へ昇格しない。

候補分布はDecisionOSへの入力であり、DecisionOSの出力ではない。

## WORLD境界

候補分布更新はpersistent WORLD stateを変更しない。

```text
persistent_world_state_unchanged = true
world_model_prediction_not_truth = true
world_mutation_not_granted = true
```

WORLD projectionの確率質量が高いことは、そのprojectionが事実または真理であることを意味しない。

## Authorityと実行境界

```text
history_read_only = true
qi_grants_no_authority = true
future_only = true
active_now = false
execution_permission = false
```

分布更新によって権限、現在周期、実行状態を変更しない。

## Fail-closed条件

次の場合はupdateを生成しない。

```text
source v1.00 certificate digestの欠落
WORLD binding、state、lineage digestの欠落
負のWORLD revision
action bundle digestの不一致
候補projection digestの欠落または重複
候補IDが有限PlanOS candidate field外
action map間の候補集合不一致
prior distributionとsource candidate fieldの不一致
負または非有限のPlan、WORLD、combined action
combined actionがPlan action未満
空または重複したadmissible candidate field
source field外のadmissible candidate
許容候補の非正prior support
prior distribution digestの不一致
負のbetaまたはentropy weight
範囲外のhold floor
無効なpartition function
正規化不一致
hold floor不保持
```

## 出力

```text
WorldConditionedObjectiveDistributionUpdate:
  source_world_conditioned_metric_certificate_digest
  source_world_binding_digest
  source_world_model_state_digest
  source_world_model_revision
  source_world_lineage_digest
  world_conditioned_action_bundle_digest
  candidate_world_projection_digests
  plan_transition_action_map
  world_transition_action_map
  combined_transition_action_map
  normalized_prior_distribution
  admissible_candidate_ids
  beta
  entropy_weight
  effective_temperature
  minimum_combined_action
  partition_function
  hold_floor
  next_distribution
  next_distribution_digest
  world_conditioned_distribution_update_digest
```

## Lean形式化

```text
world_conditioned_gibbs_factor_positive
world_conditioned_raw_weight_nonnegative
world_conditioned_distribution_is_normalized
world_conditioned_candidate_mass_is_nonnegative
world_conditioned_admissible_support_is_preserved
world_conditioned_hold_mass_is_preserved
world_conditioned_candidate_field_is_retained
world_conditioned_update_does_not_select
world_conditioned_update_preserves_world_read_only_boundary
world_conditioned_update_preserves_history_and_authority
world_conditioned_update_is_future_only_and_not_execution
```

## 接続

```text
WORLD Model
→ counterfactual WORLD projections
→ pullback geometry
→ combined candidate action
→ WORLD-conditioned candidate distribution
→ DecisionOS selection input
```

これにより、WORLDモデルはPlanOS計量だけでなく、次周期の候補確率質量へ実際に反映される。
