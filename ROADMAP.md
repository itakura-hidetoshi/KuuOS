# KuuOS / 空OS Roadmap

**基準日：2026年7月11日 JST**

このRoadmapは、`main`へ統合済みの状態、継続検証面、現在の整備項目、条件付き次段階を分離します。

subsystem versionは独立しています。

PlanOS v1.02、DecisionOS v0.6、self-organization v0.113を、一つの直線的version番号として扱いません。

## 状態分類

| 表記 | 意味 |
|---|---|
| 統合済み | `main`に存在し、対応するruntimeまたはformal surfaceを持つ |
| Current root | `runtime/kuuos_current_check.py`から実行される現在の検査面 |
| 継続検証 | 統合済みだが、依存更新時に再検証する面 |
| 完了系列 | 定義した終端へ到達し、後続権限を自動生成しない系列 |
| 整備中 | 既存機能の公開面、aggregate、root接続を同期する作業 |
| 次期候補 | 独立したPRとして設計できるが、未承認の候補 |
| Frozen boundary | additiveまたはtighten-onlyで維持する境界 |

## 現在の統合済み基準

| 系列 | 到達点 | 状態 |
|---|---|---|
| Core governance | v0.1 | Frozen boundary |
| Horizon / Context Gauge | v0.12 / v0.13 | 統合済み、継続検証 |
| Finite-cycle agent | v0.20-v0.27 | 統合済み |
| Qi diagnostic lineage | v0.28 / v0.29 | 統合済み |
| MemoryOS foundational line | v0.35、v0.37-v0.39 | 統合済み |
| Qi-WORLD | v2.3 | 統合済み |
| Causal WORLD model | v14.0 | PlanOS v1.00-v1.02のread-only source |
| Repository mutation | v1.24 | 完了系列 |
| Apoptosis Lifecycle Governance | v0.1-v0.36 | 独立完了系列 |
| Repository self-organization root lineage | v0.113 | 統合済み、Current root |
| PlanOS bounded cycle line | v0.1-v0.90 | 統合済み、継続検証 |
| PlanOS information-geometric line | v0.91-v1.02 | 統合済み、Current root |
| DecisionOS | v0.1-v0.6 | 統合済み、Current root |
| Repository strict Lean baseline | `formal/KuuOSFormal.lean` | 継続検証 |
| PlanOS v1.02 aggregate | `formal/KuuOS/PlanOSV102.lean` | 統合済み |
| DecisionOS v0.6 aggregate | `formal/KuuOSDecisionOSV0_6.lean` | 統合済み |

直近の機能統合はPR #1160です。

PR #1160により、DecisionOSはWORLD-conditioned evidence intakeから関係的部分順序によるdeliberationへ進みました。

## Current root

標準入口は次です。

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py
```

現在のroot profileは次の三面を束ねます。

```text
repository lineage through self-organization v0.113
→ PlanOS information-geometric and WORLD-conditioned line v0.91-v1.02
→ DecisionOS cumulative line v0.1-v0.6
```

個別面は次のように実行します。

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile repository
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile planos
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile decisionos
```

現在のrootはrun-all-then-decideです。

一つのstepが失敗しても残りを実行し、必要stepの失敗を最後に集約します。

## PlanOS v0.91-v1.02

### 完了した数理系列

```text
v0.91 information-geometric Qi objective
→ v0.92 KL-regularized distribution update
→ v0.93 zero-temperature minimal-action limit
→ v0.94 finite-temperature concentration certificate
→ v0.95 adaptive Qi temperature calibration
→ v0.96 hysteresis and rate limit
→ v0.97 temperature trajectory receipt
→ v0.98 trajectory stability certificate
→ v0.99 Qi- and history-conditioned information metric
→ v1.00 WORLD-conditioned pullback metric
→ v1.01 WORLD-conditioned distribution update
→ v1.02 DecisionOS handoff certificate
```

この系列は、有限候補上の分布、作用、温度、情報計量、WORLD pullback、decision evidenceを接続しました。

候補分布はfuture-onlyです。

PlanOSは候補を選択せず、ActOS execution permissionを生成しません。

### 継続検証条件

次の変更時にはv0.91-v1.02を再検証します。

- candidate fieldまたはadmissibility schemaの変更
- Qi process tensor schemaの変更
- WORLD state revisionまたはlineage bindingの変更
- information metricまたはaction formulaの変更
- entropy、lead margin、hold guardの意味変更

## DecisionOS v0.1-v0.6

現在の到達点はWORLD-conditioned relational deliberationです。

```text
admissible candidate selection surface
→ PlanOS v1.02 handoff intake validation
→ candidate evidence bundle
→ six-dimensional relational profile
→ non-dominated relational frontier
```

関係的profileは次を分離して保持します。

- Wa support
- stakeholder support
- relational support
- dissent pressure
- minority-impact risk
- uncertainty burden

確率順位と作用順位はadvisoryです。

Pareto型frontierはselection resultではありません。

## 現在の整備項目

### Public surface synchronization

README、ROADMAP、runtime rootを同じ統合済み状態へ揃えます。

旧self-organization Draftの番号をpublic current statusとして固定しません。

status compatibility surfaceとcanonical execution surfaceを区別します。

### Formal aggregate convergence

`formal/KuuOSFormal.lean`はrepository strict baselineとして維持します。

最新のPlanOS v1.02とDecisionOS v0.6はversioned aggregateに存在します。

repository-wide aggregateへ接続する場合は、既存targetのbuild時間、import cycle、warning-as-error、sorry-as-errorを独立に確認します。

versioned aggregateの存在をrepository-wide aggregate統合と誤記しません。

### Current status surface refresh

`runtime/kuuos_current_surface.py`と`status/current.*`は互換surfaceとして残っています。

これらを更新する場合は、runtime root summaryから導出し、手書きの単一Draft frontierへ戻しません。

### Legacy PR disposition

古いopen PRは、作成時点のbaseを現在のfrontierとみなしません。

再利用する場合は、現在の`main`へrebaseし、scopeを再評価し、current rootを再実行します。

不要なCI-only branchや置換済みDraftは、履歴保存の要否を確認してclose候補とします。

## 条件付き次段階

### DecisionOS bounded selection layer

次の実装候補は、v0.6 relational frontierを入力とするbounded selection requestまたはselection receiptです。

実装条件は次です。

- selected candidateはrelational frontierに含まれる
- dissent review対象を消去しない
- minority-impact riskをscalar utilityへ吸収しない
- uncertainty blockerを明示する
- PlanOS probability rankingだけで選択しない
- selection authorityの由来を独立artifactへ束縛する
- selectionとexecutionを分離する

この候補は未承認です。

### PlanOS feedback and replan

DecisionOS receiptが成立した後にだけ、selected candidateをPlanOSへ返すbounded feedback intakeを設計できます。

feedback intakeは、過去分布を書き換えず、新しいfuture-only replan stateを生成します。

### WORLD update separation

PlanOS v1.00-v1.02のWORLD projectionはread-only counterfactualです。

persistent WORLD mutationを実装する場合は、別のauthorization、application、verification、rollback系列を必要とします。

PlanOS handoffやDecisionOS deliberationからWORLD write authorityを継承しません。

### ActOS handoff separation

DecisionOS selectionが成立しても、ActOS invocationとは同一ではありません。

execution scope、constraints、owner、expiry、verification routeを持つ独立handoffを必要とします。

## Governance Gate

文書とruntime rootの同期では、少なくとも次を確認します。

```bash
python3 -m py_compile runtime/kuuos_current_check.py
PYTHONPATH=. python3 runtime/kuuos_current_check.py --summary
PYTHONPATH=. python3 runtime/kuuos_current_check.py --list
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile planos
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile decisionos
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile repository
```

Lean surfaceを変更した場合は、対象versioned aggregateとrepository strict baselineを別々にbuildします。

Gate成功は、登録surfaceの整合性receiptです。

外部定理受理、経験的真理、臨床承認、組織承認、無制限repository mutation権限ではありません。

## 固定境界

```text
candidate != authority
validation != truth
CI pass != external theorem acceptance

observation != verification
verification != truth
learning != present-cycle mutation
memory != belief sovereignty
selection != execution
relational deliberation != selected candidate
relational frontier != execution permission
receipt != successor authority
OS receipt composition

WORLD sidecar != exact WORLD
WORLD projection != WORLD mutation
WORLD candidate != empirical fact
WORLD commit != truth
Qi conditioning != authority grant
history conditioning != history sovereignty

modeled repository transition != live Git mutation
local checkpoint != remote push authority
roadmap completion != successor mutation authority
runtime success != production deployment
```
