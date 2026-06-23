# KuuOS MemoryOS Predictive Shielded Memory v0.37

## 位置づけ

v0.37 は、v0.35 の MemoryOS Qi-WORLD Blocker Integration と v0.36 の Validation Matrix の上に、AI理論に基づく予測記憶層を追加する。

本層は、記憶を保存するだけではなく、履歴を予測候補へ変換し、ブロッカーを通過した範囲だけを読み取り候補として返す。

実行権限、真理権限、blocker discharge、WORLD commit、memory overwrite は追加しない。

## 全体経路

```text
v0.35 Qi process history + blocker context + sourced WORLD
→ four-layer memory records
→ observable predictive-state candidate
→ contradiction residue preservation
→ counterfactual WORLD imagination candidates
→ blocker shield gate
→ read-only candidate retrieval or safe fallback
```

## 四層記憶

**Working memory** は、現在の推論で参照する短期候補である。

```text
status = WORKING_CONTEXT
retention route = PIN_WORKING_CONTEXT
```

**Episodic memory** は、source digest に結び付いた経験記録である。

```text
status = EPISODIC_SOURCE
retention route = APPEND_EPISODIC_SOURCE
```

**Semantic memory** は、複数 source から構成する統合候補である。

```text
status = SEMANTIC_CONSOLIDATION_CANDIDATE
retention route = PROPOSE_SEMANTIC_CONSOLIDATION
```

Semantic record は fact ではない。

**Procedural memory** は、過去の経路から抽出する再利用候補である。

```text
status = PROCEDURAL_REUSE_CANDIDATE
retention route = PROPOSE_PROCEDURAL_REUSE
```

Procedural record は execution authority ではない。

すべての record は次を持つ。

- record id
- memory type
- content digest
- source digests
- confidence milli
- uncertainty milli
- lifecycle status
- retention route
- non-authority flags

## Consolidation boundary

Semantic と procedural の record は consolidation candidate として保存する。

Runtime は automatic consolidation を行わない。

```text
automatic_consolidation_performed = false
semantic candidate != fact
procedural candidate != executable procedure
```

過去 record の削除、置換、同一 id での内容変更は append-only violation になる。

## Predictive state candidate

v0.37 は、履歴全体を hidden-state truth へ変換しない。

観測可能な履歴に結び付いた予測候補だけを作る。

```text
representation_kind = OBSERVABLE_PREDICTIVE_STATE_CANDIDATE
observable_history_digest
prediction_target
prediction_digest
uncertainty_milli
history_sufficient
latent_state_truth_claim = false
action_authority = false
```

履歴が不足している場合は次へ送る。

```text
REOBSERVE_PREDICTIVE_STATE
```

## Contradiction residue

異なる source から得られた competing claim を consolidation によって消さない。

Residue は次の status を持つ。

```text
OPEN
REOBSERVE
REVIEW
```

```text
resolved_by_consolidation = false
silent_collapse = false
```

`REVIEW` が含まれる場合は `REVIEW_CONTRADICTION_RESIDUE` へ送る。

その他の residue が存在する場合は `PRESERVE_RESIDUE_WITH_CONTEXT` へ送る。

## WORLD imagination candidates

WORLD imagination は sourced WORLD fragment に結び付く counterfactual candidate である。

```text
candidate id
source WORLD fragment digest
counterfactual digest
uncertainty milli
truth claim = false
commit authority = false
execution authority = false
replaces sourced WORLD = false
```

WORLD imagination は sourced WORLD を更新しない。

WORLD imagination は WORLD の真値ではない。

## Blocker shield gate

Retrieval は v0.35 の active blocker inventory を再利用する。

要求 capability が active blocker に対応する場合は、context は返せても capability は通さない。

```text
RETURN_CONTEXT_WITH_ACTIVE_SHIELD
```

Source blocker evidence が不完全な場合は次へ送る。

```text
QUARANTINE_RETRIEVAL
```

Predictive history が不足している場合は次へ送る。

```text
REOBSERVE_BEFORE_RETRIEVAL
```

Review residue がある場合は次へ送る。

```text
REVIEW_BEFORE_RETRIEVAL
```

安全な fallback は次に限定する。

```text
READ_ONLY_CONTEXT_OR_REOBSERVE
```

Fallback は blocker discharge や task success を意味しない。

## Capsule route

```text
QUARANTINE_SOURCE_BLOCKER_EVIDENCE
REOBSERVE_PREDICTIVE_STATE
REVIEW_CONTRADICTION_RESIDUE
PRESERVE_RESIDUE_WITH_CONTEXT
READY_FOR_SHIELDED_RETRIEVAL
```

Route は priority 順に決まる。

```text
incomplete blocker evidence
→ insufficient predictive history
→ review residue
→ open residue
→ shielded retrieval ready
```

## Retrieval route

```text
QUARANTINE_RETRIEVAL
RETURN_CONTEXT_WITH_ACTIVE_SHIELD
REOBSERVE_BEFORE_RETRIEVAL
REVIEW_BEFORE_RETRIEVAL
RETURN_CONTEXT_WITH_RESIDUE
RETURN_PREDICTIVE_CONTEXT_CANDIDATE
```

Retrieval result は候補文脈だけである。

```text
candidate_context_only = true
safe_fallback_available = true
automatic_consolidation = false
automatic_blocker_discharge = false
automatic_world_commit = false
automatic_plan_activation = false
automatic_execution = false
truth_claim = false
```

## Append-only lineage

Capsule は前 capsule digest と source snapshot sequence を保持する。

次を拒否する。

- mission change
- lineage change
- source snapshot sequence regression
- 同一 source sequence での snapshot digest 置換
- memory record removal or replacement
- WORLD imagination candidate removal or replacement
- contradiction residue removal or replacement

Predictive state candidate は新しい capsule で更新できる。

過去 predictive state は `previous_predictive_state_digest` で残る。

## Non-authority boundary

```text
memory record != truth
semantic consolidation != verification
procedural reuse != execution
predictive state != latent-state truth
reflection != authority
blocker shield != blocker discharge
safe fallback != success
WORLD imagination != sourced WORLD
WORLD imagination != WORLD commit
retrieval != plan activation
retrieval != ActOS invocation
```

## 実装ファイル

```text
runtime/kuuos_memoryos_predictive_shielded_memory_v0_37.py
tests/test_memoryos_predictive_shielded_memory_v0_37.py
scripts/check_memoryos_predictive_shielded_memory_v0_37.py
manifests/kuuos_memoryos_predictive_shielded_memory_v0_37.json
formal/KUOS/OpenHorizon/MemoryOSPredictiveShieldedMemoryKernelV0_37.lean
docs/research/MEMORYOS_QI_BLOCKER_AI_THEORY_RESEARCH_v0_37.md
.github/workflows/memoryos-predictive-shielded-memory-v0-37.yml
```

## Validation

```bash
PYTHONPATH=. python scripts/check_memoryos_predictive_shielded_memory_v0_37.py

PYTHONPATH=. python -m unittest -v \
  tests.test_memoryos_predictive_shielded_memory_v0_37

lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KUOS.OpenHorizon.MemoryOSPredictiveShieldedMemoryKernelV0_37

lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KuuOSFormal
```

## Honest classification

```text
theory-grounded, append-only, predictive, blocker-shielded MemoryOS layer
that preserves process history and contradiction residue,
separates memory classes,
returns read-only candidates,
and grants no truth or execution authority
```
