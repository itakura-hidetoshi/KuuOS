# KuuOS / 空OS Roadmap

**Theorem snapshot: 2026-10-04 JST · integrated through v5.10**

**現在地：object-labelled exact-universal sector の Whitehead-style certificate は v4.89 で閉じ、v4.90–v5.10 により exact-universal ambient completion への拡張も閉じた。v5.09 で ambient StrongTrans extension / restriction-hom EssSurj / ambient object coverage / ambient Whitehead existence が無条件化され、v5.10 で forward が actual exact-universal realization に一致する canonical WhiteheadBiequivalenceData が実体化された。現在の主 frontier は、これを弱い W-admissibility 全体へ無条件拡張することではなく、obstruction を保持したまま final mapping/classification property を正確に定式化することである。**

This roadmap separates **integrated Lean theorems** from **proposed research obligations**. Fresh exact theorem artifacts are authoritative; plans, README text, runtime output, and conversation history are not theorem evidence.

## 0. Reproducible theorem snapshot

| Role | Reference |
| --- | --- |
| Repository / canonical branch | itakura-hidetoshi/KuuOS / **main** |
| Fresh theorem-bearing main | **580e49111b566bf0f74f53c3ca68be03fdf7126b** |
| Latest theorem merge | [#1961 — Package canonical ambient Whitehead data v5.10](https://github.com/itakura-hidetoshi/KuuOS/pull/1961) |
| Exact validated PR head | **7ca818ff13d01b12a16c9fced18f9898d3f58642** |
| Associated CI | [Run #3587 / 37192661698](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/37192661698): completed / success |
| Exact-head receipts | Strict Lean: success; exact-head terminal: success |
| Build | Build completed successfully (8634 jobs) |
| Lean | leanprover/lean4:v4.30.0-rc2 |
| Mathlib | 5450b53e5ddc75d46418fabb605edbf36bd0beb6 |

The latest theorem-bearing module is:

[DependentOriginationExactUniversalAmbientWhiteheadDataV5_10.lean](formal/KUOS/DependentOriginationExactUniversalAmbientWhiteheadDataV5_10.lean)

Its public axiom reports contain only:

~~~text
propext
Classical.choice
Quot.sound
~~~

There is no sorryAx.

Authority order:

~~~text
fresh exact canonical GitHub SHA
  > formal Lean theorem artifacts at that SHA
  > README / ROADMAP
  > exact-head CI/runtime receipts
  > history / conversation memory
~~~

**Protected validation lane:** [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) is still **open / draft / unmerged** and is not canonical theorem authority. It must not be merged into the canonical line merely to validate Lean 4.31.

## 1. Long-range target

The long-range target remains a higher dependent-origination mapping/classification principle, schematically:

~~~text
eta : C -> DO(C,W,J,H)

AdmissibleContextualSystems(C,X)
  ≃
Fun(DO(C,W,J,H),X)
~~~

This is **not yet a theorem statement**.

A correct final formulation must make explicit:

- the exact source and target higher categories;
- semantic W-admissibility versus exact presentation/liftability;
- localization and descent hypotheses;
- allowed 1-cells and 2-cells;
- world, context, and presentation labels;
- factor existence;
- coherent uniqueness;
- pseudonaturality under justified context/presentation changes;
- the role of the obstruction classes on the complement of the exact-universal image.

The formal obstruction results prohibit silently replacing “exactly liftable” by “weakly admissible.”

## 2. Closed obstruction and presentation foundations — v4.00-v4.70

| Versions | Integrated theorem content | Boundary retained |
| --- | --- | --- |
| v4.00-v4.12 | Exact C2 nonfactorization and nonzero Stage-II obstruction in ZMod 2 | weak admissibility does not force exact factorization |
| v4.13-v4.48 | Incidence/capacity obstructions; recursive/inverse-limit carriers; exact Cantor dimension; switch/orientation descent | concrete carrier geometry is a stress test, not the universal definition |
| v4.49 | Abstract presentation descent iff presentation invariance | presentation result, not final mapping theorem |
| v4.50-v4.56 | Exact higher presentation sector and coherent universal-target comparison | exactness remains an explicit positive-sector condition |
| v4.57-v4.60 | Typed source objects, 1-cells, 2-cells, genuine hom categories | compatibility is part of the source type |
| v4.61-v4.68 | Whiskering, interchange, inverse laws, pentagon, triangle | bicategorical coherence is explicit |
| v4.69-v4.70 | Native source Bicategory and strict DO₂ realization | strict target realization does not make the source bicategory strict |

The positive implication chain remains:

~~~text
exact DO₂ presentation
  => higher stack-localization factorization
  => higher localization factorization
  => weak W-admissibility
~~~

The converse is false in general by the obstruction chain.

## 3. Local mapping and labelled global theory — v4.71-v4.89

### v4.71-v4.83 — local mapping theory

Closed:

- presentation-indexed liftability;
- compatible 2-cell full faithfulness;
- pointwise inverse StrongTrans coherence;
- arbitrary DO₂ 1-cell lifting between existing chosen carriers;
- hom-category equivalences.

Endpoint:

~~~text
(X ⟶ Y) ≌ (X.carrier ⟶ Y.carrier)
~~~

for existing exact-universal source objects.

This closes the local exact-universal mapping problem on the chosen source sector.

### v4.84-v4.89 — object-labelled global certificate

Closed:

- section pseudofunctor;
- label-preserving realization;
- global source unit StrongTrans;
- realized counit StrongTrans;
- Whitehead-style biequivalence certificate on the object-labelled realized sector.

The object labels are intentionally retained. Equivalent realized carriers do not erase source presentation, context history, or world binding.

## 4. Ambient reduction — v4.90-v4.95

These versions converted the ambient problem into a sequence of explicit local conditions.

### v4.90

~~~text
ExactUniversalAmbientWhiteheadExistence
  ↔
ExactUniversalAmbientObjectCoverage
~~~

### v4.91

Uniform canonical restriction universality implies ambient object coverage.

### v4.92

Restriction hom-equivalence implies canonical restriction universality.

### v4.93

Restriction is unconditionally Faithful.

### v4.94

Restriction is unconditionally Full.

Therefore:

~~~text
ExactUniversalAmbientRestrictionHomEquivalence
  ↔
ExactUniversalAmbientRestrictionHomEssSurj
~~~

### v4.95

Raw StrongTrans object components extend canonically to localized objects.

The remaining obstacle was isolated as:

~~~text
HigherLocalizedStrongTransCoherenceExtension
~~~

Existence of this extension implies restriction-hom EssSurj.

At v4.95 this was still conditional. v5.04-v5.09 subsequently discharged the condition.

## 5. StrongTrans localization coherence — v4.96-v5.03

### v4.96 — locally-discrete reduction

Source 2-cell naturality is automatic because the source is locally discrete.

The genuine remaining package became:

~~~text
HigherLocalizedStrongTransOneCellCoherenceExtension
~~~

with four fields:

1. naturality
2. naturality_id
3. naturality_comp
4. restrict_modification_naturality

### v4.97 — presentation naturality

Canonical naturality is defined on presentation-image arrows using the raw StrongTrans naturality.

The exact raw restriction square is proved.

### v4.98 — inverse naturality

Naturality is constructed on inverses of localized isomorphisms and specialized to formal W-inverse arrows.

### v4.99 — composition

The canonical StrongTrans composition constructor is formalized and pointwise existence is closed under composition.

### v5.00 — all-arrow existence

Mathlib localization generation yields Nonempty naturality data for every localized arrow.

Important historical boundary:

~~~text
∀ f, Nonempty (NaturalityIso f)
~~~

did not yet imply a coherent global choice.

### v5.01-v5.03

Closed:

- canonical identity naturality;
- exact identity coherence;
- presentation identity/composition coherence;
- transport of naturality along source 1-cell isomorphisms;
- exact Pseudofunctor.comp mapId/mapComp decomposition.

These modules supplied the normalization machinery used in the final descent.

## 6. Canonical localization descent — v5.04-v5.07

This entire former frontier is now closed.

### v5.04 — id / comp transport compatibility

[DependentOriginationExactUniversalAmbientStrongTransTransportCompatibilityV5_04.lean](formal/KUOS/DependentOriginationExactUniversalAmbientStrongTransTransportCompatibilityV5_04.lean)

Proves:

~~~text
presentation naturality on identity
  = transported canonical localized identity naturality

presentation naturality on composite
  = transported canonical localized composition naturality
~~~

Thus relations.id and relations.comp introduce no ambiguity.

### v5.05 — W-inverse relation compatibility

[DependentOriginationExactUniversalAmbientStrongTransWRelationCompatibilityV5_05.lean](formal/KUOS/DependentOriginationExactUniversalAmbientStrongTransWRelationCompatibilityV5_05.lean)

Closes the Winv₁ and Winv₂ generators using the inverse naturality specification and localized isomorphism unit/counit equations.

After v5.05, all four Mathlib localization generators are compatible with the canonical naturality assignment:

~~~text
id
comp
Winv₁
Winv₂
~~~

### v5.06 — retained generated localization invariance

No new relation language is introduced.

The existing v2.68 Type-valued syntax is reused:

~~~text
LocalizationGenerating2Cell
GeneratedCompClosure2Cell
GeneratedLocalization2Cell
~~~

The v5.06 module family supplies:

- canonical naturality evaluation on free localization paths;
- generator invariance;
- transport/whisker compatibility;
- identity/composition/associativity normalization;
- composition-closure invariance;
- full refl/symm/trans generated localization invariance.

Key endpoint:

~~~text
higherLocalizedStrongTransPathNaturality_generatedLocalization_invariant
~~~

### v5.07 — quotient-independent canonical naturality

[DependentOriginationExactUniversalAmbientStrongTransQuotientNaturalityV5_07.lean](formal/KUOS/DependentOriginationExactUniversalAmbientStrongTransQuotientNaturalityV5_07.lean)

The free-path evaluator descends to actual arrows of Mathlib's constructed localization.

The data-level endpoint is:

~~~text
higherLocalizedCanonicalStrongTransNaturality
~~~

Representative independence is theorem-level. Quot.out is only computational scaffolding.

## 7. Coherent extension and ambient closure — v5.08-v5.10

### v5.08 — assemble the v4.96 / v4.95 extension

[DependentOriginationExactUniversalAmbientStrongTransCoherentExtensionV5_08.lean](formal/KUOS/DependentOriginationExactUniversalAmbientStrongTransCoherentExtensionV5_08.lean)

Closed:

- presentation bridge;
- exact raw restriction square;
- identity normalization and v4.96 identity coherence;
- quotient composition compatibility;
- source-indexed composition normalization;
- v4.96 composition coherence;
- construction of HigherLocalizedStrongTransOneCellCoherenceExtension;
- reconstruction of the full HigherLocalizedStrongTransCoherenceExtension;
- uniform HigherLocalizedStrongTransExtensionExists.

Key declarations include:

~~~text
higherLocalizedCanonicalStrongTransNaturalityOnSource
higherLocalizedCanonicalStrongTransOneCellCoherenceExtension
higherLocalizedCanonicalStrongTransCoherenceExtension
higherLocalizedCanonicalStrongTransExtensionExists
~~~

Thus v4.95 is no longer conditional inside this exact-universal construction.

### v5.09 — close the current ambient P4 route

[DependentOriginationExactUniversalAmbientP4ClosureV5_09.lean](formal/KUOS/DependentOriginationExactUniversalAmbientP4ClosureV5_09.lean)

For every refinement atlas A, the formalization now proves:

~~~text
exactUniversalAmbientRestrictionStrongTransExtension_canonical
exactUniversalAmbientRestrictionHomEssSurj_canonical
exactUniversalAmbientObjectCoverage_canonical
exactUniversalAmbientWhiteheadExistence_canonical
~~~

The former ambient object-coverage frontier is closed.

### v5.10 — canonical ambient Whitehead data

[DependentOriginationExactUniversalAmbientWhiteheadDataV5_10.lean](formal/KUOS/DependentOriginationExactUniversalAmbientWhiteheadDataV5_10.lean)

The endpoint is made explicit as data:

~~~text
exactUniversalAmbientCanonicalWhiteheadBiequivalenceData
~~~

and the following properties are theorem-level:

- its forward pseudofunctor is the actual exact-universal realization;
- its local hom equivalence is the existing exact-universal ambient hom equivalence;
- every ambient completion object has an essentially-surjective source witness;
- the v5.09 existential Whitehead endpoint is witnessed by this canonical datum.

The current sufficient ambient P4 route is therefore completely integrated.

## 8. Current closed boundary

### CLOSED

~~~text
obstruction / nonfactorization countermodels
exact presentation and coherent universal-target sector
native source bicategory
strict DO₂ realization
local compatible full faithfulness
arbitrary DO₂ 1-cell lift between chosen carriers
source/realized hom-category equivalences
section pseudofunctor
global unit/counit StrongTrans
object-labelled Whitehead certificate
ambient Whitehead iff object coverage
restriction Faithful
restriction Full
restriction hom-equivalence iff EssSurj
canonical StrongTrans object components
automatic source 2-cell naturality
presentation-arrow naturality + exact restriction square
W-inverse naturality
composition closure
all-arrow Nonempty naturality existence
canonical identity naturality
presentation id/comp coherence
transport bridge
id / comp localization-generator compatibility
Winv₁ / Winv₂ compatibility
retained generated-localization invariance
quotient-independent canonical naturality
v4.96 one-cell coherence extension
full v4.95 StrongTrans coherence extension
ambient restriction-hom EssSurj
ambient exact-universal object coverage
ambient Whitehead existence
canonical ambient WhiteheadBiequivalenceData
~~~

## 9. What remains open

The old v5.04-v5.09 checklist is no longer the frontier.

### A. Final higher mapping/classification property

The main conceptual target is to formulate and prove the correct mapping property above the exact-universal construction.

Questions that must be settled in the statement itself:

- What is the correct category/bicategory of admissible contextual systems?
- Which systems are exact-liftable?
- Which equivalences must retain world/presentation labels?
- What is the precise functor category on the right-hand side?
- What is the correct coherent uniqueness notion?
- How should obstruction data appear when exact liftability fails?

### B. Semantic admissibility versus exact liftability

The formal program already contains both:

- positive exact-universal construction theorems;
- negative obstruction/nonfactorization theorems.

A next theorem should characterize the boundary rather than erase it.

The desired shape is not:

~~~text
weak W-admissibility => exact presentation
~~~

because that is false in general.

The useful target is closer to a criterion identifying the exact-universal image and explaining failure through obstruction data.

### C. Stronger biequivalence packaging, if required

v5.10 provides WhiteheadBiequivalenceData.

If the final application requires a stronger package—such as an explicitly chosen ambient quasi-inverse pseudofunctor, unit/counit at that ambient level, or triangle identities—those must be formalized separately.

Do not describe v5.10 as such a stronger structure until it exists.

### D. Prescribed external data versus canonical choices

The v5.x solution succeeds by making canonical naturality and representative-independent choices.

A separate question is whether independently prescribed raw components, actions, or world bindings can always be preserved by an extension. This is not implied merely by existence of the canonical extension.

### E. World-sensitive semantics

A final KuuOS semantics should not collapse conventional/world-specific distinctions merely because a paramārtha-level carrier or equivalence agrees.

The formal classification layer should retain the distinction between:

- invariant structural content;
- presentation/world binding;
- action semantics.

## 10. Proposed next theorem units

The labels below are **proposals**, not existing theorem claims.

### Proposed v5.11 — classification interface

Define the exact category/bicategory of contextual systems to be classified and the exact functor/mapping object on the target side.

Exit criterion: a type-correct theorem statement with all variance, morphism, world, and presentation data explicit.

### Proposed v5.12 — exact-liftability criterion

Relate semantic admissibility, exact presentation, and the obstruction classes already developed in v4.00-v4.48.

Exit criterion: a theorem that identifies a sufficient/necessary exact-liftability condition without contradicting the established countermodels.

### Proposed v5.13+ — higher mapping theorem

Use the exact-universal realization, hom equivalences, ambient object coverage, and v5.10 Whitehead data as the structural core of the final mapping/classification theorem.

Do not begin by postulating the final equivalence. First type and prove its factorization and coherent uniqueness components separately.

## 11. Proof-engineering rules retained

### Authority discipline

Always re-observe the fresh canonical SHA before theorem work.

Do not treat a docs-only merge, runtime check, cache hit, or historical conversation as theorem authority.

### Namespace discipline

Importing a module does not open its namespaces.

With autoImplicit false, an unopened namespace produces an immediate unknown-identifier failure, which is desirable.

### Dependent equality discipline

Prefer explicit proof terms such as:

~~~text
Eq.trans
congrArg
congrArg₂
~~~

when the equality structure is known.

Broad rw in dependent expressions can leave casts, fail to find the intended occurrence, or create fragile elaboration.

### Path/category Hom discipline

Category Hom aliases may not expose constructors to ordinary cases/induction.

Use the appropriate Paths induction/decomposition API.

### Bicategory discipline

- change only for definitional equality;
- use structure fields when the goal is exactly a structure field;
- use public Iso hom/inv projection lemmas for composite isomorphisms;
- expose endpoints before broad coherence tactics;
- double opposite reverses composition twice.

### Quotient discipline

Representative choice may be computational.

Mathematical content must be representative-independent theorem-level data.

## 12. Validation and reproduction

Latest theorem target:

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationExactUniversalAmbientWhiteheadDataV5_10
~~~

Validated exact head:

~~~text
7ca818ff13d01b12a16c9fced18f9898d3f58642
Build completed successfully (8634 jobs)
return_code = 0
~~~

Current theorem-bearing main:

~~~text
580e49111b566bf0f74f53c3ca68be03fdf7126b
~~~

Useful endpoint reproduction:

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationExactUniversalLabelledBiequivalenceV4_89 \
  KUOS.DependentOriginationExactUniversalAmbientStrongTransGeneratedLocalizationV5_06 \
  KUOS.DependentOriginationExactUniversalAmbientStrongTransQuotientNaturalityV5_07 \
  KUOS.DependentOriginationExactUniversalAmbientStrongTransCoherentExtensionV5_08 \
  KUOS.DependentOriginationExactUniversalAmbientP4ClosureV5_09 \
  KUOS.DependentOriginationExactUniversalAmbientWhiteheadDataV5_10
~~~

Aggregate and runtime entry points:

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
PYTHONPATH=. python3 runtime/kuuos_current_check.py
~~~

README/ROADMAP-only commits should not be treated as newer theorem-bearing baselines.
