# KuuOS / 空OS

![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS**は、観測、信念、記憶、計画、判断、実行、検証、学習、WORLD表現、repository evolutionを、由来、局所文脈、履歴、所有者、有限権限、明示的なreceipt chainへ束縛して接続する公開研究アーキテクチャです。

KuuOS is a public, governance-gated, proof-facing, non-Markovian, Qi-process-aware architecture for relational AI and bounded self-evolution research.

KuuOSは、候補、証拠、検証、承認、権限、実行効果、記憶、数学的表現、repository stateを同一視しません。

縁起、二諦、中道、和、局所性、履歴依存性、反証可能性、修復可能性を保ったまま、各層を型、digest、nonce、snapshot、receiptへ分離します。

KuuOSはproduction AGI runtimeではありません。

## 現在地

**基準日：2026年6月30日**

**文書化対象の機能frontier：PR #914、KuuOS Repository Atomic Checkpoint Creation v1.02**

**frontier merge commit：`e109a8d4e6896abe5eda786885683fe3e3ef8d89`**

現在の`main`系列は、MemoryOS production chainの後に、独立検証、自己改善、repository structure alignment、revision証明、bounded self-evolution、外部承認、原子的application、Git objectとreferenceの外部実行receipt、local frontier finality、checkpoint authorization、atomic checkpoint creation modelまで到達しています。

| 系列 | 統合済み到達点 |
|---|---|
| Core governance | v0.1 |
| Horizon Governance / Context Gauge Atlas | v0.12 / v0.13 |
| Modular Evolution Mesh | v0.1 |
| PlanOS control | v0.17 |
| Finite-cycle agent | v0.20からv0.27 |
| Qi diagnostic candidate / lineage | v0.28 / v0.29 |
| Open Horizon | v0.30からv0.34 |
| MemoryOS foundational line | v0.35、v0.37、v0.38、v0.39 |
| Qi-WORLD | v2.3 |
| WORLD mathematical sidecar | v0.27からv0.59 |
| Gauge-field self-organization | v0.60からv0.69 |
| Module-Bundle and MemoryOS application | v0.70からv0.76 |
| Authority topology / post-transition verification | v0.77 |
| Self-organizing improvement loop | v0.78 |
| Repository self-evolution chain | v0.79からv1.02 |
| Lean aggregate root | `formal/KuuOSFormal.lean` / target `KuuOSFormal` |
| Runtime aggregate root | `scripts/run_kuuos_runtime_full_check_v0_55.py` |
| Lean / mathlib | Lean 4、mathlib `v4.30.0-rc2` |

`run_kuuos_runtime_full_check_v0_55.py`という名称は外部workflowとの互換性のため保持しています。

現在の実体はv0.55で停止せず、統合済みruntime surfaceをv1.02まで依存順に検証します。

## 最重要境界

```text
candidate != authority
validation != truth
formal compilation != external theorem acceptance

observation != verification
verification != truth
learning != present-cycle mutation
memory != belief sovereignty
selection != execution
receipt != successor authority

local control != global constitution
local chart != global graph
curvature != veto
holonomy != sovereign memory

WORLD sidecar != exact WORLD
WORLD candidate != empirical fact
WORLD commit != truth
analytic vacuum != exact WORLD
Kū != zero vector
modular time != physical time

connection candidate != production application
application authority != performed effect
rollback != time reversal
restored payload != restored authority

modeled repository transition != live Git mutation
object candidate != object materialization
reference authorization != reference update
checkpoint authorization != checkpoint creation
checkpoint creation != checkpoint overwrite
local checkpoint != push authority
```

## OSの責務

| OS | 主な責務 |
|---|---|
| ObserveOS | source-bound observation ownership |
| BeliefOS | local and plural belief-state ownership |
| DecisionOS | admissible candidate selection |
| PlanOS | plan and replan synthesis |
| ActOS | exactly licensed bounded effect |
| VerifyOS | evidence-bound independent verification |
| LearnOS | future-only learning delta |
| MemoryOS | lineage、reconstruction、conditioned retrieval、read-only history source |
| WORLD | sourced representation and governed fragment storage |

```text
ObserveOS evidence != VerifyOS verdict
VerifyOS verdict != truth authority
LearnOS delta != immediate activation
DecisionOS selection != ActOS invocation
MemoryOS retrieval != PlanOS activation
WORLD intake != WORLD update
```

## 統合済みアーキテクチャ

### 局所文脈と有限サイクル

KuuOSは文脈を普遍的な固定グラフへ縮約しません。

文脈は、局所チャート、局所切断、遷移、曲率、cocycle residue、holonomyとして扱います。

有限サイクルは、mission binding、観測、複数信念、semantic planning、独立検証、bounded memory、effect reconciliation、checkpoint、restart recoveryを接続します。

局所サイクルの停止は、将来可能性全体の閉鎖を意味しません。

### Qi-WORLDとMemoryOS

Qi Process Tensorは、複数時点のプロセス、複数仮説、反証、不確実性、回復可能性区間を候補として保持します。

Qi-WORLD v2.3は、process supportとboundary occupationを陰陽相補系として接続します。

この構造は、気を物理的ボース粒子へ、blockerを物理的フェルミ粒子へ同一視しません。

MemoryOSは、履歴をtruth、belief sovereignty、PlanOS activation、ActOS authorityへ自動昇格させません。

### WORLD数学サイドカー

統合済み数学系列はv0.27からv0.59です。

```text
real Hilbert ℓ²
→ dense and self-adjoint operator bridge
→ noncommutative operator algebra
→ C*-local net
→ von Neumann and modular theory
→ Araki relative entropy
→ Petz recovery and conditional expectation
→ Jones theory and categorical bridges
→ higher-gauge information geometry
→ quantum Bregman and variational geometry
→ log-Sobolev contraction certificates
→ OS reflection-positive completion interface
→ analytic vacuum sector
→ vacuum-expectation receipt chain
→ Kū vacuum central reference state
→ Kū vacuum information geometry
→ closed Tomita operator bridge
→ conjugate-adjoint intermediate layer
→ four-great phase dynamics
```

Leanは、宣言された仮定の下で型付き帰結を検証します。

CI成功だけでは、外部数学界での定理受理、物理実現、経験的妥当性は成立しません。

### Gauge、Module-Bundle、MemoryOS production

v0.60からv0.69は、自己組織化を無制限な自己書換えではなく、有限候補、厳格な由来、rollback、外部reviewを持つ接続改善経路として構成します。

v0.70からv0.76は、文脈代数上の加群、意味部分加群、authority filtration、Leibniz接続、非マルコフ記憶核、外部review、単回commit、監査可能なrollbackを接続します。

v0.77は、context-independent authority role topologyと、commitまたはrollback後の独立post-transition verificationを追加します。

verification failureは自動rollbackを発火しません。

rollbackにはfresh request、独立した権限、snapshot binding、ledger CASが必要です。

## Repository self-evolution chain

v0.78以降は、KuuOS自身のrepositoryを研究対象として扱います。

各段階は有限で、source-boundで、replay可能で、fail closedです。

### 構造整合と証明連鎖

| Version | 責務 |
|---|---|
| v0.78 | bounded self-organizing improvement loopとsupervisor |
| v0.79 | repository structure alignment candidate |
| v0.80 | alignment normal form |
| v0.81 | incremental preservation |
| v0.82 | repository certificate chain |
| v0.83 | direct repository revision observation |
| v0.84 | merge certificate |
| v0.85 | revision DAG certificate |
| v0.86 | local repository frontier certificate |

### 候補選択、shadow、外部承認

| Version | 責務 |
|---|---|
| v0.87 | bounded self-evolution portfolio |
| v0.88 | shadow realization and replay |
| v0.89 | governed evolution admission |
| v0.90 | externally supplied approval receipt |
| v0.91 | single-use repository application authorization |
| v0.92 | pure atomic repository application transition |

### Git object、reference、finality、checkpoint

| Version | 責務 |
|---|---|
| v0.93 | deterministic tree and commit candidate certificate |
| v0.94 | object materialization authorization |
| v0.95 | external object materialization receipt |
| v0.96 | direct branch reference-update authorization |
| v0.97 | atomic modeled reference and nonce transition |
| v0.98 | external reference-update receipt |
| v0.99 | delayed reference stability and reachability |
| v1.00 | bounded multi-sample local frontier finality |
| v1.01 | single-use local checkpoint authorization |
| v1.02 | atomic modeled checkpoint-reference creation and nonce consumption |

```text
bounded improvement proposal
→ repository alignment and preservation certificates
→ revision and frontier evidence
→ finite portfolio selection
→ shadow replay
→ governed admission
→ external approval
→ single-use application authorization
→ atomic modeled application
→ commit candidate
→ object materialization authorization and receipt
→ reference update authorization, transition and receipt
→ delayed stability
→ local frontier finality
→ checkpoint authorization
→ atomic modeled checkpoint creation
```

## v1.02の正確な意味

v1.02は、`refs/kuuos/checkpoints/`内の新規checkpoint referenceについて、zero-OID compare-and-swapとnonce consumptionを一つの純粋な状態遷移として構成します。

commit時には次を同時に成立させます。

```text
checkpoint reference: zero OID → authorized final-tip OID
nonce registry: unused nonce → consumed nonce
```

abort時にはcheckpoint stateとnonce registryを完全に保存します。

v1.02はlive Git commandを呼びません。

v1.02単独では、live repository mutation、push、force update、delete、tag update、branch update、reflog write、object database writeを証明しません。

外部実行adapter、実行報告、post-execution observation、最終receiptは後続層です。

## Lean root

`formal/KuuOSFormal.lean`は、統合済み形式層のstrict aggregate rootです。

v0.77のauthority topologyとpost-transition verification、およびv0.78からv1.02のrepository self-evolution系列を明示的にimportします。

```bash
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KuuOSFormal
```

専用rootは各versionの局所surfaceを検証します。

aggregate rootはimport欠落、依存順の破綻、境界退行を検出します。

## Runtime root

`scripts/run_kuuos_runtime_full_check_v0_55.py`は、互換名を維持した累積runtime rootです。

現在はlegacy chainに加え、v0.56、v0.59、v0.60からv0.77、v0.78からv0.95、v0.96からv1.02のlive-contract validatorとfocused unit testsを依存順に実行します。

```bash
PYTHONPATH=. python3 scripts/run_kuuos_runtime_full_check_v0_55.py
```

v1.02 frontierだけを累積的に確認する入口も残します。

```bash
PYTHONPATH=. python3 runtime/kuuos_v102_check.py
```

root成功は、検査対象surfaceの再現可能な整合性receiptです。

真理、外部定理受理、臨床承認、組織承認、live Git mutation、無制限実行許可ではありません。

## 次の研究前線

直近の自然な次段階は、v1.02のmodeled checkpoint transitionをlive local Git executionへ直接同一視せず、限定adapterと独立receiptを追加することです。

```text
v1.02 committed modeled transition
→ exact single-use execution request
→ bounded local reference adapter
→ external execution report
→ independent post-reference observation
→ checkpoint creation receipt
→ delayed stability / finality evidence
```

checkpoint overwrite、delete、remote push、branch mutation、tag mutationは別権限です。

詳細は[`ROADMAP.md`](ROADMAP.md)に記載します。

## 非主張

KuuOSは現時点で次を主張しません。

- 無制限の実行権限を持つproduction AGI。
- 任意のshell、network、repository、deploymentへの包括権限。
- 単一真理へ収束する普遍的global-context graph。
- 独立した医療診断、トリアージ、治療、医療行為承認システム。
- 気が物理的粒子であることの証明。
- LeanまたはCIの成功だけによる外部定理受理。
- 完全な物理的量子Markov semigroup、正確な物理真空、正確なWORLD simulator。
- 解析的真空と形而上学的な空の同一視。
- rollbackによる承認権限または過去状態の復活。
- repository candidate、authorization、modeled transition、receiptの自動的なlive effect化。
- checkpoint creation authorityからoverwrite、delete、push権限への昇格。

## 最初に読む文書

```text
README.md
ROADMAP.md
GOVERNANCE.md
CONTRIBUTING.md

formal/KUOS.lean
formal/KuuOSFormal.lean
scripts/run_kuuos_runtime_full_check_v0_55.py

KUUOS_REPOSITORY_ATOMIC_CHECKPOINT_CREATION_v1_02.md
runtime/kuuos_v102_check.py
```

## ディレクトリ

```text
docs/         public specifications, boundaries and status documents
runtime/      bounded runtime kernels, adapters, stores and scenarios
src/          typed modular contracts, registries and orchestration surfaces
scripts/      validators and cumulative full-check entry points
tests/        runtime regression and boundary tests
formal/       Lean and mathlib-facing formal surfaces
manifests/    versioned component and validation manifests
cases/        governance and failure-mode cases
roadmap/      specialized additive research roadmaps
.github/      reproducible CI workflows
```

## 開発原則

```text
additive lineage
same-root binding for protected surfaces
append-only evidence
explicit versioning
fail closed on stale or substituted state
finite local authority
open global possibility horizon
independent observation after effect
visible uncertainty, dissent, residue and cost
no silent promotion from candidate to authority
rollback as monotonic compensation
stable main != active research branch
modeled transition != live mutation
```

新しい層は、入力、出力、所有者、必要権限、永続化、replay、stale-state処理、validatorの射程、外部仮定、非権限境界を明記します。

## Citation, governance and rights

引用、貢献、再利用条件は、[`CITATION.cff`](CITATION.cff)、[`GOVERNANCE.md`](GOVERNANCE.md)、[`CONTRIBUTING.md`](CONTRIBUTING.md)、repository license filesを参照してください。

**空OS、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属します。**

個別のrepository artifactの再利用は、各licenseと著作者表示に従います。

Repository artifactは、臨床権限、組織権限、数学的受理、実行権限を移転しません。
