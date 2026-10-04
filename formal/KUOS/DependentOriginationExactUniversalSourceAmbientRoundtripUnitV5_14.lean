import KUOS.DependentOriginationExactUniversalAmbientRoundtripCounitV5_13
import KUOS.DependentOriginationExactUniversalGlobalUnitStrongTransV4_87

namespace KUOS.DependentOriginationExactUniversalSourceAmbientRoundtripUnitV5_14

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalMappingHomCategoryV4_60
open KUOS.DependentOriginationExactUniversalRealizationStrictPseudofunctorV4_70
open KUOS.DependentOriginationExactUniversalRealizationFaithfulV4_76
open KUOS.DependentOriginationExactUniversalRealizationFullyFaithfulV4_77
open KUOS.DependentOriginationExactUniversalHomEquivalenceV4_83
open KUOS.DependentOriginationExactUniversalGlobalUnitSquaresV4_86
open KUOS.DependentOriginationExactUniversalGlobalUnitStrongTransV4_87
open KUOS.DependentOriginationExactUniversalAmbientCanonicalSourceV5_11
open KUOS.DependentOriginationExactUniversalAmbientSectionPseudofunctorV5_12
open KUOS.DependentOriginationExactUniversalAmbientRoundtripCounitV5_13

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Source-to-ambient roundtrip unit v5.14

v5.12 provides an ambient pseudofunctorial section and v5.13 constructs the
ambient roundtrip counit.  On the source side the composite

  Source --realization--> Ambient --canonical section--> Source

does not preserve source labels literally: an object X is sent to the canonical
source label chosen over X.carrier.

The unit component therefore cannot be the source identity.  We choose the
canonical source one-cell whose realized lift is the identity on X.carrier.
For a source one-cell f, both sides of the pseudonaturality square realize to

  f.lift >> 1
  1 >> f.lift,

so the native right-unitor followed by inverse left-unitor gives the ambient
comparison.  Full faithfulness of exact realization lifts that comparison
uniquely to the source.

All StrongTrans coherence laws are then reflected through faithful realization
and reduce to native bicategory coherence.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

abbrev Source :=
  ExactUniversalRawObject.{u, v, uH, vH} (W := W) A

abbrev Ambient :=
  DependentOriginationCompletion2.{u, v, uH, uH, vH} (W := W) A

/-- Source roundtrip through the actual ambient completion. -/
noncomputable def exactUniversalSourceAmbientRoundtrip :
    Pseudofunctor (Source (W := W) A) (Source (W := W) A) :=
  Pseudofunctor.comp
    (exactUniversalRealization (W := W) A).toPseudofunctor
    (exactUniversalAmbientCanonicalSectionPseudofunctor (W := W) A)

/-- The source roundtrip object has exactly the original carrier, although its
source label is the canonical v5.11 label rather than literally X. -/
@[simp] theorem exactUniversalSourceAmbientRoundtrip_obj_carrier
    (X : Source (W := W) A) :
    ((exactUniversalSourceAmbientRoundtrip (W := W) A).obj X).carrier =
      X.carrier := by
  exact
    exactUniversalAmbientCanonicalSource_carrier
      (W := W) A X.carrier

/-- Source roundtrip preserves realized one-cells exactly. -/
@[simp] theorem exactUniversalSourceAmbientRoundtrip_map_lift
    {X Y : Source (W := W) A}
    (f : X ⟶ Y) :
    ((exactUniversalSourceAmbientRoundtrip (W := W) A).map f).lift =
      f.lift := by
  change
    ((exactUniversalAmbientCanonicalSectionPseudofunctor
      (W := W) A).map
        ((exactUniversalRealization (W := W) A).map f)).lift =
      f.lift
  rw [exactUniversalRealization_map,
    exactUniversalAmbientCanonicalSectionPseudofunctor_map_lift]

/-- Source roundtrip preserves realized two-cells exactly. -/
@[simp] theorem exactUniversalSourceAmbientRoundtrip_map₂_lift
    {X Y : Source (W := W) A}
    {f g : X ⟶ Y}
    (eta : f ⟶ g) :
    ((exactUniversalSourceAmbientRoundtrip (W := W) A).map₂ eta).lift =
      eta.lift := by
  change
    ((exactUniversalAmbientCanonicalSectionPseudofunctor
      (W := W) A).map₂
        ((exactUniversalRealization (W := W) A).map₂ eta)).lift =
      eta.lift
  rw [exactUniversalRealization_map₂,
    exactUniversalAmbientCanonicalSectionPseudofunctor_map₂_lift]

/-- The strict realization pseudofunctor has identity mapId comparison. -/
@[simp] theorem exactUniversalRealizationPseudofunctor_mapId_hom
    (X : Source (W := W) A) :
    ((exactUniversalRealization (W := W) A).toPseudofunctor.mapId X).hom =
      𝟙 (𝟙 X.carrier) := by
  rfl

/-- The strict realization pseudofunctor has identity mapComp comparison. -/
@[simp] theorem exactUniversalRealizationPseudofunctor_mapComp_hom
    {X Y Z : Source (W := W) A}
    (f : X ⟶ Y) (g : Y ⟶ Z) :
    ((exactUniversalRealization (W := W) A).toPseudofunctor.mapComp f g).hom =
      𝟙 (f.lift ≫ g.lift) := by
  rfl

/-- The source roundtrip identity comparison realizes to identity. -/
@[simp] theorem exactUniversalSourceAmbientRoundtrip_mapId_hom_lift
    (X : Source (W := W) A) :
    ((exactUniversalSourceAmbientRoundtrip (W := W) A).mapId X).hom.lift =
      𝟙 (𝟙 X.carrier) := by
  change
    (((exactUniversalAmbientCanonicalSectionPseudofunctor
        (W := W) A).map₂
          ((exactUniversalRealization (W := W) A).toPseudofunctor.mapId X).hom) ≫
      ((exactUniversalAmbientCanonicalSectionPseudofunctor
        (W := W) A).mapId X.carrier).hom).lift =
      𝟙 (𝟙 X.carrier)
  rw [exactUniversalSourceTwoCell_comp_lift,
    exactUniversalAmbientCanonicalSectionPseudofunctor_map₂_lift,
    exactUniversalRealizationPseudofunctor_mapId_hom]
  change
    (𝟙 (𝟙 X.carrier)) ≫
        (exactUniversalAmbientSectionIdIso (W := W) A X.carrier).hom.lift =
      𝟙 (𝟙 X.carrier)
  rw [exactUniversalAmbientSectionIdIso_hom_lift]
  exact Category.comp_id (𝟙 (𝟙 X.carrier))

/-- The source roundtrip composition comparison realizes to identity. -/
@[simp] theorem exactUniversalSourceAmbientRoundtrip_mapComp_hom_lift
    {X Y Z : Source (W := W) A}
    (f : X ⟶ Y) (g : Y ⟶ Z) :
    ((exactUniversalSourceAmbientRoundtrip (W := W) A).mapComp f g).hom.lift =
      𝟙 (f.lift ≫ g.lift) := by
  change
    (((exactUniversalAmbientCanonicalSectionPseudofunctor
        (W := W) A).map₂
          ((exactUniversalRealization (W := W) A).toPseudofunctor.mapComp
            f g).hom) ≫
      ((exactUniversalAmbientCanonicalSectionPseudofunctor
        (W := W) A).mapComp f.lift g.lift).hom).lift =
      𝟙 (f.lift ≫ g.lift)
  rw [exactUniversalSourceTwoCell_comp_lift,
    exactUniversalAmbientCanonicalSectionPseudofunctor_map₂_lift,
    exactUniversalRealizationPseudofunctor_mapComp_hom]
  change
    (𝟙 (f.lift ≫ g.lift)) ≫
        (exactUniversalAmbientSectionCompIso
          (W := W) A f.lift g.lift).hom.lift =
      𝟙 (f.lift ≫ g.lift)
  rw [exactUniversalAmbientSectionCompIso_hom_lift]
  exact Category.comp_id (𝟙 (f.lift ≫ g.lift))

/-- Unit component from an original source label to the canonical source label
chosen over the same ambient carrier. -/
noncomputable def exactUniversalSourceAmbientRoundtripUnitApp
    (X : Source (W := W) A) :
    X ⟶ (exactUniversalSourceAmbientRoundtrip (W := W) A).obj X := by
  change
    X ⟶ exactUniversalAmbientCanonicalSource (W := W) A X.carrier
  exact
    exactUniversalOneCellOfLift
      (W := W) A
      X
      (exactUniversalAmbientCanonicalSource (W := W) A X.carrier)
      (𝟙 X.carrier)

/-- The unit component realizes exactly to the ambient identity. -/
@[simp] theorem exactUniversalSourceAmbientRoundtripUnitApp_lift
    (X : Source (W := W) A) :
    (exactUniversalSourceAmbientRoundtripUnitApp (W := W) A X).lift =
      𝟙 X.carrier := by
  change
    (exactUniversalOneCellOfLift
      (W := W) A
      X
      (exactUniversalAmbientCanonicalSource (W := W) A X.carrier)
      (𝟙 X.carrier)).lift =
      𝟙 X.carrier
  exact
    exactUniversalOneCellOfLift_lift
      (W := W) A
      X
      (exactUniversalAmbientCanonicalSource (W := W) A X.carrier)
      (𝟙 X.carrier)

/-- Ambient comparison underlying the source-side unit naturality square. -/
noncomputable def exactUniversalSourceAmbientRoundtripNaturalityLiftIso
    {X Y : Source (W := W) A}
    (f : X ⟶ Y) :
    (f ≫ exactUniversalSourceAmbientRoundtripUnitApp (W := W) A Y).lift ≅
      (exactUniversalSourceAmbientRoundtripUnitApp (W := W) A X ≫
        (exactUniversalSourceAmbientRoundtrip (W := W) A).map f).lift := by
  change
    f.lift ≫ 𝟙 Y.carrier ≅
      𝟙 X.carrier ≫ f.lift
  exact
    (ρ_ f.lift) ≪≫ (λ_ f.lift).symm

@[simp] theorem exactUniversalSourceAmbientRoundtripNaturalityLiftIso_hom
    {X Y : Source (W := W) A}
    (f : X ⟶ Y) :
    (exactUniversalSourceAmbientRoundtripNaturalityLiftIso
      (W := W) A f).hom =
      (ρ_ f.lift).hom ≫ (λ_ f.lift).inv := by
  change
    ((ρ_ f.lift) ≪≫ (λ_ f.lift).symm).hom =
      (ρ_ f.lift).hom ≫ (λ_ f.lift).inv
  simp only [Iso.trans_hom, Iso.symm_hom]

/-- Lift the ambient unit square uniquely through full faithfulness of exact
realization. -/
noncomputable def exactUniversalSourceAmbientRoundtripNaturalityIso
    {X Y : Source (W := W) A}
    (f : X ⟶ Y) :
    f ≫ exactUniversalSourceAmbientRoundtripUnitApp (W := W) A Y ≅
      exactUniversalSourceAmbientRoundtripUnitApp (W := W) A X ≫
        (exactUniversalSourceAmbientRoundtrip (W := W) A).map f :=
  exactUniversalSourceIsoOfLift
    (W := W) A
    (exactUniversalSourceAmbientRoundtripNaturalityLiftIso
      (W := W) A f)

/-- Realization of the lifted unit square is the prescribed ambient square. -/
theorem exactUniversalSourceAmbientRoundtripNaturalityIso_realization
    {X Y : Source (W := W) A}
    (f : X ⟶ Y) :
    (exactUniversalCompletion2HomFunctor
      (W := W) A
      X
      ((exactUniversalSourceAmbientRoundtrip (W := W) A).obj Y)).mapIso
        (exactUniversalSourceAmbientRoundtripNaturalityIso
          (W := W) A f) =
      exactUniversalSourceAmbientRoundtripNaturalityLiftIso
        (W := W) A f := by
  apply Iso.ext
  exact
    (exactUniversalCompletion2HomFunctor
      (W := W) A
      X
      ((exactUniversalSourceAmbientRoundtrip (W := W) A).obj Y)).map_preimage
        (exactUniversalSourceAmbientRoundtripNaturalityLiftIso
          (W := W) A f).hom

/-- Hom projection of the source-side unit naturality square. -/
@[simp] theorem exactUniversalSourceAmbientRoundtripNaturalityIso_hom_lift
    {X Y : Source (W := W) A}
    (f : X ⟶ Y) :
    (exactUniversalSourceAmbientRoundtripNaturalityIso
      (W := W) A f).hom.lift =
      (ρ_ f.lift).hom ≫ (λ_ f.lift).inv := by
  have h :=
    congrArg Iso.hom
      (exactUniversalSourceAmbientRoundtripNaturalityIso_realization
        (W := W) A f)
  simpa only [Functor.mapIso_hom,
    exactUniversalCompletion2HomFunctor_map,
    exactUniversalSourceAmbientRoundtripNaturalityLiftIso_hom] using h

/-- Source-side native StrongTrans unit for the ambient canonical section. -/
noncomputable def exactUniversalSourceAmbientRoundtripUnit :
    Pseudofunctor.StrongTrans
      (Pseudofunctor.id (Source (W := W) A))
      (exactUniversalSourceAmbientRoundtrip (W := W) A) where
  app X :=
    exactUniversalSourceAmbientRoundtripUnitApp (W := W) A X
  naturality f :=
    exactUniversalSourceAmbientRoundtripNaturalityIso (W := W) A f
  naturality_naturality {a b} {f g} eta := by
    apply exactUniversalCompletion2_map_injective (W := W) A
    simp only [exactUniversalSourceTwoCell_comp_lift,
      exactUniversalRealization_source_whiskerRight_lift,
      exactUniversalSourceIdentityPseudofunctor_map₂_lift,
      exactUniversalSourceAmbientRoundtripNaturalityIso_hom_lift,
      exactUniversalRealization_source_whiskerLeft_lift,
      exactUniversalSourceAmbientRoundtrip_map₂_lift]
    bicategory
  naturality_id X := by
    apply exactUniversalCompletion2_map_injective (W := W) A
    simp only [exactUniversalSourceTwoCell_comp_lift,
      exactUniversalSourceAmbientRoundtripNaturalityIso_hom_lift,
      exactUniversalRealization_source_whiskerLeft_lift,
      exactUniversalSourceAmbientRoundtrip_mapId_hom_lift,
      exactUniversalSourceIdentityPseudofunctor_mapId_hom_lift,
      exactUniversalRealization_source_whiskerRight_lift,
      exactUniversalRealization_source_leftUnitor_lift,
      exactUniversalRealization_source_rightUnitor_inv_lift]
    bicategory
  naturality_comp {a b c} f g := by
    apply exactUniversalCompletion2_map_injective (W := W) A
    simp only [exactUniversalSourceTwoCell_comp_lift,
      exactUniversalSourceAmbientRoundtripNaturalityIso_hom_lift,
      exactUniversalRealization_source_whiskerLeft_lift,
      exactUniversalSourceAmbientRoundtrip_mapComp_hom_lift,
      exactUniversalSourceIdentityPseudofunctor_mapComp_hom_lift,
      exactUniversalRealization_source_whiskerRight_lift,
      exactUniversalRealization_source_associator_lift,
      exactUniversalRealization_source_associator_inv_lift]
    bicategory

@[simp] theorem exactUniversalSourceAmbientRoundtripUnit_app_lift
    (X : Source (W := W) A) :
    ((exactUniversalSourceAmbientRoundtripUnit (W := W) A).app X).lift =
      𝟙 X.carrier := by
  exact exactUniversalSourceAmbientRoundtripUnitApp_lift (W := W) A X

theorem exactUniversalSourceAmbientRoundtripUnit_naturality
    {X Y : Source (W := W) A}
    (f : X ⟶ Y) :
    (exactUniversalSourceAmbientRoundtripUnit
      (W := W) A).naturality f =
      exactUniversalSourceAmbientRoundtripNaturalityIso
        (W := W) A f := by
  rfl

/-! ## Regression checks -/

#print axioms exactUniversalSourceAmbientRoundtrip
#print axioms exactUniversalSourceAmbientRoundtrip_obj_carrier
#print axioms exactUniversalSourceAmbientRoundtrip_map_lift
#print axioms exactUniversalSourceAmbientRoundtrip_map₂_lift
#print axioms exactUniversalSourceAmbientRoundtrip_mapId_hom_lift
#print axioms exactUniversalSourceAmbientRoundtrip_mapComp_hom_lift
#print axioms exactUniversalSourceAmbientRoundtripUnitApp
#print axioms exactUniversalSourceAmbientRoundtripUnitApp_lift
#print axioms exactUniversalSourceAmbientRoundtripNaturalityLiftIso
#print axioms exactUniversalSourceAmbientRoundtripNaturalityIso
#print axioms exactUniversalSourceAmbientRoundtripNaturalityIso_realization
#print axioms exactUniversalSourceAmbientRoundtripNaturalityIso_hom_lift
#print axioms exactUniversalSourceAmbientRoundtripUnit
#print axioms exactUniversalSourceAmbientRoundtripUnit_app_lift
#print axioms exactUniversalSourceAmbientRoundtripUnit_naturality

end

end KUOS.DependentOriginationExactUniversalSourceAmbientRoundtripUnitV5_14
