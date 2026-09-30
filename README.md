# KuuOS / 空OS

![KuuOS PR Governance Gate](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/pr-governance-gate.yml/badge.svg)
![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS** is a public research architecture for dependent origination (縁起), contextual transport, higher coherence, descent, obstruction, correction, recursive carriers, and bounded AI operation. Founder: **Hidetoshi Itakura / 板倉英俊**.

> Which structure survives justified changes of context and presentation, how can compatible local information be transported and glued, and which universal property characterizes the invariant content?

**現在の形式化到達点は v4.86。** 選択済み exact-universal sector では、source bicategory から object-labelled realized sector への strict realization と、その逆向き section pseudofunctor が構成されています。各 hom category では realization は実際に同値であり、任意の DO₂ 1-cell は source 1-cell に **exact に**持ち上がります。さらに cross-hom coherence まで section pseudofunctor として統合され、source 側 roundtrip に対する global unit の自然性形 isomorphism まで構成済みです。

**まだ最終 biequivalence ではありません。** v4.86 は global unit の各 1-cell における自然性 square を与えますが、その squares を StrongTrans の全 coherence field に組み上げる段階、realized-side counit の global packaging、object-labelled sector から全 DO₂ object への coverage、独立に指定された raw data の保持、semantic admissibility と exact liftability の関係は別課題です。

Philosophical interpretation, formal proof, runtime validation, and operational authority remain distinct. [ROADMAP](ROADMAP.md) records the exact closed results and next obligations; [docs/LEAN4_BUILD.md](docs/LEAN4_BUILD.md) describes the pinned build environment.

## Canonical theorem snapshot — 2026-09-30 JST

| Role | Reference |
| --- | --- |
| Canonical branch | **main** — re-observe before new work |
| Observed main before this docs-only refresh | **`4d1c26388480e13398cd63faaa1f4323f58b4a8f`** |
| Latest theorem-bearing baseline | **`4d1c26388480e13398cd63faaa1f4323f58b4a8f`** |
| Latest theorem merge | [#1924 — global source-roundtrip unit squares v4.86](https://github.com/itakura-hidetoshi/KuuOS/pull/1924) |
| Validated PR head | `affd9b1633ca3d82bc55681f601735a2db07ceaa` |
| Associated validation | [Run #3272 / 36670438900](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/36670438900): completed / success |
| Exact-head receipts | `chatgpt-ci-receipt/KuuOS Strict Lean formal validation`: success; `chatgpt-ci-receipt/KuuOS exact-head terminal`: success |
| Lean artifact | `11078177476`, digest `sha256:46863dbfd4043ce14adc2834f422e5ccee4354f29e8573e6cb71db0570f27278` |
| Build result | `Build completed successfully (8605 jobs)` |
| Lean / Mathlib | `leanprover/lean4:v4.30.0-rc2` / `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |

The v4.86 module contains six public axiom queries. The validated output contains the ordinary Mathlib axioms used throughout this spine and no `sorryAx`. The immutable theorem file at the theorem-bearing baseline is [DependentOriginationExactUniversalGlobalUnitSquaresV4_86.lean](https://github.com/itakura-hidetoshi/KuuOS/blob/4d1c26388480e13398cd63faaa1f4323f58b4a8f/formal/KUOS/DependentOriginationExactUniversalGlobalUnitSquaresV4_86.lean).

The observed-main SHA above is the **input** to this documentation refresh. A later README/ROADMAP-only merge advances `main` without creating a newer theorem-bearing baseline.

```text
fresh exact canonical GitHub SHA
  > formal Lean theorem artifacts at that SHA
  > README / ROADMAP
  > exact-head CI/runtime receipts
  > history / memory
```

[#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) remains the separate Lean 4.31 validation-only lane. Keep it draft and unmerged; do not mark it Ready for review, enable auto-merge, or change canonical pins through it.

## What 空 means here

空 is not “nothing exists.” Its operational role is non-reification: a chosen presentation is not intrinsic substance, a local observation is not global truth, and runtime success is not WORLD truth.

KuuOS therefore separates observation from inference, identifies the active context, retains multiple compatible presentations, follows relations and history, checks local compatibility and descent, exposes obstructions, respects the relevant authority boundary, performs only the necessary action, and re-observes afterward.

The formal program is richer than a graph. It contains contextual systems, mappings between systems, transformations between mappings, higher coherence, quotient/descent structure, obstructions, and universal properties. This is a mathematical model of dependent-origination structure, not a claim to the unique formal interpretation of Buddhist philosophy.

## Exact-universal source and realized sector

A source object `X` stores:

- a raw Cat-valued contextual system;
- a chosen exact DO₂ presentation;
- its comparison StrongTrans;
- the pointwise equivalence data required by the exact-universal sector;
- a coherent universal-target witness.

A source 1-cell `f : X ⟶ Y` stores a raw StrongTrans, a DO₂ lift, and an invertible comparison square. A source 2-cell stores compatible raw and lift modifications.

The [v4.69 source bicategory](formal/KUOS/DependentOriginationExactUniversalMappingBicategoryV4_69.lean) and [v4.70 strict realization](formal/KUOS/DependentOriginationExactUniversalRealizationStrictPseudofunctorV4_70.lean) send

```text
X   |-> X.carrier
f   |-> f.lift
eta |-> eta.lift
```

without asserting that the source bicategory itself is strict.

From v4.84 onward it is useful to separate two bicategories:

```text
Source
  = chosen exact-universal source objects and compatible source cells

RealizedSector
  = the same object labels,
    but hom categories are the DO₂ hom categories between their chosen carriers
```

Keeping the labels is deliberate. Equal or equivalent realized carriers do not erase different source presentations, contextual histories, or world bindings.

## Integrated mathematical spine

| Versions | Closed result | Main entry points |
| --- | --- | --- |
| v4.00–v4.12 | Octahedral C2 nonfactorization and nonzero Stage-II obstruction in `ZMod 2` | [v4.00](formal/KUOS/DependentOriginationAbstractNonfactorizationV4_00.lean), [v4.12](formal/KUOS/DependentOriginationStageIIObstructionClassV4_12.lean) |
| v4.13–v4.48 | Incidence/capacity obstructions, recursive/inverse-limit carriers, exact Cantor dimension, switch/orientation descent | [v4.40](formal/KUOS/DependentOriginationStageIIExactFractalCertificateV4_40.lean), [v4.48](formal/KUOS/DependentOriginationStageIIOrbitOrientationDescentV4_48.lean) |
| v4.49–v4.56 | Abstract presentation descent, exact sector, universal-target comparison and DO₂ equivalence | [v4.49](formal/KUOS/DependentOriginationAbstractPresentationDescentV4_49.lean), [v4.56](formal/KUOS/DependentOriginationExactUniversalTargetDO2EquivalenceV4_56.lean) |
| v4.57–v4.70 | Compatible source objects/1-cells/2-cells, native source bicategory, strict realization | [v4.60](formal/KUOS/DependentOriginationExactUniversalMappingHomCategoryV4_60.lean), [v4.70](formal/KUOS/DependentOriginationExactUniversalRealizationStrictPseudofunctorV4_70.lean) |
| v4.71–v4.79 | Liftability interface, local full faithfulness, source equivalences, exact fixed-leg adjunction lifting | [v4.77](formal/KUOS/DependentOriginationExactUniversalRealizationFullyFaithfulV4_77.lean), [v4.78](formal/KUOS/DependentOriginationExactUniversalSourceEquivalenceV4_78.lean), [v4.79](formal/KUOS/DependentOriginationExactUniversalAdjunctionLiftingV4_79.lean) |
| v4.80–v4.83 | Pointwise equivalence ⇒ coherent inverse/retraction ⇒ arbitrary DO₂ 1-cell exact lift; realization hom-category equivalences | [v4.80](formal/KUOS/DependentOriginationExactUniversalHomSectionV4_80.lean), [v4.82](formal/KUOS/DependentOriginationPointwiseInverseCoherenceV4_82.lean), [v4.83](formal/KUOS/DependentOriginationExactUniversalHomEquivalenceV4_83.lean) |
| v4.84–v4.86 | Cross-hom section pseudofunctor, labelled strict realization, exact realized roundtrip, source-roundtrip unit squares | [v4.84](formal/KUOS/DependentOriginationExactUniversalSectionPseudofunctorV4_84.lean), [v4.85](formal/KUOS/DependentOriginationExactUniversalLabelledRealizationV4_85.lean), [v4.86](formal/KUOS/DependentOriginationExactUniversalGlobalUnitSquaresV4_86.lean) |

The positive exact-universal results do **not** erase the earlier obstruction theorem:

```text
weak W-admissibility can hold
while exact localization / exact presentation is impossible.
```

Exactness, chosen presentation, and the universal-target witness remain explicit sector hypotheses.

## Current theorem chain — v4.80–v4.86

### v4.80 — one coherent retraction is enough for every outgoing 1-cell

[v4.80 / #1918](formal/KUOS/DependentOriginationExactUniversalHomSectionV4_80.lean) proves a conditional reduction. If the presentation comparison of `X`

```text
c_X : restrict(X.carrier) -> X.raw
```

admits coherent one-sided inverse data

```text
d_X : X.raw -> restrict(X.carrier)
c_X ; d_X ~= 1,
```

then every DO₂ 1-cell `ell : X.carrier ⟶ Y.carrier` has a source preimage whose lift is **literally** `ell`. The construction extends to a hom-functor section and hom-category equivalence.

At v4.80 the retraction is still an explicit input.

### v4.81–v4.82 — pointwise equivalences assemble into that coherent retraction

[v4.81 / #1919](formal/KUOS/DependentOriginationPointwiseInverseNaturalityV4_81.lean) starts from a Cat-valued StrongTrans whose components are equivalences and constructs the inverse naturality isomorphisms, with exact unit-compatible recovery and uniqueness.

[v4.82 / #1920](formal/KUOS/DependentOriginationPointwiseInverseCoherenceV4_82.lean) proves the missing base two-cell, identity, and composition coherence laws. The pointwise inverses become an actual inverse `StrongTrans`, and the chosen component units assemble into an invertible modification

```text
1_R ~= c ; d.
```

Its inverse is exactly the coherent retraction required by v4.80.

### v4.83 — P1 closes on the chosen exact-universal sector

[v4.83 / #1921](formal/KUOS/DependentOriginationExactUniversalHomEquivalenceV4_83.lean) instantiates v4.82 with each source object's stored presentation comparison. No additional retraction or liftability hypothesis remains.

For every chosen exact-universal `X,Y` and every realized 1-cell

```text
ell : X.carrier ⟶ Y.carrier
```

there is a source 1-cell with exact recovery:

```lean
∃ f : X ⟶ Y, f.lift = ell
```

and the actual realization hom functor is a native Mathlib equivalence:

```lean
(X ⟶ Y) ≌ (X.carrier ⟶ Y.carrier)
```

with an explicit inverse section. Thus **1-cell essential surjectivity and 2-cell full faithfulness are both closed on the existing chosen exact-universal object sector.**

This is not object-level coverage of every DO₂ object.

### v4.84 — the local inverse sections become a pseudofunctor

[v4.84 / #1922](formal/KUOS/DependentOriginationExactUniversalSectionPseudofunctorV4_84.lean) defines the object-labelled `ExactUniversalRealizedSector` and assembles the v4.83 hom sections into

```text
S : RealizedSector -> Source.
```

Identity/composition comparison isomorphisms are lifted through local full faithfulness. Left/right whiskering, associator, and both unitors are proved. `S` is a native pseudofunctor and is not claimed strict.

### v4.85 — label-preserving strict realization and exact realized-side cell recovery

[v4.85 / #1923](formal/KUOS/DependentOriginationExactUniversalLabelledRealizationV4_85.lean) constructs

```text
R : Source -> RealizedSector
```

as a native `StrictPseudofunctor`, retaining the same source-object labels.

The realized-side section/realization roundtrip recovers objects, 1-cells, and 2-cells exactly, and on every realized hom category:

```lean
S.mapFunctor X Y ⋙ R.mapFunctor X Y = 𝟭 (X ⟶ Y)
```

This is an exact cellwise/local roundtrip. It is not yet a packaged global pseudonatural counit or a final biequivalence.

### v4.86 — source roundtrip and global unit squares

[v4.86 / #1924](formal/KUOS/DependentOriginationExactUniversalGlobalUnitSquaresV4_86.lean) forms the actual source composite

```text
Source --R--> RealizedSector --S--> Source
```

and defines the source roundtrip pseudofunctor `S ∘ R`.

For every source 1-cell `f`, the v4.83 hom-unit component is retyped as

```text
f ≅ roundtrip(f)
```

and then promoted to the pseudonaturality-shaped isomorphism

```text
f ; 1  ≅  1 ; roundtrip(f).
```

Under DO₂ realization this is exactly the canonical right-unitor followed by inverse left-unitor, with the inverse direction recovered as well.

**v4.86 prepares the global unit StrongTrans; it does not yet assert its remaining StrongTrans naturality/coherence fields.**

## Closed versus open

### Closed in the chosen exact-universal sector

- native source bicategory;
- strict DO₂ realization;
- local faithfulness and fullness on 2-cells;
- source isomorphism lifting between existing source 1-cells;
- source adjoint equivalence from coherent raw equivalence data;
- exact classification of adjunction structures on fixed source legs;
- coherent inverse/retraction from the existing pointwise-equivalence field;
- exact lifting of every DO₂ 1-cell between existing chosen carriers;
- native hom-category equivalences;
- cross-hom section pseudofunctor;
- label-preserving strict realization;
- exact realized-side cellwise roundtrip;
- source-roundtrip pseudofunctor and its canonical unit squares.

### Still open

1. assemble the v4.86 unit squares into the full global source-side StrongTrans / invertible pseudonatural unit and prove all coherence fields;
2. package the realized-side exact roundtrip as the corresponding global counit/equivalence data;
3. conclude the appropriate biequivalence/equivalence statement between **Source** and the **object-labelled RealizedSector**;
4. separately decide whether the intended final theorem needs coverage of DO₂ objects outside that labelled sector;
5. handle independently prescribed raw 2-cell / unit / counit data rather than allowing compatibility to determine the raw component;
6. relate semantic admissibility to presentation-indexed exact liftability without defining one tautologically from the other;
7. formulate the final higher dependent-origination mapping/classification theorem with its target sector, variance, descent, and naturality explicit.

## CI, caching, and reproduction

[PR governance](.github/workflows/pr-governance-gate.yml) selects impacted checks and restores compatible `.lake` content. Cache reuse is a build optimization, never theorem authority.

The latest theorem was validated with:

```bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationExactUniversalGlobalUnitSquaresV4_86
```

The current global chain imports v4.85 → v4.84 → v4.83 and the v4.80/v4.82 route behind it. The separate raw-equivalence existence theorem v4.78 is not on that import path. To reproduce both current major theorem branches:

```bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationExactUniversalSourceEquivalenceV4_78 \
  KUOS.DependentOriginationExactUniversalGlobalUnitSquaresV4_86
```

The registered aggregate target and separate runtime check remain:

```bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
PYTHONPATH=. python3 runtime/kuuos_current_check.py
```

A selected successful build is not a repository-wide warning-free certificate. Historical dependency warnings remain separate from new-module validity.

**README/ROADMAP-only changes do not require manually rerunning an already successful Strict Lean theorem build.** Documentation merges advance `main`, not theorem authority.

## Proof-engineering lessons

Recent Lean work reinforced several rules:

- imports make declarations available but do not open their namespaces;
- `change` requires definitional equality; propositional normalizations such as inverse-of-`Iso.trans` need the relevant theorem;
- dependent fields should be elaborated only after their ambient source objects/endpoints are fixed;
- generated universe argument order should be inferred from typed maps rather than copied positionally across unrelated declarations;
- parenthesize a notation receiver before generalized field notation when dotted parsing would otherwise capture it;
- preserve bundled isomorphisms and explicit endpoint types instead of relying on typeclass reconstruction through wrappers;
- use faithful realization to reflect higher coherence only after the realized equality has been reduced to a small typed diagram.

These are proof-structure lessons, not reasons to add axioms, weaken statements, raise resource limits, disable linters, or broaden transparency.

## Current research statement

The chosen exact-universal source now has **hom-category equivalences** with the corresponding DO₂ hom categories, and those inverse hom sections have been assembled into a coherent pseudofunctor over the object-labelled realized sector. The converse labelled realization is strict and gives exact realized-side cell recovery. The source-side composite has canonical global unit squares whose realized forms are exactly the expected unitors.

The immediate frontier is to finish the global pseudonatural unit/counit coherence and thereby identify the precise biequivalence/equivalence statement on the object-labelled sector—without collapsing distinct contextual presentations or silently upgrading weak admissibility to exactness.
