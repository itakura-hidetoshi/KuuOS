# KuuOS / 空OS Roadmap

**Theorem snapshot: 2026-09-29 JST · integrated through v4.74**

This roadmap separates integrated Lean results from proposed theorem units. It is subordinate to the exact canonical GitHub snapshot and its formal artifacts. [README](README.md) gives the overview.

**現在地：source bicategory と DO₂ への strict realization は構成済み。** coherent raw equivalence の両方向の射の lift が存在し、同じ射の lift は DO₂ 側で同型になる。次の課題は、その同型と raw 成分の compatibility を証明して可逆 source ２射を構成し、unit/counit の整合性から source equivalence へ進むこと。

## 0. Authority and reproducible snapshot

| Role | Reference |
| --- | --- |
| Repository / canonical branch | `itakura-hidetoshi/KuuOS` / **main** |
| Observed main before this docs-only refresh | `ee0438d23119331c08f4c91365872429a6424d7f` |
| Latest theorem-bearing baseline | **`ee0438d23119331c08f4c91365872429a6424d7f`** |
| Latest theorem-bearing merge | [#1910 — equivalence-leg uniqueness v4.74](https://github.com/itakura-hidetoshi/KuuOS/pull/1910) |
| Exact validated PR head for that theorem unit | `d3d94bb3bf9b4198713a2c38ae071e8493551995` |
| Associated CI run | [#3235 / 36522637253](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/36522637253) |
| Head status receipts | `chatgpt-ci-receipt/KuuOS Strict Lean formal validation`: success; `chatgpt-ci-receipt/KuuOS exact-head terminal`: success |
| Lean | `leanprover/lean4:v4.30.0-rc2` |
| Mathlib | `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |

The observed-main row records the input to this refresh. It is not the eventual documentation commit or an assertion about a future moving branch. Subsequent docs-only commits advance `main`; they do not create a new theorem frontier. Re-observe the live branch before new work and compare its formal artifacts against this baseline.

```text
1. fresh exact GitHub canonical SHA
2. formal Lean theorem artifacts at that SHA
3. README / ROADMAP
4. exact-head CI/runtime receipts
5. history / memory
```

A CI receipt must be interpreted with its associated PR head, tested checkout, selected targets, and command. It is evidence of that validation, not a substitute for the theorem statement. Docs/runtime receipts do not validate new Lean content. The latest theorem statement is linked at the [immutable v4.74 baseline](https://github.com/itakura-hidetoshi/KuuOS/blob/ee0438d23119331c08f4c91365872429a6424d7f/formal/KUOS/DependentOriginationExactUniversalEquivalenceLegUniquenessV4_74.lean).

**Protected lane:** [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) is Lean 4.31 validation-only, outside canonical theorem authority. Keep it unmerged and in draft; do not mark Ready for review or enable auto-merge. Do not use it to change the canonical pins.

## 1. Long-range target and scope

The research target remains a higher dependent-origination mapping property. The following is a schematic objective, **not an existing Lean theorem or a finalized choice of functor category**:

```text
eta : C -> DO(C,W,J,H)

AdmissibleContextualSystems(C,X)
  ≃
Fun(DO(C,W,J,H),X)
```

A final statement must specify the exact admissible sector, higher variance, localization and stack-descent hypotheses, compatible 1-cells and 2-cells, coherent uniqueness, and naturality. The current source construction deliberately includes chosen exact presentations and universal-target witnesses. It does not silently include all weakly admissible raw systems.

A quotient, recursive carrier, inverse limit, metric fractal, or completed source bicategory is not by itself the final universal classification theorem. Likewise, strictness of realization does not establish local full faithfulness or a biequivalence.

## 2. Closed obstruction and geometric stress-test spine

### v4.00–v4.12: exact nonfactorization

The octahedral C2 countermodel separates weak W-admissibility from exact localization:

```text
weak W-admissibility                     EXISTS
coherent quotient transport              EXISTS
quotient coboundary solution             EXISTS
comparison / presentation lift           IMPOSSIBLE
HigherLocalizationFactorization          IMPOSSIBLE
```

[AbstractNonfactorizationV4_00](formal/KUOS/DependentOriginationAbstractNonfactorizationV4_00.lean) establishes nonfactorization. [StageIIObstructionClassV4_12](formal/KUOS/DependentOriginationStageIIObstructionClassV4_12.lean) gives `omega(T) = 1` in `ZMod 2` for every coherent quotient transport. A comparison lift would force the incompatible value zero.

This remains a permanent counterexample to the general implication from weak admissibility to exact presentation/localization.

### v4.13–v4.48: concrete carriers, limits, and descent

The integrated concrete sequence covers the eight-label Stage-II carrier; truncated-icosahedral incidence geometry; global/local capacity obstructions; middle-switch mates, source provenance, and integer orientation; recursive preservation at every finite depth; an inverse limit; fixed-point-free middle-switch; translated ternary Cantor fibers and exact Hausdorff dimension `log 2 / log 3`; zero-dimensional finite approximants with a Hausdorff-limit dimension jump; a bare-carrier self-homeomorphism; exact two-point orbit quotients; integer-orientation non-descent; mod-2 unique descent; and descent of the still-nonzero Stage-II class.

The geometry is a validated instance and stress test. It is not the general definition of dependent origination, and its special finite or metric conclusions are not automatically transferred to arbitrary presentations.

## 3. Closed presentation-general and universal-target layers

| Version | Integrated result | Scope boundary |
| --- | --- | --- |
| v4.49 | Presentation quotient factorization iff invariance; nonfactorization iff presentation-descent obstruction | Abstract presentation data; not the final higher mapping property |
| v4.50 | Exact DO₂ sector and its higher stack-localization factorization interface | Weak admissibility alone is insufficient |
| v4.51 | Exact presentability transported by a directed pointwise-equivalence comparison | Same DO₂ carrier, postcomposed raw comparison |
| v4.52 | Comparison hierarchy for exact presentations | A canonical common-target cospan is not automatically a coherent equivalence |
| v4.53 | Chosen coherent universal target under a coherent weak universal property plus stack descent of its chosen lift | Conditional factor existence and invertible-modification existence |
| v4.54 | Mutual coherent comparisons of universal targets; composites modification-isomorphic to identities | Not yet promoted to DO₂ equivalence at that theorem unit |
| v4.55 | Transport of universal targets under coherent two-sided raw equivalence | Chosen carrier is preserved |
| v4.56 | Mathlib `Bicategory.Equivalence` between exact coherent universal targets | Not an equivalence theorem for arbitrary exact presentations |

The exact positive-sector implications remain:

```text
exact DO₂ presentation
  => higher stack-localization factorization
  => higher localization factorization
  => weak W-admissibility
```

Reference entry points: [v4.49](formal/KUOS/DependentOriginationAbstractPresentationDescentV4_49.lean), [v4.50](formal/KUOS/DependentOriginationExactHigherPresentationSectorV4_50.lean), and [v4.56](formal/KUOS/DependentOriginationExactUniversalTargetDO2EquivalenceV4_56.lean).

## 4. Closed mapping-source construction — v4.57–v4.70

### Source interface

A source object `X` consists of a raw higher contextual system, a chosen exact DO₂ presentation, and a coherent universal-target witness. A source 1-cell `f : X -> Y` contains:

```text
f.raw   : raw StrongTrans
f.lift  : X.carrier -> Y.carrier
s_f     : restrict(f.lift) ; c_Y ≅ c_X ; f.raw
```

A source 2-cell contains a raw modification and a DO₂ modification satisfying the stored comparison-square equation. The equation is part of the type; two unrelated modifications are not a source 2-cell.

### Integrated milestones

| Version | Completed obligation | Formal entry point |
| --- | --- | --- |
| v4.57 | Objects, mapping-compatible 1-cells, identities, composition | [MappingMorphism](formal/KUOS/DependentOriginationExactUniversalMappingMorphismV4_57.lean) |
| v4.58 | Compatible 2-cell interface and restriction of modifications | [MappingTwoCell](formal/KUOS/DependentOriginationExactUniversalMappingTwoCellV4_58.lean) |
| v4.59–v4.60 | Vertical structure, genuine hom categories, raw/lift projection functors | [HomCategory](formal/KUOS/DependentOriginationExactUniversalMappingHomCategoryV4_60.lean) |
| v4.61–v4.64 | Restriction preserves whiskering; compatible left/right whiskering; horizontal composition and interchange | [Horizontal](formal/KUOS/DependentOriginationExactUniversalMappingHorizontalV4_64.lean) |
| v4.65–v4.66 | Compatible associator and both unitor homs | [Associator](formal/KUOS/DependentOriginationExactUniversalMappingAssociatorV4_65.lean), [Unitors](formal/KUOS/DependentOriginationExactUniversalMappingUnitorsV4_66.lean) |
| v4.67 | Structural inverse 2-cells, both inverse laws, hom-category `Iso` packaging | [StructuralIso](formal/KUOS/DependentOriginationExactUniversalMappingStructuralIsoV4_67.lean) |
| v4.68 | Pentagon and triangle coherence | [Coherence](formal/KUOS/DependentOriginationExactUniversalMappingCoherenceV4_68.lean) |
| v4.69 | Genuine source `Bicategory` instance, including the remaining whiskering axioms | [Bicategory](formal/KUOS/DependentOriginationExactUniversalMappingBicategoryV4_69.lean) |
| v4.70 | DO₂ realization as a Mathlib `StrictPseudofunctor` | [StrictPseudofunctor](formal/KUOS/DependentOriginationExactUniversalRealizationStrictPseudofunctorV4_70.lean) |

These are completed, not proposed milestones. There is no need to rebuild structural inverses, pentagon/triangle, or the source bicategory before continuing.

### Realization

`exactUniversalRealizationStrictCore` is packaged by `StrictPseudofunctor.mk'` as `exactUniversalRealization`:

```text
X   |-> X.carrier
f   |-> f.lift
eta |-> eta.lift
```

Identity and 1-cell composition are preserved definitionally. Left/right whiskering and the associator/unitors are preserved via the installed source projection API. The proof normalizes the strict-core `eqToHom` transports to identity 2-cells before using those projections.

The conclusion is a strict pseudofunctor between bicategories. It does not assert that the source is a strict bicategory, that realization is an equivalence, or that its hom functors are full or faithful.

## 5. Integrated lifting and uniqueness frontier — v4.71–v4.74

### v4.71 — equivalence of realized objects

File: [DependentOriginationExactUniversalRealizationRawEquivalenceV4_71.lean](formal/KUOS/DependentOriginationExactUniversalRealizationRawEquivalenceV4_71.lean).

For `X`, `Y` in the chosen exact-universal source and `E : HigherRawSystemCoherentEquivalence X.raw Y.raw`, the main results are:

```text
exactUniversalRealization_equivalent_of_rawCoherentEquivalence
exactUniversalRawObject_carrier_equivalent_of_rawCoherentEquivalence
```

They give `Nonempty (Bicategory.Equivalence X.carrier Y.carrier)` and its spelling through the realization object map. They reuse the v4.55/v4.56 transport and universal-target theorem. They do not produce a source equivalence with prescribed raw legs.

### v4.72 — presentation-indexed liftability

File: [DependentOriginationExactUniversalMorphismLiftabilityV4_72.lean](formal/KUOS/DependentOriginationExactUniversalMorphismLiftabilityV4_72.lean).

For fixed chosen source objects `X`, `Y` and `eta : X.raw -> Y.raw`:

```text
Liftable_(X,Y)(eta)
  := exists lift : X.carrier -> Y.carrier,
       Nonempty (restrict(lift) ; c_Y ≅ c_X ; eta)

Obstructed_(X,Y)(eta) := not Liftable_(X,Y)(eta)
```

Integrated API in namespace `ExactUniversalRawMorphism`:

```text
liftable_iff_exists_sourceMorphism
obstructed_iff_not_exists_sourceMorphism
liftable_raw
liftable_id
Liftable.comp
not_obstructed_raw
```

The predicate is exactly source-morphism existence over the prescribed raw projection; identities and compositions are liftable. Source and target presentation indices are explicit. Equal raw systems alone must not cause Lean to infer a different chosen source object.

This file names the logical complement of liftability. It does not give a decision procedure, a computable detector, or an independent cohomology obstruction class for every raw morphism. Comparison with an independently specified semantic admissibility condition remains open in this development.

### v4.73 — both coherent raw-equivalence legs have source lifts

File: [DependentOriginationExactUniversalEquivalenceLegLiftabilityV4_73.lean](formal/KUOS/DependentOriginationExactUniversalEquivalenceLegLiftabilityV4_73.lean).

Construction:

```text
transport X.presentation along E
  -> exact presentation of Y.raw with carrier X.carrier
  -> apply Y.universal.factor
  -> use the factor's comparison triangle as the source lifting square
```

The backward construction uses `E.symm`. The proved APIs include:

```text
ExactUniversalRawMorphism.Liftable.forward_of_rawCoherentEquivalence
ExactUniversalRawMorphism.Liftable.backward_of_rawCoherentEquivalence
exists_exactUniversalRawMorphism_forward_of_rawCoherentEquivalence
exists_exactUniversalRawMorphism_backward_of_rawCoherentEquivalence
```

These results supply actual source 1-cells over both prescribed raw legs. They do not supply compatible source unit or counit 2-cells.

### v4.74 — DO₂ isomorphism of any two lifts of the same equivalence leg

File: [DependentOriginationExactUniversalEquivalenceLegUniquenessV4_74.lean](formal/KUOS/DependentOriginationExactUniversalEquivalenceLegUniquenessV4_74.lean).

`exactPresentationComparisonOfForwardSourceMorphism` packages an existing source lift as an `ExactPresentationCoherentComparison` from the transported source presentation into the target. Given two such comparisons, `Y.universal.essential_unique` supplies an isomorphism of the underlying StrongTrans. `InducedBicategory.isoMk` turns it into a DO₂ hom-category isomorphism.

The key theorems are:

```text
exactUniversalRawMorphism_lifts_iso_of_same_forward_rawEquivalence
exactUniversalRawMorphism_lifts_iso_of_same_backward_rawEquivalence
```

For `f.raw = E.forward.comparison` and `g.raw = E.forward.comparison`, the forward conclusion is exactly:

```lean
Nonempty (f.lift ≅ g.lift)
```

**Meaning:** the realized lifts are unique up to existence of an isomorphism. **Not proved by this statement:** uniqueness of that isomorphism, equality of source morphisms, a compatible source 2-isomorphism, source adjoint equivalence, or local full faithfulness of realization.

## 6. The remaining compatibility equation

Fix source morphisms `f`, `g : X -> Y` with comparison squares `s_f`, `s_g`. For proposed components `r : f.raw -> g.raw` and `l : f.lift -> g.lift`, the [v4.58 interface](formal/KUOS/DependentOriginationExactUniversalMappingTwoCellV4_58.lean) requires:

```text
(restrict(l.hom) ▷ c_Y) ; s_g.hom
  =
s_f.hom ; (c_X ◁ r)
```

Thus the current distinction is:

```text
exists DO₂ Iso between the lifts                         PROVED in v4.74
exists one whose components satisfy the prescribed square NOT YET PROVED generally
exists compatible source 2-Iso                            NEXT CONSTRUCTION
```

Even in a fixed raw fiber, the raw component must be the prescribed identity modification after the required index transports. An arbitrary isomorphism supplied by essential uniqueness need not satisfy that condition merely by being an isomorphism.

The next proofs must either establish the equation from the existing hypotheses, identify an additional sufficient hypothesis precisely, or exhibit its failure. No compatibility hypothesis may be silently added to the existing universal-target witness, and no impossible compatibility claim should be presented as completed.

## 7. Proposed next theorem units — not yet integrated

The version labels below are planning labels. Their scope may be split or revised after fresh inspection of the formal artifacts.

### Proposed v4.75 — compatible 2-cell lifting

Start with lifts in a fixed equivalence-leg fiber and the prescribed raw identity modification. Then consider a prescribed invertible raw modification between two source 1-cells with fixed endpoints.

Exit criteria:

1. State a typed compatibility condition with all chosen source/presentation indices fixed.
2. Construct a DO₂ isomorphism satisfying that equation under explicitly stated hypotheses, or prove the precise obstruction.
3. Package the components as a compatible source 2-cell and prove inverse compatibility and both inverse laws where applicable.
4. Expose raw and DO₂ projection lemmas without equating entire dependent pseudofunctor structures.

The generic compatible-inverse proof pattern in v4.67 is reusable, but its implementation helpers are private. Reuse the argument through a deliberately designed API rather than referring to inaccessible private declarations. Those inverse arguments require compatibility of the forward cell; they do not prove that compatibility exists.

### Proposed v4.76 — compatible source unit and counit

For the forward and backward source morphisms whose raw projections are supplied by v4.73, align the raw comparison isomorphisms with the composites and identities. Construct compatible source 2-isomorphisms of the unit/counit orientation needed by the intended equivalence construction.

Exit criteria: explicit raw and lift projections, comparison-square compatibility for both cells, both inverse laws, and the required triangle/coherence equations. Keep the dependence on any extra lifting hypothesis visible. Object-level DO₂ equivalence from v4.71 and DO₂ hom isomorphisms from v4.74 do not alone close this unit.

### Proposed v4.77 — source bicategorical equivalence

Assemble the preceding compatible source data into a Mathlib `Bicategory.Equivalence` between the chosen source objects, with its raw legs related to the prescribed coherent raw equivalence. Prove the corresponding statement after applying strict realization.

Exit criteria: the actual equivalence structure and all required fields typecheck; no mere pair of opposite source morphisms is substituted for it. Choice-independence or naturality of these equivalences requires its own statement and proof.

### Subsequent units — semantic admissibility and the final mapping property

Compare an independently specified semantic admissibility condition with v4.72 `Liftable`, including identity/composition stability and the role of chosen presentations. Determine whether an implication, an equivalence under extra hypotheses, or a counterexample is the correct theorem.

Then state the final higher mapping property with the appropriate source, target, variance, transformation level, factor existence, compatible essential uniqueness, and naturality. Prove local fullness/faithfulness or an equivalence of hom categories only if the chosen classification statement requires them; they are not consequences of the current unstructured isomorphism-existence result.

The historical positive sufficient-condition program—thinness, trivial automorphisms, correction reachability, strict models, and explicit coherence/descent assumptions—remains a source of candidate hypotheses. Each application must use the precise theorem and assumptions that actually prove the relevant lifting equation.

## 8. Proof-engineering lessons for the next units

**Keep the problem at the smallest typed boundary.** v4.65/v4.66 separate pure bicategory pasting, component normal forms, and dependent source wrappers. Global equalities of StrongTrans or whole bicategory instances often ask Lean to normalize far more than the actual goal requires.

**Use extensionality at the right stage.** v4.60 source extensionality is effective for inverse laws and componentwise coherence. In the v4.70 strict-core proof, projecting first through induced-bicategory `.hom` obscured the small transport goal. The successful proof first exposes the definitionally trivial `eqToHom` transports with `change`, then composes the native projection equality with `Category.id_comp`/`Category.comp_id`.

**Distinguish definitional equality from a proved equality.** `change` only changes to a definitionally equal expression. For genuine index transport, keep `eqToHom`/`eqToIso` or a typed transport proof. Ordinary `rw` through a term on which the surrounding type depends can produce an ill-typed motive; use component APIs, typed equalities, `congrArg`, or a suitable dependent rewriting strategy.

**Avoid uncontrolled simplification of evidence.** Broad `simpa using` simplifies the supplied theorem type as well as the goal. In v4.67, projection plus a typed normalization and direct `exact` of `Iso.hom_inv_id`/`Iso.inv_hom_id` avoids this instability. In v4.71, the native equivalence witness already has the needed type by constructor-level identification, so it is reused directly.

**Fix the chosen presentation indices.** v4.72/v4.73 explicitly pass `(X := X)` and `(Y := Y)` where raw projections do not uniquely recover the source objects. v4.74 first types the underlying StrongTrans isomorphism, then applies `InducedBicategory.isoMk`.

**Preserve API and namespace discipline.** Imports do not open namespaces or propagate scoped notation. Keep `autoImplicit false`, open the needed StrongTrans/bicategory scopes, avoid typeclass shadowing and diamonds, and keep private implementation helpers out of public theorem types. Check the pinned Mathlib source before assuming an API or generated projection name.

These are proof-design lessons, not reasons to suppress warnings, raise heartbeat limits by default, weaken statements, or add axioms.

## 9. Validation and cache policy

[PR governance](.github/workflows/pr-governance-gate.yml) selects affected checks and publishes head-associated Lean/terminal status receipts. [Main formal validation](.github/workflows/lean-formal-validation.yml) builds the pinned target and provides reusable `.lake` workspace caches. The PR Lean job restores compatible cache content without saving to the shared producer lane.

Cache keys include operating system, architecture, the toolchain hash, the manifest hash, and a commit suffix. Compatible-prefix restoration reuses an earlier workspace when available. Restoration does not establish proof validity: the selected target is still built against the actual checkout. Cache hits can still involve substantial rebuilding; benchmark claims must identify both runs, their targets, and their dependency changes.

For subsequent work:

- Re-observe the exact canonical SHA and relevant artifact before editing or deciding to merge.
- A changed Lean head needs a new Lean validation receipt. Check its actual source, target selection, and associated head rather than an old GREEN badge.
- Do not rerun Strict Lean merely for README/ROADMAP-only changes when formal content, pins, and build configuration are unchanged. Run the applicable selected documentation/runtime checks instead.
- Before reusing validation across an independent base change, compare relevant blobs/diffs and the dependency/build context. Never transfer success to modified theorem content without validation.
- Keep theorem, runtime/MCP, and documentation results separate. A docs-only merge advances the branch, not the theorem frontier.
- Use GitHub as the delivery location; no ZIP artifact is needed. Leave #1558 untouched.

A successful selected workflow is not a repository-wide warning-free certificate. Historical dependency linter warnings must not be misreported as fixed by a documentation refresh.

## 10. Reproduction entry points

Pins are recorded in [lean-toolchain](lean-toolchain) and [lake-manifest.json](lake-manifest.json). The following commands reproduce the repository's configured CI interface; [docs/LEAN4_BUILD.md](docs/LEAN4_BUILD.md) and the current workflow are the build references.

Current theorem frontier, including its imported source/realization chain:

```bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationExactUniversalEquivalenceLegUniquenessV4_74
```

Focused structure and lifting targets:

```bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationExactUniversalMappingBicategoryV4_69 \
  KUOS.DependentOriginationExactUniversalRealizationStrictPseudofunctorV4_70 \
  KUOS.DependentOriginationExactUniversalMorphismLiftabilityV4_72 \
  KUOS.DependentOriginationExactUniversalEquivalenceLegLiftabilityV4_73
```

Foundational boundary targets:

```bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationAbstractNonfactorizationV4_00 \
  KUOS.DependentOriginationStageIIObstructionClassV4_12 \
  KUOS.DependentOriginationAbstractPresentationDescentV4_49 \
  KUOS.DependentOriginationExactHigherPresentationSectorV4_50 \
  KUOS.DependentOriginationExactUniversalTargetDO2EquivalenceV4_56
```

Registered aggregate target and separate runtime check:

```bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
PYTHONPATH=. python3 runtime/kuuos_current_check.py
```

These are reproduction commands, not instructions to launch a formal rebuild for this docs-only update.

## 11. Permanent no-go implications

```text
weak W-admissibility
  !=> higher localization / exact DO₂ presentation

one failing gauge
  !=> every gauge fails

local odd parity
  !=> global obstruction without the relevant theorem

finite recursion or a newly chosen inverse-limit metric
  !=> an exact positive Hausdorff-dimension theorem

two arbitrary exact presentations
  !=> DO₂ equivalence of universal targets

arbitrary one-way raw morphism
  !=> exact liftability or an equivalence

Nonempty (f.lift ≅ g.lift)
  !=> uniqueness of the Iso or equality of the source morphisms

DO₂ Iso of lifts
  !=> compatible source 2-Iso with prescribed raw component

opposite source 1-cells
  !=> source Bicategory.Equivalence without compatible coherence data

source bicategory + strict realization
  !=> local full faithfulness or the final universal mapping property

runtime/docs/cache success
  !=> theorem authority
```

## 12. Current research boundary

```text
CLOSED:
  octahedral nonfactorization and nonzero Stage-II obstruction
  concrete recursive/geometric stress test and orientation descent
  abstract presentation descent and exact Cat-valued sector
  universal-target invariance, essential uniqueness, naturality, DO₂ equivalence
  mapping-compatible source 1-cells and 2-cells
  hom categories, whiskering, horizontal interchange
  structural isomorphisms, pentagon, triangle
  genuine source bicategory
  strict DO₂ realization
  coherent raw-equivalence invariance of realized objects
  exact presentation-indexed morphism liftability boundary
  source lifts for both coherent raw-equivalence legs
  DO₂ isomorphism of any two lifts of the same equivalence leg

NEXT, WITH EXPLICIT HYPOTHESES:
  comparison-square compatibility for prescribed raw/lift 2-cell components
  compatible source 2-isomorphisms
  source unit/counit coherence and source bicategorical equivalence
  semantic admissibility versus exact liftability
  final higher dependent-origination mapping/classification theorem
```
