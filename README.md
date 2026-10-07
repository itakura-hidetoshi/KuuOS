# KuuOS / 空OS

![KuuOS PR Governance Gate](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/pr-governance-gate.yml/badge.svg)
![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS** is a public research architecture for dependent origination (縁起), contextual transport, higher coherence, descent, obstruction, exact presentation, universal properties, and bounded AI operation. Founder: **Hidetoshi Itakura / 板倉英俊**.

> Which structure survives justified changes of context and presentation, how can compatible local information be transported and glued, and which universal property characterizes the invariant content?

## Current formal status — v5.63

**2026-10-07 JST：v5.63 / PR #2020 まで canonical main に統合済み。**

The actual-lift classification layer now contains the same forward pseudofunctor, quasi-inverse, unit, counit, actual triangle pastes, native invertible triangle contractions, and a generic pre/postcomposition interface for those higher cells.

~~~text
L = ExactLiftableClassificationObject
    with actual-lift-carrying 1-cells
E = ExactUniversalClassificationObject

F : L -> E
G : E -> L

eta : Id_L => F ; G
eps : G ; F => Id_E

T_F : F => F
T_G : G => G

C_F : T_F ~= Id_F
C_G : T_G ~= Id_G
~~~

The integrated v5.57 certificate remains the source of the same actual-lift data. v5.58-v5.63 add the native higher-coherence interface around that data:

- **v5.58:** exposes both triangle contractions as invertible 2-cells in Mathlib's native bicategory of pseudofunctors.
- **v5.59:** packages F, G, eta, eps and both triangulators as an explicit IncoherentBiadjunctionDatum.
- **v5.60:** generalizes the non-strict reverse-triangle horizontal whiskering and reassociation.
- **v5.61:** precomposition of arbitrary StrongTrans values, modifications, invertible modifications, and triangulators.
- **v5.62:** non-strict postcomposition of arbitrary StrongTrans values, modifications, and invertible modifications.
- **v5.63:** constructs the canonical H.mapId comparison between postcomposition of an identity StrongTrans and the native identity, then lifts postcomposition to the full triangulator package.

The important boundary is explicit: **no swallowtail equation has yet been proved.** KuuOS therefore does not relabel the current result as a coherent biadjunction, biadjoint biequivalence, or stronger tricategorical adjunction.

## Reproducible theorem snapshot

| Role | Exact reference |
| --- | --- |
| Repository / canonical branch | itakura-hidetoshi/KuuOS / **main** |
| Latest theorem-bearing merge | **f133bd0b439e4997078a8ef460492ceacaa4ba1a** |
| Theorem PR | [#2020 — v5.63](https://github.com/itakura-hidetoshi/KuuOS/pull/2020), merged |
| Validated exact PR head | f27a32da56aba2fd7c93161accc67e8d8e1229cd |
| Validation run | [37586647612](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/37586647612), attempt 1, success |
| Strict Lean / governance | 112678278070 / 112678801540, success |
| Lean / terminal receipts | 112678801533 / 112678868864, success |
| Actual CI checkout | synthetic merge 65c6ebd49f812b9f6fea4448717c09676c7b7aae |
| Build | 8690/8690; return code 0 |
| Lean | leanprover/lean4:v4.30.0-rc2 |
| Mathlib | 5450b53e5ddc75d46418fabb605edbf36bd0beb6 |
| Lean artifact | 11466423829 |
| Artifact SHA-256 | 0932ca5db839aefd1cfc40d0302c474c3589901d77762ca0518682d00dc2d22b |

The v5.63 target has no Lean errors and no sorryAx. Its queried declarations report only propext, Classical.choice, and Quot.sound. The successful target emitted one linter warning for an unused Category.assoc simp argument; this is a proof-engineering cleanup item, not a theorem failure and not a repository-wide warning-free claim.

Authority order:

~~~text
fresh exact canonical GitHub SHA
  > formal Lean theorem artifacts at that SHA
  > README / ROADMAP
  > exact-head CI/runtime receipts
  > history / conversation memory
~~~

The separate [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) Lean 4.31 validation lane remains **open / draft / unmerged**, head 3a09839782ea82661ddbf8e13a0fd08e893079b4. It is outside canonical theorem authority. Do not merge it, mark it ready for review, or enable auto-merge.

## What 空 means here

空 is not “nothing exists.” Its operational role is non-reification: a chosen presentation is not intrinsic substance, a local observation is not global truth, equivalent carriers do not erase provenance or world binding, and successful execution is not theorem authority.

KuuOS separates observation from inference, identifies the active context, retains multiple presentations, tracks relations and history, checks local compatibility and descent, exposes obstructions, respects authority boundaries, performs only justified actions, and re-observes afterward.

The formal program uses systems, mappings, transformations between mappings, bicategorical coherence, descent, obstruction classes, exact presentations, and universal properties. These structures organize reasoning; they do not make an LLM automatically correct or authorize external actions.

## Exact-liftability boundary

The positive classification chain uses the aligned atlas specialization:

~~~text
RefinementAtlas.{u, max u v, uH} (LocalizedContext W)
~~~

and keeps external world and presentation labels explicit. The obstruction boundary remains:

~~~text
exact DO₂ presentation
  => higher stack-localization factorization
  => higher localization factorization
  => weak W-admissibility

converse: false in general
~~~

The actual-lift layer therefore does **not** assert arbitrary raw-morphism liftability, arbitrary atlas-universe reindexing, equality of independently chosen presentations, or strict preservation of a conjugated raw map.

## Current classification and higher-coherence chain

| Stage | Integrated result | Source |
| --- | --- | --- |
| v4.00-v4.48 | Nonfactorization, Stage-II obstruction, recursive/inverse-limit carriers, orientation/descent | [v4.48](formal/KUOS/DependentOriginationStageIIOrbitOrientationDescentV4_48.lean) |
| v4.49-v5.16 | Exact-universal source, realization, hom equivalences, ambient section/unit/counit and coherent triangles | [v5.16](formal/KUOS/DependentOriginationExactUniversalAmbientTriangleCoherenceV5_16.lean) |
| v5.17-v5.31 | Label-sensitive classification, global unit/counit, triangle representatives and modifications | [v5.31](formal/KUOS/DependentOriginationClassificationCoherentBiequivalenceV5_31.lean) |
| v5.32-v5.36 | Aligned exact-liftability, coherent presentation witnesses, coherent universalization | [v5.36](formal/KUOS/DependentOriginationExactLiftableCoherentUniversalizationV5_36.lean) |
| v5.37-v5.42 | Morphism liftability, actual-lift 1-cells, bicategory, strict projection F | [v5.42](formal/KUOS/DependentOriginationExactLiftableActualLiftStrictPseudofunctorV5_42.lean) |
| v5.43-v5.48 | Local hom equivalence, object coverage, Whitehead data, explicit non-strict G | [v5.48](formal/KUOS/DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48.lean) |
| v5.49-v5.52 | Native counit/unit, pointwise contractions, actual forward triangle and invertible modification | [v5.52](formal/KUOS/DependentOriginationExactLiftableActualLiftForwardTriangleModificationV5_52.lean) |
| v5.53-v5.56 | Non-strict reverse factors, reassociation, actual reverse triangle and invertible modification | [v5.56](formal/KUOS/DependentOriginationExactLiftableActualLiftQuasiInverseTriangleModificationV5_56.lean) |
| v5.57 | Integrated certificate containing the same Whitehead/F/G/eta/eps and both actual triangle modifications | [v5.57](formal/KUOS/DependentOriginationExactLiftableActualLiftCoherentBiequivalenceV5_57.lean) |
| v5.58 | Native functor-bicategory triangulators | [v5.58](formal/KUOS/DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58.lean) |
| v5.59 | Explicit IncoherentBiadjunctionDatum | [v5.59](formal/KUOS/DependentOriginationExactLiftableActualLiftIncoherentBiadjunctionV5_59.lean) |
| v5.60 | Generic non-strict reverse-triangle horizontal whiskering | [v5.60](formal/KUOS/DependentOriginationExactLiftableActualLiftIncoherentBiadjunctionHorizontalWhiskeringV5_60.lean) |
| v5.61 | StrongTrans / modification / Iso / triangulator precomposition | [v5.61](formal/KUOS/DependentOriginationStrongTransModificationPrecompositionV5_61.lean) |
| v5.62 | Non-strict StrongTrans / modification / Iso postcomposition | [v5.62](formal/KUOS/DependentOriginationStrongTransModificationPostcompositionV5_62.lean) |
| **v5.63** | **H.mapId identity comparison and full triangulator postcomposition** | [v5.63](formal/KUOS/DependentOriginationStrongTransPostcompositionIdentityTriangulatorV5_63.lean) |

## Actual-lift pair and native triangles

For Y : E, the quasi-inverse uses G(Y) := Y.toExactLiftable and one fixed adjoint equivalence eY : F(GY) ~ Y. For k : Y -> Z, its stored actual lift is:

~~~text
(eY.hom ; k) ; eZ.inv
~~~

This G is genuinely non-strict. Its mapId and mapComp comparisons are retained throughout the reverse triangle and later whiskering constructions.

The two actual triangles remain:

~~~text
T_F : F => F
T_G : G => G

C_F : T_F ~= Id_F
C_G : T_G ~= Id_G
~~~

v5.58 interprets C_F and C_G as native invertible 2-cells in Mathlib's functor bicategories, rather than replacing them by a new family.

## Higher-coherence interface — v5.58-v5.63

### Native triangulators

FunctorBicategoryTriangulator F stores:

~~~text
triangle    : F ⟶ F
contraction : triangle ≅ 𝟙 F
~~~

FunctorBicategoryTriangulatorPair F G stores the two opposite-direction triangulators, but no compatibility law between them.

### Incoherent biadjunction datum

v5.59 packages:

~~~text
base          = Whitehead/F/G/eta/eps
triangulators = forward and reverse triangulators
~~~

The name **incoherent** is deliberate: this datum does not contain a swallowtail law.

### Precomposition

v5.61 defines, for a pseudofunctor K:

~~~text
alpha                      : F => G
precompose K alpha         : K ; F => K ; G

Gamma : alpha ==> beta
precompose K Gamma         : precompose K alpha ==> precompose K beta
~~~

and preserves invertible modifications and triangulators. All actual K.mapId and K.mapComp comparisons remain in the proof.

### Postcomposition

v5.62 defines, for a pseudofunctor H:

~~~text
alpha                       : F => G
postcompose H alpha         : F ; H => G ; H

Gamma : alpha ==> beta
postcompose H Gamma         : postcompose H alpha ==> postcompose H beta
~~~

with the mapped square expressed through H.map₂ and H.mapComp.

Postcomposition has an additional non-strict identity issue:

~~~text
postcompose H (id_F) has component H.map (𝟙 _)
native id_(F ; H) has component 𝟙 _
~~~

v5.63 resolves exactly this gap with H.mapId (F.obj a), yielding:

~~~text
postcompose H (id_F) ≅ id_(F ; H)
~~~

and thereby lifting postcomposition to the full triangulator package.

## Current research frontier

The infrastructure needed to **write** the remaining higher-coherence equations is now substantially in place. The next formal work is:

1. **Modification-level horizontal pastes:** use v5.61 and v5.63 to form the two canonical pastes of the stored triangulator contractions.
2. **Typed swallowtail predicates:** state the forward and reverse swallowtail equations with the actual associators, unitors, and non-strict pseudofunctor comparators.
3. **Actual-lift specialization:** instantiate those predicates for exactLiftableActualLiftIncoherentBiadjunctionDatum.
4. **Proof or controlled adjustment:** prove the swallowtail equations for the stored contractions, or, if a standard adjustment is mathematically required, formalize that adjustment explicitly and prove preservation of the underlying biequivalence data.
5. **Only after those laws are proved:** consider introducing a stronger coherent-biadjunction / biadjoint-biequivalence certificate.

Other research directions remain:

- determine the exact hypotheses for any broader mapping principle;
- continue separating fixed-presentation equivalence, coherent transport, and genuine descent;
- connect the formal contextual/coherence layer to AI reasoning and retrieval while retaining provenance, authorization, and re-observation boundaries.

These are research directions, not theorem claims.

## Lean proof-engineering lessons

The v5.58-v5.63 work sharpened several recurring rules:

- **Explicit labels at header boundaries.** With autoImplicit false, universe-sensitive label types that are not inferable from other arguments must be routed explicitly.
- **Header elaboration precedes body inference.** Information from a declaration body cannot repair unresolved holes in an explicitly typed header.
- **Preserve non-strict comparison data.** mapId and mapComp are mathematical coherence, not noise to simplify away.
- **Reassociation is coherence, not definitional equality.**
- **Use explicit StrongTrans.homCategory when inference loses the 2-morphism universe.**
- **Use the library's native extensionality theorem.** Pseudofunctor.StrongTrans.homCategory.ext is more robust than generic ext at explicit Hom wrappers.
- **Do not over-simplify proof equalities.** A useful component equality can be simplified to True; pass the exact equality when that is what the goal needs.
- **Avoid fragile global change.** Normalize with projection and coherence lemmas first; use change only when the remaining expression is genuinely definitionally equal.
- **Postcomposition of identity is not definitionally identity.** The missing comparison is exactly H.mapId.
- **Separate root errors from cascades.** Read the whole changed file and full CI log before repairing downstream symptoms.
- **Validation is not authority.** Match exact PR head, successful run, synthetic merge, and final canonical merge separately.

## Validation and reproduction

~~~bash
git clone https://github.com/itakura-hidetoshi/KuuOS.git KuuOS-repro
cd KuuOS-repro
git checkout f133bd0b439e4997078a8ef460492ceacaa4ba1a

lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationStrongTransPostcompositionIdentityTriangulatorV5_63
~~~

Useful earlier endpoints:

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationExactLiftableActualLiftCoherentBiequivalenceV5_57 \
  KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58 \
  KUOS.DependentOriginationExactLiftableActualLiftIncoherentBiadjunctionV5_59 \
  KUOS.DependentOriginationExactLiftableActualLiftIncoherentBiadjunctionHorizontalWhiskeringV5_60 \
  KUOS.DependentOriginationStrongTransModificationPrecompositionV5_61 \
  KUOS.DependentOriginationStrongTransModificationPostcompositionV5_62
~~~

Aggregate/runtime entry points remain separate:

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
PYTHONPATH=. python3 runtime/kuuos_current_check.py
~~~

The successful v5.63 receipt is evidence for the selected target-and-dependency build, not a claim that every aggregate/runtime command was rerun in this documentation update.

See [ROADMAP.md](ROADMAP.md) for the detailed milestone ledger, higher-coherence frontier, validation evidence, and Lean proof-engineering lessons.
