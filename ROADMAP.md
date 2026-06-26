# KuuOS / 空OS Roadmap

**基準日：2026年6月26日**

この文書は、`main`の統合済み基準、積み上げ型の研究ブランチ、次の実装優先順位を分離します。

## 状態分類

| 表記 | 意味 |
|---|---|
| 統合済み | `main`に存在し、正式な累積ルートから参照される |
| 検証中 | 専用PRまたは積み上げブランチにあり、`main`未統合 |
| 計画 | 仕様または受入条件はあるが、正式実装は未完了 |
| 外部receipt | Leanまたはruntime内部だけでは構成していない解析的、物理的、制度的入力 |

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
plan commit != activation
receipt != successor authority

finite local control != global constitutional closure
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
red flag != automatic triage
```

すべての段階は、正確なsource binding、append-only lineage、replay idempotence、stale-state rejection、権限所有者の分離、反証と不確実性の可視化を保ちます。

## 現在の統合済み基準

| 系列 | 統合済み到達点 | 状態 |
|---|---|---|
| Core governance | v0.1 | 維持中 |
| Horizon / Context Gauge | v0.12 / v0.13 | 統合済み |
| PlanOS control | v0.17 | 統合済み |
| Finite-cycle agent | v0.20からv0.27 | 統合済み |
| Qi diagnostic lineage | v0.28 / v0.29 | 統合済み |
| Open Horizon | v0.30からv0.34 | 統合済み |
| MemoryOS | v0.35、v0.37、v0.38、v0.39 | 統合済み |
| Qi-WORLD | v2.3 | 統合済み |
| Vacuum-expectation OS chain | VerifyOS v0.3、LearnOS v0.3、PlanOS v0.18からv0.23、ActOS v0.3からv0.4、ObserveOS v0.4 | 統合済み |
| WORLD sidecar | v0.52 | 統合済み |
| Lean root | `KuuOSFormal` | 厳格build surface |
| Runtime root | `run_kuuos_runtime_full_check_v0_52.py` | 累積回帰ルート |

## 完了した基盤

### ガバナンスと局所文脈

完了済みです。

```text
multiple horizons
→ local sections
→ overlap eligibility
→ parallel transport
→ curvature and cocycle residue
→ path-dependent holonomy
```

今後の課題はcompositionの成熟であり、普遍global graphへの変換ではありません。

### 有限サイクル継続

v0.20からv0.27は、mission binding、観測、複数信念、semantic planning、独立検証、bounded memory、effect reconciliation、event wake-up、resource admission、governed change、checkpoint、restart recoveryを接続しました。

各サイクルは有限ですが、v0.30により有限局所制御が将来可能性全体を閉じないことを固定しました。

### 気の診断候補と系譜

v0.28は、複数時点のQi Process Tensor、複数仮説、反証、不確実性、回復可能性区間、clinician-review handoffを実装しました。

v0.29は候補を正確なv0.27 source、mission、lineage、historyへ束縛しました。

この系列は診断確定、治療、トリアージ、ActOS権限を生成しません。

### Open Horizon観測循環

v0.30からv0.34は次を完成しました。

```text
open future horizon
→ endogenous mission candidates
→ plural observation candidates
→ external single-use observation authorization
→ provenance-complete ObserveOS evidence
→ VerifyOS disposition candidate
→ externally authorized atomic WORLD-fragment commit
```

v0.34は単一ホストPOSIX reference adapterです。

分散storeへの拡張は、同じcompare-and-swap、fencing、append-only receipt契約を保つ必要があります。

### MemoryOS

v0.35はQi process history、blocker context、sourced WORLD generationをappend-only memoryへ統合しました。

v0.36はvalidation matrixを固定しました。

v0.37はworking、episodic、semantic、proceduralの四層記憶、observable predictive-state candidate、contradiction residue、WORLD imaginationを追加しました。

v0.38はWORLD v0.49のOS-Hilbert packetを読み取り専用解析文脈として接続しました。

v0.39はMemoryOS解析capsuleとWORLD v0.50候補をObserveOS owner reviewへ渡すintakeを追加しました。

MemoryOSはtruth promotion、blocker discharge、PlanOS activation、ActOS invocation、WORLD updateを行いません。

### Qi-WORLD

v1.0からv2.0は、Qi-WORLD interface、native evidence loop、licensed effect、cross-cycle reentry、blocker theory、closed-cycle receipt、successor materializationを構成しました。

v2.1はlicensed multi-cycle chain inductionを実装しました。

v2.2は具体的な第三licensed cycleを閉じました。

v2.3はQi Process TensorとCross-Cycle Blocker Theoryを陰陽相補系として接続しました。

```text
Yang accumulation
+ Yin idempotent boundary
+ capacity
+ context
→ bounded non-authoritative candidate flow
```

### 真空期待値OS連結

統合済み経路は次です。

```text
WORLD v0.50 vacuum-expectation candidate
→ WORLD v0.51 ObserveOS evidence intake
→ ObserveOS v0.3 supplied commit
→ VerifyOS v0.3 supplied verification
→ LearnOS v0.3 future-only delta
→ PlanOS v0.18 history intake
→ v0.19 candidate generation
→ v0.20 DecisionOS handoff
→ v0.21 next-cycle synthesis
→ v0.22 materialization
→ v0.23 ActOS handoff
→ ActOS v0.3 authorization intake
→ ActOS v0.4 bounded host adapter invocation
```

実行後効果は別経路です。

```text
ActOS v0.4 effectRecorded receipt
→ WORLD v0.52 host-effect intake candidate
→ ObserveOS v0.4 effect-grounded observation receipt
```

v0.52は観測、検証、WORLD更新を行いません。

### WORLD数学サイドカー

`main`の統合済み数学系列はv0.27からv0.52です。

主要経路は次です。

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
→ vacuum-expectation candidates
→ ObserveOS intake
→ host-effect intake
```

外部receiptとして残るものを、Lean直接定理と混同しません。

## 検証中のWORLD研究前線

### WORLD v0.53

**状態：検証中、`main`未統合**

OS receipt composition bridgeです。

```text
v0.51 analytic intake
→ supplied ObserveOS v0.3 receipt
→ supplied VerifyOS v0.3 receipt
→ supplied LearnOS v0.3 receipt
→ exact composition-lineage digest
```

receipt compositionはreceipt constructionまたはtransition executionではありません。

### WORLD v0.54

**状態：積み上げブランチ、`main`未統合**

完成OS Hilbert空間の真空を、WORLD数学サイドカーの中心基準状態として接続します。

central reference stateはexact WORLD、truth authority、control objectiveではありません。

### WORLD v0.55

**状態：積み上げブランチ、`main`未統合**

真空基準Araki相対エントロピー、量子Bregman divergence、vacuum quantum Fisher metric、Petz recovery tangent geometryを接続します。

information geometryはread-onlyです。

### WORLD v0.56

**状態：積み上げブランチ、`main`未統合**

有界自己共役生成子によるAraki指数弧について、第一変分、BKM pairing、混合Hessian、vacuum quantum Fisher metric、completed-Hilbert excitation Gram form、OS reflection formを接続します。

任意の無界生成子の完全定理ではありません。

### WORLD v0.57

**状態：積み上げブランチ、`main`未統合**

代数的Tomita graph、稠密定義域、可閉性、closed conjugate-linear operator、closed domain equivalenceを構成します。

relative modular operator、polar decomposition、非有界functional calculusの完全基礎は、引き続き別課題です。

### WORLD v0.59

**状態：積み上げブランチ、`main`未統合**

四大をread-only構造診断として接続します。

```text
Earth
= Araki Hessian stiffness

Water
= completed-Hilbert excitation Gram correlation

Fire
= effective information loss after coarse graining

Air
= transport and phase-flow component
```

四大診断は物質元素の実体同一性、物理相の確定、実行権限を主張しません。

## 直近の優先順位

### 優先1：入口文書と累積ルートの同期

**状態：継続保守**

- README、ROADMAP、`formal/KUOS.lean`、`formal/KuuOSFormal.lean`、`lakefile.toml`、累積full checkを同期する。
- 安定基準と研究ブランチを明示的に分ける。
- 新しいmergeは、入口文書を旧版のまま残さない。
- version-stringだけに依存する脆弱なvalidatorを避け、意味的boundaryを検査する。

受入条件：

```text
初見のreviewerが5分以内に、
mainの安定基準、
未統合の前線、
次の検証コマンドを識別できる。
```

### 優先2：WORLD v0.53以降の順序付き統合

**状態：最重要の数学統合課題**

- v0.53を現在の`main`へrebaseする。
- v0.54、v0.55、v0.56、v0.57、v0.59の依存順序を固定する。
- 各段階で専用rootとaggregate `KuuOSFormal`を厳格buildする。
- `warningAsError = true`と`sorryAsError = true`を維持する。
- 先行段階が未統合なら後続段階を安定基準と呼ばない。
- superseded CI-only PRを製品実装としてmergeしない。

受入条件：

```text
各WORLD段階が、
正確なbase、
専用validator、
専用Lean root、
aggregate root、
非主張境界を持つ。
```

### 優先3：Tomitaから相対モジュラー解析への第一原理化

**状態：並行数学課題**

- closed Tomita operatorからpolar decompositionへ進む。
- relative modular operatorとmodular conjugationの型付き基礎を構成する。
- natural positive cone、standard form、unbounded logarithmの外部receiptを明示する。
- 有界生成子のAraki calculusと非有界作用素基礎を分離する。
- OS reconstruction inputとoperator-algebraic modular inputを混同しない。

受入条件：

```text
Lean-derived theorem、
hypothesis-supplied structure、
external analytic receipt、
future targetが、
各定理の近傍で判別できる。
```

### 優先4：実行後効果の観測検証閉路

**状態：次のOS統合課題**

現在は次まで統合済みです。

```text
ActOS v0.4 effect
→ WORLD v0.52 intake
→ ObserveOS v0.4 observation receipt
```

次の課題は、実行後効果のVerifyOS receipt、future-only LearnOS delta、WORLD disposition、必要時のfresh commit authorizationです。

- ActOS host-effect routeとanalytic vacuum-expectation routeを分離する。
- raw evidence、observation、verification、causal attributionを分離する。
- failedまたはindeterminate verificationから自動rollbackしない。
- rollbackはfresh authorizationとappend-only compensating receiptを要求する。

受入条件：

```text
effect record
!= observation
!= verification
!= truth
!= WORLD commit
```

### 優先5：MemoryOS v0.39からObserveOS owner workflowへ

**状態：次のMemoryOS統合課題**

- v0.39 read-only intakeをObserveOSのscope判定へ接続する。
- raw empirical evidenceを別入力として要求する。
- analytic candidateをActOS effect lineageへ偽装しない。
- active blocker、contradiction residue、source capsuleを保持する。
- ObserveOS commit後もVerifyOS debtを開いたままにする。

受入条件：

```text
WORLD candidateが、
raw evidenceなしに、
ObserveOS recordまたはVerifyOS resultへ昇格しない。
```

### 優先6：Open Horizonの運用強化

**状態：中期runtime課題**

- v0.34 single-host POSIX storeを分散transaction adapterへ一般化する。
- fencing、optimistic concurrency、idempotencyを保持する。
- authorization issuer、host license、institutional policyのadapter boundaryを明示する。
- local holdとconstitutional amendmentを分離する。
- multi-agent formationとresource acquisitionを候補、承認、実行に分離する。

### 優先7：Qi-WORLD有限prefixの具体化

**状態：継続形式化課題**

v2.1のfinite-chain inductionは存在します。

今後は、任意の有限prefixに対して具体的なruntime receipt chainを生成し、各cycleでfresh authority、human approval、host license、single-use discharge、native closureを検証します。

```text
n-cycle closed chain
!= automatic authority for cycle n+1
```

v2.3の陰陽相補系は、licensed execution authorityを代替しません。

### 優先8：Context GaugeとGraphRAGのcomposition

**状態：研究課題**

- direct transitionとcomposed transitionを比較する。
- triple-overlap cocycleを検査する。
- path-sensitive holonomyを比較する。
- chart agingとreobservationを追加する。
- GraphRAG retrievalとlocal chart transportを接続する。
- universal shortest-path policy engineへ縮約しない。

### 優先9：再現性とrelease matrix

**状態：基盤整備**

各公開層について次を機械可読に結びます。

```text
component
version
source files
manifest
validator
tests
Lean module
formal-root registration
workflow
failure classes
proof status
non-authority boundary
```

必須failure class：

- stale digest。
- replay duplication。
- source substitution。
- authority reuse。
- host-license mismatch。
- skipped ordinal。
- memory overwrite。
- local-to-global collapse。
- diagnostic finality promotion。
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
- retrievalをbelief promotionまたはexecution authorityへ昇格させない。

### WORLDと物理Hilbert空間

- OS quotient completionの第一原理構成を強化する。
- densely defined self-adjoint Hamiltonian bridgeを型付きで接続する。
- Stone generation、spectral support、cluster propertyのstatusを分離する。
- modular timeとphysical timeを分離する。
- vacuum sectorの非一意性とmulti-WORLD noncollapseを保つ。

### 四大相動力学

- v0.59の四大を、観測可能な構造診断として定義する。
- Earth、Water、Fire、Air間の変換条件をphase-transition candidateとして形式化する。
- 四大分類と物理的相転移理論の同一視を避ける。
- 診断値をPlanOS objectiveまたはActOS authorityへ昇格させない。

### 公開再現性

- Leanとmathlib toolchainを固定する。
- deterministic fixtureを維持する。
- canonical manifestをCIで確認する。
- versioned evidence bundleを作る。
- superseded branchとcurrent product branchを明示する。

## 長期方向

KuuOSは次の状態を目指します。

```text
claims know their support
observations know their source
beliefs know their uncertainty
memories know their lineage
plans know their owner
actions know their exact license
effects know their independent observation
learning knows it is future-only
WORLD commits know they are not truth
proofs know their formal and external status
analytic vacua know they are representations
local controls know they are not global constitutions
governance knows when to stop, hold, repair or hand over
```

長期目標は、エージェントへ無制限の自由を与えることではありません。

権限崩壊を起こさず、関係的連続性、観測可能性、形式的追跡可能性を高めることです。

## 現在の優先順位一覧

```text
1. README、ROADMAP、formal roots、runtime full checkを同期する。
2. WORLD v0.53からv0.59を依存順に検証し、mainへ順序付き統合する。
3. Tomita作用素から相対モジュラー解析を第一原理化する。
4. ActOS v0.4後のObserveOS、VerifyOS、LearnOS、WORLD dispositionを閉じる。
5. MemoryOS v0.39をObserveOS owner workflowへ接続する。
6. Open Horizon v0.34のatomic storeを分散環境へ一般化する。
7. Qi-WORLDの任意有限prefixを具体的receipt chainとして生成する。
8. Context GaugeとGraphRAGのcompositionを成熟させる。
9. release matrixとproof-status classificationを機械可読化する。
10. clinical、institutional、mathematical、execution authorityを分離し続ける。
```
