# DecisionOS WORLD-Conditioned Selection Justification v0.7

## 位置づけ

本層は、DecisionOS v0.6が生成したWORLD条件付き関係的熟議receiptを受け取り、候補を一つ選択する。

ただし、PlanOS確率順位、WORLD条件付き作用、関係的frontierを、そのまま自動選択へ変換しない。

選択はDecisionOSの明示的責任として行う。

選択後も、異論、少数側、非選択候補、非許容候補、required review fieldを消去しない。

```text
PlanOS candidate distribution
→ DecisionOS evidence intake
→ relational deliberation
→ selection justification
```

## Source binding

入力はDecisionOS v0.6の次の状態に限定する。

```text
decisionos_version = v0.6
status = DECISIONOS_WORLD_CONDITIONED_RELATIONAL_DELIBERATION_READY
```

source receipt全体のdigestを再計算する。

次を再確認する。

```text
all candidates considered
candidate identity preserved
retained alternatives preserved
Wa evidence preserved
stakeholder context preserved
relational context preserved
dissent visibility preserved
minority visibility preserved
relational partial order used
single scalar utility selection forbidden
```

v0.6で候補が選択済み、decision receipt発行済み、plan synthesis済み、execution permission付与済みである場合は拒否する。

## 選択可能候補

選択候補は次の両方を満たさなければならない。

```text
candidate ∈ admissible_candidate_ids
candidate ∈ relational_frontier_candidate_ids
```

relational frontier外の候補を、確率質量、作用値、外部順序だけを理由に選択できない。

v0.6のfrontier候補は、Wa、stakeholder、relational supportのgateを通過し、dissent、minority、uncertainty、evidence blockerによって選択前保留されていない候補である。

## Candidate justification item

全候補に一つのjustification itemを要求する。

```text
candidate_id
source_deliberation_record_digest
selected
support_rationale_digests
opposition_rationale_digests
dissent_preservation_digests
minority_preservation_digests
review_resolution_digests
nonselection_reason_digest
candidate_selection_justification_digest
```

選択候補にはsupport rationaleが必要である。

選択候補にはnonselection reasonを記録できない。

非選択候補にはnonselection reasonが必要である。

候補を単に結果集合から落とすことはできない。

## 選択の一意性

`selected = true`を持つitemは一つだけでなければならない。

そのcandidate IDは、明示された`requested_selected_candidate_id`と一致しなければならない。

```text
selected_flags = [requested_selected_candidate_id]
```

暗黙選択、同時複数選択、silent substitutionは拒否する。

## Selection bundle

次を一つのselection bundle digestへ束縛する。

```text
source_deliberation_receipt_digest
selection_policy_digest
selector_responsibility_digest
requested_selected_candidate_id
hold_guard_resolution_digest
candidate_selection_justification_items
```

`selector_responsibility_digest`は、選択責任がDecisionOSのどの責任境界に属するかを固定する。

これはActOS実行権限を表さない。

## PlanOS順位とWORLD作用

PlanOS確率質量とWORLD条件付き作用は助言情報として保持する。

```text
source_probability_used_as_advisory_only = true
source_action_used_as_advisory_only = true
```

次の短絡を禁止する。

```text
argmax probability → selected candidate
argmin action → selected candidate
single scalar score → selected candidate
```

関係的部分順序と候補別理由を経なければならない。

## Dissent preservation

v0.6でdissent review対象となった候補には、`dissent_preservation_digests`を要求する。

非選択を理由に異論を消去できない。

```text
dissent_review_candidate
→ dissent_preservation_digests nonempty
```

選択receiptはdissent preservation mapを保持する。

## Minority preservation

v0.6でminority protection対象となった候補には、`minority_preservation_digests`を要求する。

多数支持または高確率を理由に少数側影響を削除できない。

```text
minority_protection_candidate
→ minority_preservation_digests nonempty
```

選択receiptはminority preservation mapを保持する。

## Hold guard

sourceで`hold_guard_active = true`の場合、`hold_guard_resolution_digest`を必須とする。

holdを選択しない場合も、hold候補を検討した事実と理由を明示する。

hold guardが無効である場合、不要なhold resolution digestは拒否する。

## 非選択候補

許容候補のうち選択されなかった候補は、retained alternativeとして保持する。

```text
retained_alternative_candidate_ids
= admissible_candidate_ids - {selected_candidate_id}
```

非許容候補も削除しない。

```text
retained_nonadmissible_candidate_ids
```

全非選択候補に対し、nonselection reason mapを生成する。

## Required review field

v0.6のrequired review fieldをsourceのまま保持する。

```text
required_review_candidate_ids
review_resolution_map
```

選択後も、代替候補に関する未解決または解決済みreview情報を消去しない。

required reviewは、選択済み候補だけの情報へ縮約されない。

## Authority boundary

選択責任はDecisionOSが行使する。

```text
selection_authority_exercised_by_decision_os = true
```

ただし、その権限をPlanOS、WORLDモデル、Qiから継承したとは扱わない。

```text
selection_authority_inherited_from_planos = false
selection_authority_inherited_from_world_model = false
selection_authority_inherited_from_qi = false
```

PlanOSは候補分布を構成する。

WORLDモデルは世界可能性を射影する。

Qiは履歴条件付き幾何を形成する。

これらはDecisionOSの選択責任そのものではない。

## Decision receipt

v0.7では実際に候補を一つ選択する。

```text
decision_selection_performed = true
selected_candidate_present = true
decision_receipt_issued = true
```

これはv0.5およびv0.6との主要な違いである。

v0.5はintakeであり、v0.6はdeliberationであった。

v0.7はselection justificationを発行する。

## 選択と計画合成の分離

候補選択は、実行可能な具体的planの合成ではない。

```text
selection_is_not_plan_synthesis = true
plan_synthesis_performed = false
```

選択候補を、ActOSが実行できるcommandへ変換しない。

次層でDecisionOSからPlanOSまたはActOS境界へ渡す際に、別のplan synthesisまたはexecution feasibility receiptが必要となる。

## 選択と実行の分離

```text
selection_is_not_execution = true
future_only = true
active_now = false
execution_permission = false
```

選択receiptは現在世界を変更しない。

## WORLD boundary

```text
persistent_world_state_unchanged = true
world_model_prediction_not_truth = true
world_mutation_not_granted = true
```

選択候補のcounterfactual WORLD projectionを事実へ昇格しない。

選択によってpersistent WORLD stateを変更しない。

## History and Qi boundary

```text
history_read_only = true
qi_grants_no_authority = true
```

履歴とQiは選択理由の条件となり得るが、選択権限の所有者ではない。

## Fail-closed条件

次の場合はselection receiptを生成しない。

```text
source v0.6 receipt欠落
source receipt digest不一致
sourceがdeliberation readyでない
sourceですでに選択済み
WORLD state、revision、lineage欠落
候補場、許容候補、非許容候補の不一致
空のrelational frontier
frontier外候補の選択
非許容候補の選択
候補justification fieldの欠落または重複
source deliberation record digest不一致
選択候補のsupport rationale欠落
非選択候補のnonselection reason欠落
dissent preservation欠落
minority preservation欠落
selected flagのゼロ件または複数件
hold guard resolution欠落
selection bundle digest不一致
```

## 出力

```text
DecisionOSWorldConditionedSelectionJustificationReceipt:
  source_deliberation_receipt_digest
  source_intake_receipt_digest
  source_planos_handoff_certificate_digest
  source_world_binding_digest
  source_world_model_state_digest
  source_world_model_revision
  source_world_lineage_digest
  selection_policy_digest
  selector_responsibility_digest
  selection_bundle_digest
  selected_candidate_id
  selected_candidate_source_record_digest
  selected_candidate_support_rationale_digests
  selected_candidate_opposition_rationale_digests
  relational_frontier_candidate_ids
  required_review_candidate_ids
  retained_alternative_candidate_ids
  retained_nonadmissible_candidate_ids
  nonselection_reason_map
  dissent_preservation_map
  minority_preservation_map
  review_resolution_map
```

## Lean形式化

```text
selection_comes_from_relational_frontier
selection_preserves_all_candidates_and_alternatives
selection_preserves_dissent_minority_and_required_review
selection_is_not_probability_or_scalar_shortcut
decision_os_exercises_selection_without_inherited_authority
selection_issues_decision_receipt_without_silent_substitution
selection_preserves_world_history_and_qi_boundaries
decision_selection_is_not_plan_synthesis_or_execution
```

## 接続

```text
WORLD possibility
→ PlanOS path geometry
→ candidate distribution
→ DecisionOS evidence intake
→ relational deliberation
→ justified candidate selection
```

次層は、選択候補を実行命令へ短絡させず、具体的なbounded planへ変換するDecisionOS to PlanOS synthesis handoffである。
