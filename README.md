# KuuOS / 空OS

![KuuOS PR Governance Gate](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/pr-governance-gate.yml/badge.svg)
![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS** is a public research architecture for dependent origination (縁起), contextual transport, higher coherence, descent, obstruction, exact presentation, universal properties, and bounded AI operation. Founder: **Hidetoshi Itakura / 板倉英俊**.

> Which structure survives justified changes of context and presentation, how can compatible local information be transported and glued, and which universal property characterizes the invariant content?

## Current formal status

**The integrated theorem spine is now through v5.15.**

The former ambient StrongTrans / P4 / object-coverage frontier is closed inside the exact-universal sector, and the resulting ambient equivalence data has now been strengthened beyond the v5.10 Whitehead-only endpoint.

For every refinement atlas A in the exact-universal sector, the formal development now provides:

- a native source bicategory of exact-universal presentations;
- a strict exact-universal realization into the ambient completion;
- local hom-category equivalences;
- canonical StrongTrans extension through the constructed localization;
- quotient-independent coherent StrongTrans naturality;
- ambient restriction-hom essential surjectivity;
- ambient object coverage;
- canonical ambient WhiteheadBiequivalenceData;
- a canonical source object over every ambient object;
- a genuine ambient-to-source section pseudofunctor;
- a native ambient roundtrip counit StrongTrans;
- a native source roundtrip unit StrongTrans;
- a single explicit ambient biequivalence certificate packaging the Whitehead data, quasi-inverse, unit, and counit.

The current closed chain is:

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
canonical StrongTrans coherence extension
        |
        |  v4.95-v5.09
        v
restriction Hom EssSurj
        |
        v
ambient object coverage
        |
        |  v5.10
        v
canonical ambient WhiteheadBiequivalenceData
        |
        |  v5.11
        v
canonical source over every ambient object
        |
        |  v5.12
        v
ambient -> source quasi-inverse pseudofunctor
        |
        |  v5.13
        v
ambient roundtrip counit StrongTrans
        |
        |  v5.14
        v
source roundtrip unit StrongTrans
        |
        |  v5.15
        v
explicit ambient biequivalence certificate
~~~

This is an exact-universal-sector theorem. It does **not** say that every weakly W-admissible raw contextual system has an exact presentation. The earlier obstruction and nonfactorization theorems remain active and explicitly rule out that converse in general.

## Canonical theorem snapshot — 2026-10-04 JST

| Role | Reference |
| --- | --- |
| Repository / canonical branch | itakura-hidetoshi/KuuOS / **main** |
| Fresh theorem-bearing main | **41d4b4628a6a3d65d4892c143ea197eab2eecb4b** |
| Latest theorem merge | [#1967 — Package ambient biequivalence certificate v5.15](https://github.com/itakura-hidetoshi/KuuOS/pull/1967) |
| Exact validated PR head | **7d222ead4eae477fefbb885e2883a505e49ea13c** |
| Exact-head validation | [Run #3598 / 37204932464](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/37204932464): completed / success |
| Exact-head receipts | Strict Lean: success; exact-head terminal: success |
| Build result | Build completed successfully (8639 jobs) |
| Lean | leanprover/lean4:v4.30.0-rc2 |
| Mathlib | 5450b53e5ddc75d46418fabb605edbf36bd0beb6 |

The v5.15 public axiom reports contain only:

~~~text
propext
Classical.choice
Quot.sound
~~~

There is no sorryAx.

The latest theorem-bearing module is:

[DependentOriginationExactUniversalAmbientBiequivalenceCertificateV5_15.lean](formal/KUOS/DependentOriginationExactUniversalAmbientBiequivalenceCertificateV5_15.lean)

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

The formal program is richer than a graph. It contains contextual systems, mappings between systems, transformations between mappings, bicategorical coherence, quotient/descent structure, obstructions, universal properties, and explicit localization/presentation interfaces.

## Three formal layers

### 1. Exact-universal source

ExactUniversalRawObject is the chosen source sector. A source object stores a raw Cat-valued contextual system together with exact presentation and coherent universal-target data.

The source has typed 1-cells and 2-cells and a native bicategory.

### 2. Object-labelled realized sector

The realized sector keeps the source-object labels while using the corresponding DO₂ carriers and morphisms.

The v4.89 certificate is label preserving. Equivalent realized carriers do not erase distinct source presentations, histories, or world bindings.

### 3. Ambient completion

The ambient completion contains arbitrary objects of the constructed DO₂ completion.

The exact-universal ambient object-coverage problem is now closed: every ambient object has a canonical exact-universal source representative, and v5.12-v5.15 provide an explicit pseudofunctorial roundtrip package connecting the source and the full ambient completion.

This is stronger than the v5.10 existential/Whitehead endpoint, but it remains a statement about the constructed exact-universal sector and its ambient completion.

## Integrated mathematical spine

| Versions | Closed result | Main anchors |
| --- | --- | --- |
| v4.00-v4.12 | Exact C2 nonfactorization and nonzero Stage-II obstruction in ZMod 2 | [v4.00](formal/KUOS/DependentOriginationAbstractNonfactorizationV4_00.lean), [v4.12](formal/KUOS/DependentOriginationStageIIObstructionClassV4_12.lean) |
| v4.13-v4.48 | Incidence/capacity obstructions, recursive/inverse-limit carriers, exact Cantor dimension, switch/orientation descent | [v4.40](formal/KUOS/DependentOriginationStageIIExactFractalCertificateV4_40.lean), [v4.48](formal/KUOS/DependentOriginationStageIIOrbitOrientationDescentV4_48.lean) |
| v4.49-v4.70 | Abstract presentation descent, exact presentation sector, native source bicategory, strict realization | [v4.49](formal/KUOS/DependentOriginationAbstractPresentationDescentV4_49.lean), [v4.69](formal/KUOS/DependentOriginationExactUniversalMappingBicategoryV4_69.lean), [v4.70](formal/KUOS/DependentOriginationExactUniversalRealizationStrictPseudofunctorV4_70.lean) |
| v4.71-v4.83 | Liftability, compatible 2-cell full faithfulness, arbitrary DO₂ 1-cell lifting between chosen carriers, hom-category equivalences | [v4.77](formal/KUOS/DependentOriginationExactUniversalRealizationFullyFaithfulV4_77.lean), [v4.83](formal/KUOS/DependentOriginationExactUniversalHomEquivalenceV4_83.lean) |
| v4.84-v4.89 | Section pseudofunctor, labelled realization, global unit/counit StrongTrans, labelled biequivalence certificate | [v4.84](formal/KUOS/DependentOriginationExactUniversalSectionPseudofunctorV4_84.lean), [v4.89](formal/KUOS/DependentOriginationExactUniversalLabelledBiequivalenceV4_89.lean) |
| v4.90-v4.95 | Ambient Whitehead reduced to object coverage/restriction universality; restriction Faithful/Full; EssSurj reduced to StrongTrans extension | [v4.90](formal/KUOS/DependentOriginationExactUniversalAmbientCoverageReductionV4_90.lean), [v4.95](formal/KUOS/DependentOriginationExactUniversalAmbientStrongTransExtensionV4_95.lean) |
| v4.96-v5.03 | Locally-discrete reduction, presentation/W-inverse/composition naturality, all-arrow existence, identity coherence, transport bridge | [v4.96](formal/KUOS/DependentOriginationExactUniversalAmbientStrongTransLocallyDiscreteV4_96.lean), [v5.03](formal/KUOS/DependentOriginationExactUniversalAmbientStrongTransPresentationTransportV5_03.lean) |
| v5.04-v5.08 | Generator compatibility, generated-localization invariance, quotient descent, and full StrongTrans coherence extension | [v5.06](formal/KUOS/DependentOriginationExactUniversalAmbientStrongTransGeneratedLocalizationV5_06.lean), [v5.08](formal/KUOS/DependentOriginationExactUniversalAmbientStrongTransCoherentExtensionV5_08.lean) |
| v5.09-v5.10 | Ambient P4 closure, object coverage, ambient Whitehead existence, canonical WhiteheadBiequivalenceData | [v5.09](formal/KUOS/DependentOriginationExactUniversalAmbientP4ClosureV5_09.lean), [v5.10](formal/KUOS/DependentOriginationExactUniversalAmbientWhiteheadDataV5_10.lean) |
| v5.11 | Canonical exact-universal source and local hom-section for every ambient object | [v5.11](formal/KUOS/DependentOriginationExactUniversalAmbientCanonicalSourceV5_11.lean) |
| v5.12 | Genuine ambient-to-source canonical section pseudofunctor | [v5.12](formal/KUOS/DependentOriginationExactUniversalAmbientSectionPseudofunctorV5_12.lean) |
| v5.13 | Ambient roundtrip recovers ambient cells and carries a native counit StrongTrans | [v5.13](formal/KUOS/DependentOriginationExactUniversalAmbientRoundtripCounitV5_13.lean) |
| v5.14 | Source-to-ambient-to-source roundtrip carries a native unit StrongTrans despite changed source labels | [v5.14](formal/KUOS/DependentOriginationExactUniversalSourceAmbientRoundtripUnitV5_14.lean) |
| v5.15 | Whitehead data + explicit quasi-inverse + source unit + ambient counit packaged into one ambient biequivalence certificate | [v5.15](formal/KUOS/DependentOriginationExactUniversalAmbientBiequivalenceCertificateV5_15.lean) |

## v5.11-v5.15: explicit ambient quasi-inverse package

### v5.11 — canonical source over every ambient object

[DependentOriginationExactUniversalAmbientCanonicalSourceV5_11.lean](formal/KUOS/DependentOriginationExactUniversalAmbientCanonicalSourceV5_11.lean)

v5.11 uses the closed ambient coverage/restriction-universality machinery to select an exact-universal source object over each ambient object.

Key properties:

~~~text
canonicalSource(Z).carrier = Z
realization.obj (canonicalSource Z) = Z
~~~

It also exposes an exact local hom-section whose lifted object/morphism is the prescribed ambient one-cell/two-cell.

### v5.12 — ambient canonical section pseudofunctor

[DependentOriginationExactUniversalAmbientSectionPseudofunctorV5_12.lean](formal/KUOS/DependentOriginationExactUniversalAmbientSectionPseudofunctorV5_12.lean)

The objectwise source choices and local hom-sections are assembled into a genuine pseudofunctor:

~~~text
Ambient -> Source
~~~

Identity/composition comparisons reuse the already validated v4.84 comparison isomorphisms specialized to the canonical source labels.

After strict realization:

~~~text
section.obj Z  -> Z
section.map f  -> f
section.map₂ η -> η
~~~

exactly.

### v5.13 — ambient roundtrip counit

[DependentOriginationExactUniversalAmbientRoundtripCounitV5_13.lean](formal/KUOS/DependentOriginationExactUniversalAmbientRoundtripCounitV5_13.lean)

Define:

~~~text
Ambient -> Source -> Ambient
~~~

The roundtrip recovers objects, one-cells, and two-cells exactly, and its mapId/mapComp comparison cells reduce to identities.

This yields a native Mathlib StrongTrans:

~~~text
canonicalSection ≫ realization
  ⟶
Id_Ambient
~~~

### v5.14 — source roundtrip unit

[DependentOriginationExactUniversalSourceAmbientRoundtripUnitV5_14.lean](formal/KUOS/DependentOriginationExactUniversalSourceAmbientRoundtripUnitV5_14.lean)

Define:

~~~text
Source -> Ambient -> Source
~~~

The roundtrip changes the source label to the canonical source over the same carrier, so the unit component is **not** taken to be a literal source identity.

Instead, the unit component is the canonical lift of the ambient identity:

~~~text
X.carrier --id--> X.carrier
~~~

Naturality is first formed in DO₂ using native unitors and then uniquely lifted back through the fully faithful exact realization.

This yields:

~~~text
Id_Source
  ⟶
realization ≫ canonicalSection
~~~

as a native StrongTrans.

### v5.15 — ambient biequivalence certificate

[DependentOriginationExactUniversalAmbientBiequivalenceCertificateV5_15.lean](formal/KUOS/DependentOriginationExactUniversalAmbientBiequivalenceCertificateV5_15.lean)

v5.15 packages:

~~~text
whitehead    := v5.10 canonical ambient Whitehead data
quasiInverse := v5.12 canonical ambient section pseudofunctor
unit         := v5.14 source roundtrip unit
counit       := v5.13 ambient roundtrip counit
~~~

into:

~~~text
ExactUniversalAmbientBiequivalenceCertificate
~~~

The endpoint therefore contains an explicit global quasi-inverse and native unit/counit, not only local equivalences plus object essential surjectivity.

## Boundaries that remain explicit

### Weak W-admissibility does not imply exact presentation

The obstruction chain remains valid:

~~~text
weak W-admissibility can hold
while exact localization / exact presentation is impossible.
~~~

The positive v4.49-v5.15 chain is an exact-universal-sector theorem. It does not erase the countermodels.

### v5.15 is not yet a triangle-modification package

The repository now has:

- forward pseudofunctor;
- explicit quasi-inverse pseudofunctor;
- native source unit StrongTrans;
- native ambient counit StrongTrans;
- local hom equivalences;
- object essential surjectivity.

What is **not yet separately formalized** is a stronger tricategorical adjoint-biequivalence structure carrying explicitly named triangle modifications/coherence between the unit and counit.

Do not silently identify v5.15 with such a stronger package.

### The final mapping/classification theorem is still open

A schematic long-range goal is:

~~~text
eta : C -> DO(C,W,J,H)

AdmissibleContextualSystems(C,X)
  ≃
Fun(DO(C,W,J,H),X)
~~~

This is not yet a final theorem statement.

A correct formulation must retain the distinction between semantic admissibility and exact liftability and must specify higher morphisms, variance, world/presentation labels, factor existence, and coherent uniqueness.

## Current research frontier

The StrongTrans localization, ambient P4, ambient object coverage, canonical Whitehead data, and explicit quasi-inverse/unit/counit packaging are now closed.

The next work should focus on:

1. **Triangle coherence, if required.** Decide whether the final target needs explicit triangle modifications beyond the v5.15 certificate, and formalize them only if they are mathematically necessary.
2. **Mapping/classification formulation.** State the correct higher universal property characterized by the exact-universal construction.
3. **Semantic admissibility versus exact liftability.** Characterize precisely which admissible systems lie in the exact-universal image and how obstruction classes govern failure.
4. **Prescribed data versus canonical choices.** Distinguish canonical extension/existence from preservation of externally prescribed components, actions, and world bindings.
5. **World/presentation-sensitive semantics.** Preserve conventional/world-specific distinctions even when invariant carriers are equivalent.

These are proposed research directions, not current theorem claims.

## Proof-engineering lessons retained

- Authority is the exact theorem-bearing Git SHA, not conversation history.
- Importing a module does not open its namespaces.
- With autoImplicit false, namespace mistakes become immediate unknown-identifier errors.
- Structure universe inference is more robust when theorem-critical field types use explicit concrete universe-instantiated types instead of underconstrained abbrev layers.
- Typeclass search does not proceed when key input types are unresolved metavariables; annotate dependent endpoints before invoking category lemmas.
- change is definitional only.
- rfl should be used only after confirming definitional equality of the exact projections involved.
- In dependent equalities, explicit Eq.trans / congrArg / congrArg₂ proof terms are often more stable than broad rw.
- For fully faithful preimages in dependent hom categories, explicitly naming source/target 1-cells can stabilize elaboration.
- Category Hom aliases may resist ordinary cases/induction; use the path-specific induction API.
- For double opposites, composition order reverses twice and returns to the original order.
- Keep quotient representatives as computational scaffolding; prove representative independence separately.
- Do not infer theorem authority from docs, runtime output, cache success, or a different Lean lane.

## Validation and reproduction

Latest theorem target:

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationExactUniversalAmbientBiequivalenceCertificateV5_15
~~~

Validated exact PR head:

~~~text
7d222ead4eae477fefbb885e2883a505e49ea13c
Build completed successfully (8639 jobs)
return_code = 0
~~~

Current theorem-bearing main merge:

~~~text
41d4b4628a6a3d65d4892c143ea197eab2eecb4b
~~~

Useful endpoint reproduction:

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationExactUniversalLabelledBiequivalenceV4_89 \
  KUOS.DependentOriginationExactUniversalAmbientStrongTransCoherentExtensionV5_08 \
  KUOS.DependentOriginationExactUniversalAmbientP4ClosureV5_09 \
  KUOS.DependentOriginationExactUniversalAmbientWhiteheadDataV5_10 \
  KUOS.DependentOriginationExactUniversalAmbientCanonicalSourceV5_11 \
  KUOS.DependentOriginationExactUniversalAmbientSectionPseudofunctorV5_12 \
  KUOS.DependentOriginationExactUniversalAmbientRoundtripCounitV5_13 \
  KUOS.DependentOriginationExactUniversalSourceAmbientRoundtripUnitV5_14 \
  KUOS.DependentOriginationExactUniversalAmbientBiequivalenceCertificateV5_15
~~~

Aggregate and runtime entry points remain:

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
PYTHONPATH=. python3 runtime/kuuos_current_check.py
~~~

README/ROADMAP-only changes are documentation changes. They do not supersede the theorem-bearing baseline.

See [ROADMAP.md](ROADMAP.md) for the completed chain, current boundaries, and proposed next theorem directions.
