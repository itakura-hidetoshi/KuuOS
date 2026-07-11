# VerifyOS bounded plan middle-way verification kernel v0.1

## 位置づけ

このkernelはVerifyOS v0.5の計画再検証層である。

入力はPlanOS v1.04が発行したbounded synthesis receiptである。

PlanOSが計画を合成した事実だけでは、その計画をmaterialization intakeへ渡してよいとは限らない。

VerifyOSは計画構造と現在のWORLD条件を分けて再検証する。

## 二種類の不一致

計画receiptのdigest、step列、checkpoint、stop condition、禁止効果、証拠lineageが破損している場合はfail-closedとする。

この場合、verification certificateを発行しない。

一方、計画構造が正しくても、現在のWORLD binding、state、revision、lineageがsourceと異なる場合がある。

これは計画が存在しなかったことを意味しない。

この場合は次へ写像する。

```text
conditional_validity_status = revision_required
verification_disposition = return_to_planos_revision
materialization_intake_admitted = false
```

計画receiptとpredecessor lineageを保持したままPlanOS改訂経路へ戻す。

## 現在条件が一致する場合

次の四つがsourceと一致する場合、WORLD条件はcurrentである。

```text
WORLD binding digest
WORLD model state digest
WORLD revision
WORLD lineage digest
```

この場合は次となる。

```text
conditional_validity_status = valid
verification_disposition = bounded_plan_verified_for_materialization_intake
materialization_intake_admitted = true
```

このadmissionはmaterializationそのものではない。

ActOS実行許可でもない。

## 構造再検証

VerifyOSは次をsource receiptから再計算する。

- receipt digest。
- 有限plan schema。
- synthesis constraint schema。
- planning horizonとstep上限。
- branch上限とrevision上限。
- step sequenceの連続性。
- step IDとaction digestの一意性。
- action classの許容集合。
- reversibleとirreversibleの排他性。
- 不可逆stepに対する先行review checkpoint。
- stop conditionの完全保持。
- 固定禁止効果の不在。
- selected candidateとplan intentの連続性。
- WORLD state dependency。
- alternative candidate record。
- dissent evidenceとminority evidence。
- lineageとresponsibility lineage。

## 固定禁止効果

次の集合を完全に保持する。

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

plan stepのeffect tagに一つでも含まれる場合、certificateを発行しない。

## Checkpoint

不可逆stepには先行するreview checkpointへの参照が必要である。

```text
irreversible step i
→ checkpoint step j exists
→ j < i
→ action_class(j) = review_checkpoint
```

reversible stepがcheckpoint参照を持つ場合も拒否する。

## 証拠と代替候補

非選択候補は空集合へ消去できない。

各alternative recordはcandidate ID、非選択理由、改訂時保持宣言を持つ。

source dissent evidenceとminority evidenceはplan全体のevidence lineageに含まれなければならない。

各stepのevidence参照はplan全体のevidence lineageの部分集合でなければならない。

## 中道的状態

VerifyOSは計画を永続的真理へ昇格しない。

```text
plan_remains_conditionally_binding = true
plan_not_reified = true
plan_not_erased = true
condition_change_routes_to_revision = true
```

WORLD条件が変化しても、計画をnullへ変換しない。

旧計画をlineageとして保持し、改訂要求を発行する。

## 権限境界

```text
selection_remains_decisionos_owned = true
selection_authority_granted_to_verifyos = false
plan_revision_authority_granted_to_verifyos = false
plan_activated = false
materialization_performed = false
execution_authority_granted = false
execution_permission = false
persistent_world_state_unchanged = true
world_mutation_not_granted = true
future_only = true
active_now = false
```

VerifyOSは計画を検証する。

VerifyOS自身が候補を選び直したり、計画を書き換えたり、実行したりしない。

## Fail-closed条件

次の場合はcertificateを発行しない。

- source receiptが存在しない。
- receipt digestが不正または期待値と不一致である。
- PlanOS v1.04境界が失われている。
- planまたはconstraint mappingが一意に見つからない。
- boundが許容範囲外である。
- alternative fieldが空または不正である。
- step sequence、action class、reversibilityが不正である。
- checkpointが欠落または後置されている。
- stop conditionまたは禁止効果が不正である。
- selected candidateまたはplan intentが差し替えられている。
- dissentまたはminority evidenceが消去されている。
- verification bundle digestが一致しない。

## Lean形式化

Lean moduleは次を表現する。

```text
current_world_conditions_admit_materialization_intake
changed_world_conditions_require_plan_revision
bounded_plan_structure_is_reverified
checkpoint_stop_and_effect_boundaries_are_reverified
verification_preserves_selection_plan_intent_and_world_dependency
verification_preserves_alternatives_dissent_and_minority
verification_preserves_lineage_and_responsibility
verified_plan_remains_middle_way_conditioned
verification_grants_no_selection_or_revision_authority
verification_is_not_activation_materialization_or_execution
```

## 接続

```text
PlanOS v1.04 bounded synthesis receipt
→ VerifyOS v0.5 structural and WORLD-condition verification
→ valid: materialization intake candidate
→ revision_required: PlanOS revision route
```

このkernelはmaterialization前の中道的preflightである。
