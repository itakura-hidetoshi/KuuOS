# KuuOS / 空OS

![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)
![MemoryOS v0.39](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/memoryos-world-observe-intake-v0-39.yml/badge.svg)
![Qi-WORLD v2.3](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/qi-world-yinyang-process-blocker-v2-3-validation.yml/badge.svg)
![WORLD v0.52](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/world-host-effect-intake-v0-52.yml/badge.svg)

**KuuOS / 空OS**は、観測、信念、記憶、計画、判断、実行、学習、WORLD表現を、独立した真理や恒久権限ではなく、由来、文脈、履歴、所有者、境界に拘束された局所候補として扱う公開研究アーキテクチャです。

KuuOS is a public, governance-gated, proof-facing, non-Markovian, Qi-process-aware architecture for relational AI systems.

## 現在の状態

**基準日：2026年6月26日**

`main`の安定基準と、未統合の研究前線を分けて表示します。

### mainの統合済み基準

| 系列 | 現在の統合済み到達点 |
|---|---|
| 中核ガバナンス | v0.1 |
| Horizon Governance / Context Gauge Atlas | v0.12 / v0.13 |
| PlanOS制御系列 | v0.17 |
| 有限サイクル自律エージェント | v0.27 |
| 気の診断候補と系譜 | v0.28 / v0.29 |
| Open Horizon | v0.30からv0.34 |
| MemoryOS | v0.35、v0.37、v0.38、v0.39 |
| Qi-WORLD | v2.3 |
| 真空期待値OS連結 | VerifyOS v0.3、LearnOS v0.3、PlanOS v0.18からv0.23、ActOS v0.3からv0.4、ObserveOS v0.4 |
| WORLD数学サイドカー | v0.52 |
| Lean統合ルート | `KuuOSFormal` |
| 累積ランタイム検証 | `scripts/run_kuuos_runtime_full_check_v0_52.py` |
| Lean / mathlib | Lean 4、mathlib `v4.30.0-rc2` |

### 未統合の研究前線

次のWORLD系列は積み上げ型の開発ブランチにあり、`main`へ統合済みとは扱いません。

```text
WORLD v0.53
OS receipt composition bridge

WORLD v0.54
Kū vacuum central reference state

WORLD v0.55
Kū vacuum information geometry

WORLD v0.56
verified Araki calculus and OS transport

WORLD v0.57
closed Tomita operator bridge

WORLD v0.59
four-great phase dynamics
```

各段階は、個別のPR、専用検証、厳格Lean build、上流ブランチとの整合が確認されてから、順番に安定基準へ移します。

## 中心命題

```text
candidate != authority
validation != truth
formal compilation != external theorem acceptance

observation != verification
verification != truth
learning != present-cycle mutation
memory != belief sovereignty
plan commit != activation
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

diagnostic candidate != final diagnosis
recovery-window interval != healing guarantee
```

空OSの中心は、AIを単に強く自律化することではありません。

候補、観測、検証、記憶、計画、権限、効果、数学的表現の身分を分離し、縁起、二諦、中道、和、局所性、履歴を保ったまま接続することです。

## 所有権境界

```text
ObserveOS
= observation ownership

BeliefOS
= local and plural belief-state ownership

DecisionOS
= admissible candidate selection

PlanOS
= plan and replan synthesis

ActOS
= exactly licensed bounded effect

VerifyOS
= evidence-bound independent verification

LearnOS
= future-only learning delta

MemoryOS
= lineage, reconstruction and conditioned retrieval

WORLD
= sourced world representation and governed fragment storage
```

```text
ObserveOS evidence != VerifyOS verdict
VerifyOS verdict != truth authority
LearnOS delta != immediate activation
DecisionOS selection != ActOS invocation
MemoryOS retrieval != PlanOS activation
WORLD intake != WORLD update
```

## 現在の主要スパイン

### ガバナンスと局所文脈

KuuOSは文脈を普遍グラフの固定ノードではなく、局所チャートとして扱います。

```text
context
→ local chart

policy state
→ local section

compatible relation
→ chart overlap

context change
→ transition function

section movement
→ parallel transport

disagreement
→ curvature / cocycle defect

path-dependent retained history
→ holonomy
```

Horizon v0.12とContext Gauge Atlas v0.13は、複数時間幅、局所性、曲率、cocycle residue、非マルコフ履歴を保持します。

### 有限サイクルと開いた将来

v0.20からv0.27は、再起動可能で、利用者が中断でき、資源境界を持つ反復可能な有限サイクルを構成します。

```text
mission
→ observation and plural belief
→ semantic planning and independent verification
→ bounded memory and learning
→ transactional effect reconciliation
→ event wake-up and resource admission
→ governed change management
→ exact checkpoint and next finite cycle
```

v0.30は、有限サイクルの局所制御を、将来可能性を閉じる全体憲法へ昇格させない境界を追加します。

```text
finite local control != permanent global ceiling
paused instance != closed future horizon
terminated instance != termination of successor possibility
```

### 観測からWORLDコミットまで

v0.31からv0.34は、未解決WORLD証拠を候補化し、外部承認された観測と独立検証を経て、単一のWORLD fragmentを原子的に更新する経路を実装します。

```text
v0.31 unresolved WORLD evidence
→ plural mission candidates
→ plural observation candidates

v0.32 external single-use observation authorization
→ provenance-complete ObserveOS evidence
→ WORLD feedback candidate

v0.33 independent VerifyOS assessment
→ adopt / reject / defer / reobserve candidate

v0.34 fresh commit authorization
→ optimistic concurrency and fencing
→ one atomic WORLD-fragment commit
→ immutable receipt
```

v0.34の参照実装は単一ホストPOSIX adapterです。

WORLD fragmentの更新は、憲法根、過去履歴、真理権限、因果権限を更新しません。

### MemoryOS

MemoryOSは、履歴を保存するだけでなく、予測候補、矛盾残渣、ブロッカー、解析的文脈を分離して保持します。

```text
v0.35
Qi process history
+ blocker context
+ sourced WORLD generation
→ append-only conditioned memory

v0.37
four-layer memory
+ observable predictive-state candidate
+ contradiction residue
+ counterfactual WORLD imagination
→ blocker-shielded read-only retrieval

v0.38
MemoryOS predictive capsule
+ supplied WORLD v0.49 OS-Hilbert packet
→ read-only analytic Hilbert context

v0.39
MemoryOS analytic capsule
+ WORLD v0.50 observation candidate
→ ObserveOS owner-review intake
```

v0.39はraw evidence、ObserveOS commit、VerifyOS resultを生成しません。

### 気のプロセスとQi-WORLD

v0.28は、複数時点の気のプロセステンソル、複数仮説、反証、回復可能性区間を診断候補として保持します。

v0.29は、その候補を正確なsource lineageへ束縛します。

Qi-WORLD v2.1は有限multi-cycle chain inductionを持ち、v2.2は具体的な第三 licensed cycleを閉じます。

v2.3は気のプロセスとブロッカー理論を陰陽相補系として接続します。

```text
Yang
= accumulable process support

Yin
= idempotent boundary occupation

coupled admissibility
= process visibility
+ continuity
+ memory continuity
+ required blockers
+ capacity
+ context
```

この構造は、気を物理的ボース粒子へ、ブロッカーを物理的フェルミ粒子へ同一視しません。

### 真空期待値から実行後観測まで

`main`には、解析的WORLD候補と実行後効果を混同しない二つの経路があります。

```text
analytic route

WORLD v0.50 vacuum-expectation candidate
→ WORLD v0.51 ObserveOS evidence-intake envelope
→ ObserveOS v0.3 supplied commit receipt
→ VerifyOS v0.3 supplied verification receipt
→ LearnOS v0.3 future-only delta
→ PlanOS v0.18からv0.23
→ ActOS v0.3からv0.4
```

```text
host-effect route

ActOS v0.4 canonical effectRecorded receipt
→ WORLD v0.52 host-effect intake candidate
→ ObserveOS v0.4 effect-grounded observation receipt
→ future VerifyOS and WORLD disposition
```

WORLD v0.52は観測、検証、WORLD更新を実行しません。

ObserveOS v0.4は、解析的真空期待値候補をActOSのhost effectとして扱いません。

### WORLD数学サイドカー

統合済み数学サイドカーはv0.27からv0.52です。

```text
real Hilbert ℓ²
→ dense and self-adjoint operator bridge
→ noncommutative operator algebra
→ C*-local net
→ von Neumann bicommutant and modular theory
→ Araki relative entropy
→ Petz recovery and conditional expectation
→ Jones basic construction and tower
→ standard invariant, Q-system and fusion bridges
→ categorical IndraNet and higher-gauge information geometry
→ quantum dual-affine and Bregman geometry
→ mirror descent, JKO and entropy-production certificates
→ finite log-Sobolev contraction bounds
→ OS reflection-positive Hilbert completion interface
→ analytic vacuum sector
→ vacuum-expectation observation candidates
→ ObserveOS intake
→ host-effect intake
```

Leanは、宣言された型付き帰結を検証します。

CI成功だけでは、外部数学界での定理受理、物理実現、経験的妥当性は成立しません。

## 実装済み

- 公開ガバナンス、非権限境界、医療モダリティ中立境界。
- State IO、allowlist、receipt、JSONL ledger、replay、stale-state rejection。
- ObserveOS、BeliefOS、DecisionOS、PlanOS、ActOS、VerifyOS、LearnOS、MemoryOSの所有権分離。
- 有限サイクル継続、Open Horizon、外因的観測承認、VerifyOS disposition、原子的WORLD commit。
- 気のプロセステンソル、診断候補、系譜束縛、Qi-WORLD finite-chain、陰陽ブロッカー相補系。
- 四層記憶、予測状態候補、矛盾残渣、WORLD imagination、blocker-shielded retrieval。
- OS Hilbert解析文脈とWORLD候補のObserveOS owner-review intake。
- WORLD v0.52までのPython validator、manifest、workflow、Lean formal surface。
- `KuuOSFormal`に集約された厳格Lean build surface。

## 非主張

KuuOSは現時点で次を主張しません。

- 無制限の実行権限を持つproduction AGI。
- 任意のshell、network、repository、deploymentへの包括権限。
- 単一の真理へ収束する普遍的global-context graph。
- 独立した医療診断、トリアージ、治療、医療行為承認システム。
- 気が物理的粒子であることの証明。
- LeanまたはCIの成功だけによる外部定理受理。
- 完全な物理的量子Markov semigroup、正確な物理真空、正確なWORLD simulator。
- 解析的真空と形而上学的な空の同一視。
- 観測候補、検証結果、記憶、WORLD commit、receiptの真理権限化。
- `main`へ未統合のWORLD v0.53以降を安定リリースとして扱うこと。

## 最初に読む文書

```text
README.md
ROADMAP.md
GOVERNANCE.md
CONTRIBUTING.md

docs/KUOS_CORE_GOVERNANCE_INDEX_v0_1.md
docs/BOUNDARY_AND_NONAUTHORITY_POLICY_v0_1.md

docs/KUUOS_OPEN_ENDED_BACKGROUND_AGENCY_v0_30.md
docs/KUUOS_ENDOGENOUS_MISSION_OBSERVATION_v0_31.md
docs/KUUOS_AUTHORIZED_OBSERVATION_WORLD_FEEDBACK_v0_32.md
docs/KUUOS_VERIFYOS_WORLD_ADOPTION_v0_33.md
docs/KUUOS_AUTHORIZED_ATOMIC_WORLD_COMMIT_v0_34.md

docs/KUUOS_MEMORYOS_QI_WORLD_BLOCKER_INTEGRATION_v0_35.md
docs/KUUOS_MEMORYOS_PREDICTIVE_SHIELDED_MEMORY_v0_37.md
docs/KUUOS_MEMORYOS_ANALYTIC_HILBERT_CONTEXT_v0_38.md
docs/KUUOS_MEMORYOS_WORLD_OBSERVE_INTAKE_v0_39.md

docs/KUUOS_QI_RECOVERY_WINDOW_DIAGNOSTIC_v0_28.md
docs/KUUOS_QI_CANDIDATE_LINEAGE_BINDING_v0_29.md
docs/KUUOS_QI_WORLD_YINYANG_PROCESS_BLOCKER_COMPLEMENTARITY_v2_3.md

docs/KU_WORLD_KUU_VACUUM_OS_HILBERT_COMPLETION_v0_49.md
docs/KU_WORLD_VACUUM_EXPECTATION_OBSERVATION_CANDIDATE_v0_50.md
docs/KU_WORLD_VACUUM_EXPECTATION_OBSERVEOS_EVIDENCE_INTAKE_v0_51.md
docs/KU_WORLD_HOST_EFFECT_INTAKE_v0_52.md

formal/KUOS.lean
formal/KuuOSFormal.lean
```

## 検証

```bash
make core-governance-checks
make all-governance-checks

python3 scripts/run_kuuos_runtime_full_check_v0_52.py

PYTHONPATH=. python scripts/check_memoryos_world_observe_intake_v0_39.py
PYTHONPATH=. python scripts/check_qi_world_yinyang_process_blocker_complementarity_v2_3.py
python3 scripts/check_world_vacuum_expectation_host_effect_intake_v0_52.py
python3 scripts/check_observeos_world_host_effect_observation_v0_4.py

lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KuuOSFormal
```

検証成功は再現可能な整合性receiptです。

真理、外部定理受理、臨床承認、組織承認、無制限の実行許可ではありません。

## ディレクトリ

```text
docs/         public specifications, boundaries and status documents
runtime/      bounded runtime kernels, adapters, stores and scenarios
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
stable main != active research branch
```

新しい層は、入力、出力、所有者、必要権限、永続化、replay、stale-state処理、validatorの射程、外部仮定、非権限境界を明記します。

## Citation, governance and rights

引用、貢献、再利用条件は、[`CITATION.cff`](CITATION.cff)、[`GOVERNANCE.md`](GOVERNANCE.md)、[`CONTRIBUTING.md`](CONTRIBUTING.md)、repository license filesを参照してください。

KuuOS / 空OSと、板倉英俊が公開した名称付きtensorおよびOS構成を含む独自アーキテクチャは、記載された著作者表示と権利表示を保持します。

Repository artifactは、臨床権限、組織権限、数学的受理、実行権限を移転しません。
