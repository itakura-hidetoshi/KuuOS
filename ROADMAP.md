# KuuOS / 空OS Roadmap

**基準日：2026年7月29日 JST**

このRoadmapは、`main`へ統合済みの事実、canonical runtime root、live再検証待ち、条件付き次段階を分離します。未merge branch、queuedまたはin-progress CI、将来構想をcurrent frontierへ混ぜません。

## 状態分類

| 表記 | 意味 |
|---|---|
| 統合済み | authoritative `main`に存在する |
| Current root | `runtime/kuuos_current_check.py`のprofileからdeterministicに検証される |
| 専用CI | subsystem固有workflowでruntime、manifest、tests、formal rootを検証する |
| Live verified | separately authorized live transactionがcompleted evidenceで閉じた |
| Live再検証待ち | 実装は統合済みだが、そのmerge後のfresh live transactionが未完了 |
| 継続検証 | 依存、aggregate、toolchain、authority boundary変更時に再検証する |
| 条件付き候補 | exact base、scope、authority、evidence contractが未確定 |
| Frozen boundary | additiveまたはtighten-onlyで維持する責任境界 |

## 現在のauthoritative functional baseline

```text
branch: main
functional milestone commit: 892621fc91e3ea5f41e5da7a683682063b862aaf
latest integrated functional PR: #1382
frontier: KuuOS GitHub MCP Sub-Issue Chain Parent Cross-Observation v1.1
current-frontier successor Draft: none designated
```

moving `main` HEADは、文書、governance、互換surfaceの同期mergeでも進みます。したがって、branch HEADと、subsystemの機能frontierを定めるmilestone commitを同一視しません。

| 系列 | 到達点 | 状態 |
|---|---|---|
| Core governance | v0.1 | Frozen boundary |
| Horizon / Context Gauge | v0.12 / v0.13 | 統合済み、継続検証 |
| Finite-cycle agent | v0.20-v0.27 | 統合済み |
| Qi diagnostic lineage | v0.28 / v0.29 | 統合済み |
| Qi-WORLD | v2.3 | 統合済み |
| Qi local-real Yin-Yang geometry | v2.4 | 統合済み、Current root |
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
| CodeAI external benchmark line | protocolからfrozen cohort / shard contractまで | 統合済み、Current root |
| GitHub MCP official-server bridge | v0.1-v1.1 | 統合済み、Current root |
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
→ architecture
→ PlanOS
→ DecisionOS
→ MemoryOS
→ CodeAI
→ GitHub MCP
```

個別実行:

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py --summary
PYTHONPATH=. python3 runtime/kuuos_current_check.py --list
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile repository
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile architecture
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile planos
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile decisionos
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile memoryos
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile codeai
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile github_mcp
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile all
```

`architecture` profileはQi Process Tensor Local-Real Yin-Yang Geometry v2.4のdeterministic projectionとfocused testsを実行します。

`codeai` profileは、PR #1342のfrozen cohort / prediction-pack / execution-shard contract、PR #1341のcomparison projection、外部評価系列のdirect predecessor regressionsを検査します。外部Docker harnessを再実行せず、外部artifactを再取得せず、gold materialをcurrent rootへ持ち込みません。

`github_mcp` profileは、v1.0 three-level chain contract、v1.1 bounded direct read / cross-observation adapter、compensation boundaryをdeterministic transportで検査します。live GitHub writeを実行しません。

ObserveOSとVerifyOSはprofile rootへ暗黙追加せず、専用workflow、Evidence Cycle累積runner、versioned formal aggregateで検証します。

## 前回の公開面同期後に統合された主要stage

### CodeAI

PR #1342 **CodeAI Frozen Cohort Prediction-Pack and Execution-Shard Contract v0.1**は`main`へ統合済みです。

統合済みの契約:

```text
shared holdout slots: 100
cohorts: baseline / CodeAI full / 3 ablations
shards per cohort: 10
samples per shard: 10
total external-only shards: 50
```

未完了:

```text
external shared-holdout materialization
authentic prediction packs complete
execution shards ready
external comparison execution
performance comparison completed
performance claimed
```

### Qi architecture

PR #1345 **Qi Process Tensor Local-Real Yin-Yang Geometry v2.4**は`main`へ統合済みです。

このstageは、local-real frame、Z2 conversion parity、non-Markov process memory、holonomy residue、admitted / held Qi、Two Truths preservationを一つのbounded architecture receiptへ接続します。

```text
Qi != substance
Yin-Yang != fixed global essence
double conversion != history erasure
recoverability gap candidate != physical 4D mass gap
```

### GitHub MCP official-server bridge

統合系列:

| PR | Stage | 到達点 |
|---|---|---|
| #1346 | GitHub MCP Server Bridge v0.1 | official stdio JSON-RPC、tool discovery、bounded admission |
| #1347 | Bridge CI Fast Path v0.1 | runtime / formal CI分離、focused governance selection |
| #1348 | Write-Capable Bridge v0.2 | direct MCP writesとexact Git delegation |
| #1349 | Live Write Verification v0.3 | write後の独立reobservation |
| #1350 | Reversible Live Canary v0.4 | Issue create / reobserve / close / reobserve |
| #1351 | Workflow Dispatch v0.5 | official MCPによるnonce / exact-head dispatch |
| #1353 | Immutable Image Dispatch v0.5.1 | official server imageをimmutable digestへ固定 |
| #1356 | Repository Label Canary v0.6 | create / exact read / delete / absence |
| #1358-#1362 | Issue–Label v0.7-v0.7.2 | reversible binding、body compatibility、50文字上限 |
| #1364 | Sub-Issue Binding v0.8 | reversible parent-child binding |
| #1367 | Bidirectional Canary v0.9 | downward child setとupward parentの独立確認 |
| #1370 | Three-Level Chain v1.0 | root → child → grandchild |
| #1374 / #1378 | Reobservation v1.0.1 / v1.0.2 | bounded direct `get_parent` retries |
| #1382 | Parent Cross-Observation v1.1 | nested-parent official-MCP cross-observation |

## GitHub MCP live integration state

### Live verified

v0.4-v0.9の段階的live transactionは、各stageのscope内でcompleted evidenceにより閉じています。特にv0.8とv0.9は、relation追加、downward / upward reobservation、relation除去、final absence、child close、artifact digest、append-only audit、token非直列化を確認済みです。

### 観測済みfailureとcompensation

v1.0-v1.0.2のlive requestでは、root → childとchild → grandchildのdownward relationが観測された一方、grandchildの直接`issue_read(get_parent)`は最大30回・60秒のbounded windowでもnullでした。

```text
direct nested parent observation: null
downward child → grandchild relation: exact
compensation attempted: true
cleanup verified: true
residual hierarchy accepted: false
```

このfailureはコード成功へ読み替えません。compensationはbounded recovery evidenceであり、VERIFIEDではありません。

### v1.1 Live再検証待ち

v1.1は、direct nested parentがnullのときに次を要求します。

1. child Issueのexact number
2. `has_parent = true`
3. exact `parent_issue_url`
4. expected parent Issueのexact number
5. parentがopen
6. non-empty parent title

すべて一致した場合だけ、既存v1.0 exact-parent shapeを合成します。不一致は元のnull observationを返してfail closedします。remove後はdirect nullだけをabsence evidenceとして使います。

#1382 merge後のfresh owner requestはまだありません。したがって現在の表記は次です。

```text
v1.1 implementation: integrated
v1.1 deterministic validation: integrated
v1.1 post-merge live transaction: pending
v1.1 live VERIFIED claim: false
```

## 優先順位

### 1. v1.1 fresh live integrationを閉じる

then-current exact `main` SHAと新しいnonceへbindingしたowner requestを1件だけ作成し、completed run / job / step / artifact / logで次を確認します。

- root、child、grandchildのexact identity
- initial parent / child sets
- root → childのdownward / upward relation
- child → grandchildのdownward relation
- v1.1 child-side parent linkとexpected parentのcross-observation
- leaf edgeからのremove
- remove後のdirect parent null
- root edge remove後のfinal absence
- child / grandchild close
- compensation未使用
- append-only audit correspondence
- token / Authorization valueの非直列化

外部service挙動が再び異なる場合は、そのcompleted evidenceを保存し、authority条件やtheorem statementを弱めずに別stageで扱います。

### 2. Public surfaceとcurrent rootを継続同期する

README、ROADMAP、`runtime/kuuos_current_check.py`を一つの責任境界として維持します。

- functional milestone commitとmoving `main` HEADを分離
- current-frontier successor Draftがないときは`null`で表現
- profile追加はdeterministic / effect-free validationに限定
- live operationをcurrent rootへ混ぜない
- legacy status tokensを保持
- completed CIだけで公開面を確定

### 3. CodeAI frozen cohortを実体化する

PR #1342の契約をpredecessorとして、別stageで次を行います。

- pinned external corpusからshared holdoutをmaterializeする
- baseline / CodeAI full / 3 ablationのauthentic prediction packを生成する
- prediction source、model / configuration、pipeline variant、candidate digestをexact bindingする
- prediction欠測、重複、cross-cohort reuse、gold leakageをHOLDまたはBLOCKする
- generation authorityとevaluation authorityを分離する
- external-only shard readinessを独立receiptで確定する

### 4. External-only shard execution

- official pinned harnessとDocker imageを使う
- shard単位のtimeout、worker、retry、artifact retentionを固定する
- kernelはharnessを実行せず、外部実行evidenceだけを受理する
- execution failureをsilent exclusionしない
- raw resultは短期検証に限定し、repositoryへはaggregate receiptだけを残す

### 5. Balanced comparison

- 全cohortのsample countとholdout bindingを一致させる
- resolved-rateをprimary metricとして計算する
- FAIL_TO_PASS、PASS_TO_PASS、execution-valid-rate、error-rateをguardrailとして保持する
- 欠測、leakage、cohort imbalance、metric欠落では比較をHOLDする
- uncertaintyとfailure distributionを報告する
- performance claimをcomparison completionと独立に承認する

### 6. Qi v2.4の解析的次段階

- local-real transportのcomposition lawを追加検証する
- conversion parityとholonomy residueの関係を分離する
- admitted / held Qi conservationを一般化する
- recoverability-gap candidateの仮定と反例境界を明示する
- modular / KMS / non-Markov依存をreceiptとして維持する
- physical mass gap、fixed Yin substance、global polarityへ同一化しない

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

PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile architecture
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile codeai
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile github_mcp

PYTHONPATH=. python3 scripts/check_qi_process_tensor_local_real_yinyang_geometry_v2_4.py
PYTHONPATH=. python3 scripts/check_kuuos_github_mcp_sub_issue_chain_canary_v1_0.py

PYTHONPATH=. python3 -m unittest \
  tests.test_qi_process_tensor_local_real_yinyang_geometry_v2_4 \
  tests.test_kuuos_codeai_frozen_cohort_prediction_pack_execution_shard_contract_v0_1 \
  tests.test_kuuos_github_mcp_sub_issue_chain_parent_cross_observation_v1_1 \
  tests.test_kuuos_github_mcp_sub_issue_chain_canary_v1_0
```

repository-wide検証:

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile all

lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KUOS.Architecture.QiProcessTensorLocalRealYinYangGeometryV2_4

lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KuuOSGitHubMCPServerBridgeV0_1

lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KuuOSFormal
```

PRをReadyへ進める前に、fixed final head、completed CI success、base SHA不変、mergeable、reviews 0、unresolved inline review threads 0、同系列duplicate PRなしを確認します。Ready後にも同じ条件を再監査します。

通常mergeはmerge commit方式です。自動mergeを使わず、merge時は`expected_head_sha`を固定します。

## Frozen boundaries

```text
candidate != authority
validation != truth
formal compilation != external theorem acceptance
CI success != correctness or performance

tool availability != authority
MCP write capability != Git authority
write acceptance != verified closeout
reobservation != universal service guarantee
compensation != success
cleanup verified != primary transaction verified
direct nested-parent null != no hierarchy
cross-observation != direct get_parent response

contract admitted != materialization complete
prediction pack contract != authentic predictions
shard contract != execution readiness
one smoke sample != population performance
comparison completion != performance claim

Qi != fixed substance
Yin-Yang != global immutable essence
local real structure != universal frame
recoverability gap candidate != physical 4D mass gap

selection != execution
receipt != successor authority
WORLD candidate != empirical fact
modeled repository transition != live Git mutation
current root success != production deployment
```
