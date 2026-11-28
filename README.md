# KuuOS / 空OS

**A research architecture for condition-dependent reasoning, mathematical structure, and responsible AI operation.**

KuuOS (空OS) investigates how intelligence can reason, learn, revise its understanding, and act without treating any particular representation, model, proof, or decision as independently authoritative. Its starting point is the fourfold core of emptiness, dependent origination, two truths, and the middle way.

The project develops mathematical foundations in Lean 4, studies concrete relational and higher-dimensional models, and investigates how their structures can inform an architecture of observation, memory, belief, decision, planning, action, reflection, and learning. Python implementations and bounded research experiments test selected connections between these layers.

KuuOS does not seek to eliminate the probabilistic nature of AI generation. It seeks to make the conditions under which generated candidates may be evaluated, combined, revised, adopted, or acted upon explicit. CodeAI and VerifyOS are important implementations of this larger research program, not its definition or its sole objective.

[Research roadmap](ROADMAP.md) · [Fourfold Core](docs/KUOS_FOURFOLD_CORE_v0_1.md) · [Core Charter](docs/KUOS_CORE_CHARTER_v0_1.md) · [Formal sources](formal/) · [License](LICENSE)

## Publication and citation

**Itakura, Hidetoshi.** *KuuOS: Beyond Hallucination Mitigation — Lean-checked foundations for evidence-governed AI, with an ongoing Yang–Mills mass gap case study.* Zenodo preprint, v1.2, 25 November 2026. [Zenodo record](https://zenodo.org/records/24521959) · [Reported DOI: 10.5281/zenodo.24521959](https://doi.org/10.5281/zenodo.24521959).

The preprint provides a research-level entry point to KuuOS and its evidence-governed approach. It is a preprint, not a claim of peer-reviewed validation, universal hallucination elimination, or a solution of the Yang–Mills mass gap problem. For current formal statements and implementation status, consult the versioned sources and verification records below.

*Bibliographic details follow the project’s recorded citation; the live Zenodo metadata and DOI resolution have not been independently rechecked for this revision.*

## 1. The fourfold core

| Principle | Role in KuuOS |
| --- | --- |
| **Emptiness (空, kū)** | No representation, output, identity, proof, memory, or world model possesses independent self-authority. A representation can be useful without being identical to what it represents. |
| **Dependent origination (縁起, engi)** | Claims, observations, models, and actions arise under conditions. Preserve their contexts, source values, relations, dependencies, and transformation histories. |
| **Two truths (二諦)** | Preserve the distinction between ultimate non-fixation and conventional operation. Within conventional operation, distinguish a formal proof, an observed effect, and permission to act. |
| **Middle way (中道)** | Avoid both unsupported acceptance and unsupported rejection. Preserve uncertainty and the possibility of correction while continuing responsible, condition-bound operation. |

These concepts provide the interpretive and design vocabulary of KuuOS. Lean theorems establish properties of explicitly defined mathematical structures; they do not establish Buddhist doctrine or metaphysical truth. Mathematical definitions and proofs, philosophical interpretation, executable implementations, and empirical observations must be read as distinct layers.

## 2. Mathematical foundations: relations, context, and descent

KuuOS studies dependent types, categorical and higher-categorical structures, sheaves, localization, transport, coherence, quotients, invariants, and obstructions. A central question is when locally valid data can legitimately be combined into a global construction, and which distinctions are lost by a chosen observation or quotient.

Selected examples from the formal library:

| Formal source | Mathematical content |
| --- | --- |
| [ScopedGluing](formal/Kuu/LivingEngi/ScopedGluing.lean) | For ordinary functions on a covering family, exact overlap compatibility is equivalent to the existence of a global function. A genuine disagreement obstructs such gluing. |
| [SourceAwareOverlapDescentCriterion](formal/Kuu/LivingEngi/SourceAwareOverlapDescentCriterion.lean) | On a cover, original-source gluing is equivalent to gluing the selected observations together with relative overlap-fiber faithfulness. Agreement of observations alone is insufficient. |
| [FrameTransport](formal/Kuu/LivingEngi/FrameTransport.lean) | Actual equivalences from dependent fibers into a common carrier give transport and coherence in a specified trivializable model, with gauge-invariant readout compatibility. |
| [ConditionedBhava](formal/Kuu/LivingEngi/ConditionedBhava.lean) | A certified conventional readout retains original typed local sections and support; future revisions retain the complete preceding snapshot. |
| [BirthAuthorization](formal/Kuu/LivingEngi/BirthAuthorization.lean) | Candidate generation, governance admission, external authorization, and an effect receipt are distinct typed stages. |
| [HistoryFeedbackRepair](formal/Kuu/LivingEngi/HistoryFeedbackRepair.lean) | A finite history-sensitive kernel distinguishes histories with the same latest observation; a scoped repair changes future behavior while retaining source and history. |

The latter examples form part of the Living Engi Cycle research, connecting mathematical conditions and source-preserving representations with the study of revision, feedback, and operation. They do not establish arbitrary higher-stack descent, general empirical non-Markov dynamics, live neural-weight modification, or external authority.

Three outcomes must remain distinct for a precisely specified proposition: a proof, a proof of its negation, and an unchecked or unresolved state. Failure to find a proof is not a proof of impossibility.

`Preference ⇏ Descent ⇏ Authority`

Preference does not establish gluing or descent; a mathematical construction does not confer practical authorization.

## 3. Concrete mathematical presentations

The general theory is investigated through multiple presentations, including Qi, Yin–Yang and the five phases, mandala-related models, and C60/F112 higher-dimensional constructions. These are research models and testbeds; no single presentation is the exclusive foundation of dependent origination.

The canonical repository includes extensive F112 research on typed boundaries, higher cells, paths, congruence, interchange, coherence, localization, and descent obstructions. Qi research investigates relations between selected five-phase observations, physical gauge structures, and original typed sources. The selected [v5.99 source bridge](formal/KUOS/Architecture/QiWuxingGK5CHP77C60GaugeOriginalSourceBridgeV5_99.lean), [north C60/K5 boundary bridge](formal/Kuu/F112/PolygonNativeC60NorthK5GaugeBoundaryBridge.lean), [triple-gauge bridge](formal/Kuu/F112/PolygonNativeC60NorthWuxingK5TripleGaugeBridge.lean), and [original five-stage F45 construction](formal/Kuu/F112/PolygonNativeC60NorthWuxingK5ActualFiveStageGauge.lean) illustrate this approach. Distinct gauges or source types are not identified merely because a chosen shadow agrees.

Higher dependent origination research continues in [PR #3555](https://github.com/itakura-hidetoshi/KuuOS/pull/3555), which remains draft and unmerged in the recorded snapshot. Individual validation results do not establish all higher coherence or authorize integration of the entire branch.

## 4. Operational architecture: from observation to renewed observation

The operating architecture is a research cycle, not a claim that one complete operating system or universally verified pipeline has been delivered:

```text
Fourfold core
  ↓
Relational mathematics, typed contexts, source and observation
  ↓
Observe → Memory / Plural / Wa → Belief
  ↓
Decision ↔ Verification ↔ Planning
  ↓
Separate authorization → Action → Observation of effects
  ↓
Reflection / Explanation → Learning / Revision → Renewed observation
```

| Research component | Role |
| --- | --- |
| ObserveOS | Preserve the actual observation, its conditions, provenance, uncertainty, and relation to an intended or executed operation. |
| MemoryOS / Plural / Wa | Retain source evidence, distinct compatible or incompatible presentations, context, and revision history. |
| BeliefOS | Form and revise conditional beliefs without substituting a summary for its evidence. |
| DecisionOS | Evaluate alternatives and preferences without treating selection as proof or authorization. |
| PlanOS | Construct conditional plans, preserve blockers, and distinguish plan preparation from execution permission. |
| ActOS | Represent and investigate authorized action within its specified scope. |
| ReflectionOS / ExplanationOS | Reconsider observations, expose reasons, and support explanation and correction without manufacturing evidence. |
| LearnOS / Self-EvolutionOS | Study history-sensitive learning, bounded revision, and improvement while preserving lineage and requiring separate admission. |
| VerifyOS | Check the evidence and conditions of selected claims and publication contracts. |
| CodeAI | Investigate proof retrieval, application, obstruction-aware search, repair, and independent Lean verification. |
| WORLD / RuntimeGovernance | Study world-model interfaces, bounded self-organization, repository evolution, and the distinct conditions for approval and effects. |

The component names above describe roles and research objectives, not uniform implementation or certification levels. The [WORLD library](formal/KUOS/WORLD/), [PlanOS authorization model](formal/KUOS/PlanOS/ExternalCommitAuthorizationGrantV0_45.lean), and [ObserveOS receipt model](formal/KUOS/ObserveOS/WorldHostEffectObservationReceiptV0_4.lean) provide concrete formal interfaces. Their validity conditions must not be mistaken for proof that the corresponding host effects occurred or that an actual external collector was independent. The [bounded self-organization supervisor](formal/KUOS/WORLD/KuuOSBoundedSelfOrganizationSupervisorV0_78.lean) establishes consequences of its stated validity conditions, not unconditional convergence or autonomous self-modification.

## 5. Current implementation and experimental research

> **Recorded research snapshot — 28 November 2026 (JST)**  
> Canonical source: [`main` at `ecfb8b1a1aaa`](https://github.com/itakura-hidetoshi/KuuOS/commit/ecfb8b1a1aaa684bebcc3420f38b8b060a407c7a). The status below retains that observation, rather than asserting a fresh live status. See the [roadmap](ROADMAP.md) for separate acceptance conditions and evidence links.

| Area | Selected recorded progress |
| --- | --- |
| General formal foundations | Living Engi Cycle and higher-dimensional formal sources are present in the public roots; general higher descent remains open. |
| Qi / C60 / F112 | Selected typed bridges and the original F45 five-stage construction are merged; separate public-root and phase–sector proposals remain draft. |
| Lean-to-Python and inter-component architecture | v0.60 formal work, v0.61 adapter and an eight-declaration Lean module are integrated; general refinement is not established. |
| CodeAI | Canonical v0.5 kernel-memory infrastructure covers 13 selected declarations. Separate research-branch R28 and R73 R3 have scoped independent verification; R74 source was observed, but its verification was not established in this snapshot. |
| VerifyOS | v0.17 is integrated, with bounded synthetic tests of signed evidence, pinned Lean projection, and fresh display replay. Production ChatGPT interception or external truth certification is not established. |
| Verification infrastructure | Certified source-bound Lean artifact reuse is integrated; changed or out-of-scope proof source still requires verification. |

CodeAI research asks whether context-bound proof and obstruction memory can improve proof search without discarding viable alternatives. R28's [independent replay](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45902979815) rechecked four positive and two negative exact-target applications and retained two HOLDs. This is a bounded pilot, not an ablation result or evidence of a general performance improvement. R73 R3's [independent run](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/46121677458/attempts/2) concerns an abstract candidate registry and recovery model; it provides no live registration authority. The [VerifyOS v0.17 experiment](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/46105861375) checked selected publication and replay conditions in a trusted-host setting.

The separate [4d-mass-gap](https://github.com/itakura-hidetoshi/4d-mass-gap) repository investigates mathematical structures associated with four-dimensional Yang–Mills theory. It offers a possible future cross-domain evaluation environment. Neither completion of the mass gap problem nor successful generalization of CodeAI to that domain is claimed here.

## 6. Reproducibility and participation

The [strict root](formal/KuuOSStrict.lean) and [public formal root](formal/KuuOSFormal.lean) identify formal library entry points. The pinned environment recorded at the source revision above is:

| Item | Setting |
| --- | --- |
| Lean | `leanprover/lean4:v4.30.0-rc2` ([toolchain](lean-toolchain)) |
| mathlib | `5450b53e5ddc75d46418fabb605edbf36bd0beb6` ([manifest](lake-manifest.json)) |
| Proof policy | No new axioms or `sorry`; audit specified declarations for standard Lean axioms only. Preserve assumptions, original definitions, and source lineage. |

```bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
```

Read exact definitions, theorem statements, imports, source revisions, and verification logs before relying on a result. Distinguish mathematical checking, runtime observation, independent CI, and authorized release. Documentation cannot confer proof or action authority. See [CONTRIBUTING.md](CONTRIBUTING.md), [AGENTS.md](AGENTS.md), and the [roadmap](ROADMAP.md).

Collaboration is welcome in the foundations, higher mathematics, concrete relational models, operational architecture, verification, and AI-assisted formal research. Useful contributions include precise questions about definitions and hypotheses, independent reconstructions, counterexamples, reproducibility studies, and proposals that explicitly retain unresolved conditions.

**Research and design: Hidetoshi Itakura (板倉英俊).** Copyright and licensing follow the relevant notices and [LICENSE](LICENSE) (Apache License 2.0).

Historical documentation: [previous canonical README](https://github.com/itakura-hidetoshi/KuuOS/blob/ecfb8b1a1aaa684bebcc3420f38b8b060a407c7a/README.md), [previous canonical roadmap](https://github.com/itakura-hidetoshi/KuuOS/blob/ecfb8b1a1aaa684bebcc3420f38b8b060a407c7a/ROADMAP.md), [22 November README](docs/history/README-SNAPSHOT-20261122.md), [22 November roadmap](docs/history/ROADMAP-SNAPSHOT-20261122.md), [earlier README](docs/history/README-THROUGH-20261121.md), [earlier roadmap](docs/history/ROADMAP-THROUGH-20261121.md). Historical records retain their original scope and evidence.
