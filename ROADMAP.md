# KuuOS / 空OS Roadmap

**基準日：2026年6月28日**

**機能基準：`main`のPR #857統合後、merge commit `de76bd615275ee755f27c1989c4514834d6ad539`**

この文書は、`main`へ統合された基盤、active research frontier、再基底が必要な独立枝、外部receipt、長期研究課題を分離します。

## 状態分類

| 表記 | 意味 |
|---|---|
| 統合済み | `main`に存在し、正式なruntimeまたはLean aggregate rootから参照される |
| 継続検証 | 統合済みだが、依存更新時に専用rootとaggregate rootを再検証する |
| Active PR | 現在の`main`を基準とする研究前線。merge前は統合済みと記載しない |
| 再基底必要 | open branch上に実装があるが、現在の`main`との競合または責務重複を解消する必要がある |
| 計画 | 受入条件は定義されているが、正式実装は未完了 |
| 外部receipt | runtimeまたはLean内部だけでは構成しない解析的、経験的、制度的、権限的入力 |
| Frozen boundary | 破壊的変更を行わず、additiveまたはtighten-onlyで維持する境界 |

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
WORLD intake != WORLD update
analytic vacuum != exact WORLD
Kū != zero vector
modular time != physical time

connection candidate != production application
application authority != performed effect
curvature decrease != truth
finite gauge equivalence != empirical equivalence
```

v0.69では、`APPROVE_EVIDENCE`とproduction application authorityを分離しません。

ただし、review constructionはlive effectまたはstate writeを行いません。

```text
APPROVE_EVIDENCE
<-> production_apply_allowed = true

REJECT_EVIDENCE
-> production_apply_allowed = false

REQUEST_MORE_EVIDENCE
-> production_apply_allowed = false
```

すべての段階は、source binding、append-only lineage、replay idempotence、stale-state rejection、rollback binding、権限所有者の分離、反証と不確実性の可視化を保ちます。

## 現在の統合済み基準

| 系列 | 到達点 | 状態 |
|---|---|---|
| Core governance | v0.1 | Frozen boundary |
| Horizon / Context Gauge | v0.12 / v0.13 | 統合済み |
| Modular Evolution Mesh | v0.1 | 統合済み |
| PlanOS control | v0.17 | 統合済み |
| Finite-cycle agent | v0.20からv0.27 | 統合済み |
| Qi diagnostic lineage | v0.28 / v0.29 | 統合済み |
| Open Horizon | v0.30からv0.34 | 統合済み |
| MemoryOS | v0.35、v0.37、v0.38、v0.39 | 統合済み |
| Qi-WORLD | v2.3 | 統合済み |
| Vacuum-expectation OS chain | ObserveOS、VerifyOS、LearnOS、PlanOS、DecisionOS、ActOS、WORLDのversioned bridge | 統合済み |
| WORLD mathematical sidecar | v0.27からv0.59 | 統合済み、継続検証 |
| Gauge-field self-organization | v0.60からv0.69 | 統合済み、継続検証 |
| Lean aggregate root | `KuuOSFormal` | 厳格build surface |
| Runtime aggregate entry | `scripts/run_kuuos_runtime_full_check_v0_55.py` | 累積回帰入口 |

## 完了した基盤

### ガバナンスと局所文脈

次の局所文脈スパインは統合済みです。

```text
multiple horizons
→ local sections
→ overlap eligibility
→ parallel transport
→ curvature and cocycle residue
→ path-dependent holonomy
```

今後の課題はcompositionと運用成熟であり、普遍global graphへの変換ではありません。

### Modular Evolution Mesh v0.1

型付きmodule contract、registry、能力依存解決、append-only hash-chain ledgerを統合しました。

ObserveOS、VerifyOS、MemoryOSは初期module manifestとして登録されています。

```text
module discovery != activation
registration != execution license
dependency resolution != effect execution
ledger receipt != truth
self-organization proposal != self-modification authorization
```

### 有限サイクル継続

v0.20からv0.27は、mission binding、観測、複数信念、semantic planning、独立検証、bounded memory、effect reconciliation、event wake-up、resource admission、governed change、checkpoint、restart recoveryを接続しました。

各サイクルは有限ですが、v0.30により有限局所制御が将来可能性全体を閉じないことを固定しました。

### 気の診断候補と系譜

v0.28は、複数時点のQi Process Tensor、複数仮説、反証、不確実性、回復可能性区間、clinician-review handoffを実装しました。

v0.29は候補をsource、mission、lineage、historyへ束縛しました。

この系列は診断確定、治療、トリアージ、ActOS権限を生成しません。

### Open Horizon観測循環

v0.30からv0.34は次を実装しました。

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

v0.37はworking、episodic、semantic、proceduralの四層記憶、observable predictive-state candidate、contradiction residue、WORLD imaginationを追加しました。

v0.38はWORLD v0.49のOS-Hilbert packetを読み取り専用解析文脈として接続しました。

v0.39はMemoryOS解析capsuleとWORLD v0.50候補をObserveOS owner reviewへ渡すintakeを追加しました。

MemoryOSはtruth promotion、blocker discharge、PlanOS activation、ActOS invocation、WORLD updateを行いません。

### Qi-WORLD

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

解析的経路は次のとおりです。

```text
WORLD v0.50 vacuum-expectation candidate
→ WORLD v0.51 ObserveOS evidence intake
→ supplied ObserveOS commit
→ supplied VerifyOS verification
→ LearnOS future-only delta
→ WORLD v0.53 OS receipt composition
→ PlanOS / DecisionOS handoff
→ ActOS bounded host adapter
```

実行後効果は別経路です。

```text
ActOS effectRecorded receipt
→ WORLD v0.52 host-effect intake candidate
→ ObserveOS effect-grounded observation receipt
```

WORLD v0.52は観測、検証、WORLD更新を行いません。

WORLD v0.53は既存receiptを合成しますが、receipt構成またはtransition実行を行いません。

### WORLD数学サイドカー

`main`の統合済み数学系列はv0.27からv0.59です。

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
→ OS receipt composition
→ Kū vacuum central reference state
→ Kū vacuum information geometry
→ verified Araki calculus and OS transport
→ closed Tomita operator bridge
→ conjugate-adjoint intermediate layer
→ four-great phase dynamics
```

外部receiptとして残る解析的構造を、Lean直接定理と混同しません。

### ゲージ場型自己組織化 v0.60からv0.69

`main`へ次の依存順で統合されています。

```text
v0.60  gauge-field self-organization foundation
→ v0.61  OS-associated gauge fields and memory holonomy
→ v0.62  finite connection candidate search
→ v0.63  governed review
→ v0.64  finite snapshot evaluation
→ v0.65  sealed staging package
→ v0.66  shadow materialization
→ v0.67  finite gauge validation
→ v0.68  evidence capsule
→ v0.69  approval-bound external evidence review
```

#### v0.60

局所場、接続、plaquette holonomy、Wilson observableを用いて、保護座標を変更しない緩和候補を構成します。

接続、評価領域、field identity、owner、authority class、rollback targetは固定します。

#### v0.61

ObserveOS、VerifyOS、MemoryOSなどの意味チャネルを随伴場として接続します。

MemoryOS履歴は、権限そのものではなく、path-dependent holonomyとして保持します。

#### v0.62

有限catalogからconnection improvement candidateを探索します。

候補はsource connection digest、gauge domain、rollbackへ束縛されます。

#### v0.63

review結果を`ADMIT`、`REJECT`、`DEFER`へ分離します。

reviewは候補の実在化またはproduction適用を行いません。

#### v0.64

review済み候補を有限snapshot上で評価します。

評価値はtruthまたは全contextでの改善保証ではありません。

#### v0.65

source、candidate、rollback、評価結果をsealed staging packageへ束縛します。

#### v0.66

sealed packageからin-memory shadowを構成します。

shadowはproduction state writeではありません。

#### v0.67

有限ゲージsample上でorbit整合性と観測量を検査します。

有限検証は連続ゲージ理論全体の証明ではありません。

#### v0.68

source、candidate、rollback、shadow、validationを有限有効期間を持つevidence capsuleへ束縛します。

#### v0.69

外部reviewer identity、reviewer class、scope、digest chain、有効期間、decision、application authorityをimmutable recordへ束縛します。

```text
valid approval
<-> application authority

application authority
!= already performed application
```

## Active research frontier

### 優先1：統合後の厳格回帰検証

**状態：最優先**

v0.60からv0.69は`main`へ統合済みです。

次の累積検査を、workflow更新または依存更新のたびに実行します。

```text
versioned runtime validators
+ canonical manifests
+ dedicated Lean roots
+ aggregate KuuOSFormal
+ runtime full check
+ no authority-boundary regression
```

必須検査：

- `run_kuuos_runtime_full_check_v0_55.py`を累積runtime入口として維持する。
- v0.60、v0.61、v0.62、v0.69の専用Lean rootを厳格buildする。
- aggregate `KuuOSFormal`を`warningAsError`と`sorryAsError`でbuildする。
- README、ROADMAP、`formal/KUOS.lean`、`formal/KuuOSFormal.lean`、`lakefile.toml`、manifest、workflow indexの同期を検査する。
- stale digest、source substitution、rollback replacement、decision-permission mismatchをfail closedで拒否する。

### 優先2：Module-Bundle Self-Organization v0.70

**状態：Active PR #860**

v0.70は、自己組織化をグラフの再配線ではなく、文脈代数上の加群接続変形として再定式化します。

```text
(A, M, {P_i}, F^•M, ∇, G)
```

- `A`：文脈代数と微分方向。
- `M`：空OS状態加群。
- `{P_i}`：protected、ObserveOS、VerifyOS、MemoryOS、Ethicsの意味射影。
- `F^•M`：authority filtration。
- `∇`：End(M)値1-form connection。
- `G`：意味チャネルとprotected部分を保存するゲージ群。

許容変形は次を満たします。

```text
commutes with semantic projectors
+ vanishes on protected submodule
+ preserves authority filtration
+ binds exact source connection
+ preserves exact rollback
+ performs no live effect
```

受入条件：

```text
dedicated runtime validator success
+ fail-closed fixtures success
+ canonical manifest valid
+ KuuOSFormalV0_70 strict build
+ aggregate KuuOSFormal strict build
+ no v0.69 authority regression
```

### 優先3：v0.69 approvalからv0.70 connection objectへの接続

**状態：次の統合課題**

v0.69はevidence reviewとapplication authorityを定義します。

v0.70は、そのapproval pathが対象とし得るmodule-connection candidateを定義します。

次段階では、両者のexact bindingを追加します。

```text
v0.70 module candidate receipt
+ source connection digest
+ deformation digest
+ rollback digest
+ v0.68 evidence capsule
+ v0.69 approved review record
→ governed application intake
```

次を禁止します。

- reviewer scopeを越えるmoduleまたはconnectionの適用。
- approval期限後の再利用。
- source、candidate、rollbackの差替え。
- approvalを利用したauthority filtrationの上昇。
- review recordをlive-effect receiptへ偽装すること。

### 優先4：CapabilityOSの再基底と責務統合

**状態：PR #832、再基底必要**

CapabilityOS v0.60は、Qi Process Tensor、陰陽blocker、複数WORLD、MemoryOS文脈、有限resource、tool、verifierをtyped capability candidateへ統合します。

現在の課題は、現行`main`とv0.70へ責務を接続することです。

```text
CapabilityCandidate
!= PlanOS activation
!= DecisionOS selection
!= ActOS license
```

統合判断では次を明確化します。

- CapabilityOS candidateとmodule-bundle connection candidateの違い。
- capability provider discoveryとmodule registry discoveryの違い。
- verifier不在時のHOLDとv0.69 evidence requestの接続。
- MemoryOS retrievalを現在周期のactivationへ昇格させないこと。

### 優先5：WORLD四大相転移宣言の再編

**状態：PR #825、再基底必要**

PR #825の`WORLD v0.60`は、四大相転移候補をfree-energy、spectral-gap closure、fixed-point subalgebra change、four-great coordinate changeの独立証人として構成します。

現行`main`には別系列の`KuuOS Gauge v0.60`が統合されています。

統合前にversion namespaceを分離します。

推奨される状態表記は次です。

```text
WORLD Four-Great Phase Transition series
!= KuuOS Gauge Self-Organization series
```

受入条件：

- 現行`main`へ再基底する。
- gauge v0.60からv0.69のimport、manifest、workflowを損なわない。
- phase-transition declarationをread-onlyに保つ。
- PlanOS objectiveまたはActOS authorityを生成しない。
- analytic witness、external physical receipt、empirical confirmationを分離する。

### 優先6：workflow consolidationの再基底

**状態：PR #835、再基底必要**

15本の基礎OS bridge workflowを統合する方針は維持します。

ただし、v0.60からv0.69およびv0.70のworkflow、manifest、integrity guard参照を欠落させてはなりません。

受入条件：

```text
no deleted-workflow reference
+ dependency-ordered validator chain
+ push / pull_request / workflow_dispatch coverage
+ runtime full check success
+ all-governance validation success
+ current gauge and module-bundle workflows preserved
```

### 優先7：実行後効果の観測検証閉路

**状態：OS統合課題**

現在は次まで統合済みです。

```text
ActOS effect
→ WORLD v0.52 intake
→ ObserveOS observation receipt
```

次の課題は、実行後効果のVerifyOS receipt、future-only LearnOS delta、WORLD disposition、必要時のfresh commit authorizationです。

- raw evidence、observation、verification、causal attributionを分離する。
- failedまたはindeterminate verificationから自動rollbackしない。
- rollbackはfresh authorizationとappend-only compensating receiptを要求する。
- v0.69 approvalとpost-effect verificationを同一receiptへ統合しない。

### 優先8：MemoryOS v0.39からObserveOS owner workflowへ

**状態：MemoryOS統合課題**

- v0.39 read-only intakeをObserveOSのscope判定へ接続する。
- raw empirical evidenceを別入力として要求する。
- analytic candidateをActOS effect lineageへ偽装しない。
- active blocker、contradiction residue、source capsuleを保持する。
- ObserveOS commit後もVerifyOS debtを開いたままにする。
- v0.70 module fiber内のMemoryOS射影と、永続化されたMemoryOS lineageを区別する。

### 優先9：Tomitaから相対モジュラー解析への第一原理化

**状態：数学研究課題**

- closed Tomita operatorからpolar decompositionへ進む。
- relative modular operatorとmodular conjugationの型付き基礎を構成する。
- natural positive cone、standard form、unbounded logarithmの外部receiptを明示する。
- 有界生成子のAraki calculusと非有界作用素基礎を分離する。
- OS reconstruction inputとoperator-algebraic modular inputを混同しない。

証明状態は次へ分類します。

```text
Lean-derived theorem
hypothesis-supplied structure
external analytic receipt
future target
```

### 優先10：4D Yang–Mills外部証明境界

**状態：外部canonical repositoryを参照**

canonical proof repositoryは[`itakura-hidetoshi/4d-mass-gap`](https://github.com/itakura-hidetoshi/4d-mass-gap)です。

KuuOSはreference、governance、receipt、adapter surfaceを保持します。

KuuOS側で次を主張しません。

```text
reference surface = final theorem authority
formal bridge = completed proof
CI pass = external mathematical acceptance
```

外部proof frontierとして残る主要課題：

- latticeからcontinuumへの厳格bridge。
- nontrivial continuum Yang–Mills theory。
- vacuum uniqueness。
- positive physical spectral gap。
- 33/20値の独立導出。
- public theorem boundaryを越える最終release判断。

## 外部receipt一覧

次はKuuOS内部の型またはvalidatorだけでは生成しません。

- raw empirical evidence。
- institutional authorization。
- production host license。
- reviewer identityとreviewer classの正当性。
- analytic assumptions for unbounded operator theory。
- OS reconstructionに必要な外部解析条件。
- physical interpretationとexperimental confirmation。
- 4D Yang–Millsのcanonical proof status。
- clinical diagnosis、treatment、triage、medical authority。

外部receiptは、由来、scope、有効期間、issuer、revocation条件を持つ必要があります。

## 共通release gate

研究枝を`main`へ統合するには、少なくとも次を満たします。

```text
current-main base
+ exact source lineage
+ versioned manifest
+ deterministic validator
+ positive fixtures
+ fail-closed negative fixtures
+ dedicated strict Lean root
+ aggregate KuuOSFormal strict build
+ runtime full-check compatibility
+ rollback or compensation contract
+ documentation synchronization
+ no authority-boundary regression
```

追加条件：

- branch上のCI成功を将来の`main`成功と同一視しない。
- stale branchの古いworkflow結果を現在の検証結果として扱わない。
- competing version namespaceを統合前に解消する。
- superseded branch、CI-only branch、product branchを明示する。
- external receiptをLean theoremとして記載しない。

## 中期研究方向

### 非マルコフMemoryOS

- scar、relapse、recovery、return-to-contextをchart-local transportへ接続する。
- semantic consolidationがcontradiction residueを消去しないことを保つ。
- predictive stateをlatent truthとして扱わない。
- collective reconstructionでindividual lineageを失わない。
- retrievalをbelief promotionまたはexecution authorityへ昇格させない。
- process tensorとして、過去の観測、介入、検証、失敗、修正が将来の応答可能性へ与える影響を表す。

### Module connectionと非可換微分計算

- v0.70の有限定数係数模型を非可換微分計算`(ΩA, d)`へ拡張する。
- Leibniz則を持つ一般接続を導入する。
- connection deformation catalogを有限探索する。
- 非マルコフ記憶核`K(t, τ)`を接続へ組み込む。
- semantic projectors、protected submodule、authority filtrationの保存を維持する。
- module candidateとexternal approvalのexact bindingを証明する。

### WORLDと物理Hilbert空間

- OS quotient completionの第一原理構成を強化する。
- densely defined self-adjoint Hamiltonian bridgeを型付きで接続する。
- Stone generation、spectral support、cluster propertyのstatusを分離する。
- modular timeとphysical timeを分離する。
- vacuum sectorの非一意性とmulti-WORLD noncollapseを保つ。

### 四大相動力学

- v0.59のread-only診断を、明示的な相転移候補条件へ拡張する。
- Earth、Water、Fire、Airの各量の連続性、半連続性、閾値依存性を分離する。
- coarse-grainingによるFireの増減とPetz recoverabilityの関係を定理化する。
- Air transportと物理時間発展を同一視しない。
- Gauge v0.60とWORLD phase-transition seriesのversion namespaceを分離する。

### Open Horizonと分散運用

- v0.34 single-host POSIX storeを分散transaction adapterへ一般化する。
- fencing、optimistic concurrency、idempotencyを保持する。
- authorization issuer、host license、institutional policyのadapter boundaryを明示する。
- local holdとconstitutional amendmentを分離する。
- multi-agent formationとresource acquisitionを候補、承認、実行に分離する。

### 公開再現性

- Leanとmathlib toolchainを固定する。
- deterministic fixtureを維持する。
- canonical manifestをCIで確認する。
- versioned evidence bundleを作る。
- superseded branchとcurrent product branchを明示する。
- component、version、source、manifest、validator、tests、Lean root、workflow、proof statusを機械可読に結ぶ。

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
closed operators know which modular structures remain open
connections know their protected submodules
approvals know their exact scope and expiry
local controls know they are not global constitutions
governance knows when to stop, hold, repair or hand over
```

長期目標は、エージェントへ無制限の自由を与えることではありません。

権限崩壊を起こさず、関係的連続性、観測可能性、形式的追跡可能性、修復可能性を高めることです。

## 現在の優先順位一覧

```text
1. v0.60からv0.69の統合後回帰を固定する。
2. Module-Bundle Self-Organization v0.70を現行main上で検証する。
3. v0.69 approval recordとv0.70 module candidateをexact bindingする。
4. CapabilityOS v0.60を再基底し、module-bundleとの責務を分離する。
5. WORLD四大相転移系列を再命名または再version化して再基底する。
6. workflow consolidationを現行workflow集合へ追従させる。
7. ActOS後のObserveOS、VerifyOS、LearnOS、WORLD dispositionを閉じる。
8. MemoryOS v0.39をObserveOS owner workflowへ接続する。
9. closed Tomita operatorから相対モジュラー解析へ進む。
10. 4D Yang–Millsのcanonical proof boundaryを保持する。
```
