# KuuOS / 空OS

![KuuOS PR Governance Gate](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/pr-governance-gate.yml/badge.svg)
![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS** is a public research architecture for dependent origination (縁起), contextual transport, higher coherence, descent, obstruction, correction, recursive carriers, and bounded AI operation. Founder: **Hidetoshi Itakura / 板倉英俊**.

> Which structure survives justified changes of context and presentation, how can compatible local information be transported and glued, and which universal property characterizes the invariant content?

## Current formal status

**The integrated theorem spine is now through v4.95.**

Two levels must be kept distinct.

1. **Object-labelled sector — closed through v4.89.**  
   For the chosen exact-universal source objects, the realization has hom-category equivalences, a coherent inverse section pseudofunctor, global source/unit and realized/counit StrongTrans data, and a Whitehead-style biequivalence certificate for the object-labelled realized sector.

2. **Full ambient DO₂ — still open, but the current route is now much narrower.**  
   v4.90 proves ambient Whitehead existence for the actual realization is equivalent to object coverage. v4.91–v4.95 provide the current constructive route:

   ```text
   StrongTrans coherence-extension data for every raw StrongTrans
              |
              |  v4.95
              v
   restriction Hom EssSurj
              |
              |  v4.94  (Full is unconditional)
              |  v4.93  (Faithful is unconditional)
              v
   restriction Hom equivalence
              |
              |  v4.92
              v
   canonical restriction presentation is universal
              |
              |  v4.91
              v
   ambient object coverage
              |
              |  v4.90  iff
              v
   ambient Whitehead existence
   ```

v4.94 closes **restriction Full** unconditionally by canonically extending modification components and proving naturality on all localized arrows with Mathlib localization generation. v4.95 then canonically extends **StrongTrans object components** and proves that a precise package of localized naturality/coherence data implies restriction EssSurj and hence ambient Whitehead existence through the chain above.

The remaining P4 frontier is therefore **not** Full and is **not** object-component reconstruction. It is construction, for every raw StrongTrans, of the explicit `HigherLocalizedStrongTransCoherenceExtension` package: localized naturality isomorphisms, 2-cell naturality, identity coherence, composition coherence, and exact agreement with the raw restriction square.

Ambient Whitehead existence is **not yet claimed unconditionally** because existence of that coherence-extension package is still open.

Philosophical interpretation, formal proof, CI validation, runtime validation, and operational authority remain distinct. [ROADMAP](ROADMAP.md) records the precise closed results and next obligations; [docs/LEAN4_BUILD.md](docs/LEAN4_BUILD.md) describes the pinned build environment.

## Canonical theorem snapshot — 2026-10-01 JST

| Role | Reference |
| --- | --- |
| Canonical branch | **main** — re-observe before new work |
| Observed main before this docs-only refresh | **`77b19267e817fafbd9d6aa850d3ffa88f0d3281f`** |
| Latest theorem-bearing baseline | **`77b19267e817fafbd9d6aa850d3ffa88f0d3281f`** |
| Latest theorem merge | [#1935 — StrongTrans extension reduction v4.95](https://github.com/itakura-hidetoshi/KuuOS/pull/1935) |
| Final validated PR head | `4f769f847e6d3c6720114af046450c03285637ba` |
| Associated validation | [Run #3329 / 36813797496](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/36813797496): completed / success |
| Exact-head receipts | Strict Lean: success; exact-head terminal: success |
| Lean artifact | `11141346204` |
| Artifact digest | `sha256:7b1ff1be49d11719aba70e232cdde6c70de67e2b580a0d4d2cf94a444d27e24e` |
| Build result | `Build completed successfully (8614 jobs)` |
| Lean / Mathlib | `leanprover/lean4:v4.30.0-rc2` / `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |

The v4.95 module's public axiom queries contain only the ordinary Mathlib axioms used throughout this spine:

```text
propext
Classical.choice
Quot.sound
```

There is no `sorryAx`.

The immutable theorem file at the theorem-bearing baseline is [DependentOriginationExactUniversalAmbientStrongTransExtensionV4_95.lean](https://github.com/itakura-hidetoshi/KuuOS/blob/77b19267e817fafbd9d6aa850d3ffa88f0d3281f/formal/KUOS/DependentOriginationExactUniversalAmbientStrongTransExtensionV4_95.lean).

A later README/ROADMAP-only merge may advance `main`; that does **not** create a newer theorem-bearing baseline.

```text
fresh exact canonical GitHub SHA
  > formal Lean theorem artifacts at that SHA
  > README / ROADMAP
  > exact-head CI/runtime receipts
  > history / memory
```

[#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) remains the separate Lean 4.31 validation-only lane. Keep it draft and unmerged; do not mark it Ready for review, enable auto-merge, or use it to alter the canonical pin.

## What 空 means here

空 is not “nothing exists.” Its operational role is non-reification: a chosen presentation is not intrinsic substance, a local observation is not global truth, and runtime success is not WORLD truth.

KuuOS therefore separates observation from inference, identifies the active context, retains multiple compatible presentations, follows relations and history, checks local compatibility and descent, exposes obstructions, respects authority boundaries, performs only justified actions, and re-observes afterward.

The formal program is richer than a graph. It contains contextual systems, mappings between systems, transformations between mappings, higher coherence, quotient/descent structure, obstructions, universal properties, and explicit presentation-localization interfaces. This is a mathematical model of dependent-origination structure, not a claim to the unique formal interpretation of Buddhist philosophy.

## Three formal layers

### Source

`ExactUniversalRawObject` is the chosen exact-universal source sector. A source object stores a raw Cat-valued contextual system, an exact DO₂ presentation, its comparison StrongTrans, and a coherent universal-target witness.

Source 1-cells and 2-cells store compatible raw and DO₂ data. The native source bicategory is constructed in v4.69.

### Object-labelled realized sector

The v4.85 realized sector retains the **same source-object labels**, while its hom categories use the corresponding DO₂ one-cells and two-cells.

This retention is deliberate. Equivalent realized carriers do not erase different source presentations, contextual histories, or world bindings.

### Ambient DO₂

The ambient completion contains arbitrary DO₂ objects, not merely those already labelled by source objects.

The distinction between the labelled sector and ambient DO₂ is the current object-coverage problem.

## Integrated mathematical spine

| Versions | Closed result | Main anchors |
| --- | --- | --- |
| v4.00–v4.12 | Exact C2 nonfactorization and nonzero Stage-II obstruction in `ZMod 2` | [v4.00](formal/KUOS/DependentOriginationAbstractNonfactorizationV4_00.lean), [v4.12](formal/KUOS/DependentOriginationStageIIObstructionClassV4_12.lean) |
| v4.13–v4.48 | Incidence/capacity obstructions, recursive/inverse-limit carriers, exact Cantor dimension, switch/orientation descent | [v4.40](formal/KUOS/DependentOriginationStageIIExactFractalCertificateV4_40.lean), [v4.48](formal/KUOS/DependentOriginationStageIIOrbitOrientationDescentV4_48.lean) |
| v4.49–v4.70 | Abstract presentation descent, exact presentation sector, native source bicategory, strict realization | [v4.49](formal/KUOS/DependentOriginationAbstractPresentationDescentV4_49.lean), [v4.69](formal/KUOS/DependentOriginationExactUniversalMappingBicategoryV4_69.lean), [v4.70](formal/KUOS/DependentOriginationExactUniversalRealizationStrictPseudofunctorV4_70.lean) |
| v4.71–v4.83 | Liftability, 2-cell full faithfulness, pointwise inverse coherence, arbitrary DO₂ 1-cell lifting between chosen carriers, hom-category equivalences | [v4.77](formal/KUOS/DependentOriginationExactUniversalRealizationFullyFaithfulV4_77.lean), [v4.82](formal/KUOS/DependentOriginationPointwiseInverseCoherenceV4_82.lean), [v4.83](formal/KUOS/DependentOriginationExactUniversalHomEquivalenceV4_83.lean) |
| v4.84–v4.89 | Section pseudofunctor, labelled strict realization, global unit/counit StrongTrans, Whitehead certificate on the object-labelled sector | [v4.84](formal/KUOS/DependentOriginationExactUniversalSectionPseudofunctorV4_84.lean), [v4.87](formal/KUOS/DependentOriginationExactUniversalGlobalUnitStrongTransV4_87.lean), [v4.88](formal/KUOS/DependentOriginationExactUniversalGlobalCounitStrongTransV4_88.lean), [v4.89](formal/KUOS/DependentOriginationExactUniversalLabelledBiequivalenceV4_89.lean) |
| v4.90–v4.95 | Ambient Whitehead reduced to object coverage and restriction universality; restriction Faithful and Full closed unconditionally; remaining EssSurj reduced to explicit StrongTrans coherence-extension data | [v4.90](formal/KUOS/DependentOriginationExactUniversalAmbientCoverageReductionV4_90.lean), [v4.93](formal/KUOS/DependentOriginationExactUniversalAmbientRestrictionFaithfulSplitV4_93.lean), [v4.94](formal/KUOS/DependentOriginationExactUniversalAmbientRestrictionFullV4_94.lean), [v4.95](formal/KUOS/DependentOriginationExactUniversalAmbientStrongTransExtensionV4_95.lean) |

The positive exact-universal results do **not** erase the earlier obstruction theorem:

```text
weak W-admissibility can hold
while exact localization / exact presentation is impossible.
```

Exactness, chosen presentation, and coherent universality remain explicit sector hypotheses.

## Recent theorem chain — v4.87–v4.95

### v4.87 — global source unit StrongTrans

[v4.87 / #1926](formal/KUOS/DependentOriginationExactUniversalGlobalUnitStrongTransV4_87.lean) bundles the v4.86 source-roundtrip unit squares into a native Mathlib

```text
Id_Source ⟶ S ∘ R
```

StrongTrans. Naturality in 2-cells and identity/composition coherence are reflected back from DO₂ using realization faithfulness.

### v4.88 — global realized counit StrongTrans

[v4.88 / #1927](formal/KUOS/DependentOriginationExactUniversalGlobalCounitStrongTransV4_88.lean) constructs the realized-side comparison

```text
R ∘ S ⟶ Id_RealizedSector.
```

Its object components are identities and its coherence reduces to native bicategory coherence in the induced realized bicategory.

### v4.89 — object-labelled Whitehead biequivalence certificate

[v4.89 / #1928](formal/KUOS/DependentOriginationExactUniversalLabelledBiequivalenceV4_89.lean) packages:

- the labelled realization pseudofunctor;
- equivalences on every hom category;
- exact agreement of those equivalences' forward functors with realization;
- object essential surjectivity inside the labelled sector;
- the chosen section, v4.87 unit, and v4.88 counit.

Because Source and RealizedSector have the same object labels, object coverage here is reflexive.

This is a Whitehead-style biequivalence certificate for the **object-labelled sector**. It is not asserted to be a stronger tricategorical adjoint-biequivalence package with triangle modifications, and it does not cover arbitrary ambient DO₂ objects.

### v4.90 — ambient Whitehead iff object coverage

[v4.90 / #1929](formal/KUOS/DependentOriginationExactUniversalAmbientCoverageReductionV4_90.lean) proves for the actual v4.70 realization:

```lean
ExactUniversalAmbientWhiteheadExistence
  ↔
ExactUniversalAmbientObjectCoverage
```

The local hom-equivalence part is already available from v4.83; only object coverage remains.

### v4.91 — canonical restriction universality is sufficient for coverage

[v4.91 / #1930](formal/KUOS/DependentOriginationExactUniversalAmbientRestrictionUniversalityV4_91.lean) takes arbitrary ambient `Z`, restricts its localized pseudofunctor back to the raw context, and forms the tautological presentation with carrier literally `Z` and identity comparison.

The tautological part is automatic. The nontrivial requirement is that this presentation be a coherent universal target. Uniformly assuming that property constructs a source object whose carrier is literally each ambient `Z`, hence ambient coverage.

### v4.92 — restriction hom equivalence implies restriction universality

[v4.92 / #1931](formal/KUOS/DependentOriginationExactUniversalAmbientRestrictionHomEquivalenceV4_92.lean) packages restriction as a functor on StrongTrans hom categories:

```text
localized StrongTrans / modifications
          |
          | restriction
          v
raw StrongTrans / modifications.
```

If this functor is an equivalence for every relevant pair, essential surjectivity gives factor existence and full faithfulness gives essential uniqueness. Therefore the v4.91 canonical restriction presentation is universal.

### v4.93 — faithfulness is unconditional

[v4.93 / #1932](formal/KUOS/DependentOriginationExactUniversalAmbientRestrictionFaithfulSplitV4_93.lean) uses Mathlib's constructed-localization object equivalence

```lean
Context ≃ W.Localization
```

and StrongTrans modification extensionality to prove restriction is faithful on every hom category without additional hypotheses.

It proves:

```lean
ExactUniversalAmbientRestrictionHomEquivalence
  ↔
ExactUniversalAmbientRestrictionHomFull
  ∧
ExactUniversalAmbientRestrictionHomEssSurj
```

### v4.94 — restriction Full is unconditional

[v4.94 / #1934](formal/KUOS/DependentOriginationExactUniversalAmbientRestrictionFullV4_94.lean) canonically reconstructs modification components on localized objects using `Localization.Construction.objEquiv`.

Modification naturality is encoded as a `MorphismProperty` on the localized base. The image-arrow case comes from the given raw modification; composition, identity, and inverse stability are proved with pinned bicategory coherence; then `Localization.Construction.morphismProperty_eq_top'` promotes the square to every localized arrow.

The resulting extension proves:

```lean
(higherLocalizedRestrictionHomFunctor ...).Full
```

without a new semantic hypothesis. Hence the ambient local-equivalence condition is reduced further:

```lean
ExactUniversalAmbientRestrictionHomEquivalence
  ↔
ExactUniversalAmbientRestrictionHomEssSurj
```

and EssSurj alone is sufficient for the v4.91–v4.90 route to ambient Whitehead existence.

### v4.95 — EssSurj reduced to explicit StrongTrans coherence extension

[v4.95 / #1935](formal/KUOS/DependentOriginationExactUniversalAmbientStrongTransExtensionV4_95.lean) removes object reconstruction from the remaining 1-cell problem.

For every raw StrongTrans `gamma`, its object components extend canonically to every localized object. The remaining data are packaged as `HigherLocalizedStrongTransCoherenceExtension`:

- a localized naturality isomorphism on every localized 1-cell;
- naturality with respect to 2-cells;
- identity coherence;
- composition coherence;
- the exact forward modification-naturality square on raw presentation arrows.

Such data assemble into a genuine localized StrongTrans, and its restriction is isomorphic to `gamma`. Therefore:

```lean
HigherLocalizedStrongTransExtensionExists ...
  -> (higherLocalizedRestrictionHomFunctor ...).EssSurj
```

and the ambient version implies `ExactUniversalAmbientWhiteheadExistence`.

This is a **reduction theorem**, not an unconditional construction of the extension data. The remaining P4 obstruction is now exactly the construction of that coherence package.

## Closed versus open

### Closed

- obstruction/nonfactorization countermodels;
- exact presentation and coherent universal-target sector;
- native source bicategory and strict realization;
- compatible 2-cell full faithfulness;
- arbitrary DO₂ 1-cell exact lift between existing chosen carriers;
- hom-category equivalences for existing source objects;
- coherent section pseudofunctor;
- label-preserving strict realization;
- global source unit StrongTrans;
- global realized counit StrongTrans;
- Whitehead-style biequivalence certificate on the object-labelled sector;
- ambient Whitehead existence iff ambient object coverage;
- canonical restriction-universality sufficient condition for coverage;
- local restriction hom-equivalence sufficient condition for that universality;
- unconditional faithfulness of the restriction hom functor;
- unconditional fullness of the restriction hom functor;
- restriction hom-equivalence iff restriction EssSurj;
- canonical extension of raw StrongTrans **object components** to all localized objects;
- reduction of restriction EssSurj to explicit StrongTrans naturality/coherence-extension data.

### Still open

1. **StrongTrans coherence extension:** for every raw StrongTrans between restrictions, construct `HigherLocalizedStrongTransCoherenceExtension`.
2. Use that construction with v4.95 and v4.94 to close restriction EssSurj, local restriction hom equivalence, ambient coverage, and ambient Whitehead existence through the current sufficient route.
3. Independently prescribed raw 2-cell / unit / counit data rather than allowing compatibility to determine the raw component.
4. Semantic admissibility versus exact liftability, without defining one tautologically from the other.
5. The final higher dependent-origination mapping/classification theorem, with target sector, variance, descent, presentation/world labels, and naturality explicit.

## Immediate proof frontier

The next theorem unit should attack **construction of the v4.95 StrongTrans coherence-extension package**, not restriction Full.

For a raw

```text
gamma : restrict(F) ⟶ restrict(G)
```

v4.95 already supplies the component

```text
higherLocalizedStrongTransExtensionApp gamma Y
```

at every localized object `Y`.

What remains is to construct, coherently:

1. `naturality f` for every localized 1-cell `f`;
2. `naturality_naturality` for localized 2-cells;
3. `naturality_id`;
4. `naturality_comp`;
5. the exact raw-arrow modification square required by restriction.

A promising route is to use the localization presentation/generation API to extend the naturality isomorphisms from presentation arrows and inverted arrows while proving relation invariance and bicategorical coherence. Ordinary 1-categorical `Localization.functorEquivalence` remains background only; it does not by itself construct a pseudonatural StrongTrans.

Exit criterion:

```lean
HigherLocalizedStrongTransExtensionExists (W := W) F G
```

for the ambient stack carriers required by v4.95. Once that is closed, v4.95 gives EssSurj, v4.94 upgrades it to local hom equivalence, and v4.92–v4.90 finish the current ambient Whitehead route.

## CI, caching, and reproduction

The latest theorem was validated with:

```bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationExactUniversalAmbientStrongTransExtensionV4_95
```

The theorem target completed successfully with **8614 jobs** at exact PR head `4f769f847e6d3c6720114af046450c03285637ba`.

To reproduce the current major endpoints:

```bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationExactUniversalLabelledBiequivalenceV4_89 \
  KUOS.DependentOriginationExactUniversalAmbientRestrictionFullV4_94 \
  KUOS.DependentOriginationExactUniversalAmbientStrongTransExtensionV4_95
```

Aggregate and runtime entry points remain:

```bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
PYTHONPATH=. python3 runtime/kuuos_current_check.py
```

Cache reuse is a build optimization, never theorem authority. A selected successful target build is not automatically a repository-wide warning-free certificate.

**README/ROADMAP-only changes do not require manually rerunning an already successful Strict Lean theorem build.** Documentation merges advance `main`, not theorem authority.

## Proof-engineering lessons

Recent Lean work reinforced several rules:

- imports expose declarations but do not open their namespaces;
- `change` requires definitional equality;
- generated universe parameter order must be checked rather than guessed;
- universes appearing only in a proposition body may need explicit `.{...}` instantiation at call sites;
- dependent endpoints should be fixed before elaborating fields such as adjunctions, preimages, or hom equivalences;
- structure fields whose type is itself a higher-order function must be bound according to the exact field type;
- in particular, `Functor.Faithful.map_injective` has type  
  `∀ {X Y}, Function.Injective F.map`, so the hom objects and the two morphisms being compared are separate binder layers;
- after a rewrite closes the goal definitionally, do not append a redundant `rfl`;
- use StrongTrans modification extensionality only after the correct hom-category endpoints are fixed;
- preserve explicit universe and category endpoints instead of relying on broad elaboration through wrappers.
- when a categorical equality is followed by more composition, prefer Mathlib's reassociated form such as `reassoc_of% h` rather than forcing a raw rewrite;
- pretty-printed bicategorical expressions can look identical while elaborated coercions prevent `rw` from matching; when an API requires an exact coherence square, store/prove that square in its native type instead of compressing it to a weaker equality and reconstructing it later;
- dependent rewrites may introduce casts; when the component is definitionally the same object, prefer direct terms such as `Iso.refl _` over rewriting through dependent endpoints.

These are proof-structure rules, not reasons to add axioms, suppress warnings, broaden transparency, or increase resource limits.

## Current research statement

The object-labelled exact-universal sector has a completed Whitehead-style biequivalence certificate. For the full ambient DO₂ bicategory, ambient Whitehead existence is equivalent to object coverage, and the current constructive route has now closed both modification-level infrastructure obligations:

```text
Faithful  — CLOSED in v4.93
Full      — CLOSED in v4.94
```

v4.95 also closes the **object-component reconstruction** part of StrongTrans extension. The remaining mathematical frontier is precisely the coherent 1-cell data:

```text
localized naturality isomorphisms
+ 2-cell naturality
+ identity coherence
+ composition coherence
+ exact raw-arrow restriction square
```

Constructing that package for every raw StrongTrans would give restriction EssSurj by v4.95, restriction hom equivalence by v4.94, canonical restriction universality by v4.92, ambient object coverage by v4.91, and ambient Whitehead existence by v4.90.

Until that coherence-extension existence theorem is proved, arbitrary ambient DO₂ objects are **not** claimed to be represented by source objects.
