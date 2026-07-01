# KuuOS / 空OS Roadmap

**基準日：2026年7月1日**

**`main`の統合済みfrontier：KuuOS Repository Bounded Blob v1.19**

**frontier merge commit：`f3ae5c69761c384e32a8e807afbec6c2ebb1a199`**

**Active Draft PR：#942、KuuOS Repository Bounded Tree and Commit v1.20**

この文書は、`main`へ統合済みの基盤、現在のactive branch、次期候補、外部receipt、長期研究課題を分離します。

## 状態分類

| 表記 | 意味 |
|---|---|
| 統合済み | `main`に存在し、正式なruntimeまたはLean aggregate rootから参照される |
| 継続検証 | 統合済みだが、依存更新時に専用rootとaggregate rootを再検証する |
| Active Draft PR | 現在の`main`を基準とする開発枝。merge前は統合済みと記載しない |
| 次期候補 | 直前versionのreceipt chainを継承する自然な次段階 |
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

repository proposal != accepted patch
accepted patch != repository application authorization
modeled application != live filesystem mutation
commit candidate != Git object materialization
object authorization != object write
live preflight != mutation authority
checkpoint reference CAS != branch or tag mutation
blob materialization != tree or commit materialization
object materialization != reference update
local mutation != remote push authority
successful test != permission to mutate an external repository
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
| Authority topology / post-transition verification v0.77 | 未統合提案 |
| Self-organizing improvement | v0.78 | 統合済み、継続検証 |
| Repository self-evolution | v0.79からv1.19 | 統合済み、継続検証 |
| Lean aggregate root | `formal/KuuOSFormal.lean` | v1.19 strict build surface |
| Runtime aggregate root | `scripts/run_kuuos_runtime_full_check_v0_55.py` | v1.19 cumulative runtime surface |
| Lake package version | `1.19.0` | `main`と同期 |
| Bounded tree and commit materialization | v1.20 | Active Draft PR #942 |

現在の正式系列にはversion gapがあります。

```text
MemoryOS rollback v0.76
→ Self-organizing improvement v0.78
→ Repository structure alignment v0.79
→ ...
→ Bounded blob materialization v1.19
```

v0.77 proposal branchesの存在は、`main`への統合を意味しません。

Lean rootとruntime rootは、実在する統合済みartifactだけを参照します。

## 完了した基盤

### 局所文脈、有限サイクル、Open Horizon

KuuOSは、multiple horizons、local sections、overlap eligibility、parallel transport、curvature、cocycle residue、path-dependent holonomyを分離します。

finite-cycle agentは、mission binding、観測、複数信念、semantic planning、独立検証、bounded memory、effect reconciliation、event wake-up、resource admission、governed change、checkpoint、restart recoveryを接続します。

Open Horizonは、有限な局所制御を将来可能性全体の閉鎖へ昇格させません。

### Qi-WORLD、MemoryOS、WORLD数学層

Qi Process Tensorは、複数時点のprocess、複数仮説、反証、不確実性、回復可能性区間を候補として保持します。

Qi-WORLD v2.3は、process supportとboundary occupationを陰陽相補系として接続します。

MemoryOSは、working、episodic、semantic、procedural memory、非マルコフ履歴、analytic capsule、contradiction residueを保持します。

WORLD数学サイドカーは、Hilbert空間、作用素環、modular theory、Araki entropy、Petz recovery、Jones theory、高次gauge情報幾何、真空候補、Tomita operator、四大相動力学までを型付きsurfaceとして接続します。

外部解析receiptとLean-derived theoremを混同しません。

### Gauge、Module-Bundle、MemoryOS application

v0.60からv0.69は、有限な接続改善候補、review、evaluation、staging、shadow、gauge validation、evidence capsule、external approvalを構成します。

v0.70からv0.72は、文脈代数上のstate module、意味部分加群、authority filtration、非可換Leibniz接続、read-only non-Markov memory kernelを構成します。

v0.73からv0.76は、有限候補評価、決定的選択、外部review、single-use atomic commit、監査可能なmonotonic rollbackを構成します。

v0.77のauthority-role topologyとpost-transition verificationは未統合提案です。

## Repository self-evolutionの統合済み連鎖

### v0.78からv0.92：自己改善、構造整合、承認、modeled application

| Version | 統合済み責務 |
|---|---|
| v0.78 | finite improvement proposal、bounded supervisor、停止条件、権限境界 |
| v0.79 | repository structure alignment candidate |
| v0.80 | alignment normal formとdeterministic normalization |
| v0.81 | incremental preservationとprotected-surface preservation |
| v0.82 | certificate chainとlineage verification |
| v0.83 | direct branch and revision observation |
| v0.84 | merge certificate |
| v0.85 | revision DAG certificate |
| v0.86 | local repository frontier certificate |
| v0.87 | bounded self-evolution portfolioとdeterministic selection |
| v0.88 | shadow realization、replay、normal-form preservation |
| v0.89 | multi-replay agreementに基づくgoverned admission |
| v0.90 | external approval、signature verification receipt、revocation status |
| v0.91 | exact scope-bound single-use application authorization |
| v0.92 | pure atomic repository application transition |

v0.92はisolated modeled stateを更新します。

live working tree、index、Git object database、referenceを暗黙に変更しません。

### v0.93からv1.02：Git object、reference、local finality、checkpoint

| Version | 統合済み責務 |
|---|---|
| v0.93 | deterministic blob、tree、commit candidate certificate |
| v0.94 | bounded single-use object materialization authorization |
| v0.95 | external object executionとpost-object observationを束縛するreceipt |
| v0.96 | direct local branch reference-update authorization |
| v0.97 | exact reference CASとnonce consumptionのmodeled atomic transition |
| v0.98 | external reference execution、observation、nonce receiptの統合receipt |
| v0.99 | delayed direct-reference stability and candidate reachability |
| v1.00 | bounded multi-sample local frontier finality |
| v1.01 | `refs/kuuos/checkpoints/`内のsingle-use checkpoint authorization |
| v1.02 | zero-OID CASとnonce consumptionのatomic modeled checkpoint creation |

この段階では、candidate generation、authorization、modeled transition、external execution report、post-operation observationを別層に保ちます。

### v1.03からv1.10：checkpoint receipt、workspace、review、repair、CAS contract

| Version | 統合済み責務 |
|---|---|
| v1.03 | v1.02 resultと独立観測を束縛するcheckpoint creation receipt |
| v1.04 | checkpointから派生作業を行うbounded evolution workspace |
| v1.05 | delayed stability、reachability、immutable-by-default evidence |
| v1.06 | discrepancy classificationとminimal human-review boundary |
| v1.07 | clean、create、repair、rejectを分離するdeterministic routing |
| v1.08 | checkpoint namespaceとrepair primitiveのcompatibility gate |
| v1.09 | exact expected OIDとproposed OIDを束縛するcheckpoint candidate |
| v1.10 | current OID observationを分離したcheckpoint CAS contract |

v1.03からv1.10は、checkpoint overwriteまたはlive Git mutationを自動許可しません。

### v1.11からv1.16：validation、coherence、authorization、modeled CAS

| Version | 統合済み責務 |
|---|---|
| v1.11 | upstream evidenceからcandidateを独立再計算するvalidation receipt |
| v1.12 | validated candidateとCAS contractのexact intake binding |
| v1.13 | candidate、contract、intakeのcoherence receipt |
| v1.14 | bounded single-use CAS authorization request |
| v1.15 | authorization decisionとnonce eligibility |
| v1.16 | fresh reference stateとnonce registryを更新するmodeled atomic CAS |

v1.16のCOMMITTED resultは、modeled checkpoint stateとnonce stateを一つの論理遷移として更新します。

v1.16単独ではlive Git commandを呼びません。

### v1.17からv1.19：限定live Git execution

| Version | 統合済み責務 |
|---|---|
| v1.17 | repository root、Git directory、object format、reference stateを固定commandでread-only observation |
| v1.18 | `refs/kuuos/checkpoints/`内の一つのdirect referenceをbounded compare-and-swap |
| v1.19 | exact payloadから一つのGit blob objectをmaterializeするかexact reuse |

v1.17はread-onlyです。

v1.18は、一つのcheckpoint direct referenceだけを更新します。

v1.19は、一つのblob object database writeだけを許可します。

v1.18とv1.19は、branch、tag、delete、force update、index、working tree、reflog、signing、remote pushを許可しません。

## Aggregate rootsの現在形

### Lean root

`formal/KuuOSFormal.lean`は、`main`へ統合済みのLean moduleだけをimportします。

```text
WORLD v0.27-v0.59
→ Gauge v0.60-v0.69
→ Module-Bundle / MemoryOS v0.70-v0.76
→ Self-organizing improvement v0.78
→ Repository self-evolution v0.79-v1.19
```

v0.77 proposal modulesとv1.20 active branch modulesはimportしません。

受入条件：

- `lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal`が成功する。
- nonexistent moduleまたはunmerged branch artifactを参照しない。
- dedicated rootとaggregate rootの境界が一致する。
- Lean-derived theoremとexternal receiptを分離する。

### Runtime root

`scripts/run_kuuos_runtime_full_check_v0_55.py`は互換名を保ち、統合済みruntime surfaceをv1.19まで実行します。

```text
legacy cumulative chain through v0.54
→ modular mesh and WORLD v0.55
→ WORLD v0.56 and v0.59
→ Gauge v0.60-v0.69
→ Module-Bundle / MemoryOS v0.70-v0.76
→ Self-organization and repository chain v0.78-v0.95
→ cumulative reference and checkpoint chain v0.96-v1.18
→ bounded blob validation v1.19
```

v0.77 proposal validatorsとv1.20 active branch validatorsは実行しません。

## Active research frontier

### 優先1：Bounded tree and commit materialization v1.20

**状態：Active Draft PR #942**

v1.20は、v0.93のdeterministic commit candidateと、必要なblobごとのvalid v1.19 resultを入力にします。

目標は、exact tree objectsと一つのexact commit objectだけをbounded Git object databaseへmaterializeすることです。

受入条件：

- candidate certificateを完全再検証する。
- すべてのcandidate blobがvalid v1.19 resultで被覆される。
- tree entryのmode、name、OID、orderingをexact bindingする。
- commit tree、parents、author、committer、message、encodingをcanonical payloadへ束縛する。
- literal Git executableとsanitized Git environmentを要求する。
- treeとcommit以外のobject writeを拒否する。
- reference、index、working tree、reflog、signing、pushを拒否する。
- post-write object type、size、content、OIDを再観測する。
- exact existing objectのreuseをmutationとして過大計上しない。
- write後のpostcondition failureでも発生したeffect accountingを消去しない。
- focused tests、strict Lean root、manifest、registry、aggregate rootを同期する。

merge前はv1.20を正式frontierへ昇格させません。

### 優先2：Materialized commitの独立receipt

**状態：次期候補、未採番**

v1.20 execution resultだけでcommit objectの成功を確定しません。

```text
v1.20 execution result
+ independent object observation
+ exact candidate replay
+ effect accounting
+ repository and executor binding
→ bounded tree and commit materialization receipt
```

受入条件：

- execution reportとpost-object observationを分離する。
- object type、canonical bytes、OID、reachability relationを再検証する。
- report substitution、observation substitution、candidate substitutionを拒否する。
- receipt constructionは追加mutationを行わない。
- receiptはreference-update authorityを生成しない。

### 優先3：Materialized commitからreference candidateへのhandoff

**状態：設計候補、未採番**

materialized commit objectの存在は、branchまたはcheckpoint referenceを更新する権限ではありません。

将来のhandoffでは、次を分離します。

```text
materialized commit receipt
→ reference target candidate
→ namespace and policy gate
→ independent authorization
→ fresh CAS preflight
→ bounded reference transition
→ post-reference observation
```

checkpoint、branch、tag、remote tracking referenceは別namespaceと別権限にします。

### 優先4：Aggregate root、manifest、registryの完全性固定

**状態：継続検証**

必須検査：

- `formal/KuuOSFormal.lean`がv0.76の後にv0.78からcurrent integrated frontierを参照する。
- 未統合v0.77またはactive PR moduleを参照しない。
- runtime rootがcurrent cumulative runtimeへ接続する。
- README、ROADMAP、CITATION、Lake version、Lean root、runtime rootを同期する。
- manifest、registry、workflow dependency chainを同期する。
- aggregate root未登録のversionを統合済み完了と記載しない。
- current frontierを機械可読manifestから検査できるようにする。

### 優先5：Checkpoint recoveryとhandover

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

### 優先6：v0.77 proposalsの再評価

**状態：再基底必要**

v0.77提案を再利用する場合、現在のv1.19 frontierへ直接mergeしません。

必要な処理：

- current `main`へ再基底する。
- v0.78以降とauthority namespaceが衝突しないか確認する。
- version番号を保持するか、新しいversionへ移すか決定する。
- current aggregate roots、manifests、workflow registryへ追加する。
- post-transition verificationをrepository self-evolution receipt chainと無条件に同一化しない。
- dedicated runtime testsとstrict Lean rootを再実行する。

### 優先7：分散repository adapter

**状態：中期研究課題**

single-host local Git contractを分散storeへ拡張する場合、compare-and-swap、fencing token、idempotency key、append-only receipt、bounded lease、independent observation、authority and executor separationを保持します。

### 優先8：一般OSの実行後検証閉路

**状態：OS統合課題**

将来のpost-transition verificationを、ActOS一般へ無条件に同一化しません。

```text
performed effect
→ raw observation
→ causal attribution
→ verification disposition
→ future-only learning delta
→ governed WORLD reconciliation candidate
```

verification failureから自動rollbackしません。

### 優先9：数学形式化frontier

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

現在の`main`はv1.19まで進んでいます。

古いbase SHAを持つopenまたはclosed-unmerged PRは、そのまま現在のfrontierとして扱いません。

### v1.20 Active Draft PR

PR #942はv1.19をbaseとするactive development branchです。

CI、formal root、runtime root、manifest、registry、documentationが揃い、reviewを経てmergeされるまでは未統合です。

### v0.77 proposal branches

Authority-role topologyとpost-transition verificationのv0.77枝は、`main`へ未統合です。

再利用時はcurrent-main rebase、namespace監査、version再決定、strict validationを要求します。

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
- live Git execution report outside disposable test repositories。
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
+ cumulative runtime registration
+ rollback, compensation, abort-preservation, or effect-accounting contract
+ documentation and citation synchronization
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
- closedまたはopenのunmerged PRを統合済みartifactとして記載しない。
- live mutation testの成功を任意repositoryへの実行許可として記載しない。

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
- memory kernel deformationとbase connection deformationを別ownerへ分離する。

### WORLDと物理解釈

- 数学的sidecar、WORLD表現、物理模型、経験的検証を別receipt classとして保持する。
- Qi Process Tensorを物理粒子ontologyへ短絡しない。
- analytic vacuumをexact physical vacuumへ昇格させない。
- modular timeをphysical timeへ同一視しない。

## 完了判定

KuuOSの研究roadmapは、単一の最終versionで閉じません。

各versionの完了は、有限scope、明示的authority、再現可能なvalidation、外部receiptとの境界、未解決事項の可視化によって判定します。

```text
local completion != global closure
bounded authority != universal sovereignty
validated artifact != truth
merged code != unrestricted execution
```
