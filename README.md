# KuuOS / 空OS

![KuuOS PR Governance Gate](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/pr-governance-gate.yml/badge.svg)
![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS** is a public research architecture for dependent origination (縁起), contextual transport, higher coherence, descent, obstruction, exact presentation, universal properties, and bounded AI operation. Founder: **Hidetoshi Itakura / 板倉英俊**.

> Which structure survives justified changes of context and presentation, how can compatible local information be transported and glued, and which universal property characterizes the invariant content?

## Current formal status — v5.48

**2026-10-06 JST：v5.48 まで main に統合済み。** exact liftability の分類、元の raw system 上の coherent universal target、actual lift を保持する1-cellの双圏、前向きの strict pseudofunctor、局所圏同値・対象の本質的全射性を統合した Whitehead 証明書に加え、戻り方向の native `Pseudofunctor` まで検証済みです。**この新しい actual-lift 層の global な擬自然 unit／counit と modification レベルの往復整合性は、次の残件です。**

The current result concerns the **actual-lift exact-liftable classification bicategory**, not arbitrary raw morphisms. Write:

~~~text
L = ExactLiftableClassificationObject, with actual-lift-carrying 1-cells
E = ExactUniversalClassificationObject

F : L -> E     strict pseudofunctor                         v5.42
F is locally an equivalence and essentially surjective     v5.43-v5.45
G : E -> L     explicit backwards pseudofunctor             v5.46-v5.48
~~~

The v5.45 `WhiteheadBiequivalenceData` and the v5.48 backwards pseudofunctor are both constructed. They are not yet packaged with global pseudonatural roundtrips for this particular pair `L, E`. Earlier ambient and localized-classification unit/counit packages remain valid, but are different interfaces.

## Reproducible theorem snapshot

| Role | Exact reference |
| --- | --- |
| Repository / canonical branch | `itakura-hidetoshi/KuuOS` / **main** |
| Latest theorem-bearing merge at this snapshot | **`ff8f9953a4f59b96f969356bd52314eb4aa24ed3`** |
| Theorem PR | [#2003 — actual-lift quasi-inverse pseudofunctor coherence v5.48](https://github.com/itakura-hidetoshi/KuuOS/pull/2003), merged |
| Validated PR head | `3076d51d6dd5cfab0dfcdc82492eee6a35ff9a08` |
| Validation run | [37436221935, attempt 1](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/37436221935), success |
| Exact-head receipts | Strict Lean: success; exact-head terminal: success |
| Actual CI checkout | Synthetic PR merge `5a33e3d9e2e004d15cc749c501e7a2503301a8b8` |
| Build | `8675/8675`; receipt `passed`; return code `0` |
| Lean | `leanprover/lean4:v4.30.0-rc2` |
| Mathlib | `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |

The validated endpoint is [DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48.lean](formal/KUOS/DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48.lean). Its nine queried central declarations report only `propext`, `Classical.choice`, and `Quot.sound`; no `sorryAx` appears. The inspected build log has no Lean errors and no warnings in the v5.48 target. Existing dependency warnings remain; this is not a repository-wide warning-free claim.

A later README/ROADMAP-only merge may advance `main` without changing this theorem-bearing baseline. Branch badges are live indicators, not substitutes for the exact-head evidence above. See [ROADMAP.md](ROADMAP.md) for the validation artifact and milestone ledger.

Authority order:

~~~text
fresh exact canonical GitHub SHA
  > formal Lean theorem artifacts at that SHA
  > README / ROADMAP
  > exact-head CI/runtime receipts
  > history / conversation memory
~~~

The separate [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) Lean 4.31 validation lane remains **open / draft / unmerged**, outside canonical theorem authority. Do not merge it, mark it ready for review, or enable auto-merge.

## What 空 means here

空 is not “nothing exists.” Its operational role is non-reification: a chosen presentation is not intrinsic substance, a local observation is not global truth, equivalent carriers do not erase provenance or world binding, and successful execution is not theorem authority. Quotient representatives are computational scaffolding; representative independence is a separate mathematical obligation.

KuuOS separates observation from inference, identifies the active context, retains multiple presentations, tracks relations and history, checks local compatibility and descent, exposes obstructions, respects authority boundaries, performs only justified actions, and re-observes afterward.

The formal program is richer than a graph: it includes systems, mappings, transformations between mappings, bicategorical coherence, descent, obstructions, and universal properties. These are mathematical structures for organizing reasoning, not evidence that an LLM's outputs are automatically correct or that every external action is authorized.

## Scope: exact liftability is not weak admissibility

The positive classification chain uses the aligned atlas specialization
`RefinementAtlas.{u, max u v, uH} (LocalizedContext W)` and the corresponding universe-polymorphic raw systems. External world and presentation labels remain explicit.

The obstruction/nonfactorization results are retained:

~~~text
exact DO₂ presentation
  => higher stack-localization factorization
  => higher localization factorization
  => weak W-admissibility

The converse is false in general.
~~~

The exact-liftability criterion, coherent witnesses, and morphism-liftability criterion characterize the permitted positive sector. They do not turn every weakly admissible system into an exact presentation, or every raw StrongTrans into a liftable 1-cell. The aligned-atlas result is not an arbitrary-universe reindexing theorem.

## The current classification chain

| Stage | Integrated result | Source anchor |
| --- | --- | --- |
| v5.17-v5.20 | Label-sensitive classification interfaces, exact-liftability criterion, factor existence, coherent uniqueness | [v5.17](formal/KUOS/DependentOriginationExactUniversalClassificationInterfaceV5_17.lean) |
| v5.21-v5.31 | Exact-universal/localized classification bicategories and realization; local/object equivalence; section, unit/counit, coherent triangle representatives and modifications | [v5.31 certificate](formal/KUOS/DependentOriginationClassificationCoherentBiequivalenceV5_31.lean) |
| v5.32-v5.35 | Aligned criterion, localized presentation witnesses, directed pointwise comparison upgraded to coherent raw equivalence | [v5.32](formal/KUOS/DependentOriginationAlignedExactLiftabilityCollapseV5_32.lean), [v5.35](formal/KUOS/DependentOriginationAlignedCoherentClassificationWitnessV5_35.lean) |
| v5.36 | A label-preserving coherent exact-universal target on the original raw system, with fixed-raw mutual coherent uniqueness | [v5.36](formal/KUOS/DependentOriginationExactLiftableCoherentUniversalizationV5_36.lean) |
| v5.37-v5.39 | Exact raw-morphism liftability criterion, bundled liftable 1-cells, local hom categories | [v5.37](formal/KUOS/DependentOriginationExactLiftableMorphismLiftabilityV5_37.lean), [v5.39](formal/KUOS/DependentOriginationExactLiftableLocalHomCategoryV5_39.lean) |
| v5.40-v5.42 | Actual-lift-carrying 1-cells, a global bicategory, and its strict actual-lift projection `F` | [v5.40](formal/KUOS/DependentOriginationExactLiftableActualLiftOneCellV5_40.lean), [v5.42](formal/KUOS/DependentOriginationExactLiftableActualLiftStrictPseudofunctorV5_42.lean) |
| v5.43-v5.45 | Local hom equivalences, object coverage, native `mapFunctor` bridge, one Whitehead certificate | [v5.45](formal/KUOS/DependentOriginationExactLiftableActualLiftWhiteheadBiequivalenceV5_45.lean) |
| v5.46-v5.48 | Fixed objectwise equivalences, conjugation hom functors, horizontal naturality, associator/unitor coherence, backwards pseudofunctor `G` | [v5.48](formal/KUOS/DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48.lean) |

### Why the actual-lift refinement matters

A v5.38 1-cell stores a prescribed raw map and a proof of liftability. Its noncomputably chosen lift need not preserve composition definitionally. v5.40 instead stores:

~~~text
prescribed label-preserving raw one-cell
actual ExactUniversalClassificationOneCell
actualLift.map.raw = prescribedRaw.map
~~~

Identity and composition use the stored exact-universal lifts directly. This removes the need to identify independently chosen lifts when constructing the v5.41 bicategory and the v5.42 strict projection. Forgetting recovers the older liftability bundle, and every older bundled 1-cell has an actual-lift refinement. This is not a claim that arbitrary choices become equal.

### What the backwards pseudofunctor does

For `Y : E`, set `G(Y) := Y.toExactLiftable` and choose once an adjoint equivalence `eY : F(G(Y)) ~ Y`. For a 1-cell `k : Y -> Z`, the stored target lift of `G(k)` is the conjugated map:

~~~text
(eY.hom ; k) ; eZ.inv
~~~

Here `;` means composition from left to right. The raw projection is the raw map of this conjugated lift, not an assertion that it equals the original `k`'s raw map.

v5.47 proves both horizontal naturality laws for arbitrary 2-cells, without invertibility assumptions on those cells. v5.48 proves associativity by exchanging counit contractions and the two unity laws from the chosen adjoint equivalences' triangle identities. `LaxFunctor.PseudoCore` and `Pseudofunctor.mkOfLax` retain the original v5.46 comparison isomorphisms.

## Earlier results remain integrated

The v4.00-v4.48 obstruction, geometry, inverse-limit, and orientation/descent development is not superseded by the positive theory. v4.49-v4.89 construct the exact-universal source, strict DO₂ realization, hom equivalences, and the object-labelled global package.

The source-to-ambient completion route is also closed through its existing interface: v5.08 closes StrongTrans extension, v5.09-v5.10 close ambient P4/object coverage and Whitehead data, and v5.11-v5.15 package an explicit section with native unit/counit. [v5.16](formal/KUOS/DependentOriginationExactUniversalAmbientTriangleCoherenceV5_16.lean) adds coherent triangle representatives and native invertible modifications to identity.

Likewise, the exact-universal-to-localized classification route has its own [v5.31 certificate](formal/KUOS/DependentOriginationClassificationCoherentBiequivalenceV5_31.lean). These triangle-representative packages are not an unnamed stronger tricategorical adjoint-biequivalence object, and they do not automatically supply the new actual-lift roundtrip data.

## Current research frontier

For the **v5.42/v5.48 pair `F, G`**, the next obligations are:

1. Construct the global target counit `G ; F => Id_E` using the fixed object equivalences, with all StrongTrans coherence fields.
2. Construct the global source unit `Id_L => F ; G`, respecting stored actual lifts and external labels.
3. Relate their actual triangle composites to coherent representatives, prove the required modifications, and package the roundtrip data at the explicitly stated coherence level.

These are proposed next steps, not current theorem claims. The unrestricted schematic mapping principle for all semantically admissible systems is also not proved; the completed exact-sector classification must not be broadened past its obstruction boundary.

## Validation and reproduction

Run from a checkout of the theorem-bearing revision, with Git and the pinned Lean toolchain available:

~~~bash
git clone https://github.com/itakura-hidetoshi/KuuOS.git KuuOS-repro
cd KuuOS-repro
git checkout ff8f9953a4f59b96f969356bd52314eb4aa24ed3
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48
~~~

Useful separate endpoints:

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationClassificationCoherentBiequivalenceV5_31 \
  KUOS.DependentOriginationExactLiftableActualLiftWhiteheadBiequivalenceV5_45 \
  KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48
~~~

Aggregate and runtime entry points remain available, but the endpoint receipt above is not a claim that these commands were separately run in this documentation update:

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
PYTHONPATH=. python3 runtime/kuuos_current_check.py
~~~

See [ROADMAP.md](ROADMAP.md) for the completed milestones, exact remaining obligations, and retained Lean proof-engineering lessons. This documentation update changes no Lean theorem, dependency pin, runtime behavior, or validation-only branch.
