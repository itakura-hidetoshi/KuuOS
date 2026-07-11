# VerifyOS Middle-Way Conditional Continuity Verification v0.4

## 位置づけ

本層は、DecisionOS v0.8のbounded plan synthesis requestをPlanOSへ渡す前に、中道的連続性が成立しているかをVerifyOSで検証する。

中道の定義そのものはKuuOS共通原理である。

VerifyOSは、その原理が具体的な状態遷移で成立しているかを証明する。

```text
DecisionOS v0.8 handoff
→ VerifyOS middle-way verification
→ verified bounded synthesis request
→ PlanOS bounded synthesis intake
```

本層は計画合成を行わない。

本層は実行許可を与えない。

## 中道不変条件

本層は次を中核不変条件とする。

```text
preserve without reifying
revise without erasing
commit without absolutizing
terminate without denying lineage
```

選択または計画要求を永続的真理として固定しない。

同時に、暫定的であることを理由に履歴、責任、異論、少数側証拠を消去しない。

## 状態表現

遷移対象を単一の値として扱わない。

```text
Xi_t = (
  object,
  conditions,
  lineage,
  responsibility
)
```

各成分は次を表す。

- `object`：選択、計画要求、計画または実行状態
- `conditions`：現在の成立条件
- `lineage`：前状態と証拠の継承関係
- `responsibility`：責任主体と理由の履歴

## 遷移種別

```text
retain
suspend
request_revision
supersede_with_lineage
complete
terminate
```

単純な`replace`は用いない。

前状態を消去せず、新状態が前状態をlineageとして保持するためである。

## 条件付き有効性

遷移種別と状態は一対一に対応する。

```text
retain                  → valid
suspend                 → suspended
request_revision        → revision_required
supersede_with_lineage  → superseded
complete                → completed
terminate               → terminated
```

`retain`では成立条件が変化していてはならない。

`retain`以外では、条件変化を明示しなければならない。

changed condition fieldは、source conditionsとcurrent conditionsの対称差と一致しなければならない。

## Lineage

次を要求する。

```text
source_lineage ⊆ resulting_lineage
predecessor_reference ∈ resulting_lineage
source_object_digest ∈ resulting_lineage
```

改訂、継承、完了、終了のいずれでも、前状態を無かったことにしない。

## 責任

```text
source_responsibility_lineage
⊆
resulting_responsibility_lineage
```

VerifyOSの責任主体もresulting responsibility lineageに含める。

責任主体の変更は、旧責任主体の削除ではなく追加lineageとして表現する。

## 異論と少数側証拠

DecisionOS v0.8で保持された異論と少数側証拠を平坦化して再検証する。

```text
source dissent evidence
⊆
preserved dissent evidence

source minority evidence
⊆
preserved minority evidence
```

改訂または終了を理由に証拠を削除できない。

## 常見側の拒否

次を拒否する。

```text
object_eternal_truth_claimed = true
authority_expansion_requested = true
execution_permission_requested = true
persistent_world_mutation_requested = true
```

選択、計画要求、WORLD predictionを永続的真理または権限源へ昇格しない。

## 断見側の拒否

次を拒否する。

```text
object_disposable_null_claimed = true
silent_rewrite_requested = true
history_erasure_requested = true
lineage_not_monotone
predecessor_reference_missing
dissent_evidence_erased
minority_evidence_erased
responsibility_lineage_not_monotone
```

空であることは無責任または無履歴を意味しない。

## Source再検証

DecisionOS v0.8 handoffについて次を再検証する。

```text
receipt digest
selected candidate continuity
bounded synthesis scope
retained alternatives
retained nonadmissible candidates
nonselection reasons
dissent visibility
minority visibility
WORLD binding and lineage
selection authority boundary
execution boundary
```

Source receiptの一部が変更されて再digestされていても、required boundaryが失われていれば拒否する。

## 出力

```text
VerifyOSMiddleWayConditionalContinuityCertificate:
  source_handoff_receipt_digest
  source_selection_receipt_digest
  source_world_binding_digest
  source_world_model_state_digest
  source_world_model_revision
  source_world_lineage_digest

  selected_candidate_id
  selected_candidate_plan_intent_digest

  verification_policy_digest
  verification_owner_responsibility_digest
  verification_request_id

  transition_spec
  transition_spec_digest
  verification_bundle_digest

  transition_kind
  conditional_validity_status
  transition_reason_digest

  conditions_explicit
  changed_conditions_explicit
  predecessor_preserved
  lineage_monotone
  responsibility_preserved
  dissent_preserved
  minority_evidence_preserved

  object_not_reified
  object_not_erased
  commitment_not_absolutized
  revision_preserves_lineage
  supersession_preserves_predecessor
  termination_does_not_erase_history

  authority_unchanged
  execution_permission_not_granted
  persistent_world_state_unchanged

  verification_passed
  certificate_digest
```

## VerifyOS境界

```text
selection_remains_decisionos_owned = true
planos_receives_verified_request_not_selection_authority = true
plan_synthesis_performed = false
concrete_plan_issued = false
plan_receipt_issued = false
active_now = false
execution_permission = false
```

VerifyOS certificateはPlanOS intakeの必要条件である。

ただし、VerifyOS certificate自体は計画でも実行許可でもない。

## Lean形式化

```text
transition_status_is_conditioned
lineage_monotone_preserves_source
predecessor_is_not_erased
revision_preserves_responsibility
dissent_is_not_erased
minority_evidence_is_not_erased
supersession_preserves_predecessor
termination_does_not_deny_lineage
middle_way_rejects_reification_and_erasure
middle_way_preserves_authority_boundary
middle_way_verification_is_not_plan_or_execution
```

## OS責務

```text
KuuOS Core
  defines middle-way conditional continuity invariants

DecisionOS
  owns selection and issues the bounded synthesis request

VerifyOS
  verifies conditional continuity, lineage and responsibility

PlanOS
  consumes only a verified bounded synthesis request

MemoryOS
  persists predecessor and lineage records

ActOS
  cannot infer execution permission from this certificate
```

これにより、中道は外付けの事後監査ではなく、OS間遷移を成立させる内部ガバナンスになる。
