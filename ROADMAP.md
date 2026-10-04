# KuuOS / 空OS Roadmap

**Theorem snapshot: 2026-10-04 JST · integrated through v5.15**

**現在地：v4.90 以降の ambient frontier は完全に進展し、v5.09 で ambient P4 / object coverage、v5.10 で canonical Whitehead data、v5.11-v5.14 で canonical ambient section・explicit quasi-inverse・source unit・ambient counit、v5.15 でそれらを束ねた explicit ambient biequivalence certificate まで形式化された。現在の主 frontier は、必要なら triangle modifications を追加することと、obstruction を保持した final mapping/classification property を正確に定式化することである。**

This roadmap separates **integrated Lean theorems** from **proposed research obligations**. Fresh exact theorem artifacts are authoritative; plans, README text, runtime output, and conversation history are not theorem evidence.

## 0. Reproducible theorem snapshot

| Role | Reference |
| --- | --- |
| Repository / canonical branch | itakura-hidetoshi/KuuOS / **main** |
| Fresh theorem-bearing main | **41d4b4628a6a3d65d4892c143ea197eab2eecb4b** |
| Latest theorem merge | [#1967 — Package ambient biequivalence certificate v5.15](https://github.com/itakura-hidetoshi/KuuOS/pull/1967) |
| Exact validated PR head | **7d222ead4eae477fefbb885e2883a505e49ea13c** |
| Associated CI | [Run #3598 / 37204932464](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/37204932464): completed / success |
| Exact-head receipts | Strict Lean: success; exact-head terminal: success |
| Build | Build completed successfully (8639 jobs) |
| Lean | leanprover/lean4:v4.30.0-rc2 |
| Mathlib | 5450b53e5ddc75d46418fabb605edbf36bd0beb6 |

The latest theorem-bearing module is:

[DependentOriginationExactUniversalAmbientBiequivalenceCertificateV5_15.lean](formal/KUOS/DependentOriginationExactUniversalAmbientBiequivalenceCertificateV5_15.lean)

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
- the role of obstruction classes on the complement of the exact-universal image.

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
| v4.69-v4.70 | Native source bicategory and strict DO₂ realization | strict target realization does not make the source bicategory strict |

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

### v4.84-v4.89 — object-labelled global certificate

Closed:

- section pseudofunctor;
- label-preserving realization;
- global source unit StrongTrans;
- realized counit StrongTrans;
- Whitehead-style local/object data;
- explicit labelled quasi-inverse;
- object-labelled biequivalence certificate.

The object labels are intentionally retained. Equivalent realized carriers do not erase source presentation, context history, or world binding.

## 4. Ambient reduction — v4.90-v4.95

These versions converted the ambient problem into explicit local conditions.

### v4.90

~~~text
ExactUniversalAmbientWhiteheadExistence
  ↔
ExactUniversalAmbientObjectCoverage
~~~

### v4.91

Uniform canonical restriction universality implies ambient object coverage.

### v4.92-v4.94

Restriction-hom equivalence is reduced to essential surjectivity:

~~~text
restriction Faithful
restriction Full

therefore

ExactUniversalAmbientRestrictionHomEquivalence
  ↔
ExactUniversalAmbientRestrictionHomEssSurj
~~~

### v4.95

StrongTrans object components extend canonically on objects, and the remaining obstruction is isolated as:

~~~text
HigherLocalizedStrongTransCoherenceExtension
~~~

Existence of this extension implies restriction-hom EssSurj.

## 5. StrongTrans localization coherence — v4.96-v5.03

### v4.96

Locally-discrete source 2-cell naturality is automatic.

The essential package becomes:

~~~text
HigherLocalizedStrongTransOneCellCoherenceExtension
~~~

with fields:

1. naturality
2. naturality_id
3. naturality_comp
4. restrict_modification_naturality

### v4.97-v5.03

Closed:

- presentation-arrow naturality;
- exact restriction square;
- formal W-inverse naturality;
- composition constructor;
- all-arrow Nonempty naturality existence;
- canonical identity naturality;
- exact identity coherence;
- presentation identity/composition coherence;
- transport of naturality along source 1-cell isomorphisms;
- exact Pseudofunctor.comp normalization.

At v5.03 the remaining issue was coherent descent through the localization relations.

## 6. Canonical localization descent — v5.04-v5.08

This entire frontier is now closed.

### v5.04

Canonical presentation identity/composition choices agree with transported localized choices.

### v5.05

Winv₁ / Winv₂ compatibility is closed.

After v5.05 all four localization generators are compatible:

~~~text
id
comp
Winv₁
Winv₂
~~~

### v5.06

The existing v2.68 relation syntax is retained:

~~~text
LocalizationGenerating2Cell
GeneratedCompClosure2Cell
GeneratedLocalization2Cell
~~~

The canonical path evaluator is invariant under:

- generator relations;
- whiskering;
- composition closure;
- associativity normalization;
- refl/symm/trans generated localization closure.

### v5.07

Naturality descends to actual localization arrows and becomes quotient-independent:

~~~text
higherLocalizedCanonicalStrongTransNaturality
~~~

### v5.08

The quotient-independent family is reindexed to the source and satisfies the full v4.96 package.

Key endpoints:

~~~text
higherLocalizedCanonicalStrongTransOneCellCoherenceExtension
higherLocalizedCanonicalStrongTransCoherenceExtension
higherLocalizedCanonicalStrongTransExtensionExists
~~~

Thus the v4.95 extension condition is unconditionally discharged in the exact-universal construction.

## 7. Ambient P4 and Whitehead closure — v5.09-v5.10

### v5.09

[DependentOriginationExactUniversalAmbientP4ClosureV5_09.lean](formal/KUOS/DependentOriginationExactUniversalAmbientP4ClosureV5_09.lean)

For every refinement atlas A:

~~~text
exactUniversalAmbientRestrictionStrongTransExtension_canonical
exactUniversalAmbientRestrictionHomEssSurj_canonical
exactUniversalAmbientObjectCoverage_canonical
exactUniversalAmbientWhiteheadExistence_canonical
~~~

are theorem-level consequences.

The former ambient object-coverage frontier is closed.

### v5.10

[DependentOriginationExactUniversalAmbientWhiteheadDataV5_10.lean](formal/KUOS/DependentOriginationExactUniversalAmbientWhiteheadDataV5_10.lean)

The ambient endpoint is exposed as actual data:

~~~text
exactUniversalAmbientCanonicalWhiteheadBiequivalenceData
~~~

with:

- forward = exact-universal realization;
- local hom equivalence = existing exact-universal hom equivalence;
- ambient object essential surjectivity.

At this point the global quasi-inverse/unit/counit were not yet packaged.

## 8. Explicit ambient quasi-inverse and roundtrips — v5.11-v5.14

### v5.11 — canonical ambient source

[DependentOriginationExactUniversalAmbientCanonicalSourceV5_11.lean](formal/KUOS/DependentOriginationExactUniversalAmbientCanonicalSourceV5_11.lean)

For every ambient object Z, choose a canonical exact-universal source with:

~~~text
canonicalSource(Z).carrier = Z
realization.obj (canonicalSource Z) = Z
~~~

and a local hom-section recovering prescribed ambient one- and two-cells exactly.

### v5.12 — ambient canonical section pseudofunctor

[DependentOriginationExactUniversalAmbientSectionPseudofunctorV5_12.lean](formal/KUOS/DependentOriginationExactUniversalAmbientSectionPseudofunctorV5_12.lean)

The v5.11 objectwise/local choices are assembled into:

~~~text
exactUniversalAmbientCanonicalSectionPseudofunctor :
  Ambient -> Source
~~~

This is a genuine Mathlib Pseudofunctor.

After strict realization, object/map/map₂ recover the original ambient data.

### v5.13 — ambient roundtrip counit

[DependentOriginationExactUniversalAmbientRoundtripCounitV5_13.lean](formal/KUOS/DependentOriginationExactUniversalAmbientRoundtripCounitV5_13.lean)

The composite:

~~~text
Ambient -> Source -> Ambient
~~~

recovers ambient objects, one-cells, and two-cells exactly.

Its structural comparisons reduce to identities, yielding:

~~~text
canonicalSection ≫ realization
  ⟶
Id_Ambient
~~~

as a native StrongTrans counit.

### v5.14 — source roundtrip unit

[DependentOriginationExactUniversalSourceAmbientRoundtripUnitV5_14.lean](formal/KUOS/DependentOriginationExactUniversalSourceAmbientRoundtripUnitV5_14.lean)

The composite:

~~~text
Source -> Ambient -> Source
~~~

changes the source label, even though the carrier is unchanged.

Therefore the unit component is not a literal source identity. It is the canonical source lift of:

~~~text
𝟙 X.carrier
~~~

The ambient naturality square is lifted uniquely through full faithfulness, producing:

~~~text
Id_Source
  ⟶
realization ≫ canonicalSection
~~~

as a native StrongTrans unit.

## 9. Ambient biequivalence certificate — v5.15

[DependentOriginationExactUniversalAmbientBiequivalenceCertificateV5_15.lean](formal/KUOS/DependentOriginationExactUniversalAmbientBiequivalenceCertificateV5_15.lean)

v5.15 packages:

~~~text
whitehead
quasiInverse
unit
counit
~~~

into:

~~~text
ExactUniversalAmbientBiequivalenceCertificate
~~~

Concretely:

~~~text
whitehead
  = exactUniversalAmbientCanonicalWhiteheadBiequivalenceData

quasiInverse
  = exactUniversalAmbientCanonicalSectionPseudofunctor

unit
  = exactUniversalSourceAmbientRoundtripUnit

counit
  = exactUniversalAmbientRoundtripCounit
~~~

Thus the current ambient endpoint is stronger than the old Whitehead-only existence statement.

The formal development now contains:

- local hom equivalences;
- ambient object essential surjectivity;
- explicit global quasi-inverse pseudofunctor;
- source unit StrongTrans;
- ambient counit StrongTrans.

## 10. Current closed boundary

### CLOSED

~~~text
obstruction / nonfactorization countermodels
exact presentation and coherent universal-target sector
native source bicategory
strict DO₂ realization
local compatible full faithfulness
arbitrary DO₂ 1-cell lift between chosen carriers
source/realized hom-category equivalences
object-labelled section pseudofunctor
object-labelled unit/counit StrongTrans
object-labelled biequivalence certificate
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
canonical ambient WhiteheadBiequivalenceData
canonical source over every ambient object
ambient-to-source section pseudofunctor
ambient roundtrip counit StrongTrans
source roundtrip unit StrongTrans
explicit ambient biequivalence certificate
~~~

## 11. What remains open

The old StrongTrans/P4/quasi-inverse packaging frontier is no longer open.

### A. Triangle modifications / stronger adjoint-biequivalence package

v5.15 records an explicit quasi-inverse and native unit/counit StrongTrans.

What is not yet separately formalized is a stronger tricategorical adjoint-biequivalence structure with explicit triangle modifications/coherence equations connecting the unit and counit.

This should be added only if the final theorem requires that stronger package.

### B. Final higher mapping/classification property

The main conceptual target remains to formulate and prove the correct universal property above the exact-universal construction.

Questions that must be fixed in the theorem statement:

- What is the precise bicategory/category of admissible contextual systems?
- Which systems are exact-liftable?
- Which world/presentation labels remain part of equivalence data?
- What is the correct mapping/functor category?
- What is the coherent uniqueness notion?
- How do the obstruction classes appear outside the exact-universal image?

### C. Semantic admissibility versus exact liftability

The repository now has both:

- a very strong positive exact-universal ambient equivalence package;
- explicit negative obstruction/nonfactorization theorems.

The next conceptual theorem should characterize the boundary between them rather than erase it.

In particular, the desired theorem cannot be:

~~~text
weak W-admissibility => exact presentation
~~~

because the repository already proves counterexamples.

### D. Prescribed external data versus canonical choices

v5.04-v5.15 use canonical, representative-independent choices.

A different question is whether independently prescribed components/actions/world bindings can be preserved by an extension. Canonical existence does not imply arbitrary prescribed-data preservation.

### E. World-sensitive semantics

A final KuuOS classification theorem should distinguish:

- invariant structural content;
- source/presentation labels;
- world binding;
- action semantics.

Paramārtha-level equivalence must not automatically erase conventional/world-specific distinctions.

## 12. Proposed next theorem units

The labels below are **proposals**, not existing theorem claims.

### Proposed v5.16 — ambient triangle coherence

If needed, formulate the two triangle composites built from the v5.14 unit and v5.13 counit and prove the appropriate modification/coherence equations.

Exit criterion:

- no new arbitrary choice;
- triangle data grounded in the existing canonical section;
- exact projection under realization;
- Strict Lean GREEN with no sorryAx.

### Proposed v5.17 — classification interface

Define the exact domain/codomain of the final mapping property.

Exit criterion:

- type-correct higher categorical statement;
- explicit variance;
- explicit morphism levels;
- explicit world/presentation labels;
- no hidden replacement of exact liftability by weak admissibility.

### Proposed v5.18 — exact-liftability criterion

Relate semantic admissibility, exact presentation, and the obstruction classes from v4.00-v4.48.

Exit criterion: a theorem identifying a mathematically correct criterion for membership in the exact-universal image without contradicting the established countermodels.

### Proposed v5.19+ — higher mapping/classification theorem

Use the mature exact-universal package:

~~~text
strict realization
+ hom equivalences
+ ambient coverage
+ canonical section
+ unit/counit
+ ambient certificate
~~~

as the structural core.

Build factor existence and coherent uniqueness as separate theorem units before stating the final equivalence.

## 13. Proof-engineering rules retained

### Authority discipline

Always re-observe the fresh canonical SHA before theorem work.

Do not treat docs-only merges, runtime checks, cache hits, or conversation history as theorem authority.

### Namespace discipline

Importing a module does not open its namespaces.

With autoImplicit false, an unopened namespace produces an immediate unknown-identifier error.

### Universe discipline

For theorem-critical dependent structures, prefer concrete universe-instantiated field types when abbrev layers leave universe metavariables underdetermined.

This lesson was decisive in v5.15.

### Typeclass/elaboration discipline

Lean does not resolve a typeclass whose input type is still an unresolved metavariable.

Fix dependent endpoints first; then invoke category/bicategory lemmas.

### Fully-faithful preimage discipline

When preimage data lives in a dependent hom category, explicitly state the source and target 1-cells if inference is ambiguous.

### Equality discipline

- change only for definitional equality;
- use explicit Eq.trans / congrArg / congrArg₂ when the equality shape is known;
- avoid broad rw across dependent source/target expressions;
- avoid redundant simp steps after previous normalization has already removed the target.

### Bicategory discipline

- project complicated source equalities to the realized DO₂ layer;
- use faithful realization to reflect equalities back;
- normalize structural comparison cells before invoking bicategory coherence;
- keep source labels even when carriers agree.

### Quotient discipline

Representative choice may be computational.

Mathematical content must be representative-independent theorem-level data.

## 14. Validation and reproduction

Latest theorem target:

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationExactUniversalAmbientBiequivalenceCertificateV5_15
~~~

Validated exact head:

~~~text
7d222ead4eae477fefbb885e2883a505e49ea13c
Build completed successfully (8639 jobs)
return_code = 0
~~~

Current theorem-bearing main:

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

Aggregate and runtime entry points:

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
PYTHONPATH=. python3 runtime/kuuos_current_check.py
~~~

README/ROADMAP-only commits should not be treated as newer theorem-bearing baselines.
