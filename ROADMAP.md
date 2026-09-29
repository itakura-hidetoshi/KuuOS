# KuuOS / 空OS Roadmap

**Theorem snapshot: 2026-09-29 JST · integrated through v4.79**

**現在地：局所充満忠実性・source 随伴同値・固定した１射対の随伴構造の対応まで統合済み。** 次は、任意の１射の持ち上げと、独立に指定された raw データの保持を分けて扱い、最終的な高次写像性へ接続する。

This roadmap separates integrated Lean results from proposed obligations. [README](README.md) gives the overview. Exact canonical source is authoritative; historical plans are not evidence that a theorem exists.

## 0. Reproducible theorem snapshot

| Role | Reference |
| --- | --- |
| Repository / canonical branch | `itakura-hidetoshi/KuuOS` / **main** |
| Observed main before this docs-only refresh | `b239068dbcfaf8d3e0bce101e7402f9cede34c9f` |
| Latest theorem-bearing baseline | **`b239068dbcfaf8d3e0bce101e7402f9cede34c9f`** |
| Latest theorem merge | [#1916 — adjunction lifting v4.79](https://github.com/itakura-hidetoshi/KuuOS/pull/1916) |
| Exact validated PR head | `e470e1269715582b9f8a0746aa213a0447132d79` |
| Tested synthetic merge checkout | `617d8fb2667324d3f078a609175da77d4ab05f4d` |
| Associated CI | [#3250 / 36563945324](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/36563945324), attempt 1: success |
| Exact-head receipts | `chatgpt-ci-receipt/KuuOS Strict Lean formal validation`: success; `chatgpt-ci-receipt/KuuOS exact-head terminal`: success |
| Lean | `leanprover/lean4:v4.30.0-rc2` |
| Mathlib | `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |

The downloaded Lean artifact `11031183566` has verified SHA-256 `36873a6e3763268445b46832789c92e8a235164d615f325cc58777cc2ce9dbe2`. Its receipt reports return code 0. The v4.79 module contains 15 regression examples and seven axiom reports, all limited to `propext`, `Classical.choice`, and `Quot.sound`, without `sorryAx`.

The [immutable v4.79 artifact](https://github.com/itakura-hidetoshi/KuuOS/blob/b239068dbcfaf8d3e0bce101e7402f9cede34c9f/formal/KUOS/DependentOriginationExactUniversalAdjunctionLiftingV4_79.lean) specifies the statement. The observed-main row records the input to this documentation refresh; its eventual docs-only merge is not a new theorem-bearing baseline.

```text
fresh exact canonical GitHub SHA
  > formal Lean theorem artifacts at that SHA
  > README / ROADMAP
  > exact-head CI/runtime receipts
  > history / memory
```

**Protected lane:** [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) is Lean 4.31 validation-only, outside canonical theorem authority. Keep it draft and unmerged; do not mark Ready for review, enable auto-merge, or change the canonical pins through it.

## 1. Long-range target and chosen sector

The target remains a higher dependent-origination mapping/classification property. This is a schematic research objective, **not an existing theorem or a finalized functor-category choice**:

```text
eta : C -> DO(C,W,J,H)

AdmissibleContextualSystems(C,X)
  ≃
Fun(DO(C,W,J,H),X)
```

A final theorem must specify admissibility, localization and stack descent, higher variance, the target sector, compatible 1-cells and 2-cells, factor existence, coherent uniqueness, and naturality. The present source **already stores** exact presentations and universal-target witnesses; it does not construct them for every weakly admissible raw system.

In particular, local full faithfulness concerns the maps on 2-cells in each hom category. It does not by itself give essential surjectivity on 1-cells, essential surjectivity on objects, or a global biequivalence.

## 2. Closed foundations — v4.00–v4.70

| Versions | Integrated result | Scope retained |
| --- | --- | --- |
| v4.00–v4.12 | Exact nonfactorization in the octahedral C2 countermodel; `omega(T) = 1` in `ZMod 2` for every coherent quotient transport | Weak admissibility, coherent quotient transport, and quotient coboundary solvability do not imply comparison liftability |
| v4.13–v4.48 | Incidence/capacity obstructions; recursive and inverse-limit carriers; exact Cantor dimension `log 2 / log 3`; middle-switch and orbit/orientation descent | Concrete geometry is a stress test, not the general definition |
| v4.49 | Presentation quotient factorization iff invariance; nonfactorization iff presentation-descent obstruction | Abstract presentation theorem, not final higher universality |
| v4.50–v4.56 | Exact Cat-valued sector; comparison hierarchy; conditional coherent universal targets; mutual uniqueness; raw-equivalence transport; DO₂ adjoint equivalence of universal targets | Exactness and universality are explicit hypotheses |
| v4.57–v4.60 | Mapping-compatible source objects/1-cells/2-cells; vertical structure; genuine hom categories and projection functors | Compatibility is part of the 2-cell type |
| v4.61–v4.68 | Restriction/whiskering compatibility; horizontal interchange; structural inverses; pentagon and triangle | Coherence is proved, not inferred from graph structure |
| v4.69–v4.70 | Native source `Bicategory` and strict DO₂ realization | Strict pseudofunctor does not mean a strict source bicategory |

Formal entry points: [v4.00](formal/KUOS/DependentOriginationAbstractNonfactorizationV4_00.lean), [v4.12](formal/KUOS/DependentOriginationStageIIObstructionClassV4_12.lean), [v4.40](formal/KUOS/DependentOriginationStageIIExactFractalCertificateV4_40.lean), [v4.48](formal/KUOS/DependentOriginationStageIIOrbitOrientationDescentV4_48.lean), [v4.49](formal/KUOS/DependentOriginationAbstractPresentationDescentV4_49.lean), [v4.50](formal/KUOS/DependentOriginationExactHigherPresentationSectorV4_50.lean), [v4.56](formal/KUOS/DependentOriginationExactUniversalTargetDO2EquivalenceV4_56.lean), [v4.60](formal/KUOS/DependentOriginationExactUniversalMappingHomCategoryV4_60.lean), [v4.69](formal/KUOS/DependentOriginationExactUniversalMappingBicategoryV4_69.lean), [v4.70](formal/KUOS/DependentOriginationExactUniversalRealizationStrictPseudofunctorV4_70.lean).

The exact positive-sector implications remain:

```text
exact DO₂ presentation
  => higher stack-localization factorization
  => higher localization factorization
  => weak W-admissibility
```

The converse from weak admissibility is false in general. No later positive-sector theorem removes that counterexample.

## 3. Closed raw-leg lifting — v4.71–v4.74

[v4.71](formal/KUOS/DependentOriginationExactUniversalRealizationRawEquivalenceV4_71.lean) gives equivalence of the realized carriers under coherent raw equivalence. [v4.72](formal/KUOS/DependentOriginationExactUniversalMorphismLiftabilityV4_72.lean) defines, for fixed chosen source objects:

```text
Liftable_(X,Y)(r)
  := exists lift : X.carrier -> Y.carrier,
       Nonempty (restrict(lift) ; c_Y ≅ c_X ; r)

Liftable_(X,Y)(r) <-> exists source 1-cell f, f.raw = r
Obstructed_(X,Y)(r) := not Liftable_(X,Y)(r)
```

Identities and composites are liftable. `Obstructed` names the exact logical complement; it is not a general decision procedure or a new computable cohomology detector.

[v4.73](formal/KUOS/DependentOriginationExactUniversalEquivalenceLegLiftabilityV4_73.lean) transports the source presentation along coherent raw equivalence and uses the target's factor field to lift both prescribed raw legs. [v4.74](formal/KUOS/DependentOriginationExactUniversalEquivalenceLegUniquenessV4_74.lean) gives `Nonempty (f.lift ≅ g.lift)` for two source lifts of the same equivalence leg.

Historically, v4.74 alone did not supply compatible source 2-isomorphisms. **v4.77 now supplies source isomorphism lifting when the raw component is allowed to be determined by compatibility.** Uniqueness of the DO₂ isomorphism itself and equality with an independently prescribed raw identity are different claims.

## 4. Closed local classification — v4.75–v4.77

For existing source 1-cells `f`, `g : X ⟶ Y`, write `s_f`, `s_g` for their comparison squares. The source compatibility equation is:

```text
(restrict(ell.hom) ▷ c_Y) ; s_g.hom
  = s_f.hom ; (c_X ◁ r)
```

### v4.75 / #1912 — compatible isomorphism classification

File: [CompatibleIsoV4_75](formal/KUOS/DependentOriginationExactUniversalCompatibleIsoV4_75.lean).

The comparison functors give a full and faithful embedding of the source hom category in Mathlib `Comma`. `Comma.isoMk` derives inverse compatibility from the forward square. `exactUniversalSourceIsoEquivCompatibleComponents` classifies source isomorphisms by compatible raw/DO₂ isomorphism pairs; `exactUniversalTwoCell_isIso_iff` detects invertibility jointly on both components.

This result concerns the **comma embedding**, not yet the DO₂ projection on its own.

### v4.76 / #1913 — faithfulness of the actual DO₂ projection

File: [RealizationFaithfulV4_76](formal/KUOS/DependentOriginationExactUniversalRealizationFaithfulV4_76.lean).

The presentation comparison is pointwise an equivalence. Its precomposition functor is faithful, so the compatibility equations recover equality of raw components from equality of lift components:

```lean
eta = theta ↔ eta.lift = theta.lift
```

The installed `Faithful` instance belongs to `exactUniversalCompletion2HomFunctor` itself.

### v4.77 / #1914 — fullness and unique compatible preimages

File: [RealizationFullyFaithfulV4_77](formal/KUOS/DependentOriginationExactUniversalRealizationFullyFaithfulV4_77.lean).

A general Cat-valued pseudofunctor lemma constructs modification preimages under left whiskering by a pointwise equivalence. The KuuOS construction applies it to the conjugated square

```text
s_f.inv ; (restrict(ell.hom) ▷ c_Y) ; s_g.hom
```

and proves compatibility. Installed APIs include:

```text
exactUniversalCompletion2Preimage
exactUniversalCompletion2HomFunctor_full
exactUniversalCompletion2HomFullyFaithful
exactUniversalTwoCellEquivLift
existsUnique_exactUniversalTwoCell_of_lift
exactUniversalSourceIsoOfLift
```

Consequently `(f ⟶ g) ≃ (f.lift ⟶ g.lift)`, and every prescribed lift 2-cell has one and only one compatible source 2-cell. `preimageIso` lifts every DO₂ isomorphism between existing source 1-cells. No independent raw component or additional fullness hypothesis is required.

**Closed:** compatible lifting with the DO₂ 2-cell prescribed and the raw component constructed. **Separate:** lifting while independently prescribing raw data, or producing a source 1-cell over an arbitrary DO₂ 1-cell.

## 5. Closed source equivalences — v4.78 / #1915

File: [SourceEquivalenceV4_78](formal/KUOS/DependentOriginationExactUniversalSourceEquivalenceV4_78.lean).

`exactUniversalEndomorphism_iso_id_of_rawIso` turns `h.raw ≅ 𝟙 X.raw` into `Nonempty (h ≅ 𝟙 X)` using a coherent endocomparison, universal-target essential uniqueness, and v4.77. Applying it to both composites of chosen source legs constructs source unit/counit. Mathlib `Equivalence.mkOfAdjointifyCounit` supplies the triangle laws.

The main theorem is:

```lean
-- E : HigherRawSystemCoherentEquivalence X.raw Y.raw
∃ e : Bicategory.Equivalence X Y,
  e.hom.raw = E.forward.comparison ∧
  e.inv.raw = E.backward.comparison
```

This is a source adjoint equivalence, not merely a pair of opposite arrows or an equivalence of realized carriers. Both raw 1-cell legs are preserved. Its raw unit/counit are **not** asserted to be the prescribed `E.unit`/`E.counit`: essential uniqueness does not select them, and adjointification changes the chosen source counit.

## 6. Closed prescribed DO₂ adjunction lifting — v4.79 / #1916

File: [AdjunctionLiftingV4_79](formal/KUOS/DependentOriginationExactUniversalAdjunctionLiftingV4_79.lean).

For fixed source legs `f : X ⟶ Y` and `g : Y ⟶ X`:

```lean
Bicategory.Adjunction f g ≃ Bicategory.Adjunction f.lift g.lift
```

The construction preserves left/right zigzags and reflects both triangle laws independently. The preimages of the specified DO₂ unit and counit provide a source adjunction without assuming either cell invertible. `Bicategory.Adjunction.ext` and local faithfulness prove both round trips and uniqueness:

```lean
-- adj : Bicategory.Adjunction f.lift g.lift
∃! a : Bicategory.Adjunction f g,
  a.unit.lift = adj.unit ∧ a.counit.lift = adj.counit
```

For invertible DO₂ data already satisfying the left triangle, `exactUniversalEquivalenceOfLiftTriangle` constructs a native source equivalence without adjointification. The source legs, realized unit/counit isomorphisms, and their inverses are retained exactly. The native structure also supplies the right triangle.

Key APIs:

```text
exactUniversal_leftTriangle_iff_lift
exactUniversal_rightTriangle_iff_lift
exactUniversalAdjunctionToLift / exactUniversalAdjunctionOfLift
exactUniversalAdjunctionEquivLift
existsUnique_exactUniversalAdjunction_of_lift
exactUniversalAdjunction_nonempty_iff_lift
exactUniversalEquivalenceOfLiftTriangle
exactUniversalEquivalenceOfLiftTriangle_unit_lift
exactUniversalEquivalenceOfLiftTriangle_counit_lift
```

Do not conflate the two completed routes: v4.78 starts with raw coherent inverse data and establishes source-equivalence existence; v4.79 starts with a DO₂ adjunction on **existing source legs** and preserves its DO₂ components exactly. Neither theorem identifies those components with separately prescribed raw unit/counit.

## 7. Next obligations — proposed, not integrated

These are mathematical targets, not preassigned version numbers. The old proposed v4.75–v4.77 labels are superseded by the actual integrated results above.

### P1. Essential surjectivity on 1-cells in each realization hom category

Fix chosen source objects `X`, `Y`. Determine the correct scope for:

```text
for every l : X.carrier -> Y.carrier,
  exists f : X -> Y, Nonempty (f.lift ≅ l)
```

Exit criterion: a source 1-cell with a raw StrongTrans and coherent invertible comparison square, under the precise necessary hypotheses. This is a proposed existence theorem, not a conclusion of v4.77. Its `preimage` operates on hom-category **morphisms (2-cells)**, not hom-category **objects (1-cells)**.

If proved for the intended sector, combine it with the existing local full faithfulness to construct hom-category equivalences. Then address their coherence/naturality; object-level essential surjectivity is another obligation for a proposed biequivalence.

### P2. Independently prescribed raw 2-cell and adjunction data

For fixed source 1-cells and an independently specified raw modification, determine whether a compatible DO₂ modification exists, or identify the precise obstruction. If both components are specified, prove the stored comparison equation rather than inferring it from isomorphism existence.

Exit criteria: exact projection identities for the prescribed raw data, compatible lifting, and any required unit/counit triangle laws without silently changing the inputs. In a fixed raw fiber, preservation of the prescribed identity modification is stronger than merely producing some source isomorphism.

This is not a request to reprove v4.79's DO₂-data preservation. Any failure statement must be proved for its stated hypotheses; lack of a current construction is not a counterexample.

### P3. Semantic admissibility versus exact raw liftability

Specify admissibility independently of `Liftable_(X,Y)`, then prove the appropriate implication, equivalence under extra hypotheses, or counterexample. Keep chosen presentations, variance, identity/composition stability, and the difference between exact and weak sectors explicit.

The historical programs involving thinness, trivial automorphisms, correction reachability, strict models, and explicit coherence/descent assumptions can supply candidate hypotheses. Do not make semantic admissibility a tautological renaming of source-morphism existence or promote weak admissibility to exact presentation.

### P4. Final higher mapping/classification property

Choose the precise source and target sectors and transformation level. Combine factor existence, mapping-level coherence, local equivalences where required, object-level coverage, and naturality under justified changes of context/presentation.

Exit criterion: a typed higher universal-property statement with all hypotheses and coherence obligations discharged. Neither a quotient/fractal carrier nor local full faithfulness alone is this final theorem. Preserve the distinction between presentation invariance and operational identification of different worlds.

## 8. Proof-engineering lessons retained

**Typed endpoints before choice.** The v4.78 unit/counit repair supplies `(X := X)` or `(X := Y)`, explicit source composition, and a typed `Nonempty` witness before `Classical.choice`. Do not ask nested choice/inversion to infer chosen presentation indices.

**Hom-category objects are 1-cells.** In v4.79, `F.map_preimage` needs the same source identity/composite objects already passed to `preimageIso`. A fully faithful projection is not an inverse on objects. Reverse these source endpoints when using an inverse isomorphism.

**Use bundled inverse data.** The v4.77 naturality proof keeps `kIso`, maps it with `mapIso`, and applies explicit isomorphism cancellation instead of requiring instance search to recover `Epi` for a named mapped morphism.

**Use the right equality interface.** `NatTrans.ext` can leave equality of component functions, requiring `funext`. Use typed `congrArg` for equality under restriction/whiskering, and explicit `Category.assoc` or stored inverse laws when generic rewrite matching is unstable. `change` only handles definitional equality; genuine index changes require `eqToHom`/`eqToIso`.

**Keep proof-only parameters and scopes visible.** Use `include` when a section hypothesis is needed only in a theorem proof. Imports do not open namespaces or scoped instances. Retain `autoImplicit false`, check pinned Mathlib APIs, and keep private helpers out of public theorem types.

These are reasons to improve proof structure, not to add axioms, weaken statements, disable linters, or raise resource limits by default. The official [fully faithful functor](https://leanprover-community.github.io/mathlib4_docs/Mathlib/CategoryTheory/Functor/FullyFaithful.html) and [bicategorical adjunction](https://leanprover-community.github.io/mathlib4_docs/Mathlib/CategoryTheory/Bicategory/Adjunction/Basic.html) documentation are explanatory references; the pinned source determines the actual API.

## 9. Validation, caching, and reproduction

[PR governance](.github/workflows/pr-governance-gate.yml) selects affected checks and publishes exact-head Lean/terminal receipts. [Main formal validation](.github/workflows/lean-formal-validation.yml) produces reusable `.lake` caches; the PR lane restores compatible workspaces. Cache keys distinguish platform, toolchain, manifest, and commit. A restored cache does not replace validation of changed Lean artifacts.

Re-observe the canonical SHA and PR head, check the selected target and actual checkout, and compare relevant dependency/build changes before reusing evidence. Do not attach old success to modified theorem content. Historical dependency linter warnings are not a new-module failure and are not fixed by this docs-only refresh.

**No manual Strict Lean rerun for README/ROADMAP-only changes.** Keep formal files, pins, and build configuration unchanged; use the selected documentation/runtime checks. Documentation merges advance the branch, not theorem authority. GitHub is the delivery location; leave #1558 untouched.

The pins live in [lean-toolchain](lean-toolchain) and [lake-manifest.json](lake-manifest.json); [docs/LEAN4_BUILD.md](docs/LEAN4_BUILD.md) is the build guide. The successful latest theorem command was:

```bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationExactUniversalAdjunctionLiftingV4_79
```

To reproduce both the raw-equivalence and prescribed-adjunction branches:

```bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationExactUniversalSourceEquivalenceV4_78 \
  KUOS.DependentOriginationExactUniversalAdjunctionLiftingV4_79
```

**Import boundary:** v4.79 imports v4.77 and v4.70, not v4.78 or v4.74. Their earlier proofs remain integrated, but are not validated anew merely by building v4.79. For direct reproduction of the historical leg-uniqueness statement, add `KUOS.DependentOriginationExactUniversalEquivalenceLegUniquenessV4_74` explicitly.

Registered aggregate target and separate runtime check:

```bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
PYTHONPATH=. python3 runtime/kuuos_current_check.py
```

Aggregate coverage depends on its actual imports. These are reproduction entry points, not instructions to launch a formal rebuild for this documentation change.

## 10. Current boundary at a glance

```text
CLOSED IN THE CHOSEN EXACT-UNIVERSAL SECTOR:
  source bicategory and strict DO₂ realization
  raw-equivalence leg existence and DO₂ essential uniqueness
  compatible raw/DO₂ isomorphism-pair classification
  actual local fullness and faithfulness of realization
  unique compatible source 2-cell over every prescribed DO₂ 2-cell
  source adjoint equivalence from coherent raw inverse data, with fixed raw legs
  exact classification of adjunctions on fixed source legs
  preservation of prescribed coherent DO₂ unit/counit, including inverses

PROPOSED NEXT:
  essential surjectivity on arbitrary DO₂ 1-cells in the intended sector
  lifting while independently prescribing raw 2-cell/adjunction data
  semantic admissibility versus presentation-indexed liftability
  final higher mapping property, object coverage, and naturality

NOT VALID WITHOUT FURTHER HYPOTHESES OR PROOF:
  weak W-admissibility => exact presentation/localization
  arbitrary one-way raw morphism => liftable morphism or equivalence
  DO₂ isomorphism => compatibility with an independently prescribed raw component
  local full faithfulness => essential surjectivity or final biequivalence
  runtime/docs/cache success => theorem authority
```
