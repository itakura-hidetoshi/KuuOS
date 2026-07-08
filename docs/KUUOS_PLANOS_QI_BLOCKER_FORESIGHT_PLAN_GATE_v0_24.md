# PlanOS Qi Blocker Foresight Plan Gate v0.24

## 位置づけ

PlanOS v0.24は、PlanOS v0.23のactivation admission ActOS handoff receiptを入力として、気のプロセステンソル、ブロッカー理論、近年のAI agent理論を候補選別の前処理へ接続する。

この層はPlanOSによるforesight gateだけを所有する。

activation authorizationとexecutionは引き続きActOSが所有する。

v0.24はplanをactivateせず、ActOSを呼び出さず、lease使用を予約せず、blockerを解除しない。

## 文献的接続

v0.24は以下のAI理論をPlanOSの非権限的候補選別へ写像する。

```text
WorldEvolver / self-evolving world model
→ episodic memory
→ semantic mismatch rule
→ selective foresight
→ low-confidence foresight filter
```

```text
Agent Process Reward Model
→ process reward trace
→ candidate weighting
→ reward is evidence, not authority
```

```text
test-time scaling for agents
→ multi-rollout candidates
→ diverse rollout trace
→ verifier trace
→ asymmetric verification
→ list-wise selection support
```

```text
agent memory governance
→ provenance-bound memory evidence
→ rollback trace
→ write-store-retrieve-execute separation
```

```text
graph-based agent memory
→ relational blocker trace
→ candidate lineage and dependency visibility
```

```text
causal world model
→ intervention trace
→ counterfactual consequence support
→ replan signal
```

## 接続経路

```text
PlanOS v0.23 ActOS handoff receipt
→ Qi process tensor foresight evidence
→ blocker classification and reroute boundary
→ AI-theory selection binding
→ low-confidence foresight filter
→ advisory candidate weight surface
→ replan-intake-only receipt
```

## 気のプロセステンソル境界

v0.24では次を要求する。

```text
process tensor visible = true
transition continuity visible = true
memory continuity visible = true
nonmarkov memory visible = true
episodic transition evidence = true
semantic mismatch rule evidence = true
selective foresight accepted = true
causal intervention trace visible = true
process reward trace visible = true
verifier trace visible = true
```

気のプロセステンソルは履歴依存の候補評価面である。

実行権限、真理権限、記憶上書き権限、blocker解除権限を持たない。

## ブロッカー理論境界

v0.24ではブロッカーを次のように扱う。

```text
blocker classified = true
protective blocker preserved = true
situational blocker rerouted = true
missing evidence held = true
blocker release granted = false
blocker bypass granted = false
missing evidence silently repaired = false
blocker context only = true
```

保護的ブロッカーは保存する。

状況的ブロッカーは候補経路のreroute理由に変換する。

不足証拠は沈黙修復せず、holdまたはreobserveの理由として保持する。

## AI-theory selection binding

v0.24では次のbindingを要求する。

```text
multi rollout candidates visible = true
diverse rollout trace bound = true
process reward trace bound = true
verifier trace bound = true
asymmetric verification bound = true
graph memory trace bound = true
memory governance provenance bound = true
rollback trace bound = true
causal world model trace bound = true
lifelong learning trace bound = true
```

これは候補の重み付け、検証、棄却、次周期replanのためのbindingである。

selection bindingはactivation authorizationではない。

## foresight gate

```text
source admission handoff bound = true
candidate weights advisory only = true
low confidence foresight filtered = true
replan signal only = true
activation authorization granted = false
ActOS invoked = false
execution granted = false
truth authority = false
memory overwrite = false
blocker release granted = false
external commit = false
```

低信頼foresightはPlanOS内で候補から落とされるか、replan signalへ変換される。

この変換はActOS起動ではない。

## event lineage

```text
v0.23 ActOS handoff index
< v0.24 foresight index
< v0.24 blocker index
< v0.24 replan intake index
```

adapter historyにはforesight、blocker、replan intakeの3 recordを追加する。

## 所有権

```text
foresight gate owner = PlanOS
activation owner = ActOS
Qi process tensor owner = evidence surface
blocker owner = boundary context
execution owner = ActOS
```

## 非権限境界

```text
foresight gate != activation authorization
candidate weighting != execution permission
process reward != truth authority
verifier trace != external commit
blocker classification != blocker release
reroute != blocker bypass
replan signal != ActOS invocation
memory provenance != memory overwrite
```

## Lean定理

```text
source_handoff_remains_non_authoritative
requires_qi_process_tensor_foresight
requires_causal_reward_and_verifier_trace
requires_blocker_classification_without_release
requires_agent_theory_selection_binding
gate_filters_to_replan_without_authority
bridge_grants_no_execution_truth_memory_or_blocker_release
events_append_strictly
history_appends_three_records
digest_is_exact
```

## Honest classification

```text
an additive PlanOS-owned foresight gate over the v0.23 ActOS handoff receipt,
using Qi process tensor continuity, blocker classification, process reward,
agent memory, causal world-model and verifier traces to produce advisory
candidate weighting and replan-intake-only evidence, while granting no
activation, execution, external commit, memory overwrite, truth authority or
blocker-release authority
```
