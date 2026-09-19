import KUOS.DependentOriginationGeneratedQuotientCoherenceV2_68
import Mathlib.Tactic.CategoryTheory.Bicategory.Basic
import Mathlib.Tactic.Convert

namespace KUOS.DependentOriginationGeneratedFactorizationV2_68

open CategoryTheory
open CategoryTheory.Bicategory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationFreePathEvaluatorV2_57
open KUOS.DependentOriginationCoherentQuotientTransportV2_59
open KUOS.DependentOriginationCoherentComparisonFactorizationV2_60
open KUOS.DependentOriginationPointwiseGeneralWChoiceV2_61
open KUOS.DependentOriginationCoherenceDefectsV2_65
open KUOS.DependentOriginationGeneratedLocalizationHolonomyV2_68
open KUOS.DependentOriginationGeneratedWhiskeringV2_68
open KUOS.DependentOriginationGeneratedPointwiseChoiceV2_68
open KUOS.DependentOriginationGeneratedCoherenceRoutesV2_68
open KUOS.DependentOriginationGeneratedQuotientCoherenceV2_68

attribute [local simp]
  CategoryTheory.PrelaxFunctor.map₂_eqToHom
  CategoryTheory.eqToHom_map
  CategoryTheory.Cat.eqToHom_app

universe u v uH vH

/-!
# Generated holonomy factorization criterion v2.68

The preceding v2.68 layers retain the complete localization relation syntax,
evaluate it canonically, construct the five concrete coherence-route pairs, and
show that generated path-independence kills the first three v2.65 quotient
transport defects.

This file closes the same argument for the two StrongTrans comparison laws.  The
raw identity/composition routes and quotient identity/composition routes have the
same endpoints.  Path-independence identifies their evaluations; strict `Cat`
bicategorical normalization turns those two equalities into exactly the v2.60
comparison laws.

Consequently all five v2.65 defects vanish for the exact canonical generated
pointwise bundle, and the already-proved v2.65 construction yields the genuine
v2.10 higher-localization factorization.

The theorem proved here is the conditional criterion

```text
GeneratedHolonomyTrivial W R D
  -> HasHigherLocalizationFactorization W R.
```

It does not assert that weak W-admissibility forces generated holonomy to be
trivial.  That implication remains the decisive post-v2.68 truth test.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Generated path-independence supplies the exact v2.60 comparison data on
the coherent quotient carrier.  The two route equalities are normalized only
after passing from Cat 2-cells to natural transformations and then components,
so Lean 4.30 never has to identify the Cat wrapper by definitional equality. -/
noncomputable def coherentGeneratedPresentationComparisonDataOfPathIndependent
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (hPI : GeneratedEvaluationPathIndependent W R D) :
    let L := generatedPointwiseGeneralWChoiceData W R D
    let hQ := generatedQuotientTransportDefectsTrivialOfPathIndependent W R D hPI
    CoherentPresentationComparisonData (W := W) R D
      (coherentQuotientTransportDataOfTrivialDefects W R D L hQ) := by
  let L := generatedPointwiseGeneralWChoiceData W R D
  let hQ := generatedQuotientTransportDefectsTrivialOfPathIndependent W R D hPI
  let T := coherentQuotientTransportDataOfTrivialDefects W R D L hQ
  refine
    { mapIso := ?_
      naturality_id := ?_
      naturality_comp := ?_ }
  · intro X Y f
    change quotientRepresentativeMap W R D (W.Q.map f) ≅ R.map f.toLoc
    exact generatedPresentationMapIso W R D f
  · intro X
    have heq := congrArg Iso.hom
      (generatedComparisonIdentityRoutes_evaluation_eq W R D hPI X)
    simp [identityComponentNaturalityIso,
      restrictHigherLocalizedSystem,
      coherentQuotientLocalizedHigherSystem,
      quotientLocalizationPseudofunctor,
      higherPresentationUnitFunctor,
      CategoryTheory.Pseudofunctor.comp,
      CategoryTheory.Functor.toPseudofunctor,
      CategoryTheory.pseudofunctorOfIsLocallyDiscrete,
      generatedComparisonIdentityRawRoute,
      generatedComparisonIdentityQuotientRoute,
      generatedPresentationMapIso, generatedIdentityMapIso,
      generatedPointwiseGeneralWChoiceData,
      coherentQuotientTransportDataOfTrivialDefects,
      generatedLocalization2CellEvaluationIso_trans,
      generatedLocalization2CellEvaluationIso_ofEq_hom,
      generatedLocalization2CellEvaluationIso_ofGenerating_hom,
      Iso.trans_hom, Iso.symm_hom, eqToIso.hom, eqToIso.inv,
      Bicategory.Strict.leftUnitor_eqToIso,
      Bicategory.Strict.rightUnitor_eqToIso] at heq ⊢
    have heqNat := congrArg (fun η => η.toNatTrans) heq
    apply Cat.Hom₂.ext
    ext A
    have heqA := NatTrans.congr_app heqNat A
    set_option backward.isDefEq.respectTransparency false in
      simpa only [Cat.Hom.id_toFunctor, Cat.Hom.id_obj, Cat.Hom.id_map,
        Cat.Hom.comp_toFunctor, Cat.Hom.comp_obj, Cat.Hom.comp_map,
        Functor.id_obj, Functor.id_map, Functor.comp_obj, Functor.comp_map,
        Cat.whiskerLeft_app, Cat.whiskerRight_app,
        Cat.Hom₂.id_app, Cat.Hom₂.comp_app, Cat.eqToHom_app,
        Functor.map_comp, eqToHom_map, eqToHom_refl,
        eqToHom_trans, eqToHom_trans_assoc,
        Category.comp_id, Category.id_comp, Category.assoc] using heqA
  · intro X Y Z f g
    have heq := congrArg Iso.hom
      (generatedComparisonCompositionRoutes_evaluation_eq W R D hPI f g)
    simp [identityComponentNaturalityIso,
      restrictHigherLocalizedSystem,
      coherentQuotientLocalizedHigherSystem,
      quotientLocalizationPseudofunctor,
      higherPresentationUnitFunctor,
      CategoryTheory.Pseudofunctor.comp,
      CategoryTheory.Functor.toPseudofunctor,
      CategoryTheory.pseudofunctorOfIsLocallyDiscrete,
      generatedComparisonCompositionRawRoute,
      generatedComparisonCompositionQuotientRoute,
      generatedCompositionMapIso,
      generatedPointwiseGeneralWChoiceData,
      coherentQuotientTransportDataOfTrivialDefects,
      generatedLocalization2CellEvaluationIso_trans,
      generatedLocalization2CellEvaluationIso_whiskerRight_hom,
      generatedLocalization2CellEvaluationIso_ofEq_hom,
      generatedLocalization2CellEvaluationIso_ofGenerating_hom,
      Iso.trans_hom, Iso.symm_hom, eqToIso.hom, eqToIso.inv,
      whiskerRightIso_hom,
      Bicategory.Strict.leftUnitor_eqToIso,
      Bicategory.Strict.rightUnitor_eqToIso,
      Bicategory.Strict.associator_eqToIso,
      Category.assoc] at heq ⊢
    have heqNat := congrArg (fun η => η.toNatTrans) heq
    apply Cat.Hom₂.ext
    ext A
    have heqA := NatTrans.congr_app heqNat A
    have hnat :=
      (generatedPresentationMapIso W R D g).hom.toNatTrans.naturality
        ((generatedPresentationMapIso W R D f).hom.toNatTrans.app A)
    set_option backward.isDefEq.respectTransparency false in
      simp only [Cat.Hom.id_toFunctor, Cat.Hom.comp_toFunctor,
        Functor.id_obj, Functor.id_map, Functor.comp_obj,
        Cat.whiskerLeft_app, Cat.whiskerRight_app,
        Cat.Hom₂.id_app, Cat.Hom₂.comp_app, Cat.eqToHom_app,
        eqToHom_refl, Category.comp_id, Category.id_comp,
        Category.assoc] at heqA hnat ⊢
    rw [← hnat]
    set_option backward.isDefEq.respectTransparency false in
      simpa only [generatedPresentationMapIso,
        generating2CellEvaluationIso,
        generatedLocalization2CellEvaluationIso_whiskerLeft_hom,
        Iso.trans_hom, Iso.symm_hom, eqToIso.hom, eqToIso.inv,
        whiskerLeftIso_hom,
        Cat.Hom.comp_toFunctor, Cat.Hom.comp_obj, Cat.Hom.comp_map,
        Cat.whiskerLeft_app, Cat.Hom₂.comp_app, Cat.eqToHom_app,
        Functor.comp_obj, Functor.comp_map, Functor.map_comp,
        eqToHom_map, eqToHom_refl, eqToHom_trans, eqToHom_trans_assoc,
        Category.comp_id, Category.id_comp, Category.assoc] using heqA

/-- The two v2.65 StrongTrans comparison defects vanish under generated
path-independence, after the first three quotient defects have been killed. -/
noncomputable def generatedComparisonDefectsTrivialOfPathIndependent
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (hPI : GeneratedEvaluationPathIndependent W R D) :
    let L := generatedPointwiseGeneralWChoiceData W R D
    let hQ := generatedQuotientTransportDefectsTrivialOfPathIndependent W R D hPI
    ComparisonDefectsTrivial W R D L hQ := by
  let L := generatedPointwiseGeneralWChoiceData W R D
  let hQ := generatedQuotientTransportDefectsTrivialOfPathIndependent W R D hPI
  refine
    { identity := ?_
      composition := ?_ }
  · intro X
    apply (comparisonIdentityDefect_eq_refl_iff W R D L hQ X).2
    exact
      (coherentGeneratedPresentationComparisonDataOfPathIndependent W R D hPI).naturality_id X
  · intro X Y Z f g
    apply (comparisonCompositionDefect_eq_refl_iff W R D L hQ f g).2
    exact
      (coherentGeneratedPresentationComparisonDataOfPathIndependent W R D hPI).naturality_comp f g

/-- All five v2.65 coherence defects vanish for the exact canonical generated
pointwise bundle under generated evaluation path-independence. -/
noncomputable def generatedFiveCoherenceDefectsTrivialOfPathIndependent
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (hPI : GeneratedEvaluationPathIndependent W R D) :
    FiveCoherenceDefectsTrivial W R D
      (generatedPointwiseGeneralWChoiceData W R D) := by
  let hQ := generatedQuotientTransportDefectsTrivialOfPathIndependent W R D hPI
  exact
    ⟨hQ, generatedComparisonDefectsTrivialOfPathIndependent W R D hPI⟩

/-- Trivial generated holonomy kills all five coherence defects. -/
noncomputable def generatedFiveCoherenceDefectsTrivialOfHolonomyTrivial
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (htriv : GeneratedHolonomyTrivial W R D) :
    FiveCoherenceDefectsTrivial W R D
      (generatedPointwiseGeneralWChoiceData W R D) :=
  generatedFiveCoherenceDefectsTrivialOfPathIndependent W R D
    (generatedEvaluationPathIndependent_of_holonomyTrivial W R D htriv)

/-- Main v2.68 factorization theorem: vanishing of fully generated localization
2-holonomy is sufficient for the genuine general-W higher-localization
factorization. -/
theorem hasHigherLocalizationFactorization_of_generatedHolonomyTrivial
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (htriv : GeneratedHolonomyTrivial W R D) :
    HasHigherLocalizationFactorization (W := W) R :=
  hasHigherLocalizationFactorization_of_fiveTrivialDefects W R D
    (generatedPointwiseGeneralWChoiceData W R D)
    (generatedFiveCoherenceDefectsTrivialOfHolonomyTrivial W R D htriv)

/-- Admissibility-shaped form of the v2.68 criterion.  Weak W-admissibility
provides the v2.56 pointwise adjoint-equivalence data; generated holonomy
triviality remains an explicit additional hypothesis. -/
theorem hasHigherLocalizationFactorization_of_admissible_and_generatedHolonomyTrivial
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (hR : IsHigherWAdmissible W R)
    (htriv : GeneratedHolonomyTrivial W R
      (pointwiseWAdjointEquivalenceDataOfAdmissible W hR)) :
    HasHigherLocalizationFactorization (W := W) R :=
  hasHigherLocalizationFactorization_of_generatedHolonomyTrivial W R
    (pointwiseWAdjointEquivalenceDataOfAdmissible W hR) htriv

/-!
## v2.68 boundary and decisive next truth test

The proved chain is now

```text
GeneratedHolonomyTrivial
  <-> GeneratedEvaluationPathIndependent
  -> three generated quotient coherence laws
  -> QuotientTransportDefectsTrivial
  -> two generated comparison coherence laws
  -> ComparisonDefectsTrivial
  -> FiveCoherenceDefectsTrivial
  -> HasHigherLocalizationFactorization.
```

Together with weak admissibility this gives the exact conditional statement

```text
IsHigherWAdmissible W R
+ GeneratedHolonomyTrivial W R D_adm
  -> HasHigherLocalizationFactorization W R.
```

What is deliberately still open is

```text
IsHigherWAdmissible W R
  -> GeneratedHolonomyTrivial W R D_adm  ?
```

The next layer must decide this implication by proof or by an explicit
nontrivial generated-holonomy countermodel.  No claim about its truth value is
made here.
-/

end KUOS.DependentOriginationGeneratedFactorizationV2_68
