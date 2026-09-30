# KuuOS / 空OS Roadmap

**Theorem snapshot: 2026-10-01 JST · integrated through v4.93**

**現在地：object-labelled exact-universal sector の Whitehead-style biequivalence は v4.89 で閉じた。ambient DO₂ への拡張は v4.90 で object coverage と同値まで還元され、v4.91–v4.93 の constructive route では restriction hom functor の Faithful が無条件に閉じ、残る本質的課題は Full と EssSurj の2つに分離された。**

This roadmap separates **integrated Lean theorems** from **proposed obligations**. Exact theorem artifacts on fresh canonical GitHub state are authoritative; plans and historical conversation are not evidence that a theorem exists.

## 0. Reproducible theorem snapshot

| Role | Reference |
| --- | --- |
| Repository / canonical branch | `itakura-hidetoshi/KuuOS` / **main** |
| Observed main before this docs-only refresh | **`6d4ef51705a71b25e167bc8a766fc6f43e89ef2e`** |
| Latest theorem-bearing baseline | **`6d4ef51705a71b25e167bc8a766fc6f43e89ef2e`** |
| Latest theorem merge | [#1932 — restriction faithfulness split v4.93](https://github.com/itakura-hidetoshi/KuuOS/pull/1932) |
| Exact validated PR head | `8be3321da513de1d2bd881ab9457e652b316b883` |
| Associated CI | [Run #3303 / 36783070351](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/36783070351): completed / success |
| Exact-head receipts | Strict Lean: success; exact-head terminal: success |
| Lean artifact | `11129581377` |
| Artifact digest | `sha256:42164e397ab008644d7d7749c03f74a0a0423c31246a33ea18a8cd5b55409520` |
| Build | `Build completed successfully (8612 jobs)` |
| Lean | `leanprover/lean4:v4.30.0-rc2` |
| Mathlib | `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |

The immutable current theorem artifact is [v4.93 at the theorem-bearing SHA](https://github.com/itakura-hidetoshi/KuuOS/blob/6d4ef51705a71b25e167bc8a766fc6f43e89ef2e/formal/KUOS/DependentOriginationExactUniversalAmbientRestrictionFaithfulSplitV4_93.lean). Its public axiom reports contain no `sorryAx`.

A later docs-only merge advances `main` but does not supersede this theorem-bearing baseline.

```text
fresh exact canonical GitHub SHA
  > formal Lean theorem artifacts at that SHA
  > README / ROADMAP
  > exact-head CI/runtime receipts
  > history / memory
```

**Protected lane:** [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) remains Lean 4.31 validation-only and outside canonical theorem authority. Keep it draft and unmerged.

## 1. Long-range target

The long-range research target remains a higher dependent-origination mapping/classification property. Schematic form:

```text
eta : C -> DO(C,W,J,H)

AdmissibleContextualSystems(C,X)
  ≃
Fun(DO(C,W,J,H),X)
```

This is **not yet a theorem statement**. A final formulation must make explicit:

- semantic admissibility and its relation to exact presentation;
- localization and stack descent;
- source and target higher categories;
- allowed 1-cells and 2-cells;
- variance, world, and presentation labels;
- factor existence;
- coherent uniqueness;
- ambient object coverage;
- pseudonaturality under justified changes of context/presentation.

The current exact-universal source stores exact presentations and universal-target witnesses. Success inside that sector must never be reported as existence of exact presentations for every weakly admissible raw system.

## 2. Closed foundations — v4.00–v4.70

| Versions | Integrated result | Boundary retained |
| --- | --- | --- |
| v4.00–v4.12 | Exact octahedral C2 nonfactorization and nonzero Stage-II obstruction in `ZMod 2` | weak admissibility does not imply exact liftability |
| v4.13–v4.48 | Incidence/capacity obstruction theory; recursive/inverse-limit carriers; exact Cantor dimension; switch/orientation descent | concrete geometry is a stress test, not the general definition |
| v4.49 | Abstract presentation descent iff presentation invariance | presentation theorem, not final universality |
| v4.50–v4.56 | Exact higher presentation sector and coherent universal-target comparison/equivalence | exactness and universality are explicit hypotheses |
| v4.57–v4.60 | Compatible source objects/1-cells/2-cells and genuine hom categories | compatibility belongs to the typed source |
| v4.61–v4.68 | Whiskering, interchange, structural inverse laws, pentagon and triangle | higher coherence is explicit |
| v4.69–v4.70 | Native source `Bicategory` and strict DO₂ realization | strict realization ≠ strict source bicategory |

Formal anchors: [v4.00](formal/KUOS/DependentOriginationAbstractNonfactorizationV4_00.lean), [v4.12](formal/KUOS/DependentOriginationStageIIObstructionClassV4_12.lean), [v4.49](formal/KUOS/DependentOriginationAbstractPresentationDescentV4_49.lean), [v4.56](formal/KUOS/DependentOriginationExactUniversalTargetDO2EquivalenceV4_56.lean), [v4.69](formal/KUOS/DependentOriginationExactUniversalMappingBicategoryV4_69.lean), [v4.70](formal/KUOS/DependentOriginationExactUniversalRealizationStrictPseudofunctorV4_70.lean).

The exact positive-sector implications remain one-way:

```text
exact DO₂ presentation
  => higher stack-localization factorization
  => higher localization factorization
  => weak W-admissibility
```

The converse is false in general by the earlier obstruction chain.

## 3. Local mapping theory closed — v4.71–v4.83

### v4.71–v4.79

The local source theory establishes presentation-indexed liftability, compatible 2-cell full faithfulness, source equivalences from coherent raw equivalences, and exact adjunction lifting on fixed source legs.

Key endpoints:

- [v4.77](formal/KUOS/DependentOriginationExactUniversalRealizationFullyFaithfulV4_77.lean):
  ```lean
  (f ⟶ g) ≃ (f.lift ⟶ g.lift)
  ```
  for existing source 1-cells;
- [v4.79](formal/KUOS/DependentOriginationExactUniversalAdjunctionLiftingV4_79.lean):
  ```lean
  Bicategory.Adjunction f g ≃ Bicategory.Adjunction f.lift g.lift
  ```
  for fixed source legs.

### v4.80–v4.83 — P1 closed

v4.80 reduces arbitrary DO₂ 1-cell lifting to a coherent retraction of the presentation comparison.

v4.81–v4.82 construct that coherent inverse StrongTrans/retraction from the already-stored pointwise equivalence data.

[v4.83](formal/KUOS/DependentOriginationExactUniversalHomEquivalenceV4_83.lean) therefore proves, for every existing exact-universal pair `X,Y`:

```lean
∃ f : X ⟶ Y, f.lift = ell
```

for every `ell : X.carrier ⟶ Y.carrier`, and packages the actual realization hom functor as an equivalence:

```lean
(X ⟶ Y) ≌ (X.carrier ⟶ Y.carrier)
```

**P1 status: CLOSED on the chosen exact-universal object sector.**

## 4. Object-labelled global biequivalence closed — v4.84–v4.89

Define:

```text
Source
  = chosen exact-universal source objects and compatible cells

RealizedSector
  = the same object labels,
    with DO₂ hom categories between the labelled carriers
```

The labels are intentionally retained.

### v4.84–v4.85

[v4.84](formal/KUOS/DependentOriginationExactUniversalSectionPseudofunctorV4_84.lean) assembles the v4.83 inverse hom sections into a native section pseudofunctor

```text
S : RealizedSector -> Source.
```

[v4.85](formal/KUOS/DependentOriginationExactUniversalLabelledRealizationV4_85.lean) gives the converse label-preserving strict realization

```text
R : Source -> RealizedSector.
```

Realized-side object/1-cell/2-cell recovery is exact.

### v4.86

[v4.86](formal/KUOS/DependentOriginationExactUniversalGlobalUnitSquaresV4_86.lean) constructs source-roundtrip unit squares.

At v4.86 these were components, not yet a bundled StrongTrans.

### v4.87 — bundled source unit

[v4.87 / #1926](formal/KUOS/DependentOriginationExactUniversalGlobalUnitStrongTransV4_87.lean) closes the full native StrongTrans:

```text
Id_Source ⟶ S ∘ R.
```

The proof projects structural equations to DO₂, reduces them to native bicategory coherence, then reflects equality back using realization faithfulness.

### v4.88 — bundled realized counit

[v4.88 / #1927](formal/KUOS/DependentOriginationExactUniversalGlobalCounitStrongTransV4_88.lean) constructs:

```text
R ∘ S ⟶ Id_RealizedSector.
```

### v4.89 — Whitehead certificate

[v4.89 / #1928](formal/KUOS/DependentOriginationExactUniversalLabelledBiequivalenceV4_89.lean) packages:

- the actual labelled realization pseudofunctor;
- an equivalence on every hom category;
- exact equality of each equivalence's forward functor with realization;
- object essential surjectivity inside the labelled sector;
- the chosen section, unit, and counit.

Because Source and RealizedSector have identical object labels, object essential surjectivity there is reflexive.

**Status: the object-labelled Whitehead-style biequivalence certificate is CLOSED.**

Boundary retained: this is not yet a claim about all ambient DO₂ objects, and no stronger adjoint-biequivalence package with triangle modifications is asserted.

## 5. Ambient P4 reduction — v4.90–v4.93

P4 is the question of extending from the labelled sector to **all ambient DO₂ objects**.

### v4.90 — ambient Whitehead exactly equals object coverage

[v4.90 / #1929](formal/KUOS/DependentOriginationExactUniversalAmbientCoverageReductionV4_90.lean) proves:

```lean
ExactUniversalAmbientWhiteheadExistence
  ↔
ExactUniversalAmbientObjectCoverage
```

for the actual v4.70 realization.

Local hom equivalence is no longer the ambient issue; object coverage is.

### v4.91 — restriction universality gives literal carrier coverage

[v4.91 / #1930](formal/KUOS/DependentOriginationExactUniversalAmbientRestrictionUniversalityV4_91.lean) takes an arbitrary ambient `Z` and constructs the tautological presentation of its raw restriction:

```text
raw      = restrict(Z)
carrier  = Z
compare  = identity
```

The identity comparison is automatically pointwise an equivalence.

The only non-tautological field is coherent universality. If the tautological presentation is universally terminal among exact presentations of the same raw restriction, then the constructed source object has carrier **literally equal to Z**, hence coverage.

This is a sufficient condition, not an unconditional theorem.

### v4.92 — universality from local restriction hom equivalence

[v4.92 / #1931](formal/KUOS/DependentOriginationExactUniversalAmbientRestrictionHomEquivalenceV4_92.lean) defines restriction as a genuine functor between StrongTrans hom categories.

If that restriction functor is an equivalence for every relevant pair:

- EssSurj lifts comparison StrongTrans and gives factor existence;
- Full + Faithful lift isomorphisms and give essential uniqueness.

Hence the v4.91 tautological presentation is universal.

### v4.93 — Faithful removed from the frontier

[v4.93 / #1932](formal/KUOS/DependentOriginationExactUniversalAmbientRestrictionFaithfulSplitV4_93.lean) proves object-surjectivity of the presentation unit from Mathlib's constructed localization:

```lean
Context ≃ W.Localization
```

and uses modification extensionality to prove restriction is faithful on every StrongTrans hom category.

It then proves the exact split:

```lean
ExactUniversalAmbientRestrictionHomEquivalence
  ↔
ExactUniversalAmbientRestrictionHomFull
    ∧ ExactUniversalAmbientRestrictionHomEssSurj
```

Thus the current constructive route is:

```text
Full + EssSurj
   ⇔ restriction Hom equivalence          [v4.93]
   ⇒ canonical restriction universality   [v4.92]
   ⇒ ambient object coverage              [v4.91]
   ⇔ ambient Whitehead existence          [v4.90]
```

Only the first equivalence and final equivalence above are proved equivalences. The middle arrows are sufficient implications. Do not silently reverse them.

## 6. Immediate next obligations

These are proposed theorem units, not preassigned theorem numbers.

### A. Restriction Full — first target

Goal:

> Every raw modification between restrictions of localized StrongTrans has a localized modification preimage.

The likely proof route should exploit Mathlib localization generation rather than manually recurse over quotient paths.

Candidate steps:

1. take `Γ : restrict(alpha) ⟶ restrict(beta)`;
2. define candidate component 2-cells on localized objects using the canonical object equivalence;
3. define the property “candidate components satisfy modification naturality along `f`” as a morphism property on the localized base category;
4. prove the property for the image of every raw context arrow using `Γ.naturality`;
5. prove stability under composition;
6. prove stability under inverses of inverted `W` arrows;
7. use `Localization.Construction.morphismProperty_eq_top` or `morphismProperty_eq_top'`;
8. assemble the genuine localized modification;
9. prove restriction recovers `Γ`.

Exit criterion:

```lean
(higherLocalizedRestrictionHomFunctor ...).Full
```

without a new semantic axiom.

### B. Restriction EssSurj — second target

Goal:

> Every raw StrongTrans between restricted localized pseudofunctors is isomorphic to the restriction of some localized StrongTrans.

This is the genuinely 1-cell/pseudonatural extension problem.

Likely required ingredients:

- object-component reconstruction;
- extension of naturality isomorphisms from raw arrows to localized arrows;
- identity coherence;
- composition coherence;
- compatibility with inverse images of `W`;
- an isomorphism after restriction, not necessarily definitional equality.

Ordinary 1-categorical `Localization.functorEquivalence` is useful background but does not by itself prove this pseudonatural StrongTrans statement.

Exit criterion:

```lean
(higherLocalizedRestrictionHomFunctor ...).EssSurj
```

for the ambient stack carriers required by v4.93.

### C. Close the current P4 route

Once A and B are closed:

```text
Full + EssSurj
  -> restriction Hom equivalence
  -> canonical restriction universality
  -> literal ambient carrier coverage
  -> ambient Whitehead existence.
```

At that point the actual v4.70 realization would have ambient Whitehead data for all DO₂ objects through the current route.

## 7. Separate obligations after P4

### P2. Independently prescribed raw 2-cell / adjunction data

Current full faithfulness says:

```text
DO₂ component prescribed
  => unique compatible raw component.
```

A stronger problem remains:

```text
DO₂ component + raw component independently prescribed
  => compatibility must be proved.
```

Do not infer the second from the first.

### P3. Semantic admissibility versus exact liftability

Define semantic admissibility independently of source-morphism existence, then prove an implication, an equivalence under stronger hypotheses, or an obstruction.

Do not define admissibility as a tautological restatement of `Liftable`.

The earlier nonfactorization theorem must remain visible: weak admissibility alone cannot imply exact presentation in general.

### P5. Final higher mapping/classification property

Only after the ambient target sector is settled should the final universal property be frozen.

Required ingredients include:

- admissibility/exactness boundary;
- ambient object coverage;
- hom equivalences;
- global unit/counit or the selected Whitehead interface;
- naturality under context/presentation change;
- descent;
- variance and world/presentation labels;
- operational binding compatibility if it is part of the mathematical statement.

## 8. Proof-engineering lessons retained

### Imported declarations do not import open namespaces

Open or qualify the declaration's namespace explicitly.

### `change` is definitional only

If the target is merely propositionally equal, use the actual normalization theorem rather than forcing `change`.

### Fix generated universes explicitly when needed

The v4.90–v4.93 ambient types include a target-category universe that can occur only inside a proposition body. At public call sites, explicit applications such as

```lean
.{u, v, uH, vH}
```

avoid fresh unconstrained universe metavariables.

### Higher-order structure fields have multiple binder layers

Pinned Mathlib defines:

```lean
Functor.Faithful.map_injective :
  ∀ {X Y}, Function.Injective F.map
```

Therefore a structure proof should distinguish:

1. the hom-category objects `X,Y`;
2. the two morphisms being compared;
3. their mapped equality.

For v4.93 the robust form is schematically:

```lean
map_injective {alpha beta} := by
  intro eta theta h
  ...
```

not a binder form that accidentally treats `eta/theta` as `alpha/beta`.

### Do not solve a goal twice

If `rw` closes the goal by definitional reduction, a following `rfl` produces `No goals to be solved`.

### Reduce wrappers before extensionality/coherence

Use the concrete component theorem for restriction, then `Pseudofunctor.StrongTrans.homCategory.ext`. Avoid asking broad simplification to reconstruct all endpoints at once.

## 9. Validation and reproduction

Latest theorem command:

```bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationExactUniversalAmbientRestrictionFaithfulSplitV4_93
```

The exact validated head completed with:

```text
Build completed successfully (8612 jobs)
return_code = 0
```

Reproduce the two current major endpoints with:

```bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationExactUniversalLabelledBiequivalenceV4_89 \
  KUOS.DependentOriginationExactUniversalAmbientRestrictionFaithfulSplitV4_93
```

Aggregate and runtime entry points:

```bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
PYTHONPATH=. python3 runtime/kuuos_current_check.py
```

Cache success does not replace exact-head validation. Historical dependency warnings do not invalidate a new module merely because they replay in its dependency build.

**README/ROADMAP-only changes should not manually rerun an already successful Strict Lean theorem build.** Use impact-selected documentation/governance checks. A docs-only merge is not a theorem-bearing baseline.

## 10. Boundary at a glance

```text
CLOSED:
  obstruction / nonfactorization countermodels
  exact presentation and universal-target sector
  native source bicategory
  strict DO₂ realization
  local full faithfulness on source 2-cells
  arbitrary DO₂ 1-cell lift between chosen carriers
  realization hom-category equivalences
  cross-hom section pseudofunctor
  label-preserving strict realization
  global source unit StrongTrans
  global realized counit StrongTrans
  object-labelled Whitehead-style biequivalence certificate
  ambient Whitehead existence iff ambient object coverage
  restriction-universality sufficient route to coverage
  restriction hom-equivalence sufficient route to universality
  unconditional restriction faithfulness
  restriction hom-equivalence iff Full + EssSurj

NEXT:
  prove restriction Full
  prove restriction EssSurj
  close the current route to ambient object coverage
  obtain ambient Whitehead existence via v4.90

SEPARATE OPEN QUESTIONS:
  independently prescribed raw components/data
  semantic admissibility vs exact liftability
  final higher mapping/classification property

NOT VALID WITHOUT FURTHER PROOF:
  weak W-admissibility => exact presentation
  arbitrary ambient DO₂ object => represented by a source object
  restriction Faithful => restriction Full
  restriction Full => restriction EssSurj
  ordinary functor localization => pseudonatural StrongTrans localization
  docs/runtime/cache success => theorem authority
```
