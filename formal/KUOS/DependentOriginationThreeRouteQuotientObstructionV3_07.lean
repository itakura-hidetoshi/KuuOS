import KUOS.DependentOriginationQuotientDefectOrbitV3_06
import KUOS.DependentOriginationFiveRouteFactorizationV2_98

namespace KUOS.DependentOriginationThreeRouteQuotientObstructionV3_07

open CategoryTheory
open CategoryTheory.Bicategory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationFreePathEvaluatorV2_57
open KUOS.DependentOriginationCoherentQuotientTransportV2_59
open KUOS.DependentOriginationCoherenceDefectsV2_65
open KUOS.DependentOriginationGeneratedLocalizationHolonomyV2_68
open KUOS.DependentOriginationGeneratedWhiskeringV2_68
open KUOS.DependentOriginationGeneratedPointwiseChoiceV2_68
open KUOS.DependentOriginationGeneratedCoherenceRoutesV2_68
open KUOS.DependentOriginationGeneratedQuotientCoherenceV2_68
open KUOS.DependentOriginationFiveRouteFactorizationV2_98
open KUOS.DependentOriginationQuotientDefectOrbitV3_06

attribute [local simp]
  CategoryTheory.PrelaxFunctor.map₂_eqToHom
  CategoryTheory.eqToHom_map
  CategoryTheory.Cat.eqToHom_app

universe u v uH vH

/-!
# Three-route quotient obstruction v3.07

The v2.69 countermodel rules out using global generated-holonomy triviality as
the first-stage target.  v2.98 already showed that five explicit route families
suffice for the complete factorization.  v3.06 identifies the first stage
exactly as the gauge orbit of the three quotient defects.

This file isolates the route-level interface for that first stage alone.

Only three generated route pairs are needed to construct the quotient
pseudofunctor carrier:

* quotient associativity;
* quotient left unit;
* quotient right unit.

No comparison-identity or comparison-composition route is required yet.
Consequently the first higher-localization obstruction is already local to
these three finite coherence families; arbitrary generated loops are irrelevant
to this stage.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Exactly the three generated route equalities consumed by the quotient
pseudofunctor coherence laws. -/
structure ThreeGeneratedQuotientRouteEqualities
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

/-- The first three fields of the v2.98 five-route package are exactly this
quotient-stage route interface. -/
def threeGeneratedQuotientRouteEqualitiesOfFiveRoutes
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (H : FiveGeneratedCoherenceRouteEqualities W R D) :
    ThreeGeneratedQuotientRouteEqualities W R D where
  associator := H.associator
  leftUnitor := H.leftUnitor
  rightUnitor := H.rightUnitor

/-- Global generated path-independence implies the three quotient routes, but
the converse is neither required nor asserted. -/
def threeGeneratedQuotientRouteEqualities_of_pathIndependent
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (hPI : GeneratedEvaluationPathIndependent W R D) :
    ThreeGeneratedQuotientRouteEqualities W R D where
  associator := generatedQuotientAssociatorRoutes_evaluation_eq W R D hPI
  leftUnitor := generatedQuotientLeftUnitorRoutes_evaluation_eq W R D hPI
  rightUnitor := generatedQuotientRightUnitorRoutes_evaluation_eq W R D hPI

/-- Three route equalities alone construct the genuine coherent quotient
transport with the canonical generated mapId/mapComp witnesses. -/
noncomputable def coherentGeneratedQuotientTransportDataOfThreeRoutes
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (H : ThreeGeneratedQuotientRouteEqualities W R D) :
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

/-- The three finite generated route families are already sufficient for
existence of the quotient pseudofunctor carrier. -/
theorem hasCoherentQuotientTransportData_of_threeGeneratedQuotientRouteEqualities
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (H : ThreeGeneratedQuotientRouteEqualities W R D) :
    HasCoherentQuotientTransportData W R D :=
  ⟨coherentGeneratedQuotientTransportDataOfThreeRoutes W R D H⟩

/-- In the v3.06 language, equality of the three canonical route pairs forces
the quotient-defect gauge orbit to meet the zero locus. -/
theorem generatedQuotientDefectGaugeTrivializable_of_threeGeneratedQuotientRouteEqualities
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (H : ThreeGeneratedQuotientRouteEqualities W R D) :
    GeneratedQuotientDefectGaugeTrivializable W R D := by
  apply
    (generatedQuotientDefectGaugeTrivializable_iff_hasCoherentQuotientTransportData
      W R D).2
  exact hasCoherentQuotientTransportData_of_threeGeneratedQuotientRouteEqualities
    W R D H

/-!
## First-stage boundary after v3.07

The quotient carrier no longer depends on a global path-independence target:

```text
global generated path-independence
        |
        v   sufficient but unnecessary
three canonical quotient route equalities
        |
        v
coherent quotient transport
        |
        v
quotient-defect orbit trivializable.
```

The v2.69 counterexample can therefore carry arbitrary nontrivial generated
holonomy away from these three route families without obstructing the first
higher-localization stage.

What remains is to understand correction of these three route families when
their canonical evaluations do not agree: the required corrections must arise
from one compatible quotient gauge `Q=(gId,gComp)`, exactly as v3.06 records.
-/

end KUOS.DependentOriginationThreeRouteQuotientObstructionV3_07
