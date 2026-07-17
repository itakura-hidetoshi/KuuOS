# KuuOS / 空OS Roadmap

**基準日：2026年7月17日 JST**

このRoadmapは、`main`へ統合済みの状態、canonical current root、完了系列、継続検証面、条件付き次段階を分離します。

subsystem versionは独立しています。ObserveOS v0.7、PlanOS v1.23、DecisionOS v0.6、MemoryOS v1.00、self-organization v0.113を、一つの連続version番号として扱いません。

## 状態分類

| 表記 | 意味 |
|---|---|
| 統合済み | `main`に存在し、対応するruntime、formal、manifest、documentationのいずれかを持つ |
| Current root | `runtime/kuuos_current_check.py`から直接または累積的に検証される面 |
| 専用CI | subsystem固有workflowでruntime、manifest、formal rootを検証する面 |
| 継続検証 | 統合済みだが、依存またはaggregate変更時に再検証する面 |
| 完了系列 | 定義した終端へ到達し、後続権限を自動生成しない系列 |
| 条件付き候補 | 独立PRとして設計可能だが、version、scope、authorityが未確定の候補 |
| Frozen boundary | additiveまたはtighten-onlyで維持する境界 |

## 現在の統合済み基準

最新の機能統合はPR #1279、ObserveOS v0.7 Sequential Epistemic Observability Envelopeです。機能frontierの基準commitは`b68f6ee5c16b3670806613226034bc4b899abac5`です。

| 系列 | 到達点 | 状態 |
|---|---|---|
| Core governance | v0.1 | Frozen boundary |
| Horizon / Context Gauge | v0.12 / v0.13 | 統合済み、継続検証 |
| Finite-cycle agent | v0.20-v0.27 | 統合済み |
| Qi diagnostic lineage | v0.28 / v0.29 | 統合済み |
| Qi-WORLD | v2.3 | 統合済み |
| Causal WORLD model | v14.0 | PlanOS active lineのread-only source |
| Repository mutation | v1.24 | 完了系列 |
| Apoptosis Lifecycle Governance | v0.1-v0.36 | 独立完了系列 |
| Repository self-organization root lineage | v0.113 | 統合済み、Current root |
| ObserveOS | v0.7 sequential epistemic observability envelope | 統合済み、専用CI、継続検証 |
| PlanOS bounded cycle line | v0.1-v0.90 | 統合済み、継続検証 |
| PlanOS active mathematical line | v0.91-v1.23 | 統合済み、Current root |
| DecisionOS | v0.1-v0.6 | 統合済み、Current root |
| MemoryOS active line | v0.40-v1.00 | 統合済み、Current root |
| Repository strict Lean baseline | `formal/KuuOSFormal.lean` | 継続検証 |
| ObserveOS v0.7 aggregate | `formal/KuuOSObserveOSV0_7.lean` | 統合済み、専用CI |
| PlanOS v1.23 aggregate | `formal/KuuOSPlanOSV1_23.lean` | 統合済み |
| DecisionOS v0.6 aggregate | `formal/KuuOSDecisionOSV0_6.lean` | 統合済み |
| MemoryOS v1.00 aggregate | `formal/KuuOSMemoryOSV1_00.lean` | 統合済み |

## Canonical current root

標準入口は次です。

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py
```

現在のrootは四面を束ねます。

```text
repository lineage through self-organization v0.113
→ PlanOS active frontier v0.91-v1.23
→ DecisionOS cumulative line v0.1-v0.6
→ MemoryOS active frontier v0.40-v1.00
```

ObserveOS v0.7はこのprofile rootへ暗黙に追加せず、専用workflowとversioned formal aggregateで独立検証します。

個別面は次のprofileで実行します。

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile repository
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile planos
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile decisionos
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile memoryos
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile all
```

rootはrun-all-then-decideです。一つのstepが失敗しても残りを実行し、必要stepの失敗を最後に集約します。

step数とexact frontierは文書へ固定せず、runtime summaryをsource of truthとします。

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py --summary
PYTHONPATH=. python3 runtime/kuuos_current_check.py --list
```

## ObserveOS v0.7 sequential epistemic observability

ObserveOS v0.7は、既存のbounded observation receiptに対し、観測過程のtraceability、provenance、sample accounting、missingness、distribution shift、逐次不確実性、conformal calibrationをsource-bound envelopeとして追加します。

```text
ObserveOS v0.6 bounded maintenance-monitoring observation receipt
→ ObserveOS v0.7 sequential epistemic observability envelope
→ VerifyOS independent observation verification
```

統合済みsurfaceは次です。

- W3C Trace Context version-00構文とtrace/span identity
- OpenTelemetry signal coverage
- W3C PROV-O Entity / Activity / Agent / relation provenance
- exact observed / missing / total sample partition
- missingness budgetとobservation window
- ADWIN distribution-shift evidence
- confidence sequence / e-process evidence
- split / online conformal calibration evidence
- replay closure、current-state effect negative、authority escalation negative
- supported、repair、review、rejectionを分ける14 disposition

```text
observation != verification
WORLD intake != WORLD update
WORLD sidecar != exact WORLD
receipt composition != receipt construction
learning != present-cycle mutation
```

主な入口は次です。

| Surface | Path |
|---|---|
| Structured index | `docs/ObserveOS/README.md` |
| Specification | `docs/OBSERVEOS_SEQUENTIAL_EPISTEMIC_OBSERVABILITY_ENVELOPE_v0_1.md` |
| Runtime envelope | `runtime/kuuos_observeos_sequential_epistemic_observability_envelope_v0_1.py` |
| Checker | `scripts/check_observeos_sequential_epistemic_observability_envelope_v0_1.py` |
| Formal kernel | `formal/KUOS/ObserveOS/SequentialEpistemicObservabilityEnvelopeV0_7.lean` |
| Formal aggregate | `formal/KuuOSObserveOSV0_7.lean` |
| Workflow | `.github/workflows/observeos-sequential-epistemic-observability-v0-1.yml` |

### ObserveOS継続検証条件

次の変更時には専用CIとrepository formal baselineを再検証します。

- traceparent / tracestate validation contractの変更
- OpenTelemetry required signal setの変更
- provenance canonicalizationまたはdigest bindingの変更
- sample partition、missingness budget、window policyの変更
- confidence sequence、e-process、conformal、ADWIN evidence schemaの変更
- replay、current-effect、authority-negative predicateの変更
- ObserveOSとVerifyOS、WORLD、LearnOSの責務境界の変更

VerifyOSによる独立再現、因果検証、経験的真理判定をObserveOS CI成功から推論しません。

## PlanOS current frontier

### v0.91-v1.02 — information geometry and WORLD-conditioned decision handoff

```text
v0.91 information-geometric Qi objective
→ v0.92 KL-regularized distribution update
→ v0.93 zero-temperature minimal-action support
→ v0.94 finite-temperature concentration
→ v0.95 adaptive Qi temperature
→ v0.96 hysteresis and asymmetric rate limit
→ v0.97 temperature trajectory receipt
→ v0.98 finite-window stability
→ v0.99 Qi- and history-conditioned metric
→ v1.00 WORLD-conditioned pullback metric
→ v1.01 WORLD-conditioned distribution update
→ v1.02 DecisionOS advisory handoff
```

この系列はfuture-only candidate distributionを構成します。probability rankingはadvisoryであり、selectionまたはexecution authorityではありません。

### v1.05-v1.20 — finite geometry, topology, persistence, and transport

この系列は、native coupled metric、state-dependent jets、curvature、Jacobi/geodesic structure、finite normal-ball cover、nerve and Cech structure、simplicial and integer homology、persistent homology、bottleneck/Wasserstein transport、finite Frechet barycenterへ進みます。

各packageは有限fixtureとexact receiptへ限定されます。一般的な多様体、無限複体、連続測度空間、外部経験世界についての包括定理とは同一ではありません。

### v1.21-v1.23 — finite Physical Quantum Qi path histories

```text
v1.21 complete finite path-history ensemble and noncollapse
→ v1.22 exact Z4 phase、Gaussian amplitudes、homotopy-block endpoint cases
→ v1.23 Hermitian coherence kernel and exact rational partial dephasing
```

v1.23は全historyを保持したまま、coherent endpoint kernelからhomotopy-block kernelまでの有限trajectoryを検証します。

```text
partial dephasing != history deletion
coherence != utility
mixedness != preference
readout intensity != selection authority
```

### PlanOS継続検証条件

次の変更時には関連するactive lineを再検証します。

- candidate、history、homotopy、coherence-block schemaの変更
- Qi process tensor、temperature、metric、action formulaの変更
- WORLD state revisionまたはlineage bindingの変更
- exact Gaussianまたはrational arithmetic表現の変更
- entropy、purity、mixedness、lead margin、hold guardの意味変更
- history supportを減らす操作の導入

## DecisionOS v0.1-v0.6

現在の到達点はWORLD-conditioned relational deliberationです。

```text
admissible candidate surface
→ PlanOS evidence intake validation
→ candidate evidence bundle
→ six-dimensional relational profile
→ non-dominated relational frontier
```

六次元profileは、Wa support、stakeholder support、relational support、dissent pressure、minority-impact risk、uncertainty burdenを分離して保持します。

Pareto型frontierはselection resultではありません。PlanOS rankingだけによる選択、dissentの消去、minority-impact riskのscalar utilityへの吸収を認めません。

## MemoryOS v0.40-v1.00

MemoryOS active lineは、observer-relative non-Markov recordから、有限なclosed-support / representable-kernel fixed-point latticeまでを累積的に検証します。

### v0.40-v0.90 — observer-relative lineage and finite representation

この区間は、append-only temporal record、finite-window influence、coherence and transport structure、confidence/revocation/gauge lineage、finite sensor consequence、closure、closed-context truth-region representationを段階的に追加します。

MemoryOSはhistory sourceであり、belief sovereignty、candidate ranking、selection、activation、executionを取得しません。

### v0.91-v0.95 — counterexamples, generators, and choice-free signatures

```text
v0.91 canonical counterexample-guided refinement
→ v0.92 finite batch saturation
→ v0.93 minimal-generator closure quotient
→ v0.94 complete choice-free generator antichain signature
→ v0.95 exact signature hull and kernel-order duality
```

この系列は代表generatorを一つ選ばず、完全な有限antichainを保持します。

### v0.96-v1.00 — fixed-point lattice completion

```text
v0.96 pointed choice-free closed-context lattice
→ v0.97 finite-family meet and join
→ v0.98 sensor-kernel polarity and fixed-point duality
→ v0.99 typed closed-support / representable-kernel order anti-isomorphism
→ v1.00 finite bounded closed-support lattice
```

v1.00は次をLean上で実装します。

```lean
Lattice ClosedSensorSupport
BoundedOrder ClosedSensorSupport
Fintype ClosedSensorSupport
Fintype RepresentableSensorKernel
```

exact operationは次です。

```text
C ⊔ D = closure(C ∪ D)
C ⊓ D = C ∩ D
⊤ = full sensor support
⊥ = closure(∅)

K(finiteJoin F) = inf {K(C) | C ∈ F}
K(finiteMeet F) = Env(sup {K(C) | C ∈ F})
```

v1.00は`CompleteLattice`、任意・無限indexed operations、distributivity、modularity、全ambient subgroupのrepresentability、unique support representation、canonical minimum supportを主張しません。

## 現在の整備項目

### Public surface synchronization

README、ROADMAP、structured ObserveOS indexを、self-organization v0.113、ObserveOS v0.7、PlanOS v1.23、DecisionOS v0.6、MemoryOS v1.00へ同期します。

公開文書は単一の古いDraft frontierをcurrent statusとして固定せず、runtime summaryとversioned aggregatesを参照します。

### Formal aggregate convergence

`formal/KuuOSFormal.lean`はrepository strict baselineとして維持します。

最新subsystem aggregateは独立して存在します。repository-wide aggregateへ接続する場合は、build時間、import cycle、warning-as-error、sorry-as-errorを個別に確認します。

versioned aggregateの存在をrepository-wide aggregate統合と誤記しません。

### Compatibility status surface

`runtime/kuuos_current_surface.py`と`status/current.*`は互換surfaceとして保持します。

更新する場合はcanonical runtime summaryから導出し、手書きの単一frontierへ戻しません。

### Legacy PR disposition

古いopen PRは、作成時点のbaseを現在のfrontierとみなしません。

再利用する場合は現在の`main`へrebaseし、scopeを再評価し、canonical current rootとgovernance gateを再実行します。置換済みDraftやCI-only branchは、履歴保存の要否を確認した上でclose候補とします。

## 条件付き次段階

次のversion番号やtheorem unitは、このRoadmapだけでは自動確定しません。各候補は独立branch、exact base SHA、明示的scope、fail-closed checker、formal target、governance gateを必要とします。

### ObserveOS independent verification handoff

ObserveOS v0.7 envelopeをVerifyOSへ渡す次段階では、観測品質evidenceと観測内容の独立検証を別receiptとして保持します。

- ObserveOS envelope digestとVerifyOS intake digestのexact binding
- confidence sequence、conformal、ADWIN artifactの独立再計算可否
- missingnessとdistribution shiftがverification scopeへ与える影響
- verification completed / debt stateの単調な遷移
- observation ownerとverification ownerの分離
- verification resultとtruth authorityの分離

この候補だけでObserveOS v0.8またはVerifyOS次versionを自動確定しません。

### MemoryOS lattice-law characterization

v1.00の有限bounded latticeについて、次の性質を調べる候補があります。

- distributivityまたはその反例
- modularityまたはその反例
- semidistributive lawまたは有限fixture上の限定条件
- support closureとkernel envelopeが追加のlattice homomorphism lawを満たす条件

成立を仮定してversionを進めません。一般lawが不成立なら、最小反例をexact artifactとして保持します。

### MemoryOS arbitrary-family boundary

`CompleteLattice`へ進むには、任意indexed family、supremum/infimumの存在、fixed-point closure、kernel transportを別々に構成する必要があります。

有限`Fintype`から無限operationを推論しません。有限enumerationを一般集合上のcomplete lattice claimへ昇格させません。

### MemoryOS representation and basis line

choice-free complete antichainとfinite bounded latticeは、canonical minimum supportまたはglobally minimum implication basisを与えません。

minimum-cardinality support、canonical basis、direct basis、query complexityを扱う場合は、現在のfixed-point latticeとは別artifactにし、存在、非一意性、計算量、selection boundaryを分離します。

### Read-only cross-OS integration

MemoryOS v1.00のclosed-supportまたはrepresentable-kernel receiptをPlanOSやDecisionOSへ渡す場合は、read-only evidence intakeとして設計します。

```text
MemoryOS order != PlanOS preference
MemoryOS kernel inclusion != DecisionOS dominance
MemoryOS closure != WORLD truth
MemoryOS receipt != activation authority
```

source provenance、observer、route root、target defect、expiry、confidence、non-authorityを明示的に束縛します。

### DecisionOS bounded selection

v0.6 relational frontierからbounded selectionへ進む場合は、少なくとも次を必要とします。

- selected candidateはrelational frontierに含まれる
- dissent review対象を消去しない
- minority-impact riskをscalar utilityへ吸収しない
- uncertainty blockerを明示する
- PlanOS rankingだけで選択しない
- selection authorityの由来を独立artifactへ束縛する
- selectionとexecutionを分離する

### PlanOS feedback and replan

DecisionOS selection receiptが成立した後にだけ、selected candidateをPlanOSへ返すbounded feedback intakeを設計できます。

feedbackは過去のdistributionまたはhistoryを上書きせず、新しいfuture-only replan stateを生成します。

### WORLD update separation

現在のWORLD利用はsource bindingまたはread-only counterfactual projectionです。

persistent WORLD mutationを実装する場合は、独立したauthorization、application、verification、rollback系列を必要とします。PlanOS、DecisionOS、MemoryOSのreceiptからWORLD write authorityを継承しません。

### ActOS handoff separation

DecisionOS selectionが成立しても、ActOS invocationとは同一ではありません。

execution scope、constraints、owner、expiry、verification routeを持つ独立handoffを必要とします。

## Governance Gate

公開面とruntime rootの同期では、少なくとも次を確認します。

```bash
python3 -m py_compile runtime/kuuos_current_check.py
PYTHONPATH=. python3 runtime/kuuos_current_check.py --summary
PYTHONPATH=. python3 runtime/kuuos_current_check.py --list
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile repository
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile planos
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile decisionos
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile memoryos
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile all
PYTHONPATH=. python3 scripts/check_observeos_sequential_epistemic_observability_envelope_v0_1.py
```

ObserveOSまたはLean surfaceを変更した場合は、対象versioned aggregateとrepository strict baselineを別々にbuildします。

```bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSObserveOSV0_7
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
```

Gate成功は登録surfaceの整合性receiptです。外部定理受理、経験的真理、臨床承認、組織承認、無制限repository mutation権限ではありません。

## 固定境界

```text
candidate != authority
validation != truth
CI pass != external theorem acceptance

observation != verification
memory != belief sovereignty
closure != empirical truth
lattice order != ranking
relational frontier != selected candidate
selection != execution
receipt != successor authority

WORLD candidate != empirical fact
WORLD intake != WORLD update
WORLD sidecar != exact WORLD
WORLD commit != truth
WORLD projection != persistent WORLD mutation
receipt composition != receipt construction
learning != present-cycle mutation
Qi conditioning != authority grant
history conditioning != history sovereignty
partial dephasing != history deletion
modular time != physical time

modeled repository transition != live Git mutation
roadmap completion != successor mutation authority
runtime success != production deployment
```
