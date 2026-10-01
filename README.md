# KuuOS / 空OS

![KuuOS PR Governance Gate](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/pr-governance-gate.yml/badge.svg)
![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS** is a public research architecture for dependent origination (縁起), contextual transport, higher coherence, descent, obstruction, correction, recursive carriers, and bounded AI operation. Founder: **Hidetoshi Itakura / 板倉英俊**.

> Which structure survives justified changes of context and presentation, how can compatible local information be transported and glued, and which universal property characterizes the invariant content?

## Current formal status

**The integrated theorem spine is now through v5.03.**

Two levels remain essential.

1. **Object-labelled exact-universal sector — closed through v4.89.**  
   The labelled realization has hom-category equivalences, a coherent section pseudofunctor, global source/unit and realized/counit StrongTrans data, and a Whitehead-style biequivalence certificate.

2. **Full ambient DO₂ — still open, but the remaining obstruction is now sharply localized.**  
   v4.90–v4.95 reduce ambient Whitehead existence to restriction-hom essential surjectivity and then to StrongTrans extension coherence. v4.96–v5.03 close most of the local ingredients of that extension.

The current constructive route is:

```text
coherent localized StrongTrans naturality family
        |
        |  v4.96
        v
HigherLocalizedStrongTransOneCellCoherenceExtension
        |
        |  v4.95
        v
restriction Hom EssSurj
        |
        |  v4.94  (Full unconditional)
        |  v4.93  (Faithful unconditional)
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
        |  v4.90 iff
        v
ambient Whitehead existence
```

The key change since v4.95 is that the remaining StrongTrans problem is no longer an undifferentiated five-field package:

- **v4.96:** 2-cell naturality is automatic because the source is locally discrete; the frontier reduces to four one-cell/coherence fields.
- **v4.97:** canonical naturality is constructed on presentation-image arrows, with the exact raw restriction square.
- **v4.98:** naturality is constructed on inverses of localized isomorphisms, in particular formal inverses of (W)-arrows.
- **v4.99:** naturality existence is closed under composition.
- **v5.00:** naturality **exists on every localized arrow** via `Localization.Construction.morphismProperty_eq_top'`.
- **v5.01:** the identity naturality choice is fixed canonically and satisfies the exact v4.96 identity equation.
- **v5.02:** presentation naturality on identities and composites is proved to satisfy the native StrongTrans identity/composition coherence equations.
- **v5.03:** a reusable transport constructor along source 1-cell isomorphisms is added; `restrictHigherLocalizedSystem.mapId/mapComp` are decomposed exactly as `Pseudofunctor.comp`; transported identity/composition candidates are defined.

What is **not** yet closed is the coherent global choice. v5.00 gives `Nonempty` for every localized arrow, but arbitrary choice would not automatically satisfy identity/composition coherence or quotient-representative independence.

The immediate frontier is therefore:

```text
presentation canonical choice
  = transported localized canonical choice
      on relations.id / relations.comp
                |
                v
W-inverse relation compatibility
      on Winv₁ / Winv₂
                |
                v
generated-relation / quotient independence
                |
                v
coherent all-arrow naturality family
                |
                v
v4.96 four-field package
                |
                v
restriction EssSurj and ambient P4 route
```

Ambient Whitehead existence is **not yet claimed unconditionally**.

## Canonical theorem snapshot — 2026-10-01 JST

| Role | Reference |
| --- | --- |
| Canonical branch | **main** — re-observe before new work |
| Fresh theorem-bearing baseline | **`3ff43ef5b268bff2852c9ad93bf6f79cf12dcea1`** |
| Latest theorem merge | [#1944 — StrongTrans presentation transport v5.03](https://github.com/itakura-hidetoshi/KuuOS/pull/1944) |
| Exact validated PR head | `86d0b52a07d92428c50f0eec5016d563665f887e` |
| Associated validation | [Run #3348 / 36851206349](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/36851206349): completed / success |
| Exact-head receipts | Strict Lean: success; exact-head terminal: success |
| Lean artifact | `11156825024` |
| Artifact digest | `sha256:9fc0ff932930f9e8702a267d9414e70b05287ed98a684e859329b97913e958fb` |
| Build result | `Build completed successfully (8622 jobs)` |
| Lean / Mathlib | `leanprover/lean4:v4.30.0-rc2` / `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |

The public axiom queries for the v5.03 declarations contain only:

```text
propext
Classical.choice
Quot.sound
```

There is no `sorryAx`.

The latest theorem-bearing module is [DependentOriginationExactUniversalAmbientStrongTransPresentationTransportV5_03.lean](formal/KUOS/DependentOriginationExactUniversalAmbientStrongTransPresentationTransportV5_03.lean).

A later README/ROADMAP-only merge may advance `main`; that does **not** create a newer theorem-bearing baseline.

Authority order is fixed:

```text
fresh exact canonical GitHub SHA
  > formal Lean theorem artifacts at that SHA
  > README / ROADMAP
  > exact-head CI/runtime receipts
  > history / memory
```

[#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) remains a separate Lean 4.31 validation-only lane. It is **open / draft / unmerged** and must stay outside canonical theorem authority.

## What 空 means here

空 is not “nothing exists.” Its operational role is non-reification: a chosen presentation is not intrinsic substance, a local observation is not global truth, and runtime success is not WORLD truth.

KuuOS therefore separates observation from inference, identifies the active context, retains multiple compatible presentations, follows relations and history, checks local compatibility and descent, exposes obstructions, respects authority boundaries, performs only justified actions, and re-observes afterward.

The formal program is richer than a graph. It contains contextual systems, mappings between systems, transformations between mappings, higher coherence, quotient/descent structure, obstructions, universal properties, and explicit presentation-localization interfaces.

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
| v4.71–v4.83 | Liftability, 2-cell full faithfulness, pointwise inverse coherence, arbitrary DO₂ 1-cell lifting between chosen carriers, hom-category equivalences | [v4.77](formal/KUOS/DependentOriginationExactUniversalRealizationFullyFaithfulV4_77.lean), [v4.83](formal/KUOS/DependentOriginationExactUniversalHomEquivalenceV4_83.lean) |
| v4.84–v4.89 | Section pseudofunctor, labelled realization, global unit/counit StrongTrans, Whitehead certificate on the object-labelled sector | [v4.84](formal/KUOS/DependentOriginationExactUniversalSectionPseudofunctorV4_84.lean), [v4.89](formal/KUOS/DependentOriginationExactUniversalLabelledBiequivalenceV4_89.lean) |
| v4.90–v4.95 | Ambient Whitehead reduced to coverage/restriction universality; restriction Faithful and Full unconditional; EssSurj reduced to StrongTrans extension | [v4.90](formal/KUOS/DependentOriginationExactUniversalAmbientCoverageReductionV4_90.lean), [v4.94](formal/KUOS/DependentOriginationExactUniversalAmbientRestrictionFullV4_94.lean), [v4.95](formal/KUOS/DependentOriginationExactUniversalAmbientStrongTransExtensionV4_95.lean) |
| v4.96–v4.99 | Locally-discrete reduction; presentation naturality; W-inverse naturality; composition closure | [v4.96](formal/KUOS/DependentOriginationExactUniversalAmbientStrongTransLocallyDiscreteV4_96.lean), [v4.99](formal/KUOS/DependentOriginationExactUniversalAmbientStrongTransCompositionNaturalityV4_99.lean) |
| v5.00–v5.03 | All-arrow existence; canonical identity; presentation identity/composition coherence; transport bridge and restriction `mapId/mapComp` decomposition | [v5.00](formal/KUOS/DependentOriginationExactUniversalAmbientStrongTransAllArrowNaturalityV5_00.lean), [v5.03](formal/KUOS/DependentOriginationExactUniversalAmbientStrongTransPresentationTransportV5_03.lean) |

The positive exact-universal results do **not** erase the earlier obstruction theorem:

```text
weak W-admissibility can hold
while exact localization / exact presentation is impossible.
```

Exactness, chosen presentation, and coherent universality remain explicit sector hypotheses.

## Current StrongTrans extension chain — v4.95–v5.03

### v4.95 — object components are no longer the obstruction

[v4.95](formal/KUOS/DependentOriginationExactUniversalAmbientStrongTransExtensionV4_95.lean) canonically extends a raw StrongTrans component to every localized object and isolates the remaining coherence data.

### v4.96 — locally discrete source removes 2-cell naturality

[v4.96](formal/KUOS/DependentOriginationExactUniversalAmbientStrongTransLocallyDiscreteV4_96.lean) proves that StrongTrans naturality with respect to source 2-cells is automatic. The remaining package is:

```lean
HigherLocalizedStrongTransOneCellCoherenceExtension
```

with exactly four fields:

- `naturality`
- `naturality_id`
- `naturality_comp`
- `restrict_modification_naturality`

### v4.97 — presentation-image naturality

[v4.97](formal/KUOS/DependentOriginationExactUniversalAmbientStrongTransPresentationNaturalityV4_97.lean) reuses the raw `gamma.naturality` on presentation arrows and proves the exact forward restriction square required by v4.96.

### v4.98 — inverse naturality

[v4.98](formal/KUOS/DependentOriginationExactUniversalAmbientStrongTransWInverseNaturalityV4_98.lean) constructs naturality on inverses of localized isomorphisms by a fully-faithful preimage argument. It specializes this to the formal inverse of every declared (W)-arrow.

### v4.99 — composition closure

[v4.99](formal/KUOS/DependentOriginationExactUniversalAmbientStrongTransCompositionNaturalityV4_99.lean) gives the canonical seven-factor StrongTrans composition constructor and proves pointwise existence is closed under composition.

### v5.00 — every localized arrow has a naturality witness

[v5.00](formal/KUOS/DependentOriginationExactUniversalAmbientStrongTransAllArrowNaturalityV5_00.lean) packages existence as a `MorphismProperty` and applies Mathlib's `Localization.Construction.morphismProperty_eq_top'`.

Therefore every localized arrow carries at least one naturality isomorphism.

**Boundary:** this is only `Nonempty`; it is not yet a coherent global family.

### v5.01 — canonical identity

[v5.01](formal/KUOS/DependentOriginationExactUniversalAmbientStrongTransIdentityNaturalityV5_01.lean) fixes the identity naturality isomorphism to the standard Mathlib formula

```text
mapId(F)
  -> left unitor
  -> right unitor^{-1}
  -> mapId(G)^{-1}
```

and proves the exact v4.96 identity equation.

### v5.02 — presentation identity/composition coherence

[v5.02](formal/KUOS/DependentOriginationExactUniversalAmbientStrongTransPresentationCoherenceV5_02.lean) proves that v4.97 presentation naturality satisfies the native StrongTrans identity and composition fields exactly.

### v5.03 — transport bridge

[v5.03](formal/KUOS/DependentOriginationExactUniversalAmbientStrongTransPresentationTransportV5_03.lean) defines naturality transport along a source 1-cell isomorphism and proves:

```text
restrict(F).mapId
  = F.map₂Iso(P.mapId) ≪≫ F.mapId

restrict(F).mapComp
  = F.map₂Iso(P.mapComp) ≪≫ F.mapComp
```

for the presentation pseudofunctor (P). It then defines transported localized identity and composition candidates on the raw presentation image.

The next theorem unit should prove that those transported candidates are exactly the canonical v4.97 presentation choices.

## Closed versus open

### Closed

- obstruction/nonfactorization countermodels;
- exact presentation and coherent universal-target sector;
- native source bicategory and strict realization;
- compatible 2-cell full faithfulness;
- arbitrary DO₂ 1-cell exact lift between existing chosen carriers;
- hom-category equivalences for existing source objects;
- coherent section pseudofunctor;
- global source unit and realized counit StrongTrans;
- Whitehead-style biequivalence certificate on the object-labelled sector;
- ambient Whitehead existence iff ambient object coverage;
- unconditional restriction Faithful and Full;
- restriction hom-equivalence iff restriction EssSurj;
- canonical extension of raw StrongTrans object components;
- automatic source 2-cell naturality for the remaining extension;
- canonical presentation naturality and exact raw restriction square;
- W-inverse naturality;
- composition closure of naturality existence;
- all-arrow naturality existence;
- canonical identity naturality and identity coherence;
- presentation identity/composition coherence;
- presentation transport bridge and exact restriction `mapId/mapComp` decomposition.

### Still open

1. Prove presentation canonical identity/composition naturality equals the v5.03 transported localized canonical candidates.
2. Prove the corresponding (W)-inverse relation compatibilities (`Winv₁`, `Winv₂`).
3. Propagate those four generator compatibilities through the existing v2.68 retained generated-relation syntax.
4. Descend the resulting canonical naturality data to quotient-independent localized arrows.
5. Assemble `HigherLocalizedStrongTransOneCellCoherenceExtension` for every raw StrongTrans.
6. Use v4.95–v4.90 to close restriction EssSurj, ambient coverage, and ambient Whitehead existence.

Separate later questions remain: independently prescribed raw components/data, semantic admissibility versus exact liftability, and the final higher mapping/classification theorem.

## Proof-engineering lessons retained

- Imported declarations do not import open namespaces; ordinary declarations and scoped notation are different mechanisms.
- `change` is definitional only.
- Prefer structure fields such as `gamma.naturality_id` / `gamma.naturality_comp` when the goal is exactly the field shape; normalized helper lemmas may contain extra inverse factors.
- For composite `Iso` homs, use public projection simp lemmas instead of blind `rfl`.
- Double-op reverses composition twice, restoring the original order.
- Dependent `rw` can insert casts; use direct definitions or exact normalization theorems where possible.
- In bicategorical goals, reduce wrappers and expose the exact endpoint types before broad coherence tactics.
- Exact-head CI receipts remain evidence only for the exact SHA they validated.

## Validation and reproduction

Latest theorem command:

```bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationExactUniversalAmbientStrongTransPresentationTransportV5_03
```

Validated result:

```text
head = 86d0b52a07d92428c50f0eec5016d563665f887e
Build completed successfully (8622 jobs)
return_code = 0
```

Useful current endpoints:

```bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationExactUniversalLabelledBiequivalenceV4_89 \
  KUOS.DependentOriginationExactUniversalAmbientRestrictionFullV4_94 \
  KUOS.DependentOriginationExactUniversalAmbientStrongTransLocallyDiscreteV4_96 \
  KUOS.DependentOriginationExactUniversalAmbientStrongTransAllArrowNaturalityV5_00 \
  KUOS.DependentOriginationExactUniversalAmbientStrongTransPresentationTransportV5_03
```

Aggregate and runtime entry points:

```bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
PYTHONPATH=. python3 runtime/kuuos_current_check.py
```

README/ROADMAP-only changes should **not** manually rerun an already successful Strict Lean theorem build. They are documentation changes, not new theorem authority.

See [ROADMAP.md](ROADMAP.md) for the exact next theorem units and boundaries.
