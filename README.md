# KuuOS / 空OS

![KuuOS PR Governance Gate](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/pr-governance-gate.yml/badge.svg)
![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS** is a public research architecture for dependent origination (縁起), contextual transport, higher coherence, descent, obstruction, correction, recursive carriers, and bounded AI operation. Founder: **Hidetoshi Itakura / 板倉英俊**.

> Which structure survives justified changes of context and presentation, how can compatible local information be transported and glued, and which universal property characterizes the invariant content?

**現在の到達点：v4.79。** 選択済み exact-universal sector で、source は Mathlib の双圏、DO₂ への実現は strict pseudofunctor です。その各 hom 関手の充満忠実性、coherent raw equivalence からの source 随伴同値、固定した１射対における随伴構造の一対一対応まで証明・統合済みです。**任意の DO₂ の１射の持ち上げと、最終的な高次写像性は、まだ別の証明課題です。**

Philosophical interpretation, formal proof, runtime validation, and operational authority remain distinct. [ROADMAP](ROADMAP.md) records the precise completed statements and next obligations; [docs/LEAN4_BUILD.md](docs/LEAN4_BUILD.md) describes the build environment.

## Canonical theorem snapshot — 2026-09-29 JST

| Role | Reference |
| --- | --- |
| Canonical branch | **main** — re-observe before new work |
| Observed main before this docs-only refresh | `b239068dbcfaf8d3e0bce101e7402f9cede34c9f` |
| Latest theorem-bearing baseline | **`b239068dbcfaf8d3e0bce101e7402f9cede34c9f`** |
| Latest theorem merge | [#1916 — adjunction lifting v4.79](https://github.com/itakura-hidetoshi/KuuOS/pull/1916) |
| Validated PR head | `e470e1269715582b9f8a0746aa213a0447132d79` |
| Tested synthetic merge checkout | `617d8fb2667324d3f078a609175da77d4ab05f4d` |
| Associated validation | [Run #3250 / 36563945324](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/36563945324), attempt 1: success; both exact-head Lean and terminal receipts: success |
| Lean / Mathlib | `leanprover/lean4:v4.30.0-rc2` / `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |

The v4.79 module builds successfully and contains 15 regression examples. All seven printed axiom dependencies contain only `propext`, `Classical.choice`, and `Quot.sound`; none contains `sorryAx`. The [immutable Lean artifact](https://github.com/itakura-hidetoshi/KuuOS/blob/b239068dbcfaf8d3e0bce101e7402f9cede34c9f/formal/KUOS/DependentOriginationExactUniversalAdjunctionLiftingV4_79.lean), rather than a badge, specifies the theorem.

The observed-main SHA is the **input to this refresh**, not its eventual documentation commit. A docs-only merge advances `main` without advancing the theorem-bearing baseline.

```text
fresh exact canonical GitHub SHA
  > formal Lean theorem artifacts at that SHA
  > README / ROADMAP
  > exact-head CI/runtime receipts
  > history / memory
```

[#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) remains the separate Lean 4.31 validation-only lane: keep it draft and unmerged; do not mark Ready for review, enable auto-merge, or change the canonical pins through it.

## What 空 means here

空 is not “nothing exists.” Its operational role is non-reification: a chosen presentation is not intrinsic substance, a local observation is not global truth, and runtime success is not WORLD truth. KuuOS separates observation from inference, retains alternative presentations, follows relations and history, checks compatibility and descent, identifies obstructions, respects the relevant authority boundary, and updates after re-observation.

The formal program goes beyond a graph: it includes contextual systems, mappings between them, transformations between mappings, and coherence under composition. This is a mathematical model of dependent-origination structure, not a claim to the unique formal interpretation of Buddhist philosophy.

## The exact-universal source and its realization

A source object `X` stores a raw Cat-valued contextual system, a chosen exact DO₂ presentation, and a coherent universal-target witness. A source 1-cell `f : X ⟶ Y` stores a raw StrongTrans, a DO₂ lift, and an invertible comparison square. A source 2-cell `eta : f ⟶ g` stores raw/lift modifications satisfying compatibility:

```text
s_f : restrict(f.lift) ; c_Y ≅ c_X ; f.raw

(restrict(eta.lift.hom) ▷ c_Y) ; s_g.hom
  = s_f.hom ; (c_X ◁ eta.raw)
```

The [v4.69 source bicategory](formal/KUOS/DependentOriginationExactUniversalMappingBicategoryV4_69.lean) has hom categories, whiskering, horizontal interchange, structural isomorphisms, pentagon, and triangle. The [v4.70 strict realization](formal/KUOS/DependentOriginationExactUniversalRealizationStrictPseudofunctorV4_70.lean) acts by:

```text
X   |-> X.carrier
f   |-> f.lift
eta |-> eta.lift
```

Strict realization is not the assertion that the source bicategory itself is strict. Source objects still include their chosen presentations; the formalization does not erase distinct contextual worlds or operational bindings.

## Integrated mathematical spine

| Versions | Completed result | Entry point |
| --- | --- | --- |
| v4.00–v4.12 | Octahedral C2 nonfactorization; transport-independent nonzero Stage-II class in `ZMod 2` | [Nonfactorization](formal/KUOS/DependentOriginationAbstractNonfactorizationV4_00.lean), [Obstruction class](formal/KUOS/DependentOriginationStageIIObstructionClassV4_12.lean) |
| v4.13–v4.48 | Incidence/capacity tests, recursive and inverse-limit carriers, exact Cantor dimension, middle-switch and orientation descent | [Exact fractal certificate](formal/KUOS/DependentOriginationStageIIExactFractalCertificateV4_40.lean), [Orientation descent](formal/KUOS/DependentOriginationStageIIOrbitOrientationDescentV4_48.lean) |
| v4.49–v4.56 | Abstract presentation descent; exact sector; universal-target comparison, uniqueness, transport, and DO₂ equivalence | [Presentation descent](formal/KUOS/DependentOriginationAbstractPresentationDescentV4_49.lean), [Exact sector](formal/KUOS/DependentOriginationExactHigherPresentationSectorV4_50.lean), [Universal-target equivalence](formal/KUOS/DependentOriginationExactUniversalTargetDO2EquivalenceV4_56.lean) |
| v4.57–v4.70 | Compatible mapping objects/1-cells/2-cells, source bicategory, strict realization | [Mapping interface](formal/KUOS/DependentOriginationExactUniversalMappingMorphismV4_57.lean), [Strict realization](formal/KUOS/DependentOriginationExactUniversalRealizationStrictPseudofunctorV4_70.lean) |
| v4.71–v4.74 | Realized-object invariance; presentation-indexed raw liftability; both raw-equivalence legs lift; their DO₂ lifts are isomorphic | [Liftability](formal/KUOS/DependentOriginationExactUniversalMorphismLiftabilityV4_72.lean), [Leg existence](formal/KUOS/DependentOriginationExactUniversalEquivalenceLegLiftabilityV4_73.lean), [Leg uniqueness](formal/KUOS/DependentOriginationExactUniversalEquivalenceLegUniquenessV4_74.lean) |
| v4.75–v4.79 | Compatible isomorphism classification, actual local full faithfulness, source adjoint equivalences, exact adjunction-data lifting | Detailed below |

Concrete geometry is a validated stress test, not the general definition of dependent origination. The positive exact-universal results do not remove the earlier counterexample:

```text
weak W-admissibility can hold while exact localization/presentation is impossible.
```

## Current results — v4.75–v4.79

### v4.75–v4.77: compatibility, then actual local full faithfulness

[v4.75 / #1912](formal/KUOS/DependentOriginationExactUniversalCompatibleIsoV4_75.lean) embeds each source hom category fully faithfully in Mathlib `Comma`, classifies source isomorphisms by compatible raw/DO₂ isomorphism pairs, and derives inverse compatibility with `Comma.isoMk`. This comma embedding is distinct from DO₂ realization.

[v4.76 / #1913](formal/KUOS/DependentOriginationExactUniversalRealizationFaithfulV4_76.lean) proves that the DO₂ component determines an already compatible source 2-cell. [v4.77 / #1914](formal/KUOS/DependentOriginationExactUniversalRealizationFullyFaithfulV4_77.lean) constructs its preimage for every prescribed DO₂ 2-cell, using the presentation comparison's stored pointwise equivalences. Thus the **actual** realization hom functor is full and faithful:

```lean
(f ⟶ g) ≃ (f.lift ⟶ g.lift)

-- For a prescribed ell : f.lift ⟶ g.lift:
∃! eta : f ⟶ g, eta.lift = ell
```

The construction proves the comparison equation; it does not assume an extra raw component or an extra fullness hypothesis. An isomorphism `f.lift ≅ g.lift` now lifts to a source isomorphism through `exactUniversalSourceIsoOfLift` and Mathlib `preimageIso`.

**Important distinction:** specifying only the DO₂ component determines a unique compatible raw component. Specifying a raw component independently still requires its compatibility with the chosen DO₂ component. Local full faithfulness concerns **2-cells between existing source 1-cells**, not existence of preimages of arbitrary DO₂ 1-cells.

### v4.78: coherent raw equivalence gives a source adjoint equivalence

[v4.78 / #1915](formal/KUOS/DependentOriginationExactUniversalSourceEquivalenceV4_78.lean) proves, for `E : HigherRawSystemCoherentEquivalence X.raw Y.raw`:

```lean
∃ e : Bicategory.Equivalence X Y,
  e.hom.raw = E.forward.comparison ∧
  e.inv.raw = E.backward.comparison
```

The proof combines v4.73 leg existence, universal-target essential uniqueness, and v4.77 isomorphism lifting. It constructs source unit/counit and uses Mathlib `Equivalence.mkOfAdjointifyCounit` for the triangle laws. Both raw **1-cell legs** are retained. The resulting raw unit/counit are not asserted to equal `E.unit`/`E.counit`; adjointification adjusts the chosen source counit.

### v4.79: prescribed DO₂ adjunction data lift exactly

[v4.79 / #1916](formal/KUOS/DependentOriginationExactUniversalAdjunctionLiftingV4_79.lean) fixes source legs `f : X ⟶ Y`, `g : Y ⟶ X` and constructs:

```lean
Bicategory.Adjunction f g ≃ Bicategory.Adjunction f.lift g.lift
```

Strict realization preserves both zigzags; local faithfulness reflects both triangle identities; local fullness supplies the unique compatible unit/counit. **No invertibility is required** for this general adjunction classification. Both Equiv round trips and unique source-adjunction existence are proved.

For prescribed DO₂ unit/counit **isomorphisms** already satisfying the left triangle, `exactUniversalEquivalenceOfLiftTriangle` constructs a native source adjoint equivalence **without adjointification or counit adjustment**. It retains both selected source legs and both complete realized isomorphisms, including their inverses; Mathlib provides the right triangle.

| Input and result | Preserved exactly | Not asserted |
| --- | --- | --- |
| v4.78: coherent raw equivalence → source adjoint equivalence | Raw forward/backward 1-cells | The supplied raw unit/counit |
| v4.79: DO₂ adjunction on fixed source legs → unique source adjunction | DO₂ unit/counit and fixed source legs | Separately prescribed raw unit/counit |

## What remains

The [ROADMAP](ROADMAP.md) separates four next obligations: essential surjectivity of the realization hom functors on **1-cells**; compatibility with independently prescribed raw 2-cell/adjunction data; semantic admissibility versus presentation-indexed exact liftability; and the final higher mapping/classification theorem, including its target sector, variance, and naturality.

Do not rebuild the already proved local fullness, faithfulness, source-equivalence existence, or fixed-leg adjunction classification. Conversely, none of them alone proves arbitrary DO₂ 1-cell liftability, object-level essential surjectivity, or the final biequivalence.

## CI, caching, and reproduction

[PR governance](.github/workflows/pr-governance-gate.yml) selects affected checks and restores compatible `.lake` content; [main formal validation](.github/workflows/lean-formal-validation.yml) produces reusable workspace caches. Cache reuse is a build optimization, not a proof receipt. A changed Lean head still needs validation of its selected targets and checkout.

The successful v4.79 command was:

```bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationExactUniversalAdjunctionLiftingV4_79
```

To reproduce **both** current branches of the theorem spine, include v4.78 explicitly; v4.79 imports v4.77 and v4.70, not v4.78:

```bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationExactUniversalSourceEquivalenceV4_78 \
  KUOS.DependentOriginationExactUniversalAdjunctionLiftingV4_79
```

The registered aggregate target and separate runtime check remain:

```bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
PYTHONPATH=. python3 runtime/kuuos_current_check.py
```

Aggregate coverage depends on the imports in the selected checkout. A selected successful build is not a repository-wide warning-free certificate. Historical dependency linter warnings are not repaired by this documentation update.

**README/ROADMAP-only changes do not require manually rerunning successful Strict Lean.** Keep theorem files, pins, and build configuration unchanged and use the applicable selected documentation/runtime checks. A docs-only receipt does not certify new Lean content.

## Proof-engineering lessons

Keep chosen source objects explicit. For `Functor.map_preimage`, its implicit objects belong to the **source hom category**: they are source 1-cells, not the outer bicategory objects. Supply the same identity/composite endpoints used by `preimageIso`, reversing them for inverse morphisms.

Use typed `Nonempty` witnesses before `Classical.choice`; preserve bundled isomorphisms with `mapIso` instead of asking instance search to rediscover invertibility. Use `congrArg`, appropriate extensionality, explicit `Category.assoc`, and stored inverse laws at small typed boundaries. `change` requires definitional equality; genuine transports use `eqToHom`/`eqToIso`. Read the pinned Mathlib implementation before relying on API names or reducibility.

**Current research statement:** the exact-universal source has a locally fully faithful strict DO₂ realization. Coherent raw equivalences induce source adjoint equivalences with prescribed raw legs, and adjunction structures on fixed source legs are classified exactly by their DO₂ realizations. The next frontier is 1-cell and prescribed-raw-data lifting, then the final higher dependent-origination mapping property.
