# KuuOS / 空OS

![KuuOS PR Governance Gate](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/pr-governance-gate.yml/badge.svg)
![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS** is a public research architecture for dependent origination (縁起), contextual transport, higher coherence, descent, obstruction, correction, recursive carriers, exact presentation, and bounded AI operation. Founder: **Hidetoshi Itakura / 板倉英俊**.

> Which structure survives justified changes of context and presentation, how can compatible local information be transported and glued, and which universal property characterizes the invariant content?

## Current formal status

**The integrated theorem spine is now through v5.10.**

The most important change is that the exact-universal ambient route that was still open at v5.03 is now closed.

For every refinement atlas A in the exact-universal sector, the formal development now provides:

- hom-category equivalences on the chosen exact-universal source objects;
- a strict realization into the ambient completion;
- canonical extension of raw StrongTrans data through the constructed localization;
- quotient-independent coherent StrongTrans naturality;
- restriction-hom essential surjectivity;
- ambient object coverage;
- ambient Whitehead existence;
- an explicit canonical WhiteheadBiequivalenceData object whose forward pseudofunctor is the exact-universal realization.

The closed chain is:

~~~text
retained localization generators
        |
        |  v5.04-v5.05
        v
canonical generator compatibility
        |
        |  v5.06
        v
generated localization invariance
        |
        |  v5.07
        v
quotient-independent canonical naturality
        |
        |  v5.08
        v
HigherLocalizedStrongTransOneCellCoherenceExtension
        |
        v
HigherLocalizedStrongTransCoherenceExtension
        |
        |  v4.95
        v
restriction Hom EssSurj
        |
        |  v4.93-v4.94
        v
restriction Hom equivalence
        |
        |  v4.92
        v
canonical restriction universality
        |
        |  v4.91
        v
ambient object coverage
        |
        |  v4.90
        v
ambient Whitehead existence
        |
        |  v5.10
        v
canonical ambient WhiteheadBiequivalenceData
~~~

This closes the current sufficient ambient P4 route **inside the exact-universal sector**.

It does **not** prove that every weakly W-admissible raw contextual system admits an exact presentation. Earlier obstruction theorems remain active and explicitly rule out that converse in general.

## Canonical theorem snapshot — 2026-10-04 JST

| Role | Reference |
| --- | --- |
| Repository / canonical branch | itakura-hidetoshi/KuuOS / **main** |
| Fresh theorem-bearing main | **580e49111b566bf0f74f53c3ca68be03fdf7126b** |
| Latest theorem merge | [#1961 — Package canonical ambient Whitehead data v5.10](https://github.com/itakura-hidetoshi/KuuOS/pull/1961) |
| Exact validated PR head | **7ca818ff13d01b12a16c9fced18f9898d3f58642** |
| Exact-head validation | [Run #3587 / 37192661698](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/37192661698): completed / success |
| Exact-head receipts | Strict Lean: success; exact-head terminal: success |
| Build result | Build completed successfully (8634 jobs) |
| Lean | leanprover/lean4:v4.30.0-rc2 |
| Mathlib | 5450b53e5ddc75d46418fabb605edbf36bd0beb6 |

The public axiom reports for the v5.10 endpoint contain only:

~~~text
propext
Classical.choice
Quot.sound
~~~

There is no sorryAx.

The latest theorem-bearing module is:

[DependentOriginationExactUniversalAmbientWhiteheadDataV5_10.lean](formal/KUOS/DependentOriginationExactUniversalAmbientWhiteheadDataV5_10.lean)

A later README/ROADMAP-only merge may advance main. Such a docs-only merge does not create a newer theorem-bearing baseline.

Authority order remains fixed:

~~~text
fresh exact canonical GitHub SHA
  > formal Lean theorem artifacts at that SHA
  > README / ROADMAP
  > exact-head CI/runtime receipts
  > history / conversation memory
~~~

[#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) remains a separate Lean 4.31 validation-only lane. It is currently **open / draft / unmerged** and is outside canonical theorem authority.

## What 空 means here

空 is not “nothing exists.” Its operational role is non-reification:

- a chosen presentation is not intrinsic substance;
- a local observation is not global truth;
- equivalent carriers do not erase provenance or world binding;
- a runtime success is not theorem authority;
- a quotient representative is computational scaffolding, not mathematical content.

KuuOS therefore separates observation from inference, identifies the active context, retains compatible presentations, tracks relations and history, checks local compatibility and descent, exposes obstructions, respects authority boundaries, performs only justified actions, and re-observes afterward.

The formal program is richer than a graph. It contains contextual systems, mappings between systems, transformations between mappings, bicategorical coherence, quotient/descent structure, obstructions, universal properties, and explicit presentation-localization interfaces.

## Three formal layers

### 1. Exact-universal source

ExactUniversalRawObject is the chosen source sector. A source object stores a raw Cat-valued contextual system together with exact presentation and coherent universal-target data.

The source has typed 1-cells and 2-cells and a native bicategory.

### 2. Object-labelled realized sector

The realized sector keeps the source-object labels while using the corresponding DO₂ carriers and morphisms.

The v4.89 Whitehead-style certificate is label preserving. Equivalent realized carriers do not erase distinct source presentations, histories, or world bindings.

### 3. Ambient completion

The ambient completion contains arbitrary objects of the constructed completion, not only those that were initially source-labelled.

The distinction remains conceptually important, but the exact-universal object-coverage problem is no longer open: v5.09 proves that every ambient completion object is equivalent to the carrier of an exact-universal source object, and v5.10 packages the resulting ambient Whitehead data canonically.

This claim is about the constructed exact-universal ambient completion. It is not a claim that every arbitrary weakly admissible external system has an exact presentation.

## Integrated mathematical spine

| Versions | Closed result | Main anchors |
| --- | --- | --- |
| v4.00-v4.12 | Exact C2 nonfactorization and nonzero Stage-II obstruction in ZMod 2 | [v4.00](formal/KUOS/DependentOriginationAbstractNonfactorizationV4_00.lean), [v4.12](formal/KUOS/DependentOriginationStageIIObstructionClassV4_12.lean) |
| v4.13-v4.48 | Incidence/capacity obstructions, recursive and inverse-limit carriers, exact Cantor dimension, switch/orientation descent | [v4.40](formal/KUOS/DependentOriginationStageIIExactFractalCertificateV4_40.lean), [v4.48](formal/KUOS/DependentOriginationStageIIOrbitOrientationDescentV4_48.lean) |
| v4.49-v4.70 | Abstract presentation descent, exact presentation sector, native source bicategory, strict realization | [v4.49](formal/KUOS/DependentOriginationAbstractPresentationDescentV4_49.lean), [v4.69](formal/KUOS/DependentOriginationExactUniversalMappingBicategoryV4_69.lean), [v4.70](formal/KUOS/DependentOriginationExactUniversalRealizationStrictPseudofunctorV4_70.lean) |
| v4.71-v4.83 | Liftability, compatible 2-cell full faithfulness, arbitrary DO₂ 1-cell lifting between chosen carriers, hom-category equivalences | [v4.77](formal/KUOS/DependentOriginationExactUniversalRealizationFullyFaithfulV4_77.lean), [v4.83](formal/KUOS/DependentOriginationExactUniversalHomEquivalenceV4_83.lean) |
| v4.84-v4.89 | Section pseudofunctor, labelled realization, global unit/counit StrongTrans, labelled Whitehead certificate | [v4.84](formal/KUOS/DependentOriginationExactUniversalSectionPseudofunctorV4_84.lean), [v4.89](formal/KUOS/DependentOriginationExactUniversalLabelledBiequivalenceV4_89.lean) |
| v4.90-v4.95 | Ambient Whitehead reduced to object coverage/restriction universality; restriction Faithful and Full; EssSurj reduced to StrongTrans extension | [v4.90](formal/KUOS/DependentOriginationExactUniversalAmbientCoverageReductionV4_90.lean), [v4.94](formal/KUOS/DependentOriginationExactUniversalAmbientRestrictionFullV4_94.lean), [v4.95](formal/KUOS/DependentOriginationExactUniversalAmbientStrongTransExtensionV4_95.lean) |
| v4.96-v5.03 | Locally-discrete reduction, presentation/W-inverse/composition naturality, all-arrow existence, canonical identity, presentation coherence, transport bridge | [v4.96](formal/KUOS/DependentOriginationExactUniversalAmbientStrongTransLocallyDiscreteV4_96.lean), [v5.03](formal/KUOS/DependentOriginationExactUniversalAmbientStrongTransPresentationTransportV5_03.lean) |
| v5.04-v5.05 | Canonical compatibility for id/comp and Winv₁/Winv₂ localization generators | [v5.04](formal/KUOS/DependentOriginationExactUniversalAmbientStrongTransTransportCompatibilityV5_04.lean), [v5.05](formal/KUOS/DependentOriginationExactUniversalAmbientStrongTransWRelationCompatibilityV5_05.lean) |
| v5.06 | Canonical path evaluator and invariance through retained generated localization relations | [generated evaluator](formal/KUOS/DependentOriginationExactUniversalAmbientStrongTransGeneratedRelationV5_06.lean), [full generated localization](formal/KUOS/DependentOriginationExactUniversalAmbientStrongTransGeneratedLocalizationV5_06.lean) |
| v5.07 | Quotient-independent canonical StrongTrans naturality on actual localization arrows | [v5.07](formal/KUOS/DependentOriginationExactUniversalAmbientStrongTransQuotientNaturalityV5_07.lean) |
| v5.08 | Identity/composition/restriction coherence assembled into the v4.96 and v4.95 StrongTrans extension packages | [v5.08](formal/KUOS/DependentOriginationExactUniversalAmbientStrongTransCoherentExtensionV5_08.lean) |
| v5.09 | Ambient StrongTrans extension, restriction EssSurj, object coverage, and ambient Whitehead existence become unconditional in the exact-universal sector | [v5.09](formal/KUOS/DependentOriginationExactUniversalAmbientP4ClosureV5_09.lean) |
| v5.10 | Canonical ambient WhiteheadBiequivalenceData with forward equal to the exact-universal realization | [v5.10](formal/KUOS/DependentOriginationExactUniversalAmbientWhiteheadDataV5_10.lean) |

## v5.04-v5.10: how the former ambient frontier closed

### v5.04 — id / comp transport compatibility

The canonical presentation choices are identified with the transported canonical localized identity and composition choices.

This closes the data-level ambiguity for the relations.id and relations.comp generators.

### v5.05 — Winv₁ / Winv₂ compatibility

The inverse naturality specification is combined with localized isomorphism unit/counit equations.

The two W-inverse localization generators are now compatible with the same canonical naturality evaluator.

### v5.06 — retained generated-relation invariance

The existing Type-valued localization syntax from v2.68 is reused rather than replaced:

~~~text
LocalizationGenerating2Cell
GeneratedCompClosure2Cell
GeneratedLocalization2Cell
~~~

A canonical naturality evaluator is defined on free localization paths. Invariance is proved first on the four generators, then through whiskering/composition closure, and finally through refl/symm/trans to all GeneratedLocalization2Cell derivations.

No arbitrary relation language is introduced.

### v5.07 — quotient-independent canonical naturality

Naturality descends from retained free-path representatives to actual morphisms of Mathlib's constructed localization.

The central data-level endpoint is higherLocalizedCanonicalStrongTransNaturality.

Quot.out is used only to select a computational representative; representative independence is theorem-level.

### v5.08 — coherent StrongTrans extension

The quotient-independent family is reindexed onto the locally-discrete source and proved to satisfy:

- identity coherence;
- composition coherence;
- the exact raw restriction square;
- automatic source 2-cell naturality via v4.96.

The development then constructs:

~~~text
higherLocalizedCanonicalStrongTransOneCellCoherenceExtension
higherLocalizedCanonicalStrongTransCoherenceExtension
higherLocalizedCanonicalStrongTransExtensionExists
~~~

Thus the v4.95 extension condition is no longer conditional.

### v5.09 — ambient P4 route closure

For every refinement atlas A:

~~~text
exactUniversalAmbientRestrictionStrongTransExtension_canonical
exactUniversalAmbientRestrictionHomEssSurj_canonical
exactUniversalAmbientObjectCoverage_canonical
exactUniversalAmbientWhiteheadExistence_canonical
~~~

are now theorem-level consequences.

The exact-universal ambient object-coverage problem that was open at v4.90-v5.08 is therefore closed.

### v5.10 — canonical ambient Whitehead data

v5.10 exposes an actual theorem-bearing data object:

~~~text
exactUniversalAmbientCanonicalWhiteheadBiequivalenceData
~~~

Its forward pseudofunctor is definitionally the exact-universal realization, its local hom equivalences are the validated exact-universal hom equivalences, and its object essential-surjectivity comes from v5.09 ambient coverage.

The endpoint is no longer merely existential.

## Boundaries that remain explicit

### Weak W-admissibility does not imply exact presentation

The obstruction chain remains valid:

~~~text
weak W-admissibility can hold
while exact localization / exact presentation is impossible.
~~~

The positive v4.49-v5.10 chain is an exact-universal-sector theorem. It does not erase the countermodels.

### WhiteheadBiequivalenceData is the formalized endpoint currently claimed

v5.10 provides the repository's Whitehead-style biequivalence data. This should not be silently upgraded to a stronger tricategorical adjoint-biequivalence package with independently specified quasi-inverse and triangle data unless such a package is separately formalized.

### The final mapping/classification theorem is still open

A schematic long-range goal is:

~~~text
eta : C -> DO(C,W,J,H)

AdmissibleContextualSystems(C,X)
  ≃
Fun(DO(C,W,J,H),X)
~~~

This is not yet a final theorem statement. A correct formulation must retain the distinction between semantic admissibility and exact liftability and must specify higher morphisms, variance, world/presentation labels, factor existence, and coherent uniqueness.

## Current research frontier

The former StrongTrans/ambient-P4 frontier is closed. The next work should focus on the conceptual gap above the exact-universal construction rather than reopening the solved localization coherence problem.

Priority questions include:

1. **Mapping/classification formulation.** State the correct higher universal property that the exact-universal construction should satisfy.
2. **Semantic admissibility versus exact liftability.** Characterize precisely which admissible systems lie in the exact-universal image and how the obstruction classes control failure.
3. **Stronger biequivalence packaging.** If needed, refine WhiteheadBiequivalenceData into a stronger explicit inverse/adjunction package without discarding presentation labels.
4. **Prescribed data versus canonical extension.** Clarify which externally prescribed components or choices can be respected, as opposed to the canonical choices constructed by v5.04-v5.10.
5. **World/presentation-sensitive semantics.** Preserve the distinction between paramārtha-level equivalence and conventional/world-specific action data in any final classification theorem.

These are proposed research directions, not current theorem claims.

## Proof-engineering lessons retained

- Authority is the exact theorem-bearing Git SHA, not conversation history.
- Importing a module does not automatically open its namespaces.
- open scoped exposes scoped notation; it is not the same as open for ordinary declarations.
- With autoImplicit false, namespace mistakes become immediate unknown-identifier errors rather than accidental implicit variables.
- change is definitional only.
- rfl should be used only after confirming definitional equality of the exact projections involved.
- In dependent equalities, explicit Eq.trans / congrArg / congrArg₂ proof terms are often more stable than broad rw.
- Category Hom aliases may resist ordinary cases/induction; use the path-specific induction API when appropriate.
- For double opposites, composition order reverses twice and returns to the original order.
- Keep quotient representatives as computational scaffolding; prove representative independence separately.
- Do not infer theorem authority from docs, runtime output, cache success, or a different Lean lane.

## Validation and reproduction

Latest theorem target:

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationExactUniversalAmbientWhiteheadDataV5_10
~~~

Validated exact PR head:

~~~text
7ca818ff13d01b12a16c9fced18f9898d3f58642
Build completed successfully (8634 jobs)
return_code = 0
~~~

Current theorem-bearing main merge:

~~~text
580e49111b566bf0f74f53c3ca68be03fdf7126b
~~~

Useful endpoint reproduction:

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationExactUniversalLabelledBiequivalenceV4_89 \
  KUOS.DependentOriginationExactUniversalAmbientStrongTransQuotientNaturalityV5_07 \
  KUOS.DependentOriginationExactUniversalAmbientStrongTransCoherentExtensionV5_08 \
  KUOS.DependentOriginationExactUniversalAmbientP4ClosureV5_09 \
  KUOS.DependentOriginationExactUniversalAmbientWhiteheadDataV5_10
~~~

Aggregate and runtime entry points remain:

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
PYTHONPATH=. python3 runtime/kuuos_current_check.py
~~~

README/ROADMAP-only changes are documentation changes. They do not supersede the theorem-bearing baseline.

See [ROADMAP.md](ROADMAP.md) for the completed chain, current boundaries, and proposed next theorem directions.
