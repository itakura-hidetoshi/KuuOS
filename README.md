# KuuOS / 空OS

![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS**は、観測、信念、記憶、計画、判断、実行、検証、学習、WORLD表現、repository evolutionを、由来、局所文脈、履歴、所有者、有限権限、明示的なreceipt chainへ束縛して接続する公開研究アーキテクチャです。

KuuOS is a public, governance-gated, proof-facing, non-Markovian, Qi-process-aware architecture for relational AI and bounded self-evolution research.

KuuOSは、候補、証拠、検証、承認、権限、実行効果、記憶、数学的表現、repository stateを同一視しません。

KuuOSはproduction AGI runtimeではありません。

## 現在地

**基準日：2026年7月1日**

**`main`の統合済みfrontier：KuuOS Repository Bounded Blob v1.19**

**frontier merge commit：`f3ae5c69761c384e32a8e807afbec6c2ebb1a199`**

**開発中frontier：Draft PR #942、KuuOS Repository Bounded Tree and Commit v1.20**

v1.20は`main`へ未統合です。

README、ROADMAP、CITATION、Lake package version、Lean aggregate root、runtime aggregate rootは、統合済み`main`のv1.19を基準にします。

| 項目 | 現在の正式値 |
|---|---|
| Repository package version | `1.19.0` |
| Lean toolchain | `leanprover/lean4:v4.30.0-rc2` |
| mathlib | `v4.30.0-rc2` |
| Lean aggregate root | `formal/KuuOSFormal.lean` |
| Lake default target | `KuuOSFormal` |
| Runtime aggregate root | `scripts/run_kuuos_runtime_full_check_v0_55.py` |
| Runtime cumulative frontier | `runtime/kuuos_v119_check.py` |
| Integrated repository frontier | v0.79からv1.19 |
| Active unmerged frontier | v1.20、Draft PR #942 |

`scripts/run_kuuos_runtime_full_check_v0_55.py`という名称は、既存workflowと外部呼出しとの互換性のため保持しています。

実際の検証frontierはv0.55ではなく、統合済みv1.19です。

## 固定境界

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
receipt composition != receipt construction

local control != global constitution
local chart != global graph
curvature != veto
holonomy != sovereign memory

WORLD sidecar != exact WORLD
WORLD candidate != empirical fact
WORLD commit != truth
WORLD intake != WORLD update
analytic vacuum != exact WORLD
Kū != zero vector
modular time != physical time

connection candidate != production application
application authority != performed effect
rollback != time reversal
restored payload != restored authority

modeled repository transition != live repository mutation
live preflight != mutation authority
checkpoint reference CAS != branch or tag update
blob materialization != tree or commit materialization
object materialization != reference update
local mutation != remote push authority
successful test != permission to mutate an external repository
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

KuuOSは、文脈を普遍的な固定グラフへ縮約しません。

文脈は、局所チャート、局所切断、遷移、曲率、cocycle residue、holonomyとして扱います。

有限サイクルは、mission binding、観測、複数信念、semantic planning、独立検証、bounded memory、effect reconciliation、checkpoint、restart recoveryを接続します。

局所サイクルの停止は、将来可能性全体の閉鎖を意味しません。

### Qi-WORLDとMemoryOS

Qi Process Tensorは、複数時点のprocess、複数仮説、反証、不確実性、回復可能性区間を候補として保持します。

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
→ vacuum-expectation observation candidate
→ ObserveOS evidence intake
→ host-effect atomic commit intake
→ OS receipt composition
→ Kū vacuum central reference state
→ Kū vacuum information geometry
→ closed Tomita operator bridge
→ conjugate-adjoint intermediate layer
→ four-great phase dynamics
```

Leanは、宣言された仮定の下で型付き帰結を検証します。

CI成功だけでは、外部数学界での定理受理、物理実現、経験的妥当性は成立しません。

### Gauge、Module-Bundle、MemoryOS application

v0.60からv0.69は、有限候補、由来、rollback、外部reviewを持つ接続改善経路を構成します。

v0.70からv0.76は、文脈代数上の加群、意味部分加群、authority filtration、Leibniz接続、非マルコフ記憶核、有限評価、外部review、単回commit、monotonic rollbackを接続します。

v0.77のauthority-role topologyとpost-transition verificationは提案枝として作成されましたが、`main`へは統合されていません。

正式なLean rootとruntime rootはv0.77を含めず、v0.76の後にv0.78へ進みます。

## Repository self-evolution chain

v0.78以降は、KuuOS自身のrepositoryを研究対象として扱います。

各段階は有限で、source-boundで、replay可能で、fail closedです。

### 構造整合と承認

| Version | 統合済み責務 |
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
| v0.87 | bounded self-evolution portfolio |
| v0.88 | shadow realization and replay |
| v0.89 | governed evolution admission |
| v0.90 | externally supplied approval receipt |
| v0.91 | single-use repository application authorization |
| v0.92 | pure atomic modeled repository application |

### Git object、reference、finality、checkpoint

| Version | 統合済み責務 |
|---|---|
| v0.93 | deterministic blob、tree、commit candidate certificate |
| v0.94 | object materialization authorization |
| v0.95 | external object materialization receipt |
| v0.96 | direct local branch reference-update authorization |
| v0.97 | modeled reference CASとnonce consumption |
| v0.98 | external reference-update receipt |
| v0.99 | delayed reference stability and reachability |
| v1.00 | bounded multi-sample local frontier finality |
| v1.01 | single-use local checkpoint authorization |
| v1.02 | modeled checkpoint-reference creation |
| v1.03 | checkpoint creation receipt |
| v1.04 | checkpoint evolution workspace |
| v1.05 | checkpoint stability and immutability evidence |
| v1.06 | discrepancy review with minimal human boundary |
| v1.07 | deterministic repair routing |
| v1.08 | checkpoint namespace compatibility gate |
| v1.09 | deterministic checkpoint candidate |
| v1.10 | checkpoint compare-and-swap contract |
| v1.11 | independent candidate validation receipt |
| v1.12 | validated CAS intake |
| v1.13 | CAS coherence receipt |
| v1.14 | bounded CAS authorization request |
| v1.15 | CAS authorization decision |
| v1.16 | modeled atomic CAS transition |
| v1.17 | live Git checkpoint preflight with read-only observations |
| v1.18 | bounded live checkpoint-reference CAS |
| v1.19 | bounded live Git blob materialization or exact reuse |

```text
bounded improvement proposal
→ repository alignment and preservation certificates
→ revision and frontier evidence
→ finite portfolio selection
→ shadow replay
→ governed admission
→ external approval
→ modeled repository application
→ object and reference evidence
→ local finality and checkpoint chain
→ independent validation and authorization
→ modeled checkpoint CAS
→ live read-only Git preflight
→ one bounded checkpoint-reference CAS
→ one bounded blob object materialization
```

## v1.19の正確な意味

v1.19は、exact byte payloadから一つのGit blob objectを作成するか、同一objectが既に存在する場合に再利用します。

入力は、repository path、repository identity、Git-directory fingerprint、v1.18 committed result、executor identity、sandbox marker、payload digest、payload size、candidate blob OIDへ束縛されます。

許可される書込みcommand shapeは次だけです。

```text
git --no-optional-locks -C <repository> hash-object -w --stdin
```

実行後は、object presence、object type、size、content digestを再検証します。

新規objectの書込み後にpostconditionが失敗した場合、結果はERRORのままですが、発生したobject-database mutationはaccountingから消去しません。

v1.19は、reference、index、working tree、reflog、signature、remote、pushを変更しません。

v1.19はtree objectまたはcommit objectを作成しません。

それらはDraft PR #942のv1.20で別権限として開発中です。

## Lean root

`formal/KuuOSFormal.lean`は、`main`へ統合済みの形式層だけを参照するstrict aggregate rootです。

現在はv0.76の後にv0.78からv1.19をimportします。

未統合のv0.77とv1.20はimportしません。

```bash
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KuuOSFormal
```

専用rootは各versionの局所surfaceを検証します。

aggregate rootは、import欠落、未統合moduleの混入、依存順の破綻、境界退行を検出します。

## Runtime root

`scripts/run_kuuos_runtime_full_check_v0_55.py`は、互換名を維持した累積runtime rootです。

legacy surfaceからv0.95までのvalidatorを実行した後、累積v1.19 chainへ接続します。

累積v1.19 chainは、v1.02以前のreference and checkpoint chain、v1.03からv1.18、v1.19 focused testsを依存順に検証します。

```bash
PYTHONPATH=. python3 scripts/run_kuuos_runtime_full_check_v0_55.py
```

v1.19 frontierを直接実行する入口もあります。

```bash
PYTHONPATH=. python3 runtime/kuuos_v119_check.py
```

root成功は、検査対象surfaceの再現可能な整合性receiptです。

真理、外部定理受理、臨床承認、組織承認、任意repositoryへのmutation authority、remote push authorityではありません。

## 開発中frontier

Draft PR #942は、v1.19のblob resultとdeterministic commit candidateを入力として、bounded tree objectと一つのexact commit objectをmaterializeするv1.20を開発しています。

v1.20では、reference、index、working tree、reflog、signing、pushを引き続き禁止します。

PRがmergeされるまでは、v1.20を`main`の統合済み機能、Lake package version、formal aggregate frontier、runtime aggregate frontierとして扱いません。

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
- rollbackによる承認権限または過去状態の復活。
- repository candidate、authorization、modeled transition、receiptの自動的なlive effect化。
- v1.18からbranch、tag、delete、force update、remote push権限への昇格。
- v1.19からtree、commit、reference、index、working-tree write権限への昇格。
- closedまたはopenの未統合proposalを`main`の機能として扱うこと。

## 最初に読む文書

```text
README.md
ROADMAP.md
GOVERNANCE.md
CONTRIBUTING.md
CITATION.cff

formal/KUOS.lean
formal/KuuOSFormal.lean
scripts/run_kuuos_runtime_full_check_v0_55.py

KUUOS_REPOSITORY_ATOMIC_CHECKPOINT_CREATION_v1_02.md
docs/KUUOS_REPOSITORY_BOUNDED_BLOB_v1_19.md
runtime/kuuos_v119_check.py
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
merged artifact != closed or open proposal
```

新しい層は、入力、出力、所有者、必要権限、永続化、replay、stale-state処理、validatorの射程、外部仮定、非権限境界を明記します。

## Citation, governance and rights

引用、貢献、再利用条件は、[`CITATION.cff`](CITATION.cff)、[`GOVERNANCE.md`](GOVERNANCE.md)、[`CONTRIBUTING.md`](CONTRIBUTING.md)、repository license filesを参照してください。

**空OS、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属します。**

個別のrepository artifactの再利用は、各licenseと著作者表示に従います。

Repository artifactは、臨床権限、組織権限、数学的受理、実行権限を移転しません。
