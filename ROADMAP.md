# KuuOS / 空OS Roadmap

**基準日：2026年6月27日**

**公開安定基準：`main` commit `162fae555a2c9a43619eae296b55557dd6f81377`**

この文書は、`main`の統合済み基準、open pull request上の研究前線、外部数学境界、次の統合順序を分離します。

## 状態分類

| 表記 | 意味 |
|---|---|
| 統合済み | `main`に存在し、正式な累積ルートから参照される |
| 検証済み研究前線 | open pull request上で専用検証と必要なaggregate検証を確認したが、`main`には未統合 |
| 検証中 | open pull request上で必要な検証の一部が進行中 |
| 計画 | 仕様または受入条件はあるが、正式実装は未完了 |
| 外部境界 | KuuOS内部だけでは確定しない数学的、物理的、臨床的、制度的入力 |

## 固定境界

```text
candidate != authority
validation != truth
CI pass != external theorem acceptance

observation != verification
verification != truth
learning != present-cycle mutation
memory != belief sovereignty
selection != action

finite local control != global constitutional closure
local chart != global graph
curvature != veto
holonomy != sovereign memory

WORLD sidecar != exact WORLD
WORLD candidate != empirical fact
analytic vacuum != exact WORLD
Kū != zero vector
modular time != physical time

module discovery != activation
connection proposal != state update
curvature decrease != truth
```

すべての段階は、source binding、append-only lineage、replay idempotence、stale-state rejection、所有者分離、反証と不確実性の可視化を保ちます。

## `main`の統合済み基準

| 系列 | 到達点 |
|---|---|
| Core governance | v0.1 |
| Horizon / Context Gauge | v0.12 / v0.13 |
| PlanOS control | v0.17 |
| Finite-cycle agent | v0.20からv0.27 |
| Qi diagnostic lineage | v0.28 / v0.29 |
| Open Horizon | v0.30からv0.34 |
| MemoryOS | v0.35、v0.37、v0.38、v0.39 |
| Qi-WORLD | v2.3 |
| Vacuum-expectation OS chain | VerifyOS v0.3、LearnOS v0.3、PlanOS v0.18からv0.23、ActOS v0.3からv0.4、ObserveOS v0.4 |
| WORLD sidecar | v0.27からv0.59 |
| Lean root | `KuuOSFormal` |
| Runtime root | `run_kuuos_runtime_full_check_v0_55.py` |

2026年6月27日の`main`には、検証workflowの修復が統合されています。

直近の修復は、stable workflow URL、対象path、失敗伝播、診断artifact、重複した全体検証の削減を扱います。

## 現在の研究前線

### 独立した研究枝

| 系列 | PR | 状態 | 主な役割 |
|---|---:|---|---|
| CapabilityOS v0.60 | #832 | 検証済み研究前線 | Qi、陰陽ブロッカー、複数WORLD、MemoryOSからread-only能力候補を構成する |
| Modular Evolution Mesh v0.1 | #836 | 検証済み研究前線 | 型付きmodule registry、依存解決、append-only ledgerを構成する |
| Workflow consolidation | #835 | open | 検証入口を整理し、同じ証明surfaceの重複実行を減らす |

CapabilityOSとModular Evolution Meshは、同じ問題を扱いません。

CapabilityOSは状況依存の能力候補を評価します。

Modular Evolution Meshは、能力moduleを登録し、依存関係と履歴を管理します。

将来の統合では、候補評価とmodule管理の所有権境界を保った接続が必要です。

### ゲージ自己組織化の積層系列

```text
PR #837  Gauge-field self-organization v0.60
→ PR #843  OS-associated gauge fields v0.61
→ PR #844  Gauge connection proposals v0.62
```

| 段階 | 状態 | 内容 |
|---|---|---|
| v0.60 | 検証済み研究前線 | 憲法ゲージ群、局所場、離散接続、曲率、holonomy、有限共変緩和候補 |
| v0.61 | 検証済み研究前線 | ObserveOS、VerifyOS、MemoryOSの局所随伴場、三場曲率、記憶holonomy |
| v0.62 | 検証中 | 有限catalogからの接続候補、曲率非増大、変更量制限、source保持 |

この系列は、普遍グラフを書き換える構造ではありません。

固定された憲法境界と意味チャネルの下で、read-only候補を構成します。

積層PRは依存順に統合します。

上流PRを飛ばして下流PRだけを`main`へ入れません。

## 完了した基盤

### 有限サイクル継続

v0.20からv0.27は、mission binding、観測、複数信念、semantic planning、独立検証、bounded memory、effect reconciliation、resource admission、checkpoint、restart recoveryを接続しました。

各サイクルは有限であり、fresh authorizationと有限leaseを要求します。

### Open Horizon

v0.30からv0.34は、有限局所制御が将来可能性全体を閉じないことを固定しました。

未解決WORLD証拠は、候補、外部承認された観測、独立検証、原子的WORLD fragment commitへ進みます。

WORLD commitは真理権限を生成しません。

### MemoryOS

v0.35はQi process history、blocker context、sourced WORLD generationをappend-only memoryへ統合しました。

v0.37は四層記憶、予測状態候補、contradiction residue、WORLD imaginationを追加しました。

v0.38はWORLD v0.49のOS-Hilbert packetをread-only解析文脈として接続しました。

v0.39はMemoryOS解析capsuleとWORLD v0.50候補をObserveOS owner reviewへ渡します。

### Qi-WORLD

v2.1はfinite-chain inductionを実装しました。

v2.2は具体的な第三licensed cycleを閉じました。

v2.3はQi Process Tensorとcross-cycle blockerを陰陽相補系として接続しました。

### 真空期待値OS連結

```text
WORLD v0.50 candidate
→ WORLD v0.51 ObserveOS intake
→ ObserveOS v0.3
→ VerifyOS v0.3
→ LearnOS v0.3
→ WORLD v0.53 receipt composition
→ PlanOS v0.18からv0.23
→ ActOS v0.3からv0.4
```

実行後効果は、WORLD v0.52とObserveOS v0.4まで統合済みです。

VerifyOSによる事後評価以降は次の課題です。

### WORLD数学サイドカー

`main`の統合済み数学系列はv0.27からv0.59です。

```text
real Hilbert ℓ²
→ self-adjoint operator bridge
→ noncommutative operator algebra
→ C*-local net and von Neumann theory
→ Araki relative entropy
→ Petz recovery
→ Jones theory
→ higher-gauge information geometry
→ quantum Bregman geometry
→ OS Hilbert completion
→ analytic vacuum sector
→ verified Araki calculus
→ closed Tomita operator
→ four-great phase dynamics
```

外部receipt、仮定として供給された構造、Lean直接定理、将来目標を混同しません。

## 直近の優先順位

### 優先1：安定基準の回帰検証

- Core governance、runtime aggregate、WORLD v0.59、MemoryOS v0.39、Qi-WORLD v2.3の入口を維持する。
- `KuuOSFormal`を`warningAsError`と`sorryAsError`で検証する。
- versioned manifestとsource pathの同期を検査する。
- workflow修復が対象外の全体検証を再導入しないことを確認する。

受入条件：

```text
versioned validator success
+ dedicated root success
+ aggregate root success
+ canonical manifest stable
+ no ownership regression
```

### 優先2：ゲージ系列v0.60からv0.62の統合

- PR #837を最初に統合する。
- PR #843をv0.60統合後の`main`へ同期する。
- PR #844をv0.61統合後の`main`へ同期する。
- 各段階でdedicated root、aggregate root、runtime regressionを再確認する。
- source digest、rollback target、固定domain、意味チャネル保存を維持する。

### 優先3：CapabilityOSとModular Evolution Meshの接続設計

- capability candidateとmodule manifestを別型として保つ。
- registry discoveryが能力採用を意味しないことを固定する。
- dependency resolutionがPlanOS採用を意味しないことを固定する。
- ownership conflictとprovider ambiguityをfail closedで扱う。
- MemoryOS retrievalを能力有効化へ自動昇格させない。

### 優先4：実行後効果の観測検証閉路

現在は次まで統合済みです。

```text
bounded effect
→ WORLD v0.52 intake
→ ObserveOS v0.4 observation receipt
```

次の課題は、VerifyOS receipt、future-only LearnOS delta、WORLD disposition、必要時のfresh commit authorizationです。

raw evidence、observation、verification、causal attributionを分離します。

### 優先5：MemoryOS v0.39のowner workflow

- v0.39 read-only intakeをObserveOSのscope判定へ接続する。
- empirical evidenceを別入力として要求する。
- active blocker、contradiction residue、source capsuleを保持する。
- ObserveOS commit後もVerifyOS debtを開いたままにする。

### 優先6：Open Horizonの運用強化

- v0.34 single-host storeを一般化する。
- compare-and-swap、fencing、idempotencyを維持する。
- local holdとconstitutional amendmentを分離する。
- multi-agent formationを候補、承認、採用に分離する。

### 優先7：Tomitaから相対モジュラー解析へ

- closed Tomita operatorからpolar decompositionへ進む。
- relative modular operatorとmodular conjugationの型付き基礎を構成する。
- natural positive cone、standard form、unbounded logarithmの状態分類を明示する。
- 有界生成子のAraki calculusと非有界作用素基礎を分離する。

### 優先8：四大相転移候補

- Earth、Water、Fire、Air間の変換条件をread-only candidateとして定義する。
- order parameter、stability threshold、coarse-graining scale、transport directionを分離する。
- 四大分類と物理的相転移理論を同一視しない。

### 優先9：Qi-WORLD有限prefix

- 任意の有限prefixに対する具体的receipt chainを構成する。
- 各cycleでfresh authority、有限lease、single-use discharge、native closureを確認する。
- closed prefixから次cycleの権限を自動導出しない。

### 優先10：4D Yang–Mills外部数学境界

canonical Lean proof repositoryは`itakura-hidetoshi/4d-mass-gap`です。

PR #282はopenであり、完全な4次元Yang–Mills構成またはmass-gap定理の完了を主張していません。

KuuOS側では次を維持します。

```text
governance consistency
!= theorem closure
!= publication acceptance
!= physical realization
```

## 統合ゲート

研究前線を`main`へ統合する前に、次を確認します。

```text
source files are versioned
manifest is canonical
validator covers declared boundaries
unit tests cover failure classes
dedicated Lean root succeeds
aggregate KuuOSFormal succeeds
runtime regression succeeds when relevant
README and ROADMAP status are updated
research branch is not described as stable main
```

主なfailure class：

- stale digest。
- replay duplication。
- source substitution。
- ownership conflict。
- ambiguous provider。
- memory overwrite。
- local-to-global collapse。
- observation and verification conflation。
- WORLD truth promotion。
- modular-time and physical-time conflation。
- Kū and zero-vector identification。
- stable main and research branch conflation。

## 中期研究方向

### 非マルコフMemoryOS

- scar、relapse、recovery、return-to-contextをchart-local transportへ接続する。
- semantic consolidationがcontradiction residueを消去しないことを保つ。
- predictive stateをlatent truthとして扱わない。
- collective reconstructionでindividual lineageを失わない。

### Context GaugeとGraphRAG

- direct transitionとcomposed transitionを比較する。
- triple-overlap cocycleを検査する。
- path-sensitive holonomyを比較する。
- chart agingとreobservationを追加する。
- universal shortest-path policyへ縮約しない。

### WORLDと物理Hilbert空間

- OS quotient completionの第一原理構成を強化する。
- densely defined self-adjoint Hamiltonian bridgeを型付きで接続する。
- Stone generation、spectral support、cluster propertyの状態を分離する。
- modular timeとphysical timeを分離する。

### 公開再現性

- Leanとmathlib toolchainを固定する。
- deterministic fixtureを維持する。
- canonical manifestをCIで確認する。
- versioned evidence bundleを作る。
- superseded branchとcurrent product branchを明示する。

## 長期方向

```text
claims know their support
observations know their source
beliefs know their uncertainty
memories know their lineage
plans know their owner
effects know their bounded authorization
learning knows it is future-only
WORLD commits know they are not truth
proofs know their formal and external status
local controls know they are not global constitutions
```

長期目標は、無制限な自由を与えることではありません。

権限崩壊を起こさず、関係的連続性、観測可能性、形式的追跡可能性を高めることです。

## 現在の優先順位一覧

```text
1. stable mainの検証入口とaggregate rootsを維持する。
2. ゲージ系列v0.60、v0.61、v0.62を依存順に統合する。
3. CapabilityOSとModular Evolution Meshの責務境界を接続する。
4. 実行後効果のObserveOS、VerifyOS、LearnOS、WORLD dispositionを閉じる。
5. MemoryOS v0.39をObserveOS owner workflowへ接続する。
6. Open Horizon v0.34のstoreを一般化する。
7. closed Tomita operatorから相対モジュラー解析へ進む。
8. 四大の相転移候補条件をread-only形式で定理化する。
9. Qi-WORLDの任意有限prefixを具体的receipt chainとして構成する。
10. 4D Yang–Millsの外部数学境界を正確に保つ。
```
