# KuuOS / 空OS Roadmap

**Theorem snapshot: 2026-10-07 JST · integrated through v5.63**

**現在地：actual-lift 分類双圏 L と exact-universal 分類双圏 E の同じ F,G,eta,eps について、unit/counit、両方向の実際の triangle StrongTrans、両 native invertible modifications に加え、functor-bicategory triangulator と非strictな pre/postcomposition の modification-level interface まで構築済み。v5.63 では postcomposition of identity と native identity の差を H.mapId で埋め、triangulator postcomposition を完成した。swallowtail equations 自体はまだ未証明。**

This roadmap distinguishes integrated Lean constructions from proposed research obligations. It does not upgrade the current native StrongTrans/modification infrastructure into a coherent biadjunction or biadjoint biequivalence before the missing higher equations are proved.

## 0. Exact theorem baseline and evidence

| Role | Reference |
| --- | --- |
| Repository / canonical branch | itakura-hidetoshi/KuuOS / **main** |
| Latest theorem-bearing merge | **f133bd0b439e4997078a8ef460492ceacaa4ba1a** |
| Theorem PR | [#2020](https://github.com/itakura-hidetoshi/KuuOS/pull/2020), v5.63, merged |
| Validated exact PR head | f27a32da56aba2fd7c93161accc67e8d8e1229cd |
| Validation run | [37586647612](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/37586647612), attempt 1, success |
| Strict Lean / governance | 112678278070 / 112678801540, success |
| Lean / terminal receipts | 112678801533 / 112678868864, success |
| Actual validation checkout | synthetic PR merge 65c6ebd49f812b9f6fea4448717c09676c7b7aae |
| Build | 8690/8690; passed; return code 0 |
| Lean | leanprover/lean4:v4.30.0-rc2 |
| Mathlib | 5450b53e5ddc75d46418fabb605edbf36bd0beb6 |
| Lean artifact | 11466423829 |
| Artifact SHA-256 | 0932ca5db839aefd1cfc40d0302c474c3589901d77762ca0518682d00dc2d22b |

Latest endpoint: [v5.63 postcomposition identity comparison and triangulator](formal/KUOS/DependentOriginationStrongTransPostcompositionIdentityTriangulatorV5_63.lean).

The v5.63 target builds successfully under the pinned environment with no Lean errors and no sorryAx. Its queried declarations report only propext, Classical.choice, and Quot.sound. The successful target currently emits one linter warning for an unused Category.assoc simp argument; this is a proof-engineering cleanup item, not a theorem failure.

Authority remains:

~~~text
fresh exact canonical GitHub SHA
  > formal Lean theorem artifacts at that SHA
  > README / ROADMAP
  > exact-head CI/runtime receipts
  > history / conversation memory
~~~

**Protected lane:** [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) remains Lean 4.31 validation-only, **open / draft / unmerged**, head 3a09839782ea82661ddbf8e13a0fd08e893079b4. It is outside canonical theorem authority.

## 1. Three retained equivalence interfaces

| Interface | Integrated data | Boundary |
| --- | --- | --- |
| Exact-universal raw source -> ambient DO₂ completion | v5.09-v5.16: coverage, Whitehead data, section, unit/counit, coherent triangle package | No stronger unnamed tricategorical object is asserted |
| Exact-universal classification -> localized classification | v5.21-v5.31: labelled bicategories, local equivalence, coverage, section, unit/counit, coherent triangle package | External labels remain explicit |
| Actual-lift exact-liftable classification -> exact-universal classification | **v5.40-v5.63: bicategory, strict F, Whitehead data, non-strict G, unit/counit, both actual triangles, both invertible modifications, native triangulators, pre/postcomposition infrastructure** | Swallowtail compatibility is still open |

The first two interfaces remain valid. They are not substitutes for the third.

## 2. Retained foundations — v4.00-v5.36

| Versions | Integrated content |
| --- | --- |
| v4.00-v4.12 | Exact C2 nonfactorization and nonzero Stage-II obstruction in ZMod 2 |
| v4.13-v4.48 | Incidence/capacity obstructions, recursive and inverse-limit carriers, exact Cantor dimension, switch/orientation descent |
| v4.49-v4.89 | Presentation descent, exact universal targets, source bicategory, strict realization, hom equivalences, labelled global package |
| v4.90-v5.08 | Restriction universality and coherent StrongTrans extension through localization |
| v5.09-v5.16 | Ambient Whitehead/section/unit/counit and coherent triangle package |
| v5.17-v5.31 | Label-sensitive exact-universal/localized classification and coherent certificate |
| v5.32-v5.35 | Aligned exact-liftability and coherent presentation witnesses |
| v5.36 | Coherent exact-universal target on the original raw system, with fixed-raw mutual coherent uniqueness |

The positive implication chain remains:

~~~text
exact DO₂ presentation
  => higher stack-localization factorization
  => higher localization factorization
  => weak W-admissibility
~~~

The converse is false in general.

## 3. Actual-lift bicategory and forward map — v5.37-v5.45

v5.37 gives the exact raw-morphism liftability criterion. v5.38-v5.39 bundle liftable maps and form local hom categories.

v5.40 refines a 1-cell to carry:

~~~text
raw        : prescribed label-preserving raw one-cell
actualLift : ExactUniversalClassificationOneCell (F X) (F Y)
raw_eq     : actualLift.map.raw = raw.map
~~~

Identity and composition use the stored exact-universal lifts rather than independently chosen lifts.

v5.41 constructs the actual-lift bicategory. v5.42 constructs the strict projection F. v5.43-v5.44 prove local hom equivalence and label-preserving object coverage. v5.45 packages WhiteheadBiequivalenceData.

## 4. Explicit non-strict quasi-inverse — v5.46-v5.48

For each Y : E, fix once:

~~~text
G.obj Y := Y.toExactLiftable
eY : F(GY) ~ Y
~~~

For k : Y -> Z, the actual lift of G(k) is:

~~~text
(eY.hom ; k) ; eZ.inv
~~~

v5.47 proves horizontal naturality for arbitrary 2-cells. v5.48 proves associator and both unitor coherence laws and assembles the native Pseudofunctor without replacing its original mapId or mapComp.

## 5. Native unit/counit and actual triangles — v5.49-v5.57

### v5.49-v5.50

The target counit and source unit are:

~~~text
eps : G ; F => Id_E
eta : Id_L => F ; G
~~~

using the already fixed object equivalences.

### v5.51-v5.52 — forward triangle

v5.51 constructs pointwise contractions. v5.52 builds the actual forward triangle and its global invertible modification.

### v5.53-v5.56 — reverse triangle for non-strict G

v5.53 constructs:

~~~text
eta_G : G => G ; (F ; G)
~~~

with the real G.mapId / G.mapComp.

v5.54 applies the counit through G:

~~~text
(G ; F) ; G => G
~~~

and reconciles the two triple bracketings through explicit comparison lemmas.

v5.55 pastes the two factors into the actual reverse triangle:

~~~text
T_G(Y) = eta_(G Y) ; G(eps_Y)
~~~

v5.56 proves the global reverse invertible modification.

### v5.57 — integrated certificate

exactLiftableActualLiftCoherentBiequivalenceCertificate stores the same Whitehead datum, F, G, eta, eps, and both actual triangle/modification pairs. Whole-record equations verify that the stored values are the already-constructed native values.

The existing certificate name is retained for compatibility. v5.58 onward makes explicit that **additional biadjunction swallowtail coherence is a separate obligation**.

## 6. Native functor-bicategory triangulators — v5.58

v5.58 imports Mathlib's FunctorBicategory.Pseudo and introduces:

~~~text
structure FunctorBicategoryTriangulator (F) where
  triangle    : F ⟶ F
  contraction : triangle ≅ 𝟙 F
~~~

Pseudofunctors are objects, StrongTrans values are 1-cells, and modifications are 2-cells in this functor bicategory. The old v5.52 and v5.56 triangle contractions are reused exactly.

It also packages:

~~~text
FunctorBicategoryTriangulatorPair F G
~~~

with forward and reverse triangulators. No compatibility law is added.

Lean lesson: label types not inferable from W and A must be explicit in typed declaration headers under autoImplicit false; body inference cannot repair unresolved header holes.

## 7. Incoherent biadjunction datum — v5.59

v5.59 introduces:

~~~text
structure IncoherentBiadjunctionDatum B C where
  base          : WhiteheadUnitCounitCertificate B C
  triangulators : FunctorBicategoryTriangulatorPair
                    base.whitehead.forward
                    base.quasiInverse
~~~

The actual-lift value is a pure repackaging of the v5.57/v5.58 data. The name **incoherent** is intentional: no swallowtail law is stored.

This is the typed input for the higher-coherence frontier, not a stronger theorem claim.

## 8. Generic non-strict horizontal whiskering — v5.60

v5.60 lifts the reverse-triangle construction from the concrete actual-lift case to arbitrary IncoherentBiadjunctionDatum.

It constructs the two native triple bracketings:

~~~text
G ; (F ; G)
(G ; F) ; G
~~~

precomposes the unit by G, postcomposes the counit by G, proves the actual mapId / mapComp comparison between bracketings, reassociates the counit factor, and vertically composes the result.

No tricategory API is assumed and no swallowtail is asserted.

## 9. Precomposition infrastructure — v5.61

For arbitrary pseudofunctor K and alpha : F => G, v5.61 constructs:

~~~text
precompose K alpha : K ; F => K ; G
~~~

while retaining K.mapId and K.mapComp.

It also defines precomposition of:

~~~text
modification
invertible modification
FunctorBicategoryTriangulator
~~~

The important proof-engineering repairs were:

- normalize remaining categorical associativity explicitly;
- bind the existing StrongTrans.homCategory at typed endpoints instead of asking typeclass search to infer the modification universe;
- use Pseudofunctor.StrongTrans.homCategory.ext directly;
- avoid simpa when it destroys the informative component equality.

Precomposition of the identity StrongTrans is definitionally the native identity at the composite endpoint, so no extra mapId bridge is needed.

## 10. Postcomposition infrastructure — v5.62

For arbitrary pseudofunctor H and alpha : F => G, v5.62 constructs:

~~~text
postcompose H alpha : F ; H => G ; H
~~~

with components:

~~~text
H.map (alpha.app a)
~~~

and naturality obtained by mapping the old square through H, padded by H.mapComp.

The generic laws preserve both source and target mapId / mapComp. v5.62 also defines postcomposition of modifications and invertible modifications using H.map₂.

A key asymmetry appears here:

~~~text
postcompose H (id_F).app a = H.map (𝟙 (F.obj a))
native id_(F ; H).app a      = 𝟙 (H.obj (F.obj a))
~~~

These are not definitionally equal for non-strict H.

## 11. Identity comparison and triangulator postcomposition — v5.63

v5.63 closes that asymmetry using exactly:

~~~text
H.mapId (F.obj a) :
  H.map (𝟙 (F.obj a)) ≅ 𝟙 (H.obj (F.obj a))
~~~

StrongTransPostcomposition.identityIso is the invertible modification:

~~~text
postcompose H (id_F) ≅ id_(F ; H)
~~~

Its naturality is proved from native mapComp_id_left/right and map₂ unitor coherence, without strictifying H.

The full postcomposed triangulator then has:

~~~text
triangle :=
  postcompose H T.triangle

contraction :=
  postcompose H T.contraction
    ; identityIso F H
~~~

Therefore both precomposition and postcomposition now preserve the full triangulator package while keeping non-strict comparison data explicit.

## 12. Current higher-coherence frontier

The next formal target is no longer “construct unit/counit” or “construct triangle modifications.” Those are closed.

### A. Modification-level horizontal pastes

Use the v5.61 precomposition and v5.63 postcomposition interfaces to construct the exact higher pastes involving the stored forward and reverse triangulator contractions.

The implementation must preserve:

- actual associators and unitors;
- native pseudofunctor mapId / mapComp;
- the original eta, eps, and triangle contractions;
- the distinction between the two functor bicategories.

### B. Typed swallowtail predicates

State the missing coherence equations before claiming a stronger structure.

Schematic form:

~~~text
forward swallowtail :
  one modification paste = the other modification paste

reverse swallowtail :
  one modification paste = the other modification paste
~~~

The actual Lean terms must include all required associator/unitor/reassociation cells; no strict 3-category shorthand may be silently substituted.

### C. Actual-lift proof

Instantiate the predicates for:

~~~text
exactLiftableActualLiftIncoherentBiadjunctionDatum
~~~

and prove them for the existing stored triangulators.

If a standard adjustment of one triangulator is mathematically required, make that adjustment explicit, prove the required law, and record exactly which data remain unchanged.

### D. Stronger certificate only after proof

Only after the swallowtail laws are formalized and proved should KuuOS introduce a structure named coherent biadjunction, biadjoint biequivalence, or equivalent stronger terminology.

## 13. Other research frontiers

### Broader mapping principle

A schematic principle such as

~~~text
AdmissibleContextualSystems(C, X) ~ Fun(DO(C, W, J, H), X)
~~~

is not yet an unrestricted theorem. Any extension must state the higher source/target, variance, atlas alignment, labels, permitted morphisms, and exact-liftability boundary.

### Descent across presentations

Continue separating:

~~~text
fixed-presentation equivalence
coherent transport between presentations
descent / gluing
presentation-independent invariant content
~~~

Equivalent carriers do not by themselves identify provenance or chosen presentations.

### AI-facing integration

Use the formal layer to constrain contextual reasoning, retrieval, and transport while keeping observation, provenance, authorization, and re-observation explicit. Runtime usefulness and theorem authority remain separate.

## 14. Lean proof-engineering lessons

**Preserve non-strict comparison data.** mapId and mapComp are part of the theorem, not implementation noise.

**Header-first elaboration matters.** Explicit declaration headers are elaborated before the body; unresolved label/universe arguments must be supplied in the header.

**Reassociation is coherence.** Do not assert equality of independently bracketed pseudofunctor composites; compare their native coherence fields.

**Bind native hom categories explicitly when needed.** Generic Iso headers may not carry enough information for typeclass search to reconstruct the modification universe.

**Prefer library extensionality to generic ext.** Pseudofunctor.StrongTrans.homCategory.ext follows the actual Hom wrapper and modification structure.

**Do not over-simplify equality proofs.** A useful component equality can be simplified to True; pass the exact equality when that is what the goal needs.

**Use change only at a truly definitional boundary.** Pseudofunctor/StrongTrans projections can be reducibility-sensitive. Normalize with library lemmas first; apply change only after nontrivial coherence has been eliminated.

**Postcomposition identity requires mapId.** The distinction between H.map (𝟙 _) and 𝟙 _ is real for a non-strict pseudofunctor.

**Read the whole file and whole CI log.** First errors may expose the root issue; later unknown identifiers, typeclass failures, or sorryAx can be cascades.

**Validation is not theorem authority.** Record exact PR head, run, synthetic merge, and final canonical merge separately.

## 15. Reproduction and document maintenance

~~~bash
git clone https://github.com/itakura-hidetoshi/KuuOS.git KuuOS-repro
cd KuuOS-repro
git checkout f133bd0b439e4997078a8ef460492ceacaa4ba1a

lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationStrongTransPostcompositionIdentityTriangulatorV5_63
~~~

Useful endpoints:

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationExactLiftableActualLiftCoherentBiequivalenceV5_57 \
  KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58 \
  KUOS.DependentOriginationExactLiftableActualLiftIncoherentBiadjunctionV5_59 \
  KUOS.DependentOriginationExactLiftableActualLiftIncoherentBiadjunctionHorizontalWhiskeringV5_60 \
  KUOS.DependentOriginationStrongTransModificationPrecompositionV5_61 \
  KUOS.DependentOriginationStrongTransModificationPostcompositionV5_62 \
  KUOS.DependentOriginationStrongTransPostcompositionIdentityTriangulatorV5_63
~~~

Aggregate/runtime commands remain separate entry points:

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
PYTHONPATH=. python3 runtime/kuuos_current_check.py
~~~

Keep [README.md](README.md) and this roadmap aligned on the same theorem-bearing snapshot. A later docs-only merge may advance main without changing the theorem-bearing baseline.
