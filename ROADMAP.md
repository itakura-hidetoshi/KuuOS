# KuuOS / 空OS Roadmap

**基準日：2026年6月28日**

**機能基準：`main`のPR #874統合後、merge commit `9a848e1344e399f762813e8b78409a4c11cd92ab`**

この文書は、`main`へ統合された基盤、直近の研究前線、再基底が必要な独立枝、外部receipt、長期研究課題を分離します。

## 状態分類

| 表記 | 意味 |
|---|---|
| 統合済み | `main`に存在し、正式なruntimeまたはLean aggregate rootから参照される |
| 継続検証 | 統合済みだが、依存更新時に専用rootとaggregate rootを再検証する |
| 次期候補 | 直前versionのreceipt chainを継承する自然な次段階 |
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
memory score decrease != truth
rollback != time reversal
restored payload != restored authority
```

v0.69とv0.74では、明示的approvalが限定されたproduction application authorityを与えます。

ただし、review constructionはlive effectまたはstate writeを行いません。

v0.75はapprovalを一度だけ消費し、MemoryOS production stateを原子的に更新します。

v0.76はcommit receiptとpre-commit snapshotを照合し、新しいrevisionとしてpayloadを復元します。

rollbackによってapprovalを再有効化しません。

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
| MemoryOS foundational line | v0.35、v0.37、v0.38、v0.39 | 統合済み |
| Qi-WORLD | v2.3 | 統合済み |
| Vacuum-expectation OS chain | ObserveOS、VerifyOS、LearnOS、PlanOS、DecisionOS、ActOS、WORLDのversioned bridge | 統合済み |
| WORLD mathematical sidecar | v0.27からv0.59 | 統合済み、継続検証 |
| Gauge-field self-organization | v0.60からv0.69 | 統合済み、継続検証 |
| Module-Bundle foundation | v0.70からv0.72 | 統合済み、継続検証 |
| MemoryOS evaluation and governed application | v0.73からv0.76 | 統合済み、継続検証 |
| Lean aggregate root | `KuuOSFormal` | 厳格build surface |
| Runtime aggregate entry | `scripts/run_kuuos_runtime_full_check_v0_55.py` | v0.76までの累積回帰入口 |

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

### Modular Evolution Mesh

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

### 気の診断候補とQi-WORLD

v0.28は、複数時点のQi Process Tensor、複数仮説、反証、不確実性、回復可能性区間、clinician-review handoffを実装しました。

v0.29は候補をsource、mission、lineage、historyへ束縛しました。

Qi-WORLD v2.3は、Qi Process TensorとCross-Cycle Blocker Theoryを陰陽相補系として接続しました。

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

### MemoryOS foundational line

v0.35はQi process history、blocker context、sourced WORLD generationをappend-only memoryへ統合しました。

v0.37はworking、episodic、semantic、proceduralの四層記憶、observable predictive-state candidate、contradiction residue、WORLD imaginationを追加しました。

v0.38はWORLD v0.49のOS-Hilbert packetを読み取り専用解析文脈として接続しました。

v0.39はMemoryOS解析capsuleとWORLD v0.50候補をObserveOS owner reviewへ渡すintakeを追加しました。

MemoryOSはtruth promotion、blocker discharge、PlanOS activation、ActOS invocation、WORLD updateを自動生成しません。

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

### Gauge-Field Self-Organization v0.60からv0.69

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

この系列は、保護座標を変更しない有限接続候補を構成し、source、candidate、rollback、review、有限有効期間をexact digestへ束縛します。

finite validationは、連続ゲージ理論全体の証明またはtruth authorityではありません。

approvalはapplication authorityを与え得ますが、review自体はlive effectを実行しません。

### Module-Bundle foundation v0.70からv0.72

v0.70は、空OS状態を文脈代数上の加群として再構成しました。

ObserveOS、VerifyOS、MemoryOS、Ethicsは、同一fiber内の意味部分加群として扱います。

```text
(A, M, {P_i}, F^•M, ∇, G)
```

v0.71は、非可換文脈代数、内部微分、Leibniz接続、加群線形な接続差、曲率、gauge共変性を追加しました。

```text
∇_i(a m) = δ_i(a)m + a∇_i(m)
```

v0.72は、read-only MemoryOS historyと有限記憶kernelを接続へ追加しました。

```text
∇_i^K(m_t, h_t) = ∇_i^(0)(m_t) + K_i(h_t)
```

履歴は変更せず、memory部分加群だけへ作用し、pathwise Leibniz則、authority filtration、rollbackを保ちます。

### MemoryOS evaluation and governed application v0.73からv0.76

v0.73は、同一source kernelへ束縛された有限候補familyを完全検証し、gauge-invariant score、変更term数、canonical digestの順で決定的に一件を選択します。

低いscoreをtruthと同一視しません。

v0.74は、selection recordを外部reviewへ渡し、次のdecisionをimmutable receiptとして固定します。

```text
APPROVE_MEMORY_SELECTION
REJECT_MEMORY_SELECTION
REQUEST_REEVALUATION
```

approvalは束縛されたselected payloadだけにproduction application authorityを与えます。

review関数は状態を書き換えません。

v0.75は、approvalを一度だけ消費し、compare-and-swapの下でMemoryOS production stateを原子的に更新します。

```text
revision := revision + 1
current kernel := selected kernel
current connection := selected connection
consumed approvals := consumed approvals + review receipt digest
previous state digest := before state digest
```

v0.76は、commit receiptとpre-commit snapshotに基づく単回rollbackを実装します。

```text
production revision := current revision + 1
current kernel := snapshot kernel
current connection := snapshot connection
previous state digest := rollback前state digest
rollback ledger revision := ledger revision + 1
ledger consumed commits := consumed commits + commit receipt digest
```

rollbackは過去状態への時間逆行ではありません。

payloadを復元しながらstate chainとledgerを前進させる補償transactionです。

## Active research frontier

### 優先1：Post-Application Verification v0.77

**状態：次期候補**

v0.75はproduction commitを実行します。

v0.76は監査可能なrollbackを実行します。

次段階では、commitまたはrollbackのreceipt chainをVerifyOSへ渡し、実行後状態を独立に検証します。

```text
application receipt
+ before / after state digests
+ approval consumption evidence
+ rollback ledger evidence when applicable
+ independent observation evidence
→ VerifyOS post-application intake
→ VERIFIED / FAILED / INDETERMINATE
```

受入条件：

- commit receiptまたはrollback receiptのself-digestを検証する。
- source state、target state、revision chainをexact bindingする。
- reviewerまたはcommitterと独立したverification ownerを要求する。
- raw observation、causal attribution、verification verdictを分離する。
- `FAILED`または`INDETERMINATE`から自動rollbackしない。
- fresh rollback requestと権限を別に要求する。
- VerifyOS verdictをtruth authorityへ昇格させない。
- future-only LearnOS delta以外の現在周期変更を行わない。

### 優先2：Aggregate rootの完全性固定

**状態：継続検証**

Lean aggregate rootとruntime aggregate rootを、`main`の統合済み到達点へ常時同期させます。

必須検査：

- `formal/KuuOSFormal.lean`がv0.69とv0.70からv0.76を直接または明示的umbrella経由で参照する。
- `scripts/run_kuuos_runtime_full_check_v0_55.py`がv0.76までのvalidatorを依存順に実行する。
- 専用Lean rootとaggregate `KuuOSFormal`を`warningAsError`と`sorryAsError`でbuildする。
- README、ROADMAP、`formal/KUOS.lean`、`formal/KuuOSFormal.lean`、`lakefile.toml`、manifest、workflow indexの同期を検査する。
- stale digest、source substitution、rollback replacement、approval replay、decision-permission mismatchをfail closedで拒否する。

### 優先3：Generic approvalとMemoryOS-specific approvalの関係固定

**状態：設計課題**

v0.69はgeneric connection evidence reviewです。

v0.74はMemoryOS selectionに特化したreviewです。

両者を暗黙に同一receiptとして扱いません。

次を明示します。

```text
v0.69 generic application authority
!= v0.74 memory-selection authority
```

必要なbridgeを追加する場合は、issuer、scope、candidate digest、rollback target、validity window、consumption ledgerをexact bindingします。

authority unionまたは権限の自動継承は禁止します。

### 優先4：CapabilityOSの再基底と責務統合

**状態：PR #832、再基底必要**

CapabilityOS v0.60は、Qi Process Tensor、陰陽blocker、複数WORLD、MemoryOS文脈、有限resource、tool、verifierをtyped capability candidateへ統合する独立枝です。

現在の課題は、現行`main`のv0.76と責務を接続することです。

```text
CapabilityCandidate
!= module deformation candidate
!= memory kernel candidate
!= PlanOS activation
!= DecisionOS selection
!= ActOS license
```

統合判断では、capability discovery、module registry、MemoryOS retrieval、production application authorityを分離します。

### 優先5：WORLD四大相転移宣言の再編

**状態：PR #825、再基底必要**

PR #825の`WORLD v0.60`は、四大相転移候補をfree-energy、spectral-gap closure、fixed-point subalgebra change、four-great coordinate changeの独立証人として構成します。

現行`main`には別系列の`KuuOS Gauge v0.60`が統合されています。

統合前にversion namespaceを分離します。

```text
WORLD Four-Great Phase Transition series
!= KuuOS Gauge Self-Organization series
```

phase-transition declarationはread-onlyに保ち、PlanOS objectiveまたはActOS authorityを生成しません。

### 優先6：Workflow consolidationの再基底

**状態：PR #835、再基底必要**

基礎OS bridge workflowを統合する方針は維持します。

ただし、v0.60からv0.76のworkflow、manifest、integrity guard、dedicated rootを欠落させてはなりません。

受入条件：

```text
no deleted-workflow reference
+ dependency-ordered validator chain
+ push / pull_request / workflow_dispatch coverage
+ runtime full check success
+ aggregate Lean root success
+ all-governance validation success
+ current gauge and memory application workflows preserved
```

### 優先7：MemoryOS v0.39とv0.72以降の関係整理

**状態：MemoryOS統合課題**

v0.39はanalytic capsuleをObserveOS owner workflowへ渡すread-only intakeです。

v0.72は確定済みMemoryOS capsuleを非マルコフ接続のread-only history sourceとして扱います。

両者を同一の書込み経路へ統合しません。

- raw empirical evidenceを別入力として要求する。
- analytic candidateをActOS effect lineageへ偽装しない。
- active blocker、contradiction residue、source capsuleを保持する。
- ObserveOS commit後もVerifyOS debtを開いたままにする。
- history sourceとproduction kernel stateを別digestへ束縛する。
- v0.75 commitがsource historyを書き換えないことを維持する。

### 優先8：Tomitaから相対モジュラー解析への第一原理化

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

### 優先9：実行後効果の一般OS閉路

**状態：OS統合課題**

MemoryOS v0.77候補とは別に、ActOS一般のeffect receiptをObserveOS、VerifyOS、LearnOS、WORLD dispositionへ接続します。

```text
ActOS effect
→ WORLD v0.52 intake
→ ObserveOS observation receipt
→ independent VerifyOS disposition
→ future-only LearnOS delta
→ governed WORLD reconciliation candidate
```

raw evidence、observation、verification、causal attributionを分離します。

failedまたはindeterminate verificationから自動rollbackしません。

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
- independent verification ownerの正当性。
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
+ runtime full-check registration
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
- aggregate rootへ未登録のversionを統合済み完了と記載しない。

## 中期研究方向

### 非マルコフMemoryOS

- scar、relapse、recovery、return-to-contextをchart-local transportへ接続する。
- semantic consolidationがcontradiction residueを消去しないことを保つ。
- predictive stateをlatent truthとして扱わない。
- collective reconstructionでindividual lineageを失わない。
- retrievalをbelief promotionまたはexecution authorityへ昇格させない。
- process tensorとして、過去の観測、介入、検証、失敗、修正が将来の応答可能性へ与える影響を表す。
- v0.72の有限履歴kernelを連続時間候補へ拡張し、離散runtimeと解析receiptを分離する。

### Module connectionと非可換微分計算

- v0.71の有限行列代数模型を一般の非可換微分計算`(ΩA, d)`へ拡張する。
- connection deformation catalogを有限探索する。
- semantic projectors、protected submodule、authority filtrationの保存を維持する。
- memory kernel deformationとbase connection deformationを別candidate classとして扱う。
- generic approvalとcandidate-specific approvalのexact bindingを証明する。

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
- v0.75とv0.76のstate CASとledger CASを分散storeへ拡張する。

### 公開再現性

- Leanとmathlib toolchainを固定する。
- deterministic fixtureを維持する。
- canonical manifestをCIで確認する。
- versioned evidence bundleを作る。
- superseded branchとcurrent product branchを明示する。
- component、version、source、manifest、validator、tests、Lean root、workflow、proof statusを機械可読に結ぶ。
- READMEとROADMAPの機能基準commitを自動検査する。

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
approvals know their exact scope, expiry and consumption
rollbacks know their source snapshot and monotonic ledger
local controls know they are not global constitutions
governance knows when to stop, hold, repair or hand over
```

長期目標は、エージェントへ無制限の自由を与えることではありません。

権限崩壊を起こさず、関係的連続性、観測可能性、形式的追跡可能性、修復可能性を高めることです。

## 現在の優先順位一覧

```text
1. v0.75とv0.76のreceipt chainをVerifyOSへ渡すv0.77を設計する。
2. Lean rootとruntime rootをv0.76の統合状態へ固定する。
3. v0.69 generic approvalとv0.74 memory approvalの関係を明示する。
4. CapabilityOS v0.60を現行mainへ再基底し、候補責務を分離する。
5. WORLD四大相転移系列を再命名または再version化して再基底する。
6. workflow consolidationをv0.76までのworkflow集合へ追従させる。
7. MemoryOS v0.39とv0.72以降のread-only source関係を整理する。
8. closed Tomita operatorから相対モジュラー解析へ進む。
9. ActOS一般の実行後観測検証閉路を閉じる。
10. 4D Yang–Millsのcanonical proof boundaryを保持する。
```
