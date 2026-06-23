# PlanOS World Host-Effect History and Qi Generation v0.25

## 位置づけ

PlanOS v0.25は、PlanOS v0.24のpristine replan intakeから、read-only non-Markov history、Qi conditioning、candidate generationまでを進める。

この層は候補を生成するが、候補を選択せず、計画を合成せず、活性化や実行を行わない。

## 接続経路

```text
LearnOS v0.4 future-only learning receipt
→ PlanOS v0.24 pristine replan intake
→ read-only non-Markov history
→ Qi context conditioning
→ primary replan candidate
→ explicit hold alternative
→ immutable generation receipt
```

## deterministic phase prefix

```text
bind
→ history
→ qiCondition
→ generate
```

`constrain`、`deliberate`、`synthesize`、`commitNext`へは自動遷移しない。

## non-Markov history

```text
previous plan changes visible = true
failed transitions visible = true
oscillation history visible = true
recovery history visible = true
stagnation history visible = true
path dependence visible = true
source history mutation = false
```

履歴は候補生成の文脈として参照されるが、元の履歴を変更しない。

## Qi境界

```text
process tensor bound = true
process history bound = true
transition readiness visible = true
hysteresis visible = true
Qi context only = true
Qi truth authority = false
Qi causal authority = false
Qi execution authority = false
Qi clinical authority = false
Qi activates plan = false
```

## verdictと候補

```text
passed
→ strengthen or hold

failed
→ repair or hold

indeterminate
→ reobserve or hold
```

すべての経路で明示的な`hold` alternativeを保持する。

## WORLD dispositionとの分離

```text
source disposition preserved = true
governance review preserved = true
WORLD commit separate = true
fresh commit authorization required = true
fresh commit authorization supplied = false
atomic commit ready = false
generated candidate is WORLD disposition = false
generation resolves WORLD disposition = false
```

replan candidateはPlanOSの候補であり、WORLD adoptionまたはrejectionの決定ではない。

## 所有権

```text
candidate generation owner = PlanOS
candidate selection owner = DecisionOS
plan synthesis owner = PlanOS
execution owner = ActOS
WORLD disposition owner = WORLD
```

## receiptとevent lineage

```text
generation receipt committed = true
generation receipt immutable = true
append only = true
exact replay idempotent = true
conflicting replay accepted = false

PlanOS intake index
< history index
< Qi index
< generation index
```

history、Qi、generationの3 phase recordをappendする。

## 非権限境界

```text
candidate generation != candidate selection
candidate generation != plan synthesis
candidate generation != replan activation
candidate generation != plan activation
candidate generation != execution permission
candidate generation != host license
candidate generation != WORLD disposition resolution
candidate generation != WORLD update
candidate generation != memory overwrite
```

## Leanファイル

```text
WorldHostEffectHistoryQiCandidateGenerationCoreV0_25.lean
WorldHostEffectHistoryQiCandidateGenerationTypesV0_25.lean
WorldHostEffectHistoryQiCandidateGenerationV0_25.lean
```

## Lean定理

```text
world_generation_preserves_disposition_candidate
generation_receipt_is_replay_safe
generation_requires_exact_planos_intake
generation_follows_deterministic_phase_prefix
generation_phase_events_append_strictly
generation_history_is_nonmarkov_and_read_only
generation_qi_is_context_without_authority
passed_verification_generates_strengthen_or_hold
failed_verification_generates_repair_or_hold
indeterminate_verification_generates_reobserve_or_hold
generation_preserves_explicit_hold_alternative
generation_preserves_world_disposition_candidate
generation_history_appends_three_phase_records
generation_commit_is_not_selection_synthesis_or_activation
generation_preserves_os_ownership
generation_bridge_grants_no_new_authority
generation_digest_is_exact
```
