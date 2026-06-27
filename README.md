# KuuOS / 空OS

![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)
![MemoryOS v0.39](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/memoryos-world-observe-intake-v0-39.yml/badge.svg)
![Qi-WORLD v2.3](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/qi-world-yinyang-process-blocker-v2-3-validation.yml/badge.svg)
![WORLD v0.59](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/world-four-great-phase-dynamics-v0-59.yml/badge.svg)

**KuuOS / 空OS**は、観測、信念、記憶、計画、判断、学習、WORLD表現を、由来、文脈、履歴、所有者、有限の許可に拘束された局所候補として扱う公開研究アーキテクチャです。

KuuOS is a public, governance-gated, proof-facing, non-Markovian and Qi-process-aware architecture for relational AI systems.

目的は、候補、検証、記憶、権限、数学的表現を分離したまま接続し、縁起、二諦、中道、和、局所性、履歴、反証可能性を保つことです。

## 現在地

**基準日：2026年6月27日**

**公開安定基準：`main` commit `162fae555a2c9a43619eae296b55557dd6f81377`**

「統合済み」は`main`に存在する機能を意味します。

open pull request上の機能は、検証済みであっても研究前線として分離します。

| 系列 | `main`の到達点 |
|---|---|
| Core governance | v0.1 |
| Horizon Governance / Context Gauge Atlas | v0.12 / v0.13 |
| PlanOS control | v0.17 |
| Repeatable finite-cycle agent | v0.20からv0.27 |
| Qi diagnostic candidate / lineage | v0.28 / v0.29 |
| Open Horizon | v0.30からv0.34 |
| MemoryOS | v0.35、v0.37、v0.38、v0.39 |
| Qi-WORLD | v2.3 |
| Vacuum-expectation OS chain | VerifyOS v0.3、LearnOS v0.3、PlanOS v0.18からv0.23、ActOS v0.3からv0.4、ObserveOS v0.4 |
| WORLD mathematical sidecar | v0.27からv0.59 |
| Lean aggregate root | `KuuOSFormal` |
| Runtime aggregate root | `scripts/run_kuuos_runtime_full_check_v0_55.py` |
| Lean / mathlib | Lean 4、mathlib `v4.30.0-rc2` |

`run_kuuos_runtime_full_check_v0_55.py`は互換性を保った累積入口の名称です。

名称中のv0.55は、リポジトリ全体の最新機能番号を意味しません。

PR #834およびPR #838からPR #842までの検証workflow修復は`main`へ統合済みです。

## 研究前線

| 系列 | Pull request | 状態 |
|---|---:|---|
| CapabilityOS v0.60 | #832 | open。専用検証とaggregate Lean検証を確認済み |
| Modular Evolution Mesh v0.1 | #836 | open。専用検証とaggregate Lean検証を確認済み |
| Gauge-field self-organization v0.60 | #837 | open。専用検証とaggregate Lean検証を確認済み |
| OS-associated gauge fields v0.61 | #843 | PR #837上のstacked PR |
| Gauge connection proposals v0.62 | #844 | PR #843上のstacked PR。現在headの必要検証は進行中 |
| Workflow consolidation | #835 | open。検証基盤の整理 |

正確なhead、検証結果、stacked dependencyは各pull requestを基準とします。

## 中心命題

```text
candidate != authority
validation != truth
formal compilation != external theorem acceptance

observation != verification
verification != truth
learning != present-cycle mutation
memory != belief sovereignty
selection != action

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

研究前線では次も固定します。

```text
module discovery != activation
dependency resolution != policy adoption
self-organization proposal != automatic adoption

gauge covariance != authority expansion
connection proposal != state update
curvature decrease != truth
Wilson observable != policy authority
```

## OSの責務

| OS | 主な責務 |
|---|---|
| ObserveOS | source-bound observation |
| BeliefOS | local and plural belief state |
| DecisionOS | admissible candidate selection |
| PlanOS | plan and replan synthesis |
| ActOS | exactly licensed bounded effect |
| VerifyOS | evidence-bound independent verification |
| LearnOS | future-only learning delta |
| MemoryOS | lineage、reconstruction、conditioned retrieval |
| WORLD | sourced representation and governed fragment storage |

観測は検証ではなく、検証は真理権限ではありません。

記憶検索は計画採用ではなく、計画選択は効果の許可ではありません。

## 統合済みの主要経路

### 有限サイクルとOpen Horizon

v0.20からv0.27は、再起動可能で、利用者が中断でき、資源境界を持つ反復可能な有限サイクルを構成します。

```text
persistent mission
→ evidence-bearing cognitive cycle
→ bounded effect
→ independent WORLD reconciliation
→ bounded learning and memory
→ checkpoint / pause / renew / terminate / handover
```

v0.30からv0.34は、有限局所制御が将来可能性全体を閉じないことを固定します。

### MemoryOS

```text
v0.35  Qi process history and blocker context
v0.37  four-layer predictive shielded memory
v0.38  read-only WORLD v0.49 OS-Hilbert context
v0.39  WORLD v0.50 candidate to ObserveOS owner-review intake
```

MemoryOSはraw evidence、ObserveOS commit、VerifyOS result、PlanOS activationを自動生成しません。

### Qi Process TensorとQi-WORLD

v0.28は、複数時点のQi Process Tensor、複数仮説、反証、不確実性、回復可能性区間を診断候補として保持します。

v0.29は、その候補を正確なsource lineageへ束縛します。

Qi-WORLD v2.3は、気のプロセスとcross-cycle blockerを陰陽相補系として接続します。

```text
Yang = accumulable process support
Yin  = idempotent boundary occupation
```

この構造は、気を物理的ボース粒子へ、ブロッカーを物理的フェルミ粒子へ同一視しません。

### 真空期待値OS連結

```text
WORLD v0.50 candidate
→ WORLD v0.51 ObserveOS intake
→ ObserveOS v0.3 receipt
→ VerifyOS v0.3 receipt
→ LearnOS v0.3 future-only delta
→ WORLD v0.53 receipt composition
→ PlanOS v0.18からv0.23
→ ActOS v0.3からv0.4
```

実行後効果は別経路で、WORLD v0.52とObserveOS v0.4へ接続されます。

### WORLD数学サイドカー

```text
real Hilbert ℓ²
→ self-adjoint operator bridge
→ noncommutative operator algebra
→ C*-local net and von Neumann theory
→ Araki relative entropy and Petz recovery
→ Jones theory and categorical bridges
→ higher-gauge information geometry
→ quantum Bregman and variational geometry
→ OS reflection-positive Hilbert completion
→ analytic vacuum sector
→ Kū vacuum information geometry
→ verified Araki calculus and OS transport
→ closed Tomita operator bridge
→ four-great phase dynamics
```

Leanは、宣言された型と仮定の下で、リポジトリ内の定理を検証します。

CI成功だけでは、外部数学界での定理受理、物理実現、経験的妥当性は成立しません。

## ゲージ自己組織化の研究方向

未統合のv0.60からv0.62は、空OSの自己組織化を、固定された憲法境界上の局所場、接続、曲率、holonomyとして構成します。

```text
constitutional gauge group
→ local context fields
→ discrete connection
→ covariant transport
→ plaquette holonomy
→ Wilson-type observables
→ finite candidate catalog
→ read-only connection proposal
```

ObserveOS、VerifyOS、MemoryOSは、意味チャネルを保つ局所随伴場として射影されます。

接続候補は、変更量、曲率、source digest、rollback targetを検査します。

候補が存在しない場合はsource connectionを保持します。

## Canonical Lean proof boundary

4次元Yang–Mills構成とmass gapに向かうcanonical Lean proof repositoryは、[`itakura-hidetoshi/4d-mass-gap`](https://github.com/itakura-hidetoshi/4d-mass-gap)です。

KuuOSは同リポジトリを参照しますが、置き換えません。

同リポジトリのPR #282は2026年6月27日時点でopenです。

そのPRは完全な4次元Yang–Mills構成またはmass-gap定理の完了を主張していません。

## 検証

```bash
make core-governance-checks
make all-governance-checks

python3 scripts/run_kuuos_runtime_full_check_v0_55.py
python3 scripts/check_world_four_great_phase_dynamics_v0_59.py

lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KuuOSFormal
```

検証成功は再現可能な整合性receiptです。

真理、外部定理受理、臨床承認、組織承認を意味しません。

## 最初に読む文書

```text
README.md
ROADMAP.md
GOVERNANCE.md
CONTRIBUTING.md
docs/KUOS_CORE_GOVERNANCE_INDEX_v0_1.md
docs/BOUNDARY_AND_NONAUTHORITY_POLICY_v0_1.md
docs/KUUOS_AUTONOMOUS_AGENT_STATUS_v0_27.md
docs/LEAN_COVERAGE_MAP_v0_1.md
formal/KUOS.lean
formal/KuuOSFormal.lean
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
stable main != active research branch
```

## Citation, governance and rights

引用、貢献、再利用条件は、[`CITATION.cff`](CITATION.cff)、[`GOVERNANCE.md`](GOVERNANCE.md)、[`CONTRIBUTING.md`](CONTRIBUTING.md)、repository license filesを参照してください。

空OS、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は、板倉英俊（Hidetoshi Itakura）に帰属します。

Repository artifactは、臨床権限、組織権限、数学的受理、運用権限を移転しません。
