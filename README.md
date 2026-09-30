# KuuOS / 空OS

![KuuOS PR Governance Gate](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/pr-governance-gate.yml/badge.svg)
![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS** is a public research architecture for dependent origination (縁起), contextual transport, higher coherence, descent, obstruction, correction, recursive carriers, and bounded AI operation. Founder: **Hidetoshi Itakura / 板倉英俊**.

> Which structure survives justified changes of context and presentation, how can compatible local information be transported and glued, and which universal property characterizes the invariant content?

## Current formal status

**The integrated theorem spine is now through v4.93.**

Two levels must be kept distinct.

1. **Object-labelled sector — closed through v4.89.**  
   For the chosen exact-universal source objects, the realization has hom-category equivalences, a coherent inverse section pseudofunctor, a global source-side unit StrongTrans, a global realized-side counit StrongTrans, and a Whitehead-style biequivalence certificate for the object-labelled realized sector.

2. **Full ambient DO₂ — still open.**  
   v4.90 proves that ambient Whitehead existence for the actual realization is equivalent to object coverage. v4.91–v4.93 then give a concrete sufficient route to that coverage:
   
   ```text
   restriction Hom Full + restriction Hom EssSurj
              |
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

The crucial new v4.93 result is that **restriction on StrongTrans hom categories is already faithful without any new hypothesis**. The genuine P4 frontier is therefore reduced to:

- **Full:** extension of raw modifications to localized modifications;
- **EssSurj:** extension of raw StrongTrans to localized StrongTrans up to isomorphism.

Neither of those two remaining obligations is claimed unconditionally yet.

Philosophical interpretation, formal proof, CI validation, runtime validation, and operational authority remain distinct. [ROADMAP](ROADMAP.md) records the precise closed results and next obligations; [docs/LEAN4_BUILD.md](docs/LEAN4_BUILD.md) describes the pinned build environment.

## Canonical theorem snapshot — 2026-10-01 JST

| Role | Reference |
| --- | --- |
| Canonical branch | **main** — re-observe before new work |
| Observed main before this docs-only refresh | **`6d4ef51705a71b25e167bc8a766fc6f43e89ef2e`** |
| Latest theorem-bearing baseline | **`6d4ef51705a71b25e167bc8a766fc6f43e89ef2e`** |
| Latest theorem merge | [#1932 — restriction faithfulness split v4.93](https://github.com/itakura-hidetoshi/KuuOS/pull/1932) |
| Final validated PR head | `8be3321da513de1d2bd881ab9457e652b316b883` |
| Associated validation | [Run #3303 / 36783070351](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/36783070351): completed / success |
| Exact-head receipts | Strict Lean: success; exact-head terminal: success |
| Lean artifact | `11129581377` |
| Artifact digest | `sha256:42164e397ab008644d7d7749c03f74a0a0423c31246a33ea18a8cd5b55409520` |
| Build result | `Build completed successfully (8612 jobs)` |
| Lean / Mathlib | `leanprover/lean4:v4.30.0-rc2` / `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |

The v4.93 module's public axiom queries contain only the ordinary Mathlib axioms used throughout this spine:

```text
propext
Classical.choice
Quot.sound
```

There is no `sorryAx`.

The immutable theorem file at the theorem-bearing baseline is [DependentOriginationExactUniversalAmbientRestrictionFaithfulSplitV4_93.lean](https://github.com/itakura-hidetoshi/KuuOS/blob/6d4ef51705a71b25e167bc8a766fc6f43e89ef2e/formal/KUOS/DependentOriginationExactUniversalAmbientRestrictionFaithfulSplitV4_93.lean).

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
| v4.90–v4.93 | Ambient Whitehead reduced to object coverage, then to canonical restriction universality, then to local restriction hom equivalence; restriction faithfulness closed unconditionally | [v4.90](formal/KUOS/DependentOriginationExactUniversalAmbientCoverageReductionV4_90.lean), [v4.91](formal/KUOS/DependentOriginationExactUniversalAmbientRestrictionUniversalityV4_91.lean), [v4.92](formal/KUOS/DependentOriginationExactUniversalAmbientRestrictionHomEquivalenceV4_92.lean), [v4.93](formal/KUOS/DependentOriginationExactUniversalAmbientRestrictionFaithfulSplitV4_93.lean) |

The positive exact-universal results do **not** erase the earlier obstruction theorem:

```text
weak W-admissibility can hold
while exact localization / exact presentation is impossible.
```

Exactness, chosen presentation, and coherent universality remain explicit sector hypotheses.

## Recent theorem chain — v4.87–v4.93

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

Therefore:

```lean
ExactUniversalAmbientRestrictionHomEquivalence
  ↔
ExactUniversalAmbientRestrictionHomFull
  ∧
ExactUniversalAmbientRestrictionHomEssSurj
```

The remaining higher-localization frontier is now sharply separated into **2-cell extension (Full)** and **1-cell extension up to iso (EssSurj)**.

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
- unconditional faithfulness of the restriction hom functor.

### Still open

1. **Restriction Full:** extend arbitrary raw modifications between restricted StrongTrans to localized modifications.
2. **Restriction EssSurj:** extend arbitrary raw StrongTrans to localized StrongTrans up to isomorphism.
3. Use those results, if proved, to close the current sufficient route to ambient coverage and ambient Whitehead existence.
4. Independently prescribed raw 2-cell / unit / counit data rather than allowing compatibility to determine the raw component.
5. Semantic admissibility versus exact liftability, without defining one tautologically from the other.
6. The final higher dependent-origination mapping/classification theorem, with target sector, variance, descent, presentation/world labels, and naturality explicit.

## Immediate proof frontier

The next natural theorem unit is the **Full** side.

Mathlib's localization construction provides morphism-generation principles such as `Localization.Construction.morphismProperty_eq_top` / `morphismProperty_eq_top'`: a property holding on image morphisms, stable under composition, and stable under inverted arrows can be promoted to all localized morphisms.

A plausible v4.94 route is therefore:

1. start from a raw modification between restricted localized StrongTrans;
2. reconstruct candidate components on localized objects using the canonical object equivalence;
3. encode modification naturality as a morphism property;
4. prove it on presentation-unit image arrows;
5. prove stability under composition and inverses;
6. invoke the localization generation theorem;
7. obtain a genuine localized modification and prove its restriction is the original one.

This is a **planned route**, not yet a theorem.

After Full, EssSurj remains the harder pseudonatural 1-cell extension problem.

## CI, caching, and reproduction

The latest theorem was validated with:

```bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationExactUniversalAmbientRestrictionFaithfulSplitV4_93
```

The theorem target completed successfully with 8612 jobs.

To reproduce the current major endpoints:

```bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationExactUniversalLabelledBiequivalenceV4_89 \
  KUOS.DependentOriginationExactUniversalAmbientRestrictionFaithfulSplitV4_93
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

These are proof-structure rules, not reasons to add axioms, suppress warnings, broaden transparency, or increase resource limits.

## Current research statement

The object-labelled exact-universal sector now has a completed Whitehead-style biequivalence certificate. For the full ambient DO₂ bicategory, the only missing Whitehead condition is object coverage, and the current constructive route has reduced that problem to local presentation-localization extension.

Within that route, **faithfulness is closed**. The immediate mathematical frontier is precisely:

```text
Full      = extend raw modifications
EssSurj   = extend raw StrongTrans up to isomorphism
```

Closing those two obligations would complete the current v4.91–v4.93 route to ambient object coverage and therefore, by v4.90, ambient Whitehead existence—without collapsing distinct presentations or silently identifying weak admissibility with exactness.
