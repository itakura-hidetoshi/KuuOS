# KuuOS / 空OS Roadmap

**Theorem snapshot: 2026-10-06 JST · integrated through v5.48**

**現在地：#2003 をマージし、actual-lift 分類双圏から exact-universal 分類双圏への strict pseudofunctor、局所圏同値、対象の本質的全射性、Whitehead 証明書に加え、戻り方向の native Pseudofunctor まで形式化・検証済み。次は、この新しい関手の組に対する global な擬自然 unit／counit と、その modification レベルの整合性である。**

This roadmap distinguishes integrated Lean constructions from proposed obligations. It replaces the old v5.15 snapshot and the already-completed v5.16-v5.19 proposals; it does not remove the earlier ambient or localized-classification results.

## 0. Exact theorem baseline and evidence

| Role | Reference |
| --- | --- |
| Repository / canonical branch | `itakura-hidetoshi/KuuOS` / **main** |
| Latest theorem-bearing merge at this snapshot | **`ff8f9953a4f59b96f969356bd52314eb4aa24ed3`** |
| Theorem PR | [#2003](https://github.com/itakura-hidetoshi/KuuOS/pull/2003), v5.48, merged |
| Validated exact PR head | `3076d51d6dd5cfab0dfcdc82492eee6a35ff9a08` |
| Validation run | [37436221935, attempt 1](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/37436221935), success |
| Strict Lean / governance jobs | `112178648971` / `112179228496`, success |
| Lean / terminal completion jobs | `112179228365` / `112179300773`, success |
| Actual validation checkout | Synthetic PR merge `5a33e3d9e2e004d15cc749c501e7a2503301a8b8` |
| Build and receipt | `8675/8675`; `passed`; return code `0` |
| Lean | `leanprover/lean4:v4.30.0-rc2` |
| Mathlib | `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |

Latest endpoint: [DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48.lean](formal/KUOS/DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48.lean).

The inspected artifact is `audit-check-lean-formal-37436221935-1` (artifact ID `11398887963`). The downloaded archive SHA-256 matched its GitHub metadata:

~~~text
cd2bda98c1d5c1c01db71a42777e9a83308d1f7c93ce9930560f948dd54b5230
~~~

The full 2,223-line log has zero Lean error lines, zero v5.48 target warnings, and no `sorryAx` or `declaration uses 'sorry'`. All nine queried central declarations, including the comparator expansion lemma, report only `propext`, `Classical.choice`, and `Quot.sound`. The log retains 116 existing dependency warnings across 37 files; no repository-wide warning-free claim is made. See the [repair and evidence record](https://github.com/itakura-hidetoshi/KuuOS/pull/2003#issuecomment-6012458786).

The PR head, synthetic validation merge, final theorem merge, and any later documentation-only merge are distinct roles. A docs-only commit does not become a newer theorem-bearing baseline. Likewise, the PR validation receipt is not a separate claim about every main-push job or the aggregate build.

Authority order remains:

~~~text
fresh exact canonical GitHub SHA
  > formal Lean theorem artifacts at that SHA
  > README / ROADMAP
  > exact-head CI/runtime receipts
  > history / conversation memory
~~~

**Protected lane:** [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) is Lean 4.31 validation-only, **open / draft / unmerged**, head `3a09839782ea82661ddbf8e13a0fd08e893079b4`. It is outside canonical theorem authority. Do not merge it, mark it ready for review, or enable auto-merge.

## 1. Keep the three equivalence interfaces distinct

| Interface | Integrated data | Boundary |
| --- | --- | --- |
| Exact-universal raw source -> constructed ambient DO₂ completion | v5.09-v5.15: coverage, Whitehead data, section, native unit/counit; v5.16: coherent triangle representatives and modifications | The representatives do not assert an additional unnamed tricategorical adjoint-biequivalence structure |
| Exact-universal classification -> localized classification | v5.21-v5.31: labelled bicategories, realization, local equivalence, object coverage, section, unit/counit and triangle-representative certificate | External classification labels are retained |
| Actual-lift exact-liftable classification -> exact-universal classification | v5.40-v5.45: bicategory, strict projection and Whitehead data; v5.46-v5.48: explicit backwards pseudofunctor | Global pseudonatural roundtrips for this new pair are the current frontier |

In particular, “global unit/counit remains open” below refers only to the third row. It does not reopen the unit/counit constructions already present in the first two rows. Conversely, their existence does not automatically supply coherence for the new pair of functors.

## 2. Retained foundations — v4.00-v5.16

| Versions | Integrated content | Source anchors |
| --- | --- | --- |
| v4.00-v4.12 | Exact C2 nonfactorization and nonzero Stage-II obstruction in ZMod 2 | [v4.00](formal/KUOS/DependentOriginationAbstractNonfactorizationV4_00.lean), [v4.12](formal/KUOS/DependentOriginationStageIIObstructionClassV4_12.lean) |
| v4.13-v4.48 | Incidence/capacity obstructions, recursive and inverse-limit carriers, exact Cantor dimension, switch/orientation descent | [v4.40](formal/KUOS/DependentOriginationStageIIExactFractalCertificateV4_40.lean), [v4.48](formal/KUOS/DependentOriginationStageIIOrbitOrientationDescentV4_48.lean) |
| v4.49-v4.70 | Presentation descent, exact universal targets, source 1-/2-cells and bicategory, strict realization | [v4.69](formal/KUOS/DependentOriginationExactUniversalMappingBicategoryV4_69.lean), [v4.70](formal/KUOS/DependentOriginationExactUniversalRealizationStrictPseudofunctorV4_70.lean) |
| v4.71-v4.89 | Prescribed raw-map liftability, compatible 2-cell full faithfulness, DO₂ hom equivalences, labelled section and global certificate | [v4.83](formal/KUOS/DependentOriginationExactUniversalHomEquivalenceV4_83.lean), [v4.89](formal/KUOS/DependentOriginationExactUniversalLabelledBiequivalenceV4_89.lean) |
| v4.90-v5.08 | Restriction universality, StrongTrans extension through localization, generator compatibility, generated-relation invariance, quotient-independent coherence | [v5.08](formal/KUOS/DependentOriginationExactUniversalAmbientStrongTransCoherentExtensionV5_08.lean) |
| v5.09-v5.15 | Ambient P4 and object coverage, canonical Whitehead data, ambient section, source unit, ambient counit, explicit certificate | [v5.15](formal/KUOS/DependentOriginationExactUniversalAmbientBiequivalenceCertificateV5_15.lean) |
| v5.16 | Coherent double-identity triangle representatives and native invertible modifications, related to the actual triangle components | [v5.16](formal/KUOS/DependentOriginationExactUniversalAmbientTriangleCoherenceV5_16.lean) |

The positive implication chain remains:

~~~text
exact DO₂ presentation
  => higher stack-localization factorization
  => higher localization factorization
  => weak W-admissibility
~~~

The converse is false in general. Concrete geometric carriers remain stress tests for obstruction and descent, not a universal replacement for the abstract definitions.

## 3. Label-sensitive classification — v5.17-v5.35

### v5.17-v5.20: interfaces, criterion, factorization and uniqueness

The [v5.17 interface](formal/KUOS/DependentOriginationExactUniversalClassificationInterfaceV5_17.lean) distinguishes semantic admissibility, exact liftability, exact-universal objects, and localized classification objects, retaining world/presentation labels. v5.18-v5.20 supply the exact-liftability criterion, factor-existence interface, and coherent-uniqueness machinery.

These concrete interfaces replace the old roadmap's purely schematic classification proposal. They do not prove a universal exact-presentation theorem for every weakly admissible raw system.

### v5.21-v5.31: localized-classification global package

The development adds classification 1-/2-cells, hom categories, a native bicategory, strict realization, local hom equivalences, object coverage, and Whitehead data. The canonical section and global unit/counit are then packaged with coherent triangle representatives.

The [v5.30 triangle layer](formal/KUOS/DependentOriginationClassificationTriangleCoherenceV5_30.lean) reuses the ambient double-identity construction. The [v5.31 certificate](formal/KUOS/DependentOriginationClassificationCoherentBiequivalenceV5_31.lean), `exactUniversalClassificationCoherentBiequivalenceCertificate`, packages the existing results without strengthening their coherence level. Its triangle data is explicitly representative-based.

### v5.32-v5.35: aligned exact-liftability and coherent witnesses

The [v5.32 aligned result](formal/KUOS/DependentOriginationAlignedExactLiftabilityCollapseV5_32.lean) specializes the atlas to:

~~~text
RefinementAtlas.{u, max u v, uH} (LocalizedContext W)
~~~

Under this specialization the exact criterion agrees with the ambient-aligned criterion. This does not prove arbitrary atlas-universe reindexing.

v5.33-v5.34 introduce localized presentation criteria and explicit label-preserving witnesses. The crucial v5.34 upgrade is:

~~~text
HigherPointwiseEquivalenceComparison R S
  -> HigherRawSystemCoherentEquivalence R S
~~~

Thus the old directed-comparison-to-coherent-transport gap is closed. [v5.35](formal/KUOS/DependentOriginationAlignedCoherentClassificationWitnessV5_35.lean) combines the explicit witness with the coherent equivalence and proves:

~~~text
ExactLiftabilityCriterion
  <-> Nonempty (label-preserving localized coherent presentation witness)
~~~

This is an existence/classification theorem with the stated labels and universe alignment, not equality of all possible presentations.

## 4. From exact-liftable objects to a bicategory — v5.36-v5.42

### v5.36: universalization on the original raw system

[v5.36](formal/KUOS/DependentOriginationExactLiftableCoherentUniversalizationV5_36.lean) connects the aligned classification source, the coherent-comparison upgrade, and coherent transport. The endpoint is:

~~~text
ExactLiftableClassificationObject.exists_labelPreserving_fixedRawExactUniversalTarget
~~~

An exact-liftable object's own raw system carries a coherent exact-universal target; the target is not confined to an auxiliary raw presentation. Fixed-raw mutual coherent uniqueness is retained.

### v5.37-v5.39: admissible morphisms and local hom categories

[v5.37](formal/KUOS/DependentOriginationExactLiftableMorphismLiftabilityV5_37.lean) lifts the raw-morphism obstruction to classification:

~~~text
Liftable(f)
  <-> exists classification 1-cell whose raw projection is exactly f.map
~~~

Identity is liftable and liftable morphisms compose. The obstruction is equivalent to nonexistence of the prescribed classification lift. No arbitrary raw StrongTrans is declared liftable.

v5.38 bundles a raw map and its liftability proof. [v5.39](formal/KUOS/DependentOriginationExactLiftableLocalHomCategoryV5_39.lean) defines local 2-cells through chosen canonical lifts and builds genuine hom categories and a canonical-lift hom functor. This alone does not provide global horizontal coherence for the independently chosen lifts.

### v5.40: retain the actual lift as data

[v5.40](formal/KUOS/DependentOriginationExactLiftableActualLiftOneCellV5_40.lean) uses the refined 1-cell type:

~~~text
ExactLiftableClassificationActualOneCell X Y
  raw        : prescribed label-preserving raw one-cell
  actualLift : ExactUniversalClassificationOneCell (F X) (F Y)
  raw_eq     : actualLift.map.raw = raw.map
~~~

The liftability proposition is derived from this data. Forgetting gives the v5.38 bundle; every v5.38 bundled 1-cell can be refined by its existing chosen lift. The existence criterion is preserved.

Crucially, the actual lift of an identity/composite is defined using the existing exact-universal identity/composition. The construction does not need an equality between `chosenLift(f ; g)` and `chosenLift(f) ; chosenLift(g)`. It also does not assert that same raw projection alone makes all selected lifts canonically equal.

### v5.41-v5.42: global bicategory and strict projection

The [v5.41 bicategory](formal/KUOS/DependentOriginationExactLiftableClassificationBicategoryV5_41.lean) inherits 2-cells, whiskering, associators, unitors, pentagon, and triangle from the stored exact-universal lifts.

The [v5.42 strict pseudofunctor](formal/KUOS/DependentOriginationExactLiftableActualLiftStrictPseudofunctorV5_42.lean), `exactLiftableActualLiftStrictPseudofunctor`, has:

~~~text
F.obj X  = CanonicalExactUniversalObject X
F.map f  = f.actualLift
F.map₂ η = η
~~~

Identity and composition are preserved definitionally by this projection. That does not make the source bicategory itself strict.

## 5. Local equivalence and the global Whitehead certificate — v5.43-v5.45

[v5.43](formal/KUOS/DependentOriginationExactLiftableActualLiftLocalHomEquivalenceV5_43.lean) proves local fullness and faithfulness because the 2-cell map is identity. It also proves essential surjectivity on 1-cells: a target 1-cell `k` between canonical endpoints supplies its own raw datum `(k.label_eq, k.map.raw)` and can be stored as its actual lift. Every explicit `actualLiftHomFunctor X Y` is therefore a Mathlib equivalence.

[v5.44](formal/KUOS/DependentOriginationExactLiftableActualLiftObjectCoverageV5_44.lean) supplies label-preserving object coverage:

~~~text
F(Y.toExactLiftable) ~ Y
~~~

The equivalence is obtained from same-raw coherent equivalence and the existing exact-universal machinery. It is not a definitional equality of chosen presentations.

[v5.45](formal/KUOS/DependentOriginationExactLiftableActualLiftWhiteheadBiequivalenceV5_45.lean) closes the interface deliberately separated in v5.43: the explicit local hom functor agrees with the native `toPseudofunctor.toPrelaxFunctor.mapFunctor`. It transfers `IsEquivalence` and packages:

~~~text
exactLiftableActualLiftWhiteheadBiequivalence
  forward
  homEquiv
  homEquiv_functor
  object_essentially_surjective
~~~

This is one genuine `WhiteheadBiequivalenceData` value for the actual-lift bicategory. The local/global hom-functor bridge is no longer an open task.

## 6. Explicit backwards pseudofunctor — v5.46-v5.48

Let `L` be the actual-lift exact-liftable classification bicategory, `E` the exact-universal classification bicategory, and `F : L -> E` the v5.42 strict projection. In this section `;` denotes composition from left to right.

### v5.46: fixed object choices and conjugation

[v5.46](formal/KUOS/DependentOriginationExactLiftableActualLiftQuasiInversePrelaxV5_46.lean) fixes:

~~~text
G.obj Y := Y.toExactLiftable
eY : F(G.obj Y) ~ Y
~~~

using one chosen adjoint equivalence per object. For `k : Y -> Z`, the stored actual lift of `G.map k` is:

~~~text
(eY.hom ; k) ; eZ.inv
~~~

Mathlib `Bicategory.precomp` and `postcomp` make this a functor on each hom category. `PrelaxFunctor.mkOfHomFunctors` assembles the vertical laws. The chosen units/counits supply invertible identity/composition comparisons.

At v5.46 these were candidate pseudofunctor data, not yet a pseudofunctor.

### v5.47: horizontal naturality

[v5.47](formal/KUOS/DependentOriginationExactLiftableActualLiftQuasiInverseNaturalityV5_47.lean), merged as [#2002](https://github.com/itakura-hidetoshi/KuuOS/pull/2002), proves:

~~~text
actualLiftQuasiInverse_map₂_whisker_left
actualLiftQuasiInverse_map₂_whisker_right
~~~

Natural isomorphisms in either argument have exactly the existing compositor's inverse as their components. `NatTrans.naturality` then gives the required equations for arbitrary 2-cells, with no invertibility hypothesis on those cells and no change to the chosen data.

### v5.48: associator, both unitors, and native pseudofunctor

[v5.48](formal/KUOS/DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48.lean), merged as [#2003](https://github.com/itakura-hidetoshi/KuuOS/pull/2003), proves the remaining three conditions in the lax direction:

- Associativity exchanges the two middle counit contractions.
- Left unity uses the chosen equivalence's `left_triangle_hom`.
- Right unity uses its `right_triangle_hom`.

The structural rearrangements are handled by `bicategory`, while exchange and triangle identities are invoked explicitly. A typed `mapIso` cancellation gives the inverse-unitor equations required by `LaxFunctor`.

The resulting constructions are:

~~~text
actualLiftQuasiInverseLax
actualLiftQuasiInversePseudoCore
actualLiftQuasiInversePseudofunctor
~~~

`Pseudofunctor.mkOfLax` retains the original v5.46 `mapId` and `mapComp`. The file proves literal agreement with the old prelax map and comparison isomorphisms, label preservation, and native associator/unitor regression examples.

**All five native pseudofunctor coherence fields are now supplied.** Do not keep horizontal naturality, associator preservation, either unitor law, or backwards-pseudofunctor assembly on the open-task list.

## 7. Current frontier: global roundtrips for the actual-lift pair

The following are **proposed obligations**, not existing v5.49+ theorem claims. Re-observe the canonical SHA before assigning a new version.

### Next A — target counit

Construct a native pseudonatural transformation / `StrongTrans`:

~~~text
G ; F => Id_E
~~~

Use the already fixed `eY.hom` as the object component. Prove naturality for every 1-cell and all 2-cell, identity, and composition coherence fields against the actual v5.48 compositor. Objectwise equivalences alone do not constitute this global transformation.

### Next B — source unit

Construct:

~~~text
Id_L => F ; G
~~~

Use the local fully faithful actual-lift projection to lift the appropriate target comparison, with `e_(F X).inv` as the expected target-side component. Establish its projection and naturality explicitly; do not replace a canonicalized source object by the original object through unproved equality.

### Next C — triangle comparisons and a combined certificate

After A and B, form the actual triangle components for these specific `F`, `G`, unit, and counit. Relate them to coherent representatives, construct native invertible modifications where required, and package the data at a stated coherence level.

The existing v5.16/v5.30/v5.31 pattern is a candidate for reuse, not a proof that the new triangles automatically coincide with the old ones. A stronger tricategorical adjoint-biequivalence claim requires its own precise structure and coherence obligations.

### Longer-range semantics and mapping principle

The concrete exact-sector classification is already substantial. A broader schema such as:

~~~text
AdmissibleContextualSystems(C, X) ~ Fun(DO(C, W, J, H), X)
~~~

is still not an unrestricted theorem. Any further formulation must specify the higher source/target, variance, atlas alignment, world/presentation labels, permitted morphisms, and the exact-liftability boundary. Obstruction results prohibit silently substituting weak admissibility for exact presentation.

Runtime reasoning and action semantics are separate from theorem-level classification. Neither equivalent carriers nor a CI pass removes provenance, external world binding, empirical uncertainty, or authorization requirements.

## 8. Lean proof-engineering lessons from the completed chain

**Names and scopes.** Importing a module does not open its namespaces. Ordinary functor-category whiskering is `CategoryTheory.Functor.isoWhiskerLeft/Right`; bicategorical whiskering is a different API. v5.47's repair qualified all 11 uses, including one hidden inside a failed outer application.

**Universes and endpoints.** Do not guess the order of universe suffixes. Let typed endpoints determine universes when possible; use explicit, checked parameters where inference is genuinely underconstrained. State `(B := ...)` for ambient bicategory lemmas when a wrapped 1-cell cannot determine the ambient type. An aligned atlas theorem is not arbitrary universe reindexing.

**Proof terms versus typed goals.** After an explicitly typed `change`, small `simp only` proofs can be more stable than constructing underconstrained standalone `Category.id_comp _` terms. Name dependent source/target 1-cells when taking fully faithful preimages. Parent projections and `Functor.hext` make the local/native hom-functor boundary explicit.

**Coherence elaboration happens early.** `⊗≫` requires `BicategoricalCoherence` while its intermediate expression is elaborated. A later `dsimp` cannot rescue a failed instance search. v5.48 writes these intermediate endpoints as explicit composites.

**Expose the actual nonstructural cells.** Unfolding an outer definition may leave a private helper opaque to the coherence tactic. v5.48's private `compIso_inv_expansion`, proved by `rfl`, exposes the original counit contraction without using a generated private name or changing the comparator. `bicategory` then handles structural reassociation; it does not replace the exchange or triangle laws.

**Use typed cancellation.** `(F.mapIso e).hom_inv_id` supplies exact cancellation at known endpoints and avoids broad reverse-`Functor.map_comp` simplification leaving residual mapped identities.

**Separate root errors from cascades.** A failed upstream declaration can cause downstream unknown identifiers, unsolved goals, or `sorryAx` reports. Read the full file and log, fix independent root causes, and rebuild. Do not suppress warnings, add axioms, increase heartbeats, or weaken theorem statements to hide a failure.

**Validation is not authority.** Confirm the current PR head, matching run, Strict Lean, governance, final receipt, and axiom output. Distinguish PR head from the synthetic merge actually compiled. Cached dependency warnings are not target warnings; docs-only success is not fresh Lean validation.

## 9. Reproduction and document maintenance

With the pinned toolchain available, run from the repository root at the theorem revision:

~~~bash
git clone https://github.com/itakura-hidetoshi/KuuOS.git KuuOS-repro
cd KuuOS-repro
git checkout ff8f9953a4f59b96f969356bd52314eb4aa24ed3
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48
~~~

To inspect the distinct global packages:

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationExactUniversalAmbientTriangleCoherenceV5_16 \
  KUOS.DependentOriginationClassificationCoherentBiequivalenceV5_31 \
  KUOS.DependentOriginationExactLiftableActualLiftWhiteheadBiequivalenceV5_45 \
  KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48
~~~

Aggregate and runtime commands are separate entry points, not additional successful runs asserted by this docs-only update:

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
PYTHONPATH=. python3 runtime/kuuos_current_check.py
~~~

Keep [README.md](README.md) and this roadmap aligned on the same theorem-bearing snapshot. Future documentation commits should update the milestone ledger and real remaining obligations without turning their own commit SHA into a new theorem result.
