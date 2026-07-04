# KuuOS / 空OS Roadmap

**基準日：2026年7月5日 JST**

**`main`の統合済み到達点：Lifecycle Stage v0.35**

**`main`の最新merge commit：`a650a8f419512679eb218d2f23401f8508c6f2b7`**

**現在のDraft frontier：PR #991、Lifecycle Completion v0.36**

**Draft branch：`codex/lifecycle-final-closure-v0-36`**

この文書は、`main`へ統合済みの基盤、完了したrepository mutation roadmap、独立したApoptosis Lifecycle Governance、現在のDraft frontier、外部receipt、長期研究課題を分離します。

v1.24の完了後に、新しいmutation機能を自動的に継続しません。

Apoptosis Lifecycle Governanceをrepository mutation roadmap v1.25以降として扱いません。

v0.36がterminal completionとしてmergeされる場合、同じlifecycle routeの後続段階を自動生成しません。

## 状態分類

| 表記 | 意味 |
|---|---|
| 統合済み | `main`に存在し、正式なruntimeまたはLean surfaceから参照される |
| Draft frontier | 現在の`main`を基準とする未mergeの研究枝 |
| 継続検証 | 統合済みだが、依存更新時に専用rootとaggregate rootを再検証する |
| 完了系列 | 定義済みの終端へ到達し、後続権限を自動生成しない |
| terminal | 同一routeのsuccessorを許可しない終端状態 |
| 次期候補 | 非mutationまたは新しい独立系列として検討できる次段階 |
| 設計候補 | 境界と受入条件は定義するが、versionと実装は未確定 |
| 未統合提案 | closedまたはopen branchに存在するが、`main`に存在しない |
| 再基底必要 | 現在の`main`との競合、重複、欠落を解消する必要がある |
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
receipt composition != receipt construction

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
checkpoint reflog record != checkpoint reference update
dedicated index != canonical index
sandbox reflection != repository-root working-tree write
local checkpoint != remote push authority
roadmap completion != successor mutation authority

Apoptosis Lifecycle Governance != repository mutation roadmap v1.25
lifecycle observation != lifecycle authorization
lifecycle authorization != lifecycle execution
lifecycle execution != repository mutation
lifecycle archive != memory sovereignty
lifecycle completion != successor route
terminal completion != future authority inheritance

merged artifact != closed proposal
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
| Authority topology / post-transition verification v0.77 | 未統合提案 | current rootsへ含めない |
| Self-organizing improvement | v0.78 | 統合済み、継続検証 |
| Repository self-evolution | v0.79からv1.24 | 統合済み、継続検証 |
| Staged repository mutation | v1.19からv1.24 | 完了系列 |
| Checkpoint recovery proposal | v0.1 | 独立した非mutation系列 |
| Apoptosis Lifecycle Governance | v0.1からv0.35 | `main`へ統合済み |
| Lifecycle Completion | v0.36 | PR #991 Draft frontier |
| Lean aggregate root | `formal/KuuOSFormal.lean` | strict build surface |
| Current runtime root | `runtime/kuuos_current_check.py` | この枝のcurrent root |
| Closed repository mutation runtime root | `runtime/kuuos_v124_check.py` | v1.24 cumulative mutation surface |
| Legacy compatibility runtime root | `scripts/run_kuuos_runtime_full_check_v0_55.py` | v1.02 compatibility surface |
| Lake package version | `0.36.0` | v0.36 lifecycle frontier alignment |

現在の正式系列にはversion gapがあります。

```text
MemoryOS rollback v0.76
→ Self-organizing improvement v0.78
→ Repository structure alignment v0.79
→ ...
→ Checkpoint-dedicated reflog v1.24
→ independent Apoptosis Lifecycle Governance v0.1-v0.35 on main
→ Lifecycle Completion v0.36 Draft frontier
```

v0.77 proposal branchesの存在は、`main`への統合を意味しません。

Lean rootとruntime rootは、実在する統合済みartifactまたは現在のDraft branchで明示追加されたartifactだけを参照します。

## 完了した基盤

### 局所文脈、有限サイクル、Open Horizon

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

```text
vacuum-expectation observation candidate
→ ObserveOS evidence intake
→ host-effect atomic commit intake
→ OS receipt composition
→ verification receipt
→ future-only learning delta
```

OS receipt compositionは既存receiptの由来と所有権を合成します。

receipt composition != receipt constructionです。

外部解析receiptとLean-derived theoremを混同しません。

### Gauge、Module-Bundle、MemoryOS application

v0.60からv0.69は、有限な接続改善候補、review、evaluation、staging、shadow、gauge validation、evidence capsule、external approvalを構成します。

v0.70からv0.72は、文脈代数上のstate module、意味部分加群、authority filtration、非可換Leibniz接続、read-only non-Markov memory kernelを構成します。

v0.73からv0.76は、有限候補評価、決定的選択、外部review、single-use atomic commit、監査可能なmonotonic rollbackを構成します。

v0.77のauthority-role topologyとpost-transition verificationは未統合提案です。

これらを現在の`main`の権限構造または検証能力として記載しません。

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

### v0.99からv1.18：checkpoint creationからlive checkpoint reference CASまで

| Version | 統合済み責務 |
|---|---|
| v0.99 | delayed direct-reference stability and candidate reachability |
| v1.00 | bounded multi-sample local frontier finality |
| v1.01 | `refs/kuuos/checkpoints/`内のsingle-use checkpoint authorization |
| v1.02 | zero-OID CASとnonce consumptionのatomic modeled checkpoint creation |
| v1.03 | checkpoint creation receipt |
| v1.04 | checkpoint evolution workspace |
| v1.05 | checkpoint stability |
| v1.06 | checkpoint discrepancy review |
| v1.07 | checkpoint repair routing |
| v1.08 | checkpoint namespace gate |
| v1.09 | checkpoint candidate |
| v1.10 | checkpoint CAS contract |
| v1.11 | checkpoint candidate validation receipt |
| v1.12 | validated CAS intake |
| v1.13 | CAS coherence |
| v1.14 | CAS authorization request |
| v1.15 | CAS authorization decision |
| v1.16 | atomic modeled CAS transition |
| v1.17 | live Git preflight |
| v1.18 | bounded live checkpoint reference CAS |

candidate、validation、intake、coherence、request、decision、modeled transition、live bounded CASを一つの権限へ縮約しません。

## 完了した段階的repository mutation roadmap

### v1.19からv1.24

| Version | 許可された限定効果 | 禁止境界 |
|---|---|---|
| v1.19 | 単一blobのobject database書込 | tree、commit、ref、index、working tree、push、signing |
| v1.20 | 限定tree objectとcommit objectの構築 | ref、index、working tree、push、signing |
| v1.21 | 構築済みcommitのcheckpoint refへのCAS公開 | branch、tag、remote、push、signing |
| v1.22 | checkpoint専用indexへの限定書込 | 標準index、working tree、ref、push、signing |
| v1.23 | repository内sandbox working treeへの限定反映 | 通常working tree、index、object、ref、reflog、push、signing |
| v1.24 | checkpoint専用reflogへの正確な一件記録 | 現在ref、object、index、working tree、other reflog、push、signing |

```text
v1.19 bounded blob write
→ v1.20 limited tree and commit construction
→ v1.21 checkpoint-reference CAS publication
→ v1.22 dedicated alternate index
→ v1.23 repository-local sandbox reflection
→ v1.24 exact checkpoint-dedicated reflog record
```

このroadmapはv1.24で完了し、閉じています。

終端は、新しいmutation authorityを生成しません。

### v1.24受入記録

PR #948の固定headは`f99a4abd259b3b310cb96c77dbfccb742657d2f1`です。

KuuOS PR Governance Gate Run #370は成功しました。

最終auditはexpected checks 108件、収集結果108件、failed checks 0件、missing receipts 0件でした。

PR #948はmerge commit `1cb1b472527e70330f5387732d5d8f39fdbeffb5`として`main`へ統合されました。

## Apoptosis Lifecycle Governance

Apoptosis Lifecycle Governanceは、repository mutation roadmap v1.19からv1.24とは独立したread-only lifecycle-governance系列です。

この系列はrepository mutationの続番ではありません。

### v0.1からv0.8：観測から実行準備まで

| Version | 責務 |
|---|---|
| v0.1 | Apoptosis observation |
| v0.2 | Apoptosis candidate |
| v0.3 | Dependency review |
| v0.4 | Authority review |
| v0.5 | Quiescence review |
| v0.6 | External review |
| v0.7 | Independent authorization |
| v0.8 | Bounded execution preparation |

### v0.9からv0.18：request、decision、operation、transition preparation

| Version | 責務 |
|---|---|
| v0.9 | Lifecycle review |
| v0.10 | Bounded request |
| v0.11 | Decision review |
| v0.12 | Authorization decision |
| v0.13 | Operation approval |
| v0.14 | Operation start |
| v0.15 | Operation completion |
| v0.16 | Completion review |
| v0.17 | Result adoption |
| v0.18 | Transition review |

### v0.19からv0.35：closure、memory、archive

| Version | 責務 |
|---|---|
| v0.19 | Transition preparation |
| v0.20からv0.25 | bounded transitionとstate adoptionの段階的拘束 |
| v0.26からv0.30 | repository mutation review、authorization、execution、result review |
| v0.31 | apoptosis closure review |
| v0.32 | post-apoptosis quarantine |
| v0.33 | post-apoptosis observation |
| v0.34 | post-apoptosis long-term memory |
| v0.35 | lifecycle archive and final-closure binding |

v0.35はlong-term memory recordを固定境界へ束縛し、final closureへ進む準備を行います。

repository変更または外部操作を行いません。

### v0.36：Lifecycle Completion Draft frontier

PR #991はLifecycle Completion v0.36を追加するDraft frontierです。

v0.36は、readyなv0.35 recordだけを受け取ります。

completion receipt、terminal digest、memory seal、fixed boundary、memorial record、covenantを束縛します。

```text
Lifecycle Stage v0.35
→ Lifecycle Completion v0.36
→ terminal completion record
```

v0.36の状態は次です。

```text
LIFECYCLE_COMPLETION_COMPLETE
LIFECYCLE_COMPLETION_ALERT
LIFECYCLE_COMPLETION_REJECTED
```

COMPLETEはterminal recordを発行し、following lifecycle routeを許可しません。

ALERTは有効recordを発行しますが、terminalにはなりません。

REJECTEDは有効recordを発行しません。

v0.36はrepositoryを変更せず、外部操作を実行しません。

merge前は`main`の統合済み機能として扱いません。

## Aggregate rootsの現在形

### Lean root

`formal/KuuOSFormal.lean`は、`main`へ統合済みのLean moduleと、このDraft branchで明示追加されたcurrent frontier moduleだけをimport対象にします。

```bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
```

受入条件：

- nonexistent moduleまたはunmerged branch artifactを参照しない。
- dedicated rootとaggregate rootの境界が一致する。
- Lean-derived theoremとexternal receiptを分離する。
- terminal completionをsuccessor authorityへ昇格させない。

### Current runtime root

`runtime/kuuos_current_check.py`は、この枝のcurrent runtime rootです。

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py
```

この入口は、closed repository mutation rootとv0.36 lifecycle completion focused checkを束ねます。

### Closed repository mutation runtime root

`runtime/kuuos_v124_check.py`は、v1.24から先行repository runtimeへ依存順に接続します。

```bash
PYTHONPATH=. python3 runtime/kuuos_v124_check.py
```

この入口はfocused tests、guards、effect accountingを含むclosed repository mutation累積検証面です。

### Lifecycle Completion focused check

```bash
python3 -m unittest tests.test_kuuos_lifecycle_completion_v0_36
```

このfocused checkはv0.36のruntime surfaceを検証します。

### Legacy compatibility runtime root

`scripts/run_kuuos_runtime_full_check_v0_55.py`は互換名を保ち、legacy cumulative surfaceをv1.02まで実行します。

```bash
PYTHONPATH=. python3 scripts/run_kuuos_runtime_full_check_v0_55.py
```

legacy root、closed repository mutation root、current lifecycle rootを同一視しません。

三者は役割を分離したまま維持します。

## v0.36後の研究前線

### 優先1：PR #991のGovernance GateとDraft解除判定

**状態：Draft frontier**

必須検査：

- README、ROADMAP、CITATION、Lake version、runtime rootをv0.36 frontierへ同期する。
- v0.36 dedicated runtime testを成功させる。
- v0.36 Lean witness layerをstrict aggregate rootと整合させる。
- manifestとCI registryを同期する。
- COMPLETEがfollowing routeを持たないことを検査する。
- ALERTとREJECTEDをterminal completionとして誤表示しない。
- repository mutationまたは外部操作が発生しないことを維持する。

### 優先2：terminal completion後のpost-terminal observation設計

**状態：新規独立系列を開始する場合の設計候補**

terminal completion後に観測を継続する場合、それはv0.36のsuccessorではありません。

新しいread-only observationまたはpreservation系列として、authority owner、scope、receipt、non-successor boundaryを明記します。

### 優先3：Checkpoint recovery proposalとhandover

**状態：設計候補、非mutation**

checkpointは復元権限そのものではありません。

```text
checkpoint receipt
→ recovery proposal
→ source and target comparison
→ external review
→ bounded recovery authorization request
→ explicit authorization decision
```

この段階ではlive repository mutationを行いません。

recovery proposalはbranch force update、history rewrite、remote pushを自動許可しません。

### 優先4：Retention、revocation、delete authorityの分離

**状態：設計候補**

checkpoint retention、revocation、deleteは別の権限系列として扱います。

検討事項：

- retention policy owner。
- revocation issuerとrevocation observation。
- delete authorityの独立requestとdecision。
- legal holdまたはinstitutional hold。
- deletion failure receipt。
- reflog、reference、object retentionの区別。

checkpoint deleteをcheckpoint creationの逆操作として暗黙に許可しません。

### 優先5：新しいmutation系列の憲法

**状態：新規系列を開始する場合の必須条件**

新しいmutation機能はv1.24の続番だけで開始しません。

開始前に、少なくとも次を新規定義します。

- 独立したauthority owner。
- policyとpolicy digest。
- requestとrequest digest。
- resultとresult digest。
- executor identityとallowlist。
- effect accounting。
- preconditionとpostcondition。
- abort preservationまたはcompensation contract。
- Lean boundary。
- dedicated tests。
- CI registry。
- manifestとpublic documentation。
- 既存権限から昇格しないことを示す非権限定理または境界記述。

新しい系列は、object、reference、index、working tree、reflog、network、push、signingを別surfaceとして扱います。

### 優先6：v0.77 proposalsの処理

**状態：再評価候補**

v0.77提案を再利用する場合、現在のfrontierへ直接mergeしません。

必要な処理：

- current `main`へ再基底する。
- v0.78以降とauthority namespaceが衝突しないか確認する。
- version番号を保持するか、新しいversionへ移すか決定する。
- current aggregate roots、manifests、workflow registryへ追加する。
- post-transition verificationをrepository mutation receipt chainと無条件に同一化しない。
- dedicated runtime testsとstrict Lean rootを再実行する。

### 優先7：分散repository adapter

**状態：中期研究課題**

single-host local Git contractを分散storeへ拡張する場合、compare-and-swap、fencing token、idempotency key、append-only receipt、bounded lease、independent observation、authority and executor separationを保持します。

分散化はlocal authorityをglobal authorityへ昇格させません。

### 優先8：一般OSの実行後検証閉路

**状態：OS統合課題**

将来のpost-transition verificationを、ActOS一般へ無条件に同一化しません。

```text
performed effect
raw observation
causal attribution
verification disposition
future-only learning delta
governed WORLD reconciliation candidate
```

verification failureから自動rollbackしません。

### 優先9：数学形式化frontier

**状態：数学研究課題**

- closed Tomita operatorからpolar decompositionへ進む。
- relative modular operator、modular conjugation、natural positive cone、standard formを分離して構成する。
- unbounded logarithmと有界Araki calculusを分離する。
- WORLD四大相転移系列をGauge v0.60系列と別namespaceへ置く。
- OS reconstruction inputとoperator-algebraic modular inputを混同しない。
- 4D Yang-Millsのcanonical proof repository境界を保持する。

証明状態は次へ分類します。

```text
Lean-derived theorem
hypothesis-supplied structure
external analytic receipt
empirical or institutional receipt
future target
```

## Open branchとPRの扱い

現在の`main`はv0.35まで進んでおり、PR #991はv0.36のDraft frontierです。

古いbase SHAを持つopenまたはclosed-unmerged PRは、そのまま現在のfrontierとして扱いません。

### v0.77 proposal branches

Authority-role topologyとpost-transition verificationのv0.77枝は、`main`へ未統合です。

文書、aggregate roots、runtime rootでは未統合提案として扱います。

再利用時はcurrent-main rebase、namespace監査、version再決定、strict validationを要求します。

### Workflow consolidation

workflow統合またはPR gate整理の枝では、v0.78からv1.24、checkpoint recovery v0.1、Apoptosis lifecycle v0.1からcurrent frontierまでのmanifest、dedicated checks、full-audit membership、aggregate rootsを欠落させないことを要求します。

古いworkflow削除だけを先行させません。

### WORLD phase-transition branch

WORLD四大相転移宣言の独立系列は、Gauge Self-OrganizationとRepository Self-Evolutionから分離します。

```text
WORLD Four-Great Phase Transition series
!= KuuOS Gauge Self-Organization v0.60 series
!= Repository Self-Evolution series
```

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
- 4D Yang-Millsのcanonical proof status。
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
+ appropriate runtime-root registration
+ rollback, compensation, abort-preservation, or terminal non-successor contract
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
- closed unmerged PRを統合済みartifactとして記載しない。
- 完了roadmapから新しいmutation authorityを推論しない。
- terminal lifecycle completionからsuccessor routeを推論しない。

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
- READMEとROADMAPの機能frontierを自動比較する。
- unmerged proposalの誤昇格を機械検査する。

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
completed roadmaps know they grant no successor authority
lifecycle completions know whether they are terminal
terminal records know they grant no successor route
local controls know they are not global constitutions
governance knows when to stop, hold, repair, preserve, or hand over
```

長期目標は、エージェントへ無制限の自由を与えることではありません。

権限崩壊を起こさず、関係的連続性、観測可能性、形式的追跡可能性、再現可能性、修復可能性を高めることです。

## 現在の優先順位

```text
1. PR #991のv0.36 documentation、Lake version、runtime root同期を完了する。
2. Governance Gateとfocused checksを確認してからDraft解除を判断する。
3. v0.36 COMPLETEをterminalとして扱い、successor lifecycle routeを作らない。
4. post-terminal observationが必要な場合は新しい独立read-only系列として設計する。
5. checkpoint recovery proposalとhandoverを非mutation系列として設計する。
6. retention、revocation、delete authorityをcheckpoint creationから分離する。
7. 新しいmutation系列を開始する場合の独立authority憲法を定義する。
8. v0.77 proposalsを未統合のまま明示し、再利用時のrebase条件を定める。
9. local Git contractを分散adapterへ一般化する際の境界を研究する。
10. ActOS一般の実行後観測検証閉路を構成する。
11. relative modular theoryとWORLD数学frontierを進める。
12. stale open PR、closed-unmerged proposal、CI-only枝、superseded枝を整理する。
13. v1.24完了を後続mutation authorityへ変換しない。
14. terminal lifecycle completionを後続authorityへ変換しない。
```
