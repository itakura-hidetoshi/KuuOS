# KuuOS / 空OS Roadmap

**基準日：2026年6月30日**

**文書化対象の機能frontier：PR #914、KuuOS Repository Atomic Checkpoint Creation v1.02**

**frontier merge commit：`e109a8d4e6896abe5eda786885683fe3e3ef8d89`**

この文書は、`main`へ統合済みの基盤、現在のrepository self-evolution frontier、次期候補、外部receipt、再基底が必要な独立枝、長期研究課題を分離します。

## 状態分類

| 表記 | 意味 |
|---|---|
| 統合済み | `main`に存在し、正式なruntimeまたはLean aggregate rootから参照される |
| 継続検証 | 統合済みだが、依存更新時に専用rootとaggregate rootを再検証する |
| 次期候補 | 直前versionのreceipt chainを継承する自然な次段階 |
| 設計候補 | 境界と受入条件は定義するが、versionと実装は未確定 |
| Active PR | 現在の`main`を基準とする研究枝。merge前は統合済みと記載しない |
| 再基底必要 | 実装または提案があるが、現在の`main`との競合、重複、欠落を解消する必要がある |
| CI-only | product mergeを目的としない独立検証枝 |
| 外部receipt | runtimeまたはLean内部だけでは生成しない解析的、経験的、制度的、権限的入力 |
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
rollback != time reversal
restored payload != restored authority

repository proposal != accepted patch
accepted patch != repository application authorization
modeled application != live filesystem mutation
commit candidate != Git object materialization
object authorization != object write
reference authorization != reference update
reference receipt != finality
checkpoint authorization != checkpoint creation
modeled checkpoint creation != live Git mutation
checkpoint creation != checkpoint overwrite
local checkpoint != remote push authority
```

すべての段階は、source binding、append-only lineage、replay idempotence、stale-state rejection、rollbackまたはabort preservation、権限所有者の分離、反証と不確実性の可視化を保ちます。

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
| WORLD mathematical sidecar | v0.27からv0.59 | 統合済み、継続検証 |
| Gauge-field self-organization | v0.60からv0.69 | 統合済み、継続検証 |
| Module-Bundle / MemoryOS application | v0.70からv0.76 | 統合済み、継続検証 |
| Authority topology / post-transition verification | v0.77 | 統合済み、継続検証 |
| Self-organizing improvement | v0.78 | 統合済み、継続検証 |
| Repository self-evolution | v0.79からv1.02 | 統合済み、継続検証 |
| Lean aggregate root | `formal/KuuOSFormal.lean` | v1.02 strict build surface |
| Runtime aggregate root | `scripts/run_kuuos_runtime_full_check_v0_55.py` | v1.02 cumulative runtime surface |

## 完了した基盤

### 局所文脈、有限サイクル、Open Horizon

次の局所文脈スパインは統合済みです。

```text
multiple horizons
→ local sections
→ overlap eligibility
→ parallel transport
→ curvature and cocycle residue
→ path-dependent holonomy
```

finite-cycle agentは、mission binding、観測、複数信念、semantic planning、独立検証、bounded memory、effect reconciliation、event wake-up、resource admission、governed change、checkpoint、restart recoveryを接続します。

Open Horizonは、有限な局所制御を将来可能性全体の閉鎖へ昇格させません。

### Qi-WORLD、MemoryOS、WORLD数学層

Qi Process Tensorは、複数時点のprocess、複数仮説、反証、不確実性、回復可能性区間を候補として保持します。

Qi-WORLD v2.3は、process supportとboundary occupationを陰陽相補系として接続します。

MemoryOSは、working、episodic、semantic、procedural memory、非マルコフ履歴、analytic capsule、contradiction residueを保持します。

WORLD mathematical sidecarは、Hilbert空間、作用素環、modular theory、Araki entropy、Petz recovery、Jones theory、高次gauge情報幾何、真空候補、Tomita operator、四大相動力学までを型付きsurfaceとして接続します。

外部解析receiptとLean-derived theoremを混同しません。

### Gauge、Module-Bundle、MemoryOS production

v0.60からv0.69は、有限な接続改善候補、review、evaluation、staging、shadow、gauge validation、evidence capsule、external approvalを構成します。

v0.70からv0.72は、文脈代数上のstate module、意味部分加群、authority filtration、非可換Leibniz接続、read-only non-Markov memory kernelを構成します。

v0.73からv0.76は、有限候補評価、決定的選択、外部review、single-use atomic commit、監査可能なmonotonic rollbackを構成します。

v0.77は二つの境界を追加します。

```text
context-independent authority-role topology
+
independent post-transition verification
```

verification verdictはtruth authorityではありません。

`FAILED`または`INDETERMINATE`は自動rollbackを起動しません。

## Repository self-evolutionの統合済み連鎖

### v0.78からv0.82：自己改善と構造整合

| Version | 統合済み責務 |
|---|---|
| v0.78 | finite improvement proposal、bounded supervisor、停止条件、権限境界 |
| v0.79 | repository structure alignment candidate |
| v0.80 | alignment normal formとdeterministic normalization |
| v0.81 | incremental preservationとprotected-surface preservation |
| v0.82 | certificate chainとlineage verification |

この段階はrepositoryを変更しません。

### v0.83からv0.86：revision、merge、frontier証明

| Version | 統合済み責務 |
|---|---|
| v0.83 | direct branch and revision observation |
| v0.84 | merge certificate |
| v0.85 | revision DAG certificate |
| v0.86 | local repository frontier certificate |

working tree、reflog、remote observationを、object databaseとdirect reference evidenceの代替にしません。

### v0.87からv0.92：選択、shadow、admission、application

| Version | 統合済み責務 |
|---|---|
| v0.87 | bounded self-evolution portfolioとdeterministic selection |
| v0.88 | shadow realization、replay、normal-form preservation |
| v0.89 | multi-replay agreementに基づくgoverned admission |
| v0.90 | external approval、signature verification receipt、revocation status |
| v0.91 | exact scope-bound single-use application authorization |
| v0.92 | pure atomic repository application transition |

v0.92はisolated modeled stateを更新します。

live working tree、index、Git object database、referenceを暗黙に変更しません。

### v0.93からv0.98：Git objectとreferenceの外部実行境界

| Version | 統合済み責務 |
|---|---|
| v0.93 | deterministic blob、tree、commit candidate certificate |
| v0.94 | bounded single-use object materialization authorization |
| v0.95 | external executionとpost-object observationを束縛するreceipt |
| v0.96 | direct local branch reference-update authorization |
| v0.97 | exact reference CASとnonce consumptionのmodeled atomic transition |
| v0.98 | external reference execution、observation、nonce receiptの統合receipt |

candidate generation、authorization、modeled transition、external execution report、post-operation observationを別層に保ちます。

### v0.99からv1.02：local finalityとcheckpoint

| Version | 統合済み責務 |
|---|---|
| v0.99 | delayed direct-reference stability and candidate reachability |
| v1.00 | bounded multi-sample local frontier finality |
| v1.01 | `refs/kuuos/checkpoints/`内のsingle-use checkpoint authorization |
| v1.02 | zero-OID CASとnonce consumptionのatomic modeled checkpoint creation |

v1.02のcommitは次を一つの論理遷移として構成します。

```text
checkpoint state: absent → authorized final-tip OID
nonce state: unused → consumed
```

abortはsource checkpoint stateとsource nonce registryを完全に保存します。

v1.02はlive Git commandを呼ばず、live repository mutationを主張しません。

## Active research frontier

### 優先1：Live checkpoint creation adapter

**状態：次期候補**

v1.02はmodeled transitionです。

次段階では、v1.02 committed resultを再検証し、一つの限定されたlocal checkpoint creation requestだけを外部adapterへ渡します。

受入条件：

- v1.02 certificate、source checkpoint state、nonce registry、repository identity、Git-directory fingerprintを完全再検証する。
- direct reference `refs/kuuos/checkpoints/<name>`だけを許可する。
- expected old OIDをzero OIDへ固定する。
- authorized final-tip OID以外を拒否する。
- overwrite、delete、force、branch、tag、remote reference、pushを拒否する。
- single-use nonceとtransaction IDをexact bindingする。
- external host licenseとauthorized executorを要求する。
- command、exit status、stderr/stdout digest、observed final OIDをexecution reportへ束縛する。
- execution reportだけで成功を確定しない。

推奨する最小経路：

```text
v1.02 committed modeled transition
→ exact execution request
→ bounded local Git reference adapter
→ external execution report
```

### 優先2：Checkpoint creation receiptと独立観測

**状態：設計候補**

adapter実行後に、direct reference storeを独立に再観測します。

```text
execution report
+ independent post-reference observation
+ nonce-consumption receipt
+ exact repository and transaction binding
→ checkpoint creation receipt
```

受入条件：

- command successとreference observationを分離する。
- observed OIDがauthorized final-tip OIDと一致することを要求する。
- symbolic reference、reflog-only evidence、working-tree evidence、remote evidenceを拒否する。
- report substitution、observation substitution、nonce replayを拒否する。
- receipt constructionは追加mutationを行わない。
- failure時にoverwriteまたはautomatic retryを行わない。

### 優先3：Checkpoint stability、finality、immutability policy

**状態：設計候補**

checkpoint creation直後の存在確認と、時間を隔てた安定性確認を分離します。

検討事項：

- delayed direct-reference observation。
- object-database reachabilityの再確認。
- checkpoint name uniqueness。
- immutable-by-default policy。
- retention、revocation、delete authorityの別系列化。
- checkpoint lossまたはsubstitutionのfailure receipt。

checkpoint deleteはcheckpoint creationの逆操作として暗黙に許可しません。

### 優先4：Aggregate root、manifest、registryの完全性固定

**状態：継続検証**

必須検査：

- `formal/KuuOSFormal.lean`がv0.77からv1.02を明示的に参照する。
- `scripts/run_kuuos_runtime_full_check_v0_55.py`がv0.77とv0.96からv1.02を含む。
- 専用Lean rootとaggregate `KuuOSFormal`を`warningAsError`と`sorryAsError`でbuildする。
- runtime rootがlive-contract checksとfocused unit testsを依存順に実行する。
- README、ROADMAP、Lean root、runtime root、lake target、manifest、workflow indexを同期する。
- aggregate root未登録のversionを統合済み完了と記載しない。
- current frontierを機械可読manifestから検査できるようにする。

### 優先5：Checkpointからのrecoveryとhandover

**状態：設計候補**

checkpointは復元権限そのものではありません。

```text
checkpoint receipt
→ recovery proposal
→ source and target comparison
→ external review
→ bounded recovery authorization
→ modeled recovery transition
→ external execution
→ independent observation
```

recoveryはbranch force update、history rewrite、remote pushを自動許可しません。

### 優先6：分散repository adapter

**状態：中期研究課題**

single-host local Git contractを分散storeへ拡張する場合、次を保持します。

- compare-and-swap。
- fencing token。
- idempotency key。
- append-only receipt。
- bounded lease。
- independent observation。
- authority and executor separation。
- local checkpointとremote replicationの分離。

### 優先7：一般OSの実行後検証閉路

**状態：OS統合課題**

MemoryOS v0.77とrepository receipt chainを、ActOS一般へ無条件に同一化しません。

共通interfaceを追加する場合は次を分離します。

```text
performed effect
raw observation
causal attribution
verification disposition
future-only learning delta
governed WORLD reconciliation candidate
```

verification failureから自動rollbackしません。

### 優先8：数学形式化frontier

**状態：数学研究課題**

- closed Tomita operatorからpolar decompositionへ進む。
- relative modular operator、modular conjugation、natural positive cone、standard formを分離して構成する。
- unbounded logarithmと有界Araki calculusを分離する。
- WORLD四大相転移系列をGauge v0.60系列と別namespaceへ置く。
- OS reconstruction inputとoperator-algebraic modular inputを混同しない。
- 4D Yang–Millsのcanonical proof repository境界を保持する。

証明状態は次へ分類します。

```text
Lean-derived theorem
hypothesis-supplied structure
external analytic receipt
empirical or institutional receipt
future target
```

## Open branchとPRの扱い

現在の`main`はv1.02まで進んでいます。

古いbase SHAを持つopen PRは、そのまま現在のfrontierとして扱いません。

### Workflow consolidation

PR #891とPR #835は、workflow統合またはPR gate整理に関する枝です。

統合判断では、v0.77からv1.02のmanifest、dedicated checks、full-audit membership、aggregate rootsを欠落させないことを要求します。

古いworkflow削除だけを先行させません。

### Lean repair branch

PR #826はdependent receipt typeの修復枝です。

現在の`main`に同等修復が含まれるかを差分で確認し、未包含部分だけをcurrent-mainへ再基底します。

### WORLD phase-transition branch

PR #825はWORLD四大相転移宣言の独立系列です。

```text
WORLD Four-Great Phase Transition series
!= KuuOS Gauge Self-Organization v0.60 series
!= Repository Self-Evolution series
```

version namespaceを分離し、read-only declarationがPlanOS objectiveまたはActOS authorityを生成しないことを維持します。

### CI-only、validation-only、superseded branch

product codeを変更しないCI-only枝、過去のmainを再検証するだけの枝、統合済みproduct headの子枝は、current frontierへ再昇格させません。

必要なreceiptを保存した後、close、archive、または明示的なnon-merge statusへ移します。

## 外部receipt一覧

次はKuuOS内部の型またはvalidatorだけでは生成しません。

- raw empirical evidence。
- institutional authorization。
- production host license。
- reviewer identityとreviewer classの正当性。
- external signature verification。
- revocation registry authority。
- authorized executor identity。
- live Git command execution report。
- independent post-operation repository observation。
- analytic assumptions for unbounded operator theory。
- physical interpretationとexperimental confirmation。
- 4D Yang–Millsのcanonical proof status。
- clinical diagnosis、treatment、triage、medical authority。

外部receiptは、由来、scope、有効期間、issuer、revocation条件、observation time、canonical digestを持つ必要があります。

## 共通release gate

研究枝を`main`へ統合するには、少なくとも次を満たします。

```text
current-main base
+ exact source lineage
+ versioned manifest
+ deterministic validator
+ positive fixtures
+ fail-closed negative fixtures
+ dedicated strict Lean root when formal surface exists
+ aggregate KuuOSFormal strict build
+ runtime full-check registration
+ rollback, compensation, or abort-preservation contract
+ documentation synchronization
+ no authority-boundary regression
```

追加条件：

- branch上のCI成功を将来の`main`成功と同一視しない。
- stale branchの古いworkflow結果を現在の検証結果として扱わない。
- competing version namespaceを統合前に解消する。
- superseded branch、CI-only branch、product branchを明示する。
- external receiptをLean theoremとして記載しない。
- modeled transitionをlive mutationとして記載しない。
- receiptからsuccessor authorityを自動生成しない。
- aggregate rootへ未登録のversionを統合済み完了と記載しない。

## 中期研究方向

### 非マルコフMemoryOS

- scar、relapse、recovery、return-to-contextをchart-local transportへ接続する。
- semantic consolidationがcontradiction residueを消去しないことを保つ。
- predictive stateをlatent truthとして扱わない。
- collective reconstructionでindividual lineageを失わない。
- retrievalをbelief promotionまたはexecution authorityへ昇格させない。
- finite history kernelを連続時間候補へ拡張し、離散runtimeと解析receiptを分離する。

### Module connectionと非可換微分計算

- 有限行列代数模型を一般の非可換微分計算`(ΩA, d)`へ拡張する。
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

### 公開再現性

- Leanとmathlib toolchainを固定する。
- deterministic fixtureを維持する。
- canonical manifestをCIで確認する。
- versioned evidence bundleを作る。
- component、version、source、manifest、validator、tests、Lean root、workflow、proof statusを機械可読に結ぶ。
- READMEとROADMAPの機能frontierを自動検査する。
- open PRをcurrent product、rebase candidate、CI-only、supersededへ分類する。

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
repository transitions know whether they are modeled or live
checkpoints know their creator, frontier, nonce and observation history
local controls know they are not global constitutions
governance knows when to stop, hold, repair or hand over
```

長期目標は、エージェントへ無制限の自由を与えることではありません。

権限崩壊を起こさず、関係的連続性、観測可能性、形式的追跡可能性、再現可能性、修復可能性を高めることです。

## 現在の優先順位

```text
1. v1.02 modeled checkpoint creationを限定live adapterへ接続する。
2. external execution reportと独立観測からcheckpoint creation receiptを構成する。
3. checkpoint stability、finality、immutability、delete authorityを分離する。
4. Lean root、runtime root、manifest、workflow registryをv1.02へ固定する。
5. checkpointからのrecovery proposalとbounded handoverを設計する。
6. local Git contractを分散adapterへ一般化する。
7. ActOS一般の実行後観測検証閉路を閉じる。
8. relative modular theoryとWORLD数学frontierを進める。
9. stale open PR、CI-only枝、superseded枝を整理する。
10. 4D Yang–Millsのcanonical proof boundaryを保持する。
```
