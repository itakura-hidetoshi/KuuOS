# PlanOS WORLD-Conditioned Distribution Decision Handoff Certificate Kernel v0.1

## 位置づけ

本層は、PlanOS v1.01が生成したWORLD条件付き候補分布を、DecisionOSへ渡す直前の証明可能なhandoffへ変換する。

v1.01は次を実装した。

```text
WORLD-conditioned candidate action
+ prior candidate distribution
→ next candidate distribution
```

v1.02は、その分布を変更せず、選択前の評価量と責務境界を証明書へ固定する。

```text
next candidate distribution
→ ranking evidence
→ ambiguity and concentration evidence
→ DecisionOS handoff certificate
```

本層は候補を選択しない。

順位一位は選択結果ではない。

## 入力

```text
source_distribution_update_digest
source_next_distribution_digest
source_world_conditioned_action_bundle_digest
source_world_binding_digest
source_world_model_state_digest
source_world_model_revision
source_world_lineage_digest
candidate_world_projection_digests
combined_transition_action_map
next_distribution
admissible_candidate_ids
minimum_lead_margin
maximum_normalized_entropy
hold_review_threshold
```

v1.01のdistribution digestとWORLD系列のbindingを保持し、handoffがどの分布とWORLD状態から構成されたかを追跡可能にする。

## 分布保存

本層は分布更新を行わない。

```text
source distribution
= handoff distribution
```

`source_next_distribution_digest` は入力分布から再計算する。

一致しない場合は証明書を生成しない。

許容候補は正の質量を持ち、不許容候補はゼロ質量を保たなければならない。

## 順位証拠

許容候補を次の順序で並べる。

```text
1. probability mass descending
2. combined transition action ascending
3. candidate id ascending
```

第二条件と第三条件は、同じ確率質量を持つ候補を決定論的に表示するための順序規則である。

この順序規則は選択規則ではない。

```text
ranking_is_advisory_only = true
decision_selection_performed = false
selected_candidate_id = ""
```

同率首位候補は `top_mass_candidate_ids` として集合で保持する。

## 先頭差

最大質量を `p_1`、二番目の質量を `p_2` とする。

```text
lead_margin = p_1 - p_2
```

候補が一つだけの場合は `p_2 = 0` とする。

```text
lead_margin_sufficient
= lead_margin >= minimum_lead_margin
```

先頭差が小さいことは、分布が候補間を十分に区別していないことを示す。

それ自体は再観測命令または選択禁止命令ではない。

DecisionOSが判断時に参照する証拠である。

## エントロピー

許容候補の確率を `p(c)` とする。

```text
H(p) = -sum_c p(c) log p(c)
```

候補数を `n` とすると、正規化エントロピーは次となる。

```text
H_normalized(p)
= H(p) / log(n)
```

候補が一つだけの場合はゼロとする。

```text
entropy_within_review_limit
= H_normalized(p) <= maximum_normalized_entropy
```

正規化エントロピーが高い場合、分布は多数候補へ拡散している。

## 集中度と有効支持数

```text
concentration
= sum_c p(c)^2
```

```text
effective_support
= 1 / concentration
```

```text
effective_support_ratio
= effective_support / n
```

有効支持数は、分布が実質的に何候補へ広がっているかを示す。

これは候補数そのものとは異なる。

## Hold review guard

```text
hold_review_guard_active
= hold is admissible
  and P(hold) >= hold_review_threshold
```

hold guardは、hold質量が無視できないことをDecisionOSへ伝える。

holdを自動選択しない。

holdが確率首位であっても、PlanOSは選択を実行しない。

## Handoff disposition

証明書は次のreview状態のいずれかを持つ。

```text
single_supported_candidate_review
top_mass_tie_review
insufficient_lead_margin_review
diffuse_distribution_review
hold_guarded_review
separated_distribution_review
```

優先順位は次である。

```text
single support
→ top tie
→ insufficient margin
→ diffuse entropy
→ hold guard
→ separated distribution
```

このdispositionはDecisionOSへの判断材料であり、DecisionOSの判断結果ではない。

## Decision review readiness

```text
decision_review_ready
= not top_mass_is_tied
  and lead_margin_sufficient
  and entropy_within_review_limit
```

`decision_review_ready = true` は、DecisionOSが証拠をレビュー可能であることだけを示す。

選択許可、決定権限、実行許可を意味しない。

## DecisionOS境界

```text
ranking_is_advisory_only = true
decision_selection_performed = false
selected_candidate_id = ""
decision_authority_granted = false
```

PlanOSは順位、確率差、エントロピー、集中度を計算する。

DecisionOSは、それらを他の規範、責任、現在状況と統合して選択を判断する。

## WORLD境界

```text
persistent_world_state_unchanged = true
world_model_prediction_not_truth = true
world_mutation_not_granted = true
```

高い候補確率は、対応するWORLD projectionが事実または真理であることを意味しない。

handoff証明書はpersistent WORLD stateを変更しない。

## Authorityと実行境界

```text
history_read_only = true
qi_grants_no_authority = true
future_only = true
active_now = false
execution_permission = false
```

履歴、Qi、WORLD予測、確率順位のいずれも権限を発生させない。

## Fail-closed条件

次の場合はhandoff証明書を生成しない。

```text
source v1.01 update digestの欠落
source distribution digestの欠落または不一致
WORLD action bundle、binding、state、lineage digestの欠落
負のWORLD revision
候補projection digestの欠落または重複
候補IDが有限PlanOS candidate field外
action mapとdistributionの候補集合不一致
負または非有限のcombined action
負または非有限の候補質量
分布総和が1でない
空または重複したadmissible candidate field
source field外のadmissible candidate
許容候補の正の支持欠落
不許容候補への非ゼロ質量
範囲外のlead margin閾値
範囲外のnormalized entropy閾値
範囲外のhold review閾値
```

## 出力

```text
DistributionDecisionHandoffCertificate:
  source bindings
  candidate projection digests
  combined transition action map
  preserved next distribution
  admissible candidate ids
  ranking records
  ranked candidate ids
  top-mass candidate set
  top mass
  runner-up mass
  lead margin
  Shannon entropy
  normalized entropy
  concentration
  effective support
  effective support ratio
  hold mass
  hold review guard
  decision review readiness
  handoff disposition
  responsibility boundaries
  decision_handoff_input_digest
  decision_handoff_certificate_digest
```

## Lean形式化

```text
lead_margin_nonnegative
effective_support_positive
handoff_preserves_source_distribution
handoff_ranking_is_advisory_only
handoff_retains_candidate_field
handoff_does_not_select_or_grant_decision_authority
handoff_preserves_world_read_only_boundary
handoff_preserves_history_and_authority_boundary
handoff_is_future_only_and_not_execution
```

## 接続

```text
WORLD model
→ WORLD-conditioned Plan geometry
→ candidate action
→ candidate distribution
→ selection-precondition evidence
→ DecisionOS review
```

これにより、PlanOSは確率分布をDecisionOSへ単に渡すのではなく、曖昧性、集中性、hold保護、WORLD lineage、非選択境界を同時に証明する。
