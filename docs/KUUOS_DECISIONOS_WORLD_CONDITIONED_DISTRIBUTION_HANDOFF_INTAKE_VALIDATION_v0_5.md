# DecisionOS WORLD-Conditioned Distribution Handoff Intake Validation v0.5

## 位置づけ

本層は、PlanOS v1.02が生成したWORLD条件付き候補分布のhandoff certificateをDecisionOSへ受理する。

PlanOS v1.02は、候補分布、候補順位、entropy、effective support、hold guardを計算した。

ただし、PlanOSは候補を選択しない。

DecisionOS v0.5は、PlanOSの順位を決定へ短絡させず、DecisionOS deliberationへ入る前の入力完全性を検証する。

```text
PlanOS v1.02 handoff certificate
+ Wa evidence
+ stakeholder evidence
+ relational evidence
+ dissent evidence
+ minority evidence
→ DecisionOS intake validation receipt
```

本層も候補選択を行わない。

## Source certificate validation

入力はPlanOS v1.02のhandoff certificate全体とする。

`decision_handoff_certificate_digest` は、digest自身を除くcertificate全体から再計算する。

次のsource bindingを保持する。

```text
source_distribution_update_digest
source_next_distribution_digest
source_world_conditioned_action_bundle_digest
source_world_binding_digest
source_world_model_state_digest
source_world_model_revision
source_world_lineage_digest
decision_handoff_input_digest
```

WORLD state、revision、lineageは読み取り専用である。

## Source boundary

PlanOS handoffは次を満たさなければならない。

```text
ranking_is_advisory_only = true
candidate_field_retained = true
persistent_world_state_unchanged = true
world_model_prediction_not_truth = true
world_mutation_not_granted = true
history_read_only = true
qi_grants_no_authority = true
future_only = true

decision_selection_performed = false
selected_candidate_id = ""
decision_authority_granted = false
active_now = false
execution_permission = false
```

一つでも昇格している場合、DecisionOS intakeは生成しない。

## Distribution validation

候補集合は、projection digest、combined action、確率分布の三つで一致しなければならない。

確率質量は非負であり、総和は1でなければならない。

許容候補は正の支持を持つ。

不許容候補は候補場に残るが、確率質量はゼロである。

```text
candidate retained
!=
candidate admissible
!=
candidate selected
```

## Advisory ranking validation

PlanOS順位を再計算する。

```text
1. probability mass descending
2. combined transition action ascending
3. candidate id ascending
```

`ranking_records` と `ranked_candidate_ids` は再計算値と一致しなければならない。

首位候補集合、lead margin、Shannon entropy、normalized entropy、concentration、effective support、effective-support ratioも再計算する。

handoff dispositionは次のいずれかである。

```text
single_supported_candidate_review
top_mass_tie_review
insufficient_lead_margin_review
diffuse_distribution_review
hold_guarded_review
separated_distribution_review
```

順位一位はselected candidateではない。

## Candidate evidence item

全候補について一つのevidence itemを要求する。

```text
candidate_id
candidate_world_projection_digest
probability_mass
combined_transition_action
advisory_rank
admissible
wa_evidence_digests
stakeholder_evidence_digests
relational_evidence_digests
dissent_evidence_digests
dissent_absence_attested
minority_evidence_digests
minority_absence_attested
zero_mass_reason_digest
candidate_intake_digest
```

候補identity、projection、確率質量、作用、順位、許容性をsource certificateと照合する。

## Wa evidence

許容候補はWa evidenceを少なくとも一つ持つ。

Wa evidenceは単純な総効用値ではない。

関係的損失、外部性、少数側への偏り、関係維持可能性をDecisionOS deliberationへ渡す。

## Stakeholder and relational evidence

許容候補はstakeholder evidenceとrelational evidenceを少なくとも一つ持つ。

候補確率だけでstakeholder contextを代替しない。

WORLD予測確率が高いことは、関係的に適切であることを意味しない。

## Dissent visibility

異論証拠が存在する場合、digest listを保持する。

異論証拠が存在しない場合、空listだけでは不十分である。

```text
dissent_evidence_digests = []
dissent_absence_attested = true
```

と明示する。

証拠存在と不在証明を同時に立てることは禁止する。

## Minority visibility

少数側証拠も同じ規則を用いる。

```text
minority_evidence_digests != []
minority_absence_attested = false
```

または、

```text
minority_evidence_digests = []
minority_absence_attested = true
```

のいずれかでなければならない。

少数側の沈黙を同意へ変換しない。

## Nonadmissible candidates

不許容候補もevidence fieldから削除しない。

不許容候補は次を持つ。

```text
admissible = false
probability_mass = 0
advisory_rank = 0
zero_mass_reason_digest != ""
```

これにより、候補除外の理由を追跡可能にする。

## Evidence bundle

次を一つのbundle digestへ固定する。

```text
stakeholder_context_digest
relational_context_digest
wa_context_digest
dissent_registry_digest
minority_registry_digest
candidate_evidence_items
```

candidate evidenceのsilent substitutionを禁止する。

## Intake receipt

成功時のstatusは次である。

```text
DECISIONOS_WORLD_CONDITIONED_HANDOFF_INTAKE_READY
```

receiptは次を保証する。

```text
intake_owned_by_decision_os = true
source_owned_by_plan_os = true
deliberation_intake_ready = true
all_candidates_considered = true
candidate_identity_preserved = true
retained_alternatives_preserved = true
wa_evidence_preserved = true
stakeholder_context_preserved = true
relational_context_preserved = true
dissent_visibility_preserved = true
minority_visibility_preserved = true
silent_substitution_detected = false
```

## Selection boundary

DecisionOSがselection責務を持つことと、このintakeがselection authorityを付与することは異なる。

```text
decisionos_owns_selection = true
selection_authority_granted_by_intake = false
decision_selection_performed = false
selected_candidate_id = ""
decision_receipt_issued = false
```

intake readyはselection completeではない。

## OS責務分離

```text
PlanOS
  WORLD-conditioned distribution and advisory ranking

DecisionOS intake
  source and evidence validation

DecisionOS deliberation
  Wa, dissent, minority, stakeholder context evaluation

DecisionOS selection
  admissible candidate selection and decision receipt

PlanOS synthesis
  selected candidateからfuture-only plan basisを合成

ActOS
  execution feasibility and bounded authorization
```

## Fail-closed条件

次の場合はreceiptを生成しない。

```text
source handoff certificate digest不一致
PlanOS version不一致
WORLD binding、state、revision、lineage欠落
source boundaryのauthorityまたはexecution昇格
selected candidateの先行設定
候補集合不一致
確率分布の非正規化
許容候補の正の支持欠落
不許容候補への非ゼロ質量
advisory ranking不一致
首位集合、margin、entropy、effective support不一致
handoff disposition不一致
candidate evidence itemの欠落または重複
candidate identity、projection、mass、action、rank不一致
許容候補のWa、stakeholder、relational evidence欠落
dissent不在の未証明
minority不在の未証明
不許容候補のzero-mass reason欠落
evidence bundle digest不一致
```

## Lean形式化

```text
intake_preserves_source_distribution_and_ranking
intake_considers_all_candidates_without_substitution
intake_preserves_wa_stakeholder_and_relational_evidence
intake_preserves_dissent_minority_and_explicit_absence
advisory_ranking_is_not_decision_selection
intake_assigns_responsibility_without_downstream_authority
intake_preserves_world_history_and_qi_boundaries
intake_is_not_decision_receipt_plan_synthesis_or_execution
```

## 接続

```text
WORLD-conditioned future distribution
→ PlanOS advisory handoff
→ DecisionOS evidence intake
→ relational deliberation
→ admissible selection
```

v0.5は、PlanOSの確率順位とDecisionOSの判断責任の間に、証拠完全性と責務分離の境界を置く。
