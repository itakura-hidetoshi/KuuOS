import KUOS.DependentOriginationGeneratedCoherenceRoutesV2_68
import KUOS.DependentOriginationCoherenceDefectsV2_65
import Mathlib.Tactic.CategoryTheory.Bicategory.Basic

namespace KUOS.DependentOriginationGeneratedQuotientCoherenceV2_68

open CategoryTheory
open CategoryTheory.Bicategory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationFreePathEvaluatorV2_57
open KUOS.DependentOriginationCoherentQuotientTransportV2_59
open KUOS.DependentOriginationPointwiseGeneralWChoiceV2_61
open KUOS.DependentOriginationCoherenceDefectsV2_65
open KUOS.DependentOriginationGeneratedLocalizationHolonomyV2_68
open KUOS.DependentOriginationGeneratedWhiskeringV2_68
open KUOS.DependentOriginationGeneratedPointwiseChoiceV2_68
open KUOS.DependentOriginationGeneratedCoherenceRoutesV2_68

universe u v uH vH

/-!
# Quotient coherence from fully generated path-independence v2.68

The five generated route pairs of the previous layer separate the genuine
localization syntax from bicategorical bookkeeping.  This file performs the
first normalization step: the associativity and two unit route equalities are
converted into exactly the three v2.59 pseudofunctor coherence equations for the
canonical generated `mapId` and `mapComp` choices.

The resulting transport is then reflected through the v2.65 iff lemmas to show
that the three quotient-transport defects of that exact pointwise bundle vanish.
No comparison law and no unrestricted holonomy-vanishing theorem is asserted in
this layer.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Generated path-independence supplies a genuine coherent quotient transport
with exactly the canonical generated pointwise identity/composition choices. -/
noncomputable def coherentGeneratedQuotientTransportData
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (hPI : GeneratedEvaluationPathIndependent W R D) :
    CoherentQuotientTransportData (W := W) R D where
  mapId := generatedIdentityMapIso W R D
  mapComp := generatedCompositionMapIso W R D
  map₂_associator := by
    intro X Y Z T f g h
    have heq := congrArg Iso.hom
      (generatedQuotientAssociatorRoutes_evaluation_eq W R D hPI f g h)
    simpa [generatedQuotientAssociatorRoute,
      generatedQuotientAssociatorDirect,
      generatedCompositionMapIso,
      generatedLocalization2CellEvaluationIso_trans,
      generatedLocalization2CellEvaluationIso_symm,
      generatedLocalization2CellEvaluationIso_whiskerLeft,
      generatedLocalization2CellEvaluationIso_whiskerRight,
      generatedLocalization2CellEvaluationIso_ofEq,
      Iso.trans_hom, Iso.symm_hom,
      whiskerLeftIso_hom, whiskerRightIso_hom,
      Functor.map_comp] using heq
  map₂_left_unitor := by
    intro X Y f
    have heq := congrArg Iso.hom
      (generatedQuotientLeftUnitorRoutes_evaluation_eq W R D hPI f)
    simpa [generatedQuotientLeftUnitorRoute,
      generatedQuotientLeftUnitorDirect,
      generatedIdentityMapIso, generatedCompositionMapIso,
      generatedLocalization2CellEvaluationIso_trans,
      generatedLocalization2CellEvaluationIso_whiskerRight,
      generatedLocalization2CellEvaluationIso_ofEq,
      Iso.trans_hom, whiskerRightIso_hom,
      Functor.map_comp, Functor.map_id] using heq
  map₂_right_unitor := by
    intro X Y f
    have heq := congrArg Iso.hom
      (generatedQuotientRightUnitorRoutes_evaluation_eq W R D hPI f)
    simpa [generatedQuotientRightUnitorRoute,
      generatedQuotientRightUnitorDirect,
      generatedIdentityMapIso, generatedCompositionMapIso,
      generatedLocalization2CellEvaluationIso_trans,
      generatedLocalization2CellEvaluationIso_whiskerLeft,
      generatedLocalization2CellEvaluationIso_ofEq,
      Iso.trans_hom, whiskerLeftIso_hom,
      Functor.map_comp, Functor.map_id] using heq

/-- The first three v2.65 defects vanish for the exact canonical generated
pointwise bundle whenever generated evaluation is path-independent. -/
noncomputable def generatedQuotientTransportDefectsTrivialOfPathIndependent
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (hPI : GeneratedEvaluationPathIndependent W R D) :
    QuotientTransportDefectsTrivial W R D
      (generatedPointwiseGeneralWChoiceData W R D) where
  associator := by
    intro X Y Z T f g h
    apply (quotientAssociatorDefect_eq_refl_iff W R D
      (generatedPointwiseGeneralWChoiceData W R D) f g h).2
    exact (coherentGeneratedQuotientTransportData W R D hPI).map₂_associator f g h
  leftUnitor := by
    intro X Y f
    apply (quotientLeftUnitorDefect_eq_refl_iff W R D
      (generatedPointwiseGeneralWChoiceData W R D) f).2
    exact (coherentGeneratedQuotientTransportData W R D hPI).map₂_left_unitor f
  rightUnitor := by
    intro X Y f
    apply (quotientRightUnitorDefect_eq_refl_iff W R D
      (generatedPointwiseGeneralWChoiceData W R D) f).2
    exact (coherentGeneratedQuotientTransportData W R D hPI).map₂_right_unitor f

/-- Trivial generated holonomy is therefore already sufficient for vanishing of
the three quotient-transport defects. -/
noncomputable def generatedQuotientTransportDefectsTrivialOfHolonomyTrivial
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (htriv : GeneratedHolonomyTrivial W R D) :
    QuotientTransportDefectsTrivial W R D
      (generatedPointwiseGeneralWChoiceData W R D) :=
  generatedQuotientTransportDefectsTrivialOfPathIndependent W R D
    (generatedEvaluationPathIndependent_of_holonomyTrivial W R D htriv)

end KUOS.DependentOriginationGeneratedQuotientCoherenceV2_68
