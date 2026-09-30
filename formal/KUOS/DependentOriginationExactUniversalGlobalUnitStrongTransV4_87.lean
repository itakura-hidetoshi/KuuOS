import KUOS.DependentOriginationExactUniversalGlobalUnitSquaresV4_86

namespace KUOS.DependentOriginationExactUniversalGlobalUnitStrongTransV4_87

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalMappingTwoCellVerticalV4_59
open KUOS.DependentOriginationExactUniversalMappingHomCategoryV4_60
open KUOS.DependentOriginationExactUniversalMappingStructuralIsoV4_67
open KUOS.DependentOriginationExactUniversalRealizationStrictPseudofunctorV4_70
open KUOS.DependentOriginationExactUniversalRealizationFaithfulV4_76
open KUOS.DependentOriginationExactUniversalRealizationFullyFaithfulV4_77
open KUOS.DependentOriginationExactUniversalHomEquivalenceV4_83
open KUOS.DependentOriginationExactUniversalSectionPseudofunctorV4_84
open KUOS.DependentOriginationExactUniversalLabelledRealizationV4_85
open KUOS.DependentOriginationExactUniversalGlobalUnitSquaresV4_86

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Global source-roundtrip unit StrongTrans v4.87

v4.86 constructed the actual source roundtrip pseudofunctor and the naturality-
shaped isomorphism

  f ≫ 𝟙 Y ≅ 𝟙 X ≫ roundtrip.map f.

This file closes the next coherence layer: those object components and one-cell
squares are bundled into a native Mathlib `Pseudofunctor.StrongTrans`

  Id_Source ⟶ roundtrip.

The proof boundary is deliberately narrow.  The roundtrip structural cells are
first projected to DO₂.  The section comparison cells project to identities,
so naturality in 2-cells and compatibility with identity/composition reduce to
native bicategory unitor/associator coherence.  Faithfulness of exact
realization then reflects the resulting equalities back to the source.

This still does not assert ambient DO₂ object coverage, the realized-side global
counit, a final biequivalence, semantic admissibility equivalence, or
independently prescribed raw components.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

abbrev Source :=
  ExactUniversalRawObject.{u, v, uH, vH} (W := W) A

/-- The source roundtrip preserves the realized component of every 2-cell
exactly. -/
@[simp] theorem exactUniversalSourceRoundtrip_map₂_lift
    {X Y : Source (W := W) A} {f g : X ⟶ Y} (eta : f ⟶ g) :
    ((exactUniversalSourceRoundtrip (W := W) A).map₂ eta).lift = eta.lift := by
  rfl

/-- Vertical composition in a source hom category projects definitionally to
vertical composition in DO₂.  State this at the categorical-notation level so
it can rewrite goals before the underlying v4.59 `vcomp` constructor is
exposed. -/
@[simp] theorem exactUniversalSourceTwoCell_comp_lift
    {X Y : Source (W := W) A} {f g h : X ⟶ Y}
    (eta : f ⟶ g) (theta : g ⟶ h) :
    (eta ≫ theta).lift = eta.lift ≫ theta.lift := rfl

/-- The section pseudofunctor's identity comparison projects to the identity
DO₂ 2-cell.  This is a field-projection wrapper around the v4.84 theorem, so
later proofs need not unfold the whole pseudofunctor structure. -/
@[simp] theorem exactUniversalSectionPseudofunctor_mapId_hom_lift
    (X : ExactUniversalRealizedSector.{u, v, uH, vH} (W := W) A) :
    ((exactUniversalSectionPseudofunctor (W := W) A).mapId X).hom.lift =
      𝟙 (𝟙 X.carrier) :=
  exactUniversalSectionIdIso_hom_lift (W := W) A X

/-- The section pseudofunctor's composition comparison projects to identity. -/
@[simp] theorem exactUniversalSectionPseudofunctor_mapComp_hom_lift
    {X Y Z : ExactUniversalRealizedSector.{u, v, uH, vH} (W := W) A}
    (f : X ⟶ Y) (g : Y ⟶ Z) :
    ((exactUniversalSectionPseudofunctor (W := W) A).mapComp f g).hom.lift =
      𝟙 (f.hom ≫ g.hom) :=
  exactUniversalSectionCompIso_hom_lift
    (W := W) A X Y Z f.hom g.hom

/-- Strict labelled realization has identity structural cell on identities. -/
@[simp] theorem exactUniversalLabelledRealization_mapId_hom_hom
    (X : Source (W := W) A) :
    ((exactUniversalLabelledRealization (W := W) A).mapId X).hom.hom =
      𝟙 (𝟙 X.carrier) := by
  rfl

/-- Strict labelled realization has identity structural cell on composition. -/
@[simp] theorem exactUniversalLabelledRealization_mapComp_hom_hom
    {X Y Z : Source (W := W) A} (f : X ⟶ Y) (g : Y ⟶ Z) :
    ((exactUniversalLabelledRealization (W := W) A).mapComp f g).hom.hom =
      𝟙 (f.lift ≫ g.lift) := by
  rfl

/-- The identity pseudofunctor does not alter a realized 1-cell component. -/
@[simp] theorem exactUniversalSourceIdentityPseudofunctor_map_lift
    {X Y : Source (W := W) A} (f : X ⟶ Y) :
    ((Pseudofunctor.id (Source (W := W) A)).map f).lift = f.lift := by
  rfl

/-- The identity pseudofunctor does not alter a realized 2-cell component. -/
@[simp] theorem exactUniversalSourceIdentityPseudofunctor_map₂_lift
    {X Y : Source (W := W) A} {f g : X ⟶ Y} (eta : f ⟶ g) :
    ((Pseudofunctor.id (Source (W := W) A)).map₂ eta).lift = eta.lift := by
  rfl

/-- The identity pseudofunctor's identity comparison realizes to identity. -/
@[simp] theorem exactUniversalSourceIdentityPseudofunctor_mapId_hom_lift
    (X : Source (W := W) A) :
    ((Pseudofunctor.id (Source (W := W) A)).mapId X).hom.lift =
      𝟙 (𝟙 X.carrier) := by
  rfl

/-- The identity pseudofunctor's composition comparison realizes to identity. -/
@[simp] theorem exactUniversalSourceIdentityPseudofunctor_mapComp_hom_lift
    {X Y Z : Source (W := W) A} (f : X ⟶ Y) (g : Y ⟶ Z) :
    ((Pseudofunctor.id (Source (W := W) A)).mapComp f g).hom.lift =
      𝟙 (f.lift ≫ g.lift) := by
  rfl

/-- Source associator inverse realizes to the native DO₂ associator inverse. -/
@[simp] theorem exactUniversalRealization_source_associator_inv_lift
    {X Y Z T : Source (W := W) A}
    (f : X ⟶ Y) (g : Y ⟶ Z) (h : Z ⟶ T) :
    (α_ f g h).inv.lift = (α_ f.lift g.lift h.lift).inv := by
  apply Bicategory.InducedBicategory.hom₂_ext
  rfl

/-- The identity comparison of the source roundtrip realizes to the identity
2-cell on the DO₂ identity. -/
@[simp] theorem exactUniversalSourceRoundtrip_mapId_hom_lift
    (X : Source (W := W) A) :
    ((exactUniversalSourceRoundtrip (W := W) A).mapId X).hom.lift =
      𝟙 (𝟙 X.carrier) := by
  change
    (((exactUniversalSectionPseudofunctor (W := W) A).map₂
        ((exactUniversalLabelledRealization (W := W) A).toPseudofunctor.mapId X).hom) ≫
      ((exactUniversalSectionPseudofunctor (W := W) A).mapId X).hom).lift =
        𝟙 (𝟙 X.carrier)
  simp only [exactUniversalSourceTwoCell_comp_lift,
    exactUniversalSectionPseudofunctor_map₂_lift,
    exactUniversalLabelledRealization_mapId_hom_hom,
    exactUniversalSectionPseudofunctor_mapId_hom_lift,
    Category.comp_id]

/-- The composition comparison of the source roundtrip realizes to the identity
2-cell on the realized composite. -/
@[simp] theorem exactUniversalSourceRoundtrip_mapComp_hom_lift
    {X Y Z : Source (W := W) A} (f : X ⟶ Y) (g : Y ⟶ Z) :
    ((exactUniversalSourceRoundtrip (W := W) A).mapComp f g).hom.lift =
      𝟙 (f.lift ≫ g.lift) := by
  change
    (((exactUniversalSectionPseudofunctor (W := W) A).map₂
        ((exactUniversalLabelledRealization (W := W) A).toPseudofunctor.mapComp f g).hom) ≫
      ((exactUniversalSectionPseudofunctor (W := W) A).mapComp
        ((exactUniversalLabelledRealization (W := W) A).map f)
        ((exactUniversalLabelledRealization (W := W) A).map g)).hom).lift =
          𝟙 (f.lift ≫ g.lift)
  simp only [exactUniversalSourceTwoCell_comp_lift,
    exactUniversalSectionPseudofunctor_map₂_lift,
    exactUniversalLabelledRealization_mapComp_hom_hom,
    exactUniversalSectionPseudofunctor_mapComp_hom_lift,
    Category.comp_id]

/-- The v4.86 unit components and squares satisfy all three native StrongTrans
coherence laws. -/
def exactUniversalSourceRoundtripUnit :
    Pseudofunctor.StrongTrans
      (Pseudofunctor.id (Source (W := W) A))
      (exactUniversalSourceRoundtrip (W := W) A) where
  app X := 𝟙 X
  naturality f :=
    exactUniversalSourceRoundtripNaturalityIso (W := W) A f
  naturality_naturality {a b} {f g} eta := by
    apply exactUniversalCompletion2_map_injective (W := W) A
    simp only [exactUniversalSourceTwoCell_comp_lift,
      exactUniversalRealization_source_whiskerRight_lift,
      exactUniversalSourceIdentityPseudofunctor_map₂_lift,
      ExactUniversalRawMorphism.id_lift,
      exactUniversalSourceRoundtripNaturalityIso_hom_lift,
      exactUniversalRealization_source_whiskerLeft_lift,
      exactUniversalSourceRoundtrip_map₂_lift]
    bicategory
  naturality_id X := by
    apply exactUniversalCompletion2_map_injective (W := W) A
    simp only [exactUniversalSourceTwoCell_comp_lift,
      exactUniversalSourceRoundtripNaturalityIso_hom_lift,
      exactUniversalRealization_source_whiskerLeft_lift,
      exactUniversalSourceRoundtrip_mapId_hom_lift,
      exactUniversalSourceIdentityPseudofunctor_mapId_hom_lift,
      exactUniversalRealization_source_whiskerRight_lift,
      ExactUniversalRawMorphism.id_lift,
      exactUniversalRealization_source_leftUnitor_lift,
      exactUniversalRealization_source_rightUnitor_inv_lift]
    bicategory
  naturality_comp {a b c} f g := by
    apply exactUniversalCompletion2_map_injective (W := W) A
    simp only [exactUniversalSourceTwoCell_comp_lift,
      exactUniversalSourceRoundtripNaturalityIso_hom_lift,
      exactUniversalRealization_source_whiskerLeft_lift,
      exactUniversalSourceRoundtrip_mapComp_hom_lift,
      exactUniversalSourceIdentityPseudofunctor_mapComp_hom_lift,
      exactUniversalRealization_source_whiskerRight_lift,
      exactUniversalSourceIdentityPseudofunctor_map_lift,
      exactUniversalSourceRoundtrip_map_lift,
      ExactUniversalRawMorphism.id_lift,
      ExactUniversalRawMorphism.comp_lift,
      exactUniversalRealization_source_associator_lift,
      exactUniversalRealization_source_associator_inv_lift]
    bicategory

@[simp] theorem exactUniversalSourceRoundtripUnit_app
    (X : Source (W := W) A) :
    (exactUniversalSourceRoundtripUnit (W := W) A).app X = 𝟙 X := rfl

theorem exactUniversalSourceRoundtripUnit_naturality
    {X Y : Source (W := W) A} (f : X ⟶ Y) :
    (exactUniversalSourceRoundtripUnit (W := W) A).naturality f =
      exactUniversalSourceRoundtripNaturalityIso (W := W) A f := rfl

/-! ## Regression checks -/

variable {X Y : Source (W := W) A}

example :
    Pseudofunctor.StrongTrans
      (Pseudofunctor.id (Source (W := W) A))
      (exactUniversalSourceRoundtrip (W := W) A) :=
  exactUniversalSourceRoundtripUnit (W := W) A

example (f : X ⟶ Y) :
    ((exactUniversalSourceRoundtripUnit (W := W) A).naturality f).hom.lift =
      (ρ_ f.lift).hom ≫ (λ_ f.lift).inv :=
  exactUniversalSourceRoundtripNaturalityIso_hom_lift (W := W) A f

#print axioms exactUniversalSourceTwoCell_comp_lift
#print axioms exactUniversalSourceRoundtrip_map₂_lift
#print axioms exactUniversalSourceRoundtrip_mapId_hom_lift
#print axioms exactUniversalSourceRoundtrip_mapComp_hom_lift
#print axioms exactUniversalSourceRoundtripUnit
#print axioms exactUniversalSourceRoundtripUnit_app
#print axioms exactUniversalSourceRoundtripUnit_naturality

end

end KUOS.DependentOriginationExactUniversalGlobalUnitStrongTransV4_87
