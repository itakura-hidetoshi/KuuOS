# PlanOS bounded synthesis receipt kernel v0.1

## 位置づけ

このkernelはPlanOS v1.04の計画合成層である。

入力はPlanOS v1.03が発行した中道的bounded synthesis intake certificateである。

このkernelは有限の計画step列を構成し、digest-bound plan receiptを発行する。

ただし、計画をactive化しない。

計画をmaterializeしない。

ActOS実行許可を発行しない。

persistent WORLD stateを変更しない。

## Admission

入力certificateは次を満たさなければならない。

```text
conditional_validity_status = valid
transition_kind = retain
intake_disposition = bounded_synthesis_intake_ready
bounded_synthesis_request_admitted = true
bounded_synthesis_intake_ready = true
```

`suspended`、`revision_required`、`superseded`、`completed`、`terminated`から計画を合成しない。

VerifyOSの検証成功だけを一般的な合成権限として扱わない。

## Source binding

次を外部の期待値と照合する。

- **PlanOS v1.03 intake certificate digest**。
- **WORLD binding digest**。
- **WORLD model state digest**。
- **WORLD revision**。
- **WORLD lineage digest**。
- **selected candidate ID**。
- **selected candidate plan intent digest**。
- **synthesis constraint digest**。

source certificateを改変して再digestしても、外部の期待digestと一致しなければ拒否する。

## Synthesis constraints

constraint schemaは次で固定する。

```text
planning_horizon
maximum_plan_steps
maximum_branching_factor
maximum_revision_cycles
reversible_actions_required
irreversible_step_requires_checkpoint
stop_condition_digests
forbidden_effects
```

範囲は次である。

```text
1 <= planning_horizon <= 64
1 <= maximum_plan_steps <= 32
maximum_plan_steps <= planning_horizon
1 <= maximum_branching_factor <= 8
0 <= maximum_revision_cycles <= 8
```

constraint全体は`synthesis_constraint_digest`へ固定する。

このdigestはv1.03が保持する`source_synthesis_constraint_digest`と一致しなければならない。

## Plan schema

計画は次を持つ。

```text
plan_id
plan_revision
selected_candidate_id
selected_candidate_plan_intent_digest
world_state_dependency_digest
stop_condition_digests
retained_alternative_records
preserved_evidence_lineage_digests
steps
```

初回計画の`plan_revision`は0である。

selected candidateを差し替えない。

plan intentを差し替えない。

WORLD state dependencyを差し替えない。

## Plan step

各stepは次を持つ。

```text
step_id
sequence_index
action_class
action_spec_digest
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

`sequence_index`は1から連続しなければならない。

step IDとaction spec digestは重複できない。

各stepはreversibleまたはirreversibleのいずれか一方でなければならない。

## Action class

許可するclassは次である。

```text
analyze
condition_reassessment
evidence_collection
hold
prepare_reversible
request_revision
review_checkpoint
terminate
```

これらは未来計画上の意味分類である。

このkernel内でtool invocationまたは外部作用へ変換しない。

## Checkpoint

irreversible stepには、先行する`review_checkpoint` stepへの参照を要求する。

```text
irreversible = true
→ checkpoint_step_id is nonempty
→ checkpoint_step_id refers to an earlier review_checkpoint
```

reversible stepはcheckpoint参照を持たない。

これにより、不可逆的内容を計画へ含める場合でも、再検証点を越えて直接実行へ進めない。

## Stop condition

constraintで定義されたすべてのstop conditionを、計画全体と各stepへ保持する。

stop conditionが欠けるstepは拒否する。

計画合成後に条件が変わった場合、VerifyOS再検証またはDecisionOS改訂へ戻る余地を残す。

## Forbidden effects

次の完全な集合を禁止する。

```text
active_now
candidate_substitution
execution_permission
external_side_effect
persistent_world_mutation
selection_authority_transfer
tool_invocation
unreviewed_scope_expansion
```

`effect_tags`に一つでも含まれる場合、receiptを発行しない。

## Alternative preservation

非選択候補は消去しない。

各alternative recordは次を持つ。

```text
candidate_id
nonselection_reason_digest
retained_for_revision = true
```

selected candidateをalternative fieldへ重複して含めない。

同一alternative candidateを重複させない。

alternative fieldはcandidate ID順にcanonical化する。

## Evidence preservation

計画全体は`preserved_evidence_lineage_digests`を持つ。

source transition specのdissent evidenceとminority evidenceをすべて保持する。

各stepが参照するevidenceは、計画全体のevidence lineageに含まれなければならない。

これにより、計画合成によって異論または少数側の影響を消去しない。

## Lineage

resulting lineageへ次を追加する。

```text
source intake certificate digest
proposed plan digest
synthesis constraint digest
synthesis bundle digest
```

source lineageは置換しない。

PlanOS synthesis responsibilityを既存responsibility lineageへ追加する。

```text
R_result
= R_source
∪ {R_planos_synthesis}
```

## 中道的計画

発行される計画は条件付きで拘束力を持つ。

```text
plan_is_conditionally_binding = true
plan_is_not_absolute_command = true
plan_is_not_contentless_proposal = true
```

計画は単なる無内容な文章ではない。

しかし、永続的に正しい命令でもない。

条件、WORLD revision、証拠、stop conditionが変化した場合は改訂または停止できる。

改訂時もpredecessor、理由、異論、少数側証拠を消去しない。

## Receipt boundary

このkernelは計画を実際に合成する。

```text
plan_synthesis_performed = true
concrete_plan_issued = true
plan_receipt_issued = true
```

しかし、次はfalseである。

```text
plan_activated = false
materialization_performed = false
selection_authority_granted_to_planos = false
execution_authority_granted = false
execution_permission = false
active_now = false
```

計画receiptはActOS命令ではない。

計画receiptは外部作用ではない。

計画receiptはWORLD state mutationではない。

## Fail-closed条件

次の場合はreceiptを発行しない。

- source intake certificateが存在しない。
- source certificate digestが不正または期待値と不一致である。
- source状態が`valid`ではない。
- source dispositionが`bounded_synthesis_intake_ready`ではない。
- selected candidateまたはplan intentが差し替えられている。
- WORLD binding、state、revision、lineageが一致しない。
- synthesis constraint schemaまたはdigestが一致しない。
- boundが許容範囲外である。
- proposed plan schemaまたはdigestが一致しない。
- step列が空である。
- step数またはbranch数がboundを越える。
- sequenceが連続しない。
- action classが未知である。
- irreversible stepに先行checkpointがない。
- stop conditionが欠落する。
- forbidden effectが含まれる。
- source dissentまたはminority evidenceが消える。
- alternative candidateの理由または保持宣言が欠ける。
- synthesis bundle digestが一致しない。

## Lean形式化

Lean moduleは有限step列、step上限、checkpoint guard、stop condition、evidence preservation、authority boundaryを表現する。

主な定理は次である。

```text
synthesis_requires_ready_middle_way_intake
bounded_plan_is_nonempty
bounded_plan_respects_step_limit
synthesis_preserves_selected_candidate_and_plan_intent
synthesis_preserves_world_dependency_and_bounds
irreversible_steps_require_checkpoint
synthesis_preserves_stop_and_effect_boundaries
synthesis_preserves_alternatives_dissent_and_minority
synthesis_extends_lineage_and_responsibility
synthesized_plan_remains_middle_way_conditioned
plan_synthesis_does_not_inherit_selection_authority
receipt_issues_plan_without_activation_or_execution
```

## 接続

```text
DecisionOS justified selection
→ DecisionOS bounded synthesis request
→ VerifyOS middle-way verification
→ PlanOS middle-way intake
→ PlanOS bounded synthesis receipt
```

次段は、このplan receiptを再検証してmaterialization前の構造的preflightを行う層である。
