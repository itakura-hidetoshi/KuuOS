# KuuOS / 空OS Roadmap

**Theorem snapshot: 2026-10-01 JST · integrated through v5.03**

**現在地：object-labelled exact-universal sector の Whitehead-style biequivalence は v4.89 で閉じている。ambient DO₂ への拡張は v4.90–v4.95 で restriction-hom EssSurj / StrongTrans extension coherence へ還元され、v4.96–v5.03 でその局所構成が大きく進んだ。現在の未解決点は「各 localized arrow に naturality iso が存在するか」ではなく、presentation / W-inverse / composition の canonical choice を localization relation と両立させ、quotient-independent な coherent global family として組み立てられるかである。**

This roadmap separates **integrated Lean theorems** from **proposed obligations**. Fresh exact theorem artifacts are authoritative; plans and historical conversation are not evidence that a theorem exists.

## 0. Reproducible theorem snapshot

| Role | Reference |
| --- | --- |
| Repository / canonical branch | `itakura-hidetoshi/KuuOS` / **main** |
| Fresh theorem-bearing baseline | **`3ff43ef5b268bff2852c9ad93bf6f79cf12dcea1`** |
| Latest theorem merge | [#1944 — StrongTrans presentation transport v5.03](https://github.com/itakura-hidetoshi/KuuOS/pull/1944) |
| Exact validated PR head | `86d0b52a07d92428c50f0eec5016d563665f887e` |
| Associated CI | [Run #3348 / 36851206349](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/36851206349): completed / success |
| Exact-head receipts | Strict Lean: success; exact-head terminal: success |
| Lean artifact | `11156825024` |
| Artifact digest | `sha256:9fc0ff932930f9e8702a267d9414e70b05287ed98a684e859329b97913e958fb` |
| Build | `Build completed successfully (8622 jobs)` |
| Lean | `leanprover/lean4:v4.30.0-rc2` |
| Mathlib | `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |

The latest theorem-bearing module is [v5.03](formal/KUOS/DependentOriginationExactUniversalAmbientStrongTransPresentationTransportV5_03.lean). Its public axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`; there is no `sorryAx`.

A later docs-only merge advances `main` but does not supersede this theorem-bearing baseline.

Authority order:

```text
fresh exact canonical GitHub SHA
  > formal Lean theorem artifacts at that SHA
  > README / ROADMAP
  > exact-head CI/runtime receipts
  > history / memory
```

**Protected lane:** [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) remains **open / draft / unmerged**, Lean 4.31 validation-only, and outside canonical theorem authority.

## 1. Long-range target

The long-range research target remains a higher dependent-origination mapping/classification property, schematically:

```text
eta : C -> DO(C,W,J,H)

AdmissibleContextualSystems(C,X)
  ≃
Fun(DO(C,W,J,H),X)
```

This is **not yet a theorem statement**. A final formulation must explicitly control:

- semantic admissibility versus exact presentation;
- localization and descent;
- source and target higher categories;
- allowed 1-cells and 2-cells;
- variance, world, and presentation labels;
- factor existence and coherent uniqueness;
- ambient object coverage;
- pseudonaturality under justified changes of context/presentation.

The exact-universal positive sector must never be conflated with a theorem that every weakly admissible raw system has an exact presentation.

## 2. Closed foundations — v4.00–v4.70

| Versions | Integrated result | Boundary retained |
| --- | --- | --- |
| v4.00–v4.12 | Exact C2 nonfactorization and nonzero Stage-II obstruction in `ZMod 2` | weak admissibility does not imply exact liftability |
| v4.13–v4.48 | Incidence/capacity obstruction theory; recursive and inverse-limit carriers; exact Cantor dimension; switch/orientation descent | concrete geometry is a stress test, not the general definition |
| v4.49 | Abstract presentation descent iff presentation invariance | presentation theorem, not final universality |
| v4.50–v4.56 | Exact higher presentation sector and coherent universal-target comparison/equivalence | exactness and universality are explicit hypotheses |
| v4.57–v4.60 | Compatible source objects/1-cells/2-cells and genuine hom categories | compatibility belongs to the typed source |
| v4.61–v4.68 | Whiskering, interchange, structural inverse laws, pentagon and triangle | higher coherence is explicit |
| v4.69–v4.70 | Native source `Bicategory` and strict DO₂ realization | strict realization ≠ strict source bicategory |

Positive-sector implications remain one-way:

```text
exact DO₂ presentation
  => higher stack-localization factorization
  => higher localization factorization
  => weak W-admissibility
```

The converse is false in general by the obstruction chain.

## 3. Local mapping and labelled global theory — v4.71–v4.89

### v4.71–v4.83 — local mapping theory

The local source theory establishes presentation-indexed liftability, compatible 2-cell full faithfulness, coherent inverse StrongTrans data, arbitrary DO₂ 1-cell lifting between existing chosen carriers, and hom-category equivalences.

Key endpoint:

```lean
(X ⟶ Y) ≌ (X.carrier ⟶ Y.carrier)
```

for existing exact-universal source objects.

**P1 is closed on the chosen exact-universal object sector.**

### v4.84–v4.89 — object-labelled Whitehead certificate

v4.84–v4.88 construct the section pseudofunctor, label-preserving realization, global source unit StrongTrans, and realized counit StrongTrans.

[v4.89](formal/KUOS/DependentOriginationExactUniversalLabelledBiequivalenceV4_89.lean) packages the Whitehead-style biequivalence certificate on the **object-labelled realized sector**.

Boundary retained: this does not yet cover arbitrary ambient DO₂ objects.

## 4. Ambient P4 reduction — v4.90–v4.95

### v4.90

Ambient Whitehead existence is equivalent to ambient object coverage:

```lean
ExactUniversalAmbientWhiteheadExistence
  ↔
ExactUniversalAmbientObjectCoverage
```

### v4.91–v4.92

Canonical restriction presentation universality is sufficient for coverage, and restriction hom-equivalence is sufficient for that universality.

### v4.93

Restriction is unconditionally Faithful.

### v4.94

Restriction is unconditionally Full, using Mathlib localization generation for modification naturality.

Therefore:

```lean
ExactUniversalAmbientRestrictionHomEquivalence
  ↔
ExactUniversalAmbientRestrictionHomEssSurj
```

### v4.95

Raw StrongTrans object components are canonically reconstructed on every localized object.

The remaining extension problem is packaged by:

```lean
HigherLocalizedStrongTransCoherenceExtension (W := W) gamma
```

and existence of that package implies restriction EssSurj.

The current ambient route remains:

```text
StrongTrans coherence extension
   -> restriction Hom EssSurj              [v4.95]
   <-> restriction Hom equivalence         [v4.94 + v4.93]
   -> canonical restriction universality   [v4.92]
   -> ambient object coverage              [v4.91]
   <-> ambient Whitehead existence         [v4.90]
```

Do not silently reverse the one-way implications.

## 5. StrongTrans extension construction — v4.96–v5.03

This is the active theorem chain.

### v4.96 — remove automatic 2-cell naturality

Because the source is:

```lean
LocallyDiscrete ((HigherLocalizedSite W)ᵒᵖ)
```

StrongTrans naturality with respect to source 2-cells is automatic for any chosen 1-cell naturality family.

The genuine remaining package is:

```lean
HigherLocalizedStrongTransOneCellCoherenceExtension
```

with four fields:

1. `naturality`
2. `naturality_id`
3. `naturality_comp`
4. `restrict_modification_naturality`

This is the real current P4 extension target.

### v4.97 — presentation generator

[v4.97](formal/KUOS/DependentOriginationExactUniversalAmbientStrongTransPresentationNaturalityV4_97.lean) constructs canonical naturality on presentation-image arrows by reusing `gamma.naturality`.

It also proves the exact raw-arrow restriction square required by v4.96.

### v4.98 — inverse generator

[v4.98](formal/KUOS/DependentOriginationExactUniversalAmbientStrongTransWInverseNaturalityV4_98.lean) constructs naturality on the inverse of any localized isomorphism by fully-faithful preimage.

Specialization gives canonical naturality on `Localization.Construction.wInv w hw`.

The theorem `higherLocalizedStrongTransNaturality_invOfIso_spec` records the crucial uniqueness/specification after whiskering by the forward equivalence.

### v4.99 — composition

[v4.99](formal/KUOS/DependentOriginationExactUniversalAmbientStrongTransCompositionNaturalityV4_99.lean) constructs the canonical StrongTrans composition naturality iso and proves closure of pointwise existence under composition.

The hom formula is the native seven-factor Mathlib formula.

### v5.00 — all-arrow existence

[v5.00](formal/KUOS/DependentOriginationExactUniversalAmbientStrongTransAllArrowNaturalityV5_00.lean) defines a `MorphismProperty` on `W.Localization` and applies:

```lean
Localization.Construction.morphismProperty_eq_top'
```

using:

- presentation-image case from v4.97;
- composition stability from v4.99;
- inverse stability from v4.98.

Result:

```text
every localized arrow has at least one StrongTrans naturality iso
```

**Critical boundary:** the result is `Nonempty`. It does not choose a coherent global family.

### v5.01 — canonical identity

[v5.01](formal/KUOS/DependentOriginationExactUniversalAmbientStrongTransIdentityNaturalityV5_01.lean) fixes identity naturality canonically using the native Mathlib formula:

```text
F.mapId
  -> left unitor
  -> right unitor^{-1}
  -> G.mapId^{-1}
```

and proves the exact v4.96 `naturality_id` equation.

### v5.02 — presentation id/comp coherence

[v5.02](formal/KUOS/DependentOriginationExactUniversalAmbientStrongTransPresentationCoherenceV5_02.lean) proves that v4.97 canonical presentation naturality satisfies the actual `StrongTrans.naturality_id` and `StrongTrans.naturality_comp` fields.

This supplies the raw-presentation cores corresponding to:

- `Localization.Construction.relations.id`
- `Localization.Construction.relations.comp`

### v5.03 — presentation transport bridge

[v5.03](formal/KUOS/DependentOriginationExactUniversalAmbientStrongTransPresentationTransportV5_03.lean) adds:

```lean
higherLocalizedStrongTransNaturalityTransport
```

for transporting a naturality iso backwards along a source 1-cell iso.

It also proves the exact restriction decompositions:

```text
restrict(F).mapId
  = F.map₂Iso(P.mapId) ≪≫ F.mapId

restrict(F).mapComp
  = F.map₂Iso(P.mapComp) ≪≫ F.mapComp
```

where:

```lean
P := (higherPresentationUnitFunctor W).toPseudofunctor
```

Finally, it defines:

- `higherLocalizedStrongTransPresentationIdentityTransport`
- `higherLocalizedStrongTransPresentationCompositionTransport`

which are the localized canonical identity/composition constructors transported back to the raw presentation image.

## 6. Immediate next theorem units

These are **proposed**, not yet theorem claims.

### v5.04 — identify presentation canonical choices with transported candidates

Prove:

```text
v4.97 presentation naturality on id
  =
v5.03 transported v5.01 identity naturality
```

and:

```text
v4.97 presentation naturality on f ≫ g
  =
v5.03 transported v4.99 composition naturality
```

This should use:

- v5.02 identity/composition StrongTrans coherence;
- v5.03 `restrict...mapId/mapComp_decomposition`;
- Mathlib `StrongTrans.naturality_naturality_iso` / hom form;
- the exact `Pseudofunctor.comp` mapId/mapComp definitions.

**Exit criterion:** the data-level cores of localization `relations.id` and `relations.comp` are closed for the canonical naturality assignment.

### v5.05 — close Winv₁ / Winv₂ compatibility

For a declared (W)-arrow `w`, prove that the canonical naturality choices on:

```text
Q(w) ≫ wInv(w)
wInv(w) ≫ Q(w)
```

reduce coherently to the canonical identity naturality.

The main tool should be v4.98:

```lean
higherLocalizedStrongTransNaturality_invOfIso_spec
```

together with the unit/counit equations of `Localization.Construction.wIso`.

Do not replace this by arbitrary `Nonempty` witnesses from v5.00.

**Exit criterion:** all four localization generators are compatible with the canonical naturality data:

```text
id
comp
Winv₁
Winv₂
```

### v5.06 — reuse v2.68 retained generated-relation syntax

Do not create a new relation language.

Existing v2.68 already provides:

```lean
LocalizationGenerating2Cell
GeneratedCompClosure2Cell
GeneratedLocalization2Cell
```

retaining the four localization generators, whiskering, `refl/symm/trans`, and erasure back to Mathlib's proposition-valued relations.

Use the v5.04/v5.05 generator compatibility theorems as the evaluator for this existing Type-valued syntax.

**Exit criterion:** canonical naturality evaluation is invariant under every retained generated localization relation.

### v5.07 — quotient-independent canonical naturality

Descend the generated relation invariance to the actual quotient localization.

Construct a **data-level** naturality family:

```lean
∀ f,
  F.map f ≫ app(target f) ≅
    app(source f) ≫ G.map f
```

that is independent of the selected path representative.

This is strictly stronger than v5.00's `Nonempty`.

### v5.08 — assemble v4.96

Use:

- quotient-independent naturality family from v5.07;
- v5.01 canonical identity;
- v4.99 canonical composition;
- v4.97 exact raw restriction square;
- v4.96 automatic 2-cell naturality.

Construct:

```lean
HigherLocalizedStrongTransOneCellCoherenceExtension (W := W) gamma
```

for every raw StrongTrans `gamma`.

Then v4.96 reconstructs the full v4.95 coherence-extension package.

### v5.09 — close current ambient P4 route

Once v5.08 is uniform:

```text
v5.08
  -> HigherLocalizedStrongTransExtensionExists
  -> restriction EssSurj               [v4.95]
  -> restriction Hom equivalence       [v4.94]
  -> restriction universality          [v4.92]
  -> ambient coverage                  [v4.91]
  -> ambient Whitehead existence       [v4.90]
```

At that point the current sufficient ambient P4 route is closed.

## 7. Relation machinery already available

The generated-relation infrastructure is not future work from zero.

[v2.68](formal/KUOS/DependentOriginationGeneratedLocalizationHolonomyV2_68.lean) already defines a Type-valued retained localization generator:

```lean
inductive LocalizationGenerating2Cell
  | id
  | comp
  | Winv₁
  | Winv₂
```

and lifts it through composition closure and equivalence closure.

This is preferable to proposition-only relation proofs when constructing quotient-independent **data**, because the exact generator and its parameters remain available for induction.

The v5.x task is to supply the StrongTrans naturality evaluator and prove the four generator compatibilities, not to reinvent the localization syntax.

## 8. Boundaries that must remain explicit

### v5.00 is not a coherent choice theorem

```text
∀ f, Nonempty (NaturalityIso f)
```

does not imply a family satisfying StrongTrans identity/composition coherence.

### Ordinary 1-categorical localization is insufficient by itself

`Localization.functorEquivalence` does not automatically produce the required pseudonatural StrongTrans extension in `Cat`.

### v4.95 remains conditional

v4.95 proves that a coherence-extension package gives EssSurj. It does not prove the package exists.

### Positive exact-universal results do not erase obstruction results

Weak (W)-admissibility alone still does not imply exact presentation in general.

## 9. Proof-engineering rules for the next stage

### Prefer structure fields when the goal is the field shape

For example:

```lean
gamma.naturality_id
gamma.naturality_comp
```

match the StrongTrans field equations directly.

The helper lemmas:

```lean
naturality_id_hom
naturality_comp_hom
```

instead expand the naturality iso hom and contain terminal inverse factors. They are useful for normal forms, but not interchangeable with the structure fields.

### Namespace discipline

`open scoped` exposes scoped syntax/notation, not ordinary declarations.

For example, `whiskerLeftIso` / `whiskerRightIso` live in `CategoryTheory.Bicategory`.

### Opposite-category discipline

The composition theorem is `CategoryTheory.op_comp`, not `Opposite.op_comp`.

A double opposite reverses composition twice, restoring the original order.

### Composite Iso homs

Do not rely on `rfl` for long `Iso.trans` chains. Prefer:

```lean
Iso.trans_hom
Iso.symm_hom
whiskerLeftIso_hom
whiskerRightIso_hom
```

### `change` is definitional only

Use it only when the target really unfolds definitionally. Otherwise use the normalization theorem or structure field that states the required equality.

### Preserve exact endpoint types

In bicategorical proofs, expose object and arrow endpoints before broad `simp`, `rw`, or coherence tactics.

## 10. Validation and reproduction

Latest theorem target:

```bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationExactUniversalAmbientStrongTransPresentationTransportV5_03
```

Validated exact head:

```text
86d0b52a07d92428c50f0eec5016d563665f887e
Build completed successfully (8622 jobs)
```

Current endpoint reproduction:

```bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationExactUniversalLabelledBiequivalenceV4_89 \
  KUOS.DependentOriginationExactUniversalAmbientRestrictionFullV4_94 \
  KUOS.DependentOriginationExactUniversalAmbientStrongTransLocallyDiscreteV4_96 \
  KUOS.DependentOriginationExactUniversalAmbientStrongTransAllArrowNaturalityV5_00 \
  KUOS.DependentOriginationExactUniversalAmbientStrongTransIdentityNaturalityV5_01 \
  KUOS.DependentOriginationExactUniversalAmbientStrongTransPresentationCoherenceV5_02 \
  KUOS.DependentOriginationExactUniversalAmbientStrongTransPresentationTransportV5_03
```

Aggregate and runtime entry points:

```bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
PYTHONPATH=. python3 runtime/kuuos_current_check.py
```

README/ROADMAP-only changes should not manually rerun an already successful Strict Lean theorem build. Docs-only merges are not theorem-bearing baselines.

## 11. Boundary at a glance

```text
CLOSED:
  obstruction / nonfactorization countermodels
  exact presentation and universal-target sector
  native source bicategory
  strict DO₂ realization
  local full faithfulness
  arbitrary DO₂ 1-cell lift between chosen carriers
  realization hom-category equivalences
  section pseudofunctor
  global unit/counit StrongTrans
  object-labelled Whitehead certificate
  ambient Whitehead iff object coverage
  restriction Faithful
  restriction Full
  hom-equivalence iff EssSurj
  canonical StrongTrans object components
  automatic source 2-cell naturality
  presentation-arrow naturality + restriction square
  W-inverse naturality
  composition closure
  all-arrow naturality existence
  canonical identity naturality
  presentation id/comp coherence
  presentation transport bridge

NEXT:
  v5.04 presentation canonical = transported canonical on id/comp
  v5.05 Winv₁/Winv₂ compatibility
  v5.06 generated-relation evaluator using existing v2.68 syntax
  v5.07 quotient-independent canonical naturality family
  v5.08 assemble v4.96 one-cell coherence extension
  v5.09 close restriction EssSurj / ambient P4 route

SEPARATE OPEN QUESTIONS:
  independently prescribed raw components/data
  semantic admissibility vs exact liftability
  final higher mapping/classification property

NOT VALID WITHOUT FURTHER PROOF:
  weak W-admissibility => exact presentation
  v5.00 => coherent all-arrow naturality family
  ordinary functor localization => StrongTrans localization
  v4.95 => unconditional EssSurj
  arbitrary ambient DO₂ object => represented by a source object
  current labelled Whitehead certificate => ambient Whitehead
  docs/runtime/cache success => theorem authority
```
