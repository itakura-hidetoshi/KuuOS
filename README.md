# KuuOS / 空OS

![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS** は、観測・文脈・記憶・WORLD 表現・計画・判断・実行・再観測・検証を、provenance、履歴、責任主体、有限権限、content address、検証可能な receipt に結び付ける公開研究アーキテクチャです。

理論的中心は、仏教語を AI に貼り付けることではありません。現在の formal spine では、**縁起を「対象を実体化する前の composable contextual transport」として置き、その上に高次 coherence、presentation-independent invariants、process/quantum realization、scaled simplicial geometry を段階的に積む**方針を取っています。

## 現在地

**基準日：2026年8月28日 JST**

Authoritative branch は `main` です。

```text
latest integrated formal milestone SHA: 9d8d9be1c001f0a6f7dbd0b30922c42066c9b21d
latest integrated formal PR: #1535
latest integrated local scaled frontier: v1.120
runtime dependent-origination executable scope: #1386 adapter v0.1
```

PR #1535 **Prove terminal fibrancy does not faithfully reflect presentation order** は、PR #1534 / v1.119 で確定した standard/canonical orthogonality diamond を terminal-map slice に制限し、presentation の strict inequality が fibrant-object semantics では collapse し得ることを theorem-level に閉じました。

現在の authoritative mathematical picture は次です。`S` を standard A/B/C generated presentation、`C` を canonical KuuOS generated presentation とします。

```text
full generated left classes:
  L_standard || L_canonical

full generated right classes:
  R_standard || R_canonical

presentation lattice:

        S ⊔ C
        /   \
       S     C
        \   /
        S ⊓ C

all four displayed edges are strict.

terminal/fibrant-object semantics:
  Fib_C ⊊ Fib_S
```

さらに `U := S ⊔ C` とすると、v1.86 の complete-lattice right-class formula と v1.115 の terminal implication により

```text
R_U = R_S ∩ R_C

Fib_U(X)
↔ Fib_S(X) ∧ Fib_C(X)
↔ Fib_C(X)
```

が成り立つ一方、v1.119 により

```text
C < U
```

です。したがって

```text
C < S ⊔ C
but
∀ X, Fib_C(X) ↔ Fib_(S ⊔ C)(X)
```

であり、presentation から fibrant objects への意味写像は injective でも order-reflecting でもありません。

これは矛盾ではありません。terminal maps は generated right class 全体の special slice であり、full orthogonal theory の違いを忠実に保持する必要はありません。

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

canonical KuuOS family 自身について small-object/WFS route は内部的に閉じています。

```text
(canonicalGeneratedScaledAnodyne,
 canonicalGeneratedScaledFibration)
is a native weak factorization system.
```

### 4. Generated-presentation quotient and complete lattice

literal generator list 自体を invariant とせず、mutual orthogonal generation で quotient した generated-presentation carrier を使います。

```text
v1.81  quotient by mutual generation
v1.83  posetal reflection
v1.84  order reflection
v1.85  fixed-point order isomorphism
v1.86  complete lattice
v1.87  standard/canonical lower and upper envelopes
```

presentation `P` には generated orthogonal pair

```text
L_P := generatedAnodyneClass P
R_P := generatedFibrationClass P

L_P.rlp = R_P
R_P.llp = L_P
```

が付随し、presentation order は

```text
P ≤ Q  ↔  L_P ≤ L_Q
       ↔  R_Q ≤ R_P
```

です。

arbitrary joins については

```text
R_(⨆ i, P_i) = ⨅ i, R_(P_i)
```

が Mathlib complete-lattice structure から exact に得られます。

### 5. Standard/canonical comparison — resolved as incomparability

standard A/B/C family と canonical KuuOS arbitrary-scaling attachment family は、generator list が違うだけでなく、generated full orthogonal theories も一致しません。

v1.107 と v1.118 の二方向の separator により、v1.119 で

```text
L_standard || L_canonical
R_standard || R_canonical
S || C
```

が確定しました。

具体的には、canonical-not-standard 側には atomic scaling / `B^2 N` terminal witness があり、standard-not-canonical 側には degree-three Type-A horn `Λ[3,1] -> Δ[3]` の relative rigidity separator があります。

したがって旧 comparison frontier

```text
standard ≤ canonical
or
canonical ≤ standard
```

を「残りの Type-A / Type-C geometry を埋めれば達成される目標」として扱うことは終了しました。Type-C geometry 自体の研究は可能ですが、それによって global inclusion や equality を復活させることはできません。

### 6. Terminal semantics — strict order and non-faithfulness

v1.115 では object-level terminal maps に限って

```text
Fib_canonical ⊊ Fib_standardABC
```

が確定しました。これは full right classes の incomparability と両立します。

v1.120 ではさらに upper envelope `U = S ⊔ C` に対して

```text
R_U = R_S ∩ R_C
Fib_U = Fib_C
C < U
```

を証明しました。

主要 theorem surface:

```text
generatedFibrationClass_upperEnvelope
upperEnvelope_isFibrant_iff_standard_and_canonical
upperEnvelope_isFibrant_iff_canonical
canonical_lt_upperEnvelope_but_same_fibrant_objects
fibrantObjectSemantics_canonical_eq_upperEnvelope
fibrantObjectSemantics_not_injective
fibrantObjectSemantics_not_orderReflecting
```

したがって terminal/fibrant-object semantics は presentation distinction の一部を忘却します。

## Retired formal frontiers

v1.69 時点の fixed `Δ[3]` A/B residual table や boundary-prism cellular classification は、その後の theorem progression のための中間 frontier でした。README / ROADMAP が長くそれを current frontier と表示していましたが、現在は historical milestone です。

同様に、standard/canonical equality または一方向 inclusion を最終目標とする comparison program は v1.119 により theorem-level に退役しています。

現在の presentation-independent 問題は「二つの presentations が同じか」ではなく、**どの semantic projection が full orthogonality information のどの部分を保持し、どの部分を忘れるか**です。

## 空OSとしての読み

現在の formal architecture に対応する読みは:

```text
空   = 一つの representation / chart / carrier に絶対 authority を置かない
縁起 = 条件・文脈・関係に沿う composable transport によって成立を記述する
二諦 = presentation-independent meaning を証明しても、それを ultimate substance に昇格しない
中道 = representation の実体化も、relation/coherence の消去も行わない
```

v1.119-v1.120 はこの原則を order-theoretic に sharpen します。同じ terminal semantics を持つことは full presentation の同一性を意味しません。observable / semantic slice が一致しても、その背後の orthogonality structure を一つの実体として同一視しない、という区別が formal theorem になっています。

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
| Generated-presentation lattice | quotient / posetal reflection / complete lattice | `formal/KUOS/DependentOriginationGeneratedPresentationCompleteLatticeV1_86.lean` |
| Standard/canonical orthogonality | strict diamond and full left/right incomparability v1.119 | `formal/KUOS/DependentOriginationStandardCanonicalOrthogonalityDiamondV1_119.lean` |
| Terminal fibrancy semantics | non-faithful presentation order v1.120 | `formal/KUOS/DependentOriginationTerminalFibrancyNonfaithfulPresentationOrderV1_120.lean` |
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

The `dependent_origination` runtime profile still validates the executable/spec contract introduced in #1386. The formal theorem line through #1535 is strict Lean authority; Python runtime checks do **not** substitute for Lean compilation.

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

Normal changes begin from an exact `main` SHA on a dedicated branch and normally enter as Draft PRs. CI status is final only after workflow, all jobs, exact selected Lean step, committed dependency manifest check, and governance/audit summary are completed / success. queued / in-progress state is not success or failure evidence.

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

full standard/canonical presentation incomparability
!= terminal/fibrant-object incomparability

same fibrant-object semantics
!= equal generated presentation

presentation inequality
!= terminal-semantic inequality

Type-C geometric refinement
!= restoration of a globally refuted presentation inclusion

KuuOS structural theorem != physical Yang-Mills theorem authority

MCP write capability != Git authority
write accepted != effect verified
receipt != successor authority
```

## Safety / research status

KuuOS is a research architecture. Repository-local validation establishes bounded consistency of the represented artifact set; it does not establish medical efficacy, legal authority, autonomous operational authority, physical truth, or universal external-service guarantees.
