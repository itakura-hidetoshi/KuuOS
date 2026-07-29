# KuuOS / 空OS

![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS**は、観測、文脈、信念、記憶、WORLD表現、計画、判断、実行、再観測、検証、学習を、由来、履歴、責任主体、有限権限、content address、検証可能なreceiptへ結び付ける公開研究アーキテクチャです。

KuuOS is a public, governance-gated, proof-facing, non-Markovian and relational AI research architecture. It keeps candidates separate from authority, evidence separate from truth, validation separate from acceptance, and selection separate from execution.

## 現在地

**基準日：2026年7月29日 JST**

authoritative branchは`main`です。この公開面が表す最新の機能milestoneは、commit `892621fc91e3ea5f41e5da7a683682063b862aaf`、PR #1382 **KuuOS GitHub MCP Sub-Issue Chain Parent Cross-Observation v1.1**です。文書またはgovernance同期のmergeでmoving `main` HEADが進んでも、このmilestoneは自動では変わりません。

現時点でcurrent-frontier successorとして指定されたDraft PRはありません。過去から残るopen PRは、明示的な再基底、scope更新、completed CI再検証なしにcurrent frontierへ昇格しません。

| 面 | 統合済み到達点 | 主な入口 |
|---|---|---|
| Repository lineage | self-organization v0.113 | `runtime/kuuos_current_root_sequence_v0_113.py` |
| ObserveOS | v0.7 sequential epistemic observability envelope | `docs/ObserveOS/README.md` |
| VerifyOS | v0.15 read-only outcome disposition handoff | `docs/VerifyOS/README.md` |
| Qi architecture | Qi Process Tensor Local-Real Yin-Yang Geometry v2.4 | `docs/KUUOS_QI_PROCESS_TENSOR_LOCAL_REAL_YINYANG_GEOMETRY_v2_4.md` |
| PlanOS | v1.23 finite Physical Quantum Qi coherence kernel and partial dephasing | `formal/KuuOSPlanOSV1_23.lean` |
| DecisionOS | v0.6 WORLD-conditioned relational deliberation | `formal/KuuOSDecisionOSV0_6.lean` |
| MemoryOS | v1.00 finite bounded closed-support lattice | `formal/KuuOSMemoryOSV1_00.lean` |
| CodeAI | frozen cohort / prediction-pack / execution-shard contract v0.1 | `docs/KUUOS_CODEAI_FROZEN_COHORT_PREDICTION_PACK_EXECUTION_SHARD_CONTRACT_v0_1.md` |
| GitHub MCP | sub-issue chain parent cross-observation v1.1 | `runtime/kuuos_github_mcp_sub_issue_chain_parent_cross_observation_v1_1.py` |
| Repository formal baseline | strict aggregate import | `formal/KuuOSFormal.lean` |
| Canonical runtime root | integrated deterministic current frontier | `runtime/kuuos_current_check.py` |

subsystem versionは独立しています。ObserveOS v0.7、VerifyOS v0.15、Qi architecture v2.4、PlanOS v1.23、DecisionOS v0.6、MemoryOS v1.00、self-organization v0.113、CodeAI各v0.1 stage、GitHub MCP v0.1-v1.1を、一つの直線的version番号や成熟度尺度として扱いません。

## GitHub MCP Serverの現在のfrontier

KuuOSはGitHub公式`github/github-mcp-server`を、無制限な権限源ではなく、KuuOSのauthority、exact repository、exact SHA、operation approval、再観測、receipt、compensation境界へ接続するadapterとして統合しています。

```text
v0.1  official MCP transport / discovery / bounded admission
→ v0.2  write-capable authority adapter
→ v0.3  independent post-write reobservation
→ v0.4  reversible live Issue canary
→ v0.5 / v0.5.1  workflow dispatch and immutable image digest
→ v0.6  reversible repository-label transaction
→ v0.7-v0.7.2  reversible Issue–Label binding and live compatibility repairs
→ v0.8  reversible sub-issue binding
→ v0.9  downward and upward bidirectional sub-issue verification
→ v1.0  reversible three-level root → child → grandchild chain
→ v1.0.1 / v1.0.2  bounded direct parent reobservation
→ v1.1  exact nested-parent cross-observation
```

v0.8とv0.9は、post-merge live transaction、cleanup、artifact digest、append-only audit、token非直列化までcompleted evidenceで検証済みです。

v1.0-v1.0.2のlive実行では、`child → grandchild`のdownward relationが正確に観測される一方、grandchildの直接`issue_read(get_parent)`が最大60秒nullのままになる公式surface挙動が観測されました。各失敗はcompensationによってleaf edgeから除去され、残存hierarchyを成功として受理していません。

v1.1は、短いdirect readの後、child Issueの`has_parent = true`とexact `parent_issue_url`を確認し、expected parent Issueを独立にreadして一致した場合だけ既存のexact parent observationを合成します。remove後のabsenceはdirect nullだけで確認します。v1.1実装とdeterministic validationは`main`へ統合済みですが、#1382 merge後のfresh owner live requestはまだ実行されていません。

## CodeAIの現在の評価frontier

外部一般benchmark系列は、protocol、corpus freeze、evaluator-only gold smoke、bounded non-gold execution、aggregate ingestion、balanced comparison preregistration、frozen cohort / prediction-pack / execution-shard contractまで統合されています。

```text
SWE-bench Verified protocol and adapter
→ exact external corpus acquisition and freeze receipt
→ evaluator-only gold-patch environment smoke validation
→ bounded non-gold official harness execution
→ aggregate result and process-evidence ingestion
→ baseline-versus-CodeAI and ablation comparison preregistration
→ frozen cohort / prediction-pack / execution-shard contract
```

観測済みのnon-gold外部実行は、固定された1件のengineering smoke sampleです。

```text
instance: sympy__sympy-20590
patch applied: true
evaluation completed: true
resolved: false
FAIL_TO_PASS: 0 success / 1 failure
PASS_TO_PASS: 21 success / 0 failure
execution errors: 0
```

この`0/1`は観測済みevidenceであり、CodeAI全体の性能推定、正しさ、一般化、優越性を意味しません。

PR #1342は、100-slot shared holdout ledger、baseline / CodeAI full / 3 ablation、各cohort 10 shard、合計50 external-only shardの契約を統合しました。ただし、authentic prediction pack、execution shard readiness、外部比較実行、performance comparison、performance claimは未完了です。

## Qi architecture v2.4

Qi Process Tensor Local-Real Yin-Yang Geometry v2.4は、陰陽を固定物質やglobal immutable labelではなく、history-bearing process carrier上のgauge-local involutive real structureとして扱います。

この層は、local-real frame transport、Z2 conversion parity、non-Markov memory、holonomy residue、admitted / held Qi conservation、modular/KMS proof receipt、recoverability-gap candidateを結びます。recoverability gapは解析的候補であり、物理的4D mass gapの主張ではありません。runtimeはanalytic receiptを生成せず、明示的な依存としてのみ受理します。

## Canonical runtime root

標準入口は次です。

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py
```

current rootはrun-all-then-decideです。一つのstepが失敗しても残りを実行し、required stepの失敗を最後に集約します。

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

| Profile | 検査面 |
|---|---|
| `repository` | repository mutationとself-organizationの累積lineage |
| `architecture` | Qi Process Tensor Local-Real Yin-Yang Geometry v2.4 |
| `planos` | PlanOS v0.91-v1.23 active frontier |
| `decisionos` | DecisionOS v0.1-v0.6 cumulative validation |
| `memoryos` | MemoryOS v0.40-v1.00 active frontier |
| `codeai` | PR #1342 contract、PR #1341 comparison、direct predecessor regressions |
| `github_mcp` | v1.0 deterministic chain contractとv1.1 parent cross-observation |
| `all` | 上記すべて |

`github_mcp` profileはdeterministic mock / fixture validationだけを実行します。GitHubへのlive write、workflow dispatch、Issue作成、label mutation、sub-issue mutationを行いません。live transactionは、owner request、exact current `main` SHA、immutable official server digest、専用workflow、completed evidenceを必要とする別の運用境界です。

ObserveOS v0.7とVerifyOS v0.13-v0.15は、各専用workflow、Evidence Cycle累積runner、versioned formal aggregateで独立検証します。current root成功は、登録されたrepository内surfaceがそのrevisionで再現可能に整合したことを示します。外部定理受理、経験的真理、臨床承認、組織承認、production deployment、live GitHub effect authorityを意味しません。

## Formal validation

Lean toolchainと依存はrepositoryに固定されています。

```bash
lake update
lake exe cache get
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KuuOSFormal
```

GitHub MCP aggregateだけをstrict buildする場合:

```bash
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KuuOSGitHubMCPServerBridgeV0_1
```

Qi architecture v2.4だけをstrict buildする場合:

```bash
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KUOS.Architecture.QiProcessTensorLocalRealYinYangGeometryV2_4
```

formal compilationはrepository内の定義と定理が固定toolchainで検査されたことを示します。外部査読、経験的妥当性、運用承認、live service behaviorの普遍性を代替しません。

## Legacy compatibility status surface

現行のsource of truthは`runtime/kuuos_current_check.py`です。次のlegacy identifiersとstable entrypointは、self-organization lineageおよび既存status consumerとの後方互換性のため保持します。

```text
KuuOS README Public Status v0.66
kuuos_current_root_sequence_v0_66
docs/kuuos_self_organization_active_state.md
```

| Surface | Path |
|---|---|
| Stable current surface CLI | `runtime/kuuos_current_surface.py` |
| Versioned current surface entrypoint | `runtime/kuuos_current_surface_entrypoint_v0_77.py` |
| Current surface index | `status/current.surface.index.json` |
| Current surface artifact | `status/current.surface.json` |
| Current resolved status artifact | `status/current.resolved.json` |
| Current manifest | `status/current.manifest.json` |

これらは互換・履歴surfaceであり、canonical runtime rootの代替ではありません。

## Repository map

| Path | 役割 |
|---|---|
| `runtime/` | executable kernels、receipts、validators、canonical current root |
| `scripts/` | fail-closed checkers、fixture projection、cumulative runners |
| `formal/` | Lean theorem packagesとaggregate imports |
| `manifests/` | machine-readable package bindings |
| `examples/` | deterministic reference projections |
| `status/` | historical and compatibility status artifacts |
| `docs/` | versioned specifications and subsystem indexes |
| `tests/` | runtime、binding、tamper、boundary、regression tests |
| `.github/workflows/` | governance、subsystem validation、separately authorized live gates |

主要なsubsystem index:

- `docs/ObserveOS/README.md`
- `docs/VerifyOS/README.md`
- `docs/CodeAI/README.md`
- `ROADMAP.md`

## 開発原則

変更はexact `main` SHAからdedicated branchを作り、通常はDraft PRとして提出します。CI判断にはcompleted run、job、step、artifact、logだけを使い、queuedまたはin-progressを成功・失敗の確定証拠にしません。

runtime、checker、manifest、documentation、formal packageを同じ責任境界へ揃えます。候補、証拠、検証、承認、権限、実行効果は別artifactとして保持し、後続権限をreceiptから自動生成しません。

GitHub MCPでは、write acceptanceをverified closeoutと同一視しません。exact reobservation、final absence、compensation record、token-free evidenceが別に必要です。外部基盤の観測差を、theoremやauthority条件の弱化で隠しません。

## 固定境界

```text
candidate != authority
validation != truth
formal compilation != external theorem acceptance
CI success != correctness or performance

observation != verification
verification outcome != truth
passed != WORLD adoption
failed != WORLD rejection
indeterminate != evidence deletion
disposition candidate != WORLD mutation
selection != execution
receipt != successor authority

MCP server configured != tool discovered
tool discovered != tool allowlisted
tool allowlisted != operation admitted
operation admitted != effect verified
write accepted != verified closeout
compensation != success
direct nested-parent null != no hierarchy
cross-observation != universal future server guarantee
MCP write capability != Git authority

aggregate benchmark evidence != raw gold evidence
one measured sample != population performance
preregistration != completed comparison
contract admitted != prediction packs complete
contract admitted != execution shards ready
external harness completion != issue resolution
patch application != correctness
benchmark result != repository mutation authority

Qi != fixed substance
Yin-Yang != global immutable polarity
double conversion != history erasure
recoverability gap candidate != physical 4D mass gap

memory != belief sovereignty
closure fixed point != empirical truth
lattice structure != ranking
WORLD candidate != empirical fact
WORLD intake != WORLD update
modular time != physical time

modeled repository transition != live Git mutation
current root success != production deployment
README public status != authority grant
```

詳細な次段階と更新条件は[ROADMAP.md](ROADMAP.md)に記載します。
