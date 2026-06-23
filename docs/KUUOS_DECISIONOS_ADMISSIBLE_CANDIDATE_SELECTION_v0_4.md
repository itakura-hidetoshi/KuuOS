# DecisionOS Admissible Candidate Selection v0.4

## 位置づけ

DecisionOS v0.4 は、PlanOS v0.20が構成した適格候補集合から一件を選択し、将来専用のselection receiptを生成する。

入力handoffではselectionは未実施である。

v0.4はDecisionOS所有の選択を行うが、plan synthesis、activation、executionは行わない。

## 接続経路

```text
PlanOS v0.20 admissible candidate set
→ DecisionOS source binding
→ all candidates considered
→ robust interval certificate
→ plural and veto-aware evaluation
→ Wa false-harmony gate
→ Two Truths and Middle Way gate
→ one selected admissible candidate
→ future-only selection receipt
```

## 選択集合

selected candidateは次のいずれかに厳密に一致する。

```text
admissible primary candidate
admissible hold candidate
```

PlanOS側のhandoffでは次を保持する。

```text
handoff committed = true
selection performed = false
```

DecisionOS receiptでは次を要求する。

```text
selection receipt supplied = true
selection performed = true
```

## relational selection

DecisionSelectionBoundaryは次を保持する。

```text
all candidates considered
selected candidate admissible
selected identity preserved
retained alternatives preserved
dissent visible
minority preserved
silent substitution absent
```

SelectionCertificateは選択intervalが全alternative intervalをrobust marginで上回ることを証明する。

## plural and Wa boundaries

```text
confirmed false harmony = false
minority preserved = true
dissent considered = true
source plural identity preserved = true
all source options profiled
retained alternatives bounded by source option count
silent substitution = false
```

選択は単純多数決や見かけ上の調和へ還元されない。

## Two Truths and Middle Way

```text
paramartha non-reified = true
selected option not absolute = true
premature collapse = false
nihilistic erasure = false
responsibility abandonment = false
```

選択は実用上の候補確定であり、絶対的真理ではない。

## authority boundary

```text
decision is truth = false
decision is execution = false
decision is host licence = false
future only = true
memory overwrite = false
```

## ownership

```text
candidate selection owner = DecisionOS
plan synthesis owner = PlanOS
execution owner = ActOS
```

DecisionOS v0.4は選択後にplanを合成せず、PlanOSへsource-preserving receiptを渡す。

## event and history

```text
indexAfter = indexBefore.append
historyAfter = appendDecision historyBefore
```

選択eventとdecision historyは一回だけappendされる。

## Lean定理

```text
selection_requires_unselected_decisionos_handoff
selected_candidate_is_from_admissible_set
selection_preserves_admissibility_identity_and_alternatives
selected_constraint_is_admissible_and_non_authoritative
robust_certificate_separates_every_alternative
wa_gate_preserves_dissent_minority_and_identity
wa_plurality_forbids_silent_substitution
selection_preserves_two_truths_and_middle_way
selection_is_not_truth_execution_or_license
selection_event_and_history_append_once
selection_bridge_grants_no_downstream_authority
selection_digest_is_exact
```

## 固定境界

```text
DecisionOS selection != truth
DecisionOS selection != plan synthesis
DecisionOS selection != plan activation
DecisionOS selection != execution permission
DecisionOS selection != host licence
DecisionOS selection != memory overwrite
DecisionOS selection != WORLD update
```

## Honest classification

```text
an exact DecisionOS-owned selection receipt over the PlanOS v0.20 admissible set,
with robust, plural, dissent-preserving, Two-Truths and Middle-Way boundaries,
but without plan synthesis, activation, execution, host licensing,
memory overwrite or WORLD update
```
