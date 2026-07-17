# KuuOS / 空OS

![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS**は、観測、信念、記憶、WORLD表現、計画、判断、実行、検証、学習を、由来、局所文脈、履歴、責任主体、有限権限、検証可能なreceiptへ結び付ける公開研究アーキテクチャです。

KuuOS is a public, governance-gated, proof-facing, non-Markovian, Qi-process-aware architecture for relational AI and bounded self-evolution research.

KuuOSは、候補と権限、予測と事実、検証と真理、選択と実行、記憶と主権を同一視しません。production AGI runtimeでもありません。

## 現在地

**基準日：2026年7月18日 JST**

公開状態のauthoritative branchは`main`です。最新の機能統合はPR #1283、**VerifyOS v0.14 Independent Evidence Verification v0.1**です。この公開面は、そのsquash merge commit `461f37e02f2439bd6fd4f2c21e72885d6d944df6`を基準に同期しています。

| 面 | 統合済み到達点 | 主な入口 |
|---|---|---|
| Repository lineage | self-organization v0.113 | `runtime/kuuos_current_root_sequence_v0_113.py` |
| ObserveOS | v0.7 sequential epistemic observability envelope | `docs/ObserveOS/README.md` |
| VerifyOS | v0.14 independent evidence verification | `docs/VerifyOS/README.md` |
| PlanOS | v1.23 finite Physical Quantum Qi coherence kernel and partial dephasing | `formal/KuuOSPlanOSV1_23.lean` |
| DecisionOS | v0.6 WORLD-conditioned relational deliberation | `formal/KuuOSDecisionOSV0_6.lean` |
| MemoryOS | v1.00 finite bounded closed-support lattice | `formal/KuuOSMemoryOSV1_00.lean` |
| WORLD dependency | KuuOS v14.0 causal WORLD state | read-only source for the integrated PlanOS line |
| Canonical runtime root | repository、PlanOS、DecisionOS、MemoryOS | `runtime/kuuos_current_check.py` |

subsystem versionは独立しています。ObserveOS v0.7、VerifyOS v0.14、PlanOS v1.23、DecisionOS v0.6、MemoryOS v1.00、self-organization v0.113を、一つの直線的version番号として扱いません。

未mergeの旧Draftや分岐は、現在の`main`へrebaseし、scopeと検証を更新しない限りcurrent frontierとはみなしません。

## Canonical runtime root

標準入口は次です。

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py
```

current rootは次を束ねます。

```text
repository mutation and self-organization lineage through v0.113
→ PlanOS active frontier v0.91-v1.23
→ DecisionOS cumulative validation v0.1-v0.6
→ MemoryOS active frontier v0.40-v1.00
```

ObserveOS v0.7とVerifyOS v0.13-v0.14はこのprofile rootへ暗黙に追加せず、各専用workflow、Evidence Cycle累積runner、versioned formal aggregateで独立検証します。

run-all-then-decide方式で、一つのstepが失敗しても残りを実行し、必要stepの失敗を最後に集約します。

### Profiles

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile repository
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile planos
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile decisionos
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile memoryos
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile all
```

| Profile | 検査面 |
|---|---|
| `repository` | repository mutationとself-organizationの累積lineage |
| `planos` | PlanOS v0.91-v1.23のactive frontier |
| `decisionos` | DecisionOS v0.1-v0.6のcumulative validation |
| `memoryos` | MemoryOS v0.40-v1.00のactive frontier |
| `all` | 上記すべて |

現在のfrontier、各profileのstep数、基準日、機能統合commitはruntimeから取得できます。

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py --summary
PYTHONPATH=. python3 runtime/kuuos_current_check.py --list
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile memoryos --list
```

root成功は、登録されたrepository内surfaceが、そのrevisionで再現可能に整合したことを示します。外部定理受理、経験的真理、臨床承認、組織承認、production deployment、無制限実行権限を意味しません。

## ObserveOS v0.7

ObserveOS v0.7は、観測対象の真偽判定ではなく、**観測過程そのものの可観測性、由来、欠測、逐次不確実性、校正、分布変化**をsource-bound envelopeとして記録します。

```text
ObserveOS v0.6 bounded maintenance-monitoring observation receipt
→ ObserveOS v0.7 sequential epistemic observability envelope
→ VerifyOS v0.13 independent verification handoff
→ VerifyOS v0.14 independent evidence verification
```

統合された検査面は次です。

- W3C Trace Contextによるtrace/span相関
- OpenTelemetry traces、metrics、logs、baggageのsignal coverage
- W3C PROV-OのEntity、Activity、Agent、relation provenance
- observed / missing / total sampleのexact accountingとmissingness budget
- ADWIN distribution-shift evidence
- confidence sequence / e-processの逐次不確実性evidence
- split / online conformal calibration evidence
- observation window、replay closure、current-effect negative、authority negative

14のdispositionを、supported、repair、review、replay rejection、current-state mutation rejection、authority escalation rejectionへ分離します。

```text
observation != verification
observability receipt != verification verdict
WORLD intake != WORLD update
WORLD sidecar != exact WORLD
receipt composition != receipt construction
learning != present-cycle mutation
```

主な入口は次です。

| Surface | Path |
|---|---|
| Structured subsystem index | `docs/ObserveOS/README.md` |
| Versioned specification | `docs/OBSERVEOS_SEQUENTIAL_EPISTEMIC_OBSERVABILITY_ENVELOPE_v0_1.md` |
| Runtime envelope | `runtime/kuuos_observeos_sequential_epistemic_observability_envelope_v0_1.py` |
| Route checker | `scripts/check_observeos_sequential_epistemic_observability_envelope_v0_1.py` |
| Formal kernel | `formal/KUOS/ObserveOS/SequentialEpistemicObservabilityEnvelopeV0_7.lean` |
| Formal aggregate | `formal/KuuOSObserveOSV0_7.lean` |
| Dedicated workflow | `.github/workflows/observeos-sequential-epistemic-observability-v0-1.yml` |

## VerifyOS v0.13 — independent verification handoff

VerifyOS v0.13は、supportedなObserveOS v0.7 receiptを消費し、独立検証のためのimmutable request artifactを準備します。観測を再収集せず、検証を完了せず、真理または因果確証を主張しません。

```text
ObserveOS v0.7 sequential epistemic observability envelope
→ VerifyOS v0.13 independent verification handoff
→ VerifyOS v0.14 independent evidence verification
```

requestは、source receipt、trace/provenance識別子、immutable evidence snapshot、environment snapshot、verification protocol、acceptance criteria、reproduction plan、verifier/reviewer independence、bounded window、replay closureをexact bindingします。

15のdispositionを、supported、source/correspondence repair、WORLD/context/review refresh、independence/evidence/protocol/criteria/reproduction/window repair、replay rejection、current-state mutation rejection、authority escalation rejectionへ分離します。

supported routeでも`verification_completed = false`と`verification_debt_open = true`を維持します。WORLD revision、plan、policy、learning、tool invocation、external effectを変更せず、selection、WORLD mutation、policy activation、execution authorityを付与しません。

| Surface | Path |
|---|---|
| Specification | `docs/KUUOS_VERIFYOS_SEQUENTIAL_EPISTEMIC_OBSERVATION_VERIFICATION_HANDOFF_v0_1.md` |
| Runtime handoff | `runtime/kuuos_verifyos_sequential_epistemic_observation_verification_handoff_v0_1.py` |
| Checker | `scripts/check_verifyos_sequential_epistemic_observation_verification_handoff_v0_1.py` |
| Manifest | `manifests/kuuos_verifyos_sequential_epistemic_observation_verification_handoff_v0_1.json` |
| Formal kernel | `formal/KUOS/VerifyOS/SequentialEpistemicObservationVerificationHandoffV0_13.lean` |
| Formal aggregate | `formal/KuuOSVerifyOSV0_13.lean` |
| Workflow | `.github/workflows/verifyos-sequential-epistemic-observation-verification-handoff-v0-1.yml` |

## VerifyOS v0.14 — independent evidence verification

VerifyOS v0.14は、canonicalでsupportedなv0.13 handoff receiptを入力とし、独立evidence、再計算、再現試行、falsification challenge、acceptance criteria、独立reviewを一つのverification cycleへ束縛します。

結果は次の三つを分離します。

```text
passed        → verification completed、debt closed
failed        → verification completed、debt closed
indeterminate → verification completed、debt open、reobservation required
```

v0.14は次をexact bindingします。

- source v0.13 handoff receiptとObserveOS receipt
- independent evidence sourceとartifact digest
- recomputed sequential uncertainty、conformal calibration、distribution shift evidence
- preregistered protocol、acceptance criteria、reproduction plan
- planned / completed / successful reproduction attempts
- falsification challengeとresult review
- verification session、nonce、operation、cycleのreplay closure
- WORLD revision、history、lineage、responsibility monotonicity

14のdispositionを、passed、failed、indeterminate、source/correspondence/independence/evidence/protocol/reproduction/acceptance/review repair、replay rejection、current-state mutation rejection、authority escalation rejectionへ分離します。

```text
verification != truth
verification outcome != causal attribution
passed != WORLD adoption
failed != WORLD rejection
indeterminate != evidence deletion
verification receipt != WORLD mutation
verification receipt != policy activation
verification receipt != execution authority
```

runtime kernelは供給されたartifactを判定・記録します。外部観測の再収集、host effect、WORLD mutation、policy activation、tool invocationを実行しません。

| Surface | Path |
|---|---|
| Structured subsystem index | `docs/VerifyOS/README.md` |
| Versioned specification | `docs/KUUOS_VERIFYOS_INDEPENDENT_EVIDENCE_VERIFICATION_v0_1.md` |
| Runtime verification | `runtime/kuuos_verifyos_independent_evidence_verification_v0_1.py` |
| Route checker | `scripts/check_verifyos_independent_evidence_verification_v0_1.py` |
| Manifest | `manifests/kuuos_verifyos_independent_evidence_verification_v0_1.json` |
| Formal kernel | `formal/KUOS/VerifyOS/IndependentEvidenceVerificationV0_14.lean` |
| Formal aggregate | `formal/KuuOSVerifyOSV0_14.lean` |
| Dedicated workflow | `.github/workflows/verifyos-independent-evidence-verification-v0-1.yml` |

専用CIはPython surfaces、manifest、全14 outcome/repair/rejection routes、tampered digest fail-closed、Evidence Cycle累積回帰、pinned dependency manifest、VerifyOS v0.14 formal root、repository formal aggregateをstrict modeで検証します。

## PlanOS v1.23

PlanOSのcurrent rootは、次の三つの層を保持します。

```text
v0.91-v1.02
information geometry、Qi-conditioned temperature、WORLD-conditioned distribution、DecisionOS advisory handoff

v1.05-v1.20
state-dependent geometry、curvature、geodesic deviation、finite topology、homology、persistence、transport and barycenter structure

v1.21-v1.23
finite Physical Quantum Qi path histories、Gaussian amplitudes、homotopy-block structure、exact rational partial dephasing
```

v1.23は、保持された全history上に有限Hermitian coherence kernelを構成し、完全coherent endpoint kernelからhomotopy-block kernelまでの有理数dephasing trajectoryを検証します。

```text
uncertainty != one best branch
interference != scalar utility
partial dephasing != history deletion
coherence observable != selection authority
```

historyのranking、pruning、selection、activation、executionは行いません。

## DecisionOS v0.6

DecisionOS v0.6は、WORLD-conditioned evidence intakeから、Wa support、stakeholder support、relational support、dissent pressure、minority-impact risk、uncertainty burdenの六次元relational profileを構成し、Pareto型のnon-dominated relational frontierを返します。

```text
PlanOS probability and action ranking
→ DecisionOS evidence intake
→ relational partial-order deliberation
→ relational frontier
```

relational frontierはselected candidateではなく、DecisionOS selection receipt、PlanOS replan、WORLD mutation、ActOS invocationも生成しません。

## MemoryOS v1.00

MemoryOS current rootはv0.40からv1.00までの累積chainを保持します。最新のclosure-theoretic sublineは次です。

```text
v0.91 counterexample-guided closed-context refinement
→ v0.92 finite batch context saturation
→ v0.93 minimal-generator closure quotient
→ v0.94 choice-free generator antichain signatures
→ v0.95 signature hull and kernel-order duality
→ v0.96 pointed closed-context lattice
→ v0.97 finite-family lattice operations
→ v0.98 sensor-kernel polarity and fixed points
→ v0.99 typed order anti-isomorphism
→ v1.00 finite bounded closed-support lattice
```

固定されたsensor family、atlas、target defect、route rootに対し、v1.00はLean上で次を持ちます。

```lean
Lattice (ClosedSensorSupport sensors atlas targetDefect root)
BoundedOrder (ClosedSensorSupport sensors atlas targetDefect root)
Fintype (ClosedSensorSupport sensors atlas targetDefect root)
Fintype (RepresentableSensorKernel sensors atlas targetDefect root)
```

閉supportでは、joinは有限unionのclosure、meetはintersection、topは全sensor support、bottomはempty supportのclosureです。

```text
ClosedSensorSupport ≃o OrderDual RepresentableSensorKernel
finite join → ambient kernel infimum
finite meet → kernel envelope of ambient kernel supremum
```

v1.00は`CompleteLattice`、任意・無限supremum/infimum、distributivity、modularity、全ambient subgroupのrepresentability、canonical minimum supportを主張しません。

## OSの責務

| OS | 主な責務 |
|---|---|
| ObserveOS | source-bound observation ownership and sequential observability envelope |
| BeliefOS | local and plural belief-state ownership |
| MemoryOS | lineage、reconstruction、conditioned retrieval、read-only history source |
| WORLD | sourced representation、causal state、governed fragment storage |
| PlanOS | candidate generation、future path ensemble、distribution、plan and replan synthesis |
| DecisionOS | admissibility、evidence intake、relational deliberation、bounded selection |
| ActOS | exactly licensed bounded effect |
| VerifyOS | independent verification handoff、independent evidence verification、outcome receipt |
| LearnOS | future-only learning delta |

```text
ObserveOS evidence != VerifyOS verdict
VerifyOS verdict != truth authority
MemoryOS retrieval != belief sovereignty
MemoryOS lattice order != candidate ranking
PlanOS distribution != selected action
DecisionOS frontier != selected candidate
DecisionOS selection != ActOS invocation
WORLD projection != WORLD mutation
LearnOS delta != present-cycle activation
```

## Formal surfaces

Repository-wide strict baselineと、最新subsystemのversioned aggregateを区別します。

| Surface | Path |
|---|---|
| Repository strict baseline | `formal/KuuOSFormal.lean` |
| ObserveOS v0.7 aggregate | `formal/KuuOSObserveOSV0_7.lean` |
| VerifyOS v0.13 handoff aggregate | `formal/KuuOSVerifyOSV0_13.lean` |
| VerifyOS v0.14 verification aggregate | `formal/KuuOSVerifyOSV0_14.lean` |
| PlanOS v1.23 aggregate | `formal/KuuOSPlanOSV1_23.lean` |
| DecisionOS v0.6 aggregate | `formal/KuuOSDecisionOSV0_6.lean` |
| MemoryOS v1.00 aggregate | `formal/KuuOSMemoryOSV1_00.lean` |

versioned aggregateが存在することと、repository-wide aggregateへ統合済みであることは同一ではありません。Lean変更時は対象aggregateとstrict baselineを別々に検証します。

## Compatibility surfaces

現在の研究前線を検査するcanonical execution surfaceは`runtime/kuuos_current_check.py`です。

現在のpublic surfaceを更新しても、既存のmachine-readable self-organization lineageは破壊しません。

| Compatibility fixed point | Versioned surface |
|---|---|
| KuuOS README Public Status v0.66 | `kuuos_current_root_sequence_v0_66` |
| KuuOS Current Root Execution Connection v0.65 | `kuuos_current_root_sequence_v0_65` |
| KuuOS README Surface Exposure v0.78 | `kuuos_current_root_sequence_v0_78` |

active-state specificationは`docs/kuuos_self_organization_active_state.md`です。

```text
README public status != authority grant
```

次のsurfaceは、既存status lineageとの互換性のため保持されています。

| Surface | Path |
|---|---|
| Stable current surface CLI | `runtime/kuuos_current_surface.py` |
| Versioned current surface entrypoint | `runtime/kuuos_current_surface_entrypoint_v0_77.py` |
| Current surface index | `status/current.surface.index.json` |
| Current surface artifact | `status/current.surface.json` |
| Current resolved status artifact | `status/current.resolved.json` |
| Current manifest | `status/current.manifest.json` |

status compatibility surfaceは報告面であり、canonical runtime rootの代替ではありません。

## Repository map

| Path | 役割 |
|---|---|
| `runtime/` | executable kernels、receipts、validators、canonical current root |
| `scripts/` | fail-closed checkersとcumulative runners |
| `formal/` | Lean theorem packagesとaggregate imports |
| `manifests/` | machine-readable package bindings |
| `status/` | historical and compatibility status artifacts |
| `docs/` | versioned specifications and research notes |
| `tests/` | repository lineage and runtime unit tests |
| `.github/workflows/` | governance and subsystem validation gates |

## 固定境界

```text
candidate != authority
validation != truth
formal compilation != external theorem acceptance

observation != verification
handoff != verification completion
verification request != truth
verification request != causal confirmation
verification outcome != truth
verification outcome != causal attribution
passed != WORLD adoption
failed != WORLD rejection
indeterminate != evidence deletion
memory != belief sovereignty
closure fixed point != empirical truth
lattice structure != ranking or selection
selection != execution
receipt != successor authority

WORLD candidate != empirical fact
WORLD intake != WORLD update
WORLD sidecar != exact WORLD
WORLD projection != persistent WORLD update
Qi conditioning != authority grant
modular time != physical time

modeled repository transition != live Git mutation
current root success != production deployment
README public status != authority grant
```

## 開発原則

変更はdedicated branchとDraft PRで行います。

runtime、checker、manifest、documentation、formal packageを同じ責任境界へ揃え、固定head SHAに対するgovernance gateを通します。

候補、証拠、検証、承認、権限、実行効果を別artifactとして保持します。新しいfrontierは旧frontierを偽装して置換せず、依存関係と非同一性を明示します。

詳細な次段階は[ROADMAP.md](ROADMAP.md)に記載します。
