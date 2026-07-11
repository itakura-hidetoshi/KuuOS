# DecisionOS Bounded Plan Synthesis Request Handoff v0.8

## 位置づけ

DecisionOS v0.8は、v0.7で理由付き選択された候補をPlanOSへ戻し、具体的計画の合成を依頼するhandoff層である。

このhandoffは実行命令ではない。

このhandoffはPlanOSへ選択権限を移転しない。

このhandoffはpersistent WORLD stateを変更しない。

## 入力

入力はDecisionOS v0.7 selection justification receiptである。

source receiptは次を満たさなければならない。

- DecisionOSが候補選択を完了している。
- 選択候補がrelational frontierに属する。
- 全候補のidentityが保持されている。
- 非選択理由が保持されている。
- 異論、少数側、required review fieldが保持されている。
- PlanOS、WORLD model、Qiから選択権限を継承していない。
- plan synthesisとexecutionがまだ行われていない。

source receipt全体、selection bundle、候補別justification digestを再計算する。

## 選択候補の不変性

handoffが受理する候補はsource receiptのselected candidateと一致しなければならない。

候補の差し替えを認めない。

handoff後も候補選択の責任はDecisionOSに残る。

PlanOSは選択をやり直さない。

PlanOSは選択理由を単一効用へ再縮約しない。

## bounded synthesis scope

handoffは次の有限境界を固定する。

- planning horizon steps
- maximum plan steps
- maximum branching factor
- maximum revision cycles
- reversible action requirement
- checkpoint before irreversible step
- required checkpoints
- stop conditions
- preserved evidence
- forbidden effects

planning horizonは1以上64以下とする。

maximum plan stepsは1以上32以下とし、planning horizonを超えてはならない。

maximum branching factorは1以上8以下とする。

maximum revision cyclesは0以上8以下とする。

## 可逆性とcheckpoint

PlanOSへ渡すrequestは、原則として可逆なactionから構成されなければならない。

不可逆なstepを候補として含める場合は、その前に明示的なcheckpointを要求する。

checkpoint digestが空の場合はfail closedとする。

## 停止条件

stop condition digestを一つ以上要求する。

境界違反、証拠矛盾、責任主体不在、scope expansionが検出された場合に停止できる構造を前提とする。

停止条件はplan synthesisの中断条件であり、execution permissionではない。

## 証拠lineage

preserved evidence fieldは少なくとも次を含む。

- source selection receipt digest
- selected candidate source record digest
- PlanOS handoff certificate digest
- WORLD binding digest
- WORLD model state digest
- WORLD lineage digest
- selected candidate support rationale digests
- selected candidate opposition rationale digests

この要件により、PlanOSは選択結果だけを受け取り、選択理由を失うことができない。

retained alternatives、nonadmissible candidates、非選択理由、異論、少数側、review resolutionもhandoff receiptへ保持する。

## 禁止効果

forbidden effects fieldは次の完全な集合と一致しなければならない。

- active now
- candidate substitution
- execution permission
- external side effect
- persistent WORLD mutation
- selection authority transfer
- tool invocation
- unreviewed scope expansion

一つでも欠ける場合はhandoffを発行しない。

## 権限境界

DecisionOSは選択済み候補に対するbounded synthesis requestを発行する。

PlanOSはその有限scope内で計画候補を合成する責任を受け取る。

PlanOSは選択権限を受け取らない。

PlanOSは実行権限を受け取らない。

WORLD model、履歴、Qiはplanning contextを条件付けるが、権限を生成しない。

## downstream requirement

v0.8はplan synthesis requestを発行するが、concrete planを発行しない。

PlanOSが生成した計画は、別のplan receiptによって検証されなければならない。

plan receiptがない結果を受理しない。

plan synthesis receiptもexecution permissionではない。

## receipt主要field

```text
source_selection_receipt_digest
synthesis_policy_digest
planos_recipient_digest
request_owner_responsibility_digest
synthesis_request_id
selected_candidate_id
selected_candidate_plan_intent_digest
synthesis_constraint_spec
synthesis_constraint_digest
synthesis_handoff_bundle_digest
```

## 主要不変条件

```text
selected_candidate_not_substituted = true
selection_remains_decisionos_owned = true
candidate_evidence_lineage_preserved = true
plan_synthesis_request_issued = true
planos_synthesis_scope_bounded = true
planos_receives_request_not_selection_authority = true
selection_authority_transferred_to_planos = false
execution_authority_granted_to_planos = false
plan_synthesis_performed = false
concrete_plan_issued = false
plan_receipt_issued = false
persistent_world_state_unchanged = true
future_only = true
active_now = false
execution_permission = false
```

## fail-closed条件

次の場合はblockedとする。

- source receiptが欠落している。
- source receipt digestまたはselection bundleが一致しない。
- source candidate justification digestが一致しない。
- 選択候補がsourceと一致しない。
- synthesis policy、recipient、owner、request ID、plan intentが欠落している。
- horizon、step数、branching、revision回数が有限境界を超える。
- 可逆性またはcheckpoint要件が解除されている。
- checkpointまたは停止条件が空である。
- 証拠lineageが欠落している。
- forbidden effects集合が変更されている。
- constraint digestまたはhandoff bundle digestが一致しない。
- source側でexecution permissionまたはWORLD mutationが昇格している。

## 接続

```text
PlanOS v1.02 advisory distribution handoff
→ DecisionOS v0.5 evidence intake
→ DecisionOS v0.6 relational deliberation
→ DecisionOS v0.7 selection justification
→ DecisionOS v0.8 bounded plan synthesis request handoff
→ future PlanOS bounded synthesis receipt
```
