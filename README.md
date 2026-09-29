# KuuOS / 空OS

![KuuOS PR Governance Gate](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/pr-governance-gate.yml/badge.svg)
![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS** is a public research architecture for dependent origination (縁起), contextual transport, higher coherence, descent, obstruction, correction, recursive carriers, and bounded AI operation. Founder: **Hidetoshi Itakura / 板倉英俊**.

> Which structure survives justified changes of context and presentation, how can compatible local information be transported and glued, what obstructs that process, and which universal property characterizes the invariant content?

**現在の到達点：v4.74。** exact universal mapping source は Mathlib の `Bicategory` として構成済みで、DO₂ への実現は `StrictPseudofunctor` になっています。coherent raw equivalence の両方向の射は source に持ち上がり、同じ射の lift は DO₂ 側で同型になります。ただし、その同型を raw 成分と整合する可逆 source ２射にする条件は、まだ別の証明課題です。

Philosophical interpretation, mathematical presentation, formal proof, runtime validation, and operational authority remain distinct evidence classes. See [ROADMAP](ROADMAP.md) for theorem-sized next steps and [the build guide](docs/LEAN4_BUILD.md) for the formal environment.

## Canonical theorem snapshot — 2026-09-29 JST

| Item | Reference for this documentation snapshot |
| --- | --- |
| Canonical branch | **main** — a moving reference, re-observe before work |
| Observed main when preparing this refresh | `ee0438d23119331c08f4c91365872429a6424d7f` |
| Theorem-bearing baseline | **`ee0438d23119331c08f4c91365872429a6424d7f`** |
| Integrated theorem frontier | **v4.74 — essential uniqueness of coherent raw-equivalence-leg lifts in the DO₂ hom category** |
| Latest theorem-bearing merge | [PR #1910](https://github.com/itakura-hidetoshi/KuuOS/pull/1910) |
| Validated PR head for v4.74 | `d3d94bb3bf9b4198713a2c38ae071e8493551995` |
| Associated validation | [Run #3235 / 36522637253](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/36522637253); Strict Lean and exact-head terminal receipts: success |
| Lean | **`leanprover/lean4:v4.30.0-rc2`** |
| Mathlib | **`5450b53e5ddc75d46418fabb605edbf36bd0beb6`** |

The SHA observed above is the **input snapshot**, not a claim that a moving `main` remains at that commit after this documentation change. A later docs-only merge advances `main` without advancing the theorem-bearing baseline. The [pinned v4.74 artifact](https://github.com/itakura-hidetoshi/KuuOS/blob/ee0438d23119331c08f4c91365872429a6424d7f/formal/KUOS/DependentOriginationExactUniversalEquivalenceLegUniquenessV4_74.lean) is the primary reference for its mathematical statement; a CI badge is not a substitute for it.

The authority order is fixed:

```text
fresh exact canonical GitHub SHA
  > formal Lean theorem artifacts at that SHA
  > README / ROADMAP
  > exact-head CI/runtime receipts
  > history / memory
```

The Lean 4.31 validation-only lane [PR #1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) is outside canonical theorem authority. Do not merge it, mark it Ready for review, or enable auto-merge. The pinned canonical environment is unchanged.

## What 空 means here

空 is not treated as “nothing exists.” Its operational role is non-reification:

```text
chosen presentation != intrinsic substance
local observation != global truth
runtime success != WORLD truth
formal encoding != unique philosophical interpretation
model generation != theorem authority
```

KuuOS keeps observations and inferences separate, preserves alternative presentations, follows relations and history, checks local compatibility and descent, identifies obstructions, respects the relevant authority boundary, and updates its interpretation after action and re-observation.

The formal program therefore studies more than a graph of elements and edges. It internalizes mappings between contextual systems, transformations between mappings, and the coherence needed when these are composed or re-associated. This is a mathematical model of dependent-origination structure, not a claim to a unique formal interpretation of Buddhist philosophy.

## Completed mathematical spine

### Obstruction and concrete verification — v4.00–v4.48

For the finite octahedral C2 countermodel, the formal development separates the following facts:

```text
weak W-admissibility                     EXISTS
coherent quotient transport              EXISTS
quotient coboundary solution             EXISTS
comparison / presentation lift           IMPOSSIBLE
HigherLocalizationFactorization          IMPOSSIBLE
```

[v4.00](formal/KUOS/DependentOriginationAbstractNonfactorizationV4_00.lean) establishes exact nonfactorization. [v4.12](formal/KUOS/DependentOriginationStageIIObstructionClassV4_12.lean) extracts the transport-independent class `omega(T) = 1` in `ZMod 2` for every coherent quotient transport `T`. Weak admissibility must not be promoted to exact localization.

The v4.13–v4.48 stress-test spine transports this obstruction through an eight-label carrier, truncated-icosahedral incidence geometry, finite-depth recursion, an inverse limit, translated ternary Cantor fibers, and the middle-switch involution. It includes exact Hausdorff dimension `log 2 / log 3`, zero-dimensional finite approximants and their dimension jump at the limit, a fixed-point-free bare-carrier self-homeomorphism, an exact two-point orbit quotient, integer-orientation non-descent, mod-2 unique descent, and descent of the still-nonzero Stage-II obstruction.

**Concrete geometry is a validated stress test, not the general definition of dependent origination.**

### Presentation-general and universal-target layers — v4.49–v4.56

[v4.49](formal/KUOS/DependentOriginationAbstractPresentationDescentV4_49.lean) proves:

```text
HasPresentationQuotientFactorization <-> IsPresentationInvariant
not HasPresentationQuotientFactorization <-> HasPresentationDescentObstruction
```

[v4.50](formal/KUOS/DependentOriginationExactHigherPresentationSectorV4_50.lean) identifies the exact Cat-valued positive sector:

```text
exact DO₂ presentation
  => higher stack-localization factorization
  => higher localization factorization
  => weak W-admissibility
```

The converse from weak admissibility is false in general. The later universal-target results do not erase that counterexample.

The v4.51–v4.56 sequence proves directed pointwise-equivalence invariance of exact presentability, separates common-target cospans from stronger coherent comparisons, constructs a coherent universal target under an explicit universal-property and stack-descent hypothesis, proves mutual coherent uniqueness and naturality under coherent raw equivalence, and obtains [DO₂ bicategorical equivalence of exact universal targets](formal/KUOS/DependentOriginationExactUniversalTargetDO2EquivalenceV4_56.lean). The last conclusion concerns **universal targets**, not arbitrary exact presentations.

## The source bicategory and strict realization are installed

### Mapping data — v4.57–v4.66

A source object stores a raw Cat-valued higher contextual system, an exact DO₂ presentation, and a coherent universal-target witness. A source 1-cell `f : X -> Y` stores a raw StrongTrans, a DO₂ lift, and an invertible square:

```text
s_f : restrict(f.lift) ; c_Y ≅ c_X ; f.raw
```

A source 2-cell between `f` and `g` stores both a raw modification and a DO₂ modification, together with the equation that makes them compatible with `s_f` and `s_g`. The sequence constructs identity and vertical composition, [hom categories](formal/KUOS/DependentOriginationExactUniversalMappingHomCategoryV4_60.lean), restriction/whiskering compatibility, left and right whiskering, horizontal composition and interchange, and compatible associator and unitor homs.

### Structural closure and realization — v4.67–v4.70

| Version | Integrated result | Formal artifact |
| --- | --- | --- |
| v4.67 | Compatible structural inverses, both inverse laws, and associator/left/right unitor `Iso` values | [StructuralIsoV4_67](formal/KUOS/DependentOriginationExactUniversalMappingStructuralIsoV4_67.lean) |
| v4.68 | Pentagon and triangle, reduced through source extensionality to native Mathlib coherence | [CoherenceV4_68](formal/KUOS/DependentOriginationExactUniversalMappingCoherenceV4_68.lean) |
| v4.69 | Genuine `ExactUniversalRawObject.bicategory` instance | [BicategoryV4_69](formal/KUOS/DependentOriginationExactUniversalMappingBicategoryV4_69.lean) |
| v4.70 | `exactUniversalRealizationStrictCore` and `exactUniversalRealization : StrictPseudofunctor ...` | [StrictPseudofunctorV4_70](formal/KUOS/DependentOriginationExactUniversalRealizationStrictPseudofunctorV4_70.lean) |

The realization acts as follows:

```text
source object X   |-> X.carrier
source 1-cell f   |-> f.lift
source 2-cell eta |-> eta.lift
```

Identity and 1-cell composition are preserved by definitional equality. The five whiskering/structural preservation obligations are closed using explicit projection lemmas and normalization of the `eqToHom` transports inserted by `StrictPseudofunctorCore`.

This is a **strict pseudofunctor**, not an assertion that every associator or unitor of the source bicategory is an identity. These construction steps are completed and must not remain listed as future work.

## Current frontier — v4.71–v4.74

### v4.71: coherent raw equivalence preserves realized objects

For chosen exact-universal source objects `X`, `Y` and `E : HigherRawSystemCoherentEquivalence X.raw Y.raw`, [v4.71](formal/KUOS/DependentOriginationExactUniversalRealizationRawEquivalenceV4_71.lean) proves:

```lean
Nonempty (Bicategory.Equivalence X.carrier Y.carrier)
```

The same statement is provided for the object map of `exactUniversalRealization`. This concerns **realized objects**. It does not yet construct an equivalence in the source bicategory with prescribed raw legs.

### v4.72: exact liftability of a prescribed raw morphism

For fixed chosen source objects `X`, `Y`, [v4.72](formal/KUOS/DependentOriginationExactUniversalMorphismLiftabilityV4_72.lean) defines `ExactUniversalRawMorphism.Liftable eta` by existence of a DO₂ lift and an invertible presentation-comparison square. It proves:

```text
Liftable_(X,Y)(eta)
  <-> exists f : ExactUniversalRawMorphism X Y, f.raw = eta

Obstructed_(X,Y)(eta)
  <-> no such source 1-cell exists
```

Liftability contains identities and is closed under composition. The chosen `X` and `Y` are part of the predicate: the raw projection alone does not determine the presentation indices.

`Obstructed` is defined as `not Liftable`. This is an exact logical boundary, **not** a new computable obstruction detector or a new cohomology-class construction. No theorem here makes every arbitrary raw morphism liftable.

### v4.73: both coherent raw-equivalence legs lift

[v4.73](formal/KUOS/DependentOriginationExactUniversalEquivalenceLegLiftabilityV4_73.lean) transports `X.presentation` along `E` and applies `Y.universal.factor`. The factor's comparison triangle is the required lifting square. Applying the construction to `E.symm` gives the backward leg.

Both forward and backward raw legs therefore have actual source 1-cell representatives. Their existence is stronger than equivalence of realized objects alone, but it is still distinct from compatible source unit/counit 2-cells.

### v4.74: essential uniqueness holds for the DO₂ lifts

[v4.74](formal/KUOS/DependentOriginationExactUniversalEquivalenceLegUniquenessV4_74.lean) converts a source morphism over a fixed equivalence leg into an `ExactPresentationCoherentComparison`, applies target-side `essential_unique`, and packages the resulting StrongTrans isomorphism with `InducedBicategory.isoMk`.

For two source morphisms `f`, `g` over the same forward leg, the conclusion is:

```lean
Nonempty (f.lift ≅ g.lift)
```

There is an analogous backward-leg theorem. This means **existence of an isomorphism between the DO₂ 1-morphisms**; it does not mean that this isomorphism is unique, that the source lifts are equal, or that it automatically extends to a compatible source 2-isomorphism.

## What remains to be proved

Let `r : f.raw -> g.raw` and `l : f.lift -> g.lift` be proposed 2-cell components. The [v4.58 interface](formal/KUOS/DependentOriginationExactUniversalMappingTwoCellV4_58.lean) requires the exact equation:

```text
(restrict(l.hom) ▷ c_Y) ; s_g.hom
  =
s_f.hom ; (c_X ◁ r)
```

Target-side essential uniqueness supplies a candidate DO₂ isomorphism, but **does not supply this compatibility equation**. The next program is:

1. Prove compatible 2-cell lifting under explicit hypotheses, or identify the obstruction; do not assume compatibility from an unstructured DO₂ isomorphism.
2. Lift the raw unit and counit for the chosen forward/backward source morphisms, prove the inverse and required triangle laws, and then construct a source `Bicategory.Equivalence`.
3. Compare the intended semantic admissibility condition with v4.72 liftability for general raw morphisms, and formulate the final mapping/classification theorem with the correct higher variance.

The [ROADMAP](ROADMAP.md) gives proposed milestones and exit criteria. The final mapping equivalence, automatic source-equivalence lifting, and local full faithfulness of realization are **not claimed** at v4.74.

## CI, caching, and reproduction

The [PR governance workflow](.github/workflows/pr-governance-gate.yml) selects affected checks. For Lean changes it restores a compatible `.lake` workspace cache before the selected Lean build; the main-branch [formal-validation workflow](.github/workflows/lean-formal-validation.yml) produces reusable workspace caches after successful builds. PR validation uses restore-only access. Keys distinguish operating system, architecture, toolchain, manifest, and commit; a compatible prefix can restore an earlier workspace.

**Cache reuse is a build optimization, not a theorem receipt.** Changed Lean artifacts still require validation associated with the new head. A cache hit does not guarantee that all dependencies are reusable or that a particular elapsed time will recur.

A README/ROADMAP-only change leaves the theorem artifacts and pins untouched. It should use the selected documentation/runtime checks without manually rerunning Strict Lean. Workflow/runtime changes and theorem changes remain separate lanes.

Using the pinned checkout, the focused current-frontier command used by the repository's CI interface is:

```bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationExactUniversalEquivalenceLegUniquenessV4_74
```

The v4.74 import chain includes v4.73, v4.72, v4.71, strict realization, and the mapping-source structure. The registered aggregate target remains:

```bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
```

Runtime validation is separate:

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py
```

A successful workflow is evidence for its selected commands and checkout, not a blanket assertion that all repository files are warning-free or that every proposed research claim has been formalized.

## Proof-engineering lessons retained

Use the pinned Mathlib APIs; import is not namespace opening, and scoped notation/instances must be opened where needed. Keep `autoImplicit false` and the chosen source-object indices explicit.

For dependent categorical proofs, prefer pure algebra, component/projection lemmas, and small wrappers over global equalities of entire pseudofunctors. Use `congrArg`, extensionality, typed local equalities, and targeted normalization. Use `change` only for definitional equality; retain `eqToHom`/`eqToIso` for genuine transports.

The v4.67 inverse laws use generic compatible-inverse helpers and native `Iso.hom_inv_id`/`Iso.inv_hom_id` directly. The v4.70 strict-core proof normalizes small transport goals **before** projecting through induced-bicategory `.hom`. A generic “apply ext, then simp” recipe is not appropriate at every wrapper boundary. Keep private implementation helpers out of public theorem types.

## Permanent boundaries

```text
weak W-admissibility                 !=> exact presentation / localization
arbitrary exact presentations       !=> equivalent universal targets
arbitrary one-way raw morphism      !=> liftable morphism or equivalence
DO₂ isomorphism of lifts            !=> compatible source 2-isomorphism
two source morphisms in opposite directions !=> source adjoint equivalence
strict realization pseudofunctor    !=> final universal mapping property
runtime/docs/cache success          !=> theorem authority
```

**Current research statement:** KuuOS has a genuine exact-universal mapping source bicategory and a strict DO₂ realization. Coherent raw-equivalence legs lift to source morphisms and have DO₂ realizations unique up to isomorphism. The next substantive boundary is compatible source 2-cell lifting and unit/counit coherence, followed by the final dependent-origination mapping property—not reconstruction of the already installed bicategory.
