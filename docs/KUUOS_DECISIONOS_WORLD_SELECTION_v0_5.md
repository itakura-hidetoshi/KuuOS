# DecisionOS World Selection v0.5

## 位置づけ

DecisionOS v0.5は、PlanOS v0.26が渡したadmissible setから、primary候補またはhold候補を明示的に選択する。

この層は計画を合成せず、活性化せず、実行せず、WORLD dispositionを解決しない。

## 接続経路

```text
PlanOS v0.26 admissible-set handoff
→ explicit DecisionOS selection
→ admissibility and identity preservation
→ robust selection certificate
→ Qi decision context
→ two-truths and middle-way gate
→ Wa endorsement and plurality preservation
→ immutable selection receipt
```

## source条件

```text
handoff committed = true
source selection receipt supplied = false
source selection performed = false
new selection receipt supplied = true
new selection performed = true
```

選択は一度だけ行われる。

## admissible set

selected candidateは次のいずれかに限る。

```text
included primary candidate
included hold candidate
```

すべての候補を考慮し、selected candidateのadmissibilityとidentityを保持する。

alternatives、dissent、minorityを削除しない。

silent substitutionを禁止する。

## robust certificate

selection certificateは、すべての代替候補について次を要求する。

```text
alternative upper bound < selected lower bound
```

この条件は候補間のrobust separationを表す。

## 和とplurality

```text
false harmony confirmed = false
minority preserved = true
dissent considered = true
plural identity preserved = true
profiled option count = source option count
retained alternatives <= source options
silent substitution = false
```

## two truthsとmiddle way

```text
paramartha non-reified = true
selected option not absolute = true
premature collapse = false
nihilistic erasure = false
responsibility abandonment = false
```

選択された候補は実用上の次cycle候補であり、絶対的真理ではない。

## WORLD dispositionとの分離

```text
source disposition preserved = true
governance review preserved = true
WORLD commit separate = true
fresh commit authorization required = true
fresh commit authorization supplied = false
atomic commit ready = false
selected replan candidate is WORLD disposition = false
selection resolves WORLD disposition = false
```

DecisionOSのreplan candidate selectionは、WORLD adoption、rejection、deferの最終決定ではない。

## future-only境界

```text
decision is truth = false
decision is execution = false
decision is host license = false
future only = true
memory overwrite = false
decision not execution = true
```

## 所有権

```text
selection owner = DecisionOS
synthesis owner = PlanOS
execution owner = ActOS
WORLD disposition owner = WORLD
```

## receiptとledger

```text
selection receipt committed = true
selection receipt immutable = true
append only = true
exact replay idempotent = true
conflicting replay accepted = false
selection event append = 1
selection history append = 1
```

## 非権限境界

```text
selection != plan synthesis
selection != plan activation
selection != execution
selection != host license
selection != WORLD disposition resolution
selection != WORLD update
selection != memory overwrite
```

## Leanファイル

```text
WorldHostEffectAdmissibleSelectionCoreV0_5.lean
WorldSelectionBridgeV0_5.lean
WorldSelectionReceiptV0_5.lean
WorldHostEffectAdmissibleSelectionTypesV0_5.lean
SelectionV0_5.lean
```

## Lean定理

```text
selection_preserves_world_disposition
decision_selection_receipt_is_replay_safe
selection_requires_unselected_decisionos_handoff
selected_candidate_is_from_admissible_set
selection_preserves_admissibility_identity_and_alternatives
selected_constraint_is_admissible_and_non_authoritative
robust_certificate_separates_every_alternative
wa_gate_preserves_dissent_minority_and_identity
wa_plurality_forbids_silent_substitution
selection_preserves_two_truths_and_middle_way
selection_preserves_world_disposition_candidate
selection_receipt_is_immutable_append_only_and_replay_safe
selection_is_not_truth_execution_license_or_world_resolution
selection_event_and_history_append_once
selection_bridge_preserves_ownership
selection_bridge_grants_no_downstream_authority
selection_digest_is_exact
```
