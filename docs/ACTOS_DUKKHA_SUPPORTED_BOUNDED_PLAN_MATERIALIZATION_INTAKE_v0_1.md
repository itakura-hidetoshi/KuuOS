# ActOS苦低減支持付き有限plan materialization intake kernel v0.1

## 位置づけ

このkernelはActOS v0.5のmaterialization intake層である。

入力はVerifyOS v0.6が`dukkha_reduction_claim_status = supported`と判定したcertificateと、そのcertificateが束縛するPlanOS v1.04 bounded synthesis receiptである。

VerifyOS certificateだけでは、個々のplan stepを復元できない。

そのため、ActOSはsource plan receiptを同時に受け取り、receipt digestとconcrete plan digestをVerifyOS certificateへ再束縛する。

## Materializationの意味

ここでいうmaterializationは外部作用ではない。

有限planの各stepを、後続のadapter bindingとactivation authorizationが扱える実行候補表現へ変換する。

各候補は次の状態に固定される。

```text
candidate_state = prepared_not_activated
adapter_binding_digest = ""
tool_invocation_requested = false
external_side_effect_requested = false
execution_permission_requested = false
active_now_requested = false
```

したがって、この層ではtoolを呼び出さず、外部状態も変更しない。

## Admission条件

次をすべて要求する。

```text
verifyos_version = v0.6
dukkha_reduction_claim_status = supported
verification_disposition =
  dukkha_reduction_supported_for_materialization_intake
materialization_intake_admitted = true
```

`indeterminate`と`contradicted`は受理しない。

構造破損もcertificateの意味的反証へ変換せず、fail-closedとする。

## Source planの再検証

PlanOS v1.04 receiptについて次を再検証する。

- receipt digest。
- concrete plan digest。
- VerifyOS certificateとのplan receipt binding。
- VerifyOS certificateとのconcrete plan binding。
- step count。
- step sequence。
- step IDとaction digestの一意性。
- action class。
- precondition。
- expected effect。
- effect tag。
- evidence lineage。
- stop condition。
- reversibility。
- irreversible stepの先行checkpoint。
- 固定禁止効果の不在。

## 一対一写像

各plan step \(s_i\) からmaterialization candidate \(m_i\) を一つだけ構成する。

\[
s_i \longmapsto m_i
\]

写像は次を保持する。

```text
source_step_id
sequence_index
source_action_class
source_action_spec_digest
precondition_digests
expected_effect_digests
effect_tags
evidence_lineage_digests
stop_condition_digests
reversible
irreversible
checkpoint_step_id
branch_ids
```

candidate IDはsource step IDから決定的に生成する。

```text
materialize-<source_step_id>
```

## Materialization class

action classは実行ではなく候補型へ写像する。

```text
analyze
→ analysis_candidate

condition_reassessment
→ condition_reassessment_candidate

evidence_collection
→ evidence_collection_candidate

hold
→ bounded_hold_candidate

prepare_reversible
→ reversible_preparation_candidate

request_revision
→ revision_request_candidate

review_checkpoint
→ review_checkpoint_candidate

terminate
→ termination_candidate
```

この型はadapter、tool、外部endpointを指定しない。

## 苦低減claimの保持

ActOSはVerifyOSの判定を再最適化しない。

次をlineageとして保持する。

```text
dukkha_assessment_digest
reference_plan_digest
dukkha_reduction_support_preserved
protected_group_nonexternalization_preserved
future_nonexternalization_preserved
revision_capacity_preserved
persistent_loop_reduction_preserved
```

ActOSが単一効用を再導入して候補順序を変更する経路はない。

## 代替、異論、少数側

PlanOS receiptが保持したalternative candidate、dissent evidence、minority evidenceをmaterialization intakeでも保持する。

選択済み候補だけを残し、非選択候補のlineageを消去してはならない。

## 権限境界

```text
selection_remains_decisionos_owned = true

selection_authority_granted_to_actos = false
plan_revision_authority_granted_to_actos = false
dukkha_minimization_authority_granted_to_actos = false

plan_activated = false
adapter_binding_performed = false
adapter_invocation_performed = false
tool_invocation_performed = false
external_side_effect_performed = false

execution_authority_granted = false
execution_permission = false
persistent_world_state_unchanged = true
active_now = false
```

materialization candidateは実行可能性の記述であり、実行許可ではない。

## Fail-closed条件

次の場合はreceiptを発行しない。

- VerifyOS v0.6 certificateが存在しない。
- certificate digestが不正または期待値と不一致である。
- claim statusが`supported`ではない。
- source plan receiptが存在しない。
- plan receipt digestまたはconcrete plan digestが不正である。
- VerifyOS certificateとplan receiptのbindingが一致しない。
- step schema、sequence、action class、reversibilityが不正である。
- checkpoint、stop condition、evidence lineageが失われている。
- forbidden effectが含まれる。
- materialization bundle digestが一致しない。

## Lean形式化

Lean moduleは次を表現する。

```text
supported_claim_is_required_for_materialization_intake

materialization_intake_preserves_step_bijection_and_sequence

materialization_intake_preserves_checkpoint_stop_and_evidence

materialization_intake_preserves_alternatives_dissent_and_minority

materialization_intake_preserves_dukkha_nonexternalization

materialization_intake_preserves_lineage_and_responsibility

materialization_intake_grants_no_selection_revision_or_minimization_authority

materialization_intake_is_not_activation_adapter_invocation_or_execution
```

## 接続

```text
DecisionOS justified selection
→ PlanOS bounded synthesis
→ VerifyOS bounded plan verification
→ VerifyOS dukkha reduction claim verification
→ ActOS bounded plan materialization intake
```

次段は、materialization candidateに対してadapter候補とauthority envelopeを束縛し、実行前のactivation authorizationを行う層である。
