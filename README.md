# KuuOS / 空OS

![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS** は、観測・文脈・記憶・WORLD 表現・計画・判断・実行・再観測・検証を、provenance、履歴、責任主体、有限権限、content address、検証可能な receipt に結び付ける公開研究アーキテクチャです。

現在の理論的中心は、仏教語を AI に貼り付けることではなく、**縁起を「対象を実体化する前の composable contextual transport」として構造化すること**です。量子・Choi・process tensor・gauge/groupoid はこの親構造の specialization であり、親定義そのものではありません。

## 現在地

**基準日：2026年8月25日 JST**

Authoritative branch は `main` です。現在の integrated functional baseline は:

```text
main functional milestone: 79e6d48029700fc3c998d28c87db069b3120bdab
latest integrated functional PR: #1420
parent formal frontier: filtered categorical cofinal dependent-origination semantics v1.4
downstream quantum specialization: integrated through causal tester / dual-recursion closure (#1415)
runtime dependent-origination executable surface: gauge-invariant local-to-global descent v0.1 (#1386)
current-frontier successor Draft: none designated
```

PR #1420 **Formalize filtered categorical cofinal dependent-origination semantics** は exact head `dc72e4dc022688002f8b99ab00acedef27b65211` で Governance Gate、Strict Lean formal validation、exact `Run selected Lean check` がすべて completed / success となった後、normal merge されました。authoritative merge SHA は `79e6d48029700fc3c998d28c87db069b3120bdab` です。

## 縁起の親構造

KuuOS の現在の parent definition は、一般の context category `Context` 上の state-valued functor です。

```text
Context  --D-->  Type

X --f--> Y
|        |
D(X) --> D(Y)
        D(f)
```

中心法則は:

```text
D(id) = id
D(g ∘ f) = D(g) ∘ D(f)
```

すなわち、

```text
縁起 = context に依存して成立する state
     + admissible relation に沿う transport
     + transport の compositional coherence
```

です。

この親構造では、最初から「同一の実体が各状況で姿を変える」とは仮定しません。context ごとに state carrier 自体が変わり得ます。可逆性も親には要求しません。

- context が groupoid なら transport は可逆になる。
- 一般 category では不可逆 transport を許す。
- finite history は free one-object category / free-monoid specialization として入る。
- memory-lifted history は enlarged state 上の specialization として入る。
- quantum/process-tensor/Choi は明示的 realization を追加した downstream specialization です。

## 現在の dependent-origination formal spine

現在の大きな流れは次です。

```text
#1400  functorial contextual transport parent
#1401-#1403
       contractive / gapped transfer specialization
       finite transfer-word specialization
#1404-#1407
       history-sensitive transport
       free-history category
       explicit memory-lifted state
       operational non-Markov process-tensor realization
#1408-#1415
       finite-dimensional Choi / comb specialization
       Choi PSD <-> Mathlib complete positivity
       native CPTP finite words
       quantum instruments and Born law
       arbitrary multi-slot Choi contraction
       open-comb history sensitivity
       tester probability law
       causal tester normalization <-> dual recursive normalization
#1416  restore the general contextual parent as the main spine
#1417  contextual refinement / overlap / semantic descent
#1418  refinement-of-refinement and exact descent transitivity
#1419  directed refinement nets and order-cofinal semantic invariance
#1420  arbitrary filtered indexing categories and categorical cofinal semantics
```

The parent non-quantum aggregate is:

```text
formal/KUOS/DependentOriginationCoreSpineV1_4.lean
```

Current parent frontier:

```text
formal/KUOS/DependentOriginationFilteredCofinalCategoryV1_4.lean
```

### 現在の主要定理的境界

Filtered indexing category `J` は、少なくとも以下を明示します。

```text
J is nonempty
any two objects admit a common future object
parallel arrows can be coequalized after further refinement
```

coherent state family `s_j` と transport-invariant readout `Q` に対しては、filteredness により任意の二 context の semantic value を共通 future で比較できるため、diagram 全体に一意の semantic value が存在します。

さらに objectwise cofinal indexing functor `F : K -> J` に対して、

```text
full filtered-diagram semantic descent
<->
semantic descent on the cofinal subsystem
```

を exact `ExistsUnique` equivalence として formalize しています。

一方で、

```text
cofinal semantic invariance
!= automatic recovery of one root state
```

です。root-state recovery には explicit local-state separation が追加で必要です。

この非対称性は意図的です。

```text
一意な意味が成立すること
!=
一個の大域的 substance carrier が存在すること
```

## 空OSとしての読み

現在の formal spine に対応する読みは:

```text
空   = どの一つの representation / chart / state carrier にも独立した絶対 authority を置かない
縁起 = 条件・文脈・関係に沿う composable transport によって成立を記述する
二諦 = invariant conventional meaning を formalize しても、それを ultimate substance に昇格しない
中道 = representation の実体化も、関係構造の消去も行わない
```

したがって KuuOS の縁起は「仏教哲学を AI に貼り付けた label system」ではなく、contextual/functorial/coherent transport を親にした形式構造です。

## Reversible / history / quantum specializations

親構造からの主要な枝は次の位置づけです。

| 枝 | 位置づけ |
|---|---|
| gauge / action groupoid / Čech | reversible presentation-change specialization |
| finite history | free-category specialization |
| memory-lifted non-Markov history | enlarged-state specialization |
| transfer semigroup | one-object additive irreversible specialization |
| process tensor | operational history-response realization |
| Choi / CP / CPTP / comb | finite-dimensional quantum realization |
| instruments / Born law | normalized quantum measurement specialization |

重要なのは、これら downstream specialization の成立から親の縁起を quantum や groupoid に同一視しないことです。

### Physical authority boundary

`itakura-hidetoshi/4d-mass-gap` の transfer/Hamiltonian/mass-gap proof pattern は KuuOS 側の structural motivation になっていますが、KuuOS はそのことによって physical Yang-Mills theorem authority を取得しません。

```text
KuuOS structural transport theorem
!=
4d-mass-gap physical theorem authority
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
| GitHub MCP | parent cross-observation v1.1 | `runtime/kuuos_github_mcp_sub_issue_chain_parent_cross_observation_v1_1.py` |
| Dependent origination runtime | executable gauge-invariant descent adapter v0.1 | `runtime/kuuos_gauge_invariant_dependent_origination_descent_v0_1.py` |
| Dependent origination parent formal | filtered categorical cofinal semantics v1.4 | `formal/KUOS/DependentOriginationFilteredCofinalCategoryV1_4.lean` |
| Dependent origination parent aggregate | non-quantum core spine v1.4 | `formal/KUOS/DependentOriginationCoreSpineV1_4.lean` |
| Repository formal baseline | strict aggregate import | `formal/KuuOSFormal.lean` |
| Canonical runtime root | deterministic current surface | `runtime/kuuos_current_check.py` |

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

The `dependent_origination` runtime profile still validates the executable/spec contract introduced in #1386. The newer formal chain through #1420 is strict Lean authority and is represented in current-root metadata; Python runtime checks do **not** substitute for Lean compilation.

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

## Legacy compatibility status surface

The current source of truth is `runtime/kuuos_current_check.py`, but historical current-root/readme identifiers remain compatibility markers because repository self-organization tests still validate them.

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

These compatibility tokens do not create new authority:

```text
active self-organization state != unbounded mutation authority
current root execution != production deployment
runtime success != external truth
README public status != authority grant
current surface CLI != authority grant
current surface index != authority grant
current surface artifact != authority grant
README surface exposure != authority grant
```

## Repository map

| Path | Role |
|---|---|
| `runtime/` | executable kernels, receipts, validators, canonical current root |
| `scripts/` | fail-closed checkers and cumulative runners |
| `formal/` | Lean theorem packages and aggregate roots |
| `specs/` | machine-readable / reviewable contracts |
| `manifests/` | package bindings and content-addressed declarations |
| `examples/` | deterministic reference projections |
| `status/` | historical and compatibility status artifacts |
| `docs/` | versioned theory, doctrine, subsystem indexes |
| `tests/` | runtime, tamper, boundary, and regression tests |
| `.github/workflows/` | governance, focused validation, separately authorized live gates |

## Development invariants

Normal changes begin from an exact `main` SHA on a dedicated branch and normally enter as Draft PRs. CI status is final only after workflow, job, and exact selected Lean step are completed. queued / in-progress state is not success or failure evidence.

Repository evolution remains append-only or tighten-only at frozen boundaries. Same-root requirements remain explicit wherever a theorem or receipt depends on them.

## Fixed boundaries

```text
candidate != authority
validation != truth
formal compilation != external theorem acceptance
CI success != theorem meaning beyond the compiled statement

observation != verification
selection != execution
receipt != successor authority

contextual transport != substance ontology
semantic descent != state descent
cofinal semantic invariance != root-state existence
filtered indexing != categorical colimit
objectwise cofinality != Mathlib final-functor theorem
reversible groupoid specialization != parent dependent origination
quantum realization != parent dependent origination
KuuOS structural theorem != physical Yang-Mills theorem authority

MCP write capability != Git authority
write accepted != effect verified
compensation != success

one benchmark sample != population performance
contract admitted != execution ready
comparison complete != performance claim approved
```

## Safety / research status

KuuOS is a research architecture. Repository-local validation establishes bounded consistency of the represented artifact set; it does not establish medical efficacy, legal authority, autonomous operational authority, physical truth, or universal external-service guarantees.
