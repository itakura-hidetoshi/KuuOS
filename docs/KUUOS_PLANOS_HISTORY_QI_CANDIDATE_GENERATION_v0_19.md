# PlanOS History Qi Candidate Generation v0.19

## 位置づけ

PlanOS v0.19 は、PlanOS v0.18のreplan intakeを、read-only non-Markov history、Qi conditioning、candidate generationへ進める。

この層が進める位相は次だけである。

```text
bind
→ history
→ qiCondition
→ generate
```

constraint、DecisionOS selection、plan synthesis、activation、executionは後続層に残る。

## candidate写像

LearnOS v0.3のlearning kindを次のprimary candidateへ写像する。

```text
reinforcement → strengthen
repair        → repair
reobservation → reobserve
hold          → hold
```

検証verdictとの合成結果は次となる。

```text
passed        → strengthen or hold
failed        → repair or hold
indeterminate → reobserve or hold
```

すべての場合に明示的なhold alternativeを保持する。

## non-Markov history

candidate generationは現在状態だけを使わない。

次の履歴を可視化する。

```text
previous plan changes
failed transitions
oscillation history
recovery history
stagnation history
path dependence
```

履歴はread-onlyであり、source history mutationはfalseである。

## Qi conditioning

Qiは次をcontextとして与える。

```text
process tensor
process history
transition readiness
hysteresis
```

Qiはtruth、causality、execution、clinical authorityを持たない。

Qiはplanをactivationしない。

## append-only phase events

PlanOS v0.18のintake eventの後に、history、Qi condition、generationの3 eventを順にappendする。

```text
intake index < history index < Qi index < generation index
```

replan historyには3 recordを追加する。

```text
historyAfterGeneration.committedRecords
  = intake.historyAfter.committedRecords + 3
```

snapshotはcommit数から導出される。

## 所有権

```text
candidate generation owner = PlanOS
candidate selection owner  = DecisionOS
plan synthesis owner       = PlanOS
execution owner            = ActOS
```

generation commitはselectionではない。

generation commitはplan synthesisではない。

## 非権限境界

```text
candidate generation != replan activation
candidate generation != DecisionOS selection
candidate generation != plan synthesis
candidate generation != execution permission
candidate generation != host licence
candidate generation != memory overwrite
candidate generation != WORLD update
```

## Lean定理

```text
generation_requires_exact_planos_intake
generation_follows_deterministic_phase_prefix
generation_phase_events_append_strictly
generation_history_is_nonmarkov_and_read_only
generation_qi_is_context_without_authority
passed_verification_generates_strengthen_or_hold
failed_verification_generates_repair_or_hold
indeterminate_verification_generates_reobserve_or_hold
generation_preserves_explicit_hold_alternative
generation_history_appends_three_phase_records
generation_commit_is_not_selection_synthesis_or_activation
generation_preserves_os_ownership
generation_bridge_grants_no_new_authority
generation_digest_is_exact
generated_candidate_value_remains_exact
```

## Honest classification

```text
an exact PlanOS candidate-generation prefix over the v0.18 intake,
using read-only non-Markov history and non-authoritative Qi context,
with a verdict-compatible primary candidate and explicit hold alternative,
but without constraint adjudication, DecisionOS selection, plan synthesis,
activation, execution, host licensing, memory overwrite or WORLD update
```
