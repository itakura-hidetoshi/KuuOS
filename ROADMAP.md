# KuuOS / 空OS Roadmap

**Theorem snapshot: 2026-09-30 JST · integrated through v4.86**

**現在地：chosen exact-universal sector では P1 が閉じ、realization hom functor は各 hom category で同値。さらに inverse hom sections は object-labelled realized sector から source への pseudofunctor に統合され、label-preserving strict realization と source-roundtrip unit squares まで構成済み。**

次は v4.86 の unit squares を native StrongTrans / pseudonatural unit に組み上げ、realized-side roundtrip と合わせて object-labelled sector 上の global equivalence / biequivalence statement を閉じる。その後、全 DO₂ object coverage、独立 raw data、semantic admissibility、最終 higher mapping property を別々に扱う。

This roadmap separates **integrated Lean theorems** from **proposed obligations**. Exact theorem artifacts on fresh canonical GitHub state are authoritative; plans and historical conversation are not evidence that a theorem exists.

## 0. Reproducible theorem snapshot

| Role | Reference |
| --- | --- |
| Repository / canonical branch | `itakura-hidetoshi/KuuOS` / **main** |
| Observed main before this docs-only refresh | **`4d1c26388480e13398cd63faaa1f4323f58b4a8f`** |
| Latest theorem-bearing baseline | **`4d1c26388480e13398cd63faaa1f4323f58b4a8f`** |
| Latest theorem merge | [#1924 — global source-roundtrip unit squares v4.86](https://github.com/itakura-hidetoshi/KuuOS/pull/1924) |
| Exact validated PR head | `affd9b1633ca3d82bc55681f601735a2db07ceaa` |
| Associated CI | [Run #3272 / 36670438900](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/36670438900): completed / success |
| Exact-head receipts | Strict Lean: success; exact-head terminal: success |
| Lean artifact | `11078177476` |
| Artifact digest | `sha256:46863dbfd4043ce14adc2834f422e5ccee4354f29e8573e6cb71db0570f27278` |
| Build | `Build completed successfully (8605 jobs)` |
| Lean | `leanprover/lean4:v4.30.0-rc2` |
| Mathlib | `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |

The immutable current theorem artifact is [v4.86 at the theorem-bearing SHA](https://github.com/itakura-hidetoshi/KuuOS/blob/4d1c26388480e13398cd63faaa1f4323f58b4a8f/formal/KUOS/DependentOriginationExactUniversalGlobalUnitSquaresV4_86.lean). The selected build succeeded and the module's six axiom reports contain no `sorryAx`.

The observed-main SHA is the input to this documentation refresh. A later docs-only merge advances `main` but does not supersede the theorem-bearing baseline.

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

- admissibility and its relation to exact presentation;
- localization and stack descent;
- source and target higher categories;
- allowed 1-cells and 2-cells;
- variance / world / presentation labels;
- factor existence;
- coherent uniqueness;
- object coverage;
- pseudonaturality under justified changes of context and presentation.

The current exact-universal source already stores exact presentations and universal-target witnesses. Therefore success inside this sector must not be misreported as existence of exact presentations for every weakly admissible raw system.

## 2. Closed foundations — v4.00–v4.70

| Versions | Integrated result | Boundary retained |
| --- | --- | --- |
| v4.00–v4.12 | Exact octahedral C2 nonfactorization and nonzero Stage-II obstruction in `ZMod 2` | weak admissibility does not imply exact liftability |
| v4.13–v4.48 | Incidence/capacity obstruction theory; recursive and inverse-limit carriers; exact Cantor dimension; switch/orientation descent | concrete geometry is a stress test, not the general definition |
| v4.49 | Abstract presentation descent iff presentation invariance | presentation theorem, not final universality |
| v4.50–v4.56 | Exact higher presentation sector and coherent universal-target comparison/equivalence | exactness and universality are explicit hypotheses |
| v4.57–v4.60 | Compatible source objects/1-cells/2-cells and genuine hom categories | compatibility belongs to the typed source |
| v4.61–v4.68 | Whiskering, interchange, structural inverse laws, pentagon and triangle | higher coherence is proved explicitly |
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

## 3. Closed local mapping theory — v4.71–v4.79

### v4.71–v4.74 — liftability and equivalence-leg existence

[v4.72](formal/KUOS/DependentOriginationExactUniversalMorphismLiftabilityV4_72.lean) defines exact presentation-indexed raw liftability. Identities and composites are liftable; obstruction is its logical complement, not a generic decision algorithm.

[v4.73](formal/KUOS/DependentOriginationExactUniversalEquivalenceLegLiftabilityV4_73.lean) lifts the forward and backward raw legs of a coherent raw equivalence. [v4.74](formal/KUOS/DependentOriginationExactUniversalEquivalenceLegUniquenessV4_74.lean) gives DO₂ isomorphism between lifts of the same leg.

### v4.75–v4.77 — actual local full faithfulness

[v4.75](formal/KUOS/DependentOriginationExactUniversalCompatibleIsoV4_75.lean) classifies compatible source isomorphisms through the comma-style compatibility interface.

[v4.76](formal/KUOS/DependentOriginationExactUniversalRealizationFaithfulV4_76.lean) proves that a compatible source 2-cell is determined by its DO₂ component.

[v4.77](formal/KUOS/DependentOriginationExactUniversalRealizationFullyFaithfulV4_77.lean) constructs the unique compatible source preimage of every prescribed DO₂ 2-cell:

```lean
(f ⟶ g) ≃ (f.lift ⟶ g.lift)
```

for existing source 1-cells `f,g`.

This closes the 2-cell part. It did not yet produce source 1-cells above arbitrary DO₂ 1-cells.

### v4.78 — coherent raw equivalence gives a source adjoint equivalence

[v4.78](formal/KUOS/DependentOriginationExactUniversalSourceEquivalenceV4_78.lean) constructs a native source adjoint equivalence from coherent raw inverse data, preserving the prescribed raw forward/backward **1-cell legs**. Its raw unit/counit are not asserted equal to independently prescribed raw unit/counit.

### v4.79 — exact fixed-leg adjunction lifting

[v4.79](formal/KUOS/DependentOriginationExactUniversalAdjunctionLiftingV4_79.lean) proves, for fixed source legs:

```lean
Bicategory.Adjunction f g ≃ Bicategory.Adjunction f.lift g.lift
```

and preserves prescribed DO₂ unit/counit exactly. This is a classification of adjunction structures on existing source legs, not yet arbitrary 1-cell lifting.

## 4. P1 closed — v4.80–v4.83

P1 was:

> For fixed chosen exact-universal objects `X,Y`, lift arbitrary DO₂ 1-cells `ell : X.carrier ⟶ Y.carrier` to source 1-cells.

### v4.80 — conditional reduction to a coherent retraction

[v4.80 / #1918](formal/KUOS/DependentOriginationExactUniversalHomSectionV4_80.lean) proves that a coherent one-sided retraction of the presentation comparison is sufficient:

```text
c_X ; d_X ≅ 1
```

implies exact 1-cell lifting, a hom section, and a hom equivalence.

At this stage the retraction was additional input, so unconditional P1 was still open.

### v4.81 — inverse naturality squares from pointwise equivalences

[v4.81 / #1919](formal/KUOS/DependentOriginationPointwiseInverseNaturalityV4_81.lean) constructs the inverse component functors and naturality isomorphisms from only pointwise `IsEquivalence` proofs.

It proves exact unit-compatible recovery and uniqueness of the complete inverse naturality isomorphism, but does not yet prove identity/composition/two-cell coherence.

### v4.82 — pointwise inverse becomes a coherent StrongTrans

[v4.82 / #1920](formal/KUOS/DependentOriginationPointwiseInverseCoherenceV4_82.lean) proves:

- base two-cell naturality;
- identity coherence;
- composition coherence;
- actual inverse `StrongTrans`;
- invertible unit modification;
- existence of the coherent retraction required by v4.80.

No extra coherence assumption is added.

### v4.83 — exact-universal realization hom equivalence

[v4.83 / #1921](formal/KUOS/DependentOriginationExactUniversalHomEquivalenceV4_83.lean) applies v4.82 to each stored presentation comparison.

For every existing exact-universal pair `X,Y`:

```lean
∃ f : X ⟶ Y, f.lift = ell
```

for every `ell : X.carrier ⟶ Y.carrier`, and

```lean
(X ⟶ Y) ≌ (X.carrier ⟶ Y.carrier)
```

is a native Mathlib equivalence whose forward functor is the existing realization and whose inverse is the explicit section.

**Status: P1 is CLOSED on the chosen exact-universal object sector.**

This does not assert that every object of the ambient DO₂ belongs to the realized image of some source object.

## 5. Cross-hom/global assembly — v4.84–v4.86

Introduce:

```text
Source
  = ExactUniversalRawObject

RealizedSector
  = same object labels,
    DO₂ hom categories between their carriers
```

The labels are retained intentionally.

### v4.84 — section pseudofunctor

[v4.84 / #1922](formal/KUOS/DependentOriginationExactUniversalSectionPseudofunctorV4_84.lean) assembles the v4.83 inverse hom functors into:

```text
S : RealizedSector -> Source
```

as a native `Pseudofunctor`.

Closed coherence fields:

- map₂ identity;
- map₂ vertical composition;
- left whiskering;
- right whiskering;
- associator;
- left unitor;
- right unitor.

Identity/composition comparison isomorphisms realize to identities. `S` is not asserted strict.

### v4.85 — labelled strict realization

[v4.85 / #1923](formal/KUOS/DependentOriginationExactUniversalLabelledRealizationV4_85.lean) constructs:

```text
R : Source -> RealizedSector
```

as a native `StrictPseudofunctor`.

Objects preserve their labels; 1-cells and 2-cells are the wrappers of `f.lift` and `eta.lift`.

The realized-side cell recovery is exact:

```lean
R.obj (S.obj X) = X

R.map (S.map f) = f

R.map₂ (S.map₂ eta) = eta
```

and on each realized hom category:

```lean
S.mapFunctor X Y ⋙ R.mapFunctor X Y = 𝟭 (X ⟶ Y)
```

This is stronger than mere essential surjectivity locally. It is still not a global pseudonatural counit/equivalence by itself.

### v4.86 — source-roundtrip unit squares

[v4.86 / #1924](formal/KUOS/DependentOriginationExactUniversalGlobalUnitSquaresV4_86.lean) forms:

```text
Source --R--> RealizedSector --S--> Source
```

and the actual roundtrip pseudofunctor `S ∘ R`.

For each source 1-cell `f`:

```lean
f ≅ (S ∘ R).map f
```

is the existing v4.83 hom-unit component, and the pseudonaturality-shaped cell is:

```lean
f ≫ 𝟙 Y ≅ 𝟙 X ≫ (S ∘ R).map f
```

Under realization it is exactly:

```text
rho(f.lift) ; lambda(f.lift)^-1
```

with inverse:

```text
lambda(f.lift) ; rho(f.lift)^-1.
```

**Status: the component squares for the global source unit are CLOSED.  
The StrongTrans coherence built from those squares is NOT yet closed.**

## 6. Immediate next obligations

These are the next mathematical tasks, not preassigned theorem numbers.

### G1. Assemble the source-side global unit

Use v4.86's object components `𝟙 X` and naturality isomorphisms to construct the actual StrongTrans / pseudonatural transformation:

```text
Id_Source  ==>  S ∘ R
```

or the orientation selected by the native Mathlib interface.

Required proofs should include the full native StrongTrans fields:

- naturality with source 2-cells;
- identity coherence;
- composition coherence;
- agreement with the already verified v4.86 naturality cells.

Exit criterion: an actual bundled StrongTrans whose components and naturality squares are exactly the v4.86 data, plus invertibility if the chosen interface requires a pseudonatural isomorphism.

### G2. Package the realized-side roundtrip globally

v4.85 already proves exact object/1-cell/2-cell recovery for `R ∘ S` on the object-labelled realized sector.

Next determine the cleanest native formulation:

- equality of pseudofunctors, if the structural fields reduce sufficiently;
- otherwise a pseudonatural counit/isomorphism whose components are identities.

Exit criterion: a bundled global comparison, not merely per-hom functor equality.

### G3. Close the Source ↔ RealizedSector equivalence/biequivalence

Combine G1 and G2 and discharge the required triangle/coherence laws in the native Mathlib framework.

The target here is specifically the **object-labelled RealizedSector**. Do not silently replace it with all of DO₂.

Exit criterion: a precise native equivalence/biequivalence statement with the chosen unit/counit and their coherence recorded.

## 7. Separate obligations after labelled-sector closure

### P2. Independently prescribed raw 2-cell / adjunction data

Current full faithfulness lets a prescribed DO₂ 2-cell determine its unique compatible raw component. A stronger problem is to specify the raw component independently and prove compatibility, or identify the exact obstruction.

Required distinction:

```text
DO₂ component prescribed
  => unique compatible raw component        [closed]

DO₂ component + raw component both prescribed
  => compatibility must be proved           [open in general]
```

Do not infer the second from the first.

### P3. Semantic admissibility versus exact liftability

Define semantic admissibility independently of source-morphism existence, then prove an implication, equivalence under stronger hypotheses, or a counterexample.

Do not define admissibility as a tautological restatement of `Liftable`.

The earlier obstruction chain must remain visible: weak admissibility alone cannot imply exact presentation.

### P4. Ambient DO₂ object coverage

The current RealizedSector has the **same object labels as Source**. If the final theorem requires all ambient DO₂ objects, prove the necessary object-level essential surjectivity or specify a justified smaller target sector.

This is now separate from P1: 1-cell coverage between chosen objects is already closed.

### P5. Final higher mapping/classification property

Only after the target sector is fixed should the final universal property be stated.

Required ingredients include:

- exact/weak admissibility boundary;
- object coverage;
- hom equivalences;
- global unit/counit;
- naturality under changes of context/presentation;
- descent and variance/world labels;
- any required compatibility with operational bindings.

## 8. Proof-engineering lessons retained

### Local scope is not imported scope

Imports expose declarations but do not open namespaces or export local instances. Use explicit namespace openings or qualified theorem names where needed.

### `change` is definitional only

Use `change` only when the new target is definitionally equal. Normalize propositional structure using the actual theorem, e.g. `Iso.trans_inv`, projection lemmas, or typed `calc`.

### Fix dependent endpoints early

For `Bicategory.Adjunction`, `map_preimage`, `preimageIso`, and related dependent APIs, specify the ambient source objects and hom-category endpoints before asking Lean to elaborate dependent fields.

### Infer generated universe signatures through typed maps

Do not copy positional universe arguments from one declaration to another when generated signatures differ. Let typed object maps determine the codomain universe where possible.

### Distinguish dotted identifiers from field notation

When a local notation such as `S` is a term receiver, write `(S).map`, `(S).obj`, etc. if `S.map` would be parsed as a dotted identifier before notation expansion.

### Reflect coherence only after reducing wrappers

Use faithful realization to reflect source equalities after the realized side has been reduced to a small homogeneous diagram. Avoid asking broad `simp` to discover categories, functors, associators, and wrappers simultaneously.

These rules improve robustness. They are not reasons to add axioms, suppress warnings, broaden transparency, or increase heartbeat limits by default.

## 9. Validation and reproduction

Latest theorem command:

```bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationExactUniversalGlobalUnitSquaresV4_86
```

The v4.86 import path includes the v4.85 → v4.84 → v4.83 route and the v4.80/v4.82 P1 machinery behind v4.83.

The separate v4.78 source-equivalence theorem is not on that import path. To reproduce both current major branches:

```bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationExactUniversalSourceEquivalenceV4_78 \
  KUOS.DependentOriginationExactUniversalGlobalUnitSquaresV4_86
```

Aggregate and runtime entry points:

```bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
PYTHONPATH=. python3 runtime/kuuos_current_check.py
```

Cache success does not replace exact-head validation. Historical dependency warnings do not invalidate a new module merely because they replay in its dependency build.

**README/ROADMAP-only changes should not manually rerun an already successful Strict Lean theorem build.** Use the impact-selected documentation/runtime checks. The documentation commit is not a theorem-bearing baseline.

## 10. Current boundary at a glance

```text
CLOSED:
  obstruction / nonfactorization countermodels
  exact presentation and universal-target sector
  native source bicategory
  strict DO₂ realization
  local full faithfulness on 2-cells
  coherent raw-equivalence source equivalences
  exact fixed-leg adjunction lifting
  pointwise-equivalence -> coherent inverse StrongTrans/retraction
  arbitrary DO₂ 1-cell exact lift between chosen carriers
  realization hom-category equivalences
  cross-hom section pseudofunctor
  label-preserving strict realization
  exact realized-side object/1-cell/2-cell roundtrip
  source-roundtrip pseudofunctor
  canonical source global-unit naturality squares

NEXT:
  bundle v4.86 squares into the source global StrongTrans / unit
  bundle the realized-side global counit / roundtrip
  close Source <-> object-labelled RealizedSector equivalence/biequivalence

SEPARATE OPEN QUESTIONS:
  coverage of ambient DO₂ objects outside the labelled sector
  independently prescribed raw components/data
  semantic admissibility vs exact liftability
  final higher mapping/classification property

NOT VALID WITHOUT FURTHER PROOF:
  weak W-admissibility => exact presentation
  arbitrary ambient DO₂ object => represented by a chosen source object
  local hom equivalence => global biequivalence without unit/counit coherence
  DO₂ 2-cell lift => compatibility with an independently prescribed raw component
  docs/runtime/cache success => theorem authority
```
