# KuuOS / 空OS — Research Roadmap

This roadmap describes the research program from its fourfold foundations through its mathematical models, operational architecture, and selected implementations. It is organized by structural role, not by which branch happens to have the most recent activity. The tracks are complementary and may progress in parallel; ordering them here does not authorize a change in research priorities or suspend any ongoing work.

[README](README.md) · [Fourfold Core](docs/KUOS_FOURFOLD_CORE_v0_1.md) · [Core Charter](docs/KUOS_CORE_CHARTER_v0_1.md)

## 0. Recorded baseline and evidence discipline

- Recorded canonical snapshot (28 November 2026 JST): [`main` at `ecfb8b1a1aaa684bebcc3420f38b8b060a407c7a`](https://github.com/itakura-hidetoshi/KuuOS/commit/ecfb8b1a1aaa684bebcc3420f38b8b060a407c7a). This revision of the roadmap retains that observation; it is not a live status report.
- Pinned Lean `v4.30.0-rc2`, mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`.
- [Protected PR #1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558), Lean 4.31 validation, was observed draft/open and must remain protected.

| Evidence state | Meaning |
| --- | --- |
| Canonical / merged | The source is adopted into `main` at an identified revision, not a guarantee about all runtime behavior. |
| Locally verified | The specified direct Lean or runtime checks succeeded; independent verification is a separate result. |
| Independently checked (scoped) | The observed independent run checked the specified source, environment, statements and declared inventory. |
| Refuted in scope | The relevant negation is proved for the exact proposition and conditions; other routes are not thereby excluded. |
| HOLD / NO_DATA | Required evidence is missing, context has changed, or a check did not establish the claim. This is not a mathematical refutation. |

Philosophical interpretation, formal mathematical statements, empirical observations, software behavior, and authorization are distinct. `Preference ⇏ Descent ⇏ Authority`. Retain original conditions and source values. A successful check cannot authorize a different proposition or world effect.

## A. Fourfold foundations and Living Engi Cycle

**Objective:** give precise mathematical content to selected operational distinctions associated with emptiness, dependent origination, two truths, and the middle way, without claiming a formal proof of the philosophical concepts themselves.

Representative formal structures in the recorded public roots:

| Source | Existing formal direction | Further research |
| --- | --- | --- |
| [ScopedGluing](formal/Kuu/LivingEngi/ScopedGluing.lean) | Exact function-sheaf gluing, quotient factorization, scoped positive/negative/unchecked evidence. | Extend to additional explicitly specified families; preserve counterexamples to invalid descent. |
| [SourceAwareOverlapDescentCriterion](formal/Kuu/LivingEngi/SourceAwareOverlapDescentCriterion.lean) | Source gluing iff observed gluing plus overlap-fiber faithfulness on a cover. | Characterize which original values and histories are lost under specific observers. |
| [FrameTransport](formal/Kuu/LivingEngi/FrameTransport.lean) | Dependent fibers and supplied common frames give transport coherence and gauge-invariant readouts. | Separate trivializable cases from genuine higher or non-flat compatibility obligations. |
| [ConditionedBhava](formal/Kuu/LivingEngi/ConditionedBhava.lean) | Certified source-retaining snapshots and future-only revision. | Strengthen conditions for transferring evidence between changing contexts. |
| [BirthAuthorization](formal/Kuu/LivingEngi/BirthAuthorization.lean) | Candidate birth, policy and external authorization, and effect evidence are distinct. | Study admission and authorization composition without manufacturing witnesses. |
| [HistoryFeedbackRepair](formal/Kuu/LivingEngi/HistoryFeedbackRepair.lean) | A finite history-sensitive counterexample and a source-preserving repair. | Investigate qualified feedback and revision in larger explicit models; no universal stability claim. |

Acceptance: retain exact source, support, context, and history; identify necessary and sufficient conditions where possible; preserve obstructions; separate a changed observation from a changed underlying value. The mathematical results concern specified constructions, not all sheaves, stacks, dynamics, or external worlds. The native F55 witnesses in the abstract two-chart Living Engi example do not constitute a geometric C60 cover.

## B. General dependent origination and higher mathematical structure

**Objective:** develop relations between typed presentations, original values, genuine endpoints, transport, localization, and higher-dimensional coherence. Study when a local construction extends globally and when such extension is obstructed.

The [strict formal root](formal/KuuOSStrict.lean) and [public formal root](formal/KuuOSFormal.lean) provide entry points to presentation, incidence, paths, nerve, localization, kernel equivalence, overlap, higher cells, and related formal work. Source-level existence of a module, inclusion in a public root, and CI certification of a proposed extension are different facts.

Higher dependent origination [PR #3555](https://github.com/itakura-hidetoshi/KuuOS/pull/3555) was observed draft/open at `a637438ceebdcb5b0247f30f14479b85b3bd0e1f`. Historical [v1.35](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45343467773) and [v1.70](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45343469142) checks succeeded within their own scope; the [v1.73 probe](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45343467763) failed. The earlier [#3548](https://github.com/itakura-hidetoshi/KuuOS/pull/3548) result is validation-only. No whole-PR admission follows from these observations.

Research directions include typed Duskin transport, whiskering, coherence, endpoint conditions, and the Type-(A), Type-(B), and Type-(C) scaling and right lifting property families. Recover original dependent types rather than replacing them with convenient surrogates. Establish precise domain and codomain conditions, preserve alternative presentations, and characterize obstruction rather than assuming global descent.

Acceptance: inspect complete changed Lean sources, imports, dependent signatures and pinned mathlib APIs; retain all assumptions and exact endpoints; verify repair without weakening, new axioms, or `sorry`; require independent checking, public-root admission where appropriate, and Governance before adoption.

## C. Concrete presentations: Qi, Yin–Yang, five phases, mandala, C60 and F112

**Objective:** investigate concrete finite, geometric, relational, and higher-dimensional presentations as mathematically defined models. They are not interchangeable, and general dependent origination is not reducible to any one of them.

Selected integrated work in the recorded snapshot:

| Research result | Source and recorded admission |
| --- | --- |
| Qi v5.99: selected five-phase observation, physical gauge structure and original typed source bridge | [Lean module](formal/KUOS/Architecture/QiWuxingGK5CHP77C60GaugeOriginalSourceBridgeV5_99.lean), [PR #3631](https://github.com/itakura-hidetoshi/KuuOS/pull/3631). |
| North C60 physical gauge and K5 boundary | [Lean module](formal/Kuu/F112/PolygonNativeC60NorthK5GaugeBoundaryBridge.lean), [PR #3632](https://github.com/itakura-hidetoshi/KuuOS/pull/3632). |
| Conditional bridge between selected five-phase, physical and K5 gauges | [Lean module](formal/Kuu/F112/PolygonNativeC60NorthWuxingK5TripleGaugeBridge.lean), [PR #3633](https://github.com/itakura-hidetoshi/KuuOS/pull/3633). |
| Original F45 five-stage construction | [Lean module](formal/Kuu/F112/PolygonNativeC60NorthWuxingK5ActualFiveStageGauge.lean), [PR #3636](https://github.com/itakura-hidetoshi/KuuOS/pull/3636). |

[Public-root PR #3635](https://github.com/itakura-hidetoshi/KuuOS/pull/3635) and [phase–sector equivalence PR #3637](https://github.com/itakura-hidetoshi/KuuOS/pull/3637) remain draft/open in the snapshot. The historical [six-declaration phase–sector check](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45251598224) does not certify a later test-merge tree. [#3634](https://github.com/itakura-hidetoshi/KuuOS/pull/3634) is validation-only. The wider F112 library includes higher-cell coherence and explicit non-descent research; do not promote a selected cell or local proof into universal coherence.

Next research: compare precisely typed presentation maps, kernels, invariants, and genuine source-fiber information; investigate where observation loses original data; extend higher coherence under the actual hypotheses. Yin–Yang, five-phase and mandala-related research should be documented by exact model and evidence rather than by names or broad equivalence claims. This roadmap has not freshly audited every model family.

## D. WORLD and inter-component operational architecture

**Objective:** connect observation, memory, beliefs, alternatives, verification, plans, action, effects, reflection and learning as condition-dependent operations with distinct responsibilities. The architecture must make correction possible without erasing prior observations or granting authority by inference alone.

| Interface | Research and acceptance goal |
| --- | --- |
| ObserveOS → MemoryOS / Plural / Wa | Preserve source evidence, observation context, uncertainty, provenance, and distinct presentations. Verify exact transfer rather than only summary equality. |
| MemoryOS → BeliefOS → DecisionOS | Support context-bound belief revisions and comparison of alternatives. Retain rejected or unresolved candidates and the reason for preference. |
| DecisionOS / VerifyOS → PlanOS | Bind typed goals, conditions, prerequisites and blockers to actual runtime operations. A chosen plan is not an approved action. |
| PlanOS → ActOS → ObserveOS | Distinguish authorization, execution, reported effect, independently collected observation, verification and world update. |
| ReflectionOS / ExplanationOS | Investigate source-grounded explanation, disagreement, re-observation, and correction. Distinguish interpretation from independently observed evidence. |
| LearnOS / Self-EvolutionOS / WORLD | Preserve prior states and histories while constructing bounded revision proposals, stopping and recovery conditions, and separately authorized adoption. |

Concrete entry points are the [PlanOS external commit grant model](formal/KUOS/PlanOS/ExternalCommitAuthorizationGrantV0_45.lean), [ObserveOS effect observation receipt](formal/KUOS/ObserveOS/WorldHostEffectObservationReceiptV0_4.lean), and [WORLD bounded supervisor](formal/KUOS/WORLD/KuuOSBoundedSelfOrganizationSupervisorV0_78.lean). In the recorded formal root, WORLD research also includes gauge connections, memory selection and rollback, repository alignment and revision DAGs, checkpoint transitions and recovery, and lifecycle review. These are research structures; their validity fields, authorization propositions and receipt types are not self-authenticating external evidence.

Integrated Lean-to-Python work includes [v0.60 #3622](https://github.com/itakura-hidetoshi/KuuOS/pull/3622), [v0.61 adapter #3626](https://github.com/itakura-hidetoshi/KuuOS/pull/3626), and [eight-declaration Lean module #3628](https://github.com/itakura-hidetoshi/KuuOS/pull/3628). [Public-root #3629](https://github.com/itakura-hidetoshi/KuuOS/pull/3629) remains draft/open; its historical [failed CI](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44980424064) and [successful public-root check](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44980424086) are distinct.

Next research: build and test exact component-to-component contracts, distinguish runtime implementations from Type-level models, strengthen local refinement results, and study bounded revision and re-observation. Full bidirectional Python–Lean refinement, a correspondence between formal WORLD and the external world, organizational independence, and general autonomous action remain unestablished.

## E. Specialized implementations: CodeAI and VerifyOS

These tracks operationalize selected principles in tractable research settings. They are neither the root of KuuOS nor substitutes for its other mathematical and architectural research.

### E1. CodeAI — contextual proof reuse and obstruction-aware search

Canonical infrastructure includes candidate verification [#3623](https://github.com/itakura-hidetoshi/KuuOS/pull/3623), [#3625](https://github.com/itakura-hidetoshi/KuuOS/pull/3625), [#3626](https://github.com/itakura-hidetoshi/KuuOS/pull/3626), and [#3630](https://github.com/itakura-hidetoshi/KuuOS/pull/3630); prior-proof review and lexical indexing [#3638](https://github.com/itakura-hidetoshi/KuuOS/pull/3638)–[#3639](https://github.com/itakura-hidetoshi/KuuOS/pull/3639); and version-bound kernel memory [#3640](https://github.com/itakura-hidetoshi/KuuOS/pull/3640)–[#3641](https://github.com/itakura-hidetoshi/KuuOS/pull/3641). The latter covers 13 selected declarations. Its deterministic HOLD callback replay is not an evaluation of an external generative model. Earlier multi-verifier admission HOLDs are not waived.

Selected evidence from the separate [research branch](https://github.com/itakura-hidetoshi/KuuOS/tree/research/codeai-nogo-memory-v1-20261126):

| Milestone | Recorded scoped result |
| --- | --- |
| [R7](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45774874136) | 47,705 type-structure entries, 2,120/2,815 modules observed, 695 unobserved, 2,390 complete types, and 5,558 negative-structure candidates. Candidate counts are not counts of certified refutations. |
| R17–R27 | Recursive premise search, AND–OR composition, proof DAGs, compiled capsules, typed applications and scoped negative recall; [R20](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45811079734), [R25](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45896476614), [R26](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45898216584), [R27](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45901313851). |
| [R28 source](https://github.com/itakura-hidetoshi/KuuOS/commit/c05a986ecd571a1b00da255a7552ee8a54b4a709), [CI](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45902979815) | Seven memory records, eight targets, four positive and two negative exact-target applications, two HOLDs, 11 audited declarations and byte-identical memory transport. |
| [R73 R3 source](https://github.com/itakura-hidetoshi/KuuOS/commit/b5c2535327eecb5158368bfb85ad13b34953dba9), [CI attempt 2](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/46121677458/attempts/2) | Ten general and six concrete new theorems, 313 cumulative audited declarations (16 fresh and 297 reused MCP audits), two retained paths. Abstract registry extension, recovery and rejection; no live registration or policy change. |
| [R74 source](https://github.com/itakura-hidetoshi/KuuOS/blob/880d06b1b3836c13c548fdc063c0d020e2df6206/scripts/lean_probes/codeai_registry_batch_readiness_v1.lean) | Candidate readiness, frame and permutation laws for a checked registry batch. Independent verification not established in this snapshot. Registry equality does not erase ordered histories. |

A proposed controlled benchmark compares proof search with and without stored obstruction certificates, holding positive proof memory, retrieval/search budget, model configuration and pinned Lean environment fixed. Use multiple held-out instances of valid reuse, a certified blocked route with a viable alternative, and insufficient evidence. Measure repeated failed attempts, false route exclusions, Lean-checked completion, HOLD rates and verification costs. Revalidate all obstructions in context. Timeouts, missing premises and failed retrieval are not formal No-Go certificates. Existing pilots do not establish performance improvement or cross-domain generalization.

Next gates: complete scoped R74 verification, improve dependency and type coverage, preserve alternatives and prior evidence, and separately establish current-main admission before integrating experimental machinery. No automatic registration, general prover completeness, or execution authority is claimed.

### E2. VerifyOS — question-bound evidence and publication

The recorded integrated [v0.17 implementation](runtime/kuuos_verifyos_lean_egress_v0_17.py) extends bounded interpretation and correction histories, signed receipt checks, separate-key witnesses, diverse audit, typed claim projection, and trusted-host egress. It recomputes evidence checks and compiles four pinned Lean modules to compare all 18 projected claim values with Python; fresh display replay compares exact publication bytes while preserving original status, branches and HOLDs.

[Dedicated CI #46105861375](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/46105861375) completed both sandbox and independent jobs successfully; independent regression 10/10. [Governance #46105861382](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/46105861382) succeeded with the Strict Lean job skipped. No new full-library build is inferred from that run.

Next gates: extend explicitly typed interpretation and claim domains, retain ambiguous branches and exclusions, strengthen source/host trust and replay conditions, distinguish structural agreement from independent execution provenance, and investigate scoped runtime-to-formal refinement. Production integration requires a separately authorized and verified execution path. No arbitrary natural-language completeness, global freshness, external truth, production ChatGPT interception, or action authority follows. Use synthetic public CI fixtures, not private evidence or keys. See [v0.17 scope](docs/KUUOS_VERIFYOS_LEAN_EGRESS_v0_17.md).

## F. Verification infrastructure and governance

Certified cross-PR Lean artifact reuse is integrated in [#3643](https://github.com/itakura-hidetoshi/KuuOS/pull/3643) and [#3644](https://github.com/itakura-hidetoshi/KuuOS/pull/3644). The [producer and verifier](scripts/ci_verified_lean_project_cache_v1.py) validate source provenance, proof scope, dependencies, manifest, and artifact digests. The historical [producer](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45615980980) completed 10,433 strict build jobs; [independent restoration](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45700676928) completed the same strict build command in 4.74 seconds. These are recorded measurements, not universal performance guarantees.

The verification process must support all research tracks, not only CodeAI:

1. Fix the exact source, conditions, dependencies, protected branches and prior evidence; search existing positive and negative results before new work.
2. Generate or repair only the unresolved part. Keep original statements, assumptions, source values, and failure histories.
3. For new formal candidates, check the fixed environment with direct Lean, actual Lean MCP and axiom audits in the isolated sandbox. Separate-runner CI follows sandbox success.
4. Check independent workflow/job/step completion, real logs, source/test-merge tree agreement, applicable public roots and Governance. Keep evidence admission and merge or action authorization distinct.
5. Re-observe and preserve append-only history. Missing or mismatched cache evidence returns to normal verification. Do not rerun unchanged certified work unnecessarily or weaken checks to avoid a failure.

Docs-only revisions need not trigger new Strict Lean proof certification. However, even documentation changes to `main` may invalidate exact-HEAD research workflows. Before adoption, coordinate with running fixed-HEAD work and check source ancestry, proof scope, dependencies and new-HEAD admission. Historical receipts retain their historical scope.

## G. Cross-domain validation, evaluation, and collaboration

### Publication and research dissemination

**Itakura, Hidetoshi.** *KuuOS: Beyond Hallucination Mitigation — Lean-checked foundations for evidence-governed AI, with an ongoing Yang–Mills mass gap case study.* Zenodo preprint, v1.2, 25 November 2026. [Zenodo record](https://zenodo.org/records/24521959) · [Reported DOI: 10.5281/zenodo.24521959](https://doi.org/10.5281/zenodo.24521959).

Preserve this publication as a versioned research record. Future revisions should explicitly distinguish new formal results, runtime observations, scoped independent verification, unresolved conditions, and proposed evaluations. Do not retrospectively attribute later repository results to the preprint or treat its release as independent certification.

*Bibliographic details follow the project’s recorded citation; the live Zenodo metadata and DOI resolution have not been independently rechecked for this revision.*

### Cross-domain evaluation and collaboration

The separate [4d-mass-gap](https://github.com/itakura-hidetoshi/4d-mass-gap) project may serve as a future cross-domain evaluation setting for selected KuuOS methods. It has its own mathematical objectives and source of truth. Define the scope, held-out tasks, evidence and comparative criteria before claiming any transfer of performance. A checked finite-lattice result does not resolve the continuum Yang–Mills mass gap problem.

Across the tracks, collaboration can focus on independent mathematical reconstruction, counterexamples and obstructions, comparison of distinct presentations, precise runtime/formal contracts, observation and feedback, and reproducible experiments. Progress in one track must not replace the outstanding conditions in another.

The long-term aim is a coherent research architecture grounded in conditional relations, preserving original evidence and plurality, enabling responsible conventional operation and correction without reification. No claim is made that all components are complete, that philosophical doctrine is formally proved, that arbitrary mathematics can be proved automatically, that hallucinations are eliminated, or that autonomous external action is unrestricted.

---

Research and design: **Hidetoshi Itakura (板倉英俊)**. See [LICENSE](LICENSE) and the relevant attribution notices.

Historical evidence and exact earlier receipt references remain available in the [previous canonical roadmap](https://github.com/itakura-hidetoshi/KuuOS/blob/ecfb8b1a1aaa684bebcc3420f38b8b060a407c7a/ROADMAP.md), [previous canonical README](https://github.com/itakura-hidetoshi/KuuOS/blob/ecfb8b1a1aaa684bebcc3420f38b8b060a407c7a/README.md), [22 November roadmap](docs/history/ROADMAP-SNAPSHOT-20261122.md), [22 November README](docs/history/README-SNAPSHOT-20261122.md), [earlier roadmap](docs/history/ROADMAP-THROUGH-20261121.md), and [earlier README](docs/history/README-THROUGH-20261121.md).
