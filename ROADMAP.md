# KuuOS / 空OS Roadmap

**基準日：2026年7月23日 JST**

このRoadmapは、`main`へ統合済みの事実、canonical runtime root、進行中Draft、条件付き次段階を分離します。未merge branch、queuedまたはin-progress CI、将来構想をcurrent frontierへ混ぜません。

## 状態分類

| 表記 | 意味 |
|---|---|
| 統合済み | authoritative `main`に存在する |
| Current root | `runtime/kuuos_current_check.py`のprofileから検証される |
| 専用CI | subsystem固有workflowでruntime、manifest、tests、formal rootを検証する |
| 継続検証 | 依存、aggregate、toolchain、authority boundary変更時に再検証する |
| Draft | open Draft PR。`main`の事実ではない |
| 条件付き候補 | exact base、scope、authority、evidence contractが未確定 |
| Frozen boundary | additiveまたはtighten-onlyで維持する責任境界 |

## 現在のauthoritative baseline

```text
branch: main
HEAD: 083ee7ef65d53bd1a8e231c73b82e4946dd1eaf7
latest integrated functional PR: #1341
frontier: Baseline-versus-CodeAI and Ablation Comparison v0.1
```

| 系列 | 到達点 | 状態 |
|---|---|---|
| Core governance | v0.1 | Frozen boundary |
| Horizon / Context Gauge | v0.12 / v0.13 | 統合済み、継続検証 |
| Finite-cycle agent | v0.20-v0.27 | 統合済み |
| Qi diagnostic lineage | v0.28 / v0.29 | 統合済み |
| Qi-WORLD | v2.3 | 統合済み |
| Causal WORLD model | v14.0 | read-only dependency |
| Repository mutation | v1.24 | 完了系列 |
| Apoptosis Lifecycle Governance | v0.1-v0.36 | 独立完了系列 |
| Repository self-organization root | v0.113 | 統合済み、Current root |
| ObserveOS | v0.7 | 統合済み、専用CI |
| VerifyOS | v0.13-v0.15 | 統合済み、専用CI |
| PlanOS | v0.91-v1.23 | 統合済み、Current root |
| DecisionOS | v0.1-v0.6 | 統合済み、Current root |
| MemoryOS | v0.40-v1.00 | 統合済み、Current root |
| CodeAI governed repository-evolution line | observationからbounded Git lifecycle、external dependency boundaryまで | 統合済み、専用CI |
| CodeAI external benchmark line | protocol、corpus freeze、gold smoke、bounded execution、aggregate ingestion、comparison preregistration | 統合済み、Current root |
| Repository strict Lean baseline | `formal/KuuOSFormal.lean` | 継続検証 |

subsystem versionは独立しています。異なる系列のversion番号を一つの成熟度尺度へ変換しません。

## Canonical runtime root

標準入口:

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py
```

現在のprofile:

```text
repository
→ PlanOS
→ DecisionOS
→ MemoryOS
→ CodeAI external benchmark comparison frontier
```

個別実行:

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py --summary
PYTHONPATH=. python3 runtime/kuuos_current_check.py --list
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile repository
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile planos
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile decisionos
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile memoryos
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile codeai
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile all
```

`codeai` profileは、PR #1341のdeterministic comparison projection、focused tests、直接predecessor regressionsを検査します。外部Docker harnessを再実行せず、過去の外部artifactを再取得せず、gold materialをruntime rootへ持ち込みません。

ObserveOSとVerifyOSはこのprofile rootへ暗黙追加せず、専用workflow、Evidence Cycle累積runner、versioned formal aggregateで検証します。

## CodeAI external evaluation track

### 統合済み

| PR | Stage | 到達した事実 |
|---|---|---|
| #1335 | External General Benchmark Protocol and SWE-bench Verified Adapter v0.1 | exact protocolとofficial prediction shapeを固定 |
| #1337 | External Corpus Acquisition and Freeze Receipt v0.1 normalization | 500-row pinned corpus artifact、schema、solver/evaluator field isolationを固定 |
| #1338 | Gold-Patch Environment Smoke Validation v0.1 | evaluator-only gold runでpinned Docker/harness environmentを確認 |
| #1339 | Bounded Official Harness Execution v0.1 | 1件のnon-gold predictionをofficial harnessで実行 |
| #1340 | External Result and Process-Evidence Ingestion v0.1 | raw materialをrepositoryへ残さずaggregate evidenceをingest |
| #1341 | Baseline-versus-CodeAI and Ablation Comparison v0.1 | 5 cohort、共通holdout、metric、missing/failure handlingをpreregister |

現時点の観測:

```text
sample count: 1
execution valid: true
resolved: false
FAIL_TO_PASS: 0 / 1
PASS_TO_PASS: 21 / 0
performance comparison completed: false
performance claimed: false
```

### 進行中Draft

PR #1342 **CodeAI Frozen Cohort Prediction-Pack and Execution-Shard Contract v0.1**

```text
base: 083ee7ef65d53bd1a8e231c73b82e4946dd1eaf7
head: daa88b75be2cdb66ce706fcf08be8723a34594e7
state: open Draft
```

このDraftは、100-slot shared holdout、baseline / CodeAI / 3 ablationのauthentic prediction pack、各cohort 10 shard、合計50 external-only shardを固定する契約です。

Draft時点では次を完了事実として扱いません。

```text
external dataset materialized
authentic prediction packs complete
execution shards ready
external execution ready
performance comparison completed
performance claimed
```

## 優先順位

### 1. #1342のcontractを完成させる

- exact baseとpredecessor digest bindingを維持する
- smoke predictionをperformance evidenceへ昇格させない
- cohort、sample、holdout、metricのcross-bindingを防ぐ
- raw gold、raw test names、raw logsをsolver側へ渡さない
- CI、strict Lean、base整合、mergeability、review、unresolved threadをcompleted evidenceで確認する
- merge前後にauthoritative `main`とのidentical relationを確認する

### 2. Frozen cohortを実体化する

#1342が統合された場合に限り、別stageで次を行います。

- pinned external corpusからshared holdoutをmaterializeする
- 5 cohortそれぞれのauthentic prediction packを生成する
- prediction source、model/configuration、pipeline variant、candidate digestをexact bindingする
- prediction欠測、重複、cross-cohort reuse、gold leakageをHOLDまたはBLOCKする
- generationとevaluation authorityを分離する

### 3. External-only shard execution

- official pinned harnessとDocker imageを使う
- shard単位のtimeout、worker、retry、artifact retentionを固定する
- kernelはharnessを実行せず、外部実行evidenceだけを受理する
- execution failureをsilent exclusionせず、preregistered ruleでunresolvedまたはerrorへ数える
- raw resultは短期検証に限定し、repositoryへはaggregate receiptだけを残す

### 4. Aggregate ingestionとbalanced comparison

- 全cohortのsample countとholdout bindingを一致させる
- resolved-rateをprimary metricとして計算する
- FAIL_TO_PASS、PASS_TO_PASS、execution-valid-rate、error-rateをguardrailとして保持する
- 欠測、leakage、cohort imbalance、metric欠落では比較をHOLDする
- point estimateだけでなくuncertaintyとfailure distributionを報告する
- performance claimをcomparison completionと独立に承認する

### 5. Temporally fresh external validity

同一frozen holdout上の比較だけで一般化を主張しません。比較完了後も、別時点または別repository familyのfresh holdoutで再評価し、dataset revision、environment、toolchain、provider、model、policy driftを明示します。

## 他系列の条件付き次段階

### ObserveOS / VerifyOS / WORLD

VerifyOS v0.15はread-only disposition candidateまでです。adopt、reject、defer、reobservationを正式なWORLD dispositionへ進める場合は、VerifyOSから独立したWORLD-owned review、authorization、application、verification、rollback artifactを必要とします。

```text
disposition candidate != WORLD disposition
authorization != WORLD mutation
reobservation candidate != observation execution
```

### MemoryOS

v1.00 finite bounded closed-support latticeについて、distributivity、modularity、semidistributivity、homomorphism lawを個別に調べます。有限`Fintype`から`CompleteLattice`を推論せず、一般lawが不成立なら最小反例をartifactとして保持します。

### DecisionOS / PlanOS

DecisionOS v0.6からbounded selectionへ進む場合は、relational frontier membership、dissent preservation、minority-impact risk、uncertainty blocker、独立selection authorityを必要とします。selection成立後に限り、PlanOSへfuture-only replan intakeを設計します。

```text
relational frontier != selected candidate
selection != execution
feedback != past-state rewrite
```

### Persistent WORLD update / ActOS

persistent WORLD mutationとActOS invocationは、既存receiptから権限継承せず、独立authorization、scope、owner、expiry、verification、rollbackを必要とします。

## Governance Gate

公開面とruntime rootの同期では、少なくとも次を確認します。

```bash
python3 -m py_compile runtime/kuuos_current_check.py
PYTHONPATH=. python3 runtime/kuuos_current_check.py --summary
PYTHONPATH=. python3 runtime/kuuos_current_check.py --list
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile codeai

PYTHONPATH=. python3 scripts/check_codeai_baseline_versus_codeai_ablation_comparison_v0_1.py
PYTHONPATH=. python3 -m unittest \
  tests.test_kuuos_codeai_baseline_versus_codeai_ablation_comparison_v0_1 \
  tests.test_kuuos_codeai_external_result_process_evidence_ingestion_v0_1 \
  tests.test_kuuos_codeai_bounded_official_harness_execution_v0_1 \
  tests.test_kuuos_codeai_gold_patch_environment_smoke_validation_v0_1 \
  tests.test_kuuos_codeai_external_corpus_acquisition_freeze_receipt_v0_1
```

repository-wide検証:

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile all
PYTHONPATH=. python3 scripts/check_observeos_sequential_epistemic_observability_envelope_v0_1.py
PYTHONPATH=. python3 scripts/check_verifyos_sequential_epistemic_observation_verification_handoff_v0_1.py
PYTHONPATH=. python3 scripts/check_verifyos_independent_evidence_verification_v0_1.py
PYTHONPATH=. python3 scripts/check_verifyos_outcome_disposition_handoff_v0_1.py
PYTHONPATH=. python3 scripts/run_evidence_cycle_os_full_checks.py

lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KuuOSCodeAIBaselineVersusCodeAIAblationComparisonV0_1

lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KuuOSFormal
```

Gate成功は登録surfaceの整合性receiptです。外部定理受理、経験的真理、性能優越、臨床承認、組織承認、production deployment、無制限repository mutation権限ではありません。

## 更新規則

README、ROADMAP、runtime rootは次のいずれかで同期更新します。

- authoritative `main`の機能frontierが変わる
- current root profileまたはstep setが変わる
- open Draftが統合、置換、closeされる
- benchmark observationまたはcomparison dispositionが変わる
- subsystem responsibilityまたはauthority boundaryが変わる
- Lean aggregate、toolchain、canonical checkerが変わる

古いopen PRを再利用する場合は、現在の`main`へrebaseし、scope、evidence contract、formal target、governance gateを再評価します。

## 固定境界

```text
candidate != authority
validation != truth
CI success != correctness or performance
formal compilation != external theorem acceptance

observation != verification
verification outcome != truth
disposition candidate != WORLD mutation
selection != execution
receipt != successor authority

protocol admission != harness execution authority
corpus freeze != solver gold access
gold smoke success != model performance
harness completion != issue resolution
patch application != correctness
aggregate evidence != raw evidence
one sample != population estimate
preregistration != completed comparison
comparison completed != performance claim
benchmark result != Git or repository mutation authority

memory != belief sovereignty
closure != empirical truth
lattice order != ranking
WORLD candidate != empirical fact
WORLD projection != persistent mutation
runtime success != production deployment
```
