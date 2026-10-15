import KUOS.DependentOriginationCorrectedGeneratedRouteV2_97
import KUOS.DependentOriginationGeneratedFactorizationV2_68
import Mathlib.Tactic.CategoryTheory.Bicategory.Basic

namespace KUOS.DependentOriginationFiveRouteFactorizationV2_98

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
open KUOS.DependentOriginationGeneratedFactorizationV2_68

attribute [local simp]
  CategoryTheory.PrelaxFunctor.map₂_eqToHom
  CategoryTheory.eqToHom_map
  CategoryTheory.Cat.eqToHom_app

universe u v uH vH

/-!
# Five-route factorization criterion v2.98

v2.68 obtained higher-localization factorization from global generated
path-independence.  v2.69 showed that global generated holonomy need not be
trivial under weak admissibility alone.  The correction program v2.70--v2.97
therefore should not try to erase every generated loop unnecessarily.

The exact v2.68 proof only consumes five families of route equalities:

* quotient associativity,
* quotient left unit,
* quotient right unit,
* comparison identity,
* comparison composition.

This file isolates those five equalities as the minimal route-level interface
used by the existing factorization construction.

Thus the sufficient chain is sharpened from

```text
all generated loops trivial
  -> global path independence
  -> factorization
```

to

```text
the five required generated route families agree
  -> five coherence defects vanish
  -> higher-localization factorization.
```

This is the right target for correction: a future coherent correction theorem
only has to repair these five route families, not every generated loop in the
free localization syntax.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Exactly the five generated route equalities consumed by the v2.59/v2.60
coherence construction. -/
structure FiveGeneratedCoherenceRouteEqualities
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) : Prop where
  associator :
    ∀ {X Y Z T : W.Localization}
      (f : X ⟶ Y) (g : Y ⟶ Z) (h : Z ⟶ T),
      generatedLocalization2CellEvaluationIso W R D
          (generatedQuotientAssociatorRoute W f g h) =
        generatedLocalization2CellEvaluationIso W R D
          (generatedQuotientAssociatorDirect W f g h)
  leftUnitor :
    ∀ {X Y : W.Localization} (f : X ⟶ Y),
      generatedLocalization2CellEvaluationIso W R D
          (generatedQuotientLeftUnitorRoute W f) =
        generatedLocalization2CellEvaluationIso W R D
          (generatedQuotientLeftUnitorDirect W f)
  rightUnitor :
    ∀ {X Y : W.Localization} (f : X ⟶ Y),
      generatedLocalization2CellEvaluationIso W R D
          (generatedQuotientRightUnitorRoute W f) =
        generatedLocalization2CellEvaluationIso W R D
          (generatedQuotientRightUnitorDirect W f)
  comparisonIdentity :
    ∀ X : Context,
      generatedLocalization2CellEvaluationIso W R D
          (generatedComparisonIdentityRawRoute W X) =
        generatedLocalization2CellEvaluationIso W R D
          (generatedComparisonIdentityQuotientRoute W X)
  comparisonComposition :
    ∀ {X Y Z : Context} (f : X ⟶ Y) (g : Y ⟶ Z),
      generatedLocalization2CellEvaluationIso W R D
          (generatedComparisonCompositionRawRoute W f g) =
        generatedLocalization2CellEvaluationIso W R D
          (generatedComparisonCompositionQuotientRoute W f g)

/-- Global generated path-independence implies the five route equalities, but
v2.98 does not require path-independence away from these five families. -/
def fiveGeneratedCoherenceRouteEqualities_of_pathIndependent
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (hPI : GeneratedEvaluationPathIndependent W R D) :
    FiveGeneratedCoherenceRouteEqualities W R D where
  associator := generatedQuotientAssociatorRoutes_evaluation_eq W R D hPI
  leftUnitor := generatedQuotientLeftUnitorRoutes_evaluation_eq W R D hPI
  rightUnitor := generatedQuotientRightUnitorRoutes_evaluation_eq W R D hPI
  comparisonIdentity := generatedComparisonIdentityRoutes_evaluation_eq W R D hPI
  comparisonComposition :=
    generatedComparisonCompositionRoutes_evaluation_eq W R D hPI

/-- The first three route equalities directly construct coherent quotient
transport with the canonical generated mapId/mapComp choices. -/
noncomputable def coherentGeneratedQuotientTransportDataOfFiveRoutes
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (H : FiveGeneratedCoherenceRouteEqualities W R D) :
    CoherentQuotientTransportData (W := W) R D where
  mapId := generatedIdentityMapIso W R D
  mapComp := generatedCompositionMapIso W R D
  map₂_associator := by
    intro X Y Z T f g h
    have heq := congrArg Iso.hom (H.associator f g h)
    simp only [generatedQuotientAssociatorRoute,
      generatedQuotientAssociatorDirect,
      generatedCompositionMapIso,
      quotientRepresentativeMap,
      generatedLocalization2CellEvaluationIso_trans,
      generatedLocalization2CellEvaluationIso_symm,
      generatedLocalization2CellEvaluationIso_whiskerLeft_hom,
      generatedLocalization2CellEvaluationIso_whiskerRight_hom,
      generatedLocalization2CellEvaluationIso_ofEq_hom,
      Iso.trans_hom, Iso.trans_inv, Iso.symm_hom, id_eq,
      eqToIso.hom, eqToIso.inv,
      whiskerLeftIso_hom, whiskerRightIso_hom,
      Bicategory.Strict.associator_eqToIso] at heq ⊢
    have heqNat := congrArg (fun η => η.toNatTrans) heq
    apply Cat.Hom₂.ext
    ext A
    have heqA := NatTrans.congr_app heqNat A
    set_option backward.isDefEq.respectTransparency false in
      simpa only [Cat.Hom.comp_toFunctor, Functor.comp_obj, Cat.Hom.comp_obj,
        Cat.whiskerLeft_app, Cat.whiskerRight_app,
        Cat.Hom₂.id_app, Cat.Hom₂.comp_app, Cat.eqToHom_app,
        Functor.map_comp, eqToHom_map, eqToHom_refl,
        eqToHom_trans, eqToHom_trans_assoc,
        Category.comp_id, Category.id_comp, Category.assoc] using heqA
  map₂_left_unitor := by
    intro X Y f
    have heq := congrArg Iso.hom (H.leftUnitor f)
    simp only [generatedQuotientLeftUnitorRoute,
      generatedQuotientLeftUnitorDirect,
      generatedIdentityMapIso, generatedCompositionMapIso,
      quotientRepresentativeMap,
      generatedLocalization2CellEvaluationIso_trans,
      generatedLocalization2CellEvaluationIso_whiskerRight_hom,
      generatedLocalization2CellEvaluationIso_ofEq_hom,
      Iso.trans_hom, Iso.symm_hom, id_eq,
      eqToIso.hom, eqToIso.inv,
      whiskerRightIso_hom,
      Bicategory.Strict.leftUnitor_eqToIso] at heq ⊢
    have heqNat := congrArg (fun η => η.toNatTrans) heq
    apply Cat.Hom₂.ext
    ext A
    have heqA := NatTrans.congr_app heqNat A
    set_option backward.isDefEq.respectTransparency false in
      simpa only [Cat.Hom.comp_toFunctor, Functor.comp_obj, Cat.Hom.comp_obj,
        Cat.whiskerLeft_app, Cat.whiskerRight_app,
        Cat.Hom₂.id_app, Cat.Hom₂.comp_app, Cat.eqToHom_app,
        Functor.map_comp, eqToHom_map, eqToHom_refl,
        eqToHom_trans, eqToHom_trans_assoc,
        Category.comp_id, Category.id_comp, Category.assoc] using heqA
  map₂_right_unitor := by
    intro X Y f
    have heq := congrArg Iso.hom (H.rightUnitor f)
    simp only [generatedQuotientRightUnitorRoute,
      generatedQuotientRightUnitorDirect,
      generatedIdentityMapIso, generatedCompositionMapIso,
      quotientRepresentativeMap,
      generatedLocalization2CellEvaluationIso_trans,
      generatedLocalization2CellEvaluationIso_whiskerLeft_hom,
      generatedLocalization2CellEvaluationIso_ofEq_hom,
      Iso.trans_hom, Iso.symm_hom, id_eq,
      eqToIso.hom, eqToIso.inv,
      whiskerLeftIso_hom,
      Bicategory.Strict.rightUnitor_eqToIso] at heq ⊢
    have heqNat := congrArg (fun η => η.toNatTrans) heq
    apply Cat.Hom₂.ext
    ext A
    have heqA := NatTrans.congr_app heqNat A
    set_option backward.isDefEq.respectTransparency false in
      simpa only [Cat.Hom.comp_toFunctor, Functor.comp_obj, Cat.Hom.comp_obj,
        Cat.whiskerLeft_app, Cat.whiskerRight_app,
        Cat.Hom₂.id_app, Cat.Hom₂.comp_app, Cat.eqToHom_app,
        Functor.map_comp, eqToHom_map, eqToHom_refl,
        eqToHom_trans, eqToHom_trans_assoc,
        Category.comp_id, Category.id_comp, Category.assoc] using heqA

/-- The first three route equalities kill the three quotient-transport defects. -/
noncomputable def generatedQuotientTransportDefectsTrivialOfFiveRoutes
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (H : FiveGeneratedCoherenceRouteEqualities W R D) :
    QuotientTransportDefectsTrivial W R D
      (generatedPointwiseGeneralWChoiceData W R D) where
  associator := by
    intro X Y Z T f g h
    apply (quotientAssociatorDefect_eq_refl_iff W R D
      (generatedPointwiseGeneralWChoiceData W R D) f g h).2
    simpa only [generatedPointwiseGeneralWChoiceData_mapComp,
      coherentGeneratedQuotientTransportDataOfFiveRoutes] using
      (coherentGeneratedQuotientTransportDataOfFiveRoutes W R D H).map₂_associator f g h
  leftUnitor := by
    intro X Y f
    apply (quotientLeftUnitorDefect_eq_refl_iff W R D
      (generatedPointwiseGeneralWChoiceData W R D) f).2
    simpa only [generatedPointwiseGeneralWChoiceData_mapId,
      generatedPointwiseGeneralWChoiceData_mapComp,
      coherentGeneratedQuotientTransportDataOfFiveRoutes] using
      (coherentGeneratedQuotientTransportDataOfFiveRoutes W R D H).map₂_left_unitor f
  rightUnitor := by
    intro X Y f
    apply (quotientRightUnitorDefect_eq_refl_iff W R D
      (generatedPointwiseGeneralWChoiceData W R D) f).2
    simpa only [generatedPointwiseGeneralWChoiceData_mapId,
      generatedPointwiseGeneralWChoiceData_mapComp,
      coherentGeneratedQuotientTransportDataOfFiveRoutes] using
      (coherentGeneratedQuotientTransportDataOfFiveRoutes W R D H).map₂_right_unitor f

/-- The last two route equalities construct the exact strong comparison on the
coherent quotient carrier built from the first three. -/
noncomputable def coherentGeneratedPresentationComparisonDataOfFiveRoutes
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (H : FiveGeneratedCoherenceRouteEqualities W R D) :
    let L := generatedPointwiseGeneralWChoiceData W R D
    let hQ := generatedQuotientTransportDefectsTrivialOfFiveRoutes W R D H
    CoherentPresentationComparisonData (W := W) R D
      (coherentQuotientTransportDataOfTrivialDefects W R D L hQ) := by
  let L := generatedPointwiseGeneralWChoiceData W R D
  let hQ := generatedQuotientTransportDefectsTrivialOfFiveRoutes W R D H
  let T := coherentQuotientTransportDataOfTrivialDefects W R D L hQ
  refine
    { mapIso := ?_
      naturality_id := ?_
      naturality_comp := ?_ }
  · intro X Y f
    change quotientRepresentativeMap W R D (W.Q.map f) ≅ R.map f.toLoc
    exact generatedPresentationMapIso W R D f
  · intro X
    have heq := congrArg Iso.hom (H.comparisonIdentity X)
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
    have heq := congrArg Iso.hom (H.comparisonComposition f g)
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
      generatedPresentationMapIso, generatedCompositionMapIso,
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
      (generatedLocalization2CellEvaluationIso W R D
        (generatedPresentationRepresentativeCell W g)).hom.toNatTrans.naturality
        ((generatedLocalization2CellEvaluationIso W R D
          (generatedPresentationRepresentativeCell W f)).hom.toNatTrans.app A)
    simp only [freePathEvaluator_map_ordinary] at hnat
    set_option backward.isDefEq.respectTransparency false in
      simp only [Cat.Hom.id_toFunctor, Cat.Hom.comp_toFunctor,
        Functor.id_obj, Functor.id_map, Functor.comp_obj,
        Cat.whiskerLeft_app, Cat.whiskerRight_app,
        Cat.Hom₂.id_app, Cat.Hom₂.comp_app, Cat.eqToHom_app,
        eqToHom_refl, Category.comp_id, Category.id_comp,
        Category.assoc] at heqA ⊢
    erw [← hnat]
    set_option backward.isDefEq.respectTransparency false in
      simpa only [generating2CellEvaluationIso,
        generatedLocalization2CellEvaluationIso_whiskerLeft_hom,
        Iso.trans_hom, Iso.symm_hom, eqToIso.hom, eqToIso.inv,
        whiskerLeftIso_hom,
        Cat.Hom.comp_toFunctor, Cat.Hom.comp_obj, Cat.Hom.comp_map,
        Cat.whiskerLeft_app, Cat.Hom₂.comp_app, Cat.eqToHom_app,
        Functor.comp_obj, Functor.comp_map, Functor.map_comp,
        eqToHom_map, eqToHom_refl, eqToHom_trans, eqToHom_trans_assoc,
        Category.comp_id, Category.id_comp, Category.assoc] using heqA

/-- The last two route equalities kill the two comparison defects. -/
noncomputable def generatedComparisonDefectsTrivialOfFiveRoutes
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (H : FiveGeneratedCoherenceRouteEqualities W R D) :
    let L := generatedPointwiseGeneralWChoiceData W R D
    let hQ := generatedQuotientTransportDefectsTrivialOfFiveRoutes W R D H
    ComparisonDefectsTrivial W R D L hQ := by
  let L := generatedPointwiseGeneralWChoiceData W R D
  let hQ := generatedQuotientTransportDefectsTrivialOfFiveRoutes W R D H
  refine
    { identity := ?_
      composition := ?_ }
  · intro X
    apply (comparisonIdentityDefect_eq_refl_iff W R D L hQ X).2
    exact
      (coherentGeneratedPresentationComparisonDataOfFiveRoutes W R D H).naturality_id X
  · intro X Y Z f g
    apply (comparisonCompositionDefect_eq_refl_iff W R D L hQ f g).2
    exact
      (coherentGeneratedPresentationComparisonDataOfFiveRoutes W R D H).naturality_comp f g

/-- The five route equalities are sufficient for all five v2.65 defects to
vanish on the canonical generated pointwise bundle. -/
noncomputable def generatedFiveCoherenceDefectsTrivialOfFiveRoutes
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (H : FiveGeneratedCoherenceRouteEqualities W R D) :
    FiveCoherenceDefectsTrivial W R D
      (generatedPointwiseGeneralWChoiceData W R D) := by
  let hQ := generatedQuotientTransportDefectsTrivialOfFiveRoutes W R D H
  exact
    ⟨hQ, generatedComparisonDefectsTrivialOfFiveRoutes W R D H⟩

/-- Sharpened Stage-I sufficient theorem: global generated path-independence is
not required; equality of the five route families actually used by the
coherence laws already yields factorization. -/
theorem hasHigherLocalizationFactorization_of_fiveGeneratedCoherenceRouteEqualities
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (H : FiveGeneratedCoherenceRouteEqualities W R D) :
    HasHigherLocalizationFactorization (W := W) R :=
  hasHigherLocalizationFactorization_of_fiveTrivialDefects W R D
    (generatedPointwiseGeneralWChoiceData W R D)
    (generatedFiveCoherenceDefectsTrivialOfFiveRoutes W R D H)

/-- Admissibility-shaped form of the sharpened five-route criterion. -/
theorem hasHigherLocalizationFactorization_of_admissible_and_fiveGeneratedCoherenceRouteEqualities
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (hR : IsHigherWAdmissible W R)
    (H :
      FiveGeneratedCoherenceRouteEqualities W R
        (pointwiseWAdjointEquivalenceDataOfAdmissible W hR)) :
    HasHigherLocalizationFactorization (W := W) R :=
  hasHigherLocalizationFactorization_of_fiveGeneratedCoherenceRouteEqualities
    W R (pointwiseWAdjointEquivalenceDataOfAdmissible W hR) H

/-!
## Boundary fixed by v2.98

The Stage-I sufficient hypothesis has now been reduced to the exact finite
coherence interface used by the construction:

```text
five generated route equalities
        |
        v
FiveCoherenceDefectsTrivial
        |
        v
HigherLocalizationFactorization.
```

Global `GeneratedHolonomyTrivial` remains a sufficient way to obtain this
interface, but it is no longer the target correction condition.

The next theorem unit should therefore define a coherent correction package
whose witnesses repair exactly these five route families and prove that the
repaired package induces `FiveGeneratedCoherenceRouteEqualities` for a
gauge-adjusted pointwise choice.  This is strictly weaker than requiring all
generated loop holonomies to vanish.
-/

end KUOS.DependentOriginationFiveRouteFactorizationV2_98
