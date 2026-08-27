# KuuOS / 空OS

![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS** は、観測・文脈・記憶・WORLD 表現・計画・判断・実行・再観測・検証を、provenance、履歴、責任主体、有限権限、content address、検証可能な receipt に結び付ける公開研究アーキテクチャです。

理論的中心は、仏教語を AI に貼り付けることではありません。現在の formal spine では、**縁起を「対象を実体化する前の composable contextual transport」として置き、その上に高次 coherence、presentation-independent invariants、process/quantum realization、scaled simplicial geometry を段階的に積む**方針を取っています。

## 現在地

**基準日：2026年8月27日 JST**

Authoritative branch は `main` です。

```text
latest integrated formal milestone SHA: 4e273f0d958b5ac4c27bb4f2b430a29ea6760968
latest integrated formal PR: #1483
latest integrated local scaled frontier: v1.69
runtime dependent-origination executable scope: #1386 adapter v0.1
```

PR #1483 **Classify the complete three-simplex A/B residual table** は Governance Gate、Strict Lean formal validation、exact `Run selected Lean check` が completed / success となった後、normal merge されました。authoritative formal milestone SHA は `4e273f0d958b5ac4c27bb4f2b430a29ea6760968` です。`main` HEAD は documentation / governance-only synchronizationでこの milestone より先へ進み得ますが、それだけで formal theorem frontier が進んだとは扱いません。

現在の重要な frontier は、`v1.69` で固定 `Δ[3]` 上の type-(A)/(B) residual table が exact に閉じたところです。まだ **全 boundary-prism rank cell が literal に pure A または A followed by one B completion であること**、および **scaled rank filtration から v1.59 cellular certificate を構成すること**は未完了です。

## 縁起の親構造

KuuOS の parent definition は、一般の context category `Context` 上の state-valued functor です。

```text
Context  --D-->  Type

X --f--> Y
|        |
D(X) --> D(Y)
        D(f)
```

中心法則は

```text
D(id) = id
D(g ∘ f) = D(g) ∘ D(f)
```

です。したがって親レベルでは

```text
縁起 = context に依存して成立する state
     + admissible relation に沿う transport
     + transport の compositional coherence
```

と読みます。

この親構造は最初から一つの固定 substance carrier を仮定しません。context ごとに state carrier 自体が変わり得ます。可逆性も親には要求しません。

- groupoid context は reversible specialization;
- finite history は free-category / one-object specialization;
- transfer semigroup は irreversible dynamical specialization;
- memory-lifted history は enlarged-state specialization;
- process tensor / Choi / CPTP / comb / tester は downstream operational/quantum realization;
- higher categorical and scaled simplicial layers are coherence/presentation structures above the same parent idea.

## Formal architecture

現在の formal authority は一つの linear version number ではなく、相互に接続された複数の層から成ります。

### 1. Contextual parent semantics

主要な流れ:

```text
#1416  contextual transport parent v1.0
#1417  contextual refinement / semantic descent v1.1
#1418  refinement transitivity v1.2
#1419  directed cofinal semantics v1.3
#1420  filtered categorical cofinal semantics v1.4
#1422  two-cell refinement coherence v1.5
#1423  native bicategorical coherence + operadic axis v1.6-v1.7
#1424  higher multicategory + monoidal process theory v1.8-v1.9
#1425-#1427
       causal process / marginals / no-signalling / joint causal factorization
#1428  enriched / stack / infinity-coherence optional layers v1.13-v1.15
#1429  category-of-elements dependent nerve: strict Segal + quasicategory v1.16
```

重要な境界は現在も変わりません。

```text
unique invariant semantics
!=
one recovered root state
```

state/root-carrier recovery には explicit separation/descent data が必要です。

### 2. Higher-categorical and presentation-independent realization

```text
#1430-#1431
       bicategorical 2-Yoneda, native mapping quasicategories,
       local scaled / complete-Segal interfaces
#1432  one global scaled Duskin nerve
#1433-#1435
       scaled-horn coherence and local/global 1-2 cell comparison
#1436  presentation-independent invariant kernel
#1437  invariance across bicategorical model equivalence
#1440-#1441
       strictly-unitary global Duskin transport and normalization-choice invariance
#1442-#1451
       scaled horn transport, presentation equivalence,
       global Duskin prisms, homotopy-class invariance,
       and conditional strictification
```

この系列での基本原則は

```text
presentation -> intrinsic bicategorical carrier -> observable
```

です。local mapping nerve や global Duskin nerve のどちらか一方を substance とせず、presentation を越えて保持される intrinsic data を invariant とします。

### 3. Canonical scaled-anodyne weak factorization system

`ScaledSSet` 上では、canonical horn-cylinder attachment family `T` を generator として

```text
canonicalGeneratedScaledAnodyne = T.rlp.llp
canonicalGeneratedScaledFibration = T.rlp
```

を構成しています。

```text
#1452-#1454  cylinder / attachment lifting -> native terminal RLP
#1455         canonical generator closure T.rlp.llp
#1456         orthogonal universality / WFS interface
#1458         Mathlib small-object interface
#1459         explicit colimits + finite presentability -> unconditional WFS
#1460         external generator comparison interface
#1461         external presentation -> global Duskin fibrancy
```

#1459 で canonical KuuOS family 自身について small-object/WFS route は内部的に閉じています。

ただし次の区別は厳守します。

```text
canonical KuuOS arbitrary-scaling attachment family
!= automatically
standard/Lurie A/B/C scaled-anodyne presentation
```

### 4. Standard scaled-anodyne A/B/C comparison

標準 generator 側は現在かなり具体化されています。

```text
#1462  canonical attachmentsを induced-scaling factorへ分解
#1463  standard type-(A) scaled inner horns
#1464-#1469
       endpoint pushout product / native Leibniz mate /
       interval cylinder / source enrichment /
       categorical scaled Leibniz pushout
#1470  standard type-(B) scaling-enrichment pushouts
#1471  q12/q23 three-simplex B completions
#1472  standard type-(C) collapsed-edge generators
#1473  standard A/B/C cellular closure and exact certificate target
```

標準 A/B/C generator familyとその generated classes は formalized 済みです。一方、canonical KuuOS family は arbitrary scaling を許すため、**canonical family = standard A/B/C family** とは主張していません。

### 5. Current frontier: type-(A) endpoint boundary prism

#1474 以降は、v1.59 の endpoint Leibniz cellular certificate を実際に構成するための prism geometry を進めています。

```text
#1474  endpoint prism factorization through full interval-boundary prism
#1475  ordinary boundary prism = inner relative cell complex
#1476  exact pullback-scaled cells; residual only in dimensions 2/3
#1477  attached dimension = n or n+1
#1478  top cells = canonical staircase σ_r
#1479  exact criterion for pure type-(A) cobase change
#1480  every cell is type-(A)-compatible
#1481  n=2 cells have maximal actual target; N=2 is pure A
#1482  q12/q23 completed scaling = maximal scaling on Δ[3]
#1483  complete fixed Δ[3] A/B residual table
```

現在 exact に統合済みの three-simplex table は

```text
cell index 1:
  missing face = 023
  horn-saturated A base = q12 base
  q12 B completion -> maximal Δ[3]

cell index 2:
  missing face = 013
  horn-saturated A base = q23 base
  q23 B completion -> maximal Δ[3]
```

また `g.n = 2, N = 3` の actual target scaling は maximal です。

### まだ未証明の直近境界

次は local geometry を増やす段階ではなく、fixed `Δ[3]` table を actual dependent cell に categorical に戻す段階です。

```text
1. N=3 actual A-pushout を fixed Δ[3] table へ canonical transport
2. equal branch g.n = N = 3 の first-coordinate endomorphismを identity と証明
3. equal branchを pure A に閉じる
4. n=2 top branchを literal A -> q12/q23 B completion と同定
5. staircase r=0,1,2 を q23,q23,q12 に exact 分類
6. 全 rank cell = pure A または A followed by one B completion
7. scaled rank filtrationを構成
8. StandardABCTypeAEndpointLeibnizCellularCertificate を構成
```

この certificate が得られて初めて、standard A/B/C cellular closure を用いた endpoint Leibniz stability を theorem-level に閉じられます。

## 空OSとしての読み

現在の formal architecture に対応する読みは:

```text
空   = 一つの representation / chart / carrier に絶対 authority を置かない
縁起 = 条件・文脈・関係に沿う composable transport によって成立を記述する
二諦 = presentation-independent meaning を証明しても、それを ultimate substance に昇格しない
中道 = representation の実体化も、relation/coherence の消去も行わない
```

sheaf / stack、operad / multicategory、process theory、enriched category、higher category、causal structure は現在、親の contextual transport を置き換えるものではなく、それぞれ追加構造を持つ specialization / realization として formalize されています。

## Quantum and physical authority boundary

量子系列では Choi / complete positivity / CPTP finite words / instruments / comb / tester / dual recursive normalization まで integrated されています。ただし quantum realization は親の縁起そのものではありません。

`itakura-hidetoshi/4d-mass-gap` の transfer/Hamiltonian/Yang-Mills formalization は KuuOS の structural motivation になり得ますが、repository authority は分離されています。

```text
KuuOS structural theorem
!=
4d-mass-gap physical Yang-Mills theorem authority
```

## Integrated subsystem map

Subsystem versions are independent; one linear maturity scaleではありません。

| 系列 | 統合済み到達点 | 主な入口 |
|---|---|---|
| Repository lineage | self-organization v0.113 | `runtime/kuuos_current_root_sequence_v0_113.py` |
| ObserveOS | v0.7 | `docs/ObserveOS/README.md` |
| VerifyOS | v0.15 | `docs/VerifyOS/README.md` |
| Qi architecture | Yin-Yang Wuxing Fibonacci History Geometry v2.5 | `docs/KUUOS_QI_YINYANG_WUXING_FIBONACCI_HISTORY_GEOMETRY_v2_5.md` |
| PlanOS | v1.23 | `formal/KuuOSPlanOSV1_23.lean` |
| DecisionOS | v0.6 | `formal/KuuOSDecisionOSV0_6.lean` |
| MemoryOS | v1.00 | `formal/KuuOSMemoryOSV1_00.lean` |
| CodeAI | frozen cohort / prediction-pack / execution-shard contract v0.1 | `docs/CodeAI/README.md` |
| GitHub MCP | durable event-driven reentry v1.3 + parent cross-observation v1.1 | `runtime/kuuos_github_ci_durable_reentry_inbox_v1_3.py` |
| Dependent origination runtime | executable gauge-invariant descent adapter v0.1 | `runtime/kuuos_gauge_invariant_dependent_origination_descent_v0_1.py` |
| Contextual parent formal | contextual transport / filtered semantic descent / higher coherence | `formal/KUOS/` |
| Global higher realization | scaled Duskin / presentation-independent invariant / scaled horn fibrancy | `formal/KUOS/` |
| Canonical scaled WFS | `T.rlp.llp / T.rlp`, explicit small-object construction | `formal/KUOS/` |
| Standard A/B/C comparison | explicit A/B/C generators and endpoint-prism cellular frontier v1.69 | `formal/KUOS/DependentOriginationStandardTypeABoundaryPrismThreeResidualClassificationV1_69.lean` |
| Repository strict Lean baseline | aggregate import | `formal/KuuOSFormal.lean` |

## Canonical runtime root

Standard entrypoint:

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py
```

Useful views:

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py --summary
PYTHONPATH=. python3 runtime/kuuos_current_check.py --list

PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile repository
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile architecture
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile planos
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile decisionos
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile memoryos
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile codeai
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile github_mcp
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile dependent_origination
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile all
```

The runtime root remains deterministic and effect-free. It does not perform live GitHub writes, workflow dispatch, external benchmark execution, external artifact acquisition, or gold-material access.

The `dependent_origination` runtime profile still validates the executable/spec contract introduced in #1386. The much newer formal theorem line through #1483 is strict Lean authority; Python runtime checks do **not** substitute for Lean compilation.

## Formal validation

Lean toolchain and dependencies are repository-pinned.

```bash
lake update
lake exe cache get
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KuuOSFormal
```

Formal compilation establishes only the repository theorem surface under the pinned toolchain. It does not substitute for external theorem acceptance, empirical validity, clinical approval, organizational approval, production deployment, or live-service behavior.

## Repository development invariants

Normal changes begin from an exact `main` SHA on a dedicated branch and normally enter as Draft PRs. CI status is final only after workflow, job, and exact selected Lean step are completed. queued / in-progress state is not success or failure evidence.

Repository evolution remains append-only or tighten-only at frozen boundaries. Same-root requirements remain explicit wherever a theorem or receipt depends on them.

## Legacy compatibility status surface

Historical current-root/readme identifiers remain compatibility markers because repository self-organization tests still validate them.

```text
KuuOS README Public Status v0.66
kuuos_current_root_sequence_v0_66
docs/kuuos_readme_public_status_v0_66.md

KuuOS Current Root Execution Connection v0.65
kuuos_current_root_sequence_v0_65
docs/kuuos_self_organization_active_state.md
self_organization_active: true
execution_scope: publish_active_self_organization_state
state_publication_applied: true

KuuOS README Surface Exposure v0.78
kuuos_current_root_sequence_v0_78
docs/kuuos_readme_surface_exposure_v0_78.md
runtime/kuuos_current_surface.py
runtime/kuuos_current_surface_entrypoint_v0_77.py
status/current.surface.index.json
status/current.surface.json
status/current.resolved.json
status/current.manifest.json
PYTHONPATH=. python3 runtime/kuuos_current_surface.py
```

These compatibility tokens do not create new authority.

## Fixed boundaries

```text
candidate != authority
validation != truth
formal compilation != external theorem acceptance
CI success != theorem meaning beyond the compiled statement

contextual transport != substance ontology
semantic descent != state descent
cofinal semantic invariance != root-state existence
reversible specialization != parent dependent origination
quantum realization != parent dependent origination
presentation-independent invariant != one privileged presentation

canonical arbitrary-scaling KuuOS generator family
!= standard A/B/C generator-level family

local three-simplex A/B table
!= completed scaled rank filtration

standard A/B/C cellular certificate
!= full canonical/external comparison until remaining inclusions are proved

KuuOS structural theorem != physical Yang-Mills theorem authority

MCP write capability != Git authority
write accepted != effect verified
receipt != successor authority
```

## Safety / research status

KuuOS is a research architecture. Repository-local validation establishes bounded consistency of the represented artifact set; it does not establish medical efficacy, legal authority, autonomous operational authority, physical truth, or universal external-service guarantees.
